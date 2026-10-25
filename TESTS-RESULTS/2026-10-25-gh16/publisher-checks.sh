#!/bin/bash
# GH-16 publisher checks a–i in disposable clones. Usage: publisher-checks.sh <XYZ-CLIO task clone> <rebalanceOS checkout>
set -uo pipefail
TASK=$(cd "$1" && pwd); UPSRC=$(cd "$2" && pwd)
W=$(mktemp -d "${TMPDIR:-/tmp}/gh16chk.XXXXXX") && [ -d "$W" ] || { echo "mktemp failed" >&2; exit 1; }
trap 'rm -rf "${W:?}"' EXIT
q() { "$@" >/dev/null 2>&1; }
BARE="$W/HiQS-Labs/rebalanceOS.git"; mkdir -p "$W/HiQS-Labs"
q git clone --bare "$UPSRC" "$BARE"
q git clone "$BARE" "$W/src"; git -C "$W/src" checkout -q development
q git clone "$TASK" "$W/xyz"; git -C "$W/xyz" checkout -q -b test-pub
P="$W/xyz/scripts/publish-from-rebalance.sh"
run() { out=$(bash "$P" "$@" 2>&1); rc=$?; }
say() { printf '%-4s %s\n' "$1" "$2"; }

touch "$W/src/utils/CLIO/dirty.tmp"; run "$W/src"; say a "dirty source: exit=$rc ($(printf '%s' "$out" | tail -1))"; rm -f "$W/src/utils/CLIO/dirty.tmp"
for u in https://github.com/HiQS-Labs/rebalanceOS-fork.git https://github.com/Someone/rebalanceOS.git https://attacker.invalid/HiQS-Labs/rebalanceOS.git; do
  git -C "$W/src" remote set-url origin "$u"; run "$W/src"; say a2 "origin $u: exit=$rc"; done
git -C "$W/src" remote set-url origin "$BARE"
git -C "$W/src" checkout -q -b unmerged; echo x >> "$W/src/test/fixtures/clio/codex-rollout.jsonl"; q git -C "$W/src" commit -qam unmerged
run "$W/src"; say b "unmerged source HEAD: exit=$rc ($(printf '%s' "$out" | tail -1))"; git -C "$W/src" checkout -q development
git -C "$W/xyz" checkout -q -b main; run "$W/src" --apply; say c "--apply on main: exit=$rc ($(printf '%s' "$out" | tail -1))"; git -C "$W/xyz" checkout -q test-pub
ls "$W/src/utils/CLIO/README.md" "$W/src/utils/CLIO/LICENSE" >/dev/null && say d0 "source has utils/CLIO/README.md and LICENSE"
run "$W/src"; say d "preview: exit=$rc $(printf '%s' "$out" | tail -1)"
base=$(git -C "$W/xyz" rev-parse HEAD); run "$W/src" --apply
say d "apply: exit=$rc; commit files: $(git -C "$W/xyz" diff --name-only "$base" HEAD | tr '\n' ' '); README/LICENSE here: $(ls "$W/xyz/utils/CLIO/README.md" "$W/xyz/utils/CLIO/LICENSE" 2>/dev/null | wc -l | tr -d ' '); status lines: $(git -C "$W/xyz" status --porcelain | wc -l | tr -d ' ')"
run --check; say e "--check: exit=$rc ($out)"
printf ' ' >> "$W/xyz/utils/CLIO/INSTALL.md"; run --check; say f "byte edit INSTALL.md: exit=$rc ($(printf '%s' "$out" | grep -o 'changed: .*' | head -1))"; git -C "$W/xyz" checkout -q -- utils/CLIO/INSTALL.md
for stray in utils/CLIO/extra.sh test/clio-extra.sh test/fixtures/clio/extra.jsonl; do
  : > "$W/xyz/$stray"; run --check; say g "stray $stray: exit=$rc ($(printf '%s' "$out" | grep -o 'not published: .*' | head -1))"; rm -f "$W/xyz/$stray"; run --check; say g "  restored: exit=$rc"; done
rm "$W/xyz/test/fixtures/clio/agy-transcript.jsonl"; run --check; say g "deleted fixture: exit=$rc ($(printf '%s' "$out" | grep -o 'missing: .*' | head -1))"; git -C "$W/xyz" checkout -q -- test/fixtures/clio/agy-transcript.jsonl; run --check; say g "  restored: exit=$rc"
h0=$(git -C "$W/xyz" rev-parse HEAD); out=$(CLIO_PUBLISH_DATE=2099-01-01 bash "$P" "$W/src" --apply 2>&1); rc=$?
say h "rerun, later date: exit=$rc ($out); new commit: $([ "$h0" = "$(git -C "$W/xyz" rev-parse HEAD)" ] && echo no || echo YES); status lines: $(git -C "$W/xyz" status --porcelain | wc -l | tr -d ' ')"
q git clone "$BARE" "$W/pusher"; git -C "$W/pusher" checkout -q development
orig=$(shasum -a 256 < "$W/xyz/test/fixtures/clio/codex-rollout.jsonl")
echo '{"synthetic":"upstream change"}' >> "$W/pusher/test/fixtures/clio/codex-rollout.jsonl"; q git -C "$W/pusher" commit -qam "upstream fixture change"; q git -C "$W/pusher" push -q origin development
q git -C "$W/src" pull -q --ff-only; run "$W/src"; say i "preview after upstream change: exit=$rc; listed: $(printf '%s' "$out" | grep -v '^source:' | tr '\n' ' ')"
i0=$(git -C "$W/xyz" rev-parse HEAD); run "$W/src" --apply; say i "apply: exit=$rc; commit files: $(git -C "$W/xyz" diff --name-only "$i0" HEAD | tr '\n' ' ')"
run --check; say i "--check: exit=$rc"
q git -C "$W/pusher" revert --no-edit HEAD; q git -C "$W/pusher" push -q origin development; q git -C "$W/src" pull -q --ff-only
run "$W/src" --apply; say i "after upstream revert, apply: exit=$rc; fixture back to original bytes: $([ "$orig" = "$(shasum -a 256 < "$W/xyz/test/fixtures/clio/codex-rollout.jsonl")" ] && echo yes || echo NO)"
(cd "$W/xyz" && unset CLIO_MIN_PROMPT_CHARS && for t in clio-capture clio-exporter clio-codex-tail clio-agy-tail; do bash test/$t.sh >/dev/null 2>&1; echo "suite test/$t.sh: exit=$?"; done; python3 test/clio-store.py >/dev/null 2>&1; echo "suite test/clio-store.py: exit=$? (1 = known date-dependent case)")
