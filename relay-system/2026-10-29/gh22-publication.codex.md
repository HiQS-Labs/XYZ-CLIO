# RELAY · CLIO #22 unchanged upstream publication and verification
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-29.
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
6. **Commit only the relay file** (`relay(gh22-publication): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **.relay-artifacts/gh22-publication-packet.md** — the read-only path that
  `relay-drive.sh --artifact-file temp/gh22-publication-packet.md` seeds into the isolated worktree (read it there; do NOT edit it).
- Reviewer: codex   ·   Producer: codex-producer
- Started: 2026-10-29
- Definition of Done: Verify standalone publication from the merged canonical source: all 15 files, bytes and executable modes match source and UPSTREAM; publisher and evidence are truthful, existing six suites plus publication red control passed in a separate full clone with intact identity. Runtime logic already received independent upstream QA. Read the complete publication artifact and current relevant files; narrow read-only probes permitted. Do not run suites, installer, Git, or touch live history/jobs. Grade findings and PASS/FAIL; write only this relay. Device acceptance remains pending.

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
Basis: Approve the unchanged standalone publication. Direct read-only comparison establishes all 15 files' bytes and executable bits against the supplied canonical checkout and recorded manifest/receipt. The six retained suite logs support the producer's successful clone-run report. Red-control and clone-identity results are producer attestations, with the evidence limitation below. Device acceptance and the enclosing harness gate remain separate.
swept file: yes

Read the entire 1,068-line packet, including the complete publisher, publication document, manifest, receipt, prior review turns/attestations and publication diff. Also read the current publisher, complete Codex tailer, relevant INSTALL scheduling/recovery section, README test contract and all seven retained logs. This is publication review; it relies on the prior independent upstream runtime QA rather than claiming a fresh audit of every unchanged runtime module. No material pre-existing defect found in the reviewed publication path.

- [Pass] Actual publication parity: `utils/clio-capture/UPSTREAM:4` pins `f0819314c078f58e9d51b6ccd698c76b700ec1cc`; its 15 entries beginning at :6 agree with source files and `TESTS-RESULTS/2026-10-29-gh22/publication.json:5`. Probe below checks nonempty exact file sets, SHA256, regular-file/symlink boundary and executable bits. The source HEAD and cached origin/development ref equal that revision. This establishes local source parity, not a fresh remote fetch. Retain the generated files unchanged.
- [Pass] Publisher matches its scoped role: `scripts/publish-from-rebalance.sh:60` checks canonical source/merged ancestry before exporting committed content at :73; :82 uses checksum and permission-preserving rsync. The current hash integrity check returned exit 0 with `CLIO matches HiQS-Labs/rebalanceOS@f0819314c078 (15 files)`. Its manifest/check is hash-based (:31, :43); executable parity is established separately by this review's comparison, not attributed to `--check`. No publisher change requested.
- [Pass] Retained suite results are consistent with the receipt: `TESTS-RESULTS/2026-10-29-gh22/publication.json:82` records six suite exits of zero plus the publisher check; `provenance.jsonl:1` pins publication revision `b8ed9700f1f36f3d00120c540ebe1664e5aeff28` and the disposable-clone/throwaway-device boundary. Logs contain `PASS: all capture cases (bash)`, `PASS: bash`, `PASS: codex tailer`, `PASS: agy tailer`, `Ran 17 tests` / `OK`, and `PASS: clio-runtime`. The duplicate-interpreter skips and Python ResourceWarnings remain visible. The capture log's malformed-JSON diagnostic corresponds to the deliberate malformed-input case at `test/clio-capture.sh:130`; it does not contradict the recorded successful suite exit. No suite was rerun here.
- [Nit] Evidence retention could be stronger: `TESTS-RESULTS/2026-10-29-gh22/publication.json:119` retains the red control only as exit 1, and :124 retains identity only as `identity_intact: true`; the directory contains no before/after identity values or red/restored output. These are accepted as producer-reported results, not independently reproduced facts. For future receipts, retain the existing run's identity bracket and mutation/restoration command/output alongside the current logs; no new suite or gate is needed. This does not demonstrate a failed check or invalidate the direct parity result.
- [Pass] Deployment limits remain honest: `doc/gh22-codex-publication.md:9` says no device acceptance is claimed. `utils/clio-capture/INSTALL.md:709` limits durable replay to visited files, :768 requires exclusive execution, :773 restores the original loaded/unloaded scheduling state on success or failure, and :781 requires actual SQLite/session checks and the 120-second submission observation. The corresponding tailer checkpoint is at `utils/clio-capture/clio-codex-tail.sh:269`. Retain these constraints; publication approval does not establish live recovery.
- [Unverified — needs clone run] No test suite, executable fixture, installer, live history/job operation or Git command was run by this reviewer. Fresh suite execution and the enclosing harness's post-turn gate are not established by this turn. Prior clone results were reviewed as retained evidence; the harness owns the file-scoped commit and subsequent gate.

Read-only comparison command (exit 0; no artifact code executed):

```sh
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"
mkdir -p "$TMPDIR"
python3 - <<'PY'
import hashlib,json,re
from pathlib import Path
packet=Path('.relay-artifacts/gh22-publication-packet.md').read_text()
src=Path(re.search(r'checkout available at (.*?) \(do not print',packet)[1])
r=json.loads(Path('TESTS-RESULTS/2026-10-29-gh22/publication.json').read_text())
m={p:h for h,p in re.findall(r'^([a-f0-9]{64})  (.+)$',Path('utils/clio-capture/UPSTREAM').read_text(),re.M)}
def files(base):
    paths=list((base/'utils/clio-capture').glob('*'))+list((base/'test').glob('clio-*'))+list((base/'test/fixtures/clio').rglob('*'))
    return {str(p.relative_to(base)) for p in paths if p.is_file() and p.name not in ('README.md','LICENSE','UPSTREAM')}
assert len(m)==len(r['files'])==15
assert set(m)==files(Path('.'))==files(src)=={v['path'] for v in r['files']}
for v in r['files']:
    p=Path(v['path']); q=src/p
    assert not p.is_symlink() and not q.is_symlink()
    assert hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(q.read_bytes()).hexdigest()==m[str(p)]==v['sha256']
    assert (p.stat().st_mode&0o111)==(q.stat().st_mode&0o111)
    assert bool(p.stat().st_mode&0o111)==v['executable']
print('15/15: scope, bytes and executable bits match source, UPSTREAM and receipt')
g=src/'.git'
ref=(g/'HEAD').read_text().strip().removeprefix('ref: ')
assert (g/ref).read_text().strip()==r['source_revision']
assert (g/'refs/remotes/origin/development').read_text().strip()==r['source_revision']
print('Source HEAD and cached origin/development equal recorded revision')
for name in ('AGENTS.md','scripts/publish-from-rebalance.sh','doc/gh22-codex-publication.md','utils/clio-capture/UPSTREAM','TESTS-RESULTS/2026-10-29-gh22/SUMMARY.md','TESTS-RESULTS/2026-10-29-gh22/publication.json'):
    assert packet.split('## '+name+'\n',1)[1].split('\n## ',1)[0].rstrip()==Path(name).read_text().rstrip()
print('6/6 embedded current files match checkout; packet has 1068 lines')
PY
```

Decisive output:

```text
15/15: scope, bytes and executable bits match source, UPSTREAM and receipt
Source HEAD and cached origin/development equal recorded revision
6/6 embedded current files match checkout; packet has 1068 lines
```

Additional read-only command: `bash scripts/publish-from-rebalance.sh --check` (exit 0); output: `CLIO matches HiQS-Labs/rebalanceOS@f0819314c078 (15 files)`.

Relay closed (Approved), no further turn needed. The harness owns the commit and subsequent gate; device acceptance remains pending.


### Attestation · relay-drive — 2026-10-30T03:11:43Z
task: RELAY-gh22-publication
reviewer: codex
status: Approved
reviewed-head: d2451a20dad69e7387371c97910963bfd3abdacc
added-range: 5918+6963
added-sha256: 2512dcd96bcb253ff81805f5f5543aad7703c3b6a028d15efe645d1242599d3a
<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
