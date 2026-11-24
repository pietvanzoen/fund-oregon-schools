import fs from "node:fs";
import path from "node:path";
import * as pagefind from "pagefind";

// PREVIEW=1 writes relative links (dir/index.html) so the build works from any folder, e.g. a hosted preview
const PREVIEW = process.env.PREVIEW === "1";

export default function (cfg) {
  cfg.addPassthroughCopy("src/assets");
  cfg.addPassthroughCopy("src/CNAME"); // records the domain; an Actions deploy takes it from the repo's Pages settings

  if (PREVIEW)
    cfg.addTransform("relative-links", function (html) {
      if (!this.page.outputPath?.endsWith(".html")) return html;
      const depth = this.page.url.replace(/[^/]*$/, "").split("/").filter(Boolean).length; // a file URL (/404.html) sits at its folder's depth
      const up = "../".repeat(depth) || "./";
      return html.replace(/(href|src|action)="\/(?!\/)([^"#]*)(#[^"]*)?"/g, (_, attr, p, hash = "") =>
        `${attr}="${up}${p}${p === "" || p.endsWith("/") ? "index.html" : ""}${hash}"`);
    });

  // Fail the build on any internal link with no page behind it
  cfg.on("eleventy.after", async ({ dir }) => {
    const out = dir.output;
    const broken = [];
    const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).forEach((f) => {
      const p = path.join(d, f.name);
      if (f.isDirectory()) return walk(p);
      if (!p.endsWith(".html")) return;
      for (const [, href] of fs.readFileSync(p, "utf8").matchAll(/href="([^"#]+)/g)) {
        if (/^(https?:|mailto:|\/\/)/.test(href)) continue;
        const target = href.startsWith("/") ? path.join(out, href) : path.join(path.dirname(p), href);
        const file = /\.\w+$/.test(target) ? target : path.join(target, "index.html");
        if (!fs.existsSync(file)) broken.push(`${path.relative(out, p)} -> ${href}`);
      }
    });
    walk(out);
    if (broken.length) throw new Error(`Broken internal links:\n  ${broken.join("\n  ")}`);

    // Search results show the title and description; every indexable page needs its own (CLAUDE.md rule 4)
    const bare = [], seen = {};
    const walkMeta = (d) => fs.readdirSync(d, { withFileTypes: true }).forEach((f) => {
      const p = path.join(d, f.name);
      if (f.isDirectory()) return walkMeta(p);
      if (!p.endsWith(".html")) return;
      const html = fs.readFileSync(p, "utf8");
      if (html.includes('name="robots" content="noindex"')) return;
      const page = path.relative(out, p);
      const desc = html.match(/<meta name="description" content="([^"]*)"/)?.[1];
      if (!desc) bare.push(page);
      for (const v of [html.match(/<title>([^<]*)<\/title>/)?.[1], desc].filter(Boolean)) (seen[v] ||= []).push(page);
    });
    walkMeta(out);
    const dupes = Object.entries(seen).filter(([, ps]) => ps.length > 1).map(([v, ps]) => `"${v}": ${ps.join(", ")}`);
    if (bare.length || dupes.length) throw new Error([
      bare.length && `Pages with no meta description:\n  ${bare.join("\n  ")}`,
      dupes.length && `Titles or descriptions used on more than one page:\n  ${dupes.join("\n  ")}`,
    ].filter(Boolean).join("\n"));

    // Search index: Pagefind reads the built pages marked data-pagefind-body (topics, people, terms)
    const { index, errors } = await pagefind.createIndex();
    if (errors.length) throw new Error(`Pagefind: ${errors.join("; ")}`);
    const added = await index.addDirectory({ path: out });
    if (added.errors.length || !added.page_count) throw new Error(`Pagefind indexed ${added.page_count} pages: ${added.errors.join("; ")}`);
    const written = await index.writeFiles({ outputPath: path.join(out, "pagefind") });
    if (written.errors.length) throw new Error(`Pagefind: ${written.errors.join("; ")}`);
    await pagefind.close();
    // The site builds its own results UI, so Pagefind's bundled UIs aren't shipped
    for (const f of fs.readdirSync(path.join(out, "pagefind"))) if (/-ui\.(css|js)$/.test(f)) fs.rmSync(path.join(out, "pagefind", f));
    // shortcut: the hosted preview serves only a fixed list of file types, so PREVIEW renames Pagefind's data files to
    // .wasm (served as bytes) and patches the paths in its scripts; drop this if the preview moves to a plain web host
    if (PREVIEW) {
      const pf = path.join(out, "pagefind");
      const walkPf = (d) => fs.readdirSync(d, { withFileTypes: true }).forEach((f) => {
        const p = path.join(d, f.name);
        if (f.isDirectory()) return walkPf(p);
        if (/\.(pf_\w+|pagefind)$/.test(f.name)) fs.renameSync(p, p + ".wasm");
        else if (/^pagefind(-worker)?\.js$/.test(f.name)) {
          const js = fs.readFileSync(p, "utf8");
          const patched = js.replace(/\.(pf_meta|pf_index|pf_filter|pf_fragment|pagefind)`/g, ".$1.wasm`");
          if (patched === js) throw new Error(`PREVIEW: no Pagefind paths to patch in ${f.name}`);
          fs.writeFileSync(p, patched);
        }
      });
      walkPf(pf);
    }
    console.log(`[pagefind] indexed ${added.page_count} pages`);
  });

  return { dir: { input: "src", output: "_site" } };
}
