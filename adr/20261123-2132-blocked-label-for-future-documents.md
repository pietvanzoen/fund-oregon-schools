# Research waiting for a future document is labelled `blocked`, not started

Status: accepted (2026-11-23, PR #N)

## Context
On #85 a comment added an item that needs the Governor's budget (due Dec. 1, 2026). The run couldn't do it and
moved it to #136, which was labelled `auto` and so could be picked up again before the budget exists. A run that
starts such an issue can only write a placeholder or move everything out again.

## Decision
An issue whose checklist needs a document that isn't out yet doesn't get `next`. It's labelled `blocked`, with a
`Waits for: <document>, expected <date>` line in its body; runs skip `blocked` issues, and Piet removes the label
once the document is archived (`RESEARCH.md` check 6; work-issue skill, steps 1 and 2).

## Options weighed
- **Reuse `later`**: already means "Backlog: after the next items", a priority. One label for both would blur the
  backlog.
- **Only a `Waits for:` line, no label**: no new label, but the queue filter and runs would have to parse issue
  bodies.
- **A `blocked` label plus the `Waits for:` line** (chosen): runs skip it by label like `manual`, and the date says
  when to look again.

## Revisit when
`blocked` issues pile up past their expected dates, or a run starts one anyway.
