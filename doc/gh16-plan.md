# GH-16 plan: publisher from the rebalanceOS upstream, UPSTREAM record, --check

Issue: https://github.com/HiQS-Labs/XYZ-CLIO/issues/16. Base `origin/main` bacd26f. Clone/branch `XYZ-CLIO-gh16-rebalance-publisher-2026-10-25` / `feat/<same>`.
Rating (recorded here; this repo has no RELEASES ledger): `rated 70/45/50/75`, 2026-10-25.
- Priority: the last step before the CLIO installer, which deploys from rebalanceOS and is published here.
- Severity: without it, a direct edit in this repo silently forks the published copy again; that is the drift that #13 had to repair by hand.
- Appeal: neutral.
- Effort: one small script plus doc lines.

## Context
Operator decision D (noelsaw1/noels-cross-project-tasks#52):
1. 0a: reconcile here. Done (#13/#15).
2. 0b: sync rebalanceOS and flip it to upstream. HiQS-Labs/rebalanceOS#362 / PR #363; it must merge before this PR's first publish step.
3. **0c (this task):** an intentional publisher in this repo pointing rebalanceOS → XYZ-CLIO, a record of what was published, a check that flags direct edits here, and maintainer notes.

## Recon
- This repo's CLIO content:
  - `utils/CLIO/{INSTALL.md, clio-agy-tail.sh, clio-codex-tail.sh, clio-store.py, prompt-log-to-md.sh}`;
  - `test/clio-{capture,exporter,codex-tail,agy-tail}.sh`, `test/clio-store.py`, `test/fixtures/clio/{agy-transcript.jsonl, codex-rollout.jsonl}`.

  After #363 every one of these is byte- and mode-identical in rebalanceOS (checksums in rebalanceOS `TESTS-RESULTS/2026-10-25+GH-362/`).
- rebalanceOS-only files under `utils/CLIO`: `README.md`, `LICENSE`. This repo deliberately has one root README/LICENSE and "no second, skill-local README" (README.md L111-113), so the publisher excludes both.
- There is no CI here; the README "Tests" block (README.md ~L118-126) is the gate.
- There is no `scripts/` directory yet.
- AGENTS.md: "No ... Git push loop here." The publisher never pushes or fetches this repo. It reads the source checkout, and fetches only that checkout's `origin development`, to prove the revision is merged.
- `rsync` (macOS `/usr/bin/rsync`) and `shasum` are available; both are standard on macOS and Linux.

## Design (one script, three modes)
`scripts/publish-from-rebalance.sh`

**Published set**, defined once in the script:
- every regular file under `utils/CLIO/` except `README.md`, `LICENSE` and `UPSTREAM`;
- `test/clio-*` files;
- every file under `test/fixtures/clio/`.

Mirror semantics apply within those three scopes: a file removed upstream is removed here. Nothing outside them is touched.

**Preview (default):** `publish-from-rebalance.sh <rebalanceOS checkout>`.
1. Source checks, refusing with exit 2 and the reason:
   - `origin`'s URL matches `(^|[/:])HiQS-Labs/rebalanceOS(\.git)?$`. This one rule admits `https://github.com/HiQS-Labs/rebalanceOS(.git)`, `git@github.com:HiQS-Labs/rebalanceOS(.git)` and a local mirror path ending in `/HiQS-Labs/rebalanceOS.git` (check i's stand-in). Any other repository name or owner is refused (plan QA R1);
   - the working tree is clean (`git status --porcelain` empty);
   - after `git -C <src> fetch -q origin development`, `HEAD` is an ancestor of `origin/development` (merged).
2. Print the source revision and an `rsync --dry-run --itemize-changes --checksum` listing for the three scopes, then "no CLIO content changes" when the listing is empty.

**`--apply`:**
- Target checks: the current branch is not `main`, and the working tree is clean (exit 2 otherwise).
- Run the same rsync for real, preserving modes (`-a --checksum --delete`, scoped with include/exclude filters).
- Write `utils/CLIO/UPSTREAM`, then `git add` the published scopes and commit `publish: CLIO from HiQS-Labs/rebalanceOS@<short>`.
- Rerun rule (plan QA R1): build the new manifest in memory first. If the copied bytes and the new `revision` + manifest lines equal the existing `UPSTREAM` (everything but the `published:` date), the script does **not** rewrite `UPSTREAM`, commits nothing, and leaves the working tree clean (`git status --porcelain` empty). It reports "no changes" and exits 0. A moved source revision rewrites `UPSTREAM`, so the record names what the bytes came from, and that is committed even when no content changed.
- Never pushes.

**`--check` (read-only, no source needed):**
- Recompute sha256 over the published set and compare it with `UPSTREAM`'s manifest. A listed file whose content differs, a listed file that is missing, or an unlisted file in the published set is reported; any of them means exit 1.
- Exit 0 prints `CLIO matches HiQS-Labs/rebalanceOS@<short> (N files)`.

**`utils/CLIO/UPSTREAM` format** (plain text; the manifest lines are `shasum -a 256` output, so a human can also run `shasum -a 256 -c`):
```
# Published from the CLIO upstream. Do not edit utils/CLIO/ or the CLIO tests here:
# change HiQS-Labs/rebalanceOS utils/CLIO first, then run scripts/publish-from-rebalance.sh.
source: HiQS-Labs/rebalanceOS
revision: <full sha>
published: <YYYY-MM-DD>
<sha256>  utils/CLIO/INSTALL.md
...
```

## Changes
1. Add `scripts/publish-from-rebalance.sh` (bash, `set -euo pipefail`, about 80 lines). Every temp dir goes through a guarded `mktemp` (`|| exit`, `${VAR:?}` on cleanup), as PR #15's receipt fix requires.
2. Maintainer notes:
   - `AGENTS.md`: a first bullet saying `utils/CLIO/` and the CLIO tests are published from rebalanceOS, are never edited here, and that `--check` runs with the suites.
   - `README.md`: a short "Upstream" note above `# CLIO`, and `bash scripts/publish-from-rebalance.sh --check` added to the Tests block.
   - `FRONTDOOR.md`: a "Upstream parity" Health row backed by that command.
3. Add a `scripts/` line to the README layout block.
4. **First publish** (after rebalanceOS #363 merges): run `--apply` against a clean rebalanceOS checkout at the merged `origin/development` revision. Expected: the commit adds only `utils/CLIO/UPSTREAM`, and no CLIO byte changes. This is the 0c proof that the two copies match.

## Non-goals
- No push, no CI, no scheduler.
- No mode tracking in `--check`. Git already shows mode changes in review, and content is the drift that matters.
- No publishing of anything outside the three scopes.
- No changes to the CLIO code itself.

## Risks / rollback
- `--delete` inside the scopes could remove a file that was added only here. That is intended: anything there must come from upstream, and preview shows it first.
- Rollback: revert the PR. The script only ever commits on a non-`main` branch, for review.

## Verification
- Manual checks run in a disposable full clone of this repo plus a disposable rebalanceOS clone as the source, with a guarded receipt script:
  - a. A dirty source → refused.
  - b. A source `HEAD` with a local unmerged commit → refused.
  - c. `--apply` on `main` → refused.
  - d. A clean merged source: preview prints "no CLIO content changes", and `--apply` commits only `UPSTREAM`.
  - e. `--check` → exit 0.
  - f. A one-byte edit to `utils/CLIO/INSTALL.md` → `--check` exit 1, naming the file (red control).
  - g. Stray and deleted files, one at a time and restored between runs (plan QA R1). Each of the following gives `--check` exit 1 naming that path, and each restore gives exit 0 again:
    - a stray `utils/CLIO/extra.sh`;
    - a stray `test/clio-extra.sh`;
    - a stray `test/fixtures/clio/extra.jsonl`;
    - a deleted `test/fixtures/clio/agy-transcript.jsonl`.
  - h. A second `--apply` from the same source with the date forced to a later day (`CLIO_PUBLISH_DATE` override, test-only) → "no changes", no new commit, and `git status --porcelain` is empty (rerun path).
  - a2. An origin of `https://github.com/HiQS-Labs/rebalanceOS-fork.git` or `https://github.com/Someone/rebalanceOS.git` → refused (exit 2).
  - i. Upstream change, full path: the disposable source's `origin` is a local bare repo at `<tmp>/HiQS-Labs/rebalanceOS.git`, so the origin check and fetch run for real. Commit a one-line fixture change to its `development`, pull it into the source, preview: exactly that file is listed. `--apply`: one fixture plus `UPSTREAM` committed; `--check` passes. Then revert it in the source and publish again: back to identical bytes.
- The README suites still pass.
- Receipt under `TESTS-RESULTS/2026-10-25-gh16/`.
