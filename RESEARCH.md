# Research approach

How this archive decides what to research, how the research is organized, and how we tell useful analysis from
analysis for its own sake. `CLAUDE.md` says how to do the work, `RUNBOOK.md` how to add sources, and `adr/` why
the repo is built the way it is.

## In one paragraph

The research starts from **decisions**: choices someone with power will make by a date, such as the Governor's
budget or a draw on the Education Stability Fund. Each decision has **options** on the table, and the people
involved take **positions** on them. Comparing the options raises **questions**, and the questions drive the
research. The **evidence** (sources, figures, topics) is what answers them. An analysis is worth doing when it
helps someone compare options before the decision is made.

## Who it's for

The archive is a warehouse; the asks get made elsewhere, by:

- parents and advocates preparing testimony, letters or talking points;
- reporters covering the budget;
- legislative and district staff checking a figure;
- the volunteers who keep it running.

What each of them needs is a **cited answer they can lift**: one or two sentences with the number, its baseline
and its source. Depth matters only as far as it backs that answer up.

## The model

```
decision ── options ── positions (who stands where)
    │          │
    └── questions (what we'd need to know to compare the options)
               │
            evidence (sources, data, derived figures, topics, quotes)
```

| Entity | What it is | Example | Where it lives |
|---|---|---|---|
| Decision | A choice, who makes it, by when, its status and outcome | Draw on the Education Stability Fund in 2027-29? | `analysis/decisions.csv` |
| Actor | A person or body with a role in a decision: decides, proposes, votes, advises | Sen. Kate Lieber, Ways and Means co-chair | `analysis/people/people.csv` (who they are and their roles); `analysis/people/<slug>.md` (their record) |
| Option | A concrete proposal on the table, who proposed it, what it costs | PPS: $500M to buy down PERS rates statewide | `analysis/options.csv` |
| Position | One person's or body's cited stance on an option | Kotek: against one-time money for ongoing costs | `stances` column in `options.csv` |
| Question | What we'd need to know to compare options | How much would each option save the districts most at risk? | GitHub issue labelled `question` |
| Evidence | What sources say, what we calculated, our analysis | Fund rules, balances, PERS rates | `sources/`, `analysis/data/`, `analysis/derived/`, `analysis/topics/`, `analysis/people/` |

**Topics are evidence, organized by subject** (the Education Stability Fund, PERS, the formula, Measures 5 and 50).
They keep their three sections and grow slowly. Questions add no new facts of their own: a fact lands in a topic
(or a people file or data table) first, and the answer to a question cites it from there.

**People profiles are evidence, organized by person**, the way topics are by subject: what someone has said and
done, dated and cited, with their quotes in `quotes_all.jsonl`. A stance in `options.csv` is a one-line summary
that cites the same source as the profile, so the facts stay in one place. `people.csv` lists every person with a
role in a decision, legislators and others (the Governor, agency heads), one row each with their roles and a link
to their profile. A person gets a profile when they have a role in an open decision; sections follow the decisions
("On the Education Stability Fund"), and what's still missing from a profile is an issue, not a "To add" list.
Organizations (districts, associations) are actors too; their stances go in `options.csv`, and their documents in
`sources/orgs/` and `sources/districts/`, labelled as their claims.

**Start light.** Positions sit in a column of `options.csv`, and criteria (what the deciders weigh) sit in the
question issues. Split either into its own file only when the rows get crowded.

### `decisions.csv`

`id, decision, decided_by, due, status, outcome, source`

- `id`: a short slug, e.g. `esf-draw-2027-29`, also used as the issue label `d:<id>`.
- `status`: `upcoming`, `in progress` or `made`. `outcome` is filled in once it's `made`, with its source.

### `options.csv`

`id, decision, option, proposed_by, proposed_on, amount, stances, source`

- `decision` is a decision `id`. `amount` is as the proposer states it, or empty.
- `stances`: `Name: stance [cite]`, separated by semicolons; only stances someone stated on the record.

### Question issues

Title: the question, as a question. Labels: `question` and `d:<decision id>`. Body:

- **Decision:** which one, and its due date.
- **Options it compares:** by `id`, or "all".
- **Criterion:** what the deciders weigh that this informs (cost, one-time vs ongoing, who qualifies, results).
- **Asked by and needed by:** who raised it, and when the answer is useful by.
- **What would change:** how a plausible answer would change what someone says or asks.

A question closes when a PR answers it: the facts land in topics, and the decision's section in
`analysis/decisions.md` gets a short answer with a link to the closed issue. A question still open when its decision
is made is closed as `not planned`, with a line saying so.

## Choosing what to work on

An issue gets `next` when it passes all four checks; otherwise it stays `later` or is closed with the reason.

1. **It serves a decision that's still open**, and lands before the decision's due date.
2. **It helps compare options** on a criterion the deciders actually use. A question every option answers the
   same way doesn't earn work.
3. **A plausible answer could change something**: what a user says, asks for or supports. This is the
   value-of-information test.
4. **Nobody official already answers it plainly.** If an agency does, archive that document and link to it
   instead of rebuilding it.

Research issues that aren't questions (archiving a document, filling a topic) name the question or decision they
serve. Housekeeping and tooling issues don't need one, but shouldn't crowd out research near a due date.

**Where questions come from**, in order of weight:

1. **The people who use the archive.** "What number or fact do you most wish you had before talking to a
   legislator?" Their answers outrank anything we derive from documents.
2. **The options on the table.** What would you need to know to choose between them?
3. **The pushback.** Each argument a decision-maker is likely to make against an option is a question an advocate
   needs a cited answer to.
4. **Promises and gaps.** What's been pledged, and what the archive admits it can't answer yet.

## What readers see

| Page | Built from | Job |
|---|---|---|
| Start here (the home page) | `analysis/START.md` | What's being decided now, the key numbers, where to go next |
| Decisions | `decisions.csv`, `options.csv`, `analysis/decisions.md` | Per decision: who decides and by when, the options, who stands where, what's known (short cited answers), open questions |
| Topics | `analysis/topics/*.md` | The evidence on one subject |
| People, Promises, Numbers, Timeline, Glossary, Sources | as today | Reference |
| About | `website/about.md` | Who runs the site, how to read it (citation tags, "Analysis:"), contact |

`analysis/decisions.md` holds the hand-written part of the Decisions page: a short "where it stands" and the
answers to closed questions, one section per decision, cited like any analysis. The tables come from the CSVs.

## Writing so it gets used

- **Answer first.** Lead with the answer, then the support (Pyramid Principle, bottom line up front).
- **Always state the baseline.** A gap means nothing without its reference point. Anchor on the state's own
  benchmarks (current service level, full Quality Education Model) and say which one, every time.
- **One claim per sentence, cited in the sentence**, so it can be lifted without the paragraph around it.
- **Say what it means as if/then**, in an "Analysis:" passage: "If the State School Fund lands at the current
  service level, then ...".
- **Write for an intelligent reader who doesn't know the field.** Plain words, the active voice, terms in the
  glossary.
- **Rate promises and positions on outcomes, not intentions**: what was funded, enacted or voted, not what was
  said or tried.

## How we know it's working

Review at each due date: Dec 1, session start, each revenue forecast, and the end of the session. These are for
steering, **not targets**: a measure chased as a target stops measuring anything (citing a document just to raise
the cited share, say).

| Measure | What good looks like |
|---|---|
| Questions answered in time | Most `question` issues closed before their needed-by date |
| Decisions covered | Each open decision has its options and stated positions recorded before its due date |
| Timeliness | The Governor's budget on the Decisions page within 72 h of Dec 1; each forecast compared with the last within a week |
| Use | A figure or quote from here turns up in testimony, letters, talking points or coverage. Noted by hand at review |
| Accuracy | Fact-check findings per PR trending down; few corrections after merge |
| Collected vs used | Most archived documents cited somewhere (85 of 104 on 2026-11-21; command below) |

```bash
# Archived documents (not text copies, news or bookkeeping files) that no analysis cites
find sources -type f ! -name '*.txt' ! -name '_*' ! -path '*/_prior/*' ! -path 'sources/news/*' \
  | sed 's#^sources/##' | sort > /tmp/src.txt
grep -rhoE 'SRC:[^] ]+' analysis | sed 's/SRC://' | sort -u > /tmp/cited.txt
comm -23 /tmp/src.txt /tmp/cited.txt
```

**At each review:** update the decisions' status and outcomes, close or re-date questions, re-rank `next` and
`later`, and add the decisions the next stage raises.

## Practices this draws on

| Practice | What we take from it |
|---|---|
| Decision-driven analytics ([De Langhe and Puntoni](https://www.esade.edu/en/articles/leading-decision-driven-data-analytics)) | Start from the decision and work back to the data, not from the data we happen to have |
| Value of information ([explainer, Resources for the Future](https://www.rff.org/publications/explainers/value-of-science-105-three-principles-of-the-value-of-information/)) | Information is worth gathering only if it could change a decision |
| [Our World in Data's topic and metric criteria](https://ourworldindata.org/choosing-our-topics-and-metrics) | Written selection criteria; measures that are easy for non-experts and hard to misuse |
| Pyramid Principle and SCQA ([Barbara Minto](https://lethain.com/pyramid-principle/)); bottom line up front | Answer first, support underneath; break questions down to plan, write answers top-down |
| Policy brief guidance ([UVM Gund Institute](https://www.uvm.edu/sites/default/files/Gund-Institute-for-Environment/Gund_Guidance_for_Writing_Policy_Briefs_2020.pdf), [Politico Pro template](https://www.politicopro.com/guides-tools/politico-pro-policy-brief-template.pdf)) | If/then implications, written for an intelligent but uninformed reader |
| [PolitiFact promise ratings](https://www.politifact.com/truth-o-meter/promises/biden-promise-tracker) | Rate on verifiable outcomes, with interim and final ratings |
| [Education Law Center, Making the Grade](https://edlawcenter.org/research/making-the-grade/) | A national report card can only compare states; Oregon's own benchmark (the Quality Education Model) lets us say how far from adequate |
| [Goodhart's law](https://en.wikipedia.org/wiki/Goodhart%27s_law) | Measures for review, not targets |
