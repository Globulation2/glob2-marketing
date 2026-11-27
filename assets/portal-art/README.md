# Web-portal art (lite build)

[Manifest](manifest.json) · [Build script](tools/build.py) · [Capture tools](tools/) · [Poki research](../../analysis/poki-listing-comparison.md) · [CrazyGames research](../../analysis/crazygames-listing-comparison.md) · [GameDistribution research](../../analysis/gamedistribution-listing-comparison.md) · [Web portal rollout](../../planning/web-portal-rollout.md) · [Footage rule](../../planning/gameplay-video.md)

Made **2026-11-26** for the portals that will ship the **lite** browser edition (Poki, CrazyGames; GameDistribution if it takes lite). Nothing here has been uploaded and no listing was changed.

Every picture is the lite build's own canvas: **Globulation 2 0.11.8.2 lite** (tag `v0.11.8.2`, commit `8fb3c06aee`), the verified `browser-release-lite` artifact of release-mirror run 45902410410 (package `b3eb782b40c80032`, the same files the lite portal zips carry), served locally and run in Playwright's own headless Chromium (WebGL2, Portable SDL renderer; `globalThis.Glob2Edition.name` read back as `lite` in every take). So the terrain, sprite quality (WebP Q70, no HD art), folded terrain materials and repeating variant blocks are what lite players see. No AI-generated or stock imagery, no painting, no retouching, no scaling up. The only addition is the game's own wordmark on the CrazyGames and GameDistribution covers (the cover rule allows the title only). **The Poki files carry no text at all.**

## Files

Stills are committed here. The three MP4s are **not committed**, following the trailer's convention ([trailer README](../storefront/trailer/README.md), `*.mp4` kept out of Git): they are in `../storefront-v2-renders/portal-art/<portal>/` relative to the repository root (`/Users/bradley/glob2/storefront-v2-renders/portal-art/` on the machine that made them), with SHA-256 in the [manifest](manifest.json). They are rebuilt byte-for-byte from the raw takes in `../storefront-v2-renders/portal-art/takes/` by `tools/build.py`.

| Portal | File | Size | Spec it meets |
| --- | --- | --- | --- |
| Poki | [`poki/poki-thumbnail-1080x1080.png`](poki/poki-thumbnail-1080x1080.png) | 1080×1080 PNG, 1.4 MB | square, ≥ 628×628, full-bleed, no text, no `#83FFE7` |
| Poki | `glob2-lite-poki-animated-thumbnail-1080x1080.mp4` (renders) | 1080×1080, 60 fps, 5.85 s, H.264, no audio, 5.9 MB | 1:1, ≥ 1080, ≥ 50 fps, 4–6 s, muted MP4, ≤ 100 MB; 3 scenes of about 2 s; opens on the static thumbnail (its first frame *is* the thumbnail); no cursor, no text |
| CrazyGames | [`crazygames/crazygames-cover-landscape-1920x1080.jpg`](crazygames/crazygames-cover-landscape-1920x1080.jpg) | 1920×1080 JPEG | 16:9 cover, title only, no border |
| CrazyGames | [`crazygames/crazygames-cover-portrait-800x1200.jpg`](crazygames/crazygames-cover-portrait-800x1200.jpg) | 800×1200 JPEG | 2:3 cover, title only |
| CrazyGames | [`crazygames/crazygames-cover-square-800x800.jpg`](crazygames/crazygames-cover-square-800x800.jpg) | 800×800 JPEG | 1:1 cover, title only |
| CrazyGames | `glob2-lite-crazygames-preview-landscape-1920x1080.mp4` (renders) | 1920×1080, 30 fps, 18.0 s, H.264, no audio, 21.5 MB | 16:9 1080p, 15–20 s, ≤ 50 MB, silent, no cursor, no black bars, real speed; opens on the 16:9 cover |
| CrazyGames | `glob2-lite-crazygames-preview-portrait-1080x1620.mp4` (renders) | 1080×1620, 30 fps, 18.0 s, H.264, no audio, 17.4 MB | 2:3 1080p, same rules; a real portrait game window, not a crop of the landscape take; opens on the 2:3 cover |
| GameDistribution | [`gamedistribution/`](gamedistribution/) `-1280x720`, `-1280x550`, `-512x384`, `-512x512`, `-200x120` (JPEG) | as named | the five standard asset sizes (action 4 of the GameDistribution list); lite art, so valid whichever build is chosen |

**Covers and preview openings.** CrazyGames asks for the static cover to be the video's opening frame. Each preview's first frame is its cover: the same game frame with the same wordmark layer. The wordmark holds for 1.2 s over the moving game and fades out by 1.8 s; the rest of each video has no text. The 1:1 cover has no video; it is a 1080×1080 window of the 16:9 cover's frame, downscaled. Every cover is a downscale or native pixels.

**Not made, and why.** Yandex Games is parked (applications closed, ads undecided); its screenshots, cover, icon and video wait for that. GamePix already has its icon and cover (2026-11-26) and its video slot takes the existing YouTube trailer, which shows the standard build. No Poki or CrazyGames text or copy is here; those are fields, not art.

## Shot list

All footage is from one match. Every colony in it is played by the game's built-in AIs, so this is **AI-versus-AI footage, a spectator view** from a player seat that shares the red colony with its AI (Cortex). The seat made no input but camera moves (minimap click, zoom buttons) and the in-game *health and food bars* toggle (key `I`, off).

| Cut | Take | From (s) | Length (s) | Tick at take start | Camera | What it shows |
| --- | --- | --- | --- | --- | --- | --- |
| Poki 1 (= static thumbnail) | `poki-p2` | 0.3 | 1.95 | 42,216 | 195 % zoom (7 clicks), minimap 0.544, 0.536 | Red Swarm, inns and hospitals, a few dozen red globs walking between them, the shore at the right |
| Poki 2 | `poki-p1` | 0.3 | 1.95 | 42,216 | same zoom, 0.535, 0.586 | A second Swarm beside a large tan building at the forest edge, globs crossing the grass |
| Poki 3 | `poki-p3` | 0.3 | 1.95 | 36,216 | same zoom, 0.45, 0.50 | Red globs along the lake shore at the colony's northern edge |
| CrazyGames 1 (16:9 and 2:3) | `land-s1`, `port-s1` | 1.0 | 6.0 | 36,170 (16:9) | 121 % (2 clicks), 0.44, 0.51 | The red colony's core between two lakes: three Swarms, inns, hospitals, wheat, many globs at work, warriors on the shore |
| CrazyGames 2 | `land-s2`, `port-s2` | 1.0 | 6.0 | 42,170 | 121 %, 0.42, 0.56 | The same colony 6,000 ticks (3 min 20 s) later; lime rival units at the left edge |
| CrazyGames 3 | `land-s3`, `port-s3` | 1.0 | 6.0 | 36,171 | 121 %, 0.36, 0.62 | The colony's southern quarter: inns in rows, a Swarm and a school, globs on the paths |

Exact ticks, frame counts, viewport, codec and SHA-256 of every take are in the [manifest](manifest.json) under `takes`.

## How it was made

1. **Match (to reach a developed colony).** Lite has no command-line tools, so the colony was grown by a headless AI-only match on the installed desktop build (Globulation 2 0.11.7.0 + 15 commits, revision `5bf966285aa8`, `/Applications/Glob2.app`; same save format, version 219, as 0.11.8.2), using only AIs that lite ships (Maxima and the JavaScript AIs are compiled out of lite):
   ```sh
   glob2 map generate crater-lakes --seed 2102 --width 128 --height 128 --teams 4 --output crater-lakes-2102.map
   GLOB2=/Applications/Glob2.app/Contents/MacOS/glob2 assets/storefront/captures/desktop/tools/run-match.sh \
     matches/crater-lakes crater-lakes-2102.map.gz 3102 48000 6000 cortex cabino cortex cabino
   ```
   Crater lakes is one of lite's random-map landscapes (the generator list is identical in 0.11.7.0 and 0.11.8.x). The 4-colony map is 128×128.
2. **Seat.** A local player was added to the red colony (team 0) of checkpoints 36,000 and 42,000 with the storefront tool `assets/storefront/captures/desktop/tools/join-seat.py IN OUT 0 --rename cortex=Cortex --rename cabino=Cabino`. Map, units and AI state are untouched.
3. **Lite takes.** `tools/record.js` serves nothing itself: the lite package is served by the game repository's `platforms/web/serve.py` (port 8791), and Playwright's Chromium (`playwright` 1.63, headless, `--use-angle=metal`) opens it. `tools/session.js` writes three preferences (`graphicsDetailAdaptive=0`, `clouds=0`, `cloudShadows=0`: the clouds-off setting the desktop captures and trailer also used), reloads, copies the seat save into the game's own save folder and opens it through **Load game**, then presses `I`. The lite build then simulates and draws the match from that save at normal speed (30 ticks a second). `record.js` zooms with the game's `+` button, centres the camera with a minimap click, waits 3 s, and records the canvas with `canvas.captureStream(60)` and `MediaRecorder` (VP9 for the square takes, H.264 for the others, 120 Mbit/s). The canvas holds only the game's drawing, so there is no cursor. Window sizes: 2122×1200 (16:9 takes), 1282×1740 (2:3 takes), 1282×1200 (square takes), at device pixel ratio 1, so map pixels are the lite build's own.
   ```sh
   NODE_PATH=<a node_modules with playwright 1.63> node tools/record.js SAVE OUT.webm W H FX FY ZOOM_CLICKS SECONDS
   ```
   Takes were recorded one at a time; runs in parallel dropped frames and were discarded. Recorded frame rates: 16:9 about 50 fps, 2:3 and square 51–60 fps.
4. **Edit.** `uv run --with pillow python assets/portal-art/tools/build.py` crops each take to the map view (below the top bar and event list, left of the 200-px panel), cuts and joins the shots, resamples to constant 30 fps (CrazyGames) or 60 fps (Poki), adds the title layer to the CrazyGames openings, encodes H.264 High, CRF 17, yuv420p, BT.709, `+faststart`, no audio track, and writes the stills and `manifest.json`. The wordmark is the key-art script's treatment of the game's `content/data/gfx/menu-wordmark.png` (imported from [`../storefront/key-art/build-assets.py`](../storefront/key-art/build-assets.py)), always downscaled.

Raw takes, the seat saves, the map, the two checkpoints and the match result are kept with the renders (`takes/`, `saves/`), not in Git.

## Needs a human eye

- **The Poki thumbnail is a busy colony, not one subject.** Poki asks for one clear foreground object. At 195 % the frame centres on a Swarm with hospitals, inns and a few dozen globs; at 200 px it reads as a red colony on grass, but a reviewer may want a tighter subject. A tighter frame needs a closer zoom (more upscaled, grainier lite sprites) or a new take.
- **The scenes are peaceful.** Lite has no Maxima, and the Cortex and Cabino colonies in the scanned matches (Crater lakes, Coral, Marchland) are thinner than the desktop footage and produced no large fights in view of a seat. The previews show a developed, busy colony and warriors, not a battle. Lime rivals appear only at the edge of shot 2.
- **Shots 1 and 2 of the CrazyGames previews frame the same part of the colony** 3 min 20 s apart; shot 3 is a different quarter.
- **Clutter that is really in the game.** The red AI's clearing-zone outlines (red squares over the wheat) are in view; the desktop captures erased them over MCP, which lite does not have. Fog of war dims unseen land in blocky patches. Event messages are cropped out.
- **Phone-size check.** Covers were checked at 960, 540 and 200 px wide, not on a real portal tile.
- **Ads claim.** Nothing in the art says "No ads" or "Free".

## Reproduce

Serve `browser-release-lite` of run 45902410410 on 127.0.0.1:8791 with `platforms/web/serve.py`, then run `record.js` with the arguments in the manifest's `takes` for each of the nine takes, put them in `../storefront-v2-renders/portal-art/takes/`, and run `build.py`. A new recording is equivalent, not identical: the AIs keep playing and frame timing depends on the machine. The edit from the existing takes is deterministic.
