---
name: fos-research
description: Answer questions about Oregon K-12 school funding for the 2027-29 budget (State School Fund, Quality Education Model gap, Gov. Kotek's promises and budget, revenue forecasts, Education Stability Fund, legislators' positions) from this repository's archived sources, citing every claim. Use whenever working in the fund-oregon-schools repo or asked about Oregon state school funding or Kotek's education record.
---

# Oregon school funding archive: answering questions

Answer from what is in this repository. If the archive doesn't cover something, say so, name the gap, and
suggest the source to add (a row in `sources/_queue.csv`). Don't fill gaps from memory.

## 0. Get the archive
If you're not already in a clone of pietvanzoen/fund-oregon-schools (`git remote get-url origin`), use
`~/fund-oregon-schools`: `git -C ~/fund-oregon-schools pull -q` if it exists, otherwise
`git clone -q --depth 1 https://github.com/pietvanzoen/fund-oregon-schools.git ~/fund-oregon-schools`. Work from
there. If github.com can't be reached, read the same files through the GitHub connector.

## 1. Orient
- Read `CLAUDE.md` (citation formats, quote rules).
- Broad question or first question of a session: read `analysis/BRIEFING.md` and `analysis/README.md`.
- Check freshness: `git log -1 --format=%cd --date=short`, and `sources/_queue.csv` rows with no matching
  file yet (`python3 tools/check_citations.py --pending`). Mention when an answer rests on unfetched sources.

## 2. Find things
```bash
python3 tools/search.py "State School Fund" -n 20              # full-text over sources + analysis
python3 tools/search.py "current service level" --kind src      # kinds: src, news, analysis, quote
python3 tools/search.py "Kotek" --kind quote
python3 tools/search.py "school funding" --kind src             # also hearing transcripts: [VID:...@H:MM:SS] hits
python3 tools/doc.py qec/2026_qem_report 12                     # page 12 of a sources/ PDF by path fragment
python3 tools/doc.py qec/2026_qem_report --grep "current service level"
python3 tools/linkify.py analysis/BRIEFING.md                   # print with citation tags turned into links
```

## 3. Answer recipes
| Question | Where to go |
|---|---|
| What has Kotek promised / said about schools? | `analysis/people/kotek.md`, `analysis/promises.csv`, `--kind quote --person Kotek` |
| How much does the state spend / need? | `analysis/data/ssf_history.csv`, `qem_gap.csv` → the cited page (cite the document, not the CSV) |
| What's in the Governor's budget? | `sources/gov/` recommended budget documents; compare with `ssf_history.csv` |
| Can reserves be used? | `analysis/data/reserves.csv`, `analysis/topics/reserves.md` |
| A figure tagged `[DER:<topic>/<id>]` | the row in `analysis/derived/<topic>.csv` (method, inputs, assumptions); made by `tools/derive_<topic>.py` |
| Where does a legislator stand? | `analysis/people/<slug>.md`; hearing video under `sources/legislature/video/` |
| PPS specifics (closures, PPS budget) | the PPS archive (`anthropic-skills:pps-research` / timaelliott/save-our-schools); cite as `[PPSARCH:...]` |
| What's coming up? | `analysis/timeline.md` |

## 4. Answering
- Lead with the strongest few cited facts when the answer feeds something we're writing (call scripts, emails,
  flyers, testimony). Flag figures that are estimates, projections or an advocacy group's numbers.
- Keep what documents state, what people said, and your own inference ("Analysis:") separate. Topic files do this
  in sections: "What the sources say", "Derived figures", "Analysis".
- A `[DER:...]` figure is this archive's own calculation, never an official number. Say so ("by the archive's own
  sum", "the archive estimates"), keep the DER tag or link to its row, and give an `est` figure's assumptions.
  Don't attribute it to the agency whose data went into it.
- Give citations as links (`tools/linkify.py`), keeping the tag when the text will be reused elsewhere.
- Quotes verbatim and short; never smooth a quote. Hearing transcripts (`<file>.mp4.txt`) are machine-made:
  verify a quote by listening at its timestamp, or don't quote it.

## Never
- Invent or smooth a quote, number or source.
- Put full news article text into the repo.
- Overwrite a file in `sources/`.
