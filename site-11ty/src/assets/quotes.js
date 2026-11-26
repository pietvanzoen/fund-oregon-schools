// What they've said: filter the quote cards by person. Without JavaScript the filter stays hidden and every quote shows
(() => {
  var filter = document.querySelector(".quote-filter");
  if (!filter) return;
  filter.hidden = false;
  filter.addEventListener("click", (e) => {
    var b = e.target.closest("button");
    if (!b) return;
    filter.querySelectorAll("button").forEach((x) => {
      x.setAttribute("aria-pressed", x === b);
    });
    document.querySelectorAll(".quote-card").forEach((c) => {
      c.hidden = !!b.dataset.person && c.dataset.person !== b.dataset.person;
    });
  });
})();
