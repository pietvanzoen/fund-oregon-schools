# Calculated values live in their own files, one plain derive script per topic

Status: accepted (2026-11-21, issue #34, PR #36 for the code rules)

## Context
Issue #34 made the split between source facts, our calculations and our analysis structural. The first plan
wrote calculated columns (`derived_`, `est_`) into the same `analysis/data/*.csv` files as values copied from
sources, filled by a shared derive library and runner. It also had a separate section-check script and a parser
for unit rescaling ($1.27B vs 1,271M). Applying the ponytail code rules (see `CLAUDE.md`, "Writing code")
trimmed it.

## Decision
- Every calculated value, per-row values included, goes in `analysis/derived/<topic>.csv`, written only by
  `tools/derive_<topic>.py`. `analysis/data/` holds only copied values.
- One plain script per topic: no shared library, no runner.
- Reproducibility needs no code: CI reruns every derive script and fails if `analysis/derived/` changes.
- The section, DER-tag and "our sum" checks live in `check_citations.py`, not a new script.
- The number-in-source check is an exact match (commas and `$` stripped) and only warns, with a `shortcut:`
  comment instead of a unit-rescaling parser.

## Options weighed
- **Calculated columns inside the data CSVs**: inputs and results side by side, but a script would edit half a
  file, which needs a check that it never touches copied columns. That was the riskiest part of the plan.
- **Separate derived files** (chosen): removes that risk and that check. Costs: inputs and results no longer
  sit side by side in one CSV.
- **A derive library and runner**: less repetition across scripts, but more code than the job needs; CI's
  rerun-and-diff already proves the outputs reproduce.
- **A unit-rescaling parser**: fewer false warnings, but a parser to maintain; reviewers catch the rest.

## Revisit when
The scripts start repeating real logic (not just reading a CSV and summing), or the number check's false alarms
are frequent enough that the warning gets ignored (then add rescaling).
