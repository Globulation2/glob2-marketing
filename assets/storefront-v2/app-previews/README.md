# Storefront-v2 App Store app previews

[Manifest](manifest.json) · [Edit data](tools/previews.json) · [Takes](tools/takes.json) · [Trailer](../trailer/README.md) · [Mobile captures](../captures/mobile/README.md) · [Footage rule](../../../planning/gameplay-video.md)

Two App Store app previews, made **2026-11-25** from the iOS app of Globulation 2 **0.11.8.0** (release commit `5e96273ff62f` plus the capture-only patch described below), recorded in the iOS Simulator while the match ran live at normal speed. Every frame is the simulator's own screen recording of the app. Nothing is AI-generated, stock, sped up or slowed down, and no desktop footage is used. They are for the **next editable iOS version** in App Store Connect; nothing has been uploaded.

| File | Device slot | Pixels | Length |
| --- | --- | --- | --- |
| `glob2-app-preview-iphone-6.9-886x1920.mp4` | iPhone 6.9-inch display, portrait | 886×1920 | 25.0 s |
| `glob2-app-preview-ipad-13-1200x1600.mp4` | iPad 13-inch display, portrait | 1200×1600 | 25.0 s |

## Where the files live

The repository keeps this README, [manifest.json](manifest.json), [tools/](tools/), the poster frames and the contact sheets. The two MP4s are **not committed**: they are in `../storefront-v2-renders/app-previews/` relative to the repository root (`/Users/bradley/glob2/storefront-v2-renders/app-previews/` on the machine that made them), beside the trailer renders, and [.gitignore](.gitignore) here ignores `*.mp4` and `*.mov`. Their bytes and SHA-256 are in the manifest (`deliverables[].sha256`). Both are reproducible from the raw takes with `tools/` (see [Reproduce](#reproduce)).

## Apple's specification and how each file meets it

Read on 2026-11-25 from App Store Connect Help, [App preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-preview-specifications), and [App previews](https://developer.apple.com/app-store/app-previews/).

| Apple requirement | iPhone 6.9-inch file | iPad 13-inch file |
| --- | --- | --- |
| Accepted resolution (iPhone 6.9/6.5/6.3-inch class: 886×1920 portrait; iPad 13-inch: 1200×1600 portrait) | 886×1920 | 1200×1600 |
| 15–30 seconds | 25.000 s | 25.000 s |
| At most 30 fps | constant 30 fps, 750 frames, every frame step 33.333 ms | same |
| H.264, up to High profile level 4.0, progressive | H.264 High, level 4.0, progressive, yuv420p | same |
| `.mov`, `.m4v` or `.mp4` | `.mp4` (faststart) | same |
| Target 10–12 Mbps | 10.89 Mbps | 10.99 Mbps |
| At most 500 MB | 34.9 MB | 35.2 MB |
| Stereo audio, AAC 256 kbps, 44.1 or 48 kHz, all tracks enabled | one stereo AAC-LC track, 256 kbps, 48 kHz, default (enabled) | same |

All of this was measured on the finished files with ffprobe by [tools/check_previews.py](tools/check_previews.py); the full report per file is in the manifest under `deliverables[].spec_check`. Loudness: -14.2 LUFS integrated, true peak -1.9 dBTP (iPhone); -14.2 LUFS, -1.9 dBTP (iPad). Colour is tagged BT.709 (the simulator records Display P3; see [Picture path](#picture-path)).

Content rules from the same pages, and how the previews follow them:

- **Only content captured from the app.** Every picture is a recording of the iOS app's screen. The only additions are the text cards and the closing wordmark (below), which Apple allows as overlays.
- **No device frames, no hands, no people**: none.
- **No prices, no calls to action, no other platforms, no dates**: none. The iPad status bar shows a date next to the time; it is pinned to the simulator override `9:41 AM Tue Jan 9` (Apple's own marketing time) so it shows no real or current date. The iPhone status bar shows only `9:41`.
- **Text legible and on screen long enough**: each line stays 2.8–4.1 s, in the trailer's heavy cream type at 70–101 px with a soft scrim.
- **Music**: one score, the game's own soundtrack, licensed with the game (below).
- **Violence**: Apple asks previews to avoid objectionable violence. The fights are the game's cartoon combat of round "globs" (no blood or gore), within the app's own App Store age rating, which already lists cartoon or fantasy violence ([claims](../../../facts/storefront-v2-claims.md)); the same imagery is in the screenshots and the trailer. Flagged here for whoever uploads.
- **Poster frame**: Apple uses the frame at 5 s unless another is chosen. See [Poster frame](#poster-frame).

## Shot lists

Both previews echo the trailer: open inside a fight with no text, then the player building, the colony fed, a second look at the fight, and the colony at work under the fair-deal line, with the wordmark over the last 2.2 s. Lines are `trailer_line_1`..`4` from `translations/en.md`.

### iPhone 6.9-inch (886×1920)

| # | Time (s) | Take, in point | Save, ticks | Camera (centre tile, tile size) | What it shows | Text |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0–3.0 | `fight-a-r1` 0.6–3.6 s | `bigpond-n-t27015`, ticks 27509–27629 | (40, 58), about 30 pt | opens inside the fight: red army against blue defenders at the front | — |
| 2 | 3.0–9.6 | `build-r3` 1.3–7.9 s | `bigpond-n-t45017`, ticks 47931–48141 | (44, 32), about 30 pt | Build palette opens, the Inn is armed, the map is tapped, Ok; the site appears and workers head for it | `trailer_line_1` |
| 3 | 9.6–12.2 | `build-r3` 29.4–32.0 s | `bigpond-n-t45017`, ticks 48772–48877 | (44, 32), about 30 pt | same take, 21.5 s later: workers finish the Inn ("The Inn is finished.") | `trailer_line_1` |
| 4 | 12.2–15.4 | `fed-r3` 1.0–4.2 s | `bigpond-n-t45017`, ticks 49549–49674 | (40, 18), about 26 pt | wheat fields above the lake shore, inns below, workers carrying | `trailer_line_2` |
| 5 | 15.4–19.4 | `fight-b-r1` 6.0–10.0 s | `bigpond-n-t27015`, ticks 27711–27861 | (39, 60), about 24 pt | the front, wider: the red and blue lines clash | `trailer_line_3` |
| 6 | 19.4–25.0 | `hero-r3` 2.0–7.6 s | `bigpond-n-t45017`, ticks 50127–50318 | (56, 29), about 20 pt | the colony core: pools, racetrack, barracks, inns and hundreds of globs | `trailer_line_4`, wordmark from 22.8 s |

Text cues: `trailer_line_1` 7.9–12.0 s, `trailer_line_2` 12.5–15.3 s, `trailer_line_3` 15.7–19.2 s, `trailer_line_4` 19.8–22.6 s; wordmark 22.8–25.0 s. Music: combat mood under the fights (0–3.0 s, 15.4–19.4 s), building mood elsewhere.

Shots 2 and 3 are one take: the Inn placed by touch at 1.5–7.4 s of the take, then a declared cut of 21.5 s to the workers finishing it ("The Inn is finished." appears in the event list).

### iPad 13-inch (1200×1600)

| # | Time (s) | Take, in point | Save, ticks | Camera (centre tile, tile size) | What it shows | Text |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0–3.0 | `fight-a-r2` 6.0–9.0 s | `bigpond-n-t27015`, ticks 27676–27794 | (39, 58), about 52 pt | opens inside the fight: red army against blue defenders at the front | — |
| 2 | 3.0–7.2 | `build-r11-a1` 1.2–5.4 s | `bigpond-n-t45017`, ticks 47972–48032 | (44, 32), about 40 pt | Build palette opens (named on tablets), the Inn is armed, the map is tapped and the ghost shows | — |
| 3 | 7.2–11.6 | `build-r11-a1` 7.8–12.2 s | `bigpond-n-t45017`, ticks 48140–48278 | (44, 32), about 40 pt | same take, 2.4 s later (cut past the app's 2 s hitch while it confirms): Ok has placed the Inn site, the palette closes, workers head for the scaffold | `trailer_line_1` |
| 4 | 11.6–15.0 | `fed-r4` 2.0–5.4 s | `bigpond-n-t45017`, ticks 49773–49863 | (40, 19), about 34 pt | wheat fields above the lake shore, inns below, workers carrying | `trailer_line_2` |
| 5 | 15.0–19.4 | `fight-b-r2` 9.0–13.4 s | `bigpond-n-t27015`, ticks 27788–27953 | (38, 59), about 44 pt | the front from a second load of the save: the red and blue lines clash | `trailer_line_3` |
| 6 | 19.4–25.0 | `hero-r1` 5.0–10.6 s | `bigpond-n-t45017`, ticks 49713–49888 | (52, 30), about 28 pt | the colony core: pools, racetracks, barracks, inns and hundreds of globs | `trailer_line_4`, wordmark from 22.8 s |

Text cues: `trailer_line_1` 7.5–11.4 s, `trailer_line_2` 11.9–14.7 s, `trailer_line_3` 15.3–19.2 s, `trailer_line_4` 19.8–22.6 s; wordmark 22.8–25.0 s. Music: combat mood under the fights (0–3.0 s, 15.0–19.4 s), building mood elsewhere.

Shots 2 and 3 are one take with a declared 2.4 s cut: the app hitched for about 2 s while the iPad confirmed the placement (frames up to 357 ms apart in the recording, on a machine under heavy load from other jobs), and the cut skips that stretch. The iPad take ends before the Inn is finished (at 50 s it had 135 of 200 hit points), so the iPad preview shows the new site and the workers at it, not the finished Inn. The iPad camera tile sizes are approximate for the takes recorded before 2026-11-25 15:20 (a calibration that overstated the screen width by 2.3 %); the exact game_view zoom is in the manifest.

Each take's tick range, camera, event-list rows and player inputs are in the manifest under `takes`.

## How it was recorded

- **App and device.** The iOS app built from the release commit with `platforms/mobile/ios.py` in the capture worktree `/Users/bradley/glob2/glob2-wt-mobile-capture`, plus [the capture-only patch](../captures/mobile/tools/capture-build.patch): three small edits that compile the desktop MCP automation listener into the simulator build so scripts can tap the real touch controls. It changes no rendering, HUD or simulation code and never ships. The simulators are the isolated set in that worktree (`build/mobile-tools/ios-simulators`): *Glob2-Capture-iPhone-6.9* (iPhone 17 Pro Max, iOS 26.5) and *Glob2-Capture-iPad-13* (iPad Pro 13-inch M5, iOS 26.5). HD artwork is forced on. The simulator package draws with the portable SDL renderer (the Metal renderer devices use is not available in the Simulator).
- **Saves.** The mature saves of the mobile captures ([../captures/mobile/saves/](../captures/mobile/saves/)): `bigpond-n-t27015` (A big pond, tick 27,015: the red army attacks the blue colony; fights in the first 1,000 ticks after loading) and `bigpond-n-t45017` (the same match at tick 45,017: about 340 workers, 240 warriors and 70 buildings; the match is won a minute after loading and the player presses *Continue playing*).
- **Player view, not spectator view.** Colony 1 (red) is **You + AI**: the Nicowar AI grew and still co-plays the colony; the HUD is the local player's. The opponents are AI colonies. The scripted inputs per take are listed in the manifest (`takes[].player_actions`): the *Health and food bars* lens switched off; *Continue playing* on the "You have won" dialog (colony saves); the zone tool erasing the co-controlling AI's forbidden, guard and clearing zones before and every 1.5 s during each take (every 3 s in the two iPhone fight takes; the clean-state protocol of the mobile captures; the AI repaints them); and in the build take, Build → Inn → tap → Ok → close.
- **Recording.** [tools/record.py](tools/record.py) loads the save through the game's Load game screen, points the camera with `game_view`, and records the simulator display with `xcrun simctl io <device> recordVideo --codec=h264 --mask=ignored` at native pixels (1320×2868, 2064×2752), while the match runs at 1x. Nothing is paused or stepped. It logs the match tick and the event-list rows every 0.5–2 s; every segment used ran at 29–30 ticks a second (the game's normal speed is 30).
- **The Inn placement.** The building is placed **by touch** in the recording: Build opens the palette, the Inn is armed, the map is tapped (the ghost shows), Ok confirms, the palette closes. The site, the workers arriving and (on iPhone) the finished Inn ("The Inn is finished.") are all in the recording; record.py checks afterwards that an Inn stands on that tile (`buildings_at_site_after` in the iPad take). To find clear ground on iPhone, record.py first asked the game where an Inn fits near the inn cluster (`game_place` with `near`, the game's own search), destroyed that probe site at once and waited, all before the recording started; the touch placement then used that spot (43, 31). On iPad the destroyed probe site kept blocking the ground, so the take uses the same tile (43, 31) directly, with no probe. Sixteen earlier iPad build takes did not place the Inn (app hitches under machine load, the probe site in the way, then a tap one tile off from a zoom calibration error; all fixed), and one that did (r10) showed zone outlines because erasing was paused during the placement; none of them is used.

### Picture path

[tools/build_previews.py](tools/build_previews.py), all edit data in [tools/previews.json](tools/previews.json):

1. Each segment is cut from its take and put on a constant 30 fps grid (`fps=30`, nearest frame): each output frame shows what the simulator showed at that moment, so the game plays at real speed. The simulator delivers 30–60 distinct frames a second, so no frame is invented.
2. **iPhone only: the Dynamic Island.** `simctl io recordVideo` composites the simulator's Dynamic Island cut-out (a black pill) into the status bar. A device screen recording and `simctl io screenshot` do not contain it: the screenshot shows flat status-bar colour there. The pill's box (native x 466–856, y 36–158, between the clock and the status icons) is filled with that flat colour. This is the only change to any game or system pixel; [tools/check_previews.py](tools/check_previews.py) checks in every second of the finished file that the filled box matches the status bar beside it (largest channel difference 0.28 of 255).
3. **Colour.** The recording is Display P3 (the status bar's sRGB 0,0,32 arrives as 0,0,30). Its primaries are converted to BT.709 with the sRGB curve kept, so the colours match the simulator screenshots and the store screenshots, and the file is tagged BT.709.
4. One Lanczos downscale to Apple's size: iPhone 1320×2868 → 886×1925, then the bottom 5 rows (the empty home-indicator band) are cropped to 886×1920; iPad 2064×2752 → 1200×1600 exactly (same 3:4 shape). Nothing is cropped from the game picture or the HUD.
5. Text cards, wordmark, music, encode (two-pass x264 at about 11 Mbps, AAC 256 kbps).

## Text and localisation

The cards are rendered by [tools/render_preview_cards.py](tools/render_preview_cards.py), which runs the trailer's [render_cards.py](../trailer/tools/render_cards.py) once per preview size with the style in [tools/previews.json](tools/previews.json): the same fields, fonts (Nunito 900 for Latin, Noto for other scripts), cream `#f9e8bb` and gold rule `#e3c077` as the trailer, laid out by headless Chromium at each preview size so no card is scaled. On iPhone, lines are 8.8 % of the width, centred at 74 % of the height (in the lower map area, above the bottom navigation bar, below the event list and clear of the action in the centre); on iPad, which has no bottom bar, 8.4 % of the width at 83 % of the height (`text_layout_by_size`). Each sits over a soft scrim. Two-sentence lines break between the sentences ("No ads. / No in-app purchases."). The text cues (field, start, end) are data in `previews.json`.

Only English is rendered now. A localized preview is two commands, once its `trailer_line_*` fields are in `translations/<locale>.md`:

```sh
uv run tools/render_preview_cards.py --locale ja --out $CARDS
uv run --with pillow --with numpy python tools/build_previews.py --raw $RAW --cards $CARDS --out $OUT --locale ja
```

The text is true of the footage: "You decide. They build." runs over the player's Inn going up; "Keep the colony fed." over wheat fields and inns with workers carrying; "Fight rivals for the land." over the red and blue armies fighting; "No ads. No in-app purchases." over the colony at work (the app has neither; see [storefront v2 claims](../../../facts/storefront-v2-claims.md)). There is no price, no "free", no call to action, no store badge and no URL. The wordmark is the game's own menu wordmark, as in the trailer.

## Music

The game's **original soundtrack by Jacques-Paul Grivaz**, licensed **GPL-3.0-or-later** like the rest of the game (`content/data/zik/original/`; credited in `docs/assets/source-attribution.md` and the in-game credits), exactly as the [trailer](../trailer/README.md#text-wordmark-and-music): the building mood (`a2.opus`) under the colony and the combat mood (`a3.opus`, lifted 4 dB) under the fights, cross-faded at the same playback position as the game's mixer does, a 2 s tail fade, and a limiter that keeps the true peak under −1 dBTP. The previews work muted, as Apple plays them by default.

## Poster frame

Apple shows the poster frame when autoplay is off, and uses the frame at 5 s unless another is set in App Store Connect. **Choose these instead** when uploading:

| Preview | Poster time | Frame | File | Why |
| --- | --- | --- | --- | --- |
| iPhone | 00:16.50 | 495 | [poster-iphone-6.9-886x1920.png](poster-iphone-6.9-886x1920.png) | Red and blue warriors clashing in the middle of the screen, "Fight rivals for the land." below: the most exciting frame that still reads at thumbnail size |
| iPad | 00:16.60 | 498 | [poster-ipad-13-1200x1600.png](poster-ipad-13-1200x1600.png) | The same beat in the iPad preview: the red army meeting the blue line, the line below |

The 5 s default would show the build palette (iPhone) or the armed Inn over the colony (iPad), which says less at a glance. The PNGs are the exact frames from the finished files, for checking what App Store Connect shows after the time is set.

## Review

Every second of both files was reviewed on 2026-11-25 by contact sheet, one frame per second (the middle frame of each second), at full size and at 240 px wide (about the width a preview plays at in App Store search results on a phone):

| Preview | Full size | Thumbnail |
| --- | --- | --- |
| iPhone | [full](contact-glob2-app-preview-iphone-6.9-886x1920-full.jpg) | [thumbnail](contact-glob2-app-preview-iphone-6.9-886x1920-thumb.jpg) |
| iPad | [full](contact-glob2-app-preview-ipad-13-1200x1600-full.jpg) | [thumbnail](contact-glob2-app-preview-ipad-13-1200x1600-thumb.jpg) |

Frames run left to right, top to bottom, one per second (0.5 s, 1.5 s, … 24.5 s).

- Every second shows colonies or a fight. No empty terrain, no early game, no menu, no black frame.
- The opening fight reads as two armies (red and blue) at thumbnail size; the build palette, the armed Inn, the ghost, the Ok button and the new site are visible at full size; the finished Inn is visible at full size and as a gold ring at thumbnail size.
- Text is legible at thumbnail size; no line covers the action it describes.
- Frame timing: constant 30 fps in both files (every step 33.333 ms). In the raw takes, the app's own frame delivery hitches once in the iPhone build segment (167 ms and 112 ms at 3.3 s of the take, while the palette arms the Inn); it shows as a held frame of 5 output frames. The iPad segments avoid the app's hitches (see the iPad shot list). Every segment ran at 29–30 ticks a second (from the take logs), so the game plays at its normal speed.

Known compromises:

- **Event list rows in the fights.** The fight segments show four to six event-list rows ("Your Warrior is under attack", conversions) at the top of the map. That is the real interface during a battle; the screenshot protocol's two-row limit cannot be held for seconds of continuous fighting. The rows sit in the top band, above the action.
- **Fog-dimmed ground in the fights.** The fights are on the blue colony's ground, which the red colony sees only around its own units, so parts of the fight frames are dimmed by fog of war (not black). The iPad fight takes were re-recorded closer (52 and 44 points a tile) so the clash fills more of the frame.
- **Simulator, not hardware.** The previews are simulator recordings of the iOS app, not recordings from a physical iPhone or iPad. Apple's pages describe capture from a device; the app's pixels are the same, but the simulator uses the portable SDL renderer and draws HD artwork forced on.
- **Footage not strictly chronological**: the fights are from the save at tick 27,015 and the colony from the same match at tick 45,017–50,500.
- **Only English** is rendered.

## Reproduce

```sh
cd assets/storefront-v2/app-previews/tools
export GLOB2_WT=/Users/bradley/glob2/glob2-wt-mobile-capture GLOB2_SCRATCH=/path/to/scratch
# GLOB2_SCRATCH holds sim.env (IPHONE=..., IPAD=..., the simulator ids) and saves/ (copies of ../../captures/mobile/saves/*.game.gz)
RUN="uv run --with pillow --with numpy python"
$RUN record.py iphone-6.9 fight-a,fight-b --tag=-r1
$RUN record.py iphone-6.9 build,fed,hero --tag=-r3
$RUN record.py ipad-13 fight-a,fight-b --tag=-r2
$RUN record.py ipad-13 hero --tag=-r1
$RUN record.py ipad-13 fed --tag=-r4
$RUN record.py ipad-13 build --tag=-r11   # retries until the Inn is placed; attempt -a1 was used
GLOB2_GAME=$GLOB2_WT uv run render_preview_cards.py --locale en --out $CARDS
GLOB2_GAME=$GLOB2_WT $RUN build_previews.py --raw $GLOB2_SCRATCH/raw --cards $CARDS --out $OUT --poster
$RUN check_previews.py $OUT/glob2-app-preview-iphone-6.9-886x1920.mp4 --device iphone-6.9 --sheets .. --json check-iphone.json
$RUN check_previews.py $OUT/glob2-app-preview-ipad-13-1200x1600.mp4 --device ipad-13 --sheets .. --json check-ipad.json
$RUN make_manifest.py --renders $OUT --raw $GLOB2_SCRATCH/raw --cards $CARDS --checks check-iphone.json,check-ipad.json
```

A loaded save does not replay identically (the AIs plan asynchronously), so a new run records a different continuation; the in points in `previews.json` belong to the takes recorded on 2026-11-25. Those raw takes (`.mov` with JSON sidecars, about 5 GB with the unused takes) stay in the session scratch directory `/private/tmp/claude-501/-Users-bradley-glob2/4d02c18b-dc3e-4981-ab5e-77b65e7adafe/scratchpad/app-previews/raw/`; their SHA-256 are in the manifest.

## Tools

| File | Purpose |
| --- | --- |
| [tools/pv.py](tools/pv.py) | Shared setup: device classes, MCP ports (47930 iPhone, 47931 iPad), reuse of the mobile capture driver |
| [tools/record.py](tools/record.py), [tools/takes.json](tools/takes.json) | Record takes from the iOS app in the Simulator with `simctl io recordVideo`; the take definitions |
| [tools/render_preview_cards.py](tools/render_preview_cards.py) | Text cards per preview size through the trailer's renderer |
| [tools/previews.json](tools/previews.json) | Edit data: timelines, text cues, wordmark, music plan, poster, island box, encode settings, card style |
| [tools/build_previews.py](tools/build_previews.py) | Cut, island fill, colour conversion, downscale, cards, music, encode, poster |
| [tools/check_previews.py](tools/check_previews.py) | Apple-spec check with ffprobe, frame timing, loudness, island check, contact sheets |
| [tools/make_manifest.py](tools/make_manifest.py) | Writes manifest.json |

Scripts are `GPL-3.0-or-later`, like the game.
