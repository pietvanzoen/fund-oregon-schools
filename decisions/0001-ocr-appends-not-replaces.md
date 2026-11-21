# 0001. OCR text is added below the page text, not swapped in

Status: accepted (2026-11-21, PR #50, issue #4)

## Context
Some slide decks have tables and charts as pictures, so pdftotext gets little or nothing from those pages.
`tools/ocr_pdfs.py` OCRs pages with an image and under 200 characters of text. In a trial, OCR garbled text that
pdftotext had read exactly: on `313099_quality-education-process.pdf` p.5, "$13.6 billion" came out as
"TT 13.6 billion … $13.6 bi".

## Decision
`<file>.pdf.ocr.txt` is the `.txt` text with each OCR'd page's OCR text added below a
`--- OCR of this page (tesseract), not checked by a person … ---` line. Page breaks (`\f`) and page numbers match
the `.txt`. Readers check the PDF page before quoting or copying anything from below the marker.

## Options weighed
- **Replace the page text with OCR text**: one clean version per page, but exact text gets worse, and verbatim
  quote checks against it would fail or pass on misread text.
- **Add OCR below a marker** (chosen): exact text stays exact; picture-only content becomes searchable; OCR is
  clearly labelled as unchecked. Costs some duplicate text on pages that had a little real text.
- **OCR every page**: catches charts on text-rich pages, but slower and adds noise to every PDF.

## Revisit when
A cited deck needs numbers from a chart on a page with 200+ characters of real text (see the `shortcut:` comment
in `tools/ocr_pdfs.py`), or OCR noise from cover pages starts crowding search results.
