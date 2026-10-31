# Storefront translation media audit

[Canonical catalogs](README.md) · [Approved imagery family](../planning/approved-storefront-rollout.md#approved-imagery-only--2026-10-30) · [Localization rollout](../planning/storefront-localization-rollout.md)

Observed **2026-10-31**. Localization v1 changes listing text and captions only. No new art, outside imagery or gameplay screenshots have been generated or uploaded in this unit.

| Surface | Existing approved media / localization treatment | Evidence boundary |
| --- | --- | --- |
| Google Play | Existing icon, feature graphic `feature-graphic-1024x500.png` and four phone images `editor-map.png`, `back1.png`, `next-setup.png`, `gameplay1.png` visible in authenticated English listing. | Retain existing actual-device gallery and icon. The console explicitly offers default graphic inheritance when text translations lack localized graphics. No locale media upload required for text-only rollout. |
| iOS | Preserve existing actual-device screenshots/icon. | Locale selector disabled during current review; no screenshot modification attempted. |
| Mac | Four approved 16:10 adapters remain listed: colony, River battle, Four Squares strategic view, Lava Shield terrain. | Locale selector and screenshot upload disabled during Waiting for Review. |
| Microsoft | Existing English desktop gallery shows four approved colony/River/Four Squares/Lava Shield captioned placements. | Fresh export verified seven retained source references in each of 31 saved locales. The actual saved Arabic listing’s seven image roles were visually compared with the approved family; other locales were reference-checked, not individually pixel-checked. |
| Amazon | Existing Fire icons, screenshot references and approved promotional image remain in submitted listing. | Images/Add localization disabled; listing subsequently advanced from Submitted to Under Review. Preserve device-specific gallery. |
| Epic | Existing authenticated Dev preview renders four carousel images plus approved key art/logo. | No translated artwork uploaded. Keep proper map names and wordmark unchanged; text translations travel with relevant entities. |
| Snap/AppStream | Approved colony/River/Four Squares/Lava Shield family already documented. | Canonical captions may be localized in maintained AppStream metadata; no native Snap locale control established. |

The canonical screenshot captions preserve **River**, **Four Squares** and **Lava Shield** as proper map names. Right-to-left text must not mirror gameplay or the wordmark. Text embedded in approved imagery remains as approved until a direct, approved derivative is needed for an actual platform requirement. Asset upload initiation or generic Save success is not proof of persisted imagery; any later upload requires completion, fresh server reload and visual comparison.

## Source-only mobile inspection

On **2026-10-31**, the actual retained Android/F-Droid source images and approved shared mobile promotional graphic were opened and visually inspected. This is direct source-file evidence, not proof of which current console placement uses those bytes.

| Inspected source | Dimensions | Visible text and finding |
| --- | --- | --- |
| [F-Droid phone screenshot 1](https://github.com/Globulation2/glob2/blob/f5272df9776818fd1798d5369f5139c383333242/fastlane/metadata/android/en-US/images/phoneScreenshots/1.png) | 320×640 | Native main menu with wordmark and English Settings / Custom game / Campaign / Load game / Tutorial / More labels. No added marketing overlay. |
| [F-Droid phone screenshot 2](https://github.com/Globulation2/glob2/blob/f5272df9776818fd1798d5369f5139c383333242/fastlane/metadata/android/en-US/images/phoneScreenshots/2.png) | 320×640 | Native gameplay, counters and English Build / Flags / Tools / Goals / Teams / Menu controls. No added marketing overlay. |
| [Approved mobile promotional graphic](../assets/storefront-approved-v1/mobile-promo/feature-graphic-1024x500.png) | 1024×500 | Approved illustrated colony and existing product wordmark only. No marketing sentence to translate. [Source treatment](../assets/storefront-approved-v1/mobile-promo/README.md). |

Source SHA-256 identities: screenshot 1 `a53420ea3d5b2454222c0e80eb088b9ac1ae87b7601e69a628df348b59690e4e`; screenshot 2 `9189b78d5f80cb786790334853fc9381aa0eba0a97db8de50342559e91d35915`; mobile promotional graphic `147f09c37234de318986a774d664480705f272ff3dd95bdcf6d8b9041385e7df`.

The two phone frames contain English **native UI**, so they are not language-neutral in the literal sense. The approved instruction preserves native gameplay UI, existing actual-device galleries and compiled icons; no marketing overlay derivative is needed for these inspected sources. No media was changed or generated.

The [iOS screenshot guide](https://github.com/Globulation2/glob2/blob/f5272df9776818fd1798d5369f5139c383333242/docs/releases/ios-app-store.md#artwork-and-screenshots) suggests optional captions and a `mobile/ios/store/` destination. That directory and actual iOS gallery files were absent from the inspected authoritative source checkout. Suggested captions are instructions for possible captures, not evidence of uploaded overlays. The [Fire release guide](https://github.com/Globulation2/glob2/blob/f5272df9776818fd1798d5369f5139c383333242/docs/releases/amazon-appstore.md) requires device screenshots but does not identify retained files corresponding to the four console references.

## Remaining console association and inspection

The authenticated Play gallery filenames above differ from the retained F-Droid files `1.png` and `2.png`. No matching dimensions/hashes or filename-to-source association was verified. Do not use the two source inspections as proof that the four current Play images were inspected. The actual console inspections below resolve the overlay question for all four displayed Play phone images, the four Fire thumbnails, and the primary iPhone-medium/iPad-13 previews. Other Apple device-size variants were not independently enumerated. Console-to-source byte associations remain unverified; default-media retention does not establish localized native UI. No gallery replacement was made.

## Actual Play gallery inspection — 2026-10-31

The mandatory AI-label modal displayed all four actual saved Play phone images together: `editor-map.png` (native map editor), `back1.png` (native menu), `next-setup.png` (native setup/map selection), and `gameplay1.png` (native colony view). Visual inspection found English native game controls, with **no separate marketing headline/caption overlay**. The illustrated feature graphic contains the unchanged Globulation 2 wordmark and approved environment. Only that feature graphic was selected for the AI label; icon and phone captures remained unselected. No image bytes, order, gallery slot or icon was changed. This directly resolves the Play-four-image overlay-inspection gap; associations with source-only fastlane captures remain unverified. The retained primary iOS and Fire galleries were subsequently inspected as recorded below.

## Actual Apple and Fire gallery inspection — 2026-10-31

Read-only App Store Connect inspection opened the actual retained **`iphone-medium-main-menu.jpg`** and **`ipad-13-main-menu.jpg`** at preview size. Both show the native main menu over the game world, with English game controls and the unchanged wordmark, **no added marketing headline or caption overlay**. These are the primary visible iPhone-medium and iPad-13 slots; additional Apple size variants were not independently enumerated. Locale/screenshot editing remains locked under the existing review.

The actual four retained Fire gallery thumbnails were also visually inspected together: native main menu, map/setup selection, colony gameplay and game-rules setup. Each uses native English game UI, with **no separate promotional headline/caption overlay**. The existing promotional graphic retains the approved illustrated wordmark-only family. Native device-gallery files/icons were neither edited nor replaced. The console header advanced independently from Submitted to **Under Review** during this read-only audit; no Amazon submission action occurred.

These observations resolve the overlay-content question for the actual inspected retained mobile galleries. They do not make English UI localized, identify every source-file hash, establish capture/build provenance beyond prior records, or authorize replacement of device screenshots. Text-only locale rollout can preserve the actual approved galleries as required.

## Saved Microsoft representative media verification — 2026-10-31

After import and fresh server readback, the actual saved **Arabic** listing was opened read-only. All seven rendered roles were visually inspected: the four colony / River / Four Squares / Lava Shield gameplay placements with localized captions, the poster, square box art and title-free 16:9 promotional landscape. They retain the approved gameplay and illustrated source family; the existing wordmark is unchanged. No new image was uploaded or edited.

The fresh server export separately verified **217 references (seven roles × 31 locales)** with the same asset type, host/path, remaining query parameters and order, differing only in per-locale parent IDs. This supports retained approved source assets across the import. The rendered comparison covers the representative Arabic listing; it is not a claim of 31 separate visual comparisons or downloaded byte-hash equality.
