#!/usr/bin/env python3
"""Check sources/_queue.csv rows and archived files against the conventions in .claude/rules/sources.md.

    python3 tools/check_sources.py      # errors fail (exit 1); warnings are printed for a reviewer to judge

Errors:
  - queue row: missing url/path/title/kind, non-http(s) URL, duplicate URL, top folder not in .claude/rules/sources.md's list,
    OLIS path without a session folder (e.g. legislature/olis/2025R1/...), or a news site URL (news is never
    archived: add a record to sources/news/index.jsonl instead)
  - archived file under sources/ with no line in sources/_manifest.jsonl
Warnings:
  - queue row from a host that isn't a known government site (a reviewer checks it's the official copy)
  - queue row URL and path with different file types (e.g. a .pdf URL saved as .html)
"""

import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SOURCES, manifest_by_path, read_queue

TOP_DIRS = {"gov", "legislature", "ode", "fiscal", "reference", "districts", "orgs"}
NEWS_HOSTS = {
    "katu.com",
    "ktvz.com",
    "wweek.com",
    "klcc.org",
    "newsfromthestates.com",
    "opb.org",
    "oregonlive.com",
    "salemreporter.com",
    "oregoncapitalchronicle.com",
    "statesmanjournal.com",
    "registerguard.com",
    "koin.com",
    "kgw.com",
    "kptv.com",
    "portlandtribune.com",
    "pamplinmedia.com",
    "oregonjournalismproject.org",
    "bendbulletin.com",
    "eastoregonian.com",
}
OFFICIAL_SUFFIXES = (".oregon.gov", ".oregonlegislature.gov", ".state.or.us", ".k12.or.us", ".gov")
OFFICIAL_HOSTS = {"oregon.gov", "oregonlegislature.gov", "oregonencyclopedia.org"}
OLIS_RE = re.compile(r"^legislature/olis/\d{4}[RIS]\d/[^/]+$")


def host_matches(host, names):
    return any(host == n or host.endswith("." + n) for n in names)


def ext(s):
    return os.path.splitext(urllib.parse.urlparse(s).path if "://" in s else s)[1].lower()


def main():
    errors, warnings = [], []
    seen = {}
    for n, r in enumerate(read_queue(), 2):
        where = f"sources/_queue.csv:{n}"
        url, path = (r.get("url") or "").strip(), (r.get("path") or "").strip()
        for k in ("path", "title", "kind"):
            if not (r.get(k) or "").strip():
                errors.append(f"{where}: missing {k}")
        u = urllib.parse.urlparse(url)
        host = (u.hostname or "").lower()
        if u.scheme not in ("http", "https"):
            errors.append(f"{where}: URL must be http(s): {url}")
        if url in seen:
            errors.append(f"{where}: same URL as line {seen[url]}")
        seen[url] = n
        if path.split("/", 1)[0] not in TOP_DIRS:
            errors.append(f"{where}: path {path} must start with one of {', '.join(sorted(TOP_DIRS))}/")
        if path.startswith("legislature/olis/") and not OLIS_RE.match(path):
            errors.append(f"{where}: OLIS path needs a session folder: legislature/olis/<2025R1>/<docId>_<slug>")
        if host_matches(host, NEWS_HOSTS):
            errors.append(f"{where}: {host} is a news site; add a news record instead of archiving the article")
        elif not (host in OFFICIAL_HOSTS or host.endswith(OFFICIAL_SUFFIXES)):
            warnings.append(f"{where}: {host} isn't a known government site; check this is the official copy")
        ue, pe = ({".htm": ".html"}.get(e, e) for e in (ext(url), ext(path)))
        if ue in (".pdf", ".html") and pe and ue != pe:
            warnings.append(f"{where}: URL is {ue} but path is {pe}")

    manifest = manifest_by_path()
    for dirpath, dirs, files in os.walk(SOURCES):
        rel_dir = os.path.relpath(dirpath, SOURCES)
        dirs[:] = [d for d in dirs if d != "_prior" and not (rel_dir == "." and d == "news")]
        for f in files:
            if f.endswith(".txt") or f.startswith("_") or f == "README.md":
                continue
            rel = os.path.normpath(os.path.join(rel_dir, f))
            if rel not in manifest:
                errors.append(f"sources/{rel}: archived file has no line in sources/_manifest.jsonl")

    for w in warnings:
        print("warn ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
