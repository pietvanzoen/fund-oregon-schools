"""Shared helpers for the fund-oregon-schools tools (stdlib only)."""
import csv
import json
import os
import re

ROOT = os.environ.get("FOS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # FOS_ROOT: tests
SOURCES = os.path.join(ROOT, "sources")
ANALYSIS = os.path.join(ROOT, "analysis")
QUEUE = os.path.join(SOURCES, "_queue.csv")
MANIFEST = os.path.join(SOURCES, "_manifest.jsonl")
NEWS_INDEX = os.path.join(SOURCES, "news", "index.jsonl")
QUOTES = os.path.join(ANALYSIS, "people", "quotes_all.jsonl")
DERIVED = os.path.join(ANALYSIS, "derived")

# [SRC:path p.3] [VID:path@1:02:03] [NEWS:id] [PPSARCH:BB:123 p.2] [DER:topic/id] (DER: our own calculation)
TAG_RE = re.compile(r"\[(SRC|VID|NEWS|PPSARCH|DER):([^\]]+)\]")


def read_queue():
    if not os.path.exists(QUEUE):
        return []
    with open(QUEUE, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("url") or "").strip()]


def read_jsonl(path):
    out = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise SystemExit(f"{path}:{n}: bad JSON: {e}")
    return out


def manifest_by_path():
    """Latest manifest entry per path."""
    m = {}
    for rec in read_jsonl(MANIFEST):
        m[rec["path"]] = rec
    return m


def parse_src(body):
    """'gov/x.pdf p.3' -> ('gov/x.pdf', 3). Page optional."""
    body = body.strip()
    m = re.match(r"^(.*?)(?:\s+p\.(\d+)(?:-\d+)?)?$", body)
    return m.group(1).strip(), (int(m.group(2)) if m.group(2) else None)


def text_path(src_path):
    """Text extraction that sits next to an archived file."""
    full = os.path.join(SOURCES, src_path)
    for cand in (full + ".ocr.txt", full + ".txt"):
        if os.path.exists(cand):
            return cand
    if full.endswith((".txt", ".md")) and os.path.exists(full):
        return full
    return None
