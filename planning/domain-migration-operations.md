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
The website check remains on its former host until the new website is ready.
Notification recipients were not changed.

## Website gate and remaining operations

Cloud DNS delegation and the new apex/WWW/application records are published.
Firebase custom domains for `glob2.online` and `www.glob2.online` exist on the
existing website site. Newly requested ACME TXT records were added to the personal
Cloud DNS zone. Firebase is still validating certificates and its latest observed
DNS discovery retained obsolete registrar parking answers. Direct HTTPS checks
still rejected the certificate for the new website names. Preserve the old
website and its certificates while this external provisioning completes.

After both new website names have valid HTTPS:

1. Deploy the qualified website source and verify canonical URLs, public routes,
   app links and feed access.
2. Set the former Firebase custom domains' `redirectTarget` to `glob2.online`.
   The REST update mask is `redirectTarget`; this is a domain-level **301**.
   Verify HTTP/HTTPS, apex/WWW, deep paths and query strings before recording the
   redirect as complete. Set new WWW canonicalization separately as appropriate.
3. Replace the website uptime resource and retarget its existing alert policy,
   preserving operational settings and any notification channels.
4. Update OAuth branding home/privacy/terms links to the new website once those
   pages are reachable. The new authorized domain and application callback are
   already saved. Browser ownership was yielded to the separate storefront work;
   avoid competing UI actions.

Firebase documents that certificate provisioning can take up to 24 hours after
DNS changes. The configured records and a pending certificate are not proof of
website availability or a completed redirect. See
[Firebase custom-domain guidance](https://firebase.google.com/docs/hosting/custom-domain).
