# Site design: direction C, "Kitchen table"

Piet picked direction C (Nov 23, 2026) from three drawn options. The mockups in `direction-c/` are exports from the
design canvas: open them in a browser to see them (they render without the canvas runtime). `screenshots/` has the
mockups and the spike as it is now. This file is the spec; the mockups win where they show something this file doesn't.

Work happens on `site-11ty/` (#155). Light only, no dark mode for now.

## Tokens

| Token | Value | Use |
|---|---|---|
| Blue | `#005eb8` | masthead, In short header, primary buttons, links |
| Deep blue | `#003087` | link hover, figures in number tiles, kind labels on cards |
| Ink | `#212b32` | body text |
| Muted | `#4c6272` | secondary text ("Our interpretation, not a source", dates) |
| Ground | `#f0f4f5` | page background, number tiles, secondary buttons |
| White | `#ffffff` | cards |
| Analysis | `#fff4cc` | "What we think this means" card and inline "We think" highlight |
| Accent | `#ffb81c` | the logo mark's dot only (decorative; never carries text) |
| Focus | `#ffeb3b` with `#212b32` border | keyboard focus and the pill being previewed |

Pills by kind (background / border / text). Kinds differ by icon and word first; colour is a second cue:
- Document: `#e8f1fa` / `#b9d3ee` / `#003087`, page icon
- News: `#f3ecfa` / `#d6c3ea` / `#4a2a7a`, newspaper icon
- Our sum or estimate: `#fff4cc` / `#e8d48a` / `#4d3d00`, calculator icon
- Recording: same as document, video icon

Type: Lexend (Google Fonts), weights 400/500/600/700. Sizes: title 40 desktop / 30 phone, section heading 25,
body 19 desktop / 17 phone, small 15, pills and labels 14. Line height 1.6 body, 1.15 titles.

Masthead: the mark, the site name and under it the tagline **Following the money behind Oregon's schools** in light
blue `#e8f1fa` on the masthead blue, 15px desktop / 13px phone, on every page.

Shape: cards radius 12, number tiles 10, pills full round, bottom sheet 16 with a drag handle. Card shadow
`0 10px 30px rgba(33,43,50,.2)`. Touch targets at least 44px (48 for sheet buttons).

Icons: inline stroke SVG (24 grid, stroke 2, `currentColor`), never emoji. The mark: a white rounded square with a
dotted trail in blue ending in a gold dot (see the mockups' masthead).

## Page structure

Topic page, top to bottom: breadcrumbs; title; **In short** card (blue header bar, white body, 21px text) from the
topic file's front matter `summary`; **What we think this means** card (the `## Analysis` section, yellow, with
"Our interpretation, not a source"); **What the documents say** card; **Numbers we worked out** (`## Derived figures`)
as tiles when there are at most 4 rows with short values, otherwise a plain table in the card. Side column: "On this
page" and "Related pages" (backlinks) cards; on phones, "On this page" goes above the article and "Related pages"
below it. A topic without a `summary` shows no In short card.

Person page: back link, name, a white summary card built from `people.csv` (office and district, party, area, the
2027 role with a "2027" tag), then the profile. People get no prose summary: their card stays factual. Without a
profile: "We haven't written about this person yet. Here's their role and the pages that mention them."

Preview card: kind label with icon, title, one or two lines, actions. Desktop: a floating card on hover or focus.
Phone: a bottom sheet on first tap, with a full-width "Open document" / "Open page" button, "Close", and "Archived
copy" as a text link below when there is one. Topic cards show the topic's `summary`; every other kind is built from
its data row.

Inline analysis in a list of facts: a yellow highlight starting with **We think:**.

Menu and footer (`chrome/`): on phones the three nav links go behind a **Menu** button in the masthead (white tab
with an up chevron when open, `aria-expanded`, `aria-controls`), opening a white list under the masthead: Topics,
Who decides, What's being decided, a divider, then **About this site**. Desktop keeps the three links inline, with no
About link. Without JavaScript the list stays open. The footer has a row of links (About this site, What's new,
Contact: hello@oregonedtrail.org with the address shown as text, Research archive on GitHub), the one-line explainer
with pills, and "Run by Oregon public school parents. Analysis licensed CC BY 4.0."

Home page (`home/`), built from `analysis/START.md`: a white top band (title, description, "Run by Oregon public school
parents. About this site", a large search box); a **Coming up** banner for the next dated row of `timeline.md`;
**Start here** as four cards from START.md's entry points, with line icons; **Key numbers for 2027-29** as tiles
("$12.56 billion", unit smaller) with a source pill each, the "Analysis:" line as the yellow box, the funding chart and
the other bullets as a list; **What's new** (latest three from `updates.csv`) beside **Read first** (first four, the
rest behind "All eight"); **Look things up** cards for the Reference list. Text the layout needs goes in START.md,
cited, never in the template.

Every sentence must still read without the cards, pills and colours (STYLE.md). AA contrast for all text.
