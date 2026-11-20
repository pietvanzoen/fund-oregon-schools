#!/usr/bin/env python3
"""Download queued sources into sources/, record provenance, extract text. Never overwrites.

    python3 tools/fetch_sources.py            # fetch queue rows whose file doesn't exist yet
    python3 tools/fetch_sources.py --refresh  # also re-fetch existing files; changed ones keep the old copy in _prior/
    python3 tools/fetch_sources.py --only gov/  # only rows whose path starts with this

Runs in the fetch-sources GitHub Action (cloud sandboxes usually can't reach oregon.gov / OLIS).
Needs pdftotext (poppler-utils) for PDF text; without it the PDF is still archived.

Each download is retried (FOS_RETRIES attempts, default 3) on timeouts, connection errors, HTTP 429 and 5xx, with
a growing pause (FOS_RETRY_DELAY seconds, default 5, then 3x that). Requests to the same host are spaced by
FOS_REQUEST_DELAY seconds (default 1). Any failed row is listed at the end, written to the GitHub job summary and
annotated as an error when run in Actions, and makes the exit code 1 even if other rows succeeded.
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
import time
import urllib.error
import urllib.parse
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


RETRIES = max(1, int(os.environ.get("FOS_RETRIES", "3")))
RETRY_DELAY = float(os.environ.get("FOS_RETRY_DELAY", "5"))
REQUEST_DELAY = float(os.environ.get("FOS_REQUEST_DELAY", "1"))
_last_request = {}


def _retryable(e):
    if isinstance(e, urllib.error.HTTPError):
        return e.code in (408, 429) or e.code >= 500
    return isinstance(e, (urllib.error.URLError, TimeoutError, ConnectionError, OSError))


def _describe(e):
    if isinstance(e, urllib.error.HTTPError):
        return f"HTTP {e.code} {e.reason}"
    if isinstance(e, urllib.error.URLError):
        return f"connection error: {e.reason}"
    return f"{type(e).__name__}: {e}"


def _download_once(url):
    host = urllib.parse.urlsplit(url).netloc
    wait = _last_request.get(host, 0) + REQUEST_DELAY - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read(), r.geturl(), r.headers.get("Content-Type", "")
    finally:
        _last_request[host] = time.monotonic()


def download(url):
    """Download with retries. Returns (data, final_url, content_type); raises the last error."""
    for attempt in range(1, RETRIES + 1):
        try:
            return _download_once(url)
        except Exception as e:  # noqa: BLE001
            if attempt == RETRIES or not _retryable(e):
                raise
            pause = RETRY_DELAY * (3 ** (attempt - 1))
            print(f"  ~ attempt {attempt} failed ({_describe(e)}); retrying in {pause:g}s", file=sys.stderr)
            time.sleep(pause)


def report_failures(failures):
    """List failed rows on stderr, in the GitHub job summary, and as Actions error annotations."""
    if not failures:
        return
    print(f"\nFAILED ({len(failures)}):", file=sys.stderr)
    for rel, url, err in failures:
        print(f"  {rel}  <=  {url}\n      {err}", file=sys.stderr)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::error title=Source not fetched::{rel}: {err} ({url})")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"### {len(failures)} source(s) failed to download\n\n| Path | Error | URL |\n|---|---|---|\n")
            for rel, url, err in failures:
                f.write(f"| `{rel}` | {err} | {url} |\n")
            f.write("\nThey stay in the queue; re-run fetch-sources (Actions -> fetch-sources -> Run workflow) to retry.\n")


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
    ok = skipped = 0
    failures = []
    for row in read_queue():
        rel = row["path"].strip().lstrip("/")
        if not rel.startswith(args.only):
            continue
        if ".." in rel.split("/") or rel.startswith("_"):
            failures.append((rel, row.get("url", "").strip(), "bad path"))
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
            err = _describe(e) + (f" (after {RETRIES} attempts)" if _retryable(e) and RETRIES > 1 else "")
            print(f"  ! failed: {err}", file=sys.stderr)
            failures.append((rel, url, err))
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
    print(f"fetched {ok}, unchanged/skipped {skipped}, failed {len(failures)}")
    report_failures(failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
