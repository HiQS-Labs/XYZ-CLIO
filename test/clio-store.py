#!/usr/bin/env python3
"""SQLite acceptance cases using only synthetic data and temporary homes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('clio_store', ROOT / 'utils/CLIO/clio-store.py')
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)


class History(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='clio-sqlite-')
        self.home = Path(self.tmp.name)
        self.environment = patch.dict(os.environ, {'HOME': str(self.home), 'CLIO_MIN_PROMPT_CHARS': '0'})
        self.environment.start()
        self.config = patch.object(store, 'CONFIG', self.home / '.claude/clio-storage.json')
        self.config.start()
        self.db = self.home / 'history.sqlite3'
        self.owner = store.initialize(self.db)
        self.counter = 0
        self.install()

    def tearDown(self):
        self.config.stop()
        self.environment.stop()
        self.tmp.cleanup()

    def install(self):
        hooks = self.home / '.claude/hooks'
        hooks.mkdir(parents=True)
        source = (ROOT / 'utils/CLIO/INSTALL.md').read_text(encoding='utf-8')
        for name in ('clio-capture.sh', 'log-prompt.sh'):
            marker = 'cat > ~/.claude/hooks/' + name + " << 'EOF'\n"
            body = source.split(marker, 1)[1].split('\nEOF\n', 1)[0] + '\n'
            (hooks / name).write_text(body, encoding='utf-8')
            (hooks / name).chmod(0o755)
        shutil.copyfile(ROOT / 'utils/CLIO/clio-store.py', hooks / 'clio-store.py')
        shutil.copyfile(ROOT / 'utils/CLIO/prompt-log-to-md.sh', hooks / 'prompt-log-to-md.sh')
        (hooks / 'prompt-log-to-md.sh').chmod(0o755)

    def activate(self):
        store.activate(self.db, self.home / '.claude/prompt-log.jsonl', fresh=True)

    def row(self, **changes):
        self.counter += 1
        row = {'timestamp': '2026-09-29T12:00:00Z', 'session_id': 's' + str(self.counter),
               'prompt': 'Synthetic multiline prompt\nUnicode: café — 日本語', 'machine': 'fixture-mbp14',
               'repo': 'rebalanceOS', 'agent': 'codex', 'branch': 'main'}
        row.update(changes)
        return row

    def add(self, row):
        return store.capture(self.db, self.owner, row)

    def rows(self, **changes):
        args = argparse.Namespace(repo=None, device=None, agent=None, session=None, record_id=None,
                                  repo_slug=None, origin=None, since=None, until=None, text=None,
                                  reference=None, limit=1000, offset=0, explain=False)
        vars(args).update(changes)
        return store.query(self.db, args)['records']

    def source(self, rows, name='legacy.jsonl'):
        path = self.home / name
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows))
        return path

    def note_and_job(self, rows, default=False):
        note = self.home / ('.claude/prompt-log.md' if default else 'vault/0. Claude Prompts.md')
        note.parent.mkdir(parents=True, exist_ok=True)
        header = '---\ntags: [work]\n---\n# My prompt history\nKeep [[My Project]] and café.\n<!-- CLIO:ENTRIES -->\n'
        body = ''
        for row in rows:
            context = row['machine'] + (' · ' + row['branch'] if row['branch'] else '')
            context += ' · ' + (row['agent'] or 'claude-code')
            body += ('\n<!-- clio:id:' + row['session_id'] + ':' + row['timestamp'].replace('.000000Z', 'Z')
                     + ' -->\n## ' + row['repo'].upper() + '\n' + row['timestamp'] + '  \n' + context
                     + '\n\n> "' + row['prompt'].replace('\n', '\n> ') + '"\n')
        note.write_text(header + body, encoding='utf-8')
        exporter = self.home / '.claude/hooks/prompt-log-to-md.sh'
        job = self.home / 'Library/LaunchAgents/com.claude.prompt-log-to-md.plist'
        job.parent.mkdir(parents=True, exist_ok=True)
        args = [str(exporter)] + ([] if default else [str(note)])
        job.write_bytes(plistlib.dumps({'Label': 'com.claude.prompt-log-to-md',
                                      'ProgramArguments': args, 'StartInterval': 60,
                                      'RunAtLoad': True, 'StandardErrorPath': '/fixture/error.log'}))
        return note, job, header

    def test_existing_schedule_reuses_obsidian_path(self):
        self.activate()
        now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        local = self.row(timestamp=now, prompt='Current local prompt')
        old = self.row(timestamp='2000-01-01T00:00:00Z', prompt='Obsolete history outside window')
        foreign = self.row(timestamp=now, machine='fixture-mini', prompt='Current foreign prompt')
        self.add(local)
        self.add(old)
        other = self.home / 'other.sqlite3'
        owner = store.initialize(other)
        store.capture(other, owner, foreign)
        snapshot = self.home / 'other.jsonl'
        store.export_device(other, snapshot)
        store.import_device(self.db, snapshot)
        note, job, header = self.note_and_job([local, foreign, old])
        original, job_bytes = note.read_bytes(), job.read_bytes()
        result = store.migrate_view(self.db, publishers_paused=True)
        self.assertEqual(result['covered_entries'], 3)
        self.assertEqual(note.read_bytes(), original)
        self.assertEqual(Path(result['backup']).read_bytes(), original)
        command = plistlib.loads(job_bytes)['ProgramArguments']
        subprocess.run(command, check=True, capture_output=True)
        self.assertEqual(job.read_bytes(), job_bytes)
        self.assertTrue(note.read_text(encoding='utf-8').startswith(header))
        self.assertIn('Current local prompt', note.read_text(encoding='utf-8'))
        self.assertIn('Current foreign prompt', note.read_text(encoding='utf-8'))
        self.assertNotIn('Obsolete history outside window', note.read_text(encoding='utf-8'))
        self.assertFalse((self.home / '.claude/prompt-log-recent.md').exists())
        self.assertEqual(len(self.rows()), 3)
        self.assertEqual(len((self.home / '.claude/prompt-log-compat.jsonl').read_text(encoding='utf-8').splitlines()), 3)
        self.assertTrue(store.migrate_view(self.db, publishers_paused=True)['already_registered'])
        later = store.utc(datetime.now(timezone.utc) + timedelta(days=8))
        store.project(self.db, cutoff=later)
        self.assertIn('No prompts in this window.', note.read_text(encoding='utf-8'))
        self.assertTrue(note.read_text(encoding='utf-8').startswith(header))
        self.assertEqual(len(self.rows()), 3)
        self.assertEqual(Path(result['backup']).read_bytes(), original)

    def test_same_path_migration_refuses_incomplete_or_ambiguous_inputs(self):
        self.activate()
        row = self.row(agent='')  # Legacy renderer's display fallback is not stored metadata.
        self.add(row)
        note, job, _ = self.note_and_job([dict(row, machine='missing-foreign-device')])
        original = note.read_bytes()
        with self.assertRaisesRegex(ValueError, 'pause all'):
            store.migrate_view(self.db)
        with self.assertRaisesRegex(ValueError, 'absent or different'):
            store.migrate_view(self.db, publishers_paused=True)
        self.assertNotIn('view', store.config())
        self.assertEqual(note.read_bytes(), original)
        with self.assertRaisesRegex(ValueError, 'differs'):
            store.migrate_view(self.db, self.home / 'different.md', True)
        job.write_bytes(plistlib.dumps({'ProgramArguments': ['sh', '-c', 'arbitrary command']}))
        with self.assertRaisesRegex(ValueError, 'unsupported'):
            store.migrate_view(self.db, note, True)
        note, _, _ = self.note_and_job([row])
        note.write_text(note.read_text(encoding='utf-8') + 'Unmanaged user note below entries\n')
        with self.assertRaisesRegex(ValueError, 'absent or different'):
            store.migrate_view(self.db, publishers_paused=True)
        self.assertNotIn('view', store.config())

    def test_migration_matches_actual_legacy_renderer(self):
        rows = [self.row(repo='café-app', agent='', prompt='Unicode 日本語\nA "quoted" prompt'),
                self.row(repo=None, machine='', branch='', agent='')]
        source = self.home / '.claude/prompt-log.jsonl'
        source.write_text(''.join(json.dumps(row) + '\n' for row in rows))
        note, job, header = self.note_and_job([])
        subprocess.run(plistlib.loads(job.read_bytes())['ProgramArguments'], check=True,
                       capture_output=True, env=dict(os.environ, PROMPT_LOG_EXCLUDE=''))
        original = note.read_bytes()
        self.assertIn('## CAFé-APP', note.read_text(encoding='utf-8'))
        self.assertIn('## UNKNOWN', note.read_text(encoding='utf-8'))
        store.import_jsonl(self.db, source)
        store.activate(self.db, source)
        for shown in ('Preserve my unmanaged reminder', ''):
            edited = re.sub(r'(?m)(^## [^\n]*\n)[^\n]*\n',
                            lambda m: m[1] + shown + '\n', original.decode()).encode()
            note.write_bytes(edited)
            with self.assertRaisesRegex(ValueError, 'timestamp display'):
                store.migrate_view(self.db, publishers_paused=True)
            self.assertNotIn('view', store.config())
            self.assertEqual(note.read_bytes(), edited)
        for shown in ('2026-09-29T12:00:00Z  ', '2026-09-29 05:00:00 PDT  ',
                      '2026-09-29 17:45:00 +0545  '):
            variant = re.sub(r'(?m)(^## [^\n]*\n)[^\n]*\n',
                             lambda m: m[1] + shown + '\n', original.decode()).encode()
            with store.database(self.db) as conn:
                self.assertEqual(store.legacy_coverage(conn, variant)[1], 2)
        note.write_bytes(original)
        result = store.migrate_view(self.db, publishers_paused=True)
        self.assertEqual(result['covered_entries'], 2)
        self.assertEqual(note.read_bytes(), original)
        self.assertEqual(Path(result['backup']).read_bytes(), original)
        store.project(self.db)
        self.assertTrue(note.read_text(encoding='utf-8').startswith(header))

    def test_same_path_default_failure_recovery_and_write_guards(self):
        self.activate()
        row = self.row(agent='')
        self.add(row)
        note, job, header = self.note_and_job([row], default=True)
        original = note.read_bytes()
        exporter = plistlib.loads(job.read_bytes())['ProgramArguments']
        rejected = subprocess.run(exporter, capture_output=True)
        self.assertNotEqual(rejected.returncode, 0)  # Activation alone is not view migration.
        self.assertEqual(note.read_bytes(), original)
        result = store.migrate_view(self.db, publishers_paused=True)
        atomic = store.atomic
        def fail_note(path, data):
            if Path(path).resolve() == note.resolve():
                raise OSError('simulated note publication failure')
            return atomic(path, data)
        with patch.object(store, 'atomic', side_effect=fail_note):
            with self.assertRaises(OSError):
                store.project(self.db, cutoff='2026-09-30T00:00:00Z')
        self.assertEqual(note.read_bytes(), original)
        store.project(self.db, cutoff='2026-09-30T00:00:00Z')
        self.assertTrue(note.read_text(encoding='utf-8').startswith(header))
        subprocess.run(exporter + ['--sqlite'], check=True, capture_output=True)
        current = note.read_bytes()
        for option in ('--status', '--repair', '--backfill'):
            refused = subprocess.run(exporter + [option], capture_output=True)
            self.assertNotEqual(refused.returncode, 0)
            self.assertEqual(note.read_bytes(), current)
        for target in (note, Path(result['backup'])):
            with self.assertRaises(ValueError):
                store.export_device(self.db, target)
            with self.assertRaises(ValueError):
                store.project(self.db, self.home / 'preview.md', target)
        note.write_bytes(current + b'Unexpected foreign arrival\n')
        with self.assertRaisesRegex(ValueError, 'outside this publisher'):
            store.project(self.db)
        self.assertTrue(note.read_bytes().endswith(b'Unexpected foreign arrival\n'))
        note.write_bytes(current)
        cfg = store.config()
        cfg['fleet'] = {'repair_generated_note': True,
                        'header_sha256': store.digest(header.encode()),
                        'coverage': cfg['view']['coverage']}
        store.atomic(store.CONFIG, (store.encode(cfg) + '\n').encode())
        hybrid = current + b'\nMerged generated-body fragment\n'
        note.write_bytes(hybrid)
        store.project(self.db, cutoff='2026-09-30T00:00:00Z')
        archives = list(Path(result['backup']).parent.glob('conflict-*.md'))
        self.assertEqual(len(archives), 1)
        self.assertEqual(archives[0].read_bytes(), hybrid)
        self.assertTrue(note.read_bytes().startswith(header.encode()))
        self.assertEqual(archives[0].stat().st_mode & 0o777, 0o600)
        # Repeated content is deduplicated; archive failure preserves current bytes.
        note.write_bytes(hybrid)
        store.project(self.db, cutoff='2026-09-30T00:00:00Z')
        self.assertEqual(len(list(archives[0].parent.glob('conflict-*.md'))), 1)
        failed_body = hybrid + b'new conflict'
        note.write_bytes(failed_body)
        with patch.object(store, 'preserve_recovery', side_effect=OSError('fixture disk failure')):
            with self.assertRaises(OSError):
                store.project(self.db)
        self.assertEqual(note.read_bytes(), failed_body)
        note.write_bytes(b'Changed personal header\n' + current)
        with self.assertRaisesRegex(ValueError, 'personal header'):
            store.project(self.db)
        unknown = current + ('\n<!-- clio:record:clio1-' + '0' * 64 + ' -->\n').encode()
        note.write_bytes(unknown)
        with self.assertRaisesRegex(ValueError, 'waiting_for_history'):
            store.project(self.db)
        waiting = store.config()['view']['waiting_since']
        with self.assertRaisesRegex(ValueError, 'waiting_for_history'):
            store.project(self.db)
        self.assertEqual(store.config()['view']['waiting_since'], waiting)
        self.assertEqual(note.read_bytes(), unknown)
        cfg = store.config()
        cfg['view']['waiting_since'] = '2000-01-01T00:00:00Z'
        store.atomic(store.CONFIG, (store.encode(cfg) + '\n').encode())
        store.project(self.db, cutoff='2026-09-30T00:00:00Z')
        self.assertTrue(any(p.read_bytes() == unknown for p in archives[0].parent.glob('conflict-*.md')))
        self.assertNotIn('waiting_since', store.config()['view'])
        note.unlink()
        store.project(self.db, cutoff='2026-09-30T00:00:00Z')
        self.assertTrue(note.read_bytes().startswith(header.encode()))
        # Admission refuses additional archives without deleting any prior data.
        note.write_bytes(failed_body)
        with patch.object(store, 'MAX_ARCHIVES', 1):
            with self.assertRaisesRegex(ValueError, 'archive_budget_exhausted'):
                store.project(self.db)
        self.assertEqual(note.read_bytes(), failed_body)
        note.write_bytes(current)
        Path(result['backup']).write_bytes(original + b'altered backup')
        with self.assertRaisesRegex(ValueError, 'backup changed'):
            store.project(self.db)

    def test_import_accounting_resume_and_negative_controls(self):
        first = self.row(machine='', agent='', client_extension={'version': 2})
        second = self.row()
        path = self.source([first, first, second])
        with path.open('ab') as f:
            f.write(b'not-json\n{"prompt":"partial')
        result = store.import_jsonl(self.db, path, max_records=2)
        self.assertEqual((result['added'], result['duplicates'], result['lines']), (1, 1, 2))
        result = store.import_jsonl(self.db, path)
        self.assertEqual((result['added'], result['quarantined'], result['lines']), (1, 1, 4))
        self.assertGreater(result['remaining_bytes'], 0)
        with self.assertRaisesRegex(ValueError, 'unaccounted bytes'):
            store.verify_import(self.db, str(path))
        with path.open('ab') as f:
            f.write(b'"}\n')
        store.import_jsonl(self.db, path)
        report = store.verify_import(self.db, str(path))
        self.assertEqual((report['occurrences'], report['quarantined']), (5, 2))
        self.assertEqual(store.import_jsonl(self.db, path)['added'], 0)
        unknown = next(row for row in self.rows() if row['machine'] == '')
        self.assertEqual(unknown['agent'], '')
        self.assertEqual(unknown['extras'], {'client_extension': {'version': 2}})
        with self.assertRaisesRegex(ValueError, 'identity fields'):
            store.normalize(dict(first, origin_id='unversioned-shadow'), self.owner)
        with sqlite3.connect(self.db) as conn:
            conn.execute('DELETE FROM events WHERE record_id=?', (unknown['record_id'],))
        with self.assertRaisesRegex(ValueError, 'missing or corrupt'):
            store.verify_import(self.db, str(path))

    def test_source_change_and_transaction_interruption(self):
        path = self.source([self.row(), self.row()])
        with patch.object(store, 'insert', side_effect=RuntimeError('simulated interruption')):
            with self.assertRaises(RuntimeError):
                store.import_jsonl(self.db, path)
        self.assertEqual(self.rows(), [])
        self.assertEqual(store.import_jsonl(self.db, path)['added'], 2)
        original = path.read_bytes()
        path.write_bytes(original.replace(b'cafe', b'CAFE') if b'cafe' in original else b' ' + original)
        with self.assertRaisesRegex(ValueError, 'prefix changed'):
            store.import_jsonl(self.db, path)

    def test_identity_replay_collision_and_busy_receipt(self):
        row = self.row()
        first = self.add(row)
        self.assertEqual(first['record_id'], self.add(row)['record_id'])
        self.add(dict(row, machine='fixture-mini'))
        self.add(dict(row, prompt='A genuinely different same-second submission'))
        self.assertEqual(len(self.rows()), 3)
        with sqlite3.connect(self.db) as held:
            held.execute('BEGIN IMMEDIATE')
            start = time.monotonic()
            pending = self.add(self.row())
            self.assertLess(time.monotonic() - start, 2)
            self.assertEqual(pending['state'], 'pending')
            self.assertEqual(len(list(store.pending_dir(self.db).glob('clio1-*.json'))), 1)
            held.rollback()
        self.assertEqual(store.drain(self.db), {'drained': 1, 'pending': 0})
        self.assertEqual(len(self.rows()), 4)
        bad = self.rows()[0]
        bad['record_id'] = 'clio1-corrupt'
        with self.assertRaisesRegex(ValueError, 'identity'):
            store.normalize(bad)

    def test_write_failures_never_acknowledge_without_receipt(self):
        original_database = store.database
        def full_database(path, writable=False):
            conn = original_database(path, writable)
            if writable:
                pages = conn.execute('PRAGMA page_count').fetchone()[0]
                conn.execute('PRAGMA max_page_count=' + str(pages))
            return conn
        with patch.object(store, 'database', side_effect=full_database):
            result = self.add(self.row(prompt='large synthetic prompt ' * 10000))
        self.assertEqual(result['state'], 'pending')
        self.assertEqual(len(self.rows()), 0)
        self.assertEqual(store.drain(self.db)['drained'], 1)
        blocked = self.home / 'blocked.sqlite3'
        owner = store.initialize(blocked)
        store.pending_dir(blocked).write_text('a file, not a writable spool directory')
        with self.assertRaises(OSError):
            store.capture(blocked, owner, self.row())
        self.assertEqual(len(self.rows()), 1)

    def test_rolling_window_atomicity_idle_expiry_and_compatibility(self):
        for timestamp in ('2026-09-22T23:59:59Z', '2026-09-23T00:00:00Z',
                          '2026-09-29T12:00:00Z', '2026-09-30T00:00:00Z', '2026-09-30T00:00:01Z'):
            self.add(self.row(timestamp=timestamp))
        md, compat = self.home / 'recent.md', self.home / 'compat.jsonl'
        result = store.project(self.db, md, compat, '2026-09-30T00:00:00Z')
        self.assertEqual((result['rows'], result['history_rows']), (3, 5))
        before = md.read_bytes()
        self.assertEqual(result['bytes'], len(before))
        store.project(self.db, md, compat, '2026-09-30T00:00:00Z')
        self.assertEqual(before, md.read_bytes())
        rows = [json.loads(line) for line in compat.read_text(encoding='utf-8').splitlines()]
        self.assertEqual(rows[0]['timestamp'], '2026-09-22T23:59:59Z')
        self.assertEqual([r['timestamp'] for r in rows], sorted(r['timestamp'] for r in rows))
        self.assertIn('日本語', md.read_text(encoding='utf-8'))
        with patch.object(store.os, 'replace', side_effect=OSError('publication interrupted')):
            with self.assertRaises(OSError):
                store.project(self.db, md, cutoff='2026-10-30T00:00:00Z')
        self.assertEqual(before, md.read_bytes())
        store.project(self.db, md, cutoff='2026-10-30T00:00:00Z')
        self.assertIn('No prompts in this window.', md.read_text(encoding='utf-8'))
        self.assertEqual(len(self.rows()), 5)
        legacy = self.home / 'shared.md'
        legacy.write_text('# Shared history\n<!-- CLIO:ENTRIES -->\n')
        before = legacy.read_bytes()
        for target in (legacy, self.home / '.claude/prompt-log.md'):
            target.write_bytes(before)
            with self.assertRaisesRegex(ValueError, 'historical'):
                store.project(self.db, target)
            with self.assertRaisesRegex(ValueError, 'historical'):
                store.project(self.db, md, target)
            with self.assertRaisesRegex(ValueError, 'historical'):
                store.export_device(self.db, target)
            self.assertEqual(target.read_bytes(), before)

        marker_prompt = 'Explain the <!-- CLIO:ENTRIES --> marker\n<!-- CLIO:ENTRIES -->'
        self.add(self.row(prompt=marker_prompt))
        snapshot = self.home / 'marker-snapshot.jsonl'
        for _ in range(2):
            store.project(self.db, md, compat, '2026-09-30T00:00:00Z')
            store.export_device(self.db, snapshot)
        for output in (compat, snapshot):
            exported = [json.loads(line) for line in output.read_text(encoding='utf-8').splitlines()]
            self.assertTrue(any(r.get('prompt') == marker_prompt for r in exported))

    def test_readonly_queries_refs_pagination_and_large_prompt(self):
        reference = {'type': 'issue', 'url': 'https://github.com/HiQS-Labs/XYZ-CLIO/issues/3', 'relation': 'mentioned'}
        long = self.row(prompt='日本語\n' * 100000, references=[reference], checkout='/fixture/checkouts/rebalance')
        captured = self.add(long)
        self.add(self.row(agent='agy'))
        self.assertEqual(self.rows(reference=reference['url'])[0]['prompt'], long['prompt'])
        self.assertEqual(self.rows(record_id=captured['record_id'])[0]['checkout'], long['checkout'])
        self.assertEqual(len(self.rows(agent='agy', device='fixture-mbp14')), 1)
        self.assertEqual(self.rows(repo="x' OR 1=1 --"), [])
        self.assertNotEqual(self.rows(limit=1)[0]['record_id'], self.rows(limit=1, offset=1)[0]['record_id'])
        with store.database(self.db) as conn:
            with self.assertRaises(sqlite3.OperationalError):
                conn.execute('DELETE FROM events')
        missing = self.home / 'missing.sqlite3'
        with self.assertRaises(sqlite3.OperationalError):
            store.database(missing)
        self.assertFalse(missing.exists())
        # Exercise the launchd interpreter against a cold database made by this
        # interpreter. On macOS these can use different SQLite versions.
        if sys.platform == 'darwin' and Path('/usr/bin/python3').exists():
            cold = self.home / 'cross-runtime.sqlite3'
            helper = ROOT / 'utils/CLIO/clio-store.py'
            source = self.source([self.row(prompt='Synthetic cold WAL Unicode: 日本語')])
            for command in (['init'], ['import-jsonl', str(source)]):
                subprocess.run([sys.executable, str(helper), '--db', str(cold), *command],
                               check=True, capture_output=True, text=True)
            # The creator has exited and checkpointed its committed data. A
            # separate main-file copy forces absent sidecars on either runtime.
            cold_copy = self.home / 'cold-copy.sqlite3'
            shutil.copyfile(cold, cold_copy)
            cold = cold_copy
            for suffix in ('-wal', '-shm'):
                self.assertFalse(Path(str(cold) + suffix).exists())
            result = subprocess.run(['/usr/bin/python3', str(helper), '--db', str(cold),
                                     'query', '--limit', '1'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            records = json.loads(result.stdout)['records']
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['prompt'], 'Synthetic cold WAL Unicode: 日本語')

    def test_device_roundtrip_preserves_owner_extras_and_no_echo(self):
        path = self.source([self.row(machine='', agent='', client_extension={'version': 2})])
        store.import_jsonl(self.db, path)
        original = self.rows()[0]
        other = self.home / 'other.sqlite3'
        other_owner = store.initialize(other)
        store.capture(other, other_owner, self.row(machine='fixture-mini'))
        a, b = self.home / 'a.jsonl', self.home / 'b.jsonl'
        store.export_device(self.db, a)
        with self.assertRaisesRegex(ValueError, 'refuse self-import'):
            store.import_device(self.db, a)
        restored = self.home / 'restored.sqlite3'
        store.backup(self.db, restored)
        with self.assertRaisesRegex(ValueError, 'refuse self-import'):
            store.import_device(restored, a)
        self.assertEqual(len(self.rows()), 1)
        self.assertEqual(store.import_device(other, a)['added'], 1)
        self.assertEqual(store.import_device(other, a)['added'], 0)
        self.assertEqual(store.export_device(other, b)['rows'], 1)
        self.assertEqual(store.import_device(self.db, b)['added'], 1)
        self.assertEqual(store.export_device(self.db, self.home / 'a-again.jsonl')['rows'], 1)
        self.assertEqual(self.rows(record_id=original['record_id'])[0], original)
        md, compat = self.home / 'recent.md', self.home / 'compat.jsonl'
        store.project(self.db, md, compat)
        third = self.home / 'third.sqlite3'
        store.initialize(third)
        store.import_jsonl(third, compat)
        with store.database(third) as conn:
            copied = json.loads(conn.execute('SELECT payload FROM events WHERE record_id=?', (original['record_id'],)).fetchone()[0])
        self.assertEqual(copied, original)
        a.write_bytes(a.read_bytes() + b'corrupt\n')
        with self.assertRaisesRegex(ValueError, 'digest'):
            store.import_device(other, a)

        # Four independent stores and Git checkouts: only fixture Git transports snapshots.
        fleet = self.home / 'fleet'
        fleet.mkdir()
        remote = fleet / 'remote.git'
        def git(repo, *args):
            self.assertTrue(repo.resolve().is_relative_to(self.home.resolve()))
            return subprocess.run(['git', '-C', str(repo), '-c', 'core.hooksPath=/dev/null',
                                   '-c', 'commit.gpgsign=false', '-c', 'user.name=Fixture',
                                   '-c', 'user.email=fixture@example.invalid', *args],
                                  check=True, capture_output=True).stdout
        git(fleet, 'init', '--bare', '-q', '--initial-branch=main', str(remote))
        nodes = []
        for number in range(4):
            home = fleet / str(number)
            home.mkdir()
            checkout = home / 'pulse'
            git(home, 'clone', '-q', str(remote), str(checkout))
            if number == 0:
                git(checkout, 'commit', '-q', '--allow-empty', '-m', 'fixture seed')
                git(checkout, 'push', '-q', 'origin', 'main')
            db = home / 'history.sqlite3'
            nodes.append((home, checkout, db, store.initialize(db)))
        owners = [node[3] for node in nodes]
        def context(node):
            return patch.object(store, 'CONFIG', node[0] / 'config.json')
        for node in nodes:
            with context(node):
                store.activate(node[2], node[0] / 'absent.jsonl', fresh=True)
                note = node[0] / '0. Claude Prompts.md'
                note.write_text('# Personal header\n<!-- CLIO:ENTRIES -->\n')
                store.migrate_view(node[2], note, True, True)
                store.configure_fleet(node[2], node[1], owners, True)
                with self.assertRaises(ValueError):
                    store.configure_fleet(node[2], node[1], owners + [owners[0]], True)
                store.capture(node[2], node[3], self.row(timestamp=store.utc(), source_event_id='fleet-' + node[3], repo='original'))
        def publish(node):
            home, checkout, db, owner = node
            git(checkout, 'pull', '-q', '--ff-only')
            destination = checkout / 'devices' / owner / 'clio.jsonl'
            with context(node):
                store.export_device(db, destination)
            git(checkout, 'add', 'devices')
            git(checkout, 'commit', '-q', '-m', 'owned snapshot')
            git(checkout, 'push', '-q', 'origin', 'main')
        for node in nodes:
            publish(node)
        def converge():
            bodies, payloads = [], []
            cutoff = store.utc()
            for node in nodes:
                git(node[1], 'pull', '-q', '--ff-only')
                with context(node):
                    result = store.reconcile_fleet(node[2])
                    self.assertFalse(result['partial'], result)
                    store.project(node[2], node[0] / '0. Claude Prompts.md', cutoff=cutoff)
                    bodies.append((node[0] / '0. Claude Prompts.md').read_bytes())
                    with store.database(node[2]) as conn:
                        payloads.append(dict(conn.execute('SELECT record_id,payload FROM events')))
            self.assertTrue(payloads[0])
            self.assertTrue(all(p == payloads[0] for p in payloads))
            self.assertTrue(all(b == bodies[0] for b in bodies))
            return payloads[0]
        self.assertEqual(len(converge()), 4)
        # Offline capture survives locally; rejoin needs no role change.
        offline = nodes[0]
        with context(offline):
            store.capture(offline[2], offline[3], self.row(timestamp=store.utc(), source_event_id='offline'))
        publish(offline)
        self.assertEqual(len(converge()), 5)
        # Dirty working files cannot become committed imports.
        foreign = nodes[1][1] / 'devices' / owners[0] / 'clio.jsonl'
        saved = foreign.read_bytes()
        foreign.write_bytes(b'uncommitted corruption')
        with context(nodes[1]):
            self.assertFalse(store.reconcile_fleet(nodes[1][2])['partial'])
        foreign.write_bytes(saved)
        # 129 replay-label restorations consume one archive, before export.
        with context(offline):
            for number in range(129):
                store.capture(offline[2], offline[3], self.row(timestamp=store.utc(), source_event_id='restore-' + str(number), repo='original'))
        publish(offline)
        converge()
        with store.database(offline[2], True) as conn:
            old = list(conn.execute('SELECT record_id,payload FROM events WHERE origin_id=?', (offline[3],)))
            for record_id, payload in old:
                row = json.loads(payload)
                row['repo'] = 'replayed'
                conn.execute('UPDATE events SET repo=?,payload=? WHERE record_id=?', ('replayed', store.encode(row), record_id))
            conn.commit()
        with context(offline):
            out = offline[0] / 'restored.jsonl'
            store.export_device(offline[2], out)
            self.assertEqual(store.recovery_metrics(offline[2])['count'], 1)
            with store.database(offline[2], True) as conn:
                self.assertEqual(conn.execute("SELECT count(*) FROM events WHERE repo='replayed'").fetchone()[0], 0)
            self.assertEqual(store.import_device(nodes[1][2], out)['added'], 0)
            # Restore missing committed own history without deleting unsent events.
            with store.database(offline[2], True) as conn:
                conn.execute('DELETE FROM events WHERE record_id=?', (old[0][0],))
                conn.commit()
            store.capture(offline[2], offline[3], self.row(timestamp=store.utc(), source_event_id='unsent'))
            restored_result = store.reconcile_fleet(offline[2])
            own = next(item for item in restored_result['origins'] if item['owner'] == offline[3])
            self.assertEqual(own['added'], 1)
            self.assertEqual(own['unsent'], 1)
            with self.assertRaisesRegex(ValueError, 'refuse self-import'):
                store.import_device(offline[2], out)
        # Foreign cumulative regression is rejected transactionally.
        raw = out.read_bytes()
        manifest, rows = store.snapshot_records(raw)
        payload = (store.encode(rows[0]) + '\n').encode()
        manifest.update(rows=1, sha256=store.digest(payload))
        with self.assertRaisesRegex(ValueError, 'regressed'):
            store.import_snapshot(nodes[1][2], (store.encode(manifest) + '\n').encode() + payload,
                                  'fixture-regression', owners[0], cumulative=True)

    def test_simultaneous_capture_read_export(self):
        rows = [self.row() for _ in range(16)]
        self.add(self.row())
        md = self.home / 'recent.md'
        def run(i):
            if i % 4 == 0:
                self.rows()
                store.project(self.db, md, cutoff='2026-09-30T00:00:00Z')
            return self.add(rows[i])
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(run, range(16)))
        store.drain(self.db)
        self.assertEqual(len(self.rows()), 17)
        self.assertEqual(len({r['record_id'] for r in results}), 16)

    def test_activation_four_agent_routes_and_rollback_export(self):
        self.activate()
        writer = self.home / '.claude/hooks/clio-capture.sh'
        for agent in ('claude-code', 'zcode'):
            result = subprocess.run(['bash', str(writer), '--agent', agent], input=json.dumps(self.row()),
                                    text=True, capture_output=True, env=os.environ.copy())
            self.assertEqual(result.returncode, 0, result.stderr)
        codex = self.home / '.codex/sessions/fixture'
        codex.mkdir(parents=True)
        shutil.copyfile(ROOT / 'test/fixtures/clio/codex-rollout.jsonl', codex / 'rollout-fixture.jsonl')
        agy = self.home / 'agy/brain/fixture/.system_generated/logs'
        agy.mkdir(parents=True)
        shutil.copyfile(ROOT / 'test/fixtures/clio/agy-transcript.jsonl', agy / 'transcript_full.jsonl')
        conversations = self.home / 'agy/conversations'
        conversations.mkdir()
        env = dict(os.environ, CLIO_TAIL_BACKFILL='1', CODEX_HOME=str(self.home / '.codex'), CLIO_AGY_ROOT=str(self.home / 'agy'))
        for agent in ('codex', 'agy'):
            command = ['bash', str(ROOT / ('utils/CLIO/clio-' + agent + '-tail.sh'))]
            result = subprocess.run(command, text=True, capture_output=True, env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            before = len(self.rows())
            subprocess.run(command, check=True, capture_output=True, env=env)
            self.assertEqual(len(self.rows()), before)
        self.assertEqual({row['agent'] for row in self.rows()}, {'claude-code', 'zcode', 'codex', 'agy'})
        self.assertFalse((conversations / 'fixture.db').exists())
        valid_logs = self.home / 'agy/brain/fixture-valid/.system_generated/logs'
        valid_logs.mkdir(parents=True)
        shutil.copyfile(ROOT / 'test/fixtures/clio/agy-transcript.jsonl', valid_logs / 'transcript_full.jsonl')
        companion = conversations / 'fixture-valid.db'
        conn = sqlite3.connect(companion)
        conn.execute('CREATE TABLE trajectory_metadata_blob(data BLOB)')
        conn.execute('INSERT INTO trajectory_metadata_blob VALUES (?)', (b'file:///fixture/path/fixture-repo',))
        conn.commit()
        conn.close()
        before_bytes = companion.read_bytes()
        subprocess.run(['bash', str(ROOT / 'utils/CLIO/clio-agy-tail.sh')], env=env, check=True, capture_output=True)
        self.assertEqual(companion.read_bytes(), before_bytes)
        self.assertTrue(any(row['repo'] == 'fixture-repo' for row in self.rows(agent='agy')))
        self.assertFalse((self.home / '.claude/prompt-log.jsonl').exists())
        store.project(self.db, self.home / 'recent.md', self.home / 'rollback.jsonl')
        self.assertEqual(len((self.home / 'rollback.jsonl').read_text(encoding='utf-8').splitlines()), len(self.rows()))
        failed = self.home / 'failed-init.sqlite3'
        with patch.object(store.sqlite3, 'connect', side_effect=sqlite3.OperationalError('synthetic disk failure')):
            with self.assertRaises(sqlite3.OperationalError):
                store.initialize(failed)
        self.assertFalse(failed.exists())
        self.assertTrue(store.initialize(failed))
        store.backup(self.db, self.home / 'backup.sqlite3')
        with store.database(self.home / 'backup.sqlite3') as conn:
            self.assertEqual(conn.execute('SELECT count(*) FROM events').fetchone()[0], len(self.rows()))

    def test_tailer_retry_freezes_first_observed_context(self):
        self.activate()
        repo = self.home / 'work'
        repo.mkdir()
        subprocess.run(['git', 'init', '-q', '-b', 'main', str(repo)], check=True)
        subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'core.hooksPath=/dev/null', 'commit', '-q', '--allow-empty', '-m', 'fixture'], check=True)
        sessions = self.home / '.codex/sessions'
        sessions.mkdir(parents=True)
        rollout = sessions / 'rollout-retry.jsonl'
        records = [
            {'type': 'session_meta', 'payload': {'id': 'retry-session', 'cwd': str(repo), 'source': 'cli'}},
            {'type': 'event_msg', 'timestamp': '2026-09-29T12:00:00Z', 'payload': {'type': 'user_message', 'message': 'first source prompt'}},
            {'type': 'event_msg', 'timestamp': '2026-09-29T12:00:00Z', 'payload': {'type': 'user_message', 'message': 'second source prompt'}},
        ]
        rollout.write_text(''.join(json.dumps(r) + '\n' for r in records))
        writer = self.home / '.claude/hooks/clio-capture.sh'
        original = writer.read_text(encoding='utf-8')
        real = writer.with_name('real-capture.sh')
        real.write_text(original)
        real.chmod(0o755)
        writer.write_text('''#!/bin/bash\ninput=$(cat)\nif printf "%s" "$input" | jq -e 'contains({prompt:"second source prompt"})' >/dev/null; then exit 3; fi\nprintf "%s" "$input" | "$(dirname "$0")/real-capture.sh" "$@"\n''')
        env = dict(os.environ, CODEX_HOME=str(self.home / '.codex'), CLIO_TAIL_BACKFILL='1')
        command = ['bash', str(ROOT / 'utils/CLIO/clio-codex-tail.sh')]
        subprocess.run(command, env=env, check=True, capture_output=True)
        first = self.rows()
        self.assertEqual(len(first), 1)
        self.assertEqual(first[0]['branch'], 'main')
        subprocess.run(['git', '-C', str(repo), 'branch', 'feature'], check=True)
        subprocess.run(['git', '-C', str(repo), 'symbolic-ref', 'HEAD', 'refs/heads/feature'], check=True)
        writer.write_text(original)
        subprocess.run(command, env=env, check=True, capture_output=True)
        self.assertEqual(len(self.rows()), 2)
        self.assertEqual(self.rows(record_id=first[0]['record_id'])[0], first[0])
        second = next(r for r in self.rows() if r['prompt'] == 'second source prompt')
        self.assertEqual(second['branch'], 'feature')
        self.assertNotEqual(second['source_event_id'], first[0]['source_event_id'])

    def test_waiting_legacy_writer_rechecks_activation(self):
        path = self.home / '.claude/prompt-log.jsonl'
        path.write_text(json.dumps(self.row()) + '\n')
        original = path.read_bytes()
        store.import_jsonl(self.db, path)
        original_import = store.import_jsonl
        children = []
        def final_import(*args, **kwargs):
            result = original_import(*args, **kwargs)
            process = subprocess.Popen(['bash', str(self.home / '.claude/hooks/clio-capture.sh'), '--agent', 'claude-code'],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, env=os.environ.copy())
            process.stdin.write(json.dumps(self.row()))
            process.stdin.close()
            process.stdin = None
            children.append(process)
            time.sleep(0.3)
            return result
        with patch.object(store, 'import_jsonl', side_effect=final_import):
            store.activate(self.db, path)
        output, error = children[0].communicate(timeout=3)
        self.assertEqual(children[0].returncode, 0, error)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(len(self.rows()), 2)

    def test_activation_import_gate_and_source_preservation(self):
        path = self.source([self.row()], name='original.jsonl')
        before = path.read_bytes()
        store.import_jsonl(self.db, path)
        with patch.object(store, 'check_deadline', side_effect=TimeoutError('cutover budget')):
            with self.assertRaises(TimeoutError):
                store.activate(self.db, path)
        self.assertFalse(store.CONFIG.exists())
        self.assertFalse((self.home / '.claude/prompt-log.lock').exists())
        store.activate(self.db, path, capture_only=True)
        self.assertEqual(path.read_bytes(), before)
        backups = list(self.home.glob('original.jsonl.pre-sqlite-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), before)
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            store.project(self.db, self.home / 'recent.md', path)
        note, job, _ = self.note_and_job([self.row()])
        note.write_bytes(note.read_bytes() + b'\n<!-- CLIO:ENTRIES -->\nUnrecovered historical content\n')
        note_bytes, job_bytes = note.read_bytes(), job.read_bytes()
        for agent in ('claude-code', 'zcode', 'codex', 'agy'):
            row = self.row(agent=agent, timestamp=store.utc(), source_event_id='capture-only-' + agent)
            subprocess.run(['bash', str(self.home / '.claude/hooks/clio-capture.sh'), '--agent', agent, '--record'],
                           input=json.dumps(row), text=True, check=True, capture_output=True)
        command = plistlib.loads(job_bytes)['ProgramArguments']
        result = json.loads(subprocess.run(command, check=True, capture_output=True, text=True).stdout)
        self.assertEqual(result['note_publication'], 'paused')
        self.assertEqual(result['history_rows'], 5)
        self.assertEqual(result['pending'], 0)
        self.assertEqual(note.read_bytes(), note_bytes)
        self.assertEqual(job.read_bytes(), job_bytes)
        self.assertEqual(path.read_bytes(), before)
        compat = self.home / '.claude/prompt-log-compat.jsonl'
        rows = [json.loads(line) for line in compat.read_bytes().splitlines()]
        self.assertEqual(len(rows), 5)
        self.assertEqual({row['agent'] for row in rows}, {'claude-code', 'zcode', 'codex', 'agy'})
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            store.project(self.db, jsonl=path, jsonl_only=True)
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            store.project(self.db, jsonl=backups[0], jsonl_only=True)
        self.assertEqual(backups[0].read_bytes(), before)
        with self.assertRaisesRegex(ValueError, 'one standalone'):
            store.migrate_view(self.db, publishers_paused=True)
        result = store.migrate_view(self.db, publishers_paused=True, archive_unreconciled_note=True)
        self.assertEqual(result['coverage'], 'archived-not-reconciled')
        self.assertIsNone(result['covered_entries'])
        self.assertEqual(Path(result['backup']).read_bytes(), note_bytes)
        self.assertEqual(note.read_bytes(), note_bytes)
        cfg = store.config()
        self.assertEqual(cfg['view']['header'], note_bytes.decode().split('<!-- CLIO:ENTRIES -->', 1)[0] + '<!-- CLIO:ENTRIES -->\n')
        result = json.loads(subprocess.run(command, check=True, capture_output=True, text=True).stdout)
        self.assertEqual(result['rows'], 5)
        explicit = subprocess.run([sys.executable, str(ROOT / 'utils/CLIO/clio-store.py'),
                                   '--db', str(self.db), 'scheduled-export', str(note)],
                                  check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(explicit.stdout).get('rows'), 5)
        self.assertTrue(note.read_bytes().startswith(cfg['view']['header'].encode()))
        self.assertIn('not fully reconciled into SQLite', note.read_text())
        self.assertEqual(job.read_bytes(), job_bytes)
        self.assertEqual(Path(cfg['view']['backup']).read_bytes(), note_bytes)
        note.write_bytes(note.read_bytes() + b'foreign publisher edit')
        with self.assertRaisesRegex(ValueError, 'outside this publisher'):
            store.project(self.db)


if __name__ == '__main__':
    unittest.main(verbosity=2)
