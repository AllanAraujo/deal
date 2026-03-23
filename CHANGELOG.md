# Changelog

## 0.1.0 — 2026-03-23

Initial release.

### Skills (7)
- `/deal:sde` — SDE calculator with blind dual-agent verification
- `/deal:dd` — Multi-agent due diligence analysis (financial, market, synthesis)
- `/deal:notes` — Surgical DD document updates with revision trail
- `/deal:box` — Interactive buyer profile creator
- `/deal:listing` — Listing review with deal box comparison and broker email drafting
- `/deal:calc` — Deal financial calculator with Year 1 pro forma
- `/deal:help` — Command reference and workflow guide

### Agents (7)
- `financial-sde-builder` — SDE calculation (primary)
- `financial-sde-verifier` — SDE calculation (independent blind verification)
- `financial-analyst` — P&L, balance sheet, and SDE valuation analysis
- `market-researcher` — Industry trends and community reputation (web only, no filesystem)
- `listing-reviewer` — Listing and broker document extraction
- `dd-synthesizer` — Cross-agent synthesis (opus model)
- `notes-updater` — Surgical DD document updates

### Architecture
- Confidentiality boundary: financial agents have no web access, web agents have no filesystem access
- File-mediated agent handoff via `_dd-working/` temp directory
- All output files gitignored by default (financial data protection)
- Web search opt-in with privacy disclosure
- Deal-per-folder organization with upward traversal for project root
