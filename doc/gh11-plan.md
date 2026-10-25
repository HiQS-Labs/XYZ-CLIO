# GH-11 plan: no central device for fleet joins or the shared note

Issue: https://github.com/HiQS-Labs/XYZ-CLIO/issues/11
Base: `origin/main` @ `d17e521`
Branch: `feat/XYZ-CLIO-gh11-fleet-peer-discovery-2026-10-24`

## Problem, observed in code

1. **Each store has a hand-kept inventory.**
   - `reconcile_fleet` (`utils/CLIO/clio-store.py:963`) reads only `fleet['origins']`, which `configure_fleet` (`:935`) writes from repeated `--origin` flags.
   - A device whose `devices/<uuid>/clio.jsonl` is committed is ignored by every peer until someone signs in to that peer and reruns `configure-fleet` with the full list.
   - Observed on 2026-10-24: a laptop delivered its snapshot, but the note-writing Mac could not be reached to add the new origin, so its prompts are stuck out of the shared note.
2. **A second device cannot register a note that is already in the SQLite format.**
   - The peer-repair design already exists: `checked_view` (`:578`) accepts a peer's byte-reproducible render as `peer_generated`, and defers on unknown IDs for at most `FLEET_WAIT_SECONDS`.
   - However, `migrate_view` (`:638`) only registers a note through `legacy_coverage` (`:531`), which matches legacy `<!-- clio:id: -->` entries, or through `--archive-unreconciled-note`.
   - Once one device has published, the note holds `<!-- clio:record: -->` entries. `legacy_coverage` then fails ("unrecognized content below the historical marker"), so every later device stays `capture_only`. The only alternative is to archive the note as unreconciled.
   - `--publishers-paused` also asserts a single publisher, which is the opposite of joining.

## Outcome sought

- **Joining:** a device is picked up after it commits `devices/<uuid>/clio.jsonl`, at each peer's next scheduled run, with no command run on any peer.
- **The note:** any device holding the converged replica can register the existing fleet-rendered note and publish it, without pausing or removing another publisher.

## Smallest viable bet

Extend the existing helper (`utils/CLIO/clio-store.py`), its docs (`utils/CLIO/INSTALL.md`) and its existing test file (`test/clio-store.py`).

1. **`configure-fleet --discover-origins`** (opt-in, persisted as `fleet['discover']=True`).
   - With the flag set, `--origin` becomes optional and the store's own owner is always included. Explicit `--origin` values remain a pinned list: if one of them has no committed snapshot, it still reports `missing`, which keeps that behaviour unchanged.
   - Without the flag, behaviour is byte-identical to today, so existing configs keep working unchanged.
2. **Discovery in `reconcile_fleet`** when `fleet.get('discover')`:
   - After pinning HEAD, run one bounded read: `git_read(checkout, ['ls-tree', '-r', '-z', '--name-only', head, '--', 'devices'], deadline)`.
   - Keep only paths matching `devices/<canonical-uuid>/clio.jsonl` that pass `valid_origin`. Non-UUID device folders (Pulse's own `devices/<name>/…`) are ignored.
   - Union the result with the configured origins, sorted and deduplicated.
   - Apply the existing 16-origin bound to the union. Exceeding it raises `ValueError`, which follows the existing partial/error path.
   - Every discovered origin goes through the same `import_snapshot` validation as a configured one: digest, owner matching its path, cumulative regression check, size bound, and refusal to self-import.
   - Status gains `discovered: [uuid…]` so the result shows which origins arrived through discovery.
   - Trust boundary: write access to the private sync repo, the same boundary that already admits configured origins' snapshot content.
3. **`migrate-view --join-fleet-note`** (mutually exclusive with `--publishers-paused` and `--archive-unreconciled-note`).
   - Requires an activated store with a fleet configured. Reconcile should run first so the replica holds the records.
   - The note must contain exactly one standalone `<!-- CLIO:ENTRIES -->` marker. The header is the text through that marker line.
   - Every `clio:record` ID in the note must be known locally. If any is unknown, refuse with `ValueError('note holds records not yet in this replica; reconcile after the next delivery and retry')`.
   - The note must be byte-reproducible by `render_markdown` at its own `UTC cutoff`, with that header and one of the two recognised coverage banners.
   - On success, register the view exactly as today: private verified backup, `accepted_hashes`, the matched `coverage`, and `legacy_entries: None`.
   - Factor the existing peer-reproduction check out of `checked_view` into one helper, `peer_render_coverage(known, original, header)`, which returns the coverage or `None`. `checked_view` and `migrate_view` both call it, so there is no second copy of the check.
   - After joining, the operator reruns `configure-fleet … --repair-generated-note`, exactly as INSTALL.md already describes. `scheduled-export` then publishes, because `capture_only and not view` becomes false. `scheduled-export` itself does not change.
4. **Docs.**
   - In INSTALL.md's device-independent section, add a short "Join without touching other Macs" procedure: init/activate, `configure-fleet --discover-origins`, collector delivery, `reconcile-fleet`, `migrate-view --join-fleet-note`, then `configure-fleet --discover-origins --repair-generated-note`.
   - Add a one-time upgrade note: each existing device runs `configure-fleet --discover-origins` once, and that is the last per-peer step.
   - Retirement needs no peer change. A device that stops delivering just stops changing, and its committed snapshot stays as history. Imports never delete rows, so there is nothing to retire.

## Non-goals

- **No change to Rebalance, the collector or `export-device`.** Rebalance owns delivery, and it already exports only the store's own origin.
- **No lease, publisher election, heartbeat, staleness alarm or retirement marker.** The existing peer-render acceptance plus the bounded wait already make concurrent publishers converge.
- **No change to the 16-origin bound, snapshot format, record identity or note renderer.**
- **No adopt-origin/exclude-origin work** (#10), no tailer reconciliation, and no capture filter changes.
- **No auto-discovery by default.** It is opt-in per device, so an existing config cannot start importing new origins without the operator choosing it.

## Alternatives rejected

- **Pulse-wide inventory file edited by hand:** it moves the N×N edit into one shared file, but still needs a human per join, and adds a second writer to the sync repo.
- **Make capture-only devices publish without registering the note:** this skips the header, backup and hash protections that `checked_view` relies on.
- **`--archive-unreconciled-note` on each joining device:** it works today, but it labels a fully reconciled note as unreconciled and archives the whole note for no reason.

## Risks and rollback

- **Risk: a stray or hostile UUID folder is imported.** It is contained by the existing snapshot validation, and the sync repo is private with write-restricted access, the same as today.
- **Risk: a junk folder pushes the union past 16 origins.** Reconcile goes partial, and capture and compatibility output continue. Remove the folder, or pin origins and turn discovery off.
- **Risk: two publishers rewrite the note every cycle.** That is the existing peer design: each accepts the other's render as `peer_generated` and does not archive it.
- **Rollback:** rerun `configure-fleet` without `--discover-origins`, which restores an explicit list. A joined view can be dropped by restoring the pre-change `clio-storage.json` backup, which returns the device to `capture_only`. No data migration is needed, and existing rows are untouched.

## Tests (bounded)

Extend `test/clio-store.py` with one method, `test_fleet_discovery_and_peer_note_join`. It reuses the existing bare-remote fixture pattern with three stores and throwaway HOMEs.

1. **Discovery off is a red control.** Node A has an explicit list `[A, B]`. Node C commits a snapshot. Reconcile on A does not import C.
2. **Discovery on.** A runs `configure_fleet(discover=True)` with no origins. After reconcile, C is `accepted` and listed in `discovered`, with no step on any other node.
3. **Non-UUID entries are ignored.** A committed `devices/fixture-name/clio.jsonl` and `devices/fixture.yaml` produce no origin entry.
4. **A bad discovered snapshot is isolated.** C's snapshot is corrupted and committed. C reports `error`, and A and B still report `accepted`.
5. **Pinned missing.** An explicitly pinned origin with no snapshot still reports `missing` when discovery is on.
6. **Joining the note:**
   - B is capture-only; A publishes the note.
   - Join refuses when the fleet is not configured.
   - Join refuses when the note holds a record B lacks. That is the red control, set up before B reconciles.
   - Join refuses after a body edit.
   - After reconcile, join succeeds and records the matching coverage.
   - After `configure_fleet(repair=True)`, `scheduled-export` on B reports `note_publication: published`.
   - A then accepts B's render as `peer_generated` with no new archive.
7. **Flag rules.** `--join-fleet-note` together with `--publishers-paused` is refused.

Run all five README suites once on the final commit in a disposable full clone with throwaway HOME. Record the results under `TESTS-RESULTS/2026-10-24-gh11/`.

## Ordered implementation, with verification

1. Factor `peer_render_coverage` out of `checked_view`. Verify: `python3 test/clio-store.py` stays green, including the existing `peer_generated` assertions.
2. Add `discover` to `configure_fleet` and the CLI (`--origin` no longer `required=True`; the function validates). Verify with the focused test cases 1, 2 and 5.
3. Add discovery to `reconcile_fleet`. Verify with cases 2–5.
4. Add `join_fleet_note` to `migrate_view` and the CLI. Verify with cases 6–7.
5. Update INSTALL.md. Verify the FRONTDOOR deterministic checks print nothing new, and that the heredoc markers are intact.
6. **Smoke test.** Use a disposable HOME and a local bare remote, driving the real CLI.
   - Main path: a new device commits its snapshot, and an existing discover-enabled device picks it up through `reconcile-fleet` with no config change.
   - Adjacent path: rerun reconcile, which adds nothing new, then join the note on a capture-only device and run `scheduled-export` twice.
   - Record the results under `TESTS-RESULTS/2026-10-24-gh11/smoke.md`.

## Rating (no RELEASES ledger in this repo; recorded here)

`rated 55/40/50/60` (pri/sev/appeal/effort), 2026-10-24.

- **Severity 40:** no data loss. Capture and replicas continue, but one device's prompts are kept out of the shared note until a manual step happens on an unreachable machine. The blocked work is visibility, not capture.
- **Priority 55:** it blocks rolling out the remaining three Macs (tracked in the private rollout tracker), and every join repeats the cost.
- **Appeal 50:** neutral. The operator asked for the issue, but gave no score.
- **Effort 60:** about 150 lines of helper code plus one test method and docs, all on existing seams.
- **Recurrence:** in the last 14 days, 1 incident (2026-10-24), with 0 in the 14 days before. The fleet had one publisher until now, so the trend is unknown.
