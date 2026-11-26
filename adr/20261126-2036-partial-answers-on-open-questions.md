# An open question can link to what's known so far; there's no "partly answered" status

Status: accepted (2026-11-26, PR #TBD)

## Context
Some questions can be answered only in part. `esf-pers-relief` (from #22, PR #209) is one: the archive has the
rules for Education Stability Fund money, but not whether pension paydowns count, the statewide cost or who would
qualify. The site showed an answer only for `answered` rows, so readers couldn't see the partial answer.
`tools/check_citations.py` already allowed `answer` on `open` rows.

## Decision
An `open` row in `analysis/questions.csv` may carry `answer`, a link to what's known so far. The site shows it as
"what's known so far" on the Questions page and in the decision Questions tables. The status stays `open` until
the question is fully answered.

## Options weighed
- **A new `partly answered` status**: makes the state explicit, but needs changes to `check_citations.py`
  (`QUESTION_STATUS`, `--measures`), the site and `RESEARCH.md`, and becomes a parking state with no rule for when
  a question is done. Rejected.
- **Keep `open`, allow `answer` on open rows** (chosen): one small site change and one line in `RESEARCH.md`;
  `--measures` keeps counting these rows as open.
- **Split a question into parts**: allowed case by case when one part is fully answerable on its own; not a
  general rule.

## Revisit when
Readers or reviewers can't tell a partly answered open question from one with nothing found yet, or many open
rows sit with a partial answer and no issue working on the rest.
