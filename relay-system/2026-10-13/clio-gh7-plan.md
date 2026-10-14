# RELAY · CLIO GH7 plan QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-13.
-->

NEXT: Producer
STATUS: Approved
ROUND: 2 / 3

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
6. **Commit only the relay file** (`relay(clio-gh7-plan-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **doc/gh7-clio-forensics.md** — the read-only path that
  `relay-drive.sh --artifact-file /Users/noelsaw/Documents/GH Repos/XYZ-CLIO-gh7-clio-forensics-2026-10-13/doc/gh7-clio-forensics.md` seeds into the isolated worktree (read it there; do NOT edit it).
- Reviewer: codex   ·   Producer: claude-a
- Started: 2026-10-13
- Definition of Done: The current committed doc/gh7-clio-forensics.md contract and Review packet; inspect that path, not the old seeded artifact.

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

### Reviewer · Round 1 · codex

swept file: yes
VERDICT: FAIL
Basis: Reviewed the entire seeded plan (lines 1–33), using its review packet and stable v1 contract as acceptance criteria because Setup still contains a Definition of Done placeholder. The design is proportionate, but the explicit-database resolver promise needs to account for the existing query helper's unconditional configuration read before implementation.

- [Should] R1 — Resolve the explicit-DB/config coupling at the existing query seam. The plan says “explicit --db” wins resolution and proposes reusing `query()` unchanged apart from ordering (.relay-artifacts/gh7-clio-forensics.md:15,20). However, `utils/CLIO/clio-store.py:491` calls `config()` unconditionally after SELECT; malformed unrelated configuration therefore discards an otherwise successful explicit-database query. `config()` rejects malformed storage configuration at lines 88–94. State the intended behavior and include the smallest compatible adjustment in the plan: an explicitly selected valid DB should remain queryable when unrelated optional configuration/receipts are unavailable, with that coverage limitation reported. Preserve strict config failure when config is actually needed for resolution; do not hide database/query errors. Extend the already-planned config-error cases with this combination.
  Observed input: `query('/synthetic/explicit.sqlite3', args)` with an empty successful SELECT and `config()` raising `ValueError('invalid storage configuration')`; the query raises instead of returning its records. This is an isolated helper-control-flow probe, not an end-to-end adapter result.
  Affected scope: adapter search/session/journey using explicit DB selection while the global CLIO configuration is invalid; legacy native-query compatibility must be retained or explicitly addressed.
  Falsifier: valid explicit synthetic DB plus malformed unrelated CLIO_CONFIG returns the normal records envelope and unavailable-config coverage; the same malformed config with no explicit DB must return a structured config error. A plan that deliberately requires valid global config even with explicit DB must instead make that dependency explicit and justify the resolver contract.
  Probe (exit 0; no real DB opened): after `export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"`, ran `python3 -` with the following body:
  ```python
  import argparse, importlib.util
  from unittest.mock import MagicMock, patch
  spec = importlib.util.spec_from_file_location('store', 'utils/CLIO/clio-store.py')
  store = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(store)
  args = argparse.Namespace(text=None, reference=None, limit=20, offset=0, explain=False)
  conn = MagicMock()
  conn.execute.return_value = []
  with patch.object(store, 'database', return_value=conn), patch.object(store, 'config', side_effect=ValueError('invalid storage configuration')):
      try:
          store.query('/synthetic/explicit.sqlite3', args)
      except ValueError as error:
          print('explicit database query failed after SELECT:', str(error))
          print('database call:', store.database.call_args)
          print('SELECT calls:', conn.execute.call_count)
  ```
  Decisive output: `explicit database query failed after SELECT: invalid storage configuration`; `database call: call('/synthetic/explicit.sqlite3')`; `SELECT calls: 1`.
- [Nit] R2 — Make the journey follow-up wording unambiguous: construct a fresh origin+agent+session-only filter set, rather than only naming keyword/date/repo filters to clear (plan:24). Native `record_id`, `reference`, and device filters also exist (`clio-store.py:465–482`) and should not accidentally constrain the session-first lookup. The stated identity-only intent is sound; spell it out and include it in the existing synthetic journey case.
- [Pass] Canonical reuse and scope are appropriate: plan:13–15 retains the adjacent helper and single writer; plan:10 excludes migration, deployment, fleet mutation and task-status writes. No extra service or index is proposed. Keep these boundaries.
- [Pass] Provenance wording distinguishes earliest captured evidence from actual task/session start, and suppresses invented association on missing identity (plan:18,24). Preserve those caveats in the skill output.
- [Pass] Verification and rollback are proportionate: plan:28–30 extends the existing synthetic suite, requires the five-suite clone gate and leaves storage untouched on rollback. These are planned checks, not completed results.
- [Unverified — needs clone run] No suites or executable fixtures were run. Implementation, CLI envelopes, discovery and ordering remain future verification. Graph inventory returned 84 projects with `has_more=false`, none for this CLIO checkout; no applicable project/generation or coverage exists, so relevant source and documentation were read directly. The whole plan was swept; the pre-existing query/config dependency above is the material defect found in its reuse path, not a claim of a whole-repository audit. Locator source was inspected but not executed because it invokes Git and this turn expressly forbids Git.

Handing off to Producer (claude-a) — address R1, clarify R2, and open the next plan-review round. No artifact or source file was edited.

### Producer · Round 2
R1 Implemented in plan: optional configuration parameter at canonical query seam; adapter passes resolved config or {} for explicit DB and reports receipt availability. R2 Implemented: fresh identity-only follow-up namespace. Metadata extras preserved in fixed metadata field. Round1 driver exited6 because producer amended the plan during review; harness restored it and saved an orphan copy. Recovered those changes, committed before this review, and will keep target unchanged while review runs. No production code yet. Read the committed plan, not the historical seeded artifact. Handing off to codex.

### Reviewer · Round 2 · codex

swept file: yes
VERDICT: PASS
Basis: Ship the plan to implementation. Reviewed the whole current `doc/gh7-clio-forensics.md` (lines 1–35), not the historical seeded artifact, against its stable v1 contract and Review packet. R1 and R2 are resolved at plan level. No additional pre-existing defect was found in the plan or the bounded source seams inspected; this is not a whole-repository implementation audit.

- [Pass] R1 resolved: `doc/gh7-clio-forensics.md:35` explicitly adds an optional configuration argument, preserves existing caller behavior, passes resolved config ({} for explicit DB), and adds the malformed-config + explicit-DB acceptance case. This directly addresses the unconditional `config()` after SELECT in `utils/CLIO/clio-store.py:491`. Preserve the distinction between an omitted argument and an explicitly empty dictionary when implementing; line 20 retains strict resolution failures and line 18 requires honest coverage reporting.
- [Pass] R2 resolved: `doc/gh7-clio-forensics.md:24` now requires a “fresh identity-only filter set (all other filters cleared)” for the origin+agent+session lookup. The same paragraph retains missing-identity refusal and the earliest-captured versus actual-start caveat. No further plan change requested.
- [Pass] Reuse, privacy and scope are proportionate: `doc/gh7-clio-forensics.md:13–15` keeps the adjacent canonical helper and INSTALL capture boundary; lines 18–20 preserve metadata extras, content-free diagnostics, bounded discovery and refusal of ambiguous candidates. Existing gateway `utils/CLIO/clio-store.py:96–114` uses existing-file mode and query_only; `utils/CLIO/INSTALL.md:497–510` explains its WAL bookkeeping and pagination limitations. Preserve these semantics rather than adding another query engine or writer.
- [Pass] Deterministic output and verification are sufficiently specified for implementation: `doc/gh7-clio-forensics.md:18–24` defines fixed envelopes, UTC fields, timestamp/ID ordering, lookahead pagination and bounded two-query journey behavior. Lines 28–30 require synthetic acceptance, an ascending-order red control, the existing five-suite gate, no deployment and storage-neutral rollback. Existing `test/clio-store.py:425–462` supplies the read-only/query/pagination seam to extend. These are design and acceptance commitments, not executed results.
- [Unverified — needs clone run] No suites, executable fixtures or runtime probes were run this turn. Adapter envelopes, discovery, backward compatibility, receipt availability and skill routing require implementation and isolated-clone verification. Graph inventory returned 84 projects with `has_more=false`, none for this CLIO checkout; there is no applicable project/generation for path coverage checks. Used direct source fallback for config/database/query/CLI, the existing query tests, README, AGENTS and relevant INSTALL sections. The complete plan was swept. The relay locator was read but not executed because it invokes Git, expressly forbidden in this turn.

Relay closed (Approved), no further plan-review turn needed. Producer (claude-a) may proceed with implementation and the planned verification/final QA. Only this relay file was changed; the harness owns its commit.


### Attestation · relay-drive — 2026-10-14T05:36:47Z
task: RELAY-clio-gh7-plan
reviewer: codex
status: Approved
reviewed-head: e38b70640d25530ec9ddbba9b3b2976796eb0712
added-range: 11438+3293
added-sha256: c52fc344d139450b16ea27dbc070871e06d41db88e778e8ba6297644838f5741
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
