"""Reproduce the synthetic JSONL baseline; writes only the explicit output path."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

cutoff = datetime(2026, 9, 30, tzinfo=timezone.utc)
with Path(sys.argv[1]).open('x') as output:
    for i in range(10000):
        row = {
            'timestamp': (cutoff - timedelta(seconds=(9999-i)*180)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'session_id': f'synthetic-session-{i//10}',
            'repo': ['rebalanceOS', 'XYZ-forge', 'needle-fork'][i%3],
            'machine': ['fixture-mbp14', 'fixture-mini', 'fixture-mbp16'][i%3],
            'agent': ['claude-code', 'zcode', 'codex', 'agy'][i%4],
            'branch': 'fixture-branch',
            'prompt': ('Synthetic CLIO benchmark history. '
                       + ('frozen packet ' if i%137 == 0 else 'ordinary task ')
                       + str(i) + '\n') * 20,
        }
        output.write(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n')
