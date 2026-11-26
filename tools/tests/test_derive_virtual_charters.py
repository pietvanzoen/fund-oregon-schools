"""Expected values are worked out by hand from the fixture below, not copied from the script's output.

The fixture has three charters in ODE's report (A = Baker Web Academy, 4728; B = Oregon Charter Academy, 4399;
C = one Prairie City charter) and one listed charter missing from it (D). Rows using the statewide constants
copied into the script use those constants."""

import unittest

from helpers import ArchiveTest

REPORT = """institution_id,virtual_charter,sponsor_district,admr_2024_25,admr_2025_26,admw_2024_25,admw_2025_26,ode_separate_extended_admw,sponsor_admw_separated,sponsor_gpg_per_ext_admw_2025_26,sponsor_charter_rate_2025_26,note,source
4728,A,Baker SD 5J,900,1000,1100,1200,1200,Yes,10000,8000,,x
4399,B,Santiam Canyon SD 129J,2800,3000,3300,3500,3500,Yes,9000,9000,,x
9001,C,Prairie City SD 4,1000,1314.25,1200,1300,1650,No,10000,10000,,x
"""
GRADE_COLS = ["fall_2025_k"] + [f"fall_2025_g{n}" for n in range(1, 13)]
# id: (grade 1 headcount, grade 9 headcount); every other grade is 0
GRADES = {"4728": (80, 20), "4399": (50, 50), "9001": (100, 0), "9002": (40, 0)}
HS_ADMW = """institution_id,virtual_charter,sponsor_district,hs_admw_9_12,note,source
4728,A,Baker SD 5J,300,,x
4399,B,Santiam Canyon SD 129J,1000,,x
9001,C,Prairie City SD 4,,,x
"""


def grades_csv():
    head = "institution_id,virtual_charter,sponsor_district," + ",".join(GRADE_COLS) + ",fall_2025_total,source\n"
    rows = []
    for iid, (g1, g9) in GRADES.items():
        counts = [0] * len(GRADE_COLS)
        counts[1], counts[9] = g1, g9
        rows.append(f"{iid},X,Y," + ",".join(map(str, counts)) + f",{g1 + g9},x\n")
    return head + "".join(rows)


class DeriveVirtualCharters(ArchiveTest):
    fetch = False

    def setUp(self):
        super().setUp()
        self.write("analysis/data/virtual_charters_2025-26.csv", REPORT)
        self.write("analysis/data/virtual_charters_grades_2025-26.csv", grades_csv())
        self.write("analysis/data/virtual_charters_hs_admw_2024-25.csv", HS_ADMW)
        self.rows = self.derive("virtual_charters")
        self.got = {k: r["value"] for k, r in self.rows.items()}

    def test_values(self):
        # GPG attributable: A 1,200 x 10,000 = 12.0M; B 3,500 x 9,000 = 31.5M; C 1,650 x 10,000 = 16.5M
        # K-8 shares: A 0.8, B 0.5, C 1.0 -> kept at the minimum: A 12.0M x 0.17, B 31.5M x 0.125, C 16.5M x 0.2
        # Baker: grant 1,200 x 8,000 = 9.6M; passed through 0.8 x 0.80 + 0.2 x 0.95 = 0.83
        expected = {
            "charter_count_2025_26": 3,
            "sponsor_count_2025_26": 3,
            "sponsors_separated_2025_26": 2,
            "sponsors_not_separated_2025_26": 1,
            "admr_total_2025_26": 5314.25,
            "admr_total_2024_25": 4700,
            "admw_total_2025_26": 6000,
            "admw_total_2024_25": 5600,
            "admr_share_2025_26": 1.0,  # 5,314.25 / 531,425
            "admw_share_2025_26": 0.9,  # 6,000 / 668,444 = 0.898%
            "prairie_city_virtual_admw_2025_26": 1300,
            "gpg_attributable_2025_26": 60.0,
            "gpg_attributable_share_2025_26": 0.76,  # 60M / 7,877,335,941 = 0.762%
            "sponsor_keep_min_2025_26": 3.0,  # 60M x 0.05
            "sponsor_keep_max_2025_26": 12.0,  # 60M x 0.20
            "virtual_charters_listed_2025_26": 4,
            "new_charters_fall_2025_students": 40,  # D
            "k8_headcount_fall_2025": 230,
            "hs_headcount_fall_2025": 70,
            "k8_share_fall_2025": 76.7,  # 230 / 300
            "sponsor_keep_gradesplit_2025_26": 9.3,  # 2.04 + 3.9375 + 3.3
            "orca_keep_at_minimum_2025_26": 3.9,  # 3.9375
            "bwa_keep_under_agreement_2025_26": 1.6,  # 9.6M x 0.17 = 1.632
            "bwa_keep_share_2025_26": 17.0,
            "bwa_passed_through_2025_26": 8.0,  # 9.6M x 0.83 = 7.968
            "hss_listed_charters": 2,
            "hs_admw_share_2024_25": 29.5,  # (300 + 1,000) / (1,100 + 3,300)
            "hs_headcount_share_hss_charters_fall_2025": 35.0,  # (20 + 50) / (100 + 100)
            "orca_formula_revenue_2025_26": 31.5,
        }
        # North Bend's and Scio's rows divide two constants copied from ODE's estimates: nothing to work out here
        assert set(self.got) - set(expected) == {"north_bend_gpg_per_current_admw", "scio_gpg_per_current_admw"}
        for k, v in expected.items():
            with self.subTest(k):
                self.assertAlmostEqual(self.got[k], v, places=6)

    def test_invariants(self):
        g = self.got
        # the grade-split estimate sits between the all-9-12 and all-K-8 bounds
        assert g["sponsor_keep_min_2025_26"] <= g["sponsor_keep_gradesplit_2025_26"] <= g["sponsor_keep_max_2025_26"]
        # what Baker kept and passed through add up to its grant (each rounded to 0.1M)
        assert abs(g["bwa_keep_under_agreement_2025_26"] + g["bwa_passed_through_2025_26"] - 9.6) <= 0.1
        assert all(self.rows[k]["kind"] == "est" for k in self.rows if "keep" in k), "estimates rest on assumptions"


if __name__ == "__main__":
    unittest.main()
