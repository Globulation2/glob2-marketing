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

Copy derives from the [selected positioning](../../analysis/positioning-v1.md) and [Epic description draft](../../planning/epic-store-profile-v1.md), shortened for scanability. The page leads with the colony economy, uses Lava Shield to make spatial strategy concrete, and retains rival pressure as text while a stronger genuine battle image remains outstanding.

| Current media | Source and context |
| --- | --- |
| [Illustrated cover](../epic-v5/README.md) | Promotional key art: generated environment, existing title and exact source-unit silhouettes. It is not a gameplay screenshot. The sidebar logo uses the same pack. |
| `media/colony.webp` | Unchanged website `public/images/home-thriving-colony.webp`, revision [6e391ebe](https://github.com/Globulation2/glob2-online-website/tree/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1). Actual Fingerprint / Quick clash replay recorded 2026-10-11, tick41350, fog disabled and outer HUD cropped. It is not a fresh Epic Windows capture. |
| [Lava Shield overview](../epic-gallery-v2/lava-shield-map.jpg) | Native engine render of an initial generated Lava Shield map. The whole island is preserved inside a landscape delivery canvas. This is a map overview, not a populated battle or a screenshot of the live strategic UI. The [capture pack](../epic-gallery-v2/README.md) records source/build identity, render and export. |

The Lava Shield overview replaces the similar expansion replay crop. Its crater, branching flows and crossings are documented in the game's [Lava Shield guide](https://github.com/Globulation2/glob2/blob/53110681a31d08423568afe26d5b8d8f9ac45dd1/docs/map-generators/lava-shield.md). The gallery has three entries: **Cover, Colony and Lava Shield**. The spatial About section uses the same map overview; the defence section is text-only, without a missing-image placeholder.

The old `media/expansion.webp` and `media/defence.webp` files remain historical source copies, but are no longer referenced by the page. Their similar crops did not communicate a sufficiently different view or a clear large battle. The [newer controls capture](../epic-gameplay-v1/README.md) also remains excluded after its abnormal fog rendering was identified. None of the evaluated coastal or Four Squares render candidates is represented as an approved battle capture; resource algae must not be mistaken for armies.

The v5 [provenance record](../epic-v5/README.md) covers its illustration and source silhouettes. See the [source asset ledger](../../facts/assets.md) and original project notices for art/attribution context. This local review does not complete release rights clearance.

## Remaining production work

A clear large-battle image and an actual strategic-UI view remain open capture tasks. The current native editor automation attempt did not yield a qualified frame, and no substitute was fabricated. The Lava Shield image demonstrates map geometry only. Obtain stronger current-build mature gameplay media, verify copy and crops in Epic's actual preview, and populate release metadata from the qualified Windows build before submission. Nothing in this local review authorizes uploads or publication.

## Visual checks

Rendered in the local browser at 1600×1100 desktop and 390×844 mobile. The mobile document has no horizontal overflow, and all images load. Gallery interaction switches the hero and updates selection state. The rejected controls image and retired expansion/defence crops are absent from both gallery and About. The Get control remains disabled. No custom fonts are bundled; typography uses the system font stack.

- [Desktop overview](desktop-overview.png)
- [About section](about-section.png)
- [Lava Shield selected](lava-shield-selection.png)
- [Full-page review](desktop-full-page.jpg)
- [Mobile overview](mobile-overview.png)

After diversifying the gallery, all four review images were regenerated with local headless Chromium at the documented desktop/mobile viewports. The full-page image is a direct full-page browser render, with no stitching or content alterations. It is a local presentation review, not an Epic portal screenshot. Three distinct gallery entries, loaded images, disabled Get, absence of retired/rejected-image references and no mobile overflow were checked. The Lava Shield selection was checked with the complete island visible.
