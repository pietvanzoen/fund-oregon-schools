# Our CSVs are stored with LF endings through `.gitattributes`, not a linter

Status: accepted (2026-11-23, PR #N)

## Context
On #137 a Python read-modify-write turned `analysis/questions.csv` rows into LF, so three untouched rows showed as
edited; only the fact-checker caught it. The file was already mixed on main (rows 11-13 CRLF since #95), and
`analysis/derived/sia.csv` was all CRLF because `tools/derive_sia.py` used the `csv` module's default line ending.
So a check for mixed endings would have failed on main as it stood. Runs work in cloud clones with no hooks
installed, and `tools/` stays stdlib-only (`20261122-1551-vale-in-ci-stdlib-in-tools.md`).

## Decision
`.gitattributes` marks `analysis/**/*.csv` and `sources/_*.csv` as `text eol=lf`, and one commit made them all LF.
Git then stores LF whatever an editor or script writes, and diffs ignore line-ending changes. Archived documents
under `sources/` aren't covered: they stay byte-for-byte as fetched (CLAUDE.md rule 1, sha256 in the manifest).
The two scripts that wrote CRLF (`derive_sia.py`, the versions log in `fetch_sources.py`) now write LF, as
`derive_virtual_charters.py` already did. There's no new check, so `tools/test_tools.py` gets no new case.

## Options weighed
- **`.gitattributes` with a one-time renormalize** (chosen): nothing to install, works in every sandbox, prevents the
  problem instead of reporting it. Covers line endings only; the cleanup commit touches `questions.csv` rows 11-13
  and every row of `sia.csv`.
- **A check in `check_citations.py` or CI** (flag mixed endings, or endings that differ from `origin/main`): catches
  it only after a push and costs a fix commit each time; with `.gitattributes` in place it can't fire.
- **A formatter in a pre-commit hook** (prettier, or a small script): runs' clones don't install hooks, so it misses
  the commits that cause this; prettier adds a Node dependency.
- **A full CSV linter in CI** (csvlint, Frictionless): checks quoting and types too, but mostly repeats
  `check_citations.py`'s column checks, for a heavier dependency.

## Revisit when
A CSV problem other than line endings (quoting, encoding, a stray BOM) shows up in a diff or review, or a file under
`sources/` that we write ourselves needs covering.
