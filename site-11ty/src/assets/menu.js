// Phones: the main nav sits behind the Menu button; without JavaScript it stays open
{
  const btn = document.getElementById("menu-button");
  const nav = document.getElementById("menu");
  const set = (open) => { btn.setAttribute("aria-expanded", String(open)); nav.classList.toggle("open", open); };
  btn.addEventListener("click", () => set(btn.getAttribute("aria-expanded") !== "true"));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { set(false); btn.focus(); }
  });
}
