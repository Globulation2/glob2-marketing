# Desktop gameplay captures for storefront-v2 (round 3)

[Manifest](manifest.json) · [Gallery order](selection.json) · [Web exports](web-1920/manifest.json) · [Contact sheet](contact-sheet.jpg) · [Round-2 final review](../../review/round-2-final.md) · [Round-1 review](../../review/round-1-desktop-and-layout.md) · [Footage rule](../../../../planning/gameplay-video.md) · [Captions](../../../../translations/en.md) · [Tools](tools/)

Captured **2026-11-24** on macOS (Apple silicon) from **Globulation 2 0.11.7.0 + 15 commits (revision 5bf966285aa8), the installed build** at `/Applications/Glob2.app`; maps, AI roster and simulation identical to the v0.11.7.0 tag. It is not the public 0.11.7.0 release binary ([claims R13](../../../../facts/storefront-v2-claims.md); `glob2 info version` reports version 0.11.7.0, revision 5bf966285aa8; executable SHA-256 in [manifest.json](manifest.json)). Every frame is the game's own framebuffer at native pixels, saved through the game's built-in MCP server. Nothing is scaled, retouched or composited, except the one labelled side-by-side image (`08b`), which places a real game frame beside a rendering of the real MCP transcript of the same session, and the 1920×1080 web exports, which are plain reductions.

Round 3 is the fix round after the [round-2 final review](../../review/round-2-final.md): the spectator opponents frame is out of the gallery (M5), the gallery is reordered (M5), both co-play images come from new sessions that end on the agent's standing order acting (M4, S4), the provenance is corrected (M7), and 1920×1080 JPEG exports are added. Frames `01`–`06` are the round-2 files, unchanged (same SHA-256).

- **16:9 set:** 3840×2160 (a 1920×1080-point window on a 2× display). These PNGs (5–11 MB) are the Microsoft Store files.
- **16:10 set:** 2880×1800 (a 1440×900-point Retina window) for the Mac App Store, **at the same zoom as each 16:9 frame** (fewer tiles in view, same unit size). It is a separate run of the same recipe, so units and the moment differ in detail.
- **Web exports:** [`web-1920/`](web-1920/) holds 1920×1080 JPEGs of the gallery and of `08b` (see below), for Epic, Snap, itch.io, Steam and AppStream.
- The `keyart-*` plates belong to the [key art](../../key-art/README.md) and are not part of the gallery; their manifest entries are carried over unchanged. Only `keyart-foursquares-cabino-zoom150-3840x2160.png` (the concept B plate) is committed; the other four are round-1 plates superseded by [`key-art/plates/`](../../key-art/plates/) and are kept out of the repository ([`.gitignore`](.gitignore)), so their manifest entries are provenance only.

## Gallery (in `selection.json` order)

The order is the review's: hero, battle, build, co-play, maps, territory, economy. Build and economy (both on Coral) are never next to each other. **A store packager pairs each image with the caption of its role** (`caption_field` in `selection.json`, `shot_caption_<role>` in [translations/en.md](../../../../translations/en.md)), never with the slot number: the role, not the position, is what the caption describes.

| # | Role | Caption field | 16:9 · 16:10 · web | Map, seat | What is visible |
| --- | --- | --- | --- | --- | --- |
| 1 | hero | `shot_caption_hero` | [`01-hero-marchland-colony-under-raid-3840x2160.png`](01-hero-marchland-colony-under-raid-3840x2160.png) · [16:10](01-hero-marchland-colony-under-raid-2880x1800.png) · [1920](web-1920/01-hero-marchland-colony-under-raid-1920x1080.jpg) | Marchland, red colony (Maxima) | 100%. A large red colony (two swarms, about twenty inns and hospitals, wheat fields, hundreds of workers) with a purple rival's raid of roughly twenty warriors meeting as many red warriors at the colony's right edge; the purple swarm at the lower right. Game minute 18. |
| 2 | battle | `shot_caption_battle` | [`04-battle-honeycomb-oasis-3840x2160.png`](04-battle-honeycomb-oasis-3840x2160.png) · [16:10](04-battle-honeycomb-oasis-2880x1800.png) · [1920](web-1920/04-battle-honeycomb-oasis-1920x1080.jpg) | Honeycomb isle, red colony (Maxima) | 150%. Red and lime (Cortex) warriors clash on the oasis sand ring, hit flashes, the lime swarm on the dark hex at the right. No guard grid, no circles, no bars. **Top stat negative (see below).** |
| 3 | build | `shot_caption_build` | [`02-build-coral-school-site-3840x2160.png`](02-build-coral-school-site-3840x2160.png) · [16:10](02-build-coral-school-site-2880x1800.png) · [1920](web-1920/02-build-coral-school-site-1920x1080.jpg) | Coral, red colony (Maxima) | 150%. A School construction site the seat had just placed is selected: the panel shows "Level 1 (construction site)", the Working slider (4/8; 7/8) and the materials delivered (Wood 3/7, Algae 1/2). The game rings the workers assigned to it; they are walking in with wood and algae. |
| 4 | ai_coplay | `shot_caption_ai_coplay` | [`08-ai-coplay-in-game-coral-3840x2160.png`](08-ai-coplay-in-game-coral-3840x2160.png) · [16:10](08-ai-coplay-in-game-coral-2880x1800.png) · [1920](web-1920/08-ai-coplay-in-game-coral-1920x1080.jpg) | Coral, red colony (Maxima) | 150%. Pure in-game frame, taken right after the agent's last `hive_program inspect` (see below): the game's own Hive card for the standing order `frontline-flag` (Active, its latest output `{"enemies":17,"moved":[68,60]}`, Pause, Cancel) and the war flag that run had just moved, at the lake corner with red warriors along the shore and cyan and lime rivals coming in. 16:10: `{"enemies":4,"moved":[58,56]}`, the flag among red warriors south of the inns, a cyan rival close by. |
| 5 | maps | `shot_caption_maps` | [`06-maps-city-states-3840x2160.png`](06-maps-city-states-3840x2160.png) · [16:10](06-maps-city-states-2880x1800.png) · [1920](web-1920/06-maps-city-states-1920x1080.jpg) | City-states, cyan colony (Maxima) | 87.5%. Inside the ring city: hex-paved roads, a stone wall and moat, lava ground, wheat, and an active cyan colony (swarm, inns, schools, barracks, towers). |
| 6 | territory | `shot_caption_territory` | [`05-territory-crater-lakes-3840x2160.png`](05-territory-crater-lakes-3840x2160.png) · [16:10](05-territory-crater-lakes-2880x1800.png) · [1920](web-1920/05-territory-crater-lakes-1920x1080.jpg) | Crater lakes, red colony (Maxima) | 75%. The red forward swarm in a clearing, the purple rival's (Cortex) swarms, inns and hospitals in the forest at the left, and red warriors pushing across the wheat and grass between them, three crater lakes below. |
| 7 | economy | `shot_caption_economy` | [`03-economy-coral-inn-and-wheat-3840x2160.png`](03-economy-coral-inn-and-wheat-3840x2160.png) · [16:10](03-economy-coral-inn-and-wheat-2880x1800.png) · [1920](web-1920/03-economy-coral-inn-and-wheat-1920x1080.jpg) | Coral, red colony (Maxima) | 150%. An Inn selected: Working 1/1, Food 9/10 (16:10: 6/10), no warning line. The Swarm above it, more inns and hospitals, wheat fields on both sides with workers on them. |
| alt | ai_coplay (alternate to 4) | `shot_caption_ai_coplay` | [`08b-ai-coplay-side-by-side-coral-3840x2160.png`](08b-ai-coplay-side-by-side-coral-3840x2160.png) (16:9 only) · [1920](web-1920/08b-ai-coplay-side-by-side-coral-1920x1080.jpg) | Coral, red colony (Maxima) | **Game frame plus transcript of the same session, arranged side by side**; see below. Not in `selection.json`; it replaces `08` in slot 4 on itch.io, Snap and AppStream, which take a second panel without difficulty. |

Which co-play image goes where (from the review): Microsoft Store and Steam/GOG take `08` (pure game interface); itch.io, Snap and AppStream/Flathub take `08b`; Epic and the Mac App Store take neither until claims R8 and R7 clear; mobile stores never. Where a store shows five or fewer images, keep build and drop economy.

Every player-seat frame shares the colony with the AI that built it; the panels name the colony after it ("Inn (Maxima)").

**Removed: `07-opponents-marchland-spectator`.** The review dropped it (half open grass, no fight, lower-case AI names in the spectator panel). Both files were moved out of the repository to the session scratchpad (`desktop-r3/removed-from-gallery/`), with copies of the round-2 `08`, `08b`, manifest, selection, contact sheet and README. "8 computer opponents" stays in the description text, where it is true.

**Microsoft caption numbering.** `translations/platforms.json` maps Microsoft `desktop_screenshot_caption_1`…`_8` to the old order (hero, build, economy, battle, territory, maps, opponents, ai_coplay) and `asset_text.desktop_gallery_order` still lists that order. Both must follow this gallery: `desktop_gallery_order` = hero, battle, build, ai_coplay, maps, territory, economy, and captions 1–7 = `shot_caption_hero`, `_battle`, `_build`, `_ai_coplay` (keeping its `ai_coplay` condition), `_maps`, `_territory`, `_economy`, with no eighth caption. This folder does not own that file; the change is handed to the coordinator.

## Web exports (`web-1920/`)

`tools/web-export.py` writes a 1920×1080 JPEG of each gallery image and of `08b`: an exact half-size Lanczos reduction of the 3840×2160 master, RGB, no alpha, no ICC profile (untagged, that is sRGB, like the game's PNGs), 4:4:4 chroma, quality 95. Nothing else is changed. Each file and its source hash are in [`web-1920/manifest.json`](web-1920/manifest.json). All eight came out at quality 95, between 0.92 and 1.47 MB.

Store caps: Epic's 4 MB is met by every file. Snap's screenshot limit recorded in the storefront-v1 validator notes is 2,000,000 bytes per image (480×480 to 3840×2160, aspect 1:2 to 2:1; not re-checked on 2026-11-24, since the Snapcraft documentation pages tried were not reachable); every export (largest 1.47 MB) fits it. itch.io has published no screenshot size limit that this project has found. Keep the 3840×2160 PNGs for the Microsoft Store.

## Clean-state protocol and how each frame meets it

Applied to every frame (see `tools/scene.py` and, for the co-play frames, `tools/coplay-session.py`):

1. **Health and food bars off:** the in-game "toggle draw information" key (`I`, the desktop counterpart of the mobile *Health and food bars* lens) pressed after each load. With it off, no war-flag range circle is drawn.
2. **Zones:** the forbidden, clearing **and guard** areas in view are erased (as the player, Flags and areas tool, through `game_zone`) shortly before each frame; the frame is then measured for pure zone-outline colours (yellow, red, blue) and discarded if any remain. Every kept frame measures under 1 outline pixel per 10,000.
3. **Top bar:** frames are kept only while the first stat (workers free/total) is not negative, read from the game's own HUD control through `ui_inspect` before and after the frame. Exception: the battle frame, see below.
4. **Event list:** kept only while the list shows at most two rows (read the same way before and after the frame); a row can be fading in the saved frame. Exception: the 16:10 hero, see below.
5. **No hint text, no menus, no pause:** no palette item or tool is armed in any frame; normal speed (1×) at capture.
6. **Zoom:** multiples of 1/8 only (seam-free); lead and battle at 100% or closer.

| Frame | Bars | Zones, guard grid, circles | First stat as drawn (16:9; 16:10) | Event rows (16:9; 16:10) | Hint text | Black | Zoom |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 hero | off | none | 100/293; 98/302 | 2; **4** | none | 0.1% | 100% |
| 04 battle | off | none | **-9/175 (red); -9/175 (red)** | 2; 2 | none | 0% | 150% |
| 02 build | off | none | 37/135; 20/124 | 1; 2 | none | 0% | 150% |
| 08 ai_coplay | off | none | 27/146; 27/144 | 1; 2 | none | 0% | 150% |
| 08b (game half) | off | none | 28/145 | 2 | none | 0% | 125% |
| 06 maps | off | none | 47/225; 1/217 | 2 (one fading); 2 | none | 0.1% | 87.5% |
| 05 territory | off | none | 26/259; 33/266 | 2; 1 | none | 0% | 75% |
| 03 economy | off | none | 40/144; 32/126 | 1; 2 | none | 0.1% | 150% |

The stats and rows were read off each saved frame (and through `ui_inspect` before and after it); "black" is the share of pure-black pixels in the map area (`tools/check-frames.py`). No event row covers a subject: the list sits over terrain at the top left in every frame. Every frame was viewed at full size and at 600 px wide.

**Fog of war.** Player-seat frames show the seat's real fog: land the colony does not see at that moment is dimmed (lightly in the HD art). For frames shot after the measurement was added, the manifest records the share of sampled tiles in view outside the colony's sight (`fog_of_war_in_view`, a one-shot Hive read on a 3-tile grid; its `black` figure is the Hive's count of tiles not marked explored, which does not match what the frames show: the co-play frames read 30–40% there but have almost no pure-black pixels, so use the pixel measure in the table). The review's 15% target is not met by most player-seat frames; see "Not achieved".

## Which sprite is wheat

From the build's own data (`Glob2.app/Contents/Resources/data/resources/registry.json`, read 2026-11-24): resource `wheat` ("Wheat", material `food`, farmable) is drawn with frames 10–19 of `data/gfx/ressource`; the HD frames are `data/highres/v1/ressource10.webp` to `ressource19.webp`. They are **small round grains on the ground, scattered in loose clusters, ripening from green through yellow and orange to red** as the stock grows. They are *not* the tall pink and violet plants: those are `trees` (frames 0–9, wood). Cherry, orange and prune trees are dark blue-violet teardrop shapes with coloured fruit (frames 50–64). So in the economy and build frames, the red, orange, yellow and green dot clusters around the Inns are wheat fields, and the workers standing on them are harvesting.

Which building is which, for captions (from `game_world` positions matched to the frames): the **Inn** is the brown horseshoe-shaped building with two pink beds; the brown pot with a magenta top is the **hospital**; the tall red (or the colony's colour) crystal spires over a dome are the **Swarm**; a **war flag** is a pink-red star on the ground; an **exploration flag** is a red-outlined diamond.

## AI co-play: exactly how the two images were made

The desktop build has a built-in MCP server (`--mcp-port`). For each co-play image, one recorded session was run with [`tools/coplay-session.py`](tools/coplay-session.py) on the Coral map, seat on the red colony (the Maxima AI shares the colony and keeps playing it). Two clients talk to the game in that session:

- **The "agent" is a scripted MCP client, not a language model.** `coplay-session.py` makes the agent's calls through `agent-session.py`'s recorder, which appends every call, request and response, to a JSON Lines transcript (the token is replaced by `<token>`). **The standing order's JavaScript (`FRONTLINE` in [`tools/agent-session.py`](tools/agent-session.py)) was written by the capture engineer**, not generated in the session. The calls and the game's responses are real and are what any MCP agent's calls would get; no image or text should describe them as a model's decisions.
- **The capture tooling** (`scene.py`, `session.py`): loading the save, the bars key, zone erases, `game_time` polls to wait for the order's next run, `ui_inspect` reads of the HUD and the Hive card, `game_world` reads of the flags, and the screenshot. These calls are not in the transcript; they are listed under `player_actions_before_capture` and `coplay_session` in the manifest.

The agent's calls, in order, all real and all in the transcript:

1. `hive_status` (Hive available, session id);
2. `game_world` `detail: brief` (the colony's status);
3. `hive_program` `install` of a named standing order, `frontline-flag`, every 150 ticks: *"Keep one war flag on the enemy warrior nearest our buildings"*. It reads only the colony's fog-filtered view and returns ordinary player orders: create a war flag (12 warriors, radius 6) on the visible enemy warrior nearest the colony's buildings, then move it (`moveFlag`) when that enemy is more than 3 tiles away from it;
4. `game_view` (the camera on the front, at the frame's zoom);
5. `hive_program` `inspect frontline-flag`, once after each run of the order from its first run on. The first shows the flag being **placed** at tile 59,59 (orders sent: 1). The session stops at the first inspect that shows the order's latest run **moving** the flag (orders sent ≥ 1) at a moment when the frame passes the clean-state checks, the in-game Hive card shows the same output, and the moved flag is in view; the frame is taken right after that inspect. Earlier "moved" runs whose frame failed a check (more than two event rows, the flag under the card or off screen, the card already showing the next run) are in the transcript and their discarded frames are in the scratchpad.

The transcripts are in [`coplay-transcripts/`](coplay-transcripts/), one per image (the token is never recorded). In the manifest, `tick_at_capture` is read after the screenshot call returns; the frame itself was drawn earlier, between the last inspect's run and that tick (the file name of the source frame in the scratchpad carries the tick read just before the call).

- **`08-ai-coplay-in-game`** (3840×2160 and 2880×1800, two separate sessions): a pure in-game frame at 150%, centred on the front south of the colony's inns. The game's Hive card reads Active and the output of the run the last inspect reported (16:9 `{"enemies":17,"moved":[68,60]}`; 16:10 `{"enemies":4,"moved":[58,56]}`), and the order's war flag stands at that tile: in 16:9 at the right-hand corner of the square lake, red warriors along the shore, cyan and lime rival warriors coming in; in 16:10 among red warriors south of the inns, a cyan rival close by. The other war-flag stars in view are the colony AI's own flags (16:9: tiles 54,65 and 63,57; 16:10: 57,60 and 56,63; listed by `game_world` just before the frame). The 16:9 session ran before the card check also read the card after the frame; the card in the saved frame was checked by eye and shows the inspected output. Transcripts: 16:9 has 8 calls (four inspects: placed [59,60], then moved [42,70], moved [64,55] and moved [68,60]; the frames after the first two moves failed a check: flag off screen, zone outlines, more than two event rows), 16:10 has 9 (five inspects: placed [59,59], holding twice (the second repeated a run that had not finished), moved [69,60] (the card changed before the frame was saved, so it was discarded), moved [58,56]). No second application is shown, so it is the candidate for the Microsoft Store, Steam and GOG.
- **`08b-ai-coplay-side-by-side`** (16:9 only): **game frame plus transcript of the same session, arranged side by side.** The left 2560×2160 is a native frame from a game window launched at 2560×2160 (a 1280×1080-point window), 125%, taken right after the session's last inspect. The game's Hive card reads `{"enemies":9,"moved":[63,59]}` and the order's war flag stands at tile 63,59 among red warriors on the sand at the top of the square lake, a cyan rival warrior beside it. The right 1280 px is a plain monospace panel rendered by `tools/coplay-side-by-side.py --all` from that session's transcript: every call in order (`hive_status`, `game_world`, `hive_program install`, `game_view`, the first `inspect` showing `placed [59,59]`, orders sent 1), then one dimmed line standing for the next four inspect calls ("… 4 more hive_program inspect calls (runs at ticks 36337–36645): holding, moved …"; one of the four repeated a run that had not finished), and last the inspect of the run at tick 36,798: `moved [63,59]`, orders sent 1, which is the moment of the frame. It is not a screenshot of a terminal window, no third-party agent product or logo appears, and nothing private (no path, user or token) is in it. This session ran an earlier revision of `coplay-session.py` whose checks were ordered differently (zones erased and the HUD read right after the inspect, the card read after the frame); the agent's calls were the same. A second war-flag star in the game half, at tile 59,58, is the colony AI's own flag (id 10; `game_world` listed it there at tick ~36,690), not the agent's.

## Not achieved, and why

- **Battle top stat.** The `04-battle` scene could not be captured with a non-negative first stat: the red colony (Maxima AI) had more jobs than idle workers for the whole fight (from -7 to -67 between ticks 66,000 and 70,000), and from the lime colony's seat the oasis is under fog. A headless sweep of all 33 matches found no larger clash among the colonies whose stat stays positive. The review accepted the frame. An alternative positive-stat clash (Lava shield, cyan seat, 137.5%, about a dozen warriors a side) is in the scratchpad (`desktop-r2/cand/battle-lava-45604.png`) but is weaker.
- **Event rows in the 16:10 hero.** In two 16:10 runs of the hero recipe, no moment of the raid had two or fewer rows. The 16:10 twin shows the raid with four rows; the 16:9 hero has two (review N5, not redone this round).
- **Placement preview in the build frame.** In the desktop interface, selecting a construction site replaces the build palette in the side panel, so a selected site and an armed palette item cannot be on screen together.
- **Fog of war under 15%.** Not met for most player-seat frames: wherever a frame shows rival land or open water, the seat's colony does not see all of it, and the game dims it. The dimming is light in the HD art.
- **Water in the co-play frames.** Coral is an island map; even at 125–150% centred on the front, the square lake and the lagoon at the left take about a fifth (open blue water is 23.5% of the 16:9 map area, 18.5% of the 16:10 and 20% of the `08b` game half by a colour count, against 31% in the round-2 `08`) of the co-play frames (review S4 asked for under a quarter). The black unexplored tile of the round-2 `08` is not in the new frames.
- **Battle size in the hero.** About twenty warriors a side, estimated by eye; the game gives no per-frame count.
- **Map variety.** Five maps across seven gallery images (Marchland, Coral, Honeycomb isle, Crater lakes, City-states). Coral carries build, economy and co-play because its colony keeps a positive stat and a quiet event list.
- **Co-play side-by-side at 16:10** was not made (the Mac App Store holds co-play until claims R7 clears).
- **The Hive card's output line is raw JSON** (product issue, review N6).

## Round-1 and round-2 frames

All fifteen round-1 finalists (and their 16:10 twins) were moved to the session scratchpad (`desktop-r2/superseded-round1/`). The round-2 `07` frames and the round-2 `08`/`08b` files are in `desktop-r3/removed-from-gallery/`. Nothing was deleted.

## How the frames were made

- **Build:** Globulation 2 0.11.7.0 + 15 commits (revision 5bf966285aa8), the installed build at `/Applications/Glob2.app` (executable SHA-256 in [manifest.json](manifest.json)).
- **Window:** off-screen with SDL's dummy video driver, `--renderer portable-sdl`, `--ui-scale 2`, a fresh profile for every game instance, HD artwork forced on (`highResolutionArtworkChoice=on`), clouds and cloud shadows off, MCP server on port 47815.
- **Matches:** the round-1 headless all-AI matches (`glob2 game run`, [tools/matches.json](tools/matches.json)); a local player seat joined to one colony with [tools/join-seat.py](tools/join-seat.py). The seat shares the colony with its AI, which built it; panels name the colony after that AI ("Inn (Maxima)").
- **Choosing moments:** a headless sweep of every checkpoint gave each colony's free-worker balance, to find colonies whose top-bar stat is positive; `tools/scan2.py` then fast-forwarded candidate seats and scored clash and colony-mix windows from the seat's own view (Hive read, no orders).
- **Player actions:** listed per file in the manifest (`player_actions_before_capture`): bars off, zone erases, and for build, economy and co-play the placement, selection or standing order described above. In the 16:9 build session only, the seat had placed three earlier test sites (a school at 66,21 and an inn at 68,21, which the colony finished and which stand just left of the selected site, and a school at 60,30). The co-play war flags were placed and moved by the standing order; the colony's AI places and moves war flags of its own as well.

## Reproduce

```sh
S=$SCRATCH   # the session scratchpad holding desktop-capture/ (round 1), desktop-r2/ and desktop-r3/
T=assets/storefront-v2/captures/desktop/tools
export GLOB2_MCP_PORT=47815 GLOB2_MCP_TOKEN_FILE=$S/desktop-r3/mcp-token
export CAPTURE_MATCHES=$S/desktop-capture/matches CAPTURE_WORK=$S/desktop-r3/work

# frames 01-06: round 2, see tools/round2-batch.sh (16:9 and 16:10 sets)

# co-play: one fresh game instance and one recorded session per image (quit the game between them)
export CAPTURE_PROFILE=$S/desktop-r3/profile-2560d; $T/launch-capture-game.sh $CAPTURE_PROFILE 2560x2160 2 47815 &
uv run --with pillow --with numpy python $T/coplay-session.py $S/desktop-r3/s2560d 63 60 1.25
uv run --with pillow python $T/coplay-side-by-side.py $S/desktop-r3/s2560d/ai-coplay-coral-<tick>.png \
  $S/desktop-r3/s2560d/coplay-transcript.jsonl $S/desktop-r3/s2560d/sbs.png --all
export CAPTURE_PROFILE=$S/desktop-r3/profile-3840d; $T/launch-capture-game.sh $CAPTURE_PROFILE 3840x2160 2 47815 &
uv run --with pillow --with numpy python $T/coplay-session.py $S/desktop-r3/s3840d 62 61 1.5
export CAPTURE_PROFILE=$S/desktop-r3/profile-2880b; $T/launch-capture-game.sh $CAPTURE_PROFILE 2880x1800 2 47815 &
uv run --with pillow --with numpy python $T/coplay-session.py $S/desktop-r3/s2880b 62 61 1.5

# copy the chosen frames and transcripts; write manifest, selection, contact sheet; then the web exports
SCRATCH=$S uv run --with pillow python $T/finalize2.py $T/final-round3.json . $T/keyart-entries.json
uv run --with pillow python $T/web-export.py .
```

A session waits for the standing order to move its flag at a clean moment, so a re-run gives an equivalent but not identical frame: the match diverges with every order and with the machine's speed.

## Tools

| File | Purpose |
| --- | --- |
| [tools/coplay-session.py](tools/coplay-session.py) | Round 3: one recorded co-play session that ends on the standing order moving its flag, with the frame taken at that moment |
| [tools/agent-session.py](tools/agent-session.py) | The transcript recorder and the `frontline-flag` standing order (written by the capture engineer) |
| [tools/coplay-side-by-side.py](tools/coplay-side-by-side.py) | Game frame beside the transcript panel (`--all`: every call, middle inspect runs collapsed into one labelled line) |
| [tools/finalize2.py](tools/finalize2.py), [tools/final-round3.json](tools/final-round3.json), [tools/keyart-entries.json](tools/keyart-entries.json) | Copy chosen frames and transcripts; write manifest, selection and contact sheet; the round-3 choices with descriptions and caption checks; the key-art entries carried over |
| [tools/web-export.py](tools/web-export.py) | The 1920×1080 JPEG exports and their manifest |
| [tools/round2-batch.sh](tools/round2-batch.sh), [tools/final-round2.json](tools/final-round2.json) | The round-2 recipes and choices (frames 01–06 are still these) |
| [tools/scene.py](tools/scene.py) | Load a seat, bars off, run to a tick, frame, erase zones, check HUD and zone outlines, hunt for clean frames, fog read |
| [tools/build-shot.py](tools/build-shot.py) | Place a site, set its workers, select it (or arm a palette item) and shoot |
| [tools/spectator.py](tools/spectator.py) | Spectator-view frames (no fog), used for the removed opponents frame |
| [tools/scan2.py](tools/scan2.py) | Clash and colony-mix scan from a seat |
| round-1 tools | `capture.py`, `recipes.json`, `selection.json` (round-1 finalize input), `join-seat.py`, `launch-capture-game.sh`, `run-match.sh`, `check-frames.py`, `finalize.py`, `explore.py`, `battle-scan.py`, `crop-keyart.py`, `mcp.py`, `session.py` |

Helper scripts are `GPL-3.0-or-later`, like the game. Candidates, discarded frames and session state are in the scratchpad under `desktop-r2/` and `desktop-r3/`, outside the repository; a reboot can clear it.
