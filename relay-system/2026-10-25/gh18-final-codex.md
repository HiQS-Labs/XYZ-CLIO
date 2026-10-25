# RELAY · gh18-final-codex
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-25.
-->

NEXT: Producer
STATUS: Approved
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
6. **Commit only the relay file** (`relay(gh18-final-codex): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: this branch. It renames the published folder to `utils/clio-capture` and points `scripts/publish-from-rebalance.sh` at it (commit eab43bc), with README/AGENTS/FRONTDOOR updates, then publishes from rebalanceOS (commit ac499fc). You cannot run git: `.relay-artifacts/gh18.diff` is `git diff -M origin/main...HEAD` (renames shown as renames).
- Evidence: `TESTS-RESULTS/2026-10-25-gh18/` (preview, apply, --check, rerun, byte parity, suites).
- Requirements (issue #18): follow the upstream rename (HiQS-Labs/rebalanceOS#364); the publisher's source/target scope and `UPSTREAM` path use `utils/clio-capture`; README/LICENSE stay excluded; this repo's own references are updated (history left alone); the published content equals rebalanceOS byte for byte and `--check` passes; `test/clio-runtime.sh` is listed in the README Tests block and passes.
- Operational envelope: a mechanical path move plus one publish, on a one-operator repo with no CI. Grade against the requirements; do not ask for new machinery.
- Reviewer: codex   ·   Producer: claude-a
- Started: 2026-10-25
- Definition of Done: every live reference and the publisher scope use the new path; history (`doc/`, `TESTS-RESULTS/`, `relay-system/`, `SHAKEDOWN/`, FRONTDOOR's fixed-finding rows) is unchanged; the publish commit contains only upstream bytes plus `UPSTREAM`; and the evidence substantiates --check, parity and the suites. Answer explicitly:
  1. Does any live file still use `utils/CLIO`, or did the rename touch history it should not?
  2. Is the publisher correct for the new path in all three modes (published_files, irregular, rsync scope, staging, the `UPSTREAM` record)?
  3. Are the README layout, Tests block and FRONTDOOR checks accurate for the new files (SKILL.md, clio-runtime.sh, UPSTREAM, test/clio-runtime.sh)?
  4. Does the receipt substantiate byte parity and the suites?

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

- [Pass] No live legacy path remains: the scratch-scoped probe `rg -n --glob '!doc/**' --glob '!TESTS-RESULTS/**' --glob '!relay-system/**' --glob '!SHAKEDOWN/**' 'utils/CLIO' .` exited 0 and returned only FRONTDOOR's two fixed-finding history rows (`FRONTDOOR.md:33-34`). `utils/CLIO` is absent; the current layout and README test command use `utils/clio-capture` at `README.md:96-115` and `README.md:129-142`.
- [Pass] The publisher consistently scopes its manifest, irregular-file guard, archive, three rsync destinations, record, and staging to the renamed path (`scripts/publish-from-rebalance.sh:14-32`, `scripts/publish-from-rebalance.sh:70-85`, `scripts/publish-from-rebalance.sh:101-114`). Narrow syntax probe `bash -n scripts/publish-from-rebalance.sh` exited 0.
- [Pass] The local published set matches the record: scratch probe `published manifest SHA-256 compared with UPSTREAM` exited 0 with `entries=15`; the record names the new path at `utils/clio-capture/UPSTREAM:1-20`.
- [Pass] The receipt substantiates parity and the required runtime harness: it records `bash test/clio-runtime.sh -> exit 0` and `differences: 0` at `TESTS-RESULTS/2026-10-25-gh18/suites.txt:2-11`; the README also lists the runtime test at `README.md:140`. The same receipt transparently notes the pre-existing date-dependent `clio-store.py` failure at `TESTS-RESULTS/2026-10-25-gh18/README.md:12`, so it is not being misrepresented as a clean all-suite run.
- [Pass] Full touched-file sweep found no pre-existing defect within the files changed by this artifact that blocks the mechanical rename; the new runtime test uses a throwaway HOME and stubbed launchctl as declared in `test/clio-runtime.sh:1-35`, and the published skill describes the deployed-copy-only boundary at `utils/clio-capture/SKILL.md:8-17`.

VERDICT: PASS

Basis: The rename is complete outside explicitly preserved history, publisher modes and receipt now use `utils/clio-capture`, README accurately lists the new layout/runtime test, and the evidence plus a current manifest probe substantiate the published bytes. No blocker or should-fix finding.

relay closed (Approved), no further turn needed.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
