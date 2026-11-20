// Quote filter and chart tooltips. Works with Material's instant loading off (default).
(function () {
  function init() {
    var filter = document.querySelector(".quote-filter");
    if (filter) {
      filter.addEventListener("click", function (e) {
        var b = e.target.closest("button");
        if (!b) return;
        filter.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        var who = b.dataset.person;
        document.querySelectorAll(".quote-card").forEach(function (c) {
          c.hidden = who && c.dataset.person !== who;
        });
      });
    }
    var tip = null;
    function show(el, x, y) {
      if (!tip) { tip = document.createElement("div"); tip.className = "chart-tip"; document.body.appendChild(tip); }
      tip.textContent = el.dataset.tip;
      tip.style.left = Math.min(x + 12, window.innerWidth - 300) + "px";
      tip.style.top = (y + 12) + "px";
      tip.hidden = false;
    }
    function hide() { if (tip) tip.hidden = true; }
    document.querySelectorAll(".chart [data-tip]").forEach(function (el) {
      el.addEventListener("mousemove", function (e) { show(el, e.clientX, e.clientY); });
      el.addEventListener("mouseleave", hide);
      el.addEventListener("focus", function () { var r = el.getBoundingClientRect(); show(el, r.left + r.width / 2, r.top); });
      el.addEventListener("blur", hide);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
