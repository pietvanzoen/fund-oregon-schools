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
# audio/video the transcribe Action turns into <file>.txt ("H:MM:SS text" lines), cited as [VID:...]
MEDIA = (".mp4", ".m4a", ".mp3", ".wav", ".webm")

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


FM_LINE = re.compile(r"([a-z_]+): ?(.*)")


def front_matter(text):
    """'---\\nsummary: >\\n  a\\n  b\\n---\\n# H1' -> ({'summary': 'a b'}, '# H1'). No front matter -> ({}, text).
    Only `key: value` and a folded `key: >` block, so the stdlib can read it the same way YAML does;
    anything else raises ValueError."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 3)
    if end < 0:
        raise ValueError("front matter has no closing ---")
    meta, key = {}, None
    for line in text[4:end].split("\n"):
        if key and line.startswith("  ") and line.strip():
            meta[key] = (meta[key] + " " + line.strip()).strip()
            continue
        m = FM_LINE.fullmatch(line)
        if not m:
            raise ValueError(f"front matter line isn't `key: value` or an indented `>` line: {line!r}")
        k, v = m.groups()
        if k in meta:
            raise ValueError(f"front matter key {k} appears twice")
        # these would mean something else in YAML (quotes, lists, comments, nested keys, | blocks)
        if v != ">" and (not v or v[0] in "'\"[]{}&*!|>%@`#" or ": " in v or " #" in v):
            raise ValueError(f"front matter {k}: use a plain value or a folded `>` block")
        meta[k], key = ("", k) if v == ">" else (v, None)
    for k, v in meta.items():
        if not v:
            raise ValueError(f"front matter {k} is empty")
    return meta, text[end + 5:]


def text_path(src_path):
    """Text extraction that sits next to an archived file."""
    full = os.path.join(SOURCES, src_path)
    for cand in (full + ".ocr.txt", full + ".txt"):
        if os.path.exists(cand):
            return cand
    if full.endswith((".txt", ".md")) and os.path.exists(full):
        return full
    return None
