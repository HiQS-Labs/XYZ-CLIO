# RELAY · gh3-auto-plan-agy-r3
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-agy-r3): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

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

VERDICT: PASS
Basis: The plan accurately addresses all requirements for the executable automatic-recovery mechanism and incorporates Fable Round 1 dispositions. It correctly implements opt-in machine-owned body logic with verified unknown-note archival, preserves original personal headers, allows own-origin snapshots to restore missing records, bounds Git commands, and cleanly separates native Rebalance #282 wiring.

- [Pass] **Markdown merges and verified archive:** The plan requires exact complete unknown-note private archives before regeneration. "atomically preserve the COMPLETE current file in the existing private view-backups directory... deduplicated by SHA-256... Archive BEFORE recording accepted outcomes or replacing the note." (doc/gh3-device-independent-plan.md:119)
- [Pass] **Header protection and peer setup:** Pinned headers, coverage, and proper setup on additional Macs are specified. "Configure additionally pins a SHA-256 of the personal header and coverage; deployment verifies header/coverage agree across Macs" (doc/gh3-device-independent-plan.md:109).
- [Pass] **Own-origin restoration:** The trusted snapshot can restore missing own records while refusing generic self-import. "allow this owner snapshot to restore missing own records transactionally while retaining all unsent local captures... A restored older same-owner DB therefore recovers automatically without a new owner." (doc/gh3-device-independent-plan.md:111).
- [Pass] **Bounded import and no new authority:** The design introduces no new external services or unbounded network calls. "No fetch, add, commit, push, reset, stash or network call." (doc/gh3-device-independent-plan.md:111) and "Bound Git calls (5s each, max16origins, total monotonic budget30s)" (doc/gh3-device-independent-plan.md:111).
- [Pass] **Honest deployment and race boundaries:** The narrow unproved race of a concurrent human edit is surfaced honestly. "The remaining narrow race is explicitly unproved: an external edit after the final comparison can be overwritten... Do not claim lossless protection of such a concurrent human edit." (doc/gh3-device-independent-plan.md:121).
- [Pass] **Native Rebalance #282 wiring:** The integration clearly reuses existing locking and pathways. "Collector wiring stays native Rebalance#282: existing publication lock encompasses owner-only export to private staging then exact-path commit/push via its current publisher." (doc/gh3-device-independent-plan.md:115).

relay closed (Approved), no further turn needed

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
