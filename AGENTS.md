# Marketing project working rules

## Delegation

The coordinating agent must oversee sub-agents for all substantive work instead of performing it directly. Assign clear file or responsibility ownership, ask sub-agents to respect concurrent edits, and review and integrate their results. Split independent work across a team and parallelize whenever useful. Avoid overlapping file ownership and competing Git operations; designate one agent to commit and push each completed work unit promptly. Workers hand off ready files and a work summary; the designated Git steward stages explicit completed paths only, so unfinished concurrent edits stay out of the commit. This coordination does not postpone the rule to commit after even small completed work.

## Git workflow

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

## Initial research boundary

Inventory the existing estate and history first; then map the marketing possibility space. The user has requested findings without recommendations or firm conclusions at this stage. Do not choose positioning, personas, channels, business models, or launch tactics. Record alternatives and tradeoffs for later decisions.

## Authorized follow-up phase

The user subsequently authorized a public platform audit and positioning-option drafts in parallel, followed by concrete player-validation preparation. Draft alternative audience/message combinations with supporting evidence and tradeoffs; keep them distinct from verified facts. Do not treat this authorization as a selected strategy, completed player research, permission to contact people, or approval to change live listings. Final launch-kit production depends on a message decision.

## Selected launch v1

The user subsequently stopped recruitment/testing as the immediate approach and selected a working launch positioning through discussion on 2026-10-26. Use [the agreed v1](analysis/positioning-v1.md) as the current message reference: colony building and economics lead, with spatial strategy and rival pressure supporting. Historical research plans remain preserved but are not active launch prerequisites. This is a user decision, not player validation or authorization to contact people or change live listings.

## Approved storefront rollout

On 2026-10-30, after reviewing the final Epic-style presentation, the user said: “this is approved for use. lets commit this and then apply this to all of our various storefroents”. The [approved storefront rollout](planning/approved-storefront-rollout.md) records the exact copy and current media. Apply this approved presentation to project-controlled storefront listings and their maintained source metadata, adapting only to platform fields and asset requirements. This authorization supersedes earlier preparation-only limits for listing updates. The subsequent publishing/submission authorization below governs actual product releases and review submissions. Preserve truthful artifact qualification, pricing and account/legal/security declarations; unrelated outreach and independent catalog control are not inferred. Record actual changes and access gaps; approval is not evidence that a listing has been updated.

## Approved imagery only

On 2026-10-30, the user required using only approved images/screenshots or direct modifications of them, with no outside imagery. All new storefront uploads must come from the [approved source family and direct derivatives](planning/approved-storefront-rollout.md#approved-imagery-only--2026-10-30). Do not add unrelated, stock or newly generated imagery. Preserve existing mobile device galleries and compiled application icons unless an approved replacement is available. Wait for uploads to finish before saving, then use a fresh server reload and visual comparison to verify the saved images; an initiated upload or generic save success is insufficient evidence.

## Publishing and approval submission authorized

On 2026-10-30, the user explicitly instructed: “We need to start getting these things live and start publishing, submitting them for approval, everything.” This supersedes the earlier marketing-only/no-release boundary. Proceed with review submissions and actual publication/releases of the current Glob2 products when the platform preflight and current-artifact checks allow; publication itself does not require another confirmation.

Keep legal, fee, security and policy answers truthful and evidence-backed. Do not blindly accept payments, agreements or declarations to bypass a gate, invent release qualification, or publish an incomplete package. Existing approved imagery/direct-derivative restrictions and the user-selected `https://glob2.online/` main website remain in force. Record saved drafts, submitted reviews, approved versions and publicly live releases separately in the [publishing ledger](planning/approved-storefront-rollout.md#publishing-and-review-submission-authorized--2026-10-30). No future action is complete merely because it is authorized.
