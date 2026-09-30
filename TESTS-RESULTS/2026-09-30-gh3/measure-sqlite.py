"""Synthetic comparison only. Usage: python3 measure-sqlite.py corpus.jsonl"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('store', ROOT / 'utils/CLIO/clio-store.py')
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)
corpus = Path(sys.argv[1]).resolve()
raw = corpus.read_bytes()
assert len(raw) == 12526701 and hashlib.sha256(raw).hexdigest() == '0f2ba3976a500dd69e895507f767cb096ec6860966617370cbca2aa650169f5e'
args = argparse.Namespace(repo='rebalanceOS', device='fixture-mbp14', agent=None, session=None,
    record_id=None, repo_slug=None, origin=None, since='2026-09-23T00:00:00Z',
    until='2026-09-30T00:00:00Z', text=None, reference=None, limit=20, offset=0, explain=True)
def jsonl_query():
    rows = [json.loads(line) for line in corpus.read_text().splitlines()]
    assert len(rows) == 10000
    return sorted([r for r in rows if r['repo'] == args.repo and r['machine'] == args.device
        and args.since <= r['timestamp'] <= args.until], key=lambda r:(r['timestamp'],r['session_id']), reverse=True)[:20]
def identity(rows):
    assert len(rows) == 20
    return [(r['session_id'], r['timestamp'].replace('.000000Z', 'Z'), r['prompt']) for r in rows]
def measure(fn, count=7):
    durations=[]
    for _ in range(count):
        begin=time.perf_counter(); result=fn(); durations.append((time.perf_counter()-begin)*1000)
    return result, {'runs_ms':durations,'median_ms':statistics.median(durations),'max_ms':max(durations)}
with tempfile.TemporaryDirectory(prefix='clio-measure-') as folder:
    home=Path(folder); os.environ['HOME']=folder
    store.CONFIG=home/'.claude/clio-storage.json'
    db=home/'history.sqlite3'; owner=store.initialize(db)
    for _ in range(10): store.import_jsonl(db,corpus)
    assert store.verify_import(db,str(corpus))['occurrences']==10000
    expected, scan=measure(jsonl_query)
    found, indexed=measure(lambda:store.query(db,args))
    assert identity(expected)==identity(found['records'])
    projection, export=measure(lambda:store.project(db,home/'recent.md',home/'compat.jsonl',args.until),3)
    assert projection['history_rows']==10000 and projection['rows']>0
    hooks=home/'.claude/hooks'; hooks.mkdir(parents=True)
    install=(ROOT/'utils/CLIO/INSTALL.md').read_text()
    body=install.split("cat > ~/.claude/hooks/clio-capture.sh << 'EOF'\n",1)[1].split('\nEOF\n',1)[0]
    writer=hooks/'clio-capture.sh'; writer.write_text(body)
    (hooks/'clio-store.py').write_bytes((ROOT/'utils/CLIO/clio-store.py').read_bytes())
    store.activate(db,home/'nonexistent.jsonl',fresh=True)
    durations=[]
    for i in range(30):
        row=dict(expected[0],session_id='latency-'+str(i),timestamp='2026-09-30T01:00:00Z')
        begin=time.perf_counter()
        subprocess.run(['bash',str(writer),'--agent','codex','--record'], input=json.dumps(row),text=True,check=True,capture_output=True,env=dict(os.environ,CLIO_MIN_PROMPT_CHARS='0'))
        durations.append((time.perf_counter()-begin)*1000)
    assert max(durations)<2000
    assert store.query(db,args)['pending']==0
    print(json.dumps({'corpus_rows':10000,'corpus_bytes':len(raw),'corpus_sha256':hashlib.sha256(raw).hexdigest(),
        'equal_nonempty_results':True,'returned':20,'jsonl_scan':scan,'sqlite_query':indexed,
        'query_plan':found['query_plan'],'projection':projection | {'markdown':'temporary recent.md'},
        'projection_timing':export,'capture_shared_writer':{'samples':30,'p50_ms':statistics.median(durations),
        'p95_ms':sorted(durations)[28],'max_ms':max(durations)},
        'limitations':'Synthetic warm local run, excludes CLI startup for query and disk/network fleet transport. Shared-writer timings include shell/Python startup. No FTS/vector speed claim.'},indent=2))
