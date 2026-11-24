# A topic's plain-language summary lives in its own file's front matter

Status: accepted (2026-11-24, PR #158)

## Context
For most readers a topic's opening is the only paragraph they read, and only 2 of the 8 topic files opened with a
summary, both dense. The site needs one short, plain summary per topic to show as "In short", in preview cards and
as the meta description (#155, #156). `20261122-2302-analysis-first-in-topic-files.md` turned down a summary
paragraph because it would drift from the analysis. Tools stay stdlib-only, so there's no YAML library.

## Decision
Each topic file starts with front matter holding one `summary` (a folded `>` block). It carries no citations;
instead every sentence must restate a cited line further down the same page, a named exception to CLAUDE.md
rule 2 that the fact-check reviewer checks. `tools/common.py` reads only `key: value` and folded `>` and rejects
anything else, so it reads the file the same way YAML does. `check_citations.py` requires a summary on every topic
and allows front matter nowhere else. Only topics get one: people keep factual cards built from `people.csv`,
because a prose summary of an official is where unfairness slips in.

## Options weighed
- **A summaries CSV** (`analysis/summaries.csv` or a `summary` column): easy to read in any tool, but the summary
  sits in another file, so a PR can change a topic's analysis without its summary showing up in the same diff.
- **An `## In short` section in the body**: no new parsing, but it breaks the fixed three-section layout that
  `check_citations.py` enforces, and the site and preview cards would have to cut it out of the Markdown.
- **Front matter in the topic file** (chosen): the summary is in the same file and the same diff as the analysis it
  summarizes, which answers the drift concern; Eleventy and MkDocs both read front matter natively.
- **Citations inside the summary**: provable at a glance, but the citation pills would bury two sentences meant
  for a parent; backing each sentence with a cited line on the page keeps it provable.
- **A YAML library**: reads any front matter, but adds a dependency to stdlib-only tools for one field.

## Revisit when
A topic needs a second front-matter field, or person profiles get a summary (then it goes in `people/<id>.md`
front matter by the same rule).
