# A wrong news record is corrected in place, with a dated note

Status: accepted (2026-11-22, PR #127)

## Context
`sources/` is primary material and is never edited, but `sources/news/index.jsonl` holds our own summaries of
articles, not the articles. On #120 a record carried over from a research brief called Tammy Carpenter "Rep." while
the KATU article calls her "Rep.-elect"; the analysis cited the record, so the error passed every check.

## Decision
A news record may be corrected after rechecking it against the article: fix the summary or key facts, add a dated
`note` saying what changed, and say so in the PR (`CLAUDE.md` rule 6). Never correct one from memory or from another
outlet. All other files in `sources/` stay untouchable.

## Options weighed
- **Never edit; add a second record for the same article**: keeps history in the file, but leaves the wrong
  summary citable and doubles the ids for one article.
- **Correct in place with a dated note** (chosen): one record per article stays accurate; git history and the note
  keep what changed and why.
- **Edit freely**: simplest, but loses the reason for the change and invites edits not checked against the article.

## Revisit when
A correction is disputed, or records need a full version history the note and git log don't give.
