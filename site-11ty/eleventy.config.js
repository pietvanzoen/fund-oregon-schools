import fs from "node:fs";
import path from "node:path";

// PREVIEW=1 writes relative links (dir/index.html) so the build works from any folder, e.g. a hosted preview
const PREVIEW = process.env.PREVIEW === "1";

export default function (cfg) {
  cfg.addPassthroughCopy("src/assets");

  if (PREVIEW)
    cfg.addTransform("relative-links", function (html) {
      if (!this.page.outputPath?.endsWith(".html")) return html;
      const depth = this.page.url.split("/").filter(Boolean).length;
      const up = "../".repeat(depth) || "./";
      return html.replace(/(href|src)="\/(?!\/)([^"#]*)(#[^"]*)?"/g, (_, attr, p, hash = "") =>
        `${attr}="${up}${p}${p === "" || p.endsWith("/") ? "index.html" : ""}${hash}"`);
    });

  // Stands in for mkdocs build --strict: fail the build on any internal link with no page behind it
  cfg.on("eleventy.after", ({ dir }) => {
    const out = dir.output;
    const broken = [];
    const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).forEach((f) => {
      const p = path.join(d, f.name);
      if (f.isDirectory()) return walk(p);
      if (!p.endsWith(".html")) return;
      for (const [, href] of fs.readFileSync(p, "utf8").matchAll(/href="([^"#]+)/g)) {
        if (/^(https?:|mailto:|\/\/)/.test(href)) continue;
        const target = href.startsWith("/") ? path.join(out, href) : path.join(path.dirname(p), href);
        const file = target.endsWith(".html") || target.endsWith(".css") ? target : path.join(target, "index.html");
        if (!fs.existsSync(file)) broken.push(`${path.relative(out, p)} -> ${href}`);
      }
    });
    walk(out);
    if (broken.length) throw new Error(`Broken internal links:\n  ${broken.join("\n  ")}`);
  });

  return { dir: { input: "src", output: "_site" } };
}
