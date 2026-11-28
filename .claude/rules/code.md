---
paths:
  - "tools/**"
  - "site-11ty/**"
  - ".github/**"
---
# Rules for code: `tools/`, workflows, site build (moved from CLAUDE.md)

## Writing code (tools/, workflows, site build)
Least new code that fully does the job; adapted from the ponytail rules
(github.com/DietrichGebert/ponytail). Lazy about the solution, never about the scope.

- **Before writing:** read the affected code and list everywhere the change must reach: callers, tests, the
  workflows, the site build (`site-11ty/`, mainly `src/_data/archive.js`), the skills (each `SKILL.md` and fos-work-issue's `steps/`), the reviewer prompts, CLAUDE.md and
  `.claude/rules/`, the nightly scheduled task's prompt (it calls `tools/next_issue.py`; tell the maintainer), README, RUNBOOK,
  the entity diagram in `RESEARCH.md` ("The model": a new file type or relationship), and any record in `adr/`
  that the change touches or reverses.
- **Pick the first option that fully works, in this order:** skip it (say so in one line); reuse what's in
  `tools/` (`common.py`, `check_citations.py`, the existing patterns); the Python standard library; a one-liner a
  reader gets at a glance; otherwise the minimum code. Tools in `tools/` stay stdlib-only (heavier jobs run only in GitHub Actions with pinned versions, like OCR,
  transcripts, the site build, the linters and the Vale style check; `adr/20261122-1551-vale-in-ci-stdlib-in-tools.md`): no new dependencies.
  Standard-library modules are fine, `unittest` included.
- **No unrequested extras:** no abstractions, wrappers, options, config or "for later" code. Deleting beats adding.
  Prefer extending an existing script over a new one.
- **Comments** say only the why the code can't show, in one line.
- **Bugs:** grep all callers first, then fix the cause in shared code.
- **Keep** validation and error handling when moving or merging code.
- **Tests:** every `tools/<tool>.py` has a `tools/tests/test_<tool>.py` (`unittest`, plain `assert`s in test
  methods, shared setup in `tools/tests/helpers.py`); `test_every_tool_has_a_test.py` fails otherwise. Run them with
  `make test` (CI runs `make check`). A change with branches, loops, parsing or money figures
  gets a test case; trivial changes don't. A bug fix gets a test that fails without the fix. Expected values are
  worked out by hand from a small fake fixture, never copied from the code's output (a copied value only confirms
  what the code does now). Tools that shell out to programs available only in GitHub Actions (`ocr_pdfs.py`,
  `save_youtube.py`) test their pure helpers; the main flow stays untested. Derive scripts (`tools/derive_*.py`)
  are tested against inline fixtures with hand-worked values, plus invariants (a bound, a total) for rows too
  costly to work out by hand; each new row gets a value or an invariant. CI's rerun of the scripts on the real data
  stays the regression check. Site code (`site-11ty/`) gets no tests: CI's site build (`cd site-11ty && npm ci &&
  npx eleventy`) covers it, failing on a broken internal link, an unknown `[[id]]` or an indexable page with no meta
  description or with a title or description another page uses. Why: `adr/20261126-1944-tests-per-tool-with-unittest.md`.
- **Linters (CI, blocking):** Ruff checks and formats `tools/` (`ruff.toml`), Biome lints and formats `site-11ty/`
  JS (`site-11ty/biome.json`), actionlint checks the workflows, and html-validate checks the built pages' markup and
  accessibility (`site-11ty/.htmlvalidate.mjs`). Fix the code, not the rule; turn a rule off only with a one-line
  why in its config. Why: `adr/20261124-2226-linters-in-ci.md`.
- **Known limits** go in a comment: `shortcut: <the limit>, <when to upgrade>`.
- **Never cut:** the rules in CLAUDE.md and `.claude/rules/` about `sources/` (keep originals, provenance), citation and quote checks,
  secrets and access handling, accessibility of the site, or anything the maintainer asked for.
- **PR description ends with** one or two lines: what was skipped or left unchecked, and any risk to know about.

## Key files
- `.gitattributes` — our CSVs (`analysis/**/*.csv`, `sources/_*.csv`) are stored with LF endings; archived files
  aren't touched (`adr/20261123-2131-csv-line-endings-via-gitattributes.md`)
- `adr/YYYYMMDD-HHMM-<slug>.md` — architecture decision records, named by the UTC time they're created: context,
  decision, options weighed, when to revisit
- Tools: `tools/search.py`, `tools/doc.py`, `tools/linkify.py`, `tools/check_citations.py` (`--measures` for the
  review measures), `tools/check_sources.py`, `tools/fetch_sources.py`, `tools/ocr_pdfs.py`, `tools/save_youtube.py`, `tools/next_issue.py`, `tools/derive_<topic>.py`,
  `tools/tests/` (one `test_<tool>.py` per tool, `helpers.py`)
- `Makefile` — the common commands (`make` lists them); CI's check job runs `make citations sources test derive-check`.
  Why: `adr/20261126-2010-makefile-for-common-commands.md`
- Site: `site-11ty/` builds oregonedtrail.org with Eleventy (`make serve`);
  every page but About (`website/about.md`) is generated from `analysis/` and `sources/` in `src/_data/archive.js`,
  guides included (`/guides/`, `adr/20261128-0005-guides-built-from-topic-summaries.md`).
  Why Eleventy: `adr/20261124-0837-site-built-with-eleventy.md`
