# RELAY · CLIO PR findings final QA
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
6. **Commit only the relay file** (`relay(clio-pr-findings-final-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-publish-final-qa.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-publish-final-qa.md
```
Final incremental QA of outstanding PR5 review fixes for issue3. Review cdceaa1: scheduled-export --db now reads capture_only and view from activated configuration; existing activation test extended, witnessed old conditional red rows None!=5 and fixed green. Fleet document now confirmed requirements/target outcomes with disconnected pilot and staged rollout still pending, existing cadence requirement not delivery guarantee. Review current entire relevant helper and test, plan, receipts, previous WAL approvals. No suites in review worktree or installed mutations. Only relay writes. Approve if both outstanding findings resolved and WAL fix preserved. Final four shell suites and16cases bothPython follow; no fleet rollout/merge authority inferred.  [Unverified — no citation]
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

Both concrete PR findings addressed with existing-case red/green receipt.

VERDICT: PASS
Basis: Ready for incremental final QA.

### Reviewer · Round 1

swept file: yes

VERDICT: PASS
Basis: Both outstanding findings are resolved and the reviewed WAL repair is preserved. Graded against the embedded artifact's explicit acceptance; the DoD placeholder adds no criterion. Read the entire storage helper, storage test, fleet plan and issue plan, plus relevant receipts and previous WAL approvals; inspected scheduler/install seams. No additional pre-existing blocker found in these swept files within the stated incremental scope. Approval covers source QA, not the pending final gates, incremental installation, fleet rollout or merge.

- [Pass] Explicit DB scheduled publication uses the activated configuration consistently. `activated = active_config(conn, path)` and `capture_only = activated.get('capture_only') and not activated.get('view')` (utils/CLIO/clio-store.py:835–844) eliminate the empty CLI-config view check. Active DB/owner validation remains at :482–487; view destination, original backup and accepted-note hashes remain checked at :560–570 before drain/project. Fix: retain this focused conditional and existing guards.
- [Pass] The existing activation case exercises the concrete failing input: activation retains capture_only=true, migration registers a view, then explicit `--db ... scheduled-export` must return rows=5 (test/clio-store.py:584, :617–633). The recorded old-conditional run reports `AssertionError: None != 5` (TESTS-RESULTS/2026-10-01-gh3-wal-repair/explicit-db-red.log:10); green reports `Ran 1 test` / `OK` (explicit-db-green.log:4–6); provenance.jsonl:9 records red_exit=1, green_exit=0 and the current helper hash. Fix: retain the case and associate the final gate with current bytes.
- [Pass] Fleet wording distinguishes requirements from delivered capability. doc/gh3-device-independent-plan.md:9 says the outcome follows the disconnected pilot/staged rollout and cadence is a scheduling requirement, not a delivery guarantee. :72–73 require the actual disconnected pilot and per-Mac rollout; :83 explicitly states replication/failover is not claimed installed or tested and note transport/#282 remain unresolved. Fix: preserve these qualifications when reporting status.
- [Pass] WAL repair remains intact: existing-file mode=rw, query_only before schema reads and close-on-validation-failure remain in utils/CLIO/clio-store.py:89–107. The existing cold-copy case still asserts absent sidecars before the Apple query and exact nonempty payload (test/clio-store.py:389–411); DELETE refusal and missing-file noncreation remain at :382–388. Prior gh3-wal-plan.md and gh3-wal-final.md have STATUS: Approved. Historical gate/installed receipts identify the previous helper hash (provenance.jsonl:2–8), so they are not claimed as current incremental gates. Fix: preserve the connection seam and both-runtime gate.
- [Pass] Narrow source-only probe corroborates receipt identity and branch selection. Command: `export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"; mkdir -p "$TMPDIR"; python3 - <<'PY'` with inline pathlib/hashlib/json/ast inspection of the helper and existing test: SHA256 bytes, compare last provenance source_sha256, enumerate database execute literals, compile/evaluate only the capture_only AST expression with three synthetic dictionaries, count test_ definitions. Exit 0. Decisive output: `helper_sha256 8f088b25863673d5ac64c3bb1115cce8e82591ab05bf74dc62f0f7d8d24a7550`; `explicit_receipt_matches True`; `reader_sql_order ['PRAGMA query_only=ON', 'PRAGMA application_id', 'PRAGMA user_version']`; capture-only without view → True, capture-only with view → False, view without capture-only → False; `storage_test_cases 16`. This is source measurement, not execution of the helper/test fixture. Fix: no additional mechanism needed.
- [Unverified — needs clone run] Final four shell suites and all 16 storage cases under both Python runtimes on the incremental helper remain pending, as stated in TESTS-RESULTS/2026-10-01-gh3-wal-repair/README.md:7 and the embedded artifact. Required next action: Producer/harness runs existing gates in a disposable full clone and records current helper identity. No suite, executable fixture, installed mutation or git command ran here.

Evidence limitation: list_projects pagination exhausted all 77 projects (has_more=false); no CLIO project or matching checkout is indexed, so no graph generation or check_index_coverage result is available. Complete direct source reads supply the bounded evidence. The relay-xyz locator returned exit 0 and found the harness, but printed `driver_lock_path_for_repo: command not found`; it is not a clean harness-validation receipt. Only this relay file was changed.

Relay closed (Approved), no further review turn needed. Producer/harness owns the pending clone gates and relay-only commit.


### Attestation · relay-drive — 2026-10-02T05:34:34Z
task: CLIO-GH3-PUBLISH-FINAL
reviewer: codex
status: Approved
reviewed-head: 6f4cc5b4cdb4c727f2df688af0beb98f69137fe2
added-range: 6216+4839
added-sha256: e1d6d01483c64f373aa24e480207f351af116e133d6fd42df8119523ace8acd7
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
