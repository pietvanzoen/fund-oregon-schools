import { layout } from "./_includes/layout.js";

export const data = { permalink: "/" };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

export function render({ archive }) {
  const cards = {};
  const item = (e) => { cards[e.url] = e; return `<li><a href="${e.url}" data-card="${e.url}">${esc(e.title)}</a>${e.stub ? ' <span class="muted">(stub)</span>' : ""}</li>`; };
  const body = `<h1>Eleventy spike</h1>
<p>A test build of three page types (topics, people and Who decides) from the same files as the live site, to try wiki-style linking: generated links on first mention, backlinks, stub pages and one tap-to-open preview card for every kind of entity. Other links go to <a href="https://fundoregonschools.org/">the live site</a>.</p>
<h2>Topics</h2><ul>${archive.nav.topics.map(item).join("")}</ul>
<h2>People</h2><p><a href="/who-decides/">Who decides</a></p><ul>${archive.nav.people.map(item).join("")}</ul>`;
  return layout({ title: "Eleventy spike", body, cards, nav: archive.nav });
}
