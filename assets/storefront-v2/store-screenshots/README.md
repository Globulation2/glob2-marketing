# Captioned store screenshots (generated)

[How they are made, and how to change them](../tools/README.md) · [Raw captures](../captures/mobile/README.md) · [Caption source](../../../translations/en.md)

Everything here is written by `../tools/screenshots.py`; do not edit by hand. Each folder is `<store-set>/<locale>/` with the images in gallery order (`<NN>-<role>-<WxH>.png`), a `manifest.json` (capture and catalog hashes, caption text, fonts, layout, output hashes) and, one level up, a `contact-sheet-<locale>.jpg` for review. The contact sheets are not store assets.

| Store set | Upload to | Pixels |
| --- | --- | --- |
| `apple-iphone-6.9` | App Store, iPhone 6.9-inch | 1320×2868 |
| `apple-ipad-13` | App Store, iPad 13-inch | 2064×2752 |
| `google-play-phone` | Google Play, phone | 1080×1920 |
| `google-play-tablet-7` | Google Play, 7-inch tablet | 1920×1200 |
| `google-play-tablet-10` | Google Play, 10-inch tablet | 2560×1600 |
| `amazon-tablet` | Amazon Appstore | 2560×1600 |
| `fdroid-phone` | F-Droid `phoneScreenshots` | 1080×1920 |

## Status on 2026-11-24

- **English reference set.** Re-rendered on 2026-11-24 after the [round 2 final review](../review/round-2-final.md), from the round 2 captures and their revised gallery, [`captures/mobile/selection.json`](../captures/mobile/selection.json): every set in the order **hero, battle, fair deal, build, economy, territory, maps** (`asset_text.mobile_gallery_order`, so a fight is in slot 2), 6 iPhone slides and 7 on every other set, 48 images in all.
- **No opponents slide.** The computer opponent picker (a menu screen) was dropped from every set and locale (review M1); "8 computer opponents" stays in the description text. Every slide is now gameplay (`capture.kind: gameplay` in each manifest).
- **iPhone battle slide.** The iPhone has no battle capture; its slot 2 is the `05-territory` capture, which shows the best fight of any phone frame, under the battle caption. The iPhone has no territory slide.
- **Line breaks.** Two-line captions break after punctuation where they can, and otherwise never end the first line with a word of four letters or fewer (review M3; see the [tool README](../tools/README.md#how-a-caption-is-fitted)).
- `uv run screenshots.py verify --locale en` passed for all 48 images on this date.
- **What is committed.** Only this README, the English `manifest.json` files and the English contact sheets ([`.gitignore`](.gitignore)). The PNGs are reproducible: `uv run screenshots.py render --locale en` writes them here again, and `verify --locale en` checks them against the committed manifests (same machine and pinned Chromium; see the [tool README](../tools/README.md)). Store packages link to the durable render folder outside the repository, not to these files.
- Other locales are not stored here. They are rendered on demand; see the all-locales command in the [tool README](../tools/README.md).
- **Android sets from emulator captures (2026-11-25).** `google-play-phone`, `google-play-tablet-7`, `google-play-tablet-10`, `amazon-tablet` and `fdroid-phone` are rendered from the Android emulator captures (`captures/mobile/android-*-emulator/`, the real Android app on Android 15), no longer from the interim host renders. The Android status bar and gesture-handle band are trimmed (phone 62 and 65 px, 1920×1200 40 and 57 px, 2560×1600 48 and 64 px; see the [tool README](../tools/README.md#system-bar-trim-per-capture)), so no system bar or the 1920×1200 class's doubled Wi-Fi glyph appears. `amazon-tablet` takes the 2560×1600 set; this clears review M8. The iPhone and iPad sets were rendered again only because the gallery and tool files changed; their images are byte-identical to the 2026-11-24 renders.
- `uv run screenshots.py verify --locale en` passed for all 48 images on 2026-11-25.
