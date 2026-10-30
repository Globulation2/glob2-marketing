# Epic page presentation — local review

[Profile copy](../../planning/epic-store-profile-v1.md) · [Epic requirements](../../planning/epic-store-requirements.md) · [Positioning](../../analysis/positioning-v1.md)

Prepared **2026-10-26** to review the store presentation as a whole: cover, genuine game gallery, short pitch, offer hierarchy and concise About sections. This is a local static mockup inspired by Epic's product-page structure, **not an official Epic screenshot, live listing, submission or custom site for publication**. Exact portal layout may differ.

## Open locally

From the repository root:

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8766/assets/epic-page-preview/` in a browser. The gallery thumbnails switch the hero image; the Get action is disabled. There are no network dependencies, analytics, forms, purchases or external actions. No developer/publisher identities, ratings, review scores, release dates, language counts or hardware specifications were invented.

The proposed Free/Windows offer follows the existing Epic preparation record. It is labeled as a proposal, rather than verified availability. Genre/focus terms are descriptive and do not imply they are exact Epic tags.

## Content and provenance

Copy derives from the [selected positioning](../../analysis/positioning-v1.md) and [Epic description draft](../../planning/epic-store-profile-v1.md), shortened for scanability. The colony economy remains central. The expanded gallery now shows five distinct roles: **Cover, Colony, Battle, Strategic view and Lava Shield**.

| Current media | Source and context |
| --- | --- |
| [Illustrated cover](../epic-v5/README.md) | Promotional key art: generated environment, existing title and exact source-unit silhouettes. It is not a gameplay screenshot. The sidebar logo uses the same pack. |
| `media/colony.webp` | Unchanged website `public/images/home-thriving-colony.webp`, revision [6e391ebe](https://github.com/Globulation2/glob2-online-website/tree/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1). Actual Fingerprint / Quick clash replay recorded 2026-10-11, tick41350, fog disabled and outer HUD cropped. It is not a fresh Epic Windows capture. |
| [Battle](../epic-gallery-v3/lava-shield-battle.jpg) | Native GameGUI output of a staged in-engine scenario with opposing warrior forces and actual combat stepped before capture. It is not a frame recovered from an ordinary completed match. |
| [Strategic view](../epic-gallery-v3/lava-shield-strategic.jpg) | The same staged scenario rendered through the native strategic-overview GUI, showing territory, building icons and unit markers. This demonstrates the actual overview presentation rather than substituting a flat map export. |
| [Lava Shield terrain in use](../epic-gallery-v3/lava-shield-terrain-in-use.jpg) | A closer native view of the staged scenario, showing colony activity and units in the lava terrain. Replaces the similar whole-map framing on 2026-10-30; the strategic view remains unchanged. |

The [staged capture pack](../epic-gallery-v3/README.md) records the scenario setup, actual combat observations, native renderer/HUD, source identities and export treatment. The scene was composed in the engine with real game units, buildings and terrain. No unit graphics, combat effects or interface elements were painted into the screenshots. It does not establish natural-match prevalence, player demand, game performance or Epic Windows launcher qualification.

The spatial About image uses the populated strategic view, and the defence section has the battle image. On **2026-10-30**, the spatial copy was broadened to explain how different maps call for different strategies; Lava Shield remains the illustration rather than the subject of that section. Lava Shield's crater, branching flows and crossings are supported by the [map guide](https://github.com/Globulation2/glob2/blob/53110681a31d08423568afe26d5b8d8f9ac45dd1/docs/map-generators/lava-shield.md). The [map capture pack](../epic-gallery-v2/README.md) retains the superseded whole-map export and its separate generation/render provenance.

The old `media/expansion.webp` and `media/defence.webp` files remain historical source copies but are not referenced by the page. The [abnormal-fog controls image](../epic-gameplay-v1/README.md) also remains excluded. Earlier coastal/Four Squares renders were rejected as battle evidence; algae resources are not armies. The v5 [provenance record](../epic-v5/README.md) and [source asset ledger](../../facts/assets.md) retain art/attribution context. This local review does not complete release rights clearance.

## Remaining production work

The requested battle and populated strategic-view roles are now prepared as representative native scene captures. Capturing a naturally developed match remains a separate possible replacement, rather than the provenance of these images. Review the gallery and copy in Epic's actual fields/crop preview, confirm release-specific rights and metadata, and qualify the Windows build before submission. Nothing in this local review authorizes uploads or publication.

## Visual checks

Rendered in the local browser at 1600×1100 desktop and 390×844 mobile. The mobile document has no horizontal overflow, and all images load. Gallery interaction switches the hero and updates selection state. The rejected controls image and retired expansion/defence crops are absent from both gallery and About. The Get control remains disabled. No custom fonts are bundled; typography uses the system font stack.

- [Desktop overview](desktop-overview.png)
- [About section](about-section.png)
- [Map-strategy section — copy updated 2026-10-30](map-strategy-section.png)
- [Battle selected](battle-selection.png)
- [Strategic view selected](strategic-selection.png)
- [Lava Shield terrain selected — updated 2026-10-30](lava-shield-selection.png)
- [Full-page review](desktop-full-page.jpg)
- [Mobile overview](mobile-overview.png)

After extending the gallery on **2026-10-27**, all review images were regenerated with local headless Chromium at the documented desktop/mobile viewports. The full-page image is a direct full-page browser render, with no stitching or content alterations. It is a local presentation review, not an Epic portal screenshot. Five entries, loaded assets, working selections, disabled Get, absence of retired/rejected-image references and no mobile overflow were checked. Delivery images and the whole map use contain framing so native HUD and map edges are preserved.

On **2026-10-30**, only the fifth gallery image was replaced with the closer terrain-in-use capture after the user approved the other images and noted the whole-map/strategic duplication. The updated Lava Shield selection proof was rendered and inspected; image loading, selection, full-frame display and mobile overflow were checked. Other approved source images and About image assignments remain byte-identical. Earlier overview/full-page proofs retain their dated gallery thumbnails; the current selected proof above shows the replacement.
