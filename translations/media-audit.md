# Storefront translation media audit

[Canonical catalogs](README.md) · [Approved imagery family](../planning/approved-storefront-rollout.md#approved-imagery-only--2026-10-30) · [Localization rollout](../planning/storefront-localization-rollout.md)

Observed **2026-10-31**. Localization v1 changes listing text and captions only. No new art, outside imagery or gameplay screenshots have been generated or uploaded in this unit.

| Surface | Existing approved media / localization treatment | Evidence boundary |
| --- | --- | --- |
| Google Play | Existing icon, feature graphic `feature-graphic-1024x500.png` and four phone images `editor-map.png`, `back1.png`, `next-setup.png`, `gameplay1.png` visible in authenticated English listing. | Retain existing actual-device gallery and icon. The console explicitly offers default graphic inheritance when text translations lack localized graphics. No locale media upload required for text-only rollout. |
| iOS | Preserve existing actual-device screenshots/icon. | Locale selector disabled during current review; no screenshot modification attempted. |
| Mac | Four approved 16:10 adapters remain listed: colony, River battle, Four Squares strategic view, Lava Shield terrain. | Locale selector and screenshot upload disabled during Waiting for Review. |
| Microsoft | Existing English desktop gallery shows four approved colony/River/Four Squares/Lava Shield captioned placements. | Localized listing media requirements must be confirmed from the real export/import and editor. Do not claim inherited or saved images before checking each locale. |
| Amazon | Existing Fire icons, screenshot references and approved promotional image remain in submitted listing. | Images/Add localization disabled under SUBMITTED. Preserve device-specific gallery. |
| Epic | Existing authenticated Dev preview renders four carousel images plus approved key art/logo. | No translated artwork uploaded. Keep proper map names and wordmark unchanged; text translations travel with relevant entities. |
| Snap/AppStream | Approved colony/River/Four Squares/Lava Shield family already documented. | Canonical captions may be localized in maintained AppStream metadata; no native Snap locale control established. |

The canonical screenshot captions preserve **River**, **Four Squares** and **Lava Shield** as proper map names. Right-to-left text must not mirror gameplay or the wordmark. Text embedded in approved imagery remains as approved until a direct, approved derivative is needed for an actual platform requirement. Asset upload initiation or generic Save success is not proof of persisted imagery; any later upload requires completion, fresh server reload and visual comparison.

## Remaining visual inspection

This pass established existing mobile gallery filenames and console counts, not a frame-by-frame overlay-language audit. The actual iOS, Play and Fire image overlays still need visual inspection before claiming every displayed localized gallery is language-neutral. Default-media retention does not establish that existing image text is localized. No gallery replacement was made.
