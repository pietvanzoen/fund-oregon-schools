#!/usr/bin/env python3
"""Check that every citation tag in analysis/ resolves, and that data files are well formed.

    python3 tools/check_citations.py            # errors fail (exit 1); pending sources are warnings
    python3 tools/check_citations.py --pending  # list queued sources not fetched yet

Errors: unknown SRC path (not archived and not queued), page beyond the document, unknown NEWS id,
CSV row with no source, malformed JSONL, duplicate queue paths or news ids;
malformed analysis/derived/<topic>.csv, unknown [DER:topic/id], a DER value not shown in its sentence or table row,
a DER figure in BRIEFING without "our sum"/"our estimate" in its sentence;
a topic file without the three sections, or a line under "What the sources say" with no source citation or with
"Analysis:".
Warnings also flag a number under "What the sources say" that isn't in the text of a source the line cites.
"""
import argparse
import csv
import glob
import os
import re
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ANALYSIS, DERIVED, NEWS_INDEX, QUOTES, ROOT, SOURCES, TAG_RE, parse_src,  # noqa: E402
                    read_jsonl, read_queue, text_path)

SECTIONS = ["What the sources say", "Derived figures", "Analysis"]
DER_COLS = ["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"]
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
BLOCK_START = re.compile(r"^\s*(?:[-*] |\d+\. |\||#+ )")
# shortcut: an abbreviation like "Gov. " also ends a sentence; reword the sentence if it splits a DER figure off
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[*])")


def blocks(lines):
    """[(line number, text)] per paragraph, list item, table row or heading; wrapped lines are joined."""
    out, open_block = [], False
    for n, line in lines:
        if not line.strip():
            open_block = False
        elif BLOCK_START.match(line) or not open_block:
            out.append([n, line.strip()])
            open_block = not line.lstrip().startswith(("|", "#"))
        else:
            out[-1][1] += " " + line.strip()
    return out


def numbers(text):
    """Numbers outside citation tags, commas dropped."""
    return [x.replace(",", "") for x in NUM_RE.findall(TAG_RE.sub(" ", text))]


def rounds_to(value, shown):
    """True if value, rounded to the precision shown ("22,100" -> hundreds, "4.0" -> tenths), equals shown."""
    d = Decimal(shown)
    exp = d.as_tuple().exponent or (len(shown) - len(shown.rstrip("0")) if shown.strip("0") else 0)
    return Decimal(value).quantize(Decimal(1).scaleb(exp), rounding=ROUND_HALF_UP) == d


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
    news_text = {r.get("id"): " ".join(str(v) for v in r.values()) for r in news}

    derived = {}  # topic -> id -> row; read first so DER tags anywhere can resolve
    for f in sorted(os.listdir(DERIVED)) if os.path.isdir(DERIVED) else []:
        if not f.endswith(".csv"):
            continue
        rel = os.path.relpath(os.path.join(DERIVED, f), ROOT)
        with open(os.path.join(DERIVED, f), newline="", encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            if rd.fieldnames != DER_COLS:
                errors.append(f"{rel}: columns must be {','.join(DER_COLS)}")
                continue
            rows = derived.setdefault(f[:-4], {})
            for n, row in enumerate(rd, 2):
                if row["id"] in rows:
                    errors.append(f"{rel}:{n}: duplicate id {row['id']}")
                if row["kind"] not in ("derived", "est"):
                    errors.append(f"{rel}:{n}: kind must be derived or est")
                try:
                    Decimal(row["value"])
                except ArithmeticError:
                    errors.append(f"{rel}:{n}: value {row['value']!r} is not a number")
                    continue
                rows[row["id"]] = row

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
        elif kind == "DER":
            topic, _, did = body.strip().partition("/")
            if did not in derived.get(topic, {}):
                errors.append(f"{where}: unknown derived figure {body.strip()} (no such id in analysis/derived/{topic}.csv)")
        elif kind == "NEWS" and body.strip() not in news_ids:
            errors.append(f"{where}: unknown NEWS id {body.strip()}")
        elif kind == "VID":
            path = body.partition("@")[0].strip()
            # the tag has no extension, so look for the file with any extension (hand-saved, not queued)
            archived = glob.glob(glob.escape(os.path.join(SOURCES, path)) + ".*")
            if not any(p.startswith(path) for p in qpaths) and not archived:
                errors.append(f"{where}: unknown video {path}")

    glossary_path = os.path.join(ANALYSIS, "glossary.csv")
    glossary = set()
    if os.path.exists(glossary_path):
        with open(glossary_path, newline="", encoding="utf-8") as fh:
            glossary = {r["term"] for r in csv.DictReader(fh)}

    for dirpath, _, files in os.walk(ANALYSIS):
        for f in sorted(files):
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, ROOT)
            if f.endswith(".md"):
                lines = list(enumerate(open(full, encoding="utf-8").read().split("\n"), 1))
                for n, line in lines:
                    for m in TAG_RE.finditer(line):
                        check_tag(f"{rel}:{n}", m.group(1), m.group(2))
                check_der_figures(rel, lines, derived, errors)
                check_glossary(rel, lines, glossary, warnings)
                if os.path.dirname(full) == os.path.join(ANALYSIS, "topics"):
                    check_sections(rel, lines, news_text, errors, warnings)
            elif dirpath == DERIVED:
                continue  # checked above
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
    print(f"{len(errors)} errors, {len(set(warnings))} warnings, {len(pending)} queued sources not fetched")
    return 1 if errors else 0


def check_der_figures(rel, lines, derived, errors):
    """Each DER value is shown in its sentence or table row; in BRIEFING that sentence says "our sum"/"our estimate"."""
    for n, text in blocks(lines):
        for sent in [text] if text.startswith("|") else SENTENCE_END.split(text):
            for m in TAG_RE.finditer(sent):
                topic, _, did = m.group(2).strip().partition("/")
                row = derived.get(topic, {}).get(did) if m.group(1) == "DER" else None
                if not row:
                    continue  # not DER, or unknown id (reported by check_tag)
                # shortcut: compares in the derived file's unit (256.6 USD millions matches "$257M", not "$0.26B")
                if not any(rounds_to(row["value"], x) for x in numbers(sent)):
                    errors.append(f"{rel}:{n}: [DER:{m.group(2)}] is {row['value']} {row['unit']}; "
                                  "no number in its sentence rounds to that")
                if rel == "analysis/BRIEFING.md" and not re.search(r"\bour (sum|estimate)\b", sent, re.I):
                    errors.append(f"{rel}:{n}: [DER:{m.group(2)}] needs \"our sum\" or \"our estimate\" in its sentence")


# Everyday abbreviations and outlet names a reader doesn't need explained.
NOT_GLOSSARY = {"FAQ", "PDF", "URL", "OCR", "COVID", "SW", "NE", "NW", "SE", "II", "III", "US", "USA",
                "KATU", "KTVZ", "OPB", "KGW", "KOIN", "KLCC", "DER"}
ABBR_RE = re.compile(r"\b[A-Z][A-Z0-9&]{1,5}[a-z]?\b")  # ADMr, ADMw too


def check_glossary(rel, lines, glossary, warnings):
    """CLAUDE.md rule 11: an abbreviation in analysis needs a glossary row, unless the line writes it out as "(XYZ)"."""
    seen = set()
    for n, line in lines:
        text = re.sub(r"`[^`]*`", " ", TAG_RE.sub(" ", line))
        for w in ABBR_RE.findall(text):
            if w in glossary or w in NOT_GLOSSARY or w in seen or f"({w})" in text:
                continue
            seen.add(w)
            warnings.append(f"{rel}:{n}: {w} isn't in analysis/glossary.csv (CLAUDE.md rule 11)")


def check_sections(rel, lines, news_text, errors, warnings):
    """Topic files: the three sections in order; every line under the first cites a source and carries no inference."""
    heads = [(i, line[3:].strip()) for i, (_, line) in enumerate(lines) if line.startswith("## ")]
    if [h for _, h in heads] != SECTIONS:
        errors.append(f"{rel}: needs exactly these sections, in order: " + ", ".join("## " + s for s in SECTIONS))
        return
    for n, text in blocks(lines[heads[0][0] + 1:heads[1][0]]):
        if text.startswith("#"):
            continue
        cites = [m for m in TAG_RE.finditer(text) if m.group(1) != "DER"]
        if not cites:
            errors.append(f"{rel}:{n}: line under \"What the sources say\" has no source citation")
        if "Analysis:" in text:
            errors.append(f"{rel}:{n}: \"Analysis:\" under \"What the sources say\"; move it to ## Analysis")
        texts = [cited_text(m, news_text) for m in cites]
        if not cites or None in texts:
            continue  # a VID/PPSARCH/pending source has no text here to compare against
        # shortcut: no unit rescaling ($1.27B vs 1,271M warns); add it if false alarms are frequent, then make this an error
        hay = set(numbers(" ".join(texts)))  # whole numbers, so "22" doesn't match inside "2022"
        for x in numbers(text):
            if x not in hay:
                warnings.append(f"{rel}:{n}: {x} is not in the text of the sources this line cites")


def cited_text(m, news_text):
    """Text of the cited page (or whole document / news record), or None if there's none to check."""
    if m.group(1) == "NEWS":
        return news_text.get(m.group(2).strip())
    if m.group(1) != "SRC":
        return None
    path, page = parse_src(m.group(2))
    tp = text_path(path)
    if not tp:
        return None
    pages = open(tp, encoding="utf-8", errors="replace").read().split("\f")
    return pages[page - 1] if page and page <= len(pages) else "\f".join(pages)


if __name__ == "__main__":
    sys.exit(main())
