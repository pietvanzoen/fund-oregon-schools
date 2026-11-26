# Oregon Ed Trail

*Following the money behind Oregon's schools.*

A research archive on Oregon K-12 funding (how much the state spends, how it's shared and what it buys), focused on the **2027-29 budget** (Gov. Tina Kotek's
Recommended Budget and the 2027 Legislature): primary sources, and analysis that cites them claim by claim.

**Browse it:** <https://oregonedtrail.org>, a readable website built from this repo.

**Start here:** [`analysis/START.md`](analysis/START.md) (the home page) and
[`analysis/decisions.md`](analysis/decisions.md): what's being decided, the options, who stands where and what's open.
How the research is organized: [`RESEARCH.md`](RESEARCH.md).

**Ask questions with Claude:** paste this into a new Claude chat and it will set you up (see [`SETUP.md`](SETUP.md)):

> Please set me up using https://raw.githubusercontent.com/pietvanzoen/fund-oregon-schools/main/SETUP.md

**Who runs it:** a volunteer group of Oregon public school parents. Contact: hello@oregonedtrail.org

Modeled on the PPS rightsizing archive ([timaelliott/save-our-schools](https://github.com/timaelliott/save-our-schools)):
primary sources kept untouched in `sources/`, and everything in `analysis/` cites back to them. Portland-specific
material stays in that archive and is cited from here as `[PPSARCH:...]`.

## Layout
- `sources/`: primary documents, untouched, with provenance in `_manifest.jsonl`; `_queue.csv` is what to fetch.
- `analysis/`: everything derived from them, every claim cited. The research model (decisions, options, positions,
  questions, evidence) is in [`RESEARCH.md`](RESEARCH.md).
- `site-11ty/`: the website, built with Eleventy from `analysis/` and `sources/`. Preview it with
  `cd site-11ty && npm ci && npx eleventy --serve`; CI runs the same build on every PR and deploys it from `main`.
- Everything else supports the research: see "How the repo supports the research" at the end of `RESEARCH.md`.

## License
Our analysis and the website text are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): reuse them for
anything, with credit. The code is MIT ([`LICENSE`](LICENSE)). Files in `sources/` belong to their publishers and
aren't covered by either. Details: [`LICENSE-content.md`](LICENSE-content.md).

## Quick use
```bash
python3 tools/search.py "State School Fund"
python3 tools/doc.py 2026_qem_report --grep "current service level"
python3 tools/linkify.py analysis/decisions.md
make check     # what CI's check job runs; `make` lists the other commands
```

## What's in progress and what's next
Open issues carry one status label: `in progress` (being worked; agents add it when they start), `next` (vetted and
ready) or `later` (backlog). The order work happens in is the pinned [Research queue](https://github.com/pietvanzoen/fund-oregon-schools/issues?q=is%3Aopen+label%3Aqueue)
issue: the nightly run, and any session not given an issue number, takes the first free issue in its list, and does
nothing if none is free. The maintainer reorders it by editing the list.

A type label says what kind of work an issue is: `research` (gathering sources or answering a question) or
`enhancement` (site, tooling, style or process). Enhancements have their own ordered list, the
[Enhancements queue](https://github.com/pietvanzoen/fund-oregon-schools/issues?q=is%3Aopen+label%3Aenhancement-queue)
(label `enhancement-queue`). Nothing picks from it automatically: the maintainer starts each item. It must never carry
the `queue` label, which the research skill uses to find the Research queue. Bookmark these:
- [In progress](https://github.com/pietvanzoen/fund-oregon-schools/issues?q=is%3Aopen+label%3A%22in+progress%22)
- [Next](https://github.com/pietvanzoen/fund-oregon-schools/issues?q=is%3Aopen+label%3Anext+-label%3A%22in+progress%22)
- [Later](https://github.com/pietvanzoen/fund-oregon-schools/issues?q=is%3Aopen+label%3Alater+-label%3A%22in+progress%22)
- [Research](https://github.com/pietvanzoen/fund-oregon-schools/issues?q=is%3Aopen+label%3Aresearch) and [Enhancements](https://github.com/pietvanzoen/fund-oregon-schools/issues?q=is%3Aopen+label%3Aenhancement)
- [Not triaged](https://github.com/pietvanzoen/fund-oregon-schools/issues?q=is%3Aopen+-label%3Anext+-label%3Alater+-label%3A%22in+progress%22)
