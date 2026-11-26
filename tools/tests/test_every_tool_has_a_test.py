import os
import unittest

from helpers import TOOLS


class EveryToolHasATest(unittest.TestCase):
    def test_test_files(self):
        here = os.path.dirname(os.path.abspath(__file__))
        tools = {f[:-3] for f in os.listdir(TOOLS) if f.endswith(".py")}
        missing = sorted(t for t in tools if not os.path.exists(os.path.join(here, f"test_{t}.py")))
        assert not missing, f"no tools/tests/test_<tool>.py for: {', '.join(missing)} (.claude/rules/code.md, Tests)"


if __name__ == "__main__":
    unittest.main()
