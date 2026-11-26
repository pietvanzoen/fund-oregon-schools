import unittest

from helpers import ArchiveTest


class CheckSources(ArchiveTest):
    def test_clean(self):
        r = self.run_tool("check_sources.py")
        assert r.returncode == 0 and "0 errors" in r.stdout, r.stdout

    def test_errors(self):
        self.write(
            "sources/_queue.csv",
            "https://www.opb.org/article/x/,gov/news_copy.html,News,,gov,\n"
            "https://www.oregon.gov/x.pdf,misc/x.pdf,Bad folder,,gov,\n",
            mode="a",
        )
        self.write("sources/gov/hand_added.pdf", "x")
        r = self.run_tool("check_sources.py")
        assert r.returncode == 1 and r.stdout.count("ERROR") == 3, r.stdout
        assert "news site" in r.stdout and "must start with" in r.stdout and "no line in" in r.stdout, r.stdout


if __name__ == "__main__":
    unittest.main()
