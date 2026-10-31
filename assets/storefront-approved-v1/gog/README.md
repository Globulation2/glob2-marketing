# GOG product artwork adapters

Prepared and coordinating visual review completed 2026-10-31, **not uploaded or portal-accepted**. [Release handoff](../../../planning/gog-release-readiness.md) · [Approved source family](../../../planning/approved-storefront-rollout.md#approved-media-and-order).

Only the approved pre-title colony raster and original wordmark are used. No outside imagery, AI generation, content retouching or new character artwork. Promotional illustration is not gameplay. The four approved gameplay PNGs remain at their [existing source paths](../README.md), in colony / River battle / Four Squares strategy / Lava Shield terrain order; no redundant screenshot conversions were needed.

| File | Delivery role |
| --- | --- |
| `prod-main-banner-1600x740.png` / `.psd` | Green product main-banner board; wordmark centered as the embedded template indicates. |
| `prod-logo-1600x740.png` | Transparent product-logo canvas, centered native 900×131 visible wordmark without upscaling. |
| `prod-box-342x482.png` / `.psd` | Green product cover board; centered title retained within the diamond-shaped corner caution pattern. |
| `prod-galaxy-background-2560x670.png` | Green Galaxy background; approved pre-title scene center-fit, no text added. |
| `prod-bg-2560x655.png` | Red linked product-background board, same Galaxy source with the last 15 rows excluded, matching its artboard relationship. |
| `key-art-layered-2560x1440.png` / `.psd` | Higher-resolution layered handoff with the approved landscape title placement. |

The official [template archive](https://items.gog.com/templates/gog_art_assets.zip), SHA-256 `50222fd566382488f2b7888ece1c0ae5596bf84d73b86600be229a587c9a2468`, was inspected in temporary storage. Artboard bounds and embedded PSB dimensions were checked; the editable main art and cover show centered-title/corner-caution placeholders, with no separate numerical safe-margin specification. The transparent-logo PSB is empty. No placeholder, guide, template text or mockup image is included in these exports. Exact Assets Manager acceptance remains unverified without a controlled product.

The PSDs contain **three genuine raster layers**: approved flattened colony composite, wordmark shadow and original wordmark. These are not vector originals, independently editable colony objects or fully reconstructed source scenes. Background native source is 1672×941 and visible title raster 900×131; larger output canvases resample those pixels with Lanczos and create no new detail. Layered files are reopened, checked for size/three layers and recomposited against the corresponding PNG (maximum one RGB code-value difference from alpha-rounding). The transparent-logo export retains its visible native dimensions.

Run `build-assets.py` with Pillow and psd-tools. The [manifest](manifest.json) records exact source hashes, crops/resampling, layer names and output hashes. The script writes only this directory. Source provenance/rights qualifications remain those of the [approved v5 artwork](../../epic-v5/README.md); these adaptations make no new blanket rights declaration.

Compiled application icons are preserved. Demo-only boards, campaign/social formats and public trailers have not been fabricated or exported. No portal upload, acceptance, QA submission or release is implied by this package.

Coordinating review confirmed centered-title fit, retained colony in portrait/wide crops and no visible guide/mockup leakage. This local review does not prove publisher portal acceptance or change unresolved onboarding.
