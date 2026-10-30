# Native battle and strategic-view captures

[Epic preview](../epic-page-preview/README.md) · [Lava Shield map media](../epic-gallery-v2/README.md) · [Capture manifest](capture-manifest.json)

Captured **2026-10-27**. These images show a deliberately authored skirmish in the actual native game: two forces of 96 warriors converge and fight on Lava Shield, while four compact colony groups supply geographic context. They are **staged scenario captures**, not an organic player match or evidence of natural colony growth, typical match pacing, or a qualified Epic Windows release.

## Delivery files

| Image | Dimensions | What it shows |
| --- | --- | --- |
| [Battle](lava-shield-battle.jpg) | 2560×1440; under 4 MB | Opposing forces in actual contact, with native unit sprites, health bars, minimap and spectator controls. |
| [Strategic view](lava-shield-strategic.jpg) | 2560×1440; under 4 MB | The actual zoomed-out strategic interface: terrain palette, warrior markers, colony-purpose icons and territory wash. |
| [Battle native source](lava-shield-battle-native.png) | 2940×1626 | Lossless source frame, preserving the entire HUD. |
| [Strategic native source](lava-shield-strategic-native.png) | 2940×1626 | Lossless source frame, preserving the entire HUD. |

The JPEGs fit each full native frame into 2560×1416, with 12-pixel dark margins above and below. No HUD edge is cropped. JPEG quality is 96 with no chroma subsampling. There is no image-generated or painted gameplay, invented interface, replacement creature anatomy, or screenshot retouching.

## What was staged and what actually ran

The source was a freshly generated Lava Shield revision-7 map, seed 713, 256×256 tiles, four colonies and four workers per colony. A temporary native companion reused a completed 0.11.4.0 build's production objects. It called the same native authoring APIs used by the editor and SGSL to place:

- 192 level-1 warriors, split into two opposing forces of 96;
- two ordinary war flags directing those forces toward contact;
- one inn, school, racetrack and hospital near each original hive;
- 24 additional workers near each colony.

Terrain and resources were not painted or replaced. The ordinary `Game::step` simulation then advanced 192 times. At the captured step, 39 warriors were in the native attacking-target movement state and total warrior health had fallen from 48,000 to 47,624. The [metrics](simulation-metrics.csv) record this progression; damage and attack animations were not injected for the image.

Both frames were drawn through the actual `GameGUI` and immutable Scene renderer. The battle uses 80% zoom. The strategic frame uses the native adaptive overview, labeled 16% by the interface; it is a populated wide view, not a claim that the whole toroidal world fits. Fog and flags were hidden through the existing spectator presentation options. The native HUD's `0.0` snapshot label is preserved and is not a performance measurement.

## Reproduction and provenance

[capture-scene.cpp](capture-scene.cpp) preserves the authoring, simulation and native drawing code. The public copy takes the asset directory from `GLOB2_MARKETING_ASSET_DIR` instead of embedding the local path used during capture. This is the only portability adaptation; the captured translation-unit hash, capture-binary hash, completed-game binary hash, input-map hash and output hashes are retained in the [manifest](capture-manifest.json).

The companion was compiled and linked in temporary directories against the completed `overview-icon-order` build, replacing only the application's main object. No shared game source or build directory was edited. The game build reported 0.11.4.0, compiled 2026-10-26 20:55, save format 186 and protocol 72; an exact matching source commit was not established.

The source map can be regenerated with that compatible runtime:

```sh
glob2 map generate lava-shield --seed 713 --width 256 --height 256 --teams 4 --workers 4 --output MAP
```

After building the companion against the corresponding completed native game objects and libraries, run it with an isolated profile, `GLOB2_MARKETING_ASSET_DIR` pointing to the game's data directory, and `MAP OUTPUT_DIRECTORY` arguments. It saves initial/captured native states and simulation metrics before taking the real frames. Native screenshot output is BMP; the retained PNG conversion preserves its RGB pixels. Raw temporary saves, machine-specific link commands and private local replays are not committed.

Artwork remains governed by the project's [source provenance and notices](../../facts/assets.md). The helper source is GPL-3.0-or-later, as identified in its SPDX header. Parent review accepted these frames for the working local gallery; publication, user approval and Epic Windows qualification remain separate.

## Closer Lava Shield terrain view — 2026-10-30

The [terrain-in-use image](lava-shield-terrain-in-use.jpg) replaces the full-map gallery entry after the user approved the other imagery and requested a closer view. It shows the lava ford, terrain/resource detail, a colony and its workers, with the edge of the opposing forces in view. The [native PNG](lava-shield-terrain-in-use-native.png) preserves the complete 2940×1634 frame; at 5.28 MB it is an inspection source, not a direct Epic carousel upload.

This is a camera/presentation variant of the same authored scenario: 192 native simulation steps, 192 warriors, 39 attacking and 47,624 total warrior health. The regenerated initial-state and metrics hashes match the original capture. The camera centers at tile (174,100), uses 40% zoom and disables the existing adaptive-detail setting so the normal terrain, building and creature sprites remain visible. Fog, flags and areas remain hidden through native spectator options. No terrain, resources or staged populations were changed.

The 2560×1440 JPEG retains the complete HUD, resizing the source to 2560×1423 with 8 pixels above and 9 below; it is under 4 MB. The original battle, strategic view and their source images remain byte-identical. [capture-terrain-scene.cpp](capture-terrain-scene.cpp) retains the temporary companion variant, with the same asset-directory portability adaptation described above; exact source, binary, state and output hashes are in the [manifest](capture-manifest.json). All original staged-scene and runtime limits apply.
