#!/usr/bin/env bash
# Wait (up to WAIT_READY_SECONDS, default 180) until the stream display and the user's audio server
# are up; used before the supervisor starts at boot. Exit 1 on timeout so systemd retries.
set -uo pipefail
source "$(dirname "$(readlink -f "$0")")/../lib.sh"
deadline=$((SECONDS + ${WAIT_READY_SECONDS:-180}))
until pactl info >/dev/null 2>&1; do
  (( SECONDS < deadline )) || { echo "audio server not ready" >&2; exit 1; }; sleep 2
done
if [[ "$STREAM_DISPLAY_BACKEND" == xorg ]]; then
  until xdpyinfo -display "$STREAM_DISPLAY" >/dev/null 2>&1; do
    (( SECONDS < deadline )) || { echo "stream X server $STREAM_DISPLAY not ready" >&2; exit 1; }; sleep 2
  done
fi
echo "ready: audio and display $STREAM_DISPLAY ($STREAM_DISPLAY_BACKEND)"
