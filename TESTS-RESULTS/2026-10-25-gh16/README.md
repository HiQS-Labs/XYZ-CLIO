# GH-16 verification (2026-10-25)

Publisher: `scripts/publish-from-rebalance.sh`. The checks ran against task-branch revision `8b94fa4` (the commit before the first publish). Source: rebalanceOS `development` `e4a7abb`, which includes the merged #363.

`publisher-checks.sh` builds disposable clones in a guarded temp dir: a target copy of the task branch, plus a source cloned from a local bare repo at `<tmp>/HiQS-Labs/rebalanceOS.git`, so the origin check and the fetch run for real. Output: `checks-out.txt`.

| Check | Result |
|---|---|
| a. dirty source | refused, exit 2 |
| a2. fork, other-owner and foreign-host origins | each refused, exit 2 |
| b. source HEAD not merged into origin/development | refused, exit 2 |
| c. `--apply` on `main` | refused, exit 2 |
| d. source has README/LICENSE; preview → apply | "no CLIO content changes"; commit = `utils/CLIO/UPSTREAM` only; README/LICENSE absent here; clean tree |
| e. `--check` | exit 0, 12 files |
| f. one-byte edit to INSTALL.md (red control) | exit 1, `changed: utils/CLIO/INSTALL.md` |
| g. stray in each of the three scopes, and a deleted fixture | each exit 1 naming the path; each restore exit 0 |
| h. rerun with a later forced date | "no changes", no commit, clean tree |
| i. real upstream change via the local bare repo | preview lists only that fixture; apply commits fixture + UPSTREAM; `--check` 0; upstream revert → bytes restored |
| README suites | capture, exporter, codex-tail, agy-tail pass; clio-store.py 1 known date-dependent failure (also on base) |

Two preview defects were found and fixed during these runs:
- `rsync -a` itemized mtime-only differences, so preview listed unchanged files. Now `-rlp` is used, and preview shows only transfers, deletions and permission changes.
- The first run of check d would have printed "codex-rollout.jsonl" for a no-op.

**First real publish** (`first-publish.txt`): preview "no CLIO content changes"; `--apply` commit `publish: CLIO from HiQS-Labs/rebalanceOS@e4a7abb9218b` changes only `utils/CLIO/UPSTREAM`; clean tree; `--check` exit 0. This is the 0c proof that rebalanceOS and XYZ-CLIO hold identical CLIO bytes.
