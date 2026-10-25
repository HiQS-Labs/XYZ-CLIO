#!/usr/bin/env bash
# publish-from-rebalance.sh — publish CLIO from its upstream, HiQS-Labs/rebalanceOS utils/CLIO (GH-16).
#
#   publish-from-rebalance.sh <rebalanceOS checkout>           preview what would change (default)
#   publish-from-rebalance.sh <rebalanceOS checkout> --apply   copy + commit on the current non-main branch
#   publish-from-rebalance.sh --check                          verify the published files match utils/CLIO/UPSTREAM
#
# Published set: utils/CLIO/* except README.md, LICENSE and UPSTREAM; test/clio-*; test/fixtures/clio/*.
# Within those scopes the copy mirrors the source (files removed upstream are removed here).
# Never pushes. Exit: 0 ok · 1 --check found drift · 2 refused (usage, source or target not eligible).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RECORD="utils/CLIO/UPSTREAM"
die() { echo "publish-from-rebalance: $*" >&2; exit 2; }

published_files() { # $1 = tree root; prints the published set, sorted, one relative path per line
  ( cd "$1" && {
      find utils/CLIO -maxdepth 1 -type f ! -name README.md ! -name LICENSE ! -name UPSTREAM 2>/dev/null
      find test -maxdepth 1 -type f -name 'clio-*' 2>/dev/null
      find test/fixtures/clio -type f 2>/dev/null
    } | LC_ALL=C sort )
}
irregular() { # $1 = tree root; prints any non-regular, non-directory entry (e.g. a symlink) in the published scopes
  ( cd "$1" && {
      find utils/CLIO -maxdepth 1 ! -type f ! -type d 2>/dev/null
      find test -maxdepth 1 -name 'clio-*' ! -type f ! -type d 2>/dev/null
      find test/fixtures/clio ! -type f ! -type d 2>/dev/null
    } | LC_ALL=C sort )
}
manifest() { # $1 = tree root; "<sha256>  <path>" per published file
  published_files "$1" | while IFS= read -r f; do (cd "$1" && shasum -a 256 "$f"); done
}

if [ "${1:-}" = --check ]; then
  [ -f "$ROOT/$RECORD" ] || { echo "publish-from-rebalance: no $RECORD; nothing has been published yet" >&2; exit 1; }
  rev=$(awk '$1 == "revision:" {print substr($2, 1, 12)}' "$ROOT/$RECORD")
  odd=$(irregular "$ROOT")
  if [ -n "$odd" ]; then
    printf '%s\n' "$odd" | sed 's/^/  not a regular file: /' >&2
    echo "publish-from-rebalance: CLIO differs from HiQS-Labs/rebalanceOS@$rev; edit upstream, then publish" >&2; exit 1
  fi
  diff <(grep -E '^[0-9a-f]{64}  ' "$ROOT/$RECORD") <(manifest "$ROOT") > /dev/null && {
    echo "CLIO matches HiQS-Labs/rebalanceOS@$rev ($(grep -cE '^[0-9a-f]{64}  ' "$ROOT/$RECORD") files)"; exit 0; }
  echo "publish-from-rebalance: CLIO differs from HiQS-Labs/rebalanceOS@$rev; edit upstream, then publish:" >&2
  diff <(grep -E '^[0-9a-f]{64}  ' "$ROOT/$RECORD" | sed 's/^[0-9a-f]*  //') <(published_files "$ROOT") | sed -n 's/^< /  missing: /p; s/^> /  not published: /p' >&2 || true
  # Records are "<64-hex>  <path>": compare by the full path suffix, so names with spaces stay whole.
  awk 'NR == FNR { h[substr($0, 67)] = substr($0, 1, 64); next }
       (substr($0, 67) in h) && h[substr($0, 67)] != substr($0, 1, 64) { print "  changed: " substr($0, 67) }' \
    <(grep -E '^[0-9a-f]{64}  ' "$ROOT/$RECORD") <(manifest "$ROOT") >&2
  exit 1
fi

SRC="${1:-}"; APPLY=0
[ -n "$SRC" ] || die "usage: publish-from-rebalance.sh <rebalanceOS checkout> [--apply] | --check"
[ "${2:-}" = "" ] || [ "${2:-}" = --apply ] || die "unknown option: $2"
[ "${2:-}" = --apply ] && APPLY=1
SRC="$(cd "$SRC" 2>/dev/null && pwd)" || die "not a directory: $1"

# Source: the canonical upstream, clean, and its HEAD merged into origin/development.
url=$(git -C "$SRC" remote get-url origin 2>/dev/null) || die "$SRC is not a git checkout with an origin"
# GitHub https/ssh forms of the upstream, or an absolute local mirror path; any other host or name is refused.
[[ "$url" =~ ^(https://github\.com/|git@github\.com:|ssh://git@github\.com/|/.+/)HiQS-Labs/rebalanceOS(\.git)?$ ]] \
  || die "origin is $url, not HiQS-Labs/rebalanceOS"
[ -z "$(git -C "$SRC" status --porcelain)" ] || die "source checkout has uncommitted changes"
git -C "$SRC" fetch -q origin development || die "could not fetch origin development in $SRC"
git -C "$SRC" merge-base --is-ancestor HEAD origin/development || die "source HEAD is not merged into origin/development"
srev=$(git -C "$SRC" rev-parse HEAD)

# Publish exactly the committed bytes and modes at that revision, never untracked or ignored files.
EXP=$(mktemp -d "${TMPDIR:-/tmp}/clio-publish.XXXXXX") && [ -d "$EXP" ] || die "mktemp failed"
trap 'rm -rf "${EXP:?}"' EXIT
git -C "$SRC" archive "$srev" utils/CLIO test | tar -x -C "$EXP" || die "could not export $srev"
mkdir -p "$EXP/test/fixtures/clio" "$ROOT/test/fixtures/clio"
odd=$(irregular "$EXP")
[ -z "$odd" ] || die "source revision has non-regular files in the published set: $odd"

# The same rsync drives preview and apply: three scopes, mirror within them, content (checksum) and
# modes compared, never mtimes, so a preview lists only real changes.
# utils/CLIO and test/ copy top-level files only, matching published_files.
sync() { # $@ = extra rsync flags
  rsync -rlp --checksum --itemize-changes --delete "$@" \
    --exclude README.md --exclude LICENSE --exclude UPSTREAM --exclude '*/' "$EXP/utils/CLIO/" "$ROOT/utils/CLIO/" | sed 's#^#utils/CLIO/ #'
  rsync -rlp --checksum --itemize-changes --delete "$@" --include 'clio-*' --exclude '*/' --exclude '*' "$EXP/test/" "$ROOT/test/" | sed 's#^#test/ #'
  rsync -rlp --checksum --itemize-changes --delete "$@" "$EXP/test/fixtures/clio/" "$ROOT/test/fixtures/clio/" | sed 's#^#test/fixtures/clio/ #'
}

if [ "$APPLY" = 0 ]; then
  echo "source: HiQS-Labs/rebalanceOS@${srev:0:12}"
  # Keep only real changes: a transfer (>, c, h), a deletion, or a permission change (column 6 = p).
  changes=$(sync --dry-run | awk '$2 ~ /^(\*deleting|[<>ch]|.....p)/' || true)
  [ -n "$changes" ] && printf '%s\n' "$changes" || echo "no CLIO content changes"
  exit 0
fi

branch=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)
[ "$branch" != main ] || die "refusing to publish on main; create a branch first"
[ -z "$(git -C "$ROOT" status --porcelain)" ] || die "this checkout has uncommitted changes"
sync >/dev/null

new_manifest=$(manifest "$ROOT")
old_body=$( [ -f "$ROOT/$RECORD" ] && grep -vE '^published: ' "$ROOT/$RECORD" || true)
body=$(printf '%s\n' \
  "# Published from the CLIO upstream. Do not edit utils/CLIO/ or the CLIO tests here:" \
  "# change HiQS-Labs/rebalanceOS utils/CLIO first, then run scripts/publish-from-rebalance.sh." \
  "source: HiQS-Labs/rebalanceOS" "revision: $srev" "$new_manifest")
if [ "$body" = "$old_body" ]; then
  echo "no changes: already published from HiQS-Labs/rebalanceOS@${srev:0:12}"; exit 0
fi
{ printf '%s\n' "$body" | sed -n '1,4p'; echo "published: ${CLIO_PUBLISH_DATE:-$(date +%Y-%m-%d)}"; printf '%s\n' "$body" | sed '1,4d'; } > "$ROOT/$RECORD"
# Stage exactly the published list (plus deletions inside the scopes) and prove nothing else moved.
published_files "$ROOT" | tr '\n' '\0' | (cd "$ROOT" && xargs -0 git add -- "$RECORD")
git -C "$ROOT" add -u -- utils/CLIO test
git -C "$ROOT" commit -q -m "publish: CLIO from HiQS-Labs/rebalanceOS@${srev:0:12}"
left=$(git -C "$ROOT" status --porcelain)
[ -z "$left" ] || die "unexpected changes after publishing (left uncommitted): $left"
echo "committed on $branch: CLIO from HiQS-Labs/rebalanceOS@${srev:0:12} (not pushed)"
