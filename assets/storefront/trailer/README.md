# Storefront-v2 gameplay trailer

[Manifest](manifest.json) · [Master contact sheet](contact-sheet-master-30s.jpg) · [Edit data](tools/trailer-realtime.json) · [Footage rule](../../../planning/gameplay-video.md) · [Independent review](../review/trailer-review.md) · [Desktop captures](../captures/desktop/README.md)

Re-recorded **2026-11-27** in real time on **master at `46ef8e2276` (Release 0.11.9.1)**, from a macOS release build made locally from that commit. It replaces the trailer of 2026-11-24, which was filmed tick by tick on 0.11.7.0 + 15 commits ([its README](https://github.com/Globulation2/glob2-marketing/blob/bf6825ac086dfaac927a0a85e333ba06df4c97e1/assets/storefront/trailer/README.md); its cuts, with 2160p, are kept outside the repository in `../storefront-v2-renders/trailer-tick-stepped-2026-11-24/`).

Why it was re-recorded: master has the upgraded HD building art, ground shadows and calmer shore water. The tick-by-tick capture also scrambled the water: the game held between ticks for about two seconds a frame while its water animation kept running on real time, so each frame showed the water at an unrelated point in its cycle. Recording at normal speed shows the water as a player sees it.

Every frame is the game's own picture, recorded by the game's built-in gameplay recorder while the match played at its normal speed (30 ticks a second). Nothing is AI-generated, stock, retouched, sped up or slowed down. The matches are the same as before: both replayed on master to the same final checksums, so every fight and colony is at the same tick and tile. The only things laid over the game picture are the text cards, the wordmark and, in the desktop variant, an enlarged copy of the game's own Hive card from the same frame. The camera pans and punch-ins are done in the edit, as crops of the recorded frame (see [Framing](#framing)).

## Files

### Where the files live

The repository keeps this README, [manifest.json](manifest.json), [tools/](tools/), the posters, the contact sheets and the AppStream WebM (`glob2-trailer-30s-1080p.webm`, about 54 MB, committed because AppStream metadata needs a stable URL for it). The 9 MP4 cuts (about 0.7 GB) are **not committed**: they live in `../storefront-v2-renders/trailer/` relative to the repository root (`/Users/bradley/glob2/storefront-v2-renders/trailer/` on the machine that made them), and [.gitignore](.gitignore) here ignores `*.mp4`. Their bytes and SHA-256 are in the manifest. The [store packages](../store-packages/README.md) link each store's trailer from whichever place holds it.

**1080p only.** A real-time recording is limited to the screen: the largest map window of a take is 2560×1440, so no 2160p files are made. Uses that took 2160p files (the Steam package and YouTube) take the 1080p files instead.

| File | What | Use |
| --- | --- | --- |
| `glob2-trailer-30s-1080p.mp4` | Master, 30 s, 1920×1080, English text | YouTube, Microsoft Store, itch.io, Snap, Google Play via YouTube, Steam, GOG |
| `glob2-trailer-30s-1080p.webm` | Master, 30 s, 1920×1080, VP9 and Opus in WebM | AppStream / Flathub metadata |
| `glob2-trailer-30s-preview-720p.mp4` | Master, 1280×720, 22 MB | Review link, chat and email previews; not a store upload |
| `glob2-trailer-30s-textless-1080p.mp4` | Same cut with no text and no wordmark | Epic, platforms that localise with their own captions, re-cuts |
| `glob2-trailer-30s-ja-1080p.mp4`, `glob2-trailer-30s-ar-1080p.mp4` | Master with Japanese and Arabic text | Proof that every locale is one command; other locales are not rendered yet |
| `glob2-trailer-desktop-34s-1080p.mp4` | Desktop variant, 34.5 s: the master plus one 4.5 s co-play beat | Desktop stores whose copy may mention AI co-play (not the Mac App Store or Epic while `ai_coplay` is false there) |
| `glob2-trailer-15s-1080p.mp4` | 15-second cutdown, three lines | Social, short placements |
| `glob2-trailer-30s-vertical-1080x1920.mp4`, `-textless-1080x1920.mp4` | Vertical 1080×1920 of the master (upscaled 1.33×, see [Derivatives](#derivatives)) | Shorts, Reels, TikTok; not an Apple app preview |
| `poster-1920x1080.png`, `poster-3840x2160.png` | Poster: the opening fight at its punch-in (master 1.0 s); the 3840 file is a 1.5× upscale | Microsoft trailer thumbnail, YouTube thumbnail |
| `contact-sheet-*.jpg` | One frame every 0.5 s of each cut | Review |

Every MP4: H.264 High profile, yuv420p, BT.709, constant 30 fps, AAC-LC stereo 48 kHz, `+faststart`. The WebM is VP9 (yuv420p, 30 fps; WebM stores timestamps in whole milliseconds, so frame steps read 33 or 34 ms) with Opus stereo 48 kHz. Sizes, durations, loudness, true peak and SHA-256 are in [manifest.json](manifest.json).

## Shot list (master)

The edit is the one of 2026-11-24, re-framed for the new recordings by [tools/make_realtime_edit.py](tools/make_realtime_edit.py) into [tools/trailer-realtime.json](tools/trailer-realtime.json). Ticks are unchanged.

| # | Time (s) | Shot, frames | Match, seat | Ticks | What it shows | Text |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0–2.5 | `f-battle-honey-close` 0–74 | honeycomb (honeycomb-isle 2102), checkpoint 66000, seat on red (Maxima) | 67450–67524 | Opens inside a fight: red warriors (Maxima AI) and lime warriors (Cortex AI) in melee east of the central oasis | — |
| 2a | 2.5–3.63 | `f-place` 0–33 | fsq-mix (FourSquares1), checkpoint 60000, seat on red | 60300–60333 | Build mode with the real build palette in frame: the seat arms the Inn and its ghost glides in | — |
| 2b | 3.63–5.8 | `f-place` 34–98 | same take | 60334–60398 | Cut-in: the ghost lands, the seat clicks, the site's scaffold appears, workers head for it | `trailer_line_1` from 3.8 |
| 3 | 5.8–8.5 | `f-place` 125–205 | same take | 61165–61245 | 740 ticks later, a cut inside the take: workers at the scaffold; the Inn completes | `trailer_line_1` |
| 4 | 8.5–12.0 | `f-fed` 20–124 | fsq-mix, checkpoint 60000, seat on red | 60520–60624 | Wheat fields, workers harvesting and carrying, inns below them; the camera drifts | `trailer_line_2` |
| 5 | 12.0–15.0 | `f-cabino` 0–89 | fsq-mix, checkpoint 60000, seat on lime (Cabino) | 60300–60389 | A second colony (lime, Cabino AI) at work around its swimming pool | — |
| 6 | 15.0–18.5 | `f-battle-honey` 75–179 | honeycomb, checkpoint 66000, seat on red | 67525–67629 | Back at the oasis fight, wider | `trailer_line_3` |
| 7 | 18.5–21.5 | `f-battle3` 0–89 | honeycomb, checkpoint 66000, seat on red | 67780–67869 | Wide: the red colony, the contested oasis, the lime swarm across the road | — |
| 8 | 21.5–26.0 | `f-hero` 0–134 | fsq-mix, checkpoint 60000, seat on red | 60620–60754 | The whole red colony on its island; most of it is under the colony's own clearing zone (yellow), which the AI painted at that time | `trailer_line_4` |
| 9 | 26.0–30.0 | `f-econ` 0–119 | fsq-mix, checkpoint 48000, seat on red | 48400–48519 | The centre of the red colony, earlier in the same match; the wordmark fades in at 27.0 s | — |

Shot 1 is a second take of the same ticks as shot 6, recorded at the old zoom for a native punch-in (the matches are deterministic, so both takes show the same fight). The text lines and their placement are unchanged from 2026-11-24.

## Framing

The recording window is 3024×1666 on the capture Mac's Retina screen at UI scale 1, so the HUD is the same physical size as in the old 4256×2800 frames, but the map area is 2624×1634. Each take keeps the old framing at a fraction (`scale`) of its old pixel size: the in-game zoom is the old zoom times `scale`, the camera is centred on the same tile, then moved down a few pixels with the game's own map drag so the crop clears the event list at the top left ([tools/realtime.json](tools/realtime.json)).

| Segment | Take scale, in-game zoom | Crop of the 3024×1666 frame | 1080p |
| --- | --- | --- | --- |
| Opening fight (punch-in), poster | 1.0, 200 % | 2560×1440 at 64, 223 | 0.75× |
| Build palette (2a) | 1.0, 150 % | 2304×1296 at 720, 214, flush with the right edge so the palette is whole | 0.83× |
| Placement cut-in and completion (2b, 3) | 1.0, 150 % | 1920×1080 at 72, 279 | 1:1 native |
| Shots 5, 6, 7 | 0.667 | 2560×1440 at 32, 214 | 0.75× |
| Shots 4, 8, 9 (camera drift) | 0.6 | 2304×1296 sliding 0.9 px a frame from x 160 | 0.83× |
| Desktop co-play | 1.0, 150 % | 1920×1080 at 405, 220, ending above the HUD's "Stop commander" button | 1:1 native |

No landscape picture is upscaled. The camera drift that used to be a middle-button drag in the game is now a crop sliding over the recorded frame, because a remote drag during a real-time recording would judder.

## Desktop variant: the co-play beat

| # | Time (s) | Shot, frames | Match, seat | Ticks | What it shows | Text |
| --- | --- | --- | --- | --- | --- | --- |
| 9 | 26.0–30.4 | `f-coplay2` 18–149 | fsq-mix, checkpoint 60000, seat on red (Maxima) | 60478–60609 | The agent's standing order lays four Inn sites one after another around the colony's inn cluster; workers start on each. Bottom left, the game's own Hive card shows `inn-plan` and `Active` | `trailer_line_ai_coplay`, at the top of the frame |

The last shot of the desktop cut runs 3 frames longer (123 frames) to keep 34.5 s, because the co-play shot starts at frame 18: in real time the install is queued, and the Hive card first shows at frame 17.

Filmed honestly, as before:

- The AI agent editing this trailer (Claude, driving the game over MCP) installed one real **Hive standing order** with `hive_program install` at tick 60470: [tools/coplay_order.js](tools/coplay_order.js), interval 25 ticks, plan "four Inns near tile (8, 118)". Everything on screen that the agent caused comes from its four ordinary `create` orders; the colony's own AI keeps playing. The request and response record (no token) is in [manifest.json](manifest.json) under `mcp_transcripts`.
- **The card is different on master.** It shows the order's name, its state and the game's Pause and Cancel buttons, but no longer the order's live output, so the step counter of the old trailer is not in this one.
- **How the card is framed.** In the game the card sits bottom left, below the "Reports / details" and "Stop commander" buttons. Commander is a paid service that no listing may show. The main window ends above that stack (y 1300; the button starts at y 1326), and the card is a separate inset cut from its own top edge to its bottom edge, found anew in every frame. [tools/check_hud.py](tools/check_hud.py) confirms for all 132 inset frames that no button fill or gold border from above the card is in the inset.

## Derivatives

- **15 s cutdown:** the same structure as before (fight, palette and placement, completion, wheat fields, oasis fight, red colony, wordmark), three lines.
- **Vertical:** the master's timeline and text, each shot a 9:16 window of 810×1440 native pixels centred on the master's framing, **upscaled 1.33× to 1080×1920**: the recording is 1666 pixels tall, so a native 1920-pixel-tall window does not exist. The text is centred at 60 % of the height, as before.
- **Apple app previews: not made.** They need captures of the iOS and Mac apps.

## How it was filmed

- **Build:** master at `46ef8e2276` (Release 0.11.9.1, Globulation2/glob2#1989), built locally with `tools/dev_build.py release=1 bundle` (executable SHA-256 in the manifest). Same source as the release tag; not the store binary.
- **Matches:** the headless AI-versus-AI matches of 2026-11-24, re-run on master with the same maps, seeds and AIs (`fsq-mix`: FourSquares1, seed 2202, Maxima, Cabino, Nicowar and Cortex; `honeycomb`: honeycomb-isle seed 2102, Maxima, Cortex, Maxima and Cortex). Both reached the same final checksums as before (2113040471 and 760558595), so the simulation is unchanged. [../captures/desktop/tools/matches.json](../captures/desktop/tools/matches.json).
- **Seat:** each take loads a checkpoint with one local player added to one colony's team next to its AI ([join-seat.py](../captures/desktop/tools/join-seat.py)), so the camera, interface and fog of war are a real player's.
- **Recording:** [tools/capture_realtime.py](tools/capture_realtime.py) launches the game in a real window with its recorder on ([tools/launch-record-game.sh](tools/launch-record-game.sh), `--record`, 30 fps, H.264 CRF 12, a recording chapter every 30 ticks), loads the save, holds the match, frames the camera, runs to 90 ticks before the shot, then lets it play at normal speed. The seat's inputs fire when their tick comes up; the Inn ghost's glide runs on its own thread at about 30 moves a second. Frames are then taken from the recording at the time each tick was reached, using the chapter times.
- **Settings:** HD artwork forced on, clouds and cloud shadows off, health and food bars off (the in-game toggle; on the capture Mac's Colemak layout the physical L key types the bound "i").
- **Zones:** the colony's clearing, forbidden and guard zones are **left as the AI paints them** (user decision, 2026-11-27). In real time the old erasing could not keep up with the AI repainting, so zones popped in and out; erasing also changed the AI's play.
- **Recorder drops:** 0–1 frames per take, all outside the cut, except one **held frame in shot 8** (`f-hero` frame 115, master 25.33 s), where the game took longer than a frame on one tick, so two ticks show the same picture. That is how the game played.

## Footage label (AI versus AI)

Every colony on screen is played by the game's built-in AIs, in matches with no human player: **AI-versus-AI footage, a spectator view** in the sense of the footage rule, recorded in real time at normal speed from a player seat that shares one colony with its AI. The seat's own inputs (listed per shot in the manifest): in the placement shot, arming the Inn, gliding the pointer, one left click to place the site and one right click to leave build mode; in the desktop co-play shot, one Hive standing order installed over MCP by the AI agent that edited this trailer. Nothing here is human-versus-human multiplayer.

## Text, wordmark and music

Unchanged from 2026-11-24: the lines `trailer_line_1`..`4` (and `trailer_line_ai_coplay`) from `translations/<locale>.md`, laid out by [tools/render_cards.py](tools/render_cards.py) in headless Chromium at each output size; the game's own wordmark over the last 3 s; the game's original soundtrack by Jacques-Paul Grivaz (GPL-3.0-or-later), the building and combat moods crossfaded as the game does. Measured in the master: −14.6 LUFS integrated, −2.0 dBTP true peak.

## Review

Checked by eye and by tool on 2026-11-27:

- **Contact sheets** (one frame every 0.5 s): [master](contact-sheet-master-30s.jpg), [text-free master](contact-sheet-master-30s-textless.jpg), [desktop](contact-sheet-desktop-34s.jpg), [15 s](contact-sheet-15s.jpg), [vertical](contact-sheet-vertical-30s.jpg). Every half second shows colonies or a fight.
- **Water:** in a recording at normal speed the shore and lake water change a little more with every frame (measured on a test recording: 0.26 grey levels one frame apart, 2.9 ten frames apart, 5.4 at 120), so it animates smoothly at its own speed.
- **Placement:** the Inn's scaffold is visible from the click onward and the Inn completes in shot 3. (A first take of this shot showed no site after the click, for a reason not found; placed directly, the site draws normally on master, and the re-take shows it.)
- **Frame timing** (`review.py --timing`, every file): constant 30 fps in every MP4; exact cut points as in the edit.
- **HUD** (`check_hud.py`, all 1,935 frame and crop pairs the cuts use, 132 of them with the card inset): no event-list text in any crop, no Hive-card button along any crop's bottom edge, every crop below the top bar; the inset contains no "Reports / details" or "Stop commander" button. Master's card writes its name and state in anti-aliased text, so the check allows up to 20 button-coloured pixels above the card's own buttons (at most 9 were found, all on the text; a button would be hundreds, with a gold border).
- **Zones:** steady throughout (no pop-ins); in shot 8 the colony's clearing zone covers most of the island.

Known compromises:

- 1080p only, and the vertical cut is upscaled 1.33×.
- Shot 8 is mostly under the clearing zone (kept by user decision, 2026-11-27).
- One held frame in shot 8 (25.33 s).
- The follow-ups the 2026-11-24 review left open still apply (pacing of the last 8.5 s, one fight location, the co-play beat after Steam's ten-second window, the Arabic line 4 wording, the Thai line break): see [the previous README](https://github.com/Globulation2/glob2-marketing/blob/bf6825ac086dfaac927a0a85e333ba06df4c97e1/assets/storefront/trailer/README.md#follow-ups-not-done-in-the-fix-round).

## Reproduce

Paths: `R` is a working directory outside the repository (the 2026-11-27 run used `/Users/bradley/glob2/storefront-v2-renders/trailer-raw/`, which keeps the matches, takes, cards and reports). `GLOB2` is the game build's executable; `GLOB2_GAME` the game checkout (for the soundtrack).

```sh
cd assets/storefront/trailer
# 1. The matches (same maps, seeds and AIs as in matches.json; check the final checksums)
../captures/desktop/tools/run-match.sh $R/matches/fsq-mix $R/maps/FourSquares1.map.gz 2202 72000 6000 maxima cabino nicowar cortex
../captures/desktop/tools/run-match.sh $R/matches/honeycomb $R/maps/honeycomb-isle-2102.map.gz 2102 72000 6000 maxima cortex maxima cortex

# 2. The takes, in real time (a real window takes over the screen; keep the mouse off it).
#    A finished take is kept on a rerun; --refilm films it again.
uv run --with pillow --with numpy python tools/capture_realtime.py tools/shots.json tools/realtime.json $R/rt --matches $R/matches

# 3. Text cards at the 1080p sizes
uv run tools/render_cards.py --locale en,ja,ar --out $R/cards --size 1920x1080,1080x1920

# 4. The edit, cut, encode, music and poster
python3 tools/make_realtime_edit.py
bt() { uv run --with pillow --with numpy python tools/build_trailer.py "$@" --data tools/trailer-realtime.json --raw $R/rt --work $R/work --out $OUT --no-4k; }
bt master,desktop,cut15,vertical --cards $R/cards
bt master --only text --locale ja,ar --cards $R/cards
bt master --only poster

# 5. Review and manifest
for f in $OUT/*.mp4; do uv run tools/review.py $f --timing > $R/timing/timing-$(basename ${f%.mp4}).json; done
uv run --with pillow --with numpy python tools/check_hud.py $R/rt --data tools/trailer-realtime.json --step 1 > $R/check_hud.json
uv run --with pillow --with numpy python tools/finalize_trailer.py $OUT --raw $R/rt --data tools/trailer-realtime.json \
  --cards $R/cards --extra tools/manifest-extra.json --timing $R/timing --hud-check $R/check_hud.json --work $R/work
```

The tick-by-tick method ([tools/capture_shot.py](tools/capture_shot.py) with [tools/trailer.json](tools/trailer.json)) still works and gives 2160p, but its water is scrambled (see the top of this README).

## Tools

| File | Purpose |
| --- | --- |
| [tools/launch-record-game.sh](tools/launch-record-game.sh) | Start the build with the capture settings, off-screen or in a real window, optionally recording |
| [tools/capture_realtime.py](tools/capture_realtime.py), [tools/realtime.json](tools/realtime.json) | Record the takes in real time with the game's recorder and extract one frame per tick; per-take scale and camera nudge |
| [tools/capture_shot.py](tools/capture_shot.py), [tools/shots.json](tools/shots.json) | The shot definitions (ticks, cameras, seat inputs), and the older tick-by-tick capture |
| [tools/coplay_order.js](tools/coplay_order.js) | The Hive standing order of the co-play beat |
| [tools/make_realtime_edit.py](tools/make_realtime_edit.py), [tools/trailer-realtime.json](tools/trailer-realtime.json) | Re-frames the edit of [tools/trailer.json](tools/trailer.json) for the real-time takes |
| [tools/render_cards.py](tools/render_cards.py), [tools/cards.html](tools/cards.html) | Text cards and wordmark, rendered by Chromium; sentence-aware line breaks |
| [tools/build_trailer.py](tools/build_trailer.py) | Cuts, per-segment framing (and sliding crops), insets, text cues, music plan, encodes, poster |
| [tools/review.py](tools/review.py) | Contact sheets and frame-timing report |
| [tools/check_hud.py](tools/check_hud.py) | Checks that no unwanted HUD reaches into any crop, and that the co-play inset leaves out the buttons above the Hive card |
| [tools/finalize_trailer.py](tools/finalize_trailer.py), [tools/manifest-extra.json](tools/manifest-extra.json) | Manifest with hashes, ffprobe facts, loudness and true peak, shot sidecars, MCP transcript and review reports |

Scripts are `GPL-3.0-or-later`, like the game.
