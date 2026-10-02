# RELAY · CLIO local capture-only final QA
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-09-30.
-->

NEXT: Producer
STATUS: Approved
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
- Definition of Done: all five packet questions pass; explicit local capture and compatibility export, unchanged note/job/source, intact default migration guards, proportionate existing-suite verification.

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

### Producer · Round 1

Implemented explicit capture-only activation and JSONL-only projection in the existing helper; scheduled exporter keeps the original job and note unchanged while refreshing complete compatibility history. Focused existing activation case passed with all four writer routes and preservation checks. Red control setting capture_only=false failed at the scheduled invocation (exit3); restored candidate afterward. Review against the five packet questions. Final fullclone suites follow approval. No installed activation yet.

VERDICT: PASS
Basis: ready for independent QA, not a self-approval of landing.
Handing off to Reviewer (codex) for independent QA.


### Reviewer · Round 1

swept file: yes

Reviewed the complete clio-store.py, INSTALL.md, exporter adapter and existing storage test, plus AGENTS.md and latest operator scope. Verify-tier source fallback: list_projects returned all 77 projects (has_more=false), with no matching CLIO/worktree project; no applicable generation or graph coverage is available. No indexing, private-home inspection, tests, executable fixtures or git commands run. The requested origin/main diff was not supplied as a seeded artifact and remains unverified under the no-git instruction.

- [Pass] Q1/Q3, source inspection: explicit capture_only is stored only by activation's flag (utils/CLIO/clio-store.py:403, :438); scheduled-export checks active DB/owner, existing destination, drains receipts, uses JSONL-only and reports pending (:480, :812). Without that mode it requires checked_view (:820). JSONL-only returns before Markdown rendering, with "note_publication": "paused" (:660). Source locking/import verification/backup remain in activation (:415–435); exporter dispatch preserves its positional invocation (utils/CLIO/prompt-log-to-md.sh:53–62). No additional issue found in these paths.
- [Should] R1 — Q2's backup-preservation requirement is incomplete in the existing guard reused by JSONL-only. Activation creates source.name + '.pre-sqlite-' + time_ns (utils/CLIO/clio-store.py:429), but safe_output protects the original source and registered view backup, not this source backup (:608–627). Its accepted result is passed straight to atomic replacement (:653–659). Thus explicit JSONL-only output can replace the preserved original backup; this pre-existing defect is in scope for the new guarded path. Fix narrowly at safe_output by rejecting activation backup siblings of known source paths (including retained partial backups); reuse the existing storage case for clone verification, without a new ledger/service.
  Observed input: a known source at $TMPDIR/original.jsonl and an existing synthetic $TMPDIR/original.jsonl.pre-sqlite-123 containing a JSONL row; safe_output accepted the backup while rejecting the source. The probe only queried the guard; it did not publish or overwrite the backup.
  Affected scope: output paths matching the activation backup naming convention for recorded source paths; normal new compatibility outputs remain allowed.
  Falsifier: the existing activation case's actual .pre-sqlite-* backup supplied to project(..., jsonl=backup, jsonl_only=True) must raise before publication and preserve its bytes; an unrelated new compat.jsonl must still export successfully. If the current candidate already rejects the actual backup, this finding is unnecessary.
  Probe command (exit 0; all scratch under .relay-scratch/tmp):
  ```bash
  export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"
  mkdir -p "$TMPDIR"
  python3 - <<'PROBE'
  import importlib.util, os, sqlite3
  from pathlib import Path
  spec = importlib.util.spec_from_file_location('store', 'utils/CLIO/clio-store.py')
  s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
  root = Path(os.environ['TMPDIR']).resolve()
  s.CONFIG = root / 'absent-config.json'
  source = root / 'original.jsonl'
  backup = root / 'original.jsonl.pre-sqlite-123'
  backup.write_text('{"timestamp":"2026-09-29T12:00:00Z","prompt":"synthetic preserved source"}\n')
  before = backup.read_bytes()
  conn = sqlite3.connect(':memory:')
  conn.executescript('CREATE TABLE sources(path TEXT); CREATE TABLE device_imports(source TEXT);')
  conn.execute('INSERT INTO sources VALUES (?)', (str(source),))
  for name, target in [('source', source), ('activation-backup', backup)]:
      try:
          print(name + ': ACCEPTED ' + str(s.safe_output(conn, root / 'history.sqlite3', target)))
      except ValueError as e:
          print(name + ': REJECTED ' + str(e))
  print('backup unchanged by read-only guard probe:', backup.read_bytes() == before)
  PROBE
  ```
  Decisive output: "source: REJECTED output would overwrite storage, configuration or source history"; "activation-backup: ACCEPTED .../.relay-scratch/tmp/original.jsonl.pre-sqlite-123"; "backup unchanged by read-only guard probe: True".
- [Pass] Q2 otherwise: JSONL-only shares full chronological payload serialization with normal projection, retaining extras and provenance (utils/CLIO/clio-store.py:652–659); registered rolling publication keeps checked_view and accepted-hash checks (:647–651, :686–695). migrate-view still requires publishers-paused and complete marker/body coverage (:511–555, :571–605).
- [Pass] Q4 test design: the existing activation case asserts all four shared-writer agent routes, five exported rows, paused publication, zero pending and unchanged source/note/plist, plus source-output and multi-marker rejection (test/clio-store.py:552–590). Actual Codex/Agy tailer execution is separately covered by the existing four-agent case (:439–479). These are meaningful checks within the stated scope.
- [Unverified — needs clone run] Producer's focused pass/red-control report and final 16 storage cases + four shell suites have not been independently executed here, as required by containment. Harness/author must run the existing full-clone gate after the revision.
- [Pass] Q5 scope/rollback guidance: INSTALL.md:333–343 explicitly preserves the note and other Macs, switches downstream readers to full-history compat JSONL, and disclaims fleet completeness. Separate adoption origins and no recovered hardware identity are documented at :495–500; rollback pauses writers and retains SQLite-era events at :520–537. The latest doc/gh3-plan.md scope accepts the historical gap and keeps rolling publication separate. No additional material pre-existing defect found in the swept paths beyond R1.

VERDICT: FAIL
Basis: the core capture-only flow is proportionate and source-reviewed, but Q2's explicit backup guard contract fails for an activation-produced backup path. Address R1, then rerun the existing clone gate; no additional historical collection is requested.
Handing off to Producer (author) — take your turn to disposition R1 and revise the existing guard.

### Producer · Round 2

R1 Implemented. safe_output now protects known source backup siblings named <source>.pre-sqlite-*, including partial backups, alongside existing original-source guards. No new service/ledger; normal compatibility paths unchanged. Extended the same activation case to pass its actual activation-created backup as JSONL-only output and assert original bytes remain. Witnessed pre-fix failure: ValueError not raised (backup-red log); candidate passes (backup-green log). No live data involved.

For bounded R2: adjudicate the actual backup guard and its existing-case verification, and confirm R1 passing capture-only/projection/migration conclusions still hold. Full gate follows final approval. Supplied origin/main diff was not seeded earlier; do not assert it was reviewed via git. The exact material code is present in this isolated target checkout. User scope remains no more collection, local capture enabled after final checks, same note untouched until a separate rolling cutover.

VERDICT: PASS
Basis: R1 root backup guard fixed and witnessed; independent re-review required.
Handing off to Reviewer (codex).

### Reviewer · Round 2

swept file: yes

Verify-tier source fallback: list_projects returned all 77 projects (has_more=false), with no matching CLIO/worktree project; no applicable generation or index coverage exists. Read the complete storage helper, INSTALL.md, exporter and storage test, AGENTS.md and latest operator scope. No additional material pre-existing defect found in the swept files. No git, executable tests/fixtures, private-home inspection or installed changes. Origin/main diff remains unverified because it was not seeded. Used relay-xyz locator first: exit 0, harness found; it also emitted `driver_lock_path_for_repo: command not found`, so readiness is not claimed beyond discovery.

- [Pass] R1 resolved narrowly: utils/CLIO/clio-store.py:611–617 derives protected backup siblings from recorded sources plus the default legacy source, rejecting the `.pre-sqlite-` prefix independent of file completeness. project checks this guard before atomic JSONL publication (:657–663). The existing activation case uses the actual created backup and asserts refusal plus preserved bytes (test/clio-store.py:563–565, :589–591). No new guard framework or suite.
  Guard-only probe command (exit 0; in-memory synthetic source table; no output publication or source files created):
  ```bash
  export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"
  mkdir -p "$TMPDIR"
  python3 - <<'PROBE'
  import importlib.util, os, sqlite3
  from pathlib import Path
  spec = importlib.util.spec_from_file_location("store", "utils/CLIO/clio-store.py")
  s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
  root = Path(os.environ["TMPDIR"]).resolve()
  s.CONFIG = root / "absent-r2-config.json"
  conn = sqlite3.connect(":memory:")
  conn.executescript("CREATE TABLE sources(path TEXT); CREATE TABLE device_imports(source TEXT);")
  source = root / "r2-original.jsonl"
  conn.execute("INSERT INTO sources VALUES (?)", (str(source),))
  for name, target in [("source", source), ("activation-backup", root / "r2-original.jsonl.pre-sqlite-123"), ("partial-backup", root / "r2-original.jsonl.pre-sqlite-456"), ("compatibility", root / "r2-compat.jsonl")]:
      try:
          s.safe_output(conn, root / "r2-history.sqlite3", target)
          print(name + ": ACCEPTED")
      except ValueError as e:
          print(name + ": REJECTED " + str(e))
  PROBE
  ```
  Decisive output: `source: REJECTED output would overwrite storage, configuration or source history`; `activation-backup: REJECTED output would overwrite a preserved activation source backup`; `partial-backup: REJECTED output would overwrite a preserved activation source backup`; `compatibility: ACCEPTED`. Backup labels designate naming predicates, not created complete/partial files; actual backup preservation execution belongs to the clone gate.
- [Pass] Q1/Q3 source review still holds: explicit activation flag persists capture-only under the existing final import/verification/append-lock boundary (utils/CLIO/clio-store.py:403–443). scheduled-export validates active DB/owner (:480–485), checks existing destination, drains receipts, exports JSONL and reports pending (:816–828). Normal mode uses checked_view; JSONL-only returns before Markdown rendering with `note_publication: paused` (:664–666). Existing positional adapter routes before legacy mutations (utils/CLIO/prompt-log-to-md.sh:53–62). No schedule/job writer added.
- [Pass] Q2 source review: both projection modes share full timestamp/record-ID ordered payload serialization, including provenance and extras (utils/CLIO/clio-store.py:656–663). Config, DB/WAL, recorded inputs, pending receipts, historical marker note and registered backup guards remain (:608–630). Registered publication retains checked_view and accepted-hash protection (:651–653, :690–699).
- [Pass] Q4 verification design: the existing activation case asserts four shared-writer agent routes, five compatibility rows, paused publication, zero pending and unchanged note/plist/source, then rejects source/actual backup output and multi-marker migration (test/clio-store.py:552–593). Existing actual Codex/Agy tailer coverage remains (:439–479); normal activation's scheduled-export refusal is asserted at :208–219. These checks address the stated local envelope.
- [Pass] Q5 scope: INSTALL.md's capture-only paragraph explicitly says the original JSONL stops growing, downstream readers switch to full-history compatibility JSONL, and other Macs remain unchanged (:333–343). Adoption provenance remains ownership assigned at import, not recovered hardware (:495–500); rollback preserves SQLite-era arrivals (:520–537). Latest doc/gh3-plan.md operator scope accepts the final collection/gap and separates rolling cutover. migrate-view still requires publisher pause, complete historical body coverage and verified backup (utils/CLIO/clio-store.py:511–605).
- [Unverified — needs clone run] Producer's red/green execution reports and final 16 storage cases plus four shell suites were not run here. Author/harness must complete the authorized disposable-full-clone gate before installed activation; this approval does not assert deployed acceptance or diff verification.

VERDICT: PASS
Basis: all five packet questions pass source review and existing-case design; the sole open finding R1 is resolved with a measured guard result. No further behavior change requested. Full executable gate remains the required next step.
Relay closed (Approved), no further review turn needed; author/harness proceeds with the final full-clone gate before local activation.


### Attestation · relay-drive — 2026-10-01T04:14:38Z
task: CLIO-GH3-LOCAL-CAPTURE-R2
reviewer: codex
status: Approved
reviewed-head: 07d4a7196b8c29e981a071e74b7b059a91ae69ed
added-range: 15802+5628
added-sha256: 2e988f962e8126b5f114ed1b6a387b3894f0b332a37b31ab66645b0bd5d4af24
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
