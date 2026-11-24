# Storefront translation terminology

[Translation contract](README.md) · [English master](en.md)

Version: `storefront-v1`. These meaning constraints apply across all locales; locale drafts establish natural equivalents and independent review checks consistency. Existing native game strings and platform locale catalogs are terminology references, not automatic approval of a storefront translation.

| English concept | Meaning to preserve |
| --- | --- |
| Globulation 2 | Fixed product/brand name; do not transliterate or redesign the wordmark. |
| colony | Player's living settlement/economy; keep consistent across headings, body and short text. |
| workers / workforce | Creatures allocated among food, construction and training; do not imply individually direct-controlled units. |
| autonomous creatures | Units act on colony priorities; this is game behavior, not a claim about generative AI. |
| economy | Food, work and resource allocation supporting growth and defense. |
| sprawling base | Expanding settlement footprint; avoid implying a specific building or endless world. |
| contested territory | Rival pressure for land and resources; do not imply a particular ranked or online mode. |
| strategy / real-time strategy / RTS | Genre meaning; use natural local genre wording and conventional acronym where appropriate. |
| expansion / growth | Colony development; avoid implying an expansion pack or paid downloadable content. |
| map / terrain / routes | Playfield, its geography and ways across it; map strategy is distinct from map editing. |
| food / resources | Keep food specific when named; do not invent currencies or resource types. |
| training | Workforce demand for preparing units; do not introduce unsupported training mechanics. |
| defense / rivals / conflict | Preserve competitive pressure; do not escalate into invented combat systems. |
| free and open source | Price and source availability are distinct; preserve both without new licensing promises. |
| single-player / offline / account | Preserve each edition's exact qualification; do not extend it to every mode. |
| touch controls | iPhone/iPad/Android qualification only where sourced. |
| River / Four Squares / Lava Shield | Named maps/terrain in approved captures; keep proper names unchanged unless an authoritative localized game name is verified. |
| iPhone / iPad / Android | Preserve platform trademarks. |
| skirmish / empire / map editor | Existing Apple keyword concepts only; keywords do not authorize adding new descriptive claims. |

Arabic, Persian and Urdu require appropriate right-to-left shaping and direction. Serbian uses Cyrillic. Portuguese Brazil/Portugal and Chinese Simplified/Traditional are separate canonical variants. Keep URLs, product name and proper names exact; do not mirror gameplay or the wordmark for RTL layouts.

## Storefront-v2 additions — 2026-11-24

These rows extend the table above for the `storefront-v2` source. Where a row here and a row above disagree, this section applies to v2 fields. The v1 rows for *River / Four Squares / Lava Shield* and for the old Apple keyword concepts have no v2 field: v2 captions name no map, and [the field map](storefront-v2-field-map.md) covers keywords. Limits, placement and tone for every field are in the field map; what may be claimed on which store is in [storefront v2 claims](../facts/storefront-v2-claims.md).

| English concept | Meaning to preserve |
| --- | --- |
| globs | The game's own name for its creatures (workers, explorers and warriors alike). Treat it as a name: keep it, or transliterate it the same way everywhere in the locale. Do not translate it as "blobs", "slimes", "insects" or "units". In v2 it replaces v1's "autonomous creatures". It is used only in the description body, after `listing_intro` explains it. Fields that stand alone (short fields, feature bullets, captions, trailer lines) say "your colony", "workers" or "warriors"; do not add "globs" to them. |
| command the colony, not every unit | The central idea: the player decides what gets built and how many globs work on it; nobody selects or steers single globs. Keep the contrast between the colony and the single unit. Do not turn it into a claim that the game is easy or plays itself. |
| real-time strategy / RTS | The genre. Use the term players in your language type into a store search; keep "RTS" as the Latin acronym where players use it. `shot_overlay_hero`, `ios_subtitle`, `headline` and `play_short_description` should use the same genre term. |
| base building | A search term for the genre habit of building up a settlement. Use the local store term; it is not a promise of a specific mode. |
| free | Costs nothing to get and play. Not "free-to-play" as a business-model label, and not "freedom" (open source is stated separately). The word must not appear in `play_short_description`, `ios_subtitle`, `ios_keywords`, `short_pitch`, `windows_search_term_*`, any `shot_overlay_*` or any `trailer_line_*`, even where it would fit: those places are covered by store rules on price wording. |
| no ads / ad-free | The game shows no advertising. Do not widen it to "no tracking", "no analytics" or "no data collected". It is the one deal fact that also appears in `play_short_description` and `ios_keywords`; never drop it from them. |
| in-app purchases | Use the exact term your language's App Store and Google Play use for in-app purchases. "No in-app purchases" is a statement about the game; never widen it to "nothing is sold", "nothing to buy anywhere", "never" or "forever". |
| loot boxes | Paid random-reward boxes. Use the term players and regulators use in your language (often the English loanword). |
| premium currency | Currency bought with real money (gems, coins, credits). "No premium currency" means there is none to buy. It must not read as "the game has no resources": wheat, wood and stone are gathered in play. Use the wording players use for paid currency; if the literal term is unclear, say "no currency to buy". Use one wording in `fair_deal_line` and `shot_caption_fair_deal`. Recorded as safe wording in [storefront v2 claims](../facts/storefront-v2-claims.md#verdict-on-the-five-claims). |
| computer opponent | One of the game's 8 built-in rivals, or the opponent a player gets in an online quick match when no other player is waiting. Always "computer opponent" (or the local equivalent of "CPU player"/"bot"); never "AI agent", and avoid a bare "AI" for it. |
| AI agent / your own AI agent | An AI assistant program the player already has and connects to the desktop game. It is not part of the game, not sold by the game and not needed to play. Keep "your own". Never the same word as "computer opponent". Nothing in the copy says game content is AI-generated; do not introduce that reading. |
| MCP server / MCP | Keep "MCP" untranslated in Latin letters in every locale. "Server" may be translated. Do not expand or explain the abbreviation: readers who have an AI agent know it, and the sentence around it says what it does. |
| optional / off unless you turn it on | The AI-agent feature is opt-in. Keep the word "optional" wherever the English has it (`desktop_short_pitch`, `feature_ai_coplay`, `ai_body`) and keep the off-by-default statement in `ai_body`. The heading, overlay and trailer line sell the feature and do not carry the word; the body always follows the heading. |
| ranked / casual | The two online 1v1 queues: ranked changes a rating and needs sign-in; casual does not. Use the usual competitive-gaming terms. |
| quick match | Automatic pairing with one opponent. No word that promises speed or a waiting opponent. |
| room / invite code | A private online lobby the host opens; friends join with a short code. Not a chat room. |
| guest / sign in | Online play can start as a guest; ranked needs a signed-in account. Do not shorten this to "no account" for online play. |
| local network play | Play between devices on the same local network (LAN), without the online service. |
| handmade maps / random landscapes / random maps | "Maps" are the 23 fixed maps made by people. "Landscapes" are the 67 kinds of randomly generated map; the game's own menus call them landscapes, so use the word from the game's translation for your language (key `[Landscape]`) where it has one. `shot_overlay_maps` ("23 maps, or random ones") no longer carries the 67: it names the 23 maps and says the others are randomly generated, without a count or the word "generators". Keep two different nouns so the two numbers do not look like one list; never "infinite" or "endless", and never "67 random maps" (each landscape makes any number of maps). |
| portrait or landscape | How the phone or tablet is held (`android_tail`, `ios_tail`). Not the game's "landscapes"; use your language's usual words for screen orientation. |
| colonies (in one match) | "Up to 16 colonies" counts sides on a map, human or computer. Not "16 players online". |
| tutorial / lesson | A guided tutorial of 10 lessons. Not a story mode; the word "campaign" must not appear anywhere in v2. |
| replays | Saved recordings of a finished game that can be watched again. |
| inn, swarm, school, racetrack, swimming pool, barracks, hospital, defense tower, stone wall, war flag | Names of things in the game. Use the name from the game's own translation for your language where it has one (`content/data/texts.<language>.txt` in the game repository, keys such as `[inn]`, `[swarm]`, `[defencetower]`, `[warflag]`), so the listing matches what the player sees. |
| open source / GPL | The source code is public under the GNU GPL, version 3. Keep "GPL" in Latin letters. Do not add licence promises beyond "read it, change it, help shape the game". |
| started in 2001 / released to the public in 2004 / volunteers over two decades | Fixed facts: work began in 2001 and the public could first download the game in 2004. Keep both years as digits and do not merge them into "25 years of development" or imply unbroken development. No counts of people. Do not use a word meaning "first" anywhere in v2 copy. |
| touch layouts | The phone and tablet interface arrangements. No claim that the game suits every phone. |
| Apple silicon / Fire tablet / itch.io | Platform names; keep as the platform writes them in your language. |

Numbers in the source (23, 67, 8, 16, 10, 45, 2001, 2004, version 3, 1v1) are verified facts: copy them exactly, as digits. Local numeral systems are accepted by the checker.
