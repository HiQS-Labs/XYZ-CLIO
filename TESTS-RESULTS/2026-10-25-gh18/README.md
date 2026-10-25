# GH-18 verification (2026-10-25)

This follows the upstream rename (HiQS-Labs/rebalanceOS#364, merged in PR #365 as `918244a`). Commits: `eab43bc`, the rename here plus the publisher scope and doc references; `ac499fc`, the publish from rebalanceOS `f10764f`.

| Check | Result | Evidence |
|---|---|---|
| Preview before publish | lists only INSTALL.md, the new SKILL.md and clio-runtime.sh, the CLIO tests' path updates and the new `test/clio-runtime.sh` | `preview.txt` |
| `--apply` | commits exactly those plus `UPSTREAM`; clean tree afterwards | `apply.txt` |
| `--check` | exit 0, 15 files | `apply.txt`, `suites.txt` |
| Rerun `--apply` | "no changes", no commit | `apply.txt` |
| Byte parity of `utils/clio-capture` (minus README/LICENSE) and `test/clio-*` vs rebalanceOS | 0 differences | `suites.txt` |
| README suites (disposable clone, `/bin/bash` 3.2) | `clio-runtime`, capture, exporter, codex-tail, agy-tail pass; `clio-store.py` 1 known date-dependent failure (also upstream) | `suites.txt` |
| Live `utils/CLIO` references | none outside history (`doc/`, `TESTS-RESULTS/`, `relay-system/`, `SHAKEDOWN/`) and FRONTDOOR's two fixed-finding history rows | grep in the session |

Plan QA was skipped as a simple change: a mechanical path rename and publisher scope update with no design decision. Final Codex QA follows.
