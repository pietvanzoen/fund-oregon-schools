// Search results from Pagefind's index, in the site's own markup. Every result loads at once (the index is
// small), so the filter counts and switching filters need no new search.
{
  const $ = (id) => document.getElementById(id);
  const params = new URLSearchParams(location.search);
  const query = (params.get("q") || "").trim();
  let kind = params.get("kind") || "";
  const ICON = { Topic: "topic", Person: "person", Term: "abbr" };
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
  // Pagefind's excerpt is escaped text with <mark> around matches; keep only the marks
  const excerpt = (html) => html.replace(/<(?!\/?mark>)[^>]*>/g, "");
  // The hosted preview serves files, not folders, so its links end in index.html (see eleventy.config.js)
  const preview = location.pathname.endsWith("/index.html");
  const root = new URL("../", location.href);
  const href = (url) => new URL(url.replace(/^\//, "") + (preview && url.endsWith("/") ? "index.html" : ""), root).href;

  $("q-page").value = query;
  if (query) {
    document.querySelector("h1").textContent = `Search results for "${query}"`;
    document.title = `Search results for "${query}" · Oregon Ed Trail`;
    run().catch(() => {
      $("search-status").textContent = "Search isn't working right now. Try again later.";
    });
  }

  async function run() {
    $("search-status").textContent = "Searching…";
    const pagefind = await import(new URL("../pagefind/pagefind.js", location.href).href);
    await pagefind.init();
    const found = await pagefind.search(query);
    const all = await Promise.all(found.results.map((r) => r.data()));
    const links = [...$("search-filters").querySelectorAll("a")];
    for (const a of links) {
      const k = a.dataset.kind;
      a.querySelector(".count").textContent = all.filter((d) => !k || d.filters.kind?.[0] === k).length;
      const p = new URLSearchParams({ q: query });
      if (k) p.set("kind", k);
      a.href = `${location.pathname}?${p}`;
      a.addEventListener("click", (e) => {
        e.preventDefault();
        kind = k;
        history.replaceState(null, "", a.href);
        show(all, links);
      });
    }
    $("search-filters").hidden = false;
    show(all, links);
  }

  function show(all, links) {
    for (const a of links)
      a.dataset.kind === kind ? a.setAttribute("aria-current", "true") : a.removeAttribute("aria-current");
    const list = all.filter((d) => !kind || d.filters.kind?.[0] === kind);
    const label = links
      .find((a) => a.dataset.kind === kind)
      ?.firstChild.textContent.trim()
      .toLowerCase();
    const n = list.length;
    $("search-status").textContent =
      `${n} ${n === 1 ? "result" : "results"} for "${query}"${kind ? ` in ${label}` : ""}`;
    $("search-none").hidden = n > 0;
    $("search-results").innerHTML = list
      .map((d) => {
        const k = d.filters.kind?.[0] || "Page";
        const line = d.meta.line ? esc(d.meta.line) : excerpt(d.excerpt);
        return (
          `<li class="box result"><p class="result-kind"><svg class="i" aria-hidden="true" focusable="false"><use href="#i-${ICON[k] || "topic"}"/></svg>${esc(k)}</p>` +
          `<h2><a href="${esc(href(d.url))}">${esc(d.meta.title)}</a></h2><p class="result-line${d.meta.line ? " muted" : ""}">${line}</p></li>`
        );
      })
      .join("");
  }
}
