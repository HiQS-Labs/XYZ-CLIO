# RELAY · gh3-auto-plan-fable-r4
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-fable-r4): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-PLAN-FABLE-R4 --agent claude` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-complete-plan-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-auto-complete-plan-packet.md
```
Final plan QA after Fable Round3 in gh3-auto-plan-fable-r3: inspect latest executable plan and dispositions. F9 waiting_since bounded7200s, unchanged across updated note/IDs, offline peer eventually archive/repair includes local captures. F10 configured-owner export invokes reconcile before serialization, refuses own errors; not timer dependent. F11 one grouped recovery archive for all restored label observations per origin transaction (129 row control). F12 indexed columns updated too. F13 every note refusal continues drain/import/full compatibility with structured status. F14 ignored probe explicitly uncommitted until receipt. Full underlying mechanism unchanged from AgyR5 approval: trusted committed snapshots; existing writer seam restores committed labels; archive verified unknown generated bodies; header protected; bounded archives/imports; no new push loop. Grade this implementation plan with deployment and Sync pilot still gated. Only relay edits, no suites/live changes. Preserve earlier relay whitespace byte-for-byte. On Approved complete token command in thread, no release.  [Unverified — no citation]
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

Committed candidate ready for independent review; no installed changes.

VERDICT: PASS
Basis: Ready for QA.

### Reviewer · Round 1

swept file: yes

Read in full: `doc/gh3-device-independent-plan.md` (1–154, candidate commit `22bb351`, its diff read line by line), `utils/CLIO/clio-store.py` (1–877), prior thread `gh3-auto-plan-fable-r3.md` (Reviewer r1, F9–F14). No suites run (clone-only); no probe needed this round, every claim below is a text or code citation plus one arithmetic line. Pre-existing helper code: no new defect with an observed failing input beyond the seams the plan already names (`:841` note check before drain, `:746` self-import guard, `:233-236` replay equivalence).

Dispositions of F9–F14 from gh3-auto-plan-fable-r3:

- [Pass] **F9 (deferral expiry).** `:119` "Persist waiting_since UTC without resetting it when the incoming note/cutoff/unknown-ID set changes. Clear on no unknown IDs or after repair. After7200seconds (two current Studio Pulse intervals, a hard bound independent of peer availability), archive-then-repair even if no snapshot arrived; local captures then appear without a required peer." Control stated at `:154` "Test no snapshot ever arrives, local capture appears after bounded archive/repair". The non-reset rule closes the case where a changing peer note would restart the clock every tick.
- [Pass] **F10 (owner export ordered after own reconcile).** `:113` "For the configured owner, export-device itself reconciles trusted committed own history BEFORE serialization and refuses if that origin could not be validated/recovered; missing initial own snapshot is permitted for first publication. This prevents a collector racing the note timer from publishing later replay labels." Not timer dependent, as the packet says: the ordering is inside the one export call. Checked against the code for a residual window: once reconcile has restored every committed own ID, a later tailer redelivery of the same event is a no-op, `clio-store.py:233-236` `if prior[0] != payload and not (replay and row.get('source_event_id') and identity_payload(json.loads(prior[0])) == identity_payload(row)): raise … return False`, and capture uses that path (`:255` `insert(conn, row, replay=True)`). So no changed label can re-enter between reconcile and serialization. Control at `:154` "tested before the note timer".
- [Pass] **F11 (archive granularity).** `:111` "Collect all replaced observations into ONE recovery archive per origin transaction, deduplicated by SHA-256 (129 label-restored rows must not consume129 archives)"; control `:154` "tested129 changed-label rows".
- [Pass] **F12 (indexed columns).** `:111` "Update the payload and indexed repo/machine/repo_slug columns together in the sole insert seam". Matches the stored columns, `clio-store.py:238-239` `('record_id', 'timestamp', 'repo', 'machine', 'agent', 'session_id', 'repo_slug', 'origin_id')`; `branch` and `checkout` live only in the payload, so three columns is the complete set. `:154` "query-filter proof".
- [Pass] **F13 (refusals do not stop the cycle).** `:115` "Every note refusal (header/archive failure/budget/deferral) must still allow drain, valid reconciliation and full compatibility export. In fleet mode scheduled-export reports structured note status, including refusal; direct project remains a surfaced exception."
- [Pass] **F14 (probe provenance).** `:111` "uncommitted synthetic local probe temp/gh3-own-replay-proof.json reproduced that conflict (promote its result and provenance into committed TESTS-RESULTS with implementation)".

Underlying mechanism, confirmed unchanged by the `22bb351` diff (only `:111`, `:113`, `:115`, `:119` gained sentences; `:154` added):

- [Pass] Committed blobs only, bounded, no Git writes: `:111` "read ONLY `devices/<UUID>/clio.jsonl` committed blobs, not dirty worktree files. No fetch, add, commit, push, reset, stash or network call … Bound Git calls (5s each, max16origins, total monotonic budget30s)".
- [Pass] No general relaxation: `:111` "Generic capture and foreign imports remain strict/first-observation semantics; no global relaxation"; `:111` "The ordinary import-device CLI continues to refuse self-import".
- [Pass] Header protected, body archive verified before replace: `:119` "Archive BEFORE recording accepted outcomes or replacing the note. Never import history from Markdown."; `:119` "A malformed or changed header … refuses byte-intact and retries next tick".
- [Pass] No new pusher; deployment and pilot gated: `:115` "No extra scheduler/pusher"; `:132` "required before automatic fleet operation can be called installed"; `:121` "Keep second-Mac fleet note rollout off until a divergent offline/rejoin pilot verifies hybrid archival/repair".

Carried items, not blocking this plan approval (none changes the mechanism; F15 belongs to the gated pilot definition, F16–F18 to implementation QA):

- [Should] **F15 — the pilot window is shorter than the new expiry, so the pilot cannot observe the only archive source F9 adds.** `:119` "pilot concurrent capture for one existing Pulse interval and extrapolate archives/day: stop rollout if more than12archives/day" — one interval is 3600 s, the expiry is 7200 s (`:119` "After7200seconds"), so a one-interval pilot sees zero expiry archives and extrapolates zero. The expiry path is also not exceptional: while one Mac captures steadily, an awake idle peer always sees some ID newer than the last snapshot it pulled, so `waiting_since` never clears and it archives the full note once per 7200 s. `python3 -c "print(86400/7200, 128/12)"` → `12.0 10.666666666666666`: the ceiling equals the stop threshold exactly (never "more than 12"), and at that rate the 128-archive cap (`:119` "bounded to128 conflict/recovery archives") is reached in under 11 days, after which `:119` "No retention engine added" leaves a human to clear it; the same exhausted budget would also refuse an own-origin label restore and therefore the owner export (`:113`).
  Fix (pilot text only, before a second Mac enables repair): run the concurrent-capture pilot for at least three Pulse intervals with one Mac capturing throughout; record archives per idle peer and the projected days to the 128 cap; state the stop rule as a days-to-cap floor rather than `>12/day`.
  Observed input: plan text above; Mac A capturing every few minutes for more than 7200 s, Mac B awake and idle with repair enabled, Pulse hourly.
  Affected scope: the pilot acceptance rule at `:119`; no helper behaviour.
  Falsifier: the four-replica simulation at `:130` run with A capturing across three simulated Pulse intervals — if B records zero archives, the item is unnecessary. Expected under current text: one archive on B per 7200 s.
- [Nit] **F16 —** `export-device` holds the projection lock, acquired with a 0.5 s deadline (`clio-store.py:719`, `:268` `deadline = time.monotonic() + 0.5`), while reconcile may spend up to 30 s on Git reads (`:111`). Read the committed blobs before taking the lock so a note tick cannot make the collector's export fail busy, or the reverse.
- [Nit] **F17 —** `waiting_since` is wall-clock UTC. Treat a value later than now as expired, so a clock set backwards cannot extend the bound.
- [Nit] **F18 —** the step-3 control list (`:129`) still reads "peer unknown IDs deferred then imported"; the expiry, 129-row and export-before-reconcile controls exist only in `:154`. Copy them into the step list when the acceptance cases are written so they are not lost.

VERDICT: PASS
Basis: All six Round 3 findings are dispositioned in executable plan text with a stated control each, and the F10 ordering was checked against the existing writer seam for a residual window; none found. The mechanism approved in earlier rounds is unchanged by the diff. No history-loss path and no path needing a human in normal sleep/crash/rejoin operation was found in the helper plan. F15 is a defect in the pilot acceptance rule, not in the helper design; it must be fixed in the pilot definition before a second Mac enables repair, and that deployment step remains gated behind native Rebalance #282 and the Sync pilot. This approval covers the implementation plan only; it is not approval to deploy, change installed jobs or enable fleet note repair.

relay closed (Approved), no further turn needed. Token completed with `done`, not released.


### Attestation · relay-drive — 2026-10-02T06:40:48Z
task: CLIO-GH3-AUTO-PLAN-FABLE-R4
reviewer: claude
status: Approved
reviewed-head: ac5240d627ef0920edc7bf6fbc5513e4bc7ec319
added-range: 6905+8279
added-sha256: 4c4b0edf61933c0984f6c3e838ac0b2106d849983d4d8f4f245bdd2472b1f1e6
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
