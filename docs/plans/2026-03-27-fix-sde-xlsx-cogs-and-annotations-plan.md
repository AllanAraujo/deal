---
title: "fix: SDE XLSX missing COGS and incomplete annotations"
type: fix
status: completed
date: 2026-03-27
---

# Fix: SDE XLSX Missing COGS and Incomplete Annotations

## Problem

Two bugs in the SDE XLSX output:

1. **COGS (and Sales, OpEx) missing from XLSX.** The SDE agents output starting from Net Income, but the XLSX template expects Sales (row 3), COGS (row 4), and Operating Expenses (row 5) as separate values — row 6 is a formula `=SUM(B3:B5)`. With rows 3-5 empty, the Net Income formula shows $0.

2. **Add-back section has no cell annotations.** The JSON example in `skills/sde/SKILL.md` only demonstrates annotations for standard rows (`sales`, `depreciation`, `interest`). The orchestrator follows the example and omits annotations for add-backs. The user expects every populated cell to have a source citation and verification status.

## Root Cause

**Bug 1:** The SDE agent output format (`agents/financial-sde-builder.md:54-65`) starts with Net Income as the first line item. It never separately extracts Sales, COGS, and Operating Expenses from the P&L. The orchestrator has no data for these fields when building the JSON.

**Bug 2:** The SKILL.md Step 7b JSON example shows only 3 annotation entries (all for standard rows). There is no instruction telling the orchestrator to annotate EVERY populated cell, including add-backs.

## Fix

### 1. Update SDE agent output format to include Sales/COGS/OpEx breakdown

**Files:** `agents/financial-sde-builder.md`, `agents/financial-sde-verifier.md`

Add three rows ABOVE Net Income in the required output table:

```
| Item | Amount | Source | Verified? |
|------|--------|--------|-----------|
| Revenue/Sales | $XXX | [P&L top line] | Direct |
| Less: COGS | ($XXX) | [P&L COGS line] | Direct |
| Less: Operating Expenses | ($XXX) | [P&L OpEx line] | Direct |
| Net Income | $XXX | [P&L bottom line or =Revenue-COGS-OpEx] | Direct |
| + Owner's Compensation | ... |
```

Add instruction: "If the P&L does not break out COGS or Operating Expenses separately, note this and provide the best available breakdown. If only Net Income is available, set Sales = Net Income and COGS = 0, OpEx = 0 with status 'Estimated'."

### 2. Update SKILL.md JSON example with complete annotations

**File:** `skills/sde/SKILL.md` (Step 7b)

- Expand the JSON example to show annotations for EVERY row type including add-backs
- Add explicit instruction: "Annotate EVERY populated value cell — standard rows AND add-backs. Every number in the XLSX should have a source citation."
- Show an add-back annotation example:

```json
"annotations": {
  "sales": { "2023": {"source": "2023 P&L: Gross Receipts", "status": "Direct", "ref": "Section 4.1"} },
  "cogs": { "2023": {"source": "2023 P&L: Cost of Goods Sold", "status": "Direct", "ref": "Section 4.1"} },
  "opex": { "2023": {"source": "2023 P&L: Total Expenses", "status": "Direct", "ref": "Section 4.1"} },
  "depreciation": { "2023": {"source": "2023 P&L: Depreciation", "status": "Direct", "ref": "Section 4.1"} },
  "Auto/Truck (Owner Benefit)": { "2023": {"source": "2023 P&L: Expedition expense", "status": "Direct", "ref": "Section 4.1"} },
  "Maintenance CapEx Reserve": { "2023": {"source": "Estimated at 2% of revenue", "status": "Estimated", "ref": "Section 4.1"} }
}
```

### 3. Update deal-knowledge skill SDE output format

**File:** `skills/deal-knowledge/SKILL.md`

Add Sales, COGS, and OpEx to the SDE output format template so agents referencing this skill see the complete format.

## Acceptance Criteria

- [x] XLSX rows 3-5 (Sales, COGS, OpEx) are populated when P&L data is available
- [x] XLSX row 6 formula (`=SUM(B3:B5)`) calculates correctly
- [x] Every populated value cell in the XLSX has a cell comment (standard rows AND add-backs)
- [x] Agent output format includes Revenue/Sales, COGS, and OpEx as separate line items above Net Income
- [x] If P&L doesn't break out COGS/OpEx, the agent notes this with "Estimated" status

## References

- Python script (no changes needed — already handles `cogs`, `opex` keys): `scripts/fill-sde-xlsx.py:25-36`
- SDE agent output format: `agents/financial-sde-builder.md:54-90`
- SKILL.md JSON example: `skills/sde/SKILL.md:200-234`
- Domain knowledge SDE format: `skills/deal-knowledge/SKILL.md:74-113`
