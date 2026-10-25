# RELAY · gh13-plan-codex
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-24.
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
6. **Commit only the relay file** (`relay(gh13-plan-codex): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: `doc/gh13-plan.md` (plan only; no code written yet)
- Evidence: `doc/gh13-rebalance-drift.diff` (exact `diff -u` of XYZ-CLIO `origin/main` vs the Rebalance copy for both tailers and the INSTALL.md writer heredoc; the Rebalance repo is not in this clone).
- Source to read for grounding: `utils/CLIO/clio-agy-tail.sh` (lock ~L40-42, `state_lookup`/`state_update` ~L54-70, main loop ~L157-185), `utils/CLIO/clio-codex-tail.sh` (lock ~L48-51, `state_lookup`/`state_update` ~L57-75, `extract_rows` ~L82-180, main loop ~L199-290), `utils/CLIO/INSTALL.md` (writer heredoc ~L52-235, `minchars` L78, docs line ~L815), `test/clio-capture.sh`, `test/clio-codex-tail.sh`, `test/clio-agy-tail.sh`, `AGENTS.md`.
- Requirements (issue #13): port the Rebalance-only fixes (stale-lock reaper, no idle state rewrite, Codex IDE-context stripping, writer default 20) without importing Rebalance's regressions, so the next step can sync Rebalance up to this revision and flip it to upstream with nothing lost.
- Operational envelope: a personal fleet of about four Macs; launchd runs each tailer every minute; bash + stdlib python. Grade against commensurate complexity: do NOT ask for PID-liveness protocols, lease files, new test suites or new services. AGENTS.md forbids new suites unless needed; manual checks are recorded under TESTS-RESULTS.
- Reviewer: codex   ·   Producer: claude-a
- Started: 2026-10-24
- Definition of Done: the plan's drift table is complete and correct against the diff (no Rebalance-only behaviour missed or misclassified), each port is grounded in the cited lines, the rejected items really are regressions, the checks are falsifiable with red controls, and the rollback is adequate. Answer explicitly:
  1. Is any Rebalance-only change in `doc/gh13-rebalance-drift.diff` missing from the table or wrongly dispositioned?
  2. Is the reaper block correct on macOS and Linux (`born` file vs dir mtime, non-numeric `born`, a race with a concurrent reaper)? Is the 300 s threshold acceptable given launchd's 60 s cadence?
  3. Does the idle-write comparison (Agy `"$inode $offset"`, Codex full record vs `$cached`) skip exactly when the stored line would be byte-identical? Any case where a needed write is skipped (legacy 5-field rows, a non-numeric offset reset to 0, tab sanitizing)?
  4. Is narrowing the strip to prompts starting `# Context from my IDE setup:` with a line-anchored `## My request( for Codex)?:` header right, versus Rebalance's unconditional split?
  5. Is the `IFS=$'\t' read` rejection correct (empty middle field)?
  6. Is the default-20 change safe for the existing suites (`skips_short_prompt` uses `push it`)?
  7. Anything over-engineered that should be cut, or any requirement missed?

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

- [Blocker] The proposed reaper still has an unguarded concurrent-reaper race: after both contenders have observed the same stale directory, the second `rm -rf "$TAIL_LOCK"` can delete the first contender's newly acquired lock (plan [L28-L34](../../doc/gh13-plan.md#L28-L34)). Probe command: `zsh -c 'p="$1/reaper-race"; rm -rf "$p"; mkdir "$p"; printf old > "$p/born"; rm -rf "$p"; mkdir "$p"; printf first > "$p/born"; rm -rf "$p"; mkdir "$p"; printf second > "$p/born"; printf "fresh-lock-owner=%s\\n" "$(cat "$p/born")"' zsh "$TMPDIR"`; exit status: `0`; decisive output: `fresh-lock-owner=second`. Replace the destructive handoff with an atomic same-parent rename of the stale directory to a unique quarantine name; only the rename winner removes its quarantine and tries `mkdir`, while a rename loser exits. This retains the accepted long-runner overlap policy without allowing a stale observer to remove a fresh lock.
  Observed input: two launchd invocations both fail `mkdir` against the same lock whose numeric `born` is older than 300 seconds.
  Affected scope: every stale-lock recovery when two minute-cadence invocations reach the reaper block concurrently.
  Falsifier: an interleaved two-contender probe in the clone in which the losing contender's atomic rename fails and the winner's newly created `$TAIL_LOCK/born` remains present; expected result: exactly one reaper owns the replacement lock.
- [Should] The verification plan does not prove the other required reaper branches: it has only old-`born` and current-`born` cases ([L52-L55](../../doc/gh13-plan.md#L52-L55)), while the Definition of Done expressly requires directory-mtime fallback and non-numeric-`born` handling. The empty-`born` branch is intentionally safe (no fallback after a successful empty read): probe command: `zsh -c 'p="$1/reaper-empty"; rm -rf "$p"; mkdir "$p"; : > "$p/born"; touch -t 202601010000 "$p"; born=$(cat "$p/born" 2>/dev/null || stat -f %m "$p" 2>/dev/null || stat -c %Y "$p" 2>/dev/null || echo ""); case "$born" in ""|*[!0-9]*) printf "born=<empty>; decision=no-op\\n";; *) printf "born=%s\\n" "$born";; esac' zsh "$TMPDIR"`; exit status: `0`; decisive output: `born=<empty>; decision=no-op`. Add falsifiable manual cases for a missing `born` plus stale directory mtime (reap), empty/non-numeric `born` (no-op), and the rename race above, with a red control for each where applicable.
- [Should] The drift table omits Rebalance's writer-contract comment change shown in the supplied diff ([`doc/gh13-rebalance-drift.diff:L168-L172`](../../doc/gh13-rebalance-drift.diff#L168-L172)). It is not a port candidate once the plan rejects the SQLite removal, but the stated complete reconciliation table should list it as **Reject — would falsely remove the legacy SQLite receipt caveat while this branch retains SQLite**. Add that explicit disposition to close the evidence ledger.
- [Unverified — no citation] The planned idle-write comparison is appropriately stronger than Rebalance's self-comparison: Agy compares its exact two-field record and Codex compares the tab-sanitized full would-be record, including the one-time legacy eligibility normalization ([L37-L38](../../doc/gh13-plan.md#L37-L38)).
- [Unverified — no citation] IDE stripping is constrained to the IDE preamble and line-anchored request headers, preserving ordinary prompts that quote the marker; the specified manual controls cover both the non-IDE quote and empty-request cases ([L38-L39](../../doc/gh13-plan.md#L38-L39), [L56-L56](../../doc/gh13-plan.md#L56-L56)).

VERDICT: FAIL

Basis: The plan covers the intended ports and the source artifact was swept, with no additional pre-existing plan defects found. However, the reaper race is reproducible by the exact proposed remove/recreate sequence, and the verification/evidence ledger gaps above prevent the Definition of Done from being met.

Handing off to Producer — go to the Producer window and say 'take your turn'.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
