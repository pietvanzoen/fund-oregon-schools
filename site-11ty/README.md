# Eleventy spike (not the live site)

A test of building the site with Eleventy instead of MkDocs + Material, to try wiki-style features. It builds the home
page, a Topics list, topic pages, person pages (including generated stub pages for everyone in `people.csv` without a
profile) and Who decides, from the same files as the live site. Everything else links to oregonedtrail.org.

What it tries:
- Citation chips, Analysis boxes and backticked file references, ported from `tools/site_hook.py`.
- Links on the first mention of each person in `people.csv`, and `<abbr>` on the first use of each glossary acronym.
- One preview card for every linked thing (people, topics, documents, news, our calculations, abbreviations):
  hover or focus with a mouse or keyboard; on touch, the first tap opens it as a bottom sheet.
- Backlinks ("Mentioned on"), a generated infobox and generated position/option tables on person pages.
- `[[lieber]]` / `[[topic:reserves]]` links that fail the build when the ID doesn't exist.
- A broken-internal-link check after every build (stands in for `mkdocs build --strict`).
- Design direction C, "Kitchen table" (`design/README.md`, #155): topic pages as cards (In short from the topic
  file's front-matter `summary`, read with the pinned `@11ty/gray-matter`), source pills with line icons, a factual
  person card from `people.csv`, and the preview card as a bottom sheet on touch.
- Search (#159): Pagefind (pinned) indexes topic, person and glossary pages after each build, with a `kind` filter;
  the results page is the site's own markup on Pagefind's JS API. Glossary pages, one per row of `glossary.csv`.
- The home page built from `analysis/START.md` (with `timeline.md`, `updates.csv` and the funding chart's data), a
  Topics page, a phone Menu button and the footer links.

    cd site-11ty && npm ci && npx eleventy --serve      # http://localhost:8080
    PREVIEW=1 npx eleventy                              # relative links, for hosting from any folder

shortcut: no search, no glossary/decisions/numbers pages, no CI workflow; add those only if the spike is adopted.
