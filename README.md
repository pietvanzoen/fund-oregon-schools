# Oregon K-12 Funding Research

A research archive on how Oregon funds K-12 public schools, focused on the **2027-29 budget** (Gov. Tina Kotek's
Recommended Budget and the 2027 Legislature): primary sources, and analysis that cites them claim by claim.

**Browse it:** <https://fundoregonschools.org>, a readable website built from this repo.

**Start here:** [`analysis/BRIEFING.md`](analysis/BRIEFING.md): what's being decided, how we got here, the numbers, who
stands where, contested claims and known gaps.

**Ask questions with Claude:** paste this into a new Claude chat and it will set you up (see [`SETUP.md`](SETUP.md)):

> Please set me up using https://raw.githubusercontent.com/pietvanzoen/fund-oregon-schools/main/SETUP.md

**Who runs it:** a volunteer group of Oregon public school parents. Contact: fundoregonschools@gmail.com

Modeled on the PPS rightsizing archive ([timaelliott/save-our-schools](https://github.com/timaelliott/save-our-schools)):
primary sources kept untouched in `sources/`, and everything in `analysis/` cites back to them. Portland-specific
material stays in that archive and is cited from here as `[PPSARCH:...]`.

## Layout
| Path | What |
|---|---|
| `sources/` | Primary documents (Governor, Legislature/OLIS, ODE and the Quality Education Commission, fiscal offices, districts, advocacy groups) with provenance in `_manifest.jsonl`; each PDF/HTML has a `.txt` text copy. `news/index.jsonl` holds news metadata and summaries, never full text. |
| `sources/_queue.csv` | Documents to archive. Add a row; the `fetch-sources` Action downloads it. |
| `analysis/` | Briefing, people and quotes, promises tracker, data tables, timeline, topics, open questions. Every claim cited. |
| `tools/` | Stdlib Python: `search.py`, `doc.py`, `linkify.py`, `check_citations.py`, `fetch_sources.py`, `test_tools.py`. |
| `CLAUDE.md`, `.claude/skills/fund-oregon-research/` | Rules and the answering skill for Claude. |
| `SETUP.md`, `setup/fund-oregon-research/` | Setup instructions for volunteers' Claude, and the skill they install on their own account. |
| `RUNBOOK.md` | Adding and refreshing sources. |
| `mkdocs.yml`, `website/`, `tools/site_hook.py`, `overrides/` | The public website. Pages are generated from `analysis/` and `sources/` on every push to `main`; only the About page and `robots.txt` live in `website/`. Page titles and meta descriptions are set in `PAGE_META` in `tools/site_hook.py`; `overrides/main.html` adds link-preview (Open Graph) tags. Preview: `pip install "mkdocs>=1.6,<2" "mkdocs-material>=9.7,<10" && mkdocs serve`. |

## Quick use
```bash
python3 tools/search.py "State School Fund"
python3 tools/doc.py 2026_qem_report --grep "current service level"
python3 tools/linkify.py analysis/BRIEFING.md
python3 tools/check_citations.py
```
