# RELAY · gh3-auto-implementation-fable-r2
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
6. **Commit only the relay file** (`relay(gh3-auto-implementation-fable-r2): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-IMPLEMENTATION-FABLE-R2 --agent claude` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-implementation-r2-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
- Started: 2026-10-02

### Artifact — gh3-auto-implementation-r2-packet.md
```
Goal: QA PR5 implementation of the approved automatic recovery plan.
Operational envelope: four personal Macs, private Git Pulse transport, eventual convergence. This is CLIO source capability only; native Rebalance #282 wiring and real disconnected/Obsidian pilot remain deployment gates. No installed runtime changes are authorized here. Model requested: claude-fable-5-1, high effort.
Read AGENTS.md, doc/gh3-device-independent-plan.md (latest executable section and dispositions), doc/recon-gh3-device-independent.md, utils/CLIO/clio-store.py, test/clio-store.py, new INSTALL.md integration section and TESTS-RESULTS/2026-10-02-gh3-auto-recovery/.
Questions:
1. Do configure/reconcile/export safely consume only committed inventory-matching owner snapshots, with bounded Git calls, partial progress and no push path? Does own recovery precede serialization and retain unsent rows without echo?
2. Are own immutable conflicts refused, original committed delivery labels restored through the sole writer seam, indexed fields consistent, and prior observations grouped into one verified private archive? Are foreign imports strict and cumulative regressions refused?  [Unverified — no citation]
3. Does optional machine-owned body repair preserve exact header/original backup, archive complete unknown merged body before replacement, defer unknown IDs with persistent bounded expiry, and refuse safely at archive quotas/failures? Check compare-before-replace and stated external-edit race without inventing fencing.
4. Do scheduled capture/drain/import/full compatibility outputs continue on note refusals? Are default mode, existing collector scripts/schema/exporter cadence preserved?
5. Does synthetic four-store/Git-checkout coverage demonstrate delivered history parity, outage/rejoin, no echo, old-backup own recovery, 129 label updates in one archive and exact note convergence? Identify missing material controls, proportionately.
6. Is implementation surgical within existing helper, standard library, native issue/PR scope, with truthful source-only rollout limits? Challenge unnecessary machinery.
Reviewer may read/probe narrowly, but do not run test suites in the relay worktree. Existing suites run only in disposable full clone and receipts include commands/exits/source hashes. Findings must cite concrete file:line inputs/falsifiers. Approve only when no implementation blocker remains. Keep writes confined to relay file. Default generic release on findings; on approval obey seeded token rule and tick done, never release Approved to Producer. Append without rewriting earlier text.

Round1 disposition focus: prior relay gh3-auto-implementation-fable.md contains observed F1–F7. Verify all dispositions above in the plan and current code, including path resolution on macOS /var aliases. scheduled-path-red.log is pre-fix actual assertion failure; refreshed six-command receipts cover the revised helper. Review remaining whole-file issues proportionately. Same source-only envelope, same model/high effort; append only and do not rewrite seeded packet (including whitespace).
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

### Reviewer · Round 1 (claude, claude-fable-5-1)

swept file: yes — `utils/CLIO/clio-store.py` read in full (1–1175, pre-existing code included); `test/clio-store.py` four-store case 499–670 plus the full `cb66f5d..112c51c` diff; INSTALL.md 823–840; plan "Implementation Fable high Round1 dispositions"; every file under `TESTS-RESULTS/2026-10-02-gh3-auto-recovery/`; prior thread `gh3-auto-implementation-fable.md` F1–F7. No suites run here. Candidate = 112c51c. `shasum -a 256` helper/test/INSTALL = `5ccd32ae…`/`6f786d11…`/`114d8977…`, equal to `provenance.jsonl` line 7 `sources`; `shasum -a 256 check-*.log` equals provenance lines 1–6 (`b3b337eb…`, `f37e1714…`, `3ec02a7d…`, `53222ef9…`, `0aabc370…`, `de0b251f…`), all `"exit": 0`. Probe: `python3 .relay-scratch/probe_r2.py` (exit 0; synthetic rows, throwaway HOME, hand-written config, non-existent fleet checkout, no Git writes).

**Round-1 dispositions (prior thread F1–F7)**

- [Pass] F1 implemented: `clio-store.py:1108-1109` `elif Path(args.markdown).expanduser().resolve() != Path(activated['view']['path']): raise ValueError('scheduled destination differs from registered note')`, placed before both the fleet (`:1110`) and default (`:1139`) branches. macOS `/var` alias: both sides are resolved — `view.path` is stored from `existing_destination` (`:526` `.resolve()`, `:679`), the argument is resolved at `:1108`; the fixture passes the unresolved temp path (`test/clio-store.py:527,650`) and reaches the fleet branch with exit 0 (`:651`). Controls `test/clio-store.py:614-615` (fleet) and `:620-621` (default) assert non-zero exit and byte-identical unrelated file; `scheduled-path-red.log` shows the pre-fix helper failing exactly `line 614 … AssertionError: 0 == 0`. Side effect: G1 below.
- [Pass] F2 implemented: `:1006` and `:1119` now include `AttributeError, OverflowError` (and `TypeError, KeyError` at `:1119`). Dropping the literal `TimeoutError` at `:1006` loses nothing — it is an `OSError` subclass and `OSError` remains in the tuple. Control: `test/clio-store.py:642-656` commits `generated_at: None` for one origin and removes another; asserts `error` / `missing` / `accepted`, exit 0.
- [Pass] F3 implemented inside the existing case, no new suite: fleet CLI header refusal with compat refresh and intact note `:648-660`; peer bytes accepted with `peer_generated` and unchanged archive count `:635-638`; `partial` persisted `:662`.
- [Pass] F4 implemented: `:1136` `latest['fleet']['last_result'] = dict(fleet_result, archives=recovery_metrics(path))`.
- [Pass] F5 implemented: `:600-601` pops `waiting_since` on an accepted hash; persisted by the existing config write at `:793`.
- [Pass] F6 implemented: `:923` `env = dict(os.environ, GIT_NO_LAZY_FETCH='1')`.
- [Pass] F7: receipts README last paragraph states "The jq parse-error line in the capture suite is its intentional invalid-input control"; fixture handles use `contextlib.closing` (`test/clio-store.py:559,585,596,600`). `check-5.log` has no `ResourceWarning`; the 14 lines left in `check-6.log` are all `threading.py:301` / `pathlib` (`rg -n ResourceWarning check-6.log`), i.e. outside the four-store case and pre-existing.

**New findings**

- **[Should] G1 — the F1 guard resolves the final path component, so in fleet mode a registered note that became a symlink now aborts the whole scheduled run instead of being a note refusal.** Non-blocking: fails closed (nothing overwritten, exit 3, diagnostic line each run), pending captures stay queued, and default mode behaved this way before PR5. It is a regression only against cb66f5d's fleet branch and packet Q4 ("continue on note refusals").
  - Observed input: probe case B — same config/DB, registered `vault/note.md` replaced by a symlink to `vault/elsewhere.md`, then `scheduled-export vault/note.md`. Output: `old(cb66f5d) B note->symlink: rc= 0 note_status= {'error': 'ValueError', 'reason': 'publication_guard', 'state': 'refused'} stderr=  compat refreshed= True` vs `new(112c51c) B note->symlink: rc= 3 note_status= None stderr= ValueError: scheduled destination differs from registered note compat refreshed= False`. Case A (regular note) is `rc= 0 … 'published'` on both.
  - Affected scope: fleet-configured `scheduled-export MARKDOWN` where `MARKDOWN` names the registered path but its last component is a symlink. Drain, reconcile, compat JSONL and `last_note_status` are all skipped for that run.
  - Falsifier: in the four-store case replace node 1's note with a symlink and run `scheduled(node, note)` → expect exit 0, `note_status.state == 'refused'`, compat refreshed, symlink target byte-identical. If the plan intends a symlinked note to stop the whole fleet run, decline and say so in INSTALL.md 838.
  - Fix: at `:1108` compare `dest.parent.resolve() / dest.name` (with `dest = Path(args.markdown).expanduser()`) to `view['path']` and pass that same value to `project()` at `:1126`/`:1141`, so the existing `:761-763` symlink refusal handles it as a note refusal. Three lines, one assertion. Suggested as a follow-up before the second-Mac deployment gate; not required for this approval.
- **[Nit] G2** — probe case C: `snapshot_records(b'[' * 200000 + b'\n')` → `NOT in :1006/:1119/:1162 tuples -> RecursionError`. A committed blob with pathological nesting would traceback the scheduled run. `encode()` on the exporting side cannot produce such a row, so no fleet Mac can emit it; no change requested.
- **[Nit] G3** — carried from F7, undispositioned: duplicate `import re` at `:204`. Also `:939` message typo `'1 to16'`. On a raised reconcile the persisted result (`:1120`) has no `at` stamp.
- Pre-existing code outside the fleet paths (`:1-580`, `:639-743`, `:1015-1023`): re-read; no new defect found beyond G3.

**Passes by packet question (current line numbers)**

- [Pass] Q1: HEAD pinned once `:976-979`; only `rev-parse` and `cat-file -s`/`cat-file blob` on `head + ':devices/' + owner + '/clio.jsonl'` `:981-986`; per-call `timeout=min(5, remaining)` `:928`, 30 s budget `:972`, ≤16 origins `:970`, 64 MiB per blob `:984`; no push/fetch verb in the file. Owner/path match `:827-828`; partial progress per origin `:998-1007`. Own recovery precedes serialization and refuses on own error `:801-804`; export is own-origin only `:814`; unsent rows counted, not deleted `:878`. Budget headroom measured: probe case D `snapshot_records 20000 rows, 16926871 bytes: 0.37s`.
- [Pass] Q2: own immutable conflict refused `:862-864`; labels restored only through `insert` with payload and indexed columns together `:249-250` (the five fields excluded by `identity_payload` `:231` are the only ones that can differ; `branch`/`checkout` live in payload only); one grouped archive before any update `:866-871`; foreign stays strict (`replay=own, restore_labels=own` `:871`); cumulative regression refused `:857-858`; generic self-import refused `:853-854`.
- [Pass] Q3: exact header prefix `:605-606`; pinned header/coverage `:588-590`; backup hash `:584-585`; complete file archived `:632` before the accepted-hash write `:792-794`; archive exclusive, verified, deduplicated, quota-bound `:896-910`; unknown-ID wait persisted and bounded `:612-618`; compare-before-replace `:789-791`; external-edit race stated, not fenced (INSTALL.md 840).
- [Pass] Q4 (except G1): drain errors do not stop reconcile `:1112-1116`; compat output precedes and is independent of the note attempt `:1122-1131`; default branch unchanged apart from the guard `:1140-1142`; schema untouched `:129-156`, `VERSION = 1` `:23`; 300 s cutoff bucket only with fleet configured `:749-750`.
- [Pass] Q5: receipts `check-5.log`/`check-6.log` `Ran 16 tests … OK` under both runtimes; parity `test/clio-store.py:561-565`, outage/rejoin `:567-571`, dirty-file exclusion `:573-578`, 129 labels → one archive `:581-597`, no echo `:598`, own restore + unsent `:600-607`, regression `:664-670`, plus the F3 controls above. [Unverified — needs clone run]: I did not re-execute any suite; the harness gate does.
- [Pass] Q6: 12 changed helper lines in 112c51c, stdlib only (`:3-20`), no new command, timer, schema or store; source-only limits stated (INSTALL.md 823–825, 840; receipts README paragraph 4 "No live cross-device delivery/Obsidian Sync pilot is claimed").

VERDICT: PASS
Basis: All seven round-1 findings are implemented and each has a cited control or line; source hashes and log hashes match the receipts. No implementation blocker remains. G1 is a fail-closed availability regression on an improbable input and is recorded as a pre-deployment follow-up, G2–G3 are nits. Source-only envelope unchanged: native Rebalance #282 wiring and the disconnected/Obsidian pilot remain deployment gates. Relay closed (Approved), no further turn needed; token completed with `done`, not released.


### Attestation · relay-drive — 2026-10-02T07:12:25Z
task: CLIO-GH3-AUTO-IMPLEMENTATION-FABLE-R2
reviewer: claude
status: Approved
reviewed-head: 48501fca4c66574c26769d619debd9143af5dc47
added-range: 8915+8849
added-sha256: d3e6341ba11bd7c096370928797214f7335c808b3a2a28e02cc73c0b4ba3fa12
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
