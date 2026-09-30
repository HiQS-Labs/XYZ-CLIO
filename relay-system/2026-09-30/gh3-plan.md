# RELAY · CLIO GH3 SQLite plan QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-09-29.
-->

NEXT: Producer
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
6. **Commit only the relay file** (`relay(clio-gh3-sqlite-plan-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-review-packet.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: author
- Started: 2026-09-29

### Artifact — gh3-review-packet.md
```
# CLIO GH3 pre-implementation plan review

Review doc/gh3-plan.md and doc/recon-gh3.md against the original issue requirements below and actual repository source. Only edit the relay thread. Local developer history tool, four agent capture paths; stdlib/minimal machinery. No enterprise threat model or unrequested supervisor. No production changes yet. Grade phase1 as local implementation through readyPR; phase2 integration has hard merge dependencies; phase3 installedpilot remains separately authorized.

Questions:
1. Does the proposed single insert/capture boundary preserve existing tailer delivery/filter contracts and account for concurrent legacy migration, missing metadata and same-second collisions?
2. Are snapshot identities, local-vs-imported origin, spool receipts and failure/rollback paths specific enough to implement without competing authorities? Flag concrete loss windows.
3. Can the plan safely keep Daily/JSONL and shared historical Markdown working while producing a deterministic rolling view? Is any acceptance criterion omitted?
4. Are readonly lookup/explicit task references and existing Rebalance semantic reuse the smallest useful route to which-device/agent lookup? Are fleet dependencies honest, rather than falsely claiming active centralized sync?
5. Are rating78/65/50/35 and recurrence uncertainty grounded, appealing score neutral, scopes/verification commensurate and stopconditions bounded?
6. Is plan implementable with listed source paths and useful tests, or does it invent redundant machinery? Keep necessary data-loss protections.

Use file:line findings and falsifiers; distinguish observed source defect from plan gap. STATUS Approved only if ready to implement. Read whole relevant files; no test execution in review worktree. Producer supplies isolated test evidence.

## Original issue acceptance (sanitized public text)

# SQLite as CLIO's canonical store; rolling seven-day Markdown projection

## Requested outcome

The operator wants **one full-history SQLite store agents can query efficiently**, plus a **rolling seven-day Markdown file for human browsing and lightweight agent context**. Seven days limits the Markdown projection, **not retention in SQLite**. This issue authorizes planning for the change; no implementation or installed-writer migration has occurred.

| Current state | Next step |
|---|---|
| JSONL capture and optional Markdown export; history is cumbersome to search and device/agent provenance can be hard to locate | Verify installed writer/readers and migration contracts, then implement and test SQLite capture plus a bounded Markdown projection |

## Verified starting point and motivation

The canonical standalone repository is `HiQS-Labs/XYZ-CLIO`, default branch `main`. Its current README identifies `utils/CLIO/INSTALL.md` as the source of truth for the embedded capture writer and Claude/ZCode shims; Codex and Agy use the bundled tailers. The current store is `~/.claude/prompt-log.jsonl`, with `session_id:timestamp` dedup identity. The exporter is `utils/CLIO/prompt-log-to-md.sh`; INSTALL documents its cursor and append-only delivery manifest. These are current documented contracts, not a complete trace of installed versions.

Recent artifact recovery for [Rebalance #232](https://github.com/HiQS-Labs/rebalanceOS/issues/232) required searching a large Markdown export to identify the original device/agent/time. SQLite should make time/repository/session/device/agent lookups direct, while keeping a readable recent-work file. Existing Rebalance SQLite ingestion is a downstream projection, not automatically CLIO's canonical writer. Trace and reuse compatible contracts rather than introducing two competing authorities.

## Scope and acceptance contract

- **Full-history database:** one configurable local SQLite path, private permissions, schema version and documented backup/restore. Preserve prompt text, UTC timestamp, repository, branch, device, agent and session ID, plus stable identity/provenance needed for idempotent import and capture. Unknown agent/device values stay unknown; do not manufacture historical metadata from a display fallback. Validate collision behavior before extending legacy IDs for multi-device import.
- **Shared capture path:** Claude Code, ZCode, Codex and Agy continue through the existing shared writer boundary. Reuse the existing Python/stdlib SQLite capability where appropriate; no new service, framework, collector or model call. Concurrent submissions must not silently disappear or stall the interactive agent indefinitely. Choose and test transaction, locking, bounded busy retry and durable recovery behavior; report capture failures explicitly.
- **Rolling Markdown:** configurable existing output location, newest first, latest **168 hours** as of one captured UTC cutoff. Include timestamp, repo, branch, device, agent, session/record identity and prompt text. Human display may use labeled local time. Publish atomically; failure preserves the prior valid file. The window advances even when no new prompts arrive, so old entries expire from Markdown on the existing exporter schedule. Empty windows render an explicit empty-state header. Repeat export of the same snapshot/cutoff is byte-identical.
- **Bounded output only:** old prompts remain queryable in SQLite after they disappear from Markdown. A seven-day window does not guarantee a small byte count; report row/byte totals. Any additional truncation must be explicit and link back to record IDs; do not silently omit large prompts.
- **Agent access:** provide documented, read-only, parameterized queries through the smallest existing reader/CLI seam. Support time range, repo, device, agent, session, stable IDs and text search with limit/pagination. Index common filters; evaluate FTS5 only if available and justified by representative measurements. Return provenance and timestamp with results. Do not make agents load the full DB or Markdown into context, and do not open source DBs through a helper that initializes/migrates them on read.
- **Compatibility:** trace Rebalance ingestion/replay, Daily, installed skills, tailer cursors, exporter receipts and any direct JSONL consumers before cutover. Define a temporary deterministic JSONL compatibility export if required; avoid independent writers creating divergent histories. Do not simply repurpose the old permanent-delivery manifest to decide membership in a rolling view—aged-out rows must be able to reappear when a requested window changes.
- **Per-device durability:** this does not authorize live SQLite/WAL files to be concurrently edited through cloud/file sync. Define per-device capture and stable-id snapshot/import behavior if cross-device history is needed, reusing existing transport where possible. Preserve device identity and disclose missing fleet coverage; no new synchronization engine by default.

## Ordered delivery plan

1. **Recon and freeze baseline.** Read current repo/skill governance, inspect installed versions and the actual writer → log → tailer cursor → exporter → downstream readers. Record every read/write seam, failure path and compatibility consumer. Capture nonempty representative fixtures and existing suite results. Verify prior art/open PRs in CLIO and relevant Rebalance/skills sources. Do not assume a local installed copy matches canonical main.
2. **Design and prove additive migration.** Preserve original JSONL and existing Markdown before any cutover. Build an idempotent importer with resumable/checkpointed progress, source hash/record accounting, duplicate handling and quarantined malformed records. Every source record must be accounted for; invalid rows must not vanish. Capture concurrent arrivals during backfill through one canonical ingestion/transaction route, then verify convergence before switching readers/writers. No silent drop from concurrent capture or legacy/mixed-version agents.
3. **Implement the smallest writer/read/export change.** Reuse current capture registrations and exporter schedule. Add SQLite storage/read queries and atomically generated rolling Markdown without new daemon/UI/scheduler. Keep existing consumers working through the documented transition. Update installer, verification/uninstall instructions and deployment-source copies through their established source-of-truth process rather than editing installed copies ad hoc.
4. **Run correctness and performance verification.** Exercise all four agent capture routes, duplicate submissions, equal timestamps across devices, unknown metadata, Unicode/multiline/large prompts, malformed/truncated JSONL, interrupted/resumed import, concurrent capture/read/export, lock contention, full disk/write failure, empty DB/window, exact cutoff boundaries, future timestamps, no-new-prompt expiration, output failure and rollback. Witness negative controls: remove a source record, corrupt an identity and interrupt export; the relevant checks must fail. Preserve existing tests and add only meaningful coverage required for this change. Measure representative historical queries and exports on the same nonempty corpus before/after, reporting corpus size, returned IDs, timing and query plan/index use; freeze an acceptable capture-latency budget before implementation. No “faster” claim from an empty or incomparable dataset.
5. **Pilot, reconcile and hand off.** Validate on one device with explicit deployed-version receipts, canonical DB/projection consistency and readable output. Keep source backups and compatibility until old writers/readers/queued work are accounted for and the rollback window is satisfied. Publish sanitized results under `TESTS-RESULTS/`, update this issue with measurements and remaining gaps, and document commands for “what did I ask about X, when, on which device/agent?” Roll out to other devices deliberately after the pilot, preserving separate device identities.

## Migration and rollback

**Reversibility: Costly at installed-writer cutover; Easy during isolated fixtures.** Blast radius: captured prompt history, agent hooks/tailers, Markdown browser view and downstream history readers. The shield is an additive import plus single-device pilot with old sources retained. Tripwires are missing/duplicate/colliding records, stalled/lost capture, unreadable databases or projections that disagree with the frozen query: halt rollout and return to the preserved capture path, reconciling post-cutover arrivals before rollback. Never overwrite or delete source history to make counts match.

Use expand → backfill with ongoing capture → verify convergence → switch reads/writes → maintain mixed-version compatibility → retire old paths only after all relevant clients/queued work and rollback needs are satisfied. A brief explicitly bounded capture queue/drain may be simpler than dual writers; choose based on measured behavior and prove no data loss. Use debug-mantra for failures (reproduce, trace, falsify, cross-reference), with bounded retries and retained diagnostics rather than silent recovery loops.

## Done means

- [ ] All four agents capture successfully into the canonical SQLite store, with witnessed concurrency/failure controls and bounded latency.
- [ ] Every legacy record is imported or explicitly accounted for, repeated migration adds no duplicates, and originals remain recoverable.
- [ ] The Markdown file contains exactly the chosen latest-seven-day snapshot, expires old entries without new capture, and publishes atomically; older history remains in SQLite.
- [ ] Agents can retrieve specific evidence quickly through indexed read-only queries, with documented examples and measured same-corpus results.
- [ ] Downstream consumers and installed copies are reconciled, a one-device pilot and rollback are verified, and private prompts/DB files are not published to GitHub.  [Unverified — no citation]

Related: [Rebalance #232](https://github.com/HiQS-Labs/rebalanceOS/issues/232) storyline trial and [#210](https://github.com/HiQS-Labs/rebalanceOS/issues/210) evidence-bound synthesis. This storage work is separate and must not silently block or replace the frozen Luna trial.
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

### Reviewer · Round 1 · codex
swept file: yes
VERDICT: FAIL
Basis: The local implementation/ready-PR scope is appropriate, but origin/metadata persistence and one existing source-read defect need explicit dispositions before implementation. This is plan QA, not installed-pilot acceptance.

Evidence scope: Read the complete embedded acceptance packet, doc/gh3-plan.md, doc/recon-gh3.md, README.md, INSTALL.md and both tailers and exporter, including pre-existing code. Graph list_projects returned 77 projects with has_more=false and no CLIO/current worktree project; no current generation or coverage can be asserted, so direct source fallback was used. Downstream external-source claims are recon evidence, not independently verified deployed behavior. No git, suites or executable fixtures run.

- [Should] R1 — Specify persisted origin independently of display machine and freeze its identity treatment (plan gap). `doc/gh3-plan.md:33` lists machine but no origin-device/local-import membership; `:43` requires imported records never be exported as local. A receiving DB must implement that predicate without guessing from historical machine names. Fix: define the minimal stored origin/ingestion provenance and export selection rule, how unknown legacy origin is assigned for ownership without manufacturing captured device metadata, and whether transport/ingestion fields participate in record_id. State that receiving-device context cannot change an imported ID. No synchronization service needed.
  Observed input: the event schema at `doc/gh3-plan.md:33` plus the rule "imported records must not be re-exported as local" at `:43`; legacy row `{timestamp:"2026-09-29T12:00:00Z",session_id:"s",prompt:"fixture",machine:""}` has no origin-device identifier (illustrative contract input, not an executed implementation failure).
  Affected scope: local legacy ingestion, local capture and device-snapshot import/export, including unknown or renamed machine labels.
  Falsifier: A captures one event and imports B's snapshot, B imports A's snapshot; repeated exports contain only each owner's events with unchanged IDs, while a legacy empty-machine row remains unknown in query results. If existing schema text already determines all those outcomes, cite the exact fields/predicate instead of adding machinery.

- [Should] R2 — Preserve unknown metadata explicitly (plan gap against the engineering contract). `doc/gh3-plan.md:33` specifies a closed event-field list and `:39` seven legacy fields plus additive provenance, but gives no retention rule for unrecognized input keys. Retaining originals is necessary but does not specify how SQLite/query/round-trip export preserves unknown metadata. Fix: state a small raw/extras JSON preservation rule, collision/identity treatment and round-trip expectations; keep normalization of recognized fields separate from preservation.
  Observed input: `doc/gh3-plan.md:33,39`; an otherwise valid legacy row with an additional `client_extension:{version:2}` key is not covered by the listed schema/export fields (contract counterexample, not a measured implementation failure).
  Affected scope: imported legacy/device rows carrying additional metadata; no requirement to guess absent values.
  Falsifier: import, query, compatibility/device export and reimport of that synthetic row retain the extension and stable ID; unknown metadata cannot silently overwrite recognized identity fields. A cited existing raw-payload contract satisfying this would resolve the finding.

- [Should] R3 — Add the existing Agy source-DB write to the narrow implementation scope (observed source defect). `utils/CLIO/clio-agy-tail.sh:112-124` uses `sqlite3.connect(db_path)` for a best-effort metadata read; when the conversations directory exists but the DB does not, this creates an empty file in agent-owned source history before catching the missing-table error. This contradicts the tailer's read-only promise at `:3-4`; recon acknowledges the metadata read at `doc/recon-gh3.md:17` but does not disposition the mutation. Fix: use a properly encoded SQLite mode=ro URI and retain the current best-effort empty-repo fallback; document it as a small existing seam correction, not a new reader subsystem.
  Observed input: nonexistent `<agy-root>/conversations/<session>.db` with its parent directory present, at `utils/CLIO/clio-agy-tail.sh:112-116`.
  Affected scope: Agy companion metadata reads only; missing/unreadable DB must not stop prompt delivery or create source files.
  Falsifier: missing DB remains absent and prompt delivery still succeeds; valid DB supplies the same repo metadata without byte changes. Verify through the existing Agy suite in a disposable clone.
  Narrow stdlib probe command (after `export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"; mkdir -p "$TMPDIR"`): `python3 -` with `with tempfile.TemporaryDirectory(dir=tempfile.gettempdir()) as d: p=pathlib.Path(d)/"missing-source.db"; print("before:",p.exists());` then `with sqlite3.connect(str(p)) as c:` execute `SELECT data FROM trajectory_metadata_blob`, catch OperationalError, and print `p.exists()` afterward. Exit 0; decisive output: `before: False`, `caught: no such table: trajectory_metadata_blob`, `after: True`. Only scratch files were created; no tailer fixture was executed.

- [Nit] R4 — Make newest-first rolling order explicit at `doc/gh3-plan.md:39,53`: use timestamp descending with a stable record-ID tie-breaker. The acceptance packet requires newest first; chronological compatibility JSONL at `:39` must remain ascending. Add explicit clone verification for simultaneous capture/read/export and full-disk/spool-persistence failure, rather than relying solely on the broad "all requirements" checkbox at `:65`.
- [Pass] The minimal authority and delivery structure is proportionate: `doc/gh3-plan.md:29,35,37` retains one shared insertion boundary, stdlib SQLite, bounded capture, durable hook receipts and final legacy-lock/config recheck. Existing nonzero cursor retry is supported by `utils/CLIO/clio-codex-tail.sh:264-281` and `utils/CLIO/clio-agy-tail.sh:196-213`. Keep those contracts.
- [Pass] Shared historical Markdown and permanent receipts remain separate from rolling membership (`doc/gh3-plan.md:39,53`; existing shared-note behavior `utils/CLIO/INSTALL.md:290-321`). Phase 2 has hard merge/fleet dependencies (`doc/gh3-plan.md:72`), and installed pilot requires separate authorization (`:88-92`). Ratings and recurrence uncertainty are stated without treating potential history loss as observed loss (`:25`).
- [Unverified — needs clone run] SQLite correctness/performance, all four capture routes, contention/crash recovery and full acceptance controls remain future implementation evidence (`doc/gh3-plan.md:51-54,65-66`). Recon's baseline statement at `doc/recon-gh3.md:40` supplies no result artifact here; do not promote it to a reviewer-witnessed suite pass. Existing lock-drop and same-second suppression are already dispositioned by the plan (`INSTALL.md:182-201`; plan `:33-37`); the additional pre-existing source defect found in this sweep is R3.

Handing off to author — disposition R1–R4, revise the plan/source-scope contracts, then open Round 2 for review. No artifact or source file was edited by Reviewer.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
