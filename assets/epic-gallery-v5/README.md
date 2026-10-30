# Four Squares mid-game strategic view

[Epic preview](../epic-page-preview/README.md) · [Capture manifest](capture-manifest.json) · [Simulation summary](simulation-summary.json)

Captured **2026-10-30** to replace the early Lava Shield strategic view with a different map and a developed position. The [delivery JPEG](four-squares-midgame-strategic.jpg) shows the actual native adaptive strategic interface, centered on two developed colonies in **FourSquares1**. Building-purpose icons, territory wash and army markers are ordinary game presentation. It is a partial view of the toroidal map, not a whole-world export.

## Genuine AI-developed position

This is an unmodified position from a new four-player **Cortex AI** match on the existing 128×128 map. The supported headless runner advanced the match to **25,000 ticks**, approximately 13 minutes 53 seconds of simulation. All four colonies remained alive and the run stopped at its tick limit with no winner. The complete state contained **799 creatures: 181 workers, seven explorers and 611 warriors**, with **64 physical buildings**, including ten construction sites. Native object enumeration counted 83 building objects when virtual flags were included. The [summary](simulation-summary.json) retains per-team counts.

No units, buildings, resources or attack states were added for the screenshot. The match developed through normal AI orders and simulation. This differs from the deliberately authored [River battle](../epic-gallery-v4/README.md) and [Lava Shield scene](../epic-gallery-v3/README.md). It is an AI-match example, not evidence of human playtesting, typical match balance or a qualified Epic Windows release.

The match was run with a compatible completed native 0.11.4.0 executable, compiled 2026-10-26 20:55, using save format 186. A matching source commit was not established. The command, from the game repository with an empty output directory, was:

```sh
glob2 game run --map-file maps/FourSquares1.map.gz --game-seed 714 \
  --player cortex --player cortex --player cortex --player cortex \
  --ticks 25000 --save every:12500 --save final \
  --output-dir OUTPUT_DIRECTORY --data-dir data --compute-threads 4
```

## Native capture and delivery

[capture-strategic-scene.cpp](capture-strategic-scene.cpp) loads the saved match read-only and draws it through the actual `GameGUI` and immutable Scene renderer. The temporary companion was compiled against the completed game's production objects, replacing only its main entry point. No shared game source or build files were changed.

The native camera centers at tile (32,64). A requested 20% zoom is clamped by the ordinary minimum for this map/window; the interface correctly displays **32%**. Adaptive detail is enabled. Fog, area overlays and flags are hidden through existing spectator settings. Clouds and their shadows are disabled. The native HUD and its `0.0` snapshot label remain intact; that label is not a performance measurement.

The [native PNG](four-squares-midgame-strategic-native.png) is a lossless conversion of the renderer's 2940×1634 BMP. The 2560×1440 JPEG fits the complete frame to 2560×1423, with eight dark pixels above and nine below, at quality 96 without chroma subsampling. It is under Epic's 4 MB carousel limit. No cropping, painted game content, AI imagery, recolouring or screenshot retouching was applied.

Reproduction uses the corresponding completed engine objects and libraries, `GLOB2_MARKETING_ASSET_DIR` pointing at the game data directory, an isolated profile, and `SAVED_GAME OUTPUT_DIRECTORY` arguments. Machine-specific link commands, raw temporary saves and full benchmark output are excluded; their relevant hashes are retained in the manifest. The helper source carries GPL-3.0-or-later. Artwork remains subject to the project's [source provenance and notices](../../facts/assets.md).

Parent visual review accepted this frame for the local working gallery. Store publication and Windows release qualification remain separate. Other approved media were not changed.
