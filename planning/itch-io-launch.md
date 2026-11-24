# itch.io launch

[Planning index](README.md) · [Approved rollout](approved-storefront-rollout.md) · [Prior account check](storefront-localization-rollout.md#existing-account-authentication-check--2026-10-31)

## Published on 2026-11-23

[Globulation 2 on itch.io](https://genixpro.itch.io/globulation-2) is public. A fresh editor load confirmed Public visibility, the four desktop download labels and platform flags, and the saved cover and four approved gameplay screenshots. All four upload rows reported Success. The gallery uses the approved colony PNG and the three corresponding approved Snap JPEG derivatives. The public page fetched without cookies contained all four download links with upload identifiers, all four gallery images and the tutorial URL.

Signed-out binary transfers, itch app installation, platform launch and search indexing remain unverified.

## Initial access attempt on 2026-11-23

The project owner authorized launching Globulation 2 on itch.io and tracking it here. Opening the [creator dashboard](https://itch.io/dashboard) redirected to the login page. Cloudflare's security verification remained visible on recheck, and an authenticated dashboard was unavailable. Existing project ownership remains unverified. This attempt ended before draft creation, file upload or publication. The authenticated follow-up below superseded this access blocker.

## Creator access and saved draft

The owner registered an itch.io account and signed in. Its dashboard offered to upload the first game. A [Globulation 2 draft](https://genixpro.itch.io/globulation-2) saved with the Strategy genre, payments disabled, the approved cover and copy, desktop installation instructions, tutorial, website and source links, and the tags `real-time-strategy`, `base-building`, `resource-management` and `open-source`. The saved AI Disclosure categories were Graphics, Text & Dialog and Code. The platform email-verification requirement was cleared before binary uploads.

## Listing

Use **Globulation 2** as the title and the approved short pitch and About copy. Lead with colony building and economy, with autonomous creatures as the distinctive mechanic. Use the Strategy genre and relevant tags such as real-time strategy, colony building and resource management. Set the initial listing to free with payments disabled. Display the [first-session tutorial](https://glob2.online/learn/getting-started/) as the browser play route and use `https://glob2.online/` as the official website. [Approved copy](approved-storefront-rollout.md#approved-copy) · [itch.io RTS browse](https://itch.io/games/tag-real-time-strategy) · [Pricing options](https://itch.io/docs/creators/pricing)

Use the approved landscape illustration for the cover and the four approved desktop gameplay screenshots in their existing order. A short gameplay clip showing the colony respond to new priorities is optional and requires approved source footage or separate approval. [Approved cover and gallery](../assets/storefront-approved-v1/README.md) · [itch.io creator guidelines](https://itch.io/docs/creators/quality-guidelines)

### AI disclosure evidence

For release 0.11.7.0, Graphics covers the generated environment in the approved cover and the shipped Trail material. Code covers AI-coauthored changes to shipped game code. Text covers AI-assisted in-game translations. The shipped soundtrack credits identify original scores and rendered samples. They provide no evidence for selecting Audio. Reassess these categories when the release or listing assets change. [Cover provenance](../assets/epic-v5/README.md#source-identity-and-transformations) · [Trail provenance](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/trail/provenance.json) · [Code change](https://github.com/Globulation2/glob2/commit/8080cf5b0d) · [Translation change](https://github.com/Globulation2/glob2/commit/808beba107) · [Shipped music credits](https://github.com/Globulation2/glob2/blob/v0.11.7.0/docs/assets/source-attribution.md#third-party-asset-attribution)

## Initial downloads

As of 2026-11-23, the official downloads page advertises desktop release **0.11.7.0**. Use the current public release at upload time. For 0.11.7.0, these are the proposed files and the SHA-256 digests published on the official downloads page. All four files were downloaded on 2026-11-23 and matched the published SHA-256 digests. The Windows portable ZIP passed `unzip -t`. Platform launch and itch.io installation checks remain pending. [Official downloads and requirements](https://glob2.online/downloads/)

| Platform | File | Published SHA-256 |
| --- | --- | --- |
| Windows x86-64 | `glob2-0.11.7.0-windows-x86_64.zip` | `f3246113413101aa051939b93dbe374c612f64e0dc9b89c2f0031613a5b8ec53` |
| macOS Apple Silicon | `Glob2-0.11.7.0-macos-arm64.dmg` | `0aafb6793c1f56f7f23de82fa7a5fae122cde7bd40c2199146b570d37e5019b6` |
| macOS Intel | `Glob2-0.11.7.0-macos-x86_64.dmg` | `014447d7ef24cc85c8f8dc23a75513d5057f6c6a8451b20be282a95802409bb1` |
| Linux x86-64 | `glob2.flatpak` | `df8f226598b69670b1b556036c6b61e8165dc39f549bc7239ca35699229f2b0f` |

The verified files were uploaded directly to itch.io. The listing covers Windows ZIP extraction, macOS DMG installation and the Flatpak runtime, and links to the release source. Verify replacement files against their published checksums before uploading each new release, preserve the matching source and notices, and check platform flags and installation instructions after saving. [Release files and source](https://github.com/Globulation2/glob2/releases/tag/v0.11.7.0) · [Creator upload guide](https://itch.io/docs/creators/getting-started)

## Verification and measurement

For each update, reload the editor and compare the cover and gallery with the approved sources. Open the public page signed out and check installation instructions, downloads, cover, gallery and tutorial destination. Track search indexing separately from public visibility. [itch.io indexing requirements](https://itch.io/docs/creators/getting-indexed)

Use itch.io views and downloads and, where available, consented Glob2 Online play-click data attributed to the listing. Record the first month's observed counts and coverage before deciding whether to embed a web build. [itch.io creator analytics](https://itch.io/docs/creators/faq) · [Glob2 website analytics notice](https://glob2.online/downloads/)

## Private browser preview

A separate private draft, **Globulation 2 Browser Preview**, tested the full released 0.11.7.0 browser package (`4fd11cca47d9d3ab`). The upload archive contained 484 files, about 135 MB zipped and 217 MB extracted. The largest file was 30.15 MB. The locally served package entered a Lava Shield custom game.

The first itch.io upload failed with a core short read. The CDN labeled an entire mixed-format asset blob as gzip because it began with a gzip member. Only that leading member was delivered or decoded. The corrected archive moved a non-gzip entry first and recalculated offsets in both runtimes. All 865 embedded files matched byte for byte. With SharedArrayBuffer enabled, the corrected private draft ran an interactive introductory match in Chrome. The default small embed triggered the phone layout on desktop.

Save and reload, other browsers, a full skirmish inside itch.io, and multiplayer remain untested. The browser shell currently selects the hosting origin and the app API returned HTTP 404 to a preflight from `https://html.itch.zone`. Shared rooms require client and backend integration. The public desktop listing was unchanged.
