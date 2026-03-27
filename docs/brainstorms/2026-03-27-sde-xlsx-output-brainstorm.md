---
title: SDE XLSX Output — Working Spreadsheet Alongside Markdown
date: 2026-03-27
status: active
type: brainstorm
---

# SDE XLSX Output — Working Spreadsheet Alongside Markdown

## What We're Building

Enhance `/deal:sde` to produce a working Excel spreadsheet (`sde-calculator.xlsx`) alongside the existing `sde-calculator.md`. The XLSX follows the user's existing SDE Calculator template structure and includes:

- All SDE values populated from the dual-agent analysis
- Excel formulas preserved (Net Income, Basic SDE, Total SDE, Weighted Average)
- Cell comments with source citations AND verification status from the reconciliation
- Editable cells so users can toggle add-backs and adjust values interactively

The XLSX is generated on every `/deal:sde` run (not opt-in).

## Why This Approach

### Template-based generation (ship blank XLSX, copy and fill)

- **Exact formatting preserved** — The user's template has specific column widths, cell formatting, and structure that would be tedious to recreate programmatically.
- **Predictable output** — Copying a known template and filling cells is more reliable than generating from scratch.
- **Easy to update** — If the template changes, swap the file. No code changes needed.
- **Formula integrity** — Excel formulas (SUM, weighted average) remain intact in the template. Only data cells are filled by the script.

## Template Structure (Single Sheet: SDE Calculator)

```
Row  | A (Category)                          | B (Year 1) | C (Year 2) | D (Year 3) | E (Weighted Avg)
-----|---------------------------------------|------------|------------|------------|------------------
1    | Category                              | [year]     | [year]     | [year]     | Weighted Average
2    | Weighting %                           | [%]        | [%]        | [%]        |
3    | Sales                                 | $value     | $value     | $value     |
4    | Less COGS (negative)                  | ($value)   | ($value)   | ($value)   |
5    | Less OpEx (negative)                  | ($value)   | ($value)   | ($value)   |
6    | = NET INCOME BEFORE TAXES             | =SUM(B3:B5)| formula    | formula    |
7    | + Depreciation & Amortization         | $value     | $value     | $value     |
8    | + Interest on Loans                   | $value     | $value     | $value     |
9    | + Corporate / LLC Taxes               | $value     | $value     | $value     |
10   | + Salary for One Owner                | $value     | $value     | $value     |
11   | + Payroll Taxes on Owner's Salary     | $value     | $value     | $value     |
12   | = BASIC DISCRETIONARY EARNINGS        | formula    | formula    | formula    |
15-39| Additional add-backs/deductions       | $value     | $value     | $value     |
40   | = SUM OF ADDITIONS/DELETIONS          | formula    | formula    | formula    |
41   | = TOTAL SDE                           | formula    | formula    | formula    | =weighted formula
```

**Owner Income sheet excluded** — that analysis belongs in `/deal:calc`.

## Cell Annotation Strategy

Every populated value cell (not formula cells) gets an Excel comment with:

```
Source: [document name], [specific line item]
Status: [Direct | Verified | Estimated | Disputed]
Note: [optional — e.g., "Agent 1: $74,407. Agent 2: $74,407. Agreed."]
Ref: sde-calculator.md Section 4.[N]
```

**Status values:**
- **Direct** — Figure taken directly from one source document
- **Verified** — Cross-referenced against multiple documents (e.g., P&L matches tax return)
- **Estimated** — No direct source; analyst's estimate (e.g., CapEx reserve)
- **Disputed** — Agent 1 and Agent 2 disagreed; reconciled figure shown, see md for details

## Key Decisions

1. **Always generate both files** — Every `/deal:sde` run produces `sde-calculator.md` AND `sde-calculator.xlsx`. No opt-in toggle.
2. **SDE Calculator sheet only** — Owner Income scenario analysis belongs in `/deal:calc`, not here.
3. **Template-based generation** — Ship a blank template XLSX with the plugin. Copy it, fill values with Python/openpyxl. Preserves formatting and formulas.
4. **Rich cell annotations** — Source citation + verification status + agent reconciliation notes + cross-reference to md section.
5. **Formulas stay intact** — Only data cells (rows 3-5, 7-11, 15-39, row 2 weights) are filled. Formula cells (rows 6, 12, 40, 41) are left as-is.
6. **openpyxl dependency** — Plugin requires Python 3 + openpyxl. The SDE skill runs a Python script via Bash to fill the template.

## Generation Flow

```
/deal:sde runs
  ├── Agent 1 + Agent 2 produce SDE calculations (existing flow)
  ├── Orchestrator reconciles and writes sde-calculator.md (existing flow)
  └── NEW: Orchestrator runs scripts/fill-sde-xlsx.py
       ├── Copies template from plugin assets to deal folder
       ├── Reads reconciled SDE data (from md or structured agent output)
       ├── Fills value cells with data
       ├── Adds cell comments with source/verification/cross-ref
       └── Saves as sde-calculator.xlsx in the deal folder
```

## Plugin File Changes

```
deal/
├── assets/
│   └── sde-template.xlsx          # Blank template (copied for each deal)
├── scripts/
│   └── fill-sde-xlsx.py           # Python script to fill the template
├── skills/sde/SKILL.md            # Updated to invoke the script after reconciliation
└── .gitignore                     # Add *.xlsx to output patterns
```

## Open Questions

*None — all resolved during brainstorm.*

## Resolved Questions

1. **When to generate?** Always, alongside the md. No opt-in.
2. **Which sheets?** SDE Calculator only. Owner Income belongs in /deal:calc.
3. **What annotations?** Source citation + verification status (both).
4. **How to generate?** Ship template XLSX, copy and fill with Python/openpyxl.
