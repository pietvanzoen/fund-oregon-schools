import unittest

import helpers  # noqa: F401  (puts tools/ on the path)
from common import front_matter


class FrontMatter(unittest.TestCase):
    def test_parses(self):
        assert front_matter("# T\n") == ({}, "# T\n")
        assert front_matter("---\nsummary: >\n  One two.\n  Three.\nk: v\n---\n# T\nx") == (
            {"summary": "One two. Three.", "k": "v"},
            "# T\nx",
        )

    def test_rejects(self):
        for bad in (
            "---\nk: v\n# T\n",
            '---\nk: "q"\n---\n',
            "---\nk: [a]\n---\n",
            "---\nk: a: b\n---\n",
            "---\nk: |\n  x\n---\n",
            "---\nk: >\n---\n",
            "---\nk: >\n  a\n\n  b\n---\n",
            "---\n- a\n---\n",
            "---\nk: v\nk: w\n---\n",
            "---\nk: v # c\n---\n",
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                front_matter(bad)


if __name__ == "__main__":
    unittest.main()
