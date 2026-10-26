# Marketing project working rules

## Delegation

The coordinating agent must oversee sub-agents for all substantive work instead of performing it directly. Assign clear file or responsibility ownership, ask sub-agents to respect concurrent edits, and review and integrate their results. Split independent work across a team and parallelize whenever useful. Avoid overlapping file ownership and competing Git operations; designate one agent to commit and push a completed batch.

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
