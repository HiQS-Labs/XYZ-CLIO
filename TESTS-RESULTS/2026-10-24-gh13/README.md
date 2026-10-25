# GH-13 verification (2026-10-24)

Revision under test: `41c65ff` (fix commit), checked out in a disposable full clone (`…-verify`). Red controls run the same scripts against `d17e521` (`origin/main`) extracted with `git archive`. Synthetic fixtures and throwaway HOMEs only; `CLIO_MIN_PROMPT_CHARS` and `CLIO_CONFIG` are unset (legacy JSONL path).

| Check | Result at 41c65ff | Red control at d17e521 | Evidence |
|---|---|---|---|
| Existing suites (capture, exporter, codex-tail, agy-tail) | pass | – | `suites.txt` |
| `test/clio-store.py` | 1 failure, `test_activation_import_gate_and_source_preservation` | same failure (pre-existing, date-dependent) | `suites.txt` |
| a. stale `born` (now−600) | reaped, 2 rows captured | lock stuck, 0 rows | `mc-head.txt` / `mc-base.txt` |
| b. fresh `born` | silent no-op, lock kept | same | ″ |
| b2. no `born`, dir mtime now−600 | reaped via mtime fallback, 2 rows | stuck, 0 rows | ″ |
| b3. `born` = `abc` | silent no-op, lock kept (fail-safe) | same | ″ |
| b4. concurrent reapers (R2 falsifier) | 30/30 one reap + one owner, both tailers | unserialized block 0/30 (both reap, both own; `rm` races are visible) | `b4-head.txt`, `b4-reaper-race-probe.sh` |
| c. idle ticks (Codex, Agy) | state mtime and sha unchanged | mtime rewritten | `mc-*.txt` |
| d. IDE stripping | request only for `## My request for Codex:` and `## My request:`; quoted marker without IDE preamble kept whole; empty request skipped | full IDE context stored | ″ |
| e. default threshold | 29-char prompt captured, `push it` dropped | 29-char prompt dropped | ″ |
| Smoke: main path + rerun, both tailers | 2 + 2 delivered, then 0 + 0; no leftover lock or `.reap` | – | `smoke.txt` |

Harness notes: `manual-checks.sh` is a one-off receipt script, not a registered suite (AGENTS.md / GH-831). The first harness run named rollouts `r.jsonl`, which the tailer ignores (it scans `rollout-*.jsonl`), and gave vacuous Codex results. The recorded runs use correct names. The plan named the boundary case `skips_short_prompt`; the edited case is actually `boundary_is_inclusive` (now 20/19).

**Safety fix after approval (2026-10-25):** an external review found the receipt scripts did not guard their scratch-dir cleanup. If `mktemp -d` failed, `b4-reaper-race-probe.sh` would run `rm -rf "$P"/*` with an empty `$P`, which expands to `rm -rf /*`. Both scripts now exit 1 unless the scratch dir exists, and every cleanup uses `${VAR:?}`. Verified: with an unwritable `TMPDIR` both scripts refuse (exit 1); normal reruns reproduce the recorded results (b4 30/30 on both tailers and 0/30 red; manual checks identical apart from timestamps and hashes). Product code is unchanged. Only the receipt scripts changed, and no deletion happened in the earlier runs (mktemp succeeded each time).
