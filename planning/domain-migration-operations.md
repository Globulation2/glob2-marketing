# Domain migration operations handoff

[Migration ledger](domain-migration.md) · [Planning index](README.md)

Initial migration observed and changed on **2026-10-30**; browser metadata and
domain-ownership follow-up observed on **2026-10-31**. This record describes the live application
transition, completed website/qualified frontend deployment and remaining
browser-only metadata handoff; it is not evidence of a new game release. All deployment operations targeted personal project
`bradley-personal-20261027`. Existing buckets whose names contain `pharaoh-418820`
were retained. The former domain registration was not changed.

## Application state and restart safety

The existing `glob2-staging` VM in `northamerica-northeast2-a` serves both
`app.glob2.online` and `app.glob2online.com`. Its canonical origin and advertised
realtime endpoint use the new hostname. During the initial canonical-domain
transition, the API, relay and edge retained their existing image references;
no image build, image pull or game release was run for that transition.
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

Initially the old edge image embedded its prior Caddy configuration. A graceful
reload alone would not persist the migrated configuration across a container
restart. After
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

### Temporary edge bridge retired

The successful qualified frontend rollout below **removed** the temporary
`/etc/caddy/Caddyfile` bind. The current image bakes the reviewed migration
configuration. Certificate volumes, the read-only `/srv/play` bind, both domain
allowlists and canonical-origin settings remain in place. The old bridge file and
private rollback snapshot are retained only for rollback; they no longer override
the running image.

For a future rollback, restore the prior image and bridge bind together while
preserving the public bridge's original ownership and **0644** mode. Private
backups and environment files remain private; never transfer a backup's **0600**
mode onto a public runtime configuration file. Avoid blanket checkout/reset/clean
operations on the VM's deliberately modified deployment checkout. Recheck active
matches, both hosts, sign-in, recovery paths and realtime after any separately
reviewed edge transition.

## Frontend activation incident and recovery

The first narrow frontend activation attempt failed its immediate TLS startup
probe. That initial result remains inconclusive: it does not establish a
candidate regression or a successful rollout. At the recovery point described
below, the candidate had been rolled back and was not deployed. The later
successful rollout is recorded separately; it does not change this incident.

The automatic rollback introduced a separate operator error. It restored the
private backup's **0600** mode onto the non-secret public Caddy bridge rather
than restoring the public file's original metadata. The old non-root Caddy then
could not read its configuration, logged permission denied and restarted in a
loop. This caused a real application-access outage; no duration is inferred
from the available observations.

Recovery restored the exact reviewed public bridge and old image digest
`sha256:f1aaadea67d60630cab9a664f30b051975b0d6d2fe2d73535926d6949f1e82f0`,
setting **only that non-secret public bridge** back to **0644**. Both application
hosts independently passed TLS and `/api/v1/instance` **200** with the new
canonical origin at **22:08:37 America/Toronto on 2026-10-30 / 02:08:37 UTC on
2026-10-31**. These are recovery checks, not candidate acceptance or a completed
multiplayer match.

Private environment/instance files and backup contents/permissions remained
unchanged. API, relay and database were not recreated during the activation
attempt or recovery. The independently verified website deployment, live
`220b965` identity and complete former-website redirects remain separate,
unchanged outcomes.

Before retrying, the operator corrected original-metadata restoration and bounded
readiness, added emergency-recovery and detached-job guards, and passed eight
operational guard tests. The actual production UID/GID **10001:10001** audit read
and hashed all 513 public files; static files and the Caddyfile were **0644**, nine
public directories were **0755**, and an isolated hardened start served both hosts
over local-CA TLS. That isolated audit did not reproduce or explain the first
production failure. The failed candidate container was removed before startup
diagnostics were retained, so the original startup cause remains inconclusive.
Preserve the failed activation and rollback/recovery evidence.

## Completed qualified frontend rollout

The separately approved detached one-shot
`frontend-domain-20261031T022941Z-49f8dd0c` completed with exit **0** at
**22:35:37.366 America/Toronto on 2026-10-30 / 02:35:37.366 UTC on 2026-10-31**.
The active-match gate was **zero**. The final live loaded OCI image is:

```text
sha256:c44335a7ef05555fc3f1c0990e6d7e339eda7dac971b6ca14f41014fd314bef6
```

Its configuration ID is
`sha256:0361b88e8110e892793c72affb93f228ead1acbc3f60024be84aa86e2e354d74`.
Provenance is frontend mirror source `86d13e76f71587f4ce8dedb9e0ff61b4a9a3fec3`,
reviewed public edge source `d01722f63167ebc1133de15360a4a9f46b292b62`, and design
`220b965b061e402df7531fa0f9ad5104bf29a638`. All 513 frontend file hashes and all
190 existing game-file hashes matched the reviewed manifests. API, relay and
Postgres retained the same container identities, images and mounts. No game build,
game release, API/relay recreation or database change occurred in this rollout.

The strict bounded readiness check passed on both application hosts at **22:35:30
Toronto / 02:35:30 UTC**. It waited through one observed SSL startup transient
without weakening TLS verification or triggering a premature rollback. That later
transient does not prove the cause of the earlier inconclusive startup failure.
The temporary Caddy bridge bind was removed because the reviewed configuration is
baked into the new image. The bridge file remains only as rollback material.

Public live checks at **22:37:43 Toronto / 02:37:43 UTC** passed all **nine checks
in each of Chromium and WebKit**: new About/download links, fallback-to-cookie
migration, actual website/application and API-sign-in theme sharing, exact
bootstrap GET/HEAD on both hosts, revalidation, case-sensitive routing, explicit
cookie priority and old/new cookie isolation. Eight public TLS/API/play/mobile
association routes returned **200**; all four former/new host and Origin
WebSocket combinations and a relay-upgrade probe returned **101**. All 64 old
hashed asset URLs retained their exact bytes. The full live monitor passed. Independent
readback verified both public design manifests identify `220b965` and the
exact API-page bootstrap/cache behavior.

Qualification also passed 294 web unit tests. The broader adjusted frontend suite
was **41 passed, five failed, four skipped**. Fresh equivalent baseline/candidate
comparisons reproduced the same four failures and passed the fifth flaky case on
both; no candidate-only failure appeared. Preserve these limits rather than
calling the entire suite green. No multiplayer match was completed, and no live
Firefox browser test body ran.

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

The deployed frontend now uses the new website/download destinations and design
`220b965`. Website/application/API-page theme sharing and fallback migration are
verified above. Former application API/recovery endpoints and old hashed asset
URLs intentionally remain for shipped-client and open-tab compatibility.

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

## Subsequent source integration

Website [PR #58](https://github.com/Globulation2/glob2-online-website/pull/58)
merged as `651401b4130e4ccdf83d0712e931681f777f305f` after final hosted verification
passed. It combines durable operations guidance, bounded Hosting convergence
checks and the `220b965` theme-preservation baseline. The [new main workflow](https://github.com/Globulation2/glob2-online-website/actions/runs/41153025573)
completed successfully for this source, with both verification and publication
jobs passing. Independent `https://glob2.online/design-system.json` readback
confirms `220b965b061e402df7531fa0f9ad5104bf29a638`. The run’s downloaded Hosting artifact records candidate and promoted version
`2c873c3132936a9a`, production release `1793408963340000` and previous version
`c1941eff894c0639`, with `unchanged=false`. The earlier `e826954` release remains
historical evidence and a rollback reference, not the current theme.

Public game [PR #1286](https://github.com/Globulation2/glob2/pull/1286) merged as
`9c49bfb1c52a5f6a8f06a78950838a76980e0de2`. The release mirror normally merged
its existing baseline and that reviewed upstream history as
`fc90352cfcfa622e450121e094d4c6c43572b472` (parents `86d13e76` and `9c49bfb1`).
The exact final tree matches the reviewed upstream; there was no force push,
history rewrite or automatic deployment. The subsequent routing-source merge is
`68f7fc038c3d758daf67a69ed9bf65f11e2e08a2` (parents `fc90352` and `3ca77178`),
with exact tree matching reviewed upstream `3ca77178`; existing tags and history
were preserved.

The API-page bootstrap and asset-namespace CSP preservation follow-up is published
in [PR #1287](https://github.com/Globulation2/glob2/pull/1287), source `d01722f631`,
merged as `3ca77178`. Focused real-Caddy cases passed. Candidate qualification is
complete with explicit baseline-known failures retained by the implementation
work unit. The first narrow Caddy activation was rolled back, with the incident preserved
above. Following reviewed readiness, metadata restoration and non-root permission
checks, the qualified frontend is now live as separately verified in the completed
rollout record. All related source PRs #58, #1286 and #1287 are merged and mirrored;
no further source changes are required for the remaining browser-only handoff.

## Google branding and ownership follow-up — 2026-10-31

The OAuth branding home, privacy and terms fields were saved as
`https://glob2.online/`, `https://glob2.online/privacy/` and
`https://glob2.online/terms/`. A fresh reload verified persistence, and all three
URLs independently returned HTTPS **200**.

The initial branding verification attempt required Search Console domain
ownership. A domain property for `glob2.online` was added, and one public Google
verification TXT record was appended to the personal Cloud DNS zone with TTL
**300**. The original Firebase hosting TXT value was preserved. All four
`ns-cloud-a1` through `ns-cloud-a4` authoritative nameservers returned both values,
with no regression to the existing RRset. Search Console confirmed ownership via
**Domain name provider** at **07:34 America/Toronto / 11:34 UTC on 2026-10-31**.
No verification token value is reproduced in this public record.

**Google branding verification is not yet confirmed.** The branding check
explicitly instructed waiting at least **24 hours** after ownership verification
before retrying. That minimum elapses at **2026-11-01 11:34 UTC / 06:34 Toronto**
after the overnight clock change. Saved branding fields and verified Search
Console ownership are separate from branding approval/status; no successful
branding recheck is claimed.

Screenshots remain outside Git in the game worktree's ignored
`artifacts/domain-migration/branding/`: `saved-branding-links.png`,
`ownership-verified.png` and `verification-issue.png`. Chrome control was released
back to the separate publishing chat. No account permission changes were made.

## Apple service field and retained legacy homepage — 2026-10-31

The separately coordinated publishing work saved the optional Apple **User Privacy
Choices URL** as `https://app.glob2.online/account` and verified the persisted
value by fresh reload. This is the optional account/service endpoint, **not the
Privacy Policy URL**. The actual Privacy Policy URL remains the existing GitHub
`docs/mobile/privacy-policy.md` destination; privacy-data answers were preserved.
The earlier session-expiry/reauthentication gap is no longer outstanding. Follow
the [storefront ledger](approved-storefront-rollout.md#destination-status) for its
separate release/submission states.

The user clarified that the migration changes `glob2online.com` references and
leaves the game repository's `globulation2.org` About homepage alone. That legacy
homepage is deliberately unchanged. GitHub sign-in or About-editor capability is
therefore no longer a migration prerequisite. The website repository About field
was already changed from the former modern domain to `https://glob2.online/`.

## Verification evidence and remaining operations

Sanitized operational outcomes are recorded above. Detailed local evidence is in
the website checkout's ignored `artifacts/domain-migration/`: `promotion.json`,
`candidate-smoke.log`, `live-smoke.log`, `live-site-checks.json`,
`domain-redirect-updates.json`, `domain-redirect-state.json`,
`domain-redirect-checks.json` and `live-monitor.log`. The subsequent automatic
website release artifacts are in `website-651401b-release/` (`release.json` and
`promotion.json`), downloaded from the successful main run. These local artifacts are
operator evidence, not public repository files; preserve private configuration
and credential material outside Git. The sanitized final application rollout
summary is `frontend-candidate/live-rollout/final-rollout-evidence.json` in the
game worktree's ignored domain-migration artifacts, alongside `REVIEW.md`,
`candidate-image-manifest.json` and `permission-start-audit.json`. Its supporting
`approved-job-result.json`, `live-browser-results.json` and `live-http-checks.json`
record the activation and public checks. Website evidence also includes
`post-frontend-live-monitor.log`.

The website deployment, full website redirect matrix, qualified application
frontend rollout and Apple service-field replacement are complete. The only
remaining migration gate is **Google branding verification** after the instructed
24-hour ownership-propagation interval. The new branding URLs are persisted and
reachable, and Search Console ownership is verified; do not mark branding
verification complete before a successful recheck. Retry no earlier than
**2026-11-01 11:34 UTC / 06:34 Toronto** after the clock change.

The hourly `finish-glob2-domain-migration` automation was **deleted** under its
stop-on-user-action instruction when the earlier Mac-lock gate required user
input. That gate has cleared, and no schedule has been recreated. Chrome remains
released to the publishing chat; no GitHub login or About edit is required for the
user-defined migration scope. Keep former-domain registrations, DNS and
certificates maintained for inbound links and old application-client recovery.
