#!/usr/bin/env python3
"""Write analysis/derived/virtual_charters.csv: our sums, shares and estimates for topics/virtual-charters.md."""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = "data/virtual_charters_2025-26.csv"
OUT = os.path.join(ROOT, "analysis", "derived", "virtual_charters.csv")
EST = "ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf"

# Statewide 2025-26 totals and North Bend's grant, copied from ODE's May 1, 2026 estimates.
STATE_ADMR = 531425  # [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.1]
STATE_ADMW = 668444  # [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.1]
DISTRICT_SHARE = 7877335941  # school district share (95.50%) of formula revenue [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.1]
NB_GPG = 36777648.12  # North Bend SD 13 General Purpose Grant [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.32]
NB_ADMW_2025_26 = 3194.12  # North Bend SD 13 2025-26 ADMw (current year) [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.32]
SCIO_GPG = 27800843.40  # Scio SD 95 General Purpose Grant [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.118]
SCIO_ADMW_2025_26 = 2356.76  # Scio SD 95 2025-26 ADMw (current year) [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.118]
# Statutory minimum pass-through to a district-sponsored charter: 80% (K-8), 95% (9-12) [SRC:legislature/ors/ors338.html]
MIN_PASS_K8, MIN_PASS_HS = 0.80, 0.95

rows = list(csv.DictReader(open(os.path.join(ROOT, "analysis", DATA), newline="", encoding="utf-8")))
GRADES = "data/virtual_charters_grades_2025-26.csv"
grades = {r["institution_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "analysis", GRADES), newline="", encoding="utf-8"))}
K8 = ["fall_2025_k"] + [f"fall_2025_g{n}" for n in range(1, 9)]
HS = [f"fall_2025_g{n}" for n in range(9, 13)]
k8 = lambda iid: sum(int(grades[iid][c]) for c in K8)
hs = lambda iid: sum(int(grades[iid][c]) for c in HS)
in_report = [r["institution_id"] for r in rows]
col = lambda k: [float(r[k]) for r in rows]
sponsors = {r["sponsor_district"]: r["sponsor_admw_separated"] for r in rows}

attributable = sum(float(r["ode_separate_extended_admw"]) * float(r["sponsor_gpg_per_ext_admw_2025_26"]) for r in rows)
keep_split = sum(float(r["ode_separate_extended_admw"]) * float(r["sponsor_gpg_per_ext_admw_2025_26"])
                 * (k8(r["institution_id"]) * (1 - MIN_PASS_K8) + hs(r["institution_id"]) * (1 - MIN_PASS_HS))
                 / (k8(r["institution_id"]) + hs(r["institution_id"])) for r in rows)
est_assume = ("money follows each sponsor's average General Purpose Grant per extended ADMw; mixes state and local "
              "formula revenue; excludes transportation and high-cost disability grants; covers only the 20 charters in "
              "ODE's 2025-26 report")
keep_common = ("every contract pays exactly the statutory minimum for a district sponsor; ignores the lower special-education "
               "minimums (ORS 338.165(2), which a district and charter may renegotiate case by case under 338.165(4)), which "
               "could let sponsors keep more; the pass-through applies to current-year "
               "ADMw but the estimate uses extended ADMw; " + est_assume)
keep_assume = ("all students K-8 (high end) or all 9-12 (low end), because the report has no grade split; "
               + keep_common)
share_assume = (est_assume + "; the denominator also includes transportation, high-cost disability grants and the "
                "educator advancement fund, which the numerator leaves out, so the share is understated")

out = [
    ("charter_count_2025_26", len(rows), "schools", "derived", "Virtual charters in ODE's 2025-26 transparency report",
     "count of rows", DATA, ""),
    ("sponsor_count_2025_26", len(sponsors), "districts", "derived", "Sponsoring districts in the 2025-26 report",
     "count of distinct sponsor_district", DATA, ""),
    ("sponsors_separated_2025_26", sum(v == "Yes" for v in sponsors.values()), "districts", "derived",
     "Sponsors whose virtual charter ADMw ODE calculates separately", "count of sponsors with sponsor_admw_separated = Yes", DATA, ""),
    ("sponsors_not_separated_2025_26", sum(v == "No" for v in sponsors.values()), "districts", "derived",
     "Sponsors whose virtual charter ADMw ODE does not calculate separately", "count of sponsors with sponsor_admw_separated = No", DATA, ""),
    ("admr_total_2025_26", round(sum(col("admr_2025_26")), 2), "students (ADMr)", "derived",
     "Virtual charter ADMr 2025-26", "sum of admr_2025_26", DATA, ""),
    ("admr_total_2024_25", round(sum(col("admr_2024_25")), 2), "students (ADMr)", "derived",
     "Virtual charter ADMr 2024-25", "sum of admr_2024_25", DATA, ""),
    ("admw_total_2025_26", round(sum(col("admw_2025_26")), 2), "ADMw", "derived",
     "Virtual charter ADMw 2025-26", "sum of admw_2025_26", DATA, ""),
    ("admw_total_2024_25", round(sum(col("admw_2024_25")), 2), "ADMw", "derived",
     "Virtual charter ADMw 2024-25", "sum of admw_2024_25", DATA, ""),
    ("admr_share_2025_26", round(100 * sum(col("admr_2025_26")) / STATE_ADMR, 2), "percent", "derived",
     "Virtual charters' share of statewide ADMr 2025-26", "admr_total_2025_26 / statewide ADMr 531,425",
     f"{DATA}; {EST} p.1", ""),
    ("admw_share_2025_26", round(100 * sum(col("admw_2025_26")) / STATE_ADMW, 2), "percent", "derived",
     "Virtual charters' share of statewide ADMw 2025-26", "admw_total_2025_26 / statewide ADMw 668,444",
     f"{DATA}; {EST} p.1", ""),
    ("prairie_city_virtual_admw_2025_26",
     round(sum(float(r["admw_2025_26"]) for r in rows if r["sponsor_district"] == "Prairie City SD 4"), 2), "ADMw",
     "derived", "Prairie City's two virtual charters, 2025-26 ADMw", "sum of admw_2025_26 for Prairie City SD 4", DATA, ""),
    ("gpg_attributable_2025_26", round(attributable / 1e6, 1), "USD millions", "est",
     "Formula revenue attributable to virtual charters 2025-26",
     "sum over charters of ode_separate_extended_admw x sponsor_gpg_per_ext_admw_2025_26", DATA, est_assume),
    ("gpg_attributable_share_2025_26", round(100 * attributable / DISTRICT_SHARE, 2), "percent", "est",
     "Estimate as a share of the school district share of 2025-26 formula revenue",
     "gpg_attributable_2025_26 / district share $7,877,335,941", f"{DATA}; {EST} p.1", share_assume),
    ("sponsor_keep_min_2025_26", round(attributable * (1 - MIN_PASS_HS) / 1e6, 1), "USD millions", "est",
     "What sponsors would keep at the statutory minimum, low end", "gpg_attributable_2025_26 x (1 - 0.95)",
     f"{DATA}; legislature/ors/ors338.html", keep_assume),
    ("sponsor_keep_max_2025_26", round(attributable * (1 - MIN_PASS_K8) / 1e6, 1), "USD millions", "est",
     "What sponsors would keep at the statutory minimum, high end", "gpg_attributable_2025_26 x (1 - 0.80)",
     f"{DATA}; legislature/ors/ors338.html", keep_assume),
    ("north_bend_gpg_per_current_admw", round(NB_GPG / NB_ADMW_2025_26), "USD per ADMw", "derived",
     "North Bend General Purpose Grant divided by current-year ADMw", "36,777,648.12 / 3,194.12", f"{EST} p.32", ""),
    ("virtual_charters_listed_2025_26", len(grades), "schools", "derived",
     "Virtual charters on ODE's 2025-26 charter school list", "count of rows", GRADES, ""),
    ("new_charters_fall_2025_students", sum(int(g["fall_2025_total"]) for i, g in grades.items() if i not in in_report),
     "students (headcount)", "derived", "Fall 2025 enrollment of listed virtual charters missing from the transparency report",
     "sum of fall_2025_total for institution_ids not in the transparency report", f"{GRADES}; {DATA}", ""),
    ("k8_headcount_fall_2025", sum(k8(i) for i in in_report), "students (headcount)", "derived",
     "K-8 enrollment, Oct 1 2025, of the 20 charters in the transparency report", "sum of K-8 grade columns", GRADES, ""),
    ("hs_headcount_fall_2025", sum(hs(i) for i in in_report), "students (headcount)", "derived",
     "Grades 9-12 enrollment, Oct 1 2025, of the 20 charters in the transparency report", "sum of grade 9-12 columns", GRADES, ""),
    ("k8_share_fall_2025", round(100 * sum(k8(i) for i in in_report) / sum(k8(i) + hs(i) for i in in_report), 1), "percent",
     "derived", "K-8 share of fall 2025 enrollment, 20 charters in the transparency report",
     "k8_headcount_fall_2025 / (k8 + hs headcount)", GRADES, ""),
    ("sponsor_keep_gradesplit_2025_26", round(keep_split / 1e6, 1), "USD millions", "est",
     "What sponsors would keep at the statutory minimum, using each school's fall 2025 grade split",
     "sum over charters of ode_separate_extended_admw x sponsor GPG x (K-8 share x 0.20 + 9-12 share x 0.05)",
     f"{DATA}; {GRADES}; legislature/ors/ors338.html",
     "each school's Oct 1 headcount split by grade stands in for its ADMw split (special education and other weights "
     "may differ by grade); " + keep_common),
    ("orca_keep_at_minimum_2025_26", round(next(
        float(r["ode_separate_extended_admw"]) * float(r["sponsor_gpg_per_ext_admw_2025_26"])
        * (k8(r["institution_id"]) * (1 - MIN_PASS_K8) + hs(r["institution_id"]) * (1 - MIN_PASS_HS))
        / (k8(r["institution_id"]) + hs(r["institution_id"])) for r in rows if r["institution_id"] == "4399") / 1e6, 1),
     "USD millions", "est", "What Santiam Canyon would keep from Oregon Charter Academy at the statutory minimum",
     "Oregon Charter Academy's ode_separate_extended_admw x Santiam Canyon GPG x (K-8 share x 0.20 + 9-12 share x 0.05)",
     f"{DATA}; {GRADES}; legislature/ors/ors338.html",
     "Oregon Charter Academy's Oct 1 headcount split by grade stands in for its ADMw split; " + keep_common),
    ("scio_gpg_per_current_admw", round(SCIO_GPG / SCIO_ADMW_2025_26), "USD per ADMw", "derived",
     "Scio General Purpose Grant divided by current-year ADMw", "27,800,843.40 / 2,356.76", f"{EST} p.118", ""),
]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"])
    w.writerows(out)
