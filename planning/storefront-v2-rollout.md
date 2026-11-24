# Storefront v2 revamp: execution ledger

[Planning index](README.md) · [Task ledger](tasks.md) · [Working rules](../AGENTS.md#storefront-v2-revamp--2026-11-24) · [Positioning v2](../analysis/positioning-v2.md) · [Storefront v1 rollout](approved-storefront-rollout.md) · [Canonical translations](../translations/README.md)

## Authorization and scope

On **2026-11-24** the user asked for the store listings to be revamped:

> I want to refresh the visual appearance as best we can, especially the main store image and the game screenshots. We kind of look amateurish right now.

Storefront-v2 replaces the storefront-v1 listing approved on 2026-10-30: new copy, key art, screenshots, icon and trailer, translated into all supported languages with independent review, and applied to every project-controlled store without interrupting in-flight reviews. The team runs end to end with no sign-off stops. The binding rules are in [AGENTS.md](../AGENTS.md#storefront-v2-revamp--2026-11-24).

This ledger records what was decided, who owns each work unit, and what has actually happened at each store. Authorization is not evidence of a change. The [v1 ledger](approved-storefront-rollout.md) stays the record of the v1 rollout and of each store's review history up to 2026-11-22.

## Decisions

| # | Topic | Decision | Source |
| --- | --- | --- | --- |
| 1 | Art sources | Real game art only: fresh in-engine captures, compositions of real game sprites and scenes, and design treatment (captions, framing, crops). No AI-generated imagery, no stock imagery. Replaces "Approved imagery only". | User selection |
| 2 | Monetisation | Nothing is sold. The listing says flatly: free, no ads, no in-app purchases, no lootboxes, no in-game currency. | User's words: "100% ad-free while also free to play and also no annoying lootboxes or in-game currencies"; and, asked what is sold to players, "Nothing is sold" |
| 3 | MCP | Never claim "first". Desktop pitch: play the same colony alongside your own AI agent through the game's built-in MCP server. Desktop-only (native Windows, macOS, Linux). | The user first wrote "the first game you can play in tandem with AI through MCP", then chose to drop "first" after seeing the [prior-art research](mcp-outreach/product-and-prior-art.md) |
| 4 | Platform split | Mobile listings lead with great real-time-strategy gameplay plus the fair deal. Desktop listings add AI co-play through MCP. Supersedes [positioning v1](../analysis/positioning-v1.md). | User's words: "For mobile users, its just great RTS gameplay"; split confirmed as a user selection |
| 5 | Rollout timing | Do not interrupt in-flight store reviews. Snap, itch.io, Microsoft Store, Google Play and the F-Droid/AppStream sources now; Apple (iOS, Mac), Epic and Amazon when each review clears or with the next version; Steam and GOG assets prepared only. | User selection |
| 6 | Icon | Faithful, sharp high-resolution redraw of the existing blue glob icon. Same shape, not a redesign. | User selection |
| 7 | Trailer | Yes, 30–45 seconds, from real in-engine recordings. | User selection |
| 8 | Localized screenshot captions | Captioned sets rendered by script for every language; uploads tiered, top languages first. | User selection |
| 9 | Sign-off | No stops. Do not wait for user approval; report results to the coordinating agent. | User selection |
| 10 | Footage | [Gameplay video for marketing](gameplay-video.md) is binding for every store screenshot and all trailer footage. | User's words: "for in-game footage, make sure it follows our marketing rules too about capturing exciting action scenes and not boring mostly empty scenes" |

## Work units

Statuses: not started, in progress, complete, blocked. Update the row and add a [log](#log) entry when a status changes.

| ID | Work unit | Owner role | Output | Status |
| --- | --- | --- | --- | --- |
| V2-00 | Record the decisions | Decision recorder | [AGENTS.md section](../AGENTS.md#storefront-v2-revamp--2026-11-24), [positioning v2](../analysis/positioning-v2.md), this ledger, index entries | Complete with the commit that adds this ledger |
| V2-01 | Research mobile store comparables and player priorities | Research analyst | [Mobile store comparables](../analysis/mobile-store-comparables.md), [player priorities](../analysis/player-priorities.md) | In progress |
| V2-02 | Verify every claim against the game source, production and store declarations; write the per-store allowed and banned wording table | Claims verifier | [Storefront v2 claims](../facts/storefront-v2-claims.md) | In progress |
| V2-03 | Write English copy v2: short fields, long description, fair-deal and desktop AI fields, overlay captions; update platform composition, glossary, tooling and tests | Copy lead | `translations/en.md` at `storefront-v2`, `translations/platforms.json`, `translations/tools/` | Not started |
| V2-04 | Edit the English and review it against each store's metadata policy | Copy editor and store-policy reviewer (independent) | Per-store policy checklist | Not started |
| V2-05 | Capture in-engine screenshots for each device class under the footage rule | Capture engineer | Captures and capture manifest in `assets/storefront-v2/` | Not started |
| V2-06 | Build key art, per-store derivatives, the caption renderer, build scripts and manifests | Compositor | `assets/storefront-v2/` | Not started |
| V2-07 | Redraw the icon as a high-resolution master and regenerate platform icons | Icon artist | Icon master; game-repository pull request | Not started |
| V2-08 | Record, cut and encode the 30–45 second trailer | Trailer editor | Trailer master and per-store encodes | Not started |
| V2-09 | Review rendered visuals in two rounds against comparables, store rules and the footage rule | Visual reviewer (independent) | Review notes and contact sheets | Not started |
| V2-10 | Translate v2 into the 44 non-English languages, each with an independent review | Translators and independent reviewers | Locale catalogs, review records, exports | Not started |
| V2-11 | Render localized captioned screenshot sets from the reviewed catalogs | Compositor | Per-locale captioned sets and manifests | Not started |
| V2-12 | Update maintained source metadata in the game repository | Store steward | Pull request for F-Droid metadata, AppStream metainfo, Snap source and release documents | Not started |
| V2-13 | Apply v2 to each store and verify by readback | Store stewards | The [per-store table](#per-store-rollout) and [log](#log) | Not started |
| V2-14 | Commit and push each completed marketing work unit to `main` | Git steward | Commits on `main` | In progress |

File ownership is disjoint. A worker hands off finished files and a summary; the Git steward stages those explicit paths only.

## Per-store rollout

Evidence levels, in order. Record each separately; a later level does not follow from an earlier one.

- **Prepared:** the text export and the image and video files for this store exist in the repository with a manifest.
- **Reviewed:** the independent reviews have passed: copy and store policy for text, visual review for media, translation review for each locale used.
- **Saved:** written to the store console, or merged to the source repository, and confirmed by a fresh reload: text compared with the payload, images compared visually with their sources. An initiated upload or a generic save message does not count.
- **Submitted:** sent into the store's review or publication pipeline. "n/a" where the store has none.
- **Publicly verified:** the public page was fetched fresh and matches the payload and uploaded images.

"When" follows decision 5. "Last recorded state" comes from the [v1 ledger](approved-storefront-rollout.md#current-publication-and-review-dependencies) and the [localization rollout](storefront-localization-rollout.md) and has not been rechecked for v2; the store steward checks the live state before any write and does not disturb a review that is in flight.

| Store | Class | When | How | Last recorded state | Prepared | Reviewed | Saved | Submitted | Publicly verified |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Snap | Desktop | Now | Dashboard: text, screenshots, banner | v1 presentation live (2026-10-30) | No | No | No | n/a | No |
| itch.io | Desktop, browser | Now | Page editor | Public listing launched 2026-11-23 with v1 cover and screenshots | No | No | No | n/a | No |
| Microsoft Store | Desktop | Now | Partner Center workbook through `microsoft_import.py`; images, trailer; publish | Package update submitted 2026-11-22 and the 44-locale update both last recorded as Publishing; outcome not recorded | No | No | No | No | No |
| Google Play | Mobile | Now | Console: text for all locales, graphics, 512 px icon, video; send for review | Closed testing only; v1 copy and feature graphic Published in console; sixteen locale changes last recorded In review ([localization rollout](storefront-localization-rollout.md)) | No | No | No | No | No |
| F-Droid metadata, AppStream metainfo, Snap source, release documents | Mobile and desktop sources | Now | Game-repository pull request | v1 text merged; no F-Droid or Flathub listing verified | No | No | No | n/a | No |
| iOS App Store | Mobile | When review clears, or with the next version | `apple-store-localize.yml` on an editable draft; screenshots and previews in App Store Connect | 0.11.700 Waiting for Review (2026-11-21) | No | No | No | No | No |
| Mac App Store | Desktop | When review clears, or with the next version | Same workflow; screenshots in App Store Connect | 0.11.700 Waiting for Review (2026-11-21) | No | No | No | No | No |
| Epic Games Store | Desktop | When review clears | `epic_template.py` CSV; images and trailer in the portal | Five Stage entities In review (2026-11-18); nothing Live | No | No | No | No | No |
| Amazon Appstore | Mobile | When review clears | Console: English plus its ten other languages, images | Submitted 2026-10-31; outcome not recorded | No | No | No | No | No |
| Steam | Desktop | Prepared only | Asset pack and copy | Account onboarding incomplete; no app or depot IDs | No | No | n/a | n/a | n/a |
| GOG | Desktop | Prepared only | Asset pack and copy | Application pending; no portal access | No | No | n/a | n/a | n/a |

Notes for stewards:

- The MCP section goes into a desktop listing only where the [claims record](../facts/storefront-v2-claims.md) confirms it for that store's build. The Mac App Store build is the open case.
- Screenshot upload tiers: tier 1 is English plus roughly ten top languages chosen from distribution-dashboard market data; the remaining locales follow. Record which locales have images uploaded, per store, in the log.
- Sign-in and multi-factor prompts stay with the user. Any new agreement, fee or declaration is put to the user.
- Binary icons ship with the next builds; Google Play's separate 512 px store icon goes up with the listing.

## Verification

From the approved plan. Record results in the log.

- `python3 translations/tools/storefront.py check --require-review` passes for all 45 locales; `python3 -m unittest discover translations/tests` passes; `export` produces payloads with no limit violations.
- Asset manifests: every image at native resolution and matching its store's size and format rules; captioned images pass the text-area check (at most 20% of the image); no banned words in images.
- Every screenshot and the trailer pass the [gameplay video](gameplay-video.md) checklist: busy developed colonies, visible action, legible at feed size, capture conditions recorded. The trailer is watched at normal speed at its opening, middle and end.
- The policy reviewer's checklist is completed per store.
- Per store: the public page, or the console readback where the listing is not yet public, is fetched fresh and compared with the exported payload and uploaded images.
- Game-repository pull request: required checks pass; the icon is checked visually at 1024 px and at 48 px.

## Flagged outside this plan

These were noticed while planning. They are not work units here and are not resolved by this revamp.

- **App Store privacy label.** The public iOS listing was observed on 2026-11-24 showing "Data Linked to You" (contact info, photos, identifiers among the categories). That undercuts a no-account pitch. It needs a product and legal review, not a copy edit.
- **Google Play production gate.** Production access still requires 12 opted-in testers for 14 days; the last recorded count is 0 ([recruitment record](android-closed-test-recruitment.md)). The new listing will not be publicly visible on Google Play until that clears.
- **Website.** `glob2-online-website` could adopt the new key art and trailer afterwards. Not in scope.

## Log

Append dated entries below, oldest first. One entry per event: date, store or work unit, what was done, the evidence level reached, and how it was checked. Keep private account details and credentials out.

No entries yet.
