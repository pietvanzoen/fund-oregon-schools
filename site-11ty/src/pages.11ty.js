// One output page per entry in archive.pages (topics, people incl. stubs, Who decides)
import { layout } from "./_includes/layout.js";

export const data = {
  pagination: { data: "archive.pages", size: 1, alias: "entry" },
  permalink: (d) => d.entry.url,
  eleventyComputed: { title: (d) => d.entry.title },
};

export function render({ entry: e }) {
  const crumbs = [["Home", "/"], ...(e.url.startsWith("/people/") ? [["Who decides", "/who-decides/"]] : []), [e.title]];
  return layout({ title: e.title, caption: e.caption, crumbs, body: e.html, aside: e.aside, meta: e.meta, cards: e.cards });
}
