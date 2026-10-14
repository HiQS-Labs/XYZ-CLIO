#!/usr/bin/env python3
"""Stable, read-only forensic views over the adjacent canonical CLIO reader."""
import argparse
import contextlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys

FILTERS = ('repo', 'device', 'agent', 'session', 'record_id', 'repo_slug',
           'origin', 'since', 'until', 'text', 'reference')
HELPER = Path(__file__).resolve().with_name('clio-store.py')


class Failure(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


class Parser(argparse.ArgumentParser):
    def error(self, message):
        # argparse messages can echo private query arguments.
        raise Failure('invalid_arguments', 'Invalid arguments; use --help for accepted options.')


def envelope():
    return dict(schema_version=1, status='error', operation=None,
                source=dict(db=None, helper=str(HELPER), resolution=None, candidates=[]),
                filters={key: None for key in FILTERS}, records=[],
                page=dict(limit=None, offset=0, order=None, has_more=False, next_offset=None),
                journey=dict(earliest_match=None, session_first_record=None, basis='not_requested'),
                coverage=dict(fleet_complete=None, capture_complete=None, pending=None,
                              fleet=None, note_status=None, config_receipts='not_loaded',
                              limitations=['Captured prompts may omit earlier or filtered turns.',
                                           'Local history does not prove complete fleet coverage.',
                                           'Reads are live; concurrent capture can shift offset pages.']),
                errors=[])


def resolve(store, args, result):
    """Prefer authoritative choices; only discover when neither config nor default exists."""
    cfg = {}
    if args.db is not None:
        candidate, method = args.db, 'explicit'
        result['coverage']['config_receipts'] = 'not_loaded_explicit_db'
    else:
        try:
            cfg = store.config()
        except (ValueError, OSError, TypeError):
            raise Failure('invalid_config', 'Cannot read CLIO configuration; correct it or select --db.')
        result['coverage']['config_receipts'] = 'loaded' if cfg else 'not_configured'
        default = Path.home() / '.claude/prompt-log.sqlite3'
        if cfg:
            candidate, method = cfg['db'], 'config'
        elif default.exists():
            candidate, method = default, 'default'
        else:
            root = Path(args.pulse_root).expanduser() if args.pulse_root else Path.home() / 'git-pulse-sync'
            candidates = set()
            # At most 100 directory entries per level; no recursive disk search.
            for folder in (root, root / 'CLIO'):
                if not folder.is_dir():
                    continue
                for index, path in enumerate(folder.iterdir()):
                    if index >= 100:
                        raise Failure('discovery_limit', 'Discovery directory is too large; select --db.')
                    if path.suffix not in ('.db', '.sqlite', '.sqlite3') or not path.is_file():
                        continue
                    try:
                        with contextlib.closing(store.database(path)):
                            candidates.add(str(path.resolve()))
                    except (ValueError, OSError, sqlite3.Error):
                        continue
            result['source']['candidates'] = sorted(candidates)
            if len(candidates) != 1:
                code = 'ambiguous_database' if candidates else 'database_not_found'
                raise Failure(code, 'Select --db from valid candidates or configure an existing CLIO database.')
            candidate, method = next(iter(candidates)), 'pulse'
    try:
        path = Path(candidate).expanduser().resolve()
        result['source'].update(db=str(path), resolution=method)
        with contextlib.closing(store.database(path)):
            pass
    except (ValueError, OSError, TypeError, sqlite3.Error):
        raise Failure('invalid_database', 'Selected database is missing, inaccessible or not a supported CLIO store.')
    return path, cfg


def record(store, row):
    timestamp = store.utc(store.instant(row['timestamp']))
    fields = ('record_id', 'session_id', 'agent', 'repo', 'repo_slug', 'branch',
              'checkout', 'origin_id', 'source_event_id', 'prompt')
    value = {key: row.get(key) or None for key in fields}
    extra = row.get('extras') or {}
    value.update(timestamp=timestamp, date=timestamp[:10], time=timestamp[11:-1], timezone='UTC',
                 device=row.get('machine') or None,
                 ide=extra.get('ide') if isinstance(extra.get('ide'), str) and extra['ide'] else None,
                 references=row.get('references') or [], metadata=extra)
    return value


def run(argv, result):
    parser = Parser(description=__doc__)
    parser.add_argument('operation', choices=('locate', 'search', 'session', 'journey'))
    parser.add_argument('--db', help='explicit existing CLIO SQLite file')
    parser.add_argument('--pulse-root', help='shallow fallback discovery root')
    for key in FILTERS:
        parser.add_argument('--' + key.replace('_', '-'))
    parser.add_argument('--limit', type=int, default=20, help='1..999 records')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--order', choices=('oldest', 'newest'), default=None)
    args = parser.parse_args(argv)
    result['operation'] = args.operation
    result['filters'] = {key: getattr(args, key) for key in FILTERS}
    order = args.order or ('newest' if args.operation == 'search' else 'oldest')
    result['page'].update(limit=args.limit, offset=args.offset, order=order)
    if not 1 <= args.limit <= 999 or args.offset < 0:
        raise Failure('invalid_arguments', 'Use limit 1..999 and a nonnegative offset.')
    if args.text is not None and not args.text.strip():
        raise Failure('invalid_arguments', 'Text must contain a non-whitespace keyword.')
    if args.operation == 'journey' and (not args.text or args.offset or order != 'oldest'):
        raise Failure('invalid_arguments', 'Journey requires --text, oldest order and offset zero.')
    if args.operation == 'session' and (not args.session or not args.session.strip() or order != 'oldest'):
        raise Failure('invalid_arguments', 'Session requires --session and oldest order.')
    spec = importlib.util.spec_from_file_location('clio_store', HELPER)
    store = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(store)
    try:
        for key in ('since', 'until'):
            if getattr(args, key) is not None:
                setattr(args, key, store.utc(store.instant(getattr(args, key))))
        if args.since and args.until and args.since > args.until:
            raise ValueError('reversed interval')
    except (ValueError, OverflowError):
        raise Failure('invalid_arguments', 'Dates must be ISO timestamps with a timezone and since <= until.')
    result['filters'] = {key: getattr(args, key) for key in FILTERS}
    path, cfg = resolve(store, args, result)
    if args.operation == 'locate':
        result['status'] = 'ok'
        return
    query_args = argparse.Namespace(**result['filters'], limit=args.limit + 1,
                                    offset=args.offset, order=order, explain=False)
    native = store.query(path, query_args, configuration=cfg)
    rows = [record(store, row) for row in native['records'][:args.limit]]
    more = len(native['records']) > args.limit
    result['page'].update(has_more=more, next_offset=args.offset + args.limit if more else None)
    result['coverage'].update(pending=native['pending'], fleet=native.get('fleet'),
                              note_status=native.get('note_status'))
    journey = result['journey']
    if args.operation == 'journey':
        journey['basis'] = 'no_matching_record'
        if rows:
            first = rows[0]
            journey.update(earliest_match=first, basis='missing_session_identity')
            if all(first[key] for key in ('origin_id', 'agent', 'session_id')):
                identity = {key: None for key in FILTERS}
                identity.update(origin=first['origin_id'], agent=first['agent'], session=first['session_id'])
                session_args = argparse.Namespace(**identity, limit=1, offset=0, order='oldest', explain=False)
                session = store.query(path, session_args, configuration=cfg)['records']
                journey.update(session_first_record=record(store, session[0]) if session else None,
                               basis='earliest_captured_match_and_session' if session else 'session_record_unavailable')
    result.update(records=rows, status='ok' if rows else 'empty')


def main(argv=None):
    result = envelope()
    try:
        run(sys.argv[1:] if argv is None else argv, result)
    except Failure as error:
        result['errors'] = [dict(code=error.code, message=str(error))]
    except (OSError, ValueError, TypeError, KeyError, sqlite3.Error, ImportError):
        result['errors'] = [dict(code='query_failed', message='Cannot read CLIO history; check the helper, database and configuration.')]
    if result['errors']:
        result.update(status='error', records=[], journey=envelope()['journey'])
        result['page'].update(has_more=False, next_offset=None)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 2 if result['status'] == 'error' else 0


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    sys.exit(main())
