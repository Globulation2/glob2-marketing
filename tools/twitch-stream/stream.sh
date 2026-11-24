#!/usr/bin/env bash
# Capture the stream display and game audio, then send it somewhere.
#   stream.sh file OUT.mp4 [seconds]    record locally, no network (default 20 s)
#   stream.sh test [seconds]            Twitch bandwidth test (?bandwidthtest=true): reaches Twitch, never goes live
#   stream.sh live --i-mean-it          real broadcast to Twitch, until stopped (down.sh or Ctrl-C)
# Video: caption bottom-left, branding (wordmark + domain) bottom-right; see README "Branding overlay".
set -euo pipefail
source "$(dirname "$(readlink -f "$0")")/lib.sh"
mode="${1:-}"; shift || true
case "$mode" in file|test|live) ;; *) sed -n 2,6p "$0"; exit 2 ;; esac
mkdir -p "$LOG_DIR" "$(dirname "$OVERLAY_FILE")"
[[ -f "$OVERLAY_FILE" ]] || printf 'Claude is playing Globulation 2 via MCP' > "$OVERLAY_FILE"
"$RIG_DIR/route-audio.sh"

# --- encoder -----------------------------------------------------------------
pick_encoder() {
  if [[ -n "$STREAM_ENCODER" ]]; then echo "$STREAM_ENCODER"; return; fi
  local encoders; encoders="$(ffmpeg -hide_banner -encoders 2>/dev/null)"  # no grep -q pipe: SIGPIPE + pipefail
  if [[ "$encoders" == *" h264_nvenc "* ]] &&
     ffmpeg -hide_banner -loglevel error -f lavfi -i "color=size=${STREAM_SIZE}:rate=${STREAM_FPS}" \
        -frames:v 1 -c:v h264_nvenc -f null - >/dev/null 2>&1; then
    echo h264_nvenc
  else
    echo libx264
  fi
}
encoder="$(pick_encoder)"
gop=$((STREAM_FPS * 2))
case "$encoder" in
  h264_nvenc) venc=(-c:v h264_nvenc -preset p5 -tune ll -rc cbr -profile:v high -bf 2) ;;
  libx264)    venc=(-c:v libx264 -preset veryfast -tune zerolatency -profile:v high -x264-params nal-hrd=cbr) ;;
  *)          venc=(-c:v "$encoder") ;;
esac
echo "encoder: $encoder" >&2

# --- inputs and filter graph -------------------------------------------------
inputs=(-thread_queue_size 1024 -f x11grab -framerate "$STREAM_FPS" -video_size "$STREAM_SIZE" -draw_mouse 1 -i "$STREAM_DISPLAY"
        -thread_queue_size 1024 -f pulse -ac 2 -ar 48000 -i "$STREAM_SINK.monitor")
scale_px() { echo $(( ($1 * ${STREAM_SIZE#*x} + 540) / 1080 )); }   # sizes are given at 1080p
font=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
graph="[0:v]drawtext=fontfile=$font:textfile=$OVERLAY_FILE:reload=1:expansion=none:fontsize=$(scale_px 26):fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=$(scale_px 10):x=$(scale_px 20):y=h-th-$(scale_px 30)[cap]"
last=cap
if [[ "$BRAND" != 0 ]]; then
  mr=$(scale_px "$BRAND_MARGIN_RIGHT"); mb=$(scale_px "$BRAND_MARGIN_BOTTOM")
  text_block=0
  if [[ -n "$BRAND_TEXT" ]]; then
    fs=$(scale_px "$BRAND_TEXT_SIZE"); pad=$(scale_px 4)
    printf '%s' "$BRAND_TEXT" > "$LOG_DIR/brand-text.txt"   # textfile avoids filter escaping
    graph+=";[$last]drawtext=fontfile=$font:textfile=$LOG_DIR/brand-text.txt:fontsize=$fs:fontcolor=white:box=1:boxcolor=black@0.45:boxborderw=$pad:x=w-tw-$mr-$pad:y=h-th-$mb-${pad}[btext]"
    last=btext; text_block=$((fs + 3 * pad))
  fi
  if [[ -f "$BRAND_LOGO" ]]; then
    inputs+=(-loop 1 -framerate "$STREAM_FPS" -i "$BRAND_LOGO")
    graph+=";[2:v]scale=$(scale_px "$BRAND_WIDTH"):-1,format=rgba,colorchannelmixer=aa=${BRAND_OPACITY}[logo]"
    graph+=";[$last][logo]overlay=x=W-w-$mr:y=H-h-$mb-$text_block:format=auto[blogo]"
    last=blogo
  else
    echo "warning: brand logo $BRAND_LOGO not found; showing text only" >&2
  fi
fi
graph+=";[$last]format=yuv420p[v]"

args=(-hide_banner -loglevel warning -stats "${inputs[@]}"
      -filter_complex "$graph" -map "[v]" -map 1:a
      "${venc[@]}" -b:v "$STREAM_VBITRATE" -maxrate "$STREAM_VBITRATE" -bufsize "$STREAM_VBITRATE"
      -g "$gop" -keyint_min "$gop" -r "$STREAM_FPS"
      -c:a aac -b:a "$STREAM_ABITRATE" -ar 48000)

# --- outputs -----------------------------------------------------------------
# The key is read into a variable and passed to ffmpeg only. ffmpeg prints the full
# ingest URL on connection errors, so its output is filtered to mask the key.
mask() { sed -u "s|$1|<stream-key>|g"; }
key() {
  [[ -s "$TWITCH_KEY_FILE" ]] || { echo "No stream key: install -m 600 /dev/stdin $TWITCH_KEY_FILE" >&2; exit 2; }
  local k; k="$(tr -d ' \n' < "$TWITCH_KEY_FILE")"
  [[ "$k" =~ ^[A-Za-z0-9_]+$ ]] || { echo "Stream key in $TWITCH_KEY_FILE has unexpected characters" >&2; exit 2; }
  printf '%s' "$k"
}
case "$mode" in
  file) out="${1:?output file}"; secs="${2:-20}"
        exec ffmpeg -y "${args[@]}" -t "$secs" "$out" 2> >(tee "$LOG_DIR/file.log" >&2) ;;
  test) secs="${1:-30}"; k="$(key)"
        exec ffmpeg "${args[@]}" -t "$secs" -f flv "$TWITCH_INGEST/$k?bandwidthtest=true" 2> >(mask "$k" | tee "$LOG_DIR/test.log" >&2) ;;
  live) [[ "${1:-}" == "--i-mean-it" ]] || { echo "Refusing to go live without --i-mean-it" >&2; exit 2; }
        k="$(key)"
        echo $$ > "$LOG_DIR/stream.pid"
        exec ffmpeg "${args[@]}" -f flv "$TWITCH_INGEST/$k" 2> >(mask "$k" >> "$LOG_DIR/stream.log") ;;
esac
