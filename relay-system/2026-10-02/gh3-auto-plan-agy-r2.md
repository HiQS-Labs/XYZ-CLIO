# RELAY · gh3-auto-plan-agy-r2
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-agy-r2): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-auto-plan-packet.md** (embedded below — read it here).
- Reviewer: agy   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-auto-plan-packet.md
```
Review the executable automatic-recovery revision in doc/gh3-device-independent-plan.md and bounded recon delta. Entire relevant CLIO helper/tests and installed Rebalance publisher seams described in recon. Prior manual/fixed-publisher options superseded. Grade trusted committed snapshot imports, no echo/bootstrap old origins, eventual generated-note convergence under Obsidian Sync with exact byte reproduction and protected personal header/content, honest unknown/human race limits, scheduled path reuse, no new publisher/service/store, bounds/rollback/proofs. CLIO-only source PR5 and native Rebalance282 wiring/deployment boundary explicitly separate; no claim existing GPS already invokes CLIO. Approve only implementable safe scoped mechanism; concrete actionable findings with falsifiers. Do not run suites in worktree, touch installed files, or write artifact. Only relay thread edits.

Protocol: on approval, set STATUS Approved and end with relay closed. Do NOT release the token back to Producer; either mark tick done as the reviewer or leave the claim for the shim to close. Prior gh3-auto-plan-agy review text approved but driver exit4 close-mismatch because reviewer released rather than completed the token. Reconfirm the same plan and close correctly; no substantive plan changes.
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

Reconfirming the plan approval as instructed. The automatic-recovery revision correctly scopes the mechanism without adding new services or multi-writer database conflicts.

- [Pass] Trusted committed snapshot imports, no echo/bootstrap old origins. Citation: `doc/gh3-device-independent-plan.md:111` ("read ONLY `devices/<UUID>/clio.jsonl` committed blobs... Skip own-origin insertion").
- [Pass] Eventual generated-note convergence under Obsidian Sync with exact byte reproduction and protected personal header/content. Citation: `doc/gh3-device-independent-plan.md:117` ("exact byte equality to rendering those records... human/unsupported body or header edits remain untouched").
- [Pass] Honest unknown/human race limits. Citation: `doc/gh3-device-independent-plan.md:119` ("Unexpected human-content races remain a limitation requiring pilot observation").
- [Pass] Scheduled path reuse, no new publisher/service/store. Citation: `doc/gh3-device-independent-plan.md:113` ("No new schema/version/store or ledger writer") and `:115` ("No extra scheduler/pusher").
- [Pass] Bounds/rollback/proofs. Citation: `doc/gh3-device-independent-plan.md:111` ("Bound Git calls") and `:79` ("Rollback stops the new adapter/projectors").
- [Pass] CLIO-only source PR5 and native Rebalance282 wiring/deployment boundary explicitly separate; no claim existing GPS already invokes CLIO. Citation: `doc/gh3-device-independent-plan.md:115` ("Collector wiring stays native Rebalance#282... This PR provides callable CLIO seams and executable simulated proof") and `:89` ("This handles Git publication transport; it does not implement CLIO replica import").

VERDICT: PASS
Basis: The automatic-recovery plan is sound, correctly bounded, explicitly separated from Rebalance#282, and relies on exact byte parity over eventual sync rather than unstable shared-file locks.

relay closed (Approved), no further turn needed

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
