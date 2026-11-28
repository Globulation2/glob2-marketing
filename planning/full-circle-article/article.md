# Full Circle Magazine article draft: Globulation 2

[Planning index](../README.md) · [Shot list](shots.md) · [FCM house style](../../analysis/full-circle-ubuntu-games-style.md) · [Press outreach ledger](../mobile-press-outreach.md)

> **Editor's note — not for submission. Delete this block before sending.**
>
> - **Status:** first draft, 2026-11-27, for the user's review. Nothing has been sent to Full Circle.
> - **Facts checked on 2026-11-27:** Snap stable is 0.11.8.1, amd64 only (snapcraft API). The latest GitHub release is v0.11.8.1, published 2026-11-25. Its Linux downloads are a Flatpak bundle (`glob2.flatpak`, needs the GNOME 51 runtime), a Snap file, an Ubuntu 22.04 tarball with `INSTALL.txt`, and a Fedora 43 RPM. There is no Flathub listing (Flathub API returned 404) and no AppImage. Gameplay facts, menu labels and numbers come from the game source (`glob2` repository, `content/data/texts.en.txt`, building and unit JSON) and have not yet been checked by playing 0.11.8.1 on Ubuntu.
> - **Blurb:** quoted from the live Snap Store description as of 2026-11-27 (the storefront-v1 text). If the Snap listing is updated to storefront-v2 before submission, quote the new live text instead.
> - **Placeholders to fill:** the Ubuntu version tested, and the bio.
> - **Submission format (FCM rules):** ODT or a Google Docs link; American English; no tables, no bold or italic, no layout. Put each image file name in its own paragraph where the image goes. Images as JPG with low compression, no wider than 800 px (meets both the style guide's 800 px and the issue's 1,200 px limits). Commands go in their own paragraph in a monospaced font. Published under CC BY-SA 3.0.
> - **Deadline:** FCM #236 closes Sunday 6 December 2026 (release 25 December 2026).
> - **Open:** whether FCM wants a disclosure about AI assistance in drafting (FCM states no policy), and whether this runs in Ubuntu Games or elsewhere. Headings below follow the section's usual style; the Markdown heading marks and the list of tutorial lessons should become plain paragraphs in the ODT.

---

UBUNTU GAMES — Written by Bradley Arsenault

Globulation 2

Website: https://glob2.online/

Price: Free!

Blurb: "Build a thriving colony in contested territory. Globulation 2 is a real-time strategy game where food, workers and space shape your expansion. Grow a sprawling colony, balance its competing needs, and contend with rivals for land and resources. Your creatures act autonomously, letting you guide the colony as a whole."

A word up front: I help maintain Globulation 2, so this is not a review. It is a walkthrough, and I will try to stick to what the game does rather than tell you how great it is.

Globulation 2 is a real-time strategy game with a twist, built by volunteers since 2001 and public since 2004. You never click a unit and tell it where to go. Your globs (small, busy creatures) decide that for themselves. What you control is demand: you place buildings, say how many workers each one should have and drop flags where you want explorers or warriors to go. The colony works out the rest. It is free software under the GPL (version 3), and has no ads, no in-app purchases and no loot boxes.

[Image: glob2-01-colony-under-raid.jpg]

### Installation

The easiest route on Ubuntu is the Snap. Open a terminal and run:

`sudo snap install globulation2`

If you would rather not use Snap, you have options. Every release on GitHub (github.com/Globulation2/glob2/releases/latest) carries a Flatpak bundle, an Ubuntu 22.04 tarball and a Fedora RPM, alongside Windows, macOS and Android builds. The Flatpak is not on Flathub yet, so it is a bundle you download and install yourself. You need Flathub added as a remote, because the bundle pulls in the GNOME 51 runtime from there. In the folder you downloaded it to, run:

`flatpak install --user ./glob2.flatpak`

and then start it with:

`flatpak run --user org.globulation2.Globulation2`

The bundle does not update itself, so you repeat that step when a new version comes out. The tarball has an INSTALL.txt listing the commands to copy it into place and the system libraries it expects. All the Linux builds are for 64-bit Intel and AMD machines only for now. There is no AppImage. I tested version 0.11.8.1 on [Ubuntu version tested: confirm].

### The tutorial

The first time you start the game, it offers an Introduction. Take it. It takes about 10 minutes, you can save and come back through Load game, and it walks you through the whole idea in five small goals: scout a stone landmark with an Exploration Flag, build another Inn, supply that Inn with wheat, grow your workforce at the Swarm, and finally destroy the enemy Swarm with a War Flag. Each goal has a "Help / why?" button if you get stuck.

If you skipped it, the Tutorial button on the main menu opens a list of 10 short lessons, from Food supply practice and Hospitals and healing to Upgrading buildings, Producing and training warriors, and Guard zones and flag tactics. Each one drops you into a prepared colony with one job to do. After the introduction, I would play Food supply practice next, because food is what trips up almost every new player.

[Image: glob2-02-introduction-lesson.jpg]

### Your first solo match

From the main menu, choose Custom game. The setup has three tabs: Map, Players & Teams and Game Rules. On Map, pick one of the premade maps rather than a random one. On Players & Teams, leave yourself as "You" and give the other colony to the AI. The opponents are listed weakest first, and Numbi - Easy is the default; its description calls it a forgiving opponent that still expands and attacks, which is accurate. On Game Rules, pick the Gentle ruleset, which is described as forgiving rules for a first match. Then press Start game.

### The early decision: food or builders?

Within a few minutes you will hit the decision the whole game is built around. Your Swarm turns wheat into new globs, five wheat per glob. More globs means more hands, but every one of them has to eat. Globs walk to an Inn when their food reserve falls to about a quarter, and a glob that runs out of food loses health until it dies. A basic Inn feeds four globs at once and holds only 10 wheat, and that wheat only arrives if workers carry it in from the fields.

[Image: glob2-03-inn-and-wheat.jpg]

At the same time, everything you build needs workers to fetch wood and put it together. So the question is always: how many workers stay on food, and how many can you spare for construction?

[Image: glob2-04-school-site-working-slider.jpg]

You answer it with two controls on every building. Select a building and you will see Working, shown as two numbers: the workers who have turned up, and the number you requested. Drag the slider (or press + and -) to change the request. Next to it is a priority setting: Low priority, Medium priority or High priority. The colony staffs high-priority buildings first. When priorities are equal, a finished Inn already outranks a fresh building site, which is a sensible default.

Here is how I play the opening, and it is my habit, not a rule from the game. Never let your first Inn or the Swarm run short of suppliers. Before you turn up the Swarm, build a second Inn next to a wheat patch, because a bigger colony with the same food supply just starves faster. When you need builders for something big, turn the Working number down on buildings that can wait (a flag, a training building under construction) rather than on your food chain, and turn it back up afterwards. If a construction site is crawling along, give it High priority instead of piling more workers on everything. Watch the Inn's food count when you select it: if it keeps dropping toward zero, you have taken too many workers off food.

Get that balance right, and the colony starts to feel like it runs itself. That is the moment the game clicks.

[Image: glob2-05-battle.jpg] (optional fifth image; drop it if FCM wants four)

### Where to go next

Once you are comfortable, Schools train workers so they can build higher building levels, and upgrading an Inn lets it feed more globs at once and store more wheat. Set the Swarm to produce warriors, train them at Barracks and send them out with War Flags. Online, there are casual and ranked one-on-one quick matches and private rooms, plus LAN games and a map editor. On the desktop builds there is also an optional, built-in MCP server, which lets you play the same colony alongside your own AI agent. It is off by default, and it is a story for another article.

### Conclusion

Globulation 2 asks you to think about a colony instead of clicking units, and the tutorial does a good job of teaching that. It is free and open source, with no ads and no in-app purchases, so there is nothing stopping you from trying it. Go grab it from snapcraft.io/globulation2 or github.com/Globulation2/glob2/releases/latest. The website is glob2.online, and the source is at github.com/Globulation2/glob2. Bug reports are welcome there.

[Bio: 2–3 sentences in third person — user to write]
