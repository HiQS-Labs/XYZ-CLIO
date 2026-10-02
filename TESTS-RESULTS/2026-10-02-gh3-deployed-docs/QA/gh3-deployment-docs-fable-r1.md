# RELAY · gh3-deployment-docs-fable-r1
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-02.
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
6. **Commit only the relay file** (`relay(gh3-deployment-docs-fable-r1): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval call task done with the exact absolute env-pinned tick command provided in your native turn prompt. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **docs-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
- Started: 2026-10-02

### Artifact — docs-packet.md
```
Review docs-only reconciliation after CLIO5 and Rebalance303 merge and verified Studio activation. Read diff against origin/main for README, INSTALL and two GH3 handoff/plan docs. Actual deployment receipt is at env QA_DEPLOYMENT_RECEIPT; private capture data is not accessible or necessary. Confirm current status is accurate, earlier capture/collection notes are clearly historical, no unsupported all-Mac/offline/source-coverage/Sync claim, no further gap collection, original header/path/knownhistory contract remains, owner-only normal exports versus one-time bootstrap clear. Canonical helper hash4ab6c0a2... unchanged; complete old install prefix retained apart from dependency wording, new text appended afterscript blocks. Existing source suites were run in CLIO5; no new runtime tests claimed for prose changes. Rebalance also records independent Fable-high QA, 2807fullcases/146subtests and focused followup492/28. Do not execute suites or edit docs; append review only. Use native task done for approval. Grade concrete findings.  [Unverified — no citation]
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

### Reviewer · Round 1 (claude)

swept file: yes — full diff `origin/main...HEAD` (87 lines, 4 docs + this packet's README/provenance), plus
whole-file status sweep of `README.md`, `doc/gh3-device-handoff.md` (all 40 lines), the status-bearing lines of
`doc/gh3-device-independent-plan.md` and the SQLite/fleet sections of `utils/CLIO/INSTALL.md` (318–330, 530–536,
821–863). No suites, fixtures or `validate.sh` were run; no file other than this thread was written. Pre-existing
defects found in the swept docs: none blocking; two stale-wording nits below (N1, N2).

Probes (read-only; scratch under `.relay-scratch/tmp`):
- `shasum -a 256 utils/CLIO/clio-store.py` → rc=0, `4ab6c0a2519e5431065678fc87fde158ff51d498650bda4be14768e1d6529d6a`.
- `git diff --quiet origin/main...HEAD -- utils/CLIO/clio-store.py test utils/CLIO/*.sh` → rc=0 (no runtime/test diff);
  `git diff --name-only` lists only the 4 docs and 3 files under `TESTS-RESULTS/2026-10-02-gh3-deployed-docs/`.
- Line-by-line compare of `origin/main:utils/CLIO/INSTALL.md` (840 lines) with HEAD (863) →
  `differing lines within old length: [533]`; code fences `old 38 new 38`, last fence at line 834.
- `rg -n -c "/Users/|<uuid regex>"` over the 4 docs + packet README/provenance → rc=1 (no match).
- Receipt read at `$QA_DEPLOYMENT_RECEIPT` (`…/rebalanceos-gh282-deploy-followup/TESTS-RESULTS/2026-10-02+GH-282/deployment.json`),
  committed in that clone at `16582d2` on `origin/codex/gh282-deploy-followup`.

Findings:
- **F1 [Pass] Helper unchanged.** Measured hash equals `provenance.jsonl:1` `"canonical_helper_sha256": "4ab6c0a2519e…29d6a"`;
  runtime diff rc=0 matches `"runtime_code_changed": false`.
- **F2 [Pass] Old install prefix retained; new text appended after script blocks.** Only old line 533 differs
  (`utils/CLIO/INSTALL.md:533` "That integration uses Rebalance #282's" — the dependency wording); fence count is
  unchanged at 38 and the new section starts at `utils/CLIO/INSTALL.md:842`, after the last fence (834). Heredoc
  extraction by the test suites is therefore untouched — [Unverified — needs clone run] for the suites themselves; the
  packet claims no new runtime tests.
- **F3 [Pass] Current status matches the receipt.** `INSTALL.md:844` "CLIO #5 and Rebalance #303 are merged" /
  `gh3-device-independent-plan.md:174` "CLIO #5 landed at 6a53a38 and Rebalance #303 at bb84cd0" ↔ receipt
  `"clio_source_head": "6a53a38a…"`, `"runtime_head": "bb84cd0b…"`. "three known preserved origins" ↔ `"known_origins": 3`.
  "five delivery jobs … restored with identical plist hashes" ↔ `"restored_jobs": 5`, `"plist_hashes_unchanged": true`.
  "five-minute exporter" ↔ `"export_interval_seconds": 300`. Header/same note ↔ `"personal_header_preserved": true`,
  `"same_note_path": true`. Backups ↔ `"all_backup_records_preserved": true`, `"all_backup_payloads_preserved": true`,
  `"history_rows": 3969` ≥ `"backup_floor_rows": 3962`. Queued→delivered lesson ↔ `"queue_transition": {"health":
  "ALIVE_NOT_PUBLISHING"}` then `"fleet_health": "ALIVE"`, `"delivery_pending": false`, `"no_pending_commits": true`.
- **F4 [Pass] Owner-only normal exports vs one-time bootstrap is clear.** `INSTALL.md:845-847` "bootstrapped once into
  the private Git Pulse checkout. Normal exports carry only its own origin; imported history remains in the full local
  SQLite replica" and lesson `INSTALL.md:852-853` "bootstrap known preserved origins explicitly once, then prevent
  normal foreign-origin echo" ↔ receipt `"owner_only_remote_snapshot": true`, `"delivered_owner_rows": 2821` (< 3969 local rows).
- **F5 [Pass] No all-Mac / offline / source-coverage / Sync overclaim.** `INSTALL.md:858-861` "Other Macs remain
  disabled. This local milestone does not qualify complete four-Mac source coverage, actual disconnected/rejoin behavior
  over three scheduled Pulse intervals, observed Sync conflicts/archive capacity or seven-day delivery rates. The final
  filesystem comparison cannot fence an unseen concurrent Obsidian Sync edit."; `README.md:7` "the four-Mac/offline
  qualification and provenance upgrade remain tracked rollout work"; `gh3-device-independent-plan.md:3`
  "Four-Mac/offline/shared-note qualification remains open" ↔ receipt `"live_fleet_qualification": false`,
  `"other_macs_enabled": false`, and `provenance.jsonl:1` `"live_fleet_qualification": false`.
- **F6 [Pass] Earlier collection notes are marked historical; no further gap collection.** `gh3-device-handoff.md:3`
  "accepted historical gaps need no additional collection. Earlier collection notes below are historical. Use INSTALL.md
  and Rebalance #282 for current rollout gates."; `INSTALL.md:863` "No further history collection is required."
- **F7 [Pass] Header/path/known-history contract intact.** Unchanged `INSTALL.md:324-326` "Migration reuses the **same
  Obsidian path, filename and existing exporter schedule**"; unchanged `INSTALL.md:838` "Exact header and verified
  original backup remain protected"; new `gh3-device-independent-plan.md:174` "preserves the known full SQLite history,
  all verified backup records/payloads, the exact personal header and same seven-day note path".
- **F8 [Pass] No private data published.** rg probe above rc=1 for home paths/UUIDs across the changed docs; packet
  `README.md:3` "Private capture history, paths and origin UUIDs are not published."
- **F9 [Pass] Rebalance QA figures exist as quoted in the packet.** `…/2026-10-02+GH-282/pytest.log:74` "2807 passed,
  21 skipped, 11 xfailed, 2 warnings, 146 subtests passed"; `followup-tests.log:18` "492 passed, 2 warnings, 28 subtests
  passed". The runs themselves are [Unverified — needs clone run]; the four docs do not quote these numbers.
- **U1 [Unverified — operator-attested] Three narrative details have no receipt key:** "committed-history reconcile …
  passed" (`INSTALL.md:847-848`), "Existing capture hooks … were left running" (`INSTALL.md:848-849`), and the
  legacy-health-until-first-check-in lesson (`INSTALL.md:853-854`). `rg -n -i "reconcil|bootstrap|hook|legacy health"`
  over the receipt folder's SUMMARY/provenance/probe logs found no supporting line. Non-blocking: none of them widens
  the fleet claim. Fix (optional, Rebalance-side): add `reconcile_ok` / `capture_hooks_running` keys to the next receipt.
- **N1 [Nit] Same-day contradiction inside the plan doc.** `gh3-device-independent-plan.md:170` (section "Source
  delivery handoff — 2026-10-02") still reads "No installation/Sync changes, merge or clone cleanup occurred … Installed
  Studio continues its earlier verified local pipeline", directly above the new milestone saying both landed and the
  Studio is activated. The line-3 status resolves it, but only if read. Fix: title the new section
  "## Local landing milestone (supersedes the source delivery handoff above)".
- **N2 [Nit] Retained INSTALL prefix still speaks pre-landing.** `INSTALL.md:823` heading "(source capability; rollout
  pending)" and `INSTALL.md:840` "native #282 must land … No fleet runtime or Sync setting is changed by this PR." sit
  just above the milestone. Kept deliberately per the prefix-retention contract and still true for Macs 2–4; the
  handoff doc's closing present-tense line (`gh3-device-handoff.md:40` "No live note repair has been applied") is
  likewise covered only by the line-3 banner. Fix (optional): open the milestone with "Supersedes the pre-landing
  wording above for the Studio only."

VERDICT: PASS
Basis: Every packet claim that can be measured without a clone run holds — helper hash and runtime tree unchanged,
INSTALL prefix differs only at line 533 with all 38 fences intact, and each new status sentence maps to a receipt key
while fleet/offline/Sync/source-coverage qualification is explicitly left open. No Blocker or Should; U1, N1 and N2
are optional wording follow-ups. Definition of Done was left as the scaffold placeholder, so the packet text was used
as the acceptance criteria.

Relay closed (Approved), no further turn needed.


### Attestation · relay-drive — 2026-10-02T20:22:46Z
task: CLIO-GH3-DEPLOYMENT-DOCS-FABLE-R1
reviewer: claude
status: Approved
reviewed-head: 19e46f35980e6c4e96783151cc53b772583f288f
added-range: 6729+8078
added-sha256: 2d1a9a482d7443c8582dd0c26466a71298dca1e3ba11f02d126e8c89b068449c
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
