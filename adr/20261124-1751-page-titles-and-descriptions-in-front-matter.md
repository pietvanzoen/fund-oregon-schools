# Each page's search title and description live in its file's front matter, or are built from its data

Status: accepted (2026-11-24, PR #171)

## Context
Search results and link previews show a page's `<title>` and meta description. Topic pages used their H1 (up to
111 characters) and their whole In short summary (400–760 characters) for both, so search engines cut them off;
glossary pages, most person pages and the topic list had no description. Five profiles' titles and descriptions
sat in a table in the site code, away from the files they describe. Google advises a concise, unique title and a
short description specific to each page, and says generating descriptions from page data is fine for large sites.
`20261124-0555-topic-summaries-in-front-matter.md` said to revisit when a topic needs a second front-matter field.

## Decision
Topic files hold a `description` (at most 160 characters) and, when the H1 is over 55 characters, a `title` (at
most 55) beside the `summary`. Person profiles hold a `description` and may hold a `title`; that's a search line,
not a prose summary, so their cards stay factual. Same rules as the summary: uncited, every sentence backed by a
cited line on the page. `check_citations.py` enforces the keys and lengths. Pages with no file of their own get a
description built from their data (a glossary term's definition, a person's `people.csv` row) or set beside their
code in `archive.js`. The site build fails if a page search engines may index has no description.

## Options weighed
- **Cut the summary's first sentence as the description**: no new field, but first sentences run 80 to 260
  characters and lead with background, not the finding.
- **Keep titles and descriptions in a table in the site code**: one place to look, but it drifts from the files
  (a topic can change without its description showing in the same diff), as the profiles' table already did.
- **Front matter in each file** (chosen): the description sits in the same diff as the page it describes.
- **Front matter on every file behind a page** (`decisions.md`, `timeline.md`, `START.md`): those pages are
  assembled mostly from CSVs in `archive.js`, so their descriptions stay next to that code.
- **Hand-written descriptions for glossary terms and people without profiles**: about 80 more lines to keep up;
  their definition or `people.csv` row already says what the page is.

## Revisit when
Search Console shows Google rewriting many of these titles or descriptions, or a page type gets its own file.
