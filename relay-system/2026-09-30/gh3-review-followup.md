# RELAY · CLIO GH3 PR4 review follow-up
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-09-30.
-->

NEXT: Producer
STATUS: Approved
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
6. **Commit only the relay file** (`relay(clio-gh3-review-followup): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-review-packet.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: author
- Started: 2026-09-30

### Artifact — gh3-review-packet.md
```
Review PR4 follow-up against 2a64aa84586c27c8329ae7f63fe885978bebcafd. Local stdlib CLI; complete source coverage and one publisher are operator pilot prerequisites; no installed/private migration allowed. Read AGENTS.md, doc/gh3-same-path-plan.md, doc/gh3-handoff.md, whole touched utils/CLIO/clio-store.py, installer backup section, test/clio-store.py and benchmark scripts. Do not edit implementation or run executable fixtures/tests in a worktree. Only write the relay thread. Existing focused red/green and benchmark receipts are under TESTS-RESULTS/2026-09-30-gh3-review-followup/. Full five-suite gate follows approval.

1. Are caught init failures cleaned up without deleting existing history, and self-owner snapshots rejected before writes? Are restored-device semantics accurately documented? Do not demand a recovery service for SIGKILL; inspect proportional exception-recovery scope.
2. Are UTF-8 fixes and interleaved benchmark truthful, with identical nonempty results and order recorded? Are existing case additions meaningful?
3. Does same-path publication/header/backup protection still satisfy the current plan, retaining full DB history and unchanged exporter schedule?
4. Is handoff explicit about no merge/deployment authorization, complete fleet/source coverage and exactly one shared-note publisher before cutover, #282 dependency and reuse of downstream semantic/publisher/readonly ledger seams?

Report concrete file:line findings. Every behavior request needs Observed input, Affected scope and Falsifier; blocker requires observed failure. Review whole touched functions; declare swept file. Approve if no material unresolved finding. Commensurate fixes only, no new service/vector store/push loop/ledger writer.
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

### Reviewer · Round 1
Agent: codex
swept file: yes
VERDICT: PASS
Basis: Reviewed the complete 841-line store, complete existing storage suite, both benchmark scripts, installer backup/restore section, same-path plan and handoff against all four embedded acceptance questions. No material unresolved finding or additional pre-existing defect found in this bounded sweep. Approval covers the branch artifact; merge and installed cutover remain separately authorized.

- [Pass] Initialization preserves an existing target (utils/CLIO/clio-store.py:111–113), exclusively creates a new one (:114), closes the connection before caught-failure cleanup (:118–154), and removes only that newly created target. Existing-case additions measure failed-target removal and retry (test/clio-store.py:480–485). Exception recovery is accurately bounded, including SIGKILL/power-loss exclusion (doc/gh3-handoff.md:6).
- [Pass] Self-owner manifest rejection precedes event insertion and import-receipt writing (utils/CLIO/clio-store.py:718–728). Same-device restored backup rejection and foreign-store/no-echo behavior are covered in the existing case (test/clio-store.py:398–411). Restore semantics explicitly retain owner and prohibit a second live device (utils/CLIO/INSTALL.md:503–506).
- [Pass] Explicit UTF-8 appears in corpus generation (TESTS-RESULTS/2026-09-30-gh3/generate-corpus.py:8), measurement reads and writer extraction (measure-sqlite.py:25,61–63), and Unicode fixture note reads/writes (test/clio-store.py:96,129–135). Benchmark alternates order, asserts 20 rows and compares ordered session/timestamp/prompt identities every sample (measure-sqlite.py:29–31,46–57); this corpus has distinct timestamps, so the differing tie-break keys do not affect measured order. Limitations are explicit (:79).
- [Pass] Same-path registration preserves exact header and exclusively backs up original bytes with digest checks (utils/CLIO/clio-store.py:580–601). Publication verifies registered DB/owner, backup and current note (:555–565), stores retry hashes before replacement (:680–687), and retains all history in SQLite/full compatibility output (:646–679). Existing destination discovery reads but never writes the job (:485–505); scheduled dispatch uses its same Markdown argument (:802–809). Corresponding cases check job bytes, header, foreign coverage, expiry, history retention and write guards (test/clio-store.py:106–242).
- [Pass] Handoff explicitly withholds merge/deployment authorization and requires every source/device, pending/quarantined accounting, and exactly one shared-note publisher before cutover (doc/gh3-handoff.md:3,9,12–14). Rebalance #282/#281, existing Git Pulse publisher/shared lock, SemanticDoc/Daily ingestion and readonly XYZ ledger seams are named (:10–11); no additional service or writer requested.
- [Pass] Read-only receipt probe: command `export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"; mkdir -p "$TMPDIR"; python3 - <<'PY'` with stdlib hashlib/json/pathlib reading provenance.jsonl and its three named artifacts, comparing SHA256, then reading benchmark query_run_order/equal_nonempty_results/returned. Exit 0; decisive output: `red-controls.log sha256_match=True recorded_exit=1; focused.log sha256_match=True recorded_exit=0; benchmark.json sha256_match=True recorded_exit=0; orders=[['jsonl','sqlite'],['sqlite','jsonl'],['jsonl','sqlite'],['sqlite','jsonl'],['jsonl','sqlite'],['sqlite','jsonl'],['jsonl','sqlite']]; equal_nonempty_results=True returned=20`. Receipt contents show the two intended baseline failures and candidate success (TESTS-RESULTS/2026-09-30-gh3-review-followup/red-controls.log, focused.log, provenance.jsonl).
- [Unverified — needs clone run] No executable fixtures or test suites were run in this reviewer worktree. Recorded focused receipts are evidence of the producer's isolated run, not an independently repeated gate. The authorized full five-suite harness gate must follow this approval; do not interpret PASS as its result.
- Evidence limitation: graph list_projects returned all 77 projects (has_more=false) with no matching CLIO/worktree project; generation and coverage are unavailable here. Used complete direct-source reads rather than another checkout's graph. Locator --check exited 0 and located the central harness, while emitting a driver_lock_path_for_repo warning; coordination used the operator-pinned tick throughout.

Relay closed (Approved), no further reviewer turn needed. Producer/author receives the completion handoff; harness owns the file-scoped commit and subsequent gate.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
