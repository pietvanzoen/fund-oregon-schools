import unittest

import helpers  # noqa: F401  (puts tools/ on the path)
from next_issue import pick


class Pick(unittest.TestCase):
    def test_pick(self):
        iss = {
            1: ("open", ["auto", "blocked"]),
            2: ("closed", ["auto"]),
            3: ("open", ["auto"]),
            4: ("open", ["auto"]),
            5: ("open", []),
            6: ("open", ["auto"]),
            7: ("open", ["auto", "in progress"]),
            8: ("open", ["auto"]),
        }
        get = lambda n: {"state": iss[n][0], "labels": iss[n][1]}
        subs = {6: [7, 8]}
        q = "1. #1 Blocked\n2. #2 Closed\n3. #3 Has a PR\n 4. #4 Has a branch\n5. #5 Not auto\n6. #6 Split\n"
        assert pick(q, get, lambda n: subs.get(n, []), ["Fixes x.\n\nCloses #3"], ["claude/issue-4-x"]) == 8
        assert pick(q, get, lambda n: [], ["closes #30"], []) == 3  # #30 doesn't close #3
        assert pick("no list", get, lambda n: [], [], []) is None


if __name__ == "__main__":
    unittest.main()
