// One output page per entry in archive.pages (everything but the home, search and 404 pages)
import { layout } from "./_includes/layout.js";

export const data = {
  pagination: { data: "archive.pages", size: 1, alias: "entry" },
  permalink: (d) => d.entry.url,
  eleventyComputed: { title: (d) => d.entry.title },
};

export function render({ entry: e }) {
  return layout({ ...e, body: e.html, crumbs: e.back ? [] : e.crumbs });
}
