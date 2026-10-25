#!/bin/bash
# GH-13 manual checks. Usage: manual-checks.sh <repo root>. Synthetic data, throwaway HOME.
set -uo pipefail
ROOT=$1; DOC="$ROOT/utils/CLIO/INSTALL.md"; T=$(mktemp -d "${TMPDIR:-/tmp}/gh13mc.XXXXXX") && [ -d "$T" ] || { echo "manual-checks: mktemp failed" >&2; exit 1; }; trap 'rm -rf "${T:?}"' EXIT
unset CLIO_MIN_PROMPT_CHARS CLIO_CONFIG
home_for() { h="$T/$1/home"; mkdir -p "$h/.claude/hooks"; awk '/^cat > ~\/\.claude\/hooks\/clio-capture\.sh << .EOF.$/{f=1;next} f&&/^EOF$/{exit} f' "$DOC" > "$h/.claude/hooks/clio-capture.sh"; chmod +x "$h/.claude/hooks/clio-capture.sh"; echo "$h"; }
rows() { [ -f "$1/.claude/prompt-log.jsonl" ] && wc -l < "$1/.claude/prompt-log.jsonl" | tr -d ' ' || echo 0; }
codex_case() { # $1 name, $2 lock setup cmd ('' none); runs codex tailer with backfill on the fixture
  h=$(home_for "$1"); cx="$T/$1/codex/sessions/2026/08/31"; mkdir -p "$cx"; cp "$ROOT/test/fixtures/clio/codex-rollout.jsonl" "$cx/rollout-x.jsonl"
  L="$h/.claude/prompt-log-codex-tail.lock"; [ -n "$2" ] && { mkdir "$L"; eval "$2"; }
  out=$(HOME="$h" CODEX_HOME="$T/$1/codex" CLIO_TAIL_BACKFILL=1 bash "$ROOT/utils/CLIO/clio-codex-tail.sh" 2>&1)
  reap=$(grep -c "reaped stale" "$h/.claude/prompt-log-errors.log" 2>/dev/null); lock=$([ -d "$L" ] && echo present || echo gone)
  echo "$1: out='${out:-<none>}' rows=$(rows "$h") reaped=${reap:-0} lock_after=$lock"
}
now=$(date +%s)
codex_case a-stale-born "echo $((now-600)) > \"\$L/born\""
codex_case b-fresh-born "echo $now > \"\$L/born\""
codex_case b2-no-born-old-mtime "touch -t \$(date -r $((now-600)) +%Y%m%d%H%M.%S) \"\$L\""
codex_case b3-nonnumeric-born "echo abc > \"\$L/born\""
# c. idle ticks: state bytes+mtime after 2nd vs 3rd run (Codex and Agy)
h=$(home_for c-codex); cx="$T/c-codex/codex/sessions/2026/08/31"; mkdir -p "$cx"; cp "$ROOT/test/fixtures/clio/codex-rollout.jsonl" "$cx/rollout-c.jsonl"
for i in 1 2; do HOME="$h" CODEX_HOME="$T/c-codex/codex" bash "$ROOT/utils/CLIO/clio-codex-tail.sh" >/dev/null; done
st="$h/.claude/prompt-log-codex-tail.state"; m1=$(stat -f %m "$st"); s1=$(shasum "$st" | cut -c1-12); sleep 1.2
HOME="$h" CODEX_HOME="$T/c-codex/codex" bash "$ROOT/utils/CLIO/clio-codex-tail.sh" >/dev/null; m2=$(stat -f %m "$st"); s2=$(shasum "$st" | cut -c1-12)
echo "c-codex-idle: mtime $m1->$m2 sha $s1->$s2 $([ "$m1" = "$m2" ] && echo UNCHANGED || echo REWRITTEN)"
h=$(home_for c-agy); ag="$T/c-agy/agy/brain/0125ee13-24a0-46e7-a59e-d6005d4e1fab/.system_generated/logs"; mkdir -p "$ag"; cp "$ROOT/test/fixtures/clio/agy-transcript.jsonl" "$ag/transcript_full.jsonl"
for i in 1 2; do HOME="$h" CLIO_AGY_ROOT="$T/c-agy/agy" bash "$ROOT/utils/CLIO/clio-agy-tail.sh" >/dev/null; done
st="$h/.claude/prompt-log-agy-tail.state"; [ -f "$st" ] || st=$(ls "$h"/.claude/*agy*state 2>/dev/null | head -1); m1=$(stat -f %m "$st"); s1=$(shasum "$st" | cut -c1-12); sleep 1.2
HOME="$h" CLIO_AGY_ROOT="$T/c-agy/agy" bash "$ROOT/utils/CLIO/clio-agy-tail.sh" >/dev/null; m2=$(stat -f %m "$st"); s2=$(shasum "$st" | cut -c1-12)
echo "c-agy-idle: mtime $m1->$m2 sha $s1->$s2 $([ "$m1" = "$m2" ] && echo UNCHANGED || echo REWRITTEN)"
# d. IDE stripping
h=$(home_for d); cx="$T/d/codex/sessions/2026/08/31"; mkdir -p "$cx"; R="$cx/rollout-d.jsonl"
um() { jq -nc --arg m "$1" --arg t "$2" '{payload:{type:"user_message",message:$m},timestamp:$t,type:"event_msg"}'; }
{ echo '{"payload":{"id":"sess-d","cwd":"/tmp/mock-repo"},"timestamp":"2099-01-01T00:00:00.000Z","type":"session_meta"}'
  um $'# Context from my IDE setup:\n\n## Active file: a.md\n\n## My request for Codex:\nPlease refactor the exporter loop so it handles rotation cleanly.' 2099-01-01T00:00:01.000Z
  um $'# Context from my IDE setup:\n\n## Open tabs:\n- b.md\n\n## My request:\nExplain why the tailer cursor only lands after a newline character.' 2099-01-01T00:00:02.000Z
  um $'Quoting the marker on purpose: ## My request: keep this whole prompt exactly as typed please.' 2099-01-01T00:00:03.000Z
  um $'# Context from my IDE setup:\n\n## Active file: c.md\n\n## My request:\n   ' 2099-01-01T00:00:04.000Z; } > "$R"
HOME="$h" CODEX_HOME="$T/d/codex" CLIO_TAIL_BACKFILL=1 bash "$ROOT/utils/CLIO/clio-codex-tail.sh" >/dev/null
echo "d-ide: rows=$(rows "$h")"; jq -r '"  stored: " + (.prompt|gsub("\n";"\\n"))' "$h/.claude/prompt-log.jsonl"
# e. default threshold via the hook
for p in "Run the CLIO suites again now" "push it"; do h=$(home_for "e-$RANDOM"); jq -nc --arg p "$p" '{session_id:"s1",prompt:$p}' | HOME="$h" bash "$h/.claude/hooks/clio-capture.sh" --agent claude-code >/dev/null 2>&1; echo "e-threshold: '${p}' (${#p} chars) rows=$(rows "$h")"; done
