import { SPRITE, icon } from "./icons.js";

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

// The site's one picture: a dotted trail on a white tile, ending in a gold marker
const MARK = `<svg class="mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#fff"/><path d="M8 30 C 16 30, 14 16, 22 18 S 29 11, 32 10" fill="none" stroke="#005eb8" stroke-width="3" stroke-linecap="round" stroke-dasharray="0.1 5.5"/><circle cx="32" cy="10" r="4" fill="#ffb81c"/></svg>`;

// Card data for this page only; the script reads it as text, never as markup
export function layout({ title, crumbs = [], back = null, description = "", body, aside = "", meta = "", cards, wide = false }) {
  const trail = back
    ? `<p class="crumbs back"><a href="${back[1]}">‹ ${esc(back[0])}</a></p>`
    : crumbs.length ? `<nav class="crumbs" aria-label="Breadcrumb"><ol>${crumbs.map(([t, u]) => `<li><a href="${u}">${esc(t)}</a></li>`).join("")}</ol></nav>` : "";
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Oregon Ed Trail</title>
${description ? `<meta name="description" content="${esc(description)}">\n` : ""}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
${SPRITE}
<a class="skip" href="#content">Skip to main content</a>
<header class="masthead">
  <div class="wrap masthead-row">
    <a class="brand" href="/">${MARK}<span><span class="brand-name">Oregon Ed Trail</span><span class="brand-tag">Following the money behind Oregon's schools</span></span></a>
    <nav class="topnav" aria-label="Main"><a href="/">Topics</a><a href="/who-decides/">Who decides</a><a href="https://fundoregonschools.org/decisions/">What's being decided</a></nav>
  </div>
</header>
<div class="wrap">
<p class="phase"><strong class="tag">Test build</strong> A preview of a new design. The facts come from the same archive as <a href="https://fundoregonschools.org/">fundoregonschools.org</a>.</p>
${trail}
<main id="content" class="${aside ? "grid" : wide ? "" : "narrow"}">
  <h1>${esc(title)}</h1>
  <article>
    ${body}
  </article>
  ${aside ? `<div class="side">${aside}</div>` : ""}
</main>
${meta ? `<section class="page-meta" aria-labelledby="about-page"><h2 id="about-page">About this page</h2>${meta}</section>` : ""}
</div>
<footer class="foot">
  <div class="wrap">
    <p>Every fact on this site links to where it comes from. <span class="cite cite-src">${icon("doc")}Document, p.3</span> opens the state or legislative document at the cited page; <span class="cite cite-news">${icon("news")}Outlet</span> is a news report; <span class="cite cite-der">${icon("calc")}our sum</span> is a figure we calculated, linked to its method; <span class="cite cite-vid">${icon("video")}Recording, 0:41:12</span> is a hearing at that time. Sections headed <strong>What we think this means</strong> and lines starting <strong>We think:</strong> are our interpretation, kept apart from what the documents say.</p>
    <p class="foot-small">Maintained by Oregon public school parents. Analysis <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. <a href="https://github.com/pietvanzoen/fund-oregon-schools">Research archive on GitHub</a>.</p>
  </div>
</footer>
<div id="card" class="card" role="dialog" aria-modal="false" aria-labelledby="card-title" hidden>
  <div class="card-handle" aria-hidden="true"></div>
  <p class="card-kind"><svg class="i" aria-hidden="true" focusable="false"><use id="card-icon" href="#i-doc"/></svg><span id="card-kind"></span></p>
  <p class="card-title" id="card-title"></p>
  <div id="card-lines"></div>
  <p class="card-actions"><a id="card-open" class="btn" href="#">Open</a><button type="button" id="card-close" class="btn btn-2">Close</button></p>
  <p class="card-also"><a id="card-also" href="#" hidden></a></p>
</div>
<script type="application/json" id="cards">${JSON.stringify(cards).replace(/</g, "\\u003c")}</script>
<script src="/assets/card.js"></script>
</body>
</html>`;
}
