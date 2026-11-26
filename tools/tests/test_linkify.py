import unittest

from helpers import ArchiveTest


class Linkify(ArchiveTest):
    def test_src_and_news_links(self):
        path = self.write(
            "analysis/a.md", "Good [SRC:gov/test_page.html] pending [SRC:gov/not_fetched.pdf p.2] news [NEWS:NEWS-1]\n"
        )
        r = self.run_tool("linkify.py", path)
        assert f"[SRC:gov/test_page.html]({self.url})" in r.stdout, r.stdout
        assert "[NEWS:NEWS-1](https://e.x/a)" in r.stdout and f"({self.url}/x#page=2)" in r.stdout, r.stdout

    def test_derived_link(self):
        self.write(
            "analysis/derived/t.csv",
            "id,value,unit,kind,label,method,inputs,assumptions\nn,1,x,derived,N,sum,data/x.csv,\n",
        )
        path = self.write("analysis/notes.md", "About 1 (our sum [DER:t/n]).\n")
        r = self.run_tool("linkify.py", path)
        link = "[DER:t/n](https://github.com/pietvanzoen/fund-oregon-schools/blob/main/analysis/derived/t.csv)"
        assert link in r.stdout, r.stdout


if __name__ == "__main__":
    unittest.main()
