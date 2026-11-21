# Online charters: State School Fund money that follows students

Issue #20. Copied values: `data/virtual_charters_2025-26.csv`. Our calculations: `derived/virtual_charters.csv`,
written by `tools/derive_virtual_charters.py`.

## What the sources say

### The law (ORS chapter 338)

- A "virtual public charter school" is a public charter school that provides online courses; it does not include a
  charter school that primarily serves students in a physical location [SRC:legislature/ors/ors338.html]
  (ORS 338.005(5)).
- **Students count where the charter is, not where they live.** For State School Fund purposes, charter students
  are treated as residents of the district in which the charter is located, and the SSF money for them is paid
  first to that district [SRC:legislature/ors/ors338.html] (ORS 338.155(1)(a)-(b)).
- **Sponsor's minimum pass-through.** A sponsoring district must contract to pay its charter at least 80% of the
  district's General Purpose Grant per ADMw for students in K-8 and at least 95% for grades 9-12; the two sides may
  agree on more [SRC:legislature/ors/ors338.html] (ORS 338.155(2), (7)). For charters sponsored by the State Board the
  minimum is 90% (K-8) and 95% (9-12), and the district must send half of the unpaid portion to ODE
  [SRC:legislature/ors/ors338.html] (ORS 338.155(3), (5)). For students eligible for special education, the payment
  per ADMw attributable to the student must be at least 40% (K-8) or 47.5% (9-12) of the grant
  [SRC:legislature/ors/ors338.html] (ORS 338.165(2)).
- **Poverty weight is borrowed from the sponsor.** A charter's ADMw assumes the same share of children in poverty
  as the district where it is located [SRC:legislature/ors/ors338.html] (ORS 338.157).
- **Separate calculation for shrinking sponsors.** If a sponsoring district's own enrollment (leaving out the
  virtual charter) fell from the year before, ODE calculates the virtual charter's ADMw separately from the
  district's when working out the district's extended ADMw [SRC:legislature/ors/ors338.html] (ORS
  338.155(1)(c)(C)). ODE publishes this calculation in a "Virtual Charter School Ext ADMw Transparency Report"
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1].
- **The 3% rule.** A student does not need the resident district's approval to enroll in a virtual charter, only to
  give notice of intent and of enrollment. But if more than 3% of a district's resident students already attend
  virtual charters the district does not sponsor, the district may refuse approval; it must then tell the family
  the current percentage, the right to appeal to the State Board, and other online options
  [SRC:legislature/ors/ors338.html] (ORS 338.125(4)-(5)). ODE's guidance dates the option to deny to HB 2301 (2011),
  with timelines adjusted by HB 3204 (2023) [SRC:ode/charter/2026-08_virtual-charter-enrollment-guidance.pdf p.3].
- **No Student Investment Account money.** Virtual charters cannot apply for SIA grants under the Student Success
  Act, and ODE removes their ADMw from their sponsors' SIA allocations; ODE's September 2026 list for 2027-29
  names the virtual charters and their sponsors [SRC:ode/charter/2027-29_sia-virtual-charter-list.pdf p.1].
- ORS 338.155's history note lists its 1999 enactment and amendments through 2025, the latest being 2025 c.386
  [SRC:legislature/ors/ors338.html]. LPRO's 2025 summary says enacted HB 3038 clarified that approved recovery
  schools that are charters are exempt from State School Fund provisions
  [SRC:legislature/lpro/2025_education-legislative-summary.pdf p.19].

### Enrollment and money (2025-26)

- ODE's 2025-26 transparency report (second-period ADM, dated Apr 27, 2026) lists each virtual charter, its
  sponsoring district, and its ADMr and ADMw for 2024-25 and 2025-26
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2]. The values are copied into
  `data/virtual_charters_2025-26.csv`.
- Baker Web Academy has 3,839.73 ADMr in 2025-26, Fossil Charter School 3,294.85 and Oregon Charter Academy
  2,601.34 [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].
- ODE's May 2026 estimate puts statewide ADMr at 531,425 and ADMw at 668,444 for 2025-26
  [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.1].
- The 2026 QEM report counts 52 virtual schools with 27,978 students (5.2%) in 2024-25
  [SRC:ode/qec/2026_qem_report.pdf p.16].
- The report marks "No" for a separate calculation in Prairie City, Paisley, Fossil and Mitchell and "Yes" in the
  other sponsoring districts [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].
- Fossil SD's charter has 3,347.06 ADMw in 2025-26 against 193.00 for the district itself; Prairie City's two
  virtual charters have 1,290.40 and 120.09 against 542.36; Baker SD's has 3,915.32 against 2,241.97
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].
- ODE's estimates give each sponsor's General Purpose Grant per extended ADMw: $10,801 for Mitchell SD
  [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.191] and $11,397 for Paisley SD
  [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.93] in 2025-26. Each district page also shows a "Charter
  Schools Rate (ORS 338.155)", which ODE does not define on the page; for North Bend it is $11,514 against a General
  Purpose Grant per extended ADMw of $11,129 [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.32].
- North Bend's 2025-26 General Purpose Grant is $36,777,648.12, its 2025-26 ADMw 3,194.12 and its extended ADMw
  3,304.67 [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.32].
- Scio's 2025-26 General Purpose Grant is $27,800,843.40, its 2025-26 ADMw 2,356.76, and its Charter Schools Rate
  $11,796 [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.118].
- ODE's 2025-26 total revenue for formula is $8,248,519,310: state revenue for formula of $5,504,883,786 (the
  $5,566,106,000 State School Fund appropriation, part of an $11,359,400,000 2025-27 budget, less transfers and
  deductions) plus local revenue. The school district share is $7,877,335,941, from which high-cost disability
  grants ($55,000,000) and the district share of the educator advancement fund ($6,003,307) are taken before
  distribution [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.1].
- The transparency report does not split virtual charter students between K-8 and 9-12
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].

### What the news reported

- The Oregon Journalism Project's investigation (published Nov 3, 2026 in Willamette Week) says about 31,000
  students, roughly 6% of K-12, are in the state's online programs, that Oregon has 76 virtual schools, and that
  state money follows each student [NEWS:NEWS-20261103-wweek-1].
- Its main example, Nyssa's online program, is set up by the district with a for-profit company; under its
  contract Nyssa kept 40% of the per-student money and the company got 60% [NEWS:NEWS-20261103-wweek-1]. Nyssa
  does not appear in ODE's virtual charter report
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].
- The article says each student who leaves a brick-and-mortar school for a virtual one costs that school more than
  $11,000 [NEWS:NEWS-20261103-wweek-1].
- The article also reports families who say online school works for them [NEWS:NEWS-20261103-wweek-1].
- Kotek's statement to OJP said she "is actively reviewing the state's current approach to virtual education"
  [NEWS:NEWS-20261103-wweek-1].

### Bills (2025 and 2026 sessions)

- OLIS lists each of the six 2025 bills below as still "In House Committee" or "In Senate Committee" with no
  chapter number [SRC:legislature/bills/2025R1_HB3444_overview.html] [SRC:legislature/bills/2025R1_HB2583_overview.html]
  [SRC:legislature/bills/2025R1_HB2144_overview.html] [SRC:legislature/bills/2025R1_SB562_overview.html]
  [SRC:legislature/bills/2025R1_SB633_overview.html] [SRC:legislature/bills/2025R1_SB647_overview.html].

- **HB 3444** (sponsored by Rep. Wright; Boomer Wright in `people/legislators.csv`): As introduced: raise the minimum pass-through to 95% for non-virtual charters only (virtual charters stay at 80% K-8 / 95% 9-12), loosen SIA eligibility for non-virtual charters only, let sponsors keep unpaid amounts but require them to be spent on charter administration, and entitle charters to local, state and federal moneys and transportation grants on the same basis as district schools. The -1 and -2 amendments would have set 95% for all charters, virtual included, and opened SIA grants to virtual charters. The staff summary lists a House Education meeting on Mar 12, 2025. [SRC:legislature/bills/2025R1_HB3444_introduced.pdf p.1] [SRC:legislature/olis/2025R1/294106_hb3444-staff-measure-summary.pdf p.1] [SRC:legislature/bills/2025R1_HB3444_overview.html]
- **HB 2583** (sponsored by Rep. McIntire): Make virtual charters without a for-profit operator eligible for SIA grants; the -1 amendment would have opened SIA to all virtual charters that meet the demographic tests. The staff summary lists House Education meetings on Apr 2 and Apr 7, 2025. [SRC:legislature/bills/2025R1_HB2583_introduced.pdf p.1] [SRC:legislature/olis/2025R1/297340_hb2583-staff-measure-summary.pdf p.1] [SRC:legislature/bills/2025R1_HB2583_overview.html]
- **HB 2144** (sponsored by Rep. McIntire): Change timelines for the 3% rule; have ODE collect virtual charter enrollment data for districts' calculations. [SRC:legislature/bills/2025R1_HB2144_introduced.pdf p.1] [SRC:legislature/bills/2025R1_HB2144_overview.html]
- **SB 562** (sponsored by Sen. Anderson): Remove the 3% approval rule. [SRC:legislature/bills/2025R1_SB562_introduced.pdf p.1] [SRC:legislature/bills/2025R1_SB562_overview.html]
- **SB 633** (sponsored by Sen. Bonham): Remove the 3% approval rule (same summary as SB 562). [SRC:legislature/bills/2025R1_SB633_introduced.pdf p.1] [SRC:legislature/bills/2025R1_SB633_overview.html] [SRC:legislature/bills/2025R1_SB562_introduced.pdf p.1]
- **SB 647** (sponsored by Sen. Bonham, at the request of former Sen. Linthicum): Raise the 3% threshold to 5%. [SRC:legislature/bills/2025R1_SB647_introduced.pdf p.1] [SRC:legislature/bills/2025R1_SB647_overview.html]

- The Legislature's 2025 education session summary marks HB 3444 and HB 2583 as not enacted
  [SRC:legislature/lpro/2025_education-legislative-summary.pdf p.12]
  [SRC:legislature/lpro/2025_education-legislative-summary.pdf p.1].
- 2026 session: ODE's summary of enacted 2026 education legislation mentions no charter or virtual school bill
  [SRC:ode/legislation/2026_summary-enacted-education-legislation.pdf p.1].

## Derived figures

Our own sums, shares and estimates; methods, inputs and assumptions are in `derived/virtual_charters.csv`.
Estimates ("est") rest on the assumptions listed there.

| Figure | Value | Kind | Tag |
|---|---|---|---|
| Virtual charters in ODE's 2025-26 report | 20 | derived | [DER:virtual_charters/charter_count_2025_26] |
| Sponsoring districts | 17 | derived | [DER:virtual_charters/sponsor_count_2025_26] |
| Sponsors with a separate ADMw calculation ("Yes") | 13 | derived | [DER:virtual_charters/sponsors_separated_2025_26] |
| Sponsors without one ("No") | 4 | derived | [DER:virtual_charters/sponsors_not_separated_2025_26] |
| Virtual charter ADMr, 2025-26 | 22,110 | derived | [DER:virtual_charters/admr_total_2025_26] |
| Virtual charter ADMr, 2024-25 | 20,413 | derived | [DER:virtual_charters/admr_total_2024_25] |
| Virtual charter ADMw, 2025-26 | 22,714 | derived | [DER:virtual_charters/admw_total_2025_26] |
| Virtual charter ADMw, 2024-25 | 21,035 | derived | [DER:virtual_charters/admw_total_2024_25] |
| Share of statewide ADMr, 2025-26 | 4.2% | derived | [DER:virtual_charters/admr_share_2025_26] |
| Share of statewide ADMw, 2025-26 | 3.4% | derived | [DER:virtual_charters/admw_share_2025_26] |
| Prairie City's two virtual charters, ADMw 2025-26 | 1,410 | derived | [DER:virtual_charters/prairie_city_virtual_admw_2025_26] |
| Formula revenue attributable to virtual charters, 2025-26 | about $257M | est | [DER:virtual_charters/gpg_attributable_2025_26] |
| That estimate as a share of the school district share of formula revenue | 3.3% | est | [DER:virtual_charters/gpg_attributable_share_2025_26] |
| What sponsors would keep if contracts paid exactly the minimum, low end (all 9-12) | about $13M | est | [DER:virtual_charters/sponsor_keep_min_2025_26] |
| Same, high end (all K-8) | about $51M | est | [DER:virtual_charters/sponsor_keep_max_2025_26] |
| North Bend General Purpose Grant per current-year ADMw | $11,514 | derived | [DER:virtual_charters/north_bend_gpg_per_current_admw] |
| Scio General Purpose Grant per current-year ADMw | $11,796 | derived | [DER:virtual_charters/scio_gpg_per_current_admw] |

The $257M estimate multiplies each virtual charter's extended ADMw in the transparency report by its sponsor's
General Purpose Grant per extended ADMw. It mixes state and local money (the grant is calculated before local
revenue is subtracted), leaves out the transportation grant and high-cost disability grants, and uses each
sponsor's average rate. It is one year of state plus local formula revenue, not State School Fund appropriation.

## Analysis

- **Same rates for online charters.** The law sets no separate rate for virtual charters: online and
  brick-and-mortar charters with the same kind of sponsor have the same minimum payment rates, including the lower
  special-education minimums (the separate ADMw calculation applies only to virtual charters).
- **Size.** Virtual charters are about 4.2% of statewide ADMr [DER:virtual_charters/admr_share_2025_26] and 3.4% of
  ADMw [DER:virtual_charters/admw_share_2025_26]. Their weighted count is close to their raw count. That says little
  about the students themselves: a charter's poverty weight is copied from its sponsor (ORS 338.157, above), and ODE's page doesn't
  say whether the statewide ADMw is current or extended, so the two may not be on the same basis.
- Baker Web Academy, Fossil Charter School and Oregon Charter Academy are the three largest virtual charters by
  ADMr. In several sponsors the virtual charter is most of the district: Fossil, Baker and Prairie City, whose two
  charters total 1,410 ADMw [DER:virtual_charters/prairie_city_virtual_admw_2025_26].
- ODE's later 2027-29 SIA list names Applegate Valley, Jefferson Classical, Lower Columbia and Stellar Pines, which
  are not in the 2025-26 transparency report; if any of them operated in 2025-26, the totals here undercount.
- **Other counts.** The QEM report doesn't say how it defines a virtual school or how it counts students; with 52
  schools against 20 virtual charters [DER:virtual_charters/charter_count_2025_26] it likely includes non-charter
  online schools, so it should not be compared one-for-one with charter ADMr. OJP's figures (about 31,000 students
  in "online programs", 76 virtual schools) are as of the article (Nov 2026) and use its own definitions. The three
  sets of numbers measure different things and are not in conflict.
- **The grant rate.** Across the sponsors the General Purpose Grant per extended ADMw runs from Mitchell's $10,801
  to Paisley's $11,397. The "Charter Schools Rate" equals or exceeds the grant rate on each sponsor's page. For
  North Bend it equals the General Purpose Grant divided by current-year ADMw, $11,514
  [DER:virtual_charters/north_bend_gpg_per_current_admw], rather than extended ADMw; the same holds for Scio, $11,796
  [DER:virtual_charters/scio_gpg_per_current_admw]. That would explain why it is never below the grant rate; not
  confirmed by ODE.
- **No ODE dollar total.** None of the archived ODE documents gives the SSF dollars attributable to virtual
  charters.
- **The money.** Our estimate is about $257M of formula revenue in 2025-26
  [DER:virtual_charters/gpg_attributable_2025_26], roughly 3.3% of the school district share
  [DER:virtual_charters/gpg_attributable_share_2025_26]. The denominator is wider than the estimate: the district share
  also pays transportation, high-cost disability grants and the educator advancement fund, which the estimate leaves
  out, so on a like-for-like basis the share would be a little higher.
- **The sponsors' share.** How much a sponsor keeps depends on each charter contract, which isn't archived, and the
  report has no grade split. A district sponsor keeps whatever it does not pass through. If every contract paid
  exactly the statutory minimum, sponsors would keep between 5% (all high school) and 20% (all K-8) of the grant,
  roughly $13M [DER:virtual_charters/sponsor_keep_min_2025_26] to $51M
  [DER:virtual_charters/sponsor_keep_max_2025_26]. Contracts may pay more than the minimum, which would lower
  that; the pass-through applies to current-year ADMw while the estimate uses extended ADMw, which could raise it a
  little; and the lower special-education minimums (ORS 338.165) mean sponsors could keep more than the high end.
- **Nyssa.** If Nyssa's program is not a charter, the ORS 338.155 pass-through minimums would not govern that
  arrangement.
- **OJP's $11,000.** That is in line with the 2025-26 General Purpose Grant per ADMw ($10,801-$11,397 among virtual
  charter sponsors, above). It is the revenue that moves with the student, not a net cost to the system.
- **Kotek.** As of Nov 20, 2026, no proposal from her on virtual schools is in the archive; her 2027-29 budget is
  due Dec 1 (see `BRIEFING.md`).
- **The bills.** Counting HB 3444's amendments, five of the six 2025 bills would have widened access to or funding for virtual charters; HB 2144
  would have changed how the 3% rule is administered and had ODE collect the enrollment data. Three would have
  loosened the 3% rule. HB 2583 would have opened Student Investment Account grants to some or all virtual
  charters. HB 3444 as introduced was about brick-and-mortar charters; its -1 and -2 amendments would have raised
  the virtual charter minimum to 95% and opened SIA to virtual charters. None left committee.
- **The statute's history.** The HB 3038 change matches ORS 338.155(1)(d); whether that is 2025 c.386 is
  unconfirmed. It does not concern virtual charters. What the 2021, 2023 and 2025 changes did is not yet
  researched.
- **What this means for other districts' SSF share.** A student who moves from a district school to a virtual
  charter mostly moves their weight from one district's count to the sponsor's rather than adding to the statewide
  total. Where other districts' shares can change: (a) students who were not in public school before (homeschooled
  or private) add new ADMw and spread the fixed state pool more thinly; (b) the extended-ADMw hold-harmless can
  count the student in the resident district's prior-year figure while the sponsor counts them this year; (c) the
  charter borrows the sponsor's poverty share (ORS 338.157), so a sponsor with a higher poverty share than the
  students' home districts adds weight statewide, and a lower one subtracts it; (d) the same hold-harmless on the
  sponsor's side, which the separate calculation in ORS 338.155(1)(c)(C) limits. None of these can be sized from
  the archived documents.
- The larger questions are what the money buys: the share sponsors keep (above), what the charters' operators
  spend it on, and outcomes. Those are outside this issue; see open questions.

### Still to find

- Charter contracts for the largest virtual charters (actual pass-through percentages and what sponsors keep).
- ODE or audit figures on SSF dollars paid to virtual charters (OJP's "hundreds of millions" is not itemized).
- Grade split (K-8 vs 9-12) of virtual charter ADMw.
- The 2017 Secretary of State audit of online schools and the 2019 follow-up cited by OJP.
- Whether any 2026 bills on virtual charters were introduced; only ODE's summary of enacted 2026 legislation has
  been searched (all 11 pages, for "charter", "virtual" and "online").
