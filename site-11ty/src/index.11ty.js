// The home page, built from analysis/START.md in archive.js
import { layout } from "./_includes/layout.js";

export const data = { permalink: "/" };

export function render({ archive: { home } }) {
  return layout({ title: home.title, hero: home.hero, body: home.html, meta: home.meta, cards: home.cards, wide: true });
}
