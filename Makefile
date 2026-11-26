# Common commands. CI's check job runs these same targets (.github/workflows/check.yml), so `make check` passing
# locally means the check job will too. Why a Makefile: adr/20261126-2010-makefile-for-common-commands.md.
PYTHON ?= python3
.DEFAULT_GOAL := help
.PHONY: help check citations sources test derive derive-check lint site serve

help: ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-13s %s\n", $$1, $$2}'

check: citations sources test derive-check ## Everything CI's check job runs (except the What's new row)

citations: ## Citations, data files, topic layout and derived-figure tags
	$(PYTHON) tools/check_citations.py

sources: ## The queue and the archived files
	$(PYTHON) tools/check_sources.py

test: ## The tool tests in tools/tests/
	$(PYTHON) -m unittest discover -s tools/tests

derive: ## Rerun every derive script; commit what changes in analysis/derived/
	@for f in tools/derive_*.py; do echo "$(PYTHON) $$f"; $(PYTHON) "$$f" || exit 1; done

derive-check: derive ## Fail if analysis/derived/ differs from what the scripts write
	@git add --intent-to-add analysis/derived/ 2>/dev/null || true  # a new, uncommitted output shows in the diff too
	@git diff --exit-code --stat -- analysis/derived/ || { echo "analysis/derived/ is out of date: commit it"; exit 1; }

lint: ## Ruff on tools/ (CI pins its version in lint.yml; needs ruff installed)
	@command -v ruff >/dev/null || { echo "ruff isn't installed; CI runs it (lint.yml)"; exit 1; }
	ruff check
	ruff format --check

site: ## Build the site into site-11ty/_site
	cd site-11ty && npm ci && npx eleventy

serve: ## Build and serve the site at http://localhost:8080
	cd site-11ty && npm ci && npx eleventy --serve
