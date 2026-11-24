// One output page per entry in archive.pages (topics, people incl. stubs, Who decides)
import { layout } from "./_includes/layout.js";

export const data = {
  pagination: { data: "archive.pages", size: 1, alias: "entry" },
  permalink: (d) => d.entry.url,
  eleventyComputed: { title: (d) => d.entry.title },
};

export function render({ entry, archive }) {
  return layout({ title: entry.title, body: entry.html, cards: entry.cards, nav: archive.nav });
}
