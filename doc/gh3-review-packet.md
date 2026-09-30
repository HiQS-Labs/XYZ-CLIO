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
- [ ] Downstream consumers and installed copies are reconciled, a one-device pilot and rollback are verified, and private prompts/DB files are not published to GitHub.

Related: [Rebalance #232](https://github.com/HiQS-Labs/rebalanceOS/issues/232) storyline trial and [#210](https://github.com/HiQS-Labs/rebalanceOS/issues/210) evidence-bound synthesis. This storage work is separate and must not silently block or replace the frozen Luna trial.
