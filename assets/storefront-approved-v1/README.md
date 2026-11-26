# Approved desktop storefront exports

[Approved copy and rollout](../../planning/approved-storefront-rollout.md) · [Manifest](manifest.json) · [Final page](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-page-preview/README.md)

Prepared **2026-10-30** after the user approved the final presentation for cross-store use. These four PNGs preserve the decoded RGB pixels of the approved gallery images exactly. There is no resize, crop, retouching or new game imagery. The original source formats remain available at their existing paths (removed 2026-11-26; kept in Git history at the links below).

| Order | PNG export | Source / context |
| --- | --- | --- |
| 1 | [Colony](01-colony.png) | [Fingerprint replay](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-page-preview/media/colony.webp), 1280×720, fog disabled and outer HUD cropped. |
| 2 | [River battle](02-river-battle.png) | [Blue/gold native battle](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-gallery-v4/README.md), staged scenario with actual combat; full HUD preserved. |
| 3 | [Four Squares strategic view](03-four-squares-strategic.png) | [Developed Cortex match](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-gallery-v5/README.md), actual AI simulation and native strategic GUI; full HUD preserved. |
| 4 | [Lava Shield terrain](04-lava-shield-terrain.png) | [Native terrain scene](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-gallery-v3/README.md), staged in-engine; full HUD preserved. |

Use these in desktop screenshot slots that require PNG, subject to the destination's current dimensions and preview. The colony source is 1280×720; do not enlarge it to imply a new capture or meet a larger source-capture requirement. The three native delivery frames are 2560×1440. The JPEG exports are smaller and remain preferable where accepted. These images do not establish Windows launcher or mobile-device qualification. Do not put desktop frames in phone/tablet screenshot fields.

## Key art and logo

Use the existing approved [illustrated landscape PNG](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-v5/offer-landscape-2560x1440.png) or [JPEG](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-v5/offer-landscape-2560x1440.jpg), 2560×1440, for compatible key-art slots. The [portrait export](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-v5/offer-portrait-1200x1600.jpg), 1200×1600, belongs to the same illustrated family but still needs a destination crop preview. The [transparent product logo](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-v5/product-logo-960x540.png), 960×540, preserves the existing wordmark. Do not use illustrated art as a gameplay screenshot or replace compiled app icons with it.

These sizes are existing Epic-oriented exports, not a claim that every store uses the same specification. Preserve source provenance and notices linked by each capture/art pack. The [approval record](../../planning/approved-storefront-rollout.md) is the current copy/media authority; older draft packs remain historical.

## Source folders removed (2026-11-26)

The superseded source folders these exports and the `gog/` and `windows/` build scripts read from (`assets/epic-v5`, `assets/epic-page-preview` and `assets/epic-gallery-v3` to `v5`) were removed from the working tree on 2026-11-26. They are kept in Git history at commit [`eb6cad4`](https://github.com/Globulation2/glob2-marketing/tree/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets). The manifests and scripts still name the old paths as provenance. To rebuild an export, restore the sources first, for example `git checkout eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba -- assets/epic-v5`, then remove them again afterwards.
