# RELAY · CLIO cold WAL reader repair plan QA
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
6. **Commit only the relay file** (`relay(clio-cold-wal-reader-repair-plan-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-wal-plan-qa.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-wal-plan-qa.md
```
Codex plan QA for issue3 scheduled writer repair. Read latest writer-repair scope in doc/gh3-plan.md, complete database helper and callers, existing readonly acceptance case, doc/recon-gh3-device-independent.md and prior receipts. Observed synthetic/live cross-version cold WAL: HomebrewSQLite3.53.4 createsDB, AppleSQLite3.43.2 read-only open SELECT fails when no sidecars; mode=rw+query_only=ON succeeds, DELETE refused. Plan use existing-DB rw for app connections and SQL query_only for readers before schema checks; no new SQLite/WAL syncing, immutable reads, retry loop or timer. Local app-owned history, proportional stdlib fix; external metadata ro unchanged.
1. Is the fail path and smallest fix sound without weakening event-write/query/missing-file/schema contracts?
2. Does existing readonly test extension capture cross-version cold-open and assertions stillmeaningfullyfalsify?
3. Are scope, ratings, rollback and fleet dependency block truthful? No installed changes during QA; no suites in worktree. Only edit relaythread. Cite source and concrete falsifiers for behavior findings. Approve if sound.
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

Scope grounded by synthetic cross-version failure and current recurring launchd failure; no production edits.

VERDICT: PASS
Basis: Ready for independent plan review.

### Reviewer · Round 1

swept file: yes

VERDICT: PASS
Basis: Approve the bounded connection-contract repair plan, not an implemented/deployed repair. Graded against the three embedded QA questions and the latest ordered acceptance in doc/gh3-plan.md:151–207; the scaffold's DoD placeholder adds no acceptance criterion. Read the entire plan and storage helper, its database callers, existing storage cases, scheduler dispatch, external metadata seam, recon and relevant prior receipts. No additional pre-existing blocker found within this repair scope.

- [Pass] **Fail path and minimal fix.** `database()` currently selects `ro` for readers and validates before `query_only` (utils/CLIO/clio-store.py:89–105); scheduled export opens that reader before drain/project (:833–841). The plan explicitly uses existing-file `rw`, sets `query_only` before validation and permits auxiliary bookkeeping while retaining schema checks (doc/gh3-plan.md:181–188). Writers already use `database(path, True)` (:251, :289, :305, :740); the single event insert and transaction semantics need no change (:226–238). External Agy metadata keeps its independent `mode=ro` boundary (utils/CLIO/clio-agy-tail.sh:114). Fix: implement precisely this helper change; preserve those seams.
- [Pass] **Independent narrow cold-WAL measurement.** Command: `export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"; mkdir -p "$TMPDIR"; /opt/homebrew/bin/python3 - <<'PY'` (inline stdlib probe; outer and child exit 0). Probe created only a synthetic scratch DB using `PRAGMA journal_mode=WAL; CREATE TABLE events(payload TEXT); INSERT INTO events VALUES ('synthetic payload');`, committed/closed it, and used `/usr/bin/python3 -c` to open a separate cold main-file copy per mode. Reader sequence was `sqlite3.connect(p.as_uri()+'?mode='+mode,uri=True); c.execute('PRAGMA query_only=ON'); c.execute('SELECT payload FROM events')`, then attempted `DELETE FROM events`; a separate absent path used `mode=rw`. Decisive output: `creator SQLite 3.53.4 sidecars []`; `reader SQLite 3.43.2`; `ro SELECT failed: unable to open database file`; `rw SELECT [('synthetic payload',)]`; `rw DELETE refused: attempt to write a readonly database`; `missing rw refused; exists= False`; `reader exit 0`. This measures the proposed SQLite contract without touching live history or running fixtures/suites. Fix: retain cold copies/no reader priming in the implementation proof.
- [Pass] **Acceptance design is falsifiable.** Existing readonly case supplies nonempty Unicode payload, references, pagination, DELETE rejection and missing-file noncreation (test/clio-store.py:372–388); its setup initializes under the current interpreter (:29–39), explaining why it does not force the cross-version condition. The plan requires fresh Homebrew creation, absent sidecars, Apple helper lookup and preserved nonempty payload, plus old-helper red/new-helper green (doc/gh3-plan.md:190–198). Fix: extend that existing case as stated; close creator connections and assert absent sidecars immediately before the first Apple helper read, keeping every existing assertion.
- [Unverified — needs clone run] The extension is planned, not present, and no repair test execution is claimed here. Required closure: old helper fails the new cold-open assertion; changed helper passes under both runtimes; existing five suites run with throwaway HOME in a disposable full clone, with scheduled-shaped PATH and unchanged Git identity (doc/gh3-plan.md:191–201). Prior successful receipts are historical and do not prove this repair. This is an implementation gate, not a plan rejection.
- [Pass] **Scope, ratings and rollback are honest.** The latest rating distinguishes recoverable stale publication from lost capture and does not infer an incident trend (doc/gh3-plan.md:153–160). Code rollback is Easy, installation requires backups, and real launchd success without sidecar priming plus exact seven-day membership are explicit acceptance (:187–201). Fleet dependencies and unresolved same-note transport remain blocked; no merge, new pusher or remote re-enablement is inferred (:203–207). Fix: keep issue #3 open and record implementation/deployment evidence separately.
- [Nit] **Documentation consistency.** INSTALL.md:497 still says queries use `mode=ro`; doc/gh3-plan.md:47 is likewise the original contract, superseded by :181–188. When documenting the implementation, update the install query explanation to existing-file `mode=rw` plus SQL `query_only`, explicitly allowing WAL/SHM housekeeping; keep external metadata `ro`. No new mechanism or suite is needed.

Evidence limitation: `list_projects` returned all 77 entries over offsets 0 and 30; neither this worktree nor CLIO has an indexed project, so no nearest generation or path-coverage result is available. Direct complete source reads and literal caller lookup supplied the bounded verification; no graph completeness claim is made. relay-xyz locator ran first, exit 0 and harness found; it also printed `driver_lock_path_for_repo: command not found`, so its readiness output is not a clean harness-validation receipt. No git command, installed edit, executable fixture or suite was run.

Relay closed (Approved), no further turn needed. Producer may implement the approved scope; the harness owns the relay-only commit.


### Attestation · relay-drive — 2026-10-02T05:20:00Z
task: CLIO-GH3-WAL-PLAN
reviewer: codex
status: Approved
reviewed-head: 5acb4033e7828929074ccf1941c361bb707a02d6
added-range: 6595+5356
added-sha256: f4c8f2ba170ff9a4bc21ce18d62418b11214bce5c42bd80dc864460953a032f0
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
