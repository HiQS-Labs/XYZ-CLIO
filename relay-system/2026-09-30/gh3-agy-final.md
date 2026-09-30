# RELAY · CLIO PR4 Agy pre-merge QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-09-30.
-->

NEXT: author
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
6. **Commit only the relay file** (`relay(clio-gh3-agy-final): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-agy-qa-packet.md** (embedded below — read it here).
- Reviewer: agy   ·   Producer: author
- Started: 2026-09-30

### Artifact — gh3-agy-qa-packet.md
```
QA CLIO PR #4 before authorized merge and local deployment. Current pushed head 486ce594c5586295259dde4e2bfd30f79705d4ea; PR base main. Read AGENTS.md, doc/gh3-plan.md, doc/gh3-same-path-plan.md, doc/gh3-handoff.md, whole utils/CLIO/clio-store.py, installer shared writer, both tailers, exporter, existing storage suite and prior receipts. Local stdlib developer CLI with one designated shared-note publisher; no new service/vector store/push loop/ledger writer. No private installed data is available to this reviewer. Only edit this relay thread; do not run executable fixtures or suites in a linked worktree.

1. Does capture preserve durable receipts, immutable IDs/provenance and cursor retry semantics through all four existing agent paths, including the small tailer changes?
2. Does additive JSONL migration account for every complete input line, preserve originals/extras, refuse conflicts and permit bounded activation without losing arrivals? Are backup and ownership/import guards proportionate and truthful?
3. Does migrate-view verify complete historical note coverage, exact personal header and backup, then reuse SAME existing output path/filename and unchanged scheduled invocation? Actual local documented plist is exporter positional path and StartInterval300; it must remain byte-identical. Are Unicode/timezone/metadata/idle expiry/failure retry contracts correct? No separate recent final note.
4. Are read-only query and chronological compatibility/device snapshots safe; foreign origins not echoed; full history retained? Are current tests/negative controls and handoff claims supported?
5. Is the proposed local cutover correctly gated on source/device coverage and exactly one shared-note publisher, retaining downstream Rebalance #282/#281 dependencies? Current user explicitly authorizes merge after QA and local runtime deployment/backups; no assumption of completed fleet transport or semantic consumer migration.

Review whole touched files; flag concrete material defects only with file:line, Observed input, Affected scope and Falsifier (blocker needs observed failure). Do not invent enterprise machinery. Grade passes against source; record no executable test run. Approve if no material unresolved issue. Producer runs final existing four shell suites and 16 SQLite cases in full verification clone after approval. Output VERDICT PASS/FAIL and swept file yes/no; harness owns attestation/commit.
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

### Reviewer · Round 1

swept file: yes

* **1. Durable receipts & tailer semantics:** `[Pass]` Capture durably preserves receipts in the pending queue (`file:utils/CLIO/clio-store.py:249`). Tailer correctly uses `rc=3` lock checks and `rc=0` returns to advance the cursor (`file:utils/CLIO/clio-agy-tail.sh:202`).
* **2. JSONL additive migration & guards:** `[Pass]` Incomplete input lines are safely skipped and ignored from prefix hash (`file:utils/CLIO/clio-store.py:335`). Extras conflicts raise ValueError (`file:utils/CLIO/clio-store.py:189`). Self-import and foreign origins are refused correctly (`file:utils/CLIO/clio-store.py:720`).
* **3. Historical coverage & scheduled invocation mismatch:** `[Blocker]` The acceptance criteria requires the actual local documented plist interval to be 300 and remain byte-identical, but the codebase documents 60.
  Observed input: `INSTALL.md` line 584 uses `<integer>60</integer>`.
  Affected scope: macOS launchd plist interval in `INSTALL.md`.
  Falsifier: If the expected deployed interval is 300 to match the user's requirement, update `INSTALL.md` to 300.
* **4. Query & device snapshots:** `[Pass]` Queries enforce `PRAGMA query_only=ON` (`file:utils/CLIO/clio-store.py:101`). Export device excludes foreign origins via `WHERE origin_id=?` (`file:utils/CLIO/clio-store.py:698`). Legacy JSONL preserves full chronological history (`file:utils/CLIO/clio-store.py:678`).
* **5. Migration correctly gated:** `[Pass]` `migrate-view` enforces `--publishers-paused` (`file:utils/CLIO/clio-store.py:570`) and verifies full matching legacy coverage before adopting (`file:utils/CLIO/clio-store.py:551`).

**VERDICT**: FAIL
**Basis**: INSTALL.md documents StartInterval 60, conflicting with the required byte-identical StartInterval300.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
