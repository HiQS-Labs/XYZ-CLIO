# Shakedown index

Newest first. One line per run.

- 2026-09-01 16:52 — [clio](2026-09-01/clio-1652.md) — **[path bug reproduced]** — the documented `install -m 0755 utils/CLIO/<script>.sh` commands are CWD-relative and have no referent once CLIO is installed as a skill. **Patch applied** on branch `clio-path-resolution` (`CLIO_SRC` resolver); tracked as FD-01 on [`FRONTDOOR.md`](../FRONTDOOR.md).
