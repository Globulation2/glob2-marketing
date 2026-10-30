# Canonical domain migration

[Planning index](README.md) · [Storefront rollout](approved-storefront-rollout.md) · [Repository evidence](../facts/repositories.md) · [Channel evidence](../facts/channels.md)

## Authorization and destination

On **2026-10-30**, the user requested switching `glob2online.com` to **`glob2.online`** across repositories, links and other uses, with the older domain redirecting to the new domain. This authorizes the corresponding maintained source, hosting and controlled-listing changes. It does not itself establish that DNS, TLS, application authentication or external publisher fields have migrated.

Use **`https://glob2.online/`** for the project website. Application-subdomain migration, redirects and production readiness require the separate checks below. Preserve paths and query strings when redirecting old public URLs; verify both HTTP and HTTPS, apex and `www`, and any existing application endpoints. An HTTPS redirect requires working TLS on the old hostname.

## Execution ledger

| Surface | Recorded status | Remaining verification |
| --- | --- | --- |
| Marketing upload fields | Updated `assets/storefront-approved-v1/snap/listing-fields.json` website to `https://glob2.online/`. | This is the maintained upload source; separately verify any live Snap publisher change. |
| Marketing reference drafts | Website, privacy and browser links in the superseded Epic/reusable profile drafts use the new domain, with a migration note distinguishing selected URLs from verified availability. | Browser runtime and privacy-page coverage require production checks. Historical copy remains superseded. |
| Marketing evidence | Original observed URLs retained in `facts/`, the gameplay capture manifest and dated storefront-verification entries; indexes/rollout now explain their historical role. | Do not replace dated evidence with an unobserved new URL or interpret those links as current upload instructions. |
| Website repository and deployment | Audit and implementation in progress. | Record exact completed source paths, commits and production checks. |
| Game/application repository | Audit and implementation in progress. | Check browser assets, APIs, CORS, CSP, cookies, authentication allowlists, account links and store metadata as applicable. |
| Design-system repository | Audit in progress. | Record whether maintained references exist and which were changed. |
| DNS, TLS and old-domain redirects | Audit in progress; no completed change recorded here yet. | Confirm authoritative host configuration, new-host readiness and path/query-preserving redirect behavior. |
| Controlled external listings and repository metadata | Audit in progress; the previous [rollout](approved-storefront-rollout.md) establishes separate historical listing states. | Verify/save website, support and privacy fields where controlled; record inaccessible consoles rather than claiming changes. |
| Independent catalogs and historical references | Outside direct source control unless separate edit access is established. | Keep old-domain redirects working for incoming links. Preserve original historical quotations, source URLs and capture provenance. |

## Evidence preserved intentionally

The `facts/` records are dated observations from the earlier estate/platform audit, including the former website and `app.glob2online.com`. The approved storefront rollout records the Snap website URL actually verified at **18:06 America/Toronto on 2026-10-30**. The `assets/epic-gameplay-v1/capture-manifest.json` URLs identify the actual runtime and downloaded assets used for that capture. These remaining old-domain strings are historical evidence, not maintained marketing destinations.

Untracked Windows storefront work present before this task is outside this migration unit and remains untouched.

## Validation and handoff

The marketing unit was checked with a case-insensitive domain search, JSON parsing, relative-link checks for edited Markdown, and `git diff --check`. Completed Git revisions and cross-repository/production outcomes are recorded as each unit is integrated. A source replacement is not a deployed redirect or verified external listing update.
