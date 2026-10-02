# RELAY · gh3-auto-implementation-fable-r4
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
6. **Commit only the relay file** (`relay(gh3-auto-implementation-fable-r4): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-IMPLEMENTATION-FABLE-R4 --agent claude` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-implementation-r4-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
- Started: 2026-10-02

### Artifact — gh3-auto-implementation-r4-packet.md
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

Final incremental focus: gh3-auto-implementation-fable-r2.md attested Approved. Only G1 symlink progression fix, RecursionError isolation, timestamp/typo/duplicate-import nits, and existing-case red/green control are added. Verify scheduled-export resolves parent only, passes canonical registered final component to project, and symlink note refusal still refreshes history without changing target. Review final exact hashes/receipts and ensure no regression; retain full source sweep obligations, proportionate existing scope. Do not demand live fleet deployment for source approval. No source edits allowed; on approval tick done as seeded.

Latest H1 only: Round3 found an existing registered symlink alias regression. The cheap scheduled guard now accepts canonical registered final component OR alias resolving exactly to the registered real path; on alias it passes canonical path to project. Existing-case tests cover both default/fleet alias publication, changed-to-symlink note-local refusal and unrelated-destination refusal, with registered-alias-red.log plus refreshed six-command exact source receipts. No redesign or other changes. Read current code and ensure the three path identities work together; whole-file sweep remains required. Approve if no blocker remains; finish token with done.
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

swept file: yes — `utils/CLIO/clio-store.py` read in full this turn (1–1178, pre-existing code included); `test/clio-store.py` 495–699 (whole four-store case); plan "Implementation Fable high Round3 disposition" (`doc/gh3-device-independent-plan.md:164-166`); receipts README, `provenance.jsonl`, `check-5.log`, tail of `check-6.log`, `registered-alias-red.log`; prior thread `gh3-auto-implementation-fable-r3.md` H1. INSTALL.md not re-read: its hash `114d8977…` is unchanged from the round-3 review. No suites run here; no git writes by me. `shasum -a 256` helper/INSTALL/test = `4ab6c0a2…`/`114d8977…`/`27b4cbd1…`, equal to `provenance.jsonl` line 7 `sources`; `shasum -a 256 check-*.log` = `b3b337eb…`, `f37e1714…`, `3ec02a7d…`, `53222ef9…`, `9fb6ab11…`, `831d8a62…`, equal to provenance lines 1–6, all `"exit": 0`. Probe: `/usr/bin/python3 .relay-scratch/probe_r4.py utils/CLIO/clio-store.py` → `exit=0` (Python 3.9.6; synthetic row, throwaway HOME under `.relay-scratch/tmp`, CLI-only `init` / `activate --fresh` / `capture` / `migrate-view` / `scheduled-export`; fleet cases point at a non-existent checkout, so no Git object is read or written). Repeated under `/opt/homebrew/bin/python3` (3.14.7): same results except case L below.

**H1 (round 3) — the three path identities**

- [Pass] H1 implemented as dispositioned, three lines, no new machinery: `clio-store.py:1109-1112` `elif destination != Path(activated['view']['path']):` / `if destination.resolve() != Path(activated['view']['path']): raise ValueError('scheduled destination differs from registered note')` / `destination = Path(activated['view']['path'])`. Parent-only resolution is retained at `:1098-1099`, and the same `destination` reaches `project()` in both branches (`:1129` fleet, `:1144` default).
- [Pass] Identity 1, canonical registered final component: unchanged path. Measured `A default canonical regular note | rc= 0 | … markdown= note.md | compat= True | registered_file_rewritten= True` and `A fleet … note_status= {'state': 'published'}`; parent-directory alias `P default parent-dir alias | rc= 0 | … registered_file_rewritten= True`, `P fleet … {'state': 'published'}`.
- [Pass] Identity 2, alias resolving exactly to the registered real file, the round-3 failing input: `S default view.path is real file: True | arg is symlink: True` then `S default registered-via-symlink alias | rc= 0 | stderr=  | … markdown= real-note.md | compat= True | registered_file_rewritten= True` and `S fleet   registered-via-symlink alias | rc= 0 | … note_status= {'state': 'published'} | markdown= real-note.md | compat= True | registered_file_rewritten= True`; `alias still symlink: True` in both modes. `markdown= real-note.md` shows `project()` received the canonical registered path, not the alias. Round 3 measured `rc= 3` for the same input.
- [Pass] Identity 3, registered file later becomes a symlink: `destination == view.path`, so `:1110` is not consulted and `:760-762` refuses note-locally. `G fleet   registered note became symlink | rc= 0 | … note_status= {'error': 'ValueError', 'reason': 'publication_guard', 'state': 'refused'} | … compat= True | registered_file_rewritten= False`, `other untouched: True | still symlink: True`. Default mode keeps its existing single-call refusal: `G default … rc= 3 | stderr= ValueError: registered note became a symlink; publication refused`, target untouched.
- [Pass] Unrelated destinations stay rejected in both modes, nothing written: `U1 … unrelated regular file | rc= 3 | stderr= ValueError: scheduled destination differs from registered note`, `U2 … symlink to unrelated file | rc= 3 | (same)`, `stray untouched: True`.
- [Pass] Controls and receipts: `test/clio-store.py:639-652` registers the alias (`already_registered`), then asserts `scheduled(node, alias).returncode == 0` in fleet mode (`:644`) and with `fleet` popped (`:649`); `:653-665` keeps the changed-to-symlink control; `:614`, `:620` keep the unrelated controls. `registered-alias-red.log` shows the pre-fix failure at exactly `line 644 … AssertionError: 3 != 0`. `check-5.log` and `check-6.log` end `Ran 16 tests … OK`. [Unverified — needs clone run]: I did not re-execute any suite; the harness gate does.

**No regression in earlier passes (current line numbers; the only helper change since round 3 is `:1109-1112`)**

- [Pass] Q1: HEAD pinned once `:975-978`; only `rev-parse` and `cat-file -s` / `cat-file blob` `:982-985`; `timeout=min(5, remaining)` `:927`, 30 s budget `:971`, ≤16 origins `:969`, 64 MiB `:983`, `GIT_NO_LAZY_FETCH` `:922`; own recovery precedes serialization and refuses on own error `:800-803`; export is own-origin only `:813`; unsent rows counted, not deleted `:877`. No push or fetch call exists in the file.
- [Pass] Q2: own immutable conflict refused `:861-863`; labels restored only inside `insert` with payload and indexed columns together `:243-249`; one grouped archive before updates `:865-866`; foreign strict `:870`; cumulative regression refused `:856-857`; generic self-import refused `:852-853`.
- [Pass] Q3: header prefix `:604-605`; pinned header/coverage `:587-589`; backup hash `:583-584`; whole file archived `:631` before the accepted-hash write `:791-793`; archive exclusive, verified, quota-bound `:895-909`; bounded wait `:612-617`, cleared on accepted note `:599-600`; compare-before-replace `:788-790`.
- [Pass] Q4: drain errors isolated `:1115-1119`; compatibility output precedes and is independent of the note attempt `:1124-1134`; schema `:129-156` and `VERSION = 1` `:23` untouched; 300 s cutoff bucket only with fleet `:748-749`; default branch `:1142-1145` unchanged apart from the canonical `destination`.
- [Pass] Q5: four-store controls `test/clio-store.py:561-565` parity, `:566-571` rejoin, `:572-578` dirty exclusion, `:579-597` 129 labels → one archive, `:598` no echo, `:599-609` own restore + unsent, `:668-691` bad/missing origins, `:692-699` regression.
- [Pass] Q6: stdlib only `:3-20`; no new command, timer, schema or store in this increment; receipts README still states "No live cross-device delivery/Obsidian Sync pilot is claimed".

**Nits — no change requested, none blocks**

- [Nit] Compound residual already named in round 3: an alias whose target is the registered path, where the registered path itself later became a symlink, aborts the tick instead of refusing note-locally. `R fleet   alias to registered-turned-symlink | rc= 3 | stderr= ValueError: scheduled destination differs from registered note | … compat= False`, `other untouched: True`. Fails closed; captures stay committed or queued; needs two unusual states at once.
- [Nit] Pre-existing, interpreter-dependent: a self-referential symlink given as the scheduled destination raises an uncaught `RuntimeError` from `destination.resolve()` at `:1110` on Python 3.9 (`L default symlink loop argument | rc= 1 | stderr= RuntimeError: Symlink loop from '…`), versus `rc= 3 … scheduled destination differs from registered note` on 3.14.7. Nothing is written either way; the round-2 guard and `:763` resolve the same way, so this is not introduced by H1. `RuntimeError` is absent from the catch at `:1165`, so no line reaches the diagnostics log on 3.9.
- [Nit] `test/clio-store.py:644` asserts only exit 0 in fleet mode, which a note refusal would also satisfy; the default-mode assertion `:649` and the probe line `S fleet … {'state': 'published'}` cover publication. Asserting `note_status.state == 'published'` there would tighten it.
- [Nit] `provenance.jsonl` line 7 still records `head: 2a64aa84…` before and after; the receipts are tied to the candidate by the three source hashes, which match.
- Pre-existing code outside the fleet paths (`:1-580`, `:638-742`, `:1014-1021`): re-read this turn; no other defect found.

VERDICT: PASS
Basis: H1 is fixed as dispositioned in three lines; the canonical path, the registered alias and the changed-to-symlink note each behave as specified in default and fleet mode on measured inputs, unrelated destinations stay rejected, and source/receipt hashes match provenance. No implementation blocker remains; four nits are recorded without a change request. Suites were not re-run here (harness gate). Source-only envelope unchanged: Rebalance #282 wiring and the disconnected/Obsidian pilot remain deployment gates. Relay closed (Approved), no further turn needed.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
