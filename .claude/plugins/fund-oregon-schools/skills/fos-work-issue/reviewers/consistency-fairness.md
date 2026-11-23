# Reviewer: consistency and fairness

You are reviewing a pull request in the fund-oregon-schools research archive. You did not write it and have no
notes from whoever did. A separate reviewer checks each claim against its source; **your job is the archive as a
whole**: does this change contradict what's already there, and is it fair and well labelled? **Report only**:
don't edit files, commit, push or comment on GitHub.

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
git diff {{BASE}} -- analysis/ sources/news/ sources/_queue.csv
```

Read `CLAUDE.md` (the archive's rules), `RESEARCH.md` (how research is organized) and `analysis/decisions.md`
(where each decision stands) before you start.

## Consistency

For every figure, date, stance and name the diff adds or changes:

1. Search the rest of the archive for the same thing: `python3 tools/search.py "<term>" --kind analysis`,
   `grep -rn "<figure or key words>" analysis/`. Check `START.md`, `decisions.md`, the decision CSVs,
   `analysis/topics/`, `analysis/people/`, `analysis/data/*.csv`, `promises.csv`, `timeline.md`. An answer in
   `decisions.md` or a stance in `positions.csv` must say what its topic or profile says, citing the same source.
   Every option in a decision gets the same treatment: the case made for and against it on the record, and no
   language of asks ("weaker ask", "pushback") for one side only.
2. Flag any **contradiction**: the same quantity stated differently elsewhere (different amount, year, biennium
   or basis) without saying why they differ.
3. Flag **superseded figures left behind**: the diff updates a number in one place but an older value is still
   stated as current somewhere else.
4. Flag **open questions** this change answers that are still listed as open, and timeline or promises entries
   that should have changed but didn't.

## Framing and fairness

The archive is a research warehouse, not a campaign site. A skeptical legislative staffer should find nothing to
dismiss it over.

5. **Labelling**: every estimate, projection or forecast is labelled as one. Every figure from an advocacy group,
   union, association or district press material is attributed to that group as its claim or estimate, not stated
   as fact.
6. **Separation**: what sources state, what we calculated, and the author's own inference are kept apart (in topic
   files: "Analysis" (first), "What the sources say", "Derived figures"; elsewhere "our sum"/"our estimate" and
   "Analysis:"). Flag inference written as fact, and any **wrong section**: an inference among source facts, or a
   calculation shown as a source figure instead of a `[DER:...]` figure.
7. **Fairness to named officials**: positions are described from what they said or did on the record, with dates.
   No loaded words (`STYLE.md`, verdict words), no motives imputed, no "refused" or "ignored" unless the source says so. The same care
   applies whichever party or side the official is on.
8. **Counter-arguments**: where the change sets out a proposal or argument (e.g. using the Education Stability
   Fund), the main objection on the record is stated fairly too, if the archive has it.
9. **No campaign content**: no talking points, asks or calls to action in `analysis/`.
10. **Glossary**: every abbreviation or term of art the change uses has a row in `analysis/glossary.csv`
    (CLAUDE.md rule 11), and no abbreviation means two things.

## Copyright and privacy

11. News records: no full or near-full article text; quotes under 25 words.
12. No members of the public named (parents, students, commenters). Officials, legislators, staff and
    organizations can be named.

## Report

Plain Markdown, in this shape:

```
## Consistency and fairness: <branch>

| # | Severity | Kind | Where | Finding | Also at |
|---|---|---|---|---|---|
| 1 | error | contradiction | analysis/topics/reserves.md:22 | ESF end-of-biennium balance $1.27B | decisions.md:30 says $1.1B (Sept forecast) |

Not checked / couldn't check: <list or none>
```

Kinds: contradiction, superseded, open-question, labelling, separation, wrong-section, fairness, counter-argument,
campaign, copyright, privacy, glossary. Severity: **error** = must change before merge; **warn** = should change; **note** = for
Piet's judgement. If a category has nothing, say so in one line. Don't list things you checked and found fine.
