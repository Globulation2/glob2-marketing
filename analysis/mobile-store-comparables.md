# Mobile and desktop store comparables

[Analysis index](README.md) · [Player priorities](player-priorities.md) · [Comparable games (mechanics)](comparables.md) · [Positioning v2](positioning-v2.md) · [Storefront v2 rollout](../planning/storefront-v2-rollout.md) · [English listing source](../translations/en.md)

Observed **2026-11-24** (US storefronts, English). This record covers how comparable strategy games present their store listings, what each store's rules allow, and where the current Globulation 2 listing falls short. It complements [comparables.md](comparables.md), which compares mechanics and motivations and did not examine any mobile store page.

## Evidence labels and limits

- **[V]** — read by the analyst on 2026-11-24 from the linked page, its raw HTML/JSON-LD, the iTunes lookup API (`https://itunes.apple.com/lookup?id=<id>&country=us`), the Flathub API (`https://flathub.org/api/v2/appstream/<app-id>`) or the Steam `appdetails` API. First screenshots and icons marked [V] were also viewed.
- **[S]** — gathered earlier in the same session (also 2026-11-24) by a different research pass and **not re-checked** here. Treat as probably right, not as verified.
- **[I]** — analyst inference or recommendation. Not an observation.

Limits: one day, one country, one language. Store pages are personalised and change; ratings and install bands are snapshots. No conversion data for any listing was available, so nothing here shows that a given treatment *causes* installs. A listing's success may come from the game, its age, press or price rather than its page. Quotations are kept to short fragments; follow the links for full text.

## 1. Comparison table

### Mobile strategy listings re-verified on 2026-11-24

| Game / sources | Title and short text (exact) | Screenshots: count and treatment | Trailer | Monetisation wording | Icon |
| --- | --- | --- | --- | --- | --- |
| **Rusted Warfare** — [Play](https://play.google.com/store/apps/details?id=com.corrodinggames.rts), [App Store](https://apps.apple.com/us/app/id1514329124). Play: $1.99, 4.6 (16,139 ratings), 100K+, no IAP, no ads label, last updated Sep 25, 2024. iOS: $2.99, 4.69 (626), last version 2022-11-12. [V] | Play title "Rusted Warfare - RTS Strategy"; short description "Build bases, extract resources and create your army in this real RTS." iOS name "Rusted Warfare - RTS"; subtitle "A real-time base building RTS". [V] | Play: 9 landscape. Shot 1 is real gameplay with a text block top-left: headline "A True PC-Style RTS!" then four lines, "NO artificial wait timers", "NO microtransactions", "NO pay-to-win", "NO ads". iOS: 5 iPhone + 5 iPad, landscape; shot 1 is the same idea reworded ("True PC-like RTS!", "NO wait timers"). [V] | Play: yes. iOS: no app-preview video found in the page. [V] | First feature bullet on both stores: "A pure RTS with no microtransactions". [V] | Gameplay crop with the letters "RTS" overlaid, green border. The only comparable with text in the icon. [V] |
| **Bad North: Jotunn Edition** — [Play](https://play.google.com/store/apps/details?id=com.PlausibleConcept.BadNorthFull), [App Store](https://apps.apple.com/us/app/id1367121168). Play: $3.99, 4.4 (10,134), 500K+, no IAP; Data safety "No data collected". iOS: $3.99, 3.76 (1,745), Editors' Choice. [V] | Play short description "A beautifully hand-crafted real-time micro strategy with Vikings." iOS subtitle "Vikings are coming". [V] | Play: 8 landscape, raw gameplay, no captions (shot 1 is a whole island under attack, centred, lots of empty margin). iOS: 5 + 5 **portrait** composites: two landscape gameplay frames stacked on a dark blurred background with the logo underneath. [V] | Play: yes. iOS: none found. [V] | None. The paid price and absent IAP label carry it. [V] | One object: a white helmet with an arrow through it, on a dark blurred scene. No text. [V] |
| **Northgard** — [Play](https://play.google.com/store/apps/details?id=com.playdigious.northgard), [App Store](https://apps.apple.com/us/app/id1533979882). Play: $8.99, 4.3 (14,038), 500K+, IAP, Editors' Choice. iOS: $8.99, 4.61 (3,675). [V] | Short description and iOS subtitle are identical: "Settle. Survive. Conquer." [V] | Play: 16 unique landscape images (two sets of 8). Shot 1 is not gameplay: DLC promo art with the logo and the caption "9 ADDITIONAL CLANS". iOS: 9 iPhone + 10 iPad, landscape, same DLC image first. [V] | Play: yes. iOS: yes. [V] | Says DLC clans are unlocked "by buying the DLCs". No fairness line. [V] | One object: a round wooden shield, on a landscape. No text. [V] |
| **The Battle of Polytopia** — [Play](https://play.google.com/store/apps/details?id=air.com.midjiwan.polytopia), [App Store](https://apps.apple.com/us/app/id1006393168). Play: free, 4.4 (236,741), 10M+, IAP, no ads label, updated Nov 12, 2026. iOS: free, 4.59 (15,565), IAP. [V] | Play short description "Turn based strategy game. Build a civilization and take it into battle!" iOS subtitle "A Civilization Strategy Game". [V] | Play: 10 landscape. Shot 1 is close-up gameplay with a black band across the bottom fifth reading "TURN BASED STRATEGY". iOS: 7 iPhone + 6 iPad, landscape; file names show one theme per slide ("strategy", "pickTribe", "conquer"). [V] | Play: yes. iOS: yes. [V] | Feature bullets: "Free turn based civilization strategy game." and "Allow offline game play." [V] | Two characters facing each other on a bright gradient. No text. [V] |

Checks made for these four: Play JSON-LD (name, short description, price, rating), the "Play trailer" button and its own video id, screenshot image count, badges, the iTunes lookup record, and the App Store HTML (subtitle, privacy label, IAP list, video stream URL). All four App Store pages show the privacy label "Data Not Linked to You"; Rusted Warfare's lists only diagnostics. [V]

### Mobile listings carried from the earlier pass (not re-checked)

| Game | Short text / subtitle (exact, [S]) | Screenshots and trailer [S] | Monetisation wording [S] |
| --- | --- | --- | --- |
| **Kingdom Two Crowns** ([Play](https://play.google.com/store/apps/details?id=com.rawfury.kingdom2crowns)) $6.99 | "Build your kingdom in this atmospheric micro strategy game." / "BUILD, EXPLORE, DEFEND" | 10 raw pixel-art shots, no captions; trailer | DLC "available via in-app purchase" |
| **Iron Marines** ([Play](https://play.google.com/store/apps/details?id=com.ironhidegames.android.ironmarines)) free + IAP | Play title "Iron Marines Offline Strategy"; iOS subtitle "Sci-Fi Space Battle Games" | 6 + 6; shot 1 is captioned key art; trailer | "offline" repeated about ten times in the description |
| **Company of Heroes** ([Play](https://play.google.com/store/apps/details?id=com.feralinteractive.companyofheroes_android)) $14.99 | "Take command in World War II, now with online multiplayer." | 8 ultrawide; shot 1 is captioned gameplay; trailer | States expansions are sold as in-app purchases |
| **Mindustry** ([Play](https://play.google.com/store/apps/details?id=io.anuke.mindustry)) free, open source | "An open-ended factory management game with RTS and tower defense elements" | 7 raw shots at mixed resolutions; no trailer detected | None, despite no ads and no IAP |
| **Unciv** ([Play](https://play.google.com/store/apps/details?id=com.unciv.app)) free, open source | "Open source 4X civilization-building game" | 8 raw UI shots; no trailer detected | Opening line includes "no ads, free forever!" |
| **Shattered Pixel Dungeon** ([Play](https://play.google.com/store/apps/details?id=com.shatteredpixel.shatteredpixeldungeon)) free, open source | "A roguelike dungeon crawler RPG that's simple to get into but hard to master!" | 4 landscape + 4 portrait, raw; trailer | No monetisation line; says it is open source |

### Open-source strategy peers on desktop channels (new, [V])

None of these four has an official phone listing that was found; they show how free, open-source strategy games present themselves where Globulation 2's desktop builds also appear.

| Game / sources | Headline and summary wording (exact) | Screenshots | Trailer | "Free" / open-source wording | Notes |
| --- | --- | --- | --- | --- | --- |
| **0 A.D.** — [site](https://play0ad.com/), [itch.io](https://play0ad.itch.io/0ad), [Flathub](https://flathub.org/apps/com.play0ad.zeroad) | Site headline "History is yours for the taking"; page title "A free, open-source game of ancient warfare". Flathub summary "Real-time strategy game". | Site: 4 in a carousel. Flathub: 4 at 1600×900, each with a descriptive caption (e.g. "Maurya village with buildings and farms"). | Site links a release trailer loaded on click; itch page embeds two YouTube videos. | itch section "0 A.D. is Free of Charge" promises: "No “freemium” model, no in-game advertising, no catch." A second section explains free "as in “Freedom”". | itch: 4.8 from 64 ratings; "Average session: About an hour". Flathub: 356,588 installs, 4,662 last month. Not found in Steam search. |
| **Widelands** — [itch.io](https://widelands.itch.io/widelands), [Flathub](https://flathub.org/apps/org.widelands.Widelands) (the project site refused automated fetches) | Flathub summary "A real-time build-up strategy game". itch search tagline "Free, cross-platform economy strategy game." Description sells delegation: "You delegate in times of war and in times of peace!" | Flathub: 7, all captioned, but **the first is "Main Menu"**. itch: 7. | itch embeds two YouTube videos. | "Free" appears in the itch tagline and Flathub's price label; no fairness sentence. | itch listing is stale: last devlog "Widelands Build 20 Released" (May 2019) and a commenter complains the installer is six years old. Flathub: 37,835 installs, 742 last month. Not on Steam search. |
| **Beyond All Reason** — [site](https://www.beyondallreason.info/), [Flathub](https://flathub.org/apps/info.beyondallreason.bar) | Site hero lines include "The Epic scale RTS experience you've been waiting for". Flathub summary "Total Annihilation Inspired RTS". | Site: full-width gameplay backgrounds. Flathub: 20, uncaptioned, mixed sizes up to 2560×1440. | Site has a "Watch Trailer" link. | Buttons read "Play for Free" and "Download & Play for Free". The home page does not use the words "open source". About 21 attributed testimonials. | Site news dated June 16, 2026 announces a publisher and a planned Steam release. Not yet in Steam search. Flathub: 115,916 installs, 2,276 last month. |
| **OpenTTD** — [site](https://www.openttd.org/), [Steam](https://store.steampowered.com/app/1536610/OpenTTD/), [Flathub](https://flathub.org/apps/org.openttd.OpenTTD) | Steam short description opens with what the player does (earn money "by transporting passengers and cargo"), then calls it "an open-source remake and expansion" of the 1995 original. | Steam: 13 at 1920×1080. Flathub: 4, each captioned with a benefit (e.g. "Plan and manage a growing transport empire"). | Steam: 1 trailer. Site: none. | Steam description ends with a "Free and open-source" section naming the GPL v2. The project home page never says "free". | Steam description uses one-word section labels: Build, Transport, Upgrade, Extend. Flathub: 90,657 installs, 1,610 last month. |

Flathub install counts come from `https://flathub.org/api/v2/stats/<app-id>` and count Flatpak installs only; they are a bounded visibility signal, not player numbers.

### Patterns across the table

Observed [V]/[S]:

1. **Genre words sit in the name or subtitle.** "RTS Strategy", "A real-time base building RTS", "A Civilization Strategy Game", "Offline Strategy", "Real-time strategy game". Only Northgard and Bad North, both with established PC brands, use mood lines.
2. **Screenshot one does a job.** Either a genre/value caption over gameplay (Rusted Warfare, Polytopia) or uncaptioned gameplay that reads at a glance (Bad North). Northgard spends it on DLC art. Widelands spends it on a menu.
3. **Counts:** 8–10 per device on Play for the four re-verified games; 5–10 on iPhone.
4. **All four re-verified Play listings have a trailer; only two of the four have an iOS app preview.**
5. **Only the games with nothing extra to sell state the deal**, and they state it bluntly and early: Rusted Warfare in screenshot one and bullet one, Unciv in its first line [S], 0 A.D. as a named section. Paid premium ports say nothing.
6. **Indirect control is sold as a benefit** by Bad North ("your soldiers do the rest") and Widelands (delegation), and Northgard's first features include "Assign your vikings to various jobs".
7. **Icons are one focal object, no text**, except Rusted Warfare.
8. **Open-source peers that caption their Flathub screenshots use benefit phrases**, not labels (OpenTTD, 0 A.D., Warzone 2100: "Seize territory + resources, build extensive bases").

Inference [I]: the fair-deal statement is a differentiator mainly on mobile, where the default expectation is ads and purchases; on desktop stores the peers treat "free and open source" as a closing fact, not a headline.

## 2. Where the current Globulation 2 listing stands

| Surface | Observed on 2026-11-24 | Source |
| --- | --- | --- |
| App Store (iPhone/iPad) | **Live**: version 0.11.700, released 2026-11-23 per the lookup API and the page's version history. Subtitle "Colony strategy under pressure". **One** iPhone and **one** iPad screenshot; the iPhone image is a portrait capture of the main menu over a sparse early-game map. No app preview. No ratings yet. Privacy label "Data Linked to You" listing contact info (email, name), user content (including photos or videos and emails or text messages), identifiers, usage data, diagnostics and other data. No accessibility declarations. Description says "free and open source" and that single-player needs no account; it does not mention ads or purchases. [V] | [App Store page](https://apps.apple.com/us/app/globulation-2/id6817603328) |
| Google Play | The public details URL returns HTTP 404. This is consistent with the closed-test status in the [rollout ledger](../planning/approved-storefront-rollout.md); the listing is not publicly visible, which also explains why store search does not return it. [V] | `https://play.google.com/store/apps/details?id=org.globulation2.glob2` |
| Microsoft Store | **Live** (catalogue record: released 2026-11-01, updated 2026-11-23). Free, no ratings. 4 screenshots (one 1280×720, three 2560×1440), 2:3 poster, 1:1 box art and 16:9 hero present. No trailer. Four feature bullets. [V] | Store catalogue API for product `9PH4FCRMX19F` |
| itch.io | Live. 4 screenshots, no video. Metadata shows "Average session: About a half-hour" and an AI disclosure reading "Generative AI assisted with some artwork, translations and code." [V] | [itch.io page](https://genixpro.itch.io/globulation-2) |
| Snap Store | Live with the v1 copy and 4 images (colony, river battle, strategic view, terrain). [V] | [Snap Store page](https://snapcraft.io/globulation2) |
| Copy source | Headline "Build a thriving colony in contested territory." No "no ads", "offline" or "no in-app purchases" outside the Amazon tail. The word "globs" does not appear. | [translations/en.md](../translations/en.md) |

The App Store status differs from the "Waiting for Review" entry the team was working from; the rollout owner should re-read the console before scheduling Apple changes.

## 3. Platform rules for assets and text

Rules below were read from the primary sources on 2026-11-24 unless marked [S]. Sizes are in pixels.

### Google Play

Sources: [Add preview assets](https://support.google.com/googleplay/android-developer/answer/9866151), [Metadata policy](https://support.google.com/googleplay/android-developer/answer/9898842), [Create and set up your app](https://support.google.com/googleplay/android-developer/answer/9859152).

- **Text limits:** app name 30, short description 80, full description 4,000. [V]
- **Title, icon, developer name (policy):** nothing indicating store performance, ranking, "price or promotional information" or Play programmes; no emoji; no all-caps unless it is the brand. [V]
- **Description (policy):** no unattributed or anonymous user testimonials. [V]
- **Short description (guidance, "highly recommended"):** state the core purpose; for games the unique aspects may include mechanics, modes and "connectivity (such as offline/online)". Avoid performance, ranking, award, testimonial, price or promotional language and calls to action; no emoji, symbols or capitals for emphasis. [V]
- **Icon:** 512×512, 32-bit PNG, at most 1,024 KB; no badges or text suggesting ranking or price. [V]
- **Feature graphic:** 1024×500, JPEG or 24-bit PNG without alpha. Required. Used as the video cover. Should not repeat the icon's branding or carry fine detail. Words to avoid include "Best", "#1", "Top", "New", **"Free"**, "Discount", "Sale". [V]
- **Screenshots:** 2–8 per device type; phone images 320–3,840 per side. To be eligible for large-format recommendation placements a game needs **at least three 16:9 landscape (min 1920×1080) or three 9:16 portrait (min 1080×1920)** screenshots showing the in-game experience. Taglines only if needed and no more than 20% of the image. Avoid performance, ranking, award, testimonial, price or promotional content and calls to action. Tablet/Chromebook sets: at least 4, 1,080–7,680, and avoid extra text because it can be cropped. [V]
- **Preview video:** one YouTube URL, public or unlisted, embeddable, not age-restricted, monetisation off. May autoplay muted for up to 30 seconds. Guidance: show the core experience within the first 10 seconds, at least 80% representative footage, limit logos and title cards, no people touching a device. Games need a video to appear in some placements. [V]
- **Labels:** "Contains ads" and "In-app purchases" are driven by console declarations, not by copy. [S]

Two distinctions matter for our wording. "Free" is named in the feature-graphic list but not in the screenshot or short-description word lists; all three, however, discourage "price and promotional information". And most of the screenshot and short-description rules are *eligibility guidance* ("highly recommended"), whose stated consequence is reduced promotion rather than removal. Rusted Warfare's live first screenshot carries "NO ads" and "NO microtransactions" [V], so such wording is tolerated at least there; whether it costs promotional eligibility is unknown [I].

### Apple App Store (iOS, iPadOS, macOS)

Sources: [Creating your product page](https://developer.apple.com/app-store/product-page/), [App Review Guidelines 2.3](https://developer.apple.com/app-store/review/guidelines/), [Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications), [App preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-preview-specifications).

- **Text limits:** name 30, subtitle 30, promotional text 170 (editable without a new version, not used for search), keywords 100. [V]
- **Description:** the first sentence is what people see before tapping "more"; avoid specific prices and keyword padding. [V]
- **2.3.3:** screenshots must show the app in use, "not merely the title art, login page, or splash screen"; text and image overlays are allowed. [V]
- **2.3.4:** previews may use only screen captures of the app; narration and text overlays are allowed. [V]
- **2.3.7:** names, subtitles, screenshots and previews should not include prices or terms; subtitles must not make unverifiable claims or reference other apps. [V]
- **2.3.8:** all metadata imagery must suit a 4+ audience. [V]
- **2.3.10:** no names, icons or imagery of other mobile platforms or marketplaces. [V]
- **2.3.2:** if there are in-app purchases, say what needs buying. Not applicable while nothing is sold. [V]
- **Screenshots:** 1–10 per device size; JPEG or PNG, no alpha. iPhone large set, portrait or landscape: 1290×2796 / 1320×2868 class, or the 6.5-inch 1284×2778 / 1242×2688. iPad 13-inch: 2064×2752 or 2048×2732 (either orientation). Mac: 16:10 at 1280×800, 1440×900, 2560×1600 or 2880×1800. Depending on orientation, the first one to three appear in search when there is no preview. [V]
- **App previews:** up to 3 per device size and language, **15–30 seconds**, 500 MB max, 30 fps max. iPhone 886×1920 or 1920×886; iPad 1200×1600 or 1600×1200; Mac 1920×1080. Autoplay muted. [V]
- Custom product pages and in-app events were described in the earlier pass and not re-checked. [S]

### Microsoft Store

Source: [App screenshots, images, and trailers](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/screenshots-and-images) (page metadata: updated 2026-08-24). [V]

- **Screenshots:** 1 required, up to 10 desktop; "at least four" suggested and the FAQ says 5–8. PNG, 1366×768 or larger, 4K supported, 50 MB max. Keep key content in the top two-thirds. No added logos, icons or marketing messages inside the image. Optional caption of up to 200 characters, entered as a field per language.
- **Store logos for games:** 2:3 poster (720×1080 or 1440×2160), strongly recommended, may include the name, bottom third kept clear; 1:1 box art (1080×1080 or 2160×2160); 1:1 tile icon 300×300.
- **16:9 super hero art:** 1920×1080 or 3840×2160 PNG, **no title or text**, avoid UI, bottom third clear. Required for games if trailers are to show at the top of the listing.
- **Trailers:** up to 15; MP4 or MOV at 1920×1080; 2 GB max; 60 seconds or less recommended; each needs a 1920×1080 PNG thumbnail and a title; no age-rating cards.

### Steam

Sources: [Graphical asset rules](https://partner.steamgames.com/doc/store/assets/rules), [Store graphical assets](https://partner.steamgames.com/doc/store/assets/standard), [Trailers](https://partner.steamgames.com/doc/store/trailer). [V]

- **Capsules** may contain only game artwork, the name and an official subtitle. No review scores, award names or logos, discount copy, or other products. Any text must be localised for every supported language. Update or event text goes through time-limited artwork overrides.
- **Sizes:** header 920×430; small 462×174 (logo should nearly fill it); main 1232×706; vertical 748×896; optional page background 1438×810.
- **Screenshots:** at least 5, 1920×1080 minimum, 16:9. They must show gameplay only: no concept art, marketing copy, awards or written descriptions. Menus only if they are a distinctive part of the game. Mark at least four as suitable for all ages.
- **Trailers:** a trailer is required; lead with a gameplay trailer; assume under ten seconds to make an impression and that it may play without sound; up to 1920×1080; visible HUD is encouraged.

### Epic Games Store

Sources: [Storefront Media Guide](https://dev.epicgames.com/docs/epic-games-store/sales-and-marketing/marketing/storefront-media-guide), [Content Requirements](https://dev.epicgames.com/docs/epic-games-store/requirements-guidelines/content-ratings/content-guidelines), [carousel merchandising PDF](https://static-assets-prod.epicgames.com/eos-docs/files/marketing-overview-files/EGS_Storefront_Merchandising_Carousel-Guidelines.pdf) [S]. The two documentation pages render only in a browser; they were read in one on 2026-11-24. [V]

- **Product logo (required):** 960×540 PNG, 1 MB max; landscape, little empty space, legible on a dark background.
- **Offer images (required):** landscape 2560×1440 and portrait 1200×1600, JPEG or PNG, for both the store and the library. They must include the logo with the product name, with key art and logo inside the critical area.
- **Media carousel (required, min 1):** images 1920×1080, 4 MB max; videos 1920×1080 MP4, 300 MB max, 30 or 60 fps. Recommended: at least five assets including a video, video first, real screenshots included, **minimal text** so the page works across languages. Epic states that carousels without screenshots or without video hurt purchase rates (no figures given).
- **About section:** text plus at least one image (at least 700 wide, 4 MB); 10,000 characters. Up to 20 optional additional images at 1920×1080 JPEG, 1 MB.
- **Social preview (optional):** 1200×1200 JPEG, 4 MB.
- **Text policy:** the About section and short description must describe only the product and must not reference or promote other storefronts. Other platforms may be mentioned where the game has crossplay.
- **Media policy:** videos must not have a black cover frame or show ratings-board ratings; media that references other platforms needs Epic's legal notice or the reference removed.
- **Localisation:** only English is required; Epic recommends English, French, German, Russian and Spanish at launch.

See also the project's own [Epic requirements note](../planning/epic-store-requirements.md).

### Amazon Appstore

Source: [Add store listing information](https://developer.amazon.com/docs/app-submission/add-store-listing-information.html). [V]

- **Text:** short description up to 2,000 bytes (about 1,200 English characters; Fire TV shows the first 200); long description 4,000 characters; plain text only. **Three to five** feature bullets. Optional comma-separated keywords.
- **Icons:** 114×114 and 512×512 PNG; guidance says not to simply scale one from the other and to use logos or key art without slogans.
- **Screenshots:** 3–10; accepted sizes include 1280×720, 1920×1080, 1920×1200 and 2560×1600; PNG or JPEG. Show only the app, on the right device type; no photographs of people using it.
- **Promotional image (optional):** 1024×500; not a screenshot; includes the app name; no price, ratings or descriptive text; text at least 50 px from the edges.
- **Videos (optional):** up to 5; 16:9 or 4:3.

The canonical source currently holds six Amazon feature bullets (`amazon_feature_1`–`6` in [en.md](../translations/en.md)); the page above says three to five. Whether the console accepted six was not checked.

### Rule conflicts that shape a shared asset set [I]

| Asset decision | Play | Apple | Microsoft | Steam | Epic | Amazon |
| --- | --- | --- | --- | --- | --- | --- |
| Caption text inside screenshots | Allowed, ≤20% of image, avoid price/ranking words | Allowed | Not inside the image; use the caption field | Not allowed | Discouraged (minimal text) | Not prohibited by the page read |
| The word "Free" in images | Avoid | Avoid (2.3.7) | Avoid (no marketing messages) | Not allowed in capsules/screenshots | Avoid | Not in the promotional image |
| Trailer length ceiling | 30 s autoplay window | 30 s hard limit | 60 s recommended | none stated | none stated | none stated |
| Naming other stores/platforms in text | — | Not other mobile platforms | — | — | Not other storefronts | — |

So: one captioned set for Play, Apple and (optionally) Amazon; one clean set for Steam, Epic, Microsoft, itch.io and AppStream/Snap, with Microsoft and AppStream captions supplied as text fields.

## 4. Ranked gaps versus comparables, with checkable recommendations

Ranking is the analyst's judgement of likely effect on a first-time visitor, weighted by how solid the evidence is [I]. Every "Check" is something a reviewer can verify on the finished asset or page. The footage rule in [gameplay-video.md](../planning/gameplay-video.md) applies to every screenshot and video frame.

### Gap 1 — Screenshots: one menu image where peers show 5–10 gameplay images

Evidence: App Store shows one portrait main-menu image per device [V]; peers show 5–10, and guideline 2.3.3 says screenshots should not be merely title art or a splash screen [V]. Widelands is the only peer that opens with a menu [V].

Recommendation (screenshot order and captions):

| Slot | Content | Caption job (captioned sets only) |
| --- | --- | --- |
| 1 | Developed colony with a fight visible at its edge | Genre plus what you do, in five words or fewer, as Polytopia and Rusted Warfare do |
| 2 | The control idea: a flag or priority being set with workers streaming to it | Indirect control as a benefit ("you decide, they do") |
| 3 | A large battle between two colours | Conflict and stakes |
| 4 | Economy close-up: food, swarm, training | The colony-economy promise |
| 5 | A different map or terrain type, pulled back | Variety of maps |
| 6 | Skirmish or campaign against computer opponents | Solo and offline play |
| 7 (mobile) | Any strong gameplay frame | The fair deal in words (see gap 2), if the store permits |
| 8 | Map editor or multiplayer lobby only if it reads instantly | Depth for those who scroll |

Checks:
- At least 6 screenshots per device size on Apple and Play; at least 5 on Steam and Epic; at least 4 on Microsoft; at least 3 on Amazon.
- Slot 1 is gameplay that satisfies the footage rule; no menu appears before slot 6.
- Play phone set includes at least three 16:9 images of at least 1920×1080.
- Each caption covers no more than 20% of the image and contains none of: Free, Best, #1, Top, New, Sale, Discount, download/play now.
- Each caption is readable when the image is scaled to 400 px wide.
- Captioned images are real device captures for the platform they are uploaded to (2.3.3; Amazon's device rule).
- Steam, Epic and Microsoft sets contain no caption text or logos.
- iPhone orientation is a deliberate choice: landscape shows one image in search and portrait shows three [S]. Bad North's portrait composites of two landscape frames are a precedent if the phone build is played in landscape [V].

### Gap 2 — The fair deal is not stated

Evidence: the only current mention of ads or purchases is the Amazon tail [V in en.md]. Rusted Warfare, Unciv [S] and 0 A.D. state it early and bluntly [V]. See [player-priorities.md](player-priorities.md) for the demand evidence.

Recommendation: one plain sentence, in the first two lines of the full description on every mobile store, covering free, no ads, no in-app purchases, no loot boxes and no premium currency, followed by the scope of offline and account-free play. Keep it out of the Play title, icon and feature graphic. On Play, prefer a gameplay-only short description and put "offline" there only if space allows, since Google lists connectivity as a legitimate short-description topic. On desktop stores place the same facts in the closing "Free and open source" block, as OpenTTD does.

Checks:
- The sentence appears within the first 250 characters of the Play, App Store and Amazon full descriptions.
- No image, title, subtitle or icon contains the word "Free" or a price.
- The Play listing shows neither the "Contains ads" nor the "In-app purchases" label, and the App Store page shows no In-App Purchases section, for the build being described.
- The claim is true of the shipped build on that store: [product facts B01–B04](../facts/product.md) record purchase and credit code that is off by default; someone must confirm it is unreachable in each store build before the sentence ships.
- "No account" is always scoped to single-player/offline play, matching the Epic and iOS tails.

### Gap 3 — No trailer

Evidence: all four re-verified Play listings and OpenTTD's Steam page have one [V]; Play, Steam and Epic each say video affects placement or purchase [V]; Globulation 2 has none on any store [V].

Recommendation: a 30–45 second master with a **30-second-or-shorter cut** for Apple and for Play's autoplay window.

Checks:
- Gameplay is on screen by second 2 and the core loop (order given, workers respond, fight) is shown within the first 10 seconds.
- At least 80% of the runtime is real gameplay at real speed; no title card longer than 2 seconds at the start.
- It is understandable with the sound off.
- Apple cut: 15–30 seconds, captured on the device family it is uploaded for, at 1920×886 (iPhone) and 1600×1200 (iPad).
- Play: YouTube video with monetisation off, public or unlisted, embeddable.
- Microsoft: 1920×1080, with a text-free 16:9 hero image uploaded, no rating card.
- Epic: first asset in the carousel, non-black cover frame, no ratings-board card.
- No fingers or devices in frame; no store badges or other platforms shown.

### Gap 4 — Name and subtitle carry no genre term

Evidence: "Colony strategy under pressure" contains neither "RTS" nor "real-time"; most peers put the genre in the name or subtitle [V]. The Play title uses 13 of 30 characters.

Recommendation: put "RTS" or "real-time strategy" in the iOS subtitle and in the first words of the Play short description; consider a suffixed store name on Play and Apple (for example a form like "Globulation 2: Colony RTS", 25 characters) [I]. A name change touches 44 locales and brand consistency, so it is a coordinator decision.

Checks: the genre term appears in name or subtitle on Apple and in title or short description on Play; subtitle ≤30 characters in every locale; no unverifiable claim ("best", "ultimate") in the subtitle.

### Gap 5 — The distinctive mechanic is described abstractly

Evidence: current copy says creatures "act autonomously" and never says "globs". Bad North, Widelands and Northgard each describe the same idea as something the player does and gains [V]. A Gamepressure editorial credits Northgard's mobile success partly to not having to control individual units on a touch screen ([source](https://www.gamepressure.com/editorials/the-best-mobile-games-2021-editors-choice/northgard-finally-a-good-mobile-rts/z14f7), [V]).

Recommendation: one concrete sentence in the first paragraph and one caption (slot 2) that names the player's verbs (place a flag, set how many workers, choose what to build) and the result (globs do the work).

Checks: the first 250 characters contain at least one player verb and the word "globs"; the sentence makes no ease or accessibility claim; a person who has not seen the game can say what the player does after reading only the first paragraph.

### Gap 6 — Privacy label works against the pitch

Evidence: our label is "Data Linked to You" with contact info and user content; all four re-verified peers show "Data Not Linked to You", and Bad North's Play page says "No data collected" [V].

Recommendation: not a copy task. The owner of the App Store privacy answers should confirm each declared category against what the iOS build actually collects, and split offline play from online-account features if the form allows.

Check: every category on the label maps to a named feature; categories that apply only to optional online play are described that way in the description.

### Gap 7 — Icon finish

Evidence: the current icon is a single blue glob on a flat purple square [V], which already matches the peers' one-object, no-text pattern. Peers add depth behind the object (scene, gradient) and a crisp silhouette [V]. The team has decided on a faithful sharp redraw.

Checks:
- Silhouette recognisable at 48 px (Play's page HTML requests the icon at 48 px for compact rows [V]).
- No text, badge or border.
- Play 512×512 32-bit PNG under 1,024 KB; Amazon 114 and 512 drawn, not scaled; Microsoft 300×300 tile; Apple master without transparency.
- The same glob shape appears on every store.
- The Play feature graphic does not simply repeat the icon.

### Gap 8 — Store-specific key art set is incomplete

Evidence: Microsoft has poster, box art and hero [V]; Play feature graphic exists per the ledger; Steam capsules, Epic offer images in final form and an Amazon promotional image were not observed. Peers use painted or composed key art with the logo (0 A.D. itch header, Northgard) [V]. The project's rule is real game art only.

Checks, per export:
- Play feature graphic 1024×500: no "Free"/ranking words, legible at half size.
- Epic: logo 960×540 PNG legible on dark; offer landscape 2560×1440 and portrait 1200×1600 with logo inside the critical area.
- Steam: 920×430, 462×174 (wordmark nearly fills it), 1232×706, 748×896; art and name only.
- Microsoft: poster and box art with the name in the top two-thirds; hero with no text.
- Amazon promotional image 1024×500 with the name, text ≥50 px from edges, not a screenshot.
- Every composition is built from in-engine captures or game sprites, and the manifest says which.

### Gap 9 — No heritage or proof line

Evidence: peers use awards, install counts, lineage and age ("inspired by", "Work on 0 A.D. began in 2001", "Over A Decade in the Making" [S]) [V]. Globulation 2 has none, though its [official site](https://glob2.online/) dates the project to 2004.

Recommendation: one dated heritage sentence near the end of the description, as Apple advises for accolades.

Checks: the year matches the official site; no superlative or ranking claim; no unattributed testimonial (Play policy); not placed in the Play short description or any image.

### Gap 10 — Listings drift out of date

Evidence: Widelands' itch page draws a public complaint about a six-year-old installer [V]. Our stores carry different versions (see the rollout ledger), and the App Store status had already moved on from the team's record [V].

Check: the storefront-v2 ledger records, per store, the live version and the date the public page was last read.

## 5. Open questions

- Does caption wording such as "No ads" reduce Play promotional eligibility? No source settles it.
- Portrait or landscape for iPhone screenshots: depends on how the phone build is actually played, which this pass did not test.
- Whether six Amazon feature bullets are accepted.
- Mac App Store page and screenshots were not examined separately.
- Apple custom product pages and in-app events remain unverified from primary sources in this pass.
