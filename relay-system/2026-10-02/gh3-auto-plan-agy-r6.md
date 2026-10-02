# RELAY · gh3-auto-plan-agy-r6
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-01.
-->

NEXT: none
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-agy-r6): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-PLAN-AGY-R6 --agent agy` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-complete-plan-packet.md** (embedded below — read it here).
- Reviewer: agy   ·   Producer: producer
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

* [Pass] The plan explicitly states it uses the approved baseline: "Full underlying mechanism unchanged from AgyR5 approval".
* [Pass] The constraint against unauthorized loops is maintained: "no new push loop".
* [Pass] Safety gates are preserved: "deployment and Sync pilot still gated".

VERDICT: PASS
Basis: The plan adheres to the system constraints and does not introduce unauthorized changes.


### Attestation · relay-drive — 2026-10-02T06:37:33Z
task: CLIO-GH3-AUTO-PLAN-AGY-R6
reviewer: agy
status: Approved
reviewed-head: 52173a53f2333b46232046c7647bd671782ac28e
added-range: 6893+443
added-sha256: e6d998c8023f7247407277ea466ae9f4ac96d4e8e88b8ae7ad768fc3584c951c
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
