#!/bin/sh
# Run one headless AI match with periodic save states.
# usage: run-match.sh OUTPUT_DIR MAP_FILE GAME_SEED TICKS SAVE_EVERY AI [AI ...]
set -eu
GLOB2="${GLOB2:-/Applications/Glob2.app/Contents/MacOS/glob2}"
out="$1"; map="$2"; seed="$3"; ticks="$4"; every="$5"; shift 5
players=""
for ai in "$@"; do players="$players --player $ai"; done
# --win-probability 0 plays the match out instead of stopping at a predicted win.
exec "$GLOB2" game run --map-file "$map" --game-seed "$seed" $players \
  --ticks "$ticks" --win-probability 0 --save "every:$every" --save final \
  --telemetry team-timeline --compute-threads 2 --output-dir "$out"
