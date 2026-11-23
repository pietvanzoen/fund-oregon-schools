# Architecture decision records (ADRs)

Why the archive works the way it does, when there was a real choice: the options weighed, what was picked, and
when to look again. PR descriptions say *what* changed; CLAUDE.md and RUNBOOK say *what to do*; these say *why*,
including choices **not** to do something, so a later session doesn't redo work that was ruled out.

- **Read** the relevant records before changing `tools/`, the workflows, or how `sources/` is stored.
- **Add** one when you weighed options and picked one, especially when you decided not to act. Routine changes
  need no record.
- **Revisiting** a decision: write a new record that supersedes the old one, and add a link to it by file name to
  the old one's status line, e.g. `Superseded by [20261201-0930-new-slug.md](20261201-0930-new-slug.md)`. Don't
  rewrite history.

One file per decision, `YYYYMMDD-HHMM-short-slug.md`, named by the UTC time you create it (`date -u +%Y%m%d-%H%M`),
so two sessions writing records at once can't pick the same name. Refer to a record by its file name, not a number.
Template:

```markdown
# <Decision, stated as what we do>

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

| Date | Decision |
|---|---|
| [2026-11-21](20261121-1522-ocr-appends-not-replaces.md) | OCR text is added below the page text, not swapped in |
| [2026-11-21](20261121-1523-embedded-attachments-not-extracted.md) | Files embedded in archived PDFs aren't extracted |
| [2026-11-21](20261121-1524-one-derive-script-per-topic.md) | Calculated values live in their own files, one plain derive script per topic |
| [2026-11-21](20261121-1525-fetch-bot-pushes-with-deploy-key.md) | The fetch-sources bot pushes with a deploy key |
| [2026-11-21](20261121-1526-no-test-framework-for-now.md) | Tests are plain asserts in one script, no framework, for now |
| [2026-11-21](20261121-1646-whats-new-from-a-csv.md) | What's new is a CSV with a PR column, checked in CI, not built from commits |
| [2026-11-21](20261121-2205-research-organized-around-decisions.md) | Research is organized around decisions, with questions in a CSV |
| [2026-11-22](20261122-1551-vale-in-ci-stdlib-in-tools.md) | Python tools stay stdlib-only; heavier checks run in GitHub Actions |
| [2026-11-22](20261122-1607-house-style.md) | Reader-facing text follows a short house style, checked by a clarity reviewer |
| [2026-11-22](20261122-1635-runs-do-not-split-issues.md) | Runs don't split issues; scope is set when an issue is labelled `next` |
| [2026-11-22](20261122-1718-correcting-append-only-rows.md) | A wrong append-only row is corrected by a new row that names the line it replaces |
| [2026-11-22](20261122-2302-analysis-first-in-topic-files.md) | Topic files put the Analysis section first |
| [2026-11-22](20261123-0249-correcting-news-records.md) | A wrong news record is corrected in place, with a dated note |
