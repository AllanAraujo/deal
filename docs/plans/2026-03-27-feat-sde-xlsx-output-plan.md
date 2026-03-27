---
title: "feat: SDE XLSX Output Alongside Markdown"
type: feat
status: completed
date: 2026-03-27
---

# SDE XLSX Output Alongside Markdown

## Overview

Enhance `/deal:sde` to produce a working Excel spreadsheet (`sde-calculator.xlsx`) alongside the existing `sde-calculator.md`. The XLSX uses a shipped template with preserved formulas, gets filled with reconciled SDE data, and includes cell comments with source citations and verification status cross-referenced to the markdown report.

## Problem Statement / Motivation

The markdown SDE report is great for reading and sharing, but business buyers and their CPAs want an interactive spreadsheet where they can toggle add-backs, adjust values, and see formulas recalculate. Generating both files from the same dual-agent analysis gives users the best of both worlds — a narrative report and a working financial model.

## Proposed Solution

Ship a blank SDE template XLSX with the plugin. After the existing reconciliation step in `/deal:sde`, run a Python script (via Bash) that copies the template, fills value cells with reconciled data, adds cell comments with annotations, and saves as `sde-calculator.xlsx` in the deal folder.

### New Files

```
deal/
├── assets/
│   └── sde-template.xlsx         # Blank template (SDE Calculator sheet only)
├── scripts/
│   └── fill-sde-xlsx.py          # Python/openpyxl script to fill template
```

### Modified Files

```
skills/sde/SKILL.md               # Add Step 7b: invoke Python script
.gitignore                         # Add **/sde-calculator.xlsx
CLAUDE.md                          # Document assets/ and scripts/ directories
```

## Technical Considerations

- **openpyxl dependency** — The script requires Python 3 + openpyxl. If openpyxl is not installed, the skill should catch the error and suggest `pip3 install openpyxl`, then proceed without the XLSX (markdown is always generated).
- **Template integrity** — Only data cells are written. Formula cells (rows 6, 12, 40, 41) and the weighted average formula (E41) remain untouched from the template.
- **Plugin asset path** — The script locates the template via `${CLAUDE_PLUGIN_ROOT}/assets/sde-template.xlsx`. For local dev, it falls back to a relative path.
- **Data serialization** — The orchestrator writes a temporary JSON file (`_sde-data.json`) with the reconciled SDE data, the script reads it, fills the XLSX, and the orchestrator cleans up the JSON.

## Acceptance Criteria

- [x] Every `/deal:sde` run produces both `sde-calculator.md` and `sde-calculator.xlsx`
- [x] XLSX uses the template structure (rows 1-41 match the user's SDE Calculator template)
- [x] Only SDE Calculator sheet included (no Owner Income sheet)
- [x] Formula cells are preserved and calculate correctly when values are filled
- [x] Each value cell has an Excel comment with: source document, verification status, and sde-calculator.md section reference
- [x] Weighting percentages (row 2) are populated from the agent's weighted average methodology
- [x] Year headers (row 1, columns B-D) show the actual years from the financial documents
- [x] If openpyxl is not installed, the skill logs a warning and skips XLSX generation (markdown still produced)
- [x] `sde-calculator.xlsx` is gitignored (contains confidential financial data)
- [x] `assets/sde-template.xlsx` is NOT gitignored (ships with the plugin)
- [x] CLAUDE.md updated with `assets/` and `scripts/` directory documentation

## Implementation Tasks

### 1. Create template asset

- [x] Copy `templates/SDE calculator command/[TEMPLATE] SDE Calculator (2) copy.xlsx` to `assets/sde-template.xlsx`
- [x] Remove the "Owner income" sheet (keep only "SDE Calculator")
- [x] Clear any pre-existing data values (keep formulas, headers, row labels)
- [x] Verify formulas reference correct cells after cleanup

### 2. Write `scripts/fill-sde-xlsx.py`

- [x] Script reads a JSON file path from command-line argument
- [x] JSON schema:

```json
{
  "business_name": "Acme Hardware",
  "years": ["2023", "2024", "2025"],
  "weights": [20, 30, 50],
  "rows": {
    "sales": [727000, 796000, 785000],
    "cogs": [-168000, -227000, -260000],
    "opex": [-220000, -372000, -235000],
    "depreciation": [10417, 74407, 24576],
    "interest": [9119, 0, 0],
    "taxes": [0, 0, 0],
    "owner_salary": [0, 0, 0],
    "owner_payroll_tax": [0, 0, 0],
    "additional_addbacks": {
      "Auto/Truck": [5819, 4395, 6651],
      "Health Insurance": [0, 2398, 7487],
      "Donations": [152, 1712, 0],
      "Meals": [582, 574, 0],
      "Gifts": [0, 8462, 0],
      "Unclassified": [633, 11239, 0],
      "Non-Recurring (Income)": [-62467, 0, 0],
      "Maintenance CapEx": [-15000, -10000, -10000]
    }
  },
  "annotations": {
    "B3": {"source": "2023 Business P&L", "status": "Direct", "ref": "Section 4.1"},
    "B7": {"source": "2023 P&L: Depreciation", "status": "Direct", "ref": "Section 4.1"},
    "C8": {"source": "Not found on 2024 P&L", "status": "Missing", "ref": "Section 4.2"}
  }
}
```

- [x] Copy template to output path (`sde-calculator.xlsx`)
- [x] Fill year headers (B1:D1) and weighting percentages (B2:D2)
- [x] Fill value cells (rows 3-5, 7-11) with core SDE data
- [x] Fill additional add-back rows (15+) dynamically — map names to row labels
- [x] Add Excel cell comments from annotations dict (source + status + ref)
- [x] Preserve all formula cells untouched
- [x] Save and exit

### 3. Update `skills/sde/SKILL.md`

- [x] After Step 7 (write sde-calculator.md), add Step 7b:
  - Serialize reconciled SDE data to `_sde-data.json` in the deal folder
  - Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/fill-sde-xlsx.py _sde-data.json sde-calculator.xlsx ${CLAUDE_PLUGIN_ROOT}/assets/sde-template.xlsx` via Bash
  - If Python/openpyxl not available: warn user, skip XLSX, continue
  - If successful: report "Also generated sde-calculator.xlsx — open in Excel to adjust values"
  - Clean up `_sde-data.json`
- [x] Update Step 8 summary to mention both output files

### 4. Update `.gitignore`

- [x] Add `**/sde-calculator.xlsx` after the `**/sde-calculator.md` line
- [x] Do NOT add a broad `**/*.xlsx` pattern (would block `assets/sde-template.xlsx`)

### 5. Update `CLAUDE.md`

- [x] Add `assets/` to File Organization section: "Plugin assets (templates, static files shipped with the plugin)"
- [x] Add `scripts/` to File Organization section: "Helper scripts invoked by skills via Bash"
- [x] Update Output File Convention to mention XLSX alongside markdown

### 6. Update `.gitignore` template in `skills/sde/SKILL.md`

- [x] Add `**/sde-calculator.xlsx` to the embedded .gitignore template that gets generated on first run

## Dependencies & Risks

- **Python 3 + openpyxl** — Users must have Python 3 installed (standard on macOS/Linux). openpyxl may not be installed. The skill should handle this gracefully with a clear error message and pip install suggestion.
- **`${CLAUDE_PLUGIN_ROOT}` resolution** — This variable points to the installed plugin directory. Needs testing to confirm it resolves correctly for marketplace-installed plugins vs. local dev.
- **Template fidelity** — The blank template must be carefully prepared (Owner Income sheet removed, values cleared, formulas intact). Any formula error in the template propagates to every user.

## References & Research

- Brainstorm: `docs/brainstorms/2026-03-27-sde-xlsx-output-brainstorm.md`
- Current SDE skill: `skills/sde/SKILL.md`
- SDE agents: `agents/financial-sde-builder.md`, `agents/financial-sde-verifier.md`
- Original template: `templates/SDE calculator command/[TEMPLATE] SDE Calculator (2) copy.xlsx`
- openpyxl docs: https://openpyxl.readthedocs.io/
