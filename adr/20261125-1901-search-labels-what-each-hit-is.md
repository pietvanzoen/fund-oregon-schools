# Search labels each hit of the archive's own files as cited, analysis, derived or summary

Status: accepted (2026-11-25, PR #TBD)

## Context
`tools/search.py` gave every hit in `analysis/` one kind, `analysis`, located by paragraph number. A hit didn't say
whether it was a cited source statement, our inference, our calculation or the uncited front matter, and since
topic files put the Analysis section first, our interpretation tends to come up before the cited lines. Lists mix
"Analysis:" items with cited ones, and a whole CSV was one hit.

## Decision
Search indexes the archive's own files one paragraph or list item per row (one record per CSV row, one file per
visual), located by `file:line (heading)`, with kind `cited`, `analysis`, `derived` or `summary`. Derived rows are
cited as `[DER:<topic>/<id>]`. `--kind` can repeat. The index rebuilds when `search.py` changes.

## Options weighed
- **Keep one kind, add the section heading to each hit**: a smaller diff, but filtering by `--kind` still can't
  leave out inference or front matter, and the reader has to know which headings mean what.
- **Kinds by what each piece is** (chosen): a search can ask for sources, citations or inference only; `--kind
  analysis` now means inference only, so callers that wanted all of `analysis/` list the kinds.
- **Parse the sections in `check_citations.py` and share them**: one definition of sections, but a shared
  helper for a dozen lines of logic.

## Revisit when
A new kind of file in `analysis/` arrives (search would call it `cited`), or the section rules in CLAUDE.md change.
