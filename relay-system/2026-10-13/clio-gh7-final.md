# RELAY · CLIO GH7 final QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-13.
-->

NEXT: Producer
STATUS: Open
ROUND: 1 / 3

## ▶ TAKE YOUR TURN — read this first (works for ANY agent: Claude, Codex, agy)
1. **Read this whole file** (header, Setup, Ground rules, every block in the Log).
2. **Check it's your turn:** `NEXT` (top) names the role to act. Confirm you are bound to it and the
   last Log block isn't already yours. If not → STOP and reply "wrong window — nudge the <other> window."
3. **Do your role's work** on the artifact named in Setup:
   - **Reviewer:** review vs the Definition of Done → graded findings
     (`[Blocker]`/`[Should]`/`[Nit]`/`[Pass]`), each with a concrete fix → set a **VERDICT**
     (exactly PASS, FAIL, or PARKED) and a **Basis** (explanation). **Review the whole file, not just the diff** (GH-268):
     a beta test had this loop reach `Approved` in two rounds while an independent audit of the same
     branch found 20 issues (1 critical, 4 high) — every one of them in the pre-existing code the
     change sat on, which nobody had read. Pre-existing defects in a file you are touching are IN
     SCOPE; if you find none, say so explicitly rather than leaving it unstated.
     **Declare it: every review block must contain a literal `swept file: yes` or `swept file: no`
     line.** Without it a reviewer that skipped the sweep is indistinguishable in the transcript from
     one that did it and found nothing — which is how the original 20 issues stayed invisible.
     Any `[Pass]` or "verified"/"confirmed" finding MUST
     carry a quoted span or a `file:line` citation — an uncited one is mechanically downgraded to
     `[Unverified — no citation]` (GH-173 B3). Do **not** edit the artifact; only append findings here.
     **A finding that asks for a behaviour change is a generalization unless you can paste the concrete
     input — a row, a value, a `file:line` — that fails under the current code** (GH-681: the gh673
     final QA relay generalized one late-error observation into "or a later invalid identity", the
     Producer implemented it, the same seat `[Pass]`ed it next round, and one historical NULL-URL
     ledger row then blanked every issue). Every `[Blocker]` or `[Should]` requesting a behaviour
     change MUST carry three lines: `Observed input:` (the failing input you saw), `Affected scope:`
     (the input predicate the change would govern), `Falsifier:` (the fixture or data that would show
     the change unnecessary or wrong, and its expected result).
     A `[Blocker]` must cite an observed failure. This is a protocol rule, not a mechanical check —
     the Producer may disposition a request lacking these as `Declined — unproven generalization`.
   - **Producer:** log a disposition for every open finding (Implemented / Modified / Declined + why,
     including `Declined — unproven generalization` for a behaviour-change request that carries no
     `Observed input:` / `Affected scope:` / `Falsifier:`), make the change, then add new work.
4. **Append ONE block** at the very bottom, directly **above** the marker line. Never edit earlier turns.
   Reviewer headings may be `### Reviewer · Round N`, `### Round N · Reviewer · <agent>`, `### Reviewer (<agent>)` (optionally followed by `— rN`), or `### Reviewer — Round N` (optionally followed by `(<agent>)`); follow the heading with a non-empty review body.
5. **Update the header:** flip `NEXT`; set `STATUS` (`Approved` closes — Reviewer only; else `Open`);
   the Producer bumps `ROUND` when opening a new cycle. If the max `ROUND` ends without `Approved`,
   set `STATUS: Escalated`.
6. **Commit only the relay file** (`relay(clio-gh7-final-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: `doc/gh7-clio-forensics.md`, `utils/CLIO/SKILL.md`, `utils/CLIO/clio-query.py`, `utils/CLIO/clio-store.py`, `test/clio-store.py`, README/INSTALL and TESTS-RESULTS/2026-10-13-gh7.
- Reviewer: codex   ·   Producer: claude-a
- Started: 2026-10-13
- Definition of Done: The plan contract and implementation/evidence sections in doc/gh7-clio-forensics.md. Local stdlib developer lookup: grade commensurately, no enterprise machinery. Verify deterministic JSON schema/errors, DRY canonical reader reuse, resolver precedence, chronological task/session evidence, unknown provenance, metadata preservation and unchanged writer semantics. Read full touched files; no test suites in reviewer worktree. All19 storage tests pass after correcting an aged fixture; full five-suite gate follows approval. No deployment or live prompts. Write only this relay thread.

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

### Reviewer · Round 1 · codex

VERDICT: FAIL
Basis: The read-only design and chronological evidence are sound on source inspection, but two measured inputs bypass the promised deterministic JSON error boundary. One small adapter correction is required before approval.
swept file: yes

Read the complete plan, skill, adapter, canonical store (including pre-existing writer/export/recovery code), storage suite, README, INSTALL and all six GH7 evidence logs. Tier 2 source fallback: list_projects returned all 84 projects with has_more=false and no matching CLIO checkout; check_index_coverage for the review paths returned "project not found or not indexed". No graph generation or coverage assurance is available. No git commands, test suites, executable fixtures, live history reads or source edits were performed. Historical diff comparison was unavailable under the no-git instruction.

- [Should] R1 — Preserve the structured error envelope for the observed AttributeError and OverflowError paths. At utils/CLIO/clio-query.py:173 the boundary omits both exceptions. Native query receipt extraction at utils/CLIO/clio-store.py:494 assumes fleet is a mapping; SQLite binding at :488 rejects an integer outside signed 64-bit range, while adapter :119 accepts every nonnegative offset. Both currently terminate with no JSON, contradicting the stable v1 error contract in doc/gh7-clio-forensics.md and SKILL.md. Cheapest fix: translate these failures into the existing content-free error envelope (or narrowly validate the corresponding inputs); retain explicit-DB config bypass and existing writer behavior. Extend an existing acceptance case or record the focused check in the producer's disposable clone; no new suite or framework.
  Observed input: Native config {"db":"<scratch>/review.sqlite3","owner":"fixture","fleet":true} with operation search; separately search --db <scratch>/review.sqlite3 --offset 9223372036854775808.
  Affected scope: Adapter calls that encounter malformed receipt metadata causing AttributeError, or SQLite integer binding overflow from accepted offsets. This does not request changing valid records, storage semantics or fleet reconciliation.
  Falsifier: The same malformed-config and oversized-offset calls should each return exit 2 and one v1 JSON error object with empty records and null journey records. The same database selected with explicit --db and ordinary offset must still bypass malformed unrelated config and return exit 0/status empty. If those results already occur on the reviewed code, this finding is wrong.

  Narrow synthetic probe command (shell setup plus inline Python; probe driver exit 0; only scratch fixtures created, reader subprocesses do not mutate event data):

  ```bash
  export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"
  mkdir -p "$TMPDIR"
  python3 - <<'PYPROBE'
  import json, os, sqlite3, subprocess, sys
  from pathlib import Path
  root = Path.cwd()
  scratch = Path(os.environ['TMPDIR'])
  db = scratch / 'review.sqlite3'
  with sqlite3.connect(db) as conn:
      conn.executescript("PRAGMA application_id=1129072975; PRAGMA user_version=1; CREATE TABLE IF NOT EXISTS events(record_id TEXT, timestamp TEXT, payload TEXT);")
  cfg = scratch / 'review-config.json'
  cfg.write_text(json.dumps(dict(db=str(db), owner='fixture', fleet=True)))
  for name, flags in [('bad-fleet', []), ('explicit-control', ['--db',str(db)]), ('large-offset', ['--db',str(db),'--offset','9223372036854775808'])]:
      command = [sys.executable,str(root/'utils/CLIO/clio-query.py'),'search',*flags]
      result = subprocess.run(command,env=dict(os.environ,CLIO_CONFIG=str(cfg)),text=True,capture_output=True)
      print(name, 'exit=',result.returncode,'stdout=',repr(result.stdout),'stderr_last=',result.stderr.splitlines()[-1:] )
  PYPROBE
  ```

  Decisive output: bad-fleet exit=1, stdout='', stderr last line="AttributeError: 'bool' object has no attribute 'get'"; large-offset exit=1, stdout='', stderr last line="OverflowError: Python int too large to convert to SQLite INTEGER". Control exit=0, JSON status="empty", config_receipts="not_loaded_explicit_db", records=[], errors=[], stderr empty. The synthetic DB intentionally contains only the schema needed by this SELECT; no production history or writer is invoked.

- [Pass] Canonical reuse and chronology: utils/CLIO/clio-query.py:145 invokes store.query with its resolved configuration; :158–161 builds a fresh identity-only follow-up scoped to origin/agent/session. utils/CLIO/clio-store.py:484–492 keeps newest as the native default and uses stable timestamp/record-ID ordering. No second SQL reader/writer is introduced in the adapter.
- [Pass] Provenance and routing: adapter record() preserves extras as metadata and only reads an explicit string IDE; SKILL.md states “A session's first captured prompt is not proof of actual session creation” and “Lookup alone never authorizes activation, import, drain, projection, repair, config changes or launchd changes.” Resolver source uses explicit/config/default before bounded Pulse discovery and refuses ambiguity (utils/CLIO/clio-query.py:41–86).
- [Unverified — needs clone run] Supplied storage-fixed.log ends “Ran 19 tests in 17.298s” / “OK”; red-order.log records the expected chronological failure, and baseline-export.log retains the aged-fixture failure. These are producer evidence, not reviewer executions. The five-suite gate remains pending by design. Run required verification after the correction in the disposable full clone and preserve the results.
- Full-file sweep: R1 includes a pre-existing canonical-reader assumption now exposed through the new adapter. No other concrete pre-existing defect was identified in this bounded review; this is not an exhaustive correctness guarantee.

Handing off to Producer (claude-a) — address R1, retain clone verification evidence, and open round 2.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
