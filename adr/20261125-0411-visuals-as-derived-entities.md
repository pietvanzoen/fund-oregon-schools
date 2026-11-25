# Charts and diagrams are their own files, checked once and embedded by id

Status: accepted (2026-11-25, PR #TBD)

## Context
Guides (#188) and topics need charts and diagrams. A visual restates archived figures in a new form, so it's derived
content, like a `[DER:...]` row. Drawn page by page, each copy needs its own fact-check and can drift from the others.
The home page's funding chart (`fundingChart` in `site-11ty/src/_data/archive.js`) was the only one, with its
labels and notes hard-coded in the build and one note uncited. Most readers are on phones, and the maintainer wants
no chart script sent to readers.

## Decision
One file per visual, `analysis/visuals/<id>.json`, checked by `tools/check_citations.py` and embedded in any page
with `<!-- site: visual <id> -->`. Each visual also gets its own page, `/visuals/<id>/`, with a generated text version, its
sources and the pages that use it.
- A visual holds no numbers. A chart's bars point to rows by reference: `data/<file>/<id>` for a row of
  `analysis/data/<file>.csv` or `derived/<topic>/<id>` for a row of `analysis/derived/<topic>.csv`. The value and
  its citation come from the row. A calculated value gets a derive row first. Data files that a visual uses get an
  `id` column (first, unique), added when a visual first needs one.
- Every text field in a visual (a note, a diagram box or arrow) carries its own citation.
- Two templates, in the site build: `bars` uses Charts.css (pinned, plain CSS on an HTML table), and `flow` is
  our own HTML and CSS: rows of boxes that stack on phones, each box listing where its money goes as text, with a
  down-arrow between rows. A path no archived source confirms is drawn as open (dashed, labelled) or left out,
  and the maintainer chooses which.
- Colour never tells series apart on its own: each bar's group is written on it.

## Options weighed
- **File format: JSON** (chosen): holds a diagram's nested boxes and arrows in one file; Python's stdlib and the
  site build read it with no new dependency. Costs: no comments, noisier diffs than CSV.
- **File format: CSV**: matches rule 8's habit, but a diagram needs two files (boxes, arrows) and a chart's list of
  bars doesn't fit a row.
- **Row references by id** (chosen): one exact match, and a renamed or deleted row fails the check. Cost: an `id`
  to fill in for each new row in those files.
- **Row references by key columns** (biennium and stage): no file changes, but `ssf_history.csv` has two 2027-29
  current service level rows, and a fixed label would quietly stop matching.
- **Bars with Charts.css** (chosen): the chart is a real data table, so screen readers get the table; no script;
  MIT, about 6 KB gzipped (60 KB minified), loaded only on pages that show a chart. Cost: one pinned dependency
  and its class names in our markup.
- **Bars with our own CSS** (`barChart`, the former template): no dependency, but every chart shape (columns, a
  stacked bar) is code to write and maintain.
- **SVG templates in the build** (the issue's first idea): full control, but SVG text shrinks with the image on a
  phone instead of wrapping.
- **Mermaid on the site**: renders at a fixed width, so text shrinks on phones; looks generic; needs headless
  Chromium in CI to render at build time. (Mermaid is fine in `RESEARCH.md`, which GitHub renders and the site
  doesn't publish.)
- **A JavaScript chart library**: redraws per screen size, but ships a script to every reader and the chart
  doesn't exist until it runs.
- **Flow diagrams with drawn connector lines** (CSS pseudo-elements, as in org-chart demos): suited to one box
  branching into many; our flows merge many sources into one fund, where drawn lines tangle and don't survive a
  phone's single column.

## Revisit when
A visual needs a shape neither template draws (a timeline for #189, a stacked bar for #191: check Charts.css first),
a flow needs crossing paths that text lists can't show clearly, or Charts.css stops being maintained.
