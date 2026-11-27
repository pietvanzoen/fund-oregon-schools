# House style

How the archive's reader-facing text sounds and looks: `analysis/START.md`, `analysis/decisions.md`,
`analysis/topics/`, `analysis/people/` pages and `analysis/timeline.md`. It applies to our own sentences; quotes stay
verbatim. The rules on citations, sections and quotes are in `.claude/rules/analysis.md`; this file covers wording. Where AP style
covers something this file doesn't, follow AP. Why these choices: `adr/20261122-1607-house-style.md`.

The mechanical rules are checked by Vale on pull requests (`.github/styles/FOS/`, added lines only, never
blocking); the clarity reviewer checks the rest.

Contents: [Voice](#voice) · [Structure](#structure) · [Weight and certainty](#weight-and-certainty) · [Names](#names) · [Abbreviations and terms](#abbreviations-and-terms) · [Numbers and dates (AP)](#numbers-and-dates-ap)

## Voice

- **Explainer.** Neutral, and say why a fact matters: what the number is compared with, what it decides, what
  changes if it moves. Not a press release and not a campaign.
  - Yes: "Budget writers start from the current service level: $12.56 billion for 2027-29, last budget's spending
    adjusted for inflation and enrollment. Proposals are measured against it."
- **A general reader.** Write for an intelligent reader who doesn't know the field: a reporter, a legislative
  aide, a school board member, a parent. Don't address any one group ("parents should…").
- **"You"** only in reading guides and how-to text ("If you compare these, compare them with each other"). Facts
  are in the third person.
- **Self-reference.** "Our analysis", "our estimate", "our sum" for our own work. "The archive" for what has been
  collected ("The archive has no statement from Kotek on the formula"). Never a bare "we".
- **The About page** (`website/about.md`, hand-written, outside the files above) speaks as the group that runs the
  site: "we" and "us" are fine there. Its other wording follows this file.

## Structure

- **Answer first.** The first sentence of a page or section says where things stand. Background follows.
  - Yes: "Kotek has not said how much her budget will give schools; it's due Dec. 1."
  - No: "In 2024, during her campaign, Kotek said… [three sentences later] She hasn't given a figure."
- **One idea per sentence** where you can. Active voice: say who did it.
- **Analysis sections a reader can scan.** Readers scan a page before they read it. A topic's `## Analysis` longer
  than about 250 words gets `###` subheadings, one per question it answers. A subheading says what that part covers
  or finds ("What a draw needs", "Positions on record"), not a label ("Background", "Other issues"). Use `###`
  only: never add a `##` (`.claude/rules/analysis.md` rule 4), and if two levels aren't enough, simplify the text.
  Each subsection opens with its answer, as above.
  - **Paragraphs** stay under about 120 words, one idea each.
  - **Bullets** only for parallel items (positions, conditions, options, open questions): at least two, after a
    lead-in sentence, and each bullet keeps its own citations. An argument or an if/then chain stays in prose. Don't
    put several lists close together.
  - Yes: "### Positions on record", a lead-in that says where the positions stand ("In May 2026 the two Ways and
    Means co-chairs saw no reason for a 2025-27 draw; in November 2026 Kotek said…"), then one cited bullet per
    person, each with its date, and the inference after the list in prose.
  - No: one 250-word paragraph that runs from the vote rule through a proposal to officials' objections.
  - Why: `adr/20261127-0051-analysis-subheadings-and-lists.md`.
- **In short.** Each topic file has a `summary` in its front matter, shown as "In short". Two or three sentences in
  everyday words, for a parent with no budget background: name the thing, say what the archive found, and what it
  can't yet say. Use a number only if it needs no context ("almost all", "about $2 billion") and it matches the
  cited figures below. No abbreviations or jargon. No new claims: every sentence restates something cited further
  down the page.
  - Yes: "Schools and other grantees spent almost all of this money each year, mostly on staff. The state's reports
    don't yet show whether it changed results for students."
  - No: "The money didn't work." (the reports can't tell, which isn't the same)
- **Search titles and descriptions.** Topic files and person profiles have a `description` in front matter, shown
  under the page's link in search results and link previews; a topic with a long H1 also has a
  shorter `title` (the lengths: `.claude/rules/analysis.md` rule 4, enforced by `tools/check_citations.py`). The
  description is one sentence that says what the page covers and
  its main finding, with the words a reader would search for (State School Fund, not "the fund"). Same rules as
  In short: plain words, no abbreviations, no new claims. The title names the subject first; the site adds
  "· Oregon Ed Trail".
  - Yes: "Oregon shares its State School Fund among school districts by a formula in state law that counts enrollment
    and gives extra weight to some students."
  - No: "This page looks at the formula." (says nothing a search result can use)

## Weight and certainty

- **No more and no less weight than the evidence supports.** Tense and mood match the record: a bill that died
  "would have" done something; a proposal "would" do it; a law "does" it.
- **Say plainly what's known and what isn't.** No hedge words ("appears to", "seems", "may possibly").
  - Yes: "The Oregon Department of Education has not published 2027-29 estimates. The latest, from March 2026, …"
  - No: "It appears estimates may not yet be available."
- **Comparison words, not verdict words.** Our own sentences use neutral comparisons: "less than", "more than",
  "the largest in dollars, not adjusted for inflation". Verdict words ("cut", "shortfall", "record", "historic",
  "underfunded", "windfall") appear only when attributed to whoever used them, with a citation.
  - Yes: "$400 million less than the current service level. The Oregon School Boards Association calls this a cut
    [SRC:…]."
  - No: "a $400 million cut"
- **Every number has its scale and baseline.** Compared with what, for what period, from when. A percentage change
  gives the starting value. A big number gets a sense of scale (a share or per-student figure from a `[DER:…]` row,
  not arithmetic in the text).
- **An estimate carries its main assumption** in the same sentence or the next.

## Names

- **First mention in running text:** AP title and full name. For legislators, add party and district, and say
  where the district is at least once per page (most readers don't know district numbers): "Sen. Jane Doe,
  D-District 14 (Beaverton & Southwest Portland)" (or "and"). After that, "Doe" or "Sen. Doe, D-District 14" is
  enough. Add the role when it helps a reader place them: "…, who chairs the Senate Education Committee". Governors and other
  statewide officials need no district: "Gov. Tina Kotek".
- **A legislator's own page** in `analysis/people/` gives party, chamber, district number and the district's area,
  cited.
- **Where these come from:** the `party`, `district` and `area` columns of `analysis/people/people.csv`, cited to the
  member's official page on the Legislature's site. `area` is the place label on that page's district line, copied
  exactly, so it stays in sync with the Legislature: "Democrat - District 22 - N/NE Portland" gives `N/NE Portland`
  (a role after the places, like "- Whip", isn't part of it). `tools/check_citations.py` errors if the archived page
  no longer contains it. In running text, write the label as it reads: compass abbreviations (N, NE, SW, N/NE) are
  fine in a district label, and "&" may be written "and"; add nothing else. The label names the places the
  Legislature lists, not the district's full extent, so write "(Beaverton & Southwest Portland)" or "(Beaverton and
  Southwest Portland)", not "which covers …". We don't use hometowns: most member pages don't state where the
  legislator lives. If a person's columns are empty, use the title and full name, and don't guess.
- **Title at the time:** name someone by the office they held when they did what the sentence says, then say what
  changed: "sponsored by Sen. Daniel Bonham, R-District 26, who resigned from the Senate in 2025", not "former Sen.
  Bonham". Use "former" only for someone already out of office at the time ("at the request of former Sen. …").
- **Elected, not yet seated:** no title. "Tammy Carpenter, D-District 27 (Beaverton and Cedar Hills), who won the
  seat in the Nov. 3, 2026, election (unofficial results)", until the results are certified; then "Rep.-elect".
  "Won" needs a source that calls the race (an outlet or the certified results), not only an unofficial count.
  Until they have a member page, the area comes from the current seat holder's member page.
- **Old rosters:** when a district number comes only from an older roster (a departed member's page is gone), say
  which years it covers: "R-District 28 in 2021-22".
- **Agencies and groups:** full name, then a plain short form: "the Department of Administrative Services … the
  department", "the Quality Education Commission … the commission".

## Abbreviations and terms

- **Spell out; rarely abbreviate.** Use an abbreviation in text only if a general reader knows it without help
  (K-12). "The State School Fund … the fund", not "SSF". Spell out the rest on first mention per page, even
  familiar ones: "the Public Employees Retirement System (PERS)", then "PERS".
- **Technical terms** (ADMw, CSL, extended ADM) belong in tables, methods and glossary rows. In text, describe
  them: "weighted enrollment", "the current service level".
- **Define a term in the text** the first time it appears on a page; tooltips don't work on phones.

## Numbers and dates (AP)

- **Money:** $12.56 billion, $256.6 million, $36 million, $4,500. Keep the source's precision. A table may put the
  unit in its column header ("$ billion").
- **Numbers:** one through nine in words, 10 and up in figures; figures for ages, percentages and money.
- **Percent:** 4.2%. Percentage points: "3 percentage points", not "3%".
- **Dates:** Dec. 1, 2026; March 2026 (months with a day are abbreviated: Jan., Feb., Aug., Sept., Oct., Nov.,
  Dec.; March through July are never abbreviated). Days of the week aren't abbreviated.
- **Reports and forecasts:** one name per document, the one it uses for itself (its headings and table titles), and
  the release date once per page, on first mention: "the December 2026 revenue forecast, released Nov. 18, 2026"
  (its executive summary and most of its tables are headed December 2026; its cover gives the release date, not a
  month name). After that, "the December 2026
  forecast". Never two names for the same document, on one page or across the site.
- **Budget periods:** 2027-29, "the 2027-29 budget" (two years). Avoid "biennium" in text except in quotes.
- **Bills:** "Senate Bill 1555" on first mention, then "SB 1555".
