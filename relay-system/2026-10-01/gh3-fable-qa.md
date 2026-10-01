# RELAY · CLIO PR 5 Claude Fable 5.1 medium QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-01.
-->

NEXT: Producer
STATUS: Approved
ROUND: 1 / 4

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
6. **Commit only the relay file** (`relay(clio-pr-5-claude-fable-5-1-medium-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-fable-qa.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: codex
- Started: 2026-10-01

### Artifact — gh3-fable-qa.md
```
Review CLIO local capture-only implementation for authorized MacStudio deployment. Read AGENTS.md, latest operator-scope section at end of doc/gh3-plan.md, complete utils/CLIO/clio-store.py, INSTALL.md capture-only guidance, exporter adapter, existing test/clio-store.py and diff against origin/main. User says collection is final, accepts unrecoverable older historical gap, wants future captures in localSQLite, other Macs installed case by case. Do NOT demand more historical collection or synthesize lost metadata. No private data is available or permitted to this reviewer. Minimal local stdlib CLI, unchanged shared writer/tailers/job/plist; no new store/service/push/ledgerwriter/newMarkdownnote.

1. Is explicit activate --capture-only the only new no-view scheduled-export path, with activated DB/owner checks, preserved source+activation lock and unchanged schedule/destination? Normal activation without this flag must still fail until registeredview.
2. Does project JSONL-only safely reuse exact full-history compatibility serialization and output guards, retain provenance+unknownmetadata, never overwrite source/config/note/backups, and leave normal registered rolling behavior intact?
3. Does scheduled capture-only mode drain receipts, report pending/historycount and note_publication paused honestly, without creating a different Markdown note or weakening migrate-view coverage/singlepublisher gates?
4. Does the existing activation case meaningfully prove four-agentfuturewrites, private-source preservation, stable scheduled compat export and unchangednote/plist, and refuse unsafeJSONLoutput/multimarkermigration? Focusedcase passed; false capture_only configflag redcontrol failed at scheduled invocation. Suites run only in separate fullclone, never this relay worktree. All16+4shell suites will run after finalapproval.
5. Scope/rollback: legacyJSONLstops growing, downstreamsource must point to compatJSONL; provided foreignJSONLcan be adopted in separate private stores thenimported by existing snapshot protocol without claiming realdeviceUUIDs. Oldnote preservedoutsideSQLite; existinggapaccepted notclaimedrecovered. Review proportionality and material correctness, cite exact source. Only edit this relaythread. No executable tests/fixtures or private-home inspection. Approve if sound; otherwise concrete observedfailures with falsifiers, no speculativeguardframeworks.

Review current PR #5 head e2eaa95 and the entire changed helper, installation guidance, tests, and sanitized deployment receipts. Verify per-Mac retry guidance and whether claims distinguish shared-writer diagnostics from real IDE callbacks. No live deployment changes, private history reads, merge, or push. Requested reviewer: Claude Code claude-fable-5-1, medium effort.
```
- Definition of Done: _<fill in the acceptance criteria the Reviewer grades against>_

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

### Producer · Round 1

Current PR #5 executable implementation and documentation are ready for an independent review. Prior Codex QA and local deployment evidence are committed; this turn requests a fresh whole-file Claude review.

VERDICT: PASS
Basis: Ready for independent review; no claim of Claude approval yet.

### Reviewer · Round 1 (claude, claude-fable-5-1)

swept file: yes — read all 860 lines of `utils/CLIO/clio-store.py`, the full `origin/main...HEAD` diff of helper/INSTALL/test/plan/handoff, and the receipts under `TESTS-RESULTS/2026-09-30-gh3-local-capture/`. Static review only; no suite, fixture, private home or database was run or read. Definition of Done is an unfilled placeholder, so I graded against the artifact's five questions.

- [Pass] Q1 only new no-view scheduled path, explicit flag. The flag is written only by `activate(..., capture_only=True)` (`utils/CLIO/clio-store.py:438-440`); the scheduled branch needs activated DB + owner and no registered view: `capture_only = active_config(conn, path).get('capture_only') and not cfg.get('view')` (`clio-store.py:820`), then `existing_destination(args.markdown)` (`:822`) refuses a destination that differs from the installed job. Without the flag it still goes to `checked_view` (`:824`) → `'run migrate-view for the existing destination before exporting'` (`:562`). Source import/verify/backup and the `prompt-log.lock` handling in `activate` are untouched by the diff (`:415-443`). The installed adapter passes no `--db` (`utils/CLIO/prompt-log-to-md.sh:62`), so `cfg` is the real config.
- [Pass] Q2 JSONL-only reuses the same serializer and guards. One compatibility writer serves both modes (`clio-store.py:657-663`), still through `safe_output`; `jsonl_only` requires a JSONL path and no Markdown (`:635-636`) and returns before any note rendering (`:664-666`). Rows are full stored payloads, so `origin_id`/`origin_kind`/`extras` ride along. New sibling guard blocks `*.pre-sqlite-*` activation backups (`:615-617`). Registered rolling path is the same statements in the same order relative to the note check (`:690-699`).
- [Pass] Q3 honest scheduled reporting. Drain runs first (`:825`), result carries `history_rows`, `'note_publication': 'paused'`, `'markdown': None` (`:665-666`) and post-drain `pending` (`:828`). `target` is `None`, so no Markdown is created; `migrate_view` gates are unchanged (`:571-573`, `legacy_coverage` `:514-516`).
- [Pass] Q4 test proves what it claims, by reading. `test/clio-store.py:561` activates capture-only; the added block (`:568-593`) drives four `clio-capture.sh --agent … --record` writes, runs the plist's own command, asserts `note_publication == 'paused'`, `history_rows == 5`, `pending == 0`, byte-identical note/plist/source, four agents in compat, and refusals for JSONL onto source, onto the backup, and for a two-marker `migrate_view`. Normal activation still failing the scheduled job is covered separately: `self.assertNotEqual(rejected.returncode, 0)  # Activation alone is not view migration.` (`test/clio-store.py:210`). Red control receipt shows the false-flag run dying at the scheduled command with `returned non-zero exit status 3` (`capture-only-red.log`).
- [Unverified — needs clone run] Suite results. I did not execute anything; `clio-store.log` reads `Ran 16 tests in 6.323s` / `OK` and the shell logs read `PASS`, but that is the Producer's receipt, not my measurement. Harness gate should confirm.
- [Pass] Q5 scope, rollback, per-Mac retry guidance matches the code. "do not initialize or activate a second store" ↔ `'already activated; preserve configuration for rollback'` (`clio-store.py:405-406`); "failed verification should leave the current capture mode intact" ↔ config is the last write in `activate` (`:440`); "`--fresh` only when the legacy source genuinely does not exist" ↔ `:421-423`. INSTALL states "This is not a rolling-note cutover or proof of complete fleet coverage" and "the original JSONL stops growing after activation". No new store, service, push loop, ledger writer or note in the diff.
- [Pass] Claims separate shared-writer diagnostics from real IDE callbacks. Receipts say "Four explicitly labelled synthetic installed shared-writer diagnostics (one per agent)" (`TESTS-RESULTS/2026-09-30-gh3-local-capture/README.md:9`), `"labelled_synthetic_health_events": 4` (`deployment.json`), and the handoff says "live four-agent shared-writer diagnostics and replay dedup passed" (`doc/gh3-handoff.md:25`). Nothing claims an IDE hook or tailer fired live. Keep that wording; "four agents verified" must never be shortened to imply real callbacks.
- [Nit] `clio-capture.log:4` ends with `jq: parse error: Invalid literal at line 1, column 5` after `PASS: all capture cases (bash)`. The receipt README discloses ResourceWarnings and skips but not this line. Fix: one sentence in the receipt README saying which case emits it and that it is expected (or pre-existing on main). No code change requested.
- [Nit] A manual `clio-store.py --db PATH scheduled-export NOTE` sets `cfg = {}` (`clio-store.py:800`), so `not cfg.get('view')` at `:820` is true even after a later `migrate-view`; that run would stay JSONL-only. It fails safe (no note write) and the installed adapter never passes `--db`, so no change requested; reading `view` from the `active_config(...)` result would remove the asymmetry if this line is touched again.
- [Nit] Pre-existing: redundant function-local `import re` (`clio-store.py:194`; module import at `:12`).
- Pre-existing sweep otherwise: no material defect found in the unchanged parts of the helper (init, normalize/identity, capture/drain receipts, import accounting, verify, migrate-view, device snapshot, backup). I have no observed failing input for any of them and request no behaviour change.

VERDICT: PASS
Basis: The capture-only path is the single explicit, owner-checked, no-view scheduled route; it reuses the existing serializer and output guards, reports paused publication honestly, leaves default activation and migrate-view fail-closed, and the docs/receipts do not overclaim. Three nits, none blocking; suite results remain the harness gate's to confirm.

relay closed (Approved), no further turn needed — the nits are optional follow-ups for the Producer.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
