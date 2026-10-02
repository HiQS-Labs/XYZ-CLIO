# RELAY · gh3-auto-plan-agy-r4
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-agy-r4): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-PLAN-AGY-R4 --agent agy` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-revised-plan-packet.md** (embedded below — read it here).
- Reviewer: agy   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-auto-revised-plan-packet.md
```
Review revised executable automatic-recovery mechanism and Fable Round1 dispositions in doc/gh3-device-independent-plan.md, recon delta and gh3-auto-plan-fable review. Substantive changes: Obsidian Markdown merges are handled via opt-in machine-owned body, exact complete unknown-note private archive before canonical reconstruction; exact personal header protected, defaults unchanged. Own trusted configured committed snapshot restores old-backup missing records automatically, general self-import still refused. Pin header/coverage and spell peer setup/archives. Verify no history loss/pusher/service/newauthority assumptions, honest race/pilot/deployment boundary, bounded committed import and tests. Native Rebalance282 wiring remains separate. Only relay edits; no suites in worktree/live writes. On Approved close token with tick done or leave for shim; do not release to Producer. Grade concrete mechanisms, request only proportional findings with falsifiers.
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

- `[Pass]` Obsidian Markdown merges handled via opt-in machine-owned body. Verified in `doc/gh3-device-independent-plan.md:117` "The repair flag explicitly designates ONLY the body after the preserved `<!-- CLIO:ENTRIES -->` header as machine-owned output" and `:119` "By opting in, unexpected body edits are preserved... then replaced".
- `[Pass]` exact complete unknown-note private archive before canonical reconstruction. Verified in `doc/gh3-device-independent-plan.md:119` "atomically preserve the COMPLETE current file in the existing private view-backups directory... Archive BEFORE recording accepted outcomes or replacing the note."
- `[Pass]` exact personal header protected, defaults unchanged. Verified in `doc/gh3-device-independent-plan.md:117` "Human comments belong above that marker... Default repair-off behavior remains refusal."
- `[Pass]` Own trusted configured committed snapshot restores old-backup missing records automatically. Verified in `doc/gh3-device-independent-plan.md:111` "allow this owner snapshot to restore missing own records transactionally... A restored older same-owner DB therefore recovers automatically".
- `[Pass]` general self-import still refused. Verified in `doc/gh3-device-independent-plan.md:111` "The ordinary import-device CLI continues to refuse self-import."
- `[Pass]` Pin header/coverage and spell peer setup/archives. Verified in `doc/gh3-device-independent-plan.md:109` "Additional Macs register their already-generated note via existing migrate-view --archive-unreconciled-note... Configure additionally pins a SHA-256 of the personal header and coverage".
- `[Pass]` Verify no history loss/pusher/service/newauthority assumptions. Verified in `doc/gh3-device-independent-plan.md:113` "No new schema/version/store or ledger writer." and `115` "No extra scheduler/pusher."
- `[Pass]` honest race/pilot/deployment boundary. Verified in `doc/gh3-device-independent-plan.md:121` "The remaining narrow race is explicitly unproved... Do not claim lossless protection of such a concurrent human edit."
- `[Pass]` bounded committed import. Verified in `doc/gh3-device-independent-plan.md:111` "Bound Git calls (5s each, max16origins, total monotonic budget30s)".
- `[Pass]` Native Rebalance282 wiring remains separate. Verified in `doc/gh3-device-independent-plan.md:115` "Collector wiring stays native Rebalance#282... not a claim that unrelated Rebalance runtime was modified."

VERDICT: PASS
Basis: The plan successfully addresses all Fable Round1 dispositions and satisfies the requirements for the automatic-recovery mechanism without compromising data safety or overstepping the architectural boundaries.

relay closed (Approved), no further turn needed

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
