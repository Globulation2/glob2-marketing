# Website analytics setup and measurement

[Planning index](README.md) · [Task ledger](tasks.md) · [Product measurement inventory](../facts/product.md#measurement-and-account-infrastructure)

## Authorization and question — 2026-11-20

The user asked whether traffic to `https://glob2.online/`, particularly unique visitors, had increased after a boosted LinkedIn post, then authorized setting up analytics. This authorizes the website measurement setup recorded here; it does not establish a historical visitor baseline, marketing lift or player conversion.

The supplied LinkedIn screenshot showed **12,073 impressions**, **10,002 members reached**, and **98% out-of-network impressions** for a post shown as one day old. These are platform exposure figures, not measured visits to Glob2. No website referral totals or LinkedIn click totals were supplied with that evidence.

## Account configuration verified — 2026-11-20

The coordinating agent created a Google Analytics 4 property and web stream for `https://glob2.online/` and verified the following saved settings in the authenticated console. Private account identifiers and screenshots are omitted from this public record.

| Setting | Verified saved state |
| --- | --- |
| Public website measurement ID | `G-C1ZQ1XR0J1` |
| Reporting timezone / currency | Toronto / CAD |
| Enhanced measurement | Off |
| Event/user data retention | Two months |
| Reset retention on new activity | Off |
| Google signals | Off |
| User-provided data collection | Off |
| Granular location/device collection | Off |
| Advertising personalization | Disabled in all 307 listed regions |

The Events console subsequently showed `play_click`, `download_click` and `store_click` enabled as key events, each created for code-emitted events, with no default monetary value and **once-per-session** key-event counting. This setting deduplicates each key-event conversion count within a session; it does not suppress raw click event counts. A fresh server reload also confirmed exactly one custom-dimension row: **Destination**, event scope, event parameter `destination`. These are saved reporting definitions, not evidence that any production events have arrived.

The Reports snapshot was saved using the **User behavior** template. Saved account/report configuration is distinct from production collection and provider processing; subsequent execution states are recorded below.

## Source review and production publication

Website [PR #76](https://github.com/Globulation2/glob2-online-website/pull/76) merged as `f5b047885ba5b68f63e40e0621e23c0a4583bdf3`. Its completed verification included **50 Node tests, 29 Python tests and 421 browser passes with two intentional skips across three engines**. Independent content/design review covered two rendered rounds at 360px and 1440px, including the actual light and Night themes. An initial dark-theme capture gap was corrected before review completion. Consent copy, equal Allow/Reject actions, mobile wrapping and desktop placement passed that bounded visual review.

The reviewed implementation emits `page_view`, `play_click`, `store_click` and `download_click` only after permission on the canonical production hostname. The footer provides Analytics settings to change that choice. Campaign labels are restricted; arbitrary query strings/fragments are excluded and referrers are reduced to origins. Enhanced measurement remains disabled. Source and operational details are maintained in the website's [analytics documentation](https://github.com/Globulation2/glob2-online-website/blob/f5b047885ba5b68f63e40e0621e23c0a4583bdf3/docs/analytics.md).

The separate game-source privacy update, [PR #1880](https://github.com/Globulation2/glob2/pull/1880), merged as `0900dd137871bded2132994714e5b3e2cc6cac63` after its required checks. This source merge is not evidence of a separate game/application deployment.

The website's [production run 44865751626](https://github.com/Globulation2/glob2-online-website/actions/runs/44865751626) completed successfully for exact source `f5b047885ba5b68f63e40e0621e23c0a4583bdf3`, with verification and publication passing, including immutable preview smoke and promotion. The production receipt identifies **Hosting version `473a3ce9b17b83e3`**, release `1795235753601000`, released **2026-11-21 at 04:35:53.601 UTC / November 20 at 23:35:53.601 Toronto**. The source worker independently read back that server release time through the Firebase API.

## Live collection verification — 2026-11-20 at 23:36 Toronto

A fresh canonical-site browser emitted **zero Google requests before opt-in**. After allowing analytics, Google's collection endpoint returned **HTTP 204** for exactly one `page_view` and each of the three exercised intent events: `store_click` (`microsoft`), `play_click` (`browser`) and `download_click` (`installer`), all addressed to `G-C1ZQ1XR0J1`. These requests occurred at **2026-11-21 04:36:56.913–04:36:57.075 UTC**, or November 20 at **23:36 Toronto**. The test used internal/QA campaign labels and `analytics_verification`; these are operator validation traffic, not acquired-player evidence.

The live check also confirmed host-only 90-day analytics cookies, zero Content Security Policy errors, and withdrawal through Reject analytics clearing the cookies and reloading. The source worker retained the detailed receipt in the website's ignored `artifacts/analytics/live-receipt.json`; raw client identifiers and browser artifacts are excluded from this public repository.

**Publication and accepted live collection requests are verified. Provider-processed Realtime/report evidence remains pending at this checkpoint.** An HTTP 204 response alone does not establish usable processed acquisition reports or a traffic trend.

## Measurement goals and interpretation

- Establish dated website visitor and page-view totals after verified collection begins, using the configured Toronto reporting timezone and equivalent comparison periods. Record the exact visitor metric shown by GA4. The implementation is opt-in: users represent consenting browsers, with Do Not Track and Global Privacy Control excluded, rather than all visitors or a census of individual people. Shared devices, cookie deletion and script blocking further affect counts.
- Inspect acquisition source/medium and campaign data where actually received. A traffic change after a post is temporal association; attributing that change to LinkedIn requires supporting referral/campaign evidence and still does not establish causation.
- Keep website visits, outbound Play/store clicks, game account activity, installations and actual gameplay distinct. Do not claim outbound-click measurement until the implemented events and saved reports are verified.
- Preserve the collection-start boundary. A newly installed tag does not reconstruct earlier website visits. An incomplete first day is not comparable with a full previous day, and a fresh property has no prior-period site baseline.
- Identify operator verification traffic separately when interpreting launch figures. A successful test visit or click establishes a technical path, not an acquired player or campaign result.

## Existing evidence and limits

The earlier website inventory reported no identified public-site analytics or measured acquisition funnel. It was a bounded source review, not a comprehensive audit of private accounts. See the [historical product inventory](../facts/product.md#measurement-and-account-infrastructure).

A Search Console domain property for `glob2.online` was verified on **2026-10-31** for OAuth branding, as recorded in the [domain operations ledger](domain-migration-operations.md#google-branding-and-ownership-follow-up--2026-10-31). Search Console search-performance figures concern Google search exposure/clicks; no export or website traffic trend has been recorded here.

Game administration reporting is a separate source-defined system for authenticated guest/registered account-day activity, with anonymous visitors excluded. Its implementation does not establish current live player totals or website visitor counts.

## Remaining verification

1. Verify provider-processed event receipt in Realtime, separately from the accepted browser requests.
2. Record ordinary report availability and any collection/access limitations. Compare complete periods only after data exists; preserve any earlier server/platform evidence separately if subsequently found.
