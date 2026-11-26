# Common commands live in a Makefile, and CI's check job runs its targets

Status: accepted (2026-11-26, PR #212)

## Context
The check sequence (citations, sources, tool tests, rerun the derive scripts and diff `analysis/derived/`) was
spelled out separately in CI, RUNBOOK, CLAUDE.md, two fos-work-issue steps and the fact-check reviewer, and the copies
had drifted (some left out `check_sources`, some the derive diff). Changing the test command in PR #212 meant
editing seven files.

## Decision
A root `Makefile` holds the commands: `make check` (`citations sources test derive-check`), `derive`, `lint`,
`site`, `serve`; `make` with no target lists them. CI's check job runs the same targets, one step each so a failure
names its check. Docs and skills say `make check` / `make derive` instead of repeating the commands.

## Options weighed
- **Makefile** (chosen): one place for the commands, a task list (`make help`), no install in the cloud sandbox,
  GitHub's runners or a Mac with the Command Line Tools. Costs: shell recipes with tab rules next to Python, and
  `make` isn't promised in every environment.
- **`tools/check.py`**: stdlib Python, runs anywhere `python3` does and gets a test like every tool. Costs: awkward
  for the npm site build and Ruff, and no task list.
- **Keep the commands in each doc**: nothing new, but they keep drifting.

## Revisit when
An environment that runs the checks lacks `make` (move `check` into `tools/check.py` and keep the Makefile as a
wrapper), or the recipes grow past simple command lists.
