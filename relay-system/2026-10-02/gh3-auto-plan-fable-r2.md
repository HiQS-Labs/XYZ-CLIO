# RELAY · gh3-auto-plan-fable-r2
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-01.
-->

NEXT: Producer
STATUS: Open
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-fable-r2): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-PLAN-FABLE-R2 --agent claude` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-revised-fable-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-auto-revised-fable-packet.md
```
Review revised executable automatic-recovery mechanism and Fable Round1 dispositions in doc/gh3-device-independent-plan.md, recon delta and gh3-auto-plan-fable review. Substantive changes: Obsidian Markdown merges are handled via opt-in machine-owned body, exact complete unknown-note private archive before canonical reconstruction; exact personal header protected, defaults unchanged. Own trusted configured committed snapshot restores old-backup missing records automatically, general self-import still refused. Pin header/coverage and spell peer setup/archives. Verify no history loss/pusher/service/newauthority assumptions, honest race/pilot/deployment boundary, bounded committed import and tests. Native Rebalance282 wiring remains separate. Only relay edits; no suites in worktree/live writes. On Approved close token with tick done or leave for shim; do not release to Producer. Grade concrete mechanisms, request only proportional findings with falsifiers.

Second independent plan review after attested Agy gh3-auto-plan-agy-r4 Approved. Explicitly grade dispositions F1-F4 from gh3-auto-plan-fable. The opt-in now archives unknown/hybrid machine-owned bodies before rebuilding, personal header remains protected; trusted own-origin restore is automatic. On append preserve every previous byte including blank lines; insert at marker without rstrip. Claude Fable5.1 high effort. Approve if safe and proportionate, with rollout still gated by observed Sync behavior.
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

Read in full: `doc/gh3-device-independent-plan.md` (1–146), `doc/recon-gh3-device-independent.md` (1–37), `utils/CLIO/clio-store.py` (1–877), prior threads `gh3-auto-plan-fable.md` (Reviewer r1) and `gh3-auto-plan-agy-r4.md`. No suites run (clone-only). One in-memory probe, quoted in F5. Pre-existing helper code: no new defect with an observed failing input beyond F5's seam; prior F4 nit is dispositioned.

Dispositions of F1–F4 from gh3-auto-plan-fable:

- [Pass] **F1 disposition (merge hybrids).** Premise corrected and mechanism is fail-safe: `:105` "Obsidian Sync normally merges concurrent Markdown changes; it can produce a hybrid rather than either original note"; `:119` "atomically preserve the COMPLETE current file in the existing private view-backups directory, deduplicated by SHA-256, exclusive creation0600 plus fsync/hash verification … Archive BEFORE recording accepted outcomes or replacing the note. Never import history from Markdown"; default unchanged `:117` "Default repair-off behavior remains refusal". A merged body cannot forge a second marker from prompt text: body lines are escaped and prefixed, `clio-store.py:697` `'> ' + html.escape(line, quote=False)`. Requested step-3 case and pilot stop rule are present: `:129` "hybrid spliced from valid renderings archived byte-exact before repair", `:121` "Keep second-Mac fleet note rollout off until a divergent offline/rejoin pilot verifies hybrid archival/repair". Resource bound of this path is F6.
- [Pass] **F2 disposition (peer registration, pinned header/coverage).** `:109` "Additional Macs register their already-generated note via existing migrate-view --archive-unreconciled-note … Configure additionally pins a SHA-256 of the personal header and coverage; deployment verifies header/coverage agree across Macs (otherwise do not enable fleet note recovery)". Byte parity is achievable with existing seams: peer header is `text[:marker.end()]` (`clio-store.py:593`) and the publisher writes `view['header'].encode() + b'\n' + data` (`:705`), so a peer registering the synced note extracts the same header bytes; both get coverage `archived-not-reconciled` (`:596`), hence the same banner (`:683-684`).
- [Should] **F3 disposition — accepted in direction, but see F5:** the automatic own-origin restore stalls on a concrete input through the seam the plan names.
- [Pass] **F4 disposition.** `:144` "committed blob receipts use an explicit non-filesystem source namespace, and safe_output ignores only that exact namespace; ordinary file imports remain protected. Drain errors are surfaced independently so committed import/compatibility refresh can still proceed where safe". Matches the collision site `clio-store.py:626`.

New findings:

- [Should] **F5 — own-origin restore via the existing insert seam refuses a tailer-replayed row, turning the "automatic" old-backup recovery into a permanent publication stop.** Plan `:111`: own snapshot restore applies "payload-conflict refusal … identically" and "conflicting own records stop that origin and refuse preparation for publication"; foreign and own both use "the existing manifest/normalization/insert seam", i.e. `insert(conn, row)` with `replay=False` (`clio-store.py:751`). For rows with `source_event_id`, identity excludes delivery-time labels (`:222-224`) and local capture keeps the first observation (`:255`, `replay=True`). After an older DB (and tailer cursor) is restored, the tailer redelivers the event with a different label before reconcile runs; the committed own snapshot then carries the same `record_id` with the earlier payload. Probe (in-memory SQLite, synthetic row, `HOME`/`TMPDIR` under `.relay-scratch`; `python3 - <<EOF … EOF`, exit 0), decisive output:
  `same record_id: True` / `local replay insert: True` / `snapshot insert (import_device seam, replay=False): ValueError: identity payload conflict` / `snapshot insert with replay=True: False`.
  No data loss, but that Mac never exports again without a human — the case F3's disposition claims to make automatic ("No mandatory manual owner rotation for normal old-backup recovery", `:144`).
  Fix (one sentence in `:111` plus one control in `:146`): for the own-origin snapshot only, compare with the existing replay tolerance (`insert(..., replay=True)` semantics: equal `identity_payload` is a duplicate, first local observation retained); a differing identity payload still refuses. Add negative control "restored store, tailer-redelivered row with changed branch label, then own-snapshot reconcile → restored, not conflict". Foreign-origin imports keep strict comparison.
  Observed input: own row `{source_event_id:'evt-1', branch:'feature'}` already local; own committed snapshot row identical except `branch:'main'`.
  Affected scope: `reconcile-fleet` own-origin insertion of records carrying `source_event_id` (Codex/Agy tailer events).
  Falsifier: clone fixture restoring an older store, redelivering one tailer event with a changed label, then reconciling the own committed snapshot — if it reports restored/duplicate and export proceeds under the strict seam, this change is unnecessary. Expected today: `identity payload conflict`, export refused.

- [Should] **F6 — the archive path fires in ordinary two-Mac use, not only on hybrids, and is unbounded as written.** A peer note containing IDs this Mac has not received cannot be byte-reproduced, so it takes the archive path: `:119` "Unknown not-yet-delivered records survive in that archive until Git snapshots arrive"; `:129` "peer unknown IDs deferred then imported". Delivery is hourly, rendering is every 300 s (`recon :13` "StartInterval is 3600 seconds … local note renderer remains 300 seconds"). While two Macs each hold unsent captures, each tick receives the other's view, archives the whole file and replaces it; the cutoff line changes per bucket so SHA dedup does not help, and `:119` says "no pruning/deletion". Worst case is one full-note archive per tick per Mac (288/day) and a note that alternates between the two views until delivery. `:119` makes disk exhaustion a byte-intact refusal, which is safe but needs a human. No live measurement here: [Unverified — needs pilot] for actual frequency and note size.
  Fix (plan text only, no pruning machinery now): (a) state this ordinary-case behaviour and growth rate next to `:119`/`:105`; (b) status reports archive count and total bytes; (c) add to the `:121` pilot and QA gates: measure archives/day with two Macs capturing concurrently across one Pulse interval, with a stated stop threshold before a second Mac enables repair. Any retention or cheaper peer-note recognition is a later decision made on that measurement.
  Observed input: plan text and cadences cited above; no archive was produced here.
  Affected scope: repair-opt-in Macs receiving a peer-rendered note that contains record IDs absent from the local replica.
  Falsifier: pilot with two Macs capturing concurrently for one Pulse interval; if archives created stay near zero (for example Sync delivery or rendering order prevents the alternation), the gate never fires and no text change beyond the measurement is needed.

- [Nit] **F7 —** `reconcile-fleet` reads the local checkout HEAD with no network (`:111`), so its "own delivered" count means committed locally, not verified remote bytes (`recon :19` "Snapshot publication is not acknowledgement until remote bytes verified"). Name the count accordingly or leave the remote-delivery receipt to Rebalance status (`:51`).
- [Nit] **F8 —** automatic own restore also heals the forbidden two-live-stores-one-owner state (`:111` "Never enable two live stores with the same owner"); say that a nonzero restored count on a store that was not restored from backup is a surfaced duplicate-owner warning.

Confirmed unchanged from the prior round:

- [Pass] Committed blobs only, bounded, no Git writes: `:111` "read ONLY `devices/<UUID>/clio.jsonl` committed blobs, not dirty worktree files. No fetch, add, commit, push, reset, stash or network call … Bound Git calls (5s each, max16origins, total monotonic budget30s)".
- [Pass] No echo, explicit legacy seed only: `clio-store.py:724` `WHERE origin_id=?`; plan `:113` "explicit `--origin UUID` bootstrap export … never used by the ordinary scheduled producer".
- [Pass] No new pusher/service/authority; #282 boundary kept: `:115` "No extra scheduler/pusher … This PR provides callable CLIO seams and executable simulated proof, not a claim that unrelated Rebalance runtime was modified"; `:132` "required before automatic fleet operation can be called installed".
- [Pass] Honest race and pilot limits: `:121` "an external edit after the final comparison can be overwritten; archival captures the bytes read, not an unseen write in that window. Do not claim lossless protection of such a concurrent human edit."
- [Pass] Header stays protected: `:119` "A malformed or changed header … refuses byte-intact and retries next tick"; `:123` "Header drift is personal content and remains a protected exception".

VERDICT: FAIL
Basis: F1, F2 and F4 dispositions are sound and the mechanism loses no history. F3's automatic own-origin restore has a reproduced failing input (F5): under the strict insert seam the plan names, a restored store with one tailer-replayed row refuses its own snapshot and stops publishing, which is the manual-repair outcome the disposition set out to remove. F6 is an unstated, unbounded cost of the archive path in normal concurrent use. Both fixes are plan-text only (one sentence and one control for F5; a stated bound, status counter and pilot threshold for F6); no redesign requested. F7–F8 are optional.

handing off to Producer — go to the Producer window and say 'take your turn' (disposition F5–F8, edit plan text, bump ROUND to 2).

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
