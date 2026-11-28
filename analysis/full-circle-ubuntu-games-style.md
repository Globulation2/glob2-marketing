[Analysis index](README.md)

# Full Circle Magazine "Ubuntu Games": house style and contributor rules

Observed: 2026-11-27. Purpose: let a maintainer write a Globulation 2 article that fits Full Circle Magazine's (FCM) "Ubuntu Games" section and its submission rules. This record describes what the magazine publishes; it does not decide whether or when to submit. Editor contact addresses are printed in every issue and are deliberately left out here.

## Sources

- FCM home page and issue pages: <https://fullcirclemagazine.org/>, for example <https://fullcirclemagazine.org/magazines/issue-235/>.
- English issue PDFs #222 to #235 (October 2025 to November 2026), at `https://dl.fullcirclemagazine.org/issue<N>_en.pdf`, for example <https://dl.fullcirclemagazine.org/issue235_en.pdf>. Text was extracted with pypdf. The Ubuntu Games pages were rendered to images and checked by eye for #225 and #230 to #235.
- The in-issue "Write For Full Circle Magazine" page (by the editor, Ronnie Tucker). It appears in every issue checked, for example #230 p.47 and #235.
- The Official Full Circle Style Guide, which the in-issue page links as <http://bit.ly/fcmwriting>. That link redirects to a Google Doc: <https://docs.google.com/document/d/1nCy0yD7DBPvMdDzMRGLaKyvRlUyS7bLwjyRmqYPh270/edit>.
- No standalone "write for us" or "contribute" page exists on the site. `/about/`, `/contribute/` and `/write-for-us/` all returned 404 on 2026-11-27. Nothing relevant was found at `wiki.ubuntu.com/UbuntuMagazine` either.

## Per-article record

Every article in the sample is "Written by Erik", the section's regular columnist. Word counts are pypdf token counts of the section pages, minus the running headers. They include the quoted publisher blurb (about 60 to 110 words), URLs and the bio box (about 40 words), so the body prose runs roughly 100 to 150 words shorter than the figure shown. Screenshots were counted only on the issues rendered and checked by eye.

| Issue (month) | Game | Words | Pages | Section headings seen | Score or verdict | Screenshots | Notes |
|---|---|---|---|---|---|---|---|
| #222 (Oct 2025) | Shardlight Special Edition | ~1,255 | 3 (pp.63–65) | Installation, Gameplay, Graphics, Sound | Prose only | not checked | GOG; aside about why the author prefers DRM-free GOG |
| #223 (Nov 2025) | Book of Hours DLC (House of Light) | ~1,590 | 4 (pp.48–51) | Installation, Graphics, Sound, Gameplay, Requirements, Conclusion | Prose only | not checked | Pasted system-requirements list |
| #224 (Dec 2025) | Sandwalkers | ~1,199 | 3 (pp.50–52) | Installation, Graphics, Sound, Gameplay, Conclusion | "four out of ten", in prose | not checked | Negative review, stated plainly |
| #225 (Jan 2026) | Endless Sky (free, open source) | ~1,229 | 3 (pp.56–58) | Installation:, Graphics:, Story:, Gameplay:, Conclusion: | Prose ("Go grab it, it's free") | 3, no captions | Closest analogue to Glob2: free and open source; AppImage, also on Steam; links to the wiki, plugins and mod sites |
| #226 (Feb 2026) | #DRIVE Rally | ~1,250 | 3 (pp.53–55) | Installation, Graphics, Gameplay, Conclusion | Prose (advises waiting for a native port) | not checked | Criticises the Unity build for "calling home" |
| #227 (Mar 2026) | The Wandering Village | ~1,192 | 3 (pp.63–65) | Installation, Sounds and Music, Graphics, Gameplay | Prose | not checked | Closes with the test hardware (i5 laptop, 16 GB) |
| #228 (Apr 2026) | Horticular | ~1,184 | 3 (pp.49–51) | Installation, Sound and Music, Graphics, Gameplay | "6/10" for sound and graphics, "9/10" for gameplay, in prose | not checked | |
| #229 (May 2026) | Primal Planet | ~1,099 | 3 (pp.55–57) | Installation | Prose ("good" but not "great") | not checked | The game "came to us via a Godot showcase" |
| #230 (Jun 2026) | Dotage DLC (Folkways) | ~1,254 | 3 (pp.61–63) | Installation:, Gameplay:, Graphics:, Sound: | Prose | 4, no captions | Reports CPU and memory use; lists DLC features as label-and-dash paragraphs |
| #231 (Jul 2026) | False Alarm (demo) | ~1,100 | 3 (pp.52–54) | None; continuous prose | Prose (try the demo) | 4 (3 game, 1 retro box art), no captions | Calls itself a spotlight on an indie game that supports Linux from day one, not a review; made in Godot |
| #232 (Aug 2026) | Tormentum II | ~1,512 | 3 (pp.50–52) | Graphics, Installation, Sounds, Gameplay, Story, Final thoughts | Prose | 5 (incl. the studio's store page and an OpenSnitch connection prompt), no captions | Two boxed "EDIT" notes on release price and a developer-supplied key, with "this review is not sponsored" |
| #233 (Sep 2026) | Pathogenic | ~1,018 | 2 (pp.45–46) | None | Prose ("go get yourself a copy") | 2 (art-book pages), no captions | |
| #234 (Oct 2026) | Warhammer 40,000: Mechanicus | ~1,349 | 3 (pp.53–55) | MINIMUM / RECOMMENDED specs; "Is the game worth your time and money?" | Prose verdict under a question heading | 4, no captions | Retrospective pegged to a sale price; YouTube links for the soundtrack |
| #235 (Nov 2026) | Anvira: Forge Defense | ~1,164 | 3 (pp.47–49) | Installation:, Sound., Graphics., Gameplay. | Prose verdict ("Is the game worth your time?") | 4, no captions | The developers contacted FCM about a Linux release; "our reviews are our own" disclaimer; ends with a reader-feedback line |

## Synthesis

- **Length.** Total section text runs from about 1,000 to 1,600 words, typically about 1,100 to 1,350. That makes the body prose about 950 to 1,250 words. Articles fill three pages in 12 of the 14 issues, two pages in one (#233) and four pages in one (#223). The magazine states no word limit (see below), so this is the observed norm, not a rule.
- **Fixed opening block.** The banner reads "UBUNTU GAMES / Written by <name>", with the game title on the right. Below it come `Website:` (URL), `Price:` (with the store, for example "$9.99 USD (GOG)", "Free!" or "TBA"), and `Blurb:`, the publisher's own store description in quotation marks, set in italics by the layout. The prose starts with a drop cap.
- **Body structure.** A chatty hook (how the game reached the writer, a sale, nostalgia, a comparable older game), then short labelled sections, usually Installation, Graphics, Sound (or "Sound and Music"), Gameplay, sometimes Story, and then a Conclusion, "Final thoughts" or "Is the game worth your time (and money)?". Heading style varies from issue to issue (with or without a colon or full stop). The order is not fixed, and some articles use no headings at all (#231, #233).
- **Verdict.** There is no pros/cons box, star rating or score panel. Verdicts are written as prose, sometimes with an informal number in the text ("four out of ten", "6/10 ... 9/10"). In practice the section does not follow the in-issue review checklist's "marks out of five" item.
- **Tone and person.** Informal, conversational and opinionated, in the first person singular ("I") mixed with an editorial "we" ("we tested", "came to us"). Plenty of parenthetical asides, humour, emoticons ("shrug", ":)") and Linux-community values: praise for DRM-free builds, native Linux ports and modest hardware use, and suspicion of telemetry. It speaks to the reader as "you". Criticism is direct. Free, demo and cheap games get "go grab it" endings.
- **Linux specifics.** Every article states the Ubuntu or Mint version tested (often 24.04), the source (GOG, Steam, AppImage, itch.io), whether the build is native or runs through Wine/Proton, and often fan noise, CPU and memory use, or the test laptop.
- **Screenshots.** Usually four per article, ranging from two to five. The layout places them about one per page, full column width, at the bottom of a page or spanning it. **None has a caption.** In #232 one image carries in-game text, but that is part of the image. Images are mainly in-game scenes, sometimes a menu or a non-gameplay image (box art, a store page, a firewall prompt) when the text refers to it ("see first screenshot").
- **Install commands.** None of the 14 articles shows a terminal command or code block. Installation is one or two sentences of prose ("installed from Steam without a hitch", "an AppImage ... requires no installation"). The style guide does define a code/command convention (a separate paragraph in a monospaced font) for other sections, so a short command would be allowed, but it is not the games section's norm.
- **Byline and bio.** "Written by <name>" sits in the section banner. At the end comes a small bio box with an icon: two or three sentences in the third person, starting with the author's bolded name. The same bio repeats every month. There is no headshot and no author contact line, though #235 adds a reader-feedback address after the verdict.
- **Disclosure.** When a developer provided a key or made contact, the article says so and adds an independence note: "this review is not sponsored" (#232) and "our reviews are our own" (#235). The text shows FCM accepts games that developers pitch to it (#229, #235). #235 also carries a how-to "from the dev" of the tool it covers (Piburn), so the magazine prints developer-written pieces, at least outside the games section.
- **Open-source precedent.** Endless Sky (#225) is the nearest match to Glob2: free, open source and community-driven. It has the standard opening block, AppImage and Steam install notes, links to the wiki and mods, and a "Go grab it, it's free" conclusion.

## Contributor guidelines

From the in-issue "Write For Full Circle Magazine" page (checked in #230 and #235; the text is unchanged):

- The single rule is that the article must somehow be linked to Ubuntu or a derivative (Kubuntu, Xubuntu, Lubuntu and so on).
- "There is no word limit for articles". Long articles may be split across several issues.
- Any software can be used, with LibreOffice recommended. Spell-check and grammar-check the text.
- Mark where each image should go by putting the image file name in a new paragraph, or embed the images in the ODT.
- Images: "JPG, no wider than 1200 pixels, and use low compression."
- "Do not use tables or any type of bold or italic formatting."
- Game and application reviews should clearly state: the title, who makes it, free or paid, where to get it (a download or homepage URL), whether it is Linux-native or run through Wine, "your marks out of five", and a summary with positive and negative points.
- Submit by email to the articles address printed on that page. It is not reproduced here.
- The page closes by saying you don't need to be an expert, and invites writing about the games, apps and hardware you use every day.

From the Official Full Circle Style Guide (linked from the in-issue page):

- Articles must relate to *buntu (Ubuntu, its flavours, Mint or other derivatives). They must be written in American English, as an OpenOffice/LibreOffice ODT file or a Google Docs link, and emailed to the articles address.
- Do not create a layout or use tables in the ODT. The layout is done in Scribus.
- Images: JPG, no wider than 800 pixels. This conflicts with the 1200-pixel limit printed in current issues; see Uncertainty.
- Code and commands go in their own paragraph, in a monospaced font such as Consolas or Courier New.
- The guide follows AP style: numbers zero to nine spelled out, no serial (Oxford) comma, and dates such as 26 Aug., 2012 or 2012/08/26.

Deadlines and demand, from the masthead and editorial of #235:

- FCM#236: deadline **Sunday 6 December 2026**, release Friday 25 December 2026. Over the sampled year, deadlines fell on a Sunday in the first half of the month, with release on the Friday about 19 days later.
- The editorials and the #235 issue page say articles are badly needed ("URGENT NOTICE: we are REEEEEALLY low on all articles"). The #234 and #235 editorials say a third HowTo is still missing.

Licensing: the issue credits page says articles are released under Creative Commons Attribution-Share Alike 3.0 Unported, so a submitted article and its images would be published under CC BY-SA 3.0.

## AI policy

**No FCM policy on AI-assisted or AI-generated writing was found**: not in the in-issue guidelines, the style guide, the editorials or the site. The issues mention AI only in news items about other projects' policies, for example GNOME Shell's ban on AI-generated extensions (#224) and Gentoo/NetBSD-style debates (#232, #234). Those are not FCM rules. The #226 and #228 game articles mention that the author tried ChatGPT for a fact lookup, without any disclosure policy attached. If AI help were used, it would be safest to ask the editor or disclose it, since there is no stated policy either way.

## Uncertainty

- The sample has only one author. All 14 articles are Erik's column, so the "house style" partly reflects his personal voice. Nothing in the sample shows how FCM handles an outside games submission, or whether it would run one in "Ubuntu Games" or as a "Review".
- Screenshots were counted for 7 of the 14 articles (#225 and #230 to #235). The other seven were not checked by eye.
- Word counts are approximate. Text extraction duplicates or garbles some display headings, and the counts include blurbs, URLs and bios.
- The image width limit conflicts (1200 px in the issues, 800 px in the style guide). The in-issue figure is more recent in placement, but which one applies is unconfirmed.
- The style guide is a shared Google Doc of uncertain date. Its editor credits suggest it is older than the in-issue page.
- The in-issue review checklist asks for marks out of five and a positives/negatives summary, but the games section does not follow this in practice. Which one an editor would expect from a newcomer is unknown.
- How long a submission waits before it is published is not stated. #225 says it might miss an already-set issue, which suggests one or two months.
- Developer-written content is accepted elsewhere (the #235 Piburn piece). Whether a project-written article about its own game is acceptable in "Ubuntu Games", and what disclosure FCM would want, is not stated.
