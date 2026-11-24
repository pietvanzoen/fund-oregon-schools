# Pages list the glossary terms they use in the side column

Status: accepted (2026-11-24, PR #173)

## Context
Readers meet terms of art without a definition (#161). Acronyms got a preview card on first use, but the 31 `kind: term`
rows showed up only on the Glossary, and the term pages had no backlinks because an `<abbr>` mention wasn't counted
as a link. #161 weighed per-page definitions, a generated box, opt-in term tooltips and in-text definitions only.

## Decision
The site build finds every `glossary.csv` row a page uses and lists them in a "Terms on this page" card in the side
column, each linking to its term page with a preview card. The same match counts as a backlink, so term pages get
"Related pages". An acronym matches in its own case or as its full name, a term in any case. Nothing in the text is
underlined beyond the existing acronym `<abbr>`.

## Options weighed
- **Side-column card, generated from `glossary.csv` (chosen):** one source of definitions; on phones it sits below
  the article with "Related pages". Long pages list up to about 30 terms, and generic rows ("proposal",
  "baseline") list wherever the word appears.
- **Collapsible box under the summary (#161 option 2):** closer to the reader, but pushes the analysis down on every
  page.
- **Per-page definitions:** would drift from the glossary and need citing twice.
- **Tooltips on `kind: term` rows:** would underline ordinary words site-wide.

## Revisit when
Readers find the list too long, or a generic row lists on pages where it doesn't carry the glossary's meaning.
