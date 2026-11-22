# The fetch-sources bot pushes with a deploy key

Status: accepted (2026-11-20, PR #29)

## Context
Claude's cloud sandboxes can't reach oregon.gov or the Legislature's site, so documents are downloaded by the
`fetch-sources` GitHub Action, which commits them. Once the `main` ruleset required pull requests, the bot's
direct pushes to `main` (after a merge that changes the queue, and on the Monday refresh) would be rejected.

## Decision
The Action checks out with an SSH deploy key that has write access (private half in the `FETCH_DEPLOY_KEY`
secret). Deploy keys are on the ruleset's bypass list, next to Repository admin. The key was generated on Piet's
own machine, so the private key never passed through Claude. Without the secret, checkout falls back to
`GITHUB_TOKEN`: pushes to `claude/**` branches still work and pushes to `main` are refused.

## Options weighed
- **`GITHUB_TOKEN` with GitHub Actions on the bypass list**: no key to manage, but every workflow's token could
  then bypass the PR rule, and a `GITHUB_TOKEN` push doesn't trigger `check` on the bot's commit.
- **A personal access token**: works, but tied to one person's account and broader than the job needs.
- **Deploy key on the bypass list** (chosen): scoped to this repo, only the workflows that use the secret can
  bypass, and its pushes trigger `check`, so the bot's commits are checked too.
- **No bypass; the bot opens PRs**: keeps the rule absolute, but every fetch and weekly refresh would wait on a
  merge.

## Revisit when
The key is exposed or rotated, a second workflow needs to push to `main`, or the bot's commits should get human
review before landing.
