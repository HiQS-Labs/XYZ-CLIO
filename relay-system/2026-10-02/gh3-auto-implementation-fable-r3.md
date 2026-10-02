# RELAY · gh3-auto-implementation-fable-r3
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-02.
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
6. **Commit only the relay file** (`relay(gh3-auto-implementation-fable-r3): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-IMPLEMENTATION-FABLE-R3 --agent claude` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-implementation-r3-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
- Started: 2026-10-02

### Artifact — gh3-auto-implementation-r3-packet.md
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

swept file: yes — `utils/CLIO/clio-store.py` read in full this turn (1–1176, pre-existing code included); `test/clio-store.py` 495–694 (whole four-store case); INSTALL.md 815–840; plan through "Implementation Fable high Round2 follow-ups" (`doc/gh3-device-independent-plan.md:160-162`); receipts README, `provenance.jsonl`, `check-1..6.log`, `scheduled-path-red.log`, `symlink-progress-red.log` (not re-read: `old-helper-hybrid-red.log`, `wait-timing-red.log`, unchanged scope); prior thread `gh3-auto-implementation-fable-r2.md` G1–G3. No suites run here and no git run by me. `shasum -a 256` helper/test/INSTALL = `f7a74cb8…`/`199ea266…`/`114d8977…`, equal to `provenance.jsonl` line 7 `sources`; `shasum -a 256 check-*.log` = `b3b337eb…`, `f37e1714…`, `3ec02a7d…`, `53222ef9…`, `05cab1fb…`, `d4700e54…`, equal to provenance lines 1–6, all `"exit": 0`. Probe: `python3 .relay-scratch/probe_r3.py` → `exit=0` (synthetic, throwaway HOME, CLI-only `init` / `activate --fresh` / `migrate-view` / `scheduled-export`; fleet cases use a non-existent checkout, no Git writes). The "r2-guard" comparison helper is a scratch copy of the current file with only `:1099` replaced by `destination = destination.resolve()` — an emulation of the round-2 guard, not a checkout of 112c51c.

**New finding**

- **[Blocker] H1 — the G1 fix (`clio-store.py:1098-1099`, `:1109`) breaks every scheduled run, in default and fleet mode, when the scheduled destination was already a symlink at registration.** `existing_destination` fully resolves the destination (`:524-525`) and `migrate_view` stores that resolved real file as `view.path` (`:678`), deliberately tolerating a symlinked job destination (`:526` compares against `detected.resolve()`). The new guard keeps the unresolved final component, so the symlink path can never equal `view.path` and the tick aborts before drain, reconcile, compatibility JSONL and note. This is a regression in default mode (packet Q4 "default mode … preserved"; final focus "ensure no regression"), and it came from my own round-2 fix suggestion, which did not consider this input. Fails closed: nothing is overwritten, exit 3, one diagnostic line per tick; committed captures are unaffected, pending receipts stay queued.
  - Observed input: probe case S — `vault/note.md` is a symlink to `vault/real-note.md`; `migrate-view --markdown vault/note.md --publishers-paused --archive-unreconciled-note` succeeds and registers `view.path == real-note.md` (`S registered view.path == real file: True | arg is symlink: True`); then `scheduled-export vault/note.md`. Output, default mode: `r2-guard(emulated) S default, registered-via-symlink | rc= 0 | stderr=  | note_status= None | compat_refreshed= True | real_note_rewritten= True` versus `r3(a90531f) S default, registered-via-symlink | rc= 3 | stderr= ValueError: scheduled destination differs from registered note | note_status= None | compat_refreshed= False | real_note_rewritten= False`. Fleet mode on the candidate is the same: `r3(a90531f) S fleet,   registered-via-symlink | rc= 3 | stderr= ValueError: scheduled destination differs from registered note | … compat_refreshed= False`. (The emulated-guard *fleet* S line is not relied on: my probe rewrote the config from a pre-publish copy, so its `refused` is a probe artifact. The candidate's rc 3 is raised at `:1110` before any hash is consulted.)
  - Affected scope: `scheduled-export MARKDOWN` where `MARKDOWN`'s final component is a symlink whose target is the registered `view.path`. Both branches (`:1111` fleet, `:1140` default). Regular-file notes and parent-directory aliases are unaffected (below).
  - Falsifier: (a) with the fix, probe case S must give `rc= 0`, note published to the real file, compat refreshed, while case G stays `rc= 0 … 'state': 'refused'` and the unrelated-path controls at `test/clio-store.py:614,620` stay non-zero; (b) alternatively, if a symlinked job destination is declared unsupported, decline this and instead make `migrate_view`/`existing_destination` refuse a symlinked final component at registration and say so in INSTALL.md 827 — then case S fails at `migrate-view`, never at the timer, and H1 is moot.
  - Fix (two lines, no new machinery): after `:1099`, `registered = Path(activated['view']['path'])` inside the existing `with`, and replace the `:1109` test with `elif destination != registered and destination.resolve() != registered: raise …`; when `destination != registered` but `destination.resolve() == registered`, set `destination = registered` so `project()` receives the canonical registered path. Case G is untouched (there `destination == registered`, and `:760-762` still refuses the symlink note-locally); an unrelated path or a symlink to an unrelated file still fails both comparisons. Add one assertion to the existing four-store case (register-through-symlink then `scheduled()` → exit 0), with the pre-fix red log beside `symlink-progress-red.log`. Residual, not requested: destination symlink → registered path that itself later became a symlink still exits 3.

**Round-2 follow-ups (G1–G3)**

- [Pass] G1 as specified: parent-only resolution `:1098-1099` `destination = destination.parent.resolve() / destination.name`; the same value reaches `project()` at `:1127` and `:1142`; `:760-762` then raises `'registered note became a symlink; publication refused'`, caught at `:1128` as a note refusal. Measured: `r3(a90531f) G fleet,   note became symlink | rc= 0 | … note_status= {'error': 'ValueError', 'reason': 'publication_guard', 'state': 'refused'} | compat_refreshed= True | real_note_rewritten= False` (emulated round-2 guard: `rc= 3 … scheduled destination differs from registered note`). Parent alias still publishes: `r3(a90531f) P default, parent-dir alias | rc= 0 | … compat_refreshed= True | real_note_rewritten= True`; regular note: `r3(a90531f) A fleet,   regular note | rc= 0 | … {'state': 'published'}`. Control `test/clio-store.py:639-651` asserts exit 0, `refused`, non-empty compat, byte-identical target, still a symlink; `symlink-progress-red.log` shows the pre-fix failure at exactly `line 647 … AssertionError: 3 != 0 : ValueError: scheduled destination differs from registered note`. H1 above is the side effect.
- [Pass] G2: `RecursionError` added to the per-origin tuple `:1005`; no new parser or guard. No fixture control was added; none requested (no fleet Mac can emit such a row via `encode()` `:35-37`).
- [Pass] G3: single `import re` at `:12` (`rg -n '^\s*import re' utils/CLIO/clio-store.py` → one hit); message `:938` reads `'fleet inventory must contain 1 to 16 unique origins'`; failed-reconcile status carries `'at': utc()` `:1121`.

**No regression in the round-2 passes (current line numbers)**

- [Pass] Q1: HEAD pinned once `:975-978`; only `rev-parse` and `cat-file -s` / `cat-file blob` `:982-985`; `timeout=min(5, remaining)` `:927`, 30 s budget `:971`, ≤16 origins `:969`, 64 MiB `:983`, `GIT_NO_LAZY_FETCH` `:922`; own recovery before serialization, refusing on own error `:800-803`; export own-origin only `:813`; unsent counted, not deleted `:877`.
- [Pass] Q2: own immutable conflict refused `:861-863`; labels restored only in `insert` with payload and indexed columns together `:243-249`; one grouped archive before updates `:865-866`; foreign strict `:870`; cumulative regression refused `:856-857`; generic self-import refused `:852-853`.
- [Pass] Q3: header prefix `:604-605`; pinned header/coverage `:587-589`; backup hash `:583-584`; whole file archived `:631` before the accepted-hash write `:791-793`; archive exclusive/verified/quota-bound `:895-909`; bounded wait `:612-617`, cleared on accepted note `:599-600`; compare-before-replace `:788-790`; race stated, not fenced (INSTALL.md 840).
- [Pass] Q4 except H1: drain errors isolated `:1113-1117`; compat precedes and is independent of the note attempt `:1123-1132`; schema `:129-156` and `VERSION = 1` `:23` untouched; 300 s bucket only with fleet `:748-749`.
- [Pass] Q5: `check-5.log` / `check-6.log` `Ran 16 tests … OK`; four-store controls `test/clio-store.py:561-565` parity, `:567-571` rejoin, `:573-578` dirty exclusion, `:581-597` 129 labels → one archive, `:598` no echo, `:600-607` own restore + unsent, `:654-677` bad/missing origins, `:679-685` regression. [Unverified — needs clone run]: I did not re-execute any suite; the harness gate does.
- [Pass] Q6: stdlib only `:3-20`; no new command, timer, schema or store in this increment; source-only limits stated (INSTALL.md 823–825, 840; receipts README "No live cross-device delivery/Obsidian Sync pilot is claimed").
- [Nit] `provenance.jsonl` line 7 records `head: 2a64aa84…` before and after; the receipts are tied to the candidate by the three source hashes, which match. No change requested.
- [Nit] Pre-existing, read not measured: the direct-CLI symlink guard `:760` compares `Path(markdown).expanduser().absolute()` to the resolved `view.path`, so `project --markdown` given through a parent-directory alias skips it and falls to `:763` as an explicit preview. The scheduled path no longer reaches this (it always passes the parent-resolved path). No change requested.
- Pre-existing code outside the fleet paths (`:1-580`, `:638-742`, `:1014-1021`): re-read; no other defect found.

VERDICT: FAIL
Basis: G1–G3 are implemented as described and hashes/receipts match, but the G1 fix introduces one measured regression (H1): a note registered through a symlinked destination, which worked before, now aborts every scheduled tick in both modes. Two-line fix or an explicit registration-time refusal resolves it; nothing else blocks. Source-only envelope unchanged. Handing off to Producer — go to the Producer window and say "take your turn".

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
