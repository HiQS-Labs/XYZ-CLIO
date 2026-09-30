# CLIO GH3 evidence

Start with `final-gate.json`, `final-approval.json`, `plan-approval.json` and `sqlite-benchmark-final.json`. All five suites passed after final approval on unchanged implementation. Raw `*-final.log` files retain warnings and interpreter skips; synthetic inputs only.

`implementation-evidence.md` records intermediate failures and fixes. Red-control logs are expected failures, not failed final gates. Earlier baseline/focused/benchmark files are historical measurements. Reproduce the frozen corpus with `generate-corpus.py`; data is not committed.

No installed capture, private history, fleet sync or pilot changed. Phase2/3 remain in `doc/gh3-plan.md` and issue3.
