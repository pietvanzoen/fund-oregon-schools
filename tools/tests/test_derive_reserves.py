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
FORECASTS = """id,forecast,released,gross_gf_revenue_million,cos_gross_gf_revenue_million,gross_change_from_cos_million,net_available_resources_million,cos_net_available_resources_million,resources_change_from_cos_million,source
a,A,x,980,1000,-20,975,1000,-25,x
b,B,x,1010,1000,10,1000,1000,0,x
"""
NEXT = """id,forecast,next_biennium,next_biennium_net_revenue_million,current_biennium,current_appropriations_million,source
n,N,2027-29,1100,2025-27,1000,x
"""


class DeriveReserves(ArchiveTest):
    fetch = False

    def test_values(self):
        self.write("analysis/data/esf_withdrawals.csv", WITHDRAWALS)
        self.write("analysis/data/reserves.csv", RESERVES)
        self.write("analysis/data/esf_trigger_forecasts.csv", FORECASTS)
        self.write("analysis/data/esf_next_biennium_test.csv", NEXT)
        got = {k: r["value"] for k, r in self.derive("reserves").items()}
        assert got == {
            "esf_withdrawals_total": 634.3,  # 150.0 + 84.3 + 400.0
            "pps_ask_share_of_esf": 40.0,  # 500 / 1,250, using the 2027-06 row, not the 2025-07 balance
            "esf_2pct_gross_a": 2.0,  # decline: 20 / 1,000
            "esf_2pct_resources_a": 2.5,  # decline: 25 / 1,000
            "esf_2pct_gross_b": -1.0,  # 10 above 1,000
            "esf_2pct_resources_b": 0.0,  # -0.0 compares equal
            "esf_2pct_gross_max_decline": 2.0,  # forecast A
            "esf_3pct_n": 10.0,  # 1,100 / 1,000 - 1
        }, got


if __name__ == "__main__":
    unittest.main()
