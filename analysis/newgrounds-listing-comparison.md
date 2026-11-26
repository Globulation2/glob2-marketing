# Newgrounds listing comparison

Observed 2026-11-26 from Newgrounds' public pages, read signed-out with `curl`: the games browser (`/games/browse?genre=66&sort=score&interval=all`, `…&interval=year`, `…genre=66&sort=views&interval=all`, `…genre=0&sort=score&interval=year`), the `/games` front page and each sampled game page (`/portal/view/<id>`). Genre 66 is "Strategy - Real-time (RTS)". Rules were read on the Newgrounds wiki pages [games and movies](https://www.newgrounds.com/wiki/help-information/content-submission/games-and-movies) and [tagging](https://www.newgrounds.com/wiki/help-information/content-submission/tagging). Our listing is recorded in the [web portal rollout](../planning/web-portal-rollout.md#newgrounds) (draft project 8315233, not published).

Sample, 25 games:

- **All-time RTS, top 10 by score:** Mastermind: World Conqueror, Age of War, House of Wolves, Stick War, Stick War 2, Age of War 2, The Killbots of C Station, Miragine War, JellyGo, Warfare 1944. All 2007–2014, all Flash.
- **RTS of the past year, top 10 by score:** Millennium Conflict, Quiet Bruise, Derpy Doobis Wars, PaxNeo, CONQUEST, R-Peak-G, Battle Pillars, Galaxy Conquest Online Demo, Chill Ants, Dirifin.
- **All genres, past year, top 5 by score:** NG's 30th Anniversary Collab, Find Matt's Cats Demo, Elden Ring - Revenant Run, Nosey's Tower Climb, Riddle School - Retakes.

## What the top games do

| Feature | All-time RTS top 10 | Past-year RTS top 10 | Past-year all genres top 5 | Globulation 2 draft |
|---|---|---|---|---|
| Frontpaged | 8 of 10 | 1 of 10 (Millennium Conflict) | 5 of 5 | not published |
| Median views | about 570,000 | 261 | 36,018 | n/a |
| Median score (of 5) | 4.65 | 3.02 | 4.66 | n/a |
| Short description, median length | 78 characters | 43 | 66 | 64 (storefront headline) |
| Author comments, median words | 68 | 177 | 115 | longer storefront-v2 copy |
| Tags, median | 4 | 0 (7 of 10 had none) | about 6 | 8 |
| Medals | none seen | none seen | 5 of 5 | none (no Newgrounds.io integration) |
| High-score boards | none seen | none seen | 3 of 5 | none |
| Daily/Weekly/Monthly award or Users' Choice | 8 of 10 | 0 of 10 | 5 of 5 | n/a |

Short descriptions in the meta tags are cut at about 90 characters (Millennium Conflict's stops mid-sentence at 89). The all-time leaders use concrete, verb-first lines: "Take control of 16 different units and 15 different turrets to defend your base" (Age of War); "Manage your minions, defend your base, and conquer this puny planet" (Mastermind).

Ratings (from the page's rating class, which may not be exact): about half of the RTS sample is rated T and half E. Millennium Conflict, the one RTS with real traffic this year, is "Suitable For All Audiences".

The one past-year RTS that broke out, Millennium Conflict (14,203 views, frontpaged two days after upload), has a 15-word short description ("You are the last survivor. Capture towers, command a squad of unique generals…"), 226 words of author comments with a "Features:" bullet list, seven tags and no medals. Its top review complains that it is a demo and the description does not say so, and another says the tutorial is too short.

## How Newgrounds discovery works

Observed:

- **Judgment.** Per the wiki, a new submission appears at once, then goes through a judgment phase in which users vote. If it "doesn't reach a sufficient score by the end of judgment", it is "blammed, aka deleted". The threshold and duration are not published.
- **Frontpage and awards.** Every highly viewed game in the sample was frontpaged and most collected a Daily/Weekly/Monthly placing. How games are chosen for the front page is not documented; secondhand forum accounts say staff pick from well-voted games. Treat it as unverified.
- **Tags.** The wiki says games have "up to four tags", hyphenated for multi-word phrases. Live pages in the sample carry up to 11, and our draft saved 8, so the wiki page appears out of date.
- **Genre field.** "Strategy - Real-time (RTS)" is its own browse genre (option value 66). Our draft uses it.
- **Limits.** Two submissions per day. No default file-size limit is stated; a raise can be requested.
- **Medals and scoreboards** come from the Newgrounds.io API and show as a "Medals" / "High Scores" panel beside the game. Every top game overall this year had medals; no RTS in the sample did.
- **Viewport.** Game pages carry both `<meta name="viewport" content="width=960">` and `width=device-width`. This matters for our phone layout (see the rollout's note on host-page viewports): which tag a phone browser honours has not been tested.

## Inferences (not validated)

- **The RTS genre is weak on Newgrounds today.** The past year's best-scored RTS games average about 3 out of 5 with a few hundred views. The audience rewards short, polished, character-led games. Glob2 is a deep, slow-start RTS, so the judgment phase is a real risk: early voters who meet a long load and a menu may vote low.
- **The first minutes and the description decide judgment.** The breakout RTS was praised for its idea and marked down for a thin tutorial and for not saying it was a demo. Saying plainly what the game is and pointing at the tutorial should help.
- **Medals are the most visible gap against top games**, but adding them is a game change (a Newgrounds.io integration), not a listing change.
- **Tag count barely matters.** Most past-year RTS games had no tags and the classics have about four. Our eight are fine as long as they are accurate.

## Limits

One day's snapshot of one sort order per list. Score-sorted lists are biased towards games with enough votes to rank. Medal and rating detection was done by parsing page markup and may miss edge cases. What made the classics successful (the Flash-portal era, sponsorship, sequels) cannot be copied through listing fields.

## Action list for our listing

Ranked by expected impact against effort. None of this has been applied: the draft stays unpublished until the user says go.

| # | Change | Evidence | Effort |
|---|---|---|---|
| 1 | **Rewrite the short description as a concrete, verb-first line of up to 90 characters**, for example: "Grow a colony and fight rivals for land: you set the priorities, your globs do the work." (88 characters, built only from approved claims). | All-time leaders use concrete action lines of about 78 characters; the meta tag cuts at about 90. The current headline is accurate but abstract. | Low |
| 2 | **Open the author comments with what the game is and how to start**: one line saying it is the full game, free, not a demo (avoid "complete": the public site still calls the browser build early access, and the Game Jolt stage is Early Access), then "Start with the 10-lesson Tutorial". Keep a short "Features" bullet list from the approved feature lines. Cut the body to about 150–250 words. | The breakout RTS was marked down for an unclear demo status and a thin tutorial; past-year RTS comments run about 177 words. | Low |
| 3 | **Before publishing, test the published page on a phone-sized screen**, because of the two viewport tags. If the desktop layout shows, untick "touchscreen friendly" rather than advertise a poor phone experience. | Newgrounds pages carry both `width=960` and `width=device-width`; our phone layout depends on the host page's viewport. | Low |
| 4 | **Keep the claims inside the rules.** Commentary may mention online rooms with invite codes, but not quick matches or busy online play (the online service is nearly empty). Scope "No ads" to the game: Newgrounds shows its own site ads. | [Storefront claims](../facts/storefront-claims.md) R12 and the ads note. | Low |
| 5 | **Publish when someone can answer the first reviews.** Judgment happens in the first days; replies to the first comments are visible to the voters who follow. | Judgment and blam rule (wiki). Inference, not measured. | Medium (ongoing) |
| 6 | **Consider Newgrounds medals** for milestones the game already tracks (tutorial lessons finished, first win against each AI level). | 5 of 5 top games this year have medals; no RTS does, so it would also stand out in the genre. | High (game-repository change) |
| 7 | **Tags: keep eight, all hyphenated and accurate**: strategy, rts, colony, base-building, economy, multiplayer, open-source, map-editor. Optionally swap `multiplayer` for `real-time-strategy`, since online play is thin. | The wiki's four-tag limit is not enforced on live pages; tags carry little weight in the sample. | Low |

**Decisions for the user**

- **Content rating:** the draft says T, with violence "Some". Game Jolt says All Ages and the Microsoft Store says ESRB E / PEGI 3. Newgrounds' art guidelines put "mild cartoon violence" under T, and the RTS sample is split between E and T. T is the safe, honest choice. E would widen the audience but could be re-rated by moderators.
- **Standard or lite build:** the standard build (126 MB zip, about 22 MB before the game starts) keeps the editor, online rooms and 45 languages. The lite build (17.7 MB zip, about 8 MB startup) loads faster during judgment but drops those features, so the listing copy would have to drop them too. The recommendation is to keep standard, because it matches the Game Jolt listing and Newgrounds sets no size limit, and to revisit if early comments complain about loading.
- **Cross-origin isolation:** Newgrounds offers a "Uses SharedArrayBuffer/Cross Origin Isolation" switch that would let the threaded runtime run. It is untested there and the serial runtime is verified, so leave it off for launch. Test it later on an unpublished project.
- **Allow Embedding:** off in the draft. Turning it on lets other sites embed the game from Newgrounds. That widens reach but puts the game next to ads we don't control.
