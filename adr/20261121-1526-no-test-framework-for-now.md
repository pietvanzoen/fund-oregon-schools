# Tests are plain asserts in one script, no framework, for now

Status: accepted, provisional (2026-11-21, PR #36 for the code rules)

## Context
`tools/test_tools.py` is the whole test suite: one script of plain `assert`s, run by CI, that starts a local HTTP
server and a throwaway copy of the repo for the fetcher tests. When the code rules were adopted (#36), the
question was whether a testing library was needed; the answer was no, since `unittest` "would only add structure
we don't need". On 2026-11-21 it was 223 lines with 42 asserts and ran in under a second. Piet expects a
framework to be worth it at some point, so this records when to switch rather than a permanent rule.

## Decision
Keep plain asserts in `test_tools.py`, stdlib only (CLAUDE.md, "Writing code": no framework for tests). Switch
when a trigger below is hit, without reopening the question each time.

## Options weighed
- **Plain asserts in one script** (chosen for now): nothing to install, CI is a bare `python3`, anyone can read
  it. Costs: the first failing assert stops the run, so later failures stay hidden, and there's no running a
  single test.
- **`unittest`** (standard library): separate tests, every failure reported, single-test runs, still no new
  dependency. Costs: class and method boilerplate.
- **pytest**: the nicest to write (plain asserts, fixtures, parametrizing), but the repo's first install step,
  which the stdlib-only rule rules out unless that rule changes too.

## Revisit when
Any of: `test_tools.py` passes about 500 lines; tests start needing shared setup or fixtures; or one failure
hiding another costs real time. Then move to `unittest` first; choose pytest only together with an explicit
change to the stdlib-only rule in CLAUDE.md.
