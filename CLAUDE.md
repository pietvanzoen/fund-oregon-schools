# Working conventions for this repository (for Claude agents)

Purpose: a research archive (primary sources + cited analysis) on Oregon K-12 funding: how much the state spends,
how it's shared (the formula) and what it buys (results and accountability), focused on
the **2027-29 budget: Gov. Tina Kotek's Recommended Budget and the 2027 Legislature**. It's a data warehouse, not a
campaign site: no talking points or asks; those are made elsewhere from this data. Core topics: the State School Fund (SSF), the
Quality Education Model (QEM) and its funding gap, the Governor's Recommended Budget (due Dec 1, 2026), revenue
forecasts and reserves (Education Stability Fund, Rainy Day Fund), what Kotek and key legislators have promised
or said, how district budget gaps (PPS and others) connect to state decisions, the funding formula, and what the
money buys (results, the Student Investment Account, SB 141 accountability).

Structure and rules are modeled on the PPS research archive (github.com/timaelliott/save-our-schools). That repo
has no license, so nothing here copies its code; the tools in `tools/` were written for this repo.

**The maintainer** is the repo's owner (GitHub `pietvanzoen`): they set scope and order, merge PRs and send the
archive's emails and records requests.

## Start here
- **Answering questions:** follow `.claude/plugins/fund-oregon-schools/skills/fos-research/SKILL.md`. Answer from what's in the repo.
- **Adding sources:** follow `RUNBOOK.md`. In short: add a row to `sources/_queue.csv`; the `fetch-sources`
  GitHub Action downloads it (cloud sandboxes usually can't reach oregon.gov or the Legislature's site).
- **A new lead** (a forwarded email, a link, a note): follow `.claude/plugins/fund-oregon-schools/skills/fos-lead/SKILL.md`
  with the maintainer: archive and vet its documents on a sources PR that merges on its own, and draft issues for the rest.
- **Working a research issue end to end:** follow `.claude/plugins/fund-oregon-schools/skills/fos-work-issue/SKILL.md` (queue → fetch on the
  issue branch → analysis → three independent reviewers → PR; the maintainer merges).
- **What to research and how it's organized:** `RESEARCH.md`: decisions, their baselines and options, dated
  positions and questions; the checks an issue passes before it's labelled `next`; staying neutral; how to write
  so the analysis gets used.
- **How the text reads:** `STYLE.md` (house style: voice, weight, numbers, names, dates). It covers our own
  sentences in reader-facing files; quotes stay verbatim.
- **Why the repo is built this way:** `adr/` (architecture decision records, one per choice, including choices not
  to do something). Read the relevant ones before changing `tools/`, workflows or how `sources/` is stored; add one
  when you weigh options and pick one (template in `adr/README.md`).
- **Where things stand:** `analysis/decisions.md` (what's being decided, per decision) and `analysis/START.md` (the
  website's home page).

## Rules
1. `sources/` is primary material. Never edit or paraphrase into it. Add files only through
   `tools/fetch_sources.py` (or by hand with an entry in `sources/_manifest.jsonl`: URL, fetch time, sha256).
   **Always keep originals.** Agencies revise and remove documents. A changed file is moved to `_prior/` and
   logged in `sources/_versions_log.csv`, never overwritten.
2. `analysis/` is derived. Every factual claim carries a citation, with one exception: front matter (rule 4: a
   topic's `summary`, `description` and `title`, a profile's `description` and `title`) has no citations, and every
   sentence in it restates a cited line further down the same page:
   - Archived file: `[SRC:<path under sources/> p.<page>]` (page = PDF page; `.pdf.txt` separates pages with \f).
     Omit `p.` for HTML pages, and for a claim about a whole PDF ("mentions no charter bill"). Path conventions:
     - `gov/` Governor's office: recommended budgets, press releases, executive orders, letters
     - `legislature/olis/<session>/<docId>_<slug>.pdf` committee meeting documents from OLIS
     - `legislature/bills/` measure text and staff measure summaries
     - `legislature/press/` caucus and committee press releases; `legislature/appointments/` committee assignment memos;
       `legislature/social/` legislators' own social media posts, saved by hand (caption text, exact);
       `legislature/members/` legislators' official member pages and the member listings that link to them, and
       Secretary of State election results for legislative seats (`<election date>_general-election-results_<office>.html`)
     - `legislature/lpro/` Legislative Policy and Research Office reports (e.g. session summaries)
     - `legislature/laws/` Oregon Laws (session laws) chapters, as `<year>orlaw<NNNN>.pdf`
     - `legislature/ors/` Oregon Revised Statutes chapters; `legislature/constitution/` the Oregon Constitution;
       `legislature/calendar/` the Legislature's session and interim calendars
     - `ode/` Oregon Department of Education, incl. `ode/qec/` Quality Education Commission reports and minutes,
       `ode/ssf/` State School Fund estimates and transparency reports, `ode/charter/` charter school lists and
       guidance, `ode/correspondence/` ODE staff's email answers to questions sent for the archive (reply text
       and the question it answers, only when nothing else citable says it; RUNBOOK, "Email replies"), `ode/legislation/` ODE summaries of enacted legislation, `ode/enrollment/` enrollment reports,
       `ode/grants/` ODE grant allocation reports (for example High School Success), `ode/sia/` Student Investment
       Account legislative reports and progress-marker reports
     - `fiscal/oea/` Office of Economic Analysis forecasts; `fiscal/das/` Department of Administrative Services (budget instructions); `fiscal/lfo/` Legislative Fiscal Office; `fiscal/lro/` Legislative Revenue Office;
       `fiscal/dor/` Department of Revenue; `fiscal/sos/` Secretary of State Audits Division reports
     - `reference/` reference works (e.g. Oregon Encyclopedia) and other agencies' explainers; prefer a primary
       source when one exists
     - `districts/<district>/` district budget documents; `orgs/<org>/` advocacy and association documents
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
   what was said, never the transcript text unchecked. If you can't listen, don't quote; paraphrase as unverified.
   OCR text (below a `--- OCR of this page` line in `<file>.pdf.ocr.txt`) misreads too: check the PDF page.
4. Keep separate what sources state (documents and what people said), what we calculated, and our own inference.
   - Topic files (`analysis/topics/*.md`) start with front matter: a `summary`, shown on the site as "In short":
     two or three plain sentences (`STYLE.md`, "In short"); a `description` for search results and link previews
     (one plain sentence, at most 160 characters); and a `title` when the H1 is over 55 characters (the browser tab
     and search results; at most 55). Person profiles (`analysis/people/<id>.md`) hold a `description` and may hold
     a `title`; people keep factual cards from `people.csv`, never a summary. Write each as `key: >` with indented
     lines. Like the summary, a description or title carries no citations and says nothing the cited lines below
     don't. Only `key: value` and folded `>` are read (no YAML library), and no other file in `analysis/` has front
     matter. Why: `adr/20261124-0555-topic-summaries-in-front-matter.md`, `adr/20261124-1751-page-titles-and-descriptions-in-front-matter.md`. The H1
     comes right after it.
   - Topic files have three sections, in this order: `## Analysis` (our interpretation;
     no "Analysis:" label needed; first, so the page leads with it, and it reads on its own: point to the evidence as
     "below"), `## What the sources say` (only statements a cited source makes; every line cited; no inference) and
     `## Derived figures` (a table of our sums, shares and estimates, each with its `[DER:...]` tag). Why:
     `adr/20261122-2302-analysis-first-in-topic-files.md`. A total the document prints itself is a source fact; it's derived only when we do the adding.
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
6. News is copyrighted: store metadata, a summary in your own words, and at most short quotes (< 25 words each)
   with attribution. Never full article text. (States Newsroom / Oregon Capital Chronicle allows republishing,
   but follow the same rule anyway for consistency.) A news record is our own summary, so it may be corrected:
   recheck it against the article (never from memory or another outlet), fix the summary or key facts, add a dated
   `note` saying what changed, and say so in the PR. Why: `adr/20261123-0249-correcting-news-records.md`.
7. Describe members of the public, don't name them. Officials, legislators, staff and organizations can be named.
   Emails and records requests sent for the archive, however they're drafted, may be published in it with their
   reply (RUNBOOK, "Email replies"): write them to be read by the public, with no private details beyond what the
   About page says about who runs the archive.
8. Prefer structured outputs (CSV/JSONL) alongside readable Markdown. Every CSV row has a `source` column, except
   `analysis/derived/*.csv`, whose rows name their `inputs`, `analysis/updates.csv`, whose rows name their PR, and
   `analysis/questions.csv`, whose rows are questions, not facts. `analysis/positions.csv` is append-only: never
   edit or delete a row. To correct one, append the corrected row with its `replaces` column set to the line number
   of the row it replaces (as `check_citations.py` reports it, header = line 1); the site shows only the newest
   version. Why: `adr/20261122-1718-correcting-append-only-rows.md`.
9. Run `python3 tools/check_citations.py` before committing analysis changes, and after changing data or a derive
   script, run every `tools/derive_*.py` and commit `analysis/derived/`. CI runs the check, reruns the scripts and
   fails if `analysis/derived/` changes.
10. **Independent fact-check before a PR is ready.** When a session adds research (new or changed files in
    `analysis/`, new news records, new quotes), it starts a separate fact-checker agent before asking for a merge.
    The fact-checker starts fresh: it gets the branch, this file and a neutral checklist, not the session's reasoning
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
11. **Glossary.** When analysis uses an abbreviation or term of art that isn't in `analysis/glossary.csv`, add a
    row (cited, like everything else). Acronyms get a short plain-text `tooltip`, shown in a preview card on the
    acronym's first use on each page, which links to the term's page (a term of art gets the same, its card
    showing its tooltip or the start of its definition); every row gets its own page under Glossary, and every page that uses it lists it
    under "Terms on this page". Don't use one abbreviation for two things: OEA is the
    Office of Economic Analysis, so write out "Oregon Education Association".

## Writing code (tools/, workflows, site build)
Least new code that fully does the job; adapted from the ponytail rules
(github.com/DietrichGebert/ponytail). Lazy about the solution, never about the scope.

- **Before writing:** read the affected code and list everywhere the change must reach: callers, tests, the
  workflows, the site build (`site-11ty/`, mainly `src/_data/archive.js`), both skills and the reviewer prompts, CLAUDE.md, README, RUNBOOK,
  the entity diagram in `RESEARCH.md` ("The model": a new file type or relationship), and any record in `adr/`
  that the change touches or reverses.
- **Pick the first option that fully works, in this order:** skip it (say so in one line); reuse what's in
  `tools/` (`common.py`, `check_citations.py`, the existing patterns); the Python standard library; a one-liner a
  reader gets at a glance; otherwise the minimum code. Tools in `tools/` stay stdlib-only (heavier jobs run only in GitHub Actions with pinned versions, like OCR,
  transcripts, the site build and the Vale style check; `adr/20261122-1551-vale-in-ci-stdlib-in-tools.md`): no new dependencies, and no
  framework for tests.
- **No unrequested extras:** no abstractions, wrappers, options, config or "for later" code. Deleting beats adding.
  Prefer extending an existing script over a new one.
- **Comments** say only the why the code can't show, in one line.
- **Bugs:** grep all callers first, then fix the cause in shared code.
- **Keep** validation and error handling when moving or merging code.
- **Tests:** anything with branches, loops, parsing, money figures or a new script gets an assert-based case in
  `tools/test_tools.py` (plain `assert`, run by CI). Trivial changes don't. Site code (`site-11ty/`) gets no tests: CI's
  site build (`cd site-11ty && npm ci && npx eleventy`) covers it, failing on a broken internal link, an unknown `[[id]]` or an indexable page with no meta description or with a title or description another page uses. Derive scripts
  (`tools/derive_*.py`) get no tests either: they're plain arithmetic on archived data, CI reruns them and fails on
  any change in output, and the fact-checker checks each method; a test would only pin today's numbers.
- **Known limits** go in a comment: `shortcut: <the limit>, <when to upgrade>`.
- **Never cut:** the rules above about `sources/` (keep originals, provenance), citation and quote checks,
  secrets and access handling, accessibility of the site, or anything the maintainer asked for.
- **PR description ends with** one or two lines: what was skipped or left unchecked, and any risk to know about.

## Key files
- `sources/_queue.csv` — what to fetch (url, path, title, date, kind, notes)
- `sources/_manifest.jsonl` — what was fetched (path, url, final_url, fetched_at, sha256, bytes, content_type)
- `sources/news/index.jsonl` — news records
- `.gitattributes` — our CSVs (`analysis/**/*.csv`, `sources/_*.csv`) are stored with LF endings; archived files
  aren't touched (`adr/20261123-2131-csv-line-endings-via-gitattributes.md`)
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
- `adr/YYYYMMDD-HHMM-<slug>.md` — architecture decision records, named by the UTC time they're created: context,
  decision, options weighed, when to revisit
- `sources/**/<file>.pdf.ocr.txt` — the PDF's text plus OCR of its picture-only pages, by `tools/ocr_pdfs.py` in fetch-sources
- `sources/**/<media file>.txt` — machine transcript of an .mp4/.m4a/.mp3/.wav/.webm, by the `transcribe` Action (or `tools/save_youtube.py` for YouTube recordings, run on the maintainer's Mac)
- Tools: `tools/search.py`, `tools/doc.py`, `tools/linkify.py`, `tools/check_citations.py` (`--measures` for the
  review measures), `tools/check_sources.py`, `tools/fetch_sources.py`, `tools/ocr_pdfs.py`, `tools/save_youtube.py`, `tools/derive_<topic>.py`,
  `tools/test_tools.py`
- Site: `site-11ty/` builds oregonedtrail.org with Eleventy (`cd site-11ty && npm ci && npx eleventy --serve`);
  every page but About (`website/about.md`) is generated from `analysis/` and `sources/` in `src/_data/archive.js`.
  Why Eleventy: `adr/20261124-0837-site-built-with-eleventy.md`
