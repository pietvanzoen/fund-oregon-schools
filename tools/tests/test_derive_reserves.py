"""Expected values are worked out by hand from the fixtures below, not copied from the script's output."""

import unittest

from helpers import ArchiveTest

WITHDRAWALS = """id,budget_period,amount_million,purpose,source
a,2001-03,150.0,x,x
b,2009-11,84.3,x,x
c,2019-21,400.0,x,x
"""
RESERVES = """fund,amount_billion,as_of,conditions_to_use,note,source
Education Stability Fund,1.012,2025-07-01 (balance),x,x,x
Education Stability Fund,1.25,2027-06 (projected end of 2025-27),x,x,x
"""


class DeriveReserves(ArchiveTest):
    fetch = False

    def test_values(self):
        self.write("analysis/data/esf_withdrawals.csv", WITHDRAWALS)
        self.write("analysis/data/reserves.csv", RESERVES)
        got = {k: r["value"] for k, r in self.derive("reserves").items()}
        assert got == {
            "esf_withdrawals_total": 634.3,  # 150.0 + 84.3 + 400.0
            "pps_ask_share_of_esf": 40.0,  # 500 / 1,250, using the 2027-06 row, not the 2025-07 balance
        }, got


if __name__ == "__main__":
    unittest.main()
