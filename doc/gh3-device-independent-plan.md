# CLIO without a required Mac — replicated SQLite through Git Pulse

Date: 2026-10-01. Status: Agy approved staged plan (relay exit 0); database requirements confirmed, note transport choice pending. Not implementation-ready for note rollout. Canonical issue: https://github.com/HiQS-Labs/XYZ-CLIO/issues/3 . Recon: [recon-gh3-device-independent.md](recon-gh3-device-independent.md).

This supersedes the permanent Studio-hub assumption in gh3-plan.md and gh3-same-path-plan.md. Their shipped capture, verified backup, same-path header and accepted-gap contracts remain. This is a plan, not authorization to upload private history, restart other Macs, change Sync settings, or modify installed jobs during this turn.

## Confirmed requirements, target outcome and limits

The operator requires that, after the disconnected pilot and staged rollout, every Mac retain a complete replica of all delivered CLIO history, capture locally even offline, query locally and refresh the SAME existing Obsidian note while the Studio is off. Use the existing deployed Git Pulse cadence (Studio collector currently hourly); this is a scheduling requirement, not a delivery guarantee. No Mac is a mandatory receiver, merger, pusher or permanent note publisher. The logical central history is the union of verified origin snapshots in the private Git Pulse repository; each SQLite file is a queryable replica plus its own durable unsent events. There is no new SQL server or one privileged SQLite binary in Git.

A Mac can only know records already delivered or captured locally; an offline peer's unsent prompts cannot be visible elsewhere. Capture survives a powered-off peer; unsent records on a physically lost source disk may still be lost. GitHub availability remains necessary for cross-device delivery, but offline capture/query/local projection continue. Existing historical gaps remain accepted, with full original note backups retained; no reconstruction or recovery chase.

## Smallest architecture

```mermaid
flowchart LR
  A[Each Mac: shared capture writer] --> B[Durable local SQLite + pending receipts]
  B --> C[Owner-only verified snapshot]
  C --> D[Existing Git Pulse cycle: exact owned paths, pull/commit/push]
  D --> E[Private Git repository: per-origin snapshots]
  E --> F[Every Mac: verify and idempotently import]
  F --> B
  B --> G[Local readonly queries and existing Daily/semantic consumers]
  B --> H[Same-path local seven-day view; note transport decision below]
```

Use the current local store, not a temporary SQL file: an OS temp purge must never lose the capture queue. Temporary files are only atomic serialization staging. One store per Mac can hold local AND imported records; a separate staging database and a second aggregate database add no value. Keep the established local DB path and configuration resolver on each Mac.

Each store owns a persistent CLIO origin UUID. Names/hardware UUIDs are inventory/display mappings, not rewritten event identities. Existing adoption origins from imported MBP histories remain intact; either adopt their store on that device deliberately or keep them as separate legacy seed origins and create a new owner for future capture. Never clone the Studio activation config/owner onto another active writer. Stable record IDs, payloads, unknown metadata and references survive import/rebuild.

Reuse `export-device` / `import-device`: one atomic versioned manifest plus canonical records, owner UUID, UTC generation, count and SHA-256. Transport cumulative owner-only snapshots under `devices/<origin-UUID>/clio.jsonl`, already the CLIO contract. Each path has exactly one producer; imported rows never echo through another origin. Full snapshots are the initial minimum mechanism, not chunks/deltas/compaction. Measure private Git growth during pilot before adding any such machinery.

## Reconciliation on the existing cycle

Rebalance owns integration into its existing Git Pulse collector/publisher, subject to #282. CLIO does not get its own pusher, watcher, cron, lease service, vector store or XYZ ledger writer. Keep one existing Git pusher per Mac, one checkout lock and exact staging allowlists; preserve foreign dirty/staged paths by refusing, never broad `git add`, stash, reset, force-push or automatic conflict erasure.

The scheduled cycle acquires the existing local Git publication lock, drains bounded local pending receipts, exports this owner to PRIVATE staging outside the checkout, verifies its manifest, and hands the exact owned path to the existing publication transaction. Persist pending local commits before pulling as existing publisher does; pull only through its safe reconciliation path. Never leave an uncommitted CLIO file for some later job to discover and accidentally wedge pull/rebase.

After pull, import every recognized foreign origin snapshot from the committed tree, NOT arbitrary dirty worktree bytes. Match pathname origin to manifest.owner; verify version, digest, count and all record identities. Track the last accepted digest per origin in existing import receipts. Unchanged payloads need not re-import just because generated_at changed. One transaction per origin: rejected/truncated/conflicting snapshots change no rows for that origin. An unchanged valid replay adds zero. Import committed snapshots before an attempted network push can fail, so known pulled history still becomes locally queryable.

Publish through the existing exact-path commit/push routine, at most its one race retry. A failed push leaves local SQLite and durable pending Git commits intact; next scheduled cycle retries delivery even if capture has no new rows. A busy lock skips that cycle with an honest status; no unbounded retry. A cumulative snapshot must not silently regress: compare known IDs/owner before replacing its prior snapshot, retain acknowledged local rows even if remote old versions reappear, and never use a smaller snapshot as a deletion instruction. Conflicting same record ID/payload stops that origin's import; independent valid origins may still import with partial-coverage status.

Optionally offset existing jobs by a deterministic device offset within their current interval, preserving frequency. This is load spreading only: simultaneous wake, drift and overlap remain correct through local lock + disjoint origin paths + existing Git race retry. No correctness rule or delivery guarantee relies on staggering.

## Complete-history bootstrap and recovery

Before road use, publish ALL existing accepted history by original origin, not merely the current Studio owner. Its two foreign adoption histories would otherwise disappear from export-device. Use retained adoption stores and the existing owner exports, or a narrow existing-helper export-by-preserved-origin extension if those stores cannot be reused. Stage and verify owner/count/digest for each seed; no ID rewriting. Never upload original private records to the public CLIO implementation repository.

Initialize each receiving Mac with its own owner or deliberate matching adoption-store owner, then import every OTHER known origin and retain its own local rows. Self-import is deliberately refused; its own history is already present. A trusted known-origin inventory records expected sources and legacy adoption mapping, separate from hardware naming. No machine must remain online after it delivers a seed. A fresh replica rebuilds from all committed seed/current snapshots. Removing a replica is never removal of history; keep its owner snapshots and backups. Reinstall uses existing origin/config if present; ambiguous reuse by two writers fails pilot qualification.

Query/Daily/semantic consume the local combined replica or existing chronological compatibility JSONL. Reuse the existing Rebalance CLIO provider/index registry/semantic store and readonly XYZ ledger joins; replication does not introduce another search index or ledger authority. Replication status exposes expected origins, last successful local capture/drain, accepted snapshot digest/generated UTC, last remote delivery receipt, last import and error per origin. It distinguishes full-known-history from stale/missing device coverage and alive-but-not-delivering. Never infer completeness from row count alone.

## Same Obsidian path without a permanent publisher

Database replication and note publication are separate safety questions. The current accepted-hash guard and Git checkout OS lock cannot fence another Mac's Obsidian Sync writes. Staggered timers or a Git lease with an unfenced local filesystem are not sufficient: a partitioned old owner can resume and upload stale note bytes.

Decision awaiting operator answer:

**A. Git Pulse transports this note; each Mac renders its own local view (preferred if exact-file Sync exclusion can be proven).** On EVERY participating vault, exclude ONLY the exact existing root note from Obsidian Sync before enabling a second projector. Keep its path/filename and all other vault syncing unchanged. Verify installed product supports this exact exclusion; official docs currently describe folder exclusion, so capability is not assumed. Never relocate the note or disable Sync for the whole vault to simulate compliance. With file exclusion verified, note is a local derived projection, not a shared multiwriter input: every Mac's existing five-minute job can render from its full replica while the Studio is off. The Git transport contains owner records and a versioned canonical header, not a multiwriter rolling-note binary. A travelling Mac includes its local unsent captures in its view; differing cutoffs are safe because these note bytes do not travel through a competing sync channel. Header changes are explicit compare-against-known-version edits via the existing Git transaction, not merged implicitly into generated body; divergent edits preserve both and stop header adoption. Preserve each original personal header/body/config in verified local backups. Local unexpected edits still refuse replacement for reconciliation. Mobile clients without this renderer are out of scope until explicitly added; do not claim automatic mobile freshness.

**B. Keep Obsidian Sync and manually transfer the one publisher.** Capture/query remain fully independent on all Macs. On road departure, explicitly stop and verify former projector, import current history and transfer note registration/header/hashes to the chosen travel Mac using verified backups; resume only its existing projector. No fixed Studio dependency, but automatic note recovery after unplanned publisher loss is NOT solved. An unreachable old owner cannot safely be assumed disabled. This option needs explicit acceptance of manual handover and stale note during ambiguous partitions; it is not the automatic no-hub note outcome.

If A cannot be demonstrated and B does not meet the requested outcome, stop note rollout and return a specific unresolved design choice; do not sign off with an implicit Studio owner. Database capture/replication can still be implemented independently. No distributed note lease/failover machinery is introduced just to conceal a second sync channel.

## Ordered implementation and proof

1. Land the currently reviewed CLIO implementation and retain private backups/adoption mapping; resolve native Rebalance intake for #282 and CLIO snapshot adapter. → one canonical issue/plan per implementation repo, no duplicate publisher.
2. Qualify exact publisher ownership and private data repo access; implement the adapter at the read recon seams in collector/git_ops. → owner-only paths under existing lock/staging, bounded retries and remote-byte receipt. No uncommitted integration artifact wedges pull. Keep existing cadence.
3. Bootstrap all retained history origins, then install a full replica on the travel Mac and a second peer. → exact record-ID/payload set parity over all delivered origins, preserved unknown metadata, zero duplicate replay; no shared owner collision. Other Macs installed case by case.
4. Resolve note transport decision and prove its precondition on every involved vault; reuse current same-path project/header/backup mechanisms. → original path retained, personal header byte parity, no competing note transport or old projector, clear accepted-gap disclosure.
5. Run existing CLIO suites in disposable full clones and relevant existing Rebalance/Pulse suites under their native policy. Record manual real-Git fault cases in committed TESTS-RESULTS provenance rather than new gate machinery. → two independent source clones capturing concurrently, simultaneous push race, sleep/wake, lock busy, failed push, malformed owner/digest/count, rollback snapshot, identity conflict, duplicate replay; no lost accepted events or foreign staged work. Witness red controls for owner and no-hub assumptions.
6. Shut down/otherwise disconnect Studio for a complete observed pilot window spanning at least two existing Pulse cycles, with two other Macs independently capturing, exchanging snapshots, querying the combined history, and refreshing the same note under chosen transport. Kill one between local write/serialization/push/import and resume. → no hidden Studio dependency, local offline captures retained, full delivered-source parity and note window/header verified, honest stale-source indicators. Do not claim this passed from simulation alone.
7. Roll out remaining Macs individually, preserving installed collectors/cursors and user disable backups. → all four Mac replicas converge on delivered ID/payload sets and all capture sources are covered; no capture gaps falsely repaired. Native Daily/semantic/readonly ledger and query checks prove consumers see fleet provenance without duplication. Retain task clone until landing and deployment evidence are reconciled, then merge-cleanup.

## Reversibility, shields and tripwires

Plan-only edit is Easy. Fleet transport and note ownership cutover are Costly: raw history enters a private Git retention plane, and mistaken sync ownership could overwrite personal content. Pilot and opt-in adapter shield the installed fleet; no existing jobs/settings changed by this plan. Tripwires: source snapshot regresses, owner mismatch, remote verification fails, foreign dirty work, any personal header mismatch, unexpected note writes, or missing known origins → stop relevant publication/adoption within that cycle, retain local capture and originals, diagnose with debug-mantra. Do not upload any seed until private destination/expected owners verified.

Rollback stops the new adapter/projectors, preserves all SQLite-era local arrivals and pending commits, exports/backs up each store, and restores verified previous config/jobs/note bytes. Never delete delivered snapshots or rewrite Git history, never reactivate legacy capture over a stale original JSONL without reconciling new arrivals. Re-enable one old note publisher only when all new note writers are proved stopped; rollback may temporarily leave the note stale while queries/capture continue. No automatic destructive undo.

## Planning honesty and remaining decisions

Confirmed operator requirements, to be proved by the disconnected pilot and staged rollout: all Macs hold complete history; use existing deployed Pulse cadence; travel Mac captures/queries/refreshes the same note with Studio off. Exact note transport choice still awaiting answer; A cannot be called implementation-ready until exact-file exclusion is proved or an alternative is explicitly chosen. #282 remains open and is not waived. Current deployed Studio still runs normally, others remain disabled. No planned replication or failover is claimed installed or tested. Agy QA must grade these prerequisites as explicit, not infer missing capabilities.
