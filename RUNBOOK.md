# RUNBOOK: adding and refreshing sources

Answering questions needs none of this; see `.claude/plugins/fund-oregon-schools/skills/fos-research/SKILL.md`.

## Add a document (most common)
1. Find the official URL (prefer the agency's own PDF over a news write-up). Copy it from a link on the agency's
   page; don't build it from a file-name pattern (dated names change when a document is revised).
2. Add a row to `sources/_queue.csv`: `url,path,title,date,kind,notes`. Pick `path` by the conventions in
   `CLAUDE.md` (e.g. `fiscal/oea/2026-11_forecast.pdf`, `legislature/olis/2027R1/<docId>_<slug>.pdf`).
   End `notes` with `from: <page URL>` (the page the link was on), so a dead link can be re-found there.
3. Commit to `main` (or merge a PR). The **fetch-sources** Action runs on any change to the queue: it downloads
   new rows, writes `<file>.txt`, OCRs PDF pages with little text (see OCR below), appends to `sources/_manifest.jsonl`, runs the citation check and commits.
   It also runs on pushes to `claude/**` branches and commits the fetched files back to that branch, so an
   agent's PR can queue documents and cite them in one go. `python3 tools/check_sources.py` (also in CI) checks
   queue rows and that every archived file has a manifest line.
   The Action pushes with a deploy key (secret `FETCH_DEPLOY_KEY`, key listed under Settings → Deploy keys with
   write access), because the `main` ruleset requires PRs and only lets roles and deploy keys bypass it.
4. You can also start it by hand: Actions → fetch-sources → Run workflow (tick "refresh" to re-download everything).
5. Downloads are retried (3 attempts, on timeouts, connection errors, 429 and 5xx). If any row still fails, the run
   still commits what did download, then turns red; the job summary lists each failed path, error and URL. Failed
   rows stay in the queue: re-run the workflow, or fix the URL if the error is a 404.

Why an Action: Claude's cloud sandbox can't reach oregon.gov or olis.oregonlegislature.gov; GitHub's runners can.
On your own computer `python3 tools/fetch_sources.py` does the same (needs `pdftotext` from poppler for PDF text;
`tools/ocr_pdfs.py` also needs `tesseract`).

## Weekly refresh
The Action re-fetches everything on Monday mornings. A changed document keeps its old copy in `<dir>/_prior/`
and is logged in `sources/_versions_log.csv`. A document removed or moved upstream shows up as a failed download
(the run turns red); the archived copy stays. Watch `gov/budget/grb_page.html` around Dec 1 for the 2027-29
budget link, then queue the budget PDFs themselves.

## Things the fetcher can't do
- **Hearing video.** Legislative video is on the Legislature's own player, not YouTube. Save the audio or video
  by hand under `sources/legislature/video/<date>_<committee>.<mp4|m4a|mp3|wav|webm>` with a manifest line, and
  cite `[VID:legislature/video/<date>_<committee>@H:MM:SS]`. Keep files under GitHub's 100 MB limit (audio only,
  if the video is bigger).
- **Pages behind scripts or logins.** Save from a browser and add a manifest line by hand (url, fetched_at, sha256).
- **News.** Don't archive articles. Add a record to `sources/news/index.jsonl`: id `NEWS-YYYYMMDD-outlet-N`, date,
  outlet, title, url, a summary in your own words, key facts, and at most short quotes (< 25 words). To correct
  a record, recheck it against the article and add a dated `note` saying what changed (`CLAUDE.md` rule 6).

## OCR
After each fetch, `tools/ocr_pdfs.py` looks at every archived PDF without a `<file>.pdf.ocr.txt`. Pages that have an
image and under 200 characters of extractable text (slides whose tables and charts are pictures, scans) are OCR'd
with tesseract. It writes `<file>.pdf.ocr.txt`: the `.txt` text with each OCR'd page's OCR text added below a
`--- OCR of this page ...` line, so page numbers and exact text stay the same. `tools/doc.py`, `tools/search.py` and
the citation check read it in place of the `.txt`. OCR misreads characters and numbers: check the PDF page before
quoting or copying a figure from below that line. To redo a file, delete its `.ocr.txt` and rerun fetch-sources.
A page with more text than that but a chart as a picture isn't OCR'd; look at the PDF page for those.

## Transcripts
The **transcribe** Action runs on pushes to `main` and `claude/**` that add audio/video under `sources/`
(including files fetch-sources commits). For each media file without one, it writes a machine transcript next
to it, `<file>.txt` (e.g. `x.mp4.txt`), one `H:MM:SS text` line per segment, and commits it. It never touches
the media file or an existing transcript; delete the transcript and rerun to redo it. For files added before
the Action existed, or a push it missed: Actions → transcribe → Run workflow (on the branch that has the files).
It uses faster-whisper `small.en` on CPU, roughly an hour per 3-hour hearing (estimated). Transcripts are
machine-made: verify every quote by listening at the timestamp before citing it.

## After adding sources
- Update `analysis/` and swap NEWS citations for SRC ones where a primary document now exists.
- `python3 tools/check_citations.py` and `python3 tools/test_tools.py` must pass (CI runs both).
- If a data file or derive script changed, run every `tools/derive_*.py` and commit `analysis/derived/`; CI reruns
  them and fails if the output differs.
