---
name: help
description: >
  Shows available deal plugin commands, recommended workflow, and quick-start
  guide. Use when the user asks for help with the deal plugin or runs /deal:help.
---

# Deal Plugin — Acquisition Due Diligence Toolkit

## Commands

| Command | Description |
|---------|-------------|
| `/deal:box` | Create or update your buyer profile (acquisition criteria) |
| `/deal:listing` | Review a business listing (URL, file, or pasted content) |
| `/deal:sde` | Calculate SDE with blind dual-agent verification |
| `/deal:dd` | Run full multi-agent due diligence analysis |
| `/deal:notes` | Add notes to update an existing DD analysis |
| `/deal:calc` | Model deal financials (Year 1 pro forma) |
| `/deal:help` | Show this help guide |

## Quick Start

1. Create a deal folder and add financial documents:
   ```
   mkdir acme-hardware/financials
   # Drop P&L files (.pdf, .xlsx, .csv) into financials/
   ```

2. Run SDE calculation:
   ```
   cd acme-hardware
   /deal:sde
   ```

3. Run full due diligence:
   ```
   /deal:dd
   ```

4. Model the deal:
   ```
   /deal:calc
   ```

## Recommended Workflow

```
/deal:box          Create buyer criteria (optional, do anytime)
     |
/deal:listing      Review a listing you found online
     |
  [Add financials to deal folder]
     |
/deal:sde          Calculate verified SDE from P&L documents
     |
/deal:dd           Full due diligence (financial + market + synthesis)
     |
/deal:notes        Add broker call notes, site visit observations
     |
/deal:calc         Model purchase price, financing, and returns
```

Commands work independently — you can start anywhere. Each command checks for outputs from prior commands and uses them if available.

## Deal Folder Structure

```
my-acquisitions/           # Your project root
├── deal-box.md            # Buyer profile (one per project)
├── acme-hardware/      # One folder per deal
│   ├── financials/        # Drop P&Ls, balance sheets here
│   ├── confidential/      # Broker documents (CIM, etc.)
│   ├── sde-calculator.md  # Output from /deal:sde
│   ├── due-diligence.md   # Output from /deal:dd
│   └── deal-calculator.md # Output from /deal:calc
└── another-deal/
    └── ...
```

## Privacy & Confidentiality

- All output files are **gitignored by default** (they contain confidential financial data)
- Web research agents have **no access to financial documents** — they only see the business name and location
- Web searches are **opt-in** — you're asked for permission with a privacy disclosure before any searches
- All output files include a **confidentiality header** reminding you of NDA obligations
