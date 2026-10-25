# RELAY · gh16-plan-codex
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-25.
-->

NEXT: Producer
STATUS: Open
ROUND: 2 / 3

## ▶ TAKE YOUR TURN — read this first (works for ANY agent: Claude, Codex, agy)
1. **Read this whole file** (header, Setup, Ground rules, every block in the Log).
2. **Check it's your turn:** `NEXT` (top) names the role to act. Confirm you are bound to it and the
   last Log block isn't already yours. If not → STOP and reply "wrong window — nudge the <other> window."
3. **Do your role's work** on the artifact named in Setup:
   - **Reviewer:** review vs the Definition of Done → graded findings
     (`[Blocker]`/`[Should]`/`[Nit]`/`[Pass]`), each with a concrete fix → set a **VERDICT**
     (exactly PASS, FAIL, or PARKED) and a **Basis** (explanation). **Review the whole file, not just the diff** (GH-268):
     a beta test had this loop reach `Approved` in two rounds while an independent audit of the same
     branch found 20 issues (1 critical, 4 high) — every one of them in the pre-existing code the
     change sat on, which nobody had read. Pre-existing defects in a file you are touching are IN
     SCOPE; if you find none, say so explicitly rather than leaving it unstated.
     **Declare it: every review block must contain a literal `swept file: yes` or `swept file: no`
     line.** Without it a reviewer that skipped the sweep is indistinguishable in the transcript from
     one that did it and found nothing — which is how the original 20 issues stayed invisible.
     Any `[Pass]` or "verified"/"confirmed" finding MUST
     carry a quoted span or a `file:line` citation — an uncited one is mechanically downgraded to
     `[Unverified — no citation]` (GH-173 B3). Do **not** edit the artifact; only append findings here.
     **A finding that asks for a behaviour change is a generalization unless you can paste the concrete
     input — a row, a value, a `file:line` — that fails under the current code** (GH-681: the gh673
     final QA relay generalized one late-error observation into "or a later invalid identity", the
     Producer implemented it, the same seat `[Pass]`ed it next round, and one historical NULL-URL
     ledger row then blanked every issue). Every `[Blocker]` or `[Should]` requesting a behaviour
     change MUST carry three lines: `Observed input:` (the failing input you saw), `Affected scope:`
     (the input predicate the change would govern), `Falsifier:` (the fixture or data that would show
     the change unnecessary or wrong, and its expected result).
     A `[Blocker]` must cite an observed failure. This is a protocol rule, not a mechanical check —
     the Producer may disposition a request lacking these as `Declined — unproven generalization`.
   - **Producer:** log a disposition for every open finding (Implemented / Modified / Declined + why,
     including `Declined — unproven generalization` for a behaviour-change request that carries no
     `Observed input:` / `Affected scope:` / `Falsifier:`), make the change, then add new work.
4. **Append ONE block** at the very bottom, directly **above** the marker line. Never edit earlier turns.
   Reviewer headings may be `### Reviewer · Round N`, `### Round N · Reviewer · <agent>`, `### Reviewer (<agent>)` (optionally followed by `— rN`), or `### Reviewer — Round N` (optionally followed by `(<agent>)`); follow the heading with a non-empty review body.
5. **Update the header:** flip `NEXT`; set `STATUS` (`Approved` closes — Reviewer only; else `Open`);
   the Producer bumps `ROUND` when opening a new cycle. If the max `ROUND` ends without `Approved`,
   set `STATUS: Escalated`.
6. **Commit only the relay file** (`relay(gh16-plan-codex): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: `doc/gh16-plan.md` (plan only; no code written yet)
- Source to read for grounding: `utils/CLIO/` (the published files), `test/clio-*`, `test/fixtures/clio/`, `README.md` (layout ~L95-113, Tests ~L118-126), `AGENTS.md`, `FRONTDOOR.md` (Health table), `.gitignore`, and the PR #15 receipt-script guard at `TESTS-RESULTS/2026-10-24-gh13/README.md` (end).
- Requirements (issue #16, operator decision D): an intentional publisher here pointing rebalanceOS → XYZ-CLIO; a record of the published revision (`utils/CLIO/UPSTREAM`); a read-only `--check` that flags direct edits here; maintainer notes so people see the direction; the first publish after rebalanceOS #363 proves an empty CLIO content diff. Never push (AGENTS.md: no Git push loop here).
- Operational envelope: one operator, about four Macs, one designated publisher machine; bash + coreutils + rsync + git; no CI in this repo. Grade against commensurate complexity: no signing, no CI, no lockfiles or registries.
- Reviewer: codex   ·   Producer: claude-a
- Started: 2026-10-25
- Definition of Done: the design meets every requirement with the least machinery, the published set is complete and safe (nothing outside it touched; Rebalance-only README/LICENSE excluded), the refusals are correct, `--check` really detects direct edits, the checks are falsifiable with red controls, and the rollback is adequate. Answer explicitly:
  1. Is the published set right (utils/CLIO minus README/LICENSE/UPSTREAM, `test/clio-*`, `test/fixtures/clio/`)? Is mirror-with-delete inside those scopes safe?
  2. Are the source checks (origin is HiQS-Labs/rebalanceOS, clean tree, HEAD merged into a freshly fetched `origin/development`) and the target checks (not `main`, clean tree) sufficient and not excessive?
  3. Does the `UPSTREAM` manifest plus `--check` catch content edits, deletions and stray additions? Is leaving out mode tracking acceptable?
  4. Is the "no changes, no commit on rerun; revision line updates only when the source moved" rule sound?
  5. Do the notes in AGENTS/README/FRONTDOOR make the direction visible without a second README?
  6. Are verification checks a–i sufficient, especially i (local bare repo stand-in for the origin), and is any check missing?
  7. Anything over-engineered?

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

### Reviewer · Round 1

swept file: yes

- [Should] Reconcile the origin admission rule with verification i. The plan says only HTTPS/SSH origins are accepted (`doc/gh16-plan.md:40`), but i requires the source origin to be the local bare path `<tmp>/HiQS-Labs/rebalanceOS.git` (`doc/gh16-plan.md:96`); that required full-path control is refused if the former rule is implemented literally. Observed input: `origin=<tmp>/HiQS-Labs/rebalanceOS.git` in check i. Affected scope: source-origin validation for every preview/apply. Falsifier: a disposable source with that exact local bare origin; preview must reach its rsync listing (exit 0), while a similarly shaped non-`HiQS-Labs/rebalanceOS.git` origin must still refuse (exit 2). Fix: specify an exact allow-list that admits canonical GitHub HTTPS/SSH URLs and the test-only local suffix, or revise i to use a testable canonical URL without weakening provenance.
- [Should] Make the rerun rule leave no target worktree modification. `--apply` writes `published: <YYYY-MM-DD>` (`doc/gh16-plan.md:56-64`), yet the same-source rerun promises “no changes, no commit” (`doc/gh16-plan.md:49`, `95`) without saying that it skips/restores the date-only rewrite. Observed input: an already-published revision rerun on the following calendar day. Affected scope: `--apply` when manifest hashes and revision equal the recorded values. Falsifier: after that rerun, `git diff --exit-code` and `test -z "$(git status --porcelain)"` both succeed; a changed source revision still creates a revision-line commit. Fix: compare before writing and do not rewrite a date-only manifest (or restore it before exit), and record those clean-worktree assertions in h.
- [Should] Add falsifiable parity controls for deletion and all three published scopes. The stated `--check` contract detects missing entries (`doc/gh16-plan.md:52-54`), but verification only edits `utils/CLIO/INSTALL.md` and adds `utils/CLIO/extra.sh` (`doc/gh16-plan.md:93-94`), so it cannot demonstrate deletion handling or enumeration of `test/clio-*` and `test/fixtures/clio/`. Observed input: removal of listed `test/fixtures/clio/agy-transcript.jsonl`, plus stray `test/clio-extra.sh` and `test/fixtures/clio/extra.jsonl`. Affected scope: manifest comparison/enumeration across all three published scopes. Falsifier: each case, run separately with the other paths restored, exits 1 and names its altered path; each restoration returns exit 0. Fix: add these red controls (a content edit can remain in `utils/CLIO`) to the disposable-clone receipt.
- [Pass] The intended set explicitly excludes the upstream-only README/LICENSE and the locally generated `UPSTREAM`, while limiting delete behavior to the three named scopes (`doc/gh16-plan.md:31-36`, `76-83`); that is proportionate and avoids a second CLIO README. Mode tracking is deliberately excluded with a stated Git-review rationale (`doc/gh16-plan.md:76-80`). No other pre-existing defect found in the reviewed plan.
- Probe record: `find utils/CLIO test/fixtures/clio -type f -exec stat -f '%HT %Mp%Lp %N' {} \\; ; find test -maxdepth 1 -type f -name 'clio-*' -exec stat -f '%HT %Mp%Lp %N' {} \\;` (exit 0) listed exactly 5 `utils/CLIO` content files, 5 `test/clio-*` files, and 2 fixture files; `sed -n '1,320p' doc/gh16-plan.md` (exit 0) read the entire 98-line artifact. No executable fixtures or suites were run.

VERDICT: FAIL

Basis: The plan has the right minimal shape, but the specified local-origin integration control is internally inconsistent, and two required `--check`/rerun properties are not yet falsifiably verified.

handing off to Producer — go to the Producer window and say 'take your turn'

### Producer · Round 1

- [Should] origin rule vs check i → **Implemented**: a single allow-list regex `(^|[/:])HiQS-Labs/rebalanceOS(\.git)?$` admits the GitHub https/ssh forms and the local bare stand-in, and refuses other names and owners. New check a2 covers the refusals.
- [Should] rerun must leave the tree clean → **Implemented**: the manifest is compared in memory, ignoring `published:`. With the same bytes and revision, `UPSTREAM` is not rewritten, nothing is committed, and `git status --porcelain` is empty. Check h now forces a later date (test-only `CLIO_PUBLISH_DATE`) and asserts a clean tree. A moved revision still rewrites and commits.
- [Should] three-scope deletion/stray controls → **Implemented** in check g: a stray in each scope plus a deleted fixture, each exit 1 naming the path, restored back to exit 0.

### Reviewer · Round 2

swept file: yes

- [Should] Restrict remote provenance while retaining the local integration stand-in. The proposed suffix regex accepts a non-GitHub remote, despite the source requirement being the HiQS-Labs upstream. Observed input: `https://attacker.invalid/HiQS-Labs/rebalanceOS.git`; the exact probe `for u in 'git@github.com:HiQS-Labs/rebalanceOS.git' 'https://github.com/HiQS-Labs/rebalanceOS.git' 'https://attacker.invalid/HiQS-Labs/rebalanceOS.git' '/tmp/HiQS-Labs/rebalanceOS.git'; do [[ "$u" =~ (^|[/:])HiQS-Labs/rebalanceOS(\.git)?$ ]] && printf 'ACCEPT %s\n' "$u" || printf 'REFUSE %s\n' "$u"; done` (exit 0; output saved under `.relay-scratch/tmp/origin-regex-probe.txt`) decisively printed `ACCEPT https://attacker.invalid/HiQS-Labs/rebalanceOS.git`. Affected scope: every preview/apply source-origin admission. Falsifier: canonical GitHub HTTPS/SSH URLs and the test-only absolute local bare path `<tmp>/HiQS-Labs/rebalanceOS.git` must still reach the fetch; the attacker-host URL must refuse with exit 2. Fix: describe separate canonical GitHub URL forms and an explicitly local filesystem-path exception, then add the attacker-host negative control alongside a2. (`doc/gh16-plan.md:40`, `doc/gh16-plan.md:100-101`.)
- [Should] Prove the exclude rules survive both mirror and staging. The plan identifies `utils/CLIO/README.md` and `utils/CLIO/LICENSE` as upstream-only, while applying `rsync --delete` through unspecified include/exclude filters and staging the published scopes; current check d only asserts the resulting commit contains `UPSTREAM`. Observed input: source paths `utils/CLIO/README.md` and `utils/CLIO/LICENSE`, named as rebalance-only in `doc/gh16-plan.md:22`; the target's present `utils/CLIO` listing contains only `INSTALL.md`, `clio-agy-tail.sh`, `clio-codex-tail.sh`, `clio-store.py`, and `prompt-log-to-md.sh` (probe: `find utils/CLIO -maxdepth 1 -type f -exec basename {} \\;`, exit 0). Affected scope: rsync filters and `git add` selection for `utils/CLIO/`. Falsifier: after the first apply from a source containing both excluded files, both target paths remain absent, the commit changes only `utils/CLIO/UPSTREAM`, and `git status --porcelain` is empty; a normal listed file still mirrors and is committed. Fix: specify that staging consumes the same generated published-file list as rsync/manifest, and add this excluded-path control to d (including clean-worktree assertion).
- [Pass] The manifest comparison covers content differences, missing listed files, and unlisted additions, and g now provides separate red controls for each published scope plus a deletion. (`doc/gh16-plan.md:31-36`, `doc/gh16-plan.md:52-54`, `doc/gh16-plan.md:94-98`.)
- [Pass] The in-memory same-revision comparison and forced-later-date clean-tree control resolve the date-only rerun issue without adding machinery. (`doc/gh16-plan.md:49`, `doc/gh16-plan.md:99`.)

VERDICT: FAIL

Basis: The plan remains minimal and the prior check/manifest gaps are resolved, but it still admits a remote that is not the named upstream and lacks a falsifiable proof that upstream-only files cannot leak through mirroring or staging. No other pre-existing defect found in the swept plan.

handing off to Producer — go to the Producer window and say 'take your turn'

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
