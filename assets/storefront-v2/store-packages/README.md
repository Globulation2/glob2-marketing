# Storefront-v2 store packages

[Build script](build.py) · [Store rules and slots](stores.json) · [Per-store manifests](manifests/) · [Final review](../review/round-2-final.md#final-galleries) · [Store rules and comparables](../../../analysis/mobile-store-comparables.md) · [Rollout ledger](../../../planning/storefront-v2-rollout.md)

`build.py` assembles, for every store, exactly the files a person or agent uploads to that store's console, in upload order, at the store's pixel size, format and file-size limit, and then checks every file again. Nobody resizes anything by hand.

Prepared 2026-11-24. Nothing here has been uploaded. A package is the "Prepared" evidence level of the [rollout ledger](../../../planning/storefront-v2-rollout.md#per-store-rollout), not Saved or Submitted, and the listing text inside it comes from an export marked `upload_eligible: false` (a preparation input that each console still has to be checked against).

## The one command

From the repository root:

```sh
uv run assets/storefront-v2/store-packages/build.py
```

That runs a fresh `translations/tools/storefront.py export --require-review`, rebuilds every package from scratch (a store's folder is deleted first, so dropped slides disappear), writes `manifests/<store>.json` here and `package.json` in each package, then verifies everything. Re-run it after any change to the review table, `captures/desktop/selection.json`, the mobile renders, the key art, the icon or the catalogs. It takes under a minute (27 seconds on 2026-11-24), most of it hashing the mobile renders.

| Command | Does |
| --- | --- |
| `build.py` | build every store, then verify |
| `build.py --store snap,itch` | build and verify only these |
| `build.py verify` | re-check the files on disk against the manifests, without rebuilding; also repeats the pending and blocked items the build recorded |
| `build.py --stage-appstream` | also copy the AppStream PNGs into `appstream/` here, where their URLs point (for the Git steward only; see AppStream below) |
| `build.py --allow-pending` | exit 0 when the only open items are pending |

Exit status: **0** clean; **1** errors (a store rule broken, a file not matching its manifest, a frame or source missing); **2** pending items only (an input the review asked to change has not changed yet). Blocked slots never fail the run.

## Where things go

- Packages: `../storefront-v2-renders/store-packages/<store>/` relative to the repository root (`/Users/bradley/glob2/storefront-v2-renders/store-packages/` on the machine that built them), outside the repository. Each holds `package.json` (same bytes as `manifests/<store>.json`) and the files to upload.
- Desktop stores: real files (`screenshots/NN-<role>-<WxH>.<ext>`, key art as `<slot>-<WxH>.<ext>`, listing text under `text/`).
- Mobile stores: one folder per store locale, `<locale>/<device>/NN-<role>-<WxH>.png`, each a **symbolic link** to the captioned render in `../storefront-v2-renders/screenshots/`, so the 4 GB of renders are not copied; store-wide images (feature graphic, icons) in `_store-wide/`; the locale's listing text as `<locale>/listing.json`.
- In the manifests, `packages:` and `renders:` prefixes stand for those two outside folders; other paths are relative to the repository root.

Every image entry records its upload order, role, file, pixels, format, mode, bytes, SHA-256, its source file with that file's SHA-256, the treatment (copied unchanged, or a Lanczos reduction with the JPEG quality) and the rules it was checked against. Desktop entries with captions carry the caption field and text: per locale for Microsoft, the English text and language count for AppStream.

## Where the gallery comes from

- **Desktop order and selection:** the "Desktop" table under "Final galleries" in [`../review/round-2-final.md`](../review/round-2-final.md), read row by row: the backticked frame numbers in the Images column, up to the first `;` (so Epic's "then add `08` after `02`" once R8 clears is not read in). GOG's "As Steam" copies Steam's list. Each frame number is resolved to the one capture `NN-*-<WxH>.png` of the store's aspect in `captures/desktop/`, and its role comes from `selection.json` (`08b` is configured as the side-by-side co-play alternative). If the review names a frame with a role (`` `04` battle ``) and `selection.json` gives that file another role, the build fails: that means the capture files were renumbered and the review table needs the new numbers.
- **Mobile order:** the "Mobile" table, keyed by the backticked store-set id. Slides are taken by role from each render manifest, so the order follows the review whatever the render file numbers are; slides the review dropped are left out and reported.
- **Switches:** an AI co-play frame on a store whose `ai_coplay` switch is off in `translations/platforms.json` is an error (Epic and the Mac App Store are off today).
- **Rules and slots:** [`stores.json`](stores.json), with the source of each limit and an `unverified` list per store.
- **1920×1080 JPEGs:** an export in `captures/desktop/web-1920/` whose name starts with the frame number is used unchanged when it fits the store's size, format and byte limit; otherwise the script reduces the native 3840×2160 capture itself (Lanczos, exactly one half, JPEG quality 92 with 4:4:4 chroma, stepping down to 84 only if a store's limit requires).

## Per store (build of 2026-11-24, 19:15)

| Store | Upload contents | Sizes and limits checked |
| --- | --- | --- |
| Microsoft Store | 7 screenshots `01 04 02 08 06 05 03` (hero, battle, build, AI co-play, maps, territory, economy), native PNG, with the caption for every one of 44 locales; poster, box art (2160² and 1080²), super hero (3840×2160 and 1920×1080); listing text for 44 locales | 3840×2160 PNG ≤ 50 MB (6.9–11.3 MB); captions ≤ 200 characters; poster 1440×2160, box 2160²/1080², hero 3840×2160/1920×1080, all PNG without alpha |
| Epic | trailer slot first (**blocked**), then 6 screenshots `01 04 02 06 05 03` (no co-play: switch off); offer landscape, offer portrait, product logo, social preview; text for 31 locales | 1920×1080 JPEG ≤ 4 MB (0.7–1.1 MB); 2560×1440 and 1200×1600 JPEG; logo 960×540 transparent PNG ≤ 1 MB; 1200×1200 JPEG ≤ 4 MB |
| Snap | 5 screenshots `01 04 08b 02 06` (side-by-side co-play third); banner; 256 px icon; English text | JPEG ≤ 2,000,000 bytes, 480–3840×2160, aspect 1:2–2:1; banner 1440×480; icon transparent PNG |
| itch.io | 7 screenshots `01 04 08b 02 06 05 03`; cover; English text | 1920×1080 JPEG; cover 630×500 |
| Mac App Store | 6 screenshots `01 04 02 06 05 03` at 16:10 (no co-play: switch off); text for 38 locales | 2880×1800 PNG, no alpha |
| Steam (prepared only) | 7 screenshots `01 04 02 08 06 05 03`; header, small, main, vertical and library capsules, library hero, library logo; English text | 1920×1080 JPEG, at least 5; capsule sizes as listed in `stores.json`; logo transparent PNG 1280 px wide |
| GOG (prepared only) | 7 screenshots as Steam; main banner, logo, box, two backgrounds; English text | 1920×1080 JPEG; boards at the GOG template sizes |
| AppStream / Flathub | 7 screenshots `01 04 08b 02 06 05 03`, stable names (`hero-1920x1080.png` …), `screenshots.xml` ready for the game's metainfo with every caption language, plus the export's `appstream-fragment.xml` and `desktop-fragment.ini` | 1920×1080 PNG, no alpha |
| Google Play | 44 Play locales × phone 7, 7-inch 7, 10-inch 7 = 924 linked screenshots; feature graphic; 512 px icon; listing text per locale; preview video **blocked** | 1080×1920, 1920×1200, 2560×1600 PNG without alpha, ≤ 8 MB, 2–8 per phone set and 4–8 per tablet set; feature 1024×500 without alpha; icon 512×512 32-bit PNG ≤ 1,024 KB |
| Apple App Store | 38 Apple locales × iPhone 6.9-inch and iPad 13-inch sets; listing text per locale | 1320×2868 and 2064×2752 PNG without alpha, 1–10 per set |
| Amazon | text for its 11 languages, 1024×500 promotional image, icons 512 and 114; screenshots **blocked** (M8) | promo 1024×500 with the wordmark at least 50 px from every edge (read from the key-art manifest); icons 512×512 and 114×114 PNG |

The exact counts, byte totals and open items of the latest run are printed at the end of every build and kept in `../storefront-v2-renders/store-packages/summary.json`.

### AppStream URLs

The intended URLs are `https://raw.githubusercontent.com/Globulation2/glob2-marketing/main/assets/storefront-v2/store-packages/appstream/<name>.png` (listed per image in [`manifests/appstream.json`](manifests/appstream.json) and in `screenshots.xml`). They resolve only after the Git steward runs `build.py --stage-appstream`, commits those seven PNGs (about 20 MB) and pushes to `main`. The names are by role, so they stay the same when the order changes; the game's current metainfo pins a commit hash rather than `main`, and the game-repository steward should decide which form to use.

### Microsoft captions and the import workbook

`desktop_screenshot_caption_N` in the export follows `asset_text.desktop_gallery_order` in `translations/platforms.json`. Since the caption touch-up of 2026-11-24 that list is the reviewed upload order (hero, battle, build, ai_coplay, maps, territory, economy), so caption field N belongs to upload slot N again and the build no longer reports a pending mismatch (rebuild of 2026-11-24, 20:51: no pending items). The manifest still gives every image its caption by role. If the review order and `desktop_gallery_order` drift apart again, the build reports it as pending, and the numbered caption columns of a `microsoft_import.py` workbook must not be fed to Partner Center until they match.

## Blocked, by design

- **Trailer** (V2-08, not finished): Microsoft trailer slot, Epic's first carousel slot, Google Play's preview video, Apple and Mac previews.
- **Amazon screenshots** (review M8): the 10-inch frames are host renders and Amazon wants the app on the right device type. Re-run after emulator or Fire-tablet captures are rendered; then take `blocked` off the `amazon` set in `stores.json`.

## Not packaged, and why

- Microsoft 1:1 app tile icon (300×300): optional; the Store uses the package's own tile logo, which the next build carries.
- Apple and Mac app icons: they come from the build's asset catalog.
- Epic About-section images: no placement decided.

## Unverified rules

Each store's `unverified` list in `stores.json` is copied into its manifest. In short:

- Microsoft: whether every slot of the existing listing takes a 3840×2160 PNG (the 2026-08-24 page says 4K, 50 MB).
- Snap: icon limits not recorded; screenshot limits come from the v1 record (2026-10-30), not re-read; Snap prefers Linux captures and these are macOS captures of the same build.
- itch.io: no published screenshot limit recorded; the 4 MB cap is this tool's own.
- Apple (iOS and Mac): per-file byte limit not recorded.
- Google Play: per-screenshot byte limit not recorded (8 MB is the renderer's ceiling); M9, which build Play users will get.
- Steam: library capsule, library hero and logo sizes are as built by the key-art agent; no Steamworks form has been seen.
- GOG: screenshot rules unconfirmed; board sizes from the template inspected for v1.
- Flathub: current screenshot guidance not re-read for v2.
- Amazon: the 114 px icon is a vector render at that size, which is how this package reads "do not simply scale"; whether Amazon accepts that is not confirmed.

## Pending checks the build makes

The build compares its inputs with what the review asked for and reports each gap as pending (exit status 2):

- `captures/desktop/selection.json` order against the review's Microsoft row (M5);
- each mobile render manifest against the current `screenshots.py`, `caption.html`, `gallery.json`, `fonts.json`, `captures/mobile/selection.json` and the locale's catalog (renders older than a fix);
- render slides the review dropped (opponents) and review slides a render lacks (the iPhone battle slide, M2);
- the Play feature graphic's wordmark margin (M6) and the Steam logo width (S6), read from the key-art manifest;
- `desktop_gallery_order` against the reviewed order (Microsoft captions).

## Dependencies

`uv` reads them from the top of `build.py`: Pillow 11.3.0 and resvg-py 0.5.0 (for the 114 px icon). The export uses the system `python3`.
