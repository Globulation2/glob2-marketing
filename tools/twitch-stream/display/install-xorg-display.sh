#!/usr/bin/env bash
# Install (or remove) a headless X server on the NVIDIA GPU for the stream display.
#
#   display/install-xorg-display.sh              install or update (idempotent)
#   display/install-xorg-display.sh --uninstall  stop and remove it
#
# Why: on Xvfb the game can't hand GPU frames to the X server (no DRI3), so every frame goes
# through a slow CPU copy and the game drew about 12 fps (measured 2026-11-24). A headless Xorg
# on NVIDIA's own X driver presents natively: the game held 60 fps and x11grab captures it.
# Needs NVIDIA's X driver (Ubuntu: xserver-xorg-video-nvidia-<version> matching the kernel
# module). It runs as a system service on STREAM_DISPLAY, with no outputs and no input devices,
# and doesn't switch VTs, so the desktop session is unaffected. Then set
# STREAM_DISPLAY_BACKEND=xorg in stream.env. Settings: STREAM_DISPLAY, STREAM_SIZE, STREAM_XAUTHORITY.
set -euo pipefail
here="$(dirname "$(readlink -f "$0")")"
# shellcheck source=../lib.sh
source "$here/../lib.sh"
operator="$(id -un)"
[[ "$operator" != root ]] || { echo "run as the operator account, not root" >&2; exit 2; }
S() { sudo -n "$@"; }
S true 2>/dev/null || { echo "needs sudo (run 'sudo -v' first)" >&2; exit 2; }
unit=glob2-stream-xorg.service
conf=/etc/X11/glob2-stream-xorg.conf
log=/var/log/glob2-stream-xorg.log
n="${STREAM_DISPLAY#:}"

if [[ "${1:-}" == --uninstall ]]; then
  S systemctl disable --now "$unit" 2>/dev/null || true
  S rm -f "/etc/systemd/system/$unit" "$conf"
  S systemctl daemon-reload
  rm -f "$STREAM_XAUTHORITY"
  echo "removed the stream X server; set STREAM_DISPLAY_BACKEND=xvfb in stream.env"
  exit 0
fi
[[ -z "${1:-}" ]] || { sed -n 2,5p "$0"; exit 2; }

drv="$(find /usr/lib -name nvidia_drv.so -print -quit 2>/dev/null || true)"
[[ -n "$drv" ]] || { echo "NVIDIA's X driver (nvidia_drv.so) isn't installed; install xserver-xorg-video-nvidia-<version>" >&2; exit 1; }
bus="$(nvidia-smi --query-gpu=pci.bus_id --format=csv,noheader | head -1)"   # 00000000:01:00.0
[[ -n "$bus" ]] || { echo "nvidia-smi found no GPU" >&2; exit 1; }
IFS=':.' read -r _ b d f <<<"$bus"
busid="PCI:$((16#$b)):$((16#$d)):$((16#$f))"
w="${STREAM_SIZE%x*}"; h="${STREAM_SIZE#*x}"

tmp="$(mktemp)"; trap 'rm -f "$tmp"' EXIT
cat > "$tmp" <<CONF
# Written by install-xorg-display.sh: headless X screen on the NVIDIA GPU for the stream.
Section "ServerFlags"
    Option "AutoAddGPU" "false"
    Option "AutoAddDevices" "false"
    Option "AutoEnableDevices" "false"
    Option "AllowMouseOpenFail" "true"
    Option "DontVTSwitch" "true"
EndSection
Section "Files"
    ModulePath "$(dirname "$drv")"
    ModulePath "/usr/lib/xorg/modules"
EndSection
Section "Device"
    Identifier "nvidia"
    Driver "nvidia"
    BusID "$busid"
    Option "AllowEmptyInitialConfiguration" "true"
    Option "UseDisplayDevice" "None"
EndSection
Section "Screen"
    Identifier "stream"
    Device "nvidia"
    DefaultDepth 24
    SubSection "Display"
        Depth 24
        Virtual $w $h
    EndSubSection
EndSection
Section "ServerLayout"
    Identifier "stream"
    Screen "stream"
EndSection
CONF
S install -o root -g root -m 644 "$tmp" "$conf"

# Auth cookie: only the operator (and root) may connect.
mkdir -p "$(dirname "$STREAM_XAUTHORITY")"
if ! xauth -f "$STREAM_XAUTHORITY" list ":$n" 2>/dev/null | grep -q .; then
  : > "$STREAM_XAUTHORITY"; chmod 600 "$STREAM_XAUTHORITY"
  xauth -q -f "$STREAM_XAUTHORITY" add ":$n" . "$(mcookie)"
fi

cat > "$tmp" <<UNIT
# Written by install-xorg-display.sh: the stream's headless NVIDIA X server.
[Unit]
Description=Claude Plays Glob: headless NVIDIA X server on :$n
After=systemd-user-sessions.service

[Service]
ExecStart=/usr/lib/xorg/Xorg :$n -config $(basename "$conf") -auth $STREAM_XAUTHORITY -nolisten tcp -noreset -sharevts -novtswitch -logfile $log
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
UNIT
S install -o root -g root -m 644 "$tmp" "/etc/systemd/system/$unit"
S systemctl daemon-reload
# Xvfb may still hold the display number from the old backend.
xp="$(pgrep -x -f "Xvfb $STREAM_DISPLAY .*" || true)"
[[ -z "$xp" ]] || { kill "$xp"; sleep 1; echo "stopped Xvfb on $STREAM_DISPLAY"; }
S systemctl enable "$unit" >/dev/null 2>&1
S systemctl restart "$unit"
for _ in $(seq 50); do XAUTHORITY="$STREAM_XAUTHORITY" xdpyinfo -display "$STREAM_DISPLAY" >/dev/null 2>&1 && break; sleep 0.2; done
XAUTHORITY="$STREAM_XAUTHORITY" xdpyinfo -display "$STREAM_DISPLAY" >/dev/null 2>&1 || { echo "X server didn't come up; see $log" >&2; exit 1; }
echo "stream X server up on $STREAM_DISPLAY ($busid, ${w}x$h). Set STREAM_DISPLAY_BACKEND=xorg in stream.env."
