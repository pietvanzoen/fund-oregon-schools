# Python tools stay stdlib-only; heavier checks run in GitHub Actions

Status: accepted (2026-11-22, PR #109)

## Context
CLAUDE.md said "tools stay stdlib-only", but the workflows already install poppler, tesseract, faster-whisper
and MkDocs. The house style (`STYLE.md`, ADR 0008) has mechanical rules that a prose linter handles better than
regexes in `check_citations.py`.

## Decision
Scripts in `tools/` (what sessions, subagents and volunteers run locally) stay stdlib-only. Jobs that need more run
only in GitHub Actions, with a pinned version, and commit their output or report on the PR, so no session needs the
dependency. The style rules run as Vale (`.vale.ini`, `.github/styles/FOS/`, `.github/workflows/style.yml`): on PRs
only, on added lines only, as warnings and suggestions that never block a merge.

## Options weighed
- **Style checks in `check_citations.py`**: every session gets them instantly, but it means a second hand-rolled
  rule system with weaker sentence handling.
- **Vale everywhere**: a session would need to install a binary, which the cloud sandboxes can't always download.
- **Vale in Actions only** (chosen): a mature linter with readable YAML rules, no local install; sessions see its
  findings on the PR.
- **Lift the stdlib rule for `tools/`**: better libraries, but install steps, version drift and code agents can't
  read whole. Not adopted.

## Revisit when
Sessions routinely miss Vale findings because they only appear after the PR opens, or the checks start blocking
work and need to run locally.
