#!/usr/bin/env python3
"""Print a page of an archived document, or grep it with page numbers.

python3 tools/doc.py qec/2026_qem_report            # list matching files and page counts
python3 tools/doc.py qec/2026_qem_report 12          # page 12 (the N in [SRC:... p.N])
python3 tools/doc.py qec/2026_qem_report --grep "current service level"
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SOURCES, text_path


def find(fragment):
    hits = []
    for dirpath, _, files in os.walk(SOURCES):
        if "/_prior" in dirpath:
            continue
        for f in files:
            if f.endswith((".txt", ".json", ".jsonl", ".csv")) or f.startswith("_"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), SOURCES)
            if fragment in rel:
                hits.append(rel)
    return sorted(hits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fragment")
    ap.add_argument("page", nargs="?", type=int)
    ap.add_argument("--grep")
    a = ap.parse_args()
    hits = find(a.fragment)
    if not hits:
        sys.exit(f"no archived file matches {a.fragment!r} (queued but not fetched yet? see sources/_queue.csv)")
    if len(hits) > 1 and (a.page or a.grep):
        print("several matches, using the first:", *hits, sep="\n  ", file=sys.stderr)
    if not a.page and not a.grep:
        for h in hits:
            tp = text_path(h)
            pages = open(tp, encoding="utf-8", errors="replace").read().count("\f") + 1 if tp else 0
            print(f"{h}  ({pages} pages{'' if tp else ', no text'})")
        return
    rel = hits[0]
    tp = text_path(rel)
    if not tp:
        sys.exit(f"{rel} has no text extraction")
    pages = open(tp, encoding="utf-8", errors="replace").read().split("\f")
    if a.grep:
        rx = re.compile(a.grep, re.IGNORECASE)
        for n, pg in enumerate(pages, 1):
            for line in pg.splitlines():
                if rx.search(line):
                    print(f"[SRC:{rel} p.{n}] {line.strip()}")
    else:
        if not 1 <= a.page <= len(pages):
            sys.exit(f"{rel} has {len(pages)} pages")
        print(f"[SRC:{rel} p.{a.page}]\n")
        print(pages[a.page - 1])


if __name__ == "__main__":
    main()
