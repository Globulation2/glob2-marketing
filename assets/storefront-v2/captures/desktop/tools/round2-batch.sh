#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Round-2 capture recipes, in gallery order. Run against a capture game that is
# already running (launch-capture-game.sh) with GLOB2_MCP_PORT, GLOB2_MCP_TOKEN_FILE,
# CAPTURE_MATCHES, CAPTURE_WORK and CAPTURE_PROFILE set (see README "Reproduce").
#
# usage: round2-batch.sh OUT_DIR [SHOT ...]     shots: hero build economy battle territory maps opponents coplay
#
# Every shot loads the recipe's checkpoint with a joined player seat (scene.py load
# switches the Health and food bars lens off and clouds off), runs to the recipe
# tick at normal speed, frames the camera, and `scene.py hunt` saves frames only
# while the top bar's workers stat is not negative and the event list has at most
# two rows, each right after an erase of the view's forbidden, clearing and guard
# areas and a check that no zone outline is left.
set -u
T="$(cd "$(dirname "$0")" && pwd)"
OUT="$1"; shift
mkdir -p "$OUT"
SHOTS="${*:-hero build economy battle territory maps opponents coplay}"
PY="uv run -q --with pillow --with numpy python -u"
sc() { python3 "$T/scene.py" "$@"; }
hunt() { timeout 400 $PY "$T/scene.py" hunt "$@"; }

for shot in $SHOTS; do
  echo "== $shot"
  case "$shot" in
  hero)
    sc load marchland 30000 0; sc view 62 114 1.0; sc goto 32900; sc view 62 114 1.0
    hunt "$OUT/hero-marchland" 150 4 4 ;;
  build)
    sc load coral 36000 0; sc goto 40800
    $PY "$T/build-shot.py" school 72 26 1.5 "$OUT/build-coral" --workers 8 --wait 4 --shots 3 ;;
  economy)
    sc load coral 36000 0; sc view 67 21 1.5; sc goto 39800; sc view 67 21 1.5; sc select inn 73 17
    hunt "$OUT/economy-coral" 120 3 6 ;;
  battle)
    sc load honeycomb 66000 0; sc view 67 62 1.5; sc goto 67500; sc view 67 62 1.5
    HUNT_MIN_FREE=-999 hunt "$OUT/battle-honeycomb" 90 3 5 ;;
  territory)
    sc load crater-lakes 54000 0; sc view 24 98 0.75; sc goto 57150; sc view 24 98 0.75
    hunt "$OUT/territory-crater-lakes" 90 3 6 ;;
  maps)
    sc load city-states 42000 2; sc view 92 54 0.875
    hunt "$OUT/maps-city-states" 240 3 4 ;;
  opponents)
    timeout 400 python3 -u "$T/spectator.py" marchland 36000 110 82 "$OUT/opponents-marchland-spectator" 150 3 ;;
  coplay)
    sc load coral 36000 0; sc view 62 56 1.0
    python3 "$T/agent-session.py" "$OUT/coplay-transcript.jsonl" call hive_status '{}'
    python3 "$T/agent-session.py" "$OUT/coplay-transcript.jsonl" call game_world '{"detail":"brief"}' > /dev/null
    python3 "$T/agent-session.py" "$OUT/coplay-transcript.jsonl" install-frontline
    sleep 8
    python3 "$T/agent-session.py" "$OUT/coplay-transcript.jsonl" call hive_program '{"action":"inspect","name":"frontline-flag"}' > /dev/null
    python3 "$T/agent-session.py" "$OUT/coplay-transcript.jsonl" call game_view '{"token":"","x":62,"y":56,"zoom":1.0}' > /dev/null
    sc view 62 56 1.0
    hunt "$OUT/ai-coplay-coral" 120 3 6 ;;
  esac
done
