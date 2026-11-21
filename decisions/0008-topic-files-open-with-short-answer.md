# 0008. Topic files open with the question they answer and a short answer

Status: proposed (2026-11-21). Not in effect until the follow-up below merges; until then CLAUDE.md rule 4 stands.

## Context
Topic files run `What the sources say`, `Derived figures`, `Analysis`. That order is good for checking (facts,
then our sums, then our inference) but buries the point: in `topics/virtual-charters.md` the Analysis section
starts about 250 lines down. Users want the answer first (`RESEARCH.md`, "Writing so it gets used").

## Decision
Each topic file keeps its three sections, and gains two things above them:
- a line under the H1, `Answers: <the core question, as a question>`; the H1 stays short, because it is the
  site's nav label;
- a `## Short answer` of three to five lines. It may only restate what the sections below establish, with the
  same citations and DER tags, and any inference starts with "Analysis:", as elsewhere.

## Options weighed
- **Short answer above the three sections** (chosen): answer-first for readers, and the fact / derived /
  inference split is kept, because the summary follows the same rules. Costs: one more place that has to agree
  with the sections, which the reviewers must check.
- **Keep the three sections only**: nothing to change, but readers have to dig.
- **Put Analysis first**: answer-first, but inference would come before the facts it rests on.
- **Separate one-page briefs per question**: easy to share, but they duplicate the topic files and would drift.

## Follow-up to put it in effect
One PR, through the fact-check (rule 10) since it adds summary text: CLAUDE.md rule 4; both reviewer prompts
(the summary must match the sections below it); the `fos-work-issue` analysis step; and short answers for
`topics/reserves.md` and `topics/virtual-charters.md`. Check `tools/site_hook.py` still renders the Analysis
boxes in the summary.

## Revisit when
Reviewers keep finding short answers that drift from their sections, or users still miss the answer.
