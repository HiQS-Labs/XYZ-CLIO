> **SQLite pilot:** opt-in full-history SQLite capture, read-only lookup, a rolling
> 168-hour Markdown view and per-device export are documented in
> [INSTALL.md](utils/CLIO/INSTALL.md#sqlite-history-and-seven-day-view-opt-in-pilot).
> Existing installations stay on JSONL until explicit migration/activation. Fleet
> publishing and Rebalance's provenance upgrade are separate dependent work; no live
> database synchronization or task-status writes are introduced.

# CLIO

A local history of captured prompts across repos and coding agents, with device
and session provenance. Capture filters exclude short and automated turns by default.

CLIO installs a shared capture writer plus per-agent registrations. Each
registered agent sends eligible prompts to one writer. Legacy mode appends JSONL
to: `~/.claude/prompt-log.jsonl`. (The `~/.claude` path is historical; it is
the cross-agent log, not a Claude-only one.)

Supported agents:

| Agent | Mechanism |
| --- | --- |
| Claude Code | `UserPromptSubmit` hook |
| ZCode | `UserPromptSubmit` hook |
| Codex (VS Code / CLI) | rollout-file tailer |
| Agy (Antigravity CLI) | transcript tailer |

Each line records a timestamp, repo name, git branch, machine name, agent,
session ID, and the prompt text — with auto-injected context (like
`<ide_selection>` blocks) stripped, so it is a record of what you actually
typed.

```json
{"timestamp":"2026-07-09T18:42:11Z","repo":"hypercart","branch":"main","machine":"fixture","agent":"claude-code","session_id":"abc123","prompt":"..."}
```

Rows written before the `agent` field existed render as `claude-code` — display
only; stored rows are never rewritten. Legacy dedup uses `session_id:timestamp`. SQLite uses a versioned content hash
including origin, agent, prompt and metadata, preserving different same-second prompts.

An optional exporter renders the JSONL as human-readable Markdown — newest
entry first — at any location you choose, such as a note in an Obsidian vault.
It runs on demand or on a 1-minute `launchd` schedule (macOS). Capture stays
fast; formatting happens later.

## Why

If you use AI coding agents across many repos, machines, and vendors, there is
no built-in way to see everything you have asked them over time. This gives you
one file you can grep, sync to notes, or keep as an audit trail.

- **Cross-device recall.** Answer "where and when did I ask for X on this
  project?" without digging through per-machine session histories.
- **Branch-level recall.** Every entry records the branch checked out at prompt
  time, so an ask can be traced back to its branch even after that branch is
  merged or deleted.
- **Cross-agent, cross-project AI memory.** Point the Markdown export at an
  Obsidian vault; once that vault is indexed for retrieval, an assistant can
  search across what you asked your coding agents to do, alongside your other
  notes.
- **A training corpus of how you actually work.** Thousands of real prompts,
  each stamped with repo, branch, agent, and time, are a labeled record of the
  work you keep repeating. Mine it to find the asks you type over and over,
  then turn those into skills, slash commands, or hooks — or fine-tune or
  few-shot a model on your own phrasing so an agent drafts the next one the way
  you would have written it.

## Requirements

- macOS or Linux
- [`jq`](https://jqlang.org/) — `brew install jq` / `apt install jq`
- Python 3.8+ — for the Codex/Agy tailers and SQLite mode (standard-library SQLite)

## Install

Full install, verify, export, auto-sync, and uninstall instructions are in
[`utils/CLIO/INSTALL.md`](utils/CLIO/INSTALL.md). That file is also the skill
definition (it carries the `name: clio` frontmatter), so a Claude Code install
can invoke it directly.

Run the install steps once, from either the root of this checkout or an installed
`clio` skill directory — the install block resolves CLIO's source files in both
layouts, and honors a `CLIO_SRC` you set yourself.

## Layout

```
utils/CLIO/
  INSTALL.md            # the skill: install / verify / uninstall procedure,
                        # and the source of truth for the capture writer and
                        # the Claude + ZCode shims (embedded as heredocs)
  clio-codex-tail.sh    # Codex rollout tailer
  clio-agy-tail.sh      # Agy transcript tailer
  prompt-log-to-md.sh   # legacy exporter or SQLite drain + projection
  clio-store.py         # SQLite history, query, migration and device exports
test/
  clio-capture.sh       # capture writer + Claude shim, against a throwaway $HOME
  clio-exporter.sh      # exporter behavior, state file, idempotency
  clio-codex-tail.sh    # Codex tailer against a fixture rollout
  clio-agy-tail.sh      # Agy tailer against a fixture transcript
  clio-store.py         # SQLite acceptance and failure cases
  fixtures/clio/        # fixture rollout + transcript
FRONTDOOR.md            # onboarding health board, refreshed by re-running its checks
SHAKEDOWN/              # dated script-path audits of the clio skill
```

The root `README.md` is the only overview; `utils/CLIO/INSTALL.md` is the only
install procedure. There is deliberately no second, skill-local README to drift
out of sync with this one.

The capture writer and the Claude/ZCode shims live as heredocs inside
`INSTALL.md` rather than as standalone scripts. The test harnesses extract them
by marker, so `INSTALL.md` stays the single source of truth and cannot drift
from what the tests exercise.

## Tests

No framework, no dependencies beyond `jq` and `python3`. Each harness runs
against a throwaway `$HOME` and fixture inputs:

```bash
bash test/clio-capture.sh
bash test/clio-exporter.sh
bash test/clio-codex-tail.sh
bash test/clio-agy-tail.sh
python3 test/clio-store.py
```

## Safety

CLIO runs on your machine with a hook that shells out and edits your agent's
`settings.json`. Captured prompts may include sensitive pasted text. JSONL, SQLite, pending
receipts and exports are unencrypted local data. Read the scripts before running them.

## License

CLIO is dual-licensed, matching the rest of the HiQS suite.

**AGPL-3.0-only** is the default and covers nearly every use — see
[`LICENSE`](LICENSE). You may use, study, modify, self-host, and redistribute
CLIO under it at no cost.

A **commercial license** is available if you need to offer a modified CLIO to
third parties over a network, or embed it in a proprietary product, without
publishing your modifications — see
[`LICENSE-COMMERCIAL.md`](LICENSE-COMMERCIAL.md). Terms are negotiated, not
click-through.

This project is provided **"AS IS," WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND**, either express or implied. Use at your own risk.
