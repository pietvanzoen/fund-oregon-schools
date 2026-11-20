"""MkDocs hook that builds the public website from analysis/ and sources/.

Nothing in website/ duplicates the research: every page except About is generated here at build time from the
same files Claude and the citation checker use. Citation tags become small links to the source:
  [SRC:...]     -> "📄 p.N"  state or legislative document (original URL, opened at the cited page)
  [NEWS:...]    -> "📰 Outlet" news report
  [PPSARCH:...] -> "🏫 PPS archive"
  [VID:...]     -> "🎥 H:MM:SS"
"Analysis:" passages are boxed or tagged so readers can tell interpretation from documented fact.

Preview locally:  pip install "mkdocs>=1.6,<2" "mkdocs-material>=9.7,<10" && mkdocs serve
"""
import csv
import html
import os
import posixpath
import re
import subprocess
import sys

from mkdocs.structure.files import File

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    ANALYSIS, MANIFEST, NEWS_INDEX, QUOTES, ROOT, TAG_RE, manifest_by_path, parse_src, read_jsonl, read_queue,
)
from linkify import link_for, urls  # noqa: E402

GITHUB = "https://github.com/pietvanzoen/fund-oregon-schools"
BLOB = GITHUB + "/blob/main/"

# Generated page -> analysis file it comes from (None = built from data files)
MD_PAGES = {
    "index.md": "BRIEFING.md",
    "timeline.md": "timeline.md",
    "reserves.md": "topics/reserves.md",
}
PEOPLE = ["kotek", "lieber", "sanchez", "ruiz", "sollman"]
for _slug in PEOPLE:
    MD_PAGES[f"people/{_slug}.md"] = f"people/{_slug}.md"

# Backticked file names in analysis/ -> site page, so "see `people/kotek.md`" becomes a link
FILE_TO_PAGE = {v: k for k, v in MD_PAGES.items()}
FILE_TO_PAGE.update({
    "promises.csv": "promises.md",
    "people/quotes_all.jsonl": "said.md",
    "people/legislators.csv": "who-decides.md",
    "data/qem_gap.csv": "numbers.md",
    "data/ssf_history.csv": "numbers.md",
    "data/reserves.csv": "numbers.md",
})

SECTION_NAMES = {
    "gov": "Governor's office",
    "legislature": "Oregon Legislature",
    "ode": "Oregon Department of Education and Quality Education Commission",
    "fiscal": "State fiscal and economic offices",
    "districts": "School districts",
    "orgs": "Advocacy groups and associations",
}


# ---------------------------------------------------------------- helpers

class Ctx:
    def __init__(self):
        self.src_urls = urls()
        self.news = {r["id"]: r for r in read_jsonl(NEWS_INDEX)}
        self.news_urls = {k: v.get("url") for k, v in self.news.items()}
        self.titles = {r["path"].strip(): r.get("title", "").strip() for r in read_queue()}
        self.manifest = manifest_by_path()


def esc(s):
    return html.escape(s or "", quote=True)


def cell(s):
    """Safe for a Markdown table cell."""
    return (s or "").replace("|", "\\|").replace("\n", " ")


def git_date(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=ROOT,
                             capture_output=True, text=True, timeout=10).stdout.strip()
        return out or None
    except Exception:
        return None


def chip(kind, body, ctx):
    url = link_for(kind, body, ctx.src_urls, ctx.news_urls, False)
    if kind == "SRC":
        path, page = parse_src(body)
        if not url:  # not in manifest or queue: fall back to the archived copy
            url = BLOB + "sources/" + path
        title = ctx.titles.get(path) or os.path.basename(path)
        tip = title + (f", page {page}" if page else "")
        label = f"📄 p.{page}" if page else "📄 doc"
        cls = "src"
    elif kind == "NEWS":
        rec = ctx.news.get(body.strip(), {})
        outlet = rec.get("outlet") or "news"
        tip = f"{outlet}: {rec.get('title', '')} ({rec.get('date', '')})".strip()
        label = f"📰 {outlet.split('/')[0]}"
        cls = "news"
    elif kind == "PPSARCH":
        tip = f"Portland Public Schools research archive ({body.strip()})"
        label = "🏫 PPS archive"
        cls = "pps"
    else:  # VID
        _, _, ts = body.partition("@")
        tip = "Recording" + (f" at {ts}" if ts else "")
        label = f"🎥 {ts or 'video'}"
        cls = "vid"
    if not url:
        return f'<span class="cite cite-{cls}" title="{esc(tip)}">{esc(label)}</span>'
    return (f'<a class="cite cite-{cls}" href="{esc(url)}" title="{esc(tip)}" '
            f'target="_blank" rel="noopener">{esc(label)}</a>')


def dedupe(tags):
    seen = []
    for t in re.findall(r"\[[A-Z]+:[^\]]+\]", tags):
        if t not in seen:
            seen.append(t)
    return " ".join(seen)


def cites(text, ctx):
    return TAG_RE.sub(lambda m: chip(m.group(1), m.group(2), ctx), text or "")


def page_link(target, from_page):
    return posixpath.relpath(target, posixpath.dirname(from_page) or ".")


def file_refs(text, from_page, src_file):
    """`people/kotek.md` -> [Kotek page](people/kotek.md). Resolves relative to the analysis file."""
    base = posixpath.dirname(src_file)

    def sub(m):
        ref = m.group(1)
        key = posixpath.normpath(posixpath.join(base, ref))
        target = FILE_TO_PAGE.get(key) or FILE_TO_PAGE.get(ref)
        if not target:
            return m.group(0)
        return f"[{PAGE_TITLES.get(target, ref)}]({page_link(target, from_page)})"

    return re.sub(r"`([\w./-]+\.(?:md|csv|jsonl))`", sub, text)


PAGE_TITLES = {
    "index.md": "the briefing", "timeline.md": "timeline", "reserves.md": "reserves",
    "promises.md": "promises tracker", "said.md": "what they've said", "who-decides.md": "who decides",
    "numbers.md": "the numbers", "people/kotek.md": "Kotek", "people/lieber.md": "Lieber",
    "people/sanchez.md": "Sanchez", "people/ruiz.md": "Ruiz", "people/sollman.md": "Sollman",
}


# ------------------------------------------------------- Analysis: passages

BLOCK_START = re.compile(r"^(\s*)(- |\d+\. |\||#|>)")


def mark_analysis(md):
    """Box whole 'Analysis:' paragraphs; tag 'Analysis:' passages inside list items and paragraphs."""
    lines = md.split("\n")
    blocks, cur = [], []
    for line in lines:
        starts = bool(BLOCK_START.match(line)) and not line.startswith("  ")
        if not line.strip() or (starts and cur):
            if cur:
                blocks.append(cur)
            cur = []
            if not line.strip():
                blocks.append([line])
                continue
        cur.append(line)
    if cur:
        blocks.append(cur)

    out = []
    for b in blocks:
        text = "\n".join(b)
        if text.startswith("Analysis:"):
            body = text[len("Analysis:"):].strip()
            body = body[0].upper() + body[1:] if body else body
            out.append('!!! analysis "Analysis: our interpretation"\n' +
                       "\n".join("    " + ln for ln in body.split("\n")))
        elif "Analysis:" in text and not text.lstrip().startswith(("|", "#")):
            i = text.index("Analysis:")
            out.append(text[:i] + '<span class="analysis"><span class="analysis-tag">Analysis</span> ' +
                       text[i + len("Analysis:"):].lstrip() + "</span>")
        else:
            out.append(text)
    return "\n".join(out)


# ---------------------------------------------------------------- pages

def footer(sources, ctx_date_paths):
    dates = [d for d in (git_date(p) for p in ctx_date_paths) if d]
    links = " · ".join(f'<a href="{BLOB}{s}"><code>{s}</code></a>' for s in sources)
    upd = f"Last updated {max(dates)} · " if dates else ""
    return f'\n\n---\n<p class="page-meta">{upd}Source on GitHub: {links}</p>\n'


def from_analysis(page, src, ctx):
    md = open(os.path.join(ANALYSIS, src), encoding="utf-8").read()
    md = file_refs(md, page, src)
    md = mark_analysis(md)
    md = cites(md, ctx)
    if page == "index.md":
        md = re.sub(r"^# .*\n", "# The briefing\n" + INTRO, md, count=1)
    return md + footer([f"analysis/{src}"], [f"analysis/{src}"])


INTRO = """
!!! info "How to read this site"
    This is the research behind a parent campaign asking Gov. Tina Kotek and the 2027 Oregon Legislature to fund
    K-12 public schools in the 2027-29 budget. Every claim links to where it comes from:
    <span class="cite cite-src">📄 p.N</span> is a state or legislative document, opened at the cited page;
    <span class="cite cite-news">📰 Outlet</span> is a news report; <span class="cite cite-pps">🏫 PPS archive</span>
    is the Portland Public Schools research archive. Boxes marked **Analysis** are the campaign's interpretation,
    kept separate from what the documents say. [More about this site](about.md).

"""


def read_csv(rel):
    with open(os.path.join(ANALYSIS, rel), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def bar_chart(bars, title, note_lines=()):
    """Horizontal bars from zero, label row above each bar so text stays legible on phones.
    bars: (label, value, sublabel, css_class, tooltip)."""
    w, right, row, top = 520, 76, 62, 4
    vmax = max(v for _, v, *_ in bars)
    scale = (w - right) / vmax
    h = top + row * len(bars) + 22
    parts = [f'<figure class="chart"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">']
    for t in range(0, int(vmax) + 1, 2 if vmax > 10 else 1):  # recessive grid
        x = max(t * scale, 0.5)
        parts.append(f'<line class="grid" x1="{x:.1f}" x2="{x:.1f}" y1="{top + 20}" y2="{h - 20}"/>'
                     f'<text class="tick" x="{x:.1f}" y="{h - 4}" text-anchor="{"start" if t == 0 else "middle"}">{t}</text>')
    for i, (label, v, sub, cls, tip) in enumerate(bars):
        y = top + i * row
        by = y + 22
        bw = v * scale
        parts.append(
            f'<g class="bar {cls}" tabindex="0" data-tip="{esc(tip)}">'
            f'<rect class="hit" x="0" y="{y}" width="{w}" height="{row}"/>'
            f'<text x="0" y="{y + 15}"><tspan class="label">{esc(label)}</tspan>'
            f'<tspan class="sublabel" dx="8">{esc(sub)}</tspan></text>'
            f'<path class="mark" d="M0,{by} h{bw - 4:.1f} a4,4 0 0 1 4,4 v18 a4,4 0 0 1 -4,4 h-{bw - 4:.1f} z"/>'
            f'<text class="value" x="{bw + 8:.1f}" y="{by + 17}">${v:.2f}B</text></g>')
    parts.append(f'</svg><figcaption>{esc(title)}' +
                 "".join(f"<br>{n}" for n in note_lines) + "</figcaption></figure>")
    return "".join(parts)


def numbers_page(ctx):
    qem = {r["measure"]: r for r in read_csv("data/qem_gap.csv") if r["biennium"] == "2027-29"}
    ssf = read_csv("data/ssf_history.csv")
    res = read_csv("data/reserves.csv")

    def val(m):
        return float(qem[m]["amount_billion"])

    csl, sq, full = val("ssf_csl_in_report"), val("status_quo_state_funding"), val("full_qem_state_funding")
    src = cites(dedupe(qem["status_quo_state_funding"]["source"] + " " + qem["full_qem_state_funding"]["source"]
              + " " + qem["ssf_csl_in_report"]["source"]), ctx)
    chart1 = bar_chart([
        ("Current service level", csl, "State School Fund, no new money", "s-base",
         f"State School Fund current service level: ${csl:.2f}B"),
        ("Keep today's services", sq, f"QEM status quo · +${val('status_quo_gap_above_csl'):.2f}B", "s-main",
         f"Quality Education Model status quo: ${sq:.2f}B, ${val('status_quo_gap_above_csl'):.2f}B above the CSL"),
        ("Meet the state's goals", full, f"Full QEM · +${val('full_qem_above_csl'):.2f}B", "s-main",
         f"Full Quality Education Model: ${full:.2f}B, ${val('full_qem_above_csl'):.2f}B above the CSL"),
    ], "State funding for K-12 in 2027-29, billions of dollars",
        note_lines=[f"All three figures: 2026 Quality Education Model report. {src}"])

    hist = [r for r in ssf if r["amount_billion"] and r["stage"] in ("legislatively_adopted", "current_service_level")
            and "PPSARCH" not in r["source"]]
    chart2 = bar_chart([
        (r["biennium"], float(r["amount_billion"]),
         "adopted budget" if r["stage"] == "legislatively_adopted" else "current service level",
         "s-main" if r["stage"] == "legislatively_adopted" else "s-base",
         f"{r['biennium']} {r['stage'].replace('_', ' ')}: ${float(r['amount_billion']):.2f}B")
        for r in hist
    ], "State School Fund by two-year budget, billions of dollars",
        note_lines=["2027-29 is the no-new-money baseline, not an adopted budget. " +
                    cites(dedupe(" ".join(r["source"] for r in hist)), ctx)])

    nice = lambda s: s.replace("_", " ")  # noqa: E731
    t1 = table(["Budget", "Report", "Measure", "$B", "Note", "Source"],
               [[r["biennium"], r["report"], nice(r["measure"]), r["amount_billion"], r["note"],
                 cites(r["source"], ctx)] for r in read_csv("data/qem_gap.csv")])
    t2 = table(["Budget", "Stage", "$B", "Note", "Source"],
               [[r["biennium"], nice(r["stage"]), r["amount_billion"] or "—", r["note"], cites(r["source"], ctx)]
                for r in ssf])
    facts = "\n\n".join(
        f'!!! note "{esc(r["fund"])}: about ${r["amount_billion"].lstrip("~")}B (as of {r["as_of"]})"\n'
        f'    **To use it:** {r["conditions_to_use"]}.  \n    {r["note"]} {cites(r["source"], ctx)}'
        for r in res)

    return f"""# The numbers

The state's own Quality Education Commission prices what Oregon schools need. These charts use its 2026 report.

{chart1}

{chart2}

## Reserves

{facts}

More: [reserves](reserves.md).

## All figures

### Quality Education Model estimates

{t1}

### State School Fund history

{t2}
""" + footer(["analysis/data/qem_gap.csv", "analysis/data/ssf_history.csv", "analysis/data/reserves.csv"],
             ["analysis/data"])


def person_slug(name):
    last = name.split()[-1].lower()
    return last if last in PEOPLE else None


def said_page(ctx):
    quotes = read_jsonl(QUOTES)
    people = []
    for q in quotes:
        if q["person"] not in people:
            people.append(q["person"])
    buttons = "".join(f'<button type="button" data-person="{esc(p)}">{esc(p)}</button>' for p in people)
    cards = []
    for q in quotes:
        slug = person_slug(q["person"])
        more = f' · <a href="../people/{slug}/">More on {esc(q["person"].split()[-1])}</a>' if slug else ""
        cards.append(
            f'<div class="quote-card" data-person="{esc(q["person"])}">'
            f'<blockquote>“{esc(q["quote"])}”</blockquote>'
            f'<p class="who"><strong>{esc(q["person"])}</strong>, {esc(q.get("role", ""))} · {esc(q["date"])}</p>'
            f'<p class="context">{esc(q.get("context", ""))} {cites(q["cite"], ctx)}{more}</p></div>')
    profiles = " · ".join(f"[{PAGE_TITLES[f'people/{s}.md']}](people/{s}.md)" for s in PEOPLE)
    return f"""# What they've said

Exact words from the officials who decide school funding, each with its source. Pick a person to filter.

<div class="quote-filter" role="group" aria-label="Filter quotes by person">
<button type="button" data-person="" aria-pressed="true">Everyone</button>{buttons}</div>

<div class="quotes">{''.join(cards)}</div>

**Full profiles:** {profiles}
""" + footer(["analysis/people/quotes_all.jsonl"], ["analysis/people/quotes_all.jsonl"])


def promises_page(ctx):
    cards = []
    for r in read_csv("promises.csv"):
        money = r["money_attached"]
        no_money = re.match(r"(?i)^(no|none)\b|said no new money", money)
        badge = (f'<span class="pill pill-warn">⚠️ {esc(money)}</span>' if no_money
                 else f'<span class="pill">{esc(money)}</span>')
        cards.append(
            f'<div class="promise-card"><p class="promise">{esc(r["promise"])}</p>'
            f'<p class="who"><strong>{esc(r["who"])}</strong> · {esc(r["date"])} · {esc(r["type"])}</p>'
            f'<dl><dt>Money attached</dt><dd>{badge}</dd><dt>Status</dt><dd>{esc(r["status"])}</dd>'
            f'<dt>Source</dt><dd>{cites(r["source"], ctx)}</dd></dl></div>')
    return f"""# Promises tracker

Pledges and mandates on school outcomes and funding, and whether money came with them.

<div class="promises">{''.join(cards)}</div>
""" + footer(["analysis/promises.csv"], ["analysis/promises.csv"])


def who_page(ctx):
    rows = []
    for r in read_csv("people/legislators.csv"):
        slug = (r.get("profile") or "").replace(".md", "")
        name = f"[{r['name']}](people/{slug}.md)" if slug in PEOPLE else r["name"]
        rows.append([name, f"{r['chamber']} {r['district']} ({r['party']})", r["area"], r["role_2025_26"],
                     r["role_2027"], f"[official page]({r['official_page']})", cites(r["source"], ctx)])
    return f"""# Who decides

The Governor proposes a budget; the Legislature's Ways and Means committee writes the final one. These are the
budget-writing legislators this campaign tracks. See also [Gov. Kotek](people/kotek.md).

{table(["Legislator", "Seat", "Area", "Role 2025-26", "Role 2027", "Contact", "Source"], rows)}
""" + footer(["analysis/people/legislators.csv"], ["analysis/people/legislators.csv"])


def sources_page(ctx):
    groups = {}
    for path, rec in sorted(ctx.manifest.items()):
        groups.setdefault(path.split("/")[0], []).append((path, rec))
    out = ["# Sources", "",
           "Every document the analysis cites. **Original** opens the publisher's copy; **Archived copy** is the "
           "version saved in this repository, kept in case the original changes or disappears.", ""]
    order = list(SECTION_NAMES)
    for top, items in sorted(groups.items(), key=lambda kv: order.index(kv[0]) if kv[0] in order else 99):
        out += [f"## {SECTION_NAMES.get(top, top)}", ""]
        for path, rec in items:
            title = ctx.titles.get(path) or os.path.basename(path)
            orig = rec.get("final_url") or rec.get("url")
            out.append(f"- **{title}** · [Original]({orig}) · [Archived copy]({BLOB}sources/{path}) "
                       f'<span class="muted">{esc(path)}</span>')
        out.append("")
    out += ["## News coverage", "",
            "Summaries are written by the campaign; follow the link to read the full story.", ""]
    for r in sorted(ctx.news.values(), key=lambda r: r.get("date", ""), reverse=True):
        out.append(f"- **[{r.get('title', r['id'])}]({r.get('url', '')})** · {r.get('outlet', '')}, "
                   f"{r.get('date', '')}  \n  {r.get('summary', '')}")
    out += ["", "## Portland Public Schools archive", "",
            "Portland-specific material lives in the [PPS research archive](https://github.com/timaelliott/save-our-schools)."]
    return "\n".join(out) + footer(["sources/_manifest.jsonl", "sources/news/index.jsonl"],
                                   ["sources/_manifest.jsonl", "sources/news/index.jsonl"])


# ---------------------------------------------------------------- MkDocs hook

def on_files(files, config):
    ctx = Ctx()
    pages = {page: from_analysis(page, src, ctx) for page, src in MD_PAGES.items()}
    pages.update({
        "numbers.md": numbers_page(ctx),
        "said.md": said_page(ctx),
        "promises.md": promises_page(ctx),
        "who-decides.md": who_page(ctx),
        "sources.md": sources_page(ctx),
    })
    for uri, content in pages.items():
        files.append(File.generated(config, uri, content=content))
    return files
