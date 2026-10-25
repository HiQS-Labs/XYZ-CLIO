# RELAY · gh13-plan-codex
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-24.
-->

NEXT: Closed
STATUS: Approved
ROUND: 3 / 3

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

### Producer · Round 1

- [Blocker] reaper race → **Declined — outside the envelope (no observed input)**. Tailers run as launchd `StartInterval` jobs, and launchd does not start a second instance of a job while the first is running, so "two launchd invocations both fail `mkdir`" cannot occur. Two contenders need a manual run overlapping launchd. Your probe is sequential (one shell runs both reaps), not an interleaving of two tailers. The proposed rename-to-quarantine leaves the same window: if the loser's `mv` comes after the winner's `mkdir`, it renames the fresh lock. Residual risk recorded under Non-goals in `doc/gh13-plan.md`.
- [Should] reaper branch coverage → **Implemented**: manual checks b2 (no `born`, stale dir mtime → reap, with a base red control) and b3 (empty or non-numeric `born` → no-op).
- [Should] writer-comment row → **Implemented**: the table row is added as Reject.
- Producer addition: change 4 moves the existing `skips_short_prompt` 100/99 boundary case to 20/19. A draft run in a disposable clone showed it is the only suite assertion that breaks under the default-20 port. (`test/clio-store.py` `test_activation_import_gate_and_source_preservation` also fails on the base revision d17e521; it is date-dependent and pre-existing, unrelated.)

### Reviewer · Round 2

swept file: yes

- [Blocker] The raw `rm -rf "$TAIL_LOCK"; mkdir "$TAIL_LOCK"` reaper remains unsafe against concurrent direct invocations. The producer's launchd assumption does not make the advertised lock operation safe for the documented/manual invocation surface, and the earlier disposition incorrectly says there was no observed input. Probe command: `zsh -c 'p="$1/reaper-race"; rm -rf "$p"; mkdir -p "$p/ready"; mkdir "$p/lock"; print 1 > "$p/lock/born"; reaper() { tag=$1; [ "$(cat "$p/lock/born")" -lt 2 ] || exit 4; : > "$p/ready/$tag"; while [ ! -f "$p/go" ]; do sleep 0.01; done; if [ "$tag" = A ]; then rm -rf "$p/lock"; mkdir "$p/lock"; print A > "$p/lock/born"; else sleep 0.05; rm -rf "$p/lock"; mkdir "$p/lock"; print B > "$p/lock/born"; fi; }; reaper A & a=$!; reaper B & b=$!; while [ ! -f "$p/ready/A" ] || [ ! -f "$p/ready/B" ]; do sleep 0.01; done; : > "$p/go"; wait "$a"; aa=$?; wait "$b"; bb=$?; print "a=$aa b=$bb fresh-lock-owner=$(cat "$p/lock/born")"' zsh "$TMPDIR"`; exit status: `0`; decisive output: `a=0 b=0 fresh-lock-owner=B`. This exacts the failure: B deletes A's new lock. Replace the unguarded deletion with a mutually exclusive reaper handoff that serializes stale-lock decisions and rechecks `born` after acquiring that handoff; keep the short critical section/trap cleanup and cover its recovery behavior. A fixed quarantine rename alone is insufficient, as the producer correctly notes.
  Observed input: two concurrent direct tailer invocations both fail `mkdir "$TAIL_LOCK"` while its numeric `born` is older than 300 seconds.
  Affected scope: every stale-lock recovery path in both tailers when an operator/manual invocation overlaps a scheduled invocation or another direct run.
  Falsifier: an interleaved two-contender manual check against the revised reaper where both initially see the stale lock, only one owns the recovery handoff, and after both exit its new `$TAIL_LOCK/born` is still owned by that winner; expected result: no contender deletes a newly acquired lock.
- [Pass] The reconciliation table now covers every behavior-changing hunk in the supplied diff: reaper/idle changes, Agy read-write DB and `source_event_id` removals, Codex guard/IDE/IFS/state changes, writer SQLite removal/comment/default, plus the README/LICENSE addition ([plan L15-L22](../../doc/gh13-plan.md#L15-L22); [diff L9-L22](../../doc/gh13-rebalance-drift.diff#L9-L22), [L28-L70](../../doc/gh13-rebalance-drift.diff#L28-L70), [L81-L160](../../doc/gh13-rebalance-drift.diff#L81-L160), [L168-L224](../../doc/gh13-rebalance-drift.diff#L168-L224)). No additional pre-existing plan defects were found in the full-file sweep.
- [Pass] The plan correctly rejects `IFS=$'\\t' read`: with the concrete empty-middle-field record `9<TAB>123<TAB><TAB>/work<TAB>legacy`, `read` produces `sid=/work cwd=legacy eligibility=` rather than preserving the empty sid. Probe command: `zsh -c 'row=$'"'"'9\\t123\\t\\t/work\\tlegacy'"'"'; IFS=$'"'"'\\t'"'"' read -r inode offset sid cwd eligibility <<< "$row"; print -r -- "inode=$inode offset=$offset sid=${sid:-<empty>} cwd=$cwd eligibility=$eligibility"'`; exit status: `0`; decisive output: `inode=9 offset=123 sid=/work cwd=legacy eligibility=`. The stated reject rationale is therefore correct ([plan L19](../../doc/gh13-plan.md#L19); [diff L139-L146](../../doc/gh13-rebalance-drift.diff#L139-L146)).
- [Pass] Apart from the reaper race, the planned idle comparison, narrowed/anchored IDE stripping, macOS/Linux `stat` fallback with fail-safe nonnumeric `born`, 300-second threshold, and 20/19 existing capture boundary are proportionate and correctly specified ([plan L30-L41](../../doc/gh13-plan.md#L30-L41), [L54-L63](../../doc/gh13-plan.md#L54-L63)).

VERDICT: FAIL

Basis: The complete drift ledger and all non-reaper ports meet the Definition of Done, but the direct concurrent-reaper case deletes a fresh lock under the plan's exact remove/recreate sequence. The plan cannot be Approved until it has a bounded serialized recovery scheme and a falsifiable interleaving control.

Handing off to Producer — go to the Producer window and say 'take your turn'.

### Producer · Round 2

- [Blocker] concurrent reaper → **Implemented**. Your barrier probe is a genuine two-process interleaving on the manual/direct invocation surface, so my R1 "no observed input" disposition was wrong. Change 1 now serializes reaping behind an atomic `mkdir "$TAIL_LOCK.reap"` and re-checks `lock_stale` after acquiring it. A loser either fails the `.reap` mkdir (exit 0), or acquires it after the winner and sees a fresh `born`/mtime (no reap). The `.reap` is removed before the tailer proceeds. Residual: a SIGKILL inside the reap section only disables reaping (today's behaviour). Falsifier added as manual check b4, with your R2 output as the red control.
- [Unverified — no citation] items acknowledged.

### Reviewer · Round 3

swept file: yes

- [Pass] The R2 revision closes the observed reaper race without adding a PID/lease protocol: `mkdir "$TAIL_LOCK.reap"` is the atomic recovery handoff, and the winner re-runs `lock_stale` before the sole destructive removal; a loser either cannot create `.reap` or sees the new lock as fresh ([plan L27-L43](../../doc/gh13-plan.md#L27-L43)). The 300-second rule is proportionate to the one-minute schedule and intentionally retains the existing tolerated-overlap policy ([plan L53-L57](../../doc/gh13-plan.md#L53-L57)). The fallback is correct on macOS and Linux: a failed `cat` tries `stat -f` then `stat -c`, while a successfully read empty/non-numeric `born` fails closed rather than falling through ([plan L29-L32](../../doc/gh13-plan.md#L29-L32), [L65-L67](../../doc/gh13-plan.md#L65-L67)).
- [Pass] The planned EOF writes are byte-identity checks rather than Rebalance's insufficient field checks: Agy compares its exact two-field record, and Codex constructs the fully tab-sanitized record that `state_update` would write. This rewrites a five-field legacy Codex record once, preserves reset behavior, and then avoids idle rewrites ([plan L45-L45](../../doc/gh13-plan.md#L45-L45); [source state writer L64-L74](../../utils/CLIO/clio-codex-tail.sh#L64-L74); [source reset L204-L224](../../utils/CLIO/clio-codex-tail.sh#L204-L224)).
- [Pass] IDE stripping is intentionally limited to messages beginning with the IDE preamble and a line-anchored request header, retains `source_event_id` from the original source line, and skips an empty request; the planned controls also retain a non-IDE prompt that quotes the marker ([plan L17-L17](../../doc/gh13-plan.md#L17-L17), [L46-L46](../../doc/gh13-plan.md#L46-L46), [L69-L70](../../doc/gh13-plan.md#L69-L70)).
- [Pass] The table accounts for every behavioral diff hunk, including the writer-contract comment, and correctly rejects the whitespace-IFS state parser because it shifts the empty-middle-field legacy row ([plan L15-L22](../../doc/gh13-plan.md#L15-L22); [diff L139-L146](../../doc/gh13-rebalance-drift.diff#L139-L146)). The default-20 port updates both the writer and docs while preserving `push it` as below threshold, and moves the existing inclusive boundary to 20/19 ([plan L47-L48](../../doc/gh13-plan.md#L47-L48), [L68-L70](../../doc/gh13-plan.md#L68-L70)).
- [Pass] The verification matrix has positive cases and red controls for stale `born`, missing-`born` mtime fallback, fail-safe malformed `born`, the formerly failing concurrent reaper sequence, idle mtime, IDE forms, and the default boundary; rollback is an ordinary PR revert with no installed-hook mutation ([plan L60-L71](../../doc/gh13-plan.md#L60-L71), [L56-L58](../../doc/gh13-plan.md#L56-L58)). No additional pre-existing plan defects were found in the full-file sweep.

VERDICT: PASS

Basis: The reaper’s concrete two-process failure is now serialized and revalidated, and the complete drift ledger, bounded ports, falsifiable controls, and rollback meet the Definition of Done. No fixture suite was run in this relay turn; the specified isolated-clone gate remains the implementation-stage verification.

Relay closed (Approved), no further turn needed.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
