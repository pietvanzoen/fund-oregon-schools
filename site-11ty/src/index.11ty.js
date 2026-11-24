import { layout } from "./_includes/layout.js";

export const data = { permalink: "/" };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

export function render({ archive }) {
  const cards = {};
  const topic = (e) => { cards[e.url] = e; return `<li><a class="list-link" href="${e.url}" data-card="${e.url}">${esc(e.title)}</a><p>${esc(e.lines[0])}</p></li>`; };
  const person = (e) => { cards[e.url] = e; return `<li><a href="${e.url}" data-card="${e.url}">${esc(e.title)}</a><span class="muted">${esc(e.lines.at(-1)?.replace(/^2027: /, "") || "")}</span></li>`; };
  const profiled = archive.nav.people.filter((p) => !p.stub);
  const body = `<p class="lead">Primary documents and cited analysis on Oregon K-12 funding: how much the state spends, how it's shared and what it buys, focused on the 2027-29 budget.</p>
<p>This test build shows topic pages, people pages and Who decides. Other links go to the current site.</p>
<div class="home-grid">
<section><h2>Topics</h2><ul class="topic-list">${archive.nav.topics.map(topic).join("")}</ul></section>
<section><h2>People</h2><ul class="people-list">${profiled.map(person).join("")}</ul>
<p><a href="/who-decides/">Everyone who decides (${archive.nav.people.length})</a></p></section>
</div>`;
  return layout({ title: "Oregon K-12 funding, document by document", body, cards, wide: true });
}
