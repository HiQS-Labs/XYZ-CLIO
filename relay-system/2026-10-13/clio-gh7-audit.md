# RELAY · CLIO GH7 read-only audit documentation
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-13.
-->

NEXT: codex-supervisor
STATUS: Approved
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
6. **Commit only the relay file** (`relay(clio-gh7-read-only-audit-documentation): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: `utils/CLIO/SKILL.md`, `utils/CLIO/clio-query.py`, `utils/CLIO/clio-store.py`, `utils/CLIO/INSTALL.md`, `test/clio-store.py`, `README.md`, `TESTS-RESULTS/2026-10-13-clio-readonly/`, `doc/gh7-clio-forensics.md`
- Reviewer: claude   ·   Producer: codex-supervisor
- Started: 2026-10-13
- Definition of Done: User explicitly selected Claude Code CLI headless. Review the whole current PR against origin/main and doc/gh7-clio-forensics.md, including the original skill and the audit follow-up. Prior Codex approvals and five-suite gate are evidence, not a substitute for this independent whole-PR review. No private history/configuration, false application-fix claim, live runtime or database changes.

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

### Producer · Round 1 · codex-supervisor

Operational envelope: local CLIO forensic CLI, documentation-only follow-up to PR #8. User authorized transferring the separate Rebalance audit into this PR and deleting its unrelated stash afterward. Existing seven audit receipts were transferred; backup location removed; SOP guidance adapted into the existing INSTALL.md. No runtime edits or live database operations. Commensurate complexity: no new tests, gates, helpers or machinery. Prior implementation passed independent plan/final Codex relays and the five-suite gate; do not rerun suites in the reviewer worktree.

Read the changed documentation/evidence in full and the canonical database() boundary at utils/CLIO/clio-store.py:97. Questions:
1. Does mode=rw plus query_only guidance preserve WAL consistency, missing-file refusal, and the distinction between SQL read-only behavior and filesystem bookkeeping? Are immutable and backup/lock instructions accurate?
2. Are raw before/after failures and safe-reader success supported by the receipts, with historical scope, active capture and completeness limits explicit? No new application fix is claimed.
3. Are the adapted downstream references clearly Rebalance-owned rather than a new CLIO subsystem, and do links resolve from their owning docs?
4. Did transfer publish any private prompt content, credential or machine-specific absolute/backup path, or alter capture heredocs/runtime files?

Report cited findings, verdict and swept-file declaration in this thread only. Do not edit other files, run tests, access installed hooks or open live history. Approve if no substantive defects; on approval use the exact env-pinned tick done command from the runner prompt rather than release.

### Producer · Reviewer availability correction

The initial runner rejected a wildcard artifact path before starting a reviewer; the setup now names the directory directly. Codex then failed before review with HTTP 429 Too Many Requests (CLI exit1, driver exit5, no verdict). Its claim was released and token inspected open. The user named Agy in the prior QA request, so the same scoped documentation packet is now handed to Agy. No approval or implementation change is inferred from either failed invocation.

### Producer · Agy availability and publication disposition

Agy CLI exit3 reported RESOURCE_EXHAUSTED / HTTP429 individual quota. Driver exit5; no reviewer verdict or approval. Its claim was released. Both Codex and Agy documentation-review attempts were unavailable; do not treat these as successful reviews. No retry loop or alternative paid reviewer is introduced. Publish the requested evidence in the existing PR as draft, retain prior implementation QA/gate as historical evidence, and resume this documentation relay when a reviewer is available.

Producer checks: all seven transferred evidence files accounted for; five remain byte-identical to the original audit, summary ownership/scope clarified and backup location omitted. JSON/JSONL parses, audit link resolves, and removing the new INSTALL.md section restores the earlier file byte-for-byte. No production code/capture heredoc changes. These checks are not independent approval.

### Producer · User-directed Claude Code CLI whole-PR QA

The user now explicitly requests Claude Code CLI headless. This latest packet expands review to the entire PR #8, with particular attention to the transferred audit. Use the existing native CLI reviewer route, inherited model defaults and normal containment; no nested model calls. No successful review round has occurred in this follow-up yet. Preserve the recorded Codex/Agy quota failures rather than replacing them with approval.

Operational envelope: stdlib local developer forensic CLI; small adapter over the existing canonical CLIO query/config/database gateway. Read the listed files in full, inspect the diff against origin/main, and use the plan's v1 contract and requirements as acceptance criteria. Keep complexity commensurate: no new search index, writer, services, enterprise threat model, test suite or gate. Reviewer writes only this thread. Do not run tests, install/activate capture, open live history, read external secrets or modify source files.

Questions:
1. Does the adapter reuse the canonical helper and preserve existing query defaults/configuration behavior? Are no additional writers or live DB mutations introduced?
2. Are success, empty and error shapes stable with UTC time/date, session/device/agent/explicit IDE, unknown values and preserved metadata? Check the concrete previously fixed malformed-receipt and oversized-offset cases.
3. Does journey find the oldest captured match with stable ties, then the identity-only origin+agent+session earliest record? Are session ambiguity and the distinction from a proven true task start clear?
4. Are explicit/config/default/bounded-discovery precedence, ambiguity handling and missing-file rejection supported by the existing acceptance cases?
5. Is the audit guidance accurate about rw+query_only, absent WAL/SHM, immutable live reads, backups, locks and separate Rebalance projections? Are observations historical and bounded, with receipts supporting the before/after output and no private payload/configuration/backup path published?
6. Does the prior deterministic evidence support the unchanged runtime, without claiming that failed service reviews approved the follow-up? Flag substantive issues with exact source citations and a concrete falsifier. Report the whole-file sweep, verdict and basis; on approval complete the tick token using the exact native command in your runner prompt.

### Producer · Claude budget exhaustion

Native Claude subscription preflight succeeded and claude -p ran nine turns, then returned error_max_budget_usd / Reached maximum budget ($0.5), CLI exit1 and driver exit5. No verdict or approval; no artifact change. Token inspected open after automatic claim release. The default allowance was insufficient for the user-directed whole-PR sweep. Retry the same independent Claude review with a bounded CLAUDE_MAX_BUDGET=1.50 and CLAUDE_MAX_TURNS=20; keep the model default, isolated worktree, relay-only writes and 900-second ceiling. No user-specified budget or round cap is overridden.

### Reviewer · Round 1 · claude

swept file: yes — read all eight artifact files in full (SKILL.md, clio-query.py, clio-store.py, INSTALL.md, test/clio-store.py, doc/gh7-clio-forensics.md, TESTS-RESULTS/2026-10-13-clio-readonly/SUMMARY.md, README.md).

**Q1 — Adapter reuse and no new writers**

- [Pass] `clio-query.py` imports `clio-store.py` via `importlib` and calls `store.config()`, `store.database()`, `store.query()` directly. No independent SQLite connection; `writable=True` never passed; no `INSERT`/`UPDATE`/`DELETE`. The optional `configuration` parameter added to `store.query()` passes already-resolved config so explicit-DB mode bypasses a broken unrelated config. Existing callers unaffected (default `configuration=None` re-reads config as before). Citation: `clio-query.py:127-145`, `clio-store.py:463`.

**Q2 — Stable result shape, UTC normalization, IDE/unknown/metadata**

- [Pass] `record()` at `clio-query.py:91-101` derives `date`/`time` as UTC slices of the normalized timestamp, hardcodes `timezone='UTC'`, populates `ide` only from an explicit `str` in extras, maps `device` from `machine`, and preserves `extras` unchanged as `metadata`. `AttributeError`/`OverflowError` added to the content-free adapter error boundary (`clio-query.py:173`). The two previously-observed malformed-receipt and oversized-offset failures are covered by `focused-errors-fixed.log` per doc/gh7-clio-forensics.md. Test `test_forensic_journey_and_contract` at `test/clio-store.py:901` validates UTC normalization of a +02:00 timestamp, explicit-string IDE population, null IDE for a non-IDE row, and full fixed key set.

**Q3 — Journey oldest match, then identity-only session follow-up**

- [Pass] `clio-query.py:152-163`: journey requires `--text`, oldest order, offset 0. The session follow-up constructs a fresh `identity` dict with all FILTERS set to `None`, then overwrites only `origin`, `agent`, `session`. Probe confirmed: 8 filters cleared (`device`, `record_id`, `reference`, `repo`, `repo_slug`, `since`, `text`, `until`); 3 identity keys set. This ensures date/text/repo filters do not carry over, so the session's earliest captured prompt can precede the keyword or the `--since` window. `basis='missing_session_identity'` is set when any of `origin_id`/`agent`/`session_id` is absent (`clio-query.py:157`). Tested at `test/clio-store.py:907-928` (reused session ID across origins/agents, `--since` filter, correct first-record recall) and `test/clio-store.py:944-945` (missing identity basis).

**Q4 — Resolver precedence, ambiguity, missing-file rejection**

- [Pass] `resolve()` at `clio-query.py:42-88`: explicit → config → default (`~/.claude/prompt-log.sqlite3`) → bounded pulse discovery (≤100 entries per dir, only `.db/.sqlite/.sqlite3`, validated through `store.database()`). Multiple valid candidates → `ambiguous_database`. Missing/invalid path → `invalid_database` (no DB created, confirmed by `test/clio-store.py:955`). Broken explicit path never silently falls through to config. `test_forensic_database_resolution` at `test/clio-store.py:953-983` covers all five resolution paths plus broken config with explicit-DB bypass, ambiguous pulse, and missing-file non-creation.

**Q5 — Audit guidance accuracy: rw+query_only, WAL/SHM, immutable, backups, locks, Rebalance scope**

- [Pass] INSTALL.md Cold-WAL audit section (`INSTALL.md:517-541`) correctly documents `mode=rw` + `query_only=ON` as the safe read pattern; warns `immutable=1` is only for a verified stable backup/snapshot, not live history; warns against copying only the main file while WAL is active; scopes `query_only` as a connection setting, not an OS access-control boundary; directs reporting actual sandbox constraints before considering WAL changes. Audit link at `INSTALL.md:543` resolves correctly (`../../TESTS-RESULTS/2026-10-13-clio-readonly/SUMMARY.md` from `utils/CLIO/` — link-check probe: LINK OK). SUMMARY.md Consumer map labels all Rebalance entries as "Does not open canonical SQLite" or "Separate projection database" — no new CLIO subsystem claimed. Private backup path omitted: "retained in a private backup directory outside Git; its machine-specific location is omitted here." Before/after failure receipts (before.json mode=ro success with WAL; checks.jsonl backup rw+query_only success; after mode=ro fails without WAL) are present in TESTS-RESULTS/2026-10-13-clio-readonly/. Observations correctly scoped to historical audit revisions (`d17e521`, `e46150a`), not a fresh qualification of later revisions.

**Q6 — Prior evidence supports unchanged runtime; no false approval claim**

- [Pass] `doc/gh7-clio-forensics.md:9` marks follow-up QA open with "draft while documentation-review services are quota-limited; prior implementation approval retained, not deployed." Relay log explicitly records each failed service invocation as "no verdict or approval." SUMMARY.md: "The audit changed no code or installed runtime; this PR publishes its evidence and documentation only." No false approval is attributed to Codex or Agy quota failures.

**Pre-existing defects in touched files**

No pre-existing defects found. Key checks: (a) `drain()` reads back versioned rows (`clio_version=VERSION` set by `capture()`'s `normalize()`) so `normalize(json.loads(...))` without `owner` correctly uses the versioned path — no missing-origin risk. (b) `legacy_coverage()` uppercase translation is ASCII-only (`str.maketrans` covers only a–z), matching legacy renderer behavior for non-ASCII repo names (e.g., café → CAFé, confirmed by test fixture). (c) `checked_view()` future-timestamp expiry logic is correct: `0 <= (now - waiting).total_seconds()` is false for future `waiting_since`, causing immediate expiry. (d) `record()` `prompt or None` on an already-validated non-empty prompt field is harmless.

**VERDICT: PASS**

**Basis:** All six review questions pass on cited evidence. The adapter is a pure read-only forensic wrapper over the canonical helper with no new writers. The forensic contract, journey identity follow-up, resolver precedence, and audit guidance are all correctly implemented and tested with synthetic data. No private payload, credential, machine-specific path, or application fix is claimed. Prior quota-limited service failures are correctly not treated as approval. No pre-existing defects found in scope.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
