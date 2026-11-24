# Eleventy spike (not the live site)

A test of building the site with Eleventy instead of MkDocs + Material, to try wiki-style features. It builds three
page types from the same files as the live site: topic pages, person pages (including generated stub pages for
everyone in `people.csv` without a profile) and Who decides. Everything else links to fundoregonschools.org.

What it tries:
- Citation chips, Analysis boxes and backticked file references, ported from `tools/site_hook.py`.
- Links on the first mention of each person in `people.csv`, and `<abbr>` on the first use of each glossary acronym.
- One preview card for every linked thing (people, topics, documents, news, our calculations, abbreviations):
  hover or focus with a mouse or keyboard; on touch, the first tap opens it as a bottom sheet.
- Backlinks ("Mentioned on"), a generated infobox and generated position/option tables on person pages.
- `[[lieber]]` / `[[topic:reserves]]` links that fail the build when the ID doesn't exist.
- A broken-internal-link check after every build (stands in for `mkdocs build --strict`).

    cd site-11ty && npm ci && npx eleventy --serve      # http://localhost:8080
    PREVIEW=1 npx eleventy                              # relative links, for hosting from any folder

shortcut: no search, no glossary/decisions/numbers pages, no CI workflow; add those only if the spike is adopted.
