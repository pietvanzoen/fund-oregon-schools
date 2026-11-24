// Line icons (24 grid, stroke 2, currentColor), drawn once per page as a sprite and used by id
const I = {
  doc: '<path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4"/>',
  news: '<path d="M4 5h13v14H6a2 2 0 0 1-2-2z"/><path d="M17 9h3v8a2 2 0 0 1-2 2"/><path d="M8 9h5M8 13h5"/>',
  calc: '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
  video: '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>',
  archive: '<path d="M3 4h18v4H3z"/><path d="M5 8v12h14V8M10 12h4"/>',
  person: '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
  topic: '<path d="M6 3h12v18l-6-4-6 4z"/>',
  abbr: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
  think: '<path d="M4 5h16v11H9l-5 4z"/>',
};
export const SPRITE = `<svg width="0" height="0" style="position:absolute" aria-hidden="true">${Object.entries(I)
  .map(([k, v]) => `<symbol id="i-${k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${v}</symbol>`).join("")}</svg>`;
export const icon = (k, cls = "i") => `<svg class="${cls}" aria-hidden="true" focusable="false"><use href="#i-${k}"/></svg>`;
