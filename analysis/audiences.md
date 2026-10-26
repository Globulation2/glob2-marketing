# Audience and persona possibility map

[Analysis index](README.md) · [Jobs to be done](jobs-to-be-done.md) · [Product evidence](../facts/product.md) · [Asset evidence](../facts/assets.md) · [Channels](../facts/channels.md)

Written **26 October 2026**, after the initial factual inventory. Every audience, motivation and persona below is an **analyst hypothesis**, not an observed customer segment, selected target or research finding. No interviews, surveys, usage-cohort analysis or willingness-to-pay studies were conducted. Personas are defined by circumstances and preferences rather than invented ages, biographies or demographic stereotypes. The rows have no priority order.

## Evidence available and missing

The factual basis is an indirectly controlled colony RTS, an existing tutorial/campaign/custom-game/editor, computer opponents, documented online competition and creator systems, and optional paid-service machinery. See product records [P01–P16 and B01–B05](../facts/product.md). The observed estate includes a long-lived open-source community, modern browser entry and platform-specific distribution traces; it does not measure demand for these particular propositions. Source capability and public availability differ.

Absent evidence includes player interviews, acquisition sources, retained-player cohorts, match/session length distribution, accessibility research, creator retention, churn reasons, willingness to pay, and how legacy players perceive the revamped game. These omissions prevent ranking the possibilities or estimating segment size.

## Psychographic dimensions

A person can occupy several dimensions and change goals between sessions. These are independent tensions, not mutually exclusive audience boxes.

| Dimension | Possible motivation at one end | Possible motivation at another end | Glob2 connection and unresolved tension |
| --- | --- | --- | --- |
| Direct execution ↔ systems orchestration | Enjoy precise unit control and rapid intervention | Enjoy setting priorities and watching a system respond | P01 supports orchestration; indirect control could feel like agency to one player and frustrating delay to another. Low click count is not proof of low difficulty. |
| Optimization ↔ observation | Diagnose bottlenecks and improve efficiency | Enjoy an inhabited colony and emergent behavior | P02 offers food, population and training feedback. The visual appeal of a colony does not establish a peaceful or cozy experience. |
| Mastery ↔ easy entry | Learn a deep ruleset and improve over repeated matches | Try something quickly with limited commitment | Tutorial/browser entry may reduce initial setup, while unfamiliar control and service dependencies may still increase learning effort. |
| Rivalry ↔ shared activity | Test skill against opponents and track progress | Spend time with friends or solve a problem together | P05–P06 support multiplayer structures; sustained opponent supply and specific cooperative modes are not established. |
| Predictability ↔ experimentation | Prefer stable rules and comparable results | Explore custom rules, content and unusual combinations | P09–P14 expose experimentation; experimental content and compatibility boundaries can conflict with stable competitive expectations. |
| Consumption ↔ authorship | Play content prepared by someone else | Make maps, music, AI or visual content | P10–P16 suggest multiple creator roles with very different skills and motivations. Content quantity is not proof of quality or a creator community. |
| Personal control ↔ assisted creation | Write code/art or give every strategic instruction personally | Use generation or an AI commander to express intent | B02–B04 introduce assistance possibilities; trust, cost predictability, authorship and ranked fairness could matter differently to different users. |
| Convenience ↔ ownership/inspectability | Start quickly and rely on hosted services | Keep local files, inspect source, self-host or contribute | Browser entry and free-software source coexist. Hosted accounts, paid services and platform restrictions can pull in a different direction from offline ownership. |
| Continuity ↔ novelty | Reconnect with familiar play and community history | Seek unfamiliar mechanics and a modern presentation | Twenty-plus years of history can support continuity; legacy screenshots, old instructions and changed behavior can create conflicting expectations. |

## Hypothetical gamer personas

| ID / circumstance | Desired experience and possible trigger | Product fit hypothesis | Frictions, constraints and counterevidence |
| --- | --- | --- | --- |
| G01 — Indirect-strategy explorer | Sees colony/task-assignment gameplay and wants a new strategic control model | P01–P03 may appeal through prioritization, logistics and consequences rather than individual movement | A familiar RTS label could create direct-control expectations. Delayed responses may feel opaque. It is unknown whether novelty survives the first-session learning cost. |
| G02 — Colony/logistics optimizer | Wants to solve food, worker allocation, training and expansion bottlenecks | P02–P04 and custom rules offer interconnected systems and repeatable practice | A colony-sim expectation may exceed campaign persistence/building scope; military pressure or abstraction may frustrate. No evidence establishes long-term colony-sandbox demand. |
| G03 — RTS competitor | Wants skill expression, fair matches, clear results and improvement | P03, P05–P06 offer conquest/prestige, ratings and match records | Population, wait time, balance, anti-abuse experience and performance are unmeasured. AI assistance permitted on enabled ranked instances could be attractive, unacceptable or irrelevant; player responses are unknown. |
| G04 — Solo learner with a limited session | Wants an understandable first success or a replayable challenge without arranging opponents | Tutorial, campaigns and AI custom games in P04; browser entry as a discovery path | Time to tutorial completion and match duration are unmeasured. [Browser-local saves](https://github.com/Globulation2/glob2/blob/c9198b854a2ea6fc16cd5524913cf96c5a80c499/docs/browser/storage.md) require care; “quick to open” does not mean “quick to finish.” Interruptions and small screens need separate testing. |
| G05 — Friend-group host or mixed-skill participant | Wants a reason to gather friends and enter the same game with little setup | Rooms/invite links, guests and AI seats in P05 could support social play | Sim-version compatibility, host responsibilities and onboarding coordination can create friction. Shared-colony/team source structures do not establish a dedicated cooperative campaign or a polished co-op progression mode. |
| G06 — Free-software/Linux or self-hosting enthusiast | Finds the game through an open-source/distribution community and values inspectability, offline use or stewardship | Open source, build documentation, offline/LAN play and documented hosting are relevant facts | Values alignment does not establish enjoyment, retention, technical ability or donations. Optional external AI/payment dependencies and divergent store policies may complicate expectations. |
| G07 — Returning legacy player | Encounters a familiar name and wants to revisit a remembered game or community | Existing history, wiki, old distributions and modern continuation can supply recognizable entry points | Memories may concern a different build, art style, balance or control feel. Old accounts/content may not carry over. Historical awareness does not establish current contactability or demand. |
| G08 — Emergent-world observer | Sees real colony footage and wants to watch autonomous behavior unfold | P01–P02 and existing UI-free/replay footage expose a visually readable possibility | Aesthetic attraction can fail when translated into actual play. Warfare, hunger, defeat and management demands complicate any relaxed-play expectation; no “cozy” classification is assumed. |

“Casual” could mean low commitment, social intent, flexible scheduling, low execution demands or low appetite for competition. Those are different needs; none establishes that Glob2 is easy, mobile-qualified, short-session or accessible to a given person.

## User, creator and contributor personas

These users may play little or never play ranked. Some may be both creators and players; overlap has not been measured.

| ID / circumstance | Job or motivation hypothesis | Relevant source-documented system | Friction / uncertainty |
| --- | --- | --- | --- |
| U01 — Map/scenario author | Express a setting, construct a challenge, share it and see it played | P10 maps/editor/catalog; optional B03 generation | Validation is not enjoyment or balance. Discovery, feedback, revision handling and audience size can determine whether publishing feels worthwhile. |
| U02 — AI/code tinkerer | Write an agent, test a strategy and learn through visible behavior | P11–P12, public AI starter repository, coding Studios | API learning, debugging, language knowledge, validation and local-vs-trusted playtests can impede progress. Coding interest does not imply spending on model calls. |
| U03 — Artist/world-building author | Change colony appearance, terrain, resources or buildings | P13–P14/P16 | Cosmetic authorship differs from changing rules. Tools may require different skill levels; asset rights, compatibility, approval and entitlement availability remain constraints. |
| U04 — Music creator | Hear an adaptive three-mood soundtrack in an actual game and share it | P15 | Loop quality, technical export requirements, licenses and feedback may matter more than winning matches. Paid generation could compete with composing by hand rather than complement it. |
| U05 — Developer/translator/maintainer | Improve a project, practice skills or preserve a game they value | Public repositories, contribution/build documentation, translations and historical material | Toolchain complexity, review work, project direction and volunteer capacity may outweigh the appeal of public source. A contributor is not necessarily a customer or launch audience. |
| U06 — Community organizer, teacher or presenter | Run an activity, explain a system, document play or assemble a small event | Rooms, guides, recording/replays and public match records are possible ingredients | No tournament product, classroom curriculum, spectator production suite or child-focused suitability is established. Scheduling, safety/moderation, device setup and permissions would be separate concerns. |

## Player, user, payer and purchaser are different roles

| Possible payer circumstance | What they might be paying for | Existing machinery versus unproven demand | Possible objections |
| --- | --- | --- | --- |
| A player wants a personal colony appearance | Identity/customization | B01 contains designer/preset entitlements and one-time checkout | May expect customization to be free; appearance value, live prices and purchase availability unverified. |
| A creator wants faster iteration | Generated maps/art/music/code | B03–B04 contain distinct Studio accounting | Uncertain output quality, separate balances, price predictability, authorship and tool alternatives can weaken value. |
| A player wants assisted command | Natural-language commander work | B02 exists behind enablement/qualification gates | Desire for assistance may conflict with mastery, trust, spending control or competitive norms. |
| A supporter wants the game to continue | Stewardship or voluntary support | A possible motivation; this pass did not verify a general support-payment program | Open source/free play does not establish willingness to donate or what recognition would be acceptable. |
| An organizer funds access for other users | Shared event/learning opportunity | Hypothesis only; organization licensing, pooled wallets or group billing are not established | Procurement, accounts, moderation and billing complexity could exceed the need. |

These roles cannot be inferred from one another: a frequent player may never pay; a creator may buy tooling and rarely compete; a supporter may fund maintenance without using a premium feature. No willingness-to-pay or payer-conversion claim follows from payment code.

## Cross-cutting constraints and interpretation risks

- **Session and device:** browser discovery, a desktop match, a phone visit and offline play are separate circumstances. Physical-device qualification, performance, save portability and actual match duration remain unknown.
- **Accessibility and agency:** indirect control may reduce repeated selection for some users while increasing cognitive demand and state ambiguity for others. Vision, motor, hearing, language and cognitive needs require specific evidence; aesthetic contrast/theme support does not establish whole-game accessibility.
- **Identity and trust:** source transparency may matter to some; others may care chiefly about reliability, account friction and whether a download is safe. Neither attitude is a demographic segment.
- **Rights and generative content:** creator ownership, reuse licenses and AI disclosure can be motivations or deterrents. No common community attitude is assumed.
- **Message-to-experience match:** colony imagery, competitive claims, free-software language and AI-tool demonstrations foreground different experiences. The [asset ledger](../facts/assets.md) records existing variants without selecting one.

## Questions that could distinguish these hypotheses

Which descriptions cause people to expect individual unit control, persistent city-building, peaceful play or short matches? What first action and outcome make the indirect-control model understandable? What brings someone back after one session? Which users prefer offline/local ownership over account services? What prevents friends entering the same match? Do creators seek feedback, reach, learning, personal expression or income? Under what conditions would AI assistance feel useful, fair and worth paying for? How do returning players distinguish continuity from unwanted change?

These are open research questions, not a research priority list or a selected positioning. See [jobs to be done](jobs-to-be-done.md) for the corresponding circumstances and observable outcomes.
