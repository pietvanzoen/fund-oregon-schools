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

## Start here
- **Answering questions:** follow `.claude/plugins/fund-oregon-schools/skills/fos-research/SKILL.md`. Answer from what's in the repo.
- **Adding sources:** follow `RUNBOOK.md`. In short: add a row to `sources/_queue.csv`; the `fetch-sources`
  GitHub Action downloads it (cloud sandboxes usually can't reach oregon.gov or the Legislature's site).
- **Working a research issue end to end:** follow `.claude/plugins/fund-oregon-schools/skills/fos-work-issue/SKILL.md` (queue → fetch on the
  issue branch → analysis → three independent reviewers → PR; Piet merges).
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
2. `analysis/` is derived. Every factual claim carries a citation:
   - Archived file: `[SRC:<path under sources/> p.<page>]` (page = PDF page; `.pdf.txt` separates pages with \f).
     Omit `p.` for HTML pages, and for a claim about a whole PDF ("mentions no charter bill"). Path conventions:
     - `gov/` Governor's office: recommended budgets, press releases, executive orders, letters
     - `legislature/olis/<session>/<docId>_<slug>.pdf` committee meeting documents from OLIS
     - `legislature/bills/` measure text and staff measure summaries
     - `legislature/press/` caucus and committee press releases; `legislature/appointments/` committee assignment memos;
       `legislature/social/` legislators' own social media posts, saved by hand (caption text, exact)
     - `legislature/lpro/` Legislative Policy and Research Office reports (e.g. session summaries)
     - `legislature/laws/` Oregon Laws (session laws) chapters, as `<year>orlaw<NNNN>.pdf`
     - `legislature/ors/` Oregon Revised Statutes chapters; `legislature/constitution/` the Oregon Constitution;
       `legislature/calendar/` the Legislature's session and interim calendars
     - `ode/` Oregon Department of Education, incl. `ode/qec/` Quality Education Commission reports and minutes,
       `ode/ssf/` State School Fund estimates and transparency reports, `ode/charter/` charter school lists and
       guidance, `ode/legislation/` ODE summaries of enacted legislation, `ode/enrollment/` enrollment reports,
       `ode/grants/` ODE grant allocation reports (for example High School Success)
     - `fiscal/oea/` Office of Economic Analysis forecasts; `fiscal/lfo/` Legislative Fiscal Office; `fiscal/lro/` Legislative Revenue Office;
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
   - Topic files (`analysis/topics/*.md`) have three sections, in this order: `## What the sources say` (only
     statements a cited source makes; every line cited; no inference), `## Derived figures` (a table of our sums,
     shares and estimates, each with its `[DER:...]` tag) and `## Analysis` (our interpretation; no "Analysis:"
     label needed). A total the document prints itself is a source fact; it's derived only when we do the adding.
     Plain unit rescaling ($1,271M as $1.271 billion) is allowed under sources.
   - Every calculated value lives in `analysis/derived/<topic>.csv`, written only by `tools/derive_<topic>.py`
     (one plain script per topic, no shared library). Columns: `id, value, unit, kind, label, method, inputs,
     assumptions`; `kind` is `derived` (plain arithmetic) or `est` (rests on assumptions, listed). A constant the
     script copies from a source carries its citation in a comment. `analysis/data/*.csv` holds only values
     copied from sources.
   - Outside `topics/`, our figures go in their own sentences, marked "our sum" or "our estimate" with
     the DER tag; inference elsewhere starts its own paragraph or list item with "Analysis:".
5. Advocacy documents (`orgs/`, district press materials) are labeled as that group's claims or estimates.
6. News is copyrighted: store metadata, a summary in your own words, and at most short quotes (< 25 words each)
   with attribution. Never full article text. (States Newsroom / Oregon Capital Chronicle allows republishing,
   but follow the same rule anyway for consistency.)
7. Describe members of the public, don't name them. Officials, legislators, staff and organizations can be named.
8. Prefer structured outputs (CSV/JSONL) alongside readable Markdown. Every CSV row has a `source` column, except
   `analysis/derived/*.csv`, whose rows name their `inputs`, `analysis/updates.csv`, whose rows name their PR, and
   `analysis/questions.csv`, whose rows are questions, not facts.
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
    row (cited, like everything else). Acronyms get a short plain-text `tooltip`, shown on hover across the whole
    site; `kind: term` rows appear only on the Glossary page. Don't use one abbreviation for two things: OEA is the
    Office of Economic Analysis, so write out "Oregon Education Association".

## Writing code (tools/, workflows, site build)
Least new code that fully does the job; adapted from the ponytail rules
(github.com/DietrichGebert/ponytail). Lazy about the solution, never about the scope.

- **Before writing:** read the affected code and list everywhere the change must reach: callers, tests, the
  workflows, `site_hook.py` and `mkdocs.yml`, both skills and the reviewer prompts, CLAUDE.md, README, RUNBOOK,
  and any record in `adr/` that the change touches or reverses.
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
  `tools/test_tools.py` (plain `assert`, run by CI). Trivial changes don't. Site code (`tools/site_hook.py`,
  `mkdocs.yml`, `overrides/`) gets no tests: CI's `mkdocs build --strict` covers it. Derive scripts
  (`tools/derive_*.py`) get no tests either: they're plain arithmetic on archived data, CI reruns them and fails on
  any change in output, and the fact-checker checks each method; a test would only pin today's numbers.
- **Known limits** go in a comment: `shortcut: <the limit>, <when to upgrade>`.
- **Never cut:** the rules above about `sources/` (keep originals, provenance), citation and quote checks,
  secrets and access handling, accessibility of the site, or anything Piet asked for.
- **PR description ends with** one or two lines: what was skipped or left unchecked, and any risk to know about.

## Key files
- `sources/_queue.csv` — what to fetch (url, path, title, date, kind, notes)
- `sources/_manifest.jsonl` — what was fetched (path, url, final_url, fetched_at, sha256, bytes, content_type)
- `sources/news/index.jsonl` — news records
- `analysis/people/<slug>.md`, `analysis/people/quotes_all.jsonl` — what officials said, dated and cited
- `analysis/decisions.csv`, `options.csv`, `positions.csv`, `questions.csv` — the decision model (`RESEARCH.md`);
  `analysis/decisions.md` — where each decision stands, with short cited answers
- `analysis/people/people.csv` — everyone with a role in a decision (`id` used across the decision files)
- `analysis/promises.csv` — pledge tracker (who, what, when, status, rating on outcomes, source)
- `analysis/data/*.csv` — SSF history, QEM gap, forecasts, reserves: values copied from sources only
- `analysis/derived/<topic>.csv` — every value we calculated, written by `tools/derive_<topic>.py` (never by hand)
- `analysis/topics/<topic>.md` — topic files in the three sections; each is published on the website automatically
- `analysis/glossary.csv` — abbreviations and terms: full name, hover tooltip, cited definition
- `analysis/START.md` (home page), `analysis/timeline.md`
- `analysis/updates.csv` — What's new for readers (`date, text, page, pr`; the site shows it newest first, the
  overview the latest three). A PR that changes reader-facing files must add a row with its number (CI checks;
  label `no-update` to waive). The maintainers' record is the PR description
- `adr/NNNN-<slug>.md` — architecture decision records: context, decision, options weighed, when to revisit
- `sources/**/<file>.pdf.ocr.txt` — the PDF's text plus OCR of its picture-only pages, by `tools/ocr_pdfs.py` in fetch-sources
- `sources/**/<media file>.txt` — machine transcript of an .mp4/.m4a/.mp3/.wav/.webm, by the `transcribe` Action
- Tools: `tools/search.py`, `tools/doc.py`, `tools/linkify.py`, `tools/check_citations.py` (`--measures` for the
  review measures), `tools/check_sources.py`, `tools/fetch_sources.py`, `tools/ocr_pdfs.py`, `tools/derive_<topic>.py`,
  `tools/site_hook.py`, `tools/test_tools.py`
