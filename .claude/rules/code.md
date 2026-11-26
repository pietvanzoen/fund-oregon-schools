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
  transcripts, the site build, the linters and the Vale style check; `adr/20261122-1551-vale-in-ci-stdlib-in-tools.md`): no new dependencies, and no
  framework for tests.
- **No unrequested extras:** no abstractions, wrappers, options, config or "for later" code. Deleting beats adding.
  Prefer extending an existing script over a new one.
- **Comments** say only the why the code can't show, in one line.
- **Bugs:** grep all callers first, then fix the cause in shared code.
- **Keep** validation and error handling when moving or merging code.
- **Tests:** anything with branches, loops, parsing, money figures or a new script gets an assert-based case in
  `tools/test_tools.py` (plain `assert`, run by CI). Trivial changes don't. Site code (`site-11ty/`) gets no tests: CI's
  site build (`cd site-11ty && npm ci && npx eleventy`) covers it, failing on a broken internal link, an unknown `[[id]]` or an indexable page with no meta description or with a title or description another page uses. Derive scripts
  (`tools/derive_*.py`) get no tests either: they're plain arithmetic on archived data, CI reruns them and fails on
  any change in output, and the fact-checker checks each method; a test would only pin today's numbers.
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
  `tools/test_tools.py`
- Site: `site-11ty/` builds oregonedtrail.org with Eleventy (`cd site-11ty && npm ci && npx eleventy --serve`);
  every page but About (`website/about.md`) is generated from `analysis/` and `sources/` in `src/_data/archive.js`.
  Why Eleventy: `adr/20261124-0837-site-built-with-eleventy.md`
