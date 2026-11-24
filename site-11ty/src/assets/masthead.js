// Masthead. Phones: the main nav sits behind the Menu button. Everywhere: the search icon opens a panel under
// the masthead (GOV.UK pattern). Without JavaScript the nav stays open and the search icon is a link to /search/.
{
  const menuBtn = document.getElementById("menu-button");
  const nav = document.getElementById("menu");
  const link = document.getElementById("search-toggle");
  const panel = document.getElementById("search-panel");
  const field = document.getElementById("q-top");

  // The link becomes a button that opens the panel in place
  const btn = document.createElement("button");
  btn.type = "button";
  btn.id = link.id;
  btn.className = link.className;
  btn.setAttribute("aria-controls", "search-panel");
  link.replaceWith(btn);

  const setMenu = (open) => { menuBtn.setAttribute("aria-expanded", String(open)); nav.classList.toggle("open", open); };
  const setSearch = (open) => {
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", open ? "Close search" : "Search");
    btn.innerHTML = `<svg class="i" aria-hidden="true" focusable="false"><use href="#i-${open ? "close" : "search"}"/></svg>`;
    panel.hidden = !open;
    if (open) { setMenu(false); field.focus(); }
  };
  setSearch(false);

  menuBtn.addEventListener("click", () => {
    const open = menuBtn.getAttribute("aria-expanded") !== "true";
    setMenu(open);
    if (open) setSearch(false);
  });
  btn.addEventListener("click", () => setSearch(btn.getAttribute("aria-expanded") !== "true"));
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (btn.getAttribute("aria-expanded") === "true") { setSearch(false); btn.focus(); }
    else if (menuBtn.getAttribute("aria-expanded") === "true") { setMenu(false); menuBtn.focus(); }
  });
}
