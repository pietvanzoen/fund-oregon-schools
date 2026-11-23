#!/usr/bin/env python3
"""Write analysis/derived/csl.csv: our sums and estimates for the current-service-level section of
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
CORE_GRANTS_2025_27 = 2202344784  # JPEA's subtotal of state grant-in-aid for core K-12, 2025-27 [SRC:legislature/olis/2025I1/310959_jpea-adequacy-report.pdf p.29]

assert STATUS_QUO - SSF_CSL == NON_SSF  # the report's three figures add up
B = lambda x: round(x / 1e9, 2)
sia_seia = SIA_2027_29 + SEIA_2027_29
with_grants = SSF_CSL + CORE_GRANTS_2025_27
grants_assume = ("the grant programs the joint committee counted as core K-12 funding in 2025-27 continue at the same "
                 "dollar amounts in 2027-29 (no inflation, no cuts); the Quality Education Model's status quo costs "
                 "include the activities those grants pay for; mixes a 2025-27 budget figure with 2027-29 estimates")

out = [
    ("sia_seia_2027_29", B(sia_seia), "$B", "derived",
     "Corporate Activity Tax money forecast for the Student Investment Account and the Statewide Education "
     "Initiatives Account, 2027-29", "SIA + SEIA distributions", OEA,
     "a revenue forecast, not an appropriation; the Statewide Education Initiatives Account also pays for programs "
     "run by the state, not only grants to districts"),
    ("sia_seia_minus_non_ssf", B(sia_seia - NON_SSF), "$B", "derived",
     "Forecast SIA + SEIA money above the model's non-SSF remainder, 2027-29",
     "(SIA + SEIA) - non-SSF remainder", f"{OEA}; {QEM}", "same as sia_seia_2027_29"),
    ("csl_plus_core_grants", B(with_grants), "$B", "est",
     "State School Fund current service level plus the 2025-27 core K-12 grants at the same amounts",
     "SSF CSL 2027-29 + core grant subtotal 2025-27", f"{QEM}; {JPEA}", grants_assume),
    ("csl_plus_core_grants_minus_status_quo", B(with_grants - STATUS_QUO), "$B", "est",
     "That total above the model's 2027-29 status quo", "(SSF CSL + core grants) - status quo",
     f"{QEM}; {JPEA}", grants_assume),
]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"])
    w.writerows(out)
