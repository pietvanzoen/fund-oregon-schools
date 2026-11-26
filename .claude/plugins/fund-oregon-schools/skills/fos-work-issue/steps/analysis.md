# Work a research issue: steps 5 (from `SKILL.md`, next to this folder)

## 5. Write the analysis

Read what you cite, at the page you cite: `python3 tools/doc.py <path fragment> <page>` or `--grep`. For a table
whose extracted text is scrambled, or a fact found in text below a `--- OCR of this page` line (machine OCR of
a picture), render the page and look at it
(`pdftoppm -f <p> -l <p> -png -r 110 sources/<path> /tmp/page`, then Read the image).

**Read a model's method in full before concluding how it treats something.** Before writing a conclusion that
depends on how a model, formula or method counts something (what the Quality Education Model's status quo
includes, what the formula weights), grep the whole document for it, appendices and method notes included
(`python3 tools/doc.py <file> --grep "<term>"` searches every page), and the previous edition of the same report if
it's archived. Put what the method section says in "What the sources say" before the Analysis relies on it. On #85
the main chapters of the 2026 QEM report (pp.100-114) seemed to settle it, but the method appendix says Student
Investment Account and High School Success revenue is netted out of the funding required in several areas
[SRC:ode/qec/2026_qem_report.pdf p.129], and a confident answer had to become a conditional one in review.

Then, as the issue needs:

- Topic file `analysis/topics/<topic>.md`, laid out as `.claude/rules/analysis.md` rule 4 says: front matter, then
  `## Analysis`, `## What the sources say` and `## Derived figures`. It is published on the website automatically,
  titled by its H1. When the research changes what the page found, update the summary and description in the same
  PR.
- Structured data in `analysis/data/<name>.csv` with a `source` column on every row: values copied from sources
  only. A total the document prints is a source value; one we add up is derived.
- Every calculated value (per-row and totals) goes in `analysis/derived/<topic>.csv`, written only by a plain
  `tools/derive_<topic>.py` that reads `analysis/data/` (columns `id, value, unit, kind, label, method, inputs,
  assumptions`; `kind` = `derived` for arithmetic, `est` when it rests on assumptions). Cite any constant the
  script copies from a source in a comment. Never type a derived value by hand. Each new or changed row gets a
  case in `tools/tests/test_derive_<topic>.py`: a value worked out by hand from the test's small fake fixture
  (never copied from the script's output), or an invariant when that isn't practical (`.claude/rules/code.md`, Tests).
- Charts and diagrams as visuals in `analysis/visuals/<id>.json`, embedded with `<!-- site: visual <id> -->`
  (`.claude/rules/analysis.md` rule 4): a bar points to a data row by its `id` (add the column to the data file if it has none) or to
  a derived row; every note, box and arrow is cited; ask the maintainer before leaving out or marking `open` a path
  no source confirms.
- Quotes in `analysis/people/quotes_all.jsonl` and the person's `analysis/people/<slug>.md`.
- Pledges in `analysis/promises.csv` (rate on outcomes, not intentions: `rating` and `rated_on`); dates in
  `analysis/timeline.md`.
- Decision files (`RESEARCH.md`, "The model"): new options in `options.csv` with their formality; each stance stated
  on the record as a new row in `positions.csv` (append, never edit a row; to correct one, append the corrected row
  with `replaces` set to the wrong row's line number, as `.claude/rules/analysis.md` rule 8 says); an answered question's `status` and
  `answer` in `questions.csv`, and its short cited answer in that decision's section of `analysis/decisions.md`.
  Facts land in a topic, profile or data table first; the decision files cite the same source. For #57 (split
  before runs stopped splitting), only the last open sub-issue writes the question's answer.
- Swap NEWS citations for SRC ones wherever the new primary document supports the same claim.
- New questions you hit go in `analysis/questions.csv` as `open` rows (describe the asker; never name a member of
  the public), not as research you chase in this PR.
- Add a row to `analysis/glossary.csv` for every abbreviation or term of art you use that isn't there yet
  (`.claude/rules/analysis.md` rule 11): cited, with a short `tooltip` for acronyms. `check_citations.py` warns on ones it finds.
- `analysis/START.md` and `analysis/decisions.md`: change "where it stands" only when the new material changes
  something already there (a figure, a date, a stance), and call it out in the PR. Our own figures go in their own
  sentence, marked "our sum" or "our estimate" with the DER tag, anywhere outside `topics/`.
- A row in `analysis/updates.csv` (the site's What's new page; the newest three show on the overview), added
  right after you open the PR (step 7), because it needs the PR's number: `date` (today), `text` (what changed,
  in plain words for a parent, one or two sentences; name pages by the title the site shows, their H1, e.g.
  "What's being decided", not by what they're about: #137's first row named "the current service level page",
  which doesn't exist), `page` (the analysis file readers should open, e.g.
  `topics/reserves.md`, or `decisions.md#esf-draw-2027-29`), `pr`, `kind` (`correction` if it corrects anything the
  archive said before, else `research` for new findings, documents or figures, else `site` for how pages look, read
  or are found; `site` rows stay off the overview). Append it at the end; the site sorts. CI fails
  a PR that changes reader-facing files (anything in `analysis/` except `updates.csv`, or the news index) without a
  row for its number. The PR description is the maintainers' record; this is for readers. For a PR readers don't need to hear about (a typo, a citation page fix), the maintainer labels it
  `no-update` instead; don't add that label yourself.

Stay within what the issue asks. Note related gaps as `open` rows in `analysis/questions.csv` or as a follow-up
issue rather than chasing them.

Run, and fix until clean:

```bash
python3 tools/check_citations.py && python3 tools/check_sources.py && python3 -m unittest discover -s tools/tests
for f in tools/derive_*.py; do python3 "$f"; done; git status --short analysis/derived/   # commit what changed
```

Commit and push.
