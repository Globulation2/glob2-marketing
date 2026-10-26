# Epic artwork v1 — review pack

[Profile draft](../../planning/epic-store-profile-v1.md) · [Requirements](../../planning/epic-store-requirements.md) · [Store visual brief](../../planning/store-assets-v1.md)

**Rejected direction, 2026-10-26:** the user rejected this pack as resembling a presentation slide. Preserve these files as historical drafts; do not use them as the current store-art direction. See the [visual reference review](../../planning/store-art-reference-review.md) for the replacement direction, currently in preparation and undergoing character-source fidelity correction; no replacement art is approved.

Prepared **2026-10-26** using the existing Glob2 identity and the agreed colony/economy positioning. These are tangible review compositions, not approved uploads or newly captured gameplay. No store or source-project files were changed.

## Files

| File | Format / dimensions | Intended slot / status |
| --- | --- | --- |
| [Product logo](product-logo-960x540.png) | Transparent PNG, 960×540 | Product logo; native-size wordmark centered on the required canvas. Under 1 MB. |
| [Landscape offer](offer-landscape-2560x1440.png) | RGB PNG, 2560×1440 | General offer / library landscape review candidate. |
| [Portrait offer](offer-portrait-1200x1600.png) | RGB PNG, 1200×1600 | General offer / library portrait review candidate. |
| [Contact sheet](review-contact-sheet.jpg) | JPEG, 1600×1000 | Review preview only; do not upload as store artwork. |
| [Build script](build-assets.py) | Python / Pillow | Rebuilds all four images from the sibling design-system and website repositories. |

Dimensions and product-logo format/size follow Epic's [official storefront media guide](https://dev.epicgames.com/docs/epic-games-store/sales-and-marketing/marketing/storefront-media-guide), checked 2026-10-26. General offer images can be reused for library slots for the base offer. Final critical-area/template and crop-preview review remains open; dimensions alone do not establish acceptance. In particular, the existing wordmark's wide proportions leave substantial transparent space above/below it on the product-logo canvas. Review that treatment against Epic's guidance to avoid significant negative space; it is not claimed upload-ready.

The offer images are branded key-art layouts with an inset existing scene. They are **not** substitutes for the required actual-game carousel image. The 1280×720 scene is kept at native size in landscape and reduced to 1040×585 in portrait; no gameplay source or wordmark is enlarged. No frame is fabricated or AI-generated. The scene's replay context must remain part of submission provenance; do not describe it as a normal player-view screenshot.

## Source provenance

| Source | Exact identity | Use |
| --- | --- | --- |
| Design-system wordmark masks | [Design-system revision acd2777](https://github.com/Globulation2/glob2-design-system/tree/acd277710acfebf528e1fc6f653d55fdf75de4b2), `assets/wordmark-letters.webp` (900×131), `assets/wordmark-two.webp` (900×131) | Composite masks in the maintained brand colors: cream `#f9e8bb`, gold `#e2b85f`; no scaling above source size. |
| Design-system font/theme | Same revision, `assets/glob2-sans.woff2`, dark-theme background `#1b1229` and cream ink | Text rendering; [DejaVu notice](LICENSE-DejaVu.txt) retained. The background's subtle ellipse is a new simple layout shape, not game art. |
| Thriving-colony scene | [Website revision 6e391eb](https://github.com/Globulation2/glob2-online-website/tree/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1), `public/images/home-thriving-colony.webp` (1280×720) | Whole source frame inset with gold border; no scene crop or gameplay edit. |

The website's [capture verification](https://github.com/Globulation2/glob2-online-website/blob/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1/docs/website-content-verification.md) records this as a 2026-10-11 four-colony Fingerprint / Quick clash replay at tick 41350, fog disabled and outer HUD cropped. It is not a new capture of the intended Epic Windows build. The design-system [provenance manifest](https://github.com/Globulation2/glob2-design-system/blob/acd277710acfebf528e1fc6f653d55fdf75de4b2/assets/provenance.json) identifies upstream game revision `6ff1ebed476f2a055ccdbe16abd737f541ffcb44` and art as GPL-3.0-or-later. Individual art attribution/usage notices still need the release's rights review; existing public display does not complete that review.

Source SHA-256 values:

```text
wordmark-letters.webp 428fc52ed064debfe273d529c4cd81284a45160879d05afff7775929a35d206d
wordmark-two.webp a33008a9088f98edb64ff494bc38f3888849f562113be90ca191c48bbb5291a2
glob2-sans.woff2 04c452fa8481ef3df8f806e358e99d0eda2a657ff9c736383ca2a033a48d4ef0
home-thriving-colony.webp 39e0ade8d634801955f55897257eb8abc6ae4f75a07dd64ae81024eefff24371
```

## Remaining asset work

- Review the visual direction and the exact Epic critical-area templates / live crop previews before upload. Replace the inset scene with a matched fresh launch-build capture if appropriate.
- Capture at least one actual-game **1920×1080** carousel image from the selected Windows candidate; the existing 1280×720 replay cannot supply those pixels without enlargement. Follow the [five-image visual story](../../planning/store-assets-v1.md) as more shots are available.
- Confirm release-specific rights/credits and keep product, offer and carousel imagery accurately distinguished. No upload, listing publication or store approval is claimed.
