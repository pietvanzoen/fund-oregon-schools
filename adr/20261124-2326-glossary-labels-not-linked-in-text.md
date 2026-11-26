# Words the site gives its own meaning are glossary labels, not linked in running text

Status: accepted (2026-11-24, PR #180)

## Context
Since #173, the first use of every `glossary.csv` row on a page links to its term page. Three rows are ordinary words
this site uses with its own meaning: baseline, benchmark and proposal (each definition starts "On this site").
They appear in plain sentences too, so the link underlined everyday words, and What's being decided defines them in its
own text anyway.

## Decision
Those rows are `kind: label`. A label lists under "Terms on this page" and counts for its page's Related pages, but
gets no link in running text.

## Options weighed
- **A kind, `label` (chosen):** the data says which rows, and the three rows are labels by their own definitions;
  changes three cells, not the file's columns.
- **A new column** (e.g. `in_text: no`): the same effect, but adds a column to every row for three values.
- **A list of words in the site code:** hides a content choice in `archive.js`.
- **Keep linking them:** one dotted link per page on a common word.

## Revisit when
Another row turns out to be a common word, or readers miss the link on a label.
