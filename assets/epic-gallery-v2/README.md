# Lava Shield gallery media

[Epic page preview](../epic-page-preview/README.md) · [Store asset brief](../../planning/store-assets-v1.md) · [Capture manifest](capture-manifest.json)

Prepared **2026-10-26** in response to the request for a gallery that shows more of Glob2's terrain, maps and strategic space. These images are actual game-renderer exports of a freshly generated **Lava Shield revision 7** map, seed 713, 256×256 tiles, four colonies and four initial workers per colony. They contain no generated or painted game graphics.

## Review files

| File | Dimensions | Role |
| --- | --- | --- |
| [Terrain view](lava-shield-terrain.jpg) | 2560×1440; under 4 MB | A wide crop showing the crater circuit, lava flows, crossings, colony approaches and coastal context. |
| [Complete map](lava-shield-map.jpg) | 2560×1440; under 4 MB | The whole map, reduced to 1440×1440 and centered with dark side margins. Preserve this framing when explaining the whole layout. |
| [Native render](lava-shield-current-map.png) | 4096×4096 | Unaltered source output for inspection and future crops; exceeds Epic's 4 MB carousel limit and is not a direct upload. |

Use **one** Lava Shield image for the terrain/map role. The two exports are alternative framings of the same map, not two different gameplay moments. Suggested gallery label: **Lava Shield**. The full-map image demonstrates geography, not the game's strategic-overview interface.

## Source and treatment

The existing native executable reported 0.11.4.0, compiled 2026-10-26 20:55, save format 186 and protocol 72. Its exact executable hash, generation parameters, input-map hash, commands and export hashes are in the [manifest](capture-manifest.json). A matching source commit for that executable was not established. No source code or pre-existing map/save was edited.

Generation used the supported `map generate lava-shield` command. Rendering used `map render` at a 4096-pixel maximum side. That mode exports the complete flat world with **fog disabled, animation frozen and no HUD**. This is genuine game imagery, but it is not a captured normal player view, an active match or a strategic-overview UI screenshot.

The terrain export crops the source at `(0, 896, 4096, 3200)` and downsamples to 2560×1440. The complete-map export downsamples the whole source and adds dark side margins. JPEG quality is 96; no objects, resources, unit counts or terrain were changed. Artwork remains subject to the project's existing [asset provenance and notices](../../facts/assets.md).

## Battle and current-build gaps

Preserved Lava Shield and Four Squares games were also inspected. Their unit counts did not produce a clear large-battle image. The conspicuous purple/green clusters in the sea were verified as **algae resources**, not armies, and were rejected as battle evidence. Older renders also contained a central black artifact that is absent from this revision-7 map.

No large-battle screenshot is supplied by this pack. Capturing a large battle and the actual strategic-overview interface remains separate work. These files also do not qualify the Epic Windows build or its map configuration. Rejected inspection renders, raw local replays and private save data are not part of the delivered pack.
