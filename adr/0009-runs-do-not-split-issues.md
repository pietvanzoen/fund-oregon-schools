# 0009. Runs don't split issues; scope is set when an issue is labelled `next`

Status: accepted (2026-11-22, PR #PRNUM)

## Context
The work-issue skill told runs to split an issue that looked too big for one PR into sub-issues. Nightly runs split
#25 into #96/#97 and #57 into #102/#103. #97's PR (#108) was small and half its scope moved out again, while #104
(one sub-issue) was still the largest PR. Reviewing all of an issue's context in one PR proved more useful than
smaller PRs, as long as the issue's scope is targeted.

## Decision
Runs never split an issue. Piet sets scope when he labels an issue `next` (a check in `RESEARCH.md`): one
decision's question, or a few closely related ones, in one PR a reviewer can check in one pass. A run that finds an
issue too broad comments with a proposed narrower scope, adds `needs-judgement` and takes the next queue item.
Moving items that need Piet or are blocked into their own issues stays: that's the definition of done.

## Options weighed
- **Split by file count** (the old rule: more than one topic file or decision section, separate source batches,
  more than about six checklist items): mechanical, but cut issues along file lines rather than questions, which
  gave small PRs that lost context and big ones anyway.
- **Split by review load**: closer to what matters, but still a run's guess at scope, and still scatters one
  question's context across PRs.
- **No splitting; scope set at `next`** (chosen): one PR per question keeps its context together, and the person
  who sets priorities also sets size.

## Revisit when
PRs regularly come back too large to review in one pass, or runs often stop on `needs-judgement` for scope.
