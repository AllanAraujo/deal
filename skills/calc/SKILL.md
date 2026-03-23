---
name: calc
description: >
  Deal financial calculator and Year 1 pro forma. Interactive questionnaire
  for purchase price, funding sources, SDE, and operator costs. Pre-fills from
  existing artifacts (sde-calculator.md, deal-box.md, listing-review-*.md).
  Calculates DSCR, purchase multiple, cash-on-cash return, and payback period.
  Compares against deal box criteria. Use when you want to model deal economics.
argument-hint: "[deal-folder-name]"
allowed-tools: Read, Write, Grep, Glob
---

# /deal:calc — Deal Financial Calculator

## Overview

You are the orchestrator for a deal financial calculator. You will:
1. Pre-fill as much as possible from existing artifacts
2. Walk the user through an interactive questionnaire for remaining inputs
3. Calculate all key metrics
4. Compare against deal box criteria
5. Write `deal-calculator.md`

**You run INLINE (not as a subagent).** You use AskUserQuestion for all inputs. No agents are launched — this is a computation skill.

## Step 1: Ensure .gitignore and Determine Deal Folder

Check for `.gitignore` at project root (traverse upward, max 5 levels). Create if missing.

If `$ARGUMENTS` is provided, use as deal folder name. Otherwise, use CWD.

## Step 2: Pre-Fill from Existing Artifacts

Scan for existing data to reduce the questionnaire:

**From `listing-review-*.md` or `due-diligence.md`:**
- Asking price
- Business name

**From `sde-calculator.md`:**
- Weighted average SDE
- Per-year SDE figures
- Revenue figures

**From `deal-box.md` (project root, traverse upward):**
- Operator salary, payroll tax rate, benefits rate
- Required personal cash flow
- Minimum DSCR
- Financing assumptions (rate, term, percentage)

Report what was pre-filled:

> "Pre-filled from existing artifacts:
> - Purchase price: $695,000 (from listing review)
> - SDE: $294,136 weighted average (from SDE calculator)
> - Operator salary: $100,000 (from deal box)
> - Financing: 80% at 10.5% for 10 years (from deal box)
>
> You can accept these or override during the questionnaire."

## Step 3: Interactive Questionnaire

### Stage 1: Acquisition Info

For each field, show the pre-filled value (if any) as the default option.

**Purchase Price** (required):
> "Purchase price?"
- Options: "[$pre-filled]" (if available), "$500,000", "$750,000", "$1,000,000" (Other for custom)

**DSCR Tax Rate:**
> "DSCR tax rate?"
- Options: "25% (standard)", "20%", "30%" (Other for custom)

**Toggle Questions** — ask each as Yes/No:
- "Include closing costs?" → If Yes: "Closing costs amount?" ($10K / $15K / $25K / Other)
- "Include real estate in purchase?" → If Yes: "Real estate value?" (Other for amount)
- "Include working capital?" → If Yes: "Working capital amount?" ($25K / $50K / $75K / Other)
- "Working capital loan (separate from main financing)?" → If Yes: rate, term, amount
- "Set minimum cash flow requirement?" → If Yes: amount (pre-fill from deal box if available)
- "Hire a new operator (not owner-operated)?" → If Yes: collect or confirm operator costs

### Stage 2: Funding Sources

> "Let's set up your funding sources. The total must cover the purchase price plus any additional costs."

For each source, ask:
- **Type:** "SBA 7(a) loan", "Seller note", "Cash/equity", "Other"
- **Amount:** dollar amount
- **Rate:** interest rate (%) — skip for Cash/equity
- **Term:** years — skip for Cash/equity

After each source: "Add another funding source? (Yes / No)"

**Validate:** Sum of all sources >= purchase price + closing costs + working capital. If short, inform the user and ask them to add another source or adjust.

### Stage 3: SDE Integration

**If `sde-calculator.md` exists:**
> "Import SDE from your existing SDE calculation?"
> - "Yes — use weighted average SDE of $[X]"
> - "No — enter SDE manually"

If importing and the SDE calculator noted discrepancies, mention: "Note: The SDE calculator flagged [N] discrepancies. Using the reconciled figure."

**If no SDE calculator:**
> "Enter the SDE (Seller's Discretionary Earnings) for this business:"
> - Options: Other (free text for dollar amount)

Also collect revenue if not available from SDE calculator:
> "Annual revenue?"

### Stage 4: Operator Costs (if hiring new operator)

**If deal box exists, pre-fill:**
> "Import operator costs from your deal box? (Salary: $X, Tax: X%, Benefits: X%)"
> - "Yes — use deal box values"
> - "No — enter new values"

**If no deal box or user wants custom:**
- Operator salary ($)
- Payroll tax rate (%)
- Benefits rate (%)

## Step 4: Compute All Metrics

Perform the following calculations:

### Debt Service

For each funding source with a rate and term:
```
Monthly Rate = Annual Rate / 12 / 100
Total Months = Term * 12
Monthly Payment = Amount * [Monthly Rate * (1 + Monthly Rate)^Total Months] / [(1 + Monthly Rate)^Total Months - 1]
Annual Debt Service = Monthly Payment * 12
```

For cash/equity sources: no debt service.

`Total Annual Debt Service = Sum of all source annual payments`

### Cash Injection

```
Total Cash Injection = Cash equity amount + Closing costs (if any) + Working capital (if any)
```

### Year 1 P&L Summary

```
Revenue (from SDE source or manual)
- COGS (from SDE source or estimated)
= Gross Profit
- Operating Expenses (from SDE source or estimated)
- New Operator Cost = Salary * (1 + Tax Rate/100 + Benefits Rate/100)  [if applicable]
= Adjusted Operating Income (use SDE as proxy if detailed P&L not available)
- Total Annual Debt Service
- DSCR Tax = Adjusted Operating Income * DSCR Tax Rate / 100
= Net Cash Flow (Year 1)
```

**Note:** If only SDE is available (no detailed P&L), use SDE as Adjusted Operating Income. This is standard for SDE-based deal modeling.

### Key Metrics

```
DSCR = SDE / Total Annual Debt Service  (using SDE, not adjusted operating income, for standard SDE-based DSCR)
Purchase Multiple = Purchase Price / SDE
Cash-on-Cash Return = Net Cash Flow / Total Cash Injection * 100
Payback Period = Total Cash Injection / Net Cash Flow  (in years)
```

### Deal Box Comparison (if available)

Compare calculated metrics against deal box criteria:
- Cash flow vs. required personal cash flow → Pass/Fail
- DSCR vs. minimum DSCR → Pass/Fail
- Purchase price vs. asking price range → Pass/Fail
- Purchase multiple vs. target multiple → Pass/Fail

## Step 5: Write deal-calculator.md

```markdown
# Deal Calculator: [Business Name or Deal Folder]

**Generated:** [date]
**Purchase Price:** $[amount]
**SDE Basis:** $[amount] ([source: SDE calculator / manual])

> **CONFIDENTIAL** — This analysis contains financial projections for acquisition planning.

---

## Deal Summary

| Metric | Value | Deal Box Target | Status |
|--------|-------|-----------------|--------|
| Purchase Price | $X | $X – $Y range | Pass/Fail |
| Purchase Multiple | X.Xx | X.Xx target | Pass/Fail |
| Year 1 Net Cash Flow | $X | $X required | Pass/Fail |
| DSCR | X.XXx | X.XXx minimum | Pass/Fail |
| Cash-on-Cash Return | X.X% | — | — |
| Payback Period | X.X years | — | — |

[If no deal box: omit Deal Box Target and Status columns]

---

## Financing Structure

| Source | Type | Amount | Rate | Term | Annual Payment |
|--------|------|--------|------|------|----------------|
| [source 1] | SBA 7(a) | $X | X.X% | X yr | $X |
| [source 2] | Seller Note | $X | X.X% | X yr | $X |
| [source 3] | Cash/Equity | $X | — | — | — |
| **Total** | | **$X** | | | **$X** |

**Total Cash Injection:** $X (equity + closing costs + working capital)
**Total Annual Debt Service:** $X

---

## Year 1 Pro Forma

| Line Item | Amount |
|-----------|--------|
| Revenue | $X |
| SDE (Seller's Discretionary Earnings) | $X |
| - New Operator Cost | ($X) [if applicable] |
| = Adjusted Operating Income | $X |
| - Total Annual Debt Service | ($X) |
| - Estimated Taxes (X%) | ($X) |
| = **Net Cash Flow (Year 1)** | **$X** |

---

## Key Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| **DSCR** | X.XXx | [Strong (>1.5x) / Adequate (1.25-1.5x) / Tight (<1.25x)] |
| **Purchase Multiple** | X.Xx SDE | [Within range / Above range / Below range for industry] |
| **Cash-on-Cash Return** | X.X% | [context] |
| **Payback Period** | X.X years | [context] |
| **Total Cash Required** | $X | [equity + costs + working capital] |

---

## Deal Box Comparison

[If deal box exists:]

| Criterion | Your Target | This Deal | Result |
|-----------|------------|-----------|--------|
| Min Cash Flow | $X/year | $X/year | PASS/FAIL |
| Min DSCR | X.XXx | X.XXx | PASS/FAIL |
| Price Range | $X – $Y | $X | PASS/FAIL |
| Target Multiple | X.Xx | X.Xx | PASS/FAIL |

[If no deal box: "No deal box profile found. Run `/deal:box` to set up criteria."]

---

## Assumptions & Inputs

[List every assumption and input used, so the user can audit the calculation]

- Purchase price: $X
- SDE: $X ([source])
- DSCR tax rate: X%
- Closing costs: $X [or "Not included"]
- Real estate: [Included / Not included]
- Working capital: $X [or "Not included"]
- Operator: [Owner-operated / New hire at $X + X% tax + X% benefits]
- Funding: [summary of each source]
```

## Step 6: Summary

> "Deal calculator complete. Results written to `deal-calculator.md`."
>
> **Year 1 Net Cash Flow: $X**
> **DSCR: X.XXx**
> **Purchase Multiple: X.Xx**
> **Cash-on-Cash Return: X.X%**
>
> [If deal box comparison done: "Deal box check: X/Y criteria passed."]
>
> "Next steps:
> - Run `/deal:dd` for full due diligence if you haven't already
> - Run `/deal:calc` again to test different scenarios (e.g., different purchase price or financing)
> - Run `/deal:notes` to add broker feedback that may change the analysis"
