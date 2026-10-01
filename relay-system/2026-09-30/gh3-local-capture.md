# RELAY · CLIO local capture-only final QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-09-30.
-->

NEXT: Reviewer
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
6. **Commit only the relay file** (`relay(gh3-local-capture): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-capture-only-qa.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: author
- Started: 2026-09-30

### Artifact — gh3-capture-only-qa.md
```
Review CLIO local capture-only implementation for authorized MacStudio deployment. Read AGENTS.md, latest operator-scope section at end of doc/gh3-plan.md, complete utils/CLIO/clio-store.py, INSTALL.md capture-only guidance, exporter adapter, existing test/clio-store.py and diff against origin/main. User says collection is final, accepts unrecoverable older historical gap, wants future captures in localSQLite, other Macs installed case by case. Do NOT demand more historical collection or synthesize lost metadata. No private data is available or permitted to this reviewer. Minimal local stdlib CLI, unchanged shared writer/tailers/job/plist; no new store/service/push/ledgerwriter/newMarkdownnote.

1. Is explicit activate --capture-only the only new no-view scheduled-export path, with activated DB/owner checks, preserved source+activation lock and unchanged schedule/destination? Normal activation without this flag must still fail until registeredview.
2. Does project JSONL-only safely reuse exact full-history compatibility serialization and output guards, retain provenance+unknownmetadata, never overwrite source/config/note/backups, and leave normal registered rolling behavior intact?
3. Does scheduled capture-only mode drain receipts, report pending/historycount and note_publication paused honestly, without creating a different Markdown note or weakening migrate-view coverage/singlepublisher gates?
4. Does the existing activation case meaningfully prove four-agentfuturewrites, private-source preservation, stable scheduled compat export and unchangednote/plist, and refuse unsafeJSONLoutput/multimarkermigration? Focusedcase passed; false capture_only configflag redcontrol failed at scheduled invocation. Suites run only in separate fullclone, never this relay worktree. All16+4shell suites will run after finalapproval.
5. Scope/rollback: legacyJSONLstops growing, downstreamsource must point to compatJSONL; provided foreignJSONLcan be adopted in separate private stores thenimported by existing snapshot protocol without claiming realdeviceUUIDs. Oldnote preservedoutsideSQLite; existinggapaccepted notclaimedrecovered. Review proportionality and material correctness, cite exact source. Only edit this relaythread. No executable tests/fixtures or private-home inspection. Approve if sound; otherwise concrete observedfailures with falsifiers, no speculativeguardframeworks.
```
- Definition of Done: _<fill in the acceptance criteria the Reviewer grades against>_

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
