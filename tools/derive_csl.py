#!/usr/bin/env python3
"""Write analysis/derived/csl.csv: our sums for the current-service-level section of
topics/quality-education-model.md (what the Quality Education Model's ~$1.2B of non-SSF state money is)."""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "analysis", "derived", "csl.csv")
QEM = "ode/qec/2026_qem_report.pdf p.103"
OEA = "fiscal/oea/2026-12_forecast.pdf p.75"
JPEA = "legislature/olis/2025I1/310959_jpea-adequacy-report.pdf p.29"

STATUS_QUO = 13775890564  # QEM status quo state funding requirement, 2027-29 [SRC:ode/qec/2026_qem_report.pdf p.103]
SSF_CSL = 12558429348  # DAS State School Fund CSL incl. SSA transfer, 2027-29 [SRC:ode/qec/2026_qem_report.pdf p.103]
NON_SSF = 1217461216  # remaining non-SSF state funds for status quo, 2027-29 [SRC:ode/qec/2026_qem_report.pdf p.103]
SIA_2027_29 = 1250.421e6  # CAT distribution to the Student Investment Account, Dec. 2026 forecast [SRC:fiscal/oea/2026-12_forecast.pdf p.75]
SEIA_2027_29 = 750.253e6  # CAT distribution to the Statewide Education Initiatives Account [SRC:fiscal/oea/2026-12_forecast.pdf p.75]
# Fund for Student Success (CAT) column of the same table: SIA, High School Success, Early Literacy, Hunger Free
# Schools, specialized student services [SRC:legislature/olis/2025I1/310959_jpea-adequacy-report.pdf p.29]
CORE_GRANTS_CAT = [1109828482, 199151203, 93780000, 127345728, 124214759]

assert STATUS_QUO - SSF_CSL == NON_SSF  # the report's three figures add up
B = lambda x: round(x / 1e9, 2)
sia_seia = SIA_2027_29 + SEIA_2027_29

out = [
    ("sia_seia_2027_29", B(sia_seia), "$B", "derived",
     "Corporate Activity Tax money forecast for the Student Investment Account and the Statewide Education "
     "Initiatives Account, 2027-29", "SIA + SEIA distributions", OEA,
     "a revenue forecast, not an appropriation; the Statewide Education Initiatives Account also pays for statewide "
     "initiatives and educator professional development, not only grants to districts"),
    ("sia_seia_minus_non_ssf", B(sia_seia - NON_SSF), "$B", "derived",
     "Forecast SIA + SEIA money above the model's non-SSF remainder, 2027-29",
     "(SIA + SEIA) - non-SSF remainder", f"{OEA}; {QEM}", "same as sia_seia_2027_29"),
    ("core_grants_cat", B(sum(CORE_GRANTS_CAT)), "$B", "derived",
     "Corporate Activity Tax (Fund for Student Success) share of the 2025-27 core K-12 grants the joint committee listed",
     "sum of the FSS (CAT) column", JPEA, ""),
]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"])
    w.writerows(out)
