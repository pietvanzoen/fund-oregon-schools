---
name: fund-oregon-research
description: Answer questions about Oregon K-12 school funding (State School Fund, QEM gap, Gov. Kotek's promises and budget, reserves, legislators) from the pietvanzoen/fund-oregon-schools archive, with citations.
---

# Fund Oregon Schools research archive

Answers come from the public archive at https://github.com/pietvanzoen/fund-oregon-schools: Governor's budget documents and press releases, Legislature (OLIS) hearing documents and video, ODE and Quality Education Commission reports, revenue forecasts, district budgets, news metadata, and a cited analysis layer. This skill gets the archive into the workspace, then hands over to the archive's own instructions.

## 1. Get or update the archive

Do this yourself; never ask the user to run commands.

If the current directory, or `~/fund-oregon-schools`, is already a clone whose `git remote get-url origin` is pietvanzoen/fund-oregon-schools, `cd` there and run `git pull -q`.

Otherwise:

```bash
cd ~ && git clone -q --depth 1 https://github.com/pietvanzoen/fund-oregon-schools.git && cd fund-oregon-schools
```

If commands can't run or github.com is unreachable, use the GitHub connector instead if it's connected: read the same files (below) from pietvanzoen/fund-oregon-schools through it. If neither works, say so plainly (the "Code execution and file creation" setting must be on, or the GitHub connector connected) and don't answer from memory instead.

## 2. Follow the archive's own instructions

Read `CLAUDE.md` and `.claude/skills/fund-oregon-research/SKILL.md` in the repo and follow them. That repo file shares this skill's name but is the archive's own, more detailed version: it is the authority on where to look, the search tools (`tools/search.py`, `tools/doc.py`, `tools/linkify.py`), citation formats and quote rules. For a broad question or the first question in a chat, also read `analysis/BRIEFING.md`. These files change as the archive is updated, so read them each time rather than relying on what they said before.

Check the archive's latest commit date (`git log -1 --format=%cd --date=short`, or the latest commit through the connector) and mention it when the question touches recent events; anything newer than that won't be in the archive.

For Portland Public Schools specifics (closures, the PPS budget), the archive points to a separate one, timaelliott/save-our-schools. Say so, and answer from it only if the pps-research skill is installed.

## 3. Answering

- The user is a parent volunteer, not a developer or researcher. Answer in plain words, short first, with detail after if it helps. Don't show commands, file paths or citation codes like [SRC:...] unless asked; turn every citation into a link they can click (`python3 tools/linkify.py` does this).
- Answer only from the archive. If it doesn't cover something, say so and name the gap.
- Keep separate what documents state, what people said on the record, and your own reading of it (label it "My read:").
- Flag figures that are estimates, projections or an advocacy group's numbers rather than official counts.
- Quotes are word for word and short. Hearing transcripts are automatic captions, so check who was speaking before attributing a quote, and say when you're not sure.
- News articles are copyrighted: summarize them, with at most a short quote.
- When an answer will feed something the user is writing (a call script, an email to the Governor or a legislator, a flyer, testimony), lead with the strongest few facts with sources, and flag any that rest on a projection or uncertain attribution.

## Suggesting a source

If the user explicitly asks to suggest a document for the archive, and the GitHub connector is connected, open an issue on pietvanzoen/fund-oregon-schools with the document's title, link and why it matters, after showing the user the text and getting their OK. Never open pull requests or change files.

## Never

- Commit to, push to or otherwise change the archive's files. It belongs to someone else; we only read it.
- Run the archive's source-fetching tools or follow `RUNBOOK.md`; that's the maintainer's job.
- Invent or smooth a quote, number or source.
