import json
import unittest

from helpers import ArchiveTest


class Search(ArchiveTest):
    def test_sources(self):
        r = self.run_tool("search.py", "school fund", "--kind", "src")
        assert "[SRC:gov/test_page.html]" in r.stdout, r.stdout + r.stderr

    def test_kinds(self):
        # the archive's own files: each row's kind says what it is, and front matter is its own uncited row
        self.write(
            "analysis/topics/k.md",
            "---\nsummary: >\n  Zebra short.\n---\n# K\n\n## Analysis\n\nZebra guess.\n\n## What the sources say\n\n"
            "- Zebra fact [SRC:gov/test_page.html].\n- Analysis: zebra aside.\n",
        )
        self.write("analysis/derived/k.csv", "id,value,label\nz1,5,zebra sum\n")
        r = self.run_tool("search.py", "zebra", "--json")
        got = {(h["kind"], h["cite"]) for h in json.loads(r.stdout)}
        assert got == {
            ("summary", "analysis/topics/k.md front matter"),
            ("analysis", "analysis/topics/k.md:9 (Analysis)"),
            ("cited", "analysis/topics/k.md:13 (What the sources say)"),
            ("analysis", "analysis/topics/k.md:14 (What the sources say)"),
            ("derived", "[DER:k/z1]"),
        }, got
        r = self.run_tool("search.py", "zebra", "--kind", "cited", "--kind", "derived")
        assert "k.md:13" in r.stdout and "[DER:k/z1]" in r.stdout and "k.md:9" not in r.stdout, r.stdout

    def test_video_transcript(self):
        # search cites the line's timestamp and the transcript header isn't indexed
        self.write("sources/legislature/video/h.mp4", "x")
        self.write(
            "sources/legislature/video/h.mp4.txt",
            "# Machine transcript, verify quotes\n0:00:02 Good morning.\n1:02:05 We have to be bold on schools.\n",
        )
        r = self.run_tool("search.py", "bold", "--kind", "src")
        assert "[VID:legislature/video/h@1:02:05]" in r.stdout and "@0:00:02" not in r.stdout, r.stdout
        assert self.run_tool("search.py", "verify").stdout.strip() == "no matches"


if __name__ == "__main__":
    unittest.main()
