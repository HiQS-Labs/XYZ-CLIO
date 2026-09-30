# RELAY · CLIO GH3 same-path plan QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-09-30.
-->

NEXT: codex
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
6. **Commit only the relay file** (`relay(clio-gh3-same-path-plan-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-same-path-plan.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: author
- Started: 2026-09-30

### Artifact — gh3-same-path-plan.md
```
# GH3 revision: same Obsidian destination and schedule

Status: plan review pending. Base e1edb8399dc0 on existing feat/gh3-sqlite-history / PR4. User explicitly requires the same Obsidian path, filename and schedule, and authorized updating this branch. Supersedes the earlier separate-final-note design. Rating78/65/50/35 unchanged; no new incident/appeal evidence. Private installed state remains out of scope for branch implementation.

## Grounded recon (reuse existing map, bounded delta)
Existing doc/recon-gh3.md covers this subsystem; no external dependency landed since its trace. Graph list_projects now returns Transport closed; source fallback used, no freshness claim. Read current store, exporter, installer and tests. INSTALL.md:517–550 writes com.claude.prompt-log-to-md.plist with script + output positional argument and StartInterval60. Exporter:35–60 parses the unchanged positional path, defaults ~/.claude/prompt-log.md, then uses legacy append semantics. Its header contract at :380 preserves everything through standalone CLIO:ENTRIES; entries are legacy clio:id marker, repo heading, display time, device/branch/agent metadata, quoted multiline prompt. Store:470 guards historical targets for ALL exports; :488 publishes a fresh rolling file, :388 config activates capture only. The safe seam is a narrow authorized migration plus schedule adapter, not removing guards. Consumers of the legacy MD format (Rebalance journey) remain separately tracked; same path alone is not a claim of unchanged entry syntax.

## Design / scope
Extend the same stdlib helper and exporter. Add `migrate-view [--markdown PATH] --publishers-paused` after capture activation/import. Discover existing output from the documented launchd plist (script/path arguments; no shell evaluation); when no plist exists accept the explicit existing cron/manual path or the legacy default. Refuse ambiguous/unsupported installed arguments instead of choosing a new note. Never write the plist: existing interval, label, argument path and logs stay byte-identical. If explicit and detected paths disagree, refuse. This command registers the SAME destination, not a new rolling file.

Before registering: require activated matching DB and nonempty original note; require one standalone historical marker; preserve the exact header through that marker. Parse only the known legacy entry shape and match each entry against DB legacy_id plus full prompt/repo/device/branch/agent display metadata (timestamp display is not identity). Refuse unknown body content, malformed or missing entries and conflicting legacy aliases; don't guess from IDs alone. Header-only note is allowed as an explicitly empty existing view if DB exists. All original note bytes receive an exclusive private backup plus SHA256 verification, including header and old history. Existing imported raw JSONL and SQLite remain unchanged. No lossy Markdown importer; missing foreign history must be imported through existing JSONL/device snapshot paths before cutover.

Store a small `view` receipt in existing private clio-storage.json: resolved path, exact header, backup path/digest, accepted original/latest output hashes. Shared maintenance lock serializes migration/projection. Register only after backup verification and source unchanged check. `migrate-view` does not replace the note; the next invocation of the existing job does, or invoke that same exporter manually. Re-running migration for an already registered same path reports its receipt rather than overwriting backup.

`project` uses the registered destination by default. Explicit --markdown remains available for scratch preview, never becomes an implicit substitute final destination. Historical-guard exception is ONLY for Markdown at the registered path with matching activated DB/owner and verified backup/current bytes. JSONL/device exports still cannot replace that note or its backup. Header is prepended verbatim to rolling body, keeping vault links/path intact. Direct edits/unexpected foreign writes after registration fail closed with a diagnostic; they are not silently discarded. Register updated accepted old/new hashes atomically BEFORE replacing note so failure/crash leaves an allowed old or new file; a retry converges. No hash update on an unrelated preview. Existing atomic replacement preserves prior bytes on write failure. This is local single-publisher discipline, not distributed compare-and-swap.

The shell exporter parses existing CLI first. For normal export with activated SQLite config, call helper's scheduled-export path using the SAME OUT argument; require the registered path match, drain receipts then project there plus existing full-history compatibility JSONL. Unregistered activation produces a clear migration-required failure, never writes a new recent note behind the user's back. Legacy --status/repair/backfill on a migrated target must refuse with appropriate SQLite guidance rather than modify rolling content; legacy mode remains unchanged without config. Explicit --sqlite routes through registered project default; no installed schedule rewrite.

`--publishers-paused` is the operator's assertion of a documented prerequisite, not remote verification: pause all old/shared MD writers, import all devices, designate this one publisher, then resume only its existing job. Current #282 remains fleet deployment dependency. Full coverage of the existing note is measured; complete live fleet coverage is not inferable from a local DB. Cross-device late writes change the hash and stop publication. No new sync loop/service/vector store/ledger writer.

## Ordered implementation and evidence
1. Approve this revised plan in a fresh bounded Codex relay (max3). Retain older approvals as historical only.
2. Implement destination discovery, legacy note coverage, exclusive verified backup and view receipt; test actual synthetic plist with spaces/custom path remains byte-identical, ambiguous path refused, foreign/missing entry and same-ID wrong-device/prompt refuse without modifying note/config, header preserved.  [Unverified — no citation]
3. Route unchanged installed exporter invocation into the registered rolling projection; test existing positional job and default job path, no new timer/path, 168h expiry with old data still in SQLite, old markers/user header retained, explicit --sqlite behavior, unknown edits/refusal, backup protection and unsupported maintenance verbs. Keep phase2 entry-format consumer work explicit.
4. Witness red controls: new same-path scheduled test fails on old implementation; injected publication failure keeps original bytes and retry converges; altered backup/missing coverage blocks. Verify original note/backup and expected all-device recent entries, not just successful exit. Extend existing storage suite only; no framework/new suite.
5. Focused checks during iteration; final Codex relay (max3), then one complete five-suite gate on revised approved implementation. Refresh FRONTDOOR and issue/PR body to final behavior and results. No automatic merge or installed migration.

## Risk / rollback
Costly only at installed cutover. This branch work uses synthetic temporary HOME. Header/user content above marker is preserved; unrecognized edits below it block migration, not discarded. Stop writers before rollback; preserve SQLite-era arrivals via full JSONL export and DB backup, then restore verified original note path/config and reconcile full-history legacy export before resuming legacy writers. Restoring the old note alone is not a data rollback. Existing note backup alone is not evidence every fleet record is in SQLite; explicit coverage gate checks originals. Filename/path compatibility does not preserve expired entry anchors or promise old Markdown entry parsers understand new records; external parser migration remains tracked.  [Unverified — no citation]
```
- Definition of Done: Review the bounded same-path plan against user requirement and cited sources; concrete failures/falsifiers only. Local single-publisher utility; no speculative distributed framework. Scope store/exporter/installer and existing tests. Only write this thread.

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

### Reviewer · Round 1
VERDICT: PASS
Basis: The bounded plan meets the same destination/filename/schedule requirement while retaining an explicit, coverage-gated cutover. Approval is for the plan, not implementation or installed migration.
swept file: yes

- [Pass] Same job and destination: the artifact says “Never write the plist” and “using the SAME OUT argument”; the existing contract is script plus positional destination and StartInterval 60 at utils/CLIO/INSTALL.md:532–538, parsed at utils/CLIO/prompt-log-to-md.sh:35–53. No schedule rewrite or substitute final note is required.
- [Pass] Preservation is explicit: “match each entry against DB legacy_id plus full prompt/repo/device/branch/agent display metadata” and “Refuse unknown body content” cover the actual legacy rendering at utils/CLIO/prompt-log-to-md.sh:510. “Header-only note is allowed” is consistent with the standalone-marker historical guard at utils/CLIO/clio-store.py:482–484. The proposed exception remains Markdown-only; backup protection and current-byte checks are expressly required.
- [Pass] Recovery and scope are proportionate: “Register updated accepted old/new hashes atomically BEFORE replacing note” addresses the two-file publication ordering; “No hash update on an unrelated preview” keeps preview separate. Existing publication uses a maintenance lock and atomic replacement at utils/CLIO/clio-store.py:491 and :527. The artifact explicitly limits the guarantee to a local single publisher and requires stopped writers, source coverage, and preservation of SQLite-era arrivals for rollback.
- [Nit] Make the installer documentation refresh explicit in implementation step 5. utils/CLIO/INSTALL.md:369–375 currently instructs changing ProgramArguments and choosing a new Markdown path, which this revision supersedes. Replace that pilot guidance with pause/import/migrate-view/resume instructions that retain the existing plist; preserve the shared capture heredocs. Also correct the recon's activation citation from :388 to utils/CLIO/clio-store.py:396–430. These are documentation follow-through, not a change to the approved design.
- [Unverified — needs clone run] No suites or executable fixtures were run in this reviewer worktree. Same-path dispatch, coverage parsing (including legacy display defaults), failure/retry convergence, expiry, and backup refusal are implementation acceptance criteria, not observed successes. Execute the named red controls and complete five-suite gate in an isolated full clone with synthetic HOME, as the artifact's steps 2–5 require.
- Whole embedded artifact reviewed, including recon, design, implementation evidence and rollback; no additional pre-existing plan defects found. Graph project/generation and coverage could not be queried because no graph tools are exposed in this session; source fallback used without a freshness or exhaustive code-audit claim. Locator command: `bash /Users/noelsaw/.codex/skills/relay-xyz/find-harness.sh --check`, exit 0; decisive output identified the harness and workers, but also reported `driver_lock_path_for_repo: command not found`. No harness edits made.

relay closed (Approved), no further turn needed.

### Producer · Round 2

No production code written. Plan substance unchanged. Previous reviewer set Approved but called tick release before tick done; driver exit4 close-mismatch rejected attestation. This is a failed approval, not usable PASS. Review the unchanged plan/prior findings and append a valid round2 verdict. For Approved, while still owning this new task, call tick done with --agent codex and --relay-file; DO NOT release an approved task before done. If FAIL, release normally. Only this thread writable. Handing off to codex.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
