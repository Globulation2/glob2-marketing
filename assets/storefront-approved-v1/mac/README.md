# Mac App Store screenshot-size adapters

[Approved gallery](../README.md) · [Manifest](manifest.json) · [Rollout ledger](../../../planning/approved-storefront-rollout.md)

Prepared **2026-10-30** for the actual Mac Media Manager screenshot sizes: 2880×1800, 2560×1600, 1440×900 or 1280×800. The approved gameplay sources are 16:9. These PNGs preserve every source RGB pixel and add only neutral black padding to fit a permitted 16:10 canvas.

| Order | PNG adapter | Source frame | Padding |
| --- | --- | --- | --- |
| 1 | [Colony](01-colony-1280x800.png) | Approved 1280×720 | 40 black pixels above and below |
| 2 | [River battle](02-river-battle-2560x1600.png) | Approved 2560×1440 | 80 black pixels above and below |
| 3 | [Four Squares strategic view](03-four-squares-strategic-2560x1600.png) | Approved 2560×1440 | 80 black pixels above and below |
| 4 | [Lava Shield terrain](04-lava-shield-terrain-2560x1600.png) | Approved 2560×1440 | 80 black pixels above and below |

No crop, resize, upscaling, added gameplay, sharpening, retouching or outside imagery is used. The native HUD remains complete wherever it exists in the approved source. These are opaque RGB PNGs. The manifest records source/output hashes, exact dimensions, padding and byte counts. Pixel comparison verifies that each central frame is byte-identical to its approved source's decoded RGB pixels; the added margins are `(0,0,0)` only.

The gallery retains its existing provenance: Fingerprint replay colony, authored native River battle, genuine developed Four Squares AI match and authored native Lava Shield terrain. Format adaptation does not make these fresh native captures. Keep the existing compiled application icon, selected build and release/policy settings separate from screenshot preparation.

Coordinating visual review approved the four adapters; inspect their actual Media Manager preview after upload. File creation is not an upload, saved listing, review submission or live-release claim. The [rollout ledger](../../../planning/approved-storefront-rollout.md) records those outcomes separately. Only approved source imagery/direct modifications are permitted.
