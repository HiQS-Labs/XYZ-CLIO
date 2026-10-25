# GH-11 verification: fleet discovery and peer note join

All data is synthetic, run in a disposable full clone of the task branch at `4b2b7d765ccfe93686bf89e42074c8d0dbf44133`. No installed runtime, fleet checkout or note was touched. `provenance.jsonl` records each command, its exit code, the environment notes and the SHA-256 of the files under test.

## Suites (README list)

| Suite | Result |
|---|---|
| `test/clio-capture.sh` | PASS with `CLIO_MIN_PROMPT_CHARS` unset. It fails only when the operator's session value (20) leaks in; the suite does not isolate that variable. That is an environment artifact, not a code defect. |
| `test/clio-exporter.sh` | PASS |
| `test/clio-codex-tail.sh` | PASS |
| `test/clio-agy-tail.sh` | PASS |
| `test/clio-store.py` | 16 of 17 pass, including the new `test_fleet_discovery_and_peer_note_join`. The one failure, `test_activation_import_gate_and_source_preservation` (expected 5 rows, got 4), **also fails on base `d17e521`**. Its fixture rows dated 2026-09-29 have aged out of the 168-hour window, so the failure depends on today's date and predates this change. |

**Red control:** the new test fails against the base helper (`TypeError: configure_fleet() got an unexpected keyword argument 'discover'`). Within the test, each refusal is checked by its message: discovery off, unknown IDs, body edit, and both forbidden flag pairs.

## Smoke test (real CLI, throwaway HOMEs, local bare remote): `smoke.sh` / `smoke.log`

- **Main path:** a new device delivers its snapshot, and a discover-enabled publisher's `reconcile-fleet` accepts it (`added 1`) with **no configuration change**.
- **Adjacent path 1:** rerunning reconcile adds 0 and is not partial.
- **Adjacent path 2:** the publisher renders, then the capture-only device runs `reconcile-fleet`, `migrate-view --join-fleet-note` (registered) and `configure-fleet --discover-origins --repair-generated-note`. It then runs `scheduled-export` twice: both runs report `published` with 0 pending, and the note holds both devices' records.
- **Adjacent path 3:** joining again reports `already_registered`.

Verdict: PASS.
