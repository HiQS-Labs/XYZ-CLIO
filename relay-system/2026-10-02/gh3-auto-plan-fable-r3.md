# RELAY · gh3-auto-plan-fable-r3
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-fable-r3): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-PLAN-FABLE-R3 --agent claude` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-final-plan-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
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

Read in full: `doc/gh3-device-independent-plan.md` (1–150), `utils/CLIO/clio-store.py` (1–877), prior thread `gh3-auto-plan-fable-r2.md` (Reviewer r1, F5–F8). No suites run (clone-only). One synthetic probe under `.relay-scratch`, quoted in F5/F10. Pre-existing helper code: no new defect with an observed failing input beyond the seams named in F10–F12.

Dispositions of F5–F8 from gh3-auto-plan-fable-r2:

- [Pass] **F5 disposition (restore committed labels, not replay tolerance).** The producer's correction is right and reproduced here. Plan `:111` "Merely replay=True while retaining restored local labels would re-export a changed payload and stall strict peers"; mechanism `:111` "restore the five delivery-label fields from that snapshot and preserve the previous local observation in an exclusive verified private recovery archive before updating … Generic capture and foreign imports remain strict/first-observation semantics; no global relaxation". The five fields are exactly the ones outside identity, `clio-store.py:223` `for key in ('repo', 'branch', 'machine', 'checkout', 'repo_slug')`, so the update cannot change `record_id` (`:210`). Probe (`HOME=$PWD/.relay-scratch/home python3 .relay-scratch/probe.py`, exit 0; two scratch stores sharing one owner, one synthetic `source_event_id` row, branch `main` vs `feature`, `export_device` then strict `import_device` at a third store): `same record_id: True` / `peer import committed snapshot (main): 1` / `peer import restored-store export (feature): ValueError: identity payload conflict`. Negative control is listed, `:146` "strict peer imports of the subsequent export still succeed; conflicting own payload -> refusal". Ordering gap that remains is F10.
- [Should] **F6 disposition — bounds and metrics accepted, but the new unknown-ID deferral has no upper bound: see F9.** Present as requested: `:119` "Admission is bounded to128 conflict/recovery archives and256MiB total per store … Count and total bytes appear in status … stop rollout if more than12archives/day or32MiB/day per Mac".
- [Pass] **F7 disposition.** `:111` "Report own committed-local/unsent/restored/label-restored counts explicitly (not remote-delivery acknowledgement)".
- [Pass] **F8 disposition.** `:111` "a nonzero restore also warns to check duplicate owner if this store was not intentionally restored".

New findings:

- [Should] **F9 — unknown-ID deferral never expires, so one peer going offline with an unsent capture freezes every other Mac's note; this is the Studio-off case the plan exists for.** `:119` "if any well-formed incoming record ID is not known locally, defer note replacement byte-intact with waiting_for_history status … after Git snapshots arrive the next tick revalidates and repairs". Nothing covers the snapshot not arriving. Rendering is every 300 s and delivery hourly (`:9` "Studio collector currently hourly", `:123` "UTC 300-second cutoff bucket"), so a Mac that captures, renders, and is shut down before its next Pulse cycle leaves a synced note holding an ID no peer can receive. The travel Mac then reports `waiting_for_history` on every tick and never adds its own captures to the note until the Studio returns, against `:9` "refresh the SAME existing Obsidian note while the Studio is off". The pilot rule only covers the other direction (`:119` "if unknown-ID deferral does not clear after verified delivery"). The same freeze follows an ID from an origin outside the inventory or one whose snapshot is refused.
  Fix (one sentence in `:119`, one control in `:129`): persist a `waiting_since` UTC when deferral starts, clear it on any tick with no unknown IDs; once it exceeds a stated bound (suggest two Pulse intervals), fall through to the existing archive-then-repair path. At that bound the worst case is 12 archives/day, the pilot threshold already stated. Control: "peer note with unknown ID, no snapshot ever arrives, local capture added → after the bound the note is archived byte-exact and rebuilt including the local capture; before the bound it is byte-intact".
  Observed input: plan text above; note containing one `clio:record` ID from an origin whose committed snapshot does not advance.
  Affected scope: repair-opt-in Macs whose current note carries a well-formed record ID absent locally for longer than the bound.
  Falsifier: clone fixture holding such a note with no new snapshot across N ticks plus one new local capture — if the note includes the local capture within a stated time without this change, it is unnecessary. Expected under current text: byte-intact indefinitely.

- [Should] **F10 — nothing orders the owner export after own-origin reconcile, so the label conflict F5 fixes can still be published first.** Reconcile runs in the 300 s `scheduled-export` (`:115`); the owner export runs in the hourly collector (`:37` "drains bounded local pending receipts, exports this owner to PRIVATE staging … verifies its manifest"). The only pre-publication comparison is by ID (`:41` "compare known IDs/owner before replacing its prior snapshot"). If the collector fires after the tailer has redelivered rows into a restored store but before the next reconcile, the snapshot has the full ID set with changed labels, passes an ID-only check, and is committed. Peers then refuse it (probe line above: `ValueError: identity payload conflict`), and the next local reconcile sees its own HEAD already carrying the changed labels, so nothing is restored. That origin stays stopped at every peer until a human intervenes.
  Fix (one sentence, `:113` or `:115`, plus one control in `:146`): when fleet is configured, `export-device` for the owner first compares against the committed own snapshot at pinned HEAD and refuses if any committed record ID is missing locally or has a different payload; equivalently, state that own reconcile runs inside the same export call before serialization. Control: "restored store, redelivered row with changed label, export attempted before reconcile → refused, no snapshot written".
  Observed input: own store row `{source_event_id:'evt-1', branch:'feature'}`; committed own snapshot and peer hold the same `record_id` with `branch:'main'`.
  Affected scope: fleet-configured owner export of `source_event_id` rows whose labels differ from the committed own snapshot.
  Falsifier: clone fixture running the collector-order export on that store before any reconcile — if the export is refused or emits `main`, the change is unnecessary. Expected today: snapshot emitted with `feature`.

- [Should] **F11 — the label-restore recovery archive shares the 128-file cap without saying how many files one restore creates.** `:111` "preserve the previous local observation in an exclusive verified private recovery archive before updating"; `:119` "bounded to128 conflict/recovery archives … reaching the cap refuses further unsafe replacement". If the archive is per row, a restored store with more than 128 redelivered rows exhausts the budget in its first reconcile, the own origin stops, and note repair is blocked on that Mac as well.
  Fix: state one recovery archive per reconcile transaction holding all replaced observations, deduplicated by SHA-256.
  Observed input: plan text; restored store with 129 label-changed own rows.
  Affected scope: own-origin label restore touching more than one row in a tick.
  Falsifier: clone fixture restoring 129 label-changed rows — if it completes with one archive and `archive_budget_exhausted` is absent, no change is needed.

- [Nit] **F12 —** `repo`, `machine` and `repo_slug` are stored as indexed columns as well as in the payload (`clio-store.py:237-239`), and `query` filters on the columns (`:451-453`). Say the label restore updates the payload and those three columns together, and add a `query --repo` check to the F5 control.
- [Nit] **F13 —** in fleet mode a note refusal (changed header, archive budget, archive failure) should not stop drain, reconcile or the compatibility export. Today the note check runs first and raises (`clio-store.py:841` before `drain` at `:842`). `:119` states continuation only for `waiting_for_history`; extend the same wording to every refusal and add it to the `:129` header-edit case.
- [Nit] **F14 —** `:111` and `:150` cite `temp/gh3-own-replay-proof.json`, which is ignored (`.gitignore:8` `/temp/`) and absent from the reviewed commit. Word it as an uncommitted local probe or record it in the committed TESTS-RESULTS provenance at implementation.

Confirmed unchanged from prior rounds:

- [Pass] Committed blobs only, bounded, no Git writes: `:111` "read ONLY `devices/<UUID>/clio.jsonl` committed blobs, not dirty worktree files. No fetch, add, commit, push, reset, stash or network call … Bound Git calls (5s each, max16origins, total monotonic budget30s)".
- [Pass] No general self-import or conflict relaxation: `:111` "The ordinary import-device CLI continues to refuse self-import … A true identity/prompt/extras/reference conflict still refuses"; existing guard `clio-store.py:746` `raise ValueError('snapshot claims this store as origin; refuse self-import')`.
- [Pass] No new pusher/service/authority; #282 and pilot stay outside this PR: `:115` "No extra scheduler/pusher … not a claim that unrelated Rebalance runtime was modified"; `:132` "required before automatic fleet operation can be called installed".
- [Pass] Header protected and race stated honestly: `:119` "A malformed or changed header … refuses byte-intact and retries next tick"; `:121` "Do not claim lossless protection of such a concurrent human edit."

VERDICT: FAIL
Basis: F5, F7 and F8 dispositions are correct and F5 is reproduced. No history-loss path found. Two gaps leave a Mac needing a human, which the automatic-recovery requirement rules out: the new deferral has no expiry, so a powered-off peer with one unsent capture freezes the note on every other Mac (F9), and the owner export can publish the changed labels before reconcile restores them (F10, same reproduced conflict). F11 is an unstated archive granularity that can exhaust the cap in one restore. All three fixes are plan text only, one sentence and one control each; no redesign or new machinery requested. F12–F14 are optional.

handing off to Producer — go to the Producer window and say 'take your turn' (disposition F9–F14, edit plan text, bump ROUND to 2).

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
