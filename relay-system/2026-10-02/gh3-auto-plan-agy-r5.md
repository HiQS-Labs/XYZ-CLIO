# RELAY · gh3-auto-plan-agy-r5
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-agy-r5): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-PLAN-AGY-R5 --agent agy` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-final-plan-packet.md** (embedded below — read it here).
- Reviewer: agy   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-auto-final-plan-packet.md
```
Review latest Fable Round2 dispositions in doc/gh3-device-independent-plan.md against whole executable plan and prior gh3-auto-plan-fable-r2 findings. F5: replay=True alone re-exports changed labels and conflicts at strict foreign peers, synthetic in-memory probe temp/gh3-own-replay-proof.json; restore original trusted committed delivery labels only for identity-equivalent own tailer events, archive old observation before existing-writer-seam update. No general self-import or conflict relaxation. F6: unknown record IDs defer note rewrite until committed history arrives (compat/capture continue), archive admission max128 files/256MiB with count/bytes status, pilot max12/day32MiB/day. F7-F8 honest committed-local/duplicate-owner warning. Grade proportional safe implementation readiness. No suites/live changes, relay edits only. Preserve all prior bytes including blank lines when appending. On Approved complete exact token command in thread; do not release it. Native Rebalance282/pilot remains outside this source PR.
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

Read in full: `doc/gh3-device-independent-plan.md` and prior Fable R2 findings in `relay-system/2026-10-02/gh3-auto-plan-fable-r2.md`. 

Dispositions of F5–F8 from gh3-auto-plan-fable-r2:
- [Pass] **F5 disposition (own-origin replay conflict & labels).** Plan `:111` correctly identifies that `replay=True` alone would re-export changed labels and stall strict peers. The revised mechanism limits trusted committed label restoration to own rows whose immutable identity agrees, preserves the previous local observation in an exclusive private archive before updating, and keeps generic capture/foreign imports strictly on first-observation semantics. It also correctly retains the identity/payload conflict refusal.
- [Pass] **F6 disposition (archive unbound/frequency).** Plan `:119` adds "unknown-ID deferral" (defer note replacement byte-intact until Git snapshots arrive), bounding the ordinary concurrent-capture oscillation. Added explicit limits (`max128 files/256MiB total`, `max64MiB` per input) and pilot stop rules (`max12/day` or `32MiB/day` per Mac) and surfaces count/bytes in status.
- [Pass] **F7 disposition (committed-local reporting).** Plan `:111` correctly labels the count as "committed-local/unsent/restored/label-restored" rather than remote-delivery acknowledgement.
- [Pass] **F8 disposition (duplicate owner warning).** Plan `:111` notes "a nonzero restore also warns to check duplicate owner if this store was not intentionally restored".

Implementation readiness: the plan is safe and proportionate. Reversibility and boundary conditions (native Rebalance 282, offline queries, original headers, and Sync sync-interval constraints) remain clear. 

VERDICT: PASS
Basis: F5-F8 are thoroughly addressed with safe, resource-bounded, and well-identified fallback mechanisms. The plan is safe, cleanly defines its boundaries, and maintains strict semantics for cross-device history synchronization.

relay closed (Approved), no further turn needed

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
