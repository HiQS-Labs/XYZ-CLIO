#!/bin/bash
# GH-11 smoke: real CLI, throwaway HOMEs, local bare remote. Arg 1 = repo checkout under test.
set -uo pipefail
REPO="$1"; W="$(mktemp -d "${TMPDIR:-/tmp}/gh11-smoke.XXXXXX")"; STORE="$REPO/utils/CLIO/clio-store.py"
unset CLIO_MIN_PROMPT_CHARS
g(){ git -C "$1" -c user.name=Smoke -c user.email=smoke@example.invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null "${@:2}"; }
git init -q --bare --initial-branch=main "$W/remote.git"
cli(){ local h="$1"; shift; HOME="$W/$h" CLIO_CONFIG="$W/$h/cfg.json" python3 "$STORE" --db "$W/$h/h.sqlite3" "$@"; }
for h in pub new; do mkdir -p "$W/$h/.claude"; git clone -q "$W/remote.git" "$W/$h/pulse" 2>/dev/null; done
g "$W/pub/pulse" commit -q --allow-empty -m seed; g "$W/pub/pulse" push -q origin main
install_hooks(){ python3 - "$REPO" "$W/$1/.claude/hooks" <<'PY'
import sys, shutil
from pathlib import Path
repo, hooks = Path(sys.argv[1]), Path(sys.argv[2]); hooks.mkdir(parents=True, exist_ok=True)
src = (repo / 'utils/CLIO/INSTALL.md').read_text()
for name in ('clio-capture.sh', 'log-prompt.sh'):
    body = src.split('cat > ~/.claude/hooks/' + name + " << 'EOF'\n", 1)[1].split('\nEOF\n', 1)[0] + '\n'
    (hooks / name).write_text(body); (hooks / name).chmod(0o755)
for name in ('clio-store.py', 'prompt-log-to-md.sh'):
    shutil.copyfile(repo / 'utils/CLIO' / name, hooks / name); (hooks / name).chmod(0o755)
PY
}
for h in pub new; do install_hooks $h; done
for h in pub new; do cli $h init >/dev/null; cli $h activate --source "$W/$h/none.jsonl" --fresh --capture-only >/dev/null; done
PUB=$(python3 -c "import json;print(json.load(open('$W/pub/cfg.json'))['owner'])"); NEW=$(python3 -c "import json;print(json.load(open('$W/new/cfg.json'))['owner'])")
TS=$(python3 -c "from datetime import datetime,timedelta,timezone;print((datetime.now(timezone.utc)-timedelta(minutes=15)).strftime('%Y-%m-%dT%H:%M:%SZ'))")
for h in pub new; do echo "{\"timestamp\":\"$TS\",\"session_id\":\"smoke-$h\",\"prompt\":\"Smoke prompt from $h with enough text to pass any filter\",\"machine\":\"smoke-$h\",\"repo\":\"smoke\",\"agent\":\"claude-code\",\"branch\":\"main\",\"source_event_id\":\"smoke-$h\"}" | cli $h capture >/dev/null; done
pubdeliver(){ g "$W/$1/pulse" pull -q --ff-only; mkdir -p "$W/$1/pulse/devices/$2"; cli $1 export-device "$W/$1/pulse/devices/$2/clio.jsonl" >/dev/null; g "$W/$1/pulse" add devices; g "$W/$1/pulse" commit -q -m snap; g "$W/$1/pulse" push -q origin main; }
echo "== publisher: note registered, discovery on"
printf '# Smoke header\n<!-- CLIO:ENTRIES -->\n' > "$W/pub/note.md"
cli pub migrate-view --markdown "$W/pub/note.md" --publishers-paused --archive-unreconciled-note | head -c 120; echo
cli pub configure-fleet "$W/pub/pulse" --discover-origins --repair-generated-note | head -c 160; echo
pubdeliver pub "$PUB"
echo "== MAIN: new device delivers; publisher reconciles with NO config change"
cli new configure-fleet "$W/new/pulse" --discover-origins >/dev/null
pubdeliver new "$NEW"
g "$W/pub/pulse" pull -q --ff-only
cli pub reconcile-fleet | python3 -c "import json,sys;r=json.load(sys.stdin);print('discovered=',r.get('discovered'),'states=',{o['owner'][:8]:(o['state'],o.get('added')) for o in r['origins']},'partial=',r['partial'])"
echo "== ADJACENT 1: rerun reconcile adds nothing"
cli pub reconcile-fleet | python3 -c "import json,sys;r=json.load(sys.stdin);print('discovered=',r.get('discovered'),'added=',sum(o.get('added',0) for o in r['origins']),'partial=',r['partial'])"
echo "== ADJACENT 2: publisher renders; capture-only device joins the note and publishes twice"
cli pub scheduled-export "$W/pub/note.md" | python3 -c "import json,sys;r=json.load(sys.stdin);print('pub note=',r['note_publication'])"
cp "$W/pub/note.md" "$W/new/note.md"
g "$W/new/pulse" pull -q --ff-only; cli new reconcile-fleet >/dev/null
cli new migrate-view --markdown "$W/new/note.md" --join-fleet-note | python3 -c "import json,sys;r=json.load(sys.stdin);print('join registered=',r['registered'],'coverage=',r['coverage'])"
cli new configure-fleet "$W/new/pulse" --discover-origins --repair-generated-note >/dev/null
for i in 1 2; do cli new scheduled-export "$W/new/note.md" | python3 -c "import json,sys;r=json.load(sys.stdin);print('new run',$i,'note=',r['note_publication'],'pending=',r['pending'])"; done
grep -c "clio:record" "$W/new/note.md" | sed 's/^/records in joined note: /'
echo "== ADJACENT 3: join refused when already registered / note hand-edited elsewhere"
cli new migrate-view --markdown "$W/new/note.md" --join-fleet-note | head -c 100; echo
rm -rf "$W"
