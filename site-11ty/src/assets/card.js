// One preview card for every [data-card] element: hover or focus shows it with a mouse,
// the first tap shows it on touch screens (the card's Open link or a second tap follows the link).
{
  const data = JSON.parse(document.getElementById("cards").textContent);
  const card = document.getElementById("card");
  const $ = (id) => document.getElementById(id);
  // Go by the input actually used, so touch laptops and phones in desktop mode behave too
  const touch = { matches: matchMedia("(hover: none)").matches };
  document.addEventListener("pointerdown", (e) => { touch.matches = e.pointerType !== "mouse"; }, true);
  let owner = null;
  let timer = null;

  function show(el) {
    const c = data[el.dataset.card];
    if (!c) return;
    clearTimeout(timer);
    owner = el;
    $("card-kind").textContent = c.kind;
    $("card-title").textContent = c.title;
    $("card-lines").replaceChildren(...c.lines.map((l) => Object.assign(document.createElement("p"), { textContent: l })));
    const open = $("card-open");
    open.hidden = !c.url;
    if (c.url) {
      open.href = !c.external && el.tagName === "A" ? el.href : c.url; // the link's own href, already right for this page
      open.textContent = c.external ? "Open document ↗" : "Open page";
      open.target = c.external ? "_blank" : "";
      open.rel = c.external ? "noopener" : "";
    }
    const also = $("card-also");
    also.hidden = !c.also;
    if (c.also) { also.href = c.also.url; also.textContent = c.also.label + " ↗"; also.target = "_blank"; }
    $("card-close").hidden = !touch.matches;
    card.hidden = false;
    el.setAttribute("aria-describedby", "card");
    place(el);
  }

  function place(el) {
    if (touch.matches || innerWidth < 600) { card.classList.add("sheet"); card.style.left = card.style.top = ""; return; }
    card.classList.remove("sheet");
    const r = el.getBoundingClientRect();
    const w = card.offsetWidth, h = card.offsetHeight;
    const left = Math.max(8, Math.min(r.left, innerWidth - w - 8));
    const below = r.bottom + 8 + h < innerHeight;
    card.style.left = left + scrollX + "px";
    card.style.top = (below ? r.bottom + 8 : r.top - h - 8) + scrollY + "px";
  }

  function hide(now) {
    clearTimeout(timer);
    const go = () => { card.hidden = true; owner?.removeAttribute("aria-describedby"); owner = null; };
    now ? go() : (timer = setTimeout(go, 250));
  }

  document.addEventListener("click", (e) => {
    const el = e.target.closest("[data-card]");
    if (el && touch.matches && owner !== el) { e.preventDefault(); show(el); return; }
    if (!el && !card.contains(e.target)) hide(true);
  });
  document.addEventListener("mouseover", (e) => {
    if (touch.matches) return;
    const el = e.target.closest("[data-card]");
    if (el) { clearTimeout(timer); timer = setTimeout(() => show(el), 300); }
    else if (card.contains(e.target)) clearTimeout(timer);
  });
  document.addEventListener("mouseout", (e) => {
    if (!touch.matches && (e.target.closest("[data-card]") || card.contains(e.target))) hide();
  });
  document.addEventListener("focusin", (e) => {
    const el = e.target.closest("[data-card]");
    if (el && !touch.matches) show(el); // a tap focuses before its click; the click decides
    else if (!el && !card.contains(e.target)) hide(true);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Tab") touch.matches = false;
    if (e.key === "Escape" && !card.hidden) { const o = owner; hide(true); o?.focus(); } });
  $("card-close").addEventListener("click", () => hide(true));
}
