# Leads are triaged in a session, and their sources merge on their own PR once vetted

Status: accepted (2026-11-24, PR #181)

## Context
Leads (a forwarded email, a link, an agenda) mix documents that exist, documents not out yet and questions.
Until now a document reached `main` only with the research PR that cited it, so other issues and `fos-research`
couldn't use it until that issue's turn in the Research queue, and nothing recorded a lead short of an issue that
met the `next` bar.

## Decision
The maintainer runs the `fos-lead` skill on each lead. It archives each document on a sources-only PR, reads the
archived text and judges it suitable and valuable, merges the PR itself once every document passes, and flags
any doubt with `needs-judgement` for the maintainer. Documents not out yet become `blocked` issues; questions
become drafted research issues the maintainer approves.

## Options weighed
- **Sources stay with research PRs** (before): one PR per issue and reviewed, but a source waits for its issue,
  and other issues can't use it meanwhile.
- **A scheduled runner that archives open `lead` issues**: no one has to be present, but it merges documents nobody
  has looked at and needs a lead issue for every pointer.
- **A `_leads.csv` file**: greppable, but a PR per lead and no place to discuss one.
- **A skill run with the maintainer** (chosen): the judgement calls happen with the maintainer present and only
  vetted documents merge unreviewed; a lead waits until the maintainer sits down with it.

## Revisit when
Leads pile up unhandled, or a document merged this way turns out wrong or off-topic.
