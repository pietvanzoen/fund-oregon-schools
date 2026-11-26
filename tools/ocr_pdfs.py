#!/usr/bin/env python3
"""OCR the pages of archived PDFs that pdftotext got little text from, writing <file>.pdf.ocr.txt.

    python3 tools/ocr_pdfs.py

A page is OCR'd when it has an image and fewer than MIN_CHARS characters of extractable text (slides whose tables
and charts are pictures, scans). <file>.pdf.ocr.txt is <file>.pdf.txt with the OCR text added under a MARKER line on
those pages, so exact text stays exact, pages stay separated by \\f, and text_path() and search.py prefer it. PDFs
that already have one are skipped, and the PDF itself is never touched. Needs pdftotext, pdfimages, pdftoppm (poppler-utils) and tesseract.
Runs in the fetch-sources Action after each fetch, so new PDFs and older ones alike get OCR'd once.
"""

import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SOURCES

# shortcut: a page with MIN_CHARS+ of real text but a chart or table as a picture isn't OCR'd, so numbers in the
# picture aren't searchable; lower MIN_CHARS (or OCR every page with a large image) if a cited deck needs them.
MIN_CHARS = 200
MARKER = (
    "--- OCR of this page (tesseract), not checked by a person: check the PDF before quoting or copying a figure ---"
)


def pages_to_ocr(pages, image_pages):
    """1-based numbers of pages with an image and under MIN_CHARS characters of text."""
    return [n for n, text in enumerate(pages, 1) if n in image_pages and len("".join(text.split())) < MIN_CHARS]


def image_pages(pdf):
    out = subprocess.run(["pdfimages", "-list", pdf], capture_output=True, text=True, check=True).stdout
    return {int(line.split()[0]) for line in out.splitlines()[2:] if line.split()}


def ocr_page(pdf, n, tmp):
    prefix = os.path.join(tmp, f"p{n}")
    subprocess.run(
        ["pdftoppm", "-r", "300", "-gray", "-png", "-singlefile", "-f", str(n), "-l", str(n), pdf, prefix], check=True
    )
    return subprocess.run(["tesseract", prefix + ".png", "stdout"], capture_output=True, text=True, check=True).stdout


def main():
    done = failed = 0
    for d, dirs, files in os.walk(SOURCES):
        dirs[:] = [x for x in dirs if x != "_prior"]
        for f in sorted(files):
            pdf = os.path.join(d, f)
            if not f.lower().endswith(".pdf") or os.path.exists(pdf + ".ocr.txt"):
                continue
            try:
                text = subprocess.run(
                    ["pdftotext", "-enc", "UTF-8", pdf, "-"], capture_output=True, text=True, check=True
                ).stdout
                pages = text.split("\f")[:-1]  # pdftotext ends every page with \f
                todo = pages_to_ocr(pages, image_pages(pdf))
                if not todo:
                    continue
                print(f"- {os.path.relpath(pdf, SOURCES)}: OCR pages {todo}", flush=True)
                with tempfile.TemporaryDirectory() as tmp:
                    for n in todo:
                        pages[n - 1] += f"\n{MARKER}\n{ocr_page(pdf, n, tmp)}"
            except (subprocess.CalledProcessError, ValueError) as e:
                print(f"  ! {os.path.relpath(pdf, SOURCES)}: {e}", file=sys.stderr)
                failed += 1
                continue
            # written only when complete, so a cancelled run leaves no partial file to commit
            with open(pdf + ".ocr.txt", "w", encoding="utf-8") as out:
                out.write("".join(p + "\f" for p in pages))
            done += 1
    print(f"OCR'd {done} PDF(s), failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
