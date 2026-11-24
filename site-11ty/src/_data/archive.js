// Builds every page of the spike from analysis/ and sources/, the same files the Python tools read.
// Output: { pages: [{url, title, html, cards}] }. Templates only wrap it in the layout.
import fs from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";
import markdownIt from "markdown-it";
import matter from "@11ty/gray-matter";
import { icon } from "../_includes/icons.js";

const ROOT = path.resolve(import.meta.dirname, "../../..");
const LIVE = "https://fundoregonschools.org/"; // pages the spike doesn't build yet link to the live site
const REPO = "https://github.com/pietvanzoen/fund-oregon-schools";
const BLOB = REPO + "/blob/main/";
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
    kind: "Person", icon: "person", title: `${TITLE[p.office] || ""} ${p.name}`.trim(), url: `/people/${p.id}/`,
    lines: [seat || p.office, p.role_2027 && `2027: ${p.role_2027}`].filter(Boolean), name: p.name, row: p,
  };
}
const topicFiles = fs.readdirSync(path.join(ROOT, "analysis/topics")).filter((f) => f.endsWith(".md")).sort();
for (const f of topicFiles) {
  const { data, content: text } = matter(read(`analysis/topics/${f}`));
  const summary = String(data.summary || "").trim();
  const h1 = (text.match(/^# (.+)$/m) || [, f])[1].trim();
  const lead = (text.split(/^## Analysis\s*$/m)[1] || text.split("\n\n")[1] || "").trim().split(/\n\s*\n/)[0];
  entities[`topic:${f.slice(0, -3)}`] = { kind: "Topic", icon: "topic", title: h1, url: `/${f.slice(0, -3)}/`, lines: [summary || clip(plain(lead))], summary, text };
}
for (const g of glossary)
  entities[`term:${g.term}`] = { kind: "Abbreviation", icon: "abbr", title: g.full_name || g.term, url: null, lines: [g.tooltip], term: g.term };

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
      also: { label: "Archived copy", url: BLOB + "sources/" + p }, icon: "doc", chip: `${shortTitle(s.title || path.basename(p))}${page ? `, p.${page}` : ""}`, cls: "src" };
  }
  if (kind === "NEWS") {
    const r = news[body] || {};
    return { kind: "News report", title: r.title || body, url: r.url, external: true, lines: [[r.outlet, r.date].filter(Boolean).join(", ")],
      icon: "news", chip: `${(r.outlet || "news").split("/")[0]}`, cls: "news" };
  }
  if (kind === "DER") {
    const r = derived[body] || {};
    const est = r.kind === "est";
    return { kind: est ? "Our estimate" : "Our calculation", title: r.label || body, external: true,
      url: BLOB + "analysis/derived/" + body.split("/")[0] + ".csv", lines: [r.method && `Method: ${r.method}`, r.assumptions && `Assumes: ${r.assumptions}`].filter(Boolean),
      icon: "calc", chip: est ? "our estimate" : "our sum", cls: "der" };
  }
  if (kind === "PPSARCH")
    return { kind: "Other archive", title: "Portland Public Schools research archive", url: "https://github.com/timaelliott/save-our-schools", external: true, lines: [body], icon: "archive", chip: "PPS archive", cls: "pps" };
  const [, ts] = body.split("@");
  return { kind: "Recording", title: path.basename(body.split("@")[0]), url: null, lines: [ts ? `At ${ts}` : ""], icon: "video", chip: `Recording${ts ? `, ${ts}` : ""}`, cls: "vid" };
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
// Files whose page the spike doesn't build: [link text, where it goes]; names follow site_hook.PAGE_TITLES
const LINKS = {
  "decisions.md": ["what's being decided", LIVE + "decisions/"], "decisions.csv": ["what's being decided", LIVE + "decisions/"],
  "positions.csv": ["what's being decided", LIVE + "decisions/"], "timeline.md": ["timeline", LIVE + "timeline/"],
  "START.md": ["start here", "/"], "promises.csv": ["promises tracker", LIVE + "promises/"],
  "people/quotes_all.jsonl": ["what they've said", LIVE + "quotes/"], "questions.csv": ["questions", LIVE + "questions/"],
  "people/people.csv": ["who decides", "/who-decides/"], "updates.csv": ["what's new", LIVE + "updates/"],
  "about.md": ["about this site", LIVE + "about/"],
};

class Page {
  constructor(id, url, title) { Object.assign(this, { id, url, title, refs: new Set(), cards: {} }); }

  card(id, data) { this.cards[id] = data; return id; }

  // Markdown with our conventions -> HTML
  render(text, srcFile) {
    text = text.replace(/`([\w./-]+\.(?:md|csv|jsonl))(#[\w-]+)?`/g, (m, ref, anchor = "") => {
      const key = path.posix.normalize(path.posix.join(path.posix.dirname(srcFile), ref));
      const ent = FILE_ENTITY[key] || FILE_ENTITY[ref];
      if (ent) return `[${entities[ent].title}](${entities[ent].url}${anchor})`;
      const link = LINKS[key] || LINKS[ref];
      return link ? `[${link[0]}](${link[1]}${anchor})` : m;
    });
    // Plain Markdown links to those files, e.g. [About this site](about.md)
    text = text.replace(/\]\(([\w./-]+\.md)(#[\w-]+)?\)/g, (m, ref, anchor = "") => (LINKS[ref] ? `](${LINKS[ref][1]}${anchor})` : m));
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
      const [first, ...more] = c.chip.split(" "); // the icon stays on the line with the first word
      const chip = `<span class="nw">${icon(c.icon)}${esc(first)}</span>${more.length ? " " + esc(more.join(" ")) : ""}`;
      return c.url ? `<a ${attrs} href="${esc(c.url)}" target="_blank" rel="noopener">${chip}</a>` : `<span ${attrs} tabindex="0">${chip}</span>`;
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
      return `<aside class="analysis">\n\n**We think:** ${body}\n\n</aside>`;
    }
    if (b.includes("Analysis:") && !/^\s*[|#]/.test(b)) {
      const i = b.indexOf("Analysis:");
      return b.slice(0, i) + '<span class="analysis"><strong>We think:</strong> ' + b.slice(i + 9).trimStart() + "</span>";
    }
    return b;
  }).join("\n");
}

const table = (head, rows) => `<table><thead><tr>${head.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>${
  rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table>`;

// Derived figures as number tiles when there are at most 4 rows with short values; otherwise the table stays
function numberTiles(text) {
  return text.replace(/(^## Derived figures\s*\n)([\s\S]*?)(?=^## |(?![\s\S]))/m, (all, h, sec) => {
    const lines = sec.split("\n").filter((l) => l.startsWith("|"));
    if (lines.length < 3) return all;
    const cells = (l) => l.replace(/^\||\|\s*$/g, "").split("|").map((c) => c.trim());
    const head = cells(lines[0]).map((c) => c.toLowerCase());
    const rows = lines.slice(2).map(cells);
    const v = head.indexOf("value");
    const tag = (r) => r.find((c) => c.includes("[DER:"));
    if (v < 1 || rows.length > 4 || rows.some((r) => !r[v] || r[v].length > 16 || !tag(r))) return all;
    const tiles = rows.map((r) => `<li class="tile"><span class="tile-value">${esc(r[v])}</span><span class="vh">: </span><span class="tile-label">${md.renderInline(r[0])}</span> ${tag(r)}</li>`);
    const table = sec.slice(sec.indexOf(lines[0]), sec.indexOf(lines.at(-1)) + lines.at(-1).length);
    return h + sec.replace(table, `<ul class="tiles">${tiles.join("")}</ul>`);
  });
}

// The topic file's sections as cards; ids stay the same, headings say what each one is
const SECTIONS = {
  analysis: ["box-analysis", "think", "What we think this means", "Our interpretation, not a source"],
  "what-the-sources-say": ["box-docs", "doc", "What the documents say"],
  "derived-figures": ["box-numbers", "calc", "Numbers we worked out"],
};

const PARTY = { D: "Democrat", R: "Republican", I: "Independent" };

const pages = [];

for (const f of topicFiles) {
  const e = entities[`topic:${f.slice(0, -3)}`];
  const p = new Page(`topic:${f.slice(0, -3)}`, e.url, e.title);
  p.body = p.render(numberTiles(e.text), `topics/${f}`);
  p.summary = e.summary;
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
  p.body = p.render([h1, "", "<!--summary-->", ...rest].join("\n") + (has ? "" : `\n\n<p class="box no-profile">We haven't written about this person yet. Here's their role and the pages that mention them.</p>`) + gen, `people/${person.id}.md`);
  // People get a factual card from people.csv, never a prose summary
  const r = person;
  const office = [r.office + (r.district ? `, District ${r.district}` : ""), PARTY[r.party] || r.party].filter(Boolean).join(" · ");
  const cites = p.render(r.source, "people/people.csv").replace(/^<p>|<\/p>\n?$/g, "");
  p.personCard = `<section class="box person-card" aria-label="Office and role"><p class="pc-office">${esc(office)}</p>${r.area ? `<p>${esc(r.area)}</p>` : ""}`
    + (r.role_2027 ? `<p><span class="year">2027</span><span class="vh">: </span> ${esc(r.role_2027)}</p>` : "")
    + `<p class="pc-more">${[r.role_2025_26 && `2025-26: ${esc(r.role_2025_26)}`, r.official_page && `<a href="${esc(r.official_page)}">Official page</a>`].filter(Boolean).join(" · ")}</p>`
    + `<p class="pc-src">Sources: ${cites}</p></section>`;
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

// Topics: the list the old placeholder home page held, now its own page
const topicsPage = new Page("topics", "/topics/", "Topics");
topicsPage.body = `<ul class="topic-list box">${topicFiles.map((f) => {
  const e = entities[`topic:${f.slice(0, -3)}`];
  topicsPage.card(`topic:${f.slice(0, -3)}`, e);
  return `<li><a class="list-link" href="${e.url}" data-card="topic:${f.slice(0, -3)}">${esc(e.title)}</a><p>${esc(e.lines[0])}</p></li>`;
}).join("")}</ul>`;
topicsPage.sourceFile = "analysis/topics";
pages.push(topicsPage);

// Backlinks: every page that links to or first-mentions an entity
const byId = Object.fromEntries(pages.map((p) => [p.id, p]));
for (const p of pages) p.backlinks = [];
for (const p of pages) for (const id of p.refs) if (byId[id] && id !== p.id) byId[id].backlinks.push(p);

for (const p of pages) {
  // The layout draws the title, so the Markdown H1 goes; the person card takes the placeholder
  p.html = p.body.replace(/^\s*<h1>[\s\S]*?<\/h1>\s*/, "").replace(/(<p>)?<!--summary-->(<\/p>)?/, p.personCard || "");
  // Wide tables scroll inside their own region, which takes keyboard focus, never the page
  p.html = p.html.replace(/<table>[\s\S]*?<\/table>/g, (t) => `<div class="scroll" tabindex="0" role="region" aria-label="Table">${t}</div>`);
  const slugs = new Set(["in-short"]);
  const heads = p.summary ? [["in-short", "In short"]] : [];
  p.html = p.html.replace(/<h2>([\s\S]*?)<\/h2>/g, (_, inner) => {
    let id = inner.replace(/<[^>]+>/g, "").toLowerCase().replace(/&[^;]+;/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    while (slugs.has(id)) id += "-2";
    slugs.add(id); heads.push([id, SECTIONS[id]?.[2] || inner.replace(/<[^>]+>/g, "")]);
    return `<h2 id="${id}">${inner}</h2>`;
  });
  if (p.id.startsWith("topic:")) {
    // The paragraph before the first section is a note for maintainers (decision, open issues, data files): it goes to the foot
    const i = p.html.indexOf("<h2 ");
    p.note = p.html.slice(0, i).trim().replace(/(^|[\s(])#(\d+)\b/g, `$1<a href="${REPO}/issues/$2">#$2</a>`);
    p.html = p.html.slice(i);
    // Each h2 and what follows it becomes one card
    p.html = p.html.replace(/<h2 id="([^"]+)">([\s\S]*?)<\/h2>([\s\S]*?)(?=<h2 id=|$)/g, (_, id, inner, rest) => {
      const [cls, ic, label, note] = SECTIONS[id] || ["box-plain", "", inner];
      const sub = note || (id === "derived-figures" && rest.includes("cite-der") ? "Our own calculations. Each one links to its method." : "");
      return `<section class="box ${cls}" aria-labelledby="${id}"><h2 id="${id}">${ic ? icon(ic, "i h-icon") : ""}${label}</h2>${sub ? `<p class="box-note">${sub}</p>` : ""}${rest}</section>`;
    });
    if (p.summary) p.html = `<section class="box box-short" aria-labelledby="in-short"><h2 id="in-short">In short</h2><p>${esc(p.summary)}</p></section>` + p.html;
  }
  p.aside = "";
  if (p.id.startsWith("topic:") && heads.length > 1)
    p.aside += `<nav class="box side-box side-top" aria-labelledby="otp"><h2 class="side-title" id="otp">On this page</h2><ul class="side-list">${heads.map(([id, t]) => `<li><a href="#${id}">${esc(t)}</a></li>`).join("")}</ul></nav>`;
  if (p.backlinks.length)
    p.aside += `<section class="box side-box" aria-labelledby="rel"><h2 class="side-title" id="rel">Related pages</h2><ul class="side-list">${p.backlinks.sort((a, b) => a.title.localeCompare(b.title))
      .map((b) => `<li><a href="${b.url}" data-card="${b.id}">${esc(b.title)}</a></li>`).join("")}</ul></section>`;
  for (const b of p.backlinks) p.card(b.id, entities[b.id] || { kind: "Page", icon: "topic", title: b.title, url: b.url, lines: [] });
  p.meta = `${p.note || ""}<p>Source on GitHub: <a href="${BLOB}${p.sourceFile}"><code>${p.sourceFile}</code></a> · <a href="${REPO}/commits/main/${p.sourceFile}">history</a></p>`;
  p.back = p.id.startsWith("person:") ? ["Who decides", "/who-decides/"] : null;
}

// ------------------------------------------------------------- home page, from analysis/START.md

const AP_MONTH = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."];
const apDate = (iso, end) => { const [y, m, d] = iso.split("-").map(Number); return `${AP_MONTH[m - 1]} ${d}${end ? `-${Number(end)}` : ""}, ${y}`; };
const WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];
const TAGLINE = "Following the money behind Oregon's schools.";
const START_ICONS = ["decide", "dollar", "scales", "target"]; // START.md's four entry points, in order

const cap = (t) => t[0].toUpperCase() + t.slice(1);
function buildHome() {
  const p = new Page("home", "/", "");
  const inline = (t) => p.render(t, "START.md").trim().replace(/^<p>([\s\S]*)<\/p>$/, "$1");
  const text = read("analysis/START.md");
  const section = (h) => (text.split(new RegExp(`^## ${h}\\s*$`, "m"))[1] || "").split(/^## /m)[0];
  const items = (block, marker) => block.split("\n").reduce((out, l) => {
    if (marker.test(l)) out.push(l.replace(marker, ""));
    else if (/^\s+\S/.test(l) && out.length) out[out.length - 1] += " " + l.trim();
    return out;
  }, []);
  const [, title] = text.match(/^# (.+)$/m);
  p.title = title.trim();

  // Top band: the paragraphs between the title and the first list (the masthead already shows the tagline)
  const intro = text.split(/^# .+$/m)[1].split(/^- /m)[0].split(/\n\s*\n/).map((t) => t.trim()).filter(Boolean)
    .filter((t) => plain(t) !== TAGLINE);
  const runBy = intro.findIndex((t) => t.startsWith("Run by "));
  const hero = `<section class="hero"><div class="wrap"><h1>${esc(p.title)}</h1>`
    + intro.map((t, i) => `<p class="${i === runBy ? "run-by" : "lead"}">${inline(t)}</p>`).join("")
    + `<form class="search" role="search" action="${LIVE}" method="get"><label class="vh" for="q">Search topics, people and terms</label>`
    + `<input id="q" name="q" type="search" placeholder="Search topics, people and terms" autocomplete="off">`
    + `<button type="submit" class="search-go">${icon("search")}<span class="vh">Search</span></button></form>`
    + `<p class="search-note">Searches the current site, fundoregonschools.org, until this one has its own search.</p></div></section>`;

  // Coming up: the next dated row of timeline.md, as on the live site
  const today = new Date().toISOString().slice(0, 10);
  const next = [...read("analysis/timeline.md").matchAll(/^\| (\d{4}-\d{2}-\d{2})(?: to \d{2}-(\d{2}))? \| ([^|]+) \| ([^|]*) \|$/gm)]
    .find((m) => m[1] >= today);
  const coming = next ? `<section class="coming-up" aria-labelledby="coming-up">${icon("calendar", "i cu-icon")}<div class="cu-text">`
    + `<h2 id="coming-up">Coming up</h2><p class="cu-event"><strong>${apDate(next[1], next[2])}:</strong> ${inline(next[3].trim() + " " + next[4])}</p></div>`
    + `<p class="cu-more"><a href="${LIVE}timeline/">All dates</a></p></section>` : "";

  // Start here: START.md's four entry points as cards
  const starts = text.split(/^- /m).slice(1, 5).map((b) => b.split("\n\n")[0].replace(/\n\s+/g, " ").trim())
    .map((b, i) => {
      const [, name, desc, ref] = b.match(/^\S+\s+\*\*(.+?):\*\*\s*(.+?)\s*→\s*`([^`]+)`/);
      const ent = FILE_ENTITY[ref] && entities[FILE_ENTITY[ref]];
      const url = ent ? ent.url : LINKS[ref][1];
      if (ent) p.card(FILE_ENTITY[ref], ent);
      return `<li class="start-card"><a href="${url}"${ent ? ` data-card="${FILE_ENTITY[ref]}"` : ""}>${icon(START_ICONS[i] || "topic", "i start-icon")}${esc(name)}</a><p>${inline(cap(desc))}</p></li>`;
    });

  // Key numbers: "**Label:** $X billion" bullets as tiles, "Analysis:" as the yellow box, the rest as a list
  const keyBlock = section("Key numbers for 2027-29");
  const tiles = [], rest = [];
  let analysis = "";
  for (const it of items(keyBlock, /^- /)) {
    const t = it.match(/^\*\*(.+?):\*\*\s*\$([\d.,]+) (billion|million)([\s\S]*)$/);
    if (t) {
      // The tile keeps the figure with its own citation; later sentences (definitions) go to the list below
      const [, own, after] = t[4].match(/^([^[]*?(?:\[[A-Z]+:[^\]]+\]\s*)+)\.?\s*([\s\S]*)$/) || [, t[4], ""];
      tiles.push(`<li class="kn-tile"><p class="kn-label">${esc(t[1])}</p><p class="kn-fig"><span class="kn-num">$${t[2]}</span> <span class="kn-unit">${t[3]}</span></p><p class="kn-rest">${inline(own.replace(/^[,.]?\s*/, ""))}</p></li>`);
      if (after.trim()) rest.push(`<li>${inline(after.trim())}</li>`);
    }
    else if (it.startsWith("Analysis:")) analysis = `<p class="analysis kn-think"><strong>We think:</strong> ${inline(it.slice(9).trim())}</p>`;
    else rest.push(`<li>${inline(it)}</li>`);
  }
  const more = (keyBlock.match(/^More: (.+)$/m) || [])[1];
  const numbers = `<section class="home-sec" aria-labelledby="key-numbers"><h2 id="key-numbers">Key numbers for 2027-29</h2>`
    + `<p class="sec-note">Each figure is from the document in its pill.</p><ul class="kn-tiles">${tiles.join("")}</ul>${analysis}`
    + (keyBlock.includes("<!-- site: funding chart -->") ? fundingChart(inline) : "")
    + `<ul class="kn-rest-list">${rest.join("")}</ul>${more ? `<p class="sec-note">More: ${inline(more)}</p>` : ""}</section>`;

  // What's new: the latest three rows of updates.csv, newest first (same date: the later row first)
  const ups = csv("analysis/updates.csv").map((r, i) => [r, i]).sort((a, b) => (b[0].date + String(b[1]).padStart(5, "0")).localeCompare(a[0].date + String(a[1]).padStart(5, "0")))
    .slice(0, 3).map(([r]) => `<li class="box update"><p class="up-date">${apDate(r.date)}</p><p>${inline(r.text)}</p></li>`);

  // Read first: the first four, then the rest behind "All eight"
  const reads = items(section("Read first"), /^\d+\. /).map((t) => `<li>${inline(t)}</li>`);
  const n = reads.length;
  const readFirst = `<ol class="box read-first">${reads.slice(0, 4).join("")}</ol>` + (n > 4
    ? `<details class="read-more"><summary>All ${WORDS[n] || n}</summary><ol class="box read-first" start="5">${reads.slice(4).join("")}</ol></details>` : "");

  // Look things up: the Reference list
  const refs = items(section("Reference"), /^- /).map((t) => {
    const [, ref, desc] = t.match(/^`([^`]+)`:\s*(.+)$/);
    const [name, url] = LINKS[ref];
    return `<li class="look"><a href="${url}">${esc(name[0].toUpperCase() + name.slice(1))}</a><p>${inline(cap(desc))}</p></li>`;
  });

  p.html = coming
    + `<section class="home-sec" aria-labelledby="start-here"><h2 id="start-here">Start here</h2><ul class="start-cards">${starts.join("")}</ul></section>`
    + numbers
    + `<div class="home-two"><section class="home-sec" aria-labelledby="whats-new"><h2 id="whats-new">What's new</h2><ol class="updates">${ups.join("")}</ol><p class="sec-more"><a href="${LIVE}updates/">All updates</a></p></section>`
    + `<section class="home-sec" aria-labelledby="read-first"><h2 id="read-first">Read first</h2>${readFirst}</section></div>`
    + `<section class="home-sec" aria-labelledby="look-up"><h2 id="look-up">Look things up</h2><ul class="look-up">${refs.join("")}</ul></section>`;
  p.html = p.html.replace(/<table>[\s\S]*?<\/table>/g, (t) => `<div class="scroll" tabindex="0" role="region" aria-label="Table">${t}</div>`);
  p.hero = hero;
  p.meta = `<p>Source on GitHub: <a href="${BLOB}analysis/START.md"><code>analysis/START.md</code></a> · <a href="${REPO}/commits/main/analysis/START.md">history</a></p>`;
  return p;
}

// The funding chart from the live site (site_hook.funding_chart), as HTML bars
function fundingChart(inline) {
  const qem = Object.fromEntries(csv("analysis/data/qem_gap.csv").filter((r) => r.biennium === "2027-29").map((r) => [r.measure, r]));
  const adopted = csv("analysis/data/ssf_history.csv").find((r) => r.biennium === "2025-27" && r.stage === "legislatively_adopted");
  const v = (m) => Number(qem[m].amount_billion);
  const bars = [
    ["Adopted for 2025-27", Number(adopted.amount_billion), "State School Fund", "base"],
    ["Current service level", v("ssf_csl_in_report"), "State School Fund · DAS estimate", "base"],
    ["Keep 2025-27 service levels", v("status_quo_state_funding"), "QEM status quo · all core state funding", "main"],
    ["Meet the state's goals", v("full_qem_state_funding"), "Full QEM · all core state funding", "main"],
  ];
  const max = Math.max(...bars.map((b) => b[1]));
  const srcs = [...new Set([qem.status_quo_state_funding, qem.full_qem_state_funding, qem.ssf_csl_in_report].flatMap((r) => r.source.match(/\[[^\]]+\]/g)))].join(" ");
  return `<figure class="box chart"><figcaption class="chart-title">State funding for K-12, billions of dollars: 2025-27 adopted and 2027-29 estimates</figcaption><ul class="bars">`
    + bars.map(([label, val, sub, cls]) => `<li class="bar-row"><p class="bar-label"><strong>${esc(label)}</strong> <span>${esc(sub)}</span></p>`
      + `<p class="bar"><span class="bar-fill bar-${cls}" style="width:calc((100% - 8.5em) * ${(val / max).toFixed(3)})"></span><span class="bar-val">$${val.toFixed(2)} billion</span></p></li>`).join("")
    + `</ul><p class="chart-src">2027-29 figures: 2026 Quality Education Model report ${inline(srcs)}. 2025-27: ${inline(adopted.source)}</p></figure>`;
}

const home = buildHome();

const nav = {
  topics: topicFiles.map((f) => entities[`topic:${f.slice(0, -3)}`]),
  people: people.map((r) => ({ ...entities[`person:${r.id}`], stub: !fs.existsSync(path.join(ROOT, `analysis/people/${r.id}.md`)) })),
};

export default {
  pages: pages.map((p) => ({ url: p.url, title: p.title, html: p.html, aside: p.aside, meta: p.meta, back: p.back, description: p.summary || "", stub: !!p.stub,
    cards: Object.fromEntries(Object.entries(p.cards).map(([k, c]) => [k, { kind: c.kind, icon: c.icon, title: c.title, url: c.url, external: !!c.external, lines: c.lines.filter(Boolean), also: c.also }])) })),
  nav: { topics: nav.topics.map(({ text, ...t }) => t), people: nav.people },
  home: { title: home.title, hero: home.hero, html: home.html, meta: home.meta,
    cards: Object.fromEntries(Object.entries(home.cards).map(([k, c]) => [k, { kind: c.kind, icon: c.icon, title: c.title, url: c.url, external: !!c.external, lines: c.lines.filter(Boolean), also: c.also }])) },
};
