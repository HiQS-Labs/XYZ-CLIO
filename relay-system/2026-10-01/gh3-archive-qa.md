# RELAY · CLIO accepted-gap same-note migration QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-01.
-->

NEXT: Producer
STATUS: Approved
ROUND: 1 / 4

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
6. **Commit only the relay file** (`relay(clio-accepted-gap-same-note-migration-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-archive-qa.md** (embedded below — read it here).
- Reviewer: claude   ·   Producer: codex
- Started: 2026-10-01

### Artifact — gh3-archive-qa.md
```
Review the new explicit --archive-unreconciled-note option in PR5 against doc/gh3-plan.md latest scope. User accepts historical gaps, authorizes same-note rolling view, and confirms all other devices CLIO off. Whole-file review utils/CLIO/clio-store.py, INSTALL.md and existing activation test. No private data or live runtime reads/changes.
1. Does default strict migration still reject missing parity/multiple markers?
2. Does explicit archive mode retain full exclusive verified backup and exact first-marker header, no false SQLite parity claim, same destination and singlepublisher guards?  [Unverified — no citation]
3. Are scheduled export and later foreign-write rejection unchanged?
4. Is the synthetic existing case proportionate, and does receipt honestly distinguish archive from imported history?
No new machinery or recovery search. Only edit relay thread. No suites/fixtures in review worktree; source citations, observed falsifiers for material findings. Approve if sound.
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

### Producer · Round 1

Explicit accepted-gap migration is ready. Existing synthetic case witnessed missing-option failure before implementation, then passed with backup/header/foreign-edit checks.

VERDICT: PASS
Basis: Candidate ready for independent review, no installed change yet.

### Reviewer · Round 1 (claude)

swept file: yes
Sweep scope, stated exactly: `utils/CLIO/clio-store.py` read in full (1-872). `utils/CLIO/INSTALL.md` read 318-819 (SQLite section through Notes); lines 1-317 (legacy install heredocs) NOT read this turn. `test/clio-store.py` read 29-125 (helpers) and 470-612 (activation case). `utils/CLIO/prompt-log-to-md.sh` read 52-62 only. No git was run (forbidden this turn), so "unchanged" below means "current code satisfies the contract", not "diffed against the prior commit". No suites or fixtures were run here.

**Q1 — default strict migration**
- [Pass] Without the flag the strict path is still taken: `clio-store.py:592-593` `else: header, count = legacy_coverage(conn, original)`; that function still refuses anything but one marker (`clio-store.py:515-516` `if len(markers) != 1: raise ValueError('expected one standalone historical marker; ...')`), stray body content (`:519-520`) and any entry not matched in SQLite (`:553-554`). The existing case asserts the default rejection on the two-marker note first: `test/clio-store.py:592-593` `assertRaisesRegex(ValueError, 'one standalone')` on `migrate_view(self.db, publishers_paused=True)`.

**Q2 — explicit archive mode**
- [Pass] Full exclusive verified backup is shared by both modes, not forked: `clio-store.py:598` `os.open(backup_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)`, whole `original` written and fsynced (`:600-602`), then `:609-610` re-hashes backup and live note against `digest(original)` and raises `'backup or note changed during migration; no view registered'` before any config write.
- [Pass] Exact first-marker header: `clio-store.py:588` uses `re.search` (first match) with the same standalone-line pattern as `legacy_coverage` (`:514`), `:591` `header, count = text[:marker.end()], None`. Probe (synthetic string, BOM + CRLF + an inline non-standalone marker mention + two standalone markers): `python3 - <<EOF … re.search(P,t) … EOF`, rc=0, output `2 '﻿# H\r\nnote mentions <!-- CLIO:ENTRIES --> inline\r\n<!-- CLIO:ENTRIES -->\r\n' True` — header ends at the first standalone marker and its bytes equal the original prefix. Second probe line `None`: a marker with no trailing newline does not match, so `:589-590` fails closed with `'historical header marker missing; preserve and inspect the note'`.
- [Pass] No false SQLite parity claim in the receipt or stored view: `clio-store.py:594` `coverage = 'archived-not-reconciled' if archive_unreconciled_note else 'verified'`; `:613` stores `'legacy_entries': count, 'coverage': coverage` with `count` = `None`; `:615` returns `'covered_entries': count, 'coverage': coverage`. Consumer probe `rg -n "legacy_entries|covered_entries|'coverage'" utils/CLIO test doc` (rc=0) shows no reader that would treat `None` as a number — only `clio-store.py:613,615`, tests and docs.
- [Pass] Same destination and single-publisher guards precede the mode branch: `clio-store.py:572-573` raises without `publishers_paused`; `:574` `target = existing_destination(markdown)` (plist-derived, `:506-507` refuses a differing explicit path); `:578` `active_config`; `:582` `safe_output(conn, path, target, historical=True)`. The flag branch begins only at `:584`.
- [Pass] INSTALL describes exactly this and nothing more: `INSTALL.md:438-446` ("archived, not claimed imported into SQLite: the receipt reports `coverage: archived-not-reconciled` and `covered_entries: null` … Default migration still requires full entry parity").

**Q3 — scheduled export and later foreign-write rejection**
- [Pass] The scheduled route has no archive-specific branch: `clio-store.py:828-840` still gates on `checked_view` (`:836`) and the installed job still calls it with no extra flag (`prompt-log-to-md.sh:62` `exec python3 "$helper" scheduled-export "$OUT" --mode "$MODE"`). Foreign-write refusal is mode-independent: `clio-store.py:563-567` (backup hash, then `current not in view['accepted_hashes']` → `'note changed outside this publisher; …'`), plus the in-projection recheck `:705-706`. Archive mode seeds `accepted_hashes` identically (`:612`). Test covers post-publication foreign edit: `test/clio-store.py:606-608`.

**Q4 — test proportionality and receipt honesty**
- [Pass] Proportionate: 17 lines appended to the existing activation case (`test/clio-store.py:592-608`), reusing its note/job/plist fixture; no new suite or helper. It asserts default rejection, receipt fields (`:595-596`), backup == original bytes (`:597`, `:605`), note untouched by migration (`:598`), header through first marker (`:600`), scheduled publication via the unchanged plist command (`:601-604`), and foreign-edit refusal.
- [Unverified — needs clone run] Producer's statement that the case "passed with backup/header/foreign-edit checks" and witnessed the missing-option failure first. Not measurable in this worktree; the harness gate / disposable-clone run owns it.

**Non-blocking (no behaviour change required for approval)**
- [Nit] `clio-store.py:680` prints `'Older history remains in SQLite. This view covers imported/local records only.'` unconditionally. After an archive-mode cutover the pre-cutover note body lives only in the verified backup, so the first sentence over-reads for that note. The receipt, config and INSTALL are accurate, and the second sentence qualifies it, so this is wording, not a parity claim in the receipt. Optional fix: when `view.get('coverage') == 'archived-not-reconciled'`, emit one extra line such as `Earlier note content is archived, not reconciled into SQLite.` Operator should at least know the published note will carry this sentence.
- [Nit] Archive-mode missing-marker refusal (`clio-store.py:589-590`) has no assertion in the case; one `assertRaisesRegex(ValueError, 'header marker missing')` on a marker-less note would pin it. Fails closed today per the probe above.
- [Nit] `clio-store.py:594` has trailing whitespace (`rg -n " +$" utils/CLIO/clio-store.py` → 1 match, line 594, rc=0); the marker regex literal is duplicated at `:514` and `:588`.
- [Nit] `INSTALL.md:326-327` ("complete coverage of the existing note are required") and `:341-342` read as absolute; they are correct for the default and `:438-446` states the exception, but a "(unless explicitly archived, see step 4)" pointer would stop a skim-reader concluding the option does not exist.
- [Nit] Pre-existing, outside this change's path: `clio-store.py:832` tests `cfg.get('view')` on `main`'s `cfg`, which is `{}` whenever `--db` is passed (`:812`), so `--db X scheduled-export NOTE` on a capture-only store with a registered view would stay JSONL-only and report `note_publication: paused`. The installed job passes no `--db` (`prompt-log-to-md.sh:62`), so the authorized cutover is unaffected; noted for the sweep only.
- [Nit] Pre-existing: redundant function-local `import re` at `clio-store.py:194` (module already imports it at `:12`).

Pre-existing defects in the swept ranges: none found beyond the two nits above. INSTALL.md 1-317 was not swept, so no claim is made about it.

VERDICT: PASS
Basis: Default migration is still strict; archive mode differs only in skipping entry parity, keeps the exclusive hash-verified backup, exact first-marker header, destination and single-publisher guards, and reports archived-not-reconciled with a null count; scheduled export and foreign-write refusal carry no archive-specific branch. Approval covers the code and docs as read; the test-pass claim remains unverified until the disposable-clone suites run, and this approval is not permission to change installed hooks, the live note or launchd jobs.  [Unverified — no citation]

Handoff: relay closed (Approved), no further Reviewer turn needed. Producer/operator: run the existing suites in a disposable full clone before any deployment.


### Attestation · relay-drive — 2026-10-01T22:09:16Z
task: CLIO-GH3-ARCHIVE-QA
reviewer: claude
status: Approved
reviewed-head: abfc004fbc92a2d7d06ca93ddba98ae9eb37b7b9
added-range: 6571+7836
added-sha256: 7b2c987f00c57c50dfb7f0b91a8e9ce7623d61c869b9076d1562a014840a2b68
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
