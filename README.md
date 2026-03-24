# Deal — Acquisition Due Diligence Plugin for Claude Code

A Claude Code plugin that helps business acquirers perform structured due diligence using multi-agent AI analysis. From reviewing listings to calculating SDE to generating comprehensive DD reports.

## Installation

```bash
claude plugin install deal
```

## Commands

| Command | Description |
|---------|-------------|
| `/deal:box` | Create or update buyer acquisition criteria |
| `/deal:listing` | Review a business listing (URL, file, or pasted text) |
| `/deal:sde` | Calculate SDE with blind dual-agent verification |
| `/deal:dd` | Run multi-agent due diligence analysis |
| `/deal:notes` | Add notes to update an existing DD report |
| `/deal:calc` | Model deal financials and Year 1 pro forma |
| `/deal:help` | Show available commands and workflow guide |

## Quick Start

```bash
# 1. Create a deal folder and add financial documents
mkdir -p my-deal/financials
# Copy P&L files (.pdf, .xlsx, .csv) into financials/

# 2. Start Claude Code in the deal folder
cd my-deal
claude

# 3. Run SDE calculation (two agents independently verify)
/deal:sde

# 4. Run full due diligence
/deal:dd

# 5. Model the deal
/deal:calc
```

## Workflow

```
/deal:box             Set up your buyer criteria (optional, anytime)
     |
/deal:listing [URL]   Review a listing you found
     |
  [Add financials to deal folder]
     |
/deal:sde             Verified SDE calculation
     |
/deal:dd              Full DD report (financial + market + synthesis)
     |
/deal:notes           Add broker call notes, refine the DD
     |
/deal:calc            Model purchase price, financing, returns
```

Commands are independent — start anywhere. Each checks for prior outputs and uses them when available.

## What Each Command Does

### `/deal:sde` — SDE Calculator

Launches two independent agents to calculate Seller's Discretionary Earnings from your P&L documents. Agent 2 works blind (never sees Agent 1's output), then the results are reconciled line-by-line. Catches add-back errors, double-counting, and categorization mistakes.

### `/deal:dd` — Due Diligence Analysis

Discovers available materials and launches specialized agents in parallel:
- **Financial analyst** — P&L trends, revenue mix, balance sheet, SDE valuation
- **Market researcher** — Industry trends, online reviews, competitive landscape
- **Listing reviewer** — Business overview from broker materials
- **Synthesizer** — Combines all findings into strengths, risks, broker questions, valuation

Produces a comprehensive DD document (typically 400-600 lines) with 9 sections.

### `/deal:calc` — Deal Calculator

Interactive financial modeling with pre-fill from existing artifacts. Supports multiple funding sources (SBA, seller note, cash). Calculates DSCR, purchase multiple, cash-on-cash return, and payback period. Compares against your deal box criteria.

### `/deal:listing` — Listing Review

Accepts a URL, file path, or pasted listing content. Extracts key facts, compares against your deal box criteria, recommends whether to pursue, and drafts a broker intro email.

### `/deal:box` — Buyer Profile

Interactive questionnaire for your acquisition criteria: cash flow requirements, financing assumptions, industry preferences, geographic focus, deal breakers. Used by other commands for comparison.

### `/deal:notes` — DD Refresh

After a broker call or site visit, add your notes and the DD document gets surgically updated. Maintains a revision trail so you can track how the analysis evolved.

## Deal Folder Structure

```
my-acquisitions/
├── deal-box.md              # Buyer profile (project root)
├── acme-hardware/        # One folder per deal
│   ├── financials/          # P&Ls, balance sheets, tax returns
│   ├── confidential/        # Broker docs (CIM, packages)
│   ├── sde-calculator.md    # /deal:sde output
│   ├── due-diligence.md     # /deal:dd output
│   └── deal-calculator.md   # /deal:calc output
└── another-deal/
    └── ...
```

## Privacy & Security

This plugin handles sensitive financial data. Key protections:

- **Confidentiality boundary.** Financial analysis agents cannot access the web. Market research agents cannot access financial files. Enforced at the agent tools level, not just by prompts.
- **Web search is opt-in.** You're asked for permission before any web searches, with a disclosure that searches create a discoverable record of your interest in the business.
- **Financial data never leaves the financial zone.** Web search agents receive only the business name, industry, and location — never revenue, margins, SDE, or asking price.
- **All output files are gitignored.** The plugin generates a `.gitignore` that excludes financial documents, broker materials, and all analysis output files by default.
- **Confidentiality headers.** Output files include a reminder about NDA obligations.

## Supported File Formats

The financial agents can read:
- PDF (`.pdf`)
- Excel (`.xlsx`, `.xls`)
- CSV (`.csv`)
- Plain text (`.txt`, `.md`)

For best results, use the original P&L exports from QuickBooks, Xero, or your CPA.

## License

MIT
