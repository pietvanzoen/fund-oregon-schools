# RUNBOOK: adding and refreshing sources

Answering questions needs none of this; see `.claude/skills/fund-oregon-research/SKILL.md`.

## Add a document (most common)
1. Find the official URL (prefer the agency's own PDF over a news write-up).
2. Add a row to `sources/_queue.csv`: `url,path,title,date,kind,notes`. Pick `path` by the conventions in
   `CLAUDE.md` (e.g. `fiscal/oea/2026-11_forecast.pdf`, `legislature/olis/2027R1/<docId>_<slug>.pdf`).
3. Commit to `main` (or merge a PR). The **fetch-sources** Action runs on any change to the queue: it downloads
   new rows, writes `<file>.txt`, appends to `sources/_manifest.jsonl`, runs the citation check and commits.
   It also runs on pushes to `claude/**` branches and commits the fetched files back to that branch, so an
   agent's PR can queue documents and cite them in one go. `python3 tools/check_sources.py` (also in CI) checks
   queue rows and that every archived file has a manifest line.
4. You can also start it by hand: Actions → fetch-sources → Run workflow (tick "refresh" to re-download everything).
5. Downloads are retried (3 attempts, on timeouts, connection errors, 429 and 5xx). If any row still fails, the run
   still commits what did download, then turns red; the job summary lists each failed path, error and URL. Failed
   rows stay in the queue: re-run the workflow, or fix the URL if the error is a 404.

Why an Action: Claude's cloud sandbox can't reach oregon.gov or olis.oregonlegislature.gov; GitHub's runners can.
On your own computer `python3 tools/fetch_sources.py` does the same (needs `pdftotext` from poppler for PDF text).

## Weekly refresh
The Action re-fetches everything on Monday mornings. A changed document keeps its old copy in `<dir>/_prior/`
and is logged in `sources/_versions_log.csv`. A document removed or moved upstream shows up as a failed download
(the run turns red); the archived copy stays. Watch `gov/budget/grb_page.html` around Dec 1 for the 2027-29
budget link, then queue the budget PDFs themselves.

## Things the fetcher can't do
- **Hearing video.** Legislative video is on the Legislature's own player, not YouTube. Save the audio and a
  transcript by hand under `sources/legislature/video/<date>_<committee>.*` with a manifest line, and cite
  `[VID:legislature/video/<date>_<committee>@H:MM:SS]`.
- **Pages behind scripts or logins.** Save from a browser and add a manifest line by hand (url, fetched_at, sha256).
- **News.** Don't archive articles. Add a record to `sources/news/index.jsonl`: id `NEWS-YYYYMMDD-outlet-N`, date,
  outlet, title, url, a summary in your own words, key facts, and at most short quotes (< 25 words).

## After adding sources
- Update `analysis/` and swap NEWS citations for SRC ones where a primary document now exists.
- `python3 tools/check_citations.py` and `python3 tools/test_tools.py` must pass (CI runs both).
- Add a line to `changelog/`.
