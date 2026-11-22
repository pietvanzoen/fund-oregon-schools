# 0008. Reader-facing text follows a short house style, checked by a clarity reviewer

Status: accepted (2026-11-22, PR #109)

## Context
The analysis text was all written by Claude sessions, with no stated style. A review of PR #101 found "the
department would adjust" for a bill that had died: accurate to the source, but a reader would take it as current.
Fact-checking doesn't catch that, because each claim matches its source. Piet chose the style in a question round.

## Decision
`STYLE.md` sets an explainer voice for a general reader, AP numbers, names and dates, spelled-out terms, answer
first, and comparison words instead of verdict words in our own sentences. A third fresh reviewer
(`reviewers/clarity.md`) checks changed reader-facing text against it with a paraphrase test, and any sentence
reworded for clarity gets a targeted fact-check rerun.

## Options weighed
- **Follow the AP Stylebook in full**: a known standard, but paywalled, changes yearly and doesn't cover weight or
  baselines, which is where the real errors are.
- **A short house style plus AP as tiebreaker** (chosen): the rules that change meaning are written down; AP fills
  gaps.
- **A reading-age score as a gate** (e.g. GOV.UK's reading age of 9): easy to measure, but fights the precision
  the archive needs and produces noise. Not adopted.
- **Verdict words ("cut", "record")**: allowed with a stated baseline (readable, but the word still takes a side);
  only in quotes (most neutral, but stiff); **our text uses comparison words and verdict words appear only when
  attributed** (chosen: neutral, and readers still find the claim next to the number).
- **"We" vs "this archive" vs "our analysis"**: "our analysis/estimate/sum" for our work, "the archive" for what's
  collected, never a bare "we" (chosen: matches the existing "our sum" markers without implying a group voice, and
  doesn't overstate searches of the archive).
- **Clarity checks inside the consistency-fairness reviewer**: one fewer agent, but that prompt is already long and
  clarity needs its own pass over every sentence. Not adopted.

## Revisit when
Clarity findings are mostly marked `false-alarm`, or readers report the text is still hard to follow.
