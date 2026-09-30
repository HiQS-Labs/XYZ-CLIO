# Relay prerequisite environment investigation

The first `bash validate.sh` run inherited `XYZ_HARNESS` and `XYZ_SKILLS_ROOT` from this session. Fixture output directly resolved the user's primary Forge checkout instead of its temporary harness. No Forge source was changed. The first run is invalid as clean-environment evidence and must not be called green.

Root cause of the nine observed fixture failures: inherited harness routing overrides at invocation; fix site: invocation environment; why not source: clearing only these overrides made the same unchanged fixtures pass in a second full clone at identical head34e43dbb. The working trees and HEAD stayed unchanged. Pool contention and source regression were alternative hypotheses; identical failures passed serially with overrides cleared. Isolation affected both concurrency and environment, so the environment explanation is supported by direct wrong-path output, not solely by pass/fail differential.

Clean-environment focused checks returned0: gh448-driver-lock-resolver, gh372-escalation-log-tail, marathon-drive (162passes), gh358-wave-reconcile-vendored-paths, gh429-wave-reconcile-vendored-observe, find-harness, xyz-vendor, gh362-marathon-plan-link-bullets, gh396-find-harness-roots. Codex turn-taker also returned0 (43passes).

A complete clean-environment validate run is pending. No Codex plan review or implementation approval is claimed. The locator itself returns0 when run from the selected isolated harness root; its foreign-CWD warning path in the installed copy had the missing helper error noted in recon.

Complete clean-environment `validate.sh` subsequently returned0 at unchanged34e43dbb with a clean working tree. The initial contaminated run returned1 with12routing-related failures; do not relabel it green. The complete clean run, plus the separately passing43-case Codex turn-taker suite, satisfy preflight for the actual plan relay. Summary and provenance are retained alongside this note.
