# Twitch streaming

[Planning index](README.md) · [Social account inventory](../facts/social-media-accounts.md) · [Social media strategy](social-media-strategy.md) · [Channel C06: long-form video and livestreams](../analysis/channels-and-business-models.md) · [Stream rig code](../tools/twitch-stream/README.md)

## Status — 2026-11-24

- **One setup.** Claude Plays Glob runs only on the tracked [stream rig](../tools/twitch-stream/README.md). The separate host-local OBS automation recorded earlier was retired in favour of this rig.
- **Nothing broadcast yet.** Only Twitch bandwidth tests have reached Twitch, and Twitch never shows those on the channel. No live broadcast has run.
- **Going live needs the user's go-ahead.** A go-ahead to start a continuous run covers that supervisor run, including its automatic restarts, until it is stopped. `supervisor.py run --stream live` and `stream.sh live` refuse to start without `--i-mean-it`.
- **Sandboxed agents.** Both agents run as a separate unprivileged OS user (`glob2agent`) from root-owned code, through one narrow sudo rule. They use restricted Claude tools and only the rig's own MCP servers, so viewers' prompt injection can't reach the operator's files, keys, accounts or claude.ai connectors. Their Claude token is a long-lived `claude setup-token` token on the user's subscription. Every system change comes from `sandbox/install-agent-sandbox.sh`, checked by `sandbox/verify-sandbox.sh` ([Security and sandboxing](../tools/twitch-stream/README.md#security-and-sandboxing)).
- **Layered lockdown, checked against the Claude Code docs (2026-11-24).** On the user's request the agent controls were reviewed against the official Claude Code documentation and layered so no single control is relied on: OS user and file permissions; a root-owned wrapper with an argument allowlist; CLI flags (`--restricted`, fixed tools, `--disable-slash-commands`, `dontAsk` with no prompt answerer, strict MCP config); a root-owned `--settings` policy per role (explicit deny rules, outside-directory read and write blocks, an MCP server allowlist, connectors, hooks, skills, auto memory and non-essential built-in plugins off); documented environment switches; root-owned empty plugin, skill, agent and command directories; and a network layer, where nftables limits the agent user to loopback and an allowlist proxy reaches only `api.anthropic.com`. System-wide managed settings were left out because they would also change the operator's own Claude Code; the README records that tradeoff.
- **Two agents, both Sonnet 5.5 by default.** The player plays one sandboxed session per match under the supervisor, with a prompt built from the [playbook](../tools/twitch-stream/stream-playbook.md) word for word. A separate [chat host](../tools/twitch-stream/chat/README.md) talks with Twitch viewers and never touches the game, so chat can't distract or steer the player.

## Channel and show

The project selected **Claude Plays Glob** on 2026-11-24 as the 24/7 show on the official [Globulation 2 Twitch channel](https://www.twitch.tv/globulation2). Claude controls one colony through the game's embedded MCP server in live local matches. The format uses game audio, on-screen text and no microphone. The channel keeps the Globulation 2 identity and links viewers to [Play Globulation 2](https://glob2.online/).

- **Stream title** `Claude Plays Glob | 24/7 live colony RTS | AI vs AI | Free & Open-Source` (set 2026-11-24; earlier `Claude Plays Glob | 24/7 live colony RTS`)
- **Category and language** Globulation 2, English.
- **Tags** `RTS`, `Strategy`, `RealTimeStrategy`, `AI`, `Claude`, `AIPlaysGames`, `OpenSource`, `Indie`, `BaseBuilding`, `English`. Set through the Twitch API on 2026-11-24 after the user accepted the recommendation, and read back from the API. `NoCommentary` was dropped: Claude narrates in game chat and the chat host talks to viewers. The genre and AI tags target RTS players and AI-curious viewers, since the Globulation 2 category itself has little browsing traffic. The picks are reasoned from Twitch's tag rules, not from Twitch tag analytics; compare discovery sources in the four-week review. [Twitch tags](https://help.twitch.tv/s/article/guide-to-tags?language=en_US)
- **Go-live notification** “Claude is running a colony live. Can it keep the globs fed?”
- **About copy for the show** “Claude plays live local matches in Globulation 2, a free, open-source colony RTS. Watch it keep workers fed, expand and face the game's built-in opponents. Game audio and on-screen updates.”
- **On screen** Show the opponent and running score, current objective, and the latest action verified in the game. An example is “Goal: survive the first raid · Last action: assigned two workers to the Inn.” Keep the text and approved Globulation 2 branding clear of the HUD. Label between-match, paused or recovery states when possible, and reset stale match text before starting the next game.
- **Chat** The player narrates in game chat and the caption. A separate [chat host agent](../tools/twitch-stream/chat/README.md) answers Twitch viewers from the published match status. It discloses that it is an AI bot, and its replies pass code-enforced filters and rate limits. Viewer ideas reach the player only as untrusted suggestions between matches. Arrange human moderator coverage before promoting chat interaction. Use the [playbook](../tools/twitch-stream/stream-playbook.md) for camera, match settings and fog-of-war rules.

On 2026-11-24, the saved title, category, language, tags and notification were verified by reopening Edit Stream Info. The Creator Dashboard showed the channel offline after the save. Clips and Store past broadcasts were enabled when inspected.

## Weekly promotion and measurement

Feature one challenge at a regular time on the existing live feed. Enter it in the channel schedule and announce it in Discord. Lead with a gameplay stake such as “Can this colony stay fed through the first raid?” Include **Claude Plays Glob** so the setup is clear. For AI-focused audiences, lead with Claude and use the same in-game stakes. Show losses and observed mistakes along with successes. Publish a short captioned highlight showing a decision and consequence. Feature it on Twitch and reuse good standalone cuts on YouTube Shorts. [Gameplay video guide](gameplay-video.md#claude-plays-glob-clips) · [Twitch channel setup](https://help.twitch.tv/s/article/channel-page-setup?language=en_US)

Use the first four weeks as a baseline. Review Twitch discovery sources, weekly featured-window unique and average concurrent viewers where available, clip views, and follows. Use matched windows on the continuous feed for comparison and keep raids or collaboration traffic visible in the notes. Track browser play clicks from Twitch with a tagged link if attribution is available. A four-week sample can suggest changes to promotion or scheduling. [Twitch Discovery Analytics](https://help.twitch.tv/s/article/discovery?language=en_US) · [Website analytics](website-analytics.md)

Public observations are directional. Claude Plays Pokémon averaged 1,551 viewers in its first tracked 48 hours and about 16–22 in tracked July 2025 sessions. The independent Claude Plays Games channel averaged about five over 579 tracked hours in a November 2026 snapshot. Beyond All Reason's established official channel averaged 272–304 during its November 7–8 Omega event and 79–93 during two regular King of the Hill streams. The seasons, games, audiences and promotional exposure differ. These observations motivate treating scheduled challenges and clips as ways to introduce the continuous feed. [Claude Plays Pokémon history](https://twitchtracker.com/claudeplayspokemon/streams) · [Claude Plays Games tracking](https://lurkology.com/claude_plays_games) · [Beyond All Reason tracking](https://streamervitals.com/beyondallreasonofficial)

## Broadcast setup and verification

The tracked [Linux rig](../tools/twitch-stream/README.md) ran local recordings and Twitch ingest tests on 2026-11-24. Twitch bandwidth-test sessions are hidden from the public channel. The game ran from Globulation2/glob2 master `898fb00afc` using its existing launch options. `stream.sh live` retains its explicit `--i-mean-it` switch.

`supervisor.py` runs the show:
- **Game and stream.** It keeps the game, stream and chat host running and checks the 1920×1080 window before every match.
- **Opponents.** It assigns each match an opponent, rotating through Cortex, Nicowar and Cabino (Medium in the game's AI list) and Maxima (Hard), least recently played first.
- **Player sessions.** It runs one sandboxed `claude -p` player session per match.
- **Bookkeeping.** The player records setup, captions and results through the `stream-ctl` MCP tools. The supervisor keeps the official record in local state and publishes `status.json` for the chat host and `status.py`.

The rig ran on the maintainer's Linux laptop: Ubuntu 24.04, an NVIDIA RTX 3070 Ti Laptop GPU and PipeWire audio.

- The game draws on a hidden 1920×1080 Xvfb display. Vulkan (`sdl-gpu`) rendered on the NVIDIA GPU and presented into Xvfb. On Xvfb, OpenGL would have fallen back to software rendering.
- Only the game's audio reaches the stream, through a dedicated null sink. SDL3's PipeWire backend ignored `PULSE_SINK`, and PipeWire's remembered routing sent the first test session's music to the laptop speakers. The scripts now force the PulseAudio backend and move audio by display (`route-audio.sh`).
- ffmpeg captures the display and the sink and encodes with NVENC: H.264 1080p60 at 6000 kbps CBR (1080p30 at 4500 kbps until 2026-11-24, when viewers saw judder), 2-second keyframes and 160 kbps AAC. The [match caption command](../tools/twitch-stream/README.md#match-caption) puts the opponent, record from the game log, goal and latest confirmed move into the overlay. Free text handles intermissions and results.
- **Branding.** A small corner overlay sits bottom right over the map: the approved Globulation 2 wordmark (a crop-only derivative of the [Epic v5 product logo](../assets/epic-v5/product-logo-960x540.png), see [rig assets](../tools/twitch-stream/assets/README.md)), with `glob2.online` beneath it. It is 200 px wide at 1080p, 0.85 opacity, and 224 px from the right edge so it clears the game's sidebar and zoom controls. It is configurable or can be disabled (`BRAND=0`).
- A separate Claude Code MCP server, `glob2-stream`, connects to that game on port 27300, so a desktop game on the default port is unaffected.

### Linux test results

| Test | Result |
| --- | --- |
| Local recording, 12 s, Introduction tutorial | 1920×1080 H.264 at 30 fps, ~4.5 Mbps, 0 dropped frames. AAC audio peaks at −9.7 dB. Caption visible. |
| Twitch bandwidth test, 30 s | 874 frames sent at 4.5 Mbps, 1.03× real time. 25 frames dropped, most likely while the connection started. Exit 0. |
| Committed scripts, 5 s local recordings | NVENC auto-selected; the forced `libx264` fallback also produced 1080p30 with audio. |
| Branding, 6 s local recording | Wordmark and domain bottom right over the map, clear of the sidebar, minimap and zoom controls. 180 frames, 0 dropped, audio peak −9.3 dB. `BRAND=0`, text-only (missing logo) and logo-only variants also checked. |
| Key handling | ffmpeg prints the full ingest URL on connection errors. `stream.sh` masks the key in its output and logs; checked with a fake key against an unreachable ingest. |

During script validation a short (2 s) Twitch bandwidth test also ran unintentionally, because a local settings file overrode test variables. That precedence bug is fixed. The run was bandwidth-test only, and no key appeared in its log.

### Smoothness fix (2026-11-24)

The first live hour looked like 5–10 fps on Twitch. Three measured causes, fixed in turn:

1. **Overlays in RGB.** The caption and logo graph used about 3 CPU cores and starved capture. Converting to yuv420p first cut it to about half a core.
2. **30 fps sampling.** Sampling a game that draws unevenly faster than 30 fps judders. The stream now runs 1080p60 at 6000 kbps (Twitch's maximum frame rate and non-partner bitrate).
3. **Xvfb.** The game itself drew only about 12 fps (its MCP `frame_id` counter), because Xvfb lacks DRI3 and every GPU frame went through the CPU. Weston with Xwayland reached about 40 fps but captured black. A headless X server on NVIDIA's X driver (`display/install-xorg-display.sh`, `STREAM_DISPLAY_BACKEND=xorg`) holds 59–60 fps without touching the desktop session.

After all three, a 16 s pull of the public stream with streamlink showed 1920×1080 at 60 fps with 959 of 960 frames distinct, and the user confirmed it looks good. Earlier pulls: 30 distinct frames per second at 30 fps, then about 54 at 60 fps on Xvfb (mostly repeated content).

### Scoreboard

The caption shows the game number and overall record ("vs Nicowar · Game 2 · overall 1W–0L–0D"); the head-to-head record stays in `match_info` and the chat host's status. The first caption showed only the record against the current opponent, which read as 0 wins right after a win against a different AI.

### Unattended operation (2026-11-24)

At the user's request the rig now starts at boot without a login: a systemd user service runs the supervisor (live, with chat), on top of the enabled display, firewall and proxy system services and lingering for the operator. **Reboot test passed (2026-11-24, 12:47 local).** With nobody logged in, the display, firewall and proxy services and the user service came up on their own. The supervisor's first start failed its Twitch token check before DNS was ready; systemd retried 20 s later and it ran, and `wait-ready.sh` now also waits for DNS. Within about 10 minutes: game at 59.6 fps on the NVIDIA display, the public stream 1080p60 with 953 of 960 frames distinct, the chat host connected and answering, and a player session running. The reboot ended match 3 mid-game, and the recovery session set up a fresh game under the same number, hiding the first one's outcome; match control now refuses a second setup on a different map for one match number, so the lost game gets recorded as aborted first. Hourly check-ins by Claude run for the rest of 2026-11-24 to tune prompts and fix issues.

### Camera for viewers (2026-11-24)

The user asked that the chat host be able to move the camera, zooming out and showing what viewers ask about, while the player keeps playing. Decision: the player still runs the show camera and narrates, and the chat host can additionally show viewer requests. Both move it only through one code gate (`tools/twitch-stream/chat/camera.py`): zoom 100% or wider, rate limited, cleaned labels, and a viewer-request hold of about 40 s during which the player's camera moves are refused. The player's policy denies `game_view`, so it can't bypass the gate; the chat host's only state change is the camera. Tested on a separate test game: moves, zoom refusals, frame widening, hold, label expiry, token never in any output, and a simulated "show me Claude's base" request answered with a labelled camera move.

### Game control owned by the rig (2026-11-24)

The player used to hold its game-control token in context. In game 22 an aggressive compaction dropped it, the lease stayed held, and the colony ran on autopilot while the player told viewers it couldn't control anything. The user called it a harness flaw. The player's game connection is now `game_proxy.py`, which takes, renews and releases control itself and injects the token, so the model never sees one; tested on a separate game (lost lease re-acquired, leftover lease adopted, release on exit or SIGTERM, no token in output) and with a Claude session calling a control tool without a token. Upstream suggestion for the game's MCP server: tie control to the MCP session or connection instead of a token argument, so no agent harness has to carry one.

### Smooth camera drift (2026-11-24)

The user found the picture lifeless between camera cuts and saw globs walk off-screen. The chat agent now runs `chat/camera_drift.py`: between explicit moves it pans slowly toward fresh alerts, nearby enemy units or Claude's moving units, else circles the last target, using tiny middle-button drags (arrow keys scrolled ~38 tiles/s, far too fast). On a test game it steered the view toward a target within 0.6 tiles of its own tracking, followed moving worker groups without jitter after target smoothing, paused after explicit moves, and added ~60 ms median latency to other MCP calls. Smoothness on the 60 fps NVIDIA display is judged after deployment. `game_world` detail full reports per-unit tile positions (`colony.unit_list`, `others.unit_list`) and the current view rectangle, which the drift uses.

## Gaps and next work

- **24/7 operation.** The supervisor restarts failed streams, sessions and the chat host, and caps log growth. Still to verify before an unattended public run:
  - several hours of picture and audio;
  - long matches near the session limit;
  - model quota or sign-in expiry (set up long-lived authentication, for example with `claude setup-token`);
  - systemd user units, so the run survives a reboot.
- **Model cost.** The first supervised test cost about $1.09 for 2.5 minutes of match setup and early play with Sonnet 5.5, roughly $25 an hour if sustained, or about $600 a day for 24/7. Confirm the budget, or plan scheduled hours, before an unattended run. The supervisor logs every turn's cost.
- **Gameplay quality.** Watch the first supervised matches for setup accuracy, camera variety, narration pace and lease renewal, and refine `prompts/player.md` and the playbook from what is seen.
- **Agent sandbox.** On the streaming machine: run `sandbox/install-agent-sandbox.sh`, have the user create and install the agents' Claude token (`claude setup-token`), then run `sandbox/verify-sandbox.sh` until all checks pass. Rerun the installer after each `git pull`.
- **Chat host.** The `globulation2` account is authorized for `chat:read` and `chat:edit`, and the rig refreshes its token automatically over HTTPS. Replies need `TWITCH_BOT_USER`, the user's go-ahead and a staffed human moderator before chat interaction is promoted.
- **Tags.** Apply the recommended tags in Stream Manager.
- **Other Linux hardware.** Testing covered the NVIDIA/Vulkan setup above. The libx264 path was verified locally.
- **Account readiness.** Backup access, recovery coverage and moderator roles for the channel remain unverified (see the [account inventory](../facts/social-media-accounts.md)).
