#!/usr/bin/env python3
"""SQLite acceptance cases using only synthetic data and temporary homes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
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
        source = (ROOT / 'utils/CLIO/INSTALL.md').read_text()
        for name in ('clio-capture.sh', 'log-prompt.sh'):
            marker = 'cat > ~/.claude/hooks/' + name + " << 'EOF'\n"
            body = source.split(marker, 1)[1].split('\nEOF\n', 1)[0] + '\n'
            (hooks / name).write_text(body)
            (hooks / name).chmod(0o755)
        shutil.copyfile(ROOT / 'utils/CLIO/clio-store.py', hooks / 'clio-store.py')

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
        rows = [json.loads(line) for line in compat.read_text().splitlines()]
        self.assertEqual(rows[0]['timestamp'], '2026-09-22T23:59:59Z')
        self.assertEqual([r['timestamp'] for r in rows], sorted(r['timestamp'] for r in rows))
        self.assertIn('日本語', md.read_text())
        with patch.object(store.os, 'replace', side_effect=OSError('publication interrupted')):
            with self.assertRaises(OSError):
                store.project(self.db, md, cutoff='2026-10-30T00:00:00Z')
        self.assertEqual(before, md.read_bytes())
        store.project(self.db, md, cutoff='2026-10-30T00:00:00Z')
        self.assertIn('No prompts in this window.', md.read_text())
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

    def test_device_roundtrip_preserves_owner_extras_and_no_echo(self):
        path = self.source([self.row(machine='', agent='', client_extension={'version': 2})])
        store.import_jsonl(self.db, path)
        original = self.rows()[0]
        other = self.home / 'other.sqlite3'
        other_owner = store.initialize(other)
        store.capture(other, other_owner, self.row(machine='fixture-mini'))
        a, b = self.home / 'a.jsonl', self.home / 'b.jsonl'
        store.export_device(self.db, a)
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
        self.assertEqual(len((self.home / 'rollback.jsonl').read_text().splitlines()), len(self.rows()))
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
        original = writer.read_text()
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
        store.activate(self.db, path)
        self.assertEqual(path.read_bytes(), before)
        backups = list(self.home.glob('original.jsonl.pre-sqlite-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), before)
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            store.project(self.db, self.home / 'recent.md', path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
