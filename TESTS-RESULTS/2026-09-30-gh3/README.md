# CLIO GH3 pre-change baseline

All four existing shell suites returned exit0 in the isolated full CLIO clone. Production files remained at a0674039; only plan/recon documents were added. Logs use throwaway HOME and synthetic prompts. The malformed-input jq diagnostic is expected in capture coverage; the explicit duplicate-interpreter SKIP means no second Bash version was tested.

These are **baseline** results, not SQLite implementation or deployed pilot evidence. Relay harness preflight is running separately in a disposable full Forge clone. No plan approval claimed.

The 10,000-row synthetic lookup baseline is in `jsonl-benchmark-baseline.json`. Reproduce the exact input on another computer with `python3 TESTS-RESULTS/2026-09-30-gh3/generate-corpus.py /tmp/clio-benchmark.jsonl` (output must not already exist). Its SHA256 was checked against the baseline receipt. Query filters/order, result count/hash and all seven timings are in the receipt. No SQLite speedup is claimed yet.
