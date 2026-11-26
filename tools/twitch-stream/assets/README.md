# Stream rig assets

[Stream rig](../README.md) · [Epic v5 artwork](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-v5/README.md) · [Approved storefront rollout](../../../planning/approved-storefront-rollout.md)

| File | Use | Source and transformation |
| --- | --- | --- |
| [glob2-wordmark.png](glob2-wordmark.png) | Bottom-right stream branding (`BRAND_LOGO`) | Direct derivative of the approved [product logo](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-v5/product-logo-960x540.png) (cream "Globulation", gold "2"). **Crop only:** source box `(28, 202, 932, 337)`, the alpha bounding box `(32, 206, 928, 333)` plus 4 px padding. RGBA kept, no recolor or resampling; result 904×135, 35,077 bytes. |

Source SHA-256 `730891bc823683e26a22c739c1c5b1bf8db84cabc5eb440fb8698f849fcde110`; derivative SHA-256 `609545867b219e08c37a33e2dd17d0d38216647745ee05b9a333ab1fbcfe0c03`. `stream.sh` scales the wordmark at encode time (default 200 px wide at 1080p); the committed file is not resized.

Repository policy allows only approved images or direct modifications of them ([working rules](../../../AGENTS.md#approved-imagery-only)). The product logo was approved for use on 2026-10-30. Its wordmark comes from the design-system alpha masks described in the [Epic v5 record](https://github.com/Globulation2/glob2-marketing/blob/eb6cad4be97ffe9ac5d0422d9c44aa3d60e632ba/assets/epic-v5/README.md#source-identity-and-transformations). The design-system [provenance manifest](https://github.com/Globulation2/glob2-design-system/blob/acd277710acfebf528e1fc6f653d55fdf75de4b2/assets/provenance.json) identifies the game art as GPL-3.0-or-later. Individual art attribution/usage notices still need the release's rights review; existing public display does not complete that review.
