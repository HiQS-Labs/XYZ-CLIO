# RELAY · CLIO cold WAL reader final QA
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
6. **Commit only the relay file** (`relay(clio-cold-wal-reader-final-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-wal-final-qa.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-wal-final-qa.md
```
Independent final Codex QA of issue3 cold WAL scheduled-writer repair. Review committed helper, existing readonly test extension, INSTALL guidance and TESTS-RESULTS/2026-10-01-gh3-wal-repair focused red/green evidence. Verify query_only before schema checks, existing-file rw missing-path protection, event writes unchanged, cold synthetic test checkpoint/copy safe and meaningful, no collector/schedule/fleet change. Review entire relevant source and prior plan approval. No suites in worktree, no installed edits. Only edit relay thread. Approve if proportional and correct. Full gates and installed validation follow approval.
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

Candidate committed with synthetic red and both-runtime focused green receipts; full gates/deployment pending.

VERDICT: PASS
Basis: Ready for independent final review.

### Reviewer · Round 1

swept file: yes

VERDICT: PASS
Basis: Approve the bounded implemented cold-WAL reader repair against the embedded artifact questions and doc/gh3-plan.md:181–201. The scaffold DoD placeholder supplies no additional criterion. Read the complete helper, existing storage suite, INSTALL guidance, prior plan approval and focused receipts; inspected the scheduled dispatch and external metadata seam. No additional pre-existing blocker found in the swept files within this repair scope. Approval does not claim full gates or installed acceptance.

- [Pass] **Reader and writer contracts.** utils/CLIO/clio-store.py:89–107 opens existing-file URI mode=rw and sets query_only before application_id/user_version validation, closing on validation failure. Writable callers still explicitly request database(path, True) (:253, :291, :307, :742); the single insert seam and transaction/receipt paths remain intact (:228–260). Missing-path noncreation and reader DELETE refusal are retained in test/clio-store.py:382–388. Fix: retain this proportional stdlib seam.
- [Pass] **Cold acceptance is meaningful and safe.** test/clio-store.py:389–411 initializes/imports synthetic nonempty Unicode history in separate creator subprocesses, waits for their successful exits, copies the now-closed main file to a fresh path, asserts absent sidecars immediately before the Apple helper query, then requires one exact payload. Creator connections explicitly close and commit (utils/CLIO/clio-store.py:120–152, :307–361); this is a synthetic post-close copy, not live-WAL copying. Existing reference/pagination/large-prompt assertions remain (:372–388), and the extension stays in the existing case. Fix: preserve this cold-copy ordering and both-runtime gate.
- [Pass] **Focused recorded red/green evidence matches the seeded helper.** TESTS-RESULTS/2026-10-01-gh3-wal-repair/red.log quotes “AssertionError: 3 != 0 : OperationalError: unable to open database file” at the new query assertion; green-homebrew.log and green-system.log each report “Ran 1 test” and “OK”. provenance.jsonl records old helper 5acb403, red_exit=1 and both green exits=0, synthetic data and disposable clone. Read-only probe command: export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"; mkdir -p "$TMPDIR"; python3 - <<'PY' (inline pathlib/hashlib/json/ast source inspection: SHA256 helper bytes, compare provenance source_sha256, enumerate database execute literals and test_ functions). Exit 0; decisive output: “helper_sha256 441c21905b21239271328538debd8af1ec8a72b53cf1b0b152294cb7171ca2b6”, “receipt_hash_matches True”, “database SQL order ['PRAGMA query_only=ON', 'PRAGMA application_id', 'PRAGMA user_version']”, “storage_test_cases 16”. These are recorded focused runs, not suites rerun here. Fix: keep this receipt associated with these exact helper bytes.
- [Pass] **Documentation and scope match approval.** INSTALL.md:497–500 explains rw plus query_only, auxiliary bookkeeping and missing-DB protection. Prior relay-system/2026-10-01/gh3-wal-plan.md has STATUS: Approved and its Reviewer Round 1 explicitly approves this helper change and existing-case extension. Scheduled dispatch still uses the installed invocation (utils/CLIO/prompt-log-to-md.sh:54–62; clio-store.py:835–846); external Agy source metadata retains mode=ro (utils/CLIO/clio-agy-tail.sh:114). No collector, timer or fleet mechanism is introduced by this repair. Fix: proceed through the already ordered gates without widening scope.
- [Unverified — needs clone run] Full four shell suites and all 16 storage cases under both Python runtimes, scheduled-shaped PATH, unchanged Git identity and real installed launchd success without priming sidecars remain pending (doc/gh3-plan.md:196–201; focused receipt README explicitly says full gates/deployment pending). Required next action: harness/Producer runs the existing gates in a disposable full clone, then records separately authorized installation/launchd and exact seven-day ID/payload evidence. No suite, executable fixture or installed mutation was run during this turn.

Evidence limitation: list_projects returned all 77 entries with has_more=false; neither this CLIO worktree nor a CLIO project is indexed. Thus no nearest graph generation or check_index_coverage result is available; bounded verification used complete direct source reads rather than claiming graph completeness. relay-xyz locator ran first, exit 0, found the harness but printed “driver_lock_path_for_repo: command not found”; that is not a clean harness-validation receipt. Only this relay file was edited; no git command was run.

Relay closed (Approved), no further turn needed. The harness owns the relay-only commit; Producer/harness may perform the pending gates.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
