# Storefront-v2 field map for translators and reviewers

[Translation contract](README.md) · [English master](en.md) · [Terminology](glossary.md) · [Platform matrix](platforms.json) · [Storefront v2 claims](../facts/storefront-v2-claims.md) · [Positioning v2](../analysis/positioning-v2.md)

Written 2026-11-24 for the `storefront-v2` English source and revised the same day after an independent copy and store-policy review, and again when the caption renderer measured how much text fits on a screenshot: overlay captions now have a limit per script instead of 28 characters everywhere, and trailer lines have 44 instead of 32 ([overlay caption length by script](#overlay-caption-length-by-script)). Revised 2026-11-26 to add `android_title`. It lists every field, how it differs from `storefront-v1`, its limits, where players see it, and how to handle the tight ones. It records the prepared source only; it does not show that any store listing has changed.

## What changed, in short

- v1 had 38 fields. v2 has 78. Three keep their v1 text, one is renamed with the same text, 17 are rewritten under the same ID, 17 are removed and 57 are new.
- 2026-11-26: `android_title` added at the user's request, so v2 now has 79 fields. It is the title on Google Play and Amazon only; see the [field status table](#field-status-against-storefront-v1).
- The listing now says what the player does ("you command the colony, not every unit"), states the deal on the second line ("Free. No ads. No in-app purchases. No loot boxes. No premium currency."), and lists verified numbers.
- Stores no longer share one description. Each store composes its own from shared blocks, so a field can appear on some stores and not others. Translate every field as if it could stand next to any other; do not rely on a sentence from another field for context.
- The word "globs" appears only in the description body, after `listing_intro` has said what globs are. Short fields, feature bullets, captions and trailer lines stand alone, so they say "your colony", "workers" or "warriors" instead. Do not put "globs" into a field whose English does not have it.
- Screenshot text now comes in two forms: short overlay captions drawn onto mobile screenshots, and plain caption sentences for stores with a caption field.

## Rules that apply to every field

- **Do not translate:** `Globulation 2`; `MCP`; `JavaScript`; `GPL`; every URL, character for character, including the space before a full stop that follows a URL. The checker rejects a field where one of these, or one of the numbers 23, 67, 16, 45, 2001 or 2004, is in the English and missing from the translation. Local numerals are accepted for the numbers.
- **Copy all other numbers exactly** (8 opponents, 10 lessons, version 3, 1v1). They are verified facts. Write every number as digits, not as words, and do not round, convert or add a number.
- **Platform names** (iPhone, iPad, Mac, Apple silicon, Android, Fire, Windows, macOS, Linux, itch.io) follow how the platform writes its own name in your language.
- **Never add a claim.** No "first", "best", "forever", "never", no player or download numbers, no "nothing is sold", no privacy promise, no "campaign", no promise about how fast an online opponent is found or how well an AI agent plays. If a faithful translation would imply one of these, reword it.
- **No all-capitals words** for emphasis, no emoji, no calls to action ("download now"), no hype adjectives.
- **Voice:** second person, short sentences, concrete verbs. Plain and warm. The English avoids idioms on purpose; do not add any. The one figure of speech is "a war is won at the inns as much as at the front" (`defense_body`): it means an attack fails when its food supply fails. If the image does not work in your language, say that plain fact instead.
- **Pronouns.** In `shot_overlay_build` and `trailer_line_1` ("You decide. They build."), "they" is the colony's creatures shown in the picture. Where your language needs a noun or a gender, use the word for the colony or its workers. "It" in `ai_body` ("watch what it does") is the AI agent.
- **"Landscape" has two meanings.** In `map_body` and `feature_maps` a landscape is one of the game's 67 kinds of randomly generated map. In `android_tail` and `ios_tail`, "portrait or landscape" is how the device is held. Use different words.
- **Headings end with a full stop** (or your language's equivalent) because some stores print a heading and its body on one line.
- **Feature bullets (`feature_*`) have no final full stop** and must each read correctly alone: Microsoft and Amazon show them as separate list entries. Do not type a bullet character, a dash, a number or a line break at the start of a bullet; the export adds the bullet mark each store needs. Every field is one paragraph of plain text with no line breaks.
- **Do not truncate to fit a limit.** Rephrase. The checker measures the composed store field and reports the excess. Spaces and punctuation count towards every limit.
- **Two kinds of rival:** "computer opponent" is built into the game; "AI agent" is the player's own outside program. Never use one word for both. See the [glossary](glossary.md).

## Field status against storefront-v1

Status: **unchanged** (keep the reviewed v1 translation), **renamed** (move the reviewed v1 translation to the new ID), **changed** (same ID, new English: retranslate), **new**, **removed** (delete from the locale file).

| Field | Status | Note |
| --- | --- | --- |
| `product_name` | unchanged | Always exactly `Globulation 2`. Still the title on every store except Google Play and Amazon. |
| `android_title` | new (2026-11-26) | `Globulation 2 - Offline RTS`. Added at the user's request of 2026-11-26: "For Android, on google play and amazon appstore - rename main title from "Globulation 2" to "Globulation 2 - Offline RTS" and translate that into all the languages. All other stores, just keep as is." The offline claim is safe on every platform ([storefront v2 claims](../facts/storefront-v2-claims.md), "Offline single-player without an account"), and the Amazon Fire edition is LAN and offline only. |
| `epic_tail`, `epic_legal` | unchanged | Account and legal wording saved in the Epic console. |
| `windows_search_term_1` | renamed from `windows_search_term` | Same English ("real time strategy"). |
| `headline`, `short_pitch`, `listing_intro` | changed | |
| `economy_heading`, `economy_body`, `map_heading`, `map_body`, `defense_heading`, `defense_body` | changed | `defense_*` now covers rivals and battle. |
| `open_source_heading`, `open_source_body` | changed | Now the heritage section. |
| `appstream_summary`, `ios_subtitle`, `ios_keywords` | changed | |
| `android_tail`, `ios_tail`, `amazon_tail` | changed | |
| `fair_deal_line`, `play_short_description`, `desktop_short_pitch` | new | |
| `windows_search_term_2` … `_7` | new | |
| `control_heading`, `control_body`, `features_heading` | new | |
| `feature_control`, `feature_maps`, `feature_opponents`, `feature_colonies`, `feature_tutorial`, `feature_editor`, `feature_replays`, `feature_offline`, `feature_scripting`, `feature_languages`, `feature_ai_coplay` | new | Replace the per-store v1 bullets. |
| `multiplayer_heading`, `multiplayer_online_body`, `multiplayer_crossplay`, `multiplayer_crossplay_apple`, `multiplayer_lan_body` | new | |
| `ai_heading`, `ai_body`, `ai_guide` | new | Desktop stores only. |
| `mac_tail`, `itch_downloads_note` | new | |
| `shot_overlay_<role>` (9), `shot_caption_<role>` (9) | new | Roles: `hero`, `build`, `economy`, `battle`, `territory`, `maps`, `opponents`, `fair_deal`, `ai_coplay`. |
| `trailer_title`, `trailer_line_1` … `_4`, `trailer_line_ai_coplay` | new | |
| `about_intro` | removed | Its content is in `listing_intro` and `control_body`. |
| `listing_open_source` | removed | Covered by `fair_deal_line` and `open_source_body`. |
| `windows_tail` | removed | Its facts are in `feature_offline` and `multiplayer_lan_body`; online play is switched per store. |
| `windows_feature_1` … `_4`, `amazon_feature_1` … `_6` | removed | Stores now reuse the shared `feature_*` fields. `amazon_feature_5` claimed campaigns; none ship. |
| `screenshot_caption_colony`, `_battle`, `_strategic`, `_terrain` | removed | They named maps. The new captions name none, so they survive re-captures. |

## Limits and where each field appears

Units are characters unless marked bytes. "Bytes" means UTF-8 bytes: a Latin letter is 1, an accented Latin letter or a Cyrillic, Greek, Arabic or Hebrew letter is 2, and a CJK, Thai or Indic character is 3. A "character" is one Unicode code point, so in Indic scripts, Thai, Arabic and Hebrew every vowel sign, tone mark or other combining mark counts as one character, and a space or punctuation mark counts as one. A zero-width space (U+200B) also counts as one.

### Short fields (the tight ones)

| Field | Limit | Appears | Notes |
| --- | --- | --- | --- |
| `android_title` | 30 in every locale | Google Play title; Amazon Appstore title | Keep `Globulation 2` exactly and the ` - ` separator, then "Offline RTS" in the words players in your language type into a store search: the genre term of your `ios_keywords` (usually "RTS") and the word for offline your catalog already uses, or the local loanword when that does not fit. No price word, ranking word, call to action, emoji or all-capitals word other than the acronym. The 30 is Google Play's title limit and binds in every locale (Amazon allows 200). English uses 27. |
| `play_short_description` | 80 | Google Play short description; F-Droid summary | The line under the title on Google Play, and the only text most visitors read. Names the genre, says "no ads" and "offline", and gives the colony-not-units contrast. No price word ("free", "no purchases"), no call to action ("play now", "download"), no ranking word, no capitals for emphasis, no symbols. Full stops are allowed because there are two sentences. English uses 75. |
| `ios_subtitle` | 30 | App Store and Mac App Store subtitle | Genre terms players search for. No price word, no claim that cannot be checked. English uses 25. |
| `ios_keywords` | 100 **bytes** | App Store keywords (not shown to players) | Comma-separated, no spaces after commas. Do not repeat words from the name or your subtitle. No price word, no other app's name. English uses 100. |
| `short_pitch` | 170 | App Store promotional text; Epic, Amazon and itch.io short description | Three sentences: genre with "no ads" and "no in-app purchases"; what you do; how you play. The deal comes first because the App Store cuts this text off after about three lines. Must not name AI agents, MCP or any other platform, and must not say "free". English uses 147. |
| `desktop_short_pitch` | 270 | Microsoft Store short description; Steam and GOG (prepared) | Desktop only. The three sentences of `short_pitch` with "free" added, then the optional AI-agent sentence. It must not repeat `headline` word for word: Microsoft shows it directly above the description. English uses 235. |
| `appstream_summary` | 78 | Snap summary; AppStream summary; desktop launcher comment | No final full stop. Snapcraft's schema sets the 78-character maximum. It must not repeat `headline` word for word: Snap shows it directly above the description. English uses 59. |
| `windows_search_term_1` … `_7` | 30 each | Microsoft Store search terms (not shown) | Lower case unless a name. Microsoft's own pages give 30 and 40 characters in different places; 30 is used here. Microsoft also allows at most 21 different words across all seven; English uses 14. No price word ("free") and no other product's name ([Store policy 10.1.3](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)). Term 7 is about the AI agent; keep "MCP". |
| `shot_overlay_<role>` | By script: 20 to 50, Latin 40. Aim for the target, Latin 32. See [overlay caption length by script](#overlay-caption-length-by-script) | Drawn onto screenshots for Google Play, App Store, Amazon, F-Droid and itch.io | 2 to 5 words in English, no final full stop, must make sense alone, one caption per picture. No price word and never "free". `ai_coplay` is used on desktop sets only. English uses 18 to 28; the phone sets are set at 95% (iPhone) and 97% (Android phone) of full size. |
| `shot_caption_<role>` | 100 | Caption field under screenshots: Microsoft Store, AppStream | One plain sentence saying what the picture shows. Names no map. |
| `trailer_title` | 50 | Microsoft Store trailer title; video title elsewhere | |
| `trailer_line_1` … `_4`, `trailer_line_ai_coplay` | 44 | Text on screen in the trailer | Shown one at a time, in order: control, economy, battle, the deal. Each line must make sense alone. The AI line is in desktop cuts only, after line 3. No price word. The limit is the same in every locale: a trailer card is the full width of a 16:9 frame. English uses 20 to 29. |
| `feature_*`, `fair_deal_line` | 200 | Microsoft Store feature list; Amazon bullets; description bullet lists | English is far below the limit. |

### Description blocks

Every description starts with `headline` on line one and `fair_deal_line` on line two. The composed description limits are 4,000 characters on Google Play, F-Droid, the App Store, the Mac App Store and Amazon, 4,096 on Snap and 10,000 on Microsoft and Epic. The exception is Amazon Japanese: the console caps it at 1,200 characters, so `locale_overrides` in the platform matrix composes it without `map_heading`/`map_body` (1,158 characters with the reviewed text; the 23 maps and 67 terrain types remain in the first feature bullet). English uses about 2,400 to 2,800 on the mobile stores and 2,500 to 3,500 on desktop, so a translation may run about 44% longer than English on Google Play, the tightest mobile store, before it hits a limit. Snap is the tightest desktop store (about 24% headroom) and is mapped for English only.

| Fields | Appears on | Notes |
| --- | --- | --- |
| `headline` | Every store, first line | The hook. It must work alone: fewer than 2% of visitors open the full description. Keep the genre term and the colony/unit contrast. |
| `fair_deal_line` | Every store, second line; Microsoft feature 2; Amazon bullet 5 | Five flat statements. Keep them as five short sentences in the same order. "Free" is the price (costs nothing), not freedom. "No premium currency" means there is no currency to buy with real money. |
| `listing_intro` | Every store | Says what globs are. Every later "globs" depends on this sentence, so keep the explanation ("small, busy creatures that work, eat, train and fight"). |
| `control_heading`, `control_body` | Every store | The main mechanic. No claim that it is easy. |
| `economy_*`, `map_*`, `defense_*` | Every store | Building names follow the game's own translation; see the glossary. |
| `features_heading` + bullets `feature_maps`, `_opponents`, `_colonies`, `_tutorial`, `_editor`, `_replays`, `_offline` | Every store | |
| `feature_scripting` | Microsoft, Snap, AppStream, itch.io, Steam, GOG | Not on mobile, Apple or Epic. |
| `feature_languages` | Google Play, F-Droid, Microsoft, Snap, AppStream, itch.io, Steam, GOG | Not on Apple (the App Store shows 6 languages), Amazon or Epic. |
| `feature_control` | Microsoft feature 1; Amazon bullet 1 | Stands alone at the top of a list, so it does not say "globs". |
| `feature_ai_coplay` | Microsoft feature 3 | |
| `multiplayer_heading`, `multiplayer_lan_body` | Every store | `multiplayer_lan_body` sometimes stands alone under the heading and sometimes follows the online sentences. It must read correctly both ways; do not start it with "or" or "also". |
| `multiplayer_online_body`, `multiplayer_crossplay` | Stores whose build can play online: now Google Play, F-Droid, Snap, AppStream, itch.io, Steam, GOG | Never on Amazon. Switched off on Microsoft and Epic until their packages are current. |
| `multiplayer_crossplay_apple` | App Store, Mac App Store | Same fact as `multiplayer_crossplay` without naming a device class. Must not name any platform or store. |
| `ai_heading`, `ai_body` | Microsoft, Snap, AppStream, itch.io, Steam, GOG | Written for the Mac App Store and Epic too, but switched off there until verified. Keep "your own" in the heading, and in the body keep "optional", "off unless you turn it on", "only on your own computer", "does not include one" and "complete without one". The body must not name a device class or another store ("desktop", "Windows"), because it is also written for the Mac App Store. |
| `ai_guide` | Snap, itch.io, GOG | Translate only "Setup guide". Not composed for Microsoft or Steam: Microsoft's listing guidance says not to put URLs in the description, and Steam does not allow store descriptions to link to other websites. |
| `open_source_heading`, `open_source_body` | Every store | Heritage as proof, near the end. |
| `android_tail` | Google Play, F-Droid | |
| `ios_tail` | App Store | |
| `mac_tail` | Mac App Store | |
| `amazon_tail` | Amazon Appstore | The Fire tablet edition has no online play and no accounts. |
| `itch_downloads_note` | itch.io | English page only today. |
| `epic_tail`, `epic_legal` | Epic Games Store | Unchanged. |

### Which locales reach which store

A locale file must hold all 79 fields, but a limit only binds where the locale is mapped to that store in the [platform matrix](platforms.json). The limits on overlay, trailer and caption fields bind in every locale, because the images and video are rendered for all 45: the overlay limit of the locale's script, 44 for a trailer line, 50 for the trailer title and 100 for a caption sentence. `android_title` is also held to 30 in every locale, so the Play title fits wherever a locale is added to Play later.

## Advice for the tight fields

Long-word languages (German, Finnish, Hungarian, Dutch, the Nordic and Slavic languages, Greek, Turkish, Tamil, Telugu, Malay, Filipino) will not fit a literal translation into the tightest fields. Adapt in this order of priority.

**`shot_overlay_<role>` (limit and target by script, [table below](#overlay-caption-length-by-script)).** Say the whole idea in the words players know, and stay within your script's target. The earlier limit of 28 characters in every script forced cuts that are no longer needed, so restore the full wording wherever it fits the target:

- `fair_deal`: the two facts are "no ads" and "no in-app purchases". English writes them as two short sentences, "No ads. No in-app buys", so the line breaks between the two facts; "in-app buys" is only the shorter English for "in-app purchases", chosen because "No ads, no in-app purchases" could break only as "No ads, no / in-app purchases" and set the whole English gallery at 78%. Keep the break between the two facts (two sentences, or a comma). Use the term your app stores use for in-app purchases, or a shorter form that still clearly means purchases inside the game, never a bare "no purchases". A compound such as an "ad-free" adjective is fine. Never drop one of the two facts.
- `maps`: "23 maps, or random ones" says that you play one of the 23 hand-made maps or a randomly generated one. Keep the number 23 and make clear that the random ones are game maps (say "random maps" if "ones" does not carry that in your language); never a bare "generators", and do not add the number 67, "infinite" or "endless". The break falls after the comma.
- `hero`: use the same genre term as your `ios_subtitle`, and keep "colony" where it fits the target.
- `opponents`: keep the number 8 and "computer"; the verb can go (English: "8 computer opponents", without the verb).
- `ai_coplay`: keep "AI agent" and the sense of playing on the same side; never a word that means playing against it.
- `build`: see the note on "they" above.

Articles and "your" can still go, and two strong words still beat five weak ones: a caption is read at thumbnail size. Do not pad a caption because there is room. Do not use all capitals to save space. In right-to-left scripts write the caption normally; the renderer handles direction. One long word that cannot be broken (a German, Dutch or Finnish compound) can fill a whole line and make the type shrink, so check the caption with the renderer as described below.

**`ios_subtitle` (30).** This is a search field first. Keep the genre term your players search for ("RTS" if they use it), then "colony" if it fits. Drop "real-time" before you drop "strategy".

**`play_short_description` (80).** English uses 75, so most languages must cut. Keep, in this order of priority: the genre term, "no ads", the colony-not-units contrast, then "offline". Drop "offline" first; if it still does not fit, shorten the contrast ("command a whole colony"). Never drop "no ads" and never add "free". "Offline" may be the local loanword.

**`ios_keywords` (100 bytes).** Do not translate the English list word for word. Choose the terms players in your language search for, from these concepts only: RTS, base building, offline, no ads, war, army, battle, skirmish, multiplayer, LAN, map editor, economy, tactics. Keep "no ads" in the form players search for. In Cyrillic, Greek or Arabic script expect room for 6 to 8 terms; in CJK, Thai or Indic scripts 4 to 6. Leaving out a concept is fine; adding one not on the list is not. No brand or competitor names.

**`windows_search_term_*` (30 each, 21 different words in all).** One search phrase per field, as players type it. Keep each to as few words as the English.

**`trailer_line_*` (44).** Each line is on screen for about two seconds, so the limit is room for the full wording, not a length to aim for. Keep each line as close to the length of the English as the full wording allows. `trailer_line_1` is the same text as `shot_overlay_build`, `trailer_line_4` the same facts as `shot_overlay_fair_deal` (the trailer card is wide enough for "No ads. No in-app purchases."; the overlay may use the shorter form for in-app purchases), and `trailer_line_ai_coplay` the same text as `shot_overlay_ai_coplay`: use the same wording in both.

**`short_pitch` (170) and `desktop_short_pitch` (270).** English uses 147 and 235, so a language that runs more than about 15% longer must cut. Cut whole sentences, in this order: first "You set the priorities; your colony does the work.", which leaves room for a translation about 75% longer than the English in `short_pitch` and about 45% longer in `desktop_short_pitch`; then shorten "Grow a colony and fight rivals for land." Never cut the opening sentence (genre, no ads, no in-app purchases) or, on desktop, the AI-agent sentence.

## Overlay caption length by script

A caption is drawn in the band above the screenshot, on one line or on two balanced lines. The caption renderer measured on 2026-11-24 how long a caption can be on the narrowest image, the portrait iPhone screenshot ([how long a caption can be](../assets/storefront-v2/tools/README.md#how-long-a-caption-can-be)). Two numbers follow from that for each script, both counted in characters as defined above:

- **Target:** up to this length a caption is normally set at 85% of full type size or more. Write to the target.
- **Limit:** the ceiling, up to which a caption can still be set at 70% of full size or more. `check` and the renderer reject a longer caption. Between target and limit the caption is accepted but may be set visibly smaller than its neighbours, so go there only when the full wording needs it, and check the result with the renderer.

| Script group | Locales | Target | Limit |
| --- | --- | --- | --- |
| Latin | `en`, `pt-BR`, `ca`, `cs`, `de`, `da`, `es`, `eo`, `eu`, `fr`, `hu`, `it`, `nl`, `pl`, `pt-PT`, `ro`, `sl`, `sk`, `fi`, `sv`, `tr`, `id`, `vi`, `sw`, `nb`, `ms`, `fil` | 32 | 40 |
| Cyrillic, Greek | `ru`, `uk`, `bg`, `sr-Cyrl`, `el` | 28 | 36 |
| Chinese | `zh-Hans`, `zh-Hant` | 20 | 24 |
| Japanese | `ja` | 18 | 20 |
| Korean | `ko` | 22 | 32 |
| Devanagari | `hi`, `mr` | 40 | 48 |
| Bengali | `bn` | 36 | 46 |
| Telugu | `te` | 32 | 50 |
| Tamil | `ta` | 24 | 32 |
| Arabic, Persian | `ar`, `fa` | 40 | 48 |
| Urdu | `ur` | 28, on one line | 28 |
| Thai | `th` | 28 with a break point at a phrase boundary; about 20 without | 28 |

The limits are `field_limits` → `shot_overlay_*` → `script_groups` in [platforms.json](platforms.json), which also records each target. All 45 locales are assigned to a group. A locale code that is in no group gets the default limit of 28.

**Thai.** Thai is written without spaces between words, and the renderer never breaks a Thai caption inside a run of letters, because automatic word breaking cuts loanwords and compounds in the wrong place. A caption with no break point is therefore set on one line and shrinks once it is longer than about 20 characters. Where a caption has no natural space, put a zero-width space (U+200B) at each phrase boundary, never inside a word or a name. It is invisible in the catalog and in the image, and it counts as one character. Use it in `shot_overlay_*` fields only.

**Urdu** is set in Nastaliq, which is tall: keep the caption to one line.

**Chinese, Japanese and Korean** captions count every character, including digits, Latin letters and spaces, so "AI" is 2 and "67" is 2.

### Checking legibility with the renderer

The character limit is a coarse filter. Whether a caption reads well is decided by setting it in the real font on every image size, which the renderer's `fit` command does without writing any image:

```sh
cd assets/storefront-v2/tools    # from the marketing repository root
uv run screenshots.py fit --locale <code>
```

`<code>` is one locale, a comma-separated list, or `all` (about three minutes). The fonts must have been downloaded once with `python3 fetch_fonts.py` in that directory; the [renderer's README](../assets/storefront-v2/tools/README.md) has the other options.

What it prints (run on 2026-11-24 against the catalogs of that day):

- One line per store set and a total, when everything fits. For `en`: `apple-iphone-6.9: 1 locale(s) fit` and the same for the other six sets, then `51 captions fit`, exit status 0.
- A list headed `N caption(s) worth a look (no good break at a space, so a fallback was used):` for captions that were set, but not in the preferred way. Each entry gives the store set, locale and role, the caption as set with ` | ` at the line break, the type size used in pixels, and the reason: `one line at reduced size`, or `line break by the 'free' rule` (or `'words'`) when the break was not at a space, a zero-width space or punctuation. For `th`: `apple-iphone-6.9 / th / hero: เกมวางแผนอาณานิคมเรียลไทม์  (90px, one line at reduced size)`. For `ja`: `apple-iphone-6.9 / ja / opponents: 8種類の | コンピューター対戦相手に挑もう  (74px, line break by the 'free' rule)`. The exit status is still 0 if nothing else is wrong.
- A list headed `N caption(s) could not be rendered:` and exit status 1 for a caption that is over its limit, uses a banned word or a character no bundled font has, or cannot be set at the smallest allowed size. For `ja`: `apple-iphone-6.9 / ja / hero: ja/shot_overlay_hero: 21 characters exceeds 20; reviewed adaptation required`.

Reading the pixel figure: full type size is 128 px on `apple-iphone-6.9`, 145 px on `apple-ipad-13`, 90 px on the phone sets of Google Play and F-Droid, 93 px on `google-play-tablet-7` and 124 px on the 10-inch tablet sets, multiplied by 0.90 for Chinese and Japanese, 0.92 for Korean, 0.94 for Tamil, 0.96 for Urdu and 1.04 for Arabic and Persian. So 90 px for the Thai caption above is 70% of full size and 74 px for the Japanese one is 64%: both should be reworded, shortened or given a break point. A flagged caption at full size (Japanese `economy` at 115 px) only needs a look at where the line broke.

`fit` does not print a percentage, and it lists only the two fallback cases. A caption that broke at a space or at punctuation is not listed even when it was shrunk to fit, so a run with no list does not prove that every caption is at 85% or more. Staying within the target is what keeps a caption there. For an exact figure after `render`, each `manifest.json` records `caption.font_size` and `caption.full_size` for every image.

## Per-store switches

Two switches in [platforms.json](platforms.json) decide whether a block is composed for a store. They follow the [claims record](../facts/storefront-v2-claims.md) and are flipped only when that record changes.

| Store | `ai_coplay` | `online_play` | Why |
| --- | --- | --- | --- |
| Google Play, F-Droid | not present | on | MCP is not in the Android build. |
| App Store (iOS) | not present | on | MCP is not in the iOS build. |
| Mac App Store | **off** | on | MCP in the sandboxed store build is unverified (claims R7). The section is written and switched off. |
| Microsoft Store | on | **off** | The Store package on record is 0.11.6.5, which the online service refuses (R6). Turn on when the package is 0.11.7.0 or newer. |
| Epic Games Store | **off** | **off** | The artifact in review is 0.11.4.0: it predates the colony tools (R8) and cannot play online (R6). |
| Amazon Appstore | not present | not present | The Fire tablet edition has no online play at all, so its composition never mentions it. |
| Snap, AppStream, itch.io | on | on | |
| Steam, GOG | on | on | Prepared only; no listing exists. |

With `ai_coplay` on, Microsoft also gets the AI-agent short description, feature 3, search term 7 and screenshot caption 8. Its description carries the AI-agent section without the `ai_guide` link. With it off, the short description falls back to `short_pitch`, feature 3 becomes `feature_tutorial`, and term 7 and caption 8 are not exported.

## Screenshot roles and order

The gallery orders are recorded in `asset_text` in [platforms.json](platforms.json).

| Gallery | Key | Order |
| --- | --- | --- |
| Captioned mobile sets (App Store, Google Play, Amazon, F-Droid) | `mobile_gallery_order` | `hero`, `build`, `fair_deal`, `battle`, `economy`, `territory`, `maps`, `opponents` |
| Clean desktop galleries (Microsoft Store, Steam, Epic, AppStream) | `desktop_gallery_order` | `hero`, `build`, `economy`, `battle`, `territory`, `maps`, `opponents`, `ai_coplay` |

The fair-deal slide is third on mobile because App Store search results show the first three portrait screenshots, so the deal is seen without opening the listing. `fair_deal` is not in desktop galleries and `ai_coplay` is not in mobile ones. A device class with fewer captures keeps the same relative order.

The desktop order is unchanged: `platforms.microsoft.fields.desktop_screenshot_caption_1` … `_8` and the AppStream caption list are numbered in it, and a test holds the three together. If the final clean desktop gallery uses a different order or fewer images, change `desktop_gallery_order` and those entries together before export; a caption must describe the picture it sits under.

The matrix records the mobile order; it does not apply it. The caption renderer takes its slots from `assets/storefront-v2/captures/mobile/selection.json`, or from `provisional_gallery` in its `gallery.json` until that file exists, so those lists must be written in this order.

`shot_caption_fair_deal` is supplied for a store that shows a caption beside a captioned image. No store composes it today.

## Epic About items

Epic's About section is entered as heading-and-body items. The composed `epic.description` in the matrix shows the order. The intended items are:

| Item | Heading | Body |
| --- | --- | --- |
| 1 | `headline` | `fair_deal_line`, then `listing_intro` |
| 2 | `control_heading` | `control_body` |
| 3 | `economy_heading` | `economy_body` |
| 4 | `map_heading` | `map_body` |
| 5 | `defense_heading` | `defense_body` |
| 6 | `features_heading` | the seven shared bullets, as a Markdown list |
| 7 | `multiplayer_heading` | `multiplayer_lan_body` (plus the online sentences when `online_play` is on) |
| 8, when `ai_coplay` is on | `ai_heading` | `ai_body` |
| last | `open_source_heading` | `open_source_body`, then `epic_tail` |

`tools/epic_template.py` still maps the five-item storefront-v1 layout and the removed `listing_open_source` field. It must be updated to this layout before an Epic import. Until then it stops instead of writing a mixed listing, because the saved English no longer matches the canonical fields and `listing_open_source` no longer exists.
