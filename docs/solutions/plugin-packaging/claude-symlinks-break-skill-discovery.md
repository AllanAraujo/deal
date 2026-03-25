---
title: "Broken symlinks in .claude/ directory prevent skill discovery after plugin installation"
date: 2026-03-25
status: solved
category: plugin-packaging
tags:
  - claude-code-plugin
  - symlinks
  - git
  - skill-discovery
  - marketplace-install
modules:
  - .claude/skills
  - .claude/agents
  - skills/
  - agents/
symptoms:
  - "Skill missing from autocomplete after marketplace install (e.g., /deal:dd not listed)"
  - "Some skills discoverable while others are not"
  - "Broken relative symlinks in ~/.claude/plugins/cache/"
  - "Inconsistent skill availability between local dev and installed plugin"
root_cause: "Committed .claude/ symlinks with relative paths that resolve in the source repo but break in the marketplace cache, causing duplicate/conflicting skill entries that interfere with auto-discovery."
---

# Broken symlinks in .claude/ prevent skill discovery after plugin install

## Problem

After installing a Claude Code plugin via a local marketplace, some skills did not appear in the autocomplete list. Specifically, `/deal:dd` was missing while other skills like `/deal:notes` and `/deal:sde` worked fine. Typing `/deal:dd` would match to `/deal:notes` instead.

## Root Cause

During local development, `.claude/skills/` and `.claude/agents/` contained symlinks pointing to the plugin's root-level directories:

```
.claude/skills/dd -> ../../skills/dd
.claude/skills/sde -> ../../skills/sde
.claude/agents/financial-analyst.md -> ../../agents/financial-analyst.md
```

These symlinks were committed to git. When the plugin was installed via marketplace (cloned to `~/.claude/plugins/cache/deal-marketplace/deal/0.1.0/`), the relative paths broke because the cache directory structure is different from the source repo.

Claude Code loads skills from BOTH `.claude/skills/` (project-level) AND root `skills/` (plugin-level). When `.claude/skills/` exists but contains broken symlinks, Claude Code fails to index those skills. It does **not** fall back to the root `skills/` directory for the broken entries. The `.claude/` directory effectively shadows the working root-level definitions.

## Solution

### Step 1: Remove `.claude/` from git tracking

```bash
git rm -r --cached .claude/
```

This unstages the directory but leaves the symlinks on disk for local development.

### Step 2: Add `.claude/` to `.gitignore`

```gitignore
# Claude Code local config (symlinks are for local dev only, not distributed)
.claude/
```

### Step 3: Commit and push

```bash
git add .gitignore
git commit -m "fix: remove .claude/ from git — fixes skill discovery in installed plugin"
git push
```

### Step 4: Reinstall the plugin

```bash
claude plugin uninstall deal
# Update marketplace if using pinned SHA
claude plugin install deal
```

### Step 5: Verify

- `git ls-files .claude/` returns nothing (not tracked)
- Installed plugin cache has no `.claude/` directory
- All skills appear in `/deal:` autocomplete in a new session

## Key Insight

`.claude/` is a **local workspace configuration directory** — analogous to `.vscode/` or `.idea/`. It should never be committed to a plugin repository. The plugin's distributable interface is defined exclusively by root-level `skills/` and `agents/` directories plus `.claude-plugin/plugin.json`. Claude Code auto-discovers from these root directories without needing `.claude/` duplicates.

The confusion arises because `.claude/skills/` is the correct place for **project-level** skills (skills specific to a project, not a plugin). But for **plugin development**, the root `skills/` directory is what gets distributed. Having both creates conflicts when the plugin is installed elsewhere.

## Prevention

### At project init

Add `.claude/` to `.gitignore` before the first commit:

```bash
echo ".claude/" >> .gitignore
```

### Pre-release checklist

- [ ] `.claude/` is in `.gitignore`
- [ ] `.claude/` is not tracked: `git ls-files .claude/` returns nothing
- [ ] No symlinks in committed files: `git ls-files -s | grep ^120000` returns nothing
- [ ] All skills defined in root `skills/` (not `.claude/skills/`)
- [ ] All agents defined in root `agents/` (not `.claude/agents/`)
- [ ] Fresh clone to `/tmp/` passes skill discovery test

### Local dev workflow

If you need `.claude/` symlinks for local testing:
1. Create them locally (they stay on disk, gitignored)
2. Or develop against root `skills/` directly — Claude Code discovers from there when the CWD is the plugin repo
3. Never commit them

## Related

- Plugin plan: `docs/plans/2026-03-23-feat-deal-acquisition-due-diligence-plugin-plan.md`
- CLAUDE.md architectural invariants (especially invariant about skill/agent discovery)
- Claude Code plugin docs: https://code.claude.com/docs/en/plugins
- Claude Code skills docs: https://code.claude.com/docs/en/skills
