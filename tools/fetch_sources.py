#!/usr/bin/env python3
"""Download queued sources into sources/, record provenance, extract text. Never overwrites.

    python3 tools/fetch_sources.py            # fetch queue rows whose file doesn't exist yet
    python3 tools/fetch_sources.py --refresh  # also re-fetch existing files; changed ones keep the old copy in _prior/
    python3 tools/fetch_sources.py --only gov/  # only rows whose path starts with this

Runs in the fetch-sources GitHub Action (cloud sandboxes usually can't reach oregon.gov / OLIS).
Needs pdftotext (poppler-utils) for PDF text; without it the PDF is still archived.
"""
import argparse
import csv
import datetime as dt
import hashlib
import html.parser
import json
import os
import shutil
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import MANIFEST, SOURCES, manifest_by_path, read_queue  # noqa: E402

UA = "Mozilla/5.0 (compatible; fund-oregon-schools-archiver; +https://github.com/pietvanzoen/fund-oregon-schools)"
VERSIONS_LOG = os.path.join(SOURCES, "_versions_log.csv")


class _Text(html.parser.HTMLParser):
    SKIP = {"script", "style", "noscript", "nav", "footer", "header", "svg"}
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "table"}

    def __init__(self):
        super().__init__()
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")
        if tag == "a" and not self.skip:
            href = dict(attrs).get("href")
            if href and href.lower().endswith(".pdf"):
                self.out.append(f" <{href}> ")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def html_to_text(raw):
    p = _Text()
    p.feed(raw.decode("utf-8", "replace"))
    lines = [" ".join(l.split()) for l in "".join(p.out).splitlines()]
    text, blank = [], False
    for l in lines:
        if l:
            text.append(l)
            blank = False
        elif not blank:
            text.append("")
            blank = True
    return "\n".join(text).strip() + "\n"


def extract_text(path, content_type):
    if path.lower().endswith(".pdf") or "pdf" in content_type:
        if shutil.which("pdftotext"):
            subprocess.run(["pdftotext", "-enc", "UTF-8", path, path + ".txt"], check=False)
        else:
            print(f"  ! pdftotext missing; no text for {path}", file=sys.stderr)
    elif path.lower().endswith((".html", ".htm")) or "html" in content_type:
        with open(path, "rb") as f:
            raw = f.read()
        with open(path + ".txt", "w", encoding="utf-8") as f:
            f.write(html_to_text(raw))


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read(), r.geturl(), r.headers.get("Content-Type", "")


def log_version(path, prior, old_sha, new_sha, now):
    new = not os.path.exists(VERSIONS_LOG)
    with open(VERSIONS_LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["path", "prior_copy", "old_sha256", "new_sha256", "detected_at"])
        w.writerow([path, prior, old_sha, new_sha, now])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    known = manifest_by_path()
    ok = fail = skipped = 0
    for row in read_queue():
        rel = row["path"].strip().lstrip("/")
        if not rel.startswith(args.only):
            continue
        if ".." in rel.split("/") or rel.startswith("_"):
            print(f"  ! bad path {rel!r}", file=sys.stderr)
            fail += 1
            continue
        dest = os.path.join(SOURCES, rel)
        if os.path.exists(dest) and not args.refresh:
            skipped += 1
            continue
        url = row["url"].strip()
        print(f"- {rel}  <=  {url}")
        try:
            data, final_url, ctype = download(url)
        except Exception as e:  # noqa: BLE001
            print(f"  ! failed: {e}", file=sys.stderr)
            fail += 1
            continue
        now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
        sha = hashlib.sha256(data).hexdigest()
        if os.path.exists(dest):
            old_sha = known.get(rel, {}).get("sha256") or hashlib.sha256(open(dest, "rb").read()).hexdigest()
            if old_sha == sha:
                skipped += 1
                continue
            prior_dir = os.path.join(os.path.dirname(dest), "_prior")
            os.makedirs(prior_dir, exist_ok=True)
            stem, ext = os.path.splitext(os.path.basename(dest))
            prior = os.path.join(prior_dir, f"{stem}.{now[:10]}{ext}")
            shutil.move(dest, prior)
            for side in (".txt", ".ocr.txt"):
                if os.path.exists(dest + side):
                    shutil.move(dest + side, prior + side)
            log_version(rel, os.path.relpath(prior, SOURCES), old_sha, sha, now)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)
        extract_text(dest, ctype)
        rec = {"path": rel, "url": url, "final_url": final_url, "fetched_at": now, "sha256": sha,
               "bytes": len(data), "content_type": ctype, "title": row.get("title", ""),
               "date": row.get("date", ""), "kind": row.get("kind", "")}
        with open(MANIFEST, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        ok += 1
    print(f"fetched {ok}, unchanged/skipped {skipped}, failed {fail}")
    return 1 if fail and not ok else 0


if __name__ == "__main__":
    sys.exit(main())
