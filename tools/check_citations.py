#!/usr/bin/env python3
"""Check that every citation tag in analysis/ resolves, and that data files are well formed.

    python3 tools/check_citations.py            # errors fail (exit 1); pending sources are warnings
    python3 tools/check_citations.py --pending  # list queued sources not fetched yet

Errors: unknown SRC path (not archived and not queued), page beyond the document, unknown NEWS id,
CSV row with no source, malformed JSONL, duplicate queue paths or news ids.
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ANALYSIS, NEWS_INDEX, QUOTES, ROOT, SOURCES, TAG_RE, parse_src,  # noqa: E402
                    read_jsonl, read_queue, text_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pending", action="store_true")
    a = ap.parse_args()
    errors, warnings = [], []

    queue = read_queue()
    qpaths = [r["path"].strip() for r in queue]
    for p in {p for p in qpaths if qpaths.count(p) > 1}:
        errors.append(f"sources/_queue.csv: duplicate path {p}")
    pending = [p for p in qpaths if not os.path.exists(os.path.join(SOURCES, p))]
    if a.pending:
        print("\n".join(pending) or "nothing pending")
        return 0

    news = read_jsonl(NEWS_INDEX)
    ids = [r.get("id") for r in news]
    for i in {i for i in ids if ids.count(i) > 1}:
        errors.append(f"news index: duplicate id {i}")
    for r in news:
        for k in ("id", "date", "outlet", "title", "url", "summary"):
            if not r.get(k):
                errors.append(f"news {r.get('id')}: missing {k}")
        for q in r.get("quotes", []) or []:
            if len(str(q.get("text", "")).split()) >= 25:
                errors.append(f"news {r.get('id')}: quote of 25+ words")
    news_ids = set(ids)

    def check_tag(where, kind, body):
        if kind == "SRC":
            path, page = parse_src(body)
            full = os.path.join(SOURCES, path)
            if os.path.exists(full):
                tp = text_path(path)
                if page and tp:
                    n = open(tp, encoding="utf-8", errors="replace").read().count("\f") + 1
                    if page > n:
                        errors.append(f"{where}: {path} has {n} pages, cited p.{page}")
            elif path in qpaths:
                warnings.append(f"{where}: pending (queued, not fetched): {path}")
            else:
                errors.append(f"{where}: unknown source {path} (not archived, not in _queue.csv)")
        elif kind == "NEWS" and body.strip() not in news_ids:
            errors.append(f"{where}: unknown NEWS id {body.strip()}")
        elif kind == "VID":
            path = body.partition("@")[0].strip()
            if not any(p.startswith(path) for p in qpaths) and not os.path.exists(os.path.join(SOURCES, path)):
                errors.append(f"{where}: unknown video {path}")

    for dirpath, _, files in os.walk(ANALYSIS):
        for f in sorted(files):
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, ROOT)
            if f.endswith(".md"):
                for n, line in enumerate(open(full, encoding="utf-8"), 1):
                    for m in TAG_RE.finditer(line):
                        check_tag(f"{rel}:{n}", m.group(1), m.group(2))
            elif f.endswith(".csv"):
                with open(full, newline="", encoding="utf-8") as fh:
                    rd = csv.DictReader(fh)
                    if "source" not in (rd.fieldnames or []):
                        errors.append(f"{rel}: no 'source' column")
                        continue
                    for n, row in enumerate(rd, 2):
                        s = (row.get("source") or "").strip()
                        if not s:
                            errors.append(f"{rel}:{n}: row has no source")
                        for m in TAG_RE.finditer(s):
                            check_tag(f"{rel}:{n}", m.group(1), m.group(2))
            elif f.endswith(".jsonl"):
                for n, q in enumerate(read_jsonl(full), 1):
                    for k in ("person", "date", "quote", "cite"):
                        if full == QUOTES and not q.get(k):
                            errors.append(f"{rel}:{n}: missing {k}")
                    for m in TAG_RE.finditer(q.get("cite", "")):
                        check_tag(f"{rel}:{n}", m.group(1), m.group(2))

    for w in sorted(set(warnings)):
        print("warn ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors, {len(set(warnings))} pending-source warnings, {len(pending)} queued sources not fetched")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
