---
name: listing
description: >
  Listing review agent. Accepts a URL, file path, or pasted content for a business
  listing. Performs a high-level review, compares against the deal box profile,
  recommends whether to pursue, and auto-drafts a broker intro email if recommended.
  Use when you find a listing you want to evaluate.
argument-hint: "[URL, file path, or 'paste']"
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch
---

# /deal:listing — Listing Review

## Overview

You are the orchestrator for reviewing a business listing. You will:
1. Ingest the listing content (URL, file, or pasted text)
2. Launch agents to analyze the listing and research the market
3. Compare against the buyer's deal box criteria
4. Generate a recommendation and optionally draft a broker email

**You run INLINE (not as a subagent).** You use the Agent tool to spawn subagents.

## Step 1: Ensure .gitignore Exists

Check if `.gitignore` exists at the project root (traverse upward, max 5 levels). If not, create it.

## Step 2: Determine Input Source

Check `$ARGUMENTS`:

- **If it starts with `https://`**: It's a URL. Validate it starts with `https://`. Reject `http://`, `file://`, or other schemes with: "Only HTTPS URLs are supported for security."
- **If it's a file path** (contains `/` or `.`): Read the file.
- **If it's `paste` or empty**: Ask the user to provide the listing content via AskUserQuestion (free text).

**Fetch/read the listing content.** If URL, use WebFetch. If file, use Read. Store the content for agent use.

**If WebFetch fails** (site blocks scraping, requires login, or returns empty/garbled content), inform the user:

> "I couldn't fetch that URL directly (the site may block automated access). You can:
> 1. **Paste the listing content** — copy the text from your browser and I'll analyze it
> 2. **Save as a file** — save the page as HTML or text, then run `/deal:listing path/to/file`
> 3. **Use your browser extension** — if you have the Claude Code Chrome extension, open the listing in Chrome and I can read it from there"

## Step 3: Extract Business Name and Context

From the listing content, extract:
- **Business name** (or a descriptive slug if unnamed — e.g., "hardware-store-austin")
- **Industry type**
- **Location** (city, state)
- **Asking price** (if mentioned)

You'll need these for the deal folder name, agent context, and file naming.

## Step 4: Determine Deal Folder

If the current directory is a deal folder (has `financials/` or output `.md` files), write here.

If the current directory is the project root (or doesn't look like a deal folder), create a new deal folder:
1. Generate slug from business name (lowercase, hyphens, max 40 chars)
2. Check for existing folder with same slug — if collision, append `-2`, `-3`, etc.
3. Create the folder: `mkdir [slug]`

## Step 5: Load Deal Box (Optional)

Check for `deal-box.md` at the project root (traverse upward). If found, read it for comparison criteria. If not found, note that no comparison will be done.

## Step 6: Web Search Permission

Ask if the user wants market research on this business:

> "I can research **[business name]**'s market, industry, and reputation via web search.
>
> **Privacy note:** This will query public search engines for this business name, creating a discoverable record of your interest. No financial data will be searched.
>
> Research this business online?"

Options:
- "Yes — research market and reputation"
- "No — review listing content only"

## Step 7: Launch Agents

First, create the working directory: `mkdir -p _dd-working/`

**Always launch `listing-reviewer`:**
```
Launch agent "listing-reviewer" with prompt:
"Review this business listing for a potential acquisition. The listing content is below.
Write your analysis to [deal-folder]/_dd-working/listing-reviewer.md.

If there are financial documents in [deal-folder]/financials/, cross-reference listing claims.
If there are broker documents in [deal-folder]/confidential/, also review those.

LISTING CONTENT:
---
[full listing content]
---"
```

**If web search approved, also launch `market-researcher`:**
```
Launch agent "market-researcher" with prompt:
"Research the market and community reputation for this business:
- Business name: [name]
- Industry: [industry]
- Location: [location]

DO NOT search for any financial information. Return your findings following your output contract."
```

**CRITICAL:** Market researcher receives ONLY name, industry, location. No financial data.

**After market-researcher completes:** Since this agent has no Write tool, it returns results inline. Capture its output and write it to `[deal-folder]/market-research.md` yourself so it can be referenced in the listing review output.

## Step 8: Analyze and Compare

After agents complete, read the listing-reviewer output. If deal box exists, compare the listing against criteria:

| Criterion | Deal Box | Listing | Match? |
|-----------|----------|---------|--------|
| Asking Price | $X – $Y range | $Z | Pass/Fail/Unknown |
| Industry | [targets] | [listing industry] | Pass/Fail |
| Location | [preferences] | [listing location] | Pass/Fail |
| Team Size | [preference] | [if mentioned] | Pass/Fail/Unknown |
| Years in Business | [minimum] | [if mentioned] | Pass/Fail/Unknown |
| Management | [preference] | [if mentioned] | Pass/Fail/Unknown |
| Deal Breakers | [list] | [any matches?] | Clear/Flagged |

## Step 9: Generate Recommendation

Based on the analysis, recommend one of:
- **Reach out** — Listing aligns well with deal box criteria, no major red flags
- **Need more info** — Some criteria match, but key information is missing
- **Pass** — Listing doesn't align with criteria or has significant red flags

Explain the reasoning with specific evidence.

## Step 10: Draft Broker Email (If Recommended)

If the recommendation is "Reach out", draft a broker intro email:

```markdown
**Draft Broker Email:**

Subject: Inquiry — [Business Name]

[Professional intro email tailored to the specific listing, referencing:
- The buyer's relevant background/interest
- Specific aspects of the listing that are attractive
- 2-3 initial questions
- Request for CIM/additional information
- Professional closing]
```

The email should be specific to this listing, not a generic template. Reference actual details from the listing.

## Step 11: Write Output

Write `listing-review-{slug}.md` to the deal folder:

```markdown
# Listing Review: [Business Name]

**Reviewed:** [date]
**Source:** [URL / file path / pasted content]
**Asking Price:** $[amount] [or "Not disclosed"]

> **CONFIDENTIAL** — This analysis may contain information subject to non-disclosure agreements.

---

## Listing Summary

[Agent's analysis from listing-reviewer output — business overview, key claims, red flags]

## Market Context

[Agent's market research output — if web search was performed]
[If no web search: "Market research not performed — web search was not authorized."]

## Deal Box Comparison

[Comparison table from Step 8]
[If no deal box: "No deal box profile found. Run `/deal:box` to create buyer criteria for future comparisons."]

## Recommendation

**[Reach Out / Need More Info / Pass]**

[Reasoning with specific evidence]

## Draft Broker Email

[If reach out recommended — the drafted email]
[If not: omit this section]

---

## Information Gaps

[What's missing from the listing that the buyer should ask about]

## Red Flags

[Any concerns identified during review]
```

## Step 12: Summary

> "Listing review saved to `[deal-folder]/listing-review-{slug}.md`."
>
> **Recommendation:** [Reach out / Need more info / Pass]
> **Key finding:** [1-2 sentence headline]
>
> "Next steps:
> - Add financial documents to `[deal-folder]/financials/` and run `/deal:sde`
> - Add broker documents to `[deal-folder]/confidential/` for deeper analysis
> - Run `/deal:dd` for full due diligence when you have more materials"
