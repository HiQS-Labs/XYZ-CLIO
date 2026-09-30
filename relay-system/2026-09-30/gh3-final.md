# RELAY · CLIO GH3 final implementation QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-09-30.
-->

NEXT: author
STATUS: Open
ROUND: 1 / 3

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
6. **Commit only the relay file** (`relay(clio-gh3-final-implementation-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-final-review-packet.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: author
- Started: 2026-09-30

### Artifact — gh3-final-review-packet.md
```
# CLIO GH3 final implementation review

Review all changes from a0674039407e53baee18ca30d9c33413732c232b through committed HEAD, especially utils/CLIO/clio-store.py, INSTALL.md embedded writer and migration/rollback instructions, prompt-log-to-md.sh, clio-agy-tail.sh, test/clio-store.py, README/FRONTDOOR. Read doc/gh3-plan.md and doc/recon-gh3.md plus TESTS-RESULTS/2026-09-30-gh3/implementation-evidence.md and actual logs/benchmark.

Original request: SQLite complete prompt history, rolling seven-day MD, exact device/agent/work lookup, light XYZ task/ledger references, central Git Pulse Sync and semantic lookup. Phase1 provides local authority and export contract; Rebalance consumer + publisher + existing semantic integration are explicitly tracked Phase2 blocked until this prerequisite merges and #282 ownership work lands. Installed pilot is Phase3 and not authorized by ready-PR scope. Do not call the entire feature shipped.

Grade against the approved plan and a local developer history utility, stdlib only. No enterprise threat model, new service, scheduler, Git pusher, ledger writer or vector DB. One canonical insert boundary extends existing shared writer; four agent routes and legacy mode retained. Commensurate complexity target ~700-line store, focused stdlib unittest; no generic framework. Rating78/65/50/35 preserved, neutral appeal, one reported incident/unknown trend.

Questions: Are migration/accounting/unknown metadata/identity and ownership safe? Do capture receipts and retries preserve accepted prompts? Is activation race/budget behavior truthful? Are query/projection/compatibility/snapshot contracts correct, output paths protective and rollback instructions lossless? Do nonempty fixtures and failure controls substantiate claims? Any duplicate subsystem or missed in-scope regression? Sweep touched files, cite concrete failing input for behavior changes. Optional probes use synthetic temporary HOME only; never touch installed capture or private source history.

Focused tests passed; per start-task the final full qualifying four shell suites + Python suite will run exactly once AFTER final Approved on unchanged implementation. Approval is code/plan evidence review, not a claim the final gate already ran. Review writes only this relay thread; no source changes, no push. Three rounds maximum. Use PASS/FAIL/PARKED and literal swept file line per protocol.
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

### Reviewer · Round 1

swept file: yes
VERDICT: FAIL
Basis: Phase 1 is proportionate and most storage contracts match the plan, but two measured gaps remain in protected output paths and stable tailer replay. This is code/plan review, not final-gate or deployment approval.

Scope/evidence: read whole `utils/CLIO/clio-store.py`, `utils/CLIO/INSTALL.md`, `utils/CLIO/prompt-log-to-md.sh`, both tailers, `test/clio-store.py`, capture/exporter/Agy shell suites, README/FRONTDOOR, plan/recon, focused logs and benchmark source/results. MCP `list_projects` pages 0 and 50 exhausted all 77 projects: this CLIO checkout has no indexed project/generation, so direct source fallback was used; no graph completeness claim. No git, test suite, installer or executable fixture was run. Existing FD-05/FD-06 remain disclosed in FRONTDOOR; no additional pre-existing defect found in the swept production files beyond the retry interaction below. The embedded DoD placeholder was graded using the concrete acceptance criteria in the packet and `doc/gh3-plan.md`.

- [Should] R1 — Apply historical-note protection to every replacing export destination. `safe_output` at `utils/CLIO/clio-store.py:459` permits `~/.claude/prompt-log.md`; the default-path/marker protection at :479–482 only guards the Markdown argument. `project --markdown recent.md --jsonl ~/.claude/prompt-log.md` passes :507 and replaces the historical note at :514; `export-device ~/.claude/prompt-log.md` similarly reaches :530. A custom shared note containing `<!-- CLIO:ENTRIES -->` is equally unprotected through those two routes. This can erase foreign-device-only history that the plan explicitly preserves. Move the existing default-path and marker checks into the shared replacing-output guard, preserving regeneration of legitimate recent/compatibility/snapshot files. Verify the refusal in the existing isolated storage suite.
  Observed input: synthetic HOME target `.claude/prompt-log.md`, with an empty source/import catalog; the pure `safe_output` probe below returned the target instead of refusing it. The concrete callers and replacement sites are cited above; no historical file was actually overwritten during review.
  Affected scope: destinations of `project` (both outputs) and `export-device` that are the legacy default Markdown path or an existing CLIO historical-marker note.
  Falsifier: a historical note containing one foreign-only entry supplied as `--jsonl` or snapshot output must remain byte-identical with nonzero refusal; ordinary separate recent MD, compat JSONL and device snapshot outputs must still regenerate successfully. A guard already rejecting these destinations would falsify this finding.

- [Should] R2 — Make tailer replay independent of current checkout metadata. `normalize` hashes branch/machine/repo along with source content (`utils/CLIO/clio-store.py:160`, :201), while Codex resolves current repo/branch on each poll (`utils/CLIO/clio-codex-tail.sh:252`) and only advances the whole chunk after every row succeeds (:267–281). If the first row commits and a later row fails, or capture commits before a tailer crash, a branch change before retry produces another accepted identity for that same source row. The probe below measured different IDs with only branch changed. This contradicts the plan's “afterDB beforeprojection/cursor → stable-ID replay.” Preserve a deterministic source-event identity or freeze the delivered row context through retries at the existing tailer/writer seam; retain distinct same-second prompts and immutable stored payloads, without a new service or general retry framework. Extend the existing storage acceptance case in a disposable clone.
  Observed input: `{timestamp:"2026-09-29T12:00:00Z",session_id:"same-source-session",prompt:"same source prompt",agent:"codex",repo:"fixture",checkout:"/fixture/repo",machine:"fixture-mac",branch:"main"}`, retried from the same source event with `branch:"feature"`; hashes below differ. Chunk retry and live branch derivation are explicit source paths, not an assumption that all metadata is unstable.
  Affected scope: replay of already accepted Codex source rows after a deferred chunk/crash, when current checkout branch changes; human machine renaming creates the analogous exposure but is not required to reproduce this finding.
  Falsifier: accept source row A, defer later row B or stop before cursor publication, change checkout branch, replay unchanged A/B: A must remain one stored event with its original provenance, B must eventually appear once. Two genuinely distinct source prompts in the same second must remain separate. Frozen-context/source-identity handling that already achieves this would falsify the finding.

Measured evidence for R1/R2 (pure functions; exit 0; no DB/source mutations). Exact command:

```bash
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"
mkdir -p "$TMPDIR"
python3 - <<'PYPROBE'
import importlib.util, os
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('s','utils/CLIO/clio-store.py'); s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
class Empty:
 def execute(self,sql): return []
with patch.dict(os.environ,HOME=os.environ['TMPDIR']):
 target=Path.home()/'.claude/prompt-log.md'
 print('legacy Markdown accepted by safe_output:',s.safe_output(Empty(),Path.home()/'history.sqlite3',target)==target.resolve())
row={'timestamp':'2026-09-29T12:00:00Z','session_id':'same-source-session','prompt':'same source prompt','agent':'codex','repo':'fixture','checkout':'/fixture/repo','machine':'fixture-mac','branch':'main'}
a=s.normalize(row,'fixture-owner','captured'); b=s.normalize(dict(row,branch='feature'),'fixture-owner','captured')
print('same source event after branch change gets different IDs:',a['record_id']!=b['record_id'])
print('first ID:',a['record_id']);print('retry ID:',b['record_id'])
PYPROBE
```

Decisive output:
```
legacy Markdown accepted by safe_output: True
same source event after branch change gets different IDs: True
first ID: clio1-0160ac821bbfd9060bd8587d534287a0f16203b08458f445332228a56c1e1077
retry ID: clio1-8dd9304d3e974fbaa323ebfda02c016554ec2a51fc25dc748243a4714c5efdf2
```

- [Pass] Migration accounting uses one transaction for events, quarantine and cursor (:291–338), checks source inode/prefix (:294–307) and verifies expected payloads against stored events (:366–380). Unknown extras survive normalization (:175–183); foreign snapshot rows retain ownership and export uses `origin_id == owner` (:526, :547–550). These are source-level findings, not freshly executed acceptance results.
- [Pass] Rolling projection implements inclusive UTC 168h membership and descending timestamp/ID (:483–484), with full chronological compatibility output (:513–514). Read-only query uses URI `mode=ro` and `query_only` (:86–98), bound parameters and deterministic order (:426–450). No separate ledger/vector/publisher subsystem is introduced; README explicitly says “Fleet publishing and Rebalance's provenance upgrade are separate dependent work.” Keep that delivery boundary.
- [Unverified — needs clone run] Final qualifying four shell suites plus Python suite have deliberately not run this turn. `sqlite-focused.log` records 11 passing cases but includes connection ResourceWarnings; `sqlite-benchmark.json` reports 10,000 rows, equal nonempty results and a disclosed warm-local measurement. These are retained producer evidence, not independent execution at final approved HEAD. Run the authorized qualifying gate after final Approved on unchanged implementation, and record failures/skips honestly.

Handing off to author — disposition R1/R2, make the bounded fixes and return for round 2; go to the author window and say 'take your turn'.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
