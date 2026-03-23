---
name: box
description: >
  Interactive buyer profile creator. Walks the user through quantitative criteria
  (cash flow, salary, financing, price range) and qualitative criteria (industry,
  geography, team size, management, must-haves, deal breakers). Creates or updates
  deal-box.md at the project root. Use when setting up acquisition criteria or
  updating buyer preferences.
allowed-tools: Read, Write, Grep, Glob
---

# /deal:box — Buyer Profile Creator

## Overview

Create or update a buyer profile (`deal-box.md`) that defines the user's acquisition criteria. This profile is used by other commands to compare deals against the buyer's requirements.

**You run INLINE (not as a subagent).** You use AskUserQuestion for all inputs.

## Step 1: Ensure .gitignore Exists

Check if `.gitignore` exists at the project root (traverse upward, max 5 levels — look for `.git/` or existing `.gitignore`). If not, create it with the standard template.

## Step 2: Find Project Root and Check for Existing Profile

Traverse upward from the current directory (max 5 levels) looking for `deal-box.md` or `.git/`. The project root is where `.git/` lives, or the highest directory you've checked.

**If `deal-box.md` exists:** Read it and enter partial update mode (Step 3a).
**If `deal-box.md` does not exist:** Enter full creation mode (Step 3b).

## Step 3a: Partial Update Mode

Present the existing profile summary and ask:

> "Your deal box already exists. What would you like to update?"

Use AskUserQuestion with options:
- "Quantitative criteria" — Cash flow, salary, financing, price range
- "Qualitative criteria" — Industry, geography, team size, management
- "Must-haves and deal breakers" — Free text requirements
- "View current profile" — Show the full deal box without changes

Based on selection, jump to the relevant section in Step 3b. After updating, merge with existing values for unchanged sections and write the updated file.

## Step 3b: Full Creation / Section Questionnaire

Walk through each section using AskUserQuestion. Show sensible defaults — the user can accept by selecting the default option or provide custom values.

### Section 1: Personal Requirements

Ask: "What is your required personal cash flow from the business (annual, after debt service)?"
- Options: "$50,000", "$75,000", "$100,000", "$150,000" (Other for custom)

### Section 2: Operator Settings

Ask: "What operator salary would you budget for running the business?"
- Options: "$60,000", "$80,000", "$100,000", "$120,000" (Other for custom)

Ask: "Payroll tax rate?"
- Options: "10%", "12%", "15%" (Other for custom)

Ask: "Benefits rate?"
- Options: "0% (no benefits)", "10%", "15%", "20%" (Other for custom)

### Section 3: Financing Assumptions

Ask: "What percentage of the purchase would you finance?"
- Options: "80% (SBA standard)", "70%", "90%", "100% (all financed)" (Other for custom)

Ask: "Expected interest rate?"
- Options: "10.5% (current SBA 7a)", "9%", "11%", "12%" (Other for custom)

Ask: "Loan term?"
- Options: "10 years (SBA standard)", "7 years", "15 years", "25 years (with real estate)" (Other for custom)

Ask: "Minimum acceptable DSCR (Debt Service Coverage Ratio)?"
- Options: "1.25x (SBA minimum)", "1.5x", "1.75x", "2.0x" (Other for custom)

### Section 4: Purchase Information

Ask: "Target purchase price multiple (times SDE)?"
- Options: "2.0x", "2.5x", "3.0x", "3.5x" (Other for custom)

Ask: "What is your asking price range?"

Ask for minimum: Options: "$100,000", "$250,000", "$500,000", "$750,000" (Other)
Ask for maximum: Options: "$500,000", "$1,000,000", "$2,000,000", "$5,000,000" (Other)

### Section 5: Industry Preferences

Ask: "Which industries are you targeting?" (multiSelect: true)
- Options: "Service businesses", "Manufacturing", "Healthcare", "Technology/SaaS" (Other for custom)

Then ask: "Any industries to exclude?" (free text via Other)

### Section 6: Geographic Preferences

Ask: "Geographic focus?"
- Options: "US only", "Specific states/cities", "International", "No preference"

If specific: ask for state and city combinations (free text).

### Section 7: Team Size

Ask: "Preferred team size?"
- Options: "No preference", "No employees (solo)", "Micro (1-5)", "Small (6-20)" (Other for custom)

### Section 8: Financing Options Available

Ask: "What financing options do you have access to?" (multiSelect: true)
- Options: "Own cash", "SBA loan", "Seller financing", "Other (ROBS, investors, etc.)"

### Section 9: Business Maturity

Ask: "Minimum years in business?"
- Options: "No preference", "2+ years", "5+ years", "10+ years"

### Section 10: Management Structure

Ask: "Preferred management structure?"
- Options: "Owner operated", "Has general manager", "Absentee/management team", "No preference"

### Section 11: Must-Haves and Deal Breakers

Ask: "Any must-haves for your ideal acquisition?" (free text)
Ask: "Any absolute deal breakers?" (free text)

## Step 4: Confirmation

Show a summary of all selections and ask:

> "Here's your deal box profile. Does this look correct?"

Options:
- "Save" — Write the file
- "Edit a section" — Go back to a specific section
- "Start over" — Re-run the full questionnaire

## Step 5: Write deal-box.md

Write to the project root (NOT inside a deal folder):

```markdown
---
created: YYYY-MM-DD
last-modified: YYYY-MM-DD
---

# Deal Box — Buyer Profile

## Quantitative Criteria

### Personal Requirements
- **Required Personal Cash Flow:** $X/year

### Operator Settings
- **Operator Salary:** $X/year
- **Payroll Tax Rate:** X%
- **Benefits Rate:** X%

### Financing Assumptions
- **Financing Percentage:** X%
- **Interest Rate:** X%
- **Loan Term:** X years
- **Minimum DSCR:** X.XXx

### Purchase Information
- **Target Multiple:** X.Xx SDE
- **Asking Price Range:** $X – $Y

## Qualitative Criteria

### Industry Preferences
- **Target:** [list]
- **Excluded:** [list or "None"]

### Geographic Preferences
- **Focus:** [description]
- **Locations:** [list or "No preference"]

### Team Size
- **Preference:** [selection]

### Financing Options Available
- [list]

### Years in Business
- **Minimum:** [selection]

### Management Structure
- **Preference:** [selection]

## Requirements

### Must-Haves
- [list or "None specified"]

### Deal Breakers
- [list or "None specified"]
```

## Step 6: Summary

> "Deal box saved to `deal-box.md` at the project root."
>
> "Your profile will be used by other commands:
> - `/deal:listing` will compare listings against your criteria
> - `/deal:calc` will import operator costs and check deal metrics
> - `/deal:dd` will reference your requirements in the analysis
>
> Run `/deal:box` again anytime to update your criteria."
