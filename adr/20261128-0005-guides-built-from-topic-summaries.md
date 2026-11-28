# Guides walk through topics in order, built from each topic's summary

Status: accepted (2026-11-28, PR #TBD)

## Context
Each topic holds the evidence on one subject, and Start here and What's being decided assume the reader knows how
the pieces fit together. A reader who doesn't know what the State School Fund is has nowhere to start (#188).
Topics already carry a cited-below `summary` written for that reader (`adr/20261124-0555-topic-summaries-in-front-matter.md`),
and charts and diagrams are their own entities, embedded by id (`adr/20261125-0411-visuals-as-derived-entities.md`).

## Decision
A new page type, **guides**: `analysis/guides/<slug>.md`, published at `/guides/<slug>/` and listed at `/guides/`
and in the main navigation.
- **Front matter:** `title` (optional, as for topics), `description`, `summary` (shown as "In short") and `topics`,
  the ordered list of the topics whose summaries the guide shows, written as a block list (`topics:` then
  `  - <slug>` lines). `tools/common.py` reads block lists for this; the site's YAML reader reads them the same way.
- **Body:** one `##` section per step. Each step places a topic's summary with `<!-- site: summary <slug> -->`,
  shown with a link to the topic, and joins it to the next step with a sentence or two of our own. A guide makes no
  claims beyond those joining sentences, and they're cited like any analysis. The front-matter summary and
  description follow the topics' rules: no citations, nothing the page doesn't back.
- **Order:** `topics` is the declared order, and the markers say where each summary goes. `check_citations.py`
  fails unless the markers match the list exactly: every topic exists and appears once, in the same order. A step
  with no topic (one whose evidence isn't researched yet, or one that only points to other pages) has joining
  sentences only.
- **Visuals:** guides embed visuals by id, like any page, and never draw their own.
- **Review:** the fact-checker checks every joining sentence and every visual a guide embeds. The topic summaries
  are checked where they live.
- **Readability check:** before a guide merges, read the built page on a phone-width screen. If it reads like a list
  of summaries rather than a walkthrough, say so in the PR; the maintainer decides whether to fall back to
  hand-written steps for that guide.

## Options weighed
- **Steps built from topic summaries plus joining sentences** (chosen): almost nothing new to fact-check, and a
  guide updates when a topic's summary changes. Cost: summaries were written to stand alone, so a guide can read
  like a list, repeat a fact across steps, or show a summary that answers a different question than its step.
- **Hand-written steps:** reads as one walkthrough. Cost: every step needs its own citations and a check whenever a
  linked topic changes, so guides drift from their topics.
- **Topic order in the body only** (markers, no front-matter list): one place to edit. Not chosen: the maintainer
  wanted the order declared in front matter, where tools and the build read it without parsing the body.
- **Topic order in front matter only** (no markers): the build would have to guess where in a step each summary
  goes, and a step with two topics or none doesn't fit a one-topic-per-step list.
- **A topic shown in more than one step:** not allowed, so the same summary never appears twice on a page; a later
  step links to the topic in a joining sentence.

## Revisit when
A guide's built page reads like a list and the maintainer chooses hand-written steps for it (record which guides,
and how their citations are kept in step with the topics), a guide needs a step drawn from something other than a
topic (a decision or a person), or summaries start being written to suit a guide rather than their topic.
