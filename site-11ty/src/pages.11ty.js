// One output page per entry in archive.pages (topics, people incl. stubs, Who decides)
import { layout } from "./_includes/layout.js";

export const data = {
  pagination: { data: "archive.pages", size: 1, alias: "entry" },
  permalink: (d) => d.entry.url,
  eleventyComputed: { title: (d) => d.entry.title },
};

export function render({ entry: e }) {
  const crumbs = ["/who-decides/", "/topics/", "/glossary/"].includes(e.url) ? [["Home", "/"]] : [["Home", "/"], ["Topics", "/topics/"]];
  return layout({ title: e.title, crumbs, back: e.back, description: e.description, body: e.html, aside: e.aside, meta: e.meta, search: e.search, cards: e.cards });
}
