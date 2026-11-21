# 0007. Research is chosen by a short list of core questions tied to decision dates

Status: accepted (2026-11-21)

## Context
Issues have come from documents found, gaps noticed and follow-ups, with `next` and `later` set case by case.
Nothing written down said which work matters most before Dec 1 or the 2027 session, or how to tell whether the
archive is useful to the people who make the asks. The archive is growing fast (40+ open issues), so the risk is
depth on low-stakes topics while the questions users will ask first stay open.

## Decision
`RESEARCH.md` keeps about ten core questions, each with who asks it, the decision it serves and a needed-by date.
An issue gets `next` only if it serves a core question, lands before its decision, could change what a user says
or asks, and isn't already answered by an official source. A few review measures (coverage, timeliness, use,
accuracy, collected vs used, focus) are checked at each decision point. They are for steering, not targets.

## Options weighed
- **Core questions with a four-check selection test, reviewed at decision points** (chosen): small, fits the
  existing labels, and points the work at what users need by when. Costs: the list must be maintained, and the
  "use" measure is gathered by hand.
- **Keep choosing issue by issue**: no overhead, but it drifts toward whatever documents turn up.
- **A scored research agenda** (weighting stakes, urgency and effort for every issue): more rigorous, but heavy
  for a volunteer archive, and the scores would invite false precision.
- **Numeric targets** (e.g. N topics per month, a cited share to hit): easy to report, but chasing them would
  reward volume over usefulness.

## Revisit when
The 2027 session ends; or the list changes so often that it needs its own file; or reviewers find issues labelled
`next` that serve no core question.
