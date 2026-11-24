#!/usr/bin/env bash
# Set the caption that ffmpeg reads from the overlay file.
set -e
source "$(dirname "$(readlink -f "$0")")/lib.sh"

if [[ "${1:-}" == --match ]]; then
  shift
  if [[ $# -lt 3 || $# -gt 4 || -z "$1" || -z "$2" || -z "$3" ]]; then
    echo 'Usage: caption.sh --match OPPONENT RECORD GOAL [LAST_MOVE]' >&2
    exit 2
  fi
  printf -v caption 'Claude Plays Glob · vs %s · %s\nGoal: %s' "$1" "$2" "$3"
  if [[ -n "${4:-}" ]]; then
    printf -v caption '%s\nLast move: %s' "$caption" "$4"
  fi
else
  caption="$*"
fi

mkdir -p "$(dirname "$OVERLAY_FILE")"
tmp="$(mktemp "$OVERLAY_FILE.XXXXXX")"
trap 'rm -f "$tmp"' EXIT
printf '%s' "$caption" > "$tmp"
mv "$tmp" "$OVERLAY_FILE"
