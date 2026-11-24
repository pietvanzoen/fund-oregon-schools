# The site is built with Eleventy, not MkDocs and Material

Status: accepted (2026-11-24, PR #154)

## Context
The live site is MkDocs with Material, shaped by `tools/site_hook.py` (citation chips, Analysis boxes, generated
tables, the home page) and `overrides/`. Material's own build notice says MkDocs 2.0 removes the plugin system, breaks
all theme overrides, has no migration path, has a closed contribution model and is unlicensed. That would strand the
hook and the overrides. The redesign (#155, direction C) and the wiki features the archive wants (first-mention links,
one preview card for every linked thing, backlinks, generated person pages, `[[id]]` links that fail the build) need
full control of the markup. The Eleventy spike (`site-11ty/`, #154, #160, #162) builds them from the same `analysis/`
and `sources/` files.

## Decision
Build the site with Eleventy (pinned) from `site-11ty/`, reading the archive's files directly, with Pagefind (pinned)
for search. MkDocs, Material, `site_hook.py` and `overrides/` are retired once the remaining pages move over; until
then the live site stays on MkDocs.

## Options weighed
- **Stay on MkDocs 1.x and Material, frozen**: no migration work now, but no fixes or upgrades, and the redesign
  and wiki features would have to be forced through hook regexes and theme overrides.
- **Zensical** (Material's successor): closest to today's setup, but early and built around Material's look and
  extension points; still a theme to work around, not markup the site owns.
- **Quartz**: has backlinks and wiki links built in, but expects an Obsidian-style vault. The archive's own
  conventions (`[SRC:…]` citations, CSV-driven pages, front-matter summaries) would need plugins in its framework.
- **Eleventy** (chosen): plain JavaScript templates over the archive's files, so every convention is a few lines in
  `site-11ty/src/_data/archive.js`. It's pinned and stable, needs no theme, and its broken-link check runs in the
  same build. Costs: the remaining pages to port, a new Pages workflow, and the docs that say `mkdocs build --strict`.

## Revisit when
Eleventy stops being maintained, or the site needs something a static build can't do (server-side search over the
archived documents, accounts, comments).
