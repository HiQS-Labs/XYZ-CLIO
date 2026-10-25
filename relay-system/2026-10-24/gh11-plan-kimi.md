# RELAY · gh11-plan-kimi
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

### Reviewer · Round 1
VERDICT: FAIL
Basis: The architecture is appropriately small and the central code claims are grounded, but the proposed upgrade command can disable an existing publisher's note repair, and one join test can pass its refusal step for the wrong reason. Both are narrow plan fixes; no architectural rework is needed.
swept file: yes

Pre-existing sweep: I found no unrelated pre-existing defect in the supplied helper/test seams that needs to be added to this GH-11 scope. No suites or executable probes were run; the findings below use concrete source and plan inputs, not claims of test execution.

- [Should] **The one-time upgrade instruction must preserve an existing publisher's repair configuration.** The plan says each existing device runs literally `configure-fleet --discover-origins` once. `configure_fleet` constructs a fresh fleet mapping with `repair_generated_note: repair`, and carries `header_sha256`/`coverage` only inside `if repair` (`utils/CLIO/clio-store.py:935-961`). Thus an existing repair-enabled publisher following that instruction with the default `repair=False` loses those settings; a later valid peer render can then hit the repair-off foreign-edit refusal instead of converging.
  - Observed input: an existing config produced by `configure_fleet(..., repair=True)`, followed by the plan's upgrade invocation without `--repair-generated-note`.
  - Affected scope: the documented one-time upgrade of existing repair-enabled publishers, not the initial configuration of a capture-only device.
  - Falsifier: apply the exact documented upgrade to a synthetic repair-enabled config; if repair remains enabled and its header/coverage pins remain intact, this finding is unnecessary. With the current constructor and omitted flag, the expected result is `repair_generated_note: False`.
  - Concrete fix: make the upgrade documentation distinguish capture-only devices from existing repair-enabled publishers, and show the latter retaining `--repair-generated-note` and any desired pinned `--origin` arguments. Add a focused assertion for the resulting configuration; no new helper mechanism is required.
- [Should] **Isolate the body-edit join refusal from the unknown-ID refusal.** Test 6 currently orders the unknown-ID red control before B reconciles, then tries a body-edit refusal, and only afterward reconciles B. While B still lacks A's record, both a pristine note and an edited note fail at the “every record ID known” gate, so the body-edit step does not prove byte-reproduction validation.
  - Observed input: a fleet-rendered note containing a record absent from B, followed by the same note with a body edit before B reconciles.
  - Affected scope: the planned red control for `migrate-view --join-fleet-note` body integrity.
  - Falsifier: after B reconciles, joining pristine bytes with all IDs known should succeed; changing one body byte should then fail specifically at byte reproduction, leave the note unchanged, and register no view. The current ordering cannot distinguish that failure from the earlier unknown-ID failure.
  - Concrete fix: reconcile B (or use a note containing only B-known IDs) before the body-edit control, restore the exact pristine peer bytes afterward, and then perform the successful join. Also test both forbidden flag combinations, not only `--join-fleet-note` with `--publishers-paused`.
- [Nit] **Make the discovery parser explicit.** State that `-z` output is split on NUL, not lines, and that the complete path must full-match `devices/<canonical-uuid>/clio.jsonl`. Add a nested-path and newline-named decoy to test 3. This closes the parsing ambiguity without another Git read, service, or threat-model work.
- [Nit] **Make the final `peer_generated` assertion reach that branch.** If B's render is already byte-identical to one of A's `accepted_hashes`, `checked_view` takes the accepted-hash path and does not record `last_note_repair` (`utils/CLIO/clio-store.py:578-635`). Give A a different currently accepted note/cutoff before presenting B's valid render, then assert `peer_generated` and no archive growth.

Definition-of-done answers:

1. **Yes.** `legacy_coverage` recognizes only `<!-- clio:id:... -->` entries and rejects unrecognized body content when that list is empty (`utils/CLIO/clio-store.py:531-576`). A SQLite-rendered note instead starts its generated body with `# CLIO — recent 168 hours` and uses `clio:record` IDs (`render_markdown`, `utils/CLIO/clio-store.py:712-756`), so normal `migrate_view` registration cannot reconcile it (`utils/CLIO/clio-store.py:638-690`).
2. **Yes, with the parsing clarification above.** The pinned-HEAD read remains within `git_read`'s timeout/deadline seam; the union is bounded before per-origin snapshot reads, and each snapshot retains the existing size, owner, digest, count, identity, and regression checks (`git_read`/`reconcile_fleet`, `utils/CLIO/clio-store.py:912-1020`; `snapshot_records`/`import_snapshot`, `:820-880`). Exact NUL/full-path matching rejects newline and nested decoys. `cat-file blob` reads the committed blob rather than dereferencing a worktree symlink, and its bytes still face snapshot validation. Given the operator-only private repository, no additional trust mechanism is warranted.
3. **Yes.** Opt-in discovery preserves existing configurations by default, while unioning discovered origins with explicit pins retains the deliberate `missing` status for a pinned origin without a snapshot. The upgrade documentation needs finding 1's correction so enabling discovery does not inadvertently change note-repair behavior.
4. **Yes.** Stopping delivery is sufficient under the stated append-only history model: reconciliation imports/updates through the existing snapshot seam and never treats a missing or stopped origin as a deletion instruction (`utils/CLIO/clio-store.py:843-880`). Zero committed changes is within “at most one”; no retirement marker is needed for this requirement.
5. **Yes.** Factoring the existing reproduction check is sound provided it retains unique IDs, canonical cutoff validation, and the existing future-cutoff guard. Known IDs plus exact byte reproduction authenticates the generated body against local SQLite records, while the existing migration path still supplies the private backup, exact header, accepted hashes, and coverage registration. Join must precede repair configuration because repair requires a registered, verified view; the plan has that order right.  [Unverified — no citation]
6. **No architectural requirement is missing and nothing needs cutting.** The only missed operational case is the repair-setting upgrade in finding 1. Discovery, joining, scheduled reconciliation, and rollback all reuse existing seams without a parallel publisher or delivery mechanism.
7. **They are bounded and otherwise well targeted.** Discovery-off is a genuine red control, and bad-origin isolation, pinned-missing behavior, replay, and scheduled publication cover the main risks. Apply finding 2 so the join body control is falsifiable, and the two nits so its parsing and peer-repair assertions are deterministic.

<!-- ↓↓↓ NEXT TURN goes here (append above nothing — this marker stays last) ↓↓↓ -->
