# Recon Map — CLIO history and fleet provenance
Commit: a0674039407e53baee18ca30d9c33413732c232b · 2026-09-30 UTC
Mode: graph inventory + source fallback. CLIO absent from 77 indexed projects.
Rebalance graph generation 2026-09-02T03:54:57Z is stale; coverage reports changed metadata for pulse/semantic modules and excludes scripts. Exact source was read instead.
Lanes: A entry points (parent), B state, C external contracts, D operations (three read-only explorers).

## Subject and authority classification
Source of truth, explicitly requested by the operator: SQLite replaces local JSONL authority.
Derived Markdown, JSONL compatibility and fleet snapshots never own task state. XYZ RELEASES remains task authority; Rebalance remains a derived search index. A read projection alone solves lookup, but does not meet the explicit SQLite-authority request.

## Seams and call paths
| Seam | Confirmed location | Contract / consequence |
|---|---|---|
| Claude/ZCode hooks | utils/CLIO/INSTALL.md:57, :207 | Embedded shared writer is installer and test source; preserve registrations and cleaning rules. |
| Shared persistence | utils/CLIO/INSTALL.md:137, :189, :201 | Seven fields, UTC seconds, session:timestamp dedup; same-time different-device/text collisions are currently suppressed. |
| Codex source/cursor | utils/CLIO/clio-codex-tail.sh:55, :183, :264 | Source rollout → normalized row → shared writer → advance inode/offset/context only after success. |
| Agy source/cursor | utils/CLIO/clio-agy-tail.sh:107, :155, :196 | USER_EXPLICIT full transcript → writer; retry nonzero without cursor advance. Auxiliary metadata DB only supplies best-effort repo basename. |
| Existing Markdown | utils/CLIO/prompt-log-to-md.sh:484, :500, :560 | JSONL cursor + permanent ID receipt; append-only shared note, not rolling membership. |
| Schedule | utils/CLIO/INSTALL.md:318, :343 | Multiple devices contribute to shared note; existing 60-second job can drive expiry while idle. |
| Fixture install | test/clio-capture.sh:18; test/clio-codex-tail.sh:25; test/clio-agy-tail.sh:25 | Tests extract writer heredoc. Preserve markers; install new helper explicitly in SQLite fixtures. |

## External consumers (Rebalance checkout 17e08c17)
Paths in this section are relative to HiQS-Labs/rebalanceOS.
- src/rebalance/paths.py:101 chooses one JSONL source via argument/env/user-config/default.
- src/rebalance/ingest/clio.py:88 scans JSONL; :134 derives own ID from session/time/filtered text; schema at :25 drops device and branch. Incoming stable IDs currently ignored.
- src/rebalance/ingest/clio.py:162 supplies existing SemanticDoc provider; metadata :190 lacks device. index_ops.py:1564 invokes registry providers, :2291 registers CLIO. Vectorization already exists; no second vector store needed.
- utils/daily_work_synthesis.py:97 reads last 512KB, reverses and stops at first old timestamp. Compatibility JSONL MUST be chronological.
- src/rebalance/ingest/clio_journey.py:113 parses legacy Markdown marker/heading/blockquote; :195 dedups source provenance. Keep historical note untouched during pilot.
- src/rebalance/ingest/pulse.py:807 publisher holds git_publish_lock. experimental/git-pulse/collect.sh:597 stages a device-owned PDDA registry; reuse publisher seam, never add a CLIO push loop.
- utils/daily_work_synthesis.py:203 collect_issue_statuses → utils/py/releases_cycle.py:39 read_work_status → trusted releases_app.py load_work_evidence: readonly bounded ledger evidence, canonical repo+issue joins; reuse this seam rather than add a CLIO ledger reader.
- Bounded downstream prior-art search: #141 is original semantic ingestion; #202 session producer status; #232 journey trial; #233 delivered status display; #203/#282 fleet ownership. No specific CLIO provenance-consumer ticket found. Open PRs #298/#294 do not cover it; predecessor repo had no open PRs. New follow-up intake must use Rebalance PDDA inbox + ROADMAP queue, not Forge SQL registration (native policy differs).
- Live Rebalance #282 remains open, one owner per device path and one pusher per Mac. #281 config ownership remains open. PR235 is merged (9fd0d494); #233 planned wording is stale. Reuse existing readonly ledger integration in downstream work.

## State and failure audit
Resting: JSONL, MD, delivery manifest, tailer state. In flight: stdin hook payload, parsed tailer chunk, temp export. No external messages/payments; filesystem writes only.
Existing hook lock exhaustion returns0 and drops (INSTALL.md:182); tailers can retry any nonzero. New hook path must spool durably before acknowledging under contention. Crash before spool receipt is a surfaced failure; crash after spool/DB commit is replayable by deterministic ID. Projection failures cannot undo committed capture. Import progress must commit atomically with rows/quarantine; incomplete tail stays pending. Empty imports cannot authorize activation. Legacy metadata remains unknown. Cross-device same-second records need a stronger ID with legacy ID only a nonunique alias.
Existing shared MD cannot be atomically regenerated from only local records without losing foreign view entries. Initial rolling output must be separate. Old receipts and cursor must not be reused for expiry.

## Build and rollback
Four shell suites use throwaway HOME; capture baseline passed this session. All four baseline logs and provenance are retained at TESTS-RESULTS/2026-09-30-gh3/. No package/build/CI or PDDA/RELEASES infrastructure exists in this small repo. Keep source history and installed runtime unchanged during isolated build. Pilot is a separate deployment step. Rollback after pilot requires exporting SQLite-era rows into a chronological compatibility log before re-enabling legacy writer; preserve source backups and tailer state.
Relay locator foreign-CWD advisory branch calls undefined driver_lock_path_for_repo; running locator from an isolated full harness clone succeeds. Real driver --target-root can review CLIO with thread inside CLIO; no vendoring or unrelated source fix needed.

## Review-confirmed source defect
Agy companion metadata uses writable sqlite3.connect at clio-agy-tail.sh:112–124. A scratch stdlib probe in plan review created a previously absent DB before the missing-table error (exit0; before False → after True). Include the tiny mode=ro URI correction in phase1; preserve best-effort fallback. This is distinct from changing CLIO persistence.

## Unknowns
| Unknown | Why it matters | How to settle |
|---|---|---|
| Installed versions across all Macs | Mixed writers cannot safely share one live log | Pilot deployment receipts and writer checksum inventory before cutover |
| Historical exact duplicate occurrence vs retry | Old seven-field rows lack source-event ID | Preserve source occurrence/accounting and disclose deterministic dedup rule; cannot reconstruct lost events |
| Full fleet coverage | Local DB is not proof every Mac synchronized | Device manifests with last publication and expected-device list in downstream reader |
| Live embeddings freshness | Provider exists, deployment not verified | Readonly Rebalance pilot query after downstream merge |

Current radius: four agent capture routes, their cursors, shared Markdown, Rebalance ingest/Daily/replay/semantic provider, device publisher; no live runtime changes authorized by start-task.
