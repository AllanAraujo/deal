---
name: deal-knowledge
description: Domain knowledge for business acquisition due diligence — SDE methodology, add-back categories, valuation benchmarks, and DD document structure. Loaded by financial agents for reference.
user-invocable: false
---

# Deal Acquisition Domain Knowledge

## SDE (Seller's Discretionary Earnings) Methodology

SDE is the standard valuation metric for owner-operated small businesses. It represents the total financial benefit available to a single owner-operator.

### SDE Calculation Structure

```
  Revenue/Sales (from P&L top line)
- Cost of Goods Sold (COGS)
- Operating Expenses
= Net Income (from P&L, or calculated as Revenue - COGS - OpEx)

+ Owner's Compensation (ONLY if expensed on the P&L — see critical note below)
+ Depreciation & Amortization
+ Interest Expense
= Basic SDE

+ Owner Benefit Add-Backs (see categories below)
+ Non-Recurring Expense Add-Backs
- Non-Recurring Income Deductions
- Maintenance CapEx Reserve (estimated if no CapEx schedule provided)
= Total SDE

SDE Margin = Total SDE / Total Revenue × 100
```

### Critical Note: Owner Compensation

Owner compensation is ONLY added back if it was deducted as an expense on the P&L. In many sole proprietorships and LLCs, owners take draws from equity rather than paying themselves a salary — in these cases, compensation is NOT on the P&L and there is NO add-back. Always verify against Schedule C, tax returns, and the actual P&L entries. Look for year-end reversals where CPAs zero out monthly salary entries.

### SDE Add-Back Categories

**Standard Add-Backs (always check for):**

| Category | Description | Examples |
|----------|-------------|---------|
| **Owner's Compensation** | Salary, wages, bonuses expensed on P&L | W-2 wages, management fees (only if deducted) |
| **Depreciation & Amortization** | Non-cash charges | Straight-line, MACRS, Section 179 elections |
| **Interest Expense** | Cost of existing debt (buyer will have their own) | Bank loans, lines of credit, equipment financing |

**Owner Benefit Add-Backs (case-by-case):**

| Category | Description | Look For |
|----------|-------------|----------|
| **Auto/Truck** | Personal vehicle expenses run through business | Named vehicles (e.g., "Expedition"), auto insurance |
| **Health Insurance** | Owner's personal health coverage | Health insurance line items, HSA contributions |
| **Life/Disability Insurance** | Owner's personal policies | Insurance expenses beyond business liability |
| **Meals & Entertainment** | Personal meals charged to business | Meals line, entertainment, client entertainment |
| **Travel** | Personal travel charged to business | Non-business travel, family trips |
| **Donations** | Charitable giving through business | Donations, contributions |
| **Gifts** | Personal gifts charged to business | Gift line items, holiday gifts above normal |
| **Personal Expenses** | Any personal cost run through business | Cell phone, home office, subscriptions |
| **Unclassified Expenses** | CPA catch-all categories | "Ask My Accountant", uncategorized expenses |

**Non-Recurring Items (deduct or add back):**

| Type | Action | Examples |
|------|--------|---------|
| Non-recurring income | Deduct from SDE | PPP loan forgiveness, insurance settlements, government grants, one-time asset sales |
| Non-recurring expenses | Add back to SDE | Lawsuit settlements, one-time moving costs, natural disaster costs, startup costs |

**Estimated Adjustments:**

| Item | When to Apply | Typical Range |
|------|---------------|---------------|
| Maintenance CapEx Reserve | When no CapEx schedule is provided | 1-5% of revenue, depending on asset intensity |
| Rent Adjustment | If owner owns real estate and charges below/above market | Adjust to market rate |
| Salary Adjustment | If key employee is underpaid/overpaid vs. market | Adjust to market rate |

### SDE Output Format (Required for All SDE Calculations)

Every SDE calculation MUST use this table format for each year analyzed:

```markdown
### SDE Calculation — [Year] ([Context Note])

| Item | Amount | Source | Verified? |
|------|--------|--------|-----------|
| Revenue/Sales | $XXX,XXX | [P&L: Gross Receipts/Sales] | Direct |
| Less: COGS | ($XXX,XXX) | [P&L: Cost of Goods Sold] | Direct |
| Less: Operating Expenses | ($XXX,XXX) | [P&L: Total Expenses] | Direct |
| **Net Income** | **$XXX,XXX** | [P&L bottom line or calculated] | Direct |
| + Owner's Compensation | $X | [Explanation of why/why not] | Verified/Direct |
| + Depreciation & Amortization | $X | [P&L line item] | Direct |
| + Interest Expense | $X | [P&L line item] | Direct/Missing |
| **Basic SDE** | **$XXX,XXX** | | |
| + [Add-back item] | $X | [Source] | Direct/Estimated |
| – [Non-recurring deduction] | ($X) | [Source] | Direct |
| – Maintenance CapEx Reserve | ($X) | Estimated | Est. |
| **Total SDE** | **$XXX,XXX** | | |
```

**Verification status values:**
- **Direct** — Figure taken directly from a source document
- **Verified** — Cross-referenced against multiple documents (e.g., P&L vs. tax return)
- **Estimated** — No direct source; analyst's reasonable estimate with stated methodology
- **Missing** — Expected data not found in provided documents; flagged for broker follow-up

### Multi-Year SDE Summary

After per-year calculations, provide a weighted average:

```markdown
### Weighted Average SDE

| Year | SDE | Weight | Weighted Value | Rationale |
|------|-----|--------|----------------|-----------|
| [Oldest] | $XXX | X% | $XX,XXX | [Why this weight] |
| [Middle] | $XXX | X% | $XX,XXX | [Why this weight] |
| [Recent] | $XXX | X% | $XX,XXX | [Why this weight] |
| **Weighted Average** | | | **$XXX,XXX** | |
```

Typical weighting: more recent years weighted higher (e.g., 20/30/50 or 25/35/40). Adjust if a year is anomalous (e.g., hurricane, COVID, one-time event).

## Valuation Benchmarks

### Small Business Valuation Multiples by Industry

| Industry | Typical SDE Multiple | Notes |
|----------|---------------------|-------|
| Service businesses (general) | 2.0x – 3.5x | Higher for recurring revenue |
| Marine/boat dealers | 2.0x – 3.0x | Asset-dependent, seasonal |
| HVAC/plumbing/electrical | 2.5x – 4.0x | Recurring maintenance contracts add value |
| Restaurants/food service | 1.5x – 2.5x | High failure rate suppresses multiples |
| Manufacturing | 3.0x – 5.0x | Equipment value, customer contracts |
| Professional services | 2.0x – 4.0x | Key-person risk reduces multiples |
| E-commerce | 2.5x – 4.0x | Growth rate dependent |
| Franchises | 2.0x – 3.5x | Brand value, but franchise fees reduce SDE |
| Healthcare practices | 3.0x – 6.0x | Regulated, high barriers to entry |
| Landscaping/home services | 2.0x – 3.0x | Seasonal, labor-intensive |

**Multiple adjusters (increase or decrease from baseline):**
- Recurring/contract revenue → +0.5x to +1.0x
- Owner-dependent (key person risk) → -0.5x to -1.0x
- Growing vs. declining revenue → +/- 0.5x
- Real estate included → may justify higher total price
- Asset-heavy business → floor value based on tangible assets
- Single customer concentration (>25%) → -0.5x

### SDE vs. EBITDA

For businesses under $5M in value, SDE is the standard metric. EBITDA is used for larger businesses where the owner is not the operator.

| Metric | Use When | Includes Owner Comp? |
|--------|----------|---------------------|
| SDE | Owner-operated, sub-$5M deals | Yes (adds back ALL owner compensation) |
| EBITDA | Manager-run, $5M+ deals | No (only adds back one market-rate salary) |

## DD Document Structure (9 Sections)

The due diligence document follows this section structure:

1. **Business Overview** — Key facts table, narrative, products/services
2. **Market Analysis** — Local micro-market, critical risk factors, national/industry trends
3. **Financial Analysis** — Data sources, revenue/profitability, revenue mix, critical findings, normalized SDE, SDE trends, balance sheet, revenue breakdown, financier quick-reference
4. **SDE Detailed Build-Up** — Per-year line-by-line tables with verification status, weighted average, valuation at asking price
5. **Key Strengths** — Numbered list with supporting evidence
6. **Key Risks & Concerns** — Numbered list with specific detail and magnitude
7. **Due Diligence Questions for the Broker** — Organized by category: Financial/Tax, Real Estate, Operations, Market/Customer, Legal/Compliance
8. **Recommended Next Steps** — Prioritized action items with rationale
9. **Preliminary Valuation Summary** — Bear/conservative/base/bull scenario table with narrative
