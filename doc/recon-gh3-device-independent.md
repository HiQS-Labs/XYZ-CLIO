# Recon delta — device-independent CLIO

2026-10-01. CLIO HEAD 4a309cd; bounded delta to doc/recon-gh3.md, not a fresh exhaustive audit. Lanes A/B/C/D traced in parent using existing recon plus current source. CLIO is absent from all 77 graph projects. Rebalance graph generation 2026-09-02T03:54:57Z: publication lookup returns only old git_pull_rebase_safe; coverage for lib/git_ops.py, ingest/pulse.py and experimental/git-pulse/collect.sh reports metadata_changed. Exact installed source fallback read; graph does not establish current behavior. No private prompt content inspected for this plan.

## Current paths and authority

- utils/CLIO/INSTALL.md shared writer → clio-store.py capture → insert (:226) → local events; busy writes use existing durable pending receipts and drain (:280). Capture is already independent of Markdown and network.
- clio-store.py export_device (:716) exports ONLY metadata.owner's events in one atomic manifest+payload, with digest, count and UTC; import_device (:731) verifies digest/count/origin and idempotently inserts, rejects self-import and identity conflicts. Imported events never re-export as local. Reuse these seams; no live SQLite/WAL Git transport.
- clio-store.py project (:634) writes chronological complete compatibility JSONL and 168-hour Markdown. Current checked_view (:557) protects exclusive original backup and accepted local hashes, not a distributed lock. Current Studio view is archived-not-reconciled, personal header preserved, gap accepted.
- Rebalance runtime experimental/git-pulse/collect.sh:314-333 uses the local OS publication lock; :482-508 refuses foreign dirty paths and pulls safely; :593-621 stages existing snapshot paths and performs one push-race retry. CLIO devices/<UUID>/clio.jsonl is NOT currently an owned/staged path. Extend exact ownership in this existing cycle rather than drop dirty files in a live clone.
- Rebalance runtime src/rebalance/lib/git_ops.py:36 git_publish_lock is local to the checkout; :404 publish_git_paths commits exact paths, one pull/push race retry and verifies upstream blobs. No fleet lease/fencing is provided by this local lock.
- ingest/pulse.py:807 wrapper holds git_publish_lock across render/write/publish. Existing consumers and semantic/Daily/readonly ledger seams are enumerated in doc/recon-gh3.md; not re-audited in this bounded delta.
- Installed com.user.git-pulse StartInterval is 3600 seconds. User chooses the existing cadence, not a new five-minute network push loop. Existing local note renderer remains 300 seconds.
- Data repo Hypercart-Dev-Tools/rebalance-git-pulse is private (gh repo view, 2026-10-01). Public CLIO code repo never receives prompts/snapshots/DBs. Privacy and access must be rechecked at rollout.
- Canonical open dependency https://github.com/HiQS-Labs/rebalanceOS/issues/282 requires per-device owned paths, build fleet views on read, one pusher/Mac, one local lock and honest liveness. Predecessor Hypercart-Dev-Tools/rebalance-OS #282 is unrelated; never use it as this dependency.

## Failure and rollback

Studio off currently stops that note's publication, but each installed capture can remain local. Other Macs are presently disabled by operator. A replicated store must retain local unsent events during outages and rebuild imported history from Git. Snapshot publication is not acknowledgement until remote bytes verified. No phase deletes local DB/events, receipts, adoption stores, backups or Git history.

Obsidian Sync queues offline changes and has no demonstrated CLIO fencing. Staggering local writers is NOT mutual exclusion; resumed Studio can replay old writes. Official sync docs describe per-device exclusions and folder exclusion, but do not establish an exact-root-file exclusion mechanism on installed versions: https://obsidian.md/help/sync/settings . The root note must not be moved or an entire vault excluded to fake the prerequisite.

## Unknowns / scoped prerequisites

Exact-file Sync exclusion and all four installed Pulse versions require per-Mac proof. Mobile note refresh requirements are not supplied. Raw-history seed owner mapping/adoption stores must be preserved; no historical recovery chase. Rebalance #282 structural rollout remains open. Stagger offsets cannot imply freshness under sleep/network outage. Git remote availability is a shared external dependency, not a required Mac.
