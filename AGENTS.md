# Marketing project working rules

## Delegation

The coordinating agent must oversee sub-agents for all substantive work instead of performing it directly. Assign clear file or responsibility ownership, ask sub-agents to respect concurrent edits, and review and integrate their results. Split independent work across a team and parallelize whenever useful. Avoid overlapping file ownership and competing Git operations; designate one agent to commit and push each completed work unit promptly. Workers hand off ready files and a work summary; the designated Git steward stages explicit completed paths only, so unfinished concurrent edits stay out of the commit. This coordination does not postpone the rule to commit after even small completed work.

## Git workflow

These Git workflow rules apply only to the `glob2-marketing` repository. On 2026-10-31, the user explicitly clarified that the no-pull-request rule does not apply to other repositories. Work in other repositories follows their own `AGENTS.md`, default-branch workflow, pull-request requirements and branch protections; this marketing policy does not authorize bypassing them.

- Work directly on `main`. Use trunk-based development only: no feature branches and no pull requests.
- Commit after completing work, including small amounts of work, and push directly to `origin/main`.
- Use a concise subject and a thorough commit body. Record the marketing work completed, evidence reviewed, findings or uncertainty documented, validation performed, and remaining follow-up where relevant. Do not merely list changed files or use shallow descriptions.
- Review the diff and status before committing. Stage only the assigned completed work; preserve other agents' edits. Never rewrite shared history or discard others' work.

## Information and directory conventions

- Prefer simple plain Markdown. Use the existing `facts/`, `analysis/`, and `planning/` structure, lowercase hyphenated filenames, directory README indexes, and relative links.
- `facts/` holds observed existing assets, product capabilities, channels, platforms, repositories, and historical evidence. Cite sources with observation dates; identify current, historical, and unverified records explicitly. A listing's existence does not establish account control or current availability.
- `analysis/` holds analyst assertions, possibilities, psychographics, personas, jobs to be done, comparisons, tradeoffs, and business-model hypotheses. Link to supporting facts, label uncertainty, and separate evidence from inference.
- `planning/` holds task ledgers and execution records. Update status, dependencies, evidence links, gaps, and next work as progress is made.
- Keep paths and indexes consistent. Link related records instead of creating divergent copies. Preserve provenance and asset usage-rights uncertainty.
- This repository is public: do not commit secrets, tokens, private account details, or unnecessary private correspondence. Use public evidence and minimal relevant metadata.
- **No version labels in names** (user requests, 2026-11-26: "why do we have all these v1s and v2s and v3s in the repo when the repo already has a version history", then "Yes, clean up"; and "why do we have any v's in the names at all", then "Yes, rename them"). Files and folders carry no version labels: the current set is simply `assets/storefront/`, `planning/storefront-rollout.md`, `facts/storefront-claims.md`, `analysis/positioning.md` and so on. Update assets and records in place, and never create `-v1`, `-v2` or similar copies: Git history keeps earlier versions. Refer to a past version with a permanent GitHub link at a commit SHA (`https://github.com/Globulation2/glob2-marketing/blob/<sha>/<path>`), and mark an approved set with a Git tag. The storefront-v1 upload set (`assets/storefront-approved-v1/`) and positioning v1 were removed on 2026-11-26 rather than renamed; they remain at commit `4e62f80` ([tree](https://github.com/Globulation2/glob2-marketing/tree/4e62f805935fa57724d66338071ee8553f059f18)). "storefront-v1" and "storefront-v2" remain fine as names of those rollouts in dated records and prose.

## Initial research boundary

Inventory the existing estate and history first; then map the marketing possibility space. The user has requested findings without recommendations or firm conclusions at this stage. Do not choose positioning, personas, channels, business models, or launch tactics. Record alternatives and tradeoffs for later decisions.

## Authorized follow-up phase

The user subsequently authorized a public platform audit and positioning-option drafts in parallel, followed by concrete player-validation preparation. Draft alternative audience/message combinations with supporting evidence and tradeoffs; keep them distinct from verified facts. Do not treat this authorization as a selected strategy, completed player research, permission to contact people, or approval to change live listings. Final launch-kit production depends on a message decision.

## Selected launch v1

**Superseded as the current message reference on 2026-11-24** by [positioning v2](analysis/positioning.md); see [Storefront v2 revamp](#storefront-v2-revamp--2026-11-24). The text below is kept as the record of the earlier decision.

The user subsequently stopped recruitment/testing as the immediate approach and selected a working launch positioning through discussion on 2026-10-26. Use [the agreed v1](https://github.com/Globulation2/glob2-marketing/blob/4e62f805935fa57724d66338071ee8553f059f18/analysis/positioning-v1.md) as the current message reference: colony building and economics lead, with spatial strategy and rival pressure supporting. Historical research plans remain preserved but are not active launch prerequisites. This is a user decision, not player validation or authorization to contact people or change live listings.

## Approved storefront rollout

On 2026-10-30, after reviewing the final Epic-style presentation, the user said: “this is approved for use. lets commit this and then apply this to all of our various storefroents”. The [approved storefront rollout](planning/approved-storefront-rollout.md) records the exact copy and current media. Apply this approved presentation to project-controlled storefront listings and their maintained source metadata, adapting only to platform fields and asset requirements. This authorization supersedes earlier preparation-only limits for listing updates. The subsequent publishing/submission authorization below governs actual product releases and review submissions. Preserve truthful artifact qualification, pricing and account/legal/security declarations; unrelated outreach and independent catalog control are not inferred. Record actual changes and access gaps; approval is not evidence that a listing has been updated.

## Approved imagery only

**Superseded on 2026-11-24** by the [real-game-art-only rule](#real-game-art-only) in the storefront v2 section below. The text below is kept as the record of the earlier rule and still describes what was uploaded under storefront-v1. Its upload-verification requirement is unchanged and carries into v2: wait for uploads to finish before saving, then use a fresh server reload and visual comparison.

On 2026-10-30, the user required using only approved images/screenshots or direct modifications of them, with no outside imagery. All new storefront uploads must come from the [approved source family and direct derivatives](planning/approved-storefront-rollout.md#approved-imagery-only--2026-10-30). Do not add unrelated, stock or newly generated imagery. Preserve existing mobile device galleries and compiled application icons unless an approved replacement is available. Wait for uploads to finish before saving, then use a fresh server reload and visual comparison to verify the saved images; an initiated upload or generic save success is insufficient evidence.

## Publishing and approval submission authorized

On 2026-10-30, the user explicitly instructed: “We need to start getting these things live and start publishing, submitting them for approval, everything.” This supersedes the earlier marketing-only/no-release boundary. Proceed with review submissions and actual publication/releases of the current Glob2 products when the platform preflight and current-artifact checks allow; publication itself does not require another confirmation.

Keep legal, fee, security and policy answers truthful and evidence-backed. Do not blindly accept payments, agreements or declarations to bypass a gate, invent release qualification, or publish an incomplete package. Existing approved imagery/direct-derivative restrictions and the user-selected `https://glob2.online/` main website remain in force. Record saved drafts, submitted reviews, approved versions and publicly live releases separately in the [publishing ledger](planning/approved-storefront-rollout.md#publishing-and-review-submission-authorized--2026-10-30). No future action is complete merely because it is authorized.

## Storefront v2 revamp — 2026-11-24

On 2026-11-24 the user asked for a revamp of the store listings and made the decisions below. They are binding for all storefront work from that date. The working records are [positioning v2](analysis/positioning.md) and the [storefront v2 rollout ledger](planning/storefront-rollout.md); work from those files, not from chat.

Where the user's own words are available they are quoted. The other decisions were selected by the user from options the coordinating agent presented, and are recorded as user selections, not quotations.

### What the user asked for

> I want to refresh the visual appearance as best we can, especially the main store image and the game screenshots. We kind of look amateurish right now.

> make sure we are mentioning some of our biggest advantages like being 100% ad-free while also free to play and also no annoying lootboxes or in-game currencies. For desktop users, being the first game you can play in tandem with AI through MCP is a selling point. For mobile users, its just great RTS gameplay.

> for in-game footage, make sure it follows our marketing rules too about capturing exciting action scenes and not boring mostly empty scenes

### Authorization

The user authorized, as one piece of work:

- revamping the canonical listing as storefront-v2: copy, key art, screenshots, icon and trailer;
- translating it into all supported languages (the English source plus the 44 non-English catalogs in [translations](translations/README.md)), each with an independent review;
- applying it to project-controlled stores and their maintained source metadata, without interrupting in-flight store reviews.

**No sign-off stops** (user selection). The team runs end to end. Do not pause for user approval between phases; report results to the coordinating agent, which sends key deliverables to the user as they land without blocking on a reply.

This does not widen anything else. Sign-in and multi-factor prompts stay with the user. A new agreement, fee or declaration is put to the user rather than accepted to clear a gate. The [publishing rules above](#publishing-and-approval-submission-authorized) on truthful legal, fee, security and policy answers still apply, and so does `https://glob2.online/` as the main website. Changes in other repositories follow those repositories' own rules. Authorization is not evidence that a listing has been updated; record prepared, reviewed, saved, submitted and publicly verified states separately in the ledger.

**Rollout timing** (user selection). Update Snap, itch.io, Microsoft Store, Google Play and the maintained F-Droid/AppStream source metadata now. Update Apple (iOS and Mac), Epic and Amazon when each review clears or with the next version. Prepare Steam and GOG assets only. Before writing to any store, check that no review is in flight there.

### Real game art only

This replaces [Approved imagery only](#approved-imagery-only) (user selection).

- Allowed: fresh in-engine captures, compositions of real game sprites and scenes, and design treatment of them (captions, framing, crops).
- Not allowed: AI-generated imagery and stock imagery, in any storefront image or video.
- The storefront-v1 source family is no longer the limit on what may be uploaded. A v1 image may be reused only if it meets this rule and the footage rule below; the v1 illustrated cover is replaced by key art built from real game art.
- The earlier instruction to preserve existing mobile device galleries and application icons is lifted for v2: the galleries are replaced with fresh captures, and the icon with a faithful, sharp high-resolution redraw of the existing blue glob icon (same shape, not a redesign; user selection).
- Upload verification is unchanged. Wait for uploads to finish before saving, then use a fresh server reload and visual comparison to verify the saved images. An initiated upload or a generic save success is insufficient evidence.

Wherever an earlier section or ledger refers to the approved-imagery restriction as still in force, read it as this rule for v2 work.

### Footage rule

[Gameplay video for marketing](planning/gameplay-video.md) is binding for every store screenshot and all trailer footage, not only for social clips. In short: developed colonies with many visible buildings and units, visible activity from the first frame, the action recognisable at phone and feed size, and the actual match, interface and gameplay speed. No mostly empty terrain, early-game starts, fog-black frames or menu screens as gameplay shots. Label AI-versus-AI footage as a spectator view and record build, platform, map and capture conditions.

### Monetisation: nothing is sold

When asked what is sold to players, the user answered: "Nothing is sold". The listing says so flatly: free, no ads, no in-app purchases, no lootboxes, no in-game currency.

The source contains payment and credit machinery for colony skins, Hive Mind and the Studios ([product ledger](facts/product.md#existing-commercial-machinery)). Those are not promoted in any listing. The claims verifier checks production and each store's ads and purchase declarations and records the result in [storefront v2 claims](facts/storefront-claims.md). A claim that cannot be confirmed for a store is dropped or scoped there and reported to the user.

### MCP: never claim "first"

The user's first wording called Globulation 2 "the first game you can play in tandem with AI through MCP". After being shown the [prior-art research](planning/mcp-outreach/product-and-prior-art.md), the user chose to drop "first". Do not write "first" about MCP or AI play in any form, in any language, in copy, captions, images or video.

The desktop pitch is: play the same colony alongside your own AI agent through the game's built-in MCP server. MCP is desktop-only (native Windows, macOS and Linux). It is not mentioned in mobile listings, and it is used for a desktop store only where the claims verifier has confirmed it for that store's build.

### Platform split

- **Mobile listings** lead with great real-time-strategy gameplay plus the fair deal (free, no ads, no in-app purchases).
- **Desktop listings** carry the same, and add AI co-play through MCP.

This supersedes [positioning v1](https://github.com/Globulation2/glob2-marketing/blob/4e62f805935fa57724d66338071ee8553f059f18/analysis/positioning-v1.md), including its line that AI tooling is not the lead promise. Positioning v2 is a user decision, not player validation.

### Other user selections

- **Trailer:** yes, 30–45 seconds, from real in-engine recordings.
- **Localized screenshot captions:** captioned sets rendered by script for all 44 non-English languages and English; uploads are tiered, top languages first.

## Web portal ads — 2026-11-26

After the [portal listing research](analysis/README.md) showed that Poki, GameDistribution and Yandex Games require their ad SDKs, and CrazyGames requires them for Full Launch, the user said: "Yes please implement all of these reccomendations and get to work on enabling portal-specific builds with portal-ads that follow the reccomendations of each of these platforms."

- **Scope:** only the portal packages whose portal requires or expects ads (Poki, GameDistribution, Yandex Games, CrazyGames, and GamePix where its SDK offers interstitials), each following that portal's own ad rules. Our own site, itch.io, desktop and mobile stores stay ad-free, and so do Game Jolt and Newgrounds, which don't require game ads.
- **Claims:** a listing for an ad-enabled portal package must not say "No ads" or "ad-free" in any form. "No in-app purchases" and "no loot boxes" stay true. Copy elsewhere is unchanged. Record each portal's ad configuration in the [web portal rollout](planning/web-portal-rollout.md).
- **Still not sold:** nothing is sold to players. Portal ads are the portal's monetisation, and revenue share is under each portal's developer terms, which the user accepts. Agreements, payout and tax forms stay with the user.
- The approved listing recommendations in the per-portal `analysis/*-listing-comparison.md` files are authorized for execution, subject to the claims record and the real-game-art and footage rules above.
