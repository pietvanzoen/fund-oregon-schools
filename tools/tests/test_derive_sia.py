"""Expected values are worked out by hand from the fixture below, not copied from the script's output."""

import unittest

from helpers import ArchiveTest

DATA = """school_year,allocated,spent,health_safety,well_rounded,reduced_class_size,source
2020-21,100000000,90000000,30000000,20000000,10000000,x
2021-22,200000000,200000000,50000000,50000000,50000000,x
2024-25,300000000,250000000,100000000,50000000,50000000,x
"""


class DeriveSia(ArchiveTest):
    fetch = False

    def test_values(self):
        self.write("analysis/data/sia_spending.csv", DATA)
        got = {k: r["value"] for k, r in self.derive("sia").items()}
        assert got == {
            "spent_total_2020_25": 0.54,  # (90 + 200 + 250) million
            "allocated_total_2020_25": 0.6,  # (100 + 200 + 300) million
            "spent_growth_2021_22_to_2024_25": 25.0,  # 250 / 200 - 1
            "big3_share_2024_25": 80.0,  # (100 + 50 + 50) / 250
        }, got


if __name__ == "__main__":
    unittest.main()
