# Twitch streaming

[Planning index](README.md) · [Social account inventory](../facts/social-media-accounts.md) · [Social media strategy](social-media-strategy.md) · [Channel C06: long-form video and livestreams](../analysis/channels-and-business-models.md) · [Stream rig code](../tools/twitch-stream/README.md)

This record tracks streaming Claude playing Globulation 2 on the project's [Twitch channel](https://www.twitch.tv/globulation2). Claude controls the game through its embedded MCP server, and the stream shows the game exactly as it plays.

## Status — 2026-11-24

- **Rig built and tested; nothing broadcast.** The reusable scripts are in [tools/twitch-stream](../tools/twitch-stream/README.md). A Twitch bandwidth test reached Twitch's ingest. Bandwidth-test sessions are accepted by Twitch but never appear on the channel.
- **No live stream has run.** Going live needs the user's explicit go-ahead for that session. `stream.sh live` refuses to start without `--i-mean-it`.
- **Playbook written.** The [stream playbook](../tools/twitch-stream/stream-playbook.md) records the user's 2026-11-24 streaming recommendations: the match format, camera rules (never zoom in), game-chat narration, fair play within fog of war, and local notes for learning.
- **Game unmodified.** The game ran from Globulation2/glob2 master `898fb00afc` with its existing `--mcp-port`, `--renderer sdl-gpu` and `--window-size` options. No OBS or other broadcast software was involved.

## Setup tested

The rig ran on the maintainer's Linux laptop: Ubuntu 24.04, an NVIDIA RTX 3070 Ti Laptop GPU and PipeWire audio.

- The game draws on a hidden 1920×1080 Xvfb display. Vulkan (`sdl-gpu`) rendered on the NVIDIA GPU and presented into Xvfb. On Xvfb, OpenGL would have fallen back to software rendering.
- Only the game's audio reaches the stream, through a dedicated null sink. SDL3's PipeWire backend ignored `PULSE_SINK`, and PipeWire's remembered routing sent the first test session's music to the laptop speakers. The scripts now force the PulseAudio backend and move audio by display (`route-audio.sh`).
- ffmpeg captures the display and the sink and encodes with NVENC: H.264 1080p30 at 4500 kbps CBR, 2-second keyframes and 160 kbps AAC. A caption bar is drawn from a text file the agent can update.
- **Branding.** A small corner overlay sits bottom right over the map: the approved Globulation 2 wordmark (a crop-only derivative of the [Epic v5 product logo](../assets/epic-v5/product-logo-960x540.png), see [rig assets](../tools/twitch-stream/assets/README.md)), with `glob2.online` beneath it. It is 200 px wide at 1080p, 0.85 opacity, and 224 px from the right edge so it clears the game's sidebar and zoom controls. It is configurable or can be disabled (`BRAND=0`).
- A separate Claude Code MCP server, `glob2-stream`, connects to that game on port 27300, so a desktop game on the default port is unaffected.

## Test results

| Test | Result |
| --- | --- |
| Local recording, 12 s, Introduction tutorial | 1920×1080 H.264 at 30 fps, ~4.5 Mbps, 0 dropped frames. AAC audio peaks at −9.7 dB. Caption visible. |
| Twitch bandwidth test, 30 s | 874 frames sent at 4.5 Mbps, 1.03× real time. 25 frames dropped, most likely while the connection started. Exit 0. |
| Committed scripts, 5 s local recordings | NVENC auto-selected; the forced `libx264` fallback also produced 1080p30 with audio. |
| Branding, 6 s local recording | Wordmark and domain bottom right over the map, clear of the sidebar, minimap and zoom controls. 180 frames, 0 dropped, audio peak −9.3 dB. `BRAND=0`, text-only (missing logo) and logo-only variants also checked. |
| Key handling | ffmpeg prints the full ingest URL on connection errors. `stream.sh` masks the key in its output and logs; checked with a fake key against an unreachable ingest. |

During script validation a short (2 s) Twitch bandwidth test also ran unintentionally, because a local settings file overrode test variables. That precedence bug is fixed. The run was bandwidth-test only, and no key appeared in its log.

## Gaps and next work

- **First live session.** The format was decided by the user on 2026-11-24: 1v1 against an AI with default rules, on randomly generated 256×256 maps, rotating the map generator each game (see the [playbook](../tools/twitch-stream/stream-playbook.md)). Still to choose: the stream title, category and tags, and the session length. Run a final `stream.sh test` immediately before going live.
- **Overlays and chat.** Viewer chat, a reasoning or commentary panel and a stream schedule are not built. Any chat-driven control needs moderation and abuse limits first.
- **Long sessions.** systemd user units for automatic restarts are not set up. Long runs are untested for memory, disk use of logs, or MCP token renewal (control leases are 300 s).
- **Other hardware.** Untested on non-NVIDIA GPUs, without Vulkan, or on non-Debian distributions. The libx264 path is only verified locally.
- **Account readiness.** Backup access, recovery coverage and moderator roles for the channel remain unverified (see the [account inventory](../facts/social-media-accounts.md)).
- **Agent conduct on stream.** The game's agent tools respect fog of war; commentary must not claim knowledge of hidden enemy state.
