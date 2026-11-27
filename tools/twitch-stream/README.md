# Twitch stream rig

[Twitch streaming record](../../planning/twitch-streaming.md) · [Planning index](../../planning/README.md) · [Glob2 MCP guide](https://github.com/Globulation2/glob2/blob/master/docs/development/mcp-ui-server.md)

The single setup for **Claude Plays Glob**: Claude playing Globulation 2 around the clock on the official Twitch channel. A supervisor keeps the game, the stream and the agents running. One Claude agent plays each match through the game's embedded MCP server. A second, separate Claude agent talks with viewers in Twitch chat, so it never distracts the player. The game runs on a hidden virtual display, so the streaming machine's desktop stays usable. ffmpeg captures that display and the game's sound and sends them to Twitch.

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

- **Display.** The game draws on an invisible X display, chosen by `STREAM_DISPLAY_BACKEND`:
  - `xorg` (recommended with an NVIDIA GPU): a headless X server on NVIDIA's own X driver, installed as a system service by `display/install-xorg-display.sh`. The game presents natively and holds 60 fps. It has no outputs or input devices and doesn't switch VTs, so the desktop session is unaffected. Connections need its auth cookie (`STREAM_XAUTHORITY`).
  - `xvfb` (works anywhere): Xvfb has no DRI3, so every GPU frame is copied through the CPU and the game managed only about 12 fps on the maintainer laptop. Viewers saw that as 5–10 fps.
  - A headless Wayland compositor with Xwayland was also tried: the game drew about 40 fps there, but x11grab captured black frames.
  Either way the game uses its `sdl-gpu` (Vulkan) renderer.
- **Audio.** A null sink receives only the stream game's audio, and ffmpeg records its monitor. Desktop sounds and other games never reach the stream.
- **Encoding.** NVIDIA NVENC is used when it works, otherwise x264 on the CPU. 1080p60, 6000 kbps CBR, 2-second keyframes and 160 kbps AAC (Twitch's ceiling for non-partners). 60 fps matters: sampling a game that draws faster than the stream rate judders visibly even with no dropped frames. The filter graph converts to yuv420p before the overlays; drawing them in RGB cost about 3 CPU cores and starved capture.
- **Caption.** A bottom-left text box shows match context or an intermission message from `caption.sh`. ffmpeg reloads it during capture.
- **Camera.** The player moves the camera for the show; when a viewer asks to see something, the chat host shows it and holds the camera for about 40 s. Both go through one gate, `chat/camera.py`. See [Camera](#camera).
- **Camera label.** While a viewer request holds the camera (or briefly after a labelled player move), "Showing: … · asked by @name" appears centred over the map under the top bar (`CAMERA_OVERLAY_FILE`; empty draws nothing).
- **Branding.** A small Globulation 2 wordmark with `glob2.online` beneath it sits bottom right over the map, clear of the game's sidebar. See [Branding overlay](#branding-overlay).

### Agents and the supervisor

```text
 supervisor.py run ──┬─ game-up.sh (display, sink, game) and a 1920x1080 window check before every match
                     ├─ stream.sh file|live   (restarted if it dies; live needs --i-mean-it)
                     ├─ per match: claude -p  PLAYER (PLAYER_MODEL, Sonnet 5.5)
                     │     prompt = prompts/player.md + stream-playbook.md + this match's assignment
                     │     tools: glob2-stream MCP (the game via game_proxy.py, which owns the control lease),
                     │            stream-ctl MCP (match bookkeeping, narrate, match_wait, camera_show, fast-forward),
                     │            Read/Edit/Write inside NOTES_DIR only
                     ├─ --chat: chat/chat_agent.py  CHAT HOST (CHAT_MODEL, Sonnet 5.5), no game tools
                     └─ every 10 s: $STATE_DIR/status.json (read by the chat host and status.py)
```

- **Game control is never the model's job.** The player's `glob2-stream` server is `game_proxy.py`, which takes control of the game itself and keeps it: the model calls tools without a token and never sees one. Before 2026-11-24 the player carried the token in its context; an aggressive compaction lost it, the lease stayed held, and the colony ran on autopilot while the player told viewers it was locked out. The proxy adopts a still-valid published token, re-acquires once on a lost lease, and releases control when the session ends (the supervisor releases a lease a killed proxy left behind).
- **One session per match.** The supervisor assigns the opponent, rotating through Cortex, Nicowar, Cabino and Maxima with the least recently played first, and starts a fresh player session. The session sets up a 1v1 on a random 256×256 map with a new generator, plays it, records the result and ends. If the model ends its turn mid-match, the supervisor resumes the same session (`claude -p --resume`) with a nudge to keep playing. A session that crashes or reaches `--game-timeout` without a result is retried as a recovery session, which first checks whether the match can continue. After three tries, the match is recorded as aborted.
- **Sandbox.** Both agents run as a separate unprivileged user with a restricted tool set. See [Security and sandboxing](#security-and-sandboxing).
- **Score.** `$STATE_DIR/games.jsonl` is the official record. `match_result` appends to it, and the captions and record come from it. Aborted matches are logged but never counted.
- **Chat host.** The chat host is a separate process with its own sandbox. It reads the game through `status.json` and a read-only proxy, can point the camera at what viewers ask about, and relays the best viewer questions and ideas to the player through `viewer_relay.py`. See [chat/README.md](chat/README.md).
- **Cost.** Every player session's cost is logged in `logs/supervisor.log`; `analysis/cost_report.py` and `analysis/tool_usage.py` measure it from the transcripts. Matches 58–140 cost about $3.80 an hour at API list prices ([tool usage analysis](../../analysis/twitch-mcp-tool-usage.md)). Changes made from that analysis (2026-11-27):
  - `match_wait` returns the alerts and only the status counters that changed, with a full snapshot every 12 waits (about half the size per wait); the speed line, fast-forward reminder and camera nudge repeat only when something changed or at most once a minute;
  - waits wake on attacks on buildings, not on every unit attacked (`attack` is an `also_until` option);
  - a narration sent within 30 s of the last is queued, not refused, and costs no pacing slot;
  - `match_info` carries the `## Current playbook` section of `strategy.md` (capped at 4,000 characters) and the last three `games.md` entries, so sessions don't read the full notes; `match_result` keeps `games.md` to its newest 30 entries and moves older ones to `games-archive.md`;
  - `match_fast_forward` also accepts a long stalemate (past tick 300,000, win chance within 15 points and no building lost over 100,000 ticks, from `$STATE_DIR/match-trend.json`);
  - the player's prompt cache lasts five minutes (`CLAUDE_CODE_PROMPT_CACHE_TTL=5m` in `agent-run`; `AGENT_PLAYER_CACHE_TTL` in the agent config), not the subscription default of one hour;
  - never-used game tools (`game_alliance`, `ui_drag`, `ui_move`, `ui_mouse_button`, `ui_type_text`, `ui_release_inputs`) are hidden by `game_proxy.py`;
  - the player's camera moves wait out the 8 s gap instead of being refused.
- **Logs and disk.** Player transcripts are gzipped per match (the newest 100 are kept; `autostart/archive-transcripts.sh` hard-links every one into `logs/player-archive` for analysis, about 0.9 MB a match). Stream and chat logs rotate at 20 MB, and the supervisor log at 5 MB. A local recording stops if less than 2 GiB is free.

## Quick start

```sh
./setup.sh --with-game                                # packages, ~/glob2-stream, GPU report, glob2 checkout
install -m 600 /dev/stdin ~/.config/glob2-stream/twitch.key   # paste the key from Twitch > Settings > Stream, then Ctrl-D
(cd ~/glob2-stream/src && python3 tools/dev_build.py perf=1)  # build the game (setup.sh prints SDL3 notes)
./display/install-xorg-display.sh                     # NVIDIA GPU: headless X server for a 60 fps game; then STREAM_DISPLAY_BACKEND=xorg
./game-up.sh                                          # display (Xvfb, or checks the xorg service), audio sink, game with MCP on 27300
./register-mcp.sh                                     # Claude Code MCP server "glob2-stream"; open a new session
./sandbox/install-agent-sandbox.sh                    # agent user, agent code, policies, shared dirs, sudo rule, firewall
claude setup-token                                    # then install the token it prints (Security and sandboxing)
./sandbox/verify-sandbox.sh                           # check the sandbox, including one cheap call per agent
./stream.sh file ~/glob2-stream/logs/check.mp4 15     # local check: picture, caption and sound
./stream.sh test 30                                   # Twitch bandwidth test: reaches Twitch, never goes live
./supervisor.py run --stream file:$HOME/glob2-stream/logs/run.mp4 --max-games 1   # one supervised match, recorded locally
./status.py                                           # what is running, the current match and the record
./supervisor.py run --stream live --i-mean-it --chat  # Claude Plays Glob 24/7, only with the user's go-ahead
./autostart/install-autostart.sh                     # or run it as a boot-time service (see Running unattended)
./down.sh                                             # stop everything
```

Run the scripts from anywhere; they find each other through their own location.

## Running unattended

`autostart/install-autostart.sh` makes the whole rig come up at boot with nobody logged in:

- **What starts:** the systemd user service `glob2-stream.service` runs `supervisor.py`, which brings up the game, the stream, the player and (with `AUTOSTART_CHAT=1`) the chat host, and restarts any of them that exits. systemd restarts the supervisor itself if it exits.
- **Lingering:** the installer enables lingering for the operator, so the user manager, PipeWire and the service start at boot without a login.
- **System services it relies on:** `glob2-stream-xorg` (the NVIDIA display), `glob2-agent-egress` and `glob2-agent-proxy` (the agents' firewall and proxy), installed and enabled by `display/install-xorg-display.sh` and `sandbox/install-agent-sandbox.sh`.
- **Order:** `autostart/wait-ready.sh` waits for the audio server, DNS and the stream display before the supervisor starts; on timeout systemd retries. Verified by a reboot on 2026-11-24.
- **Stopping and restarting:** `systemctl --user stop glob2-stream` ends the stream, chat and player but leaves the game and its match running (`KillMode=process`), so `restart` resumes the match. Logs: `logs/supervisor-console.log`, `journalctl --user -u glob2-stream`.
- **Going live is a standing decision.** With `AUTOSTART_STREAM=live` (the default) every boot broadcasts. Use `none` or `file:PATH` for a machine that shouldn't go live on its own, or `--uninstall`.

- **Restarting the game without cutting a match short:** `touch $STATE_DIR/restart-game` (default `/var/lib/glob2-stream/state/restart-game`). After the current match's result, the supervisor stops the game and relaunches it through `game-up.sh`, which applies `STREAM_GAME_PREFS`. Use it for game settings or a new game build.

Don't run a hand-started `supervisor.py` while the service is active: stop the service first.

## Camera

One gate, `chat/camera.py`, moves the stream camera for everyone. It calls the game's `game_view` with the player's control token, which the player's game proxy (`game_proxy.py`) publishes to `$STATE_DIR/control-token` (0644 inside the 2770 operator:agent state dir) and deletes when it releases control; no model ever sees the token, and tool replies never contain it.

- **Player:** `camera_show` on its stream-ctl MCP server. Its policy denies `game_view`, so it can't bypass the gate.
- **Chat host:** `camera_show` in its read-only proxy, one move per reply, with `asked_by`. A chat move sets a hold (`$STATE_DIR/camera-hold.json`, `CAMERA_HOLD_SECONDS`, default 40 s) during which the player's moves are refused with "keep playing and narrate instead"; the chat host can still move it.
- **For every source:** zoom 0 to 1 only (above 1 is refused; a framed `width`/`height` is widened to at least the 100% view, about 54×34 tiles at 1080p), at least `CAMERA_MIN_INTERVAL` (8 s) between moves, labels cleaned to letters, digits and plain punctuation with links and mass mentions dropped, at most 60 characters.
- **Label:** chat moves show "Showing: … · asked by @name" for the hold; labelled player moves show for `CAMERA_LABEL_SECONDS` (12 s). The supervisor and chat host clear expired labels.
- **Director:** `chat/director.py` moves the camera when nobody has for `CAMERA_IDLE_SECONDS` (alerts first, then a rotation of the colony, buildings, resources, frontier, enemy buildings seen and the whole map). It is on by default as a fallback (`CAMERA_DIRECTOR=1`, 90 s).
- **Drift:** between explicit moves, `chat/camera_drift.py` (in the chat agent, no model calls) pans the view slowly toward the action so the picture is never still and globs don't walk off-screen. Every 3 s it reads `game_world` (read-only, fog of war respected) and targets, in order: fresh alerts, visible enemy units near the view, Claude's units on the move (the biggest moving group), else a slow circle around the last explicit target. It glides by holding the middle mouse button and moving the pointer a few pixels about 30 times a second (`CAMERA_DRIFT_PX_PER_S`, default 60 px/s, about 2.7 tiles/s at 70% zoom; `CAMERA_DRIFT_STEP` 0.033 s), re-anchoring at the screen centre every 3.5 s because button holds expire after 5 s. Short drags every 0.2 s looked stop-start; the continuous glide looked much smoother on stream (2026-11-24). Arrow keys were too fast to drift with (~38 tiles/s held). It never zooms, pauses 2 s after any explicit move, only circles a viewer request's target during its hold, and ignores action farther than `CAMERA_DRIFT_RANGE` tiles (that's for explicit cuts). Each drag holds the game's MCP queue for 120 ms, so other calls wait a little (median ~60 ms measured).
- The sandboxed agents use the default hold, interval and label times; the operator-side settings in `stream.env` only affect the chat host's unsandboxed mode and the director.

## Clips and highlights

Viewers mostly find the channel through clips and past broadcasts, and Twitch deletes past broadcasts after a few days. So every match is labelled and clipped on Twitch automatically by `highlights.py`, which runs as its own user service, `glob2-stream-highlights`. It's separate from the supervisor so it can be updated and restarted without ending the broadcast:

- **Match starts:** the stream title becomes "Claude Plays Glob · Claude vs Cortex · Game 83 on Canals · overall 26W–56L–0D", and a stream marker "Game 83 start: …" is added. Twitch's highlight editor (Creator Dashboard → Content → Video Producer → the past broadcast) lists the markers, so one game becomes a permanent Highlight in a couple of clicks.
- **Momentum swing:** when the win chance moves `HIGHLIGHT_SWING` points (default 25) within three minutes, it clips the last 60 s ("Claude vs Cortex · Game 83: the tide turns for Claude (30% to 62%)"). At most one swing clip every `HIGHLIGHT_COOLDOWN` seconds (600). There are none while fast-forwarding.
- **Match ends:** a marker "Game 83 end: Cortex beats Claude" and a clip of the finish. Aborted matches get neither.
- **What it reads:** the shared match state and `game_world`'s win chance, with no control lease. The broadcaster's token stays operator-side. Clip edit links are logged to `logs/highlights.jsonl`, never to the shared state dir.
- **Scopes:** titles and markers need `channel:manage:broadcast`; clips need `clips:edit`. Without a scope it logs once and skips that part. To add scopes, log in again as the broadcaster and reinstall the token:
  ```sh
  twitch token -u -s 'chat:read chat:edit channel:manage:broadcast clips:edit'
  chat/token_refresh.py refresh
  highlights.py status          # shows which parts are enabled
  ```
  From another machine (the CLI's browser login needs a browser on the stream machine): run `chat/token_refresh.py login-url`, open the link where you're signed in to Twitch **as the channel account**, authorize, then copy the `http://localhost:3000/?code=…` address the page fails to load and run `chat/token_refresh.py redeem 'ADDRESS'` within a few minutes.
- **Wrong-account guard:** a token whose login isn't `TWITCH_BOT_USER` (else `TWITCH_CHANNEL`) is never installed or used, so a browser signed in to the owner's personal account can't make the rig chat, retitle or clip as that account (on 2026-11-26 three logins in a row came back as the personal account). If it happens, sign in as the channel account (log out on twitch.tv first, or use a browser already signed in as it) and disconnect the app from the personal account under Twitch Settings → Connections.
- **Fewer, longer broadcasts:** every supervisor or stream restart ends the broadcast and starts a new past-broadcast video, which splits viewer counts. Prefer `touch $STATE_DIR/restart-game` and changes to the highlights service, which leave the broadcast running.
- **Live watchdog:** Twitch ends any broadcast after 48 hours, and ffmpeg keeps sending without an error while the channel shows offline (10.5 hours lost on 2026-11-27). The highlights service checks every 30 s that the channel is live: if the encoder runs while Twitch says offline for three checks, it stops ffmpeg (`logs/stream.pid`) and the supervisor starts a new broadcast. After 46.5 hours it restarts the encoder between matches instead, so no game is cut off. `LIVE_WATCH=0` turns it off.
- **Manual tests:** `highlights.py marker TEXT` and `highlights.py clip TITLE`. `HIGHLIGHTS=0` turns it off; `autostart/install-autostart.sh` installs the service only for `AUTOSTART_STREAM=live`.

## File layout

| Path | Contents |
| --- | --- |
| `lib.sh` | Shared settings and defaults, sourced by every script. Precedence: environment, then `$GLOB2_STREAM_HOME/stream.env`, then defaults. |
| `stream.env.example` | Every setting with its default; `setup.sh` copies it to `$GLOB2_STREAM_HOME/stream.env`. |
| `setup.sh`, `register-mcp.sh` | One-time machine setup and Claude Code MCP registration. |
| `game-up.sh`, `down.sh`, `route-audio.sh` | Start and stop the display, audio sink and game; keep game audio on the sink. |
| `stream.sh`, `caption.sh` | Capture, overlays, encoding and output; caption text. |
| `supervisor.py`, `status.py` | The 24/7 run (game, stream, player sessions, chat host, status) and its read-only status report. |
| `stream_ctl.py`, `rigstate.py`, `rigconfig.py` | Match bookkeeping: the CLI, and the `stream-ctl` MCP server the player uses; shared state and settings for the Python tools. |
| `prompts/` | [`player.md`](prompts/player.md), the player's role brief (the playbook is appended to it), and `chat.md`, the chat host's prompt. |
| [`chat/`](chat/README.md) | The Twitch chat host: IRC client, agent loop, read-only game proxy, token refresh and its setup guide. |
| `sandbox/` | `install-agent-sandbox.sh` (install, resync, `--uninstall`), `verify-sandbox.sh`, `agent-run` (the wrapper every agent starts through), `policy/` (the Claude Code `--settings` file for each role) and `egress_proxy.py` (the agents' only way to the internet). See [Security and sandboxing](#security-and-sandboxing). |
| `mcp/` | Python helpers that drive the game over MCP without an agent (`mcp_call.py`, `activate.py`). Standard library only. |
| [`stream-playbook.md`](stream-playbook.md) | How Claude plays and presents on stream: setup checks, camera, narration, fair play, notes. |
| `assets/` | Branding image and its [provenance](assets/README.md). |

Local state never lives here: `$GLOB2_STREAM_HOME` (default `~/glob2-stream`) holds `stream.env`, `logs/`, `profile/` and usually the game checkout `src/`. The keys stay in `~/.config/glob2-stream/`. Notes, state and the caption live in `AGENT_SHARED_DIR` (default `/var/lib/glob2-stream`), shared with the sandboxed agents.

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
| `supervisor.py run [--stream none\|file:PATH\|live] [--i-mean-it] [--chat] [--max-games N] [--game-timeout MIN] [--down]` | Run matches continuously. Defaults: no capture, no chat, unlimited matches, 120-minute sessions. `--down` stops everything on exit. |
| `status.py [--json]` | Display, game, supervisor, stream, current match, player, chat host, record by opponent, recent results and free disk. |
| `stream_ctl.py info\|setup-done\|caption\|result` | The player's match tools from a shell, for operators and tests. `stream_ctl.py mcp` serves them to the player. |
| `highlights.py run\|status\|marker TEXT\|clip TITLE` | Per-game Twitch titles, markers and clips (the `glob2-stream-highlights` service runs `run`). |
| `analysis/cost_report.py "YYYY-MM-DD HH:MM"` | API-equivalent model cost since a local time, from the player transcripts and the chat log: tokens by kind, $/h, $/day, calls per minute. Prices are in the script. |
| `analysis/player_tail.py [N]` | The newest player session's last N tool calls, errors and text (tokens dropped): is it stuck or looping? |
| `analysis/setup_tokens.py [TRANSCRIPT ...]` | Tokens each session spends before the match starts and in total (default: the five newest). |
| `down.sh` | Stop the supervisor, stream, game, Xvfb and sink. |
| `mcp/activate.py [--acquire] KEY` | Activate a game control by key over MCP (for example `menu/1`, then `tutorial/lesson/0`). |
| `mcp/mcp_call.py TOOL [JSON]` | Call any game MCP tool over HTTP, for scripting without an agent. |

## Match caption

During a supervised run, the player sets the caption through `match_caption` (goal and last confirmed move), and the tool fills in the opponent and the record from `games.jsonl`. `match_result` shows the result between matches. By hand, the same actions are available from a shell:

```sh
./stream_ctl.py caption --goal 'Keep the colony fed through the first raid' --last 'Assigned two workers to the Inn'
./caption.sh --match Nicowar '3W–2L–0D' 'Keep the colony fed through the first raid'   # lower level, any values
./caption.sh 'Between matches · Win against Nicowar · 4W–2L–0D'                        # free text
```

Each value is one line of at most 70 characters, so three lines fit beside the branding. The caption replaces the previous overlay in one update. Check the picture with `stream.sh file` after changing the caption layout.

## Configuration

`$GLOB2_STREAM_HOME/stream.env` overrides the defaults in `lib.sh`; see [stream.env.example](stream.env.example).

| Setting | Default | Notes |
| --- | --- | --- |
| `GLOB2_SRC`, `GLOB2_BIN` | `~/glob2-stream/src`, its perf build | Game checkout and binary. |
| `GAME_RENDERER` | `sdl-gpu` | `software` works without a GPU but is slow. |
| `STREAM_DISPLAY`, `STREAM_SIZE`, `STREAM_FPS` | `:99`, `1920x1080`, `60` | |
| `CAMERA_OVERLAY_FILE`, `CAMERA_HOLD_SECONDS`, `CAMERA_MIN_INTERVAL`, `CAMERA_LABEL_SECONDS` | `overlay/camera.txt`, `40`, `8`, `12` | The camera label file and gate timings (see [Camera](#camera)). |
| `CAMERA_DIRECTOR`, `CAMERA_IDLE_SECONDS` | `1`, `90` | Fallback director: shows the action (alerts, colony, explorers) when nobody has moved the camera for 90 s. On since 2026-11-24, after the camera sat still on empty ground in a long match. |
| `CAMERA_DRIFT`, `CAMERA_DRIFT_PX_PER_S`, `CAMERA_DRIFT_MAX_PX_PER_S`, `CAMERA_DRIFT_RANGE` | `1`, `60`, `240`, `40` | Smooth drift toward the action between explicit camera moves: on/off, glide speed near the target, top speed for distant action (it ramps up with distance, ~25 tiles for full speed), and how far (tiles) it will chase action. Runs in the chat agent, so it needs `--chat`. |
| `STREAM_GAME_PREFS` | `clouds=0 cloudShadows=0` | Game settings (`preferences.txt` keys) forced in the stream profile by `game-up.sh` at every launch. Clouds are off because they turn into blocky smears after H.264 encoding. |
| `AGENT_COMPACT_WINDOW`, `AGENT_COMPACT_PCT` | `100000`, `50` | Agent context compaction, passed by `agent-run` as `CLAUDE_CODE_AUTO_COMPACT_WINDOW` and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (validated whole numbers; window at least 100000). Aggressive on purpose: older turns are stale in a real-time match, and lessons live in the notes. Rerun the sandbox installer after changing. |
| `AUTOSTART_STREAM`, `AUTOSTART_CHAT` | `live`, `1` | What the boot service runs (`autostart/install-autostart.sh`). |
| `STREAM_DISPLAY_BACKEND`, `STREAM_XAUTHORITY` | `xvfb`, `$GLOB2_STREAM_HOME/display/Xauthority` | `xorg` uses the headless NVIDIA X server (`display/install-xorg-display.sh`); its auth cookie is the second setting. |
| `STREAM_VBITRATE`, `STREAM_ABITRATE` | `6000k`, `160k` | Keep video at or below 6000k for Twitch. |
| `STREAM_ENCODER` | auto | `h264_nvenc`, `libx264`, or another ffmpeg encoder. |
| `STREAM_SINK` | `glob2_stream` | |
| `MCP_PORT` | `27300` | A desktop game normally uses 27202. |
| `TWITCH_INGEST`, `TWITCH_KEY_FILE` | auto ingest, `~/.config/glob2-stream/twitch.key` | |
| `BRAND*` | on | See [Branding overlay](#branding-overlay). |
| `PLAYER_MODEL`, `CHAT_MODEL` | `claude-sonnet-5-5` | Models for the player and the chat host. See [Models](#models). |
| `STATE_DIR`, `NOTES_DIR`, `OVERLAY_FILE` | `state/`, `notes/`, `overlay/caption.txt` in `AGENT_SHARED_DIR` | Match state and score; the player's notes and working directory; the caption text. |
| `AGENT_USER`, `AGENT_INSTALL_DIR`, `AGENT_ETC_DIR`, `AGENT_SUDOERS`, `AGENT_SHARED_DIR` | `glob2agent`, `/opt/glob2-stream-agent`, `/etc/glob2-stream`, `/etc/sudoers.d/glob2-stream`, `/var/lib/glob2-stream` | The agent sandbox. `AGENT_USER=""` runs the agents as you, with `AGENT_SHARED_DIR` defaulting to `~/glob2-stream`. Rerun the installer after changing any of these. |
| `TWITCH_CLI_ENV` | `~/.config/twitch-cli/.twitch-cli.env` | Twitch CLI login used to refresh the chat token. |
| `TWITCH_CHANNEL`, `TWITCH_BOT_USER`, `TWITCH_CHAT_TOKEN_FILE` | `globulation2`, none, `~/.config/glob2-stream/twitch-chat.token` | Chat host account. Without a bot user and token it only reads. |
| Chat tuning (environment only) | see [chat/README.md](chat/README.md#running) | `CHAT_GAME_ACCESS`, `CHAT_MAX_GAME_CALLS`, `CHAT_MAX_BUDGET_USD`, `CHAT_MIN_INTERVAL`, `CHAT_MAX_PER_MIN`, `CHAT_BATCH_WAIT`, `CHAT_MODEL_TIMEOUT`. |

## Models

Both agents default to **Sonnet 5.5** (`claude-sonnet-5-5`). Set `PLAYER_MODEL` or `CHAT_MODEL` in `stream.env` to change one. With the sandbox, the agents use a long-lived token from `claude setup-token`, tied to your Claude subscription and installed for the agent user only. See [Security and sandboxing](#security-and-sandboxing). Without the sandbox, they use your own `claude` sign-in, which expires.

## Security and sandboxing

Viewers can write anything in chat, and the agents read game text and their own notes. Assume any of that may try to steer an agent (prompt injection). The sandbox makes sure a steered agent still can't reach anything that matters on the machine: your files, keys, accounts, connected services or other projects.

### Threat model

- **Untrusted input:** Twitch chat, which only the chat host reads, and anything shown in game.
- **Protected:** your home directory, SSH, cloud and GitHub credentials, the stream and Twitch keys, your Claude login, and your claude.ai connectors (Gmail, Drive, Calendar and so on).
- **Out of scope:** someone who already controls your account. The operator account starts and stops everything, and the sandbox protects it from the agents, not the other way round.

### Layers

Every layer below is independent: a mistake or bypass in one still leaves the others. The Claude Code controls follow the official documentation: [settings](https://code.claude.com/docs/en/settings), [settings reference](https://code.claude.com/docs/en/settings-reference), [permissions](https://code.claude.com/docs/en/permissions), [CLI reference](https://code.claude.com/docs/en/cli-reference), [environment variables](https://code.claude.com/docs/en/env-vars), [MCP](https://code.claude.com/docs/en/mcp), [memory](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [sub-agents](https://code.claude.com/docs/en/sub-agents), [headless mode](https://code.claude.com/docs/en/headless) and [sandboxing](https://code.claude.com/docs/en/sandboxing).

| # | Layer | Player | Chat host |
| --- | --- | --- | --- |
| 1 | **OS user** | `AGENT_USER` (`glob2agent`): a system user with no login shell, no extra groups and its own home. Your home is closed to it (mode 750 or tighter). | Same user, for the model call only. The Twitch connection, filtering and rate limits run as you. |
| 2 | **File permissions** | `AGENT_SHARED_DIR` (notes, state, overlay) is `operator:glob2agent` 2770. Notes are sticky (3770) and `session-brief.md` is written 644, so the player can read its rules but not change, delete or replace them. `AGENT_INSTALL_DIR` and `AGENT_ETC_DIR` are root-owned. | Same, with `state/chat-sandbox` as its empty working directory. |
| 3 | **Sudo rule and wrapper** | The sudo rule (`AGENT_SUDOERS`) lets only the operator run `agent-run` as `AGENT_USER`. `agent-run` (root-owned) accepts only `player --model M [--resume ID]`, each value checked against a pattern, and builds every other flag itself. | `chat --model M [--max-budget-usd N] [--max-game-calls N \| --no-game]`. |
| 4 | **Claude binary** | A root-owned copy in `AGENT_INSTALL_DIR/bin`, never anything in your home; updates are disabled. | Same. |
| 5 | **CLI flags** | `--restricted` (no code-running tools or WebFetch, file tools confined to the working directory, user and project settings ignored), `--tools Read,Edit,Write`, `--disable-slash-commands`, `--strict-mcp-config` with a fixed `--mcp-config`, `--permission-mode dontAsk` and `--permission-prompts none` (anything not pre-approved is denied), and an `--allowedTools` list of the two MCP servers plus `Read(./**)` and `Edit(./**)`. | `--tools ""` (no built-in tools), `--restricted`, the same permission flags, `--no-session-persistence`, a JSON schema for the answer, a budget cap. `--no-game` adds `--disallowedTools "mcp__*"`. |
| 6 | **Policy file** (`--settings`) | `sandbox/policy/player.json`, installed root-owned in `AGENT_INSTALL_DIR/policy`: deny rules for every other built-in tool (Bash, web, subagents, skills, tasks, cron, artifacts, workflows and more) and for `mcp__claude_ai_*`; deny rules for writing `CLAUDE.md`, `AGENTS.md`, `CLAUDE.local.md`, `.claude/`, `.mcp.json` and `session-brief.md` in the notes directory; `blockReadsOutsideWorkingDirectories` and `blockWritesOutsideWorkingDirectories`; bypass and auto modes disabled; `allowedMcpServers` exactly `glob2-stream` and `stream-ctl`; claude.ai connectors, hooks, bundled skills, skill shell execution, auto memory, artifacts and workflows off; built-in plugins other than the privacy plugin disabled. Deny rules win over any allow. | `chat.json`: the same, with Read, Edit and Write denied too and `allowedMcpServers` exactly `glob2-readonly`. `chat-nogame.json` allows no MCP servers at all. |
| 7 | **Environment** | `agent-run` clears the environment, then sets only HOME, PATH, umask 002, the token and documented switches: `ENABLE_CLAUDEAI_MCP_SERVERS=false`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` (also stops claude.ai skill and plugin sync), no updates, telemetry, error reports, feedback or feature flags, `CLAUDE_CODE_DISABLE_CLAUDE_MDS`, no auto memory, bundled skills, built-in subagents, web fetch, artifacts, workflows, cron or background tasks, and `CLAUDE_CODE_RESTRICTED=1`. | Same, plus `CLAUDE_CODE_SKIP_PROMPT_HISTORY`. |
| 8 | **Extension points** | The agent's `~/.claude` is `root:glob2agent` 1770; `plugins/`, `skills/`, `agents/`, `commands/`, `CLAUDE.md` and `settings.json` in it are root-owned and empty, so nothing can be installed or loaded from there. Session files (`projects/`, used by `--resume`) stay writable. | Same. |
| 9 | **MCP tools** | Only the game, through `game_proxy.py` (a stdio proxy to 127.0.0.1 that owns the control lease: it takes and renews control, adds the token to calls, strips any token the model passes, hides the acquire/renew/release tools and every `token` parameter, takes control again if the lease is lost, and releases it on exit), and `stream-ctl` (match bookkeeping, narration, waits and `camera_show`, no shell). `game_view`, `game_wait` and `game_chat` are denied and hidden, so camera moves, waits and narration pass their gates. | Only `glob2-readonly`: an allowlist of eight read tools plus `camera_show`, tokens stripped, a few calls and one camera move per reply. |
| 10 | **Network** | An nftables table (`glob2-agent-egress.service`) lets `glob2agent`'s packets reach only 127.0.0.1 on the game's MCP port and the egress proxy port; everything else, DNS included, is rejected. The proxy (`glob2-agent-proxy.service`, `sandbox/egress_proxy.py`, running as you) tunnels only to `EGRESS_ALLOW` (`api.anthropic.com`) on port 443 and logs every decision to the journal. `agent-run` refuses to start Claude if a direct connection to the internet succeeds or the proxy is down. | Same. |
| 11 | **Output filters** | Game actions, captions and the result in `games.jsonl`. | One JSON reply. Code filters it before Twitch sees it: no links except glob2.online and the channel, no internals, one line, rate-limited. |

#### What the documentation says isn't covered

- **Managed settings.** Claude Code's strongest controls (managed-only keys such as `allowManagedModsOnly` and `disableSideloadFlags`, and the built-in mod guard) need `/etc/claude-code/managed-settings.json`. Those apply to every account on the machine, including your own Claude Code, with no per-user scoping documented, so the rig doesn't install them. A session signed in with a long-lived `CLAUDE_CODE_OAUTH_TOKEN` doesn't count for the mod guard either. The compensating controls are layers 6 to 8: plugins and synced skills are off by policy and environment, the places they would load from are root-owned and empty, and the policy denies or disables every other extension point. A dedicated streaming machine could add managed settings safely; see the [managed settings](https://code.claude.com/docs/en/settings#settings-files) docs.
- **Claude Code's own sandbox** (`sandbox.*` settings) only covers shell commands. The agents have no shell, so the rig relies on the OS user and the nftables rule instead.
- **The account's server-side settings.** Claude Code fetches remote settings and policy limits for the signed-in account; those come from Anthropic for your account and can only tighten.

### What the agents can't reach

- Your home: dotfiles, SSH keys, `~/.config` (including the stream key, the Twitch chat token and the Twitch CLI login), `~/.claude` and your own Claude login, your gh and gcloud configs, and other projects.
- Your claude.ai connectors: `--strict-mcp-config`, `ENABLE_CLAUDEAI_MCP_SERVERS=false`, `disableClaudeAiConnectors`, a deny rule for `mcp__claude_ai_*` and an `allowedMcpServers` list of the rig's servers only. `verify-sandbox.sh` checks that each session lists only the rig's servers.
- Any other network service: the firewall allows only loopback, and the proxy only `api.anthropic.com`. The agents can't fetch web pages, call other APIs or send data anywhere else, even through a bug in a Claude Code control.
- Plugins, skills, subagents, hooks and slash commands: off by flag, policy and environment, with nothing installable in the agent's `~/.claude`. `verify-sandbox.sh` checks the session's lists are empty apart from the built-in privacy plugin.
- The game's code and files: the player has no shell, and its file tools can't leave the notes directory. The game is reached only over MCP, which follows fog of war.
- The Claude token itself: it is readable by the agent user, so that `claude` can authenticate, but the file tools can't reach `AGENT_ETC_DIR`. `verify-sandbox.sh` asks the player to read it and checks the refusal.

### Prompt-injection paths

- **Chat → chat host.** Viewer text is wrapped and labelled untrusted, and the host has no tools beyond the read-only game view and `camera_show`. The camera is the only state it can change: a steered host can at worst move the camera (zoom 100% or wider, at least 8 s apart, one move per reply, each hold at most `CAMERA_HOLD_SECONDS`) and put a filtered label of up to 60 characters on screen. Its reply passes code-enforced filters and rate limits before reaching Twitch.
- **Chat → player.** Only through `viewer_relay.py`: the chat side relays a one-line summary in its own words with the viewer's name; code keeps it to 140 characters of plain text with no links, one every 2 minutes, at most 3 waiting, each expiring after 5 minutes, from a viewer in the batch being answered. The player sees them only inside `match_wait` replies, labelled untrusted, and answers in `narrate` with @name (which marks them answered so the chat side can tell the viewer). Viewer text copied word for word into the notes, which outlive the match, is flagged back to the player. The player never reads Twitch chat, and its tools are unchanged, so a relayed message can at worst make it play or talk badly.
- **Game → agents.** Game text reaches them only through the game's MCP tools. Nothing they can do reaches beyond the game, the notes and the caption.
- **Player → its own rules.** A steered player could try to rewrite the brief it rereads after compaction. The brief is read-only to it and is regenerated from the repo's `prompts/player.md` and `stream-playbook.md` for every session; `verify-sandbox.sh` checks it can't be modified or replaced.

### Setting up a machine

1. Install the rig and build the game (Quick start), then run `sandbox/install-agent-sandbox.sh` as the operator. It is idempotent and uses sudo:
   - creates `AGENT_USER`;
   - installs `AGENT_INSTALL_DIR`, with a copy of the current `claude` (override it with `CLAUDE_BIN`);
   - writes `AGENT_ETC_DIR/agent.env`;
   - creates `AGENT_SHARED_DIR`, moving `notes/`, `state/` and the caption from `~/glob2-stream` the first time;
   - installs and validates the sudo rule;
   - installs the policy files and locks the agent's `~/.claude`;
   - with `AGENT_EGRESS=1` (the default), installs and starts `glob2-agent-egress.service` (nftables) and `glob2-agent-proxy.service`.

   It needs nftables (`/usr/sbin/nft`). Installing the firewall cuts off any agent session that started before it, because older sessions don't use the proxy; install between matches, or let the supervisor's recovery start a fresh session.

   It warns if `stream.env` still points `STATE_DIR`, `NOTES_DIR` or `OVERLAY_FILE` elsewhere.
2. Create the agents' Claude token. This is interactive: it opens a browser to sign in with the Claude subscription. `claude setup-token` creates a long-lived (one-year) OAuth token for non-interactive use. Install it for the agent user without echoing it:

   ```sh
   claude setup-token
   sudo install -o root -g glob2agent -m 640 /dev/stdin /etc/glob2-stream/claude-oauth-token
   ```

   Paste the token, press Enter, then Ctrl-D. Use `AGENT_USER` and `AGENT_ETC_DIR` if you changed them. The token is never copied from your own login.
3. Run `sandbox/verify-sandbox.sh`. It checks users, ownership and modes, the sudo rule and the option allowlist, and probes file access as the agent user. It checks the policy files and the locked `~/.claude`, the two services and the nftables table, and probes the network as the agent user: no direct connection or DNS, the game port reachable, the proxy refusing example.com and tunnelling to api.anthropic.com. It then makes one cheap call per agent (`claude-haiku-5-5`), checking the tools, MCP servers, plugins, skills, subagents and slash commands, and that reads outside the sandbox and writing `./CLAUDE.md` are refused. Without a token, `--dummy-token` checks start-up up to the (expected) login failure.

### Updating and uninstalling

- After `git pull`, or a `claude` update you want the agents to use, rerun `sandbox/install-agent-sandbox.sh`. It resyncs the root-owned copy and removes stale files. Stop the supervisor first, so that no agent is mid-session.
- `sandbox/install-agent-sandbox.sh --uninstall` removes the two services and the nftables table, the sudo rule, `AGENT_INSTALL_DIR`, `AGENT_ETC_DIR` (including the token) and the agent user with its home. It keeps `AGENT_SHARED_DIR` and prints the command to delete it.
- The proxy's decisions are in the journal: `journalctl -u glob2-agent-proxy`. To allow another host, set `EGRESS_ALLOW` in `stream.env` and rerun the installer; only add hosts the official [network configuration](https://code.claude.com/docs/en/network-config) docs list as required.
- `AGENT_EGRESS=0` skips the firewall and proxy. The other layers still apply, but the agents then have direct internet access.
- `AGENT_USER=""` in `stream.env` runs the agents as you, with only the Claude-level restrictions. That is less isolated: a steered agent would be one permission bug away from your files and connectors. Use it for development only.

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
- **Choppy stream.** Measure the game's own draw rate: two `mcp/mcp_call.py ui_status` calls a few seconds apart give `frame_id` per second. About 12 means Xvfb is the bottleneck: use `STREAM_DISPLAY_BACKEND=xorg`. If the game is near 60 but the stream isn't, check the `frame=`/`drop=` counters in `logs/stream.log` and the encoder's CPU. To see what viewers get, pull a sample with `streamlink` and count distinct frames (ffmpeg `mpdecimate`).
- **`llvmpipe` in the logs.** The game fell back to software OpenGL. Keep `GAME_RENDERER=sdl-gpu` and check that `setup.sh` lists a Vulkan GPU. The "No DRI3 support" warnings come from Mesa drivers.
- **xorg backend won't start.** `journalctl -u glob2-stream-xorg` and `/var/log/glob2-stream-xorg.log`. It needs NVIDIA's X driver matching the kernel module (Ubuntu: `xserver-xorg-video-nvidia-<version>`).
- **Stopping processes.** Stop them by PID file or exact command line (`down.sh`). `pkill -f <pattern>` run from a shell can match and kill that shell.
- **Branding covers the HUD or looks wrong.** Check `BRAND_MARGIN_RIGHT` (at least about 210 at 1080p) and that `BRAND_LOGO` exists; the warning `brand logo ... not found` means text only. `BRAND=0` isolates overlay problems.
- **Watching the hidden display.** `ffplay -f x11grab -video_size 1920x1080 -i :99` (with the xorg backend, set `XAUTHORITY` to `STREAM_XAUTHORITY` first), or `stream.sh file` and play the result.
- **The player isn't moving.** Run `status.py`, then check `logs/supervisor.log` and the newest `logs/player/match-*.jsonl.gz` (`zcat … | tail`). The supervisor ends a session after `--game-timeout` minutes and retries the match.
- **Stale MCP token (operator tools).** `mcp/activate.py --acquire` takes control again and saves a fresh token. The player never handles tokens; if it reports it can't control the game, check `$STATE_DIR/control-token` and the game's `ui_status`: another client holding control blocks the proxy until that lease lapses.

## Safety

- `stream.sh live` and `supervisor.py run --stream live` refuse to start without `--i-mean-it`. Agents broadcast only after the user explicitly says to go live. A go-ahead for a continuous run covers that supervisor run until it's stopped. Use `test`, `file` or `--stream none` for checks.
- Both agents run in the OS-level sandbox described in [Security and sandboxing](#security-and-sandboxing). The chat host has no game tools, and its replies pass code-enforced filters and rate limits ([chat/README.md](chat/README.md)).
- The stream key never enters this repository, the command line output or the logs. Keep it at mode 600. `.gitignore` excludes `stream.env`, `*.key`, `logs/` and `profile/` here as a backstop.
- The game's agent tools respect fog of war: they never reveal hidden enemy state, so on-stream commentary only reflects what a player could see.
- The stream shows only the virtual display and the game's audio, never the host desktop or microphone.
