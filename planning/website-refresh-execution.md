# Website release and media refresh

[Planning index](README.md) · [Approved storefront rollout](approved-storefront-rollout.md) · [Website localization](website-localization-rollout.md)

## Scope and current state — 2026-11-18

The user identified outdated website links, including Discord; requested greater emphasis on real storefront releases than browser play or direct downloads; supplied a screenshot of a wrapping header; and reported that the game screenshots and homepage recording no longer represent the latest visual quality. Implementation is authorized. The selected colony-building/economics message remains the [positioning reference](../analysis/positioning-v1.md).

Website implementation is in [Globulation2/glob2-online-website](https://github.com/Globulation2/glob2-online-website), branch `codex/website-release-refresh`. Source changes, independent review and rendered verification are in progress. No merge, website deployment or public refresh is claimed by this entry. The website repository follows its own pull-request and deployment rules; the marketing repository's direct-to-main policy does not apply there.

## Public link observations

Checked on **2026-11-18**. Public visibility and availability of the newest build are separate facts; a live listing does not establish that every platform has the same version.

| Destination | Observed state and website treatment |
| --- | --- |
| [Current website downloads](https://glob2.online/downloads/) | HTTP 200; browser early access appears first, direct packages advertise `0.11.4.0`, and the page says no verified production App Store release is listed. These are the existing public presentation, not a current cross-platform release inventory. |
| [Microsoft Store](https://apps.microsoft.com/detail/9PH4FCRMX19F) | Public HTTP 200 product page titled “Globulation 2 - Free download and play on Windows”. Eligible for a Windows storefront link; exact installed release remains a separate qualification. |
| [Apple App Store](https://apps.apple.com/us/app/globulation-2/id6817603328) | Public iPhone/iPad product page. This supersedes the website's absent-App-Store statement. The page says “Designed for iPad. Not verified for macOS”; do not present this URL as evidence of a dedicated native Mac release. New editable Apple candidates remain distinct from the public version; see the [publishing ledger](approved-storefront-rollout.md#latest-apple-candidates-qualified-and-saved--2026-11-17). |
| [Snap Store](https://snapcraft.io/globulation2) | Public product page reports `latest/stable 0.11.6.0`, updated November 18. This is newer than the website's direct-package version and supersedes earlier Snap-version observations. |
| [Google Play public product URL](https://play.google.com/store/apps/details?id=org.globulation2.glob2) | HTTP 404 in the unauthenticated check. Existing closed testing is not a public production release; do not advertise general availability. |
| Epic | November 18 authenticated ledger evidence records Stage entities In review and no Live entities. Its proposed storefront URL is not a public release; see [current gates](approved-storefront-rollout.md#epic-current-review-and-publication-gates--2026-11-18). |
| Discord | Old website invite `https://discord.gg/xnVrafzMD` returned HTTP 404 with `Invite is expired.` A replacement public invite, [Join Globulation2](https://discord.gg/rQn3Br6AFA), was created and independently resolved through Discord's public invite API with HTTP 200 to the intended project community. Website source replacement is pending integration. No outreach was performed. |

## Execution ledger

| Work | Status | Verification or remaining work |
| --- | --- | --- |
| Public destination audit | Complete for the destinations above | Fresh website HTML, official product pages and Discord public API responses reviewed. Other historical links still need page-level audit coverage. |
| Repair Discord destination | Replacement created and validated | Integrate the verified public URL into maintained website data, then verify rendered and deployed links. |
| Storefront-first acquisition flow | In progress in website branch | Link only verified public stores; retain browser/direct packages as secondary choices and truthful platform/version qualification. |
| Header and responsive layout | In progress in website branch | Reproduce the supplied search-page header wrap, fix responsive grouping, and complete two rendered review rounds including desktop, mobile and long/RTL labels. |
| Current gameplay screenshots and homepage video | Capture and replacement pending | Existing media should not be relabeled as the latest release. Verify the running build, capture genuine gameplay, inspect quality, and replace screenshots, recording and matching poster together. |
| Website publication | Pending | Complete repository checks and independent reviews, merge through the website workflow, then confirm the deployed public pages and destinations. |

## Media provenance and remaining gaps

The live homepage references `/brand/colony-loop.mp4`, poster `/brand/colony-1600.webp`, and `/images/home-thriving-colony.webp`, `/images/home-colony-defence.webp`, `/images/home-rival-expansion.webp`. Website Git history records the homepage screenshot refresh in `6b67616` on **2026-10-12**. That is a source-history date, not proof of the exact captured game build or the recording date. The latest user-reported visual improvements postdate that screenshot refresh.

Capture work must establish the actual build/version and preserve genuine game visuals and source provenance. Review economy/colony development, expansion and rival-pressure scenes against the current positioning. Keep video/poster framing consistent, provide a static reduced-motion fallback, and inspect the delivered encodes at actual page sizes. Do not substitute generated or outside imagery. Any later storefront-media rollout must preserve the [approved imagery boundary](approved-storefront-rollout.md#approved-imagery-only--2026-10-30); this website refresh is not evidence of new storefront uploads or replacement approval.

The [October 26 browser capture](../assets/epic-gameplay-v1/README.md) was explicitly rejected for abnormal fog rendering and remains excluded. Historical retained media and current-release captures are distinct evidence sets.
