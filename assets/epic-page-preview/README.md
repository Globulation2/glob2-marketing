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

Copy derives from the [selected positioning](../../analysis/positioning-v1.md) and [Epic description draft](../../planning/epic-store-profile-v1.md), shortened for scanability. The page presents the colony economy first, spatial growth second, and control/rival pressure as supporting parts of the experience.

The hero uses the [v5 landscape illustration](../epic-v5/README.md), with its existing title and exact source-unit silhouettes. It is promotional key art, not a gameplay screenshot. The product logo uses the v5 transparent export. Both are linked directly from the sibling pack to avoid divergent copies. Existing genuine gallery and About references are copied unchanged from the website:

| Local file | Source | Context |
| --- | --- | --- |
| `media/colony.webp` | `public/images/home-thriving-colony.webp` | Replay view: colony/economy composition |
| `media/expansion.webp` | `public/images/home-rival-expansion.webp` | Replay view: territorial context |
| `media/defence.webp` | `public/images/home-colony-defence.webp` | Replay view: rival pressure |
| [Current controls capture](../epic-gameplay-v1/early-colony-controls.png) | Public browser build, captured 2026-10-26 | Live local-player view: Inn worker demand, normal fog and HUD, 2560×1440 |

Website source revision: [6e391ebe93b725747827a3ed7cea78f0d0d8f7e1](https://github.com/Globulation2/glob2-online-website/tree/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1). The homepage replay views were recorded 2026-10-11 on Fingerprint / Quick clash, tick 41350, with fog disabled and outer HUD cropped. They are not fresh player-view captures of the Epic Windows edition. The fresh controls image follows the [current capture manifest](../epic-gameplay-v1/capture-manifest.json); it is browser evidence, not Epic Windows launcher qualification. Source roles and limitations belong in submission provenance even when the preview presents images cleanly.

The v5 [provenance record](../epic-v5/README.md) covers its generated environment, actual game-unit silhouettes, existing wordmark masks and maintained cream/gold colors. This page introduces no third-party game art or additional character substitutes. See the [source provenance ledger](../../facts/assets.md) and original project notices for art/attribution context; this review does not finish release rights clearance.

## Remaining production work

The cover is the current v5 direction; the genuine gallery combines documented earlier replay captures with a fresh current-browser controls view. Replace that gallery with stronger current-build captures when ready, verify the copy in Epic's actual field/preview system, and populate release-specific metadata from the qualified build. This file does not authorize uploads or publication.

## Visual checks

Rendered in the local browser at 1600×1100 desktop and 390×844 mobile. The mobile document has no horizontal overflow, and all images load. Gallery interaction switches the hero and updates selection state. The Get control remains disabled. No custom fonts are bundled; typography uses the system font stack.

- [Desktop overview](desktop-overview.png)
- [About section](about-section.png)
- [Full-page review](desktop-full-page.jpg)
- [Mobile overview](mobile-overview.png)

The full-page review assembles overlapping browser viewport captures at their measured scroll offsets, with no content alterations. It is a local presentation review, not an Epic portal screenshot.
