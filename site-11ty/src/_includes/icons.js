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
  decide: '<rect x="2" y="2" width="20" height="20" rx="4"/><path d="M6 12l4 4 8-8"/>',
  dollar: '<circle cx="12" cy="12" r="9"/><path d="M14.5 9.5c-.5-1-1.5-1.5-2.5-1.5-1.7 0-2.5 1-2.5 2s1 1.6 2.5 2 2.5 1 2.5 2-1 2-2.5 2c-1.1 0-2-.5-2.5-1.5M12 6v2M12 16v2"/>',
  scales: '<path d="M12 3v18M5 7h14M5 7l-3 7h6zM19 7l-3 7h6zM8 21h8"/>',
  target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
  chevron: '<path d="M6 9l6 6 6-6"/>',
  close: '<path d="M6 6l12 12M18 6L6 18"/>',
};
export const SPRITE = `<svg width="0" height="0" style="position:absolute" aria-hidden="true">${Object.entries(I)
  .map(([k, v]) => `<symbol id="i-${k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${v}</symbol>`).join("")}</svg>`;
export const icon = (k, cls = "i") => `<svg class="${cls}" aria-hidden="true" focusable="false"><use href="#i-${k}"/></svg>`;
