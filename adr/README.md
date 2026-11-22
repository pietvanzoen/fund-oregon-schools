# Architecture decision records (ADRs)

Why the archive works the way it does, when there was a real choice: the options weighed, what was picked, and
when to look again. PR descriptions say *what* changed; CLAUDE.md and RUNBOOK say *what to do*; these say *why*,
including choices **not** to do something, so a later session doesn't redo work that was ruled out.

- **Read** the relevant records before changing `tools/`, the workflows, or how `sources/` is stored.
- **Add** one when you weighed options and picked one, especially when you decided not to act. Routine changes
  need no record.
- **Revisiting** a decision: write a new record that supersedes the old one, and add `Superseded by NNNN` to the
  old one's status line. Don't rewrite history.

One file per decision, `NNNN-short-slug.md`, numbered in order. Template:

```markdown
# NNNN. <Decision, stated as what we do>

Status: accepted (YYYY-MM-DD, PR #N)

## Context
Two or three lines: the problem and the facts that shaped the choice.

## Decision
What we do, in a sentence or two.

## Options weighed
- **<Option>**: what it gives, what it costs. (Mark the chosen one.)

## Revisit when
The concrete signal that should reopen this.
```

| # | Decision |
|---|---|
| [0001](0001-ocr-appends-not-replaces.md) | OCR text is added below the page text, not swapped in |
| [0002](0002-embedded-attachments-not-extracted.md) | Files embedded in archived PDFs aren't extracted |
| [0003](0003-one-derive-script-per-topic.md) | Calculated values live in their own files, one plain derive script per topic |
| [0004](0004-fetch-bot-pushes-with-deploy-key.md) | The fetch-sources bot pushes with a deploy key |
| [0005](0005-no-test-framework-for-now.md) | Tests are plain asserts in one script, no framework, for now |
| [0006](0006-whats-new-from-a-csv.md) | What's new is a CSV with a PR column, checked in CI, not built from commits |
| [0007](0007-research-organized-around-decisions.md) | Research is organized around decisions, with questions in a CSV |
| [0008](0008-house-style.md) | Reader-facing text follows a short house style, checked by a clarity reviewer |
| [0009](0009-runs-do-not-split-issues.md) | Runs don't split issues; scope is set when an issue is labelled `next` |
