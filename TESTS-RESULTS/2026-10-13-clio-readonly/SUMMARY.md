# CLIO read-only access audit — 2026-10-13

Contents: Outcome · Consumer map · Checks · Backup · Limits

## Outcome

Approach1 is already implemented and installed. No consumer or writer code change was necessary. The installed helper is byte-identical to canonical XYZ-CLIO main's helper. The safe ad-hoc audit procedure is documented in `utils/CLIO/INSTALL.md`; live mode=ro is not a reliable audit entrypoint in the observed cold-WAL configuration. No immutable live reader was found in the searched executable paths. No journal-mode change, vacuum, migration, record write, lock deletion, or new test/gate was performed.

Scope: current local rebalanceOS production source (including scripts and MCP modules), canonical XYZ-CLIO, Git Pulse Sync executable/distributed skill files, configured installed CLIO helper and installed fleet collector. Generated prompt/history payloads are not executable consumers and were not searched for prompt content. No assertion about unlocated historical one-off agent commands or other devices.

## Consumer map

| Consumer | Source and connection behavior | Change |
|---|---|---|
| Native CLIO query/export/projection/backup | XYZ-CLIO `utils/CLIO/clio-store.py:97`: database(); mode rw at103; query_only at107, before schema reads. query at463; projection744; export-device798; backup1014. Installed `~/.claude/hooks/clio-store.py` is identical. | Already approach1 |
| Fleet check-in CLIO export | Rebalance `experimental/git-pulse/collect.sh:620`, native helper call629; installed `~/bin/git-pulse` has the same call. Configured helper is the installed native helper above. | Already approach1 through canonical helper |
| New clio skill | PR8 adapter calls canonical query(), which uses database(); no independent SQLite connection. | Already approach1 |
| Rebalance CLIO ingest | `src/rebalance/ingest/clio.py:96` resolves JSONL, line111 opens it; writes its separate Rebalance projection via103. | Does not open canonical SQLite |
| Rebalance journey | `src/rebalance/ingest/clio_journey.py:555` resolves prompt export;564 queries GitHub snapshots in Rebalance DB. Its mode-ro gateway is for github_items, not canonical events. | Outside native-history connection seam |
| Rebalance daily/semantic CLIO readers | `clio.py:66` reads clio_prompts in caller's Rebalance DB; `clio_semantic_docs` at190 receives Rebalance connection. | Separate projection database |
| Fleet rollup/probes | `src/rebalance/ingest/pulse_health.py:231` reads YAML and bounded Git status/page objects; health-check.py consumes those results. | No CLIO SQLite open |
| Agy companion metadata | XYZ-CLIO `clio-agy-tail.sh:112–114` reads conversations/<session>.db trajectory metadata with mode=ro. | Separate external DB; preserve contract |
| Experimental release-board/freshness/triage and release ledger | release-board/spike.py:627 and freshness/spike.py:314 default to rebalance.db; triage/spike.py:44 uses Rebalance; utils/py/releases_cycle.py:47 selects releases.db. | Separate stores; unchanged |
| Other Rebalance read-only gateway callers | `src/rebalance/ingest/db/connection.py:91` serves Rebalance/other explicitly supplied databases. No audited caller passes the configured canonical CLIO file. | Preserve mode=ro; no global widening |
| Ad-hoc count audit | INSTALL.md “Cold-WAL audit queries”: mode=rw then query_only, or canonical helper. | Guidance added; no new script |
| Writer journal setup | Native clio-store.py:130 initializes WAL; capture/import use same gateway with writable=True. | Unchanged |

Graph generation2026-09-02 was stale for CLIO and omitted scripts/MCP subtrees. Graph results were provisional and direct current-source reads/rg covered those paths. XYZ-CLIO/Pulse had no graph project. No negative claim relies solely on graph results.

## Checks and decision

Question: does the reported cold-WAL read fail, and is there an actual remaining native-history consumer to repair? Reused the existing reviewed cold-WAL protocol in XYZ-CLIO doc/gh3-plan.md (WAL repair section) and existing test_readonly_queries_refs_pagination_and_large_prompt, plus the operator's exact manual check. Decision: stop at approach1 if native consumers already use it; do not widen unrelated database gateways or change writer mode.

| Check | Result |
|---|---|
| Before: requested sqlite3 mode=ro SELECT count(*) | exit0, `4491`; WAL/SHM present |
| Fresh online backup, no sidecars, system mode=ro validation | exit14, unable to open database file |
| Backup mode=rw; query_only=ON; integrity_check/count | exit0, `ok`, `4492` |
| Installed helper via Apple SQLite3.43.2 | exit0, events4492, query_only1, journal wal |
| Installed helper via Homebrew SQLite3.53.4 | exit0, events4492, query_only1, journal wal |
| After: requested sqlite3 mode=ro SELECT count(*) | exit14, `Error: in prepare, unable to open database file (14)`; WAL/SHM absent |
| Supported manual mode=rw + query_only count | exit0, `4492` |
| Existing native cold-WAL/read-only case | PASS; cross-runtime absent-sidecar read, nonempty payload, SQL write rejection and missing-file noncreation |
| Existing Rebalance CLIO/fleet suites |26 passed,3 subtests passed |

This reproduces the original failure on a fresh backup and subsequently on the live raw-ro check. It does not show an application regression: both installed native readers succeed. The extra event between first check and backup arrived while capture remained running; these checks issue no event writes. Preserve raw-ro failure as evidence rather than keeping a process alive to prime sidecars.

Audit source revisions: Rebalance `e46150a0fdd8dd2e9f14ba27d74483ad9aa0db2e`; canonical CLIO `d17e521f3ed2b51a9158ea15fdc954959341b3d3`. These are historical observations from the audit, not a fresh qualification of later revisions. The PR adapter was checked in the isolated task clone.

Raw receipts: before.json, backup.json, checks.jsonl, immutable-scans.jsonl, existing-tests.txt. Exact live count probe is in manual-commands.txt. No private prompt records are in these files.

## Backup

Fresh online backup of the actual prompt-log.sqlite3 (not the old GH-282 backup):
retained in a private backup directory outside Git; its machine-specific location is omitted here.
Validated integrity `ok`,4492events, SHA256 in backup.json. Backup remains private outside Git.
The live project lock was observed and never deleted; the drain lock was absent at sampled moments, not assumed inactive globally.

## Limits

A snapshot count is not a fleet-completeness assertion. Capture stayed active; counts and sidecars can change independently of the audit. A passing raw mode-ro check only qualifies that instant. The clone test is synthetic and supports the connection contract, not every runtime/device. No actual sandbox with denied directory writes was tested; such a consumer would require a separate constraint-specific decision. query_only is a connection setting, not an OS access-control boundary against a caller that deliberately turns it off. The audit changed no code or installed runtime; this PR publishes its evidence and documentation only. Existing test output is retained without inventing a new harness; no broad suite or doctor run was needed for this documentation-only outcome.

References: [SQLite read-only WAL conditions](https://sqlite.org/wal.html#read_only_databases), [query_only pragma](https://sqlite.org/pragma.html#pragma_query_only). These explain why auxiliary-file handling and SQL write permission are distinct; the runtime-specific failure above is established by local observations.
