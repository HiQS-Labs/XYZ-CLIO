# RELAY · gh11-plan-kimi
<!--
  Single source of truth for this two-agent relay. Read the ENTIRE file before acting.
  Scaffolded by relay-automation/new-relay.sh on 2026-10-24.
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
6. **Commit only the relay file** (`relay(gh11-plan-kimi): <role> r<N>`); no push. **Stop** and report one line.
7. **Hand off explicitly — EVERY turn, not just the first** (GH-268). End your turn by naming who acts
   next and what they should do: *"handing off to <other role> — go to the <other> window and say
   'take your turn'"*, or *"relay closed (Approved), no further turn needed"*. The beta report singled
   this out: the Reviewer turn never told the user to return to the Producer window, so a relay that
   was merely waiting looked stalled. A turn that ends without this line is not finished.

## Setup
- Artifact under review: `doc/gh11-plan.md` (plan only; no code written yet)
- Source to read for grounding (read in full where cited): `utils/CLIO/clio-store.py` (`configure_fleet` ~L935, `reconcile_fleet` ~L963, `checked_view` ~L578, `migrate_view` ~L638, `legacy_coverage` ~L531, `render_markdown` ~L712, `snapshot_records`/`import_snapshot` ~L820-880, `main`/`scheduled-export` ~L1024-1150), `test/clio-store.py` (`test_device_roundtrip_preserves_owner_extras_and_no_echo` ~L465-700), `utils/CLIO/INSTALL.md` (device-independent section ~L808-868), `AGENTS.md`, `doc/gh3-device-independent-plan.md` (the design this extends).
- Requirements (issue #11): a new device joins by committing its own `devices/<uuid>/clio.jsonl`, peers pick it up on their next scheduled reconcile with no command run on any peer; retiring needs at most one committed change; any healthy device can produce the shared note, so an absent/offline device only delays its own rows; existing explicit-origin configs keep working; no duplicate rows.
- Operational envelope: a personal fleet of about four Macs sharing one PRIVATE Git repo that only the operator can write; stdlib-only local CLI helper. Grade against commensurate complexity: do NOT ask for leases, election, signing, heartbeats, multi-tenant threat models, new test suites or new services. AGENTS.md: no second ledger writer, Git push loop or scheduler in this repo; Rebalance owns delivery.
- Reviewer: aider   ·   Producer: claude-a
- Started: 2026-10-24
- Definition of Done: the plan is grounded (every code claim matches the cited lines), meets every requirement above or justifies the gap, extends the existing helper/writer without a parallel path, has falsifiable checks with red controls, and has adequate rollback. Answer these explicitly:
  1. Is the claim that a second device cannot register an already SQLite-rendered note (via `legacy_coverage`) correct? Cite the lines.
  2. Does discovery via `git ls-tree -r -z --name-only <pinned head> -- devices` + `valid_origin` + the existing `import_snapshot` validation stay inside the existing trust boundary and Git-read bounds (`git_read`, deadline, `MAX_FLEET_BYTES`)? Any path-parsing hole (e.g. a name with newline, a nested path, a symlink blob)?
  3. Is making discovery opt-in (`fleet['discover']`) the right compatibility call, and does keeping explicit `--origin` as a pinned list (still reports `missing`) preserve current behaviour?
  4. Is "retirement needs no committed change" an acceptable reading of the retirement requirement given imports never delete rows? If not, what is the smallest fix?
  5. `migrate-view --join-fleet-note`: is reusing the `checked_view` peer-reproduction check via one factored helper sound? Is requiring all record IDs known + byte reproduction at the note's own cutoff enough to keep the header/backup/hash protections? Any ordering trap with `configure-fleet --repair-generated-note` (which requires a registered view)?
  6. Is there any requirement missed, any code claim wrong, or anything over-engineered that should be cut?
  7. Are the test cases (one new method in the existing `test/clio-store.py`) sufficient and bounded, with real red controls?

## Ground rules
1. This file is the single source of truth. The agents never share memory — read the whole file.
2. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns.
4. Stay tight — findings are bullets, not essays. Grade every finding.
5. **The Reviewer never edits the artifact.** It proposes graded findings; the Producer implements.
6. The relay ends on **Approved** (Reviewer only). End each turn by committing just this file; no push.

## Log

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
