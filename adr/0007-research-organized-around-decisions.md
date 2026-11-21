# 0007. Research is organized around decisions, with questions in a CSV

Status: accepted (2026-11-21)

## Context
For its first two days the archive was organized around a 277-line `BRIEFING.md`, with open items in
`open_questions.md` and work in GitHub issues. Nothing said which research mattered most before Dec 1 or the 2027
session, and the briefing repeated facts that also lived in topics and profiles. Three independent reviews of a
first draft (skeptic, reader, maintainer) found that a decision model drifts toward advocacy unless every decision has
a baseline, that GitHub issues are invisible to the archive's own tools and to readers, and that a packed stances
column escapes the citation check.

## Decision
Research starts from decisions (`analysis/decisions.csv`), each with a baseline and options (`options.csv`), dated
stances (`positions.csv`) and questions (`questions.csv`). Topics and people profiles are the evidence. The briefing,
the overview and `open_questions.md` are removed; the site's home page is `START.md` and the decisions page is built
from the CSVs plus `decisions.md`. Research with no due date (results, the formula, history) is a standing track.
The rules are in `RESEARCH.md`.

## Options weighed
- **A hand-written list of about ten core questions**: one ranked view, but it pins the questions down before
  readers have asked any, and drifts from the issues.
- **Topics phrased as questions**: no separate list, but questions nobody has researched stay invisible.
- **Questions as GitHub issues only**: no new file, but the citation check, the fact-checker, the research skill and
  readers without GitHub accounts can't see them.
- **Decisions, options, positions and questions as CSVs** (chosen): the repo stays the source of truth, every row
  is checked, and the site can show it. Costs: four new files to keep consistent, and a check that their ids agree.
- **Keep the briefing as a view over the CSVs**: a familiar entry point, but a second place that says where things
  stand. The repo was a day old, so nothing depended on it from outside.

## Revisit when
The CSVs get rows nobody updates (stale statuses after a decision is made), or a decision needs fields the model
can't hold (criteria per option, votes), or the end of the 2027 session.
