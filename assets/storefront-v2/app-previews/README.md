# Storefront-v2 App Store app previews

[Manifest](manifest.json) · [Edit data](tools/previews.json) · [Takes](tools/takes.json) · [Trailer](../trailer/README.md) · [Mobile captures](../captures/mobile/README.md) · [Footage rule](../../../planning/gameplay-video.md)

Two App Store app previews, **version 2**, made **2026-11-25** from the iOS app of Globulation 2 **0.11.8.0** (release commit `5e96273ff62f` plus the capture-only patches described below), filmed in the iOS Simulator **frame by frame: one game tick per frame, played back at 30 fps**, which is the game's normal speed of 30 ticks a second. Every frame is a `simctl io screenshot` of the running app at the device's native pixels. Nothing is AI-generated, stock, interpolated, blended, sped up or slowed down, and no desktop footage is used. They are for the **next editable iOS version** in App Store Connect. On 2026-11-25 they replaced version 1 in the English (U.S.) iPhone 6.9-inch and iPad 13-inch preview sets of the iOS draft 0.11.802, with the poster frames below (saved and verified by a fresh reload; not submitted; see the [rollout ledger](../../../planning/storefront-v2-rollout.md#log)).

| File | Device slot | Pixels | Length |
| --- | --- | --- | --- |
| `glob2-app-preview-iphone-6.9-886x1920.mp4` | iPhone 6.9-inch display, portrait | 886×1920 | 25.0 s |
| `glob2-app-preview-ipad-13-1200x1600.mp4` | iPad 13-inch display, portrait | 1200×1600 | 25.0 s |

## Why version 2

The owner watched version 1 and found "glitches", "hiccups in the underlying recording", and asked for a retake. Version 1 was a real-time `simctl io recordVideo` capture of the app made while the Mac was heavily loaded (an Android NDK build pushed the load average to about 37). That produced uneven motion, held frames and, on iPad, a 2 s app hitch that the edit had to cut around.

Version 2 keeps the approved structure, text, music and length, and changes how the pictures were made: the match is held between ticks and stepped one tick per frame, and each frame is a screenshot of the held app (see [How it was filmed](#how-it-was-filmed)). How long a screenshot takes no longer matters, so machine load cannot cause a stutter. Measured on the finished files ([Review](#review)):

| | Version 1 iPhone | Version 2 iPhone | Version 1 iPad | Version 2 iPad |
| --- | --- | --- | --- | --- |
| Held frames (gameplay area unchanged from the frame before) | 10, in 6 runs (1.7 s, 5.0–5.5 s) | **0** | 20, in 17 runs | **0** |
| Frames that jump more than 3× their neighbours' motion | 1 | 1 (the Inn armed: build outlines appear) | 11 (largest 39.6×) | 1 (the wordmark fading in) |
| Game ticks between consecutive frames | 29–30 ticks a second on average, uneven per frame | exactly 1, except the one declared cut | uneven | exactly 1, except the one declared cut |

The hiccups are gone: no frame of either preview repeats the one before, and every frame inside a shot is exactly one tick after the previous one. The remaining large frame-to-frame changes are interface events (the build palette opening, the Inn being armed, the wordmark fading in), not motion stalls.

Version 1 is not deleted: its two MP4s are in `../storefront-v2-renders/app-previews/superseded/` (sizes and SHA-256 in the manifest under `superseded`), and its README, tools and takes are in this folder's Git history (commit `2052b8d`).

Also fixed while retaking:

- **The iPad build beat now ends with the Inn finished**, as on iPhone. Version 1's iPad take ended with the site at 135 of 200 hit points.
- **No 2 s cut around an app hitch** on iPad: the placement plays continuously, tap by tap.
- **Event-list rows:** the colony shots show zero to two rows. The fights still show three to six rows (see [Known compromises](#known-compromises)).
- **Fog in the fights:** somewhat less of the fight frames is fog-dimmed than in version 1 (iPhone 27 % and 36 % against 41 % and 42 %; iPad 40 % and 50 % against 47 % and 56 %), but the iPad fights in particular are still partly dimmed (see [Known compromises](#known-compromises)).

## Where the files live

The repository keeps this README, [manifest.json](manifest.json), [tools/](tools/), the poster frames and the contact sheets. The two MP4s are **not committed**: they are in `../storefront-v2-renders/app-previews/` relative to the repository root (`/Users/bradley/glob2/storefront-v2-renders/app-previews/` on the machine that made them), beside the trailer renders, and [.gitignore](.gitignore) here ignores `*.mp4` and `*.mov`. Their bytes and SHA-256 are in the manifest (`deliverables[].sha256`). Both are reproducible from the raw frames with `tools/` (see [Reproduce](#reproduce)).

## Apple's specification and how each file meets it

Read on 2026-11-25 from App Store Connect Help, [App preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-preview-specifications), and [App previews](https://developer.apple.com/app-store/app-previews/).

| Apple requirement | iPhone 6.9-inch file | iPad 13-inch file |
| --- | --- | --- |
| Accepted resolution (iPhone 6.9/6.5/6.3-inch class: 886×1920 portrait; iPad 13-inch: 1200×1600 portrait) | 886×1920 | 1200×1600 |
| 15–30 seconds | 25.000 s | 25.000 s |
| At most 30 fps | constant 30 fps, 750 frames, every frame step 33.333 ms | same |
| H.264, up to High profile level 4.0, progressive | H.264 High, level 4.0, progressive, yuv420p | same |
| `.mov`, `.m4v` or `.mp4` | `.mp4` (faststart) | same |
| Target 10–12 Mbps | 11.04 Mbps | 11.04 Mbps |
| At most 500 MB | 35.3 MB | 35.3 MB |
| Stereo audio, AAC 256 kbps, 44.1 or 48 kHz, all tracks enabled | one stereo AAC-LC track, 256 kbps, 48 kHz, default (enabled) | same |

All of this was measured on the finished files with ffprobe by [tools/check_previews.py](tools/check_previews.py); the full report per file is in the manifest under `deliverables[].spec_check`. Loudness: -14.2 LUFS integrated, true peak -1.9 dBTP (iPhone); -14.2 LUFS, -1.9 dBTP (iPad). Colour is tagged BT.709; the screenshots are sRGB.

Content rules from the same pages, and how the previews follow them:

- **Only content captured from the app.** Every picture is a screenshot of the iOS app. The only additions are the text cards and the closing wordmark (below), which Apple allows as overlays. No pixel of the app's picture is edited.
- **No device frames, no hands, no people**: none.
- **No prices, no calls to action, no other platforms, no dates**: none. The iPad status bar shows a date next to the time; it is pinned to the simulator override `9:41 AM Tue Jan 9` (Apple's own marketing time) so it shows no real or current date. The iPhone status bar shows only `9:41`.
- **Text legible and on screen long enough**: each line stays 2.8–4.1 s, in the trailer's heavy cream type with a soft scrim.
- **Music**: one score, the game's own soundtrack, licensed with the game (below).
- **Violence**: Apple asks previews to avoid objectionable violence. The fights are the game's cartoon combat of round "globs" (no blood or gore), within the app's own App Store age rating, which already lists cartoon or fantasy violence ([claims](../../../facts/storefront-v2-claims.md)); the same imagery is in the screenshots and the trailer. Flagged here for whoever uploads.
- **Poster frame**: Apple uses the frame at 5 s unless another is chosen. See [Poster frame](#poster-frame).

## Shot lists

Both previews have the same structure, the approved one of version 1: open inside a fight with no text, then the player building an Inn by touch and the workers finishing it, the colony fed, a second look at the fight, and the colony at work under the fair-deal line, with the wordmark over the last 2.2 s. Lines are `trailer_line_1`..`4` from `translations/en.md`. In points (`in`) are frame numbers of the take; 30 frames are one second of the match.

### iPhone 6.9-inch (886×1920)

| # | Time (s) | Take, frames | Save, ticks | Camera (centre tile, tile size) | What it shows | Event rows | Text |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0–3.0 | `fight-a-r1` 110–199 | `bigpond-n-t27015`, 27721–27810 | (40, 58), 30 pt | opens inside the fight: the red army meets the blue line at the front | 3–5 | — |
| 2 | 3.0–9.6 | `build-r2` 39–236 | `bigpond-n-t45017`, 47964–48161 | (44, 32), 30 pt | Build palette opens (3.2 s), the Inn is armed (4.7 s), the map is tapped and the ghost shows (6.3 s), Ok (7.9 s): the site appears and workers head for it | 0–2 | `trailer_line_1` from 7.9 |
| 3 | 9.6–12.2 | `build-r2` 318–395 | `bigpond-n-t45017`, 48411–48488 | (44, 32), 30 pt | same take after a declared cut of 250 ticks (8.3 s): workers bring the last wood and the Inn is finished at about 11.0 s ("The Inn is finished.") | 0–1 | `trailer_line_1` |
| 4 | 12.2–15.4 | `fed-r1` 54–149 | `bigpond-n-t45017`, 49128–49223 | (40, 18), 26 pt | wheat fields above the lake shore, inns below, workers carrying | 0–1 | `trailer_line_2` |
| 5 | 15.4–19.4 | `fight-b-r1` 100–219 | `bigpond-n-t27015` (second load), 27824–27943 | (39, 60), 24 pt | the front, wider: the red and blue lines clash | 5–6 | `trailer_line_3` |
| 6 | 19.4–25.0 | `hero-r1` 30–197 | `bigpond-n-t45017`, 49404–49571 | (56, 29), 20 pt | the colony core: pools, racetrack, barracks, inns and hundreds of globs | 0–1 | `trailer_line_4`, wordmark from 22.8 |

### iPad 13-inch (1200×1600)

| # | Time (s) | Take, frames | Save, ticks | Camera (centre tile, tile size) | What it shows | Event rows | Text |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0–3.0 | `fight-a-r2` 110–199 | `bigpond-n-t27015`, 27725–27814 | (39, 58), 52 pt | opens inside the fight: the red army meets the blue line at the front | 3–5 | — |
| 2 | 3.0–9.6 | `build-r3` 39–236 | `bigpond-n-t45017`, 47980–48177 | (44, 32), 40 pt | Build palette opens with named buttons (3.2 s), the Inn is armed (4.7 s), the map is tapped and the ghost shows (6.2 s), Ok (7.5 s): the site appears; tablets keep the Inn armed until the palette is closed (9.2 s) | 0–1 | `trailer_line_1` from 7.9 |
| 3 | 9.6–12.2 | `build-r3` 440–517 | `bigpond-n-t45017`, 48459–48536 | (44, 32), 40 pt | same take after a declared cut of 282 ticks (9.4 s): workers bring the last wood and the Inn is finished at about 11.0 s | 0–1 | `trailer_line_1` |
| 4 | 12.2–15.4 | `fed-r2` 50–145 | `bigpond-n-t45017`, 48707–48802 | (40, 19), 34 pt | wheat fields above the lake shore, inns below, workers carrying | 0–1 | `trailer_line_2` |
| 5 | 15.4–19.4 | `fight-b-r2` 0–119 | `bigpond-n-t27015` (second load), 27750–27869 | (38, 59), 44 pt | the front from a second load of the save: the red and blue lines clash | 3–5 | `trailer_line_3` |
| 6 | 19.4–25.0 | `hero-r2` 30–197 | `bigpond-n-t45017`, 48987–49154 | (52, 30), 28 pt | the colony core: pools, racetracks, barracks, inns and hundreds of globs | 0 | `trailer_line_4`, wordmark from 22.8 |

The iPhone and iPad timelines are now identical in timing (version 1's iPad cut was shorter on the build and longer on the fights to avoid the app hitch).

Text cues (both previews): `trailer_line_1` 7.9–12.0 s, `trailer_line_2` 12.5–15.3 s, `trailer_line_3` 15.7–19.2 s, `trailer_line_4` 19.8–22.6 s; wordmark 22.8–25.0 s. Music: combat mood under the fights (0–3.0 s, 15.4–19.4 s), building mood elsewhere.

Shots 2 and 3 of each preview are one take with one declared cut: the Inn is placed by touch, the take skips a few seconds of game time (the ticks run, unfilmed), and resumes while workers bring the last material, so the Inn is seen finishing. Each take's tick range, camera, event-list rows and player inputs are in the manifest under `takes`.

## How it was filmed

- **App and device.** The iOS app built from the release commit with `platforms/mobile/ios.py` in the capture worktree `/Users/bradley/glob2/glob2-wt-mobile-capture`, with two capture-only patches that never ship:
  - [capture-build.patch](../captures/mobile/tools/capture-build.patch) (from the mobile captures): compiles the desktop MCP automation listener into the simulator build so scripts can tap the real touch controls.
  - [tools/capture-frame-clock.patch](tools/capture-frame-clock.patch) (new for version 2): the **capture clock**, switched on and off over MCP (`game_time capture_clock`). While it runs, the match view draws exactly two frames for every tick that runs (a 60 Hz display at the normal 30 ticks a second) and nothing in between. The presentation clocks read a frame clock that advances exactly 1/60 s per drawn frame: water, shore and cloud animation, the event list's lifetimes and fades, the tick-rate readout, unit-motion and fog-fade fractions. While the match is held between ticks, the game would normally show a "Paused" label and darken the map; the capture clock leaves both out, because a device playing normally shows neither. With the clock off (always, outside a take), the app behaves exactly as the release. Neither patch changes the simulation.

  The simulators are the isolated set in that worktree (`build/mobile-tools/ios-simulators`): *Glob2-Capture-iPhone-6.9* (iPhone 17 Pro Max, iOS 26.5) and *Glob2-Capture-iPad-13* (iPad Pro 13-inch M5, iOS 26.5), plus a second identical iPad device, *Glob2-Capture-iPad-13-b*, used for the iPad build take so it could run beside the other iPad takes. HD artwork is forced on. The simulator package draws with the portable SDL renderer (the Metal renderer devices use is not available in the Simulator).
- **Saves.** The mature saves of the mobile captures ([../captures/mobile/saves/](../captures/mobile/saves/)): `bigpond-n-t27015` (A big pond, tick 27,015: the red army attacks the blue colony; the fights are in the first 1,000 ticks after loading) and `bigpond-n-t45017` (the same match at tick 45,017: about 340 workers, 240 warriors and 70 buildings; the match is won a minute after loading and the player presses *Continue playing*). Each fight take loads its save afresh, so the two fight shots are two different continuations of the same battle.
- **Player view, not spectator view.** Colony 1 (red) is **You + AI**: the Nicowar AI grew and still co-plays the colony; the HUD is the local player's. The opponents are AI colonies. The scripted inputs per take are listed in the manifest (`takes[].player_actions`): the *Health and food bars* lens switched off; *Continue playing* on the "You have won" dialog (colony saves); the zone tool erasing the co-controlling AI's forbidden, guard and clearing zones before and during each take (the clean-state protocol of the mobile captures; the AI repaints them); and in the build take, Build → Inn → tap → Ok → close.
- **Frames.** [tools/capture_frames.py](tools/capture_frames.py) loads the save through the game's Load game screen, points the camera with `game_view`, holds the match (`game_time pause`), starts the capture clock and runs a 150-tick lead-in so the tick-rate readout's 3 s window holds only frame-clock time (it then reads `30`, as on a device). Then, for every frame: perform that frame's scripted player inputs, step exactly one tick (`game_time step ticks=1`), wait until the app reports both frames of that tick drawn, and save the screen with `xcrun simctl io screenshot` at native pixels (1320×2868, 2064×2752). Each take's sidecar records the tick and drawn-frame count of every frame; in every take used, consecutive frames are exactly one tick and two drawn frames apart (the manifest's `frame_ticks` and `drawn_frames_per_filmed_frame`).
- **Checks while filming.** Every 50th frame, a second screenshot 0.4 s later had to be pixel-identical to the first, which shows the frame is really held while it is saved (all passed). The simulator now and then paints its Dynamic Island cut-out into the framebuffer, which a device screenshot never contains; such a screenshot was retaken (the frame is held, so the retake is the same frame) until it showed the plain status bar. The island is therefore in no frame, and no pixel was filled or edited.
- **The Inn placement.** The building is placed **by touch**, frame by frame: Build opens the palette, the Inn is armed, the map is tapped (the ghost shows), Ok confirms, the palette closes. To find clear ground, before filming and with the match held, the script armed the Inn, tapped candidate tiles until the placement's Ok was enabled (the game's own check), and cancelled; nothing was placed or destroyed. Both devices found tile (43, 31) free. At frame 240 the script checked that the Inn site stands there (`game_world`). Then the take skipped unfilmed ticks until the site lacked one unit of material, and filmed on; a site finishes the moment its last material arrives. On iPad that took longer, so the iPad take filmed on until the game reported the Inn finished and kept only the last 150 frames before that check plus 120 after (frames 336–605; the single frame filmed right after the skip, 270, also remains; the 65 discarded frames 271–335 were deleted, never edited in). The iPhone take used a fixed 240 frames after the cut, recorded before that rolling option existed.

### Picture path

[tools/build_previews.py](tools/build_previews.py), all edit data in [tools/previews.json](tools/previews.json):

1. Each segment takes its frames from the take's PNG sequence, one output frame per take frame, at 30 fps. Nothing is dropped, repeated, interpolated or blended.
2. One Lanczos downscale to Apple's size: iPhone 1320×2868 → 886×1925, then the bottom 5 rows (the empty home-indicator band) are cropped to 886×1920; iPad 2064×2752 → 1200×1600 exactly (same 3:4 shape). Nothing is cropped from the game picture or the HUD, and nothing is upscaled.
3. Text cards, wordmark, music, encode (two-pass x264 at about 11 Mbps, AAC 256 kbps). The PNGs are sRGB and are converted to BT.709 video once, at the encode.

## Text and localisation

The cards are rendered by [tools/render_preview_cards.py](tools/render_preview_cards.py), which runs the trailer's [render_cards.py](../trailer/tools/render_cards.py) once per preview size with the style in [tools/previews.json](tools/previews.json): the same fields, fonts (Nunito 900 for Latin, Noto for other scripts), cream `#f9e8bb` and gold rule `#e3c077` as the trailer, laid out by headless Chromium at each preview size so no card is scaled. On iPhone, lines are 8.8 % of the width, centred at 74 % of the height (in the lower map area, above the bottom navigation bar, below the event list and clear of the action in the centre); on iPad, which has no bottom bar, 8.4 % of the width at 83 % of the height (`text_layout_by_size`). Each sits over a soft scrim. Two-sentence lines break between the sentences ("No ads. / No in-app purchases."). The text cues (field, start, end) are data in `previews.json`. The English cards are byte-identical to version 1's.

Only English is rendered now. A localized preview is two commands, once its `trailer_line_*` fields are in `translations/<locale>.md`:

```sh
uv run tools/render_preview_cards.py --locale ja --out $CARDS
uv run --with pillow --with numpy python tools/build_previews.py --raw $RAW --cards $CARDS --out $OUT --locale ja
```

The text is true of the footage: "You decide. They build." runs over the player's Inn going up and being finished; "Keep the colony fed." over wheat fields and inns with workers carrying; "Fight rivals for the land." over the red and blue armies fighting; "No ads. No in-app purchases." over the colony at work (the app has neither; see [storefront v2 claims](../../../facts/storefront-v2-claims.md)). There is no price, no "free", no call to action, no store badge and no URL. The wordmark is the game's own menu wordmark, as in the trailer.

## Music

The game's **original soundtrack by Jacques-Paul Grivaz**, licensed **GPL-3.0-or-later** like the rest of the game (`content/data/zik/original/`; credited in `docs/assets/source-attribution.md` and the in-game credits), exactly as the [trailer](../trailer/README.md#text-wordmark-and-music): the building mood (`a2.opus`) under the colony and the combat mood (`a3.opus`, lifted 4 dB) under the fights, cross-faded at the same playback position as the game's mixer does, a 2 s tail fade, and a limiter that keeps the true peak under −1 dBTP. The previews work muted, as Apple plays them by default.

## Poster frame

Apple shows the poster frame when autoplay is off, and uses the frame at 5 s unless another is set in App Store Connect. **Choose these instead** when uploading:

| Preview | Poster time | Frame | File | Why |
| --- | --- | --- | --- | --- |
| iPhone | 00:16.50 | 495 | [poster-iphone-6.9-886x1920.png](poster-iphone-6.9-886x1920.png) | The blue line and the red line locked together in the middle of the screen, "Fight rivals for the land." below: the most exciting frame that still reads at thumbnail size |
| iPad | 00:16.60 | 498 | [poster-ipad-13-1200x1600.png](poster-ipad-13-1200x1600.png) | The same beat in the iPad preview: the red army pressing the blue line, the line below |

The 5 s default would show the build palette with the Inn being armed, which says less at a glance.

The PNGs are the exact frames from the finished files, for checking what App Store Connect shows after the time is set.

## Review

Every second of both files was reviewed on 2026-11-25 by contact sheet at four frames a second (one row per 5 s, 160 px wide), and at one frame per second at full size and at 240 px wide (about the width a preview plays at in App Store search results on a phone):

| Preview | 4 frames a second | Full size, 1 a second | Thumbnail, 1 a second |
| --- | --- | --- | --- |
| iPhone | [4 fps](contact-glob2-app-preview-iphone-6.9-886x1920-4fps.jpg) | [full](contact-glob2-app-preview-iphone-6.9-886x1920-full.jpg) | [thumbnail](contact-glob2-app-preview-iphone-6.9-886x1920-thumb.jpg) |
| iPad | [4 fps](contact-glob2-app-preview-ipad-13-1200x1600-4fps.jpg) | [full](contact-glob2-app-preview-ipad-13-1200x1600-full.jpg) | [thumbnail](contact-glob2-app-preview-ipad-13-1200x1600-thumb.jpg) |

- Every quarter second shows colonies or a fight. No empty terrain, no early game, no menu, no black frame.
- The opening fight reads as two armies (red and blue) at thumbnail size; the build palette, the armed Inn, the ghost, the Ok button, the new site and the finished Inn are visible at full size.
- Text is legible at thumbnail size; no line covers the action it describes.
- No "Paused" label, darkening or Dynamic Island in any frame. The tick-rate readout reads `30`, except in the first second of the iPad's second fight, where it shows `31` and `29` (its 3 s window still covers part of the lead-in, which was stepped three ticks at a time); a device at normal speed also wobbles between those values.

**Frame cadence** ([tools/check_cadence.py](tools/check_cadence.py), on the finished files; per file in the manifest under `deliverables[].cadence_check`). For every pair of consecutive frames it measures how much the gameplay area changed. A held frame (no change) is what a hitch looks like in a recording; a change far above its neighbours is the jump that follows a hitch. Results:

| File | Frames | Held frames | Frame-to-frame change (median, smallest) | Changes above 3× their neighbours | What those are |
| --- | --- | --- | --- | --- | --- |
| iPhone | 750 | **0** | 2.628, 1.037 | 1 | 4.7 s: the Inn is armed and every building's footprint outline appears |
| iPad | 750 | **0** | 3.188, 0.914 | 1 | 23.07 s: the wordmark fading in over the dimmed picture |

The cuts between shots (3.0, 9.6, 12.2, 15.4 and 19.4 s) are excluded from the jump count. Changes between 2× and 3× (8 on iPhone, 9 on iPad) are the build palette opening and the wordmark's fade; none follows a held frame. The smallest change between any two frames (0.914 levels) is still far above an unchanged frame (below 0.05).

Version 1 measured with the same tool for comparison: iPhone 10 held frames in 6 runs (at 1.7 s and 5.0–5.5 s, the hitch while the palette armed the Inn), largest jump 3.5×; iPad 20 held frames in 17 runs (most in the opening fight, 0.0–0.9 s) and 11 jumps above 3× (largest 39.6×, around the cut past the app's 2 s hitch). Motion in version 2 is even from frame to frame, by construction.

At the source, every frame of every shot is exactly one simulation tick after the one before and two drawn frames later (`frame_ticks`, `drawn_frames_per_filmed_frame` per take in the manifest); the only exception is the declared cut inside each build take.

### Known compromises

- **Event-list rows in the fights.** The fight shots show three to six event-list rows ("Your Warrior is under attack", conversions) in the band at the top of the map. That is the real interface during a battle; the screenshot protocol's two-row limit cannot be held for seconds of continuous fighting, and in the filmed stretches no window of the needed length had fewer than three. The rows sit above the action. The colony shots show at most two rows.
- **Fog-dimmed ground in the fights.** The fights are on the blue colony's ground, which the red colony sees only around its own units, so parts of the fight frames are dimmed by fog of war (not black): measured on the finished files (dark-green share of the map above the text band, every 0.5 s), the opening fight is 27 % dimmed on iPhone and 40 % on iPad, the second fight 36 % and 50 % (version 1: 41 % and 47 %, 42 % and 56 %). The cameras centre the clash, which is lit; the dimmed ground is at the sides, where the red colony has no units. The clash itself is in lit ground.
- **Simulator, not hardware.** The previews are simulator screenshots of the iOS app, not recordings from a physical iPhone or iPad. Apple's pages describe capture from a device; the app's pixels are the same, but the simulator uses the portable SDL renderer and draws HD artwork forced on.
- **Frame-stepped, not a live recording.** The match was held between ticks and stepped. The simulation is unchanged by this (it runs the same ticks), and the capture clock makes every presentation clock advance as on a 60 Hz device. The AIs plan on their own threads in real time, so they had more wall-clock time per tick than on a device; that changes which continuation of the match was filmed, not how it looks. Units are drawn at their exact tick positions (the in-between motion smoothing a device adds between ticks is off while a match is held), which is what a 30 Hz capture of a device would show at each tick.
- **Footage not strictly chronological**: the fights are from the save at tick 27,015 and the colony from the same match at tick 45,017 onwards.
- **Only English** is rendered.

## Reproduce

```sh
# 1. App: the capture worktree at origin/master 5e96273ff62f with both patches applied
git -C glob2-wt-mobile-capture apply ../glob2-marketing/assets/storefront-v2/captures/mobile/tools/capture-build.patch
git -C glob2-wt-mobile-capture apply ../glob2-marketing/assets/storefront-v2/app-previews/tools/capture-frame-clock.patch
GLOB2_CAPTURE_MCP=1 python3 platforms/mobile/ios.py build --environment simulator --release --developer-dir $DEVELOPER_DIR
#    (Python 3.13 first in PATH; the mobile captures README has the dependency steps)

# 2. Frames
cd assets/storefront-v2/app-previews/tools
export GLOB2_WT=/Users/bradley/glob2/glob2-wt-mobile-capture GLOB2_SCRATCH=/path/to/scratch
# GLOB2_SCRATCH holds sim.env (IPHONE=..., IPAD=..., IPAD_B=..., the simulator ids) and saves/ (copies of ../../captures/mobile/saves/*.game.gz)
RUN="uv run --with pillow --with numpy python"
$RUN capture_frames.py iphone-6.9 build,fed,hero,fight-a,fight-b --tag=-r1   # build-r1 not used
$RUN capture_frames.py iphone-6.9 build --tag=-r2
$RUN capture_frames.py ipad-13 build,fed,hero,fight-a,fight-b --tag=-r2      # build-r2 not used
GLOB2_SIM_KEY=IPAD_B GLOB2_MCP_PORT_OVERRIDE=47932 $RUN capture_frames.py ipad-13 build --tag=-r3
$RUN take_metrics.py $GLOB2_SCRATCH/raw-frames/iphone-6.9/fight-a-r1        # rows and fog per frame, for in points

# 3. Cards, previews, checks, manifest
GLOB2_GAME=$GLOB2_WT uv run render_preview_cards.py --locale en --out $CARDS
GLOB2_GAME=$GLOB2_WT $RUN build_previews.py --raw $GLOB2_SCRATCH/raw-frames --cards $CARDS --out $OUT --poster
$RUN check_previews.py $OUT/glob2-app-preview-iphone-6.9-886x1920.mp4 --device iphone-6.9 --sheets .. --json check-iphone.json
$RUN check_previews.py $OUT/glob2-app-preview-ipad-13-1200x1600.mp4 --device ipad-13 --sheets .. --json check-ipad.json
$RUN check_cadence.py $OUT/glob2-app-preview-iphone-6.9-886x1920.mp4 --device iphone-6.9 --cuts 3.0,9.6,12.2,15.4,19.4 --json cadence-iphone.json
$RUN check_cadence.py $OUT/glob2-app-preview-ipad-13-1200x1600.mp4 --device ipad-13 --cuts 3.0,9.6,12.2,15.4,19.4 --json cadence-ipad.json
$RUN make_manifest.py --renders $OUT --raw $GLOB2_SCRATCH/raw-frames --cards $CARDS --checks check-iphone.json,check-ipad.json \
    --cadence cadence-iphone.json,cadence-ipad.json --superseded $OUT/superseded
```

A loaded save does not replay identically (the AIs plan asynchronously), so a new run films a different continuation; the in points in `previews.json` belong to the takes filmed on 2026-11-25. Those raw frames (PNG with a `take.json` per take, about 30 GB with the unused takes) stay in the session scratch directory `/private/tmp/claude-501/-Users-bradley-glob2/4d02c18b-dc3e-4981-ab5e-77b65e7adafe/scratchpad/app-previews-v2/raw-frames/`; a SHA-256 over each used take's frames is in the manifest (`frames_sha256`).

## Tools

| File | Purpose |
| --- | --- |
| [tools/pv.py](tools/pv.py) | Shared setup: device classes, MCP ports (47930 iPhone, 47931 iPad, overridable), reuse of the mobile capture driver |
| [tools/capture-frame-clock.patch](tools/capture-frame-clock.patch) | The capture-only game patch: the capture clock (draw gate, frame clock, no hold label) and its `game_time` switch |
| [tools/capture_frames.py](tools/capture_frames.py), [tools/takes.json](tools/takes.json) | Film takes from the iOS app in the Simulator, one tick per frame; the take definitions |
| [tools/take_metrics.py](tools/take_metrics.py) | Event rows, fog and unit pixels per frame of a take, to choose in points |
| [tools/render_preview_cards.py](tools/render_preview_cards.py) | Text cards per preview size through the trailer's renderer |
| [tools/previews.json](tools/previews.json) | Edit data: timelines (in frames), text cues, wordmark, music plan, poster, encode settings, card style |
| [tools/build_previews.py](tools/build_previews.py) | Frames to 30 fps, downscale, cards, music, encode, poster |
| [tools/check_previews.py](tools/check_previews.py) | Apple-spec check with ffprobe, frame timing, loudness, status-bar check, contact sheets (1 and 4 frames a second) |
| [tools/check_cadence.py](tools/check_cadence.py) | Held and jumping frames in the gameplay area, for finished files or raw takes |
| [tools/make_manifest.py](tools/make_manifest.py) | Writes manifest.json |

Version 1's real-time recorder (`tools/record.py`) is replaced by `capture_frames.py`; it remains in Git history. Scripts are `GPL-3.0-or-later`, like the game.
