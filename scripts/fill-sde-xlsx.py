#!/usr/bin/env python3
"""
fill-sde-xlsx.py — Fill an SDE Calculator XLSX template with reconciled data.

Usage:
    python3 fill-sde-xlsx.py <data.json> <output.xlsx> <template.xlsx>

The JSON file contains reconciled SDE data from the /deal:sde skill.
The template is copied, filled with values and cell comments, then saved.
"""

import json
import shutil
import sys
from pathlib import Path

try:
    import openpyxl
    from openpyxl.comments import Comment
except ImportError:
    print("ERROR: openpyxl is not installed. Install it with: pip3 install openpyxl", file=sys.stderr)
    sys.exit(1)


# Row mapping for standard SDE line items
STANDARD_ROWS = {
    "sales": 3,
    "cogs": 4,
    "opex": 5,
    # Row 6 = Net Income (formula)
    "depreciation": 7,
    "interest": 8,
    "taxes": 9,
    "owner_salary": 10,
    "owner_payroll_tax": 11,
    # Row 12 = Basic SDE (formula)
}

# Additional add-back rows start at 15, map by label
ADDBACK_START_ROW = 15
ADDBACK_END_ROW = 39

# Column mapping: year index -> Excel column
YEAR_COLS = {0: "B", 1: "C", 2: "D"}


def fill_template(data_path: str, output_path: str, template_path: str) -> None:
    with open(data_path) as f:
        data = json.load(f)

    # Copy template to output
    shutil.copy2(template_path, output_path)

    wb = openpyxl.load_workbook(output_path)
    ws = wb["SDE Calculator"]

    years = data.get("years", [])
    weights = data.get("weights", [])
    rows = data.get("rows", {})
    annotations = data.get("annotations", {})
    addbacks = rows.get("additional_addbacks", {})

    # Fill year headers (B1:D1)
    for i, year in enumerate(years[:3]):
        col = YEAR_COLS[i]
        ws[f"{col}1"].value = int(year) if str(year).isdigit() else year

    # Fill weighting percentages (B2:D2)
    for i, weight in enumerate(weights[:3]):
        col = YEAR_COLS[i]
        ws[f"{col}2"].value = weight

    # Fill standard rows
    for key, row_num in STANDARD_ROWS.items():
        values = rows.get(key, [])
        for i, val in enumerate(values[:3]):
            col = YEAR_COLS[i]
            cell_ref = f"{col}{row_num}"
            ws[cell_ref].value = val

    # Fill additional add-backs dynamically
    addback_row = ADDBACK_START_ROW
    for label, values in addbacks.items():
        if addback_row > ADDBACK_END_ROW:
            break
        ws[f"A{addback_row}"].value = label
        for i, val in enumerate(values[:3]):
            col = YEAR_COLS[i]
            ws[f"{col}{addback_row}"].value = val
        addback_row += 1

    # Add cell comments from annotations
    for cell_ref, ann in annotations.items():
        cell = ws[cell_ref]
        parts = []
        if "source" in ann:
            parts.append(f"Source: {ann['source']}")
        if "status" in ann:
            parts.append(f"Status: {ann['status']}")
        if "note" in ann:
            parts.append(f"Note: {ann['note']}")
        if "ref" in ann:
            parts.append(f"Ref: {ann['ref']}")

        if parts:
            comment_text = "\n".join(parts)
            cell.comment = Comment(comment_text, "deal:sde")

    wb.save(output_path)
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <data.json> <output.xlsx> <template.xlsx>", file=sys.stderr)
        sys.exit(1)

    data_path, output_path, template_path = sys.argv[1], sys.argv[2], sys.argv[3]

    if not Path(data_path).exists():
        print(f"ERROR: Data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    if not Path(template_path).exists():
        print(f"ERROR: Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    fill_template(data_path, output_path, template_path)
