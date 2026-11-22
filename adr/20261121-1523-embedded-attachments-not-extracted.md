# Files embedded in archived PDFs aren't extracted

Status: accepted (2026-11-21, issue #4)

## Context
`legislature/olis/2025I1/310555_jpea.pdf` looked text-less but is a one-page cover email (text extracts fine)
with the Nov 7, 2025 "REVISION 1" draft of the JPEA report embedded as a PDF attachment. That draft has the same
figures as the Nov 5 version (`310553_jpea.pdf`); only the wording the email lists differs (mainly the three
funding alternatives). The Nov 14 version (`310695_jpea.pdf`), the one cited, has different figures. A scan of
the archive found only one other PDF with embedded files: `legislature/olis/2018R1/146437_lro-school-local-option.pdf`,
with three embedded Excel files (likely the data behind its charts).

## Decision
Leave embedded files inside their PDFs. The cover email, which lists the Nov 5 → Nov 7 changes, is already
archived and citable. This record notes the unarchived draft.

## Options weighed
- **Leave it** (chosen): no code, no new files. The draft's own pages can't be searched or cited.
- **Extract the Nov 7 draft by hand** (`pdfdetach`, manifest line naming 310555's URL and "extracted from"):
  full draft history searchable, but adds a third report version to search, two with matching figures, raising
  the risk of citing a superseded draft; the file has no URL of its own.
- **Extract embedded files automatically in `fetch_sources.py`**: covers future cases and the LRO spreadsheets,
  but the most code (naming, a manifest field for provenance, non-PDF types with no text step), for two cases.

## Revisit when
The Nov 7 draft's funding alternatives need citing (extract that one by hand), or the 146437 LRO chart data
matters, or more PDFs with embedded files turn up (then consider automating).
