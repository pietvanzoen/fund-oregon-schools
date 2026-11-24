#!/usr/bin/env python3
"""Check that every citation tag in analysis/ resolves, and that data files are well formed.

    python3 tools/check_citations.py            # errors fail (exit 1); pending sources are warnings
    python3 tools/check_citations.py --pending  # list queued sources not fetched yet

Errors: unknown SRC path (not archived and not queued), page beyond the document, unknown NEWS id,
CSV row with no source, malformed JSONL, duplicate queue paths or news ids;
malformed analysis/derived/<topic>.csv, unknown [DER:topic/id], a DER value not shown in its sentence or table row,
a DER figure outside topics/ without "our sum"/"our estimate" in its sentence;
a topic file without an uncited `summary` in its front matter, front matter outside topics/ or beyond `key: value`
and folded `>`; a topic file without the three sections in order (Analysis first), or a line under
"What the sources say" with no source citation or with "Analysis:".
Warnings also flag a number under "What the sources say" that isn't in the text of a source the line cites.
analysis/updates.csv (What's new) has its own columns instead of a source: date, text, page, pr.
The decision files (RESEARCH.md) must agree: every option, position and question names a decision in decisions.csv,
every decision has a baseline option, statuses and kinds are known values, and a position's actor is a people.csv id
or an organization's name. A people.csv area must appear on the legislature/members/ page its row cites.
questions.csv has no source column; tags in any *source column are checked.

    python3 tools/check_citations.py --measures  # RESEARCH.md's review measures: questions and decisions

    python3 tools/check_citations.py --pr 64 --base origin/main  # also: a PR that changes reader-facing files
                                                                # must add an updates.csv row with its number
"""
import argparse
import csv
import glob
import os
import re
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ANALYSIS, DERIVED, NEWS_INDEX, QUOTES, ROOT, SOURCES, TAG_RE, front_matter,  # noqa: E402
                    parse_src, read_jsonl, read_queue, text_path)

SECTIONS = ["Analysis", "What the sources say", "Derived figures"]
DER_COLS = ["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"]
UPDATE_COLS = ["date", "text", "page", "pr"]
UPDATES = os.path.join(ANALYSIS, "updates.csv")
NOT_READER_FACING = {"analysis/updates.csv"}  # not shown on the site
QUESTIONS = os.path.join(ANALYSIS, "questions.csv")
DATE_RE = re.compile(r"\d{4}(-\d{2}(-\d{2})?)?")
KINDS = {"baseline", "benchmark", "proposal"}
DECISION_STATUS = {"open", "decided", "implemented"}
QUESTION_STATUS = {"open", "answered", "not planned"}
ZERO_WIDTH = re.compile("[\u200b-\u200d\ufeff]")
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
BLOCK_START = re.compile(r"^\s*(?:[-*] |\d+\. |\||#+ )")
# shortcut: an abbreviation like "Gov. " also ends a sentence; reword the sentence if it splits a DER figure off
TABLE_SEP = re.compile(r"^\|[\s:|-]+\|$")
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
    ap.add_argument("--pr", type=int, help="pull request number: require an updates.csv row for it")
    ap.add_argument("--base", default="origin/main", help="branch the PR merges into, for --pr")
    ap.add_argument("--measures", action="store_true", help="print RESEARCH.md's review measures")
    a = ap.parse_args()
    errors, warnings = [], []
    if a.measures:
        return measures()

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
                text = open(full, encoding="utf-8").read()
                lines = list(enumerate(text.split("\n"), 1))
                try:
                    meta, body = front_matter(text)
                except ValueError as e:
                    errors.append(f"{rel}: {e}")
                    continue
                body_lines = lines[len(lines) - len(body.split("\n")):]  # keeps the file's line numbers
                for n, line in lines:
                    for m in TAG_RE.finditer(line):
                        check_tag(f"{rel}:{n}", m.group(1), m.group(2))
                check_der_figures(rel, body_lines, derived, errors)
                check_glossary(rel, lines, glossary, warnings)  # the summary too: STYLE.md allows no abbreviations
                if os.path.dirname(full) == os.path.join(ANALYSIS, "topics"):
                    check_summary(rel, meta, errors)
                    check_sections(rel, body_lines, news_text, errors, warnings)
                elif meta:
                    errors.append(f"{rel}: only topic files may have front matter (CLAUDE.md rule 4)")
            elif dirpath == DERIVED:
                continue  # checked above
            elif full == UPDATES:
                check_updates(rel, errors)
            elif full == QUESTIONS:
                continue  # checked with the decision files
            elif f.endswith(".csv"):
                with open(full, newline="", encoding="utf-8") as fh:
                    rd = csv.DictReader(fh)
                    if "source" not in (rd.fieldnames or []):
                        errors.append(f"{rel}: no 'source' column")
                        continue
                    for n, row in enumerate(rd, 2):
                        if not (row.get("source") or "").strip():
                            errors.append(f"{rel}:{n}: row has no source")
                        for col in (c for c in rd.fieldnames if c.endswith("source")):
                            for m in TAG_RE.finditer(row.get(col) or ""):
                                check_tag(f"{rel}:{n}", m.group(1), m.group(2))
            elif f.endswith(".jsonl"):
                for n, q in enumerate(read_jsonl(full), 1):
                    for k in ("person", "date", "quote", "cite"):
                        if full == QUOTES and not q.get(k):
                            errors.append(f"{rel}:{n}: missing {k}")
                    for m in TAG_RE.finditer(q.get("cite", "")):
                        check_tag(f"{rel}:{n}", m.group(1), m.group(2))

    if os.path.exists(os.path.join(ANALYSIS, "decisions.csv")):
        check_model(errors)
    if a.pr:
        check_pr_update(a.pr, a.base, errors)

    for w in sorted(set(warnings)):
        print("warn ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors, {len(set(warnings))} warnings, {len(pending)} queued sources not fetched")
    return 1 if errors else 0


def model_csv(name):
    path = os.path.join(ANALYSIS, name)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check_model(errors):
    """decisions, options, positions and questions refer to each other by id (RESEARCH.md, "The model")."""
    decisions = model_csv("decisions.csv")
    ids = {d["id"] for d in decisions}
    options = model_csv("options.csv")
    opt_ids = {o["id"] for o in options}
    people = {r["id"] for r in model_csv("people/people.csv")}
    for n, r in enumerate(model_csv("people/people.csv"), 2):
        # area is the member page's district label, copied exactly (STYLE.md, Names); catches drift on refresh
        m = re.search(r"\[SRC:(legislature/members/[^\]\s]+\.html)\]", r.get("source") or "")
        tp = m and r.get("area") and text_path(m.group(1))
        if tp and r["area"] not in ZERO_WIDTH.sub("", open(tp, encoding="utf-8").read()):
            errors.append(f"analysis/people/people.csv:{n}: area {r['area']!r} isn't on {m.group(1)}")
    for n, d in enumerate(decisions, 2):
        where = f"analysis/decisions.csv:{n}"
        if d["status"] not in DECISION_STATUS:
            errors.append(f"{where}: status must be one of {', '.join(sorted(DECISION_STATUS))}")
        if not DATE_RE.fullmatch(d["due"]):
            errors.append(f"{where}: due must be YYYY-MM-DD")
        if d["status"] != "open" and not d["outcome"].strip():
            errors.append(f"{where}: a {d['status']} decision needs an outcome")
        for r in filter(None, d["related"].split(";")):
            if r not in ids:
                errors.append(f"{where}: related decision {r} isn't in decisions.csv")
        if not any(o["decision"] == d["id"] and o["kind"] == "baseline" for o in options):
            errors.append(f"{where}: decision {d['id']} has no baseline option in options.csv")
    for n, o in enumerate(options, 2):
        where = f"analysis/options.csv:{n}"
        if o["decision"] not in ids:
            errors.append(f"{where}: decision {o['decision']} isn't in decisions.csv")
        if o["kind"] not in KINDS:
            errors.append(f"{where}: kind must be one of {', '.join(sorted(KINDS))}")
    for n, p in enumerate(model_csv("positions.csv"), 2):
        where = f"analysis/positions.csv:{n}"
        if p.get("replaces") and not (p["replaces"].isdigit() and 2 <= int(p["replaces"]) < n):
            errors.append(f"{where}: replaces must be the line number of an earlier row")
        if p["decision"] not in ids:
            errors.append(f"{where}: decision {p['decision']} isn't in decisions.csv")
        if p["option"] and p["option"] not in opt_ids:
            errors.append(f"{where}: option {p['option']} isn't in options.csv")
        if re.fullmatch(r"[a-z-]+", p["actor"]) and p["actor"] not in people:
            errors.append(f"{where}: actor {p['actor']} isn't an id in people/people.csv")
        if not DATE_RE.fullmatch(p["date"]):
            errors.append(f"{where}: date must be YYYY, YYYY-MM or YYYY-MM-DD")
    for n, q in enumerate(model_csv("questions.csv"), 2):
        where = f"analysis/questions.csv:{n}"
        if q["decision"] and q["decision"] not in ids:
            errors.append(f"{where}: decision {q['decision']} isn't in decisions.csv")
        if q["status"] not in QUESTION_STATUS:
            errors.append(f"{where}: status must be one of {', '.join(sorted(QUESTION_STATUS))}")
        if q["status"] != "open" and not q["answer"].strip():
            errors.append(f"{where}: an {q['status']} question needs an answer (a link, or what was found)")
        if q["needed_by"] and not DATE_RE.fullmatch(q["needed_by"]):
            errors.append(f"{where}: needed_by must be YYYY-MM-DD")


def measures():
    """RESEARCH.md, "How we know it's working": counts for the review at each due date."""
    qs = model_csv("questions.csv")
    by = {s: [q for q in qs if q["status"] == s] for s in QUESTION_STATUS}
    print(f"questions: {len(by['open'])} open, {len(by['answered'])} answered, {len(by['not planned'])} not planned")
    for d in model_csv("decisions.csv"):
        if d["status"] != "open":
            continue
        kinds = {o["kind"] for o in model_csv("options.csv") if o["decision"] == d["id"]}
        ps = model_csv("positions.csv")
        replaced = {p["replaces"] for p in ps if p.get("replaces")}
        stances = sum(p["decision"] == d["id"] and str(n) not in replaced for n, p in enumerate(ps, 2))
        print(f"{d['id']} (due {d['due']}): baseline {'yes' if 'baseline' in kinds else 'NO'}, "
              f"proposals {'yes' if 'proposal' in kinds else 'none'}, {stances} stances")
    return 0


def read_updates():
    with open(UPDATES, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        return rd.fieldnames, list(rd)


def check_updates(rel, errors):
    cols, rows = read_updates()
    if cols != UPDATE_COLS:
        errors.append(f"{rel}: columns must be {','.join(UPDATE_COLS)}")
        return
    for n, r in enumerate(rows, 2):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"]):
            errors.append(f"{rel}:{n}: date must be YYYY-MM-DD")
        if not r["text"].strip():
            errors.append(f"{rel}:{n}: no text")
        page = r["page"].split("#")[0]
        if page and not os.path.exists(os.path.join(ANALYSIS, page)):
            errors.append(f"{rel}:{n}: page {page} isn't a file under analysis/")
        if r["pr"] and not r["pr"].isdigit():
            errors.append(f"{rel}:{n}: pr must be a PR number")


def check_pr_update(pr, base, errors):
    """Readers learn about new research from What's new, so a PR that changes what the site shows adds a row."""
    out = subprocess.run(["git", "-C", ROOT, "diff", "--name-only", f"{base}...HEAD"],
                         capture_output=True, text=True)
    if out.returncode:
        errors.append(f"--pr: git diff against {base} failed: {out.stderr.strip()}")
        return
    changed = [f for f in out.stdout.split() if (f.startswith("analysis/") and f not in NOT_READER_FACING)
               or f == "sources/news/index.jsonl"]
    if changed and not any(r["pr"] == str(pr) for r in read_updates()[1]):
        errors.append(f"PR #{pr} changes {', '.join(changed[:3])}{' …' if len(changed) > 3 else ''} but "
                      f"analysis/updates.csv has no row with pr {pr}. Add one (date, text for readers, page, {pr}), "
                      "or label the PR no-update if readers don't need to know.")


def check_der_figures(rel, lines, derived, errors):
    """Each DER value is shown in its sentence or table row; outside topics/ that sentence says "our sum"/"our estimate"."""
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
                if not rel.startswith("analysis/topics/") and not re.search(r"\bour (sum|estimate)\b", sent, re.I):
                    errors.append(f"{rel}:{n}: [DER:{m.group(2)}] needs \"our sum\" or \"our estimate\" in its sentence")


# Everyday abbreviations and outlet names a reader doesn't need explained.
NOT_GLOSSARY = {"FAQ", "PDF", "URL", "OCR", "COVID", "SW", "NE", "NW", "SE", "II", "III", "US", "USA",
                "KATU", "KTVZ", "OPB", "KGW", "KOIN", "KLCC", "DER"}
ABBR_RE = re.compile(r"\b[A-Z][A-Z0-9&]{1,5}[a-z]?\b")  # ADMr, ADMw too


def check_glossary(rel, lines, glossary, warnings):
    """CLAUDE.md rule 11: an abbreviation in analysis needs a glossary row, unless the line writes it out as "(XYZ)".
    Quoted text is skipped: it's the source's wording (e.g. a bill's "Representative WRIGHT")."""
    seen = set()
    for n, line in lines:
        text = re.sub(r"`[^`]*`|\"[^\"]*\"|“[^”]*”", " ", TAG_RE.sub(" ", line))  # quoted text is verbatim
        for w in ABBR_RE.findall(text):
            if w in glossary or w in NOT_GLOSSARY or w in seen or f"({w})" in text:
                continue
            seen.add(w)
            warnings.append(f"{rel}:{n}: {w} isn't in analysis/glossary.csv (CLAUDE.md rule 11)")


def check_summary(rel, meta, errors):
    """Topic files: front matter holds only a `summary` (STYLE.md, "In short"), uncited; the page below backs it."""
    if not meta.get("summary"):
        errors.append(f"{rel}: no `summary` in front matter (STYLE.md, \"In short\")")
    for k in meta.keys() - {"summary"}:
        errors.append(f"{rel}: front matter key {k} isn't used; topic files hold only `summary`")
    if TAG_RE.search(meta.get("summary", "")):
        errors.append(f"{rel}: the summary carries no citations; back each sentence with a cited line below")


def check_sections(rel, lines, news_text, errors, warnings):
    """Topic files: the three sections in order; every line under "What the sources say" cites a source and carries no inference."""
    heads = [(i, line[3:].strip()) for i, (_, line) in enumerate(lines) if line.startswith("## ")]
    if [h for _, h in heads] != SECTIONS:
        errors.append(f"{rel}: needs exactly these sections, in order: " + ", ".join("## " + s for s in SECTIONS))
        return
    rows = blocks(lines[heads[1][0] + 1:heads[2][0]])
    for i, (n, text) in enumerate(rows):
        # headings, and a table's header and separator rows, carry no facts to cite
        if text.startswith("#") or TABLE_SEP.match(text) or (i + 1 < len(rows) and TABLE_SEP.match(rows[i + 1][1])):
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
