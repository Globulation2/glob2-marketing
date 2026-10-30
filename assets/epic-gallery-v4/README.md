# River battle capture

[Epic preview](../epic-page-preview/README.md) · [Earlier Lava Shield captures](../epic-gallery-v3/README.md) · [Manifest](capture-manifest.json)

Captured **2026-10-30** after the user requested another map and different team colours for the large-army battle image. The [delivery JPEG](river-battle.jpg) shows two native warrior formations converging beside a colony and resource fields on **River revision 5**, seed 713. Blue and gold/yellow are native team hues, 210° and 55°; no image recolouring was used.

The JPEG is 2560×1440 and under 4 MB. The [native PNG](river-battle-native.png) retains the full 2940×1634 frame. Delivery downsizes the whole frame to 2560×1423 and adds 8 dark pixels above and 9 below; no HUD edge is cropped. The native source is for inspection, not a separately qualified Epic upload.

## Authored scenario and real simulation

This is a deliberately staged in-engine skirmish, not an organic match. The supported generator created a 128×128 map with two colonies and four initial workers each. A temporary native companion used ordinary editor/SGSL production APIs to place two forces of 96 level-1 warriors, two war flags, four economic buildings per colony and 24 additional workers per colony. Warrior placement selected legal free grass around two opposing formations; terrain and resources were not painted or cleared.

The real simulation advanced 192 steps. At capture, all 192 warriors remained alive, 32 were actively attacking and combined warrior health had fallen from 48,000 to 47,672. [Metrics](simulation-metrics.csv) record the progression; damage and attack animations were not injected. The actual GameGUI/Scene rendered the 80% view with native sprites, health bars, minimap and spectator controls. Fog, flags and area overlays were hidden with native spectator options. The preserved HUD snapshot label is not a performance measurement.

## Reproduction and limits

[capture-scene.cpp](capture-scene.cpp) preserves the temporary companion. As with the earlier pack, it links the completed native build’s production objects and matching libraries while replacing only the application main. No game source or shared build directory was edited. The public source uses `GLOB2_MARKETING_ASSET_DIR` instead of a local absolute asset path; comments and whitespace are normalized. The [manifest](capture-manifest.json) records original translation-unit, companion, map, state and output hashes, plus map parameters and staging details. Run with an isolated profile and `MAP OUTPUT_DIRECTORY` arguments.

The runtime reported 0.11.4.0, compiled 2026-10-26 20:55, save format 186 and protocol 72; an exact matching source commit was not established. This is not Epic Windows qualification, player research or permission to publish. Existing approved colony, strategic, terrain and cover imagery remain unchanged. Source art remains governed by the project’s [provenance and notices](../../facts/assets.md); the helper retains its GPL-3.0-or-later SPDX header.
