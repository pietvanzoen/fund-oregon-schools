const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

// Card data for this page only; the script reads it as text, never as markup
export function layout({ title, body, cards, nav }) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Oregon Ed Trail (spike)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header class="top"><a class="brand" href="/">Oregon Ed Trail <span class="muted">spike</span></a>
<nav><a href="/who-decides/">Who decides</a><a href="/reserves/">Reserves</a><a href="/formula/">Formula</a></nav></header>
<main>${body}</main>
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
