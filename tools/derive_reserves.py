#!/usr/bin/env python3
"""Write analysis/derived/reserves.csv: our sums for topics/reserves.md (Education Stability Fund history and scale)."""

import csv
import os

from common import ROOT

DATA = os.path.join(ROOT, "analysis", "data")
OUT = os.path.join(ROOT, "analysis", "derived", "reserves.csv")

with open(os.path.join(DATA, "esf_withdrawals.csv"), encoding="utf-8") as f:
    withdrawals = list(csv.DictReader(f))
with open(os.path.join(DATA, "reserves.csv"), encoding="utf-8") as f:
    esf_end_2025_27 = next(
        r for r in csv.DictReader(f) if r["fund"] == "Education Stability Fund" and r["as_of"].startswith("2027-06")
    )

PPS_ASK = 500.0  # $ million, PPS's request to buy down PERS rates statewide [NEWS:NEWS-20261102-opb-1]
balance = float(esf_end_2025_27["amount_billion"]) * 1000

total = sum(float(r["amount_million"]) for r in withdrawals)
out = [
    (
        "esf_withdrawals_total",
        round(total, 1),
        "$M",
        "derived",
        "Total of the Education Stability Fund allocations the Legislative Fiscal Office lists, 2001-03 to 2019-21 (nine allocations)",
        "sum of amount_million",
        "data/esf_withdrawals.csv",
        "dollars as listed, not adjusted for inflation",
    ),
    (
        "pps_ask_share_of_esf",
        round(100 * PPS_ASK / balance),
        "%",
        "derived",
        "Portland Public Schools' $500 million request as a share of the fund's projected balance at the end of 2025-27",
        "500 / projected balance",
        "data/reserves.csv (Education Stability Fund, 2027-06); NEWS:NEWS-20261102-opb-1",
        "the balance is a forecast (December 2026), not a cash figure",
    ),
]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"])
    w.writerows(out)
