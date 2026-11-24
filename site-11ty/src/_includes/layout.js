import { SPRITE, icon } from "./icons.js";

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

// The site's one picture: a dotted trail on a white tile, ending in a gold marker
const MARK = `<svg class="mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#fff"/><path d="M8 30 C 16 30, 14 16, 22 18 S 29 11, 32 10" fill="none" stroke="#005eb8" stroke-width="3" stroke-linecap="round" stroke-dasharray="0.1 5.5"/><circle cx="32" cy="10" r="4" fill="#ffb81c"/></svg>`;

const SITE = "https://oregonedtrail.org";

// seo: the <title> and link-preview title when it differs from the H1; the home page's is the site name alone.
// The home page also names the site for Google's site-name display (WebSite structured data)
export function layout({ url, title, seo = "", crumbs = [], back = null, description = "", hero = "", body, aside = "", meta = "", search = null, script = "", cards, wide = false, noindex = false }) {
  const full = seo === "Oregon Ed Trail" ? seo : `${seo || title} · Oregon Ed Trail`;
  const trail = back
    ? `<p class="crumbs back"><a href="${back[1]}">‹ ${esc(back[0])}</a></p>`
    : crumbs.length ? `<nav class="crumbs" aria-label="Breadcrumb"><ol>${crumbs.map(([t, u]) => `<li><a href="${u}">${esc(t)}</a></li>`).join("")}</ol></nav>` : "";
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(full)}</title>
${description ? `<meta name="description" content="${esc(description)}">\n` : ""}${noindex ? '<meta name="robots" content="noindex">\n' : ""}${url ? `<link rel="canonical" href="${SITE}${url}">\n<meta property="og:url" content="${SITE}${url}">\n` : ""}<meta property="og:type" content="website">
<meta property="og:site_name" content="Oregon Ed Trail">
<meta property="og:title" content="${esc(seo || title)}">
${description ? `<meta property="og:description" content="${esc(description)}">\n` : ""}<meta name="twitter:card" content="summary">
${url === "/" ? `<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Oregon Ed Trail","url":"${SITE}/"}</script>\n` : ""}<!-- Umami Cloud page analytics: cookieless, no personal data -->
<script defer src="https://cloud.umami.is/script.js" data-website-id="da03c53e-e3dd-49c6-9802-664629302cd2"></script>
<link rel="icon" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script>document.documentElement.classList.add("js")</script>
</head>
<body>
${SPRITE}
<a class="skip" href="#content">Skip to main content</a>
<header class="masthead">
  <div class="wrap masthead-row">
    <a class="brand" href="/">${MARK}<span><span class="brand-name">Oregon Ed Trail</span><span class="brand-tag">Following the money behind Oregon's schools</span></span></a>
    <button type="button" id="menu-button" class="menu-button" aria-expanded="false" aria-controls="menu">${icon("chevron")}Menu</button>
    <nav id="menu" class="topnav" aria-label="Main"><ul><li><a href="/topics/">Topics</a></li><li><a href="/who-decides/">Who decides</a></li><li><a href="/decisions/">What's being decided</a></li><li class="menu-about"><a href="/about/">About this site</a></li></ul></nav>
    <span class="mast-divider" aria-hidden="true"></span>
    <a href="/search/" id="search-toggle" class="search-toggle" aria-label="Search">${icon("search")}</a>
  </div>
</header>
<div id="search-panel" class="search-panel" hidden>
  <form class="wrap" role="search" action="/search/" method="get">
    <label for="q-top" class="search-label">Search Oregon Ed Trail</label>
    <div class="search"><input id="q-top" name="q" type="search" autocomplete="off" aria-describedby="q-top-hint"><button type="submit" class="search-go">${icon("search")}<span class="vh">Search</span></button></div>
    <p id="q-top-hint" class="search-hint">Topics, people and terms, for example "PERS" or "Lieber"</p>
  </form>
</div>
${hero}
<div class="wrap">
${trail}
<main id="content" class="${aside ? "grid" : wide ? "" : "narrow"}"${search?.kind ? ` data-pagefind-body data-pagefind-filter="kind:${search.kind}" data-pagefind-meta="line[data-line]" data-line="${esc(search.line)}"` : ""}>
  ${hero ? "" : `<h1>${esc(title)}</h1>`}
  <article>
    ${body}
  </article>
  ${aside ? `<div class="side" data-pagefind-ignore>${aside}</div>` : ""}
</main>
${meta ? `<section class="page-meta" aria-labelledby="about-page"><h2 id="about-page">About this page</h2>${meta}</section>` : ""}
</div>
<footer class="foot">
  <div class="wrap">
    <nav aria-label="About the site"><ul class="foot-links"><li><a href="/about/">About this site</a></li><li><a href="/updates/">What's new</a></li><li><a href="mailto:hello@oregonedtrail.org">Contact: hello@oregonedtrail.org</a></li><li><a href="https://github.com/pietvanzoen/fund-oregon-schools">Research archive on GitHub</a></li></ul></nav>
    <p>Every fact links to where it comes from: <span class="cite cite-src">${icon("doc")}Document, p.3</span> a document, <span class="cite cite-news">${icon("news")}Outlet</span> a news report, <span class="cite cite-der">${icon("calc")}our sum</span> our own calculation. Our interpretation is kept apart from what the documents say, in yellow boxes headed or starting <strong>Our analysis</strong>.</p>
    <p class="foot-small">Run by Oregon public school parents. Analysis licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
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
<script src="/assets/masthead.js"></script>
${search === "page" ? '<script src="/assets/search.js"></script>' : ""}${script ? `<script src="/assets/${script}.js"></script>` : ""}
</body>
</html>`;
}
