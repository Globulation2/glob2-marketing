# Web-portal art (lite build)

[Manifest](manifest.json) · [Build script](tools/build.py) · [Capture tools](tools/) · [Poki research](../../analysis/poki-listing-comparison.md) · [CrazyGames research](../../analysis/crazygames-listing-comparison.md) · [GameDistribution research](../../analysis/gamedistribution-listing-comparison.md) · [Web portal rollout](../../planning/web-portal-rollout.md) · [Footage rule](../../planning/gameplay-video.md)

Made **2026-11-26** for the portals that will ship the **lite** browser edition (Poki, CrazyGames; GameDistribution if it takes lite). Nothing here has been uploaded and no listing was changed.

Every picture is the lite build's own canvas: **Globulation 2 0.11.8.2 lite** (tag `v0.11.8.2`, commit `8fb3c06aee`), the verified `browser-release-lite` artifact of release-mirror run 45902410410 (package `b3eb782b40c80032`, the same files the lite portal zips carry), served locally and run in Playwright's own headless Chromium (WebGL2, Portable SDL renderer; `globalThis.Glob2Edition.name` read back as `lite` in every take). So the terrain, sprite quality (WebP Q70, no HD art), folded terrain materials and repeating variant blocks are what lite players see. No AI-generated or stock imagery, no painting, no retouching, no scaling up. The only addition is the game's own wordmark on the CrazyGames and GameDistribution covers (the cover rule allows the title only). **The Poki files carry no text at all.**

## Files

Stills and a review sheet are committed here. The three MP4s are **not committed**, following the trailer's convention ([trailer README](../storefront/trailer/README.md), `*.mp4` kept out of Git): they are in `../storefront-v2-renders/portal-art/<portal>/` relative to the repository root (`/Users/bradley/glob2/storefront-v2-renders/portal-art/` on the machine that made them), with SHA-256 in the [manifest](manifest.json). They are rebuilt byte-for-byte from the raw takes in `../storefront-v2-renders/portal-art/takes/` by `tools/build.py`.

| Portal | File | Size | Spec it meets |
| --- | --- | --- | --- |
| Poki | [`poki/poki-thumbnail-1080x1080.png`](poki/poki-thumbnail-1080x1080.png) | 1080×1080 PNG, 1.3 MB | square, ≥ 628×628, full-bleed, no text, no `#83FFE7` |
| Poki | `glob2-lite-poki-animated-thumbnail-1080x1080.mp4` (renders) | 1080×1080, 60 fps, 5.87 s, H.264, no audio, 4.3 MB | 1:1, ≥ 1080, ≥ 50 fps, 4–6 s, muted MP4, ≤ 100 MB; 3 scenes of about 2 s; opens on the static thumbnail (its first frame *is* the thumbnail); no cursor, no text |
| CrazyGames | [`crazygames/crazygames-cover-landscape-1920x1080.jpg`](crazygames/crazygames-cover-landscape-1920x1080.jpg) | 1920×1080 JPEG | 16:9 cover, title only, no border |
| CrazyGames | [`crazygames/crazygames-cover-portrait-800x1200.jpg`](crazygames/crazygames-cover-portrait-800x1200.jpg) | 800×1200 JPEG | 2:3 cover, title only |
| CrazyGames | [`crazygames/crazygames-cover-square-800x800.jpg`](crazygames/crazygames-cover-square-800x800.jpg) | 800×800 JPEG | 1:1 cover, title only |
| CrazyGames | `glob2-lite-crazygames-preview-landscape-1920x1080.mp4` (renders) | 1920×1080, 30 fps, 18.1 s, H.264, no audio, 13.2 MB | 16:9 1080p, 15–20 s, ≤ 50 MB, silent, no cursor, no black bars, real speed; opens on the 16:9 cover |
| CrazyGames | `glob2-lite-crazygames-preview-portrait-1080x1620.mp4` (renders) | 1080×1620, 30 fps, 18.1 s, H.264, no audio, 12.0 MB | 2:3 1080p, same rules; a real portrait game window, not a crop of the landscape take; opens on the 2:3 cover |
| GameDistribution | [`gamedistribution/`](gamedistribution/) `-1280x720`, `-1280x550`, `-512x384`, `-512x512`, `-200x120` (JPEG) | as named | the five standard asset sizes (action 4 of the GameDistribution list); lite art, so valid whichever build is chosen |

**Covers and preview openings.** CrazyGames asks for the static cover to be the video's opening frame. Each preview's first frame is its cover: the same game frame with the same wordmark layer. The wordmark holds for 1.2 s over the moving game and fades out by 1.8 s; the rest of each video has no text. The 1:1 cover has no video; it is a 1080×1080 window of the 16:9 cover's frame, downscaled. Every cover is a downscale or native pixels.

**Not made, and why.** Yandex Games is parked (applications closed, ads undecided); its screenshots, cover, icon and video wait for that. GamePix already has its icon and cover (2026-11-26) and its video slot takes the existing YouTube trailer, which shows the standard build. No Poki or CrazyGames text or copy is here; those are fields, not art.

## Shot list

All footage is from one match, watched in the lite build's **spectator view** (see "Clean picture"). Both colonies are played by the game's built-in AIs (red: Cortex, cyan: Cabino), so this is **AI-versus-AI footage, a spectator view**. The only inputs were camera moves (minimap click, zoom buttons) and the *health and food bars* key (`I`).

| Cut | Take | From (s) | Length (s) | Tick at take start | Camera | What it shows | Water in frame |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Poki 1 (= static thumbnail) | `poki-p1` | 0.3 | 1.95 | ~40,050 | 195 % (7 clicks), minimap 0.76, 0.87 | **The fight:** cyan Cabino warriors raid a row of red hospitals and inns; two are burning (smoke), red warriors meet them, hit flashes | none |
| Poki 2 | `poki-p2` | 0.3 | 1.95 | ~39,200 | 195 %, 0.65, 0.48 | A red Swarm with wheat fields and globs around it | none |
| Poki 3 | `poki-p3` | 0.3 | 1.95 | ~42,570 | 195 %, 0.715, 0.83 | A second clash: cyan warriors pushing through a forest gap into red warriors | none |
| CrazyGames 1 (16:9 and 2:3; covers) | `land-s1`, `port-s1` | 0.5 | 7.0 | ~40,050 | 195 %, 0.733, 0.87 | The same fight as Poki 1, wider | 16:9: a small corner of a lake at the top right |
| CrazyGames 2 | `land-s2`, `port-s2` | 1.0 | 5.5 | ~39,170 | 121 % (2 clicks), 0.61, 0.44 | The red colony's core: three Swarms, inns, hospitals, wheat, globs at work, cyan scouts among them | 16:9: a corner at the bottom left; 2:3: a corner at the top |
| CrazyGames 3 | `land-s3`, `port-s3` | 1.0 | 5.5 | ~42,560 | 161 % (5 clicks), 0.70 / 0.715, 0.83 | The second clash, cyan warriors coming through the forest gap | 16:9: a thin strip at the right edge |

Exact ticks, frame counts, viewport, codec and SHA-256 of every take are in the [manifest](manifest.json) under `takes`.

**Water (lite water is under investigation).** The owner is looking at how lite draws water (flat dark blue with rows of plant sprites). Every shot was framed to keep water out. Files with any water: the 16:9 cover and the GameDistribution images cut from it (a corner at the top right), the 16:9 preview (that corner in shot 1, a corner at the bottom left in shot 2, a strip at the right edge in shot 3) and the 2:3 preview (a corner in shot 2). **No water:** the Poki thumbnail and animated thumbnail, the 2:3 and 1:1 covers. Redo the files with water after a water fix.

## How it was made

1. **Match.** Lite has no command-line tools, so the match was played headless on the installed desktop build (Globulation 2 0.11.7.0 + 15 commits, revision `5bf966285aa8`, `/Applications/Glob2.app`; same save format, version 219, as 0.11.8.2), with only AIs that lite ships (Maxima and the JavaScript AIs are compiled out of lite):
   ```sh
   glob2 map generate marchland --seed 2104 --width 128 --height 128 --teams 2 --output marchland-2t-2104.map
   GLOB2=/Applications/Glob2.app/Contents/MacOS/glob2 assets/storefront/captures/desktop/tools/run-match.sh \
     matches/marchland-2t marchland-2t-2104.map.gz 4104 54000 3000 cortex cabino
   ```
   Marchland is one of lite's random-map landscapes (the generator list is identical in 0.11.7.0 and 0.11.8.x). A 2-colony map was chosen so the AIs meet; the 4-colony matches tried first (Crater lakes, Coral, Marchland) produced no ground fight in view.
2. **Finding the fight.** The same match re-run with `--telemetry warrior-tactics` (identical final checksum, 1848144303) logs every warrior's fighting episodes with tile positions. The biggest clash is around tile (44, 56) from tick 40,000, and a second around tile (44, 52) near tick 42,500. The camera was aimed with the minimap, which the game centres on the red colony's start (`src/render/Minimap.cpp`).
3. **Lite takes.** The lite package is served by the game repository's `platforms/web/serve.py` (port 8791) and opened in Playwright's own headless Chromium (`playwright` 1.63, `--use-angle=metal`). `tools/session.js` writes `graphicsDetailAdaptive=0`, `clouds=0`, `cloudShadows=0` (clouds off, as in the desktop captures and trailer), reloads, copies the checkpoint (39,000 or 42,000) into the game's save folder, opens it through **Load game**, and presses `I`. The lite build then simulates and draws the match from that save at normal speed (30 ticks a second). `tools/record.js` zooms with the game's `+` button, centres with a minimap click, waits (31 s at 39,000 to reach the fight, 15 s at 42,000, else 3 s) and records the canvas with `canvas.captureStream(60)` and `MediaRecorder` (VP9 for the square takes, H.264 for the others, 120 Mbit/s). The canvas holds only the game's drawing, so there is no cursor. Windows: 2122×1260 (16:9), 1282×1800 (2:3), 1282×1260 (square), device pixel ratio 1.
   ```sh
   NODE_PATH=<a node_modules with playwright 1.63> node tools/record.js SAVE OUT.webm W H FX FY ZOOM_CLICKS SECONDS [WAIT_MS]
   ```
   Takes were recorded one at a time, and re-recorded when a take came out under about 45 fps.
4. **Edit.** `uv run --with pillow python assets/portal-art/tools/build.py` crops each take to the map view (below the top bar and the event list, left of the 200-px panel), cuts and joins the shots, resamples to constant 30 fps (CrazyGames) or 60 fps (Poki), adds the title layer to the CrazyGames openings, encodes H.264 High, CRF 17, yuv420p, BT.709, `+faststart`, no audio track, and writes the stills, [`contact-sheet-tile-size.png`](contact-sheet-tile-size.png) and `manifest.json`. The wordmark is the key-art script's treatment of the game's `content/data/gfx/menu-wordmark.png` (imported from [`../storefront/key-art/build-assets.py`](../storefront/key-art/build-assets.py)), always downscaled. It sits at the bottom of each cover, clear of the fight.

Raw takes, the two checkpoints, the map, the match result and the warrior telemetry are kept with the renders (`takes/`, `saves/`), not in Git.

## Clean picture: no zone outlines

The first pass (commit d6be195) showed the red AI's clearing zones as red squares. They are gone, by the first method on the review's list: **a display option in the lite build.** Loading an AI-only save (no player seat) opens the game's live **spectator view** (`GlobalContainer::liveSpectating`). Its option panel has **Show areas**, off by default (`replayShowAreas = false`, `src/engine/EngineInit.cpp`; drawn only when set, `src/render/GameRender.cpp` and `GameRenderTerrain.cpp`), so forbidden, guard and clearing areas are not drawn. The same view starts with **Fog of war** off and **Combined vision** on, so no land is dimmed. Nothing was erased and the match is unchanged. Flags stay shown (the panel default).

## Checked at tile size

[`contact-sheet-tile-size.png`](contact-sheet-tile-size.png) shows every still as a portal shows it: the Poki thumbnail at 200 px, the CrazyGames covers at 300 px wide (portrait at 200×300), and the GameDistribution 200×120 at its own size. At those sizes the red and cyan warriors and the burning buildings read as a fight, and the title is legible on every CrazyGames and GameDistribution image.

## Needs a human eye

- **Grain.** The fight shots are at 195 %, so lite's sprites are drawn at about twice their native size by the game. That is what a lite player zoomed in sees, but it is softer than the 121 % shots.
- **Fight size.** About a dozen to twenty warriors a side, the largest clash the telemetry found in this match.
- **Water.** See the list above.
- **Event list.** The crop starts below the deepest five-row event list seen; a sixth row would show at the top edge. Checked by eye on contact sheets of every cut.
- **Ads claim.** Nothing in the art says "No ads" or "Free".

## Reproduce

Serve `browser-release-lite` of run 45902410410 on 127.0.0.1:8791 with `platforms/web/serve.py`, then run `record.js` with the arguments in the manifest's `takes` for each of the nine takes, put them in `../storefront-v2-renders/portal-art/takes/`, and run `build.py`. A new recording is equivalent, not identical: the AIs keep playing and frame timing depends on the machine. The edit from the existing takes is deterministic.
