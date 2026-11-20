#!/usr/bin/env python3
"""Full-text search over sources, news records, analysis and quotes (SQLite FTS5, stdlib only).

    python3 tools/search.py "State School Fund" -n 20
    python3 tools/search.py "current service level" --kind src     # src | news | analysis | quote
    python3 tools/search.py "budget" --kind quote --person Kotek
    python3 tools/search.py '"Education Stability Fund" AND emergency' --json

The index lives in .cache/search.sqlite and rebuilds itself when any file is newer than it.
"""
import argparse
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ANALYSIS, NEWS_INDEX, QUOTES, ROOT, SOURCES, read_jsonl  # noqa: E402

DB = os.path.join(ROOT, ".cache", "search.sqlite")


def corpus_files():
    for base in (SOURCES, ANALYSIS):
        for dirpath, _, files in os.walk(base):
            if "/_prior" in dirpath:
                continue
            for f in files:
                yield os.path.join(dirpath, f)


def stale():
    if not os.path.exists(DB):
        return True
    built = os.path.getmtime(DB)
    return any(os.path.getmtime(p) > built for p in corpus_files())


def build():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.execute("CREATE VIRTUAL TABLE docs USING fts5(kind, cite, person, date, body, tokenize='porter unicode61')")
    rows = []
    # archived source text, one row per page
    for dirpath, _, files in os.walk(SOURCES):
        if "/_prior" in dirpath:
            continue
        for f in files:
            if not f.endswith(".txt"):
                continue
            full = os.path.join(dirpath, f)
            orig = full[:-8] if full.endswith(".ocr.txt") else full[:-4]
            if full.endswith(".txt") and os.path.exists(orig + ".ocr.txt") and not full.endswith(".ocr.txt"):
                continue  # prefer OCR text when present
            rel = os.path.relpath(orig, SOURCES)
            pages = open(full, encoding="utf-8", errors="replace").read().split("\f")
            is_pdf = rel.lower().endswith(".pdf")
            for n, pg in enumerate(pages, 1):
                if pg.strip():
                    rows.append(("src", f"[SRC:{rel} p.{n}]" if is_pdf else f"[SRC:{rel}]", "", "", pg))
    for r in read_jsonl(NEWS_INDEX):
        body = " ".join(str(r.get(k, "")) for k in ("title", "outlet", "summary", "key_facts", "quotes"))
        rows.append(("news", f"[NEWS:{r['id']}]", "", r.get("date", ""), body))
    for q in read_jsonl(QUOTES):
        rows.append(("quote", q.get("cite", ""), q.get("person", ""), q.get("date", ""),
                     f"{q.get('quote', '')}  ({q.get('context', '')})"))
    for dirpath, _, files in os.walk(ANALYSIS):
        for f in files:
            if f.endswith((".md", ".csv")):
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, ROOT)
                for i, chunk in enumerate(open(full, encoding="utf-8").read().split("\n\n")):
                    if chunk.strip():
                        rows.append(("analysis", f"{rel}#{i}", "", "", chunk))
    con.executemany("INSERT INTO docs VALUES (?,?,?,?,?)", rows)
    con.commit()
    return con


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=15)
    ap.add_argument("--kind", choices=["src", "news", "analysis", "quote"])
    ap.add_argument("--person")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    con = build() if stale() else sqlite3.connect(DB)
    sql = "SELECT kind, cite, person, date, snippet(docs, 4, '«', '»', ' … ', 24) FROM docs WHERE docs MATCH ?"
    params = [a.query]
    if a.kind:
        sql += " AND kind = ?"
        params.append(a.kind)
    if a.person:
        sql += " AND person LIKE ?"
        params.append(f"%{a.person}%")
    sql += " ORDER BY rank LIMIT ?"
    params.append(a.n)
    try:
        res = con.execute(sql, params).fetchall()
    except sqlite3.OperationalError as e:
        sys.exit(f"bad query: {e}")
    if a.json:
        print(json.dumps([dict(zip(["kind", "cite", "person", "date", "snippet"], r)) for r in res], indent=1))
        return
    for kind, cite, person, date, snip in res:
        meta = " ".join(x for x in (date, person) if x)
        print(f"{kind:8} {cite} {meta}\n         {' '.join(snip.split())}\n")
    if not res:
        print("no matches")


if __name__ == "__main__":
    main()
