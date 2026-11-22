# What's new is a CSV with a PR column, checked in CI, not built from commit messages

Status: accepted (2026-11-21)

## Context
What's new (`analysis/updates.md`) was a hand-edited list, and nothing checked that a PR added a line: #51 merged
new research without one. Readers also had no way to get from an entry to the change behind it.

## Decision
`analysis/updates.csv` (`date, text, page, pr`) holds the entries; the site renders What's new and the overview's
latest three from it, each linking its page and its PR. CI (`check_citations.py --pr`) fails a PR that changes
reader-facing files (`analysis/` except `updates.csv`, and the news index) without a row
for its own number. The `no-update` label waives it. Merges should be squash-only (a repo setting Piet sets), so main has one commit per PR.

## Options weighed
- **CSV with a PR column, checked in CI** (chosen): reviewed like any other change, easy to fix after merge,
  enforced before merge. Costs: the row is added after the PR opens (it needs the number), and two open PRs
  that both append can conflict, as the Markdown list did.
- **Build the list from squash-commit messages** (an "Update:" line in each): the PR link comes free and there are
  no conflicts. But the message is written at merge time, often on a phone, with no check after it; a typo means
  rewriting main's history; and the Pages build would need full git history.
- **Keep `updates.md`, add a check that it changed**: least change, but no PR link and a looser check (any edit
  passes).

## Revisit when
Append conflicts in `updates.csv` become a regular chore, or most PRs end up labelled `no-update`.
