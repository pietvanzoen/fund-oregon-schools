# Topic files put the Analysis section first

Status: accepted (2026-11-22, PR #TBD)

## Context
Topic files opened with "What the sources say" and "Derived figures", which can run to hundreds of lines
(`virtual-charters.md` is nearly 400), so the analysis most readers came for was last. `STYLE.md` says answer first.
The site renders each topic file as is.

## Decision
Topic files have three sections in this order: `## Analysis`, `## What the sources say`, `## Derived figures`.
`check_citations.py` enforces the order. The Analysis section reads on its own and points to the evidence as "below".
The site keeps rendering the files directly.

## Options weighed
- **Keep the old order and add a summary paragraph at the top**: no move, but the summary would duplicate the
  analysis and drift from it.
- **Reorder sections at build time in `site_hook.py`**: files stay as they are, but the site and the files would
  disagree, and a reader of the repo still meets the evidence first.
- **Analysis first in the files themselves** (chosen): one order everywhere; a one-time mechanical move.

## Revisit when
Readers or reviewers find the Analysis hard to follow without the evidence before it.
