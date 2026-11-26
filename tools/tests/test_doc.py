import unittest

from helpers import ArchiveTest


class Doc(ArchiveTest):
    def test_grep(self):
        r = self.run_tool("doc.py", "test_page", "--grep", "billion")
        assert "13 billion" in r.stdout, r.stdout + r.stderr


if __name__ == "__main__":
    unittest.main()
