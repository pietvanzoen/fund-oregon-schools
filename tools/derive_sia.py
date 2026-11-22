#!/usr/bin/env python3
"""Write analysis/derived/sia.csv: our sums and changes for topics/student-investment-account.md."""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = "data/sia_spending.csv"
OUT = os.path.join(ROOT, "analysis", "derived", "sia.csv")

rows = {r["school_year"]: r for r in csv.DictReader(open(os.path.join(ROOT, "analysis", DATA), newline="", encoding="utf-8"))}
val = lambda y, k: int(rows[y][k])
years = sorted(rows)
spent = sum(val(y, "spent") for y in years)
alloc = sum(val(y, "allocated") for y in years)
big3 = lambda y: val(y, "health_safety") + val(y, "well_rounded") + val(y, "reduced_class_size")

out = [
    ("spent_total_2020_25", round(spent / 1e9, 3), "$B", "derived",
     f"SIA spending reported by grantees, {years[0]} to {years[-1]}", "sum of spent", DATA,
     "each year as ODE extracted it for that year's report; 2021-22 and 2022-23 were extracted before every grantee's spending was final"),
    ("allocated_total_2020_25", round(alloc / 1e9, 3), "$B", "derived",
     f"SIA allocations, {years[0]} to {years[-1]}", "sum of allocated", DATA, ""),
    ("spent_growth_2021_22_to_2024_25", round(100 * (val("2024-25", "spent") / val("2021-22", "spent") - 1), 1), "%", "derived",
     "Change in yearly SIA spending, 2021-22 to 2024-25 (not adjusted for inflation)",
     "spent 2024-25 / spent 2021-22 - 1", DATA, ""),
    ("big3_share_2024_25", round(100 * big3("2024-25") / val("2024-25", "spent"), 1), "%", "derived",
     "Share of 2024-25 SIA spending on health and safety, well-rounded education and smaller classes",
     "(health_safety + well_rounded + reduced_class_size) / spent, 2024-25", DATA, ""),
]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"])
    w.writerows(out)
