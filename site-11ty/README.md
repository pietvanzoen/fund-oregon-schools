# The website (oregonedtrail.org)

Eleventy builds every page from the archive's own files: `analysis/` and `sources/`, plus the hand-written About page
in `website/about.md`. Nothing here repeats the research. Why Eleventy: `adr/20261124-0837-site-built-with-eleventy.md`.

    cd site-11ty && npm ci && npx eleventy --serve      # http://localhost:8080
    PREVIEW=1 npx eleventy                              # relative links, for hosting from any folder

- `src/_data/archive.js` turns the files into pages: citation pills, "Our analysis" boxes (the files' "Analysis:"
  marker), backticked file references as links, first-mention links to people and `<abbr>` on acronyms, backlinks,
  generated person pages (a stub for everyone in `people.csv` without a profile), the decision tables from the
  decision CSVs, and the list pages (numbers, quotes, promises, timeline, sources, What's new, questions, glossary).
- `src/_includes/layout.js` is the frame of every page: masthead, search panel, footer, preview card, page metadata
  and Umami analytics. `src/*.11ty.js` are the templates; `src/assets/` the CSS and scripts.
- The build fails on a broken internal link or an unknown `[[id]]` (`eleventy.config.js`), then Pagefind indexes
  topic, person and glossary pages for search.
- `.github/workflows/pages.yml` runs the build on every PR and deploys `_site/` to GitHub Pages from `main`.
- The design spec is `design/README.md` (direction C, #155); its mockups and screenshots are in `design/`.
- Pinned: `@11ty/eleventy`, `@11ty/gray-matter`, `csv-parse`, `markdown-it` and `pagefind` (`package.json`).
