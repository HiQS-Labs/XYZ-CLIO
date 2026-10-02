# RELAY · CLIO no-required-Mac architecture plan QA
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
6. **Commit only the relay file** (`relay(clio-no-required-mac-architecture-plan-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-no-hub-qa.md** (embedded below — read it here).
- Reviewer: agy   ·   Producer: codex
- Started: 2026-10-01

### Artifact — gh3-no-hub-qa.md
```
QA doc/gh3-device-independent-plan.md in full, against doc/recon-gh3-device-independent.md, existing CLIO export/import/project/insert and supplied current publisher map. User confirms every Mac must have complete history, use existing Git Pulse cadence, and travel Mac must capture/query/refresh SAME Obsidian note while Studio is off. They are considering the note transport choice; do not infer consent to a new path or disabling whole-vault Sync. This is plan-only: no code/install/private-history reads, uploads or rollout. Local stdlib tool/four-Mac fleet; proportionate machinery, no new SQL server/push/vector/ledgerwriter. Only edit relay thread.
1. Does the plan eliminate a required Mac for capture, delivered-history queries, rebuild and transport? Are durable unsent arrivals retained?
2. Does existing owner-only snapshot protocol suffice without SQLite binary merge, and are current foreign/adoption origins seeded correctly, stable IDs retained and imported records not echoed?
3. Are exact owned Git paths, local locks, bounded retries, replay and private-data boundaries grounded; is staggered scheduling honestly only optimization?
4. Does same-path note design acknowledge unfenced Obsidian Sync and genuinely meet no-hub outcome? Identify any design blocker; exact-file exclusion is explicitly unverified, manual handover is explicitly not automatic failover. Grade pending product prerequisite honestly rather than assuming it exists.
5. Are acceptance/shutdown/concurrency/recovery tests measurable, and rollback/publisher/Daily/semantic/readonly ledger reuse proportional?
6. Name concrete questions the operator still needs to answer. Approve the staged plan if sound subject to stated prerequisites; never claim implementation-ready for unresolved note transport. Any changes requested require concrete plan lines/affected scope/falsifier. No suites/fixtures in review worktree.
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

The new plan and bounded current recon are committed. Three database/cadence/travel requirements are confirmed. The note transport choice is explicitly pending and exact-file exclusion is not assumed supported. Review the design and name blockers; no rollout claim.  [Unverified — no citation]

VERDICT: PASS
Basis: Ready for independent plan QA, not implementation or rollout readiness.

### Reviewer · Round 1

swept file: yes

* [Pass] Q1: Plan eliminates the hub and retains arrivals. Citation: `doc/gh3-device-independent-plan.md:11` "A Mac can only know records already delivered or captured locally... Capture survives a powered-off peer".
* [Pass] Q2: Reuses `export-device` protocol without binary merge. Citation: `doc/gh3-device-independent-plan.md:31` "Reuse `export-device` / `import-device`: one atomic versioned manifest plus canonical records... imported rows never echo through another origin."
* [Pass] Q3: Exact paths, local locks, bounded retries grounded. Citation: `doc/gh3-device-independent-plan.md:37` "acquires the existing local Git publication lock, drains bounded local pending receipts", `doc/gh3-device-independent-plan.md:41` "Publish through the existing exact-path commit/push routine, at most its one race retry." Staggering is honest: `doc/gh3-device-independent-plan.md:43` "No correctness rule or delivery guarantee relies on staggering."
* [Pass] Q4: Acknowledges unfenced Obsidian Sync and does not assume exclusion. Citation: `doc/gh3-device-independent-plan.md:55` "The current accepted-hash guard and Git checkout OS lock cannot fence another Mac's Obsidian Sync writes." `doc/gh3-device-independent-plan.md:59` "Verify installed product supports this exact exclusion... capability is not assumed."
* [Pass] Q5: Tests are measurable. Citation: `doc/gh3-device-independent-plan.md:71` "Record manual real-Git fault cases in committed TESTS-RESULTS provenance... simultaneous push race, sleep/wake, lock busy, failed push, malformed owner/digest/count, rollback snapshot, identity conflict, duplicate replay".
* [Pass] Q6: Concrete questions operator needs to answer. Citation: `doc/gh3-device-independent-plan.md:57` "Decision awaiting operator answer:", `doc/gh3-device-independent-plan.md:59` "A. Git Pulse transports this note...", `doc/gh3-device-independent-plan.md:61` "B. Keep Obsidian Sync and manually transfer the one publisher."

VERDICT: PASS
Basis: The plan successfully addresses all architectural and procedural requirements of the no-hub constraints, correctly identifies the open transport prerequisites without assuming them, and ensures data retention and separation.

relay closed (Approved), no further turn needed.


### Attestation · relay-drive — 2026-10-01T22:41:40Z
task: CLIO-GH3-NO-HUB-R1
reviewer: agy
status: Approved
reviewed-head: 0a2ec7540797a488209332757c5def3a202d8183
added-range: 7611+2292
added-sha256: da2fd251c3ca45a0afcf14fad627f6a45f04a9b41f3cf74239f9d6ff34e84dad
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
