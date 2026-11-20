#!/usr/bin/env python3
"""Print a Markdown file with citation tags turned into links (the tag text is kept).

    python3 tools/linkify.py analysis/BRIEFING.md            # to stdout
    python3 tools/linkify.py analysis/BRIEFING.md --repo     # link SRC to the archived copy on GitHub instead

SRC → the original URL from the manifest (or the queue, if not fetched yet), with #page=N for PDFs.
NEWS → the article URL. PPSARCH → the PPS archive on GitHub. VID → URL from the manifest plus #t=seconds.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import NEWS_INDEX, TAG_RE, manifest_by_path, parse_src, read_jsonl, read_queue  # noqa: E402

REPO = "https://github.com/pietvanzoen/fund-oregon-schools/blob/main/sources/"
PPSARCH = "https://github.com/timaelliott/save-our-schools"


def urls():
    u = {r["path"].strip(): r["url"].strip() for r in read_queue()}
    u.update({p: r.get("final_url") or r["url"] for p, r in manifest_by_path().items()})
    return u


def secs(t):
    s = 0
    for part in t.split(":"):
        s = s * 60 + int(part)
    return s


def link_for(kind, body, src_urls, news, repo):
    if kind == "SRC":
        path, page = parse_src(body)
        base = (REPO + path) if repo else src_urls.get(path)
        if not base:
            return None
        return base + (f"#page={page}" if page and path.lower().endswith(".pdf") else "")
    if kind == "VID":
        path, _, ts = body.partition("@")
        match = [u for p, u in src_urls.items() if os.path.splitext(p)[0] == path.strip()]
        return (match[0] + (f"#t={secs(ts)}" if ts else "")) if match else None
    if kind == "NEWS":
        return news.get(body.strip())
    if kind == "PPSARCH":
        return PPSARCH
    return None


def linkify(text, repo=False):
    src_urls = urls()
    news = {r["id"]: r.get("url") for r in read_jsonl(NEWS_INDEX)}

    def sub(m):
        url = link_for(m.group(1), m.group(2), src_urls, news, repo)
        return f"[{m.group(0)[1:-1]}]({url})" if url else m.group(0)

    return TAG_RE.sub(sub, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--repo", action="store_true")
    a = ap.parse_args()
    print(linkify(open(a.file, encoding="utf-8").read(), a.repo), end="")


if __name__ == "__main__":
    main()
