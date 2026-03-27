---
name: sde
description: >
  SDE calculator with blind dual-agent verification. Reads P&L documents from
  the deal folder's financials/ directory, launches two independent agents to
  calculate SDE, then reconciles their results. Outputs sde-calculator.md with
  the reconciled SDE, discrepancy report, and both agents' full workings.
  Use when you have financial documents and need an SDE calculation.
argument-hint: "[deal-folder-name]"
allowed-tools: Read, Write, Grep, Glob
---

# /deal:sde — SDE Calculator with Blind Dual-Agent Verification

## Overview

You are the orchestrator for a blind SDE verification process. You will:
1. Discover financial documents in the deal folder
2. Launch two independent agents to calculate SDE
3. Reconcile their results and flag discrepancies
4. Write the final `sde-calculator.md`

**You run INLINE (not as a subagent).** You use the Agent tool to spawn subagents.

## Step 1: Ensure .gitignore Exists

Check if `.gitignore` exists at the project root (traverse upward to find the root — the directory containing `deal-box.md` or `.gitignore` or `.git/`). If it does not exist, create it with:

```
# Financial source documents (sensitive)
**/financials/

# Broker documents (NDA-protected)
**/confidential/
**/cim/

# Plugin working files
**/_dd-working/

# Plugin output files (contain confidential financial analysis)
**/due-diligence.md
**/due-diligence-*.md
**/sde-calculator.md
**/sde-calculator.xlsx
**/deal-calculator.md
**/listing-review-*.md
**/deal-box.md
```

## Step 2: Determine Deal Folder

If `$ARGUMENTS` is provided, use it as the deal folder name relative to the project root. Otherwise, use the current working directory.

Verify the deal folder contains a `financials/` subdirectory. If not, show this error and stop:

> "No `financials/` directory found. Create a `financials/` folder in your deal directory and add P&L documents (PDF, Excel, CSV, or text files), then run `/deal:sde` again."

## Step 3: Discover Financial Documents

Use Glob to find all files in `financials/` matching these extensions: `.pdf`, `.xlsx`, `.xls`, `.csv`, `.txt`, `.md`

Present the discovered documents to the user:

> "Found [N] financial documents in `financials/`:"
> - [filename] ([size/type])
> - ...
>
> "I'll now run two independent SDE calculations on these documents. This takes a few minutes."

If no documents are found, show this error and stop:

> "No financial documents found in `financials/`. Add P&L files (.pdf, .xlsx, .csv, or .txt) and try again."

## Step 4: Launch Dual Agents (Parallel)

Launch BOTH agents in parallel using the Agent tool. Pass each agent the same information:
- The deal folder path
- The list of discovered document file paths
- Instructions to read all documents and build a complete SDE calculation

**Agent 1 — SDE Builder (Primary):**
Launch the `financial-sde-builder` agent with prompt:
"Calculate SDE for the business using the financial documents in [deal-folder-path]/financials/. The documents are: [list of file paths]. Read each document and build a complete per-year SDE calculation following your output format exactly."

**Agent 2 — SDE Verifier (Independent):**
Launch the `financial-sde-verifier` agent with prompt:
"Independently verify the SDE for the business using the financial documents in [deal-folder-path]/financials/. The documents are: [list of file paths]. Read each document and build a complete per-year SDE calculation from scratch following your output format exactly."

**CRITICAL: Do NOT pass Agent 1's output to Agent 2. Each agent works in its own isolated context.**

## Step 5: Reconcile Results

After both agents complete, compare their results line by line:

### 5a. Compare Per-Year SDE Totals

For each year both agents calculated:
- Compare Total SDE figures
- If they differ by more than 5%, flag as a **material discrepancy**
- If they differ by 1-5%, flag as a **minor discrepancy**
- If they differ by less than 1%, mark as **agreed**

### 5b. Compare Line Items

For each year, compare individual line items:
- Net Income (should match exactly if reading the same document)
- Owner's Compensation add-back (common source of disagreement)
- Depreciation & Amortization
- Interest Expense
- Each owner benefit add-back
- Non-recurring adjustments
- CapEx reserve estimate

Flag any line items where the agents disagree on:
- Whether to include the item at all
- The dollar amount
- The source document cited

### 5c. Compare Weighted Average

Compare the final weighted average SDE and the weighting methodology.

## Step 6: Present Reconciliation to User

If there are material discrepancies, present them to the user using AskUserQuestion:

> "The two independent SDE calculations found discrepancies:"
>
> | Item | Agent 1 | Agent 2 | Variance |
> |------|---------|---------|----------|
> | [item] | $X | $Y | Z% |
>
> For each discrepancy, ask:
> "Which figure should we use for [item]?"
> Options: Agent 1's figure ($X) / Agent 2's figure ($Y) / Use conservative (lower) / Enter custom amount

If no material discrepancies, inform the user:

> "Both agents agree within 5% on all line items. Using Agent 1's figures as the primary calculation."

## Step 7: Write sde-calculator.md

Write the final `sde-calculator.md` to the deal folder with this structure:

```markdown
# SDE Calculator: [Business Name or Deal Folder]

**Generated:** [date]
**Method:** Blind dual-agent verification
**Documents analyzed:** [list]
**Verification status:** [Agreed / Reconciled with X discrepancies]

---

## Reconciled SDE Summary

| Year | SDE | SDE Margin | Status |
|------|-----|------------|--------|
| [year] | $XXX,XXX | XX.X% | Agreed/Reconciled |

**Weighted Average SDE: $XXX,XXX**
**Weighting:** [methodology]

---

## Discrepancy Report

[If no discrepancies:]
Both agents agreed within 5% on all line items. No reconciliation needed.

[If discrepancies existed:]
| Item | Year | Agent 1 | Agent 2 | Variance | Resolution |
|------|------|---------|---------|----------|------------|
| [item] | [year] | $X | $Y | Z% | [User chose X / Conservative / Custom] |

---

## Detailed SDE Calculations

### Agent 1 — Primary Calculation

[Full Agent 1 output]

### Agent 2 — Independent Verification

[Full Agent 2 output]

---

## Issues & Follow-Up Items

[Combined list of issues flagged by both agents, deduplicated]
```

## Step 7b: Generate sde-calculator.xlsx

After writing the markdown file, generate the interactive Excel workbook.

1. **Serialize reconciled SDE data to JSON.** Write a temporary `_sde-data.json` file in the deal folder containing:
   - `business_name`: business name or deal folder name
   - `years`: array of year strings (e.g., ["2023", "2024", "2025"])
   - `weights`: array of weighting percentages (e.g., [20, 30, 50])
   - `rows`: object with keys `sales`, `cogs`, `opex`, `depreciation`, `interest`, `taxes`, `owner_salary`, `owner_payroll_tax` — each an array of values per year
   - `rows.additional_addbacks`: object mapping add-back label → array of values per year
   - `annotations`: object mapping cell references (e.g., "B3") to objects with `source`, `status`, `note`, `ref` fields

   Use the reconciled agent data to populate these fields. For annotations:
   - `source`: the document name and line item cited by the agent
   - `status`: "Direct", "Verified", "Estimated", "Missing", or "Disputed"
   - `note`: any reconciliation note (e.g., "Agent 1: $X. Agent 2: $Y. Agreed.")
   - `ref`: cross-reference to sde-calculator.md section (e.g., "sde-calculator.md Section 4.1")

2. **Run the fill script via Bash:**
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/fill-sde-xlsx.py _sde-data.json sde-calculator.xlsx ${CLAUDE_PLUGIN_ROOT}/assets/sde-template.xlsx
   ```

   If `${CLAUDE_PLUGIN_ROOT}` is not available (local dev), try the relative path:
   ```
   python3 ../../scripts/fill-sde-xlsx.py _sde-data.json sde-calculator.xlsx ../../assets/sde-template.xlsx
   ```

3. **Handle errors gracefully.** If Python or openpyxl is not installed, inform the user:
   > "Could not generate Excel workbook (Python 3 + openpyxl required). Install with `pip3 install openpyxl` and re-run. The markdown report was generated successfully."

   Do NOT fail the entire command — the markdown output is always the primary artifact.

4. **Clean up.** Delete `_sde-data.json` after the script completes.

## Step 8: Summary

After writing both files, present a brief summary:

> "SDE calculation complete."
>
> **Files generated:**
> - `sde-calculator.md` — Full report with dual-agent verification
> - `sde-calculator.xlsx` — Interactive workbook (open in Excel to adjust values)
>
> **Weighted Average SDE: $XXX,XXX**
> **Verification: [Agreed / Reconciled with N discrepancies]**
> **Issues flagged: [N items for broker follow-up]**
>
> "The Excel workbook has cell comments with source citations and verification status. Adjust any values and the formulas will recalculate automatically."
>
> "Next steps: Run `/deal:dd` for full due diligence analysis, or `/deal:calc` to model the deal financials."
