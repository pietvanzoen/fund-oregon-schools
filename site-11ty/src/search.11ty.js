// The search page: the form and empty containers; assets/search.js fills them from Pagefind's index
import { layout } from "./_includes/layout.js";
import { icon } from "./_includes/icons.js";

export const data = { permalink: "/search/" };

// Filter pills, in this order; Documents stays at 0 until the archived documents are indexed
const KINDS = [["", "All"], ["Topic", "Topics"], ["Person", "People"], ["Term", "Terms"], ["Document", "Documents"]];

export function render() {
  const body = `<form class="search search-page" role="search" action="/search/" method="get">
<label class="vh" for="q-page">Search topics, people and terms</label>
<input id="q-page" name="q" type="search" autocomplete="off"><button type="submit" class="search-go">${icon("search")}<span class="vh">Search</span></button>
</form>
<p id="search-status" class="search-status" role="status">Enter a word to search topics, people and terms.</p>
<nav id="search-filters" class="filters" aria-label="Filter results" hidden><ul>${KINDS.map(([k, label]) =>
    `<li><a href="/search/" data-kind="${k}">${label} <span class="count">0</span></a></li>`).join("")}</ul></nav>
<ol id="search-results" class="results"></ol>
<div id="search-none" class="box no-results" hidden>
<p>Nothing on this site matches that. Check the spelling, try a shorter word, or browse the <a href="/topics/">topic list</a> and <a href="/who-decides/">Who decides</a>.</p>
</div>
<p class="search-docs">Looking for an original document? Search finds pages on this site. The documents themselves are listed under each topic's <strong>What the documents say</strong>.</p>`;
  return layout({ title: "Search", crumbs: [["Home", "/"]], body, search: "page", cards: {} });
}
