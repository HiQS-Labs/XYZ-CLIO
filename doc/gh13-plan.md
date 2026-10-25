# GH-13 plan: reconcile tailer and writer drift from the Rebalance copy

Issue: https://github.com/HiQS-Labs/XYZ-CLIO/issues/13. Base: `origin/main` d17e521. Clone/branch: `XYZ-CLIO-gh13-reconcile-tailer-drift-2026-10-24` / `fix/<same>`.
Rating (recorded on the issue; this repo has no RELEASES ledger): `rated 72/75/50/80`.

## Context
This is the last change authored directly in XYZ-CLIO (operator decision D, noelsaw1/noels-cross-project-tasks#52). Next, Rebalance's `utils/CLIO` is synced up to this revision and becomes upstream, and XYZ-CLIO becomes a published downstream. So every fix that exists only in Rebalance must land here first, or the sync would erase it.

## Recon (Rebalance `origin/development` vs XYZ-CLIO `origin/main`, `utils/CLIO`)
- XYZ-CLIO is ahead everywhere else: `clio-store.py`, SQLite hooks in the writer and exporter, `source_event_id`, the read-only Agy DB open, and the scheduled export. Rebalance lacks all of it; 0b brings it over.
- Rebalance-only changes, and what this plan does with each:

| # | Change (Rebalance) | Files | Disposition |
|---|---|---|---|
| 1 | Reap a tailer lock older than 300 s (from `born`, falling back to the dir mtime) | both tailers | **Port** |
| 2 | Idle tick at EOF skips `state_update` when nothing changed | both tailers | **Port, reworked**: Rebalance's Codex check compares `cached_since` with itself (always equal). Compare the full would-be record with the stored one instead. |
| 3 | Strip Codex IDE context, keeping the text after `## My request:` | Codex tailer | **Port, narrowed**: only when the prompt starts with `# Context from my IDE setup:`; accept `## My request:` and `## My request for Codex:` (both appear in real rollouts); skip if empty. Rebalance strips any prompt containing the marker, which would truncate a real prompt that quotes it. |
| 4 | Writer default `CLIO_MIN_PROMPT_CHARS` 100 → 20 | INSTALL.md writer heredoc and its docs line | **Port** (operator decision C, 2026-10-24) |
| – | Dropped the `not session_id` / non-string guard; `IFS=$'\t' read` of the state line | Codex tailer | **Reject**: tab is IFS whitespace, so an empty sid field shifts cwd and eligibility. |
| – | Dropped `source_event_id`; read-write Agy DB open; removed the SQLite branches | both tailers, exporter, writer | **Reject** (Rebalance is just behind) |
| – | Rebalance's own `README.md`/`LICENSE` under `utils/CLIO` | – | Out of scope; 0b decides (this repo keeps them at the root). |
| – | Writer header comment `Legacy contract (SQLite mode returns nonzero …)` → `Contract:` | INSTALL.md writer | **Reject**: it would drop the SQLite receipt caveat while this branch keeps SQLite mode. |

- Separate finding: current Codex no longer writes `event_msg/user_message`, so Codex capture is silent. Filed as #14; it is to be authored upstream in Rebalance after the flip and is **not** part of this change.

## Changes (surgical; no new files except this plan and a TESTS-RESULTS receipt)
1. `utils/CLIO/clio-agy-tail.sh`, `utils/CLIO/clio-codex-tail.sh`: replace `mkdir "$TAIL_LOCK" 2>/dev/null || exit 0` with the same reaper block in both. Reaping is serialized behind an atomic `mkdir "$TAIL_LOCK.reap"`, and the age is re-checked after acquiring it, so a contender that saw the old lock can never delete a lock another contender just took (plan QA R2):
   ```bash
   lock_stale() { # the held lock is older than 300 s (born stamp, else dir mtime); empty/non-numeric = not stale
     born=$(cat "$TAIL_LOCK/born" 2>/dev/null || stat -f %m "$TAIL_LOCK" 2>/dev/null || stat -c %Y "$TAIL_LOCK" 2>/dev/null || echo "")
     case "$born" in ''|*[!0-9]*) return 1 ;; esac
     [ $(( $(date +%s) - born )) -gt 300 ]
   }
   if ! mkdir "$TAIL_LOCK" 2>/dev/null; then
     lock_stale || exit 0
     mkdir "$TAIL_LOCK.reap" 2>/dev/null || exit 0          # one reaper at a time
     lock_stale && { rm -rf "$TAIL_LOCK"; diag "reaped stale tail lock born at $born"; }
     mkdir "$TAIL_LOCK" 2>/dev/null; got=$?
     rmdir "$TAIL_LOCK.reap"
     [ "$got" = 0 ] || exit 0
   fi
   ```
   Residual (accepted): only SIGKILL inside the millisecond reap section leaves `.reap` behind. That disables reaping, not normal locking, so it degrades to today's behaviour and a diag-free `rmdir` clears it.
   Update the header `overlap =` comment to mention the 300 s reap.
2. Idle write (Agy): `[ "$cached" = "$inode $offset" ] || state_update …`. (Codex): build the would-be record `inode\toffset\tsid\tcwd\teligibility` with the same tab sanitizing `state_update` uses, and write only if it differs from `$cached`. A legacy 5-field row (empty eligibility) is therefore rewritten once as `legacy`, then stays stable.
3. Codex `extract_rows`: after the timestamp and `since` checks, when `text.lstrip().startswith("# Context from my IDE setup:")`, take the text after the first line-anchored `## My request( for Codex)?:` header, strip it, and `continue` if it is empty. Keep `source_event_id` on the original line.
4. `test/clio-capture.sh` `skips_short_prompt` boundary case: move the pinned boundary from 100/99 to 20/19 characters. This edits an existing case, not a new suite; it is the only existing assertion of the old default (it fails against the draft until updated, and a draft run proved it).
5. INSTALL.md: the writer default becomes `${CLIO_MIN_PROMPT_CHARS:-20}`, the docs line says default **20**, and short-prompt examples stay valid (`yes`/`push it` are still dropped).

## Non-goals
- No Codex format fix (#14), no Rebalance edits (0b), no publisher (0c), no installer.
- No new suites (repo contract: extend existing suites only if an acceptance check cannot be shown manually; this plan uses manual checks).
- Reaper race: R1 declined it as outside launchd's cadence. R2 showed it with a two-process interleaving on the manual-invocation surface, so it is now **Implemented** as the `.reap` handoff in change 1 (a rename-to-quarantine alone would not close it).
- No PID-liveness lock protocol. The age rule matches Rebalance's production behaviour; overlap after a reap is tolerated because the writer's ID suppression and the shared append lock prevent duplicate rows.

## Risks / rollback
- A tailer that legitimately runs over 300 s (a big backfill) could have its lock reaped by the next tick. Impact: two tailers on the same files; duplicate rows are suppressed by the writer's ID check, and the cursor converges. Accepted (same as the Rebalance devices running today).
- Rollback: revert the PR; nothing is installed by merging (AGENTS.md: a PR is not permission to touch installed hooks).

## Verification (isolated full clone, throwaway HOME, synthetic data)
- Existing suites: `bash test/clio-capture.sh`, `bash test/clio-exporter.sh`, `bash test/clio-codex-tail.sh`, `bash test/clio-agy-tail.sh`, `python3 test/clio-store.py`, all run with `CLIO_MIN_PROMPT_CHARS` unset.
- Manual checks, recorded under `TESTS-RESULTS/2026-10-24-gh13/`:
  - a. Lock with `born` = now−600: the tailer reaps it, captures a pending row, and leaves a diag line. **Red control:** the base revision exits 0 and captures nothing.
  - b. Lock with `born` = now: silent no-op, lock untouched.
  - b2. Lock dir with no `born` file and mtime set 10 min back: reaped, falling back to the dir mtime. **Red control:** the base revision makes no capture.
  - b4. Concurrent reapers (plan QA R2 falsifier): the R2 barrier probe, run against the exact `lock_stale` + `.reap` block (A and B both pass the first `lock_stale`, then race). Expected: exactly one `reaped` line, and the final `$TAIL_LOCK/born` belongs to the winner. **Red control:** the same probe against the unserialized `rm -rf; mkdir` block shows B deleting A's lock (R2 output `fresh-lock-owner=B`).
  - b3. Lock with an empty or non-numeric `born` (`abc`): silent no-op, lock untouched (fail-safe; the dir mtime is not consulted after a successful read).
  - c. Two idle ticks: state file bytes and mtime unchanged after the second. **Red control:** the base revision changes the mtime.
  - d. A Codex `user_message` with the IDE context and `## My request for Codex:` → stored prompt is only the request. A prompt that merely quotes `## My request:` with no IDE header → stored unchanged. An IDE prompt with an empty request → no row.
  - e. A 30-character prompt via the hook with the env unset → captured. `push it` → dropped.
- Smoke: run the installed-shape tailers (Codex and Agy) from a throwaway HOME twice (main path + rerun).
