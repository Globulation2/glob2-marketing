# Storefront-v2 gameplay trailer

[Manifest](manifest.json) · [Master contact sheet](contact-sheet-master-30s.jpg) · [Edit data](tools/trailer.json) · [Footage rule](../../../planning/gameplay-video.md) · [Independent review](../review/trailer-review.md) · [Desktop captures](../captures/desktop/README.md)

Made **2026-11-24** from real in-engine footage of Globulation 2 **0.11.7.0 + 15 commits, revision `5bf966285aa8`** on macOS. This is **not the public release binary**: it is the build installed at `/Applications/Glob2.app`, 15 commits after the `v0.11.7.0` tag, and it has MCP tools the release lacks (such as `game_time`, which stepped every frame of the capture). Its maps, AI roster and simulation are identical to the tag. Every frame is the game's own framebuffer, one simulation tick per frame, played at the game's normal speed. Nothing is AI-generated, stock, retouched, sped up or slowed down. The only things laid over the game picture are the text cards, the wordmark and, in the desktop variant, an enlarged crop of the game's own Hive card taken from the same frame. Some shots are punched in, which means cropped closer and scaled (see [Framing](#framing)).

Fix round, same day: the cuts were re-made after the [independent review](../review/trailer-review.md) (M1–M8, S4–S6). See [What changed in the fix round](#what-changed-in-the-fix-round).

## Files

### Where the files live

The repository keeps this README, [manifest.json](manifest.json), [tools/](tools/), the posters, the contact sheets and the AppStream WebM (`glob2-trailer-30s-1080p.webm`, about 30 MB, committed because AppStream metadata needs a stable URL for it). The 13 MP4 cuts (about 0.9 GB) are **not committed**: they live in `../storefront-v2-renders/trailer/` relative to the repository root (`/Users/bradley/glob2/storefront-v2-renders/trailer/` on the machine that made them), beside the captioned screenshot renders, and [.gitignore](.gitignore) here ignores `*.mp4`. Every MP4 is reproducible from the raw frames with `tools/` (see [Reproduce](#reproduce)); its bytes and SHA-256 in the manifest identify the exact file, and all 13 matched after the move on 2026-11-24. The manifest records this under `storage` and gives each deliverable a `location`. The [store packages](../store-packages/README.md) link each store's trailer from whichever place holds it.

| File | What | Use |
| --- | --- | --- |
| `glob2-trailer-30s-2160p.mp4` | Master, 30 s, 3840×2160, English text | Steam, Epic, YouTube for Google Play |
| `glob2-trailer-30s-1080p.mp4` | Master, 30 s, 1920×1080, English text | Microsoft Store (1920×1080), itch.io, Snap, Google Play via YouTube |
| `glob2-trailer-30s-1080p.webm` | Master, 30 s, 1920×1080, VP9 and Opus in WebM | AppStream / Flathub metadata (the spec asks for VP9 or AV1 in WebM or Matroska) |
| `glob2-trailer-30s-preview-720p.mp4` | Master, 1280×720, 16 MB | Review link, chat and email previews; not a store upload |
| `glob2-trailer-30s-textless-2160p.mp4`, `-textless-1080p.mp4` | Same cut with no text and no wordmark | Platforms that localise with their own captions, and future re-cuts |
| `glob2-trailer-30s-ja-1080p.mp4`, `glob2-trailer-30s-ar-1080p.mp4` | Master with Japanese and Arabic text | Proof that every locale is one command; other locales are not rendered yet |
| `glob2-trailer-desktop-34s-2160p.mp4`, `-1080p.mp4` | Desktop variant, 34.5 s: the master plus one 4.5 s co-play beat filmed with the game's MCP server driving the colony | Desktop stores whose copy may mention AI co-play (not the Mac App Store or Epic while `ai_coplay` is false there) |
| `glob2-trailer-15s-2160p.mp4`, `-1080p.mp4` | 15-second cutdown, three lines | Social, short placements |
| `glob2-trailer-30s-vertical-1080x1920.mp4`, `-textless-1080x1920.mp4` | Vertical 1080×1920 of the master, reframed from the native frames (downscaled or 1:1, never upscaled) | Shorts, Reels, TikTok; not an Apple app preview |
| `poster-1920x1080.png`, `poster-3840x2160.png` | Poster: the opening fight at its 1.5× punch-in (master 1.0 s) | Microsoft trailer thumbnail (1920×1080 PNG), YouTube thumbnail base |
| `contact-sheet-*.jpg` | One frame every 0.5 s of each cut | Review |

Every MP4: H.264 High profile, yuv420p, BT.709, constant 30 fps, AAC-LC stereo 48 kHz, `+faststart`. The WebM is VP9 (yuv420p, 30 fps; WebM stores timestamps in whole milliseconds, so frame steps read 33 or 34 ms) with Opus stereo 48 kHz. Sizes, durations, loudness, true peak and SHA-256 are in [manifest.json](manifest.json). The desktop variant was 33.5 s (`-desktop-33s-`) before the fix round; it is now 34.5 s, and the file name changed to `-desktop-34s-`.

## Shot list (master)

| # | Time (s) | Shot, frames | Match, seat | Ticks | Camera and framing | What it shows | Text |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0–2.5 | `f-battle-honey` 0–74 | honeycomb (honeycomb-isle 2102), checkpoint 66000, seat on red (Maxima) | 67450–67524 | tile (72, 63), 200 %, fixed; **1.5× punch-in** on the clash | Opens inside a fight: red warriors (Maxima AI) and lime warriors (Cortex AI) in melee east of the central oasis. | — |
| 2a | 2.5–3.63 | `f-place` 0–33 | fsq-mix (FourSquares1), checkpoint 60000, seat on red (Maxima) | 60300–60333 | tile (0, 124), 150 %, fixed; window **includes the real build palette** (1.35×) | Build mode: the seat arms the Inn at frame 10 and the right-hand palette shows it selected; every building shows its footprint; the Inn ghost glides in. | — |
| 2b | 3.63–5.8 | `f-place` 34–98 | same take, continuous ticks | 60334–60398 | same camera; **2× cut-in** on the placement | The ghost lands, the seat clicks (tick 60348, 4.1 s) and the site appears; right click leaves build mode (60358); workers head for the site. | `trailer_line_1` from 3.8 |
| 3 | 5.8–8.5 | `f-place` 125–205 | same take | 61165–61245 | same 2× window | 767 ticks (25.6 s) later, a cut inside the take: workers at the scaffold; the Inn completes at tick 61186 (6.5 s). | `trailer_line_1` |
| 4 | 8.5–12.0 | `f-fed` 20–124 | fsq-mix, checkpoint 60000, seat on red | 60520–60624 | tile (124, 112), 150 %, drifts 1.5 px/frame | Wheat fields from green to ripe, workers harvesting and carrying, inns below them; the far edge of the fields is dimmed by fog of war. | `trailer_line_2` |
| 5 | 12.0–15.0 | `f-cabino` 0–89 | fsq-mix, checkpoint 60000, seat on lime (Cabino) | 60300–60389 | tile (125, 64), 150 %, fixed | A second colony (lime, Cabino AI) at work around its swimming pool, swarms and inns. | — |
| 6 | 15.0–18.5 | `f-battle-honey` 75–179 | honeycomb, checkpoint 66000, seat on red | 67525–67629 | tile (72, 63), 200 %, fixed (not punched in) | Back at the oasis fight, wider: the next 3.5 s of the same exchange. | `trailer_line_3` |
| 7 | 18.5–21.5 | `f-battle3` 0–89 | honeycomb, checkpoint 66000, seat on red | 67780–67869 | tile (64, 59), 125 %, fixed | Wide: the red colony top left, the contested oasis with the clash on its east side, the lime swarm across the road; the forest top right is dimmed by fog of war. | — |
| 8 | 21.5–26.0 | `f-hero` 0–134 | fsq-mix, checkpoint 60000, seat on red | 60620–60754 | tile (0, 0), 100 %, drifts 1.5 px/frame | The whole red colony on its island, its buildings and globs at work. | `trailer_line_4` |
| 9 | 26.0–30.0 | `f-econ` 0–119 | fsq-mix, checkpoint 48000, seat on red | 48400–48519 | tile (0, 0), 125 %, drifts 1.5 px/frame | The centre of the red colony, earlier in the same match; the wordmark fades in at 27.0 s. | — |

Shot 1 opens on frame 0 of the take with the fight already under way: no logo, no black, no fade. Shots 2a, 2b and 3 are one take: 2a to 2b is a cut-in on continuous ticks, and 2b to 3 is the declared 740-tick skip. Shots 1 and 6 are the same take (0–74, then 75–179), so the master never repeats a frame. The desktop variant inserts the co-play shot between shots 8 and 9 (see below), which moves the last shot to 30.5–34.5 s and the wordmark to 31.5 s.

The four lines (`trailer_line_1`..`4` from `translations/<locale>.md`) sit over shots that show what they say. "You decide. They build." runs over the build palette, the Inn placed by the seat and completed by workers. "Keep the colony fed." runs over wheat fields, inns and carrying workers. "Fight rivals for the land." runs over the red and lime warriors fighting at the oasis. "No ads. No in-app purchases." runs over the whole red colony at work. The wordmark covers the last 3 s over live gameplay. There is no call to action, no "free", no store badge and no URL.

## Framing

The edit's default frame is the 3840×2160 map rectangle at (0, 200) of each 4256×2800 frame. It shows the map at the player's real camera and zoom, without the HUD. A segment can set its own 16:9 rectangle of the native frame instead (`crop` in [tools/trailer.json](tools/trailer.json)). Each output size is scaled straight from that rectangle (Lanczos), so the 1080p files are downscales or native pixels, and only the 2160p files upscale a punch-in.

| Segment | Native rectangle (w×h at x, y) | 1080p | 2160p |
| --- | --- | --- | --- |
| Default | 3840×2160 at 0, 200 | 0.5× | 1:1 |
| Opening fight (master shot 1, 15 s 0–1.5 s, poster) | 2560×1440 at 770, 630 (centred near map-rectangle 2050, 1150) | 0.75× | 1.5× upscale |
| Placement, palette (2a) | 2848×1602 at 1408, 40: the right-hand sidebar with the build palette, below the top bar, above the "Paused" label | 0.67× | 1.35× upscale |
| Placement, cut-in and completion (2b, 3) | 1920×1080 at 680, 846 | 1:1 native | 2× upscale |
| Desktop co-play | 2144×1206 at 901, 627, plus the Hive card inset | 0.9× | 1.8× upscale |

In the master that is 2.5 s at 1.5×, 1.1 s at 1.35× and 4.9 s at 2× of upscaled picture in the 2160p file. The desktop variant adds 4.5 s at 1.8×.

## Desktop variant: the co-play beat

| # | Time (s) | Shot, frames | Match, seat | Ticks | Camera and framing | What it shows | Text |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9 | 26.0–30.5 | `f-coplay2` 15–149 | fsq-mix (FourSquares1), checkpoint 60000, seat on red (Maxima) | 60475–60609 | tile (8, 119), 150 %, fixed; **1.8× on the four Inn sites** around tile (8, 118) | The agent's standing order lays four Inn sites one after another around the colony's inn cluster: left at 26.8 s, right at 27.6 s, below at 28.5 s and above at 29.3 s. Workers start on each one. Bottom left, the game's own Hive card shows `inn-plan`, `Active` and the order's live output, its step counter advancing with each site (`{"at":[5,118],"of":4,"placing":"inn","step":1}` … `step":4}`, then `{"done":[…]}`). | `trailer_line_ai_coplay`, **at the top of the frame**, 26.4–30.2 |

Filmed honestly, as the brief requires:

- The game ran with its embedded MCP server on (as in every shot). The AI agent that edited this trailer (Claude, driving the game over MCP) installed one real **Hive standing order** with `hive_program install` at frame 10 of the take (tick 60470): [tools/coplay_order.js](tools/coplay_order.js), interval 25 ticks, plan "four Inns near tile (8, 118)". Each run reads the colony's own fog-filtered view of the ground (`map.region`), picks the nearest free grass footprint and returns one ordinary `create` order. It ran every 25 ticks from tick 60495 (observed in the order's own reports: step 1 submitted at 60495, step 3 at 60545), and at 60595 reported `done: [[5,118],[11,118],[8,121],[7,115]]`. Everything on screen in that shot that the agent caused comes from those four orders; the colony's own AI keeps playing as in every other shot.
- The full MCP request and response record of that shot (hive_status, hive_program install, list and inspect, with the program source and its outputs; no token) is in [manifest.json](manifest.json) under `mcp_transcripts`.
- Nothing was staged: no tool call is shown that did not happen, and no text was added beyond `trailer_line_ai_coplay`. The Hive card is the game's own interface, not an overlay drawn for the trailer.
- **How the card is framed.** In the game, the card sits at the bottom left, below a stack of two buttons ("Reports / details" and "Stop commander"). Commander is the name of a paid service that no listing may show. The main picture is a 1.8× window on the sites that ends well above the card stack. The card is shown as a separate inset in the bottom-left corner, cut from the same frame. The cut runs from the card's own top edge to its bottom edge, so the buttons above it stay out. The card grows upwards as its output gets longer, so its top edge is found anew in every frame (`card_top` in [tools/build_trailer.py](tools/build_trailer.py); the edges per frame are in the manifest under `inset_card_tops`). Nothing inside the card or the main window is altered. The inset is drawn at native pixels in the 1080p file and at 2× in the 2160p file, with a soft drop shadow behind it. [tools/check_hud.py](tools/check_hud.py) confirms for all 135 frames that no button fill or gold border from above the card is inside the inset.
- The line sits at the top of the frame for this one shot, with its scrim hanging from the top edge, so the scrim leaves the card and the sites clear.
- A first take of this shot (`f-coplay`, not used) failed honestly: the seat's zone erasing filled the 64-order human order queue, the game rejected the order's submission ("Human order queue full") and paused the program. The used take erases zones only every 15 frames.
- The desktop variant is for stores whose listing may claim AI co-play. Per `translations/platforms.json`, `ai_coplay` is false for the Mac App Store and Epic until verified, so use the master there.

## Derivatives

- **15 s cutdown** (`glob2-trailer-15s-*`): fight (1.5×, 0–1.5 s), palette and placement (1.5–3.5 s), the Inn completing (3.5–4.8 s), wheat fields (4.8–5.8 s), the oasis fight (5.8–9.0 s), the red colony (9.0–12.3 s) and the wordmark shot (12.3–15.0 s). It carries three lines: `trailer_line_1` 1.8–4.8 s, `trailer_line_3` 6.0–8.8 s and `trailer_line_4` 9.4–12.2 s. That gives 3.0, 2.8 and 2.8 s on screen, with 1.2 and 0.6 s of clean picture between them. "Keep the colony fed." is dropped; the wheat fields stay as a 1 s picture beat. The wordmark fades in at 12.5 s.
- **Vertical** (`glob2-trailer-30s-vertical-*`): the master's timeline and text. Each shot is reframed by a 1215×2160 window of the native map rectangle, downscaled to 1080×1920 (x per segment in `tools/trailer.json`, `vertical.reframe`). Shot 7 is the exception: it uses a native 1080×1920 window at 1:1. Shot 5 sits on the lime colony's west building cluster (window x 560): two huts, three inns, the school and the pool. Shot 7 is centred on the clash (window x 1960, 240 px below the top of the map rectangle). The punch-ins of the landscape cut do not carry over; the vertical framing already fills the frame with the clash. The text is centred at 60 % of the height, above the band that Shorts, Reels and TikTok cover with their own captions and buttons. "No ads. / No in-app purchases." breaks between the two sentences.
- **Apple app previews: not made.** Apple wants device captures of the iOS app (886×1920 or 1920×886 on iPhone, 1200×1600 on iPad, 15–30 s, at most 30 fps). This footage is the desktop interface; follow up with a capture from the iOS build on a simulator or device.

## How it was filmed

- **Build:** 0.11.7.0 + 15 commits, revision `5bf966285aa8`, at `/Applications/Glob2.app` (executable SHA-256 in the manifest, `build.public_release: false`). It is not the public release binary; its maps, AI roster and simulation are identical to the `v0.11.7.0` tag. macOS 26.6, Apple silicon.
- **Matches:** real headless AI-versus-AI matches run by that build (`glob2 game run`, one AI per colony, a save every 6,000 ticks), the same ones the desktop screenshots use. `fsq-mix` is bundled map FourSquares1, game seed 2202, with Maxima, Cabino, Nicowar and Cortex. `honeycomb` is generated `honeycomb-isle` seed 2102, 128×128, with Maxima, Cortex, Maxima and Cortex. Maps, seeds and commands: [../captures/desktop/tools/matches.json](../captures/desktop/tools/matches.json).
- **Seat:** each shot loads a checkpoint with one local player added to one colony's team next to its AI ([join-seat.py](../captures/desktop/tools/join-seat.py)), so the camera, interface and fog of war are a real player's. The AI keeps playing the colony.
- **Window and renderer:** off-screen 4256×2800 window (SDL dummy video driver), `--renderer portable-sdl`, `--ui-scale 2`, high-resolution artwork forced on, clouds and cloud shadows off, health and food bars off (in-game toggle, key I), MCP UI server on port 47814 in a fresh temporary profile. [tools/launch-record-game.sh](tools/launch-record-game.sh).
- **Frames:** [tools/capture_shot.py](tools/capture_shot.py) runs the match to the shot's start tick and holds it. Then, for every frame, it steps exactly one simulation tick (`game_time step ticks=1`), performs that frame's scripted seat inputs, and saves the next rendered frame at native pixels (`ui_screenshot`). The game runs at 30 ticks a second, so 30 frames a second is real gameplay speed. The sidecar of every shot lists the tick of every frame. [tools/finalize_trailer.py](tools/finalize_trailer.py) checks that each frame is exactly one tick after the one before. The only exception is the declared cut inside the placement take (740 ticks).
- **Why not a screen recording:** the game's own recorder cannot read the off-screen renderer's framebuffer, and a real window on this machine cannot reach 3840×2160 (see [../captures/desktop/README.md](../captures/desktop/README.md)). Stepping tick by tick also guarantees there are no dropped or doubled frames on a heavily loaded machine.
- **Crop:** see [Framing](#framing). The HUD (top bar, event list, right-hand sidebar) and the "Paused" label, which the game prints while a match is held between ticks, are outside every crop. There are two exceptions on purpose: the build palette in the sidebar during placement segment 2a, and the Hive card inset in the desktop co-play beat. Nothing was re-filmed for the fix round; every change is a re-cut of the same raw frames.
- **Camera:** each shot is centred with `game_view` at a seam-free zoom (100 %, 125 %, 150 %, 200 %). Three shots drift sideways by 1.5 native pixels a frame (45 px a second) with the game's own middle-button map drag.
- **Clean state:** the seat erases the colony's forbidden, clearing and guard areas in and around the view (Flags and areas tool, an ordinary player action) before and during each take, so zone outlines do not clutter the picture; the AI repaints them within seconds. Health and food bars are off. The event list and the free-worker count are outside every crop.

## Footage label (AI versus AI)

Every colony on screen is played by the game's built-in AIs, in matches with no human player. The trailer is therefore **AI-versus-AI footage, a spectator view** in the sense of the footage rule, filmed from a player seat that shares one colony with its AI. The seat's own inputs are all listed per shot in the manifest (`shots[].seat_inputs`):

- the zone erase described above;
- in the placement shot, arming the Inn in the build palette, gliding the pointer, one left click to place the site and one right click to leave build mode;
- in the desktop co-play shot, one Hive standing order installed over MCP by the AI agent that edited this trailer.

Nothing here is human-versus-human multiplayer.

## Text, wordmark and music

- **Text:** the only on-screen text is `trailer_line_1`..`4` (and `trailer_line_ai_coplay` in the desktop variant), read from `translations/<locale>.md`. [tools/render_cards.py](tools/render_cards.py) lays each line out in headless Chromium (HarfBuzz shaping, ICU bidi, CJK line breaking) with [tools/cards.html](tools/cards.html), at every output size (3840×2160, 1920×1080, 1080×1920), so no card is scaled. The style is brand cream `#f9e8bb` text with a gold `#e3c077` rule, in a heavy weight: Nunito 900 from the design system for Latin, and the caption tool's Noto fonts for other scripts. Lines are 8.2 % of the frame height (9.2 % of the width in portrait), over a soft dark scrim. Landscape lines are centred at 80 % of the height, except the co-play line, which sits at 15 % with its scrim hanging from the top. Portrait lines are centred at 60 %. No ffmpeg drawtext is used.
- **Line breaks:** a line that needs two lines and holds two sentences breaks between them ("No ads. / No in-app purchases.", "広告なし。/ アプリ内課金なし。"). Otherwise the two lines are balanced, and never break inside a hyphenated word. `render_cards.py` reports any two-sentence card that splits inside a sentence. All 45 locales were rendered at 1080×1920 for this check on 2026-11-24, and none split.
- **Wordmark:** the game's own `content/data/gfx/menu-wordmark.png`, keyed into two masks and coloured cream and gold, over a full-frame dim of the live footage for the last 3 s (2.5 s in the 15 s cut).
- **Music:** the game's **original soundtrack by Jacques-Paul Grivaz**, licensed **GPL-3.0-or-later** like the rest of the game (`content/data/zik/original/`; credited in `docs/assets/source-attribution.md` and the in-game credits `content/data/authors.txt`). The edit uses the building (`a2.opus`) and combat (`a3.opus`) moods of the same piece. They share one timeline, and the edit crossfades between them at the same playback position, as the game's own sound mixer does: combat under the fights, building under the colony. It then fades the tail over 2.5 s (2 s in the 15 s cut). In the game's files the combat mood is mixed quieter, so the edit lifts it by 4 dB, and the fights no longer drop to a lull. A limiter at 4× oversampling then keeps the true peak at or below −1 dBTP. Measured (ebur128) in every file: true peak −2.0 dBTP (WebM −1.7). Integrated loudness is −14.6 LUFS for the 30 s cuts, −14.3 for the desktop cut and −14.0 for the 15 s cut. The trailer carries its story in pictures and text, so it works muted.

## Review

Checked by eye and by tool on 2026-11-24, after the fix round:

- **Contact sheets** (one frame every 0.5 s): [master](contact-sheet-master-30s.jpg), [text-free master](contact-sheet-master-30s-textless.jpg), [desktop](contact-sheet-desktop-34s.jpg), [15 s](contact-sheet-15s.jpg), [vertical](contact-sheet-vertical-30s.jpg). Every half second shows colonies or a fight; no empty terrain, no early game, no menu.
- **Changed shots by eye:** each changed shot was looked at as a full 1920×1080 or 1080×1920 frame and as a 360 px feed thumbnail (200 px for portrait). That covers the fight punch-in, the palette, the cut-in and completion, the co-play beat, the whole 15 s cut, vertical shots 5 and 7, the portrait text, the poster, and the Japanese and Arabic lines.
  - In the feed thumbnails, the red and lime warriors of the opening fight read as two armies.
  - The palette's highlighted Inn, the build-mode footprints and the placed site are visible.
  - Each co-play site appears as a red footprint where the previous frame had grass.
- **Frame timing** (`review.py --timing`, every file): constant 30 fps (each MP4 frame step 33.333 ms). No frame repeats the one before, so there is no stutter and no dropped or doubled frame. The cuts fall exactly where the edit puts them: master 2.5, 3.633, 8.5, 12.0, 15.0, 18.5, 21.5 and 26.0 s; desktop adds 30.5 s; 15 s cut 1.5, 2.367, 4.8, 5.8, 9.0 and 12.3 s. At the source, every frame of every shot is exactly one simulation tick after the one before (`frame_ticks` in each shot sidecar). The one exception is the declared cut inside the placement take.
- **Fog-black:** near-black pixels are at most 0.5 % of any frame. The exception is placement segment 2a, where the navy build-palette sidebar is 11.8 % of the frame; that is interface, not fog. Fog of war dims, but does not blacken, the far edge of the wheat fields in shot 4 and the forest at the top right of shot 7 (top of the vertical shot 7); that is the colony's real view.
- **HUD** (`check_hud.py`, every one of the 1,935 frame and crop pairs the cuts use, 135 of them with the card inset): no event-list text inside any crop, no Hive-card button along any crop's bottom edge, and every crop below the top bar and above the "Paused" label. The co-play inset contains no "Reports / details" or "Stop commander" button.
- **Clean state:** no health or food bars (switched off in game), no forbidden, clearing or guard area outlines (erased by the seat), no negative worker count or event list (outside every crop), clouds off.
- **Text:** every line sits over the picture it describes (see the shot list). In the 15 s cut every line is on screen for at least 2.8 s, with at least 0.6 s of clean picture between lines.
  - Japanese and Arabic, checked by eye: kana and kanji in Noto Sans JP; Arabic joined, right to left, with the full stop on the left, in Noto Sans Arabic.
  - Vertical: "You decide. / They build.", "Fight rivals / for the land." and "No ads. / No in-app purchases."; "Keep the colony fed." fits on one line.
- **Sound:** AAC stereo, 48 kHz (Opus in the WebM). The fights now sit at about −16 to −17 dB RMS per 3 s, against −15 to −18 dB for the building passages; before the fix round they were −18.6 to −19.7 dB against −13.8 to −16.7 dB.

Known compromises:

- Shots 1 and 6 come from one camera on the same fight (0–74 and 75–179 of one take). Shot 1 is now punched in and shot 6 is not, so the two read as close and wide views of one exchange. A second honeycomb take from the other colony's seat found no fight in view and was discarded, as were City-states, Oasis and Crater-lakes scouts (fights mostly under fog of war).
- The fights are skirmishes of a few dozen warriors, the largest the build's AIs produced in the scanned matches (see the desktop capture README).
- The 2160p files upscale the punch-ins (see [Framing](#framing)): 8.5 s of the master and 13 s of the desktop variant. They are softer than the native shots at 100 % view; at any store or feed size they are indistinguishable. A sharper 2160p would mean re-filming those takes at a higher zoom.
- Shot 9 (under the wordmark) is from tick 48,400 of the same match as shots 2–4 and 8 (about 60,300–60,750), so it is 6.5 game minutes earlier; the edit is not chronological.

## Follow-ups not done in the fix round

These are left as the review listed them, or found during the fix round:

- **S1, pacing of the last 8.5 s:** shots 8 and 9 still give 8.5 s of the red colony core from similar overhead views.
- **S2, more fight locations:** shot 7 is still the third view of the one oasis fight.
- **S3:** shot 5 is still 3 s in the landscape cut.
- **S7:** the desktop co-play beat is still at 26.0 s, after Steam's ten-second window. Moving it to follow shot 3 (about 8.5 s) is a structural change to the edit.
- **S8:** the Arabic line 4 wording ("مشتريات داخلية") is for the Arabic translation reviewer.
- **M7 option:** 1.5 s of the agent's real MCP client issuing `hive_program install`, captured on screen, was not added.
- **Thai, found in the portrait check:** `trailer_line_ai_coplay` wraps inside the word "เอเจนต์" at 1080×1920. That line is not used in any portrait cut today; fix the Thai line breaking before a Thai desktop vertical is made.

## What changed in the fix round

| Review item | Change | Where |
| --- | --- | --- |
| M1 | The build is recorded as "0.11.7.0 + 15 commits, revision 5bf966285aa8; not the public release binary; maps, AI roster and simulation identical to the tag"; `build.public_release` is false | This README, `manifest.json` `build` |
| M2 | The placement beat first shows the real build palette with the Inn armed, then cuts in to 2× on the placement inside the same take; shot 3 keeps the 2× window | Master, text-free, ja, ar and desktop 2.5–8.5 s; 15 s cut 1.5–4.8 s |
| M3 | 1.5× punch-in on the opening clash; 1080p is a downscale, 2160p a 1.5× upscale | Master, text-free, ja, ar and desktop 0.0–2.5 s; 15 s cut 0.0–1.5 s |
| M4 | Vertical shot 7 is reframed onto the clash (x 1960, native 1080×1920) | Vertical 18.5–21.5 s |
| M5 | Vertical shot 5 is reframed onto the lime colony's west building cluster (x 560) | Vertical 12.0–15.0 s |
| M6 | Two-sentence lines break between the sentences: "No ads. / No in-app purchases."; all 45 locales were checked at 1080×1920 | Vertical 22.0–25.0 s |
| M7 | The co-play beat is re-cut at 1.8× on the four sites, 4.5 s, with the game's Hive card inset bottom left (cropped below the "Stop commander" button) and the line at the top; the desktop cut is now 34.5 s | Desktop 26.0–30.5 s |
| M8 | The 15 s cut drops "Keep the colony fed."; the three remaining lines run 3.0, 2.8 and 2.8 s with gaps of 1.2 and 0.6 s | 15 s cut |
| S4 | The combat mood is lifted 4 dB; every file's true peak is ≤ −1 dBTP (measured −2.0, WebM −1.7) | All cuts |
| S5 | The poster is the opening fight at its 1.5× punch-in (frame 30 of the take) | `poster-*.png` |
| S6 | Portrait text is centred at 60 % of the height | Vertical |
| S9 | Microsoft points to the 1080p file; the vertical line-break claim is corrected | This README |
| — | New files: the VP9 WebM for AppStream, and a 720p preview (16 MB) | `glob2-trailer-30s-1080p.webm`, `-preview-720p.mp4` |

## Reproduce

Paths: `T` is a scratch working directory. `MATCHES` holds the headless match checkpoints (`<match>/checkpoint-<tick>.game.gz`, made with [../captures/desktop/tools/run-match.sh](../captures/desktop/tools/run-match.sh) as listed in its `matches.json`).

```sh
cd assets/storefront-v2/trailer
export GLOB2_CAPTURE_TOOLS=$PWD/../captures/desktop/tools   # mcp.py, session.py, join-seat.py
export GLOB2_MCP_TOKEN_FILE=$T/profile/mcp-token

# 1. The off-screen game (4256x2800, HD art, clouds off, MCP on port 47814)
tools/launch-record-game.sh $T/profile 4256x2800 2 47814 > $T/game.log 2>&1 &

# 2. Film the shots (one PNG per tick plus shot.json per shot; about 4 s a frame on a loaded machine)
uv run --with pillow --with numpy python tools/capture_shot.py tools/shots.json $T/raw \
  --matches $MATCHES --profile $T/profile
pkill -f "mcp-port 47814"

# 3. Text cards at every output size (Chromium via Playwright: `uv run --with playwright==1.63.0 playwright install chromium` once;
#    fonts from ../tools/fetch_fonts.py)
uv run tools/render_cards.py --locale en,ja,ar --out $T/cards --size 3840x2160,1920x1080,1080x1920

# 4. Cut, encode, music, poster (GLOB2_GAME points at the game checkout for the soundtrack)
export GLOB2_GAME=/path/to/glob2
B="uv run --with pillow --with numpy python tools/build_trailer.py"
$B master,desktop,cut15,vertical --raw $T/raw --work $T/work --out . --cards $T/cards
$B master --only text --locale ja,ar --raw $T/raw --work $T/work --out . --cards $T/cards
$B master --only poster --raw $T/raw --work $T/work --out .

# 5. Review and manifest
uv run tools/review.py glob2-trailer-30s-1080p.mp4 --sheet contact-sheet-master-30s.jpg --every 0.5
for f in *.mp4; do uv run tools/review.py $f --timing > $T/timing/timing-${f%.mp4}.json; done
uv run tools/review.py glob2-trailer-30s-1080p.webm --timing > $T/timing/timing-glob2-trailer-30s-1080p-webm.json
uv run --with pillow --with numpy python tools/check_hud.py $T/raw --step 1 > $T/check_hud.json
uv run --with pillow --with numpy python tools/finalize_trailer.py . --raw $T/raw --cards $T/cards \
  --extra tools/manifest-extra.json --timing $T/timing --hud-check $T/check_hud.json --work $T/work
```

Another language is `render_cards.py --locale xx --size 1920x1080` and then `build_trailer.py master --only text --locale xx` (1080p). `--locale all` renders every locale in `translations/platforms.json`.

Steps 4 and 5 write and read the MP4s in this folder, as they did when the trailer was made. The finished MP4s were then moved to `../storefront-v2-renders/trailer/` (see [Where the files live](#where-the-files-live)); to re-run step 5 on them, put them (or symbolic links to them) back here first, and move the new ones out again afterwards.

The raw footage (21 GB of native PNG frames with their `shot.json` sidecars) and the joined saves stay in the session scratch directory: `/private/tmp/claude-501/-Users-bradley-glob2/4d02c18b-dc3e-4981-ab5e-77b65e7adafe/scratchpad/trailer/raw2/`. The fix round's lossless timelines, cards and inset frames are in `.../scratchpad/trailer-fix/`.

## Tools

| File | Purpose |
| --- | --- |
| [tools/launch-record-game.sh](tools/launch-record-game.sh) | Start the build off-screen with the capture settings |
| [tools/capture_shot.py](tools/capture_shot.py), [tools/shots.json](tools/shots.json) | Film shots tick by tick through the MCP UI server; the shot definitions used |
| [tools/coplay_order.js](tools/coplay_order.js) | The Hive standing order of the co-play beat |
| [tools/render_cards.py](tools/render_cards.py), [tools/cards.html](tools/cards.html) | Text cards and wordmark, rendered by Chromium; sentence-aware line breaks |
| [tools/build_trailer.py](tools/build_trailer.py), [tools/trailer.json](tools/trailer.json) | Cuts, per-segment framing and insets, text cues, music plan, encodes, poster |
| [tools/review.py](tools/review.py) | Contact sheets and frame-timing report |
| [tools/check_hud.py](tools/check_hud.py) | Checks that no unwanted HUD reaches into any crop, and that the co-play inset leaves out the buttons above the Hive card |
| [tools/finalize_trailer.py](tools/finalize_trailer.py), [tools/manifest-extra.json](tools/manifest-extra.json) | Manifest with hashes, ffprobe facts, loudness and true peak, shot sidecars, MCP transcript and review reports |

Scripts are `GPL-3.0-or-later`, like the game.
