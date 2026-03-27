# Deal Plugin — Development Conventions

## What This Is

A Claude Code plugin (`/deal` namespace) for business acquisition due diligence. 7 user-invocable skills + 1 domain knowledge skill + 7 agents.

## Architecture

- **Skills** (`skills/<name>/SKILL.md`) orchestrate workflows and interact with users
- **Agents** (`agents/<name>.md`) are domain specialists launched as subagents by skills
- **Domain knowledge** (`skills/deal-knowledge/SKILL.md`) provides SDE methodology and valuation reference

## Architectural Invariants

These are non-negotiable. Verify before every commit:

1. **All orchestrator skills run inline (no `context: fork`).** Required for AskUserQuestion and Agent tool to work.
2. **Every agent has an explicit `tools` allowlist.** Omitting `tools` gives the agent ALL tools by default — including WebSearch. This breaks the confidentiality boundary.
3. **Web-search agents have NO filesystem access.** `market-researcher` gets `tools: ["WebSearch", "WebFetch"]` only. Context is passed inline by the orchestrator.
4. **`allowed-tools` on skills is for permission convenience, not enforcement.** Agent `tools` fields are the enforcement layer.
5. **Subagents cannot spawn other subagents.** All multi-agent orchestration happens from inline skill context.

## File Organization

- `skills/` — User-facing orchestrators (SKILL.md format)
- `agents/` — Subagent definitions (flat, domain-prefixed names)
- `assets/` — Plugin assets shipped with the plugin (templates, static files)
- `scripts/` — Helper scripts invoked by skills via Bash (Python, shell)
- `templates/` — Development reference materials (gitignored, not part of distributed plugin)
- `docs/` — Plans and brainstorms (development only)

## Agent Naming Convention

Flat directory with domain prefixes: `financial-`, `market-`, `listing-`, `dd-`, `notes-`.

## Output File Convention

All plugin outputs are written to the user's deal folder:
- `deal-box.md` — at project root
- `sde-calculator.md` + `sde-calculator.xlsx` — SDE report and interactive workbook
- `due-diligence.md`, `deal-calculator.md`, `listing-review-*.md` — in deal folder

## Confidentiality Rules

- Financial agents: `tools: ["Read", "Grep", "Glob"]` or `["Read", "Write", "Grep", "Glob"]` — NEVER WebSearch/WebFetch
- Web agents: `tools: ["WebSearch", "WebFetch"]` — NEVER Read/Grep/Glob
- Synthesizer: `tools: ["Read", "Write", "Grep", "Glob"]` — reads agent output files, writes final document
- Web agents receive ONLY: business name, industry, geography. NEVER financial figures.

## Skill Frontmatter

Every orchestrator skill should include:
```yaml
allowed-tools: [tools the skill's subagents need auto-approved]
```
And must NOT include `context: fork`.

## Testing

- Use Lake Lure Marine reference data in `templates/Due Diligence/` as the gold standard
- SDE template in `templates/SDE calculator command/`
- Deal box UI reference in `templates/deal box command/`
