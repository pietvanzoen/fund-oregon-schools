"""Only the page selection is tested: the OCR itself shells out to pdfimages and tesseract, which run in
GitHub Actions only."""

import unittest

import helpers  # noqa: F401  (puts tools/ on the path)
from ocr_pdfs import MIN_CHARS, pages_to_ocr


class PagesToOcr(unittest.TestCase):
    def test_picks_pages(self):
        # p.1 picture-only slide, p.2 text-rich page with a logo, p.3 blank page without an image
        assert pages_to_ocr(["Title", "x" * MIN_CHARS, ""], {1, 2}) == [1]
        assert pages_to_ocr(["  a b  " * 5, ""], {1}) == [1]


if __name__ == "__main__":
    unittest.main()
