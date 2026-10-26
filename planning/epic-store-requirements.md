# Epic Games Store preparation requirements

[Planning index](README.md) · [Epic profile draft](epic-store-profile-v1.md) · [Reusable copy](store-profile-v1.md) · [Asset brief](store-assets-v1.md)

Checked **2026-10-26** against Epic's public documentation. The user selected Epic as the first storefront. This record covers preparing its Windows profile; no Developer Portal session, account state, submission or publication was inspected or changed. Portal validation and previews remain the final field checks.

## Copy and page fields

The product home page uses a media carousel and an About description composed of headline/body blocks and images. At least one carousel image is required. Optional additional images are JPG, 1920×1080, with up to 20 slots; optional social preview is JPG, 1200×1200, maximum 4 MB. An Early Access PC product needs an FAQ. [Epic product-home guide](https://dev.epicgames.com/docs/epic-games-store/product-lifecycle-management-guides/pre-release/product-announcement-and-wishlisting/product-home-page).

About and offer short-description text must describe the game's experience/features. Keep other storefront promotion out of this text. Offer/library imagery must include a readable product-name logo, with logo and key art in the critical area. Product logos must work against a dark page background. [Epic content requirements](https://dev.epicgames.com/docs/epic-games-store/requirements-guidelines/content-ratings/content-guidelines).

The exact short-description/name limits and available genre/feature choices were **not established from the official pages retrieved**. Do not present a third-party 280-character claim as a verified Epic limit. Use the draft's measured text lengths, then check the portal. Store-language availability is separate from languages supported by the Windows build.

## Image export targets

| Slot | Verified specification |
| --- | --- |
| Product logo | 960×540 PNG; maximum 1 MB |
| Offer general, landscape | 2560×1440 JPG/JPEG/PNG |
| Offer general, portrait | 1200×1600 JPG/JPEG/PNG |
| Offer library | Both landscape and portrait; same specifications as general images; general images may be copied for a base offer |
| Media carousel still | 1920×1080 JPG/JPEG/PNG/GIF; maximum 4 MB |
| About image | At least 700 px wide; JPG/JPEG/PNG/GIF; maximum 4 MB |

Each offer needs landscape and portrait general images; a base game also needs both library orientations. About requires text and at least one asset. Its limit is 10,000 characters or 30 images; images consume the character budget. Use the portal counter. A trailer is not required for this first still-image pack. If added: 1920×1080 MP4, maximum 300 MB, 30/60 fps; follow the guide's audio specification. [Epic storefront media guide](https://dev.epicgames.com/docs/epic-games-store/sales-and-marketing/marketing/storefront-media-guide).

## Small submission checklist

- Copy the agreed headline and adapted descriptions from the Epic profile draft; keep game claims aligned with the actual Windows edition.
- Prepare the logo, both offer orientations and a genuine-game carousel image. The five-image story in the asset brief is an editorial target, not Epic's minimum gallery count. Keep illustrated covers distinct from gameplay captures.
- Confirm the portal's developer/publisher identity, support and privacy links, Windows minimum/recommended specifications, supported languages, dates, availability, regions/ratings and free-base-offer configuration. Leave unverified values pending rather than copying historical editions.
- Decide whether this release is Early Access; that changes FAQ work. Do not infer its status from the current website wording or a GitHub prerelease flag.
- Preview desktop and narrow layouts, including offer-image crops and logo contrast. Exact safe-area templates/portal previews still need checking; no invented pixel margins are prescribed here.

This list is project preparation, not proof that every field is mandatory for every offer. Epic groups release setup into artifacts/binaries, store settings, offers and pages, then promotes work through private Dev and Stage before reviewed Live publication. [Epic release management](https://dev.epicgames.com/docs/epic-games-store/publishing-tools/publishing-process/release-management).

## Build and account handoff

The game's [pinned Epic setup](https://github.com/Globulation2/glob2/blob/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/docs/releases/store-setup.md#epic-games-store), reviewed locally, specifies Windows first, a free base offer, actual-game carousel media, Dev-only upload, launcher installation/testing, then Stage/review/Live. It also calls for trader/tax/payout onboarding; their completion is unknown and private details do not belong in this repository.

If online multiplayer ships, Epic requires crossplay across PC storefronts. If achievements ship on another PC storefront, Epic requires substantially similar Epic achievements. These are build qualification dependencies, not promises to add to this profile without evidence. [Epic distribution requirements](https://dev.epicgames.com/docs/epic-games-store/requirements-guidelines/distribution-requirements/requirements-overview).

Next use: check the prepared copy/artwork in the Dev preview, fill verified edition metadata, and retain the actual launch build/capture provenance. No upload, review request or launch action is performed by this checklist.
