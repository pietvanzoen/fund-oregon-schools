# Questions are listed in full once, on the Questions page

Status: accepted (2026-11-23)

## Context
The Decisions page showed a full questions table under each decision, and the Questions page showed the same rows
again. Both come from `analysis/questions.csv`. A reader seeing a one-row table at the top of the Decisions page
took it for the whole list, and nothing said how the two pages relate. The `csl-meaning` reference in
`decisions.md` named a question but didn't link to it.

## Decision
The Questions page carries who asked, the needed-by date, status and the issue link, with an anchor per question
id. The Decisions page lists each decision's questions as links to those anchors, with a count and a pointer to
the Questions page.

## Options weighed
- **Cross-link the two full tables**: least change, but every question still appears twice with the same details.
- **Per-decision question lists that link to the Questions page** (chosen): keeps each question next to its
  decision, keeps the details in one place.
- **Drop the Questions page**: one list, but no single view of what's open or answered, and the page in the nav
  that readers use to send questions would go.

## Revisit when
A decision has so many questions that the list crowds the page, or readers need dates and status next to the
decision without clicking through.
