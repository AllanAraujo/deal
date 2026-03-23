---
name: notes
description: >
  Add notes and insights to an existing DD analysis. Accepts user notes (broker
  call takeaways, site visit observations, new information) and launches the
  notes-updater agent to surgically update due-diligence.md. Maintains a revision
  trail. Use after /deal:dd has been run and you have new information to incorporate.
argument-hint: "[deal-folder-name]"
allowed-tools: Read, Write, Edit, Grep, Glob
---

# /deal:notes — Add Notes to Due Diligence Analysis

## Overview

You are the orchestrator for updating an existing DD analysis with new information. You will:
1. Verify a DD document exists
2. Collect notes from the user
3. Launch the notes-updater agent to make surgical updates
4. Confirm the changes

**You run INLINE (not as a subagent).** You use the Agent tool to spawn the updater.

## Step 1: Determine Deal Folder

If `$ARGUMENTS` is provided, use it as the deal folder name. Otherwise, use the current working directory.

## Step 2: Verify DD Document Exists

Check for `due-diligence.md` in the deal folder. If it doesn't exist, show this error and stop:

> "No due diligence document found in this deal folder. Run `/deal:dd` first to generate the initial analysis, then use `/deal:notes` to add new information."

## Step 3: Collect Notes from User

Use AskUserQuestion to gather the user's notes:

> "What new information would you like to add to the DD analysis?"
>
> Options:
> - "Broker call notes" — Information from a call with the broker
> - "Site visit observations" — Findings from visiting the business
> - "New documents received" — Additional financial or legal documents
> - "Other update" — Any other new information

After the user selects a category, ask them to provide the notes as free text:

> "Please share your [category] notes. Include as much detail as possible — specific facts, quotes, dates, and any numbers mentioned."

The user will provide their notes as free text.

## Step 4: Launch Notes Updater

Launch the `notes-updater` agent:

```
Launch agent "notes-updater" with prompt:
"Update the due diligence document at [path]/due-diligence.md with the following notes.

Note category: [category from Step 3]
Date: [today's date]
Source: [category description]

User notes:
---
[user's notes verbatim]
---

Read the existing due-diligence.md, identify which sections are affected by these notes, make surgical updates, and append a revision history entry. Write the updated document back."
```

## Step 5: Confirm Changes

After the agent completes, read the updated `due-diligence.md` and find the new Revision History entry. Present a summary to the user:

> "DD analysis updated. Changes made:"
> - [Section X]: [what changed]
> - [Section Y]: [what changed]
>
> "Revision history entry added at the bottom of due-diligence.md."
>
> "You can run `/deal:notes` again to add more information, or `/deal:dd` to regenerate the full analysis (this will prompt you to archive the current version)."
