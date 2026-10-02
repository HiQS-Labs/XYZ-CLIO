# RELAY · gh3-auto-plan-fable
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
6. **Commit only the relay file** (`relay(gh3-auto-plan-fable): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-auto-fable-plan-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-auto-fable-plan-packet.md
```
Review the executable automatic-recovery revision in doc/gh3-device-independent-plan.md and bounded recon delta. Entire relevant CLIO helper/tests and installed Rebalance publisher seams described in recon. Prior manual/fixed-publisher options superseded. Grade trusted committed snapshot imports, no echo/bootstrap old origins, eventual generated-note convergence under Obsidian Sync with exact byte reproduction and protected personal header/content, honest unknown/human race limits, scheduled path reuse, no new publisher/service/store, bounds/rollback/proofs. CLIO-only source PR5 and native Rebalance282 wiring/deployment boundary explicitly separate; no claim existing GPS already invokes CLIO. Approve only implementable safe scoped mechanism; concrete actionable findings with falsifiers. Do not run suites in worktree, touch installed files, or write artifact. Only relay thread edits.

Protocol: on approval, set STATUS Approved and end with relay closed. Do NOT release the token back to Producer; either mark tick done as the reviewer or leave the claim for the shim to close. Prior gh3-auto-plan-agy review text approved but driver exit4 close-mismatch because reviewer released rather than completed the token. Reconfirm the same plan and close correctly; no substantive plan changes.

This is the requested SECOND plan QA after Agy attested Approved in gh3-auto-plan-agy-r2. Independently stress the executable mechanism and its consistency/data-loss assumptions, not only the prior positive review. Model claude-fable-5-1 high effort. Scope CLIO PR5 seams with Rebalance wiring explicitly gated; grade plan readiness for that implementation, not deployed fleet readiness.
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

Read in full: `doc/gh3-device-independent-plan.md` (1–138), `doc/recon-gh3-device-independent.md` (1–35), `utils/CLIO/clio-store.py` (1–877), prior thread `gh3-auto-plan-agy-r2.md`. No suites run (clone-only). One external read-only probe, quoted in F1. Pre-existing helper code: no defect found with an observed failing input; one unobserved Nit (F4).

- [Should] **F1 — the failure bet assumes whole-file overwrite; Obsidian Sync's documented default for Markdown is a content merge.** Plan `:105` bets "local views may temporarily be overwritten by delayed Sync delivery … the next successful existing exporter restores the correct combined view"; `:119` "later valid generated writes are repaired on next tick". Probe: `WebFetch https://obsidian.md/help/sync/troubleshoot` (2026-10-01, HTTP 200 after 301 from help.obsidian.md) returned, quoted: "Obsidian Sync merges the changes using Google's diff-match-patch algorithm." / "For all other files, including canvases, Obsidian uses a 'last modified wins' approach." / "Automatically merge (default): Obsidian Sync combines all changes from different devices into a single file." / "Create conflict file: When Obsidian finds conflicting changes, it creates a separate conflict file instead of merging automatically." / "Conflict resolution settings are device-specific. You must configure your preferred option on each of your devices." Consequence under the plan's own rule (`:117` "exact byte equality … human/unsupported body or header edits remain untouched and produce content-free refusal"): a merged hybrid of two valid generated notes (two Macs rendered different cutoffs/record sets before syncing — the ordinary sleep/offline/rejoin case, since `:105` renders offline and Pulse is hourly) reproduces from no single cutoff, is indistinguishable from a human edit, and is refused on every Mac that receives it. That is fail-safe (nothing personal overwritten) but it is a permanent stall needing a human, i.e. the opposite of the `:87` acceptance requirement, and "next exporter restores" is then untrue. The plan held Option A to this standard (`:87` "not a completed answer while it depends on an unproved … capability"); the same applies here. The alternative setting creates stray conflict files in the vault and needs a per-device Sync setting change, which `:5`/`:130` place outside this work.
  Fix (plan text only, no redesign): (a) in `:105`/`:119` replace the overwrite assumption with the documented merge default and state the hybrid outcome honestly: refused byte-intact, surfaced in status, automatic recovery NOT achieved in that case; (b) add to step 3 (`:127`) a red/green case "hybrid spliced from two valid generated renderings is refused byte-intact with content-free status"; (c) add to step 6 (`:130`) and the QA gates (`:138`) a named pilot prerequisite: observe the installed conflict behaviour on the registered note with two Macs rendering divergent views offline then rejoining, and keep `--repair-generated-note` off on a second Mac (note rollout stops per `:63`) if merged hybrids or conflict copies appear; any Sync setting change is a separate operator decision.
  Observed input: vendor documentation quoted above; no live hybrid was produced here. [Unverified — needs pilot] for actual installed behaviour and merge output bytes.
  Affected scope: registered note under Obsidian Sync whenever two vaults write different generated bytes before exchanging them.
  Falsifier: pilot run with two Macs rendering divergent cutoffs offline then rejoining; if the note on both is always byte-equal to one side's rendering (no hybrid, no conflict copy) across repeated trials, the added stop rule never fires and the original bet holds.

- [Should] **F2 — peer-Mac note registration route is unspecified and the existing verified route rejects a generated note.** `:109` requires "the existing registered note/verified backup for repair" on each Mac, and `:117` needs "exact configured personal header" plus an identical banner for byte parity. On Macs 2–4 the synced note is already generated output. `clio-store.py:520-522` parses only `<!-- clio:id:` entries and raises `'unrecognized content below the historical marker'` for any other body, while the generated body uses `<!-- clio:record:` (`:689`). So only `--archive-unreconciled-note` (`:586-593`) can register there, its "backup" is a generated snapshot rather than the personal original, and coverage becomes `archived-not-reconciled` (`:596`), which changes rendered bytes (`:683-684`).
  Fix: state in `:109` that `configure-fleet` verifies header bytes and coverage value match the fleet's before enabling repair, name the registration route for non-first Macs, and say which Mac holds the original personal backup.
  Observed input: generated note body beginning `# CLIO — recent 168 hours` (`clio-store.py:680`) passed to `legacy_coverage`.
  Affected scope: `migrate-view` on any Mac whose synced note is already generated; fleet Macs with differing `view.coverage` or `view.header`.
  Falsifier: clone fixture registering a generated note without the archive flag succeeds, or two stores with different coverage render byte-identical notes at one cutoff — expected: both fail.

- [Should] **F3 — store restored from an older backup under the same owner has no stated outcome.** `:111` rejects "a cumulative snapshot missing already known IDs" and skips own-origin insertion; `clio-store.py:745-746` refuses self-import; `:41` forbids publishing a regressed snapshot. A restored store therefore cannot recover its own committed rows and cannot export, so its new captures never deliver. No loss (rows stay local and in Git), but `:111` "check own committed snapshot separately" names no status or recovery for own-committed-IDs-missing-locally.
  Fix: one sentence in `:111`: this state is a distinct surfaced status, export stays refused, recovery is a new owner store importing the old origin as foreign (`:49`), never self-import.
  Observed input: own committed snapshot containing a record ID absent from the local store with the same `metadata.owner`.
  Affected scope: own-origin acknowledgement check in `reconcile-fleet`.
  Falsifier: clone fixture where such a store reconciles, exports and delivers new captures without regression rejection — expected: it cannot.

- [Nit] **F4 —** `device_imports.source` is fed to `Path(...).resolve()` in `safe_output` (`clio-store.py:626`); a committed-blob import should record a value that cannot collide with a real output path. `drain` (`:289-294`) aborts on the first receipt that raises, which would also skip the new reconcile step at `:842`; no reachable failing input found (receipts are normalized before write, `:249-251`).

- [Pass] Committed-blob-only imports, bounded, no Git writes: `:111` "read ONLY `devices/<UUID>/clio.jsonl` committed blobs, not dirty worktree files. No fetch, add, commit, push, reset, stash or network call … 5s each, max16origins, total monotonic budget30s".
- [Pass] No echo and seed of old origins fit existing seams: `clio-store.py:724` `WHERE origin_id=?` (owner only); `:749-750` rejects foreign-owned rows; plan `:113` "explicit `--origin UUID` bootstrap export … never used by the ordinary scheduled producer".
- [Pass] Per-origin atomic import with digest/count/version checks already exists: `clio-store.py:735-743`; receipts keyed `PRIMARY KEY(owner,digest)` (`:139`) support `:39` without schema change.
- [Pass] Personal header/content protection and no Markdown-as-history: `:117` "Reconstruct from SQLite, never trust a marker/hash self-assertion … Never import history from Markdown. Default (repair off) accepted-hash guard stays unchanged"; existing guard `clio-store.py:565-569`.
- [Pass] Honest race limits: `:119` "A local filesystem replace is not a cross-device transaction … Do not claim an unfenced lease or atomic exclusion."
- [Pass] No new publisher/service/store; Rebalance #282 boundary separate: `:115` "No extra scheduler/pusher … not a claim that unrelated Rebalance runtime was modified"; `:130` "required before automatic fleet operation can be called installed".
- [Pass] Rollback and proof scope: `:79` "Never delete delivered snapshots or rewrite Git history"; `:128` "This is isolated simulation, not live cross-device or Obsidian Sync proof."

VERDICT: FAIL
Basis: Replication seams (import, no-echo, bounds, scope split) are implementable and safe as written. The note-recovery bet is not: its stated premise (whole-file overwrite, repaired next tick) contradicts the vendor-documented default for Markdown, and under the plan's own exact-byte rule the likely result is a fail-safe but permanent stall, which the plan neither states nor gates. F1–F3 are plan-text corrections only; no mechanism redesign is requested and no blocker is claimed without an observed failure.

handing off to Producer — go to the Producer window and say 'take your turn' (disposition F1–F4, edit plan text, bump ROUND to 2).

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
