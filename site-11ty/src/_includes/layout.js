const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

// The site's one picture: a dotted trail ending in a marker, in the Oregon flag's navy and gold
const MARK = `<svg class="mark" viewBox="0 0 40 28" aria-hidden="true"><path d="M3 24 C 12 24, 10 10, 20 12 S 30 6, 34 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-dasharray="0.1 6"/><circle cx="34" cy="5" r="4" fill="#f3c13a"/></svg>`;

// Card data for this page only; the script reads it as text, never as markup
export function layout({ title, caption, crumbs = [], body, aside = "", meta = "", cards, wide = false }) {
  const trail = crumbs.length
    ? `<nav class="crumbs" aria-label="Breadcrumb"><ol>${crumbs.map(([t, u]) => `<li>${u ? `<a href="${u}">${esc(t)}</a>` : esc(t)}</li>`).join("")}</ol></nav>` : "";
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Oregon Ed Trail</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#content">Skip to main content</a>
<header class="masthead">
  <div class="wrap masthead-row">
    <a class="brand" href="/">${MARK}<span><span class="brand-name">Oregon Ed Trail</span><span class="brand-tag">Following the money behind Oregon's schools</span></span></a>
    <nav class="topnav" aria-label="Main"><a href="/">Topics</a><a href="/who-decides/">Who decides</a><a href="https://fundoregonschools.org/decisions/">What's being decided</a></nav>
  </div>
</header>
<div class="phase"><div class="wrap"><strong class="tag">Test build</strong> A preview of a new design. The facts come from the same archive as <a href="https://fundoregonschools.org/">fundoregonschools.org</a>.</div></div>
<div class="wrap">
${trail}
<main id="content" class="${aside ? "grid" : wide ? "" : "narrow"}">
  <header class="page-head">
    ${caption ? `<p class="caption">${esc(caption)}</p>` : ""}
    <h1>${esc(title)}</h1>
  </header>
  <article>
    ${body}
  </article>
  ${aside ? `<div class="side">${aside}</div>` : ""}
</main>
${meta ? `<p class="page-meta">${meta}</p>` : ""}
</div>
<footer class="foot">
  <div class="wrap">
    <p>Every claim on this site links to where it comes from. <span class="cite cite-src">📄 Document</span> opens the state or legislative document at the cited page; <span class="cite cite-news">📰 Outlet</span> is a news report; <span class="cite cite-der">🧮 our sum</span> is a figure we calculated, linked to its method. Boxes marked <strong>Our analysis</strong> are interpretation, kept apart from what the documents say.</p>
    <p class="foot-small">Maintained by Oregon public school parents. Analysis <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. <a href="https://github.com/pietvanzoen/fund-oregon-schools">Research archive on GitHub</a>.</p>
  </div>
</footer>
<div id="card" class="card" role="dialog" aria-modal="false" aria-labelledby="card-title" hidden>
  <p class="card-kind" id="card-kind"></p>
  <p class="card-title" id="card-title"></p>
  <div id="card-lines"></div>
  <p class="card-actions"><a id="card-open" href="#">Open</a><a id="card-also" href="#" hidden></a><button type="button" id="card-close">Close</button></p>
</div>
<script type="application/json" id="cards">${JSON.stringify(cards).replace(/</g, "\\u003c")}</script>
<script src="/assets/card.js"></script>
</body>
</html>`;
}
