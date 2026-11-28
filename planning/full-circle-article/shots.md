# Full Circle Magazine article: shot list

[Planning index](../README.md) · [Article draft](article.md) · [FCM house style](../../analysis/full-circle-ubuntu-games-style.md) · [Desktop captures and their provenance](../../assets/storefront/captures/desktop/README.md) · [Footage rule](../gameplay-video.md)

Prepared 2026-11-27. FCM's Ubuntu Games articles usually carry four screenshots (two to five seen), placed about one per page, and **print no captions** ([house style](../../analysis/full-circle-ubuntu-games-style.md#synthesis)). The captions below are optional: they can go in the email to the editor or be dropped. The article marks each image's place with a standalone `[Image: file name]` paragraph, which is how FCM asks for placement.

All images are real game frames ([real game art only](../../AGENTS.md#real-game-art-only)), and the gameplay shots follow the [footage rule](../gameplay-video.md): developed colonies, visible activity, no empty terrain.

## Shots

| # | Submission file | Source | What it shows | Where it goes | Optional caption |
| --- | --- | --- | --- | --- | --- |
| 1 | `glob2-01-colony-under-raid.jpg` | Existing: [`web-1920/01-hero-marchland-colony-under-raid-1920x1080.jpg`](../../assets/storefront/captures/desktop/web-1920/01-hero-marchland-colony-under-raid-1920x1080.jpg) | Marchland, game minute 18: a large red colony (two Swarms, about 20 Inns and Hospitals, wheat fields, hundreds of workers) meeting a purple raid of about 20 warriors at its right edge | After the opening hook | A developed colony on Marchland fends off a raid. Nobody is clicking these units: the globs pick their own jobs. |
| 2 | `glob2-02-introduction-lesson.jpg` | **New capture needed** (see below) | The Introduction lesson in progress, with its goal and the colony visible | End of "The tutorial" | The Introduction teaches the idea in five goals and about 10 minutes. |
| 3 | `glob2-03-inn-and-wheat.jpg` | Existing: [`web-1920/03-economy-coral-inn-and-wheat-1920x1080.jpg`](../../assets/storefront/captures/desktop/web-1920/03-economy-coral-inn-and-wheat-1920x1080.jpg) | Coral: an Inn selected (Working 1/1, Food 9/10), the Swarm above it, more Inns and Hospitals, wheat fields on both sides with workers harvesting | Early-decision section, after the paragraph on hunger and Inns | An Inn's panel shows its food stock and how many workers keep it supplied. The coloured dots are wheat. |
| 4 | `glob2-04-school-site-working-slider.jpg` | Existing: [`web-1920/02-build-coral-school-site-1920x1080.jpg`](../../assets/storefront/captures/desktop/web-1920/02-build-coral-school-site-1920x1080.jpg) | Coral: a School construction site selected; the panel shows "Level 1 (construction site)", the Working slider and materials delivered (Wood 3/7, Algae 1/2); the assigned workers are ringed, walking in with wood and algae | Early-decision section, just before the paragraph on Working and priority | The Working slider sets how many workers a building asks for. These are walking in with wood and algae for a new School. |
| 5 (optional) | `glob2-05-battle.jpg` | Existing: [`web-1920/04-battle-honeycomb-oasis-1920x1080.jpg`](../../assets/storefront/captures/desktop/web-1920/04-battle-honeycomb-oasis-1920x1080.jpg) | Honeycomb isle: red and lime warriors clash on the oasis sand ring, the lime Swarm at the right | Before "Where to go next" | Warriors from two colonies clash on Honeycomb isle. |

If FCM wants four images, drop shot 5. If shot 2 can't be captured in time, use shot 5 in its place and move it up to the tutorial section's slot, or use the optional terminal shot below.

Not used: the AI co-play frames (`08`, `08b`). The article gives MCP one sentence only; add `08` (pure game interface) only if that paragraph grows. Shot 5's top bar shows a negative free-workers figure (the colony had more jobs than idle workers during the fight; see the [capture notes](../../assets/storefront/captures/desktop/README.md#clean-state-protocol-and-how-each-frame-meets-it)). It is harmless in a battle shot but don't use it to illustrate the feeding advice.

## Provenance the editor should know

- Shots 1, 3, 4 and 5 were captured on 2026-11-24 on **macOS**, from Globulation 2 0.11.7.0 plus 15 commits (revision `5bf966285aa8`), not from the 0.11.8.1 Linux build the article describes. Maps, AI and simulation match the 0.11.7.0 tag, and the game looks the same on Linux, but an Ubuntu-focused magazine may prefer Ubuntu captures. Either say so to the editor, or recapture the same scenes on Ubuntu with 0.11.8.1 (the scene tools are in [`captures/desktop/tools/`](../../assets/storefront/captures/desktop/tools/)).
- All of them show colonies played by the game's own AI (Maxima, with Cortex and others as rivals), from a seat that shares the colony with the AI. They are not a human's match. If a caption is used, don't call it "my colony"; "a colony" is accurate.

## New capture: shot 2, Introduction lesson

- **Build and platform:** Globulation 2 0.11.8.1 on Ubuntu (record the version and the installation route: Snap or Flatpak), so the article's one Ubuntu-native frame is from the build it describes. Record date, Ubuntu version, package, window size and desktop scale with the file.
- **Window:** 1920×1080 windowed or full screen, game zoom at 100% or closer so globs and buildings read at 800 px wide.
- **How to reach it:** main menu → Tutorial → Tutorial lessons → Introduction (or accept the first-run "Start introduction" offer on a fresh profile).
- **Moment to capture:** during goal 2 or 3 ("Build another Inn" / "Supply your new Inn"), once the new Inn site is placed and workers are carrying wood or wheat to it. The current goal text must be readable, and the frame should show the existing Inn, the Swarm, wheat and moving workers. Avoid the opening seconds, before anything moves.
- **Must not show:** a menu or dialog covering the map, the "Help / why?" text panel open over the colony, or mostly empty terrain or fog. This is an editorial walkthrough, so the lesson's on-screen goal is fine, but it is a UI-plus-gameplay frame. Don't reuse it as a store gameplay screenshot.
- **Fallback:** the Custom game setup screen (Map / Players & Teams / Game Rules, with Gentle and Numbi - Easy selected) can illustrate "Your first solo match". It is a menu screen, so the footage rule bars it from store media. Here it would be an explicitly labelled interface shot, used only because the article is a walkthrough.

## Optional Ubuntu-specific shot: installing from the terminal

An Ubuntu terminal running `sudo snap install globulation2` (or the Flatpak `flatpak install --user ./glob2.flatpak` step), with the completed output visible, captured on the tested Ubuntu machine. FCM's games section rarely shows commands, so this is a spare and not part of the four. Crop out the username, hostname and any personal paths, or use a clean demo account.

## Export recipe

From each 1920×1080 web export (or the new capture), make an RGB JPEG **800 px wide** (800×450 for 16:9) with a high-quality resample (Lanczos) and **low compression** (quality 92–95), with no other edits. 800 px meets both the style guide's 800 px and the issues' 1,200 px limits. Example with ImageMagick:

```bash
magick SOURCE.jpg -filter Lanczos -resize 800x -quality 93 glob2-NN-name.jpg
```

Save the submission JPEGs outside the repository (or in the session scratchpad) unless the user decides to keep them. Attach them with the ODT, or embed them in it as FCM allows.
