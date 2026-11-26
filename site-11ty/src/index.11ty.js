// The home page, built from analysis/START.md in archive.js
import { layout } from "./_includes/layout.js";

export const data = { permalink: "/" };

export function render({ archive: { home } }) {
  return layout({
    url: "/",
    title: home.title,
    seo: "Oregon Ed Trail",
    description: home.description,
    hero: home.hero,
    body: home.html,
    meta: home.meta,
    cards: home.cards,
    wide: true,
    charts: home.charts,
  });
}
