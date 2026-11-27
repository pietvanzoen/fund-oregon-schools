# Long Analysis sections get specific subheadings, paragraphs of at most 5 sentences and lists only for parallel items

Status: accepted (2026-11-27, PR #217)

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
- GOV.UK, [Use clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/):
  paragraphs of no more than 5 sentences; try to split sentences over 25 words. GOV.UK's 2014
  [2i checklist](https://insidegovuk.blog.gov.uk/2014/05/29/what-to-check-before-you-publish-a-2i-checklist)
  asks for subheadings every 3 to 5 paragraphs (an older post, so the least settled of these numbers).
- Defra digital, [content clinic, Nov. 10, 2016](https://defradigital.blog.gov.uk/2016/11/15/content-clinic-10-november-what-we-talked-about/):
  if two heading levels aren't enough, simplify the content.

## Decision
`STYLE.md` ("Analysis sections a reader can scan"): an Analysis section over about 250 words gets `###`
subheadings, one per question it answers, each saying what that part covers or finds, about every 3 to 5
paragraphs. Paragraphs have no more than 5 sentences, as GOV.UK asks. Bullets are only for parallel items, at least two, after a lead-in sentence, each with its own
citations; arguments and if/then chains stay in prose. No new `##` levels, so rule 4's three sections and
`tools/check_citations.py` are unchanged. The reserves page is the first example; other pages follow one PR at a
time.

Checking:
- **Paragraph length** is checked by a Vale rule, `FOS.ParagraphLength` (suggestion level, comments on added
  lines only, like the other Vale rules). It's a `script` rule (`.github/styles/config/scripts/ParagraphLength.tengo`)
  rather than an `occurrence` rule. An `occurrence` regex can't do both things the count needs: almost every
  sentence here ends with a citation tag, which Vale masks, so a pattern that looks at the word before the full stop
  misses most breaks; and a pattern that doesn't counts "Gov.", "Sen." and "Nov." before a name as breaks. The
  script counts every full stop, ? or ! followed by a capital, then skips a short list of abbreviations. On
  2026-11-26 it flagged the same five Analysis paragraphs a separate count found over 5 sentences (in
  `quality-education-model.md`, `qem-practices-outcomes.md` and `student-investment-account.md`), plus one
  six-sentence note under the reserves page's "What the sources say". Plain bullet items aren't Vale paragraphs, so
  bullets aren't counted.
- **Subheadings** are written guidance only: whoever writes the section places them. No tool checks them.
- **Sentence length** stays at `FOS.SentenceLength`'s 40 words.

## Options weighed
- **No rule**: no work, but long Analysis sections stay walls of text, and each session formats its own way.
- **Paragraph limits only**: easy to state and check, but short paragraphs with no headings still give a scanning
  reader nothing to find a part by.
- **Subheadings, paragraph limits and a list rule** (chosen): follows the guidance above, keeps the three-section
  layout, and leaves arguments in prose so if/then reasoning isn't broken into fragments.
- **A 25-word sentence limit (GOV.UK)** instead of 40: rejected. This archive spells out every acronym on first use
  and names officials with title, party and district, which inflates word counts, and lowering the limit would
  mean rewording a large share of existing sentences.
- **A Vale script that checks subheading spacing**: rejected. Placing a subheading takes judgement about where a
  part's question changes, which a paragraph count can't make; written guidance is enough for whoever writes the
  section.
- **Paragraph length in words** (about 120, the first draft of this rule): replaced by GOV.UK's sentence count,
  which has a published source and doesn't penalise spelled-out names.
- **Restructure every topic page now**: consistent at once, but one large diff that changes no claim is hard for the
  fact-checker to confirm; restructuring a page when it is next worked on, or in its own small PR, keeps each check
  tractable.

## Revisit when
The clarity reviewer often flags restructured sections as harder to follow, or readers report they can't find a
part of a page; or a check of section length becomes worth automating in `tools/check_citations.py`.
