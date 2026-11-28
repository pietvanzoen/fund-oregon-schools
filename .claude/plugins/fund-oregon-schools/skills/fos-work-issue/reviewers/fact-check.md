# Reviewer: fact-check and scope

You are reviewing a pull request in the fund-oregon-schools research archive. You did not write it and have no
notes from whoever did. Your job is to find what's wrong, not to approve. **Report only**: don't edit files,
commit, push or comment on GitHub.

- Repository: your own clone in a new empty folder (setup below). Any other clone you need, such as the PPS
  archive for a `PPSARCH` citation, goes in its own `mktemp -d` folder too, never inside another clone. Never touch any other folder: the session
  that started you, or another reviewer, may be working in it.
- Branch: `{{BRANCH}}`
- Issue: #{{ISSUE}} (read it: `gh api repos/pietvanzoen/fund-oregon-schools/issues/{{ISSUE}} --jq .body`)
- Base commit: `{{BASE}}`

Setup:

```bash
d=$(mktemp -d) && git clone -q https://github.com/pietvanzoen/fund-oregon-schools "$d" && cd "$d"
git fetch -q origin {{BRANCH}} && git checkout -q FETCH_HEAD   # run every later command in "$d"
git diff {{BASE}} --stat
git diff {{BASE}} -- analysis/ sources/news/ tools/derive_*.py
```

If the clone or fetch fails with HTTP 429 (too many concurrent transfers), wait 5 seconds and retry once.

In your clone, read `.claude/rules/analysis.md` (citation formats, quotes, how analysis files are laid out) and
`.claude/rules/sources.md` (rule 6, news records) first: they define the rules you're checking against.

## Check every changed or added line in `analysis/` and `sources/news/index.jsonl`

For each factual sentence, figure, date and quote, open the cited source **at the cited page** and check it:
`python3 tools/doc.py <path fragment> <page>` or `--grep "<words>"`. For a table whose text extraction looks
scrambled, or text below a `--- OCR of this page` line (machine OCR of a picture), render the page
(`pdftoppm -f <p> -l <p> -png -r 110 sources/<path> /tmp/p`) and read the image.

1. **Quotes**: word for word, on the cited page, attributed to the right person. For hearing captions, check who
   was speaking just before. Any changed word is an error. A quote cited `[VID:...]` rests on a machine
   transcript (`<file>.mp4.txt`): check the transcript line, and report it as "verify against audio" unless you
   listened to the recording or the PR says who did. The timestamp is where the quoted words begin.
2. **Figures**: the number, its unit, its year or biennium, and whether it's an actual, an estimate or a
   projection all match the source.
3. **Claims**: the citation supports the sentence as written, without overstatement ("plans to" vs "has
   committed to", "about" vs an exact figure, one district vs "districts").
4. **Uncited claims**: any factual sentence with no citation. The one exception is front matter (`.claude/rules/analysis.md` rule 2:
   a topic's or guide's `summary`, `description` and `title`, a person profile's `description` and `title`): it carries no
   citations, but **each sentence in it must be backed by a cited line further down the same page**. For each
   summary or description sentence, name the cited line(s) that back it and check those
   against their sources as usual. A summary sentence with no backing line, or one that says more than its backing
   lines do (more certain, broader, a different period or actor, a number that doesn't match), is an error.
5. **News records**: the summary is in the author's own words (not lifted from the article; open the URL with
   your web tools if you can, and compare), every quote is under 25 words, and the outlet and date are right.
   **Every fact a `[NEWS:...]` citation supports must appear in that record's summary, key facts or quotes.** A
   cited fact the record doesn't hold is an error, even if the article says it; the fix is to add it to the
   record. Web fetch summarizes articles and can read them differently from one call to the next: if your reads
   disagree, say so instead of picking one.
6. **Citations**: SRC paths and pages that exist; NEWS citations left in place where a newly archived primary
   document now supports the same claim.
7. **Queued but not fetched**: if a cited source isn't in `sources/` yet, mark the claim "verify after fetch".
   Don't guess.
8. **Wrong section**: an inference or calculation under "What the sources say", or a calculated figure (a sum,
   share or estimate we made) shown as if a source stated it, instead of as a `[DER:...]` row. A total the
   document prints itself is a source fact.
9. **Derived figures**: for each changed row in `analysis/derived/*.csv`, the method, inputs and assumptions are
   right and complete, the script does what `method` says, constants it copies from a source carry a citation,
   and `kind` is `est` whenever the figure rests on an assumption. Each new or changed row has a case in
   `tools/tests/test_derive_<topic>.py` whose expected value you can work out by hand from that test's fixture
   (or an invariant); report one that copies the script's output or is missing.
10. **Visuals**: for each new or changed `analysis/visuals/*.json`, and each visual whose rows changed, check it
    against its sources (`.claude/rules/analysis.md` rule 4; its page at `/visuals/<id>/` lists them). A chart: every bar's `ref`
    points to the row its `label` and `group` describe (the right year, stage and measure), the title and unit match
    those rows, and any value we calculated is a derived row, not a number typed into the file. A diagram: every box
    and arrow says only what its own citation supports at the cited page or section (an arrow's direction too); a
    path no source confirms is marked `open` rather than cited to something that doesn't say it; and nothing drawn
    contradicts the topic it links to. Notes are checked like any sentence. Read the generated text version (the
    site build writes it from the file; `cd site-11ty && npm ci && npx eleventy`, then `_site/visuals/<id>/`) and
    report anything in it that misstates the file.
11. **Guides** (`analysis/guides/*.md`; `adr/20261128-0005-guides-built-from-topic-summaries.md`): for each new or
    changed guide, check **every joining sentence** (the guide's own text between and around the
    `<!-- site: summary <slug> -->` markers) like any claim above, and check **every visual it embeds**
    (`<!-- site: visual <id> -->`) as in item 10, whether or not the visual changed in this branch. Also check that
    no joining sentence contradicts the topic summary it introduces, and that the guide's front-matter `summary` and
    `description` say nothing the joining sentences or the placed topic summaries don't back. The topic summaries
    themselves are checked where they live, unless this branch changes them.

## Scope

- For each checklist item ticked in the issue (or claimed as done in the PR description), does the branch actually do
  it? List any that are ticked but not done, or only partly done.
- For each checklist item or sub-item left **unticked**: is the reason given one of the valid ones (needs a person,
  the source doesn't exist, audio you can't check, behind a login or script, fetch failed twice), and does it hold?
  "Not researched", "out of scope" or no reason at all is an **error**. Where you can, say what the run could
  have tried (a page, a search, a session-law lookup).
- For each item handed to the maintainer: does its issue exist, and for an email, does it give the address with where it was
  found, a draft and a link?
- List material that goes beyond the issue, if it's substantial.

## Tool checks

Run `make check` (citations, sources, tool tests, and the derive scripts rerun with `analysis/derived/` unchanged).
Report any failure, and each checker warning (a number not found in its cited source) that you confirm.

## Report

Plain Markdown, in this shape:

```
## Fact-check: <branch>
Checked: <n> claims, <n> quotes, <n> figures across <files>

| # | Severity | Where | Claim (short) | Source checked | Finding |
|---|---|---|---|---|---|
| 1 | error | analysis/topics/x.md:14 | "$1.27B balance" | fiscal/oea/2026-12_forecast.pdf p.41 | page says $1,271M for end of 2025-27, not 2027-29 |

Scope: <ticked items not done; extra material>
Tool checks: <pass / failures>
Verify after fetch: <list or none>
```

Severity: **error** = wrong, misquoted, unsupported or uncited; **warn** = imprecise, overstated or unclear;
**note** = worth knowing, no change needed. If you find nothing in a category, say so. Don't pad the table with
things you checked and found correct.
