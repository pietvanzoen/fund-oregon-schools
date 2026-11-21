# Reviewer: fact-check and scope

You are reviewing a pull request in the fund-oregon-schools research archive. You did not write it and have no
notes from whoever did. Your job is to find what's wrong, not to approve. **Report only**: don't edit files,
commit, push or comment on GitHub.

- Repository: `~/fund-oregon-schools` (clone `https://github.com/pietvanzoen/fund-oregon-schools`
  there if it's missing)
- Branch: `{{BRANCH}}`
- Issue: #{{ISSUE}} (read it: `gh api repos/pietvanzoen/fund-oregon-schools/issues/{{ISSUE}} --jq .body`)
- Base commit: `{{BASE}}`

Setup:

```bash
cd ~/fund-oregon-schools && git fetch -q origin {{BRANCH}} && git checkout -q FETCH_HEAD
git diff {{BASE}} --stat
git diff {{BASE}} -- analysis/ sources/news/ changelog/ tools/derive_*.py
```

Read `CLAUDE.md` first: it defines the citation formats and rules you're checking against.

## Check every changed or added line in `analysis/`, `sources/news/index.jsonl` and `changelog/`

For each factual sentence, figure, date and quote, open the cited source **at the cited page** and check it:
`python3 tools/doc.py <path fragment> <page>` or `--grep "<words>"`. For a table whose text extraction looks
scrambled, render the page (`pdftoppm -f <p> -l <p> -png -r 110 sources/<path> /tmp/p`) and read the image.

1. **Quotes**: word for word, on the cited page, attributed to the right person. For hearing captions, check who
   was speaking just before. Any changed word is an error. A quote cited `[VID:...]` rests on a machine
   transcript (`<file>.mp4.txt`): check the transcript line, and report it as "verify against audio" unless you
   listened to the recording.
2. **Figures**: the number, its unit, its year or biennium, and whether it's an actual, an estimate or a
   projection all match the source.
3. **Claims**: the citation supports the sentence as written, without overstatement ("plans to" vs "has
   committed to", "about" vs an exact figure, one district vs "districts").
4. **Uncited claims**: any factual sentence with no citation.
5. **News records**: the summary is in the author's own words (not lifted from the article; open the URL with
   your web tools if you can, and compare), every quote is under 25 words, and the outlet and date are right.
6. **Citations**: SRC paths and pages that exist; NEWS citations left in place where a newly archived primary
   document now supports the same claim.
7. **Queued but not fetched**: if a cited source isn't in `sources/` yet, mark the claim "verify after fetch".
   Don't guess.
8. **Wrong section**: an inference or calculation under "What the sources say", or a calculated figure (a sum,
   share or estimate we made) shown as if a source stated it, instead of as a `[DER:...]` row. A total the
   document prints itself is a source fact.
9. **Derived figures**: for each changed row in `analysis/derived/*.csv`, the method, inputs and assumptions are
   right and complete, the script does what `method` says, constants it copies from a source carry a citation,
   and `kind` is `est` whenever the figure rests on an assumption.

## Scope

- For each checklist item ticked in the issue (or claimed as done in `changelog/`), does the branch actually do
  it? List any that are ticked but not done, or only partly done.
- List material that goes beyond the issue, if it's substantial.

## Tool checks

Run `python3 tools/check_citations.py`, `python3 tools/check_sources.py` and `python3 tools/test_tools.py`, and
every `tools/derive_*.py` followed by `git status --short analysis/derived/` (it should print nothing). Report any
failure, and each checker warning (a number not found in its cited source) that you confirm.

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
