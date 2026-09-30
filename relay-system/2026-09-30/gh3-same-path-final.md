# RELAY · CLIO GH3 same-path final QA
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
6. **Commit only the relay file** (`relay(clio-gh3-same-path-final-qa): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: **gh3-same-path-final-packet.md** (embedded below — read it here).
- Reviewer: codex   ·   Producer: author
- Started: 2026-09-30

### Artifact — gh3-same-path-final-packet.md
```
# Final review: same-path Obsidian revision

Review delta e1edb8399dc0..HEAD and whole touched store/exporter/installer/test functions against doc/gh3-same-path-plan.md. User requires same existing Obsidian path, filename and schedule. Plan Approved round2; scoped standard-library extension, one local designated publisher, no sync framework/new timer. No installed migration or live private input authorized here. Original issue #3 and this plan track #282 fleet dependency and separate legacy entry-parser upgrade.

1. Does migrate-view discover the documented existing job path without modifying plist, reject ambiguity, check full historical entry coverage, preserve header and verified backup, and keep sources intact?  [Unverified — no citation]
2. Does the unchanged positional exporter invocation now publish the rolling view to that registered path, with no substitute recent file, while rejecting unregistered/unknown writes and legacy maintenance mutations?
3. Are registered-target exception and backup/JSONL/device guards narrow, old/new hash receipts recoverable on publication failure, and current-byte checks truthful within paused-writer/single-publisher assumptions?
4. Do existing+new focused16 cases and witnessed old-exporter red control substantiate the behavior? Read TESTS-RESULTS/2026-09-30-gh3-same-path/. Full five-suite gate runs once AFTER final Approved on unchanged implementation; not claimed yet. Is installer/rollback guidance consistent with actual behavior?

Only write this relay thread. Concrete observed input and falsifier for behavioral findings. No speculative fleet protocol, arbitrary retry framework or unrelated cleanup. Three rounds max. Set literal swept file and PASS/FAIL/PARKED. When Approved, call tick done while owning the new task; DO NOT release before done (previous plan round had a close-mismatch). For nonapproval release normally. Driver attestation required.
```
- Definition of Done: Same-path plan, actual user requirement and four packet questions, scoped single-publisher utility.

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
VERDICT: FAIL
Basis: Same-path routing and recovery are scoped appropriately, but the historical coverage gate accepts unrecognized content in an unchecked display line. Fix S1 before approval. Swept the complete store, exporter, INSTALL.md, storage and exporter tests, including pre-existing code; no additional pre-existing defect identified. Graph tooling unavailable, so source fallback used; no index freshness/completeness claim.

- [Should] S1 — Validate the legacy timestamp-display line's shape. At utils/CLIO/clio-store.py:527–529 the match checks lines 0, 2, 3 and 4 onward, but never line 1. The in-memory probe below accepts both an unmanaged reminder and a missing display timestamp as a covered historical entry. Migration consequently authorizes replacement of content the documented gate says must stop for reconciliation (utils/CLIO/INSTALL.md:391–393). The original backup survives, but the rolling note will drop that text. Concrete fix: reject blank/arbitrary display text; accept the shipped UTC fallback and localized timestamp forms without making display timezone an identity or requiring the current host's timezone.
  Observed input: the row and full Markdown block in the probe below, with line 1 set to "Preserve my unmanaged reminder" or "".
  Affected scope: historical entry blocks evaluated by legacy_coverage during initial migrate-view registration, specifically their timestamp-display slot.
  Falsifier: the same row/block with "2026-09-29T12:00:00Z  " or a valid historical localized display such as "2026-09-29 05:00:00 PDT  " must remain covered; arbitrary text and an empty display must fail before registering a view. This does not request timestamp-display equality as identity.
  Probe command: export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"; python3 "$TMPDIR/coverage-probe.py" > "$TMPDIR/coverage-probe.out". Exit 0. Script (no fixture execution; synthetic in-memory SQLite only):
  ~~~python
import importlib.util, sqlite3, json
spec = importlib.util.spec_from_file_location("store", "utils/CLIO/clio-store.py")
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
row = dict(legacy_id="s:2026-09-29T12:00:00Z", repo="demo", machine="fixture", branch="main", agent="codex", prompt="Synthetic prompt")
c = sqlite3.connect(":memory:")
c.execute("CREATE TABLE events(payload TEXT)")
c.execute("INSERT INTO events VALUES (?)", (json.dumps(row),))
base = '<!-- CLIO:ENTRIES -->\n\n<!-- clio:id:s:2026-09-29T12:00:00Z -->\n## DEMO\n{}\nfixture · main · codex\n\n> "Synthetic prompt"\n'
for shown in ("2026-09-29T12:00:00Z  ", "Preserve my unmanaged reminder", ""):
    print(repr(shown), "=>", s.legacy_coverage(c, base.format(shown).encode()))
c.close()
  ~~~
  Decisive output:
  ~~~text
'2026-09-29T12:00:00Z  ' => ('<!-- CLIO:ENTRIES -->\n', 1)
'Preserve my unmanaged reminder' => ('<!-- CLIO:ENTRIES -->\n', 1)
'' => ('<!-- CLIO:ENTRIES -->\n', 1)
  ~~~
- [Pass] Source review: existing_destination reads the plist without writing it (utils/CLIO/clio-store.py:481–500); the unchanged positional exporter routes to scheduled-export (utils/CLIO/prompt-log-to-md.sh:56–66), which requires the registered destination before draining/projecting (utils/CLIO/clio-store.py:781–789). No replacement recent-note destination or timer is introduced.
- [Pass] Source review: registered publication checks active DB/owner, backup digest and current accepted bytes (utils/CLIO/clio-store.py:474–479,537–547); project records old/new hashes before atomic note replacement (utils/CLIO/clio-store.py:662–670). safe_output retains storage/source/backup protection and reserves the historical exception for the registered Markdown target (utils/CLIO/clio-store.py:587–608,623–629).
- [Pass] Recorded evidence, not a fresh execution: storage-focused.log says "Ran 16 tests in 5.122s" and "OK"; schedule-red-control.log records the old-exporter failure "Obsolete history outside window" and "EXPECTED RED". test/clio-store.py:105–141 asserts same note, unchanged plist, header/backup, local+foreign entries, expiry and retained DB; :186–229 covers failure/retry and write guards. exporter-focused.log records PASS plus the identical-interpreter SKIP.
- [Unverified — needs clone run] Revised complete five-suite gate remains pending by design (TESTS-RESULTS/2026-09-30-gh3-same-path/README.md: final paragraph). No tests, executable fixtures, validate.sh, private state, installed jobs or git commands run here. Harness/producer must provide final unchanged-implementation gate and driver attestation after eventual approval.

Handing off to author — disposition S1, make the scoped correction in the authorized producer checkout, refresh focused evidence, then open round 2 for review.

### Producer · Round 2

S1 — Implemented at legacy_coverage only. A timestamp-display slot must parse as timezone-aware ISO fallback or match the shipped localized datetime + nonempty zone-label shape with a valid calendar/time. Zone abbreviations are not interpreted as identity and need not match this host. Existing actual-legacy-renderer case now refuses arbitrary reminder/blank display before config registration, retains exact edited note bytes, and accepts UTC, PDT and numeric +0545 historical displays. display-red-control.log witnesses the new rejection assertion failing before the production fix; storage-focused-r2.log records all16 passing afterward. No other runtime changes. Full qualifying gate remains after Approved. When approving use tick done while owning task; do not release first. Handing off to codex for round2.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
