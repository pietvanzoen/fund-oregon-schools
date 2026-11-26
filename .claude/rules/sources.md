---
paths:
  - "sources/**"
---
# Rules for `sources/` (moved from CLAUDE.md; rule numbers kept)

## Path conventions for archived files (rule 2)
Archived files are cited as `[SRC:<path under sources/> p.<page>]` (`.claude/rules/analysis.md`, rule 2). Paths:
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
       `ode/grants/` ODE grant allocation reports (for example High School Success), `ode/state-board/` State Board of
       Education board actions and materials, with meeting recordings in `ode/state-board/video/`, `ode/sia/` Student Investment
       Account legislative reports and progress-marker reports
     - `fiscal/oea/` Office of Economic Analysis forecasts; `fiscal/das/` Department of Administrative Services (budget instructions); `fiscal/lfo/` Legislative Fiscal Office; `fiscal/lro/` Legislative Revenue Office;
       `fiscal/dor/` Department of Revenue; `fiscal/sos/` Secretary of State Audits Division reports
     - `reference/` reference works (e.g. Oregon Encyclopedia) and other agencies' explainers; prefer a primary
       source when one exists
     - `districts/<district>/` district budget documents; `orgs/<org>/` advocacy and association documents

## News records
6. News is copyrighted: store metadata, a summary in your own words, and at most short quotes (< 25 words each)
   with attribution. Never full article text. (States Newsroom / Oregon Capital Chronicle allows republishing,
   but follow the same rule anyway for consistency.) A news record is our own summary, so it may be corrected:
   recheck it against the article (never from memory or another outlet), fix the summary or key facts, add a dated
   `note` saying what changed, and say so in the PR. Why: `adr/20261123-0249-correcting-news-records.md`.

## Key files
- `sources/_queue.csv` — what to fetch (url, path, title, date, kind, notes)
- `sources/_manifest.jsonl` — what was fetched (path, url, final_url, fetched_at, sha256, bytes, content_type)
- `sources/news/index.jsonl` — news records
- `sources/**/<file>.pdf.ocr.txt` — the PDF's text plus OCR of its picture-only pages, by `tools/ocr_pdfs.py` in fetch-sources
- `sources/**/<media file>.txt` — machine transcript of an .mp4/.m4a/.mp3/.wav/.webm, by the `transcribe` Action (or `tools/save_youtube.py` for YouTube recordings, run on the maintainer's Mac)
