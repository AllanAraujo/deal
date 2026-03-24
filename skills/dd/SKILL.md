---
name: dd
description: >
  Due diligence analysis with parallel multi-agent execution. Discovers available
  materials in the deal folder, launches specialized agents (financial analyst,
  market researcher, listing reviewer) in parallel, then runs a synthesizer to
  produce a complete due-diligence.md document. Use when you have financial
  documents, broker materials, or listing content and want a full DD report.
argument-hint: "[deal-folder-name]"
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch
---

# /deal:dd — Due Diligence Analysis

## Overview

You are the orchestrator for a multi-agent due diligence analysis. You will:
1. Discover what materials are available in the deal folder
2. Ask the user for web search permission (with privacy disclosure)
3. Launch specialized agents in parallel based on available materials
4. Run a synthesizer agent to produce the complete DD document

**You run INLINE (not as a subagent).** You use the Agent tool to spawn subagents.

## Step 1: Ensure .gitignore Exists

Check if `.gitignore` exists at the project root (traverse upward, max 5 levels). If not, create it with the standard template (see /deal:sde for the template).

## Step 2: Determine Deal Folder

If `$ARGUMENTS` is provided, use it as the deal folder name relative to the project root. Otherwise, use the current working directory.

Verify the deal folder exists and contains at least one source of materials. If empty, show this error and stop:

> "No materials found in this deal folder. To run due diligence, you need at least one of:
> - Financial documents in `financials/` (P&Ls, balance sheets, tax returns)
> - Broker documents in `confidential/` (CIM, broker package)
> - A listing review (`listing-review-*.md`)
>
> Add documents and try again, or run `/deal:listing` first to review a listing."

## Step 3: Material Discovery

Scan the deal folder and catalog what's available:

```
Materials to check:
├── financials/          → P&L, balance sheet, tax returns (.pdf, .xlsx, .xls, .csv, .txt, .md)
├── confidential/        → CIM, broker packages (any files)
├── sde-calculator.md    → Output from /deal:sde
├── listing-review-*.md  → Output from /deal:listing
└── deal-box.md          → Buyer profile (traverse upward to project root)
```

Present the discovery results to the user:

> "**Materials found for due diligence:**"
> - Financial documents: [N files in financials/] — [list filenames]
> - Broker/confidential docs: [N files in confidential/] — [list filenames]
> - SDE calculator: [Yes/No]
> - Listing review(s): [Yes/No — list filenames]
> - Deal box (buyer profile): [Yes/No]

## Step 4: DD Overwrite Protection

Check if `due-diligence.md` already exists in the deal folder. If it does:

1. Read the file and check for a "## Revision History" section
2. If revision history exists (meaning `/deal:notes` was used), warn the user:

> "An existing due-diligence.md was found with revision history from /deal:notes. Re-running will overwrite those refinements."

Use AskUserQuestion:
- "Archive current version (save as due-diligence-YYYY-MM-DD.md, then overwrite)"
- "Overwrite without archiving"
- "Cancel"

If the user cancels, stop.
If archiving, rename the existing file before proceeding.

3. If no revision history exists, proceed silently (overwrite is fine).

## Step 5: Web Search Permission

If any materials exist that identify the business name, ask for web research permission with privacy disclosure:

> "I can research **[business name]**'s market position, industry trends, and online reputation through web searches.
>
> **Privacy note:** Web searches will query public search engines for this business name. This creates a discoverable record of your interest in this business. Search queries will NOT include any financial data.
>
> Allow web research?"

Use AskUserQuestion with options:
- "Yes — research market, industry, and reputation"
- "No — skip web research (Sections 2 and Community Standing will be omitted)"

Record the user's choice for the agent launch plan.

## Step 6: Build Agent Launch Plan

Based on available materials and permissions, determine which agents to launch:

| Agent | Launch Condition | Zone |
|-------|-----------------|------|
| `financial-analyst` | `financials/` has documents | Financial (no web) |
| `listing-reviewer` | `confidential/` has docs OR `listing-review-*.md` exists | Financial (no web) |
| `market-researcher` | User granted web permission AND business name is known | Web (no filesystem) |

**At minimum one agent must be launchable.** If not, the error in Step 2 should have caught this.

## Step 7: Create Working Directory

```
mkdir -p _dd-working/
```

This is where agents write their intermediate outputs.

## Step 8: Launch Agents in Parallel

Launch all applicable agents using the Agent tool. **Launch them in parallel** (multiple Agent tool calls in a single message).

**For `financial-analyst`:**
```
Launch agent "financial-analyst" with prompt:
"Analyze the financial documents for due diligence. The deal folder is at [path].
Financial documents are in [path]/financials/: [list of files].
SDE calculator output: [available at path / not available].
Write your analysis to [path]/_dd-working/financial-analyst.md following your output contract."
```

**For `listing-reviewer`:**
```
Launch agent "listing-reviewer" with prompt:
"Review the listing and broker documents for due diligence. The deal folder is at [path].
Confidential/broker documents: [list from confidential/].
Listing reviews: [list of listing-review-*.md files].
Financial documents are available in financials/ for cross-reference.
Write your analysis to [path]/_dd-working/listing-reviewer.md following your output contract."
```

**For `market-researcher` (CRITICAL — different context passing):**
```
Launch agent "market-researcher" with prompt:
"Research the market and community reputation for this business:
- Business name: [name extracted from listing/CIM/folder name]
- Industry: [industry type]
- Location: [city, state]
- Additional context: [any non-financial details about the business]

DO NOT search for any financial information. Return your findings following your output contract."
```

**CRITICAL:** The `market-researcher` agent receives ONLY the business name, industry, and location. NEVER pass financial data, revenue, SDE, margins, or asking price to this agent. This is the confidentiality boundary.

After launching, inform the user:

> "Launched [N] agents in parallel:
> - Financial analyst: analyzing P&L, balance sheet, and SDE data
> - Listing reviewer: extracting business facts from broker materials
> - Market researcher: researching industry trends and online reputation
>
> This may take a few minutes..."

## Step 9: Collect Results

As agents complete, note which ones finished successfully. If the `market-researcher` returns results inline (since it has no Write tool), write its output to `_dd-working/market-research.md` yourself.

**If an agent fails or returns no output:** Inform the user which agent failed, then continue with the agents that succeeded. The synthesizer will work with whatever results are available. For example: "The market researcher agent did not return results. Proceeding with financial analysis and listing review only — Section 2 (Market Analysis) will be omitted from the DD report."

## Step 10: Launch Synthesizer

After ALL agents have completed, launch the `dd-synthesizer` agent:

```
Launch agent "dd-synthesizer" with prompt:
"Synthesize the complete due diligence report. The deal folder is at [path].
Agent outputs are in [path]/_dd-working/. Read all .md files there.
Also check for sde-calculator.md and deal-box.md in the deal folder.
Write the complete due-diligence.md to [path]/due-diligence.md.
The business name is [name]. Today's date is [date]."
```

## Step 11: Clean Up

After the synthesizer completes:
1. Verify `due-diligence.md` was written successfully
2. Optionally clean up `_dd-working/` (or leave it for reference — it's gitignored)

## Step 12: Summary

Present the final summary to the user:

> "Due diligence analysis complete. Report written to `due-diligence.md`."
>
> **Business:** [name]
> **Agents used:** [list]
> **Sections produced:** [list which of 1-9 were populated]
> **Key findings:** [2-3 bullet headline findings from the report]
>
> "Next steps:
> - Review the report and run `/deal:notes` to add broker call insights
> - Run `/deal:calc` to model the deal financials
> - Run `/deal:dd` again after adding new documents to refresh the analysis"
