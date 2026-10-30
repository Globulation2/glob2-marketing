# Snap Store listing exports

[Approved desktop family](../README.md) · [Manifest](manifest.json) · [Exact listing fields](listing-fields.json) · [Rollout ledger](../../../planning/approved-storefront-rollout.md)

Prepared **2026-10-30** for the authenticated Snap listing editor. The summary, description and homepage in `listing-fields.json` are extracted from the approved Snap metadata merged through [game PR #1281](https://github.com/Globulation2/glob2/pull/1281). The summary is 47 characters, within the documented 79-character limit; the description preserves the approved colony/economy message.

## Gallery exports

| Order | JPEG | Dimensions | Bytes |
| --- | --- | --- | --- |
| 1 | [Colony](01-colony.jpg) | 1280×720 | 591,649 |
| 2 | [River battle](02-river-battle.jpg) | 2560×1440 | 1,593,377 |
| 3 | [Four Squares strategic view](03-four-squares-strategic.jpg) | 2560×1440 | 841,901 |
| 4 | [Lava Shield terrain](04-lava-shield-terrain.jpg) | 2560×1440 | 1,464,530 |

Each file is below Snap's **2,000,000-byte** image limit and the export target of 1,950,000 bytes. The four frames retain their original dimensions and complete content, including native HUDs: no resize, crop, recolouring or retouching. JPEG encoding is lossy; these are not the exact-RGB PNG exports. Quality and hashes are recorded in the manifest. Source imagery and its staged-scene/AI-match context remain linked by the parent pack.

Snap permits up to five gallery items, at 480×480 minimum, documented maximum 3840×2160, and aspect ratios from 1:2 to 2:1. These exports fit those file/dimension rules. Snap's guidance asks cross-platform games to use Linux workstation captures. The retained source capture provenance is unchanged; the native scenes were captured on macOS. Check their representation of the actual Snap edition and the platform guidance before gallery publication. File-format compliance alone is not build or device qualification.

## Featured banner

[Optional 1440×480 banner](banner-1440x480.jpg) is a 3:1 crop of the approved illustrated landscape: source rectangle `(0,90,2559,943)`, resampled with Lanczos. It retains the existing wordmark and central colony. This is promotional illustration, separate from gameplay. The export passed coordinating visual review; its fit in the actual banner field remains to check before upload. Preserve the existing app icon.

The banner fits Snap's documented 3:1 range of 720×240–4320×1440 and is under 2,000,000 bytes. The export manifest records its exact byte count and hash.

## Official requirements checked

The platform inventory verified these sources on 2026-10-30:

- [Snap listing guide](https://snapcraft.io/about/listing): summary and screenshot guidance.
- [Store listing and branding](https://forum.snapcraft.io/t/store-listing-and-branding/16397): screenshot, banner and icon slots.
- [Publisher screenshot validator](https://github.com/canonical/snapcraft.io/blob/main/static/js/publisher/pages/Listing/ListingDetails/Screenshots.tsx): accepted image/file-size handling.
- [Publisher banner/icon validator](https://github.com/canonical/snapcraft.io/blob/main/static/js/publisher/pages/Listing/ListingDetails/ListingDetails.tsx): banner ratio, dimensions and cap.

No screenshot or banner has been uploaded. The approved summary, full description, homepage and Games category were subsequently saved in the authenticated Snap editor, with explicit success confirmation; public propagation remains unverified. See the [rollout ledger](../../../planning/approved-storefront-rollout.md) for remaining file-upload permission and console-access work.
