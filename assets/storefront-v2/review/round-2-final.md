# Storefront-v2 visual review, round 2 (final)

[Captioned sets](../store-screenshots/README.md) · [Mobile captures](../captures/mobile/README.md) · [Desktop captures](../captures/desktop/README.md) · [Key art](../key-art/README.md) · [Round 1: mobile](round-1-mobile.md) · [Round 1: desktop and layout](round-1-desktop-and-layout.md) · [Footage rule](../../../planning/gameplay-video.md) · [Claims per platform](../../../facts/storefront-v2-claims.md) · [Store rules and comparables](../../../analysis/mobile-store-comparables.md) · [Caption source](../../../translations/en.md)

Reviewed 2026-11-24 by the independent visual reviewer, who made none of these images. The test throughout is the user's: exciting action, not boring or empty scenes, and a listing that no longer looks amateurish.

## Verdicts in brief

| Item | Verdict | One line |
| --- | --- | --- |
| 1. Captioned mobile store sets (7 sets, 45 locales) | **Ship with listed fixes** | A large step up from round 1. Drop the opponents menu slide everywhere, put a fight in slot 2, and fix the two-line wrap of the fair-deal caption in 12 locales. Amazon waits for device captures. |
| 2. Clean desktop gallery (16:9 and 16:10) | **Ship with listed fixes** | Hero and battle are now genuinely good. Drop the spectator opponents frame, make the side-by-side co-play panel end on an action, and export 1920×1080 JPEGs for stores with file caps. |
| 3. Key art (concept A and about 25 derivatives) | **Ship with listed fixes** | A is the right main image of the three: it reads at every size and the wordmark always has calm water. It is peaceful, which is its real weakness. Move the Play feature graphic's wordmark in from the edge, and correct the provenance wording. |

Nothing here needs a redo before the "update now" stores (Snap, itch.io, Microsoft Store, Google Play, F-Droid/AppStream sources), provided the must-fix list is done first.

## How the review was done

- Every English image in the seven captioned sets was viewed at full size (the viewer shows 1320×2868 at about 90%, 2560×1600 at about 95%), and every set as a strip at store-thumbnail size: 240 px wide for phones, 200 px wide for tablets and iPad.
- Locale spot-check from the durable render `/Users/bradley/glob2/storefront-v2-renders/screenshots/`: caption bands of every slide for ar, ja, th, hi, ru, de, zh-Hans, ko, hu, fa and ta on iPhone, and for ar, ja, th, hi, ru, de, zh-Hans, ko and hu on iPad and the 7-inch tablet; the full Arabic iPhone contact sheet; and the caption band of the fair-deal, hero, build, economy, territory and maps slides for **all 45 locales** on iPhone.
- Desktop: all eight 16:9 frames and `08b` at 600 px wide; `01`, `04`, `05`, `07`, `08` and `08b` at full size; the 16:10 twins at 400 px wide.
- Key art: the three concepts and their thumbnail sheet; every derivative at its store display size in one sheet (Play feature 512 wide, Steam header 460, small capsule 231, Epic portrait 240, Microsoft poster 200, box art 150, and so on); the Play feature graphic and Microsoft poster at full size; the transparent logos on dark and light grounds; wordmark margins measured from the pixels.
- File checks: every English store screenshot is RGB (no alpha) and under 8 MB. Store-set files were checked against `tools/gallery.json`.
- Source checks (read-only, game repository at `v0.11.7.0` and `origin/master`): the lobby's JavaScript-AI hint and the gating of Settings → Custom AIs; the standing-order card in the co-play frame.
- Downscaled review copies are in the session scratchpad (`review-r2/`), not in the repository.

## Item 1: captioned mobile store sets

### What is now right

- **The layout problems of round 1 are fixed.** Captions are bold and readable at 240 px in every script checked, including Thai, Devanagari, Tamil, Arabic and Persian (with Persian digits). The card runs to 93–94% of the width and bleeds off the bottom, so gameplay fills most of each slide. The card edge is visible. One caption size per set and locale. Bands are 16–17%, under Play's 20%.
- **The fair-deal slide** now has its own capture, keeps the night background, and sets the caption in gold inside a gold ring. It reads as part of the set, not as an advert.
- **Clean-state protocol works.** No zone squares anywhere. Event lists are one or two rows, mostly green. No negative first stat in any mobile gameplay frame. Health and food bars are off.
- **Phone hero and economy are what round 1 asked for.** The hero has whole pools, racetracks, inns and hundreds of globs, with the lower third filled. Economy has a non-upgrading Inn selected with Food 31/50 beside a lit wheat field and swarms.

### What still holds it back

1. **The opponents slide (last in every set) is a menu.** At thumbnail size it is a pale beige rectangle in a set of dark green scenes, so it is the first thing the eye lands on when swiping. It also shows the AI tournament ratings ("Numbi - Easy (1204)"), which the claims file says not to quote, and a ninth entry "Inactive - No AI orders" under an "8 computer opponents" caption. On iPad the menu fills only the top half of the card; the bottom 40% is empty beige.
2. **No action in the first three slots.** Hero, build and fair deal are all the same red colony at peace. The App Store shows the first three portrait screenshots in search results, so as ordered a searcher sees no fight at all. This breaks the user's rule more than any single frame does.
3. **Sameness.** On phones five of six gameplay frames are the same red colony on the same green grass (the "A big pond" save); at 240 px hero, build, fair deal and economy look alike. Acceptable for this upload, not ideal.
4. **Tablet battle frames are thin and dark.** The 7-inch, 10-inch and iPad battle frames have 41–46% of the map fog-dimmed and roughly 15–30 warriors scattered in small groups. At 200 px the 10-inch and 7-inch battle slides read as dark camouflage with specks. They pass, but they are the weakest gameplay slides.
5. **Android host renders** are visibly softer than the iOS simulator frames, and carry a flat navy strip about 30 px tall along the top of the map, visible at the card's top-left corner on the tablet sets (round-1 product issue, still there).
6. **The iPhone fair-deal frame** is about 55% sea and a fog-dimmed wheat field; the colony is in the bottom third.

### The specific questions

**(a) Opponents slide: drop it, in every set and every locale.** It fails the footage rule ("no menu screens as gameplay shots") and the user's rule, it is the visually loudest slide for the wrong reason, it quotes AI ratings, it lists nine entries under "8", its panel is entirely English text in 44 non-English listings, and on iPad it carries the JavaScript line in (b). Moving it earlier would be worse. Keep "8 computer opponents" in the description and feature bullets, where it is true and costs nothing. Without it every set still meets its store minimum: iPhone 6 slides, every other set 7.

**(b) iPad "Add JavaScript AIs in Settings → Custom AIs": yes, it misrepresents the iOS app; do not show it on the App Store.** I checked the source. The App Store build (`client_profile` free, `distribution` app_store) sets `community_ai` off, which removes the Settings → Custom AIs page (`src/ui/settings/SettingsScreen.cpp` line 214 on `origin/master`). But the lobby caption is not gated: `src/game/screens/CustomGameScreen.cpp` line 1555 adds it for every non-room lobby. So the screenshot is a faithful picture of the real App Store build, and the real build has a bug: it points players to a settings page it hides. On the listing it would advertise a feature that the [claims file](../../../facts/storefront-v2-claims.md) bans on Apple. Dropping the slide (a) removes it from the listing. Separately, the game should wrap that caption in `if constexpr (ClientFeatures::CommunityAI)`; that is a product fix for the game's owner, not a listing blocker. The iPhone opponents frame does not show the line (the open dropdown covers it). The Android and Amazon builds keep `community_ai` on, so the line is true there, but the slide is dropped anyway.

**(c) iPhone has no battle slide: use the iPhone territory capture as the battle slide.** `captures/mobile/iphone-6.9/05-territory-1320x2868.png` is the best fight on any phone: a blue line and a red line facing each other across the centre, about 15 blue and 25 red warriors, two war flags, a lit field, one red event row. It meets the battle test better than the Android phone battle frame does. Give it the `battle` role ("Fight for the land") and put it in slot 2. The iPhone then has no territory slide; nothing is lost, because the territory slides on the other sets show the same fight with the Flags palette open, and "Choose where to expand" was only partly true of them (no range circle). Six iPhone slides is within Apple's 1–10 and above the comparables' iPhone low end (5).

**(d) English game interface in 45 locales: acceptable for this upload.** Neither Apple nor Google requires the in-app language to match the listing language, and the comparables and most ports ship one set of gameplay frames under localized captions. In the gameplay frames the English is small: one event row, the tablet side-rail labels (Build, Flags, Tools, Goals, Teams, Menu), the phone Flags palette (Clear, Guard, Forbid) and the Inn card. The one slide where English dominates is the opponents menu, which is dropped. Nice to have later: re-capture the top-tier locales (de, fr, es, pt-BR, ja, ko, zh-Hans, ru) with the game set to that language, since the game ships those catalogues (incomplete, per the claims file, so check for English fallbacks in the frame).

**(e) Hungarian fair-deal break: real, and not only Hungarian.** The phone and F-Droid renders wrap greedily, so a short conjunction ends line 1 in **12 locales**: hu "Se reklám, se | in-app vásárlás", bg "Без реклами и |", eo "Sen reklamoj kaj |", fil "Walang ads o |", id "Tanpa iklan dan |", ms "Tiada iklan atau |", nl "Geen reclame of |", pt-BR and pt-PT "Sem anúncios ou |", sr-Cyrl "Без реклама и |", tr "Ne reklam ne |", sw "Bila matangazo wala |". iPad Hungarian already breaks well ("Se reklám, | se in-app vásárlás"). The other five captions wrap acceptably in all 45 locales on iPhone; Catalan territory ("Tria | on expandir-te") is the only other awkward one and can be left. Fix in the renderer, not per catalogue (must-fix M3).

### Round-1 mobile findings: status

| Round-1 finding | Status in round 2 |
| --- | --- |
| Event log 4–8 rows over the colony | **Fixed.** At most two rows, mostly one, mostly green. |
| Zone squares in 11 of 43 frames | **Fixed.** None. |
| Fog-dimmed, empty ground | **Fixed for colony frames** (under 15%). **Remains** in battle and territory frames (17–46%); a player view has no fog toggle. |
| Negative first stat in a red outline | **Fixed.** |
| Phone HUD takes 40% of the image | **Improved** by the layout (card 94%, bottom bleed); the stats block itself is unchanged (product). |
| Battle: small groups on dark ground | **Partly fixed.** Larger fights with hit effects on iPad and Android; still fog-dimmed and scattered. iPhone has no battle file, but its territory frame qualifies (c). |
| Economy shows a control panel, not food | **Fixed.** Inn card with food lines, wheat field, swarms. |
| Phone hero: buildings under the log, empty lower third | **Fixed.** |
| Territory: War Flag inspector, "0 / 0 HP" | **Fixed** as far as the game allows: palette open, flag just placed, warriors answering; no range circle (impossible with the palette open). |
| Maps: no frame for "23 maps" | **Acceptable.** A visibly different map (FourSquares, sea with algae, violet forest). |
| Opponents: no frame | **Not fixed** (menu screen). Dropped (a). |
| Spare frame for fair deal | **Fixed.** |
| Android emulator or device captures | **Not done.** Interim host renders remain. |
| iPad landscape | Not done; not needed. |
| Stop producing iPhone landscape, phone landscape, 10-inch portrait, map peek, War Flag inspector | **Done.** |
| Product issues: log cannot be dismissed, low-resolution stat icons, navy strip on Android tablet renders | **Remain** (product). |
| Layout 1–6 (bold weight, more room, visible card edge, one size per set, bands, fair-deal variant) | **All fixed.** Line count still differs between slides of one set (one line or two); acceptable. |

## Item 2: clean desktop gallery

### Per frame

| Frame | Verdict | Notes |
| --- | --- | --- |
| `01-hero-marchland-colony-under-raid` | **keep: lead image** | What round 1 asked for. A dense red colony at 100% with a purple raid meeting red warriors at its right edge, the purple swarm lower right. The fight reads at 600 px. Right third fog-dimmed; two red event rows. |
| `02-build-coral-school-site` | keep | Site selected with materials and Working slider, assigned workers ringed and walking in. The caption is true. No placement preview (impossible on desktop with a site selected). |
| `03-economy-coral-inn-and-wheat` | keep, but late in the gallery | Inn at Food 9/10, wheat on both sides, swarm above. At 600 px it is nearly the same picture as `02` (same island). |
| `04-battle-honeycomb-oasis` | **keep** | The most distinctive frame: red against lime round the oasis at 150%, hit flashes, the lime swarm at the right. Readable at 600 px. The red "-9/175" is about 9 px tall at 1920 wide; leave it. |
| `05-territory-crater-lakes` | keep, late slot | Pretty, distinct map, but at 75% the violet forest pattern dominates and the push between the colonies is hard to find at 600 px. |
| `06-maps-city-states` | **keep** | Unmistakably a different map: roads, walls, lava ground, cyan colony. |
| `07-opponents-marchland-spectator` | **drop** | About half of the frame is open grass; no fight; small colonies. The spectator side panel lists the AIs in lower case ("maxima, cortex, maxima, cortex"), which looks unfinished. If it stayed, every caption field would also need a "spectator view" label. |
| `08-ai-coplay-in-game-coral` | keep, with a follow-up | The game's own standing-order card (name, Active, Pause, Cancel) and the agent's war flag among the warriors. Honest and gameplay-only. Weak as a picture: half the frame is water, the card is small, its output line is raw JSON, and at 600 px the co-play is invisible. A small black unexplored tile shows at about (2310, 680). |
| `08b-ai-coplay-side-by-side-coral` | keep after fix M4 | Reads as "a session log next to the game" at 600 px, which is the point. But the panel ends on "status: queued" and "orders sent: 0", so the visible evidence says the agent has not done anything yet. |
| 16:10 twins | keep (same verdicts) | Same zoom as the 16:9 frames, as asked. The 16:10 hero shows four event rows. |

### The specific questions

- **Battle frame's red negative stat: ship it.** It is the real interface and tiny at display size; the scene is the strongest action frame in the set. Replace only if a positive-stat clash of equal size turns up.
- **Opponents as a labelled spectator view: drop it** (above). The footage rule permits spectator footage when labelled, but this moment is not exciting and the gallery does not need it.
- **Build and economy both on Coral:** keep both only in galleries of seven, never next to each other. Where a store shows five or fewer, keep build and drop economy.
- **Which co-play image where:**

| Store | Co-play image | Why |
| --- | --- | --- |
| Microsoft Store | `08` | Microsoft bars added content inside screenshots; `08` is pure game. MCP is "safe with caveat" there. |
| Steam, GOG (prepared) | `08` | Steam screenshots must show gameplay only; `08` is the game's own interface. |
| itch.io, Snap, AppStream/Flathub | `08b` (after M4) | These take a second panel without difficulty; scope the caption to the desktop downloads on itch.io. |
| Epic | **neither** until the Epic artifact is 0.11.6.2 or newer (claims R8) | MCP held. |
| Mac App Store | **neither** until a sandboxed-build MCP check passes (claims R7) | MCP held. |
| Every mobile store | never | MCP is desktop-only. |

- **Honesty note on the co-play images, for the coordinator.** The "agent" in these sessions is a scripted MCP client (`tools/agent-session.py`), not a language model; the standing order's JavaScript was written by the capture engineer. The README says so. The calls and the game's responses are real and are exactly what an agent's would be, so the images are a fair picture of the interface. Keep the README and manifest wording as is, and do not describe these images anywhere as a model's decisions.

### Round-1 desktop findings: status

| Round-1 finding | Status |
| --- | --- |
| Health and food bars everywhere | **Fixed.** |
| Guard grids and war-flag circles over fights | **Fixed.** |
| Negative first stat in 11 of 15 frames | **Fixed** except the battle frame (accepted). |
| Event rows | **Fixed** (two or fewer) except the 16:10 hero (four). |
| Lead and battle zoom | **Fixed** (100% and 150%). |
| Right-hand column two-thirds empty | Remains (real interface). |
| One map dominates | **Fixed** (five maps); Coral carries build, economy and co-play. |
| AI names in panels ("Inn (Maxima)") | Remains; acceptable. |
| Re-capture 2, hero with conflict | **Fixed.** |
| Re-capture 3, build | **Fixed** (no placement preview; impossible with a site selected). |
| Re-capture 4, economy | **Fixed**; the README now states which sprite is wheat. |
| Re-capture 5, three colours in one view | Answered with a spectator view, which I drop. |
| Re-capture 6, battle without overlays | **Fixed.** |
| Re-capture 7, territory lit | **Fixed**, but the frame is muddy at thumbnail size. |
| Re-capture 8, AI co-play | **Done**, both forms; `08b` needs M4. |
| Re-capture 9, 16:10 at the same zoom | **Fixed.** |

## Item 3: key art

### Concept A versus B and C

**A (shoreline colony) is the right main image of the three.** At 460×215 and 231×87 it is the only one that reads instantly as "a living colony", the red globs stand out on the grass, and the water L gives the wordmark a calm ground in every crop from 3:1 to 2:3. B's lime globs vanish on green and its plate still has unit bars. C is the only one with a fight, but at capsule size the fight is a few specks round a pond, the sand and stone read as terrain rather than a game, and the bottom-placed wordmark sits where store UI overlays.

A's real weakness is that it is peaceful, against the user's "exciting action" rule. It is still the better store image today, and the comparables at this genre (Factorio, Mindustry) use exactly this kind of dense, calm, top-down scene. The fix is a better plate, not a different concept: the desktop hero (`01-hero-marchland-colony-under-raid`) proves the raid-at-the-colony-edge moment exists, and Marchland has water at the top-left of that view. A concept D shot from that moment at 150% would carry both colony and conflict. That is a next-round item, not a blocker.

### Derivatives (concept A)

All 28 files checked at their store display size; the Play feature graphic and Microsoft poster also at full size. Every derivative is a downscale of native pixels; sprites are crisp, with no upscaling softness or JPEG blocking. The wordmark is legible in every one, including the 231×87 Steam small capsule, where it fills about 79% of the width.

| Store and file | Result |
| --- | --- |
| Google Play feature `google-play-feature-1024x500.jpg` | No "free", price or ranking text; no icon repetition; nothing important under the centre play button. **The wordmark's right edge is 55 px (5%) from the right edge and its top about 58 px from the top**: too close to the edge for a graphic Play crops and overlays (M6). |
| Microsoft poster 1440×2160 | Name in the top quarter; bottom third free of text. Good. |
| Microsoft box art 2160² and 1080² | Good. |
| Microsoft super hero 3840×2160 and 1920×1080 | Text-free, no UI. Good. |
| Snap banner 1440×480 | Good; wordmark on water. |
| itch.io cover 630×500 | Good. |
| Epic offer landscape 2560×1440, portrait 1200×1600 | Logo and key art inside the critical area. Good. |
| Epic product logo 960×540 | Legible on dark and light grounds. The wordmark's 2.8:1 shape leaves empty space above and below; acceptable. |
| Epic social preview 1200² | Good. |
| Steam header, small, main, vertical and library capsules | Art and name only, no other text. Small capsule meets "logo should nearly fill it". Good. |
| Steam library hero 3840×1240 | Text-free, as Steam requires. Good. |
| Steam logo `steam-logo-1280.png` | **The file is 1326×224**, not 1280 wide as named. Fix before Steam upload (Steam is prepared only). |
| GOG banner, logo, box, backgrounds | Good (GOG rules not confirmed in this project). |
| Open Graph 1200×630, promo tile 1024² | Good. |
| **Amazon promotional image 1024×500** | **Missing** (optional). After M6, the Play feature graphic also meets Amazon's "name included, no descriptive text, text at least 50 px from the edges", and can be reused. |

### Round-1 key-art findings: status

| Round-1 plate spec | Status |
| --- | --- |
| 150% zoom | **Met.** |
| At least 4256×2600, every crop a downscale | **Met** (4396×2600). |
| Subject: colony edge under attack, 15 or more units a side with hit flashes | **Not met.** Peaceful (README says so). |
| Calm L of water for the wordmark | **Met** (mirrored to the top-right; fine). |
| Focal cluster in the central square; nothing essential in the outer 15% | **Met.** |
| Clean state (no HUD, bars, zones, circles, selection, clouds) | **Met.** |

## Final galleries

Order is left to right as the store shows it. Mobile file names are the current English renders; after the re-render the numbers change but the roles stay.

### Mobile (captioned sets)

| Store set | Slides, in order | Count |
| --- | --- | --- |
| App Store iPhone 6.9 (`apple-iphone-6.9`) | hero · **battle** (the `05-territory` capture, re-captioned) · fair deal · build · economy · maps | 6 |
| App Store iPad 13 (`apple-ipad-13`) | hero · battle · fair deal · build · economy · territory · maps | 7 |
| Google Play phone (`google-play-phone`) | hero · battle · fair deal · build · economy · territory · maps | 7 (all 9:16, qualifies for the three-image rule) |
| Google Play 7-inch tablet (`google-play-tablet-7`) | hero · battle · fair deal · build · economy · territory · maps | 7 |
| Google Play 10-inch tablet (`google-play-tablet-10`) | hero · battle · fair deal · build · economy · territory · maps | 7 |
| Amazon (`amazon-tablet`) | Same seven as the 10-inch set, **after** device or emulator captures replace the host renders (M8). Promotional image: the Play feature graphic after M6. | 7 |
| F-Droid phone (`fdroid-phone`) | Same seven as Google Play phone | 7 |

Opponents is in none of them.

### Desktop (clean frames; captions only as text fields where the store has them)

| Store | Images, in order | Key art |
| --- | --- | --- |
| Microsoft Store (now) | `01` hero · `04` battle · `02` build · `08` co-play · `06` maps · `05` territory · `03` economy (3840×2160 PNG; `shot_caption_*` in the caption field) | poster 1440×2160, box art 2160² and 1080², super hero 3840×2160 and 1920×1080 |
| Snap (now) | `01` · `04` · `08b` · `02` · `06` | `snap-banner-1440x480` |
| AppStream / Flathub source (now) | `01` · `04` · `08b` · `02` · `06` · `05` · `03`, each with its `shot_caption_*` | none |
| itch.io (now) | `01` · `04` · `08b` · `02` · `06` · `05` · `03` | `itch-cover-630x500` |
| Epic (when its review clears) | trailer first, then `01` · `04` · `02` · `06` · `05` · `03` as 1920×1080 JPEG under 4 MB; **no co-play** until R8 clears, then add `08` after `02` | offer landscape and portrait, product logo, social preview |
| Mac App Store (when its review clears) | 16:10 2880×1800: `01` · `04` · `02` · `06` · `05` · `03`; **no co-play** until R7 clears | none in this set |
| Steam (prepared) | `01` · `04` · `02` · `08` · `06` · `05` · `03` (1920×1080 or larger, no captions) | header, small, main, vertical and library capsules, library hero, logo (after resizing to 1280) |
| GOG (prepared) | As Steam | banner, logo, box, backgrounds |

## Fix list

### Must fix before upload

Owners are by file: `captures/mobile/selection.json` and `captures/desktop/selection.json` belong to the capture engineers; `tools/screenshots.py` and `tools/gallery.json` to the compositor; `key-art/` to the key-art agent; `facts/` and `translations/` are not touched by any fix below.

- **M1. Drop the opponents slide from every mobile set.** In `captures/mobile/selection.json`, delete the `"role": "opponents"` entry from all five device classes. Remove the two now-unused `slot_trim` entries for `07-opponents-1320x2868.png` and `08-opponents-2064x2752.png` in `tools/gallery.json` if `check-config` objects to them. Re-render English and all 44 locales; run `screenshots.py verify` for every locale. Done when no store set in any locale contains an opponents image.
- **M2. Put a fight in slot 2, and give the iPhone a battle slide.** In `captures/mobile/selection.json`:
  - `iphone-6.9`: change the role of `05-territory-1320x2868.png` from `territory` to `battle`, and order the class as hero, battle (that file), fair_deal, build, economy, maps.
  - Every other class: order as hero, battle, fair_deal, build, economy, territory, maps.
  - Check that the renderer follows `selection.json` order. If it still forces `asset_text.mobile_gallery_order` from `translations/platforms.json`, ask the coordinator to change that list to hero, battle, fair_deal, build, economy, territory, maps rather than editing it yourself. Done when slot 2 of every set, in every locale, is "Fight for the land" over a fight.
- **M3. Two-line wraps must not end line 1 with a conjunction.** In `tools/screenshots.py`, when a caption needs two lines, choose the break in this order: (1) after punctuation (`,` `.` `;` `、` `。` `，` `،`) if both lines then fit; (2) otherwise the most balanced break that does not leave a word of four or fewer letters at the end of line 1; (3) only then the greedy break. Do not change scripts without spaces (ja, zh, th), which already wrap acceptably. Re-render and check the fair-deal band in all 45 locales on iPhone, Google Play phone, F-Droid and iPad. Done when hu reads "Se reklám, / se in-app vásárlás" and bg, eo, fil, id, ms, nl, pt-BR, pt-PT, sr-Cyrl, tr and sw no longer end line 1 with и, kaj, o, dan, atau, of, ou, ne or wala.
- **M4. The `08b` transcript panel must end on the agent's action.** Re-run `tools/coplay-side-by-side.py` with a transcript that includes a later `hive_program inspect frontline-flag` call from the same session whose output shows the flag being placed or moved (`"moved":[…]`) and orders sent of at least 1. Drop the second `hive_status` call to make room. If that session's transcript has no such call, record a new session with the same recipe and remake both the frame and the panel from it. Done when the last block in the panel shows the standing order acting, and the flag it names is visible in the game half.
- **M5. Desktop gallery files.** In `captures/desktop/selection.json`, remove `07-opponents-marchland-spectator` and order the entries 01, 04, 02, 08, 06, 05, 03. Produce 1920×1080 sRGB JPEG exports (quality 90, under 4 MB each, no alpha) of `01`–`06`, `08` and `08b` for Epic and any web store with a per-file cap; keep the 3840×2160 PNGs (5–11 MB) for the Microsoft Store and Steam. Check Snapcraft's and itch.io's current screenshot size limits before upload; I did not confirm them.
- **M6. Google Play feature graphic: move the wordmark in from the edge.** In `key-art/build-assets.py`, re-frame `google-play-feature-1024x500.jpg` so the wordmark is at least 80 px from the right edge and at least 60 px from the top, at the same or slightly smaller width (about 60% of the image). Check it at 512 px wide. Then reuse it as the Amazon promotional image, which needs text at least 50 px from every edge.
- **M7. Correct the build provenance.** `captures/desktop/README.md` ("Captured … from the public release 0.11.7.0") and `key-art/README.md` ("public release 0.11.7.0") describe `/Applications/Glob2.app`, whose own manifest records revision `5bf966285aa8`. The claims file (R13) says that build is 0.11.7.0 plus 15 commits and not the public release binary. Write "Globulation 2 0.11.7.0 + 15 commits (revision 5bf966285aa8), the installed build; maps, AI roster and simulation identical to the v0.11.7.0 tag" in both READMEs and any manifest field that says "public release".
- **M8. Amazon: no host renders.** Amazon asks for the app shown on the right device type. Before the Amazon upload (deferred anyway), replace the `android-tablet-10` host renders used by `amazon-tablet` with emulator or Fire-tablet captures, and re-render.
- **M9. Coordinator check before the Google Play upload.** The mobile captures show the 0.11.8.0 touch interface. The claims file (R6) records Google Play's closed test at 0.11.2.0. Confirm which build Play users will install when these screenshots go live; if it is older than 0.11.7.0, either hold the screenshot upload or confirm that the interface in the frames matches that build.

### Should fix (next capture round; not blocking)

- **S1. Tablet battle frames** (iPad, 7-inch, 10-inch): re-shoot at first contact with the camera moved toward the lit (attacking) side so no more than 25% of the map area is dimmed, and at least 20 warriors of each colour are in one cluster. If a lit fight inside the red colony can be found late in a match, prefer it.
- **S2. Android navy strip.** Trim the flat navy strip along the top of the Android host renders (about 32 px on tablets; check the phone renders too) through the `trim` setting for those sizes in `tools/gallery.json`, or remove it at capture.
- **S3. iPhone fair-deal frame.** Replace with a frame in which colony buildings fill at least the lower two-thirds of the card and no more than a quarter is sea.
- **S4. Desktop co-play `08`.** Re-shoot at 125–150% centred on the agent's flag and the enemy contact, with the standing-order card in frame and less than a quarter of the frame water; avoid the black unexplored tile.
- **S5. Game bug (for the game's owner).** Gate the lobby caption "Add JavaScript AIs in Settings → Custom AIs…" (`src/game/screens/CustomGameScreen.cpp`, line 1555 on `origin/master`) behind `ClientFeatures::CommunityAI`, so App Store builds stop pointing to a hidden page.
- **S6. Steam logo.** Resize `steam-logo-1280.png` to 1280 px wide (it is 1326).

### Nice to have

- **N1. Key art concept D** from the Marchland raid moment (see Item 3), at 150%, clean state, water top-left for the wordmark; if it reads at 231×87, make it the main image.
- **N2. A mobile hero with a fight at the colony edge.** The current mobile heroes come from a match the colony has nearly won.
- **N3. More map variety on mobile**: one more map for the fair-deal or build slot, so the phone thumbnails stop looking alike.
- **N4. Localized in-game UI** for the top-tier locales (de, fr, es, pt-BR, ja, ko, zh-Hans, ru).
- **N5. 16:10 hero** with two or fewer event rows.
- **N6. Product issues** the captures keep showing: the event list cannot be dismissed, low-resolution stat and palette icons on phones, raw JSON as the standing-order card's output line.

## Decisions for the coordinator

1. Accept dropping the opponents slide (mobile) and the spectator frame (desktop), and keeping "8 computer opponents" in text only.
2. Confirm the Google Play build version before uploading phone and tablet screenshots (M9).
3. Accept concept A as the main store image now, with concept D as the follow-up (N1).
4. If the renderer cannot follow `selection.json` order, approve the `mobile_gallery_order` change in `translations/platforms.json` (M2).
5. Note that the co-play sessions used a scripted MCP client in the agent's place; no image or text should describe them as a model's decisions.
