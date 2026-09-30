---
name: clio
description: Install, verify, or uninstall prompt capture for Claude Code, ZCode, Codex, and Agy — one shared writer logs every submitted prompt to a centralized JSONL and optionally renders it into a readable Markdown note.
---

# CLIO

CLIO installs a shared capture writer and per-agent registrations that append every
submitted prompt — from Claude Code, ZCode, Codex (VS Code / CLI), and Agy — to one
centralized JSONL: `~/.claude/prompt-log.jsonl` (the `~/.claude` name is historical;
it is the cross-agent log). An optional exporter renders that JSONL as Markdown at a
location you choose. Capture stays fast; formatting happens later, on demand or on a
schedule.

## What gets logged

One line per prompt, from every registered agent:

```json
{"timestamp":"2026-07-09T18:42:11Z","repo":"hypercart","branch":"main","machine":"fixture","agent":"claude-code","session_id":"abc123","prompt":"..."}
```

`agent` is one of `claude-code`, `zcode`, `codex`, `agy`. Rows written before the
`agent` field existed render as `claude-code` (display only — the stored rows are
never rewritten). The dedup ID stays `session_id:timestamp` for every agent.

## Install

Run once (macOS/Linux), either from the root of a CLIO checkout or from an installed
`clio` skill directory — the resolver below finds CLIO's source files in both layouts.
CLIO requires `jq` (the Codex and Agy tailers additionally use `python3`):

```bash
command -v jq >/dev/null 2>&1 || { echo "jq is required. Install it: brew install jq (macOS) / apt install jq (Linux)"; return 1 2>/dev/null || exit 1; }

# --- resolve CLIO's source files (checkout OR installed skill dir) ----------
# In a checkout the scripts live under utils/CLIO/; in an installed skill they
# sit beside INSTALL.md with no prefix. Export CLIO_SRC yourself to override.
if [ -z "${CLIO_SRC:-}" ]; then
  for c in "$PWD/utils/CLIO" "$PWD" \
           "$HOME/.claude/skills/clio" \
           "$(git rev-parse --show-toplevel 2>/dev/null)/utils/CLIO" \
           "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/clio"; do
    [ -f "$c/prompt-log-to-md.sh" ] && { CLIO_SRC="$c"; break; }
  done
fi
[ -n "${CLIO_SRC:-}" ] || { echo "CLIO source not found — set CLIO_SRC to the folder holding prompt-log-to-md.sh"; return 1 2>/dev/null || exit 1; }

mkdir -p ~/.claude/hooks

# --- shared capture writer (one append path for every agent) ----------------
cat > ~/.claude/hooks/clio-capture.sh << 'EOF'
#!/bin/bash
# CLIO shared capture writer (GH-139): one append path for every agent adapter.
#
# Usage:
#   clio-capture.sh --agent <claude-code|zcode|codex|agy>            # hook mode: one JSON object on stdin
#   clio-capture.sh --agent <name> --record                          # tailer mode: one complete JSON row on stdin
#
# Legacy contract (SQLite mode returns nonzero if no durable receipt is possible):
#   exit 0 — row appended, or deliberately skipped (filters, validation, ID
#            collision). Capture NEVER blocks the calling agent.
#   exit 2 — usage error (missing/invalid --agent or unknown option).
#   exit 3 — append lock busy (tailer mode only; the caller must NOT advance
#            its cursor — retry next tick).
#
# Every row is normalized to UTC second precision before its ID is derived:
#   clio:id = session_id:timestamp   (timestamp = YYYY-MM-DDTHH:MM:SSZ)
# A same-session, same-second collision suppresses the second append and logs
# a content-free trace — a permanent drop with an audit line, never a duplicate.
set -euo pipefail

errlog="$HOME/.claude/prompt-log-errors.log"
LOG="$HOME/.claude/prompt-log.jsonl"
LOCK="$HOME/.claude/prompt-log.lock"
mkdir -p "$HOME/.claude" 2>/dev/null || true
ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
minchars="${CLIO_MIN_PROMPT_CHARS:-100}"

AGENT=""; RECORD=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --agent) [ "$#" -ge 2 ] || { echo "$ts clio-capture: --agent requires a value" >> "$errlog"; exit 2; }; AGENT="$2"; shift 2 ;;
    --record) RECORD=1; shift ;;
    --*) echo "clio-capture: unknown option $1" >&2; exit 2 ;;
    *) echo "clio-capture: unexpected argument $1" >&2; exit 2 ;;
  esac
done

diag() { echo "$ts clio-capture[$AGENT]: $*" >> "$errlog"; }

case "$AGENT" in
  claude-code|zcode|codex|agy) ;;
  *) echo "$ts clio-capture: missing or invalid --agent (got '$AGENT')" >> "$errlog"; exit 2 ;;
esac

if ! command -v jq >/dev/null 2>&1; then diag "jq not found — row not logged"; exit 0; fi

machine=$(scutil --get ComputerName 2>/dev/null || hostname -s 2>/dev/null || hostname)
project_dir="${CLAUDE_PROJECT_DIR:-${ZCODE_PROJECT_DIR:-$PWD}}"
repo=$(basename "$(git -C "$project_dir" rev-parse --show-toplevel 2>/dev/null || echo "$project_dir")")
branch=$(git -C "$project_dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

input=$(cat)

# Adapter + cleaning + capture filters + validation, in one jq pass.
# Hook mode accepts the documented key plus likely client variants and falls
# back to the session-id environment variable; tailer (--record) rows carry
# their own timestamp/repo/branch/machine. Wrong-typed or missing keys never
# produce a row with an empty prompt or session id — they are dropped here.
# (The jq result is captured via a plain assignment + rc check: bash 3.2
# cannot parse a multi-line command substitution inside an if condition, and
# a backslash-newline inside $() breaks it too — the defect class GH-156
# documented. CLIO must parse on the stock macOS interpreter.)
jq_rc=0
row=$(printf '%s' "$input" | jq -rc --arg ts "$ts" --arg agent "$AGENT" --arg min "$minchars" --arg env_sid "${CLAUDE_SESSION_ID:-}" --arg machine "$machine" --arg repo "$repo" --arg branch "$branch" --argjson record "$RECORD" '
  def clean_prompt:
    gsub("(?i)<(ide_selection|ide_opened_file|system-reminder|task-notification|local-command-stdout|local-command-caveat|command-name|command-message|command-args|command-contents|function_results|ADDITIONAL_METADATA|USER_SETTINGS_CHANGE|tool-use-id|status|output-file|event|cross-session-message|job|usage|tool_uses|SYSTEM_MESSAGE|CONTEXT_SUMMARY|ARTIFACT)[^>]*>.*?</\\1>"; ""; "gms")
    | gsub("(?i)</?USER_REQUEST>"; ""; "g")
    | gsub("(?im)^>?[ \\t]*\"?(Ran command:|Viewed |Used tool:|The user has approved this document\\.)[^\\n]*\\n?"; ""; "g")
    | gsub("\\n[ \\t]*\\n[ \\t]*\\n+"; "\n\n")
    | sub("^\\s+"; "") | sub("\\s+$"; "");
  def textval: (if type == "string" then . else "" end);
  (if $record == 1 then ((.prompt // "") | textval) else (((.prompt // .message // .user_prompt) // "") | textval) end) as $raw
  | (if $record == 1 then ((.session_id // "") | textval) else (((.session_id // "") | textval) as $s | (if ($s | length) > 0 then $s else $env_sid end)) end) as $sid
  | ($raw | clean_prompt) as $cleaned
  | ($min | tonumber) as $minn
  | select($raw | test("<task-notification>|\\[SYSTEM NOTIFICATION - NOT USER INPUT\\]|RELAY AUTOMATION"; "i") | not)
  | select(($cleaned | length) >= $minn)
  | select(($sid | length) > 0)
  | select(($cleaned | length) > 0)
  | (if $record == 1 then ((.timestamp // "") | textval) else $ts end) as $rts
  | ($rts | sub("\\.[0-9]+"; "") | (if endswith("Z") then .[0:19] + "Z" else . end)) as $nts
  | select(($nts | length) == 20)
  | ((if $record == 1 then ((.machine // "") | textval) else "" end) as $rm
     | (if ($rm | length) > 0 then $rm else $machine end)) as $mm
  | {timestamp: $nts,
     repo: (if $record == 1 then ((.repo // "") | textval) else $repo end),
     branch: (if $record == 1 then ((.branch // "") | textval) else $branch end),
     machine: $mm,
     agent: $agent,
     session_id: $sid,
     prompt: $cleaned}
') || jq_rc=$?
if [ "$jq_rc" -ne 0 ]; then
  diag "malformed input — row not logged"
  exit 0
fi

if [ -z "$row" ]; then
  diag "row dropped (capture filter, validation, or unusable payload)"
  exit 0
fi

# --- serialized scan-suppress-append (one writer at a time) -----------------
# CLIO_SQLITE_V1: a switched writer never appends to the legacy authority.
sqlite_capture() {
  local cfg="${CLIO_CONFIG:-$HOME/.claude/clio-storage.json}"
  [ -f "$cfg" ] || return 1
  local helper="$(dirname "$0")/clio-store.py"
  # Preserve optional source context without changing the legacy seven-field row.
  local sqlite_row
  sqlite_row=$(printf '%s' "$input" | jq -c --argjson base "$row" \
    --arg cwd "$project_dir" --argjson record "$RECORD" '
    $base + {checkout:(if $record == 1 then (.cwd // .checkout // "") else $cwd end),
      repo_slug:(.repo_slug // ""), references:(.references // []), extras:(.extras // {})}')
  if printf '%s' "$sqlite_row" | python3 "$helper" capture >/dev/null; then
    return 0
  else
    local rc=$?
    diag "SQLite capture failed (rc=$rc); no success receipt"
    return "$rc"
  fi
}
if [ -f "${CLIO_CONFIG:-$HOME/.claude/clio-storage.json}" ]; then
  sqlite_capture
  exit $?
fi

acquire_lock() {
  # Give up after ~10s (tailers then defer the chunk; hooks never block).
  # The stale-break threshold (60s) MUST far exceed the give-up window, and
  # the give-up check runs FIRST — otherwise a writer that waited the full
  # window would break a legitimately held lock the moment it crossed the
  # staleness boundary.
  waited=0
  while ! mkdir "$LOCK" 2>/dev/null; do
    if [ "$waited" -ge 50 ]; then return 3; fi
    now=$(date +%s)
    # A lock without a readable born file falls back to the dir mtime, so a
    # SIGKILLed holder (or a failed born write) can never deadlock capture.
    born=$(cat "$LOCK/born" 2>/dev/null || stat -f %m "$LOCK" 2>/dev/null || stat -c %Y "$LOCK" 2>/dev/null || echo "$now")
    if [ $((now - born)) -gt 60 ]; then
      rm -rf "$LOCK"
      diag "broke a stale append lock"
      continue
    fi
    sleep 0.2
    waited=$((waited + 1))
  done
  date +%s > "$LOCK/born" 2>/dev/null || true
  return 0
}
release_lock() { rm -rf "$LOCK"; }

if ! acquire_lock; then
  # The lock belongs to another writer — leave it exactly as found.
  diag "append lock busy — row not logged"
  if [ "$RECORD" -eq 1 ]; then exit 3; fi
  exit 0
fi

# A writer may have waited while activation held this lock. Recheck before append.
if [ -f "${CLIO_CONFIG:-$HOME/.claude/clio-storage.json}" ]; then
  release_lock
  sqlite_capture
  exit $?
fi

row_id=$(printf '%s' "$row" | jq -r '(.session_id) + ":" + (.timestamp)')
if [ -s "$LOG" ]; then
  # Capture the full ID set BEFORE matching: grep -q early-exit would SIGPIPE
  # jq under pipefail and a real collision would read as "no collision".
  log_ids=$(jq -Rr 'fromjson? | ((.session_id // "") + ":" + (.timestamp // ""))' "$LOG" 2>/dev/null || true)
  case $'\n'"$log_ids"$'\n' in *$'\n'"$row_id"$'\n'*)
    diag "id-collision suppressed: $row_id"
    release_lock
    exit 0
    ;;
  esac
fi
printf '%s\n' "$row" >> "$LOG"
release_lock
exit 0
EOF
chmod +x ~/.claude/hooks/clio-capture.sh

# --- Claude Code shim (thin; keeps the existing settings.json registration) -
cat > ~/.claude/hooks/log-prompt.sh << 'EOF'
#!/bin/bash
# Claude Code shim — delegates to the shared CLIO writer. The registration in
# ~/.claude/settings.json still names this path, so upgrades need no settings
# change and the uninstall procedure is unchanged.
exec "$(dirname "$0")/clio-capture.sh" --agent claude-code
EOF
chmod +x ~/.claude/hooks/log-prompt.sh

SETTINGS=~/.claude/settings.json
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"

if grep -q "log-prompt.sh" "$SETTINGS" 2>/dev/null; then
  echo "Hook already registered in $SETTINGS — skipping."
else
  jq '.hooks.UserPromptSubmit = ((.hooks.UserPromptSubmit // []) + [{"hooks":[{"type":"command","command":"$HOME/.claude/hooks/log-prompt.sh"}]}])' \
    "$SETTINGS" > "$SETTINGS.tmp" && mv "$SETTINGS.tmp" "$SETTINGS"
  echo "Hook registered in $SETTINGS."
fi

# --- ZCode registration (config-file hooks; disabled unless enabled: true) --
ZCONFIG="$HOME/.zcode/cli/config.json"
if [ -d "$HOME/.zcode" ] || [ "${1:-}" = "--with-zcode" ]; then
  mkdir -p "$HOME/.zcode/cli"
  [ -f "$ZCONFIG" ] || echo '{}' > "$ZCONFIG"
  if grep -q "clio-capture.sh" "$ZCONFIG" 2>/dev/null; then
    echo "ZCode hook already registered in $ZCONFIG — skipping."
  else
    if jq '.hooks = ((.hooks // {}) + (if (.hooks | has("enabled") | not) then {enabled: true} else {} end))
         | .hooks.events = ((.hooks.events // {}) + {UserPromptSubmit: (((.hooks.events.UserPromptSubmit // [])
             + [{hooks: [{type: "command", command: "$HOME/.claude/hooks/clio-capture.sh --agent zcode"}]}]))})' \
      "$ZCONFIG" > "$ZCONFIG.tmp" && mv "$ZCONFIG.tmp" "$ZCONFIG"; then
      echo "ZCode hook registered in $ZCONFIG."
    else
      echo "ZCode registration failed — config untouched." >&2
    fi
  fi
fi

install -m 0755 "$CLIO_SRC/clio-store.py" ~/.claude/hooks/clio-store.py
install -m 0755 "$CLIO_SRC/prompt-log-to-md.sh" ~/.claude/hooks/prompt-log-to-md.sh

echo "✅ Installed. Smoke test (uses the Claude shim; expects agent=claude-code):"
echo '{"prompt":"a substantive session-opening prompt that runs well past the one hundred character capture threshold on its own","session_id":"install-check"}' | ~/.claude/hooks/log-prompt.sh
tail -1 ~/.claude/prompt-log.jsonl
```

The ZCode registration fires only when a `~/.zcode` directory already exists (or you
pass `--with-zcode`), so installing CLIO on a machine without ZCode changes nothing
there.

**Pinning the live ZCode payload (one-shot probe).** The writer accepts the documented
`prompt`/`session_id` keys plus likely variants and falls back to the session-id
environment variable, so capture works even if the client's payload drifts. To pin the
exact payload a client posts, register this diagnostic hook for one prompt, submit any
prompt, then remove it:

```bash
cat > ~/.claude/hooks/clio-hook-probe.sh << 'EOF'
#!/bin/bash
umask 077
input=$(cat); printf '%s' "$input" > "$HOME/clio-hook-payload.json"
exit 0
EOF
chmod +x ~/.claude/hooks/clio-hook-probe.sh
jq '.hooks.events.UserPromptSubmit = (((.hooks.events // {}).UserPromptSubmit // [])
  + [{hooks: [{type: "command", command: "$HOME/.claude/hooks/clio-hook-probe.sh"}]}])' \
  ~/.zcode/cli/config.json > /tmp/probe-config.json && mv /tmp/probe-config.json ~/.zcode/cli/config.json
# …submit one prompt in the client, then read ~/clio-hook-payload.json and unregister the probe…
```

## Verify (real session)

Start a new Claude Code or ZCode session anywhere, submit any prompt, then:

```bash
tail -f ~/.claude/prompt-log.jsonl
```

Each captured line carries `"agent":"claude-code"` or `"agent":"zcode"`.

## SQLite history and seven-day view (opt-in pilot)

Python **3.8+** is required for this mode. The installer above copies `clio-store.py`
beside the shared writer. Existing capture remains JSONL until explicit activation;
installing these scripts alone does not migrate private history. Keep the old shared
Markdown note and tailer state files. Do not point a local rolling view at the shared
historical note: it may contain other devices' only copies.

The database defaults to `~/.claude/prompt-log.sqlite3`; pass `--db /private/path/history.sqlite3`
**before** a subcommand to use another local path. Files are private. Never put a live
SQLite database, its WAL, or its pending directory in a synchronized folder.

1. Install the updated shared writer/helper and tailers, and verify all registrations
   use that shared writer. Inventory other installed copies before cutover. Preserve
   your source JSONL, old Markdown, registrations and tailer states.
2. Initialize and import while legacy capture continues:

   ```bash
   python3 ~/.claude/hooks/clio-store.py init
   python3 ~/.claude/hooks/clio-store.py import-jsonl ~/.claude/prompt-log.jsonl
   ```

   Import commits at most 1,000 complete lines per invocation. Repeat until
   `remaining_bytes` is zero; investigate after ten batches instead of leaving an
   unbounded retry loop. `--max-records` selects a different explicit batch size.
   Complete invalid lines are retained privately in `source_lines.quarantine`, with
   line/hash/reason accounting; an unterminated tail stays pending. Replaced or altered
   sources fail closed; use an explicit new `--source label` only after inspecting
   the replacement. Repeated valid rows are deduplicated while every occurrence is counted.
3. Verify nonempty source parity, then activate. Activation takes the existing append
   lock without breaking another owner's lock, imports at most 100 final arrivals,
   verifies parity/integrity, saves an untouched source backup and atomically writes
   `~/.claude/clio-storage.json`. If backlog remains, repeat online import first.
   Import, parity and backup loops check a five-second cutover deadline. Slow storage
   may extend an individual I/O call; a budget failure leaves legacy mode active.
   If a large source repeatedly exceeds the budget, pause submissions for an offline
   migration review instead of bypassing the gate. A failed backup may leave a private
   partial `.pre-sqlite-*` file; activation has not completed unless config exists.

   ```bash
   python3 ~/.claude/hooks/clio-store.py verify-import ~/.claude/prompt-log.jsonl
   python3 ~/.claude/hooks/clio-store.py activate
   ```

   For a genuinely fresh installation with **no legacy source file**, initialize then
   use `activate --fresh`; this does not bypass migration checks on an existing file.
   A busy lock or invalid source prevents activation. A queued legacy writer rechecks
   activation after obtaining its lock. Do not manually create the configuration to
   bypass these gates.
4. Reuse the existing one-minute exporter job with these ProgramArguments (one value
   per launchd `<string>`); use a **new** Markdown path:

   ```bash
   ~/.claude/hooks/prompt-log-to-md.sh --sqlite \
     --markdown "$HOME/.claude/prompt-log-recent.md" \
     --jsonl "$HOME/.claude/prompt-log-compat.jsonl"
   ```

   This drains durable pending receipts then renders the latest 168 hours, even with
   no new capture. Hook capture waits at most 500 ms for SQLite contention; accepted
   queued rows survive in `<database>.pending/` and appear after recovery. Run `drain`
   manually to inspect `drained`/`pending`; investigate a backlog persisting across
   two scheduled runs. A receipt cannot be persisted → nonzero error, never a false
   success. Diagnostics: `~/.claude/prompt-log-errors.log`, plus existing job stderr.
5. Point Rebalance/Daily's existing source configuration (`clio_prompt_log_path` or
   `REBALANCE_CLIO_PROMPT_LOG` in the **scheduled process's** environment) to the full
   chronological compatibility JSONL. Verify that effective configuration in Rebalance.
   Do not substitute the rolling Markdown or snapshot transport file. The old local
   JSONL stops growing after activation and remains a migration/rollback source.

The rolling view uses UTC, newest timestamp first with record-ID tie-breaking. Its
inclusive window is `[cutoff - 168 hours, cutoff]`; future-dated rows remain in the
DB but are omitted. `project --cutoff 2026-09-30T00:00:00Z` provides repeatable output.
Stdout reports row/byte counts; large prompts are not truncated. Legacy exporter
`--status`, `--backfill`, `--repair`, cursors and permanent receipts still apply only
to legacy mode and are never repurposed as rolling-window membership.

### Read-only agent lookup

```bash
python3 ~/.claude/hooks/clio-store.py query --repo rebalanceOS \
  --since 2026-09-23T00:00:00Z --until 2026-09-30T00:00:00Z \
  --text 'frozen packet' --limit 20
python3 ~/.claude/hooks/clio-store.py query --device 'MBP 14"' --agent codex
python3 ~/.claude/hooks/clio-store.py query --session SESSION --offset 20 --limit 20
python3 ~/.claude/hooks/clio-store.py query --record-id clio1-RECORD_HASH
python3 ~/.claude/hooks/clio-store.py query \
  --reference https://github.com/HiQS-Labs/XYZ-CLIO/issues/3 --explain
```

Queries use SQLite `mode=ro` and `query_only`, never initialize a missing DB, and use
bound parameters. Text is a literal, case-sensitive substring. Results include
prompt, time, device (`machine`), agent, session, branch, checkout, canonical repo
when supplied, identity, references and extras. `--origin` filters the stable store
owner rather than a mutable human device label. Pagination is timestamp/ID descending;
concurrent new arrivals can shift offsets, so fix a time range for stable paging.

References are **explicit producer metadata**, not inferred task status. A capture
record can include `repo_slug`, `checkout` (or a tailer's `cwd`), `extras`, and:

```json
{"references":[{"type":"issue","url":"https://github.com/HiQS-Labs/XYZ-CLIO/issues/3","relation":"task-context"},{"type":"ledger","repo_slug":"HiQS-Labs/XYZ-forge","row_id":"ROW_ID","relation":"mentioned"}]}
```

Use `type:"pr"` with a qualified `/pull/N` URL. Only `mentioned` and `task-context`
relations are accepted. No status or accepted-start writes occur. Existing client
payloads need not provide these optional fields; unknown historical values remain
unknown. Rebalance's consumer upgrade will carry this provenance through its existing
semantic provider and readonly XYZ status adapter; it is not installed by CLIO.

### Device snapshots and coverage

```bash
python3 ~/.claude/hooks/clio-store.py export-device /private/staging/clio.jsonl
python3 ~/.claude/hooks/clio-store.py import-device /private/received/clio.jsonl
```

A snapshot is one atomic file: versioned first-line manifest (owner UUID, generation
UTC, count and content hash), followed by source records. The caller can stage it at
`devices/<owner-uuid>/clio.jsonl` for the existing Git Pulse Sync publisher. CLIO never
commits, pushes or creates a timer. That integration is blocked on Rebalance #282's
file ownership/publisher work; a local query is **not** proof of complete fleet coverage.
Read accepted snapshot receipts from `device_imports` to see the source generation and
receipt time. Expected/missing device reporting belongs in the downstream consumer.

Export selects only this store's owner UUID; receiving a snapshot never changes its
origin or ID, and foreign rows are not re-exported as local. `legacy-adopted` denotes
ownership assigned during import, **not** recovered historical hardware identity.
Identical legacy files separately adopted by different stores may have different IDs;
the old data cannot prove whether they were retries or separate submissions. Original
machine/agent values and namespaced extra metadata remain intact. No live WAL sync.

### Backup, restore and rollback

```bash
python3 ~/.claude/hooks/clio-store.py drain
python3 ~/.claude/hooks/clio-store.py backup /private/backups/clio-snapshot.sqlite3
```

`backup` uses SQLite's online backup API and refuses an existing destination. It is a
snapshot of committed history: pause submissions/maintenance and require zero pending
receipts for a complete cutover recovery point. Preserve the private config and any
pending receipts too. Restore to a **new** local DB path, inspect it with `--db ... query`
and `PRAGMA integrity_check`, reconcile any later arrivals, then update the private
configuration atomically while writers are quiesced. Never replace a live database
with a raw copy of its main file while WAL is active.

For rollback, first pause submissions and scheduled tailers/exporter. Drain receipts,
back up SQLite/config/source state, and generate a full chronological rollback JSONL
at a **new** path using `project --jsonl /private/rollback.jsonl`. Verify nonempty
row counts and identities before selecting that complete file as the legacy log.
Preserve the original log under its backup name; disable the SQLite config only while
writers are stopped. Resume the legacy writer and its matching consumers together.
Keep the SQLite store and tailer cursors so SQLite-era events are not discarded.
Legacy same-second ID suppression remains a legacy limitation; the preserved SQLite
backup is the authoritative recovery copy for those collisions. Do not retire it
until all writers/readers/queued work and the rollback window are accounted for.

## Optional: export to human-readable Markdown

The exporter appends only entries not already identified in the note, with newest
ones immediately below `<!-- CLIO:ENTRIES -->`. It preserves everything above that
marker, reconciles full entries found in matching conflict siblings, and quarantines
those siblings under `.clio-reconciled/`. Each entry's metadata line reads
`machine · branch · agent` (rows without a stored `agent` render as `claude-code`).

Its cursor (`~/.claude/prompt-log-to-md.state`) is only a scan optimization. The
source-owned `~/.claude/prompt-log-manifest.txt` is an append-only delivery receipt:
one rendered `clio:id` per line, no prompt text. It remains if the cursor is deleted.

**Run it** — default location:

```bash
~/.claude/hooks/prompt-log-to-md.sh
```

**Run it** — custom location, for example an Obsidian vault:

```bash
~/.claude/hooks/prompt-log-to-md.sh ~/vault/_meta/prompt-log/prompt-log.md
```

**Preview conflict recovery without changing the note or moving files:**

```bash
CLIO_RECONCILE_DRY_RUN=1 ~/.claude/hooks/prompt-log-to-md.sh ~/vault/_meta/prompt-log/prompt-log.md
```

The first run creates a fixed header and marker, then one `## <REPO>` block per
prompt. To sync on a schedule, point a launchd job (macOS) or cron entry at the
same exporter command and output path. On a shared synced file, run it on every
machine; each device adds its own local prompts without regenerating the note.

### Auto-sync every 1 minute (macOS launchd)

Replace `OUT_PATH` with your chosen output file:

```bash
OUT_PATH="$HOME/vault/_meta/prompt-log/prompt-log.md"
PLIST=~/Library/LaunchAgents/com.claude.prompt-log-to-md.plist

cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.prompt-log-to-md</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HOME/.claude/hooks/prompt-log-to-md.sh</string>
        <string>$OUT_PATH</string>
    </array>
    <key>StartInterval</key>
    <integer>60</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/.claude/prompt-log-to-md.out.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.claude/prompt-log-to-md.err.log</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null
launchctl load "$PLIST"
```

Check it is running:

```bash
launchctl list | grep com.claude.prompt-log-to-md
```

Stop and remove it:

```bash
launchctl unload ~/Library/LaunchAgents/com.claude.prompt-log-to-md.plist
rm ~/Library/LaunchAgents/com.claude.prompt-log-to-md.plist
rm -f ~/.claude/prompt-log-to-md.out.log ~/.claude/prompt-log-to-md.err.log
```

## Optional: Codex capture (VS Code / CLI)

Codex has no prompt-submit hook, so a read-only tailer turns user prompts from Codex
session rollouts into JSONL rows. It parses only `event_msg`/`user_message` records,
never takes prompt text from `response_item` entries (where injected context can be
combined with user input), and never writes to the source. Run once from a CLIO checkout
or an installed `clio` skill directory (requires `jq` and `python3`). This is a separate
shell from the main install, so it re-resolves `CLIO_SRC` unless you exported it:

```bash
if [ -z "${CLIO_SRC:-}" ]; then
  for c in "$PWD/utils/CLIO" "$PWD" "$HOME/.claude/skills/clio"; do
    [ -f "$c/clio-codex-tail.sh" ] && { CLIO_SRC="$c"; break; }
  done
fi
[ -n "${CLIO_SRC:-}" ] || { echo "CLIO source not found — set CLIO_SRC to the folder holding clio-codex-tail.sh"; return 1 2>/dev/null || exit 1; }

install -m 0755 "$CLIO_SRC/clio-codex-tail.sh" ~/.claude/hooks/clio-codex-tail.sh
```

First run starts **now** and persists that capture boundary, even before a sessions
folder exists. Later polls capture eligible first prompts from newly discovered root
sessions, including prompts completed between polls. Existing pre-boundary history
and inherited subagent prompts are excluded. Set `CLIO_TAIL_BACKFILL=1` for an
explicit history import from **previously unseen root files**; known files retain
their existing policy. Source timestamps must be valid and timezone-aware.

Upgrading preserves legacy pending records on their original file. Replacement or
truncation switches those legacy files to the capture boundary, so previously
skipped history is not imported; older pending records cannot be recovered
automatically once that file provenance is lost. Clean polling delays retain the
boundary. An abandoned tailer lock after a forced kill still requires operator
recovery after verifying no tailer is running; this update adds no lock supervisor.

Schedule it every minute:

```bash
PLIST=~/Library/LaunchAgents/com.claude.clio-codex-tail.plist
cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.clio-codex-tail</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HOME/.claude/hooks/clio-codex-tail.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>60</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/.claude/clio-codex-tail.out.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.claude/clio-codex-tail.err.log</string>
</dict>
</plist>
EOF
launchctl unload "$PLIST" 2>/dev/null; launchctl load "$PLIST"
```

## Optional: Agy capture (Antigravity CLI)

Agy has no prompt-submit hook either; the same tailer pattern reads its per-conversation
FULL transcript JSONLs (`brain/<id>/.system_generated/logs/transcript_full.jsonl` — the
plain `transcript.jsonl` truncates large text), capturing only rows where `source` is
`USER_EXPLICIT` and `type` is `USER_INPUT`:

```bash
if [ -z "${CLIO_SRC:-}" ]; then
  for c in "$PWD/utils/CLIO" "$PWD" "$HOME/.claude/skills/clio"; do
    [ -f "$c/clio-agy-tail.sh" ] && { CLIO_SRC="$c"; break; }
  done
fi
[ -n "${CLIO_SRC:-}" ] || { echo "CLIO source not found — set CLIO_SRC to the folder holding clio-agy-tail.sh"; return 1 2>/dev/null || exit 1; }

install -m 0755 "$CLIO_SRC/clio-agy-tail.sh" ~/.claude/hooks/clio-agy-tail.sh
```

Then schedule it like the Codex tailer (label `com.claude.clio-agy-tail`, script
`$HOME/.claude/hooks/clio-agy-tail.sh`, logs `clio-agy-tail.*.log`).

## Uninstall

SQLite users: preserve the database, private configuration and pending receipts;
finish or explicitly preserve pending recovery before removing the helper.

This removes only CLIO's own registrations and installed files; unrelated hooks in
either client's config are untouched.

```bash
# Claude Code: remove the shim registration
tmp=$(mktemp)
jq 'if (.hooks // null) == null then . else
      (.hooks.UserPromptSubmit //= [])
      | .hooks.UserPromptSubmit = (.hooks.UserPromptSubmit
          | map(.hooks = ((.hooks // []) | map(select(((.command // "") == "$HOME/.claude/hooks/log-prompt.sh") | not))))
          | map(select((.hooks // []) | length > 0)))
      | if (.hooks.UserPromptSubmit // []) == [] then del(.hooks.UserPromptSubmit) else . end
    end' \
  ~/.claude/settings.json > "$tmp" && mv "$tmp" ~/.claude/settings.json

# ZCode: remove the writer registration and drop the enabled gate if CLIO set it
if [ -f ~/.zcode/cli/config.json ]; then
  tmp=$(mktemp)
  jq 'if (.hooks // null) == null then . else
        if (.hooks.events // null) == null then . else
          (.hooks.events.UserPromptSubmit //= [])
          | .hooks.events.UserPromptSubmit = (.hooks.events.UserPromptSubmit
              | map(.hooks = ((.hooks // []) | map(select(((.command // "") | contains("clio-capture.sh")) | not))))
              | map(select((.hooks // []) | length > 0)))
          | if (.hooks.events.UserPromptSubmit // []) == [] then del(.hooks.events.UserPromptSubmit) else . end
          | if ((.hooks.events // {}) == {}) then del(.hooks.events) else . end
        end
      end' \
    ~/.zcode/cli/config.json > "$tmp" && mv "$tmp" ~/.zcode/cli/config.json
fi

# launchd jobs (only if installed)
for label in com.claude.clio-codex-tail com.claude.clio-agy-tail; do
  plist=~/Library/LaunchAgents/$label.plist
  [ -f "$plist" ] && { launchctl unload "$plist" 2>/dev/null; rm "$plist"; }
done

rm ~/.claude/hooks/log-prompt.sh
rm -f ~/.claude/hooks/clio-capture.sh ~/.claude/hooks/clio-store.py ~/.claude/hooks/clio-hook-probe.sh \
      ~/.claude/hooks/clio-codex-tail.sh ~/.claude/hooks/clio-agy-tail.sh \
      ~/.claude/hooks/prompt-log-to-md.sh ~/.claude/prompt-log-to-md.state \
      ~/.claude/prompt-log-codex-tail.state ~/.claude/prompt-log-agy-tail.state \
      ~/.claude/prompt-log-manifest.txt ~/.claude/prompt-log-errors.log \
      ~/clio-hook-payload.json
```

## Notes

- **Scope:** both registrations are user-level, so one log covers every project and every registered agent.
- **Machine, branch, and agent:** all three are recorded with each prompt for later context; the agent app is the new field (GH-139), the device name is unchanged.
- **Legacy timestamps:** the raw JSONL and every `clio:id` stay **UTC** — the ID is `session_id:timestamp`, so localizing it would change all IDs, break dedup, and re-emit the note as duplicates. Only the *displayed* line is localized (`2026-07-19 14:27:50 PDT`). Conversion uses `python3` (`datetime.astimezone()`), **not** jq. Without `python3` the display falls back to UTC.
- **Capture filtering (permanent):** the writer skips two classes of prompt outright, for every agent:
  - *Automated turns* — anything containing `<task-notification>` or the `[SYSTEM NOTIFICATION - NOT USER INPUT]` preamble (background-task and monitor events). Matched on the raw prompt before tag stripping.
  - *Short prompts* — under `CLIO_MIN_PROMPT_CHARS` (default **100**) after injected blocks are stripped, so `yes` / `push it` are dropped while substantive session-opening prompts are kept. Set `CLIO_MIN_PROMPT_CHARS=0` to capture everything again.

  This is a **drop, not a hide** — unlike `PROMPT_LOG_EXCLUDE` below, a skipped prompt is unrecoverable. Prefer the render-side filter if you might want the text back later. Covered by `test/clio-capture.sh`.
- **Legacy same-second collisions:** two substantive prompts in the same session within one second share an ID; the second is suppressed and traced to the error log (content-free) rather than written as a duplicate.
- **Legacy render filtering (reversible):** `PROMPT_LOG_EXCLUDE` defaults to `file-based relay|cross-agent dependency drift`; matching text stays in raw JSONL but is omitted from the Markdown (reported as `state: excluded` by `--status`). Set it empty to render all prompts.
- **Legacy resetting:** deleting the state file rescans JSONL, but ID-based note deduplication prevents a duplicate rendered entry. The manifest is intentionally independent of that cursor.
- **Errors:** legacy hooks skip invalid/filtered prompts; tailers return nonzero on retryable failures. SQLite capture acknowledges only committed or durably queued rows and returns nonzero when no receipt can be saved. Failures and drop diagnostics go to `~/.claude/prompt-log-errors.log`; tailers surface lock/parse failures there too and never advance a cursor over undelivered rows; a manifest receipt failure is reported but never rolls back a successful export.
