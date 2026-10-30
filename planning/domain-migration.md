# Canonical domain migration

[Planning index](README.md) · [Storefront rollout](approved-storefront-rollout.md) · [Repository evidence](../facts/repositories.md) · [Channel evidence](../facts/channels.md)

## Authorization and destination

On **2026-10-30**, the user requested switching `glob2online.com` to **`glob2.online`** across repositories, links and other uses, with the older domain redirecting to the new domain. This authorizes the corresponding maintained source, hosting and controlled-listing changes. It does not itself establish that DNS, TLS, application authentication or external publisher fields have migrated.

Use **`https://glob2.online/`** for the project website. Application-subdomain migration, redirects and production readiness require the separate checks below. Preserve paths and query strings when redirecting old public URLs; verify both HTTP and HTTPS, apex and `www`, and any existing application endpoints. An HTTPS redirect requires working TLS on the old hostname.

## Execution ledger

| Surface | Recorded status | Remaining verification |
| --- | --- | --- |
| Marketing upload fields | Committed and pushed as `7ea1dfe`: updated `assets/storefront-approved-v1/snap/listing-fields.json` website to `https://glob2.online/`. | This is the maintained upload source; separately verify any live Snap publisher change. |
| Marketing reference drafts | Website, privacy and browser links in the superseded Epic/reusable profile drafts use the new domain, with a migration note distinguishing selected URLs from verified availability. | Browser runtime and privacy-page coverage require production checks. Historical copy remains superseded. |
| Marketing evidence | Original observed URLs retained in `facts/`, the gameplay capture manifest and dated storefront-verification entries; indexes/rollout now explain their historical role. | Do not replace dated evidence with an unobserved new URL or interpret those links as current upload instructions. |
| Website repository and deployment | Maintained canonical URLs, sitemap/robots/social image, player links, policies, app-path redirects, capture/smoke/monitor helpers and test expectations updated locally; production deployment held pending healthy new hosts. Feed CORS retains former origins during transition. | Final dependency integration/checks and steward commit remain in progress; do not push an automatically deployed website cutover while its new application links are unavailable. |
| Game/application repository | Audit and implementation in progress. | Check browser assets, APIs, CORS, CSP, cookies, authentication allowlists, account links and store metadata as applicable. |
| Design-system repository | Committed and pushed as `e8269547492feaceaae98957bb4aed6912989636`. Theme cookies now select the current HTTPS parent (`glob2.online` or the former parent during transition); examples/docs use the new domain. Generated distribution artifacts included. | Unit tests passed (16); Chromium/WebKit cookie-sharing checks passed for both domains (4). Firefox cannot launch on this workstation due to a profile-folder error before assertions. Candidate consumer-install smoke and downstream SHA integration remain in progress. |
| DNS, TLS and old-domain redirects | User reports registrar delegation saved to all four assigned Cloud DNS nameservers; registry propagation remains unverified. New Firebase custom domains and GCP ACME preparation are recorded by the hosting work unit; application preparation is in progress. | Recheck authoritative delegation, certificate issuance and new-host readiness before cutover; then verify permanent old-domain redirects with paths and query strings preserved. Preparation is not a verified live redirect. |
| Controlled external listings and repository metadata | Website-field updates deferred until the new destination is healthy. The previous [rollout](approved-storefront-rollout.md) establishes separate historical listing states; this task has not verified a new-domain save in those consoles. | Verify/save website, support and privacy fields where controlled after destination qualification; coordinate existing storefront work and record inaccessible consoles rather than claiming changes. |
| Independent catalogs and historical references | Outside direct source control unless separate edit access is established. | Keep old-domain redirects working for incoming links. Preserve original historical quotations, source URLs and capture provenance. |

## Evidence preserved intentionally

The `facts/` records are dated observations from the earlier estate/platform audit, including the former website and `app.glob2online.com`. The approved storefront rollout records the Snap website URL actually verified at **18:06 America/Toronto on 2026-10-30**. The `assets/epic-gameplay-v1/capture-manifest.json` URLs identify the actual runtime and downloaded assets used for that capture. These remaining old-domain strings are historical evidence, not maintained marketing destinations.

Untracked Windows storefront work present before this task is outside this migration unit and remains untouched. The user supplied a registrar handoff confirming the nameserver save; this ledger records the relevant outcome without private registrar/account details.

## Validation and handoff

The marketing unit was checked with a case-insensitive domain search, JSON parsing, relative-link checks for edited Markdown, and `git diff --check`. Completed Git revisions and cross-repository/production outcomes are recorded as each unit is integrated. A source replacement is not a deployed redirect or verified external listing update.
