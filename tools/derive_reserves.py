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
# Education Stability Fund triggers, Oregon Constitution Art. XV sec. 4(6)(a) [SRC:legislature/constitution/oregon-constitution.html]
with open(os.path.join(DATA, "esf_trigger_forecasts.csv"), encoding="utf-8") as f:
    forecasts = list(csv.DictReader(f))
for r in forecasts:
    # shown as declines: positive means below the close-of-session forecast
    gross = -100 * float(r["gross_change_from_cos_million"]) / float(r["cos_gross_gf_revenue_million"])
    res = -100 * float(r["resources_change_from_cos_million"]) / float(r["cos_net_available_resources_million"])
    out.append(
        (
            f"esf_2pct_gross_{r['id']}",
            round(gross, 2),
            "%",
            "derived",
            f"{r['forecast']} forecast: decline in 2025-27 gross General Fund revenue from the close-of-session forecast (negative: above it)",
            "-(change from close of session) / close-of-session gross General Fund revenue",
            f"data/esf_trigger_forecasts.csv ({r['id']})",
            "the trigger's test is at least 2% below; gross revenue as printed in the forecast's Table R.1",
        )
    )
    out.append(
        (
            f"esf_2pct_resources_{r['id']}",
            round(res, 2),
            "%",
            "derived",
            f"{r['forecast']} forecast: decline in 2025-27 net available General Fund resources from the close-of-session forecast (negative: above it)",
            "-(change from close of session) / close-of-session net available resources",
            f"data/esf_trigger_forecasts.csv ({r['id']})",
            "resources include the beginning balance and offsets, which are not revenue; shown for comparison",
        )
    )
worst = min(forecasts, key=lambda r: float(r["gross_change_from_cos_million"]) / float(r["cos_gross_gf_revenue_million"]))
out.append(
    (
        "esf_2pct_gross_max_decline",
        round(-100 * float(worst["gross_change_from_cos_million"]) / float(worst["cos_gross_gf_revenue_million"]), 2),
        "%",
        "derived",
        "Largest decline in 2025-27 gross General Fund revenue from the close-of-session forecast, across the 2025-27 quarterly forecasts",
        "largest of the per-forecast declines",
        "data/esf_trigger_forecasts.csv",
        f"the lowest is the {worst['forecast']} forecast",
    )
)
with open(os.path.join(DATA, "esf_next_biennium_test.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        out.append(
            (
                f"esf_3pct_{r['id']}",
                round(100 * (float(r["next_biennium_net_revenue_million"]) / float(r["current_appropriations_million"]) - 1), 1),
                "%",
                "est",
                f"{r['forecast']} forecast: {r['next_biennium']} net General Fund revenue compared with {r['current_biennium']} General Fund appropriations",
                "next-biennium net revenue / current appropriations - 1",
                f"data/esf_next_biennium_test.csv ({r['id']})",
                "net revenue stands in for 'moneys available', leaving out the beginning balance; the trigger uses the last forecast of the budget period (May 2027), not this one",
            )
        )
        out.append(
            (
                f"esf_3pct_drop_needed_{r['id']}",
                round(100 * (1 - 0.97 * float(r["current_appropriations_million"]) / float(r["next_biennium_net_revenue_million"])), 1),
                "%",
                "est",
                f"How far {r['next_biennium']} net General Fund revenue would have to fall from the {r['forecast']} forecast to be 3% below {r['current_biennium']} appropriations",
                "1 - 0.97 x current appropriations / next-biennium net revenue",
                f"data/esf_next_biennium_test.csv ({r['id']})",
                "same stand-in for 'moneys available' as esf_3pct; ignores any change in appropriations",
            )
        )

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"])
    w.writerows(out)
