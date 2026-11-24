# Demonstration and pitch brief

[Outreach project](README.md) · [Claims and precedents](product-and-prior-art.md) · [Approved storefront assets](../approved-storefront-rollout.md#approved-imagery-only--2026-10-30)

## The playable story

The expected overnight November 23–24 deployment makes online co-play the launch headline. Capture the exact public mode once it deploys. Include the local standing-order demonstration as a second way to try the idea.

Globulation 2 is an open-source colony strategy game where players already guide a settlement by assigning work and placing flags. A compatible AI coding agent can connect through the desktop game's built-in MCP server. Give it one job, such as managing worker production, and keep making the decisions about food, expansion and rivals yourself. In a local match, the agent can turn a plain-language instruction into a small JavaScript standing order, and the player can pause or cancel it in the game.

“Vibe-code a colony assistant” fits coding audiences. “I gave an AI one job in my strategy game” fits a gameplay video. “A strategy game with an interface for humans and coding agents” fits a technical feature. Each becomes more convincing when the viewer can see the job happen and recognize who made each decision.

## Local demo

Use a pinned current desktop release and one connection method proven with the specific MCP client on camera. Pick a compact map with a preflighted opening and a built-in opponent. Keep the map, seed or setup, release, agent/client, model, and initial objective beside the recording.

| Beat | What the audience should see |
| --- | --- |
| Explain the colony | Show an Inn, a Swarm and the worker requests. Explain that prioritizing new construction can leave food delivery short. |
| Delegate one job | Prompt the coding agent to inspect the colony and propose a small standing order, such as keep swarms worker-heavy while the colony grows. Show the actual JavaScript and the in-game standing-order card. |
| Split the work | Leave that routine running while the human places an exploration flag and changes a building priority. Show an actual outcome, with timestamps if edited. An accepted request alone is insufficient. |
| Show the limits | Pause and resume the routine with the in-game controls. Capture a real hesitation, correction or refused action if it explains the experience. |
| Give viewers a way in | Provide the desktop release, setup guide, exact prompt and small script or transcript. A replay can illustrate orders and outcome. A simultaneous screen recording or transcript establishes which actor issued each action. |

Make one short captioned cut and one uncut setup-to-action recording from the same run. Label actual time, sped-up sections, model, build and mode. Use actual gameplay, the approved visual family for supporting artwork, and the current official player links. A starter prompt should describe an intelligible job and human boundaries. Avoid invented match results, coding speed or model performance claims. [MCP server setup](https://glob2.online/learn/mcp-server/) · [MCP tools](https://glob2.online/learn/mcp-agent-tools/) · [Current release](https://github.com/Globulation2/glob2/releases/latest)

## Online extension

**Invitation exhibition.** Use two consenting humans on distinct Internet connections, one desktop AI-assisted seat or two disclosed AI-assisted seats, and an invite-only room. Record the released build, remote connection, who is driving each seat, the ordinary UI-only MCP actions used online and the result. Demonstrate the assistance visibly, for example by asking the agent to inspect and adjust a worker request through the ordinary game interface while the player scouts. Use the local demo for scripting. Record both views if possible. The existing engineering smoke ran on a local stack. [Engineering evidence](https://github.com/Globulation2/glob2/pull/1845)

**MCP quick-match release.** When the change ships, check the public instance listing and both clients' visible queues, then connect two human participants and verify the assisted queue, match start, result and separate match history. Test that the current unassisted client sees its ordinary queues and an ordinary match suspends its MCP endpoint. Record the release and deployment and explain the client-reported policy accurately. Queue listings alone cannot establish a real human opponent was present, and the older-client and room exceptions are meaningful. A creator challenge or a deeper fairness feature has a news event once these checks pass. [Implementation and scope](https://github.com/Globulation2/glob2/pull/1897) · [Public instance configuration](https://app.glob2.online/api/v1/instance)

**Hosted commander.** Confirm the public entitlement and credit path, target client/platform and a real command before offering this workflow as generally available. If the handbook and service state disagree, reconcile the public copy first. A feature identifier in metadata gives only configuration evidence. [Public handbook](https://glob2.online/learn/hive-mind/)

## Draft outreach approaches

Use the lead's dossier for its actual route, relevant work and timing. Tailor one sentence to that specific piece. Confirm the recipient or form still matches the pitch, check the existing [mobile outreach ledger](../mobile-press-outreach.md) for recent contact at the same newsroom and prefer one route per editorial desk. An editorial tip, a live collaboration invitation and a sponsorship inquiry are different requests. No fee or relationship is assumed.

| Audience | Subject draft | Offer |
| --- | --- | --- |
| AI engineer or newsletter | What happens when a coding agent shares control of a colony RTS? | Reproduce a local standing order in a current desktop release. Include the exact prompt, short script, permission boundaries and one observed failure. |
| PC strategy journalist | A colony RTS where you can give an AI the boring job | Try the same start with and without delegating a job. Lead with the game's food and worker tradeoffs. Footage shows the human's choices and the agent's contribution. |
| Creator | One colony, one player, one AI assistant | A short recorded challenge with a clear objective. The creator chooses what to delegate and retains the manual controls. Provide a clean reproduction path and show results in the same session. |
| Games industry or AI beat | An open-source RTS is giving AI-assisted players their own ladder | Offer an engineering interview, the exact public mode and observed behavior from both sides once the rollout is confirmed. |

### Launch-day first-touch draft

**Subject** · Bring your coding agent to an online strategy match

Hi [name],

[One sentence on a relevant experiment, article or video of theirs.]

Globulation 2 is a free, open-source RTS about feeding and growing a colony under pressure. Its desktop game lets you share the controls with a compatible AI coding agent using MCP. With the new [verified assisted mode], you can bring that setup into an online match with another player. You could ask the agent to adjust the colony’s worker assignments while you scout and plan the expansion.

I can share a short match recording, the exact desktop build and queue, and a local exercise where you ask an agent to write a small JavaScript standing order. If you want to try the multiplayer setup firsthand, I can arrange a match.

Bradley Arsenault

Globulation 2

### Desktop hands-on first-touch draft

**Subject** · A strategy game where your coding agent can help run the colony

Hi [name],

[One sentence tying this to a specific experiment, article or video of theirs.]

Globulation 2 is a free, open-source strategy game where you keep a colony fed and growing while rivals close in. Its desktop build has a built-in MCP server. In a local match, you can ask a coding agent to write a small routine for the colony, let the routine run, and keep playing manually.

If you'd like to try it, I can share the short demo, the exact prompt and build, and a setup you can replay. I’d be interested in seeing which job you'd hand off and which you'd keep.

Bradley Arsenault

Globulation 2

This project prepares research and drafts. Its demo proposal, private exhibition and public outreach were pending at handoff.
