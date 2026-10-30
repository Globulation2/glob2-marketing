# Microsoft Store promotional exports

[Approved presentation](../../../planning/approved-storefront-rollout.md) · [Approved artwork provenance](../../epic-v5/README.md) · [Manifest](manifest.json) · [Build script](build-assets.py)

Prepared **2026-10-30** for the dedicated fields inspected in the authenticated Microsoft Store product editor. These are promotional illustration exports, separate from gameplay screenshots and application icons.

| Portal field | Export | Dimensions / mode |
| --- | --- | --- |
| Poster art | [Portrait poster](poster-1440x2160.png) | 1440×2160; opaque RGB PNG |
| Box art | [Square cover](box-art-1080x1080.png) | 1080×1080; opaque RGB PNG |
| Super hero art | [Titleless landscape](super-hero-titleless-1920x1080.png) | 1920×1080; opaque RGB PNG; no product title |

The editor accepts poster dimensions 720×1080 or 1440×2160, box art 1080×1080 or 2160×2160, and Super hero art 1920×1080 or 3840×2160. These exports use the actual numeric field requirements, rather than interpreting an inconsistent ratio label. The Super hero field prohibits the product title. Keep the existing 300×300 App Tile/application icon; this pack does not replace it.

## Source and composition

All three exports start with the retained, approved [pre-title colony composite](../../epic-v5/colony-native.png), 1672×941. That layer already contains the approved illustrated environment and unchanged game-unit silhouettes placed at environmental scale. No unit is generated, repainted, restaged or anatomically altered here.

The poster uses source crop `(554,0,1178,936)` and resizes it to 1440×2160. The square uses `(365,0,1306,941)` and resizes it to 1080×1080. Their title is extracted from the approved [product-logo canvas](../../epic-v5/product-logo-960x540.png), rectangle `(30,204,930,335)`, preserving the existing cream/gold wordmark. Each format repositions that wordmark with the same shadow treatment as the [approved v5 script](../../epic-v5/build-assets.py), without clipping or stretching the title.

The titleless Super hero export fits the complete pre-title colony composition to 1920×1080 with aspect-preserving Lanczos resampling and the minimal centered aspect crop. It never loads a title-bearing cover, erases text or paints over lettering. No new image generation, inpainting or screenshot retouching is involved.

`build-assets.py` reproduces the exports from those two retained PNG sources and writes the manifest. It does not overwrite any approved source asset. The manifest records source/output hashes, dimensions, title placement, crops and file sizes. Underlying illustration, source-unit, title and licence context remain in the linked artwork provenance.

## Review and use

Coordinating visual review approved all three compositions; inspect their actual portal previews before upload. File preparation does not claim a saved listing or live publication. Keep the approved four-image gameplay gallery in screenshot slots; do not label these illustrations as actual gameplay. Existing app icons, builds, releases, prices and policy fields are outside this export unit. See the [rollout ledger](../../../planning/approved-storefront-rollout.md) for destination outcomes.
