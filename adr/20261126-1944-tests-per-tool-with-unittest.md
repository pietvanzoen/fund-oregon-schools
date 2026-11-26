# Every tool has its own test file, run with unittest; derive scripts are tested against hand-worked fixtures

Status: accepted (2026-11-26, PR #TBD). Supersedes [20261121-1526-no-test-framework-for-now.md](20261121-1526-no-test-framework-for-now.md)

## Context
`tools/test_tools.py` had reached 542 lines, one `main()` of 72 asserts sharing one throwaway root, so a failure
stopped every check after it. That hit two of the old record's triggers (about 500 lines; shared setup). Derive
scripts had no tests by rule (`.claude/rules/code.md`): CI reruns them, and a test was thought to "only pin today's
numbers". The UK government's guidance on QA of analysis code (the "Duck Book",
best-practice-and-impact.github.io/qa-of-code-guidance/testing_code.html) separates the two: a test that copies the
code's output only confirms current behaviour, while expected values worked out independently from a small, fake,
readable fixture do test the arithmetic. CI's rerun already covers the regression check.

## Decision
One `tools/tests/test_<tool>.py` per tool, run with `python3 -m unittest discover -s tools/tests` (stdlib), plain
`assert`s inside test methods, shared setup in `tools/tests/helpers.py`. `test_every_tool_has_a_test.py` fails when
a `tools/*.py` has no test file. Derive scripts take their root from `common.ROOT` like the other tools and are
tested against inline fixtures with hand-worked expected values, or invariants where hand-working a row isn't
practical; a script with no data inputs (`derive_csl.py`) gets a run-and-schema test only. Tools that shell out to
programs available only in GitHub Actions (`ocr_pdfs.py`, `save_youtube.py`) test their pure helpers, not the main
flow.

## Options weighed
- **Per-tool files with `unittest`** (chosen): each test independent, every failure reported, single tests
  runnable, a missing test visible by file name, fewer merge conflicts between parallel branches. Costs: a helper
  module, class boilerplate, and a fresh root per test (the suite went from about 2s to about 12s).
- **Per-tool files of plain-assert scripts in a CI loop**: no classes, but a failure still hides the rest of its file.
- **Keep one file**: no move, but every problem above grows with each tool.
- **pytest**: nicer fixtures and parametrizing, but a dependency; `tools/` stays stdlib-only
  ([20261122-1551-vale-in-ci-stdlib-in-tools.md](20261122-1551-vale-in-ci-stdlib-in-tools.md)).
- **Derive tests on the real data**: rejected; they'd duplicate CI's rerun check and break on every data correction.

## Revisit when
The suite takes long enough to slow PRs (share a root per class with `setUpClass`); hand-worked fixtures for a new
derive script get impractical (lean on invariants); or the stdlib-only rule changes (pytest).
