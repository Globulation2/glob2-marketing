# What strategy players say they value and resent

[Analysis index](README.md) · [Mobile and desktop store comparables](mobile-store-comparables.md) · [Audiences](audiences.md) · [Jobs to be done](jobs-to-be-done.md) · [Positioning v2](positioning.md) · [MCP claims and prior art](../planning/mcp-outreach/product-and-prior-art.md)

Observed **2026-11-24**. This record collects public evidence on twelve things mobile and PC strategy players are said to care about, how games with fair monetisation word them in store listings, and what that implies for Globulation 2's wording on mobile and on desktop. It ends with prioritised message lists.

## Evidence rules and limits

Strength labels:

- **Survey** — a stated sample and method. Most are run or paid for by vendors with an interest in the answer; that is noted where known.
- **Telemetry** — aggregated usage data from an analytics vendor.
- **Press** — editorial reviews, trade reporting, regulator or institutional publications.
- **Anecdotal** — individual store reviews, forum comments and what listings choose to say. Useful for wording, not for size.

Source labels: **[V]** read by the analyst on 2026-11-24 at the linked page; **[2nd]** a figure taken from secondary coverage because the original report is paywalled or could not be fetched; **[S]** carried from the earlier session pass and not re-checked; **[I]** analyst inference.

Limits that apply throughout:

- **No Globulation 2 players were asked anything.** The project's own research plan was stopped before it ran ([audiences.md](audiences.md)). Everything below is about other people's players.
- No survey found asks strategy players specifically. The surveys cover gamers in general, mobile gamers, or browser-game players.
- Surveys about why people *quit* games do not show that saying "no ads" in a listing wins installs. That step is inference.
- Reddit could not be fetched. Community evidence comes from Hacker News threads, public store reviews and project pages, which skew technical and English-speaking.
- "Featured review" means one of the three user reviews Google Play displayed on the public listing page when it was read; they are not a sample.
- Quotations are short fragments; follow the links for context.

Every wording implication is inference [I] and must stay true for the build on each store. The claims that need a product check before use are collected in [Claims to verify](#claims-to-verify-before-any-of-this-wording-ships).

## Summary table

| Priority | Best evidence found | Strength | Do fair-monetisation listings say it? | Mobile wording | Desktop wording |
| --- | --- | --- | --- | --- | --- |
| Ads | 64% say ads interrupt play (Bain 2025); 52% quit after repeated disruptive ads (Deloitte/AdMob 2025) | Survey | Yes, early and bluntly | Lead fair-deal fact | One clause near the end |
| Pay-to-win | Top stated reason for abandoning mobile games (Mistplay 2023); 30% quit reason in browser games (Newzoo 2026) | Survey (vendor) | Yes (Rusted Warfare) | Say it, tied to "nothing to buy" | Frame as equal rules in multiplayer |
| Timers / energy | No survey found | Anecdotal | Yes (Rusted Warfare leads with it) | Optional, carefully phrased | Omit |
| Loot boxes | Regulator and public-health attention; little on player choice | Press | No comparable says it | In the description sentence, not captions | In the description sentence |
| Premium currencies | EU consumer authorities' 2025 principles; individual reviews | Press / anecdotal | Rarely | "No premium currency" in the sentence | Same |
| Offline play | Listing practice; Google names it as a selling point; 1.29 M verified signatures for keeping games playable | Press / anecdotal | Yes | High, with scope | Medium, plus LAN |
| No-account play | 23% of browser-game players value not having to pay or register | Survey (adjacent) | Rarely | State with scope | State with scope |
| Touch controls | Reviews split on mobile RTS controls; indirect control praised | Press | Yes | Describe the control model, no ease claim | Not applicable |
| Session length | Strategy sessions average over 30 minutes (Adjust 2026) | Telemetry | Sometimes (save anywhere) | Do not promise short matches | Not a selling point |
| Multiplayer fairness | Same as pay-to-win; toxicity worries push people to bots | Survey / anecdotal | Sometimes | Secondary | Secondary, with solo first |
| AI opponents / solo play | 53% of gamers prefer single-player (MIDiA 2024) | Survey | Yes | High: "computer opponents" | High |
| Open source | No survey; strong response in developer communities | Anecdotal | Yes on open-source listings | Supporting proof | Prominent on Linux/itch channels |

## The priorities in detail

### 1. Ads

**Evidence.**
- Bain & Company's 2025 gamer survey (more than 5,000 people in six countries) reports that 64% of players say ads interrupt their gaming experience, up five points in a year. [Bain, 12 Aug 2025](https://www.bain.com/insights/gamer-survey-great-gameplay-is-no-longer-enough-gaming-report-2025/) [V]
- A Deloitte and Google AdMob study (7,000 gamers, completed early 2025) says repeated exposure to disruptive ad features pushes 52% of gamers to quit, and one in five would abandon a favourite title over bad ad design. [Deloitte press release, 10 Jun 2025](https://www.deloitte.com/us/en/about/press-room/deloitte-improve-mobile-game-advertising.html) [V]. AdMob sells ads; the study argues for better ads, not none.
- Newzoo and Google's February 2026 survey of about 7,500 browser-game players lists ads that interrupt play as the most common reason for quitting (39%). The same survey finds 40% "generally fine" with ads and 43% disliking them. [GameDev Reports recap, 28 Sep 2026](https://gamedevreports.substack.com/p/google-and-newzoo-the-h5-gaming-audience) [2nd]
- Counter-evidence carried from the earlier pass: a 2014 poll preferring free-with-ads to paid, and a PubMatic study finding South-East Asian players mostly neutral [S].

**Strength.** Survey. Solid that *interrupting* ads are resented; not evidence that every player avoids ad-supported games.

**How listings phrase it.** Rusted Warfare's first screenshot says "NO ads" [V, [Play](https://play.google.com/store/apps/details?id=com.corrodinggames.rts)]. Unciv's opening line includes "no ads, free forever!" [S]. 0 A.D.'s itch page promises "no in-game advertising" [V, [itch.io](https://play0ad.itch.io/0ad)]. A featured Polytopia review lists "no gems, no wait times, no ads" [V, [Play](https://play.google.com/store/apps/details?id=air.com.midjiwan.polytopia)].

**Implication.** Mobile: "No ads" belongs in the first fair-deal sentence; the absence of Play's "Contains ads" label backs it up. Desktop: ads are not the norm on Steam, Epic or itch.io, so leading with "no ads" there would answer a question nobody asked; fold it into the closing free-and-open-source line.

### 2. Pay-to-win

**Evidence.**
- Mistplay's 2023 mobile loyalty report: a feeling of pay-to-win was the top reason players gave for abandoning a game (65%), ahead of bugs (56%). Sample size not stated in the coverage. [GameDaily, 28 Nov 2023](https://www.gamedaily.biz/?p=9999) [2nd]. Mistplay is a rewards platform.
- Newzoo/Google 2026: a focus on pay-to-win is the third most common reason for quitting browser games (30%). [recap](https://gamedevreports.substack.com/p/google-and-newzoo-the-h5-gaming-audience) [2nd]
- A featured Rusted Warfare review calls most mobile rivals "online pvp, and obnoxiously greedy" [V, Play].
- A Beyond All Reason team member felt the need to deny rumours of "microtransactions, pay-to-win" publicly when a paid campaign was announced. [Hacker News, 21 Jun 2026](https://news.ycombinator.com/item?id=48619976) [V]

**Strength.** Survey (vendor, secondary) plus anecdotal. Consistent direction; exact numbers are soft.

**How listings phrase it.** Rusted Warfare: "NO pay-to-win" and "A pure RTS with no microtransactions" [V].

**Implication.** The claim is only credible next to "no in-app purchases": nothing to buy, so nothing to pay to win. Mobile: include the phrase; players there recognise it. Desktop: phrase it as equal footing ("every player has the same units and rules") if that is verified. The Beyond All Reason episode suggests stating the deal before anyone speculates about it.

### 3. Timers and energy

**Evidence.** No survey was found. The evidence is that Rusted Warfare opens its first screenshot with "NO artificial wait timers" [V] and that the Polytopia review above lists "no wait times" among its virtues [V].

**Strength.** Anecdotal.

**Implication.** Mobile: the phrase signals "not that kind of mobile strategy game" to RTS players, but Globulation 2 is real-time and things take time to build. If used, it must be about paying or waiting to skip ("no timers to pay past"), never a bare "no waiting". It is the most droppable item on the mobile list. Desktop: omit.

### 4. Loot boxes

**Evidence.** The public evidence is about harm and regulation, not about players choosing games.
- The UK government's response to its loot-box call for evidence and related regulator work [2nd, [gov.uk](https://www.gov.uk/government/consultations/loot-boxes-in-video-games-call-for-evidence/outcome/government-response-to-the-call-for-evidence-on-loot-boxes-in-video-games)], and a 2021 commissioned poll in which 69% agreed loot boxes promote gambling to younger players [2nd, [European Gaming](https://europeangaming.eu/portal/latest-news/2021/05/14/92391/nearly-half-of-gamers-call-for-restrictions-on-microtransactions/)]. Neither was read in full in this pass.
- None of the ten mobile comparables mentions loot boxes in its listing ([V] for four, [S] for six).

**Strength.** Press / regulatory. Thin for our purpose.

**Implication.** The project has decided to say "no loot boxes". Because no comparable does, it reads best as part of the single fair-deal sentence in the description, not as a caption or headline. It matters at least as much to PC players and parents as to mobile players [I].

### 5. Premium currencies

**Evidence.**
- On 21 March 2025 the EU's consumer-protection network published principles on in-game virtual currencies, including showing real-money prices clearly and not obscuring costs. They are not legally binding. [Arthur Cox summary, 1 Apr 2025](https://www.arthurcox.com/insights/eu-consumer-protection-new-principles-for-virtual-currencies-in-video-games/) [V for the summary; the Commission's own page could not be machine-read]
- The Polytopia review praising "no gems" and no "premium shop" [V].

**Strength.** Press / anecdotal.

**Implication.** Players say "gems", "coins" or "premium currency". "No in-game currency" is ambiguous in a game whose economy runs on in-game resources; "no premium currency" or "nothing to buy with real money" is clearer [I]. The source code contains credit wallets for optional hosted services that are off by default ([product facts B02–B04](../facts/product.md)); the sentence is only safe while those stay unreachable in store builds.

### 6. Offline play

**Evidence.**
- No survey asking mobile players about offline play was found.
- Listings treat it as a selling point: Iron Marines puts "Offline" in its Play title [S]; Polytopia says it "can be played offline" and lists "Allow offline game play." [V]; Rusted Warfare offers "Online and offline multiplayer" [V].
- Google's own guidance names "connectivity (such as offline/online)" as a legitimate topic for a game's short description. [Play Console Help](https://support.google.com/googleplay/android-developer/answer/9866151) [V]
- The "Stop Destroying Videogames" European citizens' initiative, which asks that sold games be left in a functional state, was submitted with 1,294,188 verified signatures. [European Commission, 26 Jan 2026](https://citizens-initiative.europa.eu/news/14th-valid-initiative-stop-destroying-videogames-submitted-commission-examination-2026-01-26_en) [V]. This is about PC and console games being switched off, not mobile connectivity.
- Browser-game players' top reason for liking the format is playing "anywhere, anytime" (35%). [Newzoo recap](https://gamedevreports.substack.com/p/google-and-newzoo-the-h5-gaming-audience) [2nd]

**Strength.** Press and listing practice; one large petition on an adjacent issue. No direct survey.

**Implication.** Mobile: say single-player works offline in the first lines, and consider "offline" in the Play short description. The iOS keyword list already includes it. Desktop: "plays offline and over LAN" pairs naturally with open source: a game you can keep. Always scope it; online multiplayer needs a connection, as the Windows tail already says.

### 7. Playing without an account

**Evidence.** Browser-game players value "not having to pay or register" (23%) [2nd, Newzoo recap]. No comparable listing mentions accounts ([V] for four). No mobile-specific survey found.

**Strength.** Survey on an adjacent audience; otherwise none.

**Implication.** Keep the existing scoped sentence (single-player needs no account). Do not shorten it to "no account". Two public facts cut against a blanket claim: the Epic tail says online play creates an account, and the App Store privacy label currently reads "Data Linked to You" with contact details ([comparables record](mobile-store-comparables.md#2-where-the-current-globulation-2-listing-stands)).

### 8. Touch controls

**Evidence.**
- Gamepressure's editors' choice piece on Northgard says the "touch controls have been well thought out" and credits not having to control individual units in combat. [Gamepressure, 8 Jan 2022](https://www.gamepressure.com/editorials/the-best-mobile-games-2021-editors-choice/northgard-finally-a-good-mobile-rts/z14f7) [V]
- Pocket Gamer's review of the same game (4.5/5) notes controls that "glitch a little bit", a phone screen that may be "a bit too small", and no autosave during long chapters. [Pocket Gamer, 19 Apr 2021](https://www.pocketgamer.com/northgard/review/) [V]
- A Hacker News commenter on Unciv describes how little screen area a phone leaves per map tile. [HN, 27 Nov 2023](https://news.ycombinator.com/item?id=38429039) [V]

**Strength.** Press and anecdotal. Controls are where mobile RTS reviews divide.

**How listings phrase it.** Rusted Warfare lists a "Fast interface" with minimap commands and multi-touch, and says it "Fully scales from phones to large screen tablets" [V]. Northgard says "Carefully redesigned for mobile" [V]. Bad North: "your soldiers do the rest" [V].

**Implication.** Mobile: Globulation 2's indirect control is its touch argument: no box-selecting, no chasing units. Describe the model (place a flag, set a number, globs go). Do not claim it is easy, "perfect for phones" or accessible; repository rules already bar unverified phone-compatibility claims, and small-screen readability has not been tested. Screenshots must be real device captures so the interface size is honest. Desktop: not a message.

### 9. Session length

**Evidence.**
- Adjust's 2026 report (top 5,000 apps, January 2024 to January 2026) puts average strategy-game sessions at 37.51 minutes, up from 31.72. [GameDev Reports recap, 15 Apr 2026](https://gamedevreports.substack.com/p/adjust-gaming-app-insights-report) [2nd]. "Strategy" there is dominated by large free-to-play titles.
- A Mindustry player on Hacker News likes that it is "fast to open up and play a bit, save, and then quit". [HN, 22 Dec 2023](https://news.ycombinator.com/item?id=38735403) [V]
- Rusted Warfare advertises saving and loading "for that quick lunch time battle" [V]. Pocket Gamer faulted Northgard for missing autosave [V].
- Our own itch.io page states "Average session: About a half-hour" [V]; match length has never been measured ([audiences.md](audiences.md)).

**Strength.** Telemetry (vendor) plus anecdotal.

**Implication.** Strategy players accept long sessions; what they ask for is the freedom to stop. Do not promise quick or short matches. If the game can be saved and resumed at any point on mobile, say that; it needs verifying first. Desktop: no message needed.

### 10. Multiplayer fairness

**Evidence.** The pay-to-win evidence above, plus two anecdotes: a featured Rusted Warfare review praising full lobbies at any hour [V], and a Hacker News reader who wants to try Beyond All Reason but will not touch PvP because of what they have read about its community ([HN, 21 Jun 2026](https://news.ycombinator.com/item?id=48620868)) [V].

**Strength.** Survey for the pay-to-win part; anecdotal otherwise.

**Implication.** Fairness has two meanings: nobody buys an advantage, and you are not forced into rough public matches. The first is covered by priority 2. The second argues for presenting solo play before online play. Our online population and wait times are unmeasured, so neither store should promise quick matchmaking. Any statement that phone and desktop players share the same rules or servers needs checking.

### 11. Computer opponents and solo play

**Evidence.**
- MIDiA Research: single-player is the favourite way to play for 53% of gamers; under-25s lean multiplayer. [MIDiA, 3 Oct 2024](https://www.midiaresearch.com/blog/most-gamers-prefer-single-player-games) [V]. Coverage of the full report gives 58% among mobile gamers [2nd, sample and country list not confirmed].
- The Beyond All Reason reader above asks whether they can "play this against bots" [V].
- A featured Polytopia review praises an AI that is "an actual challenge" at higher levels; a Rusted Warfare review finds single-player "A little easy" [V].

**Strength.** Survey (general gamers) plus anecdotal.

**How listings phrase it.** Rusted Warfare: campaign, skirmish and challenge missions "with full AI" [V]. Widelands: "an artificial intelligence to challenge you" [V, [Flathub](https://flathub.org/apps/org.widelands.Widelands)].

**Implication.** Both platforms: say early that you can play alone against computer opponents, with campaigns and skirmish maps. On mobile prefer "computer opponents" over "AI", so it is not mistaken for generative AI (see the next section). Do not claim difficulty quality; nobody has tested it.

### 12. Open source

**Evidence.** No survey. Signals:
- Open-source strategy games draw strong responses on Hacker News: Mindustry (600 points), Unciv (533), 0 A.D. (547 in 2013; 348 for its February 2026 release), Beyond All Reason (508 in June 2026). [HN search API](https://hn.algolia.com/api/v1/search?query=Mindustry&tags=story) [V]. That audience is developers.
- A commenter on the 0 A.D. release calls it "almost unbelievable that it is free and open source". [HN, 23 Feb 2026](https://news.ycombinator.com/item?id=47123884) [V]
- Flathub installs last month: 0 A.D. 4,662; Beyond All Reason 2,276; OpenTTD 1,610; Widelands 742 [V, Flathub stats API].

**Strength.** Anecdotal, and concentrated in Linux and developer communities.

**How listings phrase it.** Unciv's short description starts "Open source" [S]. OpenTTD's Steam page closes with a "Free and open-source" section [V]. 0 A.D. explains free "as in “Freedom”" [V]. Beyond All Reason's home page says "Play for Free" and does not mention open source [V].

**Implication.** Mobile: a supporting line that makes the fair deal believable (the code is public; there is no hidden catch). Desktop: prominent on itch.io, Snap, Flathub-style and Linux channels; a closing section on Epic, Microsoft and Steam. Pair it with the project's age for credibility.

## Playing alongside AI agents (desktop, MCP)

The project's own record, [product-and-prior-art.md](../planning/mcp-outreach/product-and-prior-art.md), establishes what can be claimed: the desktop game has an opt-in, local MCP server; the player keeps control; and several earlier projects rule out any "first" claim. This section asks a different question: is there public evidence that players *want* this?

**What exists.**

| Signal | What it shows | What it does not show |
| --- | --- | --- |
| Many builders: the prior-art table lists a dozen projects from December 2024 to November 2026 | Sustained maker interest | Player demand |
| "We ran AI agent swarms in Minecraft and Mindustry": 425 points, 176 comments ([HN, 29 Oct 2026](https://news.ycombinator.com/item?id=50296486)); one commenter: "Kinda just fun to watch" [V] | Developers enjoy *watching* agents play | Wanting to play alongside one |
| MCP Minesweeper Show HN: 123 points ([HN, Mar 2025](https://news.ycombinator.com/item?id=43420678)); an open-source LLM-plays-Pokémon project: 186 points ([HN, Feb 2025](https://news.ycombinator.com/item?id=43187231)) [V] | Novelty value in developer circles | Durability |
| Claude Plays Pokémon launch: TechCrunch described "the thousand-odd people in the Twitch chat" ([25 Feb 2025](https://techcrunch.com/2025/02/25/anthropics-claude-ai-is-playing-pokemon-on-twitch-slowly)) [V] | A spectator audience exists | Its size over time; no reliable peak figure was found |
| The two closest products, both RTS games built for human-plus-agent play: Castellan, 3 points ([HN, 26 Oct 2026](https://news.ycombinator.com/item?id=50246334)); Agent Command, 2 points ([HN, 14 Nov 2026](https://news.ycombinator.com/item?id=50498487)) [V] | Direct equivalents have not found an audience on that channel | That the idea cannot work; both are new and unknown |

**What cuts the other way.** Quantic Foundry surveyed 1,799 gamers between October and December 2025: 85% were below neutral on generative AI in games and 63% chose the most negative option. Attitudes were least negative for non-creative uses such as dynamic difficulty, and most negative for AI-made art, music and writing. [Quantic Foundry, 18 Dec 2025](https://quanticfoundry.com/2025/12/18/gen-ai/) [V]. The sample is self-selected from people who take a gamer-motivation quiz, and the questions concern AI used *in making or running* games, not a player bringing their own agent. A developer survey reported in the trade press points the same direction ([TechSpot on the GDC 2026 survey](https://www.techspot.com/news/111128-more-than-50-game-developers-generative-ai-harming.html)) [2nd, not read].

**Honest reading.** The evidence is thin. No survey found asks whether players want to share a game with their own AI agent. What exists shows curiosity among developers and AI hobbyists, mostly about watching, and broad hostility among core gamers to generative AI in games. Co-play interest among strategy players is unmeasured.

**Implications for wording [I].**

- Keep it off mobile listings entirely; the feature is desktop-only and the mobile audience gains nothing from the mention.
- On desktop, present it as an optional extra after the game itself: off unless you turn it on, your own agent, you stay in command, nothing AI-related is needed to play.
- Say what happens in plain terms (you set priorities; your agent handles a job you hand it), not "AI-powered".
- Never "first" (already decided).
- Keep "computer opponents" (built-in, deterministic) and "your AI agent" (external, optional) visibly separate so nobody thinks the game is AI-generated.
- The itch.io page already carries an AI disclosure about artwork, translations and code [V]. With the decision to use real game art only for storefront assets, whoever owns that page should confirm the disclosure still describes the product accurately; it should stay truthful rather than be minimised.
- Expect the message to do better on itch.io, GitHub-adjacent and developer channels than on Epic or the Microsoft Store.

## Prioritised messages

Order is the analyst's recommendation [I], following the project's decision that mobile leads with gameplay plus the fair deal and desktop adds AI co-play. Wording is the copywriter's; these are the jobs each line must do.

### (a) Mobile stores

1. **What it is and what you do**: a real-time strategy game where you grow a colony of globs and fight rivals for land. Genre term in the name, subtitle or first words. (Comparables pattern.)
2. **How you play**: you set priorities and place flags; globs do the work. Framed as command without micromanagement, with no ease claim. (Priority 8; Bad North, Widelands.)
3. **The fair deal, in one sentence**: free, no ads, no in-app purchases; then no loot boxes and no premium currency. (Priorities 1, 2, 4, 5.)
4. **Play alone, offline**: campaigns and skirmishes against computer opponents; single-player needs no connection and no account. (Priorities 6, 7, 11.)
5. **Nothing to pay to win**: everyone plays by the same rules. (Priorities 2, 10.)
6. **Depth**: economy, varied maps, map editor.
7. **Open source since 2004**: the reason the deal is real. (Priority 12.)
8. **Online multiplayer exists**, stated without promises about speed or population. (Priority 10.)
9. Optional and last: no pay-to-skip timers. (Priority 3.)

Leave out on mobile: AI agents and MCP; "quick matches"; "easy"; any blanket "no account".

### (b) Desktop stores

1. **What it is and what you do**: the same opening, with the colony-economy depth that PC strategy players look for.
2. **How you play**: indirect control as the distinctive design, tied to recognisable references only where a store allows it.
3. **Solo and multiplayer**: campaigns, skirmish against computer opponents, LAN and online; solo first.
4. **Free and open source since 2004**: playable offline, yours to keep, source public. On Linux, itch.io and Snap this moves up to second.
5. **Play alongside your own AI agent**: optional, opt-in, through the built-in MCP server on Windows, macOS and Linux; you stay in command. One short paragraph, after the game is fully described.
6. **Creation**: map editor; scripting where it is verified as available.
7. **The fair deal as a closing fact**: no ads, no purchases, no loot boxes, no premium currency.

Leave out on desktop: touch controls; "no timers"; any "first" claim; other storefronts' names on Epic.

## Claims to verify before any of this wording ships

| Claim | Why it needs a check |
| --- | --- |
| Nothing can be bought in the build on each store | Purchase and credit code exists in source, off by default ([product facts](../facts/product.md)) |
| Single-player works fully offline on iOS and Android | Stated for Windows; not confirmed per mobile build in this pass |
| No account for single-player on every platform | True per the iOS and Windows tails; privacy label suggests data collection paths exist |
| Games can be saved and resumed at any point on mobile | Would support the session-length message; unverified |
| All players have the same units and rules; cosmetic items confer nothing | Needed for any "no pay-to-win" or "same rules" line |
| Phone, tablet and desktop players can share matches | Needed before any cross-platform statement |
| The project dates from 2004 | Matches the [official site](https://glob2.online/); keep the citation |
| MCP is opt-in, local and desktop-only | Recorded in [product-and-prior-art.md](../planning/mcp-outreach/product-and-prior-art.md); re-check against the release being listed |

## Evidence gaps

- No survey of strategy players specifically on any of the twelve priorities.
- No survey on timers/energy, offline play on mobile, or account requirements on mobile.
- No evidence on demand for human-plus-agent co-play.
- No Reddit, Discord or TouchArcade threads could be read.
- Several survey figures rest on secondary coverage ([2nd]); the Mistplay sample size and the MIDiA mobile split are unconfirmed.
- No store-review mining beyond the featured reviews on four Play pages.
