---
title: CLIO SQLite and work provenance — build plan
status: In progress
owner: Codex
created: 2026-09-30
updated: 2026-09-30
reversibility: Costly at deployed cutover; Easy in isolated fixtures
---

# CLIO SQLite and work provenance — build plan

**2026-09-30 correction:** same-path Obsidian migration is now required. [Revision plan](gh3-same-path-plan.md) supersedes the separate-final-note clauses below. The revision is implemented, plan/final reviews are Approved, and the revised five-suite gate passed; PR4 is the handoff. Prior results remain historical.

| Most recently completed phase | What's next |
|---|---|
| Phase 1 merged as fd48d1c; Agy QA and final gate passed; local runtime installed | Local capture-only active; Phase 2 consumers eligible; rolling note not cut over; fleet blocked on #282 |

## Table of contents
- [Phase 1: Local history and export contract](#phase-1-local-history-and-export-contract)
- [Phase 2: Existing Rebalance consumers and fleet publication](#phase-2-existing-rebalance-consumers-and-fleet-publication)
- [Phase 3: Deployed pilot](#phase-3-deployed-pilot)

## Phase 1: Local history and export contract
**Goal:** CLIO can capture/query complete local history in SQLite, project exactly 168 hours to Markdown, and export provenance for current readers and future fleet consumers.

Tracking: https://github.com/HiQS-Labs/XYZ-CLIO/issues/3 . Base a0674039, branch feat/gh3-sqlite-history; task clone clio-gh3-sqlite. No PDDA/RELEASES in CLIO; issue and this document are the existing-equivalent task record, not a new governance framework. [Recon](recon-gh3.md) is the source/failure map.

Rating: **rated 78/65/50/35** (priority/severity/appeal/cheapness). Priority reflects explicit operator request and30minutes finding device; severity reflects lost provenance and potential history loss at unsafe cutover, not observed irreversible data loss. Appeal neutral 50; effort 35 because storage/capture/compatibility migration spans readers. Recurrence window Sept16–29 vs Sept2–15: one reported device-lookup incident; target issue inventory contains only #3, no independent incident trend established. Do not infer recurrence from cross-posts.

### Scope and design decisions
Python stdlib sqlite3/argparse/json/hashlib/tempfile/fcntl only; one new clio-store.py storage CLI, retaining INSTALL.md capture cleaning/shims and tailer protocols. No service, embedding model, new scheduler, Git pusher, ledger writer or vector DB. Proportional SOLID: one persistence boundary and focused capture/import/query/projection functions, no plugin classes/framework. Include the narrow Agy companion-metadata fix: use a properly encoded SQLite `mode=ro` URI instead of `sqlite3.connect(db_path)` at clio-agy-tail.sh:112–124; missing/unreadable metadata remains best-effort empty repo, and must never create or alter source files. Target ~700 lines engine; reassess if a generic framework starts to emerge.

Use opt-in activation config at ~/.claude/clio-storage.json (DB path plus private local device identifier). Existing installations remain legacy until explicit activation; installer installs helper before any config switch. Shared writer delegates the normalized row to helper only when activation config exists; capture's legacy route remains tested for rollback. Do not activate this device during start-task.

Schema version 1 contains immutable events (record_id, legacy_id, UTC timestamp, repo, branch, machine, agent, session_id, prompt, checkout, optional canonical repo_slug and typed references), import source progress/line accounting/quarantine, and device export metadata. Unknown strings remain unknown. Timestamp validation rejects naive/invalid times. New ID is deterministic SHA256 of canonical source-record fields including origin/agent/prompt (and device label for rows without source_event_id); legacy_id is a nonunique alias. Exact same normalized historical content is deduplicated; count every source occurrence separately. Tailers provide source_event_id from the immutable raw source-line hash and byte offset (scoped by origin/agent/session); never generate a random ID per retry. For those rows, identity excludes delivery-time repo/branch/machine/checkout/repo_slug observations. Capture/drain retain the first committed observations on replay; strict imports still reject differing payloads for an existing identity. Legacy/hook rows without source identity retain full-payload identity. Imports preserve original stored agent; do not copy Markdown's claude-code display fallback into history.

Persist `origin_id` and `origin_kind` independently of human `machine`: config has a stable owner UUID; new capture uses that UUID with kind `captured`; legacy JSONL explicitly adopted by this store uses it with kind `legacy-adopted` (ownership at import, not a claim about historical hardware). Captured `machine`/agent stay exactly recorded or unknown. Snapshot import preserves original origin fields and ID and records receiving/source-file/offset provenance separately. Device export selects only `origin_id == configured owner UUID`; every snapshot row must match its embedded manifest owner. Foreign rows never acquire the receiving UUID. The ID algorithm hashes a versioned canonical source payload (normalized recognized fields, origin fields, typed references and extras; tailer delivery-time observation fields excluded as described above), excluding receiving store, ingest time, source pathname/offset, projection cutoff and transport manifest. Reimport on another device therefore preserves identity. Identical unknown legacy histories independently adopted by two stores may have two ownership IDs; disclose that ambiguity instead of merging by guessed hardware.

Store unrecognized source keys losslessly as `extras` JSON alongside recognized normalized fields. Extras cannot override reserved identity/schema/provenance fields; conflicting reserved keys are rejected/accounted, not silently shadowed. Query and compatibility/device export preserve extras as a namespaced object, and the versioned importer restores it without nesting it again. Extras participate in the immutable source payload hash; receiving/transport fields never do. Test an extension such as `client_extension:{version:2}` through import → query → both exports → reimport with unchanged ID and values.

One insert function handles imports, capture and spool drain with ON CONFLICT idempotency and explicit payload-conflict detection. Private DB/spool/config files 0600, directories 0700. SQLite transactions, busy timeout≤500ms; capture budget ≤2 seconds on fixture host, report measured p50/p95/max. Tailers can retry failures. Hook capture first writes a private atomic durable spool record, then attempts transaction; if busy, receipt succeeds with pending diagnostic and scheduled drain; if spool cannot persist, nonzero + content-free error (never claim successful capture). Spool files are deleted only after committed rows, under a drain lock, idempotently. Diagnostics reuse prompt-log-errors.log; no prompt content in ordinary logs.

Migration is additive, not in-place transformation: importer reads complete JSONL lines from a retained source, commits bounded chunks with progress and source fingerprint/accounting. Malformed full lines get raw private quarantine plus reason; unterminated tail remains pending. Resume checks source identity/prefix instead of silently accepting replacement. Explicit source reset/new source name required on mismatch. Source path cannot equal compatibility output. Full capture backfill remains through same insert function; old writer continues append until final lock/drain boundary. Activation requires new helper/writer installed, old append lock acquired, final delta imported, nonempty source accounted and DB integrity/parity verified, preserved original source backup and rollback command. No source deletion or overwrite. Use existing lock protocol only for bounded final cutover; if backlog exceeds budget, refuse and run another online import first. The updated legacy writer must recheck activation config after acquiring the append lock, so a writer already waiting at cutover cannot append to the old authority. All writers on that device must use shared updated hook before activation; unknown installed clients block pilot, not isolated PR.

Compatibility JSONL is a derived, atomic chronological (timestamp,record_id) full-history export, retaining seven legacy fields plus additive provenance. Schedule catches projection failures without rolling back capture. Keep compatibility JSONL separate from the active legacy capture log while mixed writers remain; publish Markdown only at the registered existing Obsidian destination. The revised migrate-view command registers the existing Obsidian path after coverage and backup checks; project defaults to that registered path and the existing job invocation is unchanged. Existing exporter gets an explicit SQLite mode/config path; legacy mode and cursor/manifest retain original meaning. Existing60second job can invoke new mode for drain+projection with no new timer. Same snapshot+cutoff produces same bytes. UTC display avoids timezone-dependent output; all metadata and full quoted multiline prompts included. Render in timestamp descending, record_id descending order (compatibility JSONL remains timestamp ascending, record_id ascending). Select cutoff−168h ≤ timestamp ≤ cutoff; future rows retained in DB but excluded from view. Empty view states empty. Report rows and bytes; never truncate. Atomic temp+fsync+replace in destination directory preserves prior file on failure. Do not update old permanent receipt/cursor for rolling view.

Read-only query opens URI mode=ro with query_only; never initializes/migrates. Parameterized filters: from/to UTC, repo/repo_slug, device, agent, session, recordID, text, issue/PR/ledger reference, limit/offset with deterministic time+ID ordering. Return complete metadata and typed references. Add time and common filter indexes. Start substring text search; evaluate available FTS5 on nonempty measurements, add only if justified. Explicit links use fully qualified issue/PR URLs or ledger repository+rowID and relation `mentioned`/`task-context`; no NLP ownership inference, no automatic accepted-start/status writes. CLI accepts explicit metadata context; historical unknown checkout stays unknown. Captured Codex cwd should be preserved (currently dropped).

Device export is an explicit atomic versioned snapshot (stable records plus device ID, generated UTC, row count and content digest), imported idempotently with retained origin; no upload/push within CLIO. File contract devices/<device-id>/clio.jsonl uses an embedded first-line manifest so payload and digest publish in one atomic file, with one device owner; imported records must not be re-exported as local. Provide a staged export command and example for existing publisher integration; transport/combined read is Phase 2, not falsely called active fleet sync. No live SQLite/WAL sync.

CLI surface (one tool, no separate service): `init`, `import-jsonl`, `verify-import`, `activate`, `capture`, `drain`, `query`, `project`, `export-device`, `import-device`, `backup`. Reads (`query`, `verify-import`) never initialize a DB. Restore/rollback are explicit documented operations to a fresh path, not an automatic overwrite. The scheduled exporter calls drain + project; no background thread. Source-event IDs are supplied by the two tailers; typed references are optional producer metadata, not guessed from ambiguous historic text.

Open questions for reviewers: SQLite authority is explicitly requested; a read-only SQLite projection would be smaller but would not satisfy that request. Direct SQLite writes with tailer retries alone are smaller but lose hook prompts under contention; durable receipt is retained for hooks. A shared live SQLite in Git/cloud sync would be superficially centralized but violates per-device write ownership/WAL consistency. Chosen mechanism: local canonical DB plus stable per-device snapshots and reuse of existing transport.

### Ordered implementation and verification
1. Commit recon, plan and sanitized requirements; persist/read back ratings in#3; run real Codex plan relay (max 3 rounds, reviewer writes thread only) → require Approved before production edits.
2. Add schema/canonical insert, readonly query, bounded import/accounting and durable capture/spool → synthetic nonempty histories preserve all valid fields; repeated import/capture yields identical IDs, malformed rows accounted, interrupt/resume loses no complete record. Negative controls remove a row/corrupt identity and parity must fail.
3. Integrate optional writer route and preserve cwd/context, installer activation/rollback and schedule adapter → all four agents reach same insert boundary; existing four legacy suites remain valid; new SQLite cases prove busy/spool drain/retry, simultaneous capture/read/export against nonempty input, large Unicode prompts and surfaced write failure. Exercise SQLite full-page capacity or an equivalent deterministic write failure and separately an unwritable spool destination: no success without a durable DB row or spool receipt. Existing Agy suite proves a missing metadata DB remains absent and a valid metadata DB supplies the same repo without changing source bytes. New fixtures are synthetic only.
4. Add deterministic full JSONL, seven-day MD and device snapshot/import → exact boundaries/future/empty/idle expiry correct; remote same-second rows retained; A/B round-trip snapshots never echo imported foreign records as local, including an adopted empty-machine legacy row that remains unknown in results; byte-identical fixed cutoff; failed rename preserves prior bytes. Historical note backed up and header preserved by same-path migration; legacy receipts untouched. Query returns which device/agent/session/checkout with explicit issue links, unknowns shown.
5. Extend appropriate existing capture/exporter suites plus one focused stdlib storage suite if shell cannot efficiently test transactions. No testframework/fuzzer/synthetic runner. Run affected suite each iteration; final full four shell suites plus storage suite exactly once after final Approved. Measure same nonempty synthetic corpus query/export/latency vs JSONL; assert same returned IDs and report SQL query plan. No claimed speedup from different filters/corpora.
6. Commit docs/results; Codex final relay max 3 rounds; dispositions via ponytail, debugging via debug-mantra. Verify tests/diff/head then push/open ready PR against main. Re-read remote PR head/base/checks. Keep#3 open and label phase/delivery honestly. Preserve task clone for merge handoff; no automatic merge/deploy.

### Risk and failure scenarios
Source-of-truth change is operator-approved, not a reason to ask again. Crash before durable receipt → nonzero diagnostic; after receipt beforeDB → pending replay; afterDB beforeprojection/cursor → stable-ID replay. Concurrent handlers → SQLite transaction+uniqueID; projections serialized separately. New emptyDB → explicit empty header, cannot pass migration parity on empty expected source. Corrupt/partial import → quarantine or pending complete-line offset. Legacy missing metadata → unknown. JSONL/SQLite disagreement after activation → SQLite wins; regenerate derived view, never ingest compatibility output back as legacy source. Fixed IDs with differing payload → error, no overwrite.

Blast: existing hooks/tailers/readers plus new SQLite/spool/import metadata/config and exports. Shield is opt-in local pilot plus guarded compatibility output/source backups. Tripwire any missing accounted source row, latency>2s, failed atomic output or unresolved spool backlog at pilot review → stop rollout, retain artifacts, restore preserved writer after exporting SQLite-era arrivals. Rollback must not discard post-cutover events; original tailer cursors preserved. Restore backup only to new path, verify integrity/counts before switching config. Uninstall preserves DB/history/backups.

### Plan review disposition
Round1 returned non-approval (driver exit5, reviewer FAIL); no implementation started. R1 accepted: persisted origin/ingestion separation and exact owner export predicate. R2 accepted: namespaced extras with immutable source identity and round-trip verification. R3 accepted: concrete pre-existing Agy read-only violation, fixed only at the existing connection seam. R4 accepted: explicit MD descending tie-break order and named simultaneous/full-write/spool-failure checks. No new subsystem or synchronization service added. Round2 Approved with driver exit0 and attestation at reviewed bfc4dbc2ff9f; implementation started afterward.

### Phase 1 — QA checklist
- [x] Four-lane recon and explicit authority classification completed; unknowns recorded.
- [x] Rating persisted/read back; plan relay Approved.
- [x] Phase 1 requirements have nonempty correctness/failure evidence and measured latency; final review findings tracked below.
- [x] Final relay Approved (round3, ba0f97de3afd); full qualifying suites passed once afterward on unchanged implementation. See final-gate.json.
- [x] [PR #4](https://github.com/HiQS-Labs/XYZ-CLIO/pull/4) marked ready; source history/deployment unchanged. Issue3 carries remaining dependencies.

## Phase 2: Existing Rebalance consumers and fleet publication
**Goal:** the existing query/Daily/semantic path returns device/agent/session/checkout and explicit ledger links across Macs.

CLIO prerequisite **landed as fd48d1c on 2026-09-30**. Rebalance consumer work is eligible for native intake/recon; fleet publishing remains blocked by https://github.com/HiQS-Labs/rebalanceOS/issues/282 (and config#281 as applicable). No stacked-PR or merge authorization inferred. Track here and in #3. Bounded prior-art check found adjacent #141/#202/#232/#233/#203 but no duplicate provenance-consumer ticket. When unblocked, create narrow Rebalance intake with native PDDA inbox/ROADMAP queue (not Forge SQL registration); do not modify a second repo prematurely.

- [ ] Extend current CLIO table/collector to preserve incoming stableID+provenance and typed links; keep legacy import fallback.
- [ ] Surface fields in existing Daily and SemanticDoc metadata; reuse existing readonly XYZ ledger integration (#233/PR235: daily_work_synthesis.collect_issue_statuses → releases_cycle.read_work_status → trusted load_work_evidence; canonical repo+issue join), native status remains ledger-owned. Distinguish mentioned issue from accepted task context.
- [ ] Integrate exact device-owned export paths into existing Pulse publisher/shared lock, no second push loop; consume all available device snapshots into local query projection, show expected/missing device and last sync coverage.
- [ ] Use existing semantic index for paraphrase lookup followed by exact record/provenance retrieval. No second vectors DB, no model choice work.

### Phase 2 — QA checklist
- [ ] Re-recon after dependencies merge; repo-specific governance/rating/planQA before edits.
- [ ] Two-device fixture answers device/agent/time with missing/stale coverage explicit, no re-export echo or task-status mutation.
- [ ] Existing semantic path finds paraphrase then exact metadata validates result; no unsupported claim about deployed vector freshness.
- [ ] Reviewed ready PR and consumer/sync evidence recorded; status refreshed.

## Phase 3: Deployed pilot
**Goal:** one device proves installed capture, convergence, recent view and rollback before fleet rollout.

Deployment is separate from start-task's ready-PR authority. Preserve originals; inventory installed writer versions and active source paths. Other machines remain legacy until explicitly upgraded, so same-path migration must verify note coverage and designate one publisher before replacement. Establish expected fleet list and choose one combined-view publisher after Phase 2 contracts land.

- [ ] After deployment authorization, freeze private backups, verify source account parity and new hook receipts, activate one device with bounded lock/drain.
- [ ] Verify all four installed capture paths, idle expiry, compatibility ingestion and exact provenance query; exercise rollback preserving post-cutover arrivals.
- [ ] Record deployed commit and sanitized results; only then deliberate fleet rollout and eventual retirement of legacy writers/readers/queued work.

### Phase 3 — QA checklist
- [ ] No production history loss or silent unknown fleet coverage; tests and pilot receipts distinct.
- [ ] Legacy retirement gated on all clients/readers/queued work accounted and rollback window closed.
- [ ] Issue remains open until its deployed acceptance is actually met.

### Final review disposition
Round1 non-approval (exit5): R1 accepted, all replacing output paths now share historical default/marker protection. R2 accepted, existing tailers add source-line/offset identity and capture replay retains first committed observations despite branch/device changes. No new persistence table/service/retry layer. These are fixes to the reviewed stable-replay contract; final round2 reviews implementation and narrowed identity rules. Focused actual tailer fixture commits A, defers B, changes branch and retries: exactly A+B, A original provenance retained.

Round2 non-approval (exit5): R3 accepted, shared guard recognizes standalone historical marker lines, allowing repeated JSONL exports with marker text inside prompts. Witnessed new fixture fail before fix; round3 reviews the one-predicate correction and extended existing case.

Final round3 Approved and attested (exit0); five qualifying suites exit0 at bc444c619fd9. Final benchmark and warnings/skips are recorded under TESTS-RESULTS/2026-09-30-gh3/. PR#4 is the handoff; issue3 stays open for dependent consumer/fleet/pilot work. No installed deployment.

Handoff: retained full clone `/Users/noelsaw/task-clones/clio-gh3-sqlite`, branch `feat/gh3-sqlite-history`, ready PR#4 against main. Retain until landing and reconcile/retire via `/merge-cleanup`. Relay validation clones retain coordination/provenance evidence until handoff completes. No other task PR or parked experimental branch in this group.

Same-path revision completed: existing Obsidian path/filename and plist remain unchanged; migration verifies coverage/backup, preserves header and routes existing scheduled invocation. Revised16-case storage + four shell suites passed after final approval. See gh3-same-path-plan.md for current behavior; older separate-path approval/results are historical.

Review takeover and ordered merge/deployment continuation: [gh3-handoff.md](gh3-handoff.md). PR review follow-up Approved by independent Codex round1 (attested exit0); four shell suites plus 16 SQLite cases passed afterward on unchanged implementation. See TESTS-RESULTS/2026-09-30-gh3-review-followup/.

2026-09-30 deployed-source update: Agy round2 Approved (attested exit0), final five-suite gate passed, PR4 merged; five runtime files installed with existing plists and note bytes preserved. SQLite/rolling activation is held on actual coverage and ambiguous-note guards. See TESTS-RESULTS/2026-09-30-gh3-local-runtime/. Earlier “not authorized”/await-merge handoff language records prior scope; the latest user explicitly authorized merge and local deployment.


2026-09-30 local capture continuation (latest operator scope): the supplied eleven-file collection is final; the operator accepts unrecoverable older MacStudio history and requires no further recovery chase. Preserve the original note and all decoded sources privately. Implement explicit activate --capture-only: SQLite capture plus existing scheduled full-history compatibility JSONL, without any Markdown replacement. Extend the existing project function with guarded JSONL-only output; retain default fail-closed behavior for activation without this explicit mode and all migrate-view gates. No timer, collector, shared writer, new Markdown note, vector store, push loop or ledger writer. Imported legacy laptop histories receive separate local adoption-store origins; these are not claims about future installed device UUIDs. Skip the Mini’s copied Studio history after proving exact subset equivalence. Other Macs stay unchanged until individual installation. Same-path rolling publication remains separate from this capture-only stage; the known active laptop publishers make it inappropriate here.

Reversibility: code Easy; installed activation Costly. Back up scripts, source, cursor, registrations and note privately; verify import accounting. Rollback must pause capture, drain receipts and export all SQLite-era events before restoring legacy capture. The original note alone is not a history rollback. Existing storage activation test covers all four shared-writer routes, scheduled JSONL-only publication, unchanged note/plist/source and rejection of unsafe outputs and incomplete migration. A false capture-only flag witnessed the scheduled-export failure; no new suite. Independent relay and final existing suites precede runtime installation.

Local capture continuation deployed: SQLite active, existing five-minute job healthy with JSONL-only compatibility refresh, downstream configured, note preserved. Operator accepts unrecovered older history; no further collection. Other Macs remain per-install work. Rolling-note/fleet acceptance remains unclaimed.

### 2026-10-01 authorized same-path cutover

The operator confirms CLIO is turned off on all other devices and authorizes
activating the same-note seven-day view. The current note has ten historical
section markers; the accepted historical gap prevents strict parity. Extend the
existing migration with explicit `--archive-unreconciled-note`: preserve the
whole note with its verified exclusive backup, use the header through the first
marker, and report archived-not-reconciled/null covered count. Default migration,
publisher assertion, target identity, hashes, and foreign-write refusal stay
strict. No recovery chase, metadata reconstruction, new service or note.

Cutover is Costly: it replaces the live note body. Rollback must retain all
SQLite-era arrivals and restore the verified original note/config while the
local exporter is stopped. Check synthetic repeated-marker migration and
post-publication foreign edits in the existing activation case, independently
review, then run existing suites in a disposable full clone before deployment.

### 2026-10-01 no required machine — revised architecture plan

The operator rejects a permanent Studio hub. [gh3-device-independent-plan.md](gh3-device-independent-plan.md) is the new fleet architecture, superseding that assumption: every Mac holds full replicated history through existing Git Pulse; travel capture/query/same-note refresh must work with Studio off. Current local pilot remains installed unchanged. Note transport choice requires explicit resolution; no automatic failover is claimed.
