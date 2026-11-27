# Long Analysis sections get specific subheadings, short paragraphs and lists only for parallel items

Status: proposed (2026-11-27, PR #PRNUM)

## Context
No rule covered paragraph length, subheadings or bullets inside a topic's `## Analysis`. Seven of eight topic
files used prose only there; `virtual-charters.md` already used bullets and a `### Still to find` subheading. The
reserves page's Analysis was three paragraphs of about 245, 215 and 70 words, the first running from the vote rule
through a proposal to three officials' objections. The guidance this draws on:
- Nielsen Norman Group, [How users read on the web](https://www.nngroup.com/alertbox/9710a.html): users scan; the
  same text laid out for scanning measured 47% better usability; subheadings should be meaningful, not clever.
- GOV.UK, [Create a clear structure for your content](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/),
  and Essex County Council's GOV.UK-based [bullets and numbered lists pattern](https://essex.gov.uk/essex-county-councils-design-and-patterns-library/patterns/bullets-and-numbered-lists):
  bullets for related items, after a lead-in sentence.
- Government Commercial Agency, [style guide: formatting](https://www.gca.gov.uk/government-commercial-agency-style-guide/formatting):
  at least two bullets; many lists close together read as badly as a wall of text.
- Defra digital, [content clinic, Nov. 10, 2016](https://defradigital.blog.gov.uk/2016/11/15/content-clinic-10-november-what-we-talked-about/):
  if two heading levels aren't enough, simplify the content.

## Decision
`STYLE.md` ("Analysis sections a reader can scan"): an Analysis section over about 250 words gets `###`
subheadings, one per question it answers, each saying what that part covers or finds. Paragraphs stay under about
120 words. Bullets are only for parallel items, at least two, after a lead-in sentence, each with its own
citations; arguments and if/then chains stay in prose. No new `##` levels, so rule 4's three sections and
`tools/check_citations.py` are unchanged. The reserves page is the first example; other pages follow one PR at a
time.

## Options weighed
- **No rule**: no work, but long Analysis sections stay walls of text, and each session formats its own way.
- **Paragraph limits only**: easy to state and check, but short paragraphs with no headings still give a scanning
  reader nothing to find a part by.
- **Subheadings, paragraph limits and a list rule** (chosen): follows the guidance above, keeps the three-section
  layout, and leaves arguments in prose so if/then reasoning isn't broken into fragments.
- **Restructure every topic page now**: consistent at once, but one large diff that changes no claim is hard for the
  fact-checker to confirm; restructuring a page when it is next worked on, or in its own small PR, keeps each check
  tractable.

## Revisit when
The clarity reviewer often flags restructured sections as harder to follow, or readers report they can't find a
part of a page; or a check of section length becomes worth automating in `tools/check_citations.py`.
