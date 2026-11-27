---
paths:
  - "analysis/**"
---
# Rules for `analysis/` (moved from CLAUDE.md; rule numbers kept)

Contents: rules 2 (citations), 3 (quotes), 4 (sources, calculations and inference kept apart; the topic-file layout), 5 (advocacy), 8 (structured files), 10 (independent review), 11 (glossary); Key files.

2. `analysis/` is derived. Every factual claim carries a citation, with one exception: front matter (rule 4: a
   topic's `summary`, `description` and `title`, a profile's `description` and `title`) has no citations, and every
   sentence in it restates a cited line further down the same page:
   - Archived file: `[SRC:<path under sources/> p.<page>]` (page = PDF page; `.pdf.txt` separates pages with \f).
     Omit `p.` for HTML pages, and for a claim about a whole PDF ("mentions no charter bill"). Path conventions: `.claude/rules/sources.md`.
   - Hearing or meeting video/audio: `[VID:<path under sources/ without extension>@H:MM:SS]`. The `transcribe`
     Action writes a machine transcript next to each media file (`<file>.mp4.txt`, lines `H:MM:SS text`);
     `tools/search.py` searches it and returns `[VID:...@H:MM:SS]` hits.
   - News: `[NEWS:<id from sources/news/index.jsonl>]`
   - PPS archive: `[PPSARCH:<that repo's own tag>]`, e.g. `[PPSARCH:BB:14673756 p.2]`. Don't copy its files here.
   - Our own calculation: `[DER:<topic>/<id>]`, a row in `analysis/derived/<topic>.csv`. It is not a source: the
     number next to it must match the row's value at the precision shown, and the row names its inputs.
   - A queued source that hasn't been fetched yet may be cited by its planned path; `tools/check_citations.py`
     reports it as pending. Replace NEWS citations with SRC citations once the primary document is archived.
3. Quotes must be verbatim from the source. Keep them short (1–3 sentences). Never invent or "smooth" a quote.
   For transcripts, give speaker attribution with evidence and `confidence: high | medium | low`; don't use low.
   Machine transcripts (Whisper) mishear words and names: listen to the recording at that timestamp and quote
   what was said, never the transcript text unchecked. If you can't listen, don't quote; paraphrase as unverified, or
   ask the maintainer to listen (RUNBOOK, "Checking a quote against a recording": a timestamped link and what to confirm).
   OCR text (below a `--- OCR of this page` line in `<file>.pdf.ocr.txt`) misreads too: check the PDF page.
4. Keep separate what sources state (documents and what people said), what we calculated, and our own inference.
   - Topic files (`analysis/topics/*.md`) start with front matter: a `summary`, shown on the site as "In short":
     two or three plain sentences (`STYLE.md`, "In short"); a `description` for search results and link previews
     (one plain sentence, at most 160 characters); and a `title` when the H1 is over 55 characters (the browser tab
     and search results; at most 55). `tools/check_citations.py` enforces all three and both lengths. Person profiles (`analysis/people/<id>.md`) hold a `description` and may hold
     a `title`; people keep factual cards from `people.csv`, never a summary. Write each as `key: >` with indented
     lines. Like the summary, a description or title carries no citations and says nothing the cited lines below
     don't. Only `key: value` and folded `>` are read (no YAML library), and no other file in `analysis/` has front
     matter. Why: `adr/20261124-0555-topic-summaries-in-front-matter.md`, `adr/20261124-1751-page-titles-and-descriptions-in-front-matter.md`. The H1
     comes right after it.
   - Topic files have three sections, in this order: `## Analysis` (our interpretation;
     no "Analysis:" label needed; first, so the page leads with it, and it reads on its own: point to the evidence as
     "below"), `## What the sources say` (only statements a cited source makes; every line cited; no inference) and
     `## Derived figures` (a table of our sums, shares and estimates, each with its `[DER:...]` tag). Why:
     `adr/20261122-2302-analysis-first-in-topic-files.md`. Inside `## Analysis`, `###` subheadings, paragraph length
     and lists follow `STYLE.md`, "Analysis sections a reader can scan". A total the document prints itself is a source fact; it's derived only when we do the adding.
     Plain unit rescaling ($1,271M as $1.271 billion) is allowed under sources.
   - Every calculated value lives in `analysis/derived/<topic>.csv`, written only by `tools/derive_<topic>.py`
     (one plain script per topic, no shared library). Columns: `id, value, unit, kind, label, method, inputs,
     assumptions`; `kind` is `derived` (plain arithmetic) or `est` (rests on assumptions, listed). A constant the
     script copies from a source carries its citation in a comment. `analysis/data/*.csv` holds only values
     copied from sources.
   - Charts and diagrams are visuals, `analysis/visuals/<id>.json`, embedded with `<!-- site: visual <id> -->`.
     A visual holds no numbers of its own: a bar points to a row (`data/<file>/<id>`, by the data file's `id`
     column, or `derived/<topic>/<id>`), and a value we calculate gets a derive row first. Every note, diagram box
     and arrow carries its own citation; a path no archived source confirms is marked `open` (with why) or left
     out, and the maintainer chooses which. Colour is never the only way to tell bars apart: each bar names its
     group. Embedded in a page, a visual shows no citations or notes and links to its own page, which has both. Why: `adr/20261125-0411-visuals-as-derived-entities.md`.
   - Outside `topics/`, our figures go in their own sentences, marked "our sum" or "our estimate" with
     the DER tag; inference elsewhere starts its own paragraph or list item with "Analysis:". The site shows that
     marker, and a topic's `## Analysis` section, as "Our analysis"; files keep "Analysis:" (#167).
5. Advocacy documents (`orgs/`, district press materials) are labeled as that group's claims or estimates.
8\. Prefer structured outputs (CSV/JSONL) alongside readable Markdown. Every CSV row has a `source` column, except
   `analysis/derived/*.csv`, whose rows name their `inputs`, `analysis/updates.csv`, whose rows name their PR, and
   `analysis/questions.csv`, whose rows are questions, not facts. `analysis/positions.csv` is append-only: never
   edit or delete a row. To correct one, append the corrected row with its `replaces` column set to the line number
   of the row it replaces (as `check_citations.py` reports it, header = line 1); the site shows only the newest
   version. Why: `adr/20261122-1718-correcting-append-only-rows.md`.
10\. **Independent fact-check before a PR is ready.** When a session adds research (new or changed files in
    `analysis/`, new news records, new quotes), it starts a separate fact-checker agent before asking for a merge.
    The fact-checker starts fresh: it gets the branch, the rule files its prompt names and a neutral checklist, not the session's reasoning
    or notes on what's uncertain. It reports only (no edits, pushes or GitHub comments). A second fresh reviewer checks consistency with the rest of the archive and
    fairness of framing, and a third checks clarity against `STYLE.md`
    (`.claude/plugins/fund-oregon-schools/skills/fos-work-issue/reviewers/`). Checklist: every quote verbatim,
    correctly attributed and on the cited page; every factual sentence supported by its citation without
    overstatement; news summaries in own words, quotes under 25 words; nothing in the wrong section (an inference
    among source facts, or a calculation shown as a source figure instead of a DER row), "Analysis:" kept apart from
    fact, and nothing unfair to a named official; derived figures match their method and inputs; uncited claims;
    both tool checks pass. Claims resting on queued, unfetched sources are
    reported as "verify after fetch", not guessed. The session verifies each finding against the source before fixing
    it, and the PR description says what the fact-check found and what changed.
11\. **Glossary.** When analysis uses an abbreviation or term of art that isn't in `analysis/glossary.csv`, add a
    row (cited, like everything else). Acronyms get a short plain-text `tooltip`, shown in a preview card on the
    acronym's first use on each page, which links to the term's page (a term of art gets the same, its card
    showing its tooltip or the start of its definition); every row gets its own page under Glossary, and every page that uses it lists it
    under "Terms on this page". A word this site gives its own meaning (baseline, benchmark, proposal) is `kind: label`:
    listed and linked from "Terms on this page", but not linked in running text. Don't use one abbreviation for two things: OEA is the
    Office of Economic Analysis, so write out "Oregon Education Association".

## Key files
- `analysis/people/<slug>.md`, `analysis/people/quotes_all.jsonl` — what officials said, dated and cited
- `analysis/decisions.csv`, `options.csv`, `positions.csv`, `questions.csv` — the decision model (`RESEARCH.md`);
  `analysis/decisions.md` — where each decision stands, with short cited answers
- `analysis/people/people.csv` — everyone with a role in a decision (`id` used across the decision files)
- `analysis/promises.csv` — pledge tracker (who, what, when, status, rating on outcomes, source)
- `analysis/data/*.csv` — SSF history, QEM gap, forecasts, reserves: values copied from sources only
- `analysis/derived/<topic>.csv` — every value we calculated, written by `tools/derive_<topic>.py` (never by hand)
- `analysis/visuals/<id>.json` — charts (`kind: bars`, drawn with Charts.css) and diagrams (`kind: flow`): each
  has its own page at `/visuals/<id>/` with a generated text version, its notes and its sources (all listed at
  `/visuals/`); `id` columns in
  `analysis/data/*.csv` exist for the rows visuals point to
- `analysis/topics/<topic>.md` — topic files: `summary`, `description` (and `title` if the H1 is long) in front matter, then the three sections; each is published on the website automatically
- `analysis/glossary.csv` — abbreviations and terms: full name, hover tooltip, cited definition
- `analysis/START.md` (home page), `analysis/timeline.md`
- `analysis/updates.csv` — What's new for readers (`date, text, page, pr, kind`; `kind` is `correction`,
  `research` or `site`: `adr/20261124-2210-whats-new-kinds.md`; the site shows it newest first with site changes
  last, the overview the latest three that aren't `site`). A PR that changes reader-facing files must add a row with its number (CI checks;
  label `no-update` to waive). The maintainers' record is the PR description
