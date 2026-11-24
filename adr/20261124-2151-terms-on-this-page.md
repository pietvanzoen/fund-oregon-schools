# Pages list the glossary terms they use in the side column

Status: accepted (2026-11-24, PR #173)

## Context
Readers meet terms of art without a definition (#161). Acronyms got a preview card on first use, but the 31 `kind: term`
rows showed up only on the Glossary, and the term pages had no backlinks because an `<abbr>` mention wasn't counted
as a link. #161 weighed per-page definitions, a generated box, opt-in term tooltips and in-text definitions only.

## Decision
The site build finds every `glossary.csv` row a page uses and lists them in a "Terms on this page" card in the side
column, below "Related pages", each linking to its term page with a preview card; past 10 terms, the rest sit
behind "See N more". The same match counts as a backlink, so term pages get
"Related pages". An acronym matches in its own case or as its full name, a term in any case. In the text, a term of
art's first use on each page gets the same dotted underline and preview card as an acronym's (its tooltip, or the
start of its definition); later uses stay plain.

## Options weighed
- **Side-column card, generated from `glossary.csv` (chosen):** one source of definitions; on phones it sits below
  the article with "Related pages". Long pages use up to about 30 terms (10 shown, the rest behind "See N more"), and generic rows ("proposal",
  "baseline") list wherever the word appears.
- **Collapsible box under the summary (#161 option 2):** closer to the reader, but pushes the analysis down on every
  page.
- **Per-page definitions:** would drift from the glossary and need citing twice.
- **Marker on every use, not just the first:** about 100 underlines and keyboard stops on long pages once written-out
  names count; first use only matches the acronyms.
- **No in-text marker for terms of art:** a reader saw "available resources" listed as a term but nothing in the text
  said so. First use only (chosen) keeps generic rows ("proposal") to one underline per page.

## Revisit when
Readers find the list too long, or a generic row lists on pages where it doesn't carry the glossary's meaning.
