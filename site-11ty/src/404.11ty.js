// GitHub Pages serves /404.html for any path with no page; links stay absolute so they work from any depth
import { layout } from "./_includes/layout.js";

export const data = { permalink: "/404.html", eleventyExcludeFromCollections: true };

export function render() {
  const body = `<p>There's no page at this address. It may have moved, or the link may have a typo.</p>
<p>Try the <a href="/">home page</a>, the <a href="/topics/">topic list</a>, <a href="/decisions/">what's being decided</a> or <a href="/search/">search</a>.</p>`;
  return layout({ title: "Page not found", body, cards: {}, noindex: true });
}
