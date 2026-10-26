# Character correction study prompts

Built-in `image_gen.imagegen` used on **2026-10-26**, first for generation, then an identity-correction edit. No CLI/API fallback was used. The corrected study is review-only, awaiting user character feedback; no cover is approved.

## Initial landscape generation

Inputs, in exact tool order (`referenced_image_paths`; local workspace roots normalized):

1. `glob2-online-website/public/images/home-thriving-colony.webp` — game world/building reference.
2. `glob2-design-system/assets/colony-1600.webp` — terrain/resource palette reference.
3. `glob2-design-system/assets/worker-east.webp` — worker sprite strip; its anatomy was misread in the prompt.
4. `glob2-design-system/assets/inn.webp` — building identity reference.

`transparent_background: false`. Rejected generated output: `exec-aed4777b-2525-4341-814d-e106b1c68433.png`. That output had muscular humanoid creatures and is not retained in this pack.

Exact prompt:

```text
Use case: ads-marketing.
Asset type: landscape video game store key art, 16:9, 2560 by 1440 pixels.
Primary request: create a polished full-bleed promotional illustration for Globulation 2, an unusual organic colony-building real-time strategy game. This is a game cover painting, not a presentation layout and not a screenshot.
Input images: Image 1 home-thriving-colony is subject and building design reference; image 2 colony-1600 is terrain/resource palette reference; image 3 worker-east is exact creature identity reference; image 4 inn is exact building identity reference. Reinterpret these real game elements as coherent richly detailed illustrated key art; preserve their strange simple forms.
Scene: elevated oblique view over a sprawling productive alien colony beside cobalt-violet water edged with golden-yellow sand. Rounded tan organic hollow ring/stump buildings with green interiors, odd globular pools and a few crystal/spire structures are distributed among dense pink/lilac tapered crystal-like trees and patches of tiny red, yellow, orange and green round food resources. Busy organic economic life is the hero. Numerous purple globs move between food groves and buildings, with three larger readable globs in foreground making the world tangible. Globs are simple hunched soft round eyeless alien bipeds like the worker reference, no human clothes or equipment, no cute cartoon eyeballs. Foreground resource gathering and midground settlement activity form a sweeping diagonal into a much larger colony across the valley. Subtle distant rival-colored colony on far bank only, no battle scene.
Style: excellent illustrated strategy game box art, painterly crisp shapes, strong silhouettes, atmospheric depth and warm late-afternoon rim lighting, saturated natural greens with purple/cobalt accents, sophisticated lively composition. Preserve recognizable game building silhouettes, not medieval cottages, human architecture or generic fantasy.
Composition: one continuous edge-to-edge world illustration. The colony fills the image; strong foreground/midground/background depth. Upper center 20 percent relatively quiet darker forest/haze forms so an existing title can later be overlaid without a rectangular panel; do not leave a blank band. Most colony activity below and around that area. Readable at thumbnail size.
Text: absolutely no text, letters, logos, titles, watermark or interface; the exact existing game title will be added separately.
Avoid: slide design, graphic panels, inset screenshots, borders, marketing copy, icons, charts, UI/HUD, wheat farms, machinery, beavers, humans, castles, armies, dramatic combat, generic sci-fi, photorealism, clay toy render, disconnected collage.
```

## Corrective identity edit

Inputs, in exact tool order (`referenced_image_paths`; local workspace roots normalized):

1. Rejected initial landscape generated output above — edit target.
2. `/tmp/glob2-character-source-audit.png` — temporary source audit board with original-derived worker/warrior/explorer, website worker/warrior sprites and stylized project icon. It is a source comparison, not a generated character design.
3. `glob2/datasrc/gfx/production/original-derived/unit256r.png` — original worker source render.

`transparent_background: false`. Corrected output `exec-ca00a7a8-cfae-4f06-ab0f-cbcaef644ddd.png` is copied byte-for-byte to [character-correction-study.png](character-correction-study.png).

Exact prompt:

```text
Use case: identity-preserve.
EDIT TARGET: Image 1 is the landscape colony artwork. Correct the character anatomy throughout it. KEEP the existing colony environment, camera, composition, lighting, buildings, food patches, crystal groves, shores and color palette. Change only the creatures and their immediate contact with food/ground.
IDENTITY REFERENCE: Image 2 is an authoritative source audit board of the REAL Globulation 2 creature anatomy. Image 3 is the original worker source render. The bottom-right icon on Image 2 gives the clearest silhouette: one continuous central oval/ellipsoid joined by FOUR narrowing tapered branches to FOUR smooth rounded terminal lobes. This is a soft living branching/metaball organism, not a humanoid. Match the recognizable branched silhouette exactly, with asymmetrical extension/contraction like source sprites.
REPLACE all three large purple foreground humanoids and every smaller purple colony creature with this source-form organism. Maintain purple team color. The four terminal lobes are rounded blobs, not hands/feet. No separate head, neck, shoulders, torso/waist, elbows/knees, digits, eyes, face or musculature. Do NOT merely remove facial details from a human. Do NOT create a head above a muscular body. The entire organism is a continuous oval with four tapering lobe connections, like the supplied blue project icon brought to life in purple.
Foreground poses: keep three visible organisms near food gathering. One leans its continuous central oval toward food with rounded terminal lobes contacting resources; another moves across the field with one branch extended and one compressed, and third bends its branching soft body. They may cradle a few round fruit resources between terminal lobes without any human hands/fingers. Preserve a clear readable four-lobed branching silhouette in each, allowing normal perspective occlusion. No fist shapes or bodybuilding.
Render in the existing painterly light/material quality, purple smooth soft skin with modest organic shading. No new text, logos or UI. Don't change the environment. Correct all creatures, not only the largest one.
```
