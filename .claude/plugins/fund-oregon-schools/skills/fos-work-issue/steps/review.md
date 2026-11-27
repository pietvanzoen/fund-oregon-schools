# Work a research issue: steps 6 (from `SKILL.md`, next to this folder)

## 6. Independent review

Start **all three** reviewers at the same time as fresh agents (not forks: they mustn't see your reasoning). Give each
one only:

- the prompt in `.claude/plugins/fund-oregon-schools/skills/fos-work-issue/reviewers/<name>.md`, filled in with the branch name, the issue
  number and the base commit (`git merge-base origin/main HEAD`)
- nothing else: not your notes, not what you think is shaky, not your own summary of the changes

Reviewers:
- `fact-check.md` — every claim, quote and number against its cited page; derived figures against their method;
  wrong-section findings; scope (do the ticked items really do what the issue asked)
- `consistency-fairness.md` — conflicts with the rest of the archive, superseded figures left behind, framing,
  labelling of estimates and advocacy numbers, wrong-section findings, fairness to named officials, copyright,
  privacy
- `clarity.md` — how the changed reader-facing text reads: paraphrase test against the source, weight and tense,
  scale and baseline for numbers, answer first, clear references, house style (`STYLE.md`)

If you can't start fresh agents, don't skip the review and don't review your own work in their place.
- **You're a background worker another session started** (background workers can't start agents): open the PR
  with "Reviewers pending: run by the session that started this one" at the top of its Review section, don't add
  `needs-human` for that alone, and put the branch, issue number and base commit in your final report. That
  session fills in the reviewer prompts as above, runs the three reviewers on your branch, handles the findings
  as below and updates the PR. So a session that hands an issue to a background worker plans to run its reviewers.
- **No session started you** (a scheduled run without the tool): say "reviewers not run" at the top of the
  Review section and add `needs-human`.

The PR doesn't merge until all three reviews have run.

They report only. For each finding:

1. Check it against the source yourself. Reviewers can be wrong.
2. If it's right, fix it. If it's wrong, record why in one line.
   If two findings pull in opposite directions (one calls a sentence inference, another says it's unclear
   without it), settle it with the source, e.g. cite the page that states it, rather than dropping the claim (a
   November 2025 report named as a committee's was flagged as inference; the fix was a citation to its cover page).
3. Reviews run in up to three rounds, so no substantive fix goes out checked only by you:
   - **Round 1:** all three reviewers, on all of the branch's changes (above).
   - **Round 2:** after substantive fixes (a changed claim, figure, citation or framing; not typo-level), rerun only
     the reviewers whose findings led to those fixes, each limited to the lines changed since its last review
     (list their file:line and the commit in the prompt). A reviewer whose findings needed no substantive fix
     doesn't rerun.
   - **Round 3:** the same again, if round 2's findings led to more substantive fixes: only those reviewers, only
     the lines changed since round 2.
   - If round 3 still finds substantive problems, fix what you can, list the rest in the PR's Review section and add
     `needs-human`; don't start a fourth round.
4. A sentence reworded for clarity can change what it claims. If clarity fixes reword any sentence that states a
   fact, include `fact-check.md` in the next round for those sentences (list their file:line in the prompt), even
   if the fact-checker raised nothing on them.
