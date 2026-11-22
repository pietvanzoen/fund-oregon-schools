# House style

How the archive's reader-facing text sounds and looks: `analysis/START.md`, `analysis/decisions.md`,
`analysis/topics/`, `analysis/people/` pages and `analysis/timeline.md`. It applies to our own sentences; quotes stay
verbatim. The rules on citations, sections and quotes are in `CLAUDE.md`; this file covers wording. Where AP style
covers something this file doesn't, follow AP. Why these choices: `adr/20261122-1607-house-style.md`.

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

## Structure

- **Answer first.** The first sentence of a page or section says where things stand. Background follows.
  - Yes: "Kotek has not said how much her budget will give schools; it's due Dec. 1."
  - No: "In 2024, during her campaign, Kotek said… [three sentences later] She hasn't given a figure."
- **One idea per sentence** where you can. Active voice: say who did it.

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
- **Agencies and groups:** full name, then a plain short form: "the Department of Administrative Services … the
  department", "the Quality Education Commission … the commission".

## Abbreviations and terms

- **Spell out; rarely abbreviate.** Use an abbreviation in text only if a general reader knows it without help
  (PERS, K-12). "The State School Fund … the fund", not "SSF".
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
- **Budget periods:** 2027-29, "the 2027-29 budget" (two years). Avoid "biennium" in text except in quotes.
- **Bills:** "Senate Bill 1555" on first mention, then "SB 1555".
