# Domain migration operations handoff

[Migration ledger](domain-migration.md) · [Planning index](README.md)

Observed and changed on **2026-10-30**. This record describes the live application
transition and the remaining website gate; it is not evidence of a new game
release. All deployment operations targeted personal project
`bradley-personal-20261027`. Existing buckets whose names contain `pharaoh-418820`
were retained. The former domain registration was not changed.

## Application state and restart safety

The existing `glob2-staging` VM in `northamerica-northeast2-a` serves both
`app.glob2.online` and `app.glob2online.com`. Its canonical origin and advertised
realtime endpoint use the new hostname. The API, relay and edge retained their
existing image references; no image build, image pull or game release was run.
API and relay health checks passed. Active matches were checked immediately before
service transitions and were zero. The aggregate account count was 307 before and
after. Existing database, signing-key, certificate and other persistent volumes
were retained.

Runtime configuration remains in `/opt/glob2/config/production.env` and
`/opt/glob2/config/instance.yaml`; Compose is
`/opt/glob2/src/deploy/compose.yaml`. Private backups are retained beside the
changed configuration files. Do not publish their contents.

The persisted environment selects `app.glob2.online` as `GLOB2_DOMAIN`,
`https://app.glob2.online` as `GLOB2_PUBLIC_ORIGIN`, and the former application
hostname as `GLOB2_ADDITIONAL_DOMAIN` and `GLOB2_AUTH_REDIRECT_DOMAIN`.
`instance.web.allowedOrigins` and `GLOB2_RELAY_ALLOWED_ORIGINS` include both
application HTTPS origins. The relay list is comma-separated. The live Compose
file includes the corresponding relay override and edge environment fields.

The current edge image embeds its Caddy configuration. A graceful reload alone
would not persist the migrated environment across a container restart. After
checking for active matches, the edge was recreated with its existing image,
certificate volumes and a temporary read-only configuration mount:

```text
/opt/glob2/config/domain-migration.Caddyfile:/etc/caddy/Caddyfile:ro
```

The file starts with the existing image configuration and adds only the migration
sign-in matcher. The final container environment and mount were inspected after
recreation. A missing scoped `GLOB2_PUBLIC_ORIGIN` entry was corrected with a
second short edge recreation; the correction retained image digest
`sha256:f1aaadea67d60630cab9a664f30b051975b0d6d2fe2d73535926d6949f1e82f0`.
The API, relay and database were not restarted for those edge corrections.

### Remove the temporary edge bridge on the next qualified deployment

The maintained game and release-mirror sources now contain the sign-in matcher,
its environment fields, and the relay-origin override. When a qualified Caddy
image containing those changes is deployed:

1. Preserve the private runtime environment, instance configuration and persistent
   volumes. Confirm the candidate source/image contains all migration settings.
2. Reconcile the deliberate domain changes in the VM checkout before checking out
   another revision. The live Compose file has local migration changes; avoid a
   blanket reset or clean that could discard concurrent work.
3. Remove the temporary `/etc/caddy/Caddyfile` bind from Compose so the qualified
   image supplies its maintained configuration. Keep the canonical and former-host
   environment settings and both origin allowlists.
4. Validate the effective configuration; check active matches before an edge
   recreation. Recheck both hosts, sign-in redirects, recovery routes and realtime.
5. Retire the bridge file only after successful deployment and rollback review.
   Do not leave a host configuration silently overriding future image updates.

## Verified application behavior

- New-host TLS is valid. Both instance endpoints advertise
  `https://app.glob2.online` and `wss://app.glob2.online/realtime`.
- Existing-account Google sign-in completed through the new callback and returned
  to the application. Both former and new OAuth origins/callbacks remain
  configured; the existing personal-project OAuth client and secrets were retained.
- Old-host GET `/signin` and `/auth/*/start` return **302** to the new host,
  preserving the path and encoded query. This begins the OAuth state cookie on
  the same origin that receives its callback. Callbacks and POSTs are excluded
  from this narrow redirect.
- Old-host `/play/`, `/api/v1/instance` and association files remain **200**.
  Both browser-game hosts retain the isolation headers. WebSocket upgrades were
  **101** for all four combinations of former/new host and browser Origin.
- The tests above did not complete a multiplayer match. Existing browser saves
  remain origin-bound; they are not automatically copied between domains.
  Browser cookies also do not transfer between the two domain families. Native
  access tokens may need refresh after the issuer change; opaque refresh and
  device credentials remain backed by the same database. Retain the former
  application recovery and API endpoints during qualification of shipped clients.

The currently deployed web assets still contain some former-domain website
guide/download links. Their exact build provenance does not justify rebuilding
unrelated application code during this cutover. These links depend on the pending
former-website redirects until a separately qualified web release replaces them.
The embedded design-system revision also keeps theme selection in the new app's
origin-local storage but does not recognize the new shared website theme cookie;
cross-subdomain preference sharing awaits the qualified frontend update.

## Feeds, variables and monitoring

The public feed bucket retained its existing name and URLs. Its CORS configuration
now allows new apex/WWW origins alongside all prior origins. A request for the
rankings object returned **200** and
`Access-Control-Allow-Origin: https://glob2.online`.

The website repository variable `API_ORIGIN` now selects the new application
origin. The release-mirror variable `GLOB2_ONLINE_WEBSITE` selects the new website.
Readback confirmed both values. Updating them did not dispatch a release.

Cloud Monitoring does not permit changing an uptime check's monitored resource.
A replacement application check, `glob2-multiplayer-app-B2WF84Y7Drw`, targets
`app.glob2.online` with the previous HTTPS, certificate validation, API path,
five-minute interval and USA probe settings. The existing application availability
policy now follows that check. The former check,
`glob2-multiplayer-app-rI7tosdUrOI`, remains as **Glob2 app legacy compatibility**.
After both new website names passed HTTPS, replacement website check
`glob2-public-website-0-k989RRMuM` was created for `glob2.online`; existing policy
`824494495873556283` was retargeted with the same settings. The former website
check remains as **Glob2 website legacy compatibility**. Notification recipients
were not changed.

## Website HTTPS and deployment transition

Cloud DNS delegation and the new apex/WWW/application records are published.
Firebase custom domains for `glob2.online` and `www.glob2.online` exist on the
existing website site. Newly requested ACME TXT records were added to the personal
Cloud DNS zone. Earlier checks rejected the website certificates while Firebase
retained obsolete registrar parking answers in its discovery cache.

At **20:25 America/Toronto on 2026-10-30 / 00:25 UTC on 2026-10-31**, both new
website names returned HTTPS **200** with valid hostname certificates. Firebase
reported `HOST_ACTIVE` and `OWNERSHIP_ACTIVE`, with `CERT_PROPAGATING` / `TEMPORARY`
and no issues. This establishes observed HTTPS readiness; managed-certificate
propagation is still in progress.

[Website PR #57](https://github.com/Globulation2/glob2-online-website/pull/57)
merged as `7d0d5e401c42b8d61cbec3598f489311f5409964`. The [main workflow](https://github.com/Globulation2/glob2-online-website/actions/runs/41150137135)
passed verification, including all three hosted browser projects, but its publish
preview smoke encountered stale Firebase edge redirect configuration immediately
after candidate release. The candidate API configuration was correct; the failed
workflow did not promote production.

The exact existing candidate subsequently passed the complete smoke check:
**29 handbook chapters and 237 immutable media assets**. The authorized operator
then promoted that same immutable version, `c1941eff894c0639`, as release
`1793407232643000` at **20:40:32 America/Toronto on 2026-10-30 / 00:40:32 UTC on
2026-10-31**. No rebuild or asset substitution occurred. The previous production
version is `8b593ba5415e69f4`; preserve it as the rollback reference.

The full live `https://glob2.online` smoke check passed after promotion. Home,
downloads, privacy, terms and learn routes returned **200** with new-domain
canonicals and no former-domain player links. Robots and sitemap use the new
hostname; the theme metadata identifies `e826954`; the feed returned **200** with
the new-origin CORS header. The original workflow publish failure remains
historical evidence alongside this separate successful operator promotion.

Around **20:42 Toronto**, the former apex/WWW domains and new WWW received
`redirectTarget=glob2.online`. Both WWW hosts initially passed **301** checks while the former apex still returned
stale **200** responses. The apex converged naturally. At **20:44 Toronto on
2026-10-30 / 00:44 UTC on 2026-10-31**, all **12** HTTP/HTTPS root/deep-path cases
for the former apex/WWW and new WWW returned **301** to `https://glob2.online`,
preserving encoded queries exactly. Followed privacy routes on all three
redirecting hosts reached the new **200** page. Firebase operations completed
without errors, with active host/ownership/certificate states and no legacy-domain
conflict. Former-domain certificates remain valid. The full live availability
monitor passed.

## Verification evidence and remaining operations

Sanitized operational outcomes are recorded above. Detailed local evidence is in
the website checkout's ignored `artifacts/domain-migration/`: `promotion.json`,
`candidate-smoke.log`, `live-smoke.log`, `live-site-checks.json`,
`domain-redirect-updates.json`, `domain-redirect-state.json`,
`domain-redirect-checks.json` and `live-monitor.log`. These local artifacts are
operator evidence, not public repository files; preserve private configuration
and credential material outside Git.

The website deployment and full website redirect matrix are complete. Remaining
work is separate:

1. Update OAuth branding home/privacy/terms links after verifying their current
   console fields. The new authorized domain and application callback are already
   saved. Browser ownership remains with the separate publishing work; avoid
   competing UI actions.
2. Follow the [storefront destination ledger](approved-storefront-rollout.md#destination-status)
   for verified new-domain listing fields rather than duplicating their saves.
   Apple's global privacy/service field still uses
   `https://app.glob2online.com/account`; its service-destination migration remains
   outstanding and must preserve its purpose.
3. Check the game repository's About homepage through its UI when the browser
   lease is available. The available REST update path returned 404; this does not
   establish that a maintainer cannot edit the website's About field.
4. Complete review/verification of the website operations and bounded Hosting
   convergence follow-up in [PR #58](https://github.com/Globulation2/glob2-online-website/pull/58).
   Preserve the original transient edge/first WebKit failure evidence; do not
   treat the original main publish job as successful.
5. Replace former-domain links and reconcile theme-preference sharing in the
   separately qualified application frontend. Remove the temporary edge bridge
   on the next qualified image deployment, using the earlier cleanup checklist.

The hourly `finish-glob2-domain-migration` follow-up is saved for unfinished
migration work. A scheduled check is separate from the verified deployment and
redirect outcomes above. Keep former-domain registrations, DNS and certificates
maintained for inbound links and old application-client recovery.
