# Repository and web-property ledger

[Fact index](README.md) · [Assets](assets.md) · [Product](product.md) · [Channels](channels.md) · [Distribution](distribution.md)

Observed **26 October 2026**. This is a bounded source inventory, not a claim that every repository or account has been discovered. Local checkouts were read only. No production credentials or private account data were inspected or copied. GitHub visibility and additional public repositories are separately checked by the public-estate researcher.

## Repository records

| ID | Repository | Observed revision / role | Marketing-relevant contents and boundary |
| --- | --- | --- | --- |
| R01 | [Globulation2/glob2](https://github.com/Globulation2/glob2) | Local HEAD `c9198b854a2ea6fc16cd5524913cf96c5a80c499`; main game and online platform | C++ engine; native/browser/mobile clients; TypeScript accounts, multiplayer, content libraries, optional paid services; artwork/music originals, release workflows and store metadata. Source support is not deployed availability. |
| R02 | [Globulation2/glob2-online-website](https://github.com/Globulation2/glob2-online-website) | Local HEAD `6e391ebe93b725747827a3ed7cea78f0d0d8f7e1`; static Astro public website | Editorial copy, gameplay guides, history/archive references, download metadata, community links and gameplay screenshots. Independently deployed from game/app. |
| R03 | [Globulation2/glob2-design-system](https://github.com/Globulation2/glob2-design-system) | Worktree HEAD `acd277710acfebf528e1fc6f653d55fdf75de4b2` | Shared tokens, Meadow/Night themes, typography, controls, wordmark, icons, fonts and colony footage with provenance. Consumers own editorial content and page layouts. |
| R04 | [Globulation2/glob2-marketing](https://github.com/Globulation2/glob2-marketing) | New project; foundation commit `3eedc602d8193f1aee364f9a7d588249b2ae05de` | Marketing evidence, hypotheses, task ledger and working rules. No release/deployment authority inferred. |
| R05 | [Globulation2/glob2-javascript-ai-starter-exampler](https://github.com/Globulation2/glob2-javascript-ai-starter-exampler) | Public organization metadata discovered by foundation researcher; contents not locally audited | Description identifies a documented JavaScript AI template with modular source and a single-file bundle; potential contributor-learning asset. Do not infer quality, current API compatibility or adoption. |
| R06 | Release mirror (access-restricted lead) | Main game's local `release` remote and [release procedure](https://github.com/Globulation2/glob2/blob/c9198b854a2ea6fc16cd5524913cf96c5a80c499/docs/releases/releasing.md) establish a separate packaging mirror | Private repository identifier and contents omitted. This is a release dependency lead, not a public marketing destination or verified public installer source. |

Other access-restricted asset leads were excluded from the public inventory. The above list does not establish organization completeness or account control. R05's metadata was supplied by the foundation agent; its content still needs direct review.

## Web and infrastructure records

| ID | Property or source-defined surface | Evidence | What is established / remains open |
| --- | --- | --- | --- |
| W01 | [glob2online.com](https://glob2online.com/) | R02 [README](https://github.com/Globulation2/glob2-online-website/blob/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1/README.md) and `src/data/site.ts` | Public static marketing/learning site, Firebase Hosting publishing described in `docs/hosting.md`; public journey is covered in [channels](channels.md). Domain/DNS ownership was not audited. |
| W02 | [app.glob2online.com](https://app.glob2online.com/) | R01 [README](https://github.com/Globulation2/glob2/blob/c9198b854a2ea6fc16cd5524913cf96c5a80c499/README.md); R02 `src/data/site.ts` | Browser game at `/play/`, sign-in `/signin`, leaderboard `/leaderboard`, matches `/matches`, maps `/maps`; app/game has independent deployment and account system. Other implemented routes may be optional or disabled. |
| W03 | [globulation2.org](https://globulation2.org/wiki/Main_Page) | R01 README, R02 migration manifest and community links | Original wiki, manuals, news and translations; historical/current distinctions and ownership remain important. See [history](history.md). |
| W04 | Website public guide-media storage | R02 `src/data/guide-media.json` | Versioned public cloud-storage URLs, dimensions, hashes and captions for handbook media; source manifest does not prove every URL currently resolves. |
| W05 | Website public feed/rankings pipeline | R02 `scripts/RANKINGS.md`, `.github/workflows/rankings.yml`, `docs/hosting.md` | Sanitized public rankings snapshot; website docs explicitly separate public feed from account persistence. No engagement figures collected here. |
| W06 | Self-hostable online instance and services | R01 [hosting index](https://github.com/Globulation2/glob2/blob/c9198b854a2ea6fc16cd5524913cf96c5a80c499/docs/hosting/README.md), `deploy/README.md` | API, relay, workers, validation and optional studios documented. Deployment examples do not prove production topology, operating cost, capacity or active players. |

## Existing content and publication machinery

- R02 `src/data/marketing.ts` centralizes homepage/game/download/community editorial copy; `src/content/guides/` has gameplay/AI handbook chapters; `src/content/news/`, `src/content/history/`, `src/content/archive/` hold other editorial collections. `content/migration-manifest.json` records original wiki revisions, authorship links, language and unresolved reuse rights.
- R02 `README.md` says `src/data/events.json` deliberately stays empty until reviewed human-organized events exist. An events page is not proof of a current event program.
- R01 `.github/workflows/` includes release/package paths for browser, Steam, Epic, Microsoft Store, GOG staging, Snap, Flathub updates, Android Play, F-Droid, Amazon, Mac App Store, iOS/TestFlight and direct downloads. Existence of automation is not listing acceptance; see [distribution](distribution.md).
- R01 retains application/store identities and metadata under `data/`, `fastlane/metadata/`, `mobile/`, `darwin/`, `snap/`, `flatpak/`; [assets](assets.md) records the screenshot families and copy variations.
- Website documentation says public pages use no analytics/account cookies; app source separately implements operational/account activity reporting. See [product measurement inventory](product.md#measurement-and-account-infrastructure).

## Scope gaps

Public organization metadata checked by the foundation researcher reports five public repositories at [the organization API](https://api.github.com/orgs/Globulation2). Its creation timestamp is 26 December 2019, which is an organization-account date, not the game's founding date. Public repository enumeration is bounded to that organization and does not enumerate forks or other owners.

No exhaustive owner/account-access ledger, DNS registrar audit, private store-dashboard audit, ad-account audit, mailing-list audit, revenue audit, or historical repository archive was completed. Public source paths and discovered links are leads, not proof of account control. Further public evidence and unverified estate records are maintained in [channels](channels.md), [distribution](distribution.md) and [history](history.md).
