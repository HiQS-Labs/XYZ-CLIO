# CLIO engineering contract

- **Upstream is rebalanceOS.** `utils/clio-capture/` and the CLIO tests (`test/clio-*`, `test/fixtures/clio/`) are published from HiQS-Labs/rebalanceOS `utils/clio-capture/` by `scripts/publish-from-rebalance.sh`, recorded in `utils/clio-capture/UPSTREAM`. Never edit them here. Change them in rebalanceOS first through a reviewed PR, then publish on a branch and open a PR here. `bash scripts/publish-from-rebalance.sh --check` runs with the suites and flags a direct edit.
- `utils/clio-capture/INSTALL.md` owns the shared capture writer and installation procedure; tests extract its heredocs. Preserve that single capture boundary.
- Apply SOLID proportionally: focused functions and existing seams, without speculative abstractions or extra services. Prefer Python's standard library for SQLite work.
- Preserve private prompt history, unknown metadata and tailer retry/cursor semantics. Never publish live prompts, databases, snapshots or credentials in this repository.
- Storage migration work follows `doc/gh3-plan.md` and issue #3. A reviewed PR is not permission to modify installed hooks, source history or launchd jobs.
- Run capture/exporter/Codex/Agy suites listed in README in an isolated full clone. Use synthetic data and throwaway HOME; record failed/skipped checks honestly.
- Automated reviews use the `relay-xyz` skill; run its locator first and keep reviewer writes limited to the relay thread. Do not substitute self-review for a required relay.
- Keep scope on CLIO. Rebalance owns downstream search and fleet publication; XYZ owns task status. No second ledger writer, vector store or Git push loop here.
