# Storefront-v2 visual review, round 1: desktop captures, key-art plates and the captioned layout

[Desktop captures](../captures/desktop/README.md) · [Captioned proofs](../store-screenshots/README.md) · [Compositor](../tools/README.md) · [Mobile review](round-1-mobile.md) · [Footage rule](../../../planning/gameplay-video.md) · [Caption source](../../../translations/en.md)

Reviewed 2026-11-24 by the independent visual reviewer. Three subjects: the 15 desktop finalists (3840×2160, with 2880×1800 twins), the five `keyart-*` plates, and the layout of the captioned mobile proofs.

## Verdicts in brief

- **Desktop captures: 3 of 15 are store-ready, 10 are usable if nothing better arrives, 2 are rejected.** This set is far stronger than the mobile round. A seven-image gallery can ship today for six of the seven caption roles. The *opponents* caption has no frame that makes it literally true, and there is no AI co-play frame.
- **Key art: none of the five plates can carry the main store image.** Two are useful raw material. The plate that is needed is described below.
- **Captioned layout: structurally sound, typographically weak.** The regular-weight caption is the main reason the proofs still read as home-made beside Polytopia and Rusted Warfare. Six concrete changes are listed.

## How the review was done

- All fifteen 16:9 finalists were opened individually (the viewer shows 3840 px images at about 67%), and native-pixel crops were made of the hero and the HUD column. All fifteen were also viewed at 600 px wide.
- The 16:10 twins were viewed only as 600 px thumbnails and checked against the manifest's zoom values. They were not opened at full size. Their verdicts follow their 16:9 twins, with the caveats in [The 16:10 set](#the-1610-set).
- Each key-art plate was viewed at half size and as centre crops at 16:9, 1024×500, 3:1, 2:3, 1:1 and 3:4. Two were also opened at full size.
- Layout: the seven English contact sheets, three proofs at full size, the compositor's thumbnail comparison, and my own strips of four store sets at search-result size (240 px tall for phones, 200 px for tablets). Layout numbers come from `tools/screenshots.py`, `tools/gallery.json` and the proofs' manifests.

Verdict terms as in the mobile review: **keep**, **KINB** (keep if nothing better), **reject**.

## Part 1: desktop captures

### What is good

The HD artwork reads as attractive at full size and as a thumbnail. Colonies are dense. Every frame has a real HUD, a real match and honest fog. The engineer's choices to switch clouds off, force HD artwork on and erase forbidden and clearing zones were right. No red or yellow zone squares remain in the fifteen finalists except one yellow square in `03-battle-candidateB`.

### Problems that recur

1. **Health and food bars under every unit and building.** Every glob carries a segmented cyan-green bar, and buildings carry dotted bars and vertical yellow gauges. At full size they double the visual noise; at 600 px they turn crowds into speckle. The mobile captures switched this off; the desktop set did not. This is the largest single fix.
2. **Blue guard-area grids and war-flag circles.** Zone erasing covered forbidden and clearing areas but not guard areas. Blue dotted grids with dark teardrop markers, plus large blue range circles, sit on top of the fight in `03-battle-A`, `03-battle-B`, `04-territory-B`, `05-map-B`, `06-chaos-A` and `08-siege`, and in the corners of `01-hero-B` and `07-build-A`. In the battle frames they are the most prominent shapes in the picture. A newcomer reads them as a targeting diagram.
3. **Red text.** The first number in the top bar is red and negative in 11 of 15 frames ("-29/158", "-60/178"). The event list is short here (two to six rows, top-left) and much less harmful than on mobile, but it is still mostly red "under attack" lines.
4. **Zoom.** Eight frames are at 62.5–87.5%. At 600 px wide a glob is 6–9 px, so a thumbnail shows buildings and terrain pattern, and a fight only as a patch of mixed colour. The frames at 100–137.5% (`02`, `03`, `05-B`, `07`, `08`) read much better small. To the question "are these too zoomed out to read as exciting": the colony overviews are fine as overviews, but the lead image and the battle image should be at 100% or closer.
5. **The right-hand column.** It takes 10.5% of the width. Below the ten build icons it is two-thirds empty navy, and the icons and minimap are low-resolution art scaled up beside sharp HD sprites. It is the real interface and must stay, but it means every frame has a dark stripe on the right. Frames with a building selected (`02`) fill it better.
6. **One map dominates.** FourSquares appears in 7 of 15 frames, five of them the same red or lime home island. `01-hero-A`, `02-economy-A` and `07-build-A` are near-identical thumbnails.
7. **AI names in panels.** A selected building is titled "Inn (Maxima)" or "Swarm (Cabino)". Honest, and explained in the README, but a viewer will wonder who Maxima is.

### Per-image verdicts (16:9 files; `-3840x2160.png` omitted)

| File | Verdict | Reason |
| --- | --- | --- |
| `01-hero-thriving-colony-candidateA` | **keep** | The whole red island: about 45 buildings, forests either side, water at the corners. Symmetrical, colourful, instantly "a colony". Only two log rows. Flaws: unit bars, red "-29/158", and no fight anywhere, so it is busy but not exciting. At 87.5% the globs are small. |
| `01-hero-thriving-colony-candidateB` | KINB | Same idea in cyan, with two pools. Six log rows, a blue rectangle top-right and a blue arc bottom-right. Redundant with A. |
| `02-economy-at-work-candidateA` | KINB | Inn selected with food lines in the panel. But the panel shows a red no-entry warning ("1 units can't access needed materials"), Food is 3/10 with every fruit at 0, the centre of the frame is empty grass, and it is the red FourSquares colony again. |
| `02-economy-at-work-candidateB` | KINB | Lime colony, Swarm selected with worker slider and Worker/Explorer/Warrior ratios. Good variety of colour and well-spread buildings. Four red log rows starting "The Inn is under attack"; Food 1/20. No crop field or carrying in view. |
| `03-battle-candidateA` | KINB (strong) | The most striking frame: red against lime around the oasis at 137.5%, units large enough to read at 600 px, terrain unlike any other shot. Spoiled by five blue circles, a blue guard grid with dark markers across the fight, and "-11/175". The right fifth is dark fogged soil. |
| `03-battle-candidateB` | reject | Six log rows, a third of the frame under fog, a yellow zone square, overlapping blue circles. Muddy as a thumbnail. `03-A` does the job better. |
| `04-contested-territory-candidateA` | KINB | Two islands and a channel is a clear idea. But the rival island is dim, nothing is meeting, and at 62.5% every red unit carries an orange need icon. Third use of the red FourSquares colony. |
| `04-contested-territory-candidateB` | KINB | Red base under construction, the contested oasis, the lime Swarm: all three in one view, so the caption is true. Two black unexplored patches on the right, guard grid and circles, "-46/160". Same location as `03-A`. |
| `05-map-variety-candidateA` | **keep** | Lava flows, a crater, a sand ring and paved paths, with a full red colony on the right and cyan raiders on the left. Clearly a different map. The black crater mouth may be read as missing terrain; five log rows sit over dim ground. |
| `05-map-variety-candidateB` | KINB | Stone roads and sand are distinctive and the colony is dense. Guard grid over the left, a quarter of the frame fogged. |
| `06-multiplayer-chaos-candidateA` | KINB (weak) | A lot is happening, but three guard grids, many circles and fog over a third of the frame make it muddy. Third City-states frame. |
| `06-multiplayer-chaos-candidateB` | **keep** | Three crater lakes, violet forest, red warriors overrunning purple Swarms and a ring of small buildings. The prettiest frame in the set and the fight is findable. Flaws: 75% zoom, a fog band upper right, five log rows. |
| `07-build-menu-candidateA` | KINB | Footprint outlines on every building do say "placement". But the armed Inn's preview is not findable at a glance, the panel text ("Inn. Feeds your units") is tiny, the hint "Ctrl + Drag = Line" shows bottom-left, and the thumbnail is almost the same as `01-A`. |
| `07-build-menu-candidateB` | reject | The Flags tab is sixteen unlabelled icons; no flag is placed; "The Inn is under attack" in red. A third lime/red FourSquares colony shot with nothing new in it. |
| `08-siege-on-a-hive-candidateA` | KINB | Good subject (two cyan Swarms, a smoking building, about 25 red warriors between two lakes). Dark fog bands, a guard grid and four circles over the fight, "-60/178". |

### The 16:10 set

Each twin is one zoom step further out, so units are smaller still. By the manifest, the 16:10 twins of `04-A`, `04-B`, `05-A`, `06-A` and `06-B` are at 62.5%, the zoom at which the game draws need icons over every unit (visible in the 16:9 `04-A`). The hero twins are at 75%. For the Mac App Store I would rather have the same zoom as the 16:9 frame and fewer tiles in view than the same tiles and smaller units.

### Recommended desktop gallery

Seven images. The order alternates colony and conflict so that no two neighbouring thumbnails look alike; the caption roles stay attached to their images whatever order a store shows.

| Slot | Caption role | Image | Level | Is the caption true of it? |
| --- | --- | --- | --- | --- |
| 1 | hero | `01-hero-thriving-colony-candidateA` | keep | Yes. |
| 2 | battle | `03-battle-candidateA` | KINB | Yes. |
| 3 | build | `07-build-menu-candidateA` | KINB | Half. It shows choosing a building. It does not show the worker count or workers building. |
| 4 | economy | `02-economy-at-work-candidateB` | KINB | Partly. Inns and Swarms are there and the panel shows production. I could not find wheat being carried. |
| 5 | territory | `04-contested-territory-candidateB` | KINB | Yes. |
| 6 | maps | `05-map-variety-candidateA` | keep | Yes. |
| 7 | opponents | `06-multiplayer-chaos-candidateB` | keep as an image | Not demonstrably. Two colonies are in view; "several" needs three. |
| 8 | AI co-play | **no image** | | |

- **Lead image:** `01-A` today. It is the cleanest and reads fastest. It should be replaced by a hero at 100% or closer with a fight at the colony's edge (see re-capture 2), because the first image should promise conflict as well as building.
- **Store subsets:** Steam (five or more): slots 1, 2, 3, 5, 6, 7. Microsoft (four or more): slots 1, 2, 6, 7, then 3. Snap (five): slots 1, 2, 6, 7, 4.
- **Redundant:** `01-B` (with `01-A`), `02-A` and `07-A` (same colony as `01-A`; keep at most one beside it), `03-B`, `05-B` and `06-A` (three City-states frames, none clean), `07-B`.

### The AI co-play frame

The caption is "A local game shared with the player's own AI agent, connected through the built-in MCP server." For that to be true of a picture, the picture has to show three things: the game running, an agent that is visibly a separate program, and one sign that the two are connected (an action the agent just took that is visible in the colony).

**A real capture of the game beside a terminal or agent window is the right picture, with conditions.**

- One real screenshot of one real session. Not a composite of a game frame and a separately made terminal image.
- Game window about two-thirds of the width, agent window one-third. The agent's last lines should name an action in plain words (for example placing a flag or raising a building's worker count) and the same flag or building should be visible in the game window, ideally just placed.
- At 600 px the transcript will not be legible. It only has to read as "a chat or terminal next to the game", so use a large font, a dark theme close to the game's navy, and few lines.
- Nothing in the agent window may show a path, user name, token or private project name.
- A named third-party agent product in the window is a brand-use and store-policy question for the coordinator, not a visual one. A neutral terminal avoids it.

Where to use it: itch.io, Snap and AppStream take it without difficulty. Steam asks for gameplay-only screenshots, Microsoft forbids added marketing material inside screenshots, and Apple's 2.3.3 is about the app itself in use, so on Steam, the Microsoft Store and the Mac App Store a desktop screenshot showing a second application is a risk. For those, the better picture is a pure in-game frame in which the agent's presence shows in the game's own interface. I have not checked whether the game has such a surface (a Teams panel entry, a connection indicator, attributed events). If it has none, leave the slot out on those three stores.

### Desktop re-capture list, in priority order

1. **Clean-state protocol for every desktop frame.** Fixed means: no health or food bars under units and buildings (use the display option if the desktop interface has one; say so if it does not); no guard-area grid; no red or negative first stat; at most two log rows and none red where avoidable; no "Ctrl + Drag" hint; no black unexplored ground; no more than about 15% of the map under fog. War-flag range circles: at most one, and not across the fight.
2. **Hero with conflict.** Now: a calm colony at 87.5%. Fixed: 100% zoom or closer; a colony core (Swarm, pool, school, inns) filling the left two-thirds; a visible fight of at least 15 units a side at the right or lower edge with hit flashes; two strongly contrasting team colours; a different map from the build shot.
3. **Build.** Now: outlines everywhere and a preview nobody can find. Fixed: a construction site selected so the panel shows its materials and Working slider, workers visibly carrying to it, and one unmistakable placement preview on open ground. A different map or colony colour from the hero.
4. **Economy.** Now: no crops, food near zero, a red warning. Fixed: a crop field with workers on it in the same frame as an Inn and a Swarm; the selected Inn's food above half; no warning line in the panel. Please also confirm in the README which sprite is wheat, so the caption can be checked against the picture.
5. **Opponents.** Now: two colonies in view. Fixed: at least three colony colours fighting or building in one lit frame at 75% or closer. A small map with many colonies, seated in the middle, is the likeliest way to get it. If it cannot be done, tell the coordinator so the caption can change.
6. **Battle.** The `03-A` scene with the guard area erased and no circle crossing the units, or a larger clash elsewhere. Keep it at 125–150%.
7. **Territory.** Both colonies lit, no black, on a map not used for the battle shot.
8. **AI co-play**, as specified above.
9. **16:10 set** at the same zoom as the 16:9 set, never at 62.5%.
10. **Key-art plate**, as specified in part 2.

## Part 2: key-art plates

The main store image has to survive six shapes. I tested each plate with a centre crop at each.

| Plate | Verdict | Why |
| --- | --- | --- |
| `keyart-foursquares-colony-zoom100` | reject | Dozens of red zone squares remain along the top, bottom and edges, with a blue grid bottom-right. Beyond that: the island shape that makes the 16:9 work disappears in the 2:3, 1:1 and 3:4 crops, which become a field of small buildings; there is no calm area for a wordmark. |
| `keyart-foursquares-colony-zoom200` | usable raw material | Buildings read as characters. There is a natural calm patch of grass in the upper middle, about a fifth of the frame, where a wordmark could sit in the 16:9 and 1024×500 crops. Problems: a blue range arc crosses the top; unit and building bars are everywhere; no conflict; the focal building (the pool) is at the right edge, so the portrait and square centre crops get grass and one tower. At 200% the art is magnified and slightly soft, which is acceptable at half size. |
| `keyart-foursquares-cabino-zoom150` | usable raw material; the best of the five | Clean, with no overlays. A clear focal pair (pool and Swarm) left of centre, violet forest framing both sides, water at the bottom corners. It survives the 3:1 and 1024×500 crops well, and a 2:3 or 1:1 crop moved left to centre the pool and Swarm works. Problems: no calm area large enough for the wordmark without a scrim; a peaceful scene; unit bars. |
| `keyart-isles-colony-zoom150` | reject | Seven near-identical towers, Swarms cut off at the top edge, no focal point. |
| `keyart-honeycomb-battle-zoom200` | reject as captured | The only plate with action, and the blue circles, guard grid and markers cover it. The right quarter is grey stone and dark soil. The same scene without the guard grid would be a candidate. |

**None is good enough.** The store image has to say "real-time strategy" in one glance, hold a wordmark, and work as a tall poster and a wide banner. The clean plates are peaceful, and the action plate is covered in overlays.

### The plate to capture

- **Zoom:** 150% (96 px a tile). Buildings come out 300–500 px across in a 3840 px frame and globs about 90 px: characters, not specks, and sharper than 200%.
- **Size:** as large as the off-screen window allows, at least the 4256×2600 already used and preferably 5120×2880, so each crop is cut from native pixels.
- **Subject:** the edge of a developed colony under attack. A home cluster (Swarm, pool, school, two or three inns) as the focal group, and a rival's warriors of a strongly contrasting colour coming in with hit flashes. Fifteen or more units a side.
- **Calm area:** water wrapping the top and the left of the frame, in an L shape: roughly the top 30% and the left 30%. Fogged water is dark blue-violet, close to the brand night colour, and a cream wordmark reads on it without a scrim. The inner corner of a FourSquares island gives exactly this shape: water in one quadrant, colony in the rest.
- **Placement:** the focal cluster inside the central square of the frame, so the 1:1 crop holds it. The fight below or right of the cluster, inside the central 3:4. Nothing essential in the outer 15% left and right.
- **How each crop then works:** 16:9 and 1024×500 put the wordmark top-left over water. The 3:1 banner loses the top and bottom, so it puts the wordmark on the left water. The 2:3, 3:4 and 1:1 crops are taken from the left-centre so the top water becomes the top third for the wordmark and the cluster sits below it.
- **Clean state:** no HUD, no health or food bars, no zone squares, no guard grid, no flag circles, no selection, clouds off.

Until that exists, `keyart-foursquares-cabino-zoom150` with a scrim behind the wordmark is the least bad interim base, and I would not ship it as the main image.

## Part 3: captioned layout

Judged on layout only; the captures inside the proofs are the rejected round-1 frames.

### What works

- One consistent system across all seven store sets: same night background, cream caption, card with ring and shadow.
- The caption sits in its own band and never covers gameplay.
- The colours are the brand's and the band shares stay under Google Play's 20% (17.2% on iPhone, 18% on Android phones, 15.5% on Android tablets, 17.5% on iPad).
- The card treatment is a respectable pattern (Bad North's App Store set uses cards too).

### What still looks amateurish

1. **Caption weight.** The caption is set at weight 400. At search-result size the strokes are about one pixel wide and the caption greys out, while Polytopia's heavy white capitals and Rusted Warfare's bold outlined headline stay readable. This is the main gap in the thumbnail comparison.
2. **Wasted canvas.** The card is inset on three sides, so gameplay gets 72% of the image on iPhone, 62% on Android phones, 64% on iPad and 65% on Android tablets (from the proofs' manifests). Polytopia gives gameplay 80% and Rusted Warfare 100%. Side margins are 5.4% on iPhone but 9–11% on every other set, because there the card is fitted by height.
3. **The card has no visible top edge.** The game's own HUD is the same dark purple as the background, and the ring (`#4f3c6b`, 0.3% of the width) is nearly the same value. On phones the stats tiles appear to float on the background and the card reads as an irregular shape.
4. **Caption sizes change within a set.** The iPhone set uses four font sizes (112 to 128 px), the iPad set three and the Android phone set two; only the Android tablet sets use one. On iPad, "23 maps, 67 map generators" and the fair-deal caption wrap to two lines while the others are one line, and on phones one-line and two-line captions alternate. The set looks uneven when swiped.
5. **The gold slide.** A single accent slide for the fair deal is a good idea. The flat mustard field (`#e3c077`) with thin dark text looks like a different product's advert and is the weakest-looking slide in each set.
6. **Phone HUD under the caption.** On phones the first third of the card is the stats block and event list, so caption plus HUD take the top 40% before any gameplay appears. This is a capture and product matter more than a layout one, but the layout can avoid making it worse (see change 2).

### Changes

1. **Weight and size.** Set captions in a bold cut of the brand display face (weight 700; DejaVu Sans Bold is the same family and licence as Glob2 Sans). Raise the phone caption size to about 11% of the canvas width: 128 px to about 148 px on the 1320 px iPhone canvas (+15%), and 90 px to about 118 px on the 1080 px Android canvas (+30%; it is currently smaller in proportion than the iPhone's). Tighten letter-spacing by about 1%. Keep sentence case: capitals do not exist in many of the 44 scripts.
2. **Give the game more room.**
   - Phones: card 93–94% of the width (side margin 3–3.5% instead of 5.4% on iPhone and 10.6% on Android), and let the card run off the bottom edge with no bottom margin and square bottom corners. On Android phones fit the card by width, not height, and let the excess run off the bottom.
   - Tablets and iPad: card 92% of the width (side margin 4% instead of 9–10%), same bottom bleed.
   - Target: gameplay at least 78% of the image area in every set.
3. **Make the card edge visible.** Ring in the cream caption colour (`#f9e8bb`) at 55–65% opacity, about 0.4% of the width, or lift the background behind the card a step lighter than the HUD. Either way the top edge of the card must be visible where it meets the stats block.
4. **One caption size per store set.** Choose the size that fits the longest caption (two lines on phones, one line on tablets and iPad) and use it for every slide in that set. Keep the band height constant. On tablets and iPad, break no caption onto two lines unless every language's longest caption needs it; if it does, give all slides the two-line band.
5. **Bands.** With bold type the bands can stay close to where they are: 17–18% on phones, 16% on Android tablets (from 15.5%), 17% on iPad. Do not go above 19%, to leave margin under Play's 20%.
6. **Fair-deal variant.** Keep the night background. Set the caption in the accent gold and give the card a gold ring twice the normal width. If a gold field is kept, use the design system's accent gold, a top-to-bottom gradient no more than 8% in lightness, and the bold caption. Give the slide its own capture; in the proofs it repeats the hero.

After these, re-run the thumbnail comparison at 240 px (phones) and 200 px (tablets) against the same three comparables. The test is that every caption can be read at that size without zooming.

### Not changed, on purpose

- No logo or wordmark on the slides: Play discourages repeating the icon's branding, and the band is better spent on the caption.
- No device frame: it would cost more canvas.
- No caption over gameplay on phones: the top of the capture is already HUD.
