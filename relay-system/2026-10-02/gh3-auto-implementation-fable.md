# RELAY · gh3-auto-implementation-fable
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
6. **Commit only the relay file** (`relay(gh3-auto-implementation-fable): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Approval token rule (overrides generic handoff instructions)
On approval execute exactly `TICK_REPO_ROOT=/Users/noelsaw/task-clones/clio-gh3-sqlite "/Users/noelsaw/Documents/GH Repos/XYZ-forge/bin/tick" done CLIO-GH3-AUTO-IMPLEMENTATION-FABLE --agent claude` before ending. Never release an Approved task to Producer. On findings only, release is valid.

## Setup
- Artifact under review: **gh3-auto-implementation-packet.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: producer
- Started: 2026-10-01

### Artifact — gh3-auto-implementation-packet.md
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

swept file: yes — `utils/CLIO/clio-store.py` read in full (1–1171, pre-existing code included), `test/clio-store.py` in full, the new INSTALL.md section (822–840), plan executable section + dispositions, recon delta, and every file under `TESTS-RESULTS/2026-10-02-gh3-auto-recovery/`. No suites run here; probes were synthetic, throwaway HOME, under `.relay-scratch/`. Candidate = cb66f5d; `shasum -a 256` of helper/test/INSTALL = `b7a61ebb…`/`492412d7…`/`114d8977…`, equal to `provenance.jsonl` line 7 `sources`.

**Findings**

- **[Blocker] F1 — scheduled-export lost its registered-path guard; it now overwrites an arbitrary other file, exit 0, no backup (default mode AND fleet mode).** The candidate deleted the pre-check `else: checked_view(conn, path, Path(args.markdown).expanduser().resolve())` (old helper, scheduled-export branch) whose first test is `clio-store.py:582` `if not view or Path(view['path']) != target: raise ValueError('run migrate-view for the existing destination before exporting')`. Now `clio-store.py:1099-1105` only checks that a view exists, and `project()` treats a non-matching path as an unregistered preview (`:763` `registered = … False` → `:792` `atomic(target, data)`).
  - Observed input: probe `.relay-scratch/probe1/p.py` (exit 0): config with `view.path=…/vault/registered.md`, no fleet; `python3 clio-store.py scheduled-export …/vault/unrelated-personal.md` where that file held `My unrelated personal note\n`. Output: `B rc= 0 stderr=` / `B unrelated note now: '# CLIO — recent 168 hours\n\nUTC cutoff: …'` / `B registered note unchanged: True` / `B backups dir: []`. Prior helper refused this call with the `:583` message. Reachable from the installed job: `prompt-log-to-md.sh:62` passes the plist's `$OUT` straight through, so a plist/arg that drifts from the registered view replaces that file every five minutes.
  - Affected scope: `scheduled-export MARKDOWN` when a view is registered and `MARKDOWN` resolves to anything other than `view.path` (both the `:1122` fleet call and the `:1137` default call).
  - Falsifier: in the existing same-path case, register view A, run `scheduled-export B` (B = existing file without the marker) → expect non-zero exit, B byte-identical, in both fleet and non-fleet config. If the old helper also overwrote B, this finding is wrong (it does not: removed line called `checked_view` first).
  - Fix: restore only the cheap path-equality refusal in the `:1099-1105` block (do not restore the content check there — that is what must stay non-fatal in fleet mode). Two lines; no new machinery.

- **[Should] F2 — one malformed committed snapshot aborts the whole scheduled-export / export-device instead of marking that origin `error`.** The per-origin catch at `:1004` is `(ValueError, KeyError, TypeError, OSError, sqlite3.Error, TimeoutError)` and the scheduled catch at `:1115` is `(ValueError, OSError, sqlite3.Error)`; `main` (`:1158`) and `import_jsonl` (`:358`) already know about `AttributeError`/`OverflowError`, these two do not. Result: no compatibility JSONL, no note, no status write, and later origins in the loop never import — contrary to plan "Valid origins can import when another origin is bad" and packet Q4.
  - Observed input: probe1 (exit 0): manifest `{"clio_snapshot":1,"owner":U,"generated_at":null,"rows":0,"sha256":sha256("")}` → `A1 generated_at=null -> AttributeError 'NoneType' object has no attribute 'replace'` (from `:827` → `:45`); snapshot row with `"timestamp":"0001-01-01T00:00:00+14:00"` → `A2 … -> OverflowError date value out of range` (`:835` → `:48`). Neither type is in `:1004` or `:1115`.
  - Affected scope: any inventory origin whose committed blob has a non-string `generated_at` or a row timestamp that overflows on UTC conversion; every Mac importing it.
  - Falsifier: commit that manifest for origin B in the four-store fixture, run fleet `scheduled-export` on A → expect exit 0, B `state: error`, C/D `accepted`, compat JSONL refreshed. If that already holds, decline.
  - Fix: make `:1004` and `:1115` catch the same tuple as `:1158` (or validate `generated_at` is `str` in `snapshot_records`). One line each.

- **[Should] F3 — the fleet branch of scheduled-export (`:1106-1134`) and the peer path have no executable control.** `rg -n "note_status|drain_errors|peer_generated|'missing'|scheduled-export" test/clio-store.py` → one hit, `794: … 'scheduled-export', str(note)` (non-fleet). The four-store case calls `store.reconcile_fleet`/`store.project` directly (`test/clio-store.py:550-552`) and each node writes its own private note (`:526`), so these plan-step-2/3 and F13 controls are absent: (a) fleet scheduled-export continuing with structured status on a note refusal; (b) a peer-generated note accepted without an archive (`:621-632` `peer_generated`); (c) one missing/bad origin while others import (`partial`/`missing`, only `assertFalse(partial)` at `:551,572` exists). My probe2 C1 shows (a) does work today (`rc= 0 note_status= {'error': 'ValueError', 'reason': 'header_changed', 'state': 'refused'} … compat exists= True`, note byte-intact) — so this is missing proof, not a known defect. Fix: three short assertions inside the two existing cases (no new suite): run the node's plist command in fleet config with an edited header; copy node 0's projected note bytes over node 1's note and assert zero new `conflict-*`; drop one origin's committed path and assert `partial` + others `accepted`. These also give F1/F2 their red/green controls.

- **[Nit] F4** — `:1132` `setdefault('last_result', fleet_result)` keeps the previous result when `reconcile_fleet` itself raises, so `query` status shows the older run with no error. Probe2 C2 (inventory without owner): stdout `fleet.partial= True` but persisted `last_result: at= <previous run> … error= None`. Assign the failed result (or stamp `error`/`at`) instead.
- **[Nit] F5** — `waiting_since` is only cleared inside the unrecognized-note branch (`:617-618`, `:633`); if the note returns to an accepted hash (`:600` false) a stale value survives and a later unknown-ID note skips its deferral (`:614`). Pop it on the accepted path. No observed production input; not requesting a behaviour change beyond the plan's own "Clear on no unknown IDs".
- **[Nit] F6** — `git_read` (`:921-926`) does not set `GIT_NO_LAZY_FETCH=1`; on a partial clone `cat-file` of an absent blob would contact the remote, against "no network call". [Unverified — Pulse checkouts not inspected]; one env key.
- **[Nit] F7** — `check-1.log` line 1 is `jq: parse error: Invalid literal at line 1, column 5` above a PASS; say in the receipts README whether that is an intended negative control. `check-6.log` shows `ResourceWarning: unclosed database` from `with store.database(...)` in the four-store case (`test/clio-store.py:554,580,591,595`) — wrap in `contextlib.closing`. Pre-existing duplicate `import re` at `:204`.

**Passes (by packet question)**

- [Pass] Q1 committed-only, bounded, no push: `:974` pins `HEAD^{commit}` once; `:979-984` reads only `head + ':devices/' + owner + '/clio.jsonl'` via `cat-file -s`/`cat-file blob`; `:926` `timeout=min(5, remaining)`, `:970` 30 s budget, `:968` ≤16 origins; only git verbs in the file are `rev-parse` and `cat-file` (`:939,974,981,984`). Path/owner match `:825-826`; per-origin partial progress `:996-1006`. Own recovery precedes serialization and refuses on own error `:799-802`; no echo `:812` (`WHERE origin_id=?`); unsent rows retained and counted `:876`.
- [Pass] Q2: own immutable conflict refused `:860-862`; labels restored only in the writer seam with payload + indexed columns together `:249-250`; one grouped archive per origin transaction `:864-865`, written before the updates `:866-869`; foreign stays strict (`replay=own, restore_labels=own` `:869`) and cumulative regression refused `:855-856`; generic self-import still refused `:851-852`, `:880`.
- [Pass] Q3: exact header prefix required `:603-604`, pinned header/coverage `:588-590`, backup hash `:584-585`; complete file archived before any accepted-hash write `:630` vs `:790-792`; archive exclusive/verified/deduplicated `:893-908`, quotas `:899-901`; unknown-ID deferral persisted without reset and bounded `:612-616`; compare-before-replace `:787-789`; the post-comparison race is stated, not fenced (INSTALL.md 840).
- [Pass] Q4 (except F1): compatibility output precedes and is independent of the note attempt `:1118-1127`; drain errors do not stop reconcile `:1108-1112`; non-fleet branch unchanged apart from F1 `:1136-1138`; no schema change (`:129-156` untouched, `VERSION = 1` `:23`); 300 s cutoff bucket only when fleet is configured `:747-748`.
- [Pass] Q5 receipts: `provenance.jsonl` lines 1–6 exit 0 for the four shell suites and both Python runtimes; `check-5.log`/`check-6.log` `Ran 16 tests … OK`; four-store parity `test/clio-store.py:556-558`, rejoin `:562-566`, dirty-file exclusion `:568-573`, 129 labels → one archive `:576-592`, strict peer re-import `:593`, own restore + unsent `:599-602`, regression `:610-612`. Gaps are F3. [Unverified — needs clone run]: I did not re-execute any suite.
- [Pass] Q6: stdlib only (`:3-20`), single helper, no new store/timer/pusher; rollout limits stated truthfully (INSTALL.md 823–825, 840; receipts README last paragraph).

VERDICT: FAIL
Basis: F1 is an observed regression of an existing write guard — the scheduled exporter can now replace an unrelated note with exit 0 and no backup. F2 and F3 are small and share the same test additions. Everything else measured holds; no redesign requested. Handing off to Producer — go to the Producer window and say "take your turn" (disposition F1–F7, re-run suites in the disposable clone, refresh receipts).

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
