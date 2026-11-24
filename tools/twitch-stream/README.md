# Twitch stream rig

[Twitch streaming record](../../planning/twitch-streaming.md) · [Planning index](../../planning/README.md) · [Glob2 MCP guide](https://github.com/Globulation2/glob2/blob/master/docs/development/mcp-ui-server.md)

The Linux rig for streaming Claude playing Globulation 2 to Twitch. Claude drives the game through the game's embedded MCP server. The game runs on a hidden virtual display, so the streaming machine's desktop stays usable. ffmpeg captures that display and the game's sound and sends them to Twitch.

**Streaming?** Follow the [stream playbook](stream-playbook.md) for match format, camera, narration, fair play and the learning loop. The [Twitch streaming record](../../planning/twitch-streaming.md#broadcast-setup-and-verification) tracks what this rig has verified.

This directory holds code only. The stream key, game profile, logs and settings live outside the repository in `$GLOB2_STREAM_HOME` (default `~/glob2-stream`) and `~/.config/glob2-stream/`.

## How it works

```text
                Claude Code ──MCP (stdio)──> tools/mcp_stdio.py ──HTTP 127.0.0.1:27300──┐
                                                                                         v
 Xvfb :99 (1920x1080) <── window ── glob2 play --mcp-port 27300 --renderer sdl-gpu
        │                                │  Vulkan renders on the real GPU and presents into Xvfb
        │                                └─ audio ──> null sink "glob2_stream" (Pulse/PipeWire)
        v                                                   │ .monitor
 ffmpeg x11grab ──┬─ drawtext caption, bottom-left (overlay/caption.txt)
                  ├─ branding, bottom-right (assets/glob2-wordmark.png + "glob2.online")
                  └─ pulse input <──────────────────────────┘
        │
        └─ h264_nvenc (or libx264) + AAC ── FLV/RTMP ──> rtmp://live.twitch.tv/app/<key>
```

- **Display.** Xvfb provides an invisible X display. OpenGL there would be llvmpipe (software), so the game uses its `sdl-gpu` renderer. Vulkan can present into Xvfb while rendering on the machine's GPU.
- **Audio.** A null sink receives only the stream game's audio, and ffmpeg records its monitor. Desktop sounds and other games never reach the stream.
- **Encoding.** NVIDIA NVENC is used when it works, otherwise x264 on the CPU. 1080p30, 4500 kbps CBR, 2-second keyframes and 160 kbps AAC match Twitch's ingest guidance.
- **Caption.** A bottom-left text box shows match context or an intermission message from `caption.sh`. ffmpeg reloads it during capture.
- **Branding.** A small Globulation 2 wordmark with `glob2.online` beneath it sits bottom right over the map, clear of the game's sidebar. See [Branding overlay](#branding-overlay).

## Quick start

```sh
./setup.sh --with-game                                # packages, ~/glob2-stream, GPU report, glob2 checkout
install -m 600 /dev/stdin ~/.config/glob2-stream/twitch.key   # paste the key from Twitch > Settings > Stream, then Ctrl-D
(cd ~/glob2-stream/src && python3 tools/dev_build.py perf=1)  # build the game (setup.sh prints SDL3 notes)
./game-up.sh                                          # Xvfb, audio sink, game with MCP on 27300
./register-mcp.sh                                     # Claude Code MCP server "glob2-stream"; open a new session
./stream.sh file ~/glob2-stream/logs/check.mp4 15     # local check: picture, caption and sound
./stream.sh test 30                                   # Twitch bandwidth test: reaches Twitch, never goes live
./stream.sh live --i-mean-it                          # real broadcast, only with the go-ahead
./down.sh                                             # stop everything
```

Run the scripts from anywhere; they find each other through their own location.

## File layout

| Path | Contents |
| --- | --- |
| `lib.sh` | Shared settings and defaults, sourced by every script. Precedence: environment, then `$GLOB2_STREAM_HOME/stream.env`, then defaults. |
| `stream.env.example` | Every setting with its default; `setup.sh` copies it to `$GLOB2_STREAM_HOME/stream.env`. |
| `setup.sh`, `register-mcp.sh` | One-time machine setup and Claude Code MCP registration. |
| `game-up.sh`, `down.sh`, `route-audio.sh` | Start and stop the display, audio sink and game; keep game audio on the sink. |
| `stream.sh`, `caption.sh` | Capture, overlays, encoding and output; caption text. |
| `mcp/` | Python helpers that drive the game over MCP without an agent (`mcp_call.py`, `activate.py`). Standard library only. |
| [`stream-playbook.md`](stream-playbook.md) | How Claude plays and presents on stream: setup checks, camera, narration, fair play, notes. |
| `assets/` | Branding image and its [provenance](assets/README.md). |

Local state never lives here: `$GLOB2_STREAM_HOME` (default `~/glob2-stream`) holds `stream.env`, `logs/`, `profile/`, `notes/`, `overlay/caption.txt` and usually the game checkout `src/`; the key stays in `~/.config/glob2-stream/`.

## Commands

| Command | Purpose |
| --- | --- |
| `setup.sh [--with-game]` | Install missing packages (sudo), create `$GLOB2_STREAM_HOME` and `stream.env`, check the key and report NVENC and Vulkan. `--with-game` clones Globulation2/glob2 to `GLOB2_SRC` and prints the build command. |
| `game-up.sh [--no-game]` | Start Xvfb, the audio sink and the game. Reuses anything already running. |
| `register-mcp.sh [name]` | Register the stream game as a user-scope Claude Code MCP server. The server reuses the running game, or starts one on the stream display. |
| `stream.sh file OUT [s]` | Record locally. Default 20 s. |
| `stream.sh test [s]` | Twitch bandwidth test (`?bandwidthtest=true`). Default 30 s. |
| `stream.sh live --i-mean-it` | Broadcast until stopped. Logs to `logs/stream.log`. |
| `caption.sh "text"` | Set the on-stream caption. |
| `caption.sh --match OPPONENT RECORD GOAL [LAST_MOVE]` | Show the opponent, record, goal and optional latest confirmed move. |
| `route-audio.sh` | Move audio from processes on the stream display onto the sink. `game-up.sh` and `stream.sh` run it automatically. |
| `down.sh` | Stop the stream, game, Xvfb and sink. |
| `mcp/activate.py [--acquire] KEY` | Activate a game control by key over MCP (for example `menu/1`, then `tutorial/lesson/0`). |
| `mcp/mcp_call.py TOOL [JSON]` | Call any game MCP tool over HTTP, for scripting without an agent. |

## Match caption

Use the completed games in the [playbook's game log](stream-playbook.md#learning-loop) to count wins, losses and draws against the current opponent. Pass short, single-line values to `caption.sh`. Start without a last move, then add one when it has been confirmed in-game. The game log remains the source of the record, so an interrupted or still-running game does not change the score.

```sh
./caption.sh --match Nicowar '3W–2L–0D' 'Keep the colony fed through the first raid'
./caption.sh --match Nicowar '3W–2L–0D' 'Keep the colony fed through the first raid' 'Assigned two workers to the Inn'
./caption.sh 'Between matches · Win against Nicowar · 4W–2L–0D'
```

The caption replaces the previous overlay in one update. Check the picture with `stream.sh file` when changing the caption layout or using longer text.

## Configuration

`$GLOB2_STREAM_HOME/stream.env` overrides the defaults in `lib.sh`; see [stream.env.example](stream.env.example).

| Setting | Default | Notes |
| --- | --- | --- |
| `GLOB2_SRC`, `GLOB2_BIN` | `~/glob2-stream/src`, its perf build | Game checkout and binary. |
| `GAME_RENDERER` | `sdl-gpu` | `software` works without a GPU but is slow. |
| `STREAM_DISPLAY`, `STREAM_SIZE`, `STREAM_FPS` | `:99`, `1920x1080`, `30` | |
| `STREAM_VBITRATE`, `STREAM_ABITRATE` | `4500k`, `160k` | Keep video at or below 6000k for Twitch. |
| `STREAM_ENCODER` | auto | `h264_nvenc`, `libx264`, or another ffmpeg encoder. |
| `STREAM_SINK` | `glob2_stream` | |
| `MCP_PORT` | `27300` | A desktop game normally uses 27202. |
| `TWITCH_INGEST`, `TWITCH_KEY_FILE` | auto ingest, `~/.config/glob2-stream/twitch.key` | |
| `BRAND*` | on | See [Branding overlay](#branding-overlay). |

## Branding overlay

`stream.sh` draws the [wordmark](assets/glob2-wordmark.png) bottom right with the domain right-aligned beneath it, small and slightly transparent. The default right margin keeps both over the map: the game's right sidebar is about 200 px wide at 1080p, and its zoom controls sit in its bottom corner. Sizes are given at 1080p and scaled to `STREAM_SIZE`.

| Setting | Default | Notes |
| --- | --- | --- |
| `BRAND` | `1` | `0` turns off the logo and the text. |
| `BRAND_LOGO` | `assets/glob2-wordmark.png` | Any RGBA image. If the file is missing, the stream continues with text only and prints a warning. |
| `BRAND_TEXT` | `glob2.online` | Empty for logo only. White DejaVu Sans Bold on a black@0.45 box. |
| `BRAND_TEXT_SIZE` | `22` | Font size in px. |
| `BRAND_WIDTH` | `200` | Logo width in px; height keeps the aspect ratio. |
| `BRAND_OPACITY` | `0.85` | Logo opacity, 0–1. |
| `BRAND_MARGIN_RIGHT` | `224` | Distance from the right edge. Keep it above about 210, or the branding covers the sidebar and zoom controls. |
| `BRAND_MARGIN_BOTTOM` | `16` | Distance from the bottom edge. |

Only approved imagery or direct derivatives may be used ([assets README](assets/README.md)). Check a `stream.sh file` frame after changing any of these.

## Troubleshooting

- **Game sound plays on the speakers, or the stream is silent.** SDL3's PipeWire backend ignores `PULSE_SINK`, and PipeWire remembers per-application routing, so a stream named `glob2` can return to the speakers. `game-up.sh` forces SDL's PulseAudio backend, and `route-audio.sh` moves every audio stream whose process has `DISPLAY` set to the stream display. Run it again if the sound moves.
- **The window is small in the corner.** Fullscreen is not applied on Xvfb, so the game is sized with `--window-size` instead.
- **Low frame rate, or `llvmpipe` in the logs.** The game fell back to OpenGL on Xvfb. Keep `GAME_RENDERER=sdl-gpu` and check that `setup.sh` lists a Vulkan GPU. The "No DRI3 support" warnings come from Mesa drivers and are harmless when another device presents.
- **Stopping processes.** Stop them by PID file or exact command line (`down.sh`). `pkill -f <pattern>` run from a shell can match and kill that shell.
- **Branding covers the HUD or looks wrong.** Check `BRAND_MARGIN_RIGHT` (at least about 210 at 1080p) and that `BRAND_LOGO` exists; the warning `brand logo ... not found` means text only. `BRAND=0` isolates overlay problems.
- **Watching the hidden display.** `ffplay -f x11grab -video_size 1920x1080 -i :99`, or `stream.sh file` and play the result.
- **Stale MCP token.** `mcp/activate.py --acquire` takes control again and saves a fresh token.

## Safety

- `stream.sh live` refuses to start without `--i-mean-it`. Agents broadcast only after the user explicitly says to go live. Use `test` and `file` for checks.
- The stream key never enters this repository, the command line output or the logs. Keep it at mode 600. `.gitignore` excludes `stream.env`, `*.key`, `logs/` and `profile/` here as a backstop.
- The game's agent tools respect fog of war: they never reveal hidden enemy state, so on-stream commentary only reflects what a player could see.
- The stream shows only the virtual display and the game's audio, never the host desktop or microphone.
