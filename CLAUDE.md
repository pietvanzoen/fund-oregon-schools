# Working conventions for this repository (for Claude agents)

Purpose: a research archive (primary sources + cited analysis) on Oregon K-12 funding: how much the state spends,
how it's shared (the formula) and what it buys (results and accountability), focused on
the **2027-29 budget: Gov. Tina Kotek's Recommended Budget and the 2027 Legislature**. It's a data warehouse, not a
campaign site: no talking points or asks; those are made elsewhere from this data. Core topics: the State School Fund (SSF), the
Quality Education Model (QEM) and its funding gap, the Governor's Recommended Budget (due Dec 1, 2026), revenue
forecasts and reserves (Education Stability Fund, Rainy Day Fund), what Kotek and key legislators have promised
or said, how district budget gaps (PPS and others) connect to state decisions, the funding formula, and what the
money buys (results, the Student Investment Account, SB 141 accountability).

Structure and rules are modeled on the PPS research archive (github.com/timaelliott/save-our-schools). That repo
has no license, so nothing here copies its code; the tools in `tools/` were written for this repo.

**The maintainer** is the repo's owner (GitHub `pietvanzoen`): they set scope and order, merge PRs and send the
archive's emails and records requests.

## Start here
- **Answering questions:** follow `.claude/plugins/fund-oregon-schools/skills/fos-research/SKILL.md`. Answer from what's in the repo.
- **Adding sources:** follow `RUNBOOK.md`. In short: add a row to `sources/_queue.csv`; the `fetch-sources`
  GitHub Action downloads it (cloud sandboxes usually can't reach oregon.gov or the Legislature's site).
- **A new lead** (a forwarded email, a link, a note): follow `.claude/plugins/fund-oregon-schools/skills/fos-lead/SKILL.md`
  with the maintainer: archive and vet its documents on a sources PR that merges on its own, and draft issues for the rest.
- **Working a research issue end to end:** follow `.claude/plugins/fund-oregon-schools/skills/fos-work-issue/SKILL.md` (queue → fetch on the
  issue branch → analysis → three independent reviewers → PR; the maintainer merges).
- **What to research and how it's organized:** `RESEARCH.md`: decisions, their baselines and options, dated
  positions and questions; the checks an issue passes before it's labelled `next`; staying neutral; how to write
  so the analysis gets used.
- **How the text reads:** `STYLE.md` (house style: voice, weight, numbers, names, dates). It covers our own
  sentences in reader-facing files; quotes stay verbatim.
- **Why the repo is built this way:** `adr/` (architecture decision records, one per choice, including choices not
  to do something). Read the relevant ones before changing `tools/`, workflows or how `sources/` is stored; add one
  when you weigh options and pick one (template in `adr/README.md`).
- **Where things stand:** `analysis/decisions.md` (what's being decided, per decision) and `analysis/START.md` (the
  website's home page). Guides (`analysis/guides/`) walk a new reader through topics in order.
- **Rules by area** are in `.claude/rules/`: `sources.md` (archiving: path conventions, news records),
  `analysis.md` (citations, quotes, how analysis files are laid out, glossary) and `code.md` (tools, workflows,
  site build). Each loads on its own when a session reads files in its folders; skills and reviewers also name
  the ones they need. Rule numbers are kept across the files.

## Rules
These apply to every session. The rest are in `.claude/rules/` (above).
1. `sources/` is primary material. Never edit or paraphrase into it. Add files only through
   `tools/fetch_sources.py` (or by hand with an entry in `sources/_manifest.jsonl`: URL, fetch time, sha256).
   **Always keep originals.** Agencies revise and remove documents. A changed file is moved to `_prior/` and
   logged in `sources/_versions_log.csv`, never overwritten.
7\. Describe members of the public, don't name them. Officials, legislators, staff and organizations can be named.
   Emails and records requests sent for the archive, however they're drafted, may be published in it with their
   reply (RUNBOOK, "Email replies"): write them to be read by the public, with no private details beyond what the
   About page says about who runs the archive.
9\. Run `make check` before committing analysis changes (`make` lists every command), and after changing data or a
   derive script, run `make derive` and commit `analysis/derived/`. CI runs the check, reruns the scripts and
   fails if `analysis/derived/` changes.
