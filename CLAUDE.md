# Working conventions for this repository (for Claude agents)

Purpose: source archive + cited analysis for a parent campaign asking **Gov. Tina Kotek and the 2027 Oregon
Legislature to fund K-12 public schools in the 2027-29 budget**. Core topics: the State School Fund (SSF), the
Quality Education Model (QEM) and its funding gap, the Governor's Recommended Budget (due Dec 1, 2026), revenue
forecasts and reserves (Education Stability Fund, Rainy Day Fund), what Kotek and key legislators have promised
or said, and how district budget gaps (PPS and others) connect to state decisions.

Structure and rules are modeled on the PPS research archive (github.com/timaelliott/save-our-schools). That repo
has no license, so nothing here copies its code; the tools in `tools/` were written for this repo.

## Start here
- **Answering questions:** follow `.claude/skills/fund-oregon-research/SKILL.md`. Answer from what's in the repo.
- **Adding sources:** follow `RUNBOOK.md`. In short: add a row to `sources/_queue.csv`; the `fetch-sources`
  GitHub Action downloads it (cloud sandboxes usually can't reach oregon.gov or the Legislature's site).
- **The campaign position:** `analysis/BRIEFING.md`.

## Rules
1. `sources/` is primary material. Never edit or paraphrase into it. Add files only through
   `tools/fetch_sources.py` (or by hand with an entry in `sources/_manifest.jsonl`: URL, fetch time, sha256).
   **Always keep originals.** Agencies revise and remove documents. A changed file is moved to `_prior/` and
   logged in `sources/_versions_log.csv`, never overwritten.
2. `analysis/` is derived. Every factual claim carries a citation:
   - Archived file: `[SRC:<path under sources/> p.<page>]` (page = PDF page; `.pdf.txt` separates pages with \f).
     Omit `p.` for HTML pages. Path conventions:
     - `gov/` Governor's office: recommended budgets, press releases, executive orders, letters
     - `legislature/olis/<session>/<docId>_<slug>.pdf` committee meeting documents from OLIS
     - `legislature/bills/` measure text and staff measure summaries
     - `legislature/press/` caucus and committee press releases; `legislature/appointments/` committee assignment memos
     - `ode/` Oregon Department of Education, incl. `ode/qec/` Quality Education Commission reports and minutes
     - `fiscal/oea/` Office of Economic Analysis forecasts; `fiscal/lfo/` Legislative Fiscal Office; `fiscal/lro/` Legislative Revenue Office
     - `districts/<district>/` district budget documents; `orgs/<org>/` advocacy and association documents
   - Hearing or meeting video/audio: `[VID:<path under sources/ without extension>@H:MM:SS]`
   - News: `[NEWS:<id from sources/news/index.jsonl>]`
   - PPS archive: `[PPSARCH:<that repo's own tag>]`, e.g. `[PPSARCH:BB:14673756 p.2]`. Don't copy its files here.
   - A queued source that hasn't been fetched yet may be cited by its planned path; `tools/check_citations.py`
     reports it as pending. Replace NEWS citations with SRC citations once the primary document is archived.
3. Quotes must be verbatim from the source. Keep them short (1–3 sentences). Never invent or "smooth" a quote.
   For transcripts, give speaker attribution with evidence and `confidence: high | medium | low`; don't use low.
4. Keep separate: what documents state, what people said, and your own inference (label it "Analysis:").
5. Advocacy documents (`orgs/`, district press materials) are labeled as that group's claims or estimates.
6. News is copyrighted: store metadata, a summary in your own words, and at most short quotes (< 25 words each)
   with attribution. Never full article text. (States Newsroom / Oregon Capital Chronicle allows republishing,
   but follow the same rule anyway for consistency.)
7. Describe members of the public, don't name them. Officials, legislators, staff and organizations can be named.
8. Prefer structured outputs (CSV/JSONL) alongside readable Markdown. Every CSV row has a `source` column.
9. Run `python3 tools/check_citations.py` before committing analysis changes. CI runs it too.

## Key files
- `sources/_queue.csv` — what to fetch (url, path, title, date, kind, notes)
- `sources/_manifest.jsonl` — what was fetched (path, url, final_url, fetched_at, sha256, bytes, content_type)
- `sources/news/index.jsonl` — news records
- `analysis/people/<slug>.md`, `analysis/people/quotes_all.jsonl` — what officials said, dated and cited
- `analysis/promises.csv` — pledge tracker (who, what, when, source, status)
- `analysis/data/*.csv` — SSF history, QEM gap, forecasts, reserves
- `analysis/timeline.md`, `analysis/open_questions.md`
- Tools: `tools/search.py`, `tools/doc.py`, `tools/linkify.py`, `tools/check_citations.py`, `tools/fetch_sources.py`
