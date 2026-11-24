# What's new rows have a kind; site changes stay off the overview

Status: accepted (2026-11-24)

## Context
What's new says it lists new research and data, but about half its rows were site changes (house style, page
order, the redesign, the rename), and the overview's latest three were all site changes on Nov. 24. Several of
those rows also carried corrections (#108, #115, #126, #158), which readers need to see.

## Decision
`analysis/updates.csv` gets a `kind` column: `correction` when the row corrects something the archive stated
before, whatever else it says; otherwise `research` when it adds findings, documents or figures; otherwise `site`.
The overview's latest three skip `site` rows; What's new lists research and corrections first, then site changes
under their own heading. `check_citations.py` rejects any other kind. The PR rule from
`20261121-1646-whats-new-from-a-csv.md` is unchanged: a reader-facing PR still adds a row.

## Options weighed
- **A `kind` column, site rows listed last and kept off the overview** (chosen): the overview shows findings,
  corrections stay visible, the PR check keeps working. Costs: one column, a call on each PR, and rows that mix a
  site change with new content need a judgment (#81, #89).
- **Change the page description only**: no code, but the overview keeps showing site changes.
- **Drop site rows and label those PRs `no-update`**: cheapest, but corrections inside them disappear and
  `no-update` becomes the label for about half of all PRs, which weakens the check.

## Revisit when
Readers ask for site changes on the overview, or classifying a row is regularly unclear.
