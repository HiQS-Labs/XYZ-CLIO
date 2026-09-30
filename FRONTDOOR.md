# CLIO front door

How hard is it for someone with zero context to get CLIO running? This board tracks that,
and every status on it is backed by a command in [Deterministic checks](#deterministic-checks--re-run-to-refresh)
— nothing here is merely asserted. Refresh it after any change to `README.md`,
`utils/CLIO/INSTALL.md`, the bundled scripts, or the repo's top-level layout: run the
checks block from the repo root and flip any finding whose check has gone silent.

| | |
| --- | --- |
| **Last audited** | 2026-09-30 — GH-3 opt-in SQLite; same-path revision: plan approved, focused16-case storage/exporter checks passed; revised final review/gate pending |
| **Method** | `/frontdoor` walk (7 dimensions) + `/shakedown` static audit and live harness |
| **Verdict** | ⚠️ **Bumpy** — a newcomer with an AI agent reaches a captured prompt in ~10 minutes with no account, key, or payment required; two low-severity gaps remain, none blocking |
| **Remediation plan** | [`SHAKEDOWN/2026-09-01/clio-1652.md`](SHAKEDOWN/2026-09-01/clio-1652.md) — the path-resolution audit and its patch |

## Health at a glance

| Dimension | | Note |
| --- | --- | --- |
| One front door | ✅ | Root `README.md` is the only overview; `utils/CLIO/INSTALL.md` is the only install procedure. The competing skill-local README was removed. |
| 🔑 Leaked secrets | ✅ | No live-looking credential in the tree. Fixtures are synthetic prompt text. |
| Install path | ✅ | Resolves from a checkout *or* an installed skill dir via `CLIO_SRC`; `jq` and `python3` are declared. |
| Execution environment | ⚠️ | macOS/Linux only, stated up front. A sandboxed agent may be blocked from `launchctl` and from the git credential helper — see FD-06. |
| Auth & access | ✅ | No hoops at all: no account, API key, OAuth, paid tier, or admin grant. Everything is local. |
| First success | ⚠️ | The install block ends in a smoke test that prints a captured row, but there is no troubleshooting path when it prints nothing — FD-05. |
| Doc ↔ code drift | ✅ | One overview, one install doc, and the writer plus both shims are extracted from `INSTALL.md` by the tests, so they cannot drift from what is exercised. |

## Findings

| ID | Area | Sev | Status | Fix |
| --- | --- | --- | --- | --- |
| FD-01 | Install path | 🔴 | ✅ FIXED | `install -m 0755 utils/CLIO/<script>.sh` was CWD-relative and had no referent once CLIO was installed as the `clio` skill. Replaced with a `CLIO_SRC` resolver that covers both layouts. |
| FD-02 | One front door | 🟠 | ✅ FIXED | `utils/CLIO/README.md` competed with the root `README.md` — same `# CLIO` title, overlapping Why and Requirements. Removed; the root README is canonical. |
| FD-03 | Doc ↔ code drift | 🟠 | ✅ FIXED | The skill-local README advertised a 5-minute `launchd` schedule where the root README and `INSTALL.md` say 1 minute, framed CLIO as Claude-only, and omitted `python3`. Resolved by FD-02. |
| FD-04 | First success | 🔴 | ✅ FIXED | `clio-agy-tail.sh` printed its summary to stderr while its Codex twin used stdout, so `test/clio-agy-tail.sh` failed on its first assertion and the rest of its cases never ran. Aligned to stdout. |
| FD-05 | First success | 🟡 | ⬜ OPEN | No troubleshooting section. When the smoke test prints nothing, the newcomer has no documented next move (check `~/.claude/prompt-log-errors.log`, confirm the `settings.json` registration, confirm the prompt cleared `CLIO_MIN_PROMPT_CHARS`). Add `## Troubleshooting` to `INSTALL.md`. |
| FD-06 | Install path | 🟡 | ⬜ OPEN | The Agy scheduling step is prose only — "schedule it like the Codex tailer" — where every other step is copy-pasteable. Give Agy its own plist block. |
| FD-07 | Repo hygiene | 🟡 | ✅ FIXED | `.gitignore` excludes local databases, pending receipts, bytecode and scratch output. |

## Verified baselines (keep green)

| ID | Baseline | Why it matters |
| --- | --- | --- |
| BL-01 | No live-looking secret in the tree | CLIO logs prompt text; a credential landing here would be a stop-everything finding. |
| BL-02 | The writer and Claude shim heredoc markers are intact in `INSTALL.md` | The test harnesses extract them by marker. If a marker moves, the tests stop exercising the shipped code — and they fail loudly rather than silently passing. |
| BL-03 | Both tailers reach the writer by absolute path | `$HOME/.claude/hooks/clio-capture.sh`, not a relative path — this is what makes them CWD-robust wherever `launchd` starts them. |
| BL-04 | Five test harnesses present and referenced by the README | The README's Tests section lists exactly what exists. |

**Recorded suite state (updated by hand, never auto-derived):** 2026-09-30 final
gate passed after relay approval: four shell suites and 12 SQLite cases. Evidence:
`TESTS-RESULTS/2026-09-30-gh3/final-gate.json`. Python fixture ResourceWarnings and
same-interpreter duplicate skips remain in logs; no failed assertions.
Re-run them yourself after changes; this board does not execute them.

## Deterministic checks — re-run to refresh

Run from the repo root. **Empty output means every finding above is closed and every
baseline is green. Any printed line names something that is open.** These checks are
read-only — `grep` and `test` only. They never run CLIO's scripts, its installer, or its
test suite.

```bash
# --- open findings ----------------------------------------------------------
grep -q 'install -m 0755 utils/CLIO/' utils/CLIO/INSTALL.md \
  && echo "FD-01 OPEN: install command is still CWD-relative (utils/CLIO/ prefix)"
grep -q 'CLIO_SRC' utils/CLIO/INSTALL.md \
  || echo "FD-01 OPEN: the CLIO_SRC resolver is missing from INSTALL.md"
test -f utils/CLIO/README.md \
  && echo "FD-02 OPEN: a second, skill-local README is back alongside the root one"
stale=$(grep -rl '5-minute `launchd`' --include='*.md' . 2>/dev/null \
  | grep -v -e '^\./SHAKEDOWN/' -e '^\./FRONTDOOR\.md$')
[ -n "$stale" ] && echo "FD-03 OPEN: a doc still advertises the 5-minute schedule: $stale"
grep -q 'clio-agy-tail: delivered=.*>&2' utils/CLIO/clio-agy-tail.sh \
  && echo "FD-04 OPEN: the agy tailer summary went back to stderr; its harness will fail"
grep -qi '^## Troubleshooting' utils/CLIO/INSTALL.md \
  || echo "FD-05 OPEN: INSTALL.md has no troubleshooting section"
grep -q 'Then schedule it like the Codex tailer' utils/CLIO/INSTALL.md \
  && echo "FD-06 OPEN: the Agy scheduling step is still prose, not a copy-pasteable block"
test -f .gitignore \
  || echo "FD-07 OPEN: no .gitignore at the repo root"

# --- baselines (must stay green) --------------------------------------------
# Reports the file and line only — never the matched value.
grep -rlE 'sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY' \
  --exclude-dir=.git --exclude-dir=SHAKEDOWN --exclude=FRONTDOOR.md . 2>/dev/null \
  | while read -r f; do
      echo "BL-01 FAILED: possible live credential in $f (value withheld) — rotate it at the provider FIRST, then purge history"
    done
grep -q '^cat > ~/.claude/hooks/clio-capture.sh << .EOF.$' utils/CLIO/INSTALL.md \
  || echo "BL-02 FAILED: the clio-capture.sh heredoc marker moved; test/clio-capture.sh can no longer extract it"
grep -q '^cat > ~/.claude/hooks/log-prompt.sh << .EOF.$' utils/CLIO/INSTALL.md \
  || echo "BL-02 FAILED: the log-prompt.sh heredoc marker moved; test/clio-capture.sh can no longer extract it"
for t in clio-codex-tail clio-agy-tail; do
  grep -q 'WRITER="\$HOME/.claude/hooks/clio-capture.sh"' "utils/CLIO/$t.sh" \
    || echo "BL-03 FAILED: $t.sh no longer reaches the writer by absolute path"
done
for t in clio-capture clio-exporter clio-codex-tail clio-agy-tail; do
  test -f "test/$t.sh" || echo "BL-04 FAILED: test/$t.sh is missing"
  grep -q "bash test/$t.sh" README.md || echo "BL-04 FAILED: README does not list test/$t.sh"
done
test -f test/clio-store.py || echo "BL-04 FAILED: test/clio-store.py is missing"
grep -q "python3 test/clio-store.py" README.md || echo "BL-04 FAILED: README does not list SQLite suite"
```

## The hoops

None. CLIO needs no account, no API key, no OAuth consent, no paid tier, and no admin
grant — it reads local files and writes to your home directory. The only prerequisites
are `jq` and, for the two tailers and SQLite mode, `python3`.

The one environment caveat is not CLIO's: an AI agent running in a sandbox may be unable
to reach the OS keychain or run `launchctl`, so the scheduling steps and any `git push`
may need to run outside it. That surfaces as a misleading credential error, not as a
permissions message.
