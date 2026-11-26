# Storefront-v2 visual review, round 1: raw mobile captures

[Captures under review](../captures/mobile/README.md) · [manifest](../captures/mobile/manifest.json) · [Footage rule](../../../planning/gameplay-video.md) · [Store comparables and image rules](../../../analysis/mobile-store-comparables.md) · [Caption source](../../../translations/en.md)

Reviewed 2026-11-24 by the independent visual reviewer. Scope: the 43 unique raw captures in `captures/mobile/` (`fdroid-phone/` is byte-identical to `android-phone/` and takes the same verdicts), plus about 300 of the alternate candidate frames.

## Verdict

**3 of 43 images are store-ready today. 17 are usable only if nothing better arrives. 23 are rejected.**

No device class can fill a six-slot gallery with images that pass. The iPad and both Android tablet sizes can reach six slots, but only by swapping in alternates from the candidate pool and accepting mostly weak frames; the phones reach four (iPhone) and five (Android). No class has an acceptable image for the *opponents* caption, and neither phone has an acceptable *economy* or *territory* image.

The capture engineer did the hard parts properly: real interface, real match, normal speed, native pixels, honest manifest. The problem is what is in the frames. Four things recur and each one alone would make a listing look unfinished:

1. **The event log.** Four to eight rows of semi-transparent text, mostly red "Your Warrior is under attack", sit across the upper-middle of nearly every frame. On phones it covers a 370–700 px tall band right where the colony is. On tablets it sits over the centre of the map. It is the first thing the eye reads at full size and a purple smear at thumbnail size.
2. **Zone squares.** Red and yellow outlined squares painted by the co-controlling AI are visible in 11 of the 43 frames (counted by detecting the outline colours), and in six of those there are dozens. Where they appear in number (island frames, the tablet battle raid, the war-flag frames) the image reads as a debug overlay.
3. **Fog-dimmed, empty ground.** In many frames 30–50% of the map area is dark blotchy grass with nothing on it. This is the "mostly empty terrain" the footage rule forbids, and at 300 px it turns the lower half of the image into dark camouflage.
4. **HUD weight on phones.** On iPhone portrait the first uncluttered map pixel is 34% of the way down the image (status band, stats block, event log); the bottom 9% is the button bar. Roughly 57% of the screenshot is left for the game, and the stats block is an irregular L-shape with visibly pixelated icons.

By comparison (Google Play pages opened 2026-11-24): Rusted Warfare's first screenshot is gameplay edge to edge with an explosion in the middle and a HUD limited to a money readout and minimap; Polytopia's is a close-up of bright units filling the frame above a one-fifth caption band. In both the subject fills about 80% of the image and nothing transparent lies over it. Bad North's App Store set uses portrait composites of two landscape frames. Our best tablet frames approach that density. Our phone frames do not.

## How the review was done

- Every final image was opened individually with the image viewer. The viewer downscales to about 2,576 px on the long side, so the 2868- and 2752-px images were seen at roughly 90% and 80%; native-pixel crops were made where detail mattered (HUD icons, zone overlays, dark bands).
- Every final image was also viewed as a thumbnail 300 px on the long side, in per-class sheets.
- Candidates: contact sheets were built for all frames from the busy saves in six candidate directories (iPhone portrait, iPad portrait, Android phone portrait, 7-inch landscape, 10-inch landscape; about 300 frames). Frames from the early `calm` save, map-peek frames, iPhone landscape, Android phone landscape, 7-inch portrait and 10-inch portrait were not mined, for the reasons in [Orientation](#orientation). About thirty promising candidates were then opened at 1,280–1,400 px.
- Reading of two overlays, from the game source (`src/render/GameRenderTerrain.cpp`): outlined red squares are forbidden zones, outlined yellow squares are clearing zones. The fields of coloured dots with no outline are, as far as I can tell, the wheat art; the AI's red grid sits over wheat and forest, which fits. I could not confirm the wheat reading from the art files, so treat it as my inference.

Verdict terms: **keep** = can ship as a raw input today; **KINB** = keep if nothing better, usable to fill a slot but should be replaced; **reject** = must not ship.

## Per-image verdicts

### `iphone-6.9/` portrait, 1320×2868

| File | Verdict | Reason |
| --- | --- | --- |
| `01-hero-colony` | KINB | The colony core (barracks, pool, school) is there and recognisable at thumbnail size. But a 5-row log (4 red) lies across the band above it, the lower third is sparse grass with fog blotches, the second pool is cut off at the right edge, and red zone squares peek out along the top edge under the stats block. |
| `02-economy-swarm-inspector` | reject | The selected Swarm is hidden under the inspector header, food bar and log. What remains is grass, a dial and two small buildings. Nothing in the picture says "fed" except the text "Food 6/20". |
| `03-battle-warriors-clash` | KINB (weak) | About ten blue and eight red warriors loosely scattered mid-frame; no hit effects; half the frame is fog-dimmed; four log rows. A newcomer sees dots on dark grass. |
| `04-build-menu` | KINB | Densest phone frame and the palette explains itself. But the log is seven rows deep (a quarter of the map), palette icons are unlabelled and soft, and a dark blotch fills the bottom. |
| `05-war-flag-front` | reject | The inspector title and a log line are drawn through each other; the inspector reads "0 / 0 HP"; the dial covers the lower half; the ground is dark. |
| `06-island-raid` | reject | First stat reads "-11/117" inside a red outline, which looks like an error. Wheat dots and haze dominate; the raid is five units on a shoreline; the enemy Swarm is fogged to grey. |
| `07-map-peek` | reject | A modal over a dimmed scene, showing a 100-pixel minimap blown up into blocks. It is the least attractive frame in the set and sells nothing. |

### `iphone-6.9/` landscape, 2868×1320

All four **reject**. The map occupies only x = 184–2680 (87% of the width) with flat navy bands left, right and below the button bar, so the screenshot looks letterboxed. The log runs the full width through the vertical centre, directly over the pool and school in `01` and `04`. In `02` the inspector header, food bar and log stack to cover 45% of the height. In `04` a log line is cut off behind the build palette. `03` has a readable fight (green warriors ringing a red one) but the log sits on top of the approach. Do not upload a landscape iPhone set.

### `ipad-13/` portrait, 2064×2752

| File | Verdict | Reason |
| --- | --- | --- |
| `01-hero-colony` | KINB | Widest view of the colony, with a skirmish bottom-left. But a grid of red zone squares covers the left edge and top-left, a yellow zone box sits on an inn, and the lower 35% is fog blotches. Replace with candidate `hero-bp2-2` (below). |
| `02-economy-swarm-inspector` | KINB | Clean inspector card ("Assigned 6 · Target 6", worker/explorer/warrior counts) beside three Swarms. Bottom 40% is empty with one large dark blotch, and the red "Destroy" button is the most prominent control. |
| `03-battle-raid` | KINB | The most attractive frame on iPad: violet forest, algae water, the blue colony, war flags. As a battle it is thin: about four red warriors are visible, so it reads as "blue town" more than "fight". Six log rows; lower right hazed. |
| `04-build-menu` | **keep** | Named palette (Stone Wall … Inn), a full colony with two construction sites, and a real fight bottom-left. Log is six rows but small at this scale. Fog blotches in the lower half are the remaining weakness. |
| `05-war-flag-front` | reject | A red zone grid fills a fifth of the frame; "0 / 0 HP"; four "Minimum required level" buttons; most of the map is dark. |
| `06-island-colony` | reject | Dozens of red zone squares on the forest ring and fields, plus two yellow boxes; six log rows, five red; white haze over the centre. The island itself is a good subject. |

All iPad frames carry the date in the status bar, a black strip under the map and the iPadOS resize handle bottom-right. These are honest and acceptable; the caption design should not draw attention to that corner.

### `android-phone/` portrait, 1080×1920 (also `fdroid-phone/`)

| File | Verdict | Reason |
| --- | --- | --- |
| `01-hero-colony` | KINB | Tighter and better filled than the iPhone hero, but the six-row log hides the barracks and the top of the pool, and sprites are visibly soft (see [Store fitness](#store-fitness)). |
| `02-economy-swarm-inspector` | reject | Same failure as iPhone: Swarm under the header, six log rows, dial over grass. |
| `03-battle-warriors-clash` | KINB | A red line facing a blue line right of centre, enemy buildings around. Dark. Candidate `battle2-bp-2` is clearly better. |
| `04-build-menu` | KINB | Best of the phone set: core buildings centred, four log rows. Palette icons unlabelled and soft. |
| `05-war-flag-front` | reject | Seven log rows drawn through the inspector header; "0 / 0 HP"; dark. |
| `06-island-colony` | reject | Eight log rows cover the top 45% of the map including the racetrack; red and yellow zone squares. |
| `07-map-peek` | reject | As iPhone. |

### `android-phone/` landscape, 1920×1080 (also `fdroid-phone/`)

All four **reject**. `01`, `02` and `04` come from the early save (tick 15,465–16,266; the first stat totals 92–104 where the busy save shows 170–230): two Swarms and a few inns on open grass, with black unexplored areas on the minimap, and `01` also has four red zone squares. That is an early-game start, which the footage rule excludes. `02` shows "-1/97" in a red outline. `04` has a log line truncated behind the palette. `03` is from the busy save and the fight is good, but five log rows lie across it. Sprites are soft throughout. The set is not needed: three 9:16 portrait images meet Google Play's requirement.

### `android-tablet-7/` landscape, 1920×1200

| File | Verdict | Reason |
| --- | --- | --- |
| `01-hero-colony` | KINB | Good spread of buildings, but the six-row log sits exactly on the barracks and the top of the pool, the two buildings that carry the shot. Candidate `hero-bp-1` has four rows. |
| `02-economy-swarm-inspector` | KINB | Readable card; four or five red zone squares top-right; a third of the frame is card. |
| `03-battle-raid` | KINB | The prettiest frame in the whole delivery (forest, water, combat puff, no zone squares). The fight is four red against four blue in the middle; the right third is dim. Better as an atmosphere frame than as the battle. |
| `04-build-menu` | KINB | Palette covers half the pool and a log line is cut off behind it. Candidate `build-bp-2` fixes the log. |
| `05-island-colony` | reject | Eight log rows over the racetrack; red and yellow squares. |

### `android-tablet-10/` landscape, 2560×1600

| File | Verdict | Reason |
| --- | --- | --- |
| `01-hero-colony` | **keep** | Pool, school, barracks, tower, hospitals, inns, racetrack and dozens of globs, well spread. Six log rows (five red) are the flaw, but they sit between buildings. The dark wheat field bottom-left is a quarter of the frame and should shrink in a re-capture. |
| `02-economy-swarm-inspector` | KINB | Clean card, three Swarms, inns and a pool. Half the frame is open grass. |
| `03-battle-raid` | reject | Dozens of red and more than a dozen yellow zone squares across the forest and field. The scene underneath is the best battle composition captured; the overlay ruins it. |
| `04-build-menu` | **keep** | The best image in the delivery. Dense colony, two construction sites, named palette, only two log rows. This is the standard the other frames should meet. |
| `05-war-flag-front` | reject | About 60% of the map is fog-dimmed; the card is the brightest thing; "0 / 0 HP". |
| `06-island-colony` | reject | Zone squares along the whole forest ring; seven log rows. |

### `android-tablet-10/` portrait, 1600×2560

| File | Verdict | Reason |
| --- | --- | --- |
| `01-hero-colony` | KINB | Much of the colony in view; lower third dark. |
| `02-economy-swarm-inspector` | reject | More than twenty red zone squares upper right. |
| `03-battle-warriors-clash` | KINB | A clear red column against blue in the centre; the frame is more than half fog. |
| `04-build-menu` | KINB | Good. |

In portrait the stats bar shrinks to tiny text. I recommend not using this orientation (see below).

## Recommended galleries

Slots follow the caption order. Finals are relative to `captures/mobile/`. Candidates are named as `candidates/<directory>/<file>` under
`<session scratchpad>/mobile-capture/`; full paths are in the next section. The scratchpad is temporary, so the capture engineer should publish any accepted candidate through `tools/selection.json` promptly.

A caption has to be literally true of its picture. Three captions cannot be satisfied by any gameplay frame captured so far:

- **maps** ("23 maps, 67 map generators"): one island colony shows a second map, not 23 maps or any generator. The honest picture is the map chooser. A menu is allowed from slot 6.
- **opponents** ("Face 8 computer opponents"): the matches captured have two or three AI colonies. No frame shows eight of anything. The honest picture is the lobby's opponent picker, or the caption changes. The coordinator should also confirm what "8" counts.
- **fair_deal** ("No ads, no in-app purchases"): true of any clean gameplay frame, but it needs one that is not already used. Only the Android phone set has a spare, and it is a weak one.

### iPhone 6.9, portrait

| Slot | Caption role | Image | Level |
| --- | --- | --- | --- |
| 1 | hero | `iphone-6.9/01-hero-colony-1320x2868.png` | KINB |
| 2 | build | `iphone-6.9/04-build-menu-1320x2868.png` | KINB |
| 3 | economy | **no acceptable image** | |
| 4 | battle | candidate `iphone-6.9-portrait/battle3-bp-2.png` | KINB |
| 5 | territory | **no acceptable image** (nearest: candidate `flags-bp-2.png`, which shows "-1/215" in a red outline) | |
| 6 | maps | candidate `iphone-6.9-portrait/hero-fs-1.png`, as "a second map" only | KINB |
| 7 | opponents | **no acceptable image** | |
| 8 | fair_deal | **no acceptable image** | |

Four slots, none at keep level. Not ready.

### iPad 13, portrait

| Slot | Caption role | Image | Level |
| --- | --- | --- | --- |
| 1 | hero | candidate `ipad-13-portrait/hero-bp2-2.png` | keep |
| 2 | build | `ipad-13/04-build-menu-2064x2752.png` (or candidate `build-bp-2.png`, same view with a larger fight) | keep |
| 3 | economy | candidate `ipad-13-portrait/economy1-inn-bp-1.png` | KINB |
| 4 | battle | `ipad-13/03-battle-raid-2064x2752.png` | KINB |
| 5 | territory | candidate `ipad-13-portrait/flags-bp2-1.png` | KINB |
| 6 | maps | candidate `ipad-13-portrait/hero-fs-1.png`, as "a second map" only | KINB |
| 7 | opponents | **no acceptable image** | |
| 8 | fair_deal | **no acceptable image** | |

Six slots, two at keep level. Shippable as an interim five- or six-image set if Apple's window forces it.

### Android phone and F-Droid phone, portrait

| Slot | Caption role | Image | Level |
| --- | --- | --- | --- |
| 1 | hero | `android-phone/01-hero-colony-1080x1920.png` | KINB |
| 2 | build | `android-phone/04-build-menu-1080x1920.png` | KINB |
| 3 | economy | **no acceptable image** | |
| 4 | battle | candidate `android-phone-portrait/battle2-bp-2.png` | keep |
| 5 | territory | **no acceptable image** (nearest: candidate `flags-bp-1.png`: three unlabelled icons, dim ground) | |
| 6 | maps | candidate `android-phone-portrait/hero-fs-1.png`, as "a second map" only | KINB |
| 7 | opponents | **no acceptable image** | |
| 8 | fair_deal | `android-phone/03-battle-warriors-clash-1080x1920.png` (a different fight from slot 4) | KINB |

Five slots, one at keep level. Not ready for a six-slot gallery; enough for Play's three-screenshot minimum.

### Android tablet 7-inch, landscape

| Slot | Caption role | Image | Level |
| --- | --- | --- | --- |
| 1 | hero | candidate `android-tablet-7-landscape/hero-bp-1.png` | KINB |
| 2 | build | candidate `android-tablet-7-landscape/build-bp-2.png` | KINB |
| 3 | economy | `android-tablet-7/02-economy-swarm-inspector-1920x1200.png` | KINB |
| 4 | battle | `android-tablet-7/03-battle-raid-1920x1200.png` | KINB |
| 5 | territory | candidate `android-tablet-7-landscape/flags-bp-2.png` | KINB |
| 6 | maps | candidate `android-tablet-7-landscape/hero-fs-1.png`, as "a second map" only | KINB |
| 7 | opponents | **no acceptable image** | |
| 8 | fair_deal | **no acceptable image** | |

Six slots, none at keep level.

### Android tablet 10-inch, landscape

| Slot | Caption role | Image | Level |
| --- | --- | --- | --- |
| 1 | hero | `android-tablet-10/01-hero-colony-2560x1600.png` | keep |
| 2 | build | `android-tablet-10/04-build-menu-2560x1600.png` | keep |
| 3 | economy | `android-tablet-10/02-economy-swarm-inspector-2560x1600.png` | KINB |
| 4 | battle | candidate `android-tablet-10-landscape/battle3-fs-1.png` | KINB |
| 5 | territory | candidate `android-tablet-10-landscape/flags-bp-2.png` | KINB |
| 6 | maps | candidate `android-tablet-10-landscape/hero-fs-1.png`, as "a second map" only | KINB |
| 7 | opponents | **no acceptable image** | |
| 8 | fair_deal | **no acceptable image** | |

Six slots, two at keep level. The strongest class.

### Does the set tell the story?

Slots 1 and 2 do: a newcomer sees a busy colony and a menu of things to build. After that the story breaks. The economy frames show a control panel, not food. The battle frames show small groups on dark ground, so "Fight for the land" promises more than the picture delivers. Territory, maps and opponents have nothing true to show. As captured, the set says "there is a town and some menus"; it does not yet say "you grow it, feed it, and take land from rivals".

## Better alternates found among the candidates

All under `<session scratchpad>/mobile-capture/candidates/`.

| Candidate (full path) | Replaces | Why it is better | What is still wrong |
| --- | --- | --- | --- |
| `<session scratchpad>/mobile-capture/candidates/ipad-13-portrait/hero-bp2-2.png` | `ipad-13/01-hero-colony` | Closer zoom, so the colony fills two-thirds of the frame; no zone squares; a skirmish at the bottom edge. | Six log rows; two dark blotches. |
| `<session scratchpad>/mobile-capture/candidates/ipad-13-portrait/hero-bp2-1.png` | same (second choice) | Same view with a bright wheat field and a fight at the bottom. | White haze upper right. |
| `<session scratchpad>/mobile-capture/candidates/ipad-13-portrait/build-bp-2.png` | `ipad-13/04-build-menu` (optional) | Same view, more units, and a fight of about forty units bottom-left. | Five log rows. |
| `<session scratchpad>/mobile-capture/candidates/ipad-13-portrait/economy3-barracks-bp2-2.png` | alternative for the build slot | A construction site selected, with "Wood 9/10 · Stone 10/10 · Assigned 1 · Target 12" beside the pool and school. It is the most literal picture of "You decide. They build." | Lower half dark and empty. |
| `<session scratchpad>/mobile-capture/candidates/ipad-13-portrait/economy1-inn-bp-1.png` | `ipad-13/02-economy-swarm-inspector` | An Inn selected, with "Food · Cherries · Oranges · Prunes" lines, inns, two Swarms and a lit wheat field. It is about food. | Food reads "0/30"; six log rows. |
| `<session scratchpad>/mobile-capture/candidates/ipad-13-portrait/flags-bp2-1.png` | `ipad-13/05-war-flag-front` | Flags palette open beside a clear blue line meeting a red line; no zone squares near the fight. | First stat "-4/199" in a red outline; dark ground. |
| `<session scratchpad>/mobile-capture/candidates/ipad-13-portrait/hero-fs-1.png` | `ipad-13/06-island-colony` | One yellow box instead of dozens of red squares; the log lies over forest and water. | Seven log rows; haze. |
| `<session scratchpad>/mobile-capture/candidates/iphone-6.9-portrait/battle3-bp-2.png` | `iphone-6.9/03-battle-warriors-clash` | A visible hit flash, only three log rows, no zone squares. | Fight is in the top third; lower half is empty. |
| `<session scratchpad>/mobile-capture/candidates/iphone-6.9-portrait/battle2-bp-4.png` | same (second choice) | Two columns of warriors facing each other in the centre: the most legible fight on iPhone. | Two red zone squares at the left edge; fog. |
| `<session scratchpad>/mobile-capture/candidates/iphone-6.9-portrait/hero-fs-1.png` | `iphone-6.9/06-island-raid` | Shows the island colony itself, with forest and water; no negative stat. | Yellow box at the right edge; six log rows. |
| `<session scratchpad>/mobile-capture/candidates/android-phone-portrait/battle2-bp-2.png` | `android-phone/03-battle-warriors-clash` | Red warriors breaking out of the forest into the blue base, water above, enemy tower and pool below; three log rows; no zone squares. The best battle frame on any phone. | Soft sprites. |
| `<session scratchpad>/mobile-capture/candidates/android-phone-portrait/hero-fs-1.png` | `android-phone/06-island-colony` | No red squares. | Seven log rows over the top of the colony; yellow box. |
| `<session scratchpad>/mobile-capture/candidates/android-tablet-7-landscape/hero-bp-1.png` | `android-tablet-7/01-hero-colony` | Four log rows instead of six. | Still touches the barracks roof. |
| `<session scratchpad>/mobile-capture/candidates/android-tablet-7-landscape/build-bp-2.png` | `android-tablet-7/04-build-menu` | Three log rows, none cut off by the palette; barracks visible. | Palette still covers half the pool. |
| `<session scratchpad>/mobile-capture/candidates/android-tablet-7-landscape/flags-bp-2.png` | (territory slot, none selected) | Named flag palette with a fight at the enemy Swarm. | Four red squares top-left; dim. |
| `<session scratchpad>/mobile-capture/candidates/android-tablet-7-landscape/hero-fs-1.png` | `android-tablet-7/05-island-colony` | One yellow box, no red grid. | Seven log rows over the racetrack. |
| `<session scratchpad>/mobile-capture/candidates/android-tablet-10-landscape/battle3-fs-1.png` | `android-tablet-10/03-battle-raid` | Home defence at a Swarm with smoke, purple raiders and many red globs; no zone squares. | First stat "-16/120" in a red outline. |
| `<session scratchpad>/mobile-capture/candidates/android-tablet-10-landscape/flags-bp-2.png` | `android-tablet-10/05-war-flag-front` | Named flag palette (Exploration Flag, War Flag, Clearing Flag, Forbid, Guard, Clear) with red warriors streaming toward the blue colony; mostly green log; no zone squares. | Left third dark. |
| `<session scratchpad>/mobile-capture/candidates/android-tablet-10-landscape/hero-fs-1.png` | `android-tablet-10/06-island-colony` | One yellow box instead of a ring of red squares. | Seven log rows. |

Candidates I checked and do not recommend: every `battle1-bp-*` on Android phone (a black unexplored patch, which is a fog-black frame); the iPad and 10-inch `battle1-bp*` and `build-fs-*` frames (zone squares); every tablet `economy1-inn` frame except the iPad one above (the Inn is mid-upgrade, so the card shows wood, not food).

## Orientation

| Class | Engineer's recommendation | My view |
| --- | --- | --- |
| iPhone | Portrait primary, landscape secondary | **Portrait only.** Landscape is letterboxed to 87% of the width and the log crosses the middle of the scene; it looks broken. The App Store also shows three portrait screenshots where it would show one landscape. Portrait's cost is the HUD share noted above, which the caption design has to work around. |
| iPad | Landscape preferred, only portrait captured | **Ship portrait.** The portrait frames at the closer zoom (0.96–1.2) are among the best in the delivery. Landscape would probably be a little better, judging by the 10-inch Android frames, but it is a lower priority than fixing overlays. |
| Android phone | Portrait primary, landscape secondary | **Portrait only.** 1080×1920 is 9:16 and three of them meet Play's requirement, so landscape is unnecessary, and the landscape frames fail on their own. |
| Android tablet 7-inch | Landscape | **Agree.** |
| Android tablet 10-inch | Landscape primary, portrait also good | **Landscape only.** In portrait the stats bar becomes tiny and the frames are half fog. |

## Store fitness

- **Apple 2.3.3.** Every frame shows the app in use. Pixel sizes are valid (1320×2868, 2064×2752). The 9:41 status bar is correct. Simulator captures are acceptable. iPad needs at least one image; the interim set above would pass review.
- **Google Play.** 1080×1920 qualifies for the 9:16 requirement; 1920×1200 and 2560×1600 are within the tablet range; tablet sets need at least four images. All are real gameplay.
- **Honesty of the Android sets.** They are host renders, not device or emulator screenshots, as the README says plainly. That fails this project's own check in the comparables record ("captioned images are real device captures for the platform they are uploaded to"). I would accept them as an interim upload only if the rollout ledger says so. Separately, the phone renders are visibly soft compared with the iPhone captures of the same scene (look at the pool and school in `android-phone/01` against `iphone-6.9/01`). If a real Android phone draws sharper, these undersell the game; if it does not, that is a product issue. Either way an emulator capture is needed to know.
- **Caption room.** Play asks that taglines take no more than 20% of the image. On phone portrait the HUD and log already take about 40%, so the caption band must sit over the status band and stats area or over the button bar, not over the remaining map.

## Re-capture requests, in priority order

Written for the capture engineer. "Fixed" means the acceptance test in each item.

**1. A clean-state protocol for every frame.** This fixes most rejections.
- *Zone squares.* Now: visible in 11 finals. Fixed: zero red or yellow outlined squares anywhere in the frame at 100%, including under the HUD and at the edges. Erase and shoot inside the gap before the AI repaints, or find a way to stop it repainting for the capture (for example, if the Teams panel lets the human take sole control after loading). Check each frame before publishing.
- *Event log.* Now: 4–8 rows. Fixed: at most two rows, and no row over a building that carries the shot. For hero, build and economy frames, first pull the warriors home as a player (destroy the war flags, record it in the manifest), wait until "under attack" stops, then wait at least 10 seconds so the list empties. For battle frames, shoot in the first few seconds of contact, or place the camera so the log's rectangle falls on water, forest or grass. On the 10-inch layout that rectangle is roughly x 950–1790, y 340–590.
- *Fog.* Now: 30–50% of many frames. Fixed: no dark blotch inside the colony and no more than about 15% of the map area dimmed. Move the camera, zoom in one step, or wait for units to light the area.
- *Stats.* Fixed: the first stat is not negative and has no red outline.
- *Selection rings.* Fixed: none, unless the shot is about the selected thing.

**2. Battle, all classes.** Now: small groups on dark ground. Fixed: at least twelve units of each colour in one screen, a visible hit effect (smoke or flash), at least two enemy buildings in frame, on lit ground, fight centred in the free map area. Template: `android-phone-portrait/battle2-bp-2.png`. The 10-inch `03-battle-raid` view without its zone squares would also do.

**3. Economy ("Keep the colony fed"), all classes.** Now: a Swarm with a dial. Fixed: an Inn that is *not* upgrading is selected, so its card shows the food lines; a lit wheat field with workers on it and a Swarm are in the same frame; on phones the Inn sits left of centre, clear of the header and the dial. Template: `ipad-13-portrait/economy1-inn-bp-1.png`, ideally with food above zero.

**4. Phone hero, iPhone and Android.** Now: core buildings under the log, empty lower third. Fixed: barracks, pool and school sit in the middle of the free map band; the second pool and racetrack to the south-east are fully inside the frame instead of cut off at the right edge; the bottom third holds buildings or a visible skirmish; clean-state protocol applied. Try moving the camera about five tiles east and four south of the current position.

**5. Territory ("Choose where to expand"), all classes.** Now: the War Flag inspector, which shows "0 / 0 HP" and four "Minimum required level" buttons. Fixed: the Flags palette is open, a flag has just been placed on the frontier with its range circle visible, and globs are moving toward it over lit ground. On tablets the named palette is good. On phones three of the six buttons are unlabelled icons, so choose a moment where the placed flag makes the meaning obvious.

**6. Maps ("23 maps, 67 map generators").** Nothing captured shows this. Fixed: a capture of the map chooser in the touch interface with the map list or previews, and the generator list if it fits, on each device class. Keep one island-colony gameplay frame per class with zero zone squares as the fallback, and add a third map that looks different from both at thumbnail size.

**7. Opponents ("Face 8 computer opponents").** Nothing captured shows this. Fixed: either the custom-game lobby with the opponent picker listing the computer players, or a gameplay frame where at least three enemy colours are fighting in one view. Tell the coordinator which is possible; if neither is, the caption has to change.

**8. A spare clean frame per class for the fair-deal slot.** Fixed: one more hero-quality frame of a different part of the colony or a different map, under the clean-state protocol.

**9. Android emulator or device captures**, once the SDK licences are accepted, to replace the host renders.

**10. iPad landscape (2752×2064).** Useful, not urgent.

**Stop producing:** iPhone landscape, Android phone landscape, Android 10-inch portrait, the map peek and the War Flag inspector.

## Product issues the captures expose

These are not capture faults, but a faithful screenshot will keep showing them until the game changes. The coordinator should decide whether any are fixed before the final capture round.

- The event log cannot be dismissed, keeps up to eight rows for about eight seconds each, and on tablets sits over the middle of the map.
- Log text is drawn through the inspector header and behind the build palette.
- The phone stats block is an L-shape of seven tiles with low-resolution icons scaled up.
- The first stat can show a negative number in a red outline ("-11/117").
- The War Flag inspector shows "0 / 0 HP".
- iPhone landscape leaves 13% of the width as empty navy bands.
- Android tablet renders have a 32-pixel navy strip along the top edge that shows at the top-left corner beside the stats bar. It may simply be where the system status bar would be, but in a host render it looks like a glitch.
- Wheat is drawn as fields of coloured dots, which newcomers will not read as crops.
