#!/usr/bin/env python3
"""Full-text search over sources, news records, analysis and quotes (SQLite FTS5, stdlib only).

    python3 tools/search.py "State School Fund" -n 20
    python3 tools/search.py "current service level" --kind src     # archived documents only
    python3 tools/search.py "reserves" --kind analysis --kind derived   # our inference and our calculations

Kinds: src (archived documents), news (news records), quote (quotes_all.jsonl); and the archive's own files in
analysis/: cited (what sources say, cited), analysis (our inference: a "## Analysis" section or an "Analysis:"
item), derived (our calculations, cited as [DER:...]) and summary (front matter: uncited, never cite it).
    python3 tools/search.py "budget" --kind quote --person Kotek
    python3 tools/search.py '"Education Stability Fund" AND emergency' --json

Machine transcripts of audio/video (<file>.txt) come back one line per hit, as [VID:<path>@H:MM:SS].
The index lives in .cache/search.sqlite and rebuilds itself when any file is newer than it.
"""

import argparse
import csv
import io
import json
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ANALYSIS, MEDIA, NEWS_INDEX, QUOTES, ROOT, SOURCES, front_matter, read_jsonl

KINDS = ["src", "news", "quote", "cited", "analysis", "derived", "summary"]
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
    return any(os.path.getmtime(p) > built for p in [__file__, *corpus_files()])  # a change here changes the index


def analysis_rows(rel, text):
    """The archive's own files, kind by what each piece is: analysis (our inference), cited (what sources say,
    with citations), derived (our calculations), summary (uncited front matter). One row per paragraph or list
    item of a .md, per record of a .csv, per visual."""
    if rel.endswith(".json"):
        return [("cited", rel, "", "", text)]
    if rel.endswith(".csv"):
        rows, reader = [], csv.reader(io.StringIO(text))
        header, start = next(reader, []), 2
        for rec in reader:
            r = dict(zip(header, rec))
            if any(rec):
                derived = rel.startswith("analysis/derived/")
                cite = f"[DER:{os.path.basename(rel)[:-4]}/{r.get('id', '')}]" if derived else f"{rel}:{start}"
                rows.append(
                    ("derived" if derived else "cited", cite, "", "", "  ".join(f"{k}: {v}" for k, v in r.items() if v))
                )
            start = reader.line_num + 1
        return rows
    try:
        meta, body = front_matter(text)
    except ValueError:  # check_citations reports it; still index the text
        meta, body = {}, text
    rows = [("summary", f"{rel} front matter", "", "", "  ".join(meta.values()))] if meta else []
    buf, section, heading = [], "", ""

    def flush():
        if buf:
            chunk = "\n".join(line for _, line in buf)
            kind = {"Analysis": "analysis", "Derived figures": "derived"}.get(section, "cited")
            if re.match(r"(- )?Analysis:", chunk):
                kind = "analysis"
            rows.append((kind, f"{rel}:{buf[0][0]}" + (f" ({heading})" if heading else ""), "", "", chunk))
            buf.clear()

    first = text[: len(text) - len(body)].count("\n") + 1
    for n, line in enumerate(body.split("\n"), first):
        if not line.strip() or re.match(r"#{1,6} |- ", line):
            flush()  # a list item is its own row: one list can mix "Analysis:" items with cited ones
        if re.match(r"#{1,6} ", line):
            heading = line.lstrip("#").strip()
            section = heading if line.startswith("## ") else section
        elif line.strip():
            buf.append((n, line))
    flush()
    return rows


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
            if rel.lower().endswith(MEDIA):  # transcript: one row per "H:MM:SS text" line, cited as VID
                # shortcut: a phrase split across two transcript lines isn't found; index runs of lines if that bites
                for line in open(full, encoding="utf-8", errors="replace"):
                    ts, _, said = line.strip().partition(" ")
                    if re.fullmatch(r"\d+:\d\d:\d\d", ts):
                        rows.append(("src", f"[VID:{os.path.splitext(rel)[0]}@{ts}]", "", "", said))
                continue
            pages = open(full, encoding="utf-8", errors="replace").read().split("\f")
            is_pdf = rel.lower().endswith(".pdf")
            for n, pg in enumerate(pages, 1):
                if pg.strip():
                    rows.append(("src", f"[SRC:{rel} p.{n}]" if is_pdf else f"[SRC:{rel}]", "", "", pg))
    for r in read_jsonl(NEWS_INDEX):
        body = " ".join(str(r.get(k, "")) for k in ("title", "outlet", "summary", "key_facts", "quotes"))
        rows.append(("news", f"[NEWS:{r['id']}]", "", r.get("date", ""), body))
    for q in read_jsonl(QUOTES):
        rows.append(
            (
                "quote",
                q.get("cite", ""),
                q.get("person", ""),
                q.get("date", ""),
                f"{q.get('quote', '')}  ({q.get('context', '')})",
            )
        )
    for dirpath, _, files in os.walk(ANALYSIS):
        for f in files:
            if f.endswith((".md", ".csv")) or dirpath.endswith("visuals") and f.endswith(".json"):
                full = os.path.join(dirpath, f)
                rows += analysis_rows(os.path.relpath(full, ROOT), open(full, encoding="utf-8").read())
    con.executemany("INSERT INTO docs VALUES (?,?,?,?,?)", rows)
    con.commit()
    return con


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=15)
    ap.add_argument("--kind", action="append", choices=KINDS, help="repeat for several")
    ap.add_argument("--person")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    con = build() if stale() else sqlite3.connect(DB)
    sql = "SELECT kind, cite, person, date, snippet(docs, 4, '«', '»', ' … ', 24) FROM docs WHERE docs MATCH ?"
    params = [a.query]
    if a.kind:
        sql += f" AND kind IN ({','.join('?' * len(a.kind))})"
        params += a.kind
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
