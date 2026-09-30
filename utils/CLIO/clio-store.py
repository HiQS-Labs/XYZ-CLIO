#!/usr/bin/env python3
"""CLIO's local history store. Stdlib only; no network or background process."""
import argparse
import contextlib
import fcntl
import hashlib
import html
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
import uuid

APP_ID = 0x434C494F
VERSION = 1
FIELDS = ('timestamp', 'repo', 'branch', 'machine', 'agent', 'session_id',
          'prompt', 'checkout', 'repo_slug')
RESERVED = set(FIELDS) | {'record_id', 'legacy_id', 'origin_id', 'origin_kind',
                          'references', 'extras', 'clio_version'}
CONFIG = Path(os.environ.get('CLIO_CONFIG', str(Path.home() / '.claude/clio-storage.json')))


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def instant(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timestamp must include a timezone')
    return parsed.astimezone(timezone.utc)


def utc(value=None):
    value = value or datetime.now(timezone.utc)
    return value.isoformat(timespec='microseconds').replace('+00:00', 'Z')


def atomic(path, data):
    """One-file publication; never expose an incomplete replacement."""
    path = Path(path).expanduser().absolute()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def diagnostic(message):
    # Callers pass content-free descriptions, never input or SQL parameter values.
    path = Path.home() / '.claude/prompt-log-errors.log'
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with path.open('a') as stream:
        stream.write(utc() + ' clio-store: ' + message + '\n')


def config():
    if not CONFIG.exists():
        return {}
    value = json.loads(CONFIG.read_text())
    if not isinstance(value, dict) or not value.get('db') or not value.get('owner'):
        raise ValueError('invalid storage configuration')
    return value


def database(path, writable=False):
    path = Path(path).expanduser().absolute()
    mode = 'rw' if writable else 'ro'
    conn = sqlite3.connect('file:' + quote(str(path), safe='/') + '?mode=' + mode,
                           uri=True, timeout=0.5)
    conn.row_factory = sqlite3.Row
    try:
        if conn.execute('PRAGMA application_id').fetchone()[0] != APP_ID:
            raise ValueError('not a CLIO database')
        if conn.execute('PRAGMA user_version').fetchone()[0] != VERSION:
            raise ValueError('unsupported CLIO schema version')
        if not writable:
            conn.execute('PRAGMA query_only=ON')
        return conn
    except Exception:
        conn.close()
        raise


def initialize(path):
    path = Path(path).expanduser().absolute()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.exists():
        with contextlib.closing(database(path)) as conn:
            return conn.execute('SELECT owner FROM metadata').fetchone()[0]
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    owner = str(uuid.uuid4())
    with contextlib.closing(sqlite3.connect(path, timeout=0.5)) as conn:
        conn.executescript('''
            PRAGMA journal_mode=WAL;
            BEGIN IMMEDIATE;
            CREATE TABLE metadata(owner TEXT NOT NULL);
            CREATE TABLE events(
                record_id TEXT PRIMARY KEY, timestamp TEXT NOT NULL,
                repo TEXT, machine TEXT, agent TEXT, session_id TEXT,
                repo_slug TEXT, origin_id TEXT NOT NULL, payload TEXT NOT NULL);
            CREATE INDEX event_time ON events(timestamp,record_id);
            CREATE INDEX event_repo ON events(repo,timestamp,record_id);
            CREATE INDEX event_machine ON events(machine,timestamp,record_id);
            CREATE INDEX event_agent ON events(agent,timestamp,record_id);
            CREATE INDEX event_session ON events(session_id,timestamp,record_id);
            CREATE INDEX event_slug ON events(repo_slug,timestamp,record_id);
            CREATE INDEX event_origin ON events(origin_id,timestamp,record_id);
            CREATE TABLE device_imports(
                owner TEXT NOT NULL, digest TEXT NOT NULL, generated_at TEXT NOT NULL,
                source TEXT NOT NULL, rows INTEGER NOT NULL, received_at TEXT NOT NULL,
                PRIMARY KEY(owner,digest));
            CREATE TABLE sources(
                source TEXT PRIMARY KEY, path TEXT NOT NULL, inode TEXT NOT NULL,
                origin_id TEXT NOT NULL, offset INTEGER NOT NULL DEFAULT 0,
                lines INTEGER NOT NULL DEFAULT 0, prefix_hash TEXT NOT NULL);
            CREATE TABLE source_lines(
                source TEXT NOT NULL, line INTEGER NOT NULL, raw_hash TEXT NOT NULL,
                record_id TEXT, reason TEXT, quarantine BLOB,
                PRIMARY KEY(source,line));
        ''')
        conn.execute('INSERT INTO metadata VALUES (?)', (owner,))
        conn.execute('PRAGMA application_id=' + str(APP_ID))
        conn.execute('PRAGMA user_version=' + str(VERSION))
        conn.commit()
    return owner


def normalize(row, owner=None, kind='legacy-adopted'):
    if not isinstance(row, dict):
        raise ValueError('record must be an object')
    versioned = row.get('clio_version') == VERSION
    if not versioned and {'record_id', 'legacy_id', 'origin_id', 'origin_kind'}.intersection(row):
        raise ValueError('identity fields require a versioned record')
    if 'clio_version' in row and not versioned:
        raise ValueError('unsupported record version')
    result = {}
    for field in FIELDS:
        value = row.get(field, '')
        value = '' if value is None else value
        if not isinstance(value, str):
            raise ValueError('invalid field type')
        result[field] = value
    if not result['prompt'].strip():
        raise ValueError('empty prompt')
    result['timestamp'] = utc(instant(result['timestamp']))
    result['origin_id'] = row.get('origin_id') if versioned else owner
    result['origin_kind'] = row.get('origin_kind') if versioned else kind
    if not isinstance(result['origin_id'], str) or not result['origin_id']:
        raise ValueError('missing origin identity')
    if result['origin_kind'] not in ('captured', 'legacy-adopted'):
        raise ValueError('invalid origin kind')
    extras = row.get('extras', {})
    if not isinstance(extras, dict) or RESERVED.intersection(extras):
        raise ValueError('extras shadow reserved fields')
    extras = dict(extras)
    for key, value in row.items():
        if key not in RESERVED:
            if key in extras and extras[key] != value:
                raise ValueError('conflicting extra metadata')
            extras[key] = value
    references = row.get('references', [])
    if not isinstance(references, list):
        raise ValueError('references must be a list')
    import re
    for ref in references:
        if not isinstance(ref, dict) or ref.get('relation') not in ('mentioned', 'task-context'):
            raise ValueError('invalid reference relation')
        if ref.get('type') in ('issue', 'pr'):
            segment = 'issues' if ref['type'] == 'issue' else 'pull'
            if not re.fullmatch(r'https://github\.com/[\w.-]+/[\w.-]+/' + segment + r'/[1-9][0-9]*', ref.get('url', '')):
                raise ValueError('reference requires a qualified GitHub URL')
        elif ref.get('type') == 'ledger':
            if not re.fullmatch(r'[\w.-]+/[\w.-]+', ref.get('repo_slug', '')) or not isinstance(ref.get('row_id'), str) or not ref['row_id']:
                raise ValueError('ledger reference requires repository and row identity')
        else:
            raise ValueError('invalid reference type')
    result.update(extras=extras, references=references, clio_version=VERSION)
    record_id = 'clio1-' + digest(encode(result).encode())
    if versioned and row.get('record_id') != record_id:
        raise ValueError('record identity does not match payload')
    result['record_id'] = record_id
    result['legacy_id'] = result['session_id'] + ':' + result['timestamp'].replace('.000000Z', 'Z')
    return result


def insert(conn, row):
    """The only event writer, shared by import, capture and recovery."""
    payload = encode(row)
    prior = conn.execute('SELECT payload FROM events WHERE record_id=?', (row['record_id'],)).fetchone()
    if prior:
        if prior[0] != payload:
            raise ValueError('identity payload conflict')
        return False
    conn.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?)',
                 tuple(row[k] for k in ('record_id', 'timestamp', 'repo', 'machine',
                       'agent', 'session_id', 'repo_slug', 'origin_id')) + (payload,))
    return True


def pending_dir(path):
    path = Path(path).expanduser().absolute()
    return path.with_name(path.name + '.pending')


def capture(path, owner, value):
    row = normalize(value, owner, 'captured')
    pending = pending_dir(path) / (row['record_id'] + '.json')
    atomic(pending, encode(row).encode())
    try:
        with contextlib.closing(database(path, True)) as conn, conn:
            conn.execute('BEGIN IMMEDIATE')
            insert(conn, row)
        pending.unlink(missing_ok=True)
        return {'record_id': row['record_id'], 'state': 'committed'}
    except (sqlite3.Error, OSError, ValueError):
        diagnostic('capture queued durably; run drain or the scheduled SQLite exporter')
        return {'record_id': row['record_id'], 'state': 'pending'}


@contextlib.contextmanager
def lock(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with path.open('a') as stream:
        deadline = time.monotonic() + 0.5
        while True:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise TimeoutError('maintenance lock busy')
                time.sleep(0.01)
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def drain(path, limit=100):
    folder = pending_dir(path)
    if not folder.exists():
        return {'drained': 0, 'pending': 0}
    count = 0
    with lock(folder / '.drain.lock'):
        for source in sorted(folder.glob('clio1-*.json'))[:limit]:
            row = normalize(json.loads(source.read_text()))
            with contextlib.closing(database(path, True)) as conn, conn:
                conn.execute('BEGIN IMMEDIATE')
                insert(conn, row)
            source.unlink(missing_ok=True)
            count += 1
    return {'drained': count, 'pending': len(list(folder.glob('clio1-*.json')))}


def check_deadline(deadline):
    if deadline is not None and time.monotonic() >= deadline:
        raise TimeoutError('cutover budget exceeded; retain legacy mode and retry offline')


def import_jsonl(path, source_path, source_id=None, max_records=1000, deadline=None):
    source_path = Path(source_path).expanduser().resolve()
    source_id = source_id or str(source_path)
    with source_path.open('rb') as stream, contextlib.closing(database(path, True)) as conn:
        stat = os.fstat(stream.fileno())
        inode = str(stat.st_dev) + ':' + str(stat.st_ino)
        owner = conn.execute('SELECT owner FROM metadata').fetchone()[0]
        with conn:
            conn.execute('BEGIN IMMEDIATE')
            prior = conn.execute('SELECT * FROM sources WHERE source=?', (source_id,)).fetchone()
            if prior and (prior['path'] != str(source_path) or prior['inode'] != inode):
                raise ValueError('source replaced; use an explicit new --source identity')
            offset, number = (prior['offset'], prior['lines']) if prior else (0, 0)
            prefix = hashlib.sha256()
            remaining = offset
            while remaining:
                check_deadline(deadline)
                block = stream.read(min(remaining, 1024 * 1024))
                if not block:
                    raise ValueError('source shrank')
                prefix.update(block)
                remaining -= len(block)
            if prior and prefix.hexdigest() != prior['prefix_hash']:
                raise ValueError('source prefix changed')
            if not prior:
                conn.execute('INSERT INTO sources VALUES (?,?,?,?,?,?,?)',
                             (source_id, str(source_path), inode, owner, 0, 0, prefix.hexdigest()))
            else:
                owner = prior['origin_id']
            added = duplicates = rejected = 0
            for _ in range(max_records):
                check_deadline(deadline)
                raw = stream.readline()
                if not raw or not raw.endswith(b'\n'):
                    break
                number += 1
                row, reason = None, None
                try:
                    row = normalize(json.loads(raw), owner)
                except (ValueError, TypeError, KeyError, AttributeError, OverflowError):
                    reason = 'invalid JSON or record fields'
                if row:
                    if insert(conn, row):
                        added += 1
                    else:
                        duplicates += 1
                else:
                    rejected += 1
                conn.execute('INSERT INTO source_lines VALUES (?,?,?,?,?,?)',
                             (source_id, number, digest(raw), row['record_id'] if row else None,
                              reason, raw if reason else None))
                prefix.update(raw)
                offset += len(raw)
            conn.execute('UPDATE sources SET offset=?,lines=?,prefix_hash=? WHERE source=?',
                         (offset, number, prefix.hexdigest(), source_id))
        return {'source': source_id, 'added': added, 'duplicates': duplicates,
                'quarantined': rejected, 'lines': number, 'offset': offset,
                'remaining_bytes': os.fstat(stream.fileno()).st_size - offset}


def verify_import(path, source_id, deadline=None):
    with contextlib.closing(database(path)) as conn:
        conn.execute('BEGIN')
        source = conn.execute('SELECT * FROM sources WHERE source=?', (source_id,)).fetchone()
        if source is None:
            source_id = str(Path(source_id).expanduser().resolve())
            source = conn.execute('SELECT * FROM sources WHERE source=?', (source_id,)).fetchone()
        if not source or not source['lines']:
            raise ValueError('no nonempty imported source to verify')
        with Path(source['path']).open('rb') as stream:
            stat = os.fstat(stream.fileno())
            if source['inode'] != str(stat.st_dev) + ':' + str(stat.st_ino):
                raise ValueError('source replaced')
            prefix = hashlib.sha256()
            count = quarantined = 0
            for evidence in conn.execute('SELECT * FROM source_lines WHERE source=? ORDER BY line', (source_id,)):
                check_deadline(deadline)
                raw = stream.readline()
                count += 1
                if not raw.endswith(b'\n') or digest(raw) != evidence['raw_hash']:
                    raise ValueError('source occurrence mismatch')
                prefix.update(raw)
                if evidence['record_id']:
                    expected = normalize(json.loads(raw), source['origin_id'])
                    stored = conn.execute('SELECT payload FROM events WHERE record_id=?',
                                          (evidence['record_id'],)).fetchone()
                    if not stored or encode(expected) != stored[0]:
                        raise ValueError('missing or corrupt imported event')
                else:
                    if raw != evidence['quarantine']:
                        raise ValueError('quarantine mismatch')
                    quarantined += 1
            if count != source['lines'] or prefix.hexdigest() != source['prefix_hash'] or stream.tell() != source['offset']:
                raise ValueError('source accounting mismatch')
            pending = stat.st_size - stream.tell()
            if pending:
                raise ValueError('source still has unaccounted bytes')
        return {'verified': True, 'source': source_id, 'occurrences': count,
                'quarantined': quarantined, 'prefix_hash': prefix.hexdigest()}


def activate(path, source_path, fresh=False):
    """Explicit pilot operation. Does not install hooks or schedule jobs."""
    if CONFIG.exists():
        raise ValueError('already activated; preserve configuration for rollback')
    writer = Path.home() / '.claude/hooks/clio-capture.sh'
    helper = writer.with_name('clio-store.py')
    if not writer.exists() or 'CLIO_SQLITE_V1' not in writer.read_text() or not helper.exists():
        raise ValueError('install the SQLite-aware shared writer and helper first')
    with contextlib.closing(database(path)) as conn:
        owner = conn.execute('SELECT owner FROM metadata').fetchone()[0]
        if conn.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('database integrity check failed')
    append_lock = Path.home() / '.claude/prompt-log.lock'
    append_lock.mkdir()  # Refuse busy/stale locks; never remove another writer's lock.
    try:
        deadline = time.monotonic() + 5
        (append_lock / 'born').write_text(str(int(time.time())))
        source_path = Path(source_path).expanduser().resolve()
        if fresh:
            if source_path.exists():
                raise ValueError('fresh activation requires no legacy source')
        else:
            result = import_jsonl(path, source_path, max_records=100, deadline=deadline)
            if result['remaining_bytes']:
                raise ValueError('backlog remains; run online import before activation')
            verify_import(path, str(source_path), deadline=deadline)
            backup = source_path.with_name(source_path.name + '.pre-sqlite-' + str(time.time_ns()))
            with source_path.open('rb') as src, backup.open('xb') as dst:
                while block := src.read(1024 * 1024):
                    check_deadline(deadline)
                    dst.write(block)
                dst.flush()
                os.fsync(dst.fileno())
        check_deadline(deadline)
        atomic(CONFIG, (encode({'db': str(Path(path).expanduser().absolute()), 'owner': owner}) + '\n').encode())
    finally:
        (append_lock / 'born').unlink(missing_ok=True)
        append_lock.rmdir()
    return {'activated': True, 'config': str(CONFIG), 'owner': owner}


def query(path, args):
    conditions, values = [], []
    for key, column in [('repo', 'repo'), ('device', 'machine'), ('agent', 'agent'),
                        ('session', 'session_id'), ('record_id', 'record_id'),
                        ('repo_slug', 'repo_slug'), ('origin', 'origin_id')]:
        value = getattr(args, key, None)
        if value is not None:
            conditions.append(column + '=?')
            values.append(value)
    for key, operation in [('since', '>='), ('until', '<=')]:
        value = getattr(args, key, None)
        if value:
            conditions.append('timestamp' + operation + '?')
            values.append(utc(instant(value)))
    if args.text is not None:
        conditions.append("instr(json_extract(payload,'$.prompt'),?)>0")
        values.append(args.text)
    if args.reference:
        conditions.append("EXISTS (SELECT 1 FROM json_each(events.payload,'$.references') r WHERE json_extract(r.value,'$.url')=? OR (json_extract(r.value,'$.repo_slug')||':'||json_extract(r.value,'$.row_id'))=?)")
        values.extend([args.reference, args.reference])
    sql = 'SELECT payload FROM events' + (' WHERE ' + ' AND '.join(conditions) if conditions else '')
    sql += ' ORDER BY timestamp DESC,record_id DESC LIMIT ? OFFSET ?'
    values.extend([args.limit, args.offset])
    with contextlib.closing(database(path)) as conn:
        rows = [json.loads(row[0]) for row in conn.execute(sql, values)]
        plan = [list(row) for row in conn.execute('EXPLAIN QUERY PLAN ' + sql, values)] if args.explain else None
    result = {'records': rows, 'limit': args.limit, 'offset': args.offset,
              'pending': len(list(pending_dir(path).glob('clio1-*.json')))}
    if plan is not None:
        result['query_plan'] = plan
    return result


def safe_output(conn, path, output):
    target = Path(output).expanduser().resolve()
    forbidden = {Path(path).expanduser().resolve(), CONFIG.resolve()}
    forbidden.update(Path(row[0]).resolve() for row in conn.execute('SELECT path FROM sources'))
    forbidden.update(Path(row[0]).resolve() for row in conn.execute('SELECT source FROM device_imports'))
    forbidden.add((Path.home() / '.claude/prompt-log.jsonl').resolve())
    base = Path(path).expanduser().resolve()
    forbidden.update(Path(str(base) + suffix) for suffix in ('-wal', '-shm', '.project.lock'))
    if target in forbidden or target == pending_dir(path).resolve() or pending_dir(path).resolve() in target.parents:
        raise ValueError('output would overwrite storage, configuration or source history')
    return target


def project(path, markdown, jsonl=None, cutoff=None):
    cutoff_dt = instant(cutoff) if cutoff else datetime.now(timezone.utc)
    cutoff_text, since = utc(cutoff_dt), utc(cutoff_dt - timedelta(hours=168))
    with lock(str(Path(path).expanduser().absolute()) + '.project.lock'):
        with contextlib.closing(database(path)) as conn:
            conn.execute('BEGIN')
            target = safe_output(conn, path, markdown)
            if target == (Path.home() / '.claude/prompt-log.md').resolve():
                raise ValueError('use a separate recent view; preserve the legacy shared Markdown')
            if target.exists() and '<!-- CLIO:ENTRIES -->' in target.read_text():
                raise ValueError('preserve the historical shared Markdown; choose a new output')
            all_rows = [json.loads(row[0]) for row in conn.execute('SELECT payload FROM events ORDER BY timestamp,record_id')]
            recent = [row for row in reversed(all_rows) if since <= row['timestamp'] <= cutoff_text]
            lines = ['# CLIO — recent 168 hours', '', 'UTC cutoff: ' + cutoff_text,
                     'Window starts: ' + since, 'Records: ' + str(len(recent)),
                     'Older history remains in SQLite. This view covers imported/local records only.', '']
            if not recent:
                lines.extend(['No prompts in this window.', ''])
            for row in recent:
                esc = lambda value: html.escape(value or 'unknown', quote=False)
                lines.extend(['<!-- clio:record:' + row['record_id'] + ' -->',
                              '## ' + esc(row['repo']), row['timestamp'] + ' (UTC)',
                              ' · '.join(esc(row[key]) for key in ('machine', 'branch', 'agent')),
                              'Session: ' + esc(row['session_id']),
                              'Checkout: ' + esc(row['checkout']),
                              'Repository: ' + esc(row['repo_slug']),
                              'Origin: ' + esc(row['origin_id']) + ' (' + row['origin_kind'] + ')',
                              'Record: ' + row['record_id'], ''])
                lines.extend('> ' + html.escape(line, quote=False) for line in row['prompt'].split('\n'))
                if row['extras']:
                    lines.extend(['', 'Metadata: ' + html.escape(encode(row['extras']), quote=False)])
                if row['references']:
                    lines.extend(['', 'References: ' + html.escape(encode(row['references']), quote=False)])
                lines.append('')
            data = ('\n'.join(lines) + '\n').encode()
            compat = safe_output(conn, path, jsonl) if jsonl else None
            if compat == target:
                raise ValueError('Markdown and JSONL outputs must differ')
            if compat:
                # Legacy Rebalance derives IDs from the timestamp text; keep UTC-second
                # spelling where exact seconds were originally captured.
                compatibility = [dict(row, timestamp=row['timestamp'].replace('.000000Z', 'Z')) for row in all_rows]
                atomic(compat, ''.join(encode(row) + '\n' for row in compatibility).encode())
            atomic(target, data)
    return {'markdown': str(target), 'rows': len(recent), 'bytes': len(data),
            'cutoff': cutoff_text, 'history_rows': len(all_rows)}


def export_device(path, output, cutoff=None):
    with lock(str(Path(path).expanduser().absolute()) + '.project.lock'):
        with contextlib.closing(database(path)) as conn:
            conn.execute('BEGIN')
            owner = conn.execute('SELECT owner FROM metadata').fetchone()[0]
            target = safe_output(conn, path, output)
            rows = [row[0] for row in conn.execute('SELECT payload FROM events WHERE origin_id=? ORDER BY timestamp,record_id', (owner,))]
            payload = ''.join(row + '\n' for row in rows).encode()
            manifest = {'clio_snapshot': VERSION, 'owner': owner, 'generated_at': utc(instant(cutoff)) if cutoff else utc(),
                        'rows': len(rows), 'sha256': digest(payload)}
            atomic(target, (encode(manifest) + '\n').encode() + payload)
        return manifest

def import_device(path, source):
    with Path(source).open('rb') as stream:
        manifest = json.loads(stream.readline())
        payload = stream.read()
    if manifest.get('clio_snapshot') != VERSION or digest(payload) != manifest.get('sha256'):
        raise ValueError('invalid snapshot version or digest')
    instant(manifest['generated_at'])
    raw_rows = payload.splitlines()
    if len(raw_rows) != manifest.get('rows'):
        raise ValueError('snapshot row count mismatch')
    added = 0
    with contextlib.closing(database(path, True)) as conn, conn:
        conn.execute('BEGIN IMMEDIATE')
        for raw in raw_rows:
            row = normalize(json.loads(raw))
            if row['origin_id'] != manifest['owner']:
                raise ValueError('snapshot contains a foreign-owned record')
            added += insert(conn, row)
        conn.execute('INSERT OR IGNORE INTO device_imports VALUES (?,?,?,?,?,?)',
                     (manifest['owner'], manifest['sha256'], manifest['generated_at'],
                      str(Path(source).resolve()), len(raw_rows), utc()))
    return {'added': added, 'rows': len(raw_rows), 'owner': manifest['owner'],
            'generated_at': manifest['generated_at']}


def backup(path, output):
    output = Path(output).expanduser().absolute()
    # Never replace an existing backup or source.
    fd = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    with contextlib.closing(database(path)) as source, contextlib.closing(sqlite3.connect(output)) as target:
        source.backup(target)
    return {'backup': str(output)}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', help='default: activated DB, otherwise ~/.claude/prompt-log.sqlite3')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('init')
    imp = commands.add_parser('import-jsonl')
    imp.add_argument('input')
    imp.add_argument('--source')
    imp.add_argument('--max-records', type=int, default=1000)
    verify = commands.add_parser('verify-import')
    verify.add_argument('source')
    activation = commands.add_parser('activate')
    activation.add_argument('--source', default=str(Path.home() / '.claude/prompt-log.jsonl'))
    activation.add_argument('--fresh', action='store_true')
    commands.add_parser('capture')
    recovery = commands.add_parser('drain')
    recovery.add_argument('--limit', type=int, default=100)
    reader = commands.add_parser('query')
    for flag in ('repo', 'device', 'agent', 'session', 'record-id', 'repo-slug', 'origin', 'since', 'until', 'text', 'reference'):
        reader.add_argument('--' + flag)
    reader.add_argument('--limit', type=int, default=20)
    reader.add_argument('--offset', type=int, default=0)
    reader.add_argument('--explain', action='store_true')
    projection = commands.add_parser('project')
    projection.add_argument('--markdown', default=str(Path.home() / '.claude/prompt-log-recent.md'))
    projection.add_argument('--jsonl')
    projection.add_argument('--cutoff')
    exporter = commands.add_parser('export-device')
    exporter.add_argument('output')
    exporter.add_argument('--cutoff')
    importer = commands.add_parser('import-device')
    importer.add_argument('input')
    copier = commands.add_parser('backup')
    copier.add_argument('output')
    args = parser.parse_args()
    try:
        cfg = {} if args.db and args.command != 'capture' else config()
        path = args.db or cfg.get('db') or str(Path.home() / '.claude/prompt-log.sqlite3')
        if hasattr(args, 'limit') and not 1 <= args.limit <= 1000:
            raise ValueError('limit must be between 1 and 1000')
        if getattr(args, 'offset', 0) < 0 or getattr(args, 'max_records', 1) < 1:
            raise ValueError('invalid pagination or import bound')
        if args.command == 'init':
            result = {'owner': initialize(path), 'db': str(Path(path).expanduser().absolute())}
        elif args.command == 'import-jsonl':
            result = import_jsonl(path, args.input, args.source, args.max_records)
        elif args.command == 'verify-import':
            result = verify_import(path, args.source)
        elif args.command == 'activate':
            result = activate(path, args.source, args.fresh)
        elif args.command == 'capture':
            if not cfg or Path(cfg['db']).resolve() != Path(path).expanduser().resolve():
                raise ValueError('capture requires the activated database')
            result = capture(path, cfg['owner'], json.load(sys.stdin))
        elif args.command == 'drain':
            result = drain(path, args.limit)
        elif args.command == 'query':
            result = query(path, args)
        elif args.command == 'project':
            result = project(path, args.markdown, args.jsonl, args.cutoff)
        elif args.command == 'export-device':
            result = export_device(path, args.output, args.cutoff)
        elif args.command == 'import-device':
            result = import_device(path, args.input)
        else:
            result = backup(path, args.output)
        print(encode(result))
        return 0
    except (ValueError, TypeError, KeyError, AttributeError, OverflowError, OSError, sqlite3.Error) as error:
        # No raw input/parameters in diagnostics; private quarantine holds rejected source data.
        message = type(error).__name__ + ': ' + (str(error) if isinstance(error, (ValueError, sqlite3.Error)) else 'operation failed; source and pending receipts retained')
        print(message, file=sys.stderr)
        try:
            if args.command not in ('query', 'verify-import'):
                diagnostic(args.command + ': ' + message)
        except OSError:
            pass
        return 3


if __name__ == '__main__':
    sys.exit(main())
