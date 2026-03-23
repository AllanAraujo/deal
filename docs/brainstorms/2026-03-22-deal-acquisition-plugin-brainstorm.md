---
title: Deal Acquisition Due Diligence Plugin
date: 2026-03-22
status: active
type: brainstorm
---

# Deal Acquisition Due Diligence Plugin

## What We're Building

A public Claude Code plugin (`/deal` namespace) that helps business acquirers and aspiring business purchasers perform structured due diligence. The plugin provides 6 commands that form a complete acquisition analysis workflow -- from defining buyer criteria through financial analysis to deal structuring.

**Target audience:** Business buyers using Claude Code, distributed via the plugin marketplace.

### Commands

1. **`/deal box`** -- Interactive buyer profile creator. Walks the user through quantitative criteria (cash flow requirements, operator salary, financing assumptions, price range) and qualitative criteria (industry, geography, team size, management structure, must-haves, deal breakers). Outputs `deal-box.md` at the project root. Used as the comparison baseline for all other commands.

2. **`/deal listing`** -- Listing review agent. Accepts a URL, file path, or pasted content. Performs a high-level review of a business listing and compares it against the deal box profile. Highlights overlaps and divergences, recommends whether to reach out to the broker (with reasons), and auto-drafts an intro email if recommended.

3. **`/deal sde`** -- SDE calculator. Agent 1 reviews all P&L documents in the deal folder and builds an SDE calculation (based on the SDE template spec). Agent 2 independently rebuilds the SDE from scratch without seeing Agent 1's output, then reconciles differences. Final output flags any discrepancies between the two calculations.

4. **`/deal dd`** -- Due diligence analysis. Spins up parallel agents based on available materials:
   - Market/industry analysis (web research - asks permission first)
   - Social reviews & community standing (web research - asks permission first)
   - P&L financial analysis
   - Balance sheet analysis
   - SDE-to-valuation analysis (if `/deal sde` has been run)
   - Confidential materials review (if broker docs exist)
   - Synthesizer agent (runs after all others complete) -- creates DD questions for broker discovery call

   Agents run only if source material exists. Synthesizer works with whatever results come back.

5. **`/deal notes`** -- Add notes/insights that trigger a DD document refresh. User provides notes (broker call takeaways, site visit observations, etc.), and the DD document gets re-evaluated in light of the new information. Single-agent architecture -- surgical update, not a full rebuild. Maintains a revision trail within the document.

6. **`/deal calc`** -- Comprehensive deal analysis and pro forma. Interactive questionnaire covering:
   - Acquisition info (purchase price, DSCR tax rate, closing costs, real estate, working capital)
   - Funding sources breakdown (SBA loan, seller note, cash, other -- each with rate/term)
   - SDE integration (option to import from `/deal sde` output if available)
   - Output: Key metrics (Year 1 net cash flow, DSCR, purchase multiple, cash-on-cash return, payback period), financing structure, P&L summary, SDE calculation, and comparison against deal box criteria.

### All command outputs are markdown files.

## Why This Approach

### Full Plugin Architecture (plugin.json + skills/ + agents/)
- **Agent reuse**: Financial analysis agents serve both `/deal sde` and `/deal dd`. Market research agents serve both `/deal dd` and `/deal listing`.
- **Marketplace distribution**: Public plugin installable by any Claude Code user.
- **Separation of concerns**: Agent definitions (domain expertise) are separate from skill files (workflow orchestration).
- **Scalable**: Easy to add new commands or agents without restructuring.

### Deal-Per-Folder File Organization
```
my-acquisitions/                # project root
├── deal-box.md                 # buyer profile (one per project)
├── lake-lure-marine/           # deal folder
│   ├── financials/             # user drops P&Ls, balance sheets here
│   ├── listing-review.md       # output of /deal listing
│   ├── sde-calculator.md       # output of /deal sde
│   ├── due-diligence.md        # output of /deal dd, updated by /deal notes
│   └── deal-calculator.md      # output of /deal calc
└── coastal-hvac/
    └── ...
```

- User cd's into a deal folder and runs commands from there.
- Commands auto-discover `deal-box.md` by traversing up the directory tree.
- `/deal box` is smart: if invoked from inside a deal subfolder, it traverses up and creates `deal-box.md` at the project root (not inside the deal folder).

## Key Decisions

1. **Plugin namespace**: `/deal` -- short, action-oriented, intuitive.
2. **File organization**: Deal-per-folder. Each business gets its own directory. Commands run from within and output there.
3. **Deal box location**: Project root, found via upward directory traversal (like git finds `.git/`).
4. **Listing input**: Accepts URLs, file paths, or copy-pasted content. Flexible input handling.
5. **DD agent strategy**: Run only agents that have source material available. Gracefully degrade for early-stage deals.
6. **SDE verification**: Blind rebuild + reconciliation. Agent 2 builds independently first, then compares against Agent 1's output. Most thorough approach.
7. **Notes architecture**: Single agent, triggers DD refresh with revision trail. No multi-agent overhead for surgical updates.
8. **Web research**: Agents ask user permission before making web searches/fetches. Privacy-conscious for a public plugin.
9. **Architecture**: Full plugin (plugin.json + skills/ + agents/) for marketplace distribution and agent reuse.
10. **Deal box editing**: Partial updates. Detects existing profile and asks which section to change.
11. **DD versioning**: Overwrite + changelog. Revision history maintained at the bottom of the document.
12. **Forecasting scope**: Year 1 only for v1. Multi-year projections deferred.
13. **Broker email**: Contextual drafting, no user template. Each email tailored to the specific listing and deal box.

## Deal Box Schema (from BizScout DealOS reference)

### Quantitative Criteria
- **Personal Requirements**: Required personal cash flow ($)
- **Operator Settings**: Operator salary ($), payroll tax rate (%), benefits rate (%)
- **Financing Assumptions**: Financing percentage (%), interest rate (%), term (years), min DSCR
- **Purchase Information**: Purchase price multiple, assumed purchase price ($)
- **Asking Price Range**: Minimum ($), maximum ($)

### Qualitative Criteria
- **Industry Preferences**: Target industries (multi-select from ~20 categories), excluded industries
- **Geographic Preferences**: US/international, state+city combinations
- **Team Size**: No preference through Enterprise (>100)
- **Financing Options**: Own cash, SBA, other loan, seller financing, home equity, ROBS 401(k), investors, friends & family, other
- **Years in Business**: No preference, 2+, 5+, 10+, 20+
- **Management Structure**: Owner operated, general manager, ops manager, department managers, absentee owner, management team, self-managing staff
- **Must-haves**: Free text
- **Deal breakers**: Free text

## Deal Calculator Schema (from BizScout DealOS reference)

### Inputs
- Purchase price, DSCR tax rate
- Yes/No: closing costs, real estate, working capital, working capital loan, minimum cash flow requirement, hire new operator
- Financing sources (multiple): type, rate, term, amount
- SDE import (optional, from /deal sde output)

### Key Metrics Output
- Net Cash Flow (Year 1)
- DSCR (Debt Service Coverage Ratio)
- Purchase Multiple
- Cash-on-Cash Return
- Payback Period

### Sections
- Deal details, financing structure, P&L summary, SDE calculation

## SDE Calculator Schema (from Excel template)
- Net Income
- + Depreciation & Amortization
- + Interest
- + Corporate/LLC Taxes
- + Owner Benefits (salary, personal expenses, etc.)
- = Total SDE
- SDE Margin (%)

## Due Diligence Document Template (from Lake Lure Marine reference)

The DD document is the core output of `/deal dd` and the document updated by `/deal notes`. It follows this section structure, with each section mapped to the agent that produces it:

### Section 1: Business Overview
**Agent:** Listing/confidential materials agent
- Key facts table (entity type, owner, location, market share, employees, capacity, real estate, asking price, broker-stated SDE, reason for sale)
- Business description narrative
- Products/services offered

### Section 2: Market Analysis
**Agent:** Market research agent (web search - asks permission)
- **2.1 Local/micro-market analysis** -- geographic, regulatory, competitive dynamics
- **2.2 Critical risk factors** -- any major events impacting the business (natural disasters, regulatory changes, market disruptions)
- **2.3 National/industry trends** -- broader industry data, growth rates, headwinds/tailwinds
- Net market assessment

### Section 3: Financial Analysis
**Agent:** P&L financial analyst agent
- **3.1 Data sources & accounting notes** -- what documents were reviewed, accounting basis differences, reconciliation notes
- **3.2 Revenue & profitability** -- multi-year summary table (revenue, COGS, gross profit, margins, operating expenses, net income)
- **3.3 Revenue mix** -- breakdown by category with margin profiles
- **3.4 Critical financial findings** -- any errors, discrepancies, or notable discoveries (e.g., double-counting, accounting inconsistencies)
- **3.5 Normalized SDE** -- multiple approaches (conservative, moderate, aggressive) with defensible range. If a broker-provided SDE exists, reference and compare it here, but broker SDE is not required
- **3.8 SDE trend analysis** -- year-over-year drivers of change
- **3.9 Balance sheet analysis** -- assets, liabilities, equity comparison across available years
- **3.10 Revenue breakdown detail** -- granular category analysis
- **3.11 Quick-reference summary** -- headline numbers table + talking points for conversations with lenders/partners

### Section 4: SDE Detailed Build-Up
**Agent:** SDE valuation agent (uses `/deal sde` output if available)
- **4.1–4.N SDE calculation per year** -- line-by-line build-up tables with source verification status
- **4.N+1 Weighted average SDE** -- with weighting methodology explanation
- **4.N+2 Valuation at asking price** -- implied multiples at various SDE bases, comparison to industry multiples

### Section 5: Key Strengths
**Agent:** Synthesizer agent (compiles from all other agents)
- Numbered list of business strengths with supporting evidence

### Section 6: Key Risks & Concerns
**Agent:** Synthesizer agent
- Numbered list of risks with specific detail and magnitude assessment

### Section 7: Due Diligence Questions for the Broker
**Agent:** Synthesizer agent
- **Financial & tax questions** -- gaps, inconsistencies, missing data
- **Real estate questions** -- ownership, inclusion in sale, lease terms
- **Operations & franchise questions** -- transferability, certifications, transition
- **Market & customer questions** -- concentration, trends, competitive landscape
- **Event-specific questions** -- (if applicable) disaster recovery, regulatory changes
- **Legal & compliance questions** -- environmental, licensing, litigation, insurance

### Section 8: Recommended Next Steps
**Agent:** Synthesizer agent
- Prioritized action items with rationale

### Section 9: Preliminary Valuation Summary
**Agent:** Synthesizer agent
- Scenario table (bear/conservative/base/bull) with SDE basis, multiple, implied value, and comparison to asking price
- Bottom-line narrative assessment
- Key remaining questions

### Revision History (maintained by `/deal notes`)
- Dated entries showing what changed, why, and which sections were re-evaluated

## Open Questions

1. **Plugin directory structure**: Should agents be organized by domain (financial/, market/, etc.) or flat? Need to decide during planning.

## Resolved Questions

1. **Deal box updates**: Partial updates supported. `/deal box` detects an existing profile and asks which section to update rather than re-walking the full questionnaire.
2. **DD re-run behavior**: Overwrite + changelog. The `due-diligence.md` file is overwritten but maintains a revision history section at the bottom showing what changed and when.
3. **Deal calc forecasting**: Year 1 only for initial version. Multi-year forecasting deferred as a future enhancement.
4. **Broker email template**: Contextual default. The agent drafts each email based on listing details and deal box profile -- no user-maintained template file needed.
