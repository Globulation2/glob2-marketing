#!/usr/bin/env bash
# Keep every player transcript for analysis (analysis/), beyond the supervisor's rotation.
# Hard-links new $LOG_DIR/player/match-*.jsonl.gz into $LOG_DIR/player-archive, so the archive
# costs no extra space until the supervisor deletes its copy (about 0.9 MB per match).
# Run every 10 minutes by the glob2-stream-archive timer (autostart/install-autostart.sh).
set -euo pipefail
here="$(dirname "$(readlink -f "$0")")"
# shellcheck source=../lib.sh
source "$here/../lib.sh"
mkdir -p "$LOG_DIR/player-archive"
for f in "$LOG_DIR"/player/match-*.jsonl.gz; do
  [[ -e "$f" ]] || continue
  dest="$LOG_DIR/player-archive/$(basename "$f")"
  # Re-link while the session is still writing (its inode changes when the supervisor gzips it).
  [[ "$f" -ef "$dest" ]] || ln -f "$f" "$dest"
done
