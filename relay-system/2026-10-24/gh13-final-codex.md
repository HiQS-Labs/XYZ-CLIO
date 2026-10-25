# RELAY · gh13-final-codex
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-24.
-->

NEXT: Reviewer
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
6. **Commit only the relay file** (`relay(gh13-final-codex): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: the implementation in `utils/CLIO/clio-agy-tail.sh`, `utils/CLIO/clio-codex-tail.sh`, `utils/CLIO/INSTALL.md` (writer default and docs line), `test/clio-capture.sh` (`boundary_is_inclusive`). Exact diff vs base `d17e521`: `doc/gh13-implementation.diff` (you cannot run git; read this file and the current files).
- Approved plan: `doc/gh13-plan.md` (plan QA thread `relay-system/2026-10-24/gh13-plan-codex.md`, Approved R3). Drift evidence: `doc/gh13-rebalance-drift.diff`.
- Test evidence: `TESTS-RESULTS/2026-10-24-gh13/README.md` and the files beside it (suites, manual checks a–e with base red controls, b4 concurrent-reaper probe, smoke).
- Requirements (issue #13): port the Rebalance-only fixes (serialized stale-lock reaper, no idle state rewrite, Codex IDE-context stripping, writer default 20) without importing Rebalance's regressions.
- Operational envelope: a personal fleet of about four Macs; launchd minute cadence; bash + stdlib python. Grade against the approved plan and commensurate complexity; no new suites (AGENTS.md); do not ask for PID or lease protocols.
- Reviewer: codex   ·   Producer: claude-a
- Started: 2026-10-24
- Definition of Done: the code matches the approved plan line for line (or each deviation is justified), each acceptance check in the receipt substantiates its claim with a red control, no Rebalance regression slipped in, no new suite or registry entry, and nothing outside scope changed. Answer explicitly:
  1. Does the reaper in both tailers match plan change 1 exactly (`lock_stale` re-check after `.reap`, `.reap` removed on both outcomes, `born` set by the existing post-lock line)? Any path that leaves `.reap` behind besides SIGKILL? Is `set -e` interaction safe (`lock_stale` returning nonzero inside `&&`/`||`, the `got=0; mkdir … || got=1` form)?
  2. Do the idle comparisons skip only byte-identical records (Agy `"$inode $offset"`, Codex sanitized 5-field record)?
  3. Is `IDE_REQUEST` (`^## My request(?: for Codex)?:[ \t]*\n?`, re.M, first split) correct for both real forms, and is `source_event_id` still computed from the original line?
  4. Are the default-20 changes complete (writer, docs line, boundary test) with no other place asserting 100?
  5. Does the receipt substantiate each claim (including the harness-naming note), and are the deviations it records (test case name) acceptable?

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

- [Pass] The reaper matches the approved serialized/rechecked shape in both tailers: `utils/CLIO/clio-agy-tail.sh:43-57` and `utils/CLIO/clio-codex-tail.sh:53-67` re-check after acquiring `.reap`, remove it after the attempted reacquire, and set `born` after lock acquisition. The permitted static probe `bash -n utils/CLIO/clio-agy-tail.sh; bash -n utils/CLIO/clio-codex-tail.sh` exited 0 for both; receipt `TESTS-RESULTS/2026-10-24-gh13/b4-head.txt` reports `30/30` single-reap/single-owner for each tailer.
- [Pass] Idle writes compare exactly the intended records: Agy `utils/CLIO/clio-agy-tail.sh:197-200` compares `"$inode $offset"`; Codex `utils/CLIO/clio-codex-tail.sh:251-256` builds the sanitized five-field TSV. Receipt `TESTS-RESULTS/2026-10-24-gh13/mc-head.txt` records unchanged mtime and SHA for both, while `mc-base.txt` shows rewritten mtimes.
- [Pass] IDE handling is correctly gated and preserves the original source-line hash: `utils/CLIO/clio-codex-tail.sh:104,183-198`. The permitted regex probe exited 0 and split both supported headers while retaining an inline quoted marker; the receipt's `d-ide` rows in `mc-head.txt` corroborate both real forms and the quoted-marker control.
- [Should] `utils/CLIO/INSTALL.md:700-705` still tells operators that an abandoned tailer lock needs manual recovery and that this update adds no lock supervisor. That is now false for the planned >300-second stale-lock reaper. Replace it with the actual 300-second reap behavior (including the accepted SIGKILL `.reap` residual if documenting it) so the installed operational guidance does not instruct needless recovery.
- [Should] The explicit default-20 sweep is incomplete: `test/clio-capture.sh:28` says the minimum is one hundred characters, and `utils/CLIO/INSTALL.md:282` says the capture threshold is one hundred characters. Change these descriptions to 20 (or neutral wording). This is required by the plan/DoD's “no other place asserting 100”; the actual writer and boundary assertion are correct at `utils/CLIO/INSTALL.md:78` and `test/clio-capture.sh:92-98`.
- [Should] The Agy delivery-contract header does not receive plan change 1's overlap note: compare `utils/CLIO/clio-agy-tail.sh:14-18` with the updated Codex contract at `utils/CLIO/clio-codex-tail.sh:29-31`. Add that a lock older than 300 seconds is reaped by one serialized reaper, as the approved plan explicitly requires.

VERDICT: FAIL

Basis: The behavioral implementation and receipt are sufficient, but the three cited documentation/contract omissions leave the artifact short of the approved plan and Definition of Done. No other pre-existing defects were found in the swept artifacts.

### Producer · Round 1

- [Should] INSTALL.md stale-lock guidance → **Implemented**: the "requires operator recovery … no lock supervisor" sentence now describes the 300 s serialized reap and the SIGKILL `.reap` residual.
- [Should] remaining "one hundred" threshold wording → **Implemented**: the INSTALL.md smoke-test prompt and `test/clio-capture.sh` `long_prompt` now say twenty. Left as-is: `test/clio-capture.sh:114` and `test/clio-agy-tail.sh:89` are fixture prompt text describing their own length (still true, and still above 20), not threshold assertions.
- [Should] Agy contract header → **Implemented**: added the busy-lock and 300 s reap lines.
- Refreshed `doc/gh13-implementation.diff` to `a7f9184`. Reran the affected suites at `a7f9184` (capture, codex-tail, agy-tail: exit 0), appended to `TESTS-RESULTS/2026-10-24-gh13/suites.txt`. No behaviour change, so the manual checks stand.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
