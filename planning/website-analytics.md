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

Property creation and saved settings are complete. **Website instrumentation, production publication, event receipt and usable reports remain unverified at this checkpoint.** Account configuration alone does not establish collection from the live site. Website source review and deployment are in progress separately.

## Measurement goals and interpretation

- Establish dated website visitor and page-view totals after verified collection begins, using the configured Toronto reporting timezone and equivalent comparison periods. Record the exact visitor metric shown by GA4. The implementation under review is opt-in: users represent consenting browsers, with Do Not Track and Global Privacy Control excluded, rather than all visitors or a census of individual people. Shared devices, cookie deletion and script blocking further affect counts.
- Inspect acquisition source/medium and campaign data where actually received. A traffic change after a post is temporal association; attributing that change to LinkedIn requires supporting referral/campaign evidence and still does not establish causation.
- Keep website visits, outbound Play/store clicks, game account activity, installations and actual gameplay distinct. Do not claim outbound-click measurement until the implemented events and saved reports are verified.
- Preserve the collection-start boundary. A newly installed tag does not reconstruct earlier website visits. An incomplete first day is not comparable with a full previous day, and a fresh property has no prior-period site baseline.
- Identify operator verification traffic separately when interpreting launch figures. A successful test visit or click establishes a technical path, not an acquired player or campaign result.

## Existing evidence and limits

The earlier website inventory reported no identified public-site analytics or measured acquisition funnel. It was a bounded source review, not a comprehensive audit of private accounts. See the [historical product inventory](../facts/product.md#measurement-and-account-infrastructure).

A Search Console domain property for `glob2.online` was verified on **2026-10-31** for OAuth branding, as recorded in the [domain operations ledger](domain-migration-operations.md#google-branding-and-ownership-follow-up--2026-10-31). Search Console search-performance figures concern Google search exposure/clicks; no export or website traffic trend has been recorded here.

Game administration reporting is a separate source-defined system for authenticated guest/registered account-day activity, with anonymous visitors excluded. Its implementation does not establish current live player totals or website visitor counts.

## Remaining verification

1. Review and merge the website implementation under that repository's own instructions, with privacy wording and collection behavior reviewed against actual configuration.
2. Publish the reviewed website source and record the exact source/deployment receipt.
3. Verify live tag loading and the actual collection request/event receipt, distinguishing browser transmission from provider processing and reporting.
4. Record collection start, report availability and any collection/access limitations. Compare complete periods only after data exists; preserve any earlier server/platform evidence separately if subsequently found.
