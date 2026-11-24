// Builds every page of the spike from analysis/ and sources/, the same files the Python tools read.
// Output: { pages: [{url, title, html, cards}] }. Templates only wrap it in the layout.
import fs from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";
import markdownIt from "markdown-it";

const ROOT = path.resolve(import.meta.dirname, "../../..");
const LIVE = "https://fundoregonschools.org/"; // pages the spike doesn't build yet link to the live site
const BLOB = "https://github.com/pietvanzoen/fund-oregon-schools/blob/main/";
const md = markdownIt({ html: true });

const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
const csv = (p) => parse(read(p), { columns: true, skip_empty_lines: true, relax_column_count: true });
const jsonl = (p) => read(p).split("\n").filter((l) => l.trim()).map((l) => JSON.parse(l));
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
const plain = (s) => s.replace(/\[(SRC|VID|NEWS|PPSARCH|DER):[^\]]+\]/g, "").replace(/`([^`]+)`/g, "$1")
  .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/[*_]/g, "").replace(/\s+/g, " ").replace(/ ([.,;)])/g, "$1").trim();
const clip = (s, n = 220) => (s.length <= n ? s : s.slice(0, n).replace(/\s+\S*$/, "") + "…");

// ------------------------------------------------------------- data

const queue = csv("sources/_queue.csv");
const manifest = Object.fromEntries(jsonl("sources/_manifest.jsonl").map((r) => [r.path, r]));
const news = Object.fromEntries(jsonl("sources/news/index.jsonl").map((r) => [r.id, r]));
const derived = {};
for (const f of fs.readdirSync(path.join(ROOT, "analysis/derived")).filter((f) => f.endsWith(".csv")))
  for (const r of csv(`analysis/derived/${f}`)) derived[`${f.slice(0, -4)}/${r.id}`] = r;
const srcInfo = {};
for (const r of queue) srcInfo[r.path.trim()] = { title: r.title, date: r.date, url: r.url };
for (const [p, r] of Object.entries(manifest)) srcInfo[p] = { ...srcInfo[p], url: r.final_url || r.url, title: srcInfo[p]?.title || r.title, date: srcInfo[p]?.date || r.date };

const people = csv("analysis/people/people.csv");
const decisions = Object.fromEntries(csv("analysis/decisions.csv").map((r) => [r.id, r]));
// positions.csv is append-only: a row whose line number another row `replaces` is superseded (header = line 1)
const positionRows = csv("analysis/positions.csv");
const replaced = new Set(positionRows.map((r) => Number(r.replaces)).filter(Boolean));
const positions = positionRows.filter((_, i) => !replaced.has(i + 2));
const options = csv("analysis/options.csv");
const glossary = csv("analysis/glossary.csv").filter((r) => r.kind === "acronym" && r.tooltip);

// ------------------------------------------------------------- entities (everything that gets a card)

const TITLE = { Governor: "Gov.", Senate: "Sen.", House: "Rep." };
const entities = {};
for (const p of people) {
  const seat = [p.party && p.district ? `${p.party}-District ${p.district}` : "", p.area].filter(Boolean).join(", ");
  entities[`person:${p.id}`] = {
    kind: "Person", title: `${TITLE[p.office] || ""} ${p.name}`.trim(), url: `/people/${p.id}/`,
    lines: [seat || p.office, p.role_2027 && `2027: ${p.role_2027}`].filter(Boolean), name: p.name, row: p,
  };
}
const topicFiles = fs.readdirSync(path.join(ROOT, "analysis/topics")).filter((f) => f.endsWith(".md")).sort();
for (const f of topicFiles) {
  const text = read(`analysis/topics/${f}`);
  const h1 = (text.match(/^# (.+)$/m) || [, f])[1].trim();
  const lead = (text.split(/^## Analysis\s*$/m)[1] || text.split("\n\n")[1] || "").trim().split(/\n\s*\n/)[0];
  entities[`topic:${f.slice(0, -3)}`] = { kind: "Topic", title: h1, url: `/${f.slice(0, -3)}/`, lines: [clip(plain(lead))] };
}
for (const g of glossary)
  entities[`term:${g.term}`] = { kind: "Abbreviation", title: g.full_name || g.term, url: null, lines: [g.tooltip], term: g.term };

// A card for one citation chip; built per chip because the page number differs
function citeCard(kind, body) {
  body = body.trim();
  if (kind === "SRC") {
    const [, p, page] = body.match(/^(.*?)(?:\s+p\.(\d+)(?:-\d+)?)?$/);
    const s = srcInfo[p] || {};
    const base = s.url || BLOB + "sources/" + p;
    const url = base + (page && p.toLowerCase().endsWith(".pdf") ? `#page=${page}` : "");
    return { kind: "Document", title: s.title || path.basename(p), url, external: true,
      lines: [[s.date && `Dated ${s.date}`, page && `cited at page ${page}`].filter(Boolean).join(", ")],
      also: { label: "Archived copy", url: BLOB + "sources/" + p }, chip: `📄 ${shortTitle(s.title || path.basename(p))}${page ? `, p.${page}` : ""}`, cls: "src" };
  }
  if (kind === "NEWS") {
    const r = news[body] || {};
    return { kind: "News report", title: r.title || body, url: r.url, external: true, lines: [[r.outlet, r.date].filter(Boolean).join(", ")],
      chip: `📰 ${(r.outlet || "news").split("/")[0]}`, cls: "news" };
  }
  if (kind === "DER") {
    const r = derived[body] || {};
    const est = r.kind === "est";
    return { kind: est ? "Our estimate" : "Our calculation", title: r.label || body, external: true,
      url: BLOB + "analysis/derived/" + body.split("/")[0] + ".csv", lines: [r.method && `Method: ${r.method}`, r.assumptions && `Assumes: ${r.assumptions}`].filter(Boolean),
      chip: est ? "🧮 our estimate" : "🧮 our sum", cls: "der" };
  }
  if (kind === "PPSARCH")
    return { kind: "Other archive", title: "Portland Public Schools research archive", url: "https://github.com/timaelliott/save-our-schools", external: true, lines: [body], chip: "🏫 PPS archive", cls: "pps" };
  const [, ts] = body.split("@");
  return { kind: "Recording", title: path.basename(body.split("@")[0]), url: null, lines: [ts ? `At ${ts}` : ""], chip: `🎥 ${ts || "video"}`, cls: "vid" };
}

function shortTitle(t) {
  t = t.split(" (")[0];
  const head = t.split(": ")[0];
  t = head.length >= 8 ? head : t;
  return t.length <= 48 ? t : t.slice(0, 46).replace(/\s+\S*$/, "") + "…";
}

// ------------------------------------------------------------- page rendering

// Analysis file path -> entity id, for backticked references like `people/kotek.md#esf`
const FILE_ENTITY = Object.fromEntries([
  ...people.map((p) => [`people/${p.id}.md`, `person:${p.id}`]),
  ...topicFiles.map((f) => [`topics/${f}`, `topic:${f.slice(0, -3)}`]),
]);
const LIVE_PAGES = { "decisions.md": "decisions/", "timeline.md": "timeline/", "START.md": "", "promises.csv": "promises/",
  "people/quotes_all.jsonl": "quotes/", "decisions.csv": "decisions/", "positions.csv": "decisions/", "questions.csv": "questions/" };

class Page {
  constructor(id, url, title) { Object.assign(this, { id, url, title, refs: new Set(), cards: {} }); }

  card(id, data) { this.cards[id] = data; return id; }

  // Markdown with our conventions -> HTML
  render(text, srcFile) {
    text = text.replace(/`([\w./-]+\.(?:md|csv|jsonl))(#[\w-]+)?`/g, (m, ref, anchor = "") => {
      const key = path.posix.normalize(path.posix.join(path.posix.dirname(srcFile), ref));
      const ent = FILE_ENTITY[key] || FILE_ENTITY[ref];
      if (ent) return `[${entities[ent].title}](${entities[ent].url}${anchor})`;
      const live = LIVE_PAGES[key] ?? LIVE_PAGES[ref];
      return live === undefined ? m : `[${ref.replace(/\.\w+$/, "")}](${LIVE}${live}${anchor})`;
    });
    text = text.replace(/\[\[([\w:-]+)\]\]/g, (_, ref) => {
      const id = entities[ref] ? ref : `person:${ref}`;
      if (!entities[id]) throw new Error(`${srcFile}: unknown link [[${ref}]]`);
      return `[${entities[id].title}](${entities[id].url})`;
    });
    text = markAnalysis(text);
    text = text.replace(/\[(SRC|VID|NEWS|PPSARCH|DER):([^\]]+)\]/g, (_, kind, body) => {
      const c = citeCard(kind, body);
      const id = this.card(`cite:${kind}:${body.trim()}`, c);
      const attrs = `class="cite cite-${c.cls}" data-card="${esc(id)}"`;
      return c.url ? `<a ${attrs} href="${esc(c.url)}" target="_blank" rel="noopener">${esc(c.chip)}</a>` : `<span ${attrs} tabindex="0">${esc(c.chip)}</span>`;
    });
    return this.linkMentions(md.render(text));
  }

  // Cards on existing entity links; first mention of each person and abbreviation gets a link or <abbr>
  linkMentions(html) {
    const seen = new Set([this.id]);
    html = html.replace(/<a href="(\/[^"#]*)(#[^"]*)?"/g, (m, url, anchor = "") => {
      const id = Object.keys(entities).find((k) => entities[k].url === url);
      if (!id) return m;
      seen.add(id); this.refs.add(id); this.card(id, entities[id]);
      return `<a href="${url}${anchor}" data-card="${id}"`;
    });
    const names = Object.entries(entities).filter(([, e]) => e.name || e.term);
    const parts = html.split(/(<[^>]+>)/);
    let skip = 0; // inside <a>, <code>, headings or <abbr>
    for (let i = 0; i < parts.length; i++) {
      const t = parts[i];
      if (t.startsWith("<")) {
        if (/^<(a|code|h[1-6]|abbr|script)[\s>]/.test(t)) skip++;
        else if (/^<\/(a|code|h[1-6]|abbr|script)>/.test(t)) skip--;
        continue;
      }
      if (skip) continue;
      for (const [id, e] of names) {
        if (seen.has(id)) continue;
        const word = e.name || e.term;
        const re = new RegExp(`(^|[^\\w-])(${word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})(?![\\w-])`);
        if (!re.test(parts[i])) continue;
        seen.add(id); this.card(id, e);
        if (e.url) this.refs.add(id);
        parts[i] = parts[i].replace(re, (_, pre, w) => e.url
          ? `${pre}<a href="${e.url}" data-card="${id}">${w}</a>` : `${pre}<abbr data-card="${id}" tabindex="0">${w}</abbr>`);
      }
    }
    return parts.join("");
  }
}

// Port of site_hook.mark_analysis: box whole "Analysis:" paragraphs, tag inline ones
function markAnalysis(text) {
  const blocks = [];
  let cur = [];
  for (const line of text.split("\n")) {
    const starts = /^(\s*)(- |\d+\. |\||#|>)/.test(line) && !line.startsWith("  ");
    if (!line.trim() || (starts && cur.length)) {
      if (cur.length) blocks.push(cur.join("\n"));
      cur = [];
      if (!line.trim()) { blocks.push(line); continue; }
    }
    cur.push(line);
  }
  if (cur.length) blocks.push(cur.join("\n"));
  return blocks.map((b) => {
    if (b.startsWith("Analysis:")) {
      const body = b.slice(9).trim();
      return `<aside class="analysis"><p class="analysis-tag">Analysis: our interpretation</p>\n\n${body[0].toUpperCase() + body.slice(1)}\n\n</aside>`;
    }
    if (b.includes("Analysis:") && !/^\s*[|#]/.test(b)) {
      const i = b.indexOf("Analysis:");
      return b.slice(0, i) + '<span class="analysis"><span class="analysis-tag">Analysis</span> ' + b.slice(i + 9).trimStart() + "</span>";
    }
    return b;
  }).join("\n");
}

const table = (head, rows) => `<div class="scroll"><table><thead><tr>${head.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>${
  rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;

// ------------------------------------------------------------- build

const pages = [];

for (const f of topicFiles) {
  const e = entities[`topic:${f.slice(0, -3)}`];
  const p = new Page(`topic:${f.slice(0, -3)}`, e.url, e.title);
  p.body = p.render(read(`analysis/topics/${f}`), `topics/${f}`);
  p.sourceFile = `analysis/topics/${f}`;
  pages.push(p);
}

for (const person of people) {
  const id = `person:${person.id}`;
  const e = entities[id];
  const p = new Page(id, e.url, e.title);
  const file = `analysis/people/${person.id}.md`;
  const has = fs.existsSync(path.join(ROOT, file));
  let text = has ? read(file).replace(/^Official page: .*\n/m, "") : `# ${e.title}\n`;
  const [h1, ...rest] = text.split("\n");
  const pos = positions.filter((r) => r.actor === person.id);
  const opts = options.filter((r) => r.proposed_by.split(/[;,]\s*/).includes(person.id));
  const decisionLink = (d) => `<a href="${LIVE}decisions/#${d}">${esc(decisions[d]?.decision || d)}</a>`;
  let gen = "";
  if (pos.length) gen += `\n\n## Positions on decisions\n\n` + table(["Decision", "Date", "Position", "Source"],
    pos.map((r) => [decisionLink(r.decision), esc(r.date), esc(r.stance), r.source]));
  if (opts.length) gen += `\n\n## Options proposed\n\n` + table(["Decision", "Date", "Option", "Source"],
    opts.map((r) => [decisionLink(r.decision), esc(r.proposed_on), esc(r.option), r.source]));
  p.body = p.render([h1, "", "<!--infobox-->", ...rest].join("\n") + (has ? "" : "\n\n*No profile written yet. This page is built from the archive's data.*") + gen, `people/${person.id}.md`);
  const r = person;
  p.infobox = [["Office", r.office + (r.district ? `, District ${r.district}` : "")], ["Party", r.party], ["Area", r.area],
    ["Role 2025-26", r.role_2025_26], ["Role 2027", r.role_2027],
    ["Official page", r.official_page && `<a href="${esc(r.official_page)}">${esc(r.official_page.replace(/^https?:\/\/(www\.)?/, ""))}</a>`]]
    .filter(([, v]) => v).map(([k, v]) => `<dt>${k}</dt><dd>${k === "Official page" ? v : esc(v)}</dd>`).join("");
  p.infoboxCites = p.render(r.source, "people/people.csv").replace(/^<p>|<\/p>\n?$/g, "");
  p.sourceFile = has ? file : "analysis/people/people.csv";
  p.stub = !has;
  pages.push(p);
}

const who = new Page("who", "/who-decides/", "Who decides");
who.body = who.render(`# Who decides

The Governor proposes a budget; the Legislature's Ways and Means committee writes the final one. These are the
people with a role in a decision this archive tracks.`, "who-decides.md") + table(["Name", "Office", "Area", "Role 2025-26", "Role 2027"],
  people.map((r) => [`<a href="/people/${r.id}/" data-card="person:${r.id}">${esc(r.name)}</a>`, esc([r.office, r.district && `District ${r.district}`, r.party && `(${r.party})`].filter(Boolean).join(" ")),
    esc(r.area), esc(r.role_2025_26), esc(r.role_2027)]));
people.forEach((r) => { who.refs.add(`person:${r.id}`); who.card(`person:${r.id}`, entities[`person:${r.id}`]); });
who.sourceFile = "analysis/people/people.csv";
pages.push(who);

// Backlinks: every page that links to or first-mentions an entity
const byId = Object.fromEntries(pages.map((p) => [p.id, p]));
for (const p of pages) p.backlinks = [];
for (const p of pages) for (const id of p.refs) if (byId[id] && id !== p.id) byId[id].backlinks.push(p);

for (const p of pages) {
  p.html = p.body.replace("<!--infobox-->", p.infobox ? `<aside class="infobox"><dl>${p.infobox}</dl><p class="infobox-src">${p.infoboxCites}</p></aside>` : "");
  if (p.backlinks.length)
    p.html += `<section class="backlinks"><h2>Mentioned on</h2><ul>${p.backlinks.sort((a, b) => a.title.localeCompare(b.title))
      .map((b) => `<li><a href="${b.url}" data-card="${b.id}">${esc(b.title)}</a></li>`).join("")}</ul></section>`;
  for (const b of p.backlinks) p.card(b.id, entities[b.id] || { kind: "Page", title: b.title, url: b.url, lines: [] });
  p.html += `<p class="page-meta">Source on GitHub: <a href="${BLOB}${p.sourceFile}"><code>${p.sourceFile}</code></a> · <a href="https://github.com/pietvanzoen/fund-oregon-schools/commits/main/${p.sourceFile}">history</a></p>`;
}

const nav = {
  topics: topicFiles.map((f) => entities[`topic:${f.slice(0, -3)}`]),
  people: people.map((r) => ({ ...entities[`person:${r.id}`], stub: !fs.existsSync(path.join(ROOT, `analysis/people/${r.id}.md`)) })),
};

export default {
  pages: pages.map((p) => ({ url: p.url, title: p.title, html: p.html, stub: !!p.stub,
    cards: Object.fromEntries(Object.entries(p.cards).map(([k, c]) => [k, { kind: c.kind, title: c.title, url: c.url, external: !!c.external, lines: c.lines.filter(Boolean), also: c.also }])) })),
  nav,
};
