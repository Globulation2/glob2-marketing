# Communication channels and public web estate

[Fact index](README.md) · [Distribution](distribution.md) · [Assets](assets.md) · [History](history.md)

Observed **2026-10-26**. “Observed” means public HTML or source was inspected, not that an account is controlled by the present team. No messages, registrations, edits, or invitations were sent. Traffic, conversion, membership quality and account access are unmeasured.

## Project-associated surfaces

| ID | Surface | Evidence and observed state | Control / remaining uncertainty |
| --- | --- | --- | --- |
| CH-01 | [glob2online.com](https://glob2online.com/) | Direct HTTP fetch returned 200. Current homepage presents colony construction, food and competing colonies; browser early access; tutorial, download and Discord calls to action. Three replay screenshots and colony animation. Links to learn, game, community, search, news, competition, history and legacy archive sections. | Public availability established; domain, hosting and editorial administrators not audited. |
| CH-02 | [Online application](https://app.glob2online.com/) | HTTP 200 returned an application shell titled Globulation 2. Homepage links to play, sign-in, leaderboards, matches and maps. | JavaScript workflows, player activity and service health not tested. See [product](product.md). |
| CH-03 | [Discord invitation](https://discord.gg/xnVrafzMD) | Linked by current public website and website source `src/data/site.ts`. Public invite API returned 403 in this environment. | Server existence behind invite, invitation validity, moderators and member totals not verified. |
| CH-04 | [Legacy wiki](https://globulation2.org/wiki/Main_Page) | Readable. Main-page revision dated 2019-09-12; displayed news ends with 2017 server moves. Describes reduced micromanagement, GPLv3, YOG, AI, editor and scripting. Links multilingual manuals and contributor material. | Historical content still publicly served; current maintainers/control unknown. |
| CH-05 | [Legacy forum](https://forums.globulation2.org/) | HTTP 200. General, help, strategies, maps/campaigns, tournaments, Spanish, German, French and archive sections. Last-post dates shown on index largely 2009–2015. Archives link UserVoice and Savannah bugs. | A readable forum is not proof of active community or reachable administrators. Guest/session counts excluded as audience evidence. |
| CH-06 | [IRC documentation](https://globulation2.org/wiki/IRC) | Page last edited 2017-08-15 describes OFTC via `irc.globulation2.org` / `irc.oftc.net`, channels `#glob2` and `#glob2-dev`. | Historical documented endpoints only; no IRC connection or population check. Older FAQ references to Freenode differ from this later page. |
| CH-07 | [Savannah mailing lists](https://savannah.nongnu.org/mail/?group=glob2), [project](https://savannah.nongnu.org/projects/glob2/), [news](https://savannah.nongnu.org/news/?group=glob2), [bugs](https://savannah.nongnu.org/bugs/?group=glob2) | Linked from wiki/forum; direct mailing/project fetches timed out. | Established historical project links; present access, subscriber activity and authority unknown. |
| CH-08 | [GitHub game/issues](https://github.com/Globulation2/glob2), [organization](https://github.com/Globulation2) | Current website sends contributors and bug reporters here. Public release API inspected. Five public org repositories reported; see [repository ledger](repositories.md). | Stars/forks are not player or buyer counts. Account permissions not audited. |
| CH-09 | [SourceForge project/news](https://sourceforge.net/projects/globulation2/) | Public project profile and archived announcements remain discoverable. Listed maintainers genixpro/k776; update field 2013-04-03. | Platform record does not prove present publishing access. Details in [distribution](distribution.md). |
| CH-10 | [Legacy videos](https://globulation2.org/wiki/Videos) | Readable index, revision 2017-08-15, links FOSDEM 2008, three historical match/tutorial examples, YouTube, Internet Archive and older Google Video/Box endpoints. | Index inspected, individual videos and rights/continued playback not verified. No official contemporary video channel established. |

## Independent visibility, not owned channels

| Surface | Observed record | Limit |
| --- | --- | --- |
| [Libregamewiki](https://libregamewiki.org/Globulation_2) | Search-readable profile calls 0.9.4.1 (2009) latest and links original site and distro packages. | Community catalog, older product snapshot. |
| [Wikipedia](https://en.wikipedia.org/wiki/Globulation_2) | Search-readable article describes legacy RTS/YOG and cites historical coverage. | Secondary reference, no project editorial control assumed. |
| [AlternativeTo](https://alternativeto.net/software/globulation-2/) | Search results expose a Globulation 2 entry, Mac/Windows/Linux tags and image captions “Battle” / “Building camp.” | Discovery evidence; direct entry/media not fully inspected. |
| [NeonRoof](https://neonroof.com/platform/store/globulation-2) | Search-readable catalog expressly disclaims developer affiliation; version 0.9.4.4 and three screenshot captions. | Independent referral catalog; no submission/account control inferred. |
| [OnWorks](https://www.onworks.net/software/linux/app-globulation-2-to-run-in-linux-online) | Search-readable page says it obtains software from SourceForge; multiple screenshot slots. | Independent wrapper/aggregator, not the current browser application. |
| [Reddit historical recollection](https://www.reddit.com/r/Ubuntu/comments/frz14r/) and [separate Globulation 3 proposal](https://www.reddit.com/r/linux_gaming/comments/1reukzo/project_globulation_3/) | Search found recollection and another revival proposal. | Third-party conversations; identity, affiliation and audience size not established. Globulation 3 is not treated as this revamp. |

## Discovery boundaries and open records

No official newsletter, contemporary YouTube/Twitch channel, dedicated subreddit, X/Twitter, Mastodon, Bluesky, Facebook, Instagram, TikTok or crowdfunding profile was verified in this pass. This is a discovery gap, not proof none exist. Platform dashboards, submitted-but-unpublished listings, analytics, mailing contacts and private Discord content were outside the public inventory.

Sources were direct page fetches above plus website `src/data/site.ts`; the web search tool could not open the new website, so direct HTTP retrieval was used. The three live homepage images are `/images/home-thriving-colony.webp`, `/images/home-colony-defence.webp`, `/images/home-rival-expansion.webp`; the site labels them replay views with fog of war off. Their presence is established from HTML; image-by-image visual equivalence across storefronts remains untested. See [asset ledger](assets.md).
