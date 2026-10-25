#!/bin/bash
# GH-13 check b4: two contenders that both see a stale lock race through the reaper block
# extracted from a tailer (A and B released together by a barrier after the first lock_stale).
# Usage: b4-reaper-race-probe.sh <tailer script> [red]   ("red" runs the unserialized rm/mkdir block)
set -uo pipefail
blk=$(awk '/^lock_stale\(\)/,/^fi$/' "$1")
[ "${2:-}" = red ] && blk='lock_stale() { born=$(cat "$TAIL_LOCK/born"); [ $(( $(date +%s) - born )) -gt 300 ]; }
if ! mkdir "$TAIL_LOCK" 2>/dev/null; then
  lock_stale || exit 0
  diag "reaped"; rm -rf "$TAIL_LOCK"; mkdir "$TAIL_LOCK" 2>/dev/null || exit 0
fi'
P=$(mktemp -d "${TMPDIR:-/tmp}/b4.XXXXXX"); ok=0
for i in $(seq 1 30); do
  rm -rf "$P"/*; mkdir "$P/lock"; echo 1 > "$P/lock/born"
  for tag in A B; do ( TAIL_LOCK="$P/lock"; diag(){ echo "$tag $*" >> "$P/diag"; }
    eval "$(printf '%s' "$blk" | sed 's/^  lock_stale || exit 0$/  lock_stale || exit 0; while [ ! -f "$P\/go" ]; do :; done/')"
    echo $tag > "$TAIL_LOCK/born"; echo $tag >> "$P/owners" ) & done
  sleep 0.2; : > "$P/go"; wait
  [ "$(grep -c reaped "$P/diag")" = 1 ] && [ "$(wc -l < "$P/owners" | tr -d ' ')" = 1 ] && ok=$((ok+1))
done
rm -rf "$P"; echo "iterations-with-single-reap-and-single-owner=$ok/30"
