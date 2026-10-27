# Illustrated colony environment prompt

Prepared 2026-10-26 using the built-in image-generation tool. One successful generation; no CLI/API fallback and no generated creature anatomy.

## Ordered image inputs

1. Website `public/images/home-thriving-colony.webp` — actual-game world/architecture reference, not a composition to copy.
2. Design-system `assets/swarm.webp` — original spired hive reference.
3. Design-system `assets/inn.webp` — original ring-shaped organic building reference.

The generated file was retained unchanged as `environment-native.png`. Actual units and the existing wordmark were then composed by [the native asset script](build-assets.py).

## Exact prompt

```text
Use case: ads-marketing
Asset type: premium videogame store key art background, landscape 16:9
Primary request: create an art-directed full-bleed illustrated world for Globulation 2, a real-time strategy game about building a thriving autonomous colony in contested territory. This is ENVIRONMENT key art only. No text and absolutely NO creatures or characters: exact game units will be composited later.
Input images: image 1 is actual game reference for the organic architecture, food patches, vegetation, violet/blue water and colony logic, not a composition to copy; image 2 is the authentic spired hive architecture; image 3 is the authentic hollow ring-shaped inn. Preserve these distinctive forms when illustrating the world.
Scene: a broad productive alien colony in a green valley, seen from an elevated oblique viewpoint. A single recognizable organic spired hive with a softly luminous violet core is the main landmark, centered in the lower-middle. A network of low tan hollow organic ring structures surrounds it, with rich green inner sleeping/feeding surfaces as in the reference. Round red/orange/yellow food patches and pale lilac tapered tree/crystal groves follow the landscape, expressing an organized productive colony. A cobalt river and golden shoreline wind into the distant landscape; a few distant colony structures suggest contested land.
Composition: the upper 30 percent should be quiet dark teal-violet sky and distant atmospheric mountains with very little high-contrast detail, deliberately reserved for a large title added later. Occupied world fills the remaining lower 70 percent. The strongest colony landmark and economic world forms sit in the central 40 percent of the frame so that a beautiful vertical portrait crop remains possible. Large foreground silhouettes of crystal vegetation, fruit and a partial organic building frame the colony at the bottom corners and give depth; NO giant character. Make one clear focal point and readable large shapes. Do not spread equal visual contrast across every detail.
Style: polished painterly videogame cover illustration with disciplined cinematic light and rich crafted surface detail, exciting but source-faithful organic alien architecture. Warm light catches the hive and productive colony; cooler shadow frames the edges. Jewel violet, fresh green and deep blue grounded by earthy tan and warm gold. Favor clear forms, spatial depth and atmosphere over candy-like gloss or visual noise.
Constraints: no creatures, no people, no globs, no silhouettes shaped as characters, no animals, no humanoids, no military troops, no weaponry, no human cottages, no medieval castle, no factory machines or invented pipes. No title/text/logo/watermark, no slogan, no UI, no inset, no border, no slide layout. It must feel like a videogame WORLD cover, not an infographic or an empty landscape.
```
