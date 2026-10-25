# RELAY · gh16-final-codex
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-25.
-->

NEXT: Producer
STATUS: Open
ROUND: 1 / 3

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
6. **Commit only the relay file** (`relay(gh16-final-codex): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: `scripts/publish-from-rebalance.sh`, `utils/CLIO/UPSTREAM` (first publish), the notes in `AGENTS.md`, `README.md` and `FRONTDOOR.md`, and the receipt `TESTS-RESULTS/2026-10-25-gh16/`. You cannot run git: `.relay-artifacts/gh16-impl.diff` is the full diff from the plan-approval head `a23f96a` to HEAD.
- Approved plan: `doc/gh16-plan.md` (plan QA `relay-system/2026-10-25/gh16-plan-codex.md`, Approved R3).
- Operational envelope: one operator, one publisher machine, no CI; bash + git + rsync + shasum. Grade against the approved plan and commensurate complexity.
- Reviewer: codex   ·   Producer: claude-a
- Started: 2026-10-25
- Definition of Done: the script implements the approved design (published set, refusals, archive-sourced bytes, staging from the same list, clean-tree assertion, rerun rule, `--check` semantics, no push), the receipt substantiates every check a–i with red controls, the first publish proves an empty CLIO content diff, and the notes make the direction visible. Answer explicitly:
  1. Does the script match the plan line by line? Note the two implementation deviations found by the checks: `rsync -rlp` instead of `-a`, and preview filtered to transfers, deletions and permission changes. Are they correct, and do they hide any real change (for example a deletion or a mode-only change)?
  2. Is any path able to stage or commit something outside the published set, or leave the tree dirty without failing?
  3. Is `--check` correct for edits, deletions and strays in all three scopes (including the `join`/`diff` reporting)? Any false pass, for example a filename containing spaces?
  4. Are the guarded temp dirs (`EXP`, the receipt's `W`) safe against an empty `mktemp` result?
  5. Do AGENTS/README/FRONTDOOR state the direction accurately without a second README?
  6. Anything missing or over-engineered?

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

- [Should] `--check` detects a changed whitespace-containing filename through the whole-manifest `diff`, but its required changed-path report truncates it at the first space. `scripts/publish-from-rebalance.sh:35` uses whitespace-field `join`/`awk`, although the manifest path is the entire suffix after the two-space hash delimiter. Observed probe (exit 0): `old=000…001  test/fixtures/clio/a b.jsonl`, `new=000…002  test/fixtures/clio/a b.jsonl`; the exact line-35 pipeline printed `changed: test/fixtures/clio/a`, not the real path. Fix the changed-record comparison to preserve the full path suffix (rather than whitespace splitting) and add this red control to the disposable-clone receipt.
  Observed input: two manifest records for `test/fixtures/clio/a b.jsonl` with distinct 64-hex checksums (probe command: `join -j 2 <(sort -k2 old) <(sort -k2 new) | awk '$2 != $3 {print "  changed: " $1}'`; exit 0; decisive output: `changed: test/fixtures/clio/a`).
  Affected scope: any published pathname containing whitespace whose bytes differ from `UPSTREAM`.
  Falsifier: a clone check that changes `test/fixtures/clio/a b.jsonl` must exit 1 and report the complete literal pathname; a corrected report means this finding is unnecessary.

- [Should] A symlink stray in a published scope has a false-clean `--check`: `published_files` admits only `-type f` (`scripts/publish-from-rebalance.sh:19-21`), so it neither appears in the recomputed manifest nor is called `not published`; meanwhile `sync` explicitly preserves links with `-l` (`scripts/publish-from-rebalance.sh:65-68`). Reject non-regular entries in every published scope (both source and target) or otherwise account for them consistently, and add a symlink red control.
  Observed input: a target-only `test/fixtures/clio/stray-link -> /dev/null` alongside an unchanged manifest.
  Affected scope: symlinks in `utils/CLIO/`, top-level `test/clio-*`, or `test/fixtures/clio/`.
  Falsifier: with that lone stray link present, `--check` must exit 1 and name it; if current code does so, the finding is wrong. Narrow probe: `find "$TMPDIR/symlink-probe/test/fixtures/clio" -type f -exec basename {} \;` returned `regular-files=<>; find_exit=0; symlink_test=0`, proving the exact `-type f` predicate omits the extant link.

- [Pass] The direction is stated consistently without a second local README: `AGENTS.md:3`, `README.md:12-14`, and `FRONTDOOR.md:26` identify rebalanceOS as upstream and point maintainers to the publisher/check. The diff’s receipt also records the required clean first publish (`TESTS-RESULTS/2026-10-25-gh16/first-publish.txt:2-13`). I swept the complete changed script and all changed documentation/receipt files; apart from the two findings above, no pre-existing defect was found in those touched files. The receipt’s executable-clone claims were not rerun here, per relay containment rules.

VERDICT: FAIL

Basis: The core design, guarded temp directories (`scripts/publish-from-rebalance.sh:56-57`; `TESTS-RESULTS/2026-10-25-gh16/publisher-checks.sh:5-6`), filtered preview, and documented first-publish evidence are aligned with the plan, but `--check` does not yet meet its all-path/all-stray reporting contract for whitespace names and symlinks.

Handing off to Producer — go to the Producer window and say 'take your turn'.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
