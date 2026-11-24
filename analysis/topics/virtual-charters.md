---
summary: >
  State school money for students at online charter schools goes first to the district where the school is
  located; a district that sponsors one must pass on at least 80% of its per-student grant for kindergarten
  through eighth grade and 95% for high school, and keeps the rest. The education department says it doesn't
  publish a total for online schools; our estimate is about $257 million of state and local school money in 2025-26, a
  little over 3% of the money shared among school districts. How much sponsors keep depends on contracts, and
  the archive has the terms for only one online charter.
---
# Online charters: State School Fund money that follows students

Issue #20. Copied values: `data/virtual_charters_2025-26.csv`, `data/virtual_charters_grades_2025-26.csv` and
`data/virtual_charters_hs_admw_2024-25.csv`. Our calculations: `derived/virtual_charters.csv`,
written by `tools/derive_virtual_charters.py`. The archived copy of the Baker School District 5J's 2025-26 service
agreement came from the district in reply to a public records request (issue #46); it wasn't on the district's board
or business office pages (see "Still to find").

## Analysis

- **Same rates for online charters.** The law sets no separate rate for virtual charters: online and
  brick-and-mortar charters with the same kind of sponsor have the same minimum payment rates, including the lower
  special-education minimums (the separate weighted-count calculation applies only to virtual charters).
- **Size.** Virtual charters are about 4.2% of the statewide student count [DER:virtual_charters/admr_share_2025_26]
  and 3.4% of the weighted count [DER:virtual_charters/admw_share_2025_26]. Their weighted count is close to their raw
  count. That says little about the students themselves: a charter's poverty weight is copied from its sponsor (ORS
  338.157, below), and the Oregon Department of Education's page doesn't say whether the statewide weighted count is
  current or extended, so the two may not be on the same basis.
- Baker Web Academy, Fossil Charter School and Oregon Charter Academy are the three largest virtual charters by
  student count. In several sponsoring districts the virtual charter's 2025-26 weighted count is larger than the district's own: Fossil
  (3,347.06 against 193.00), Baker (3,915.32 against 2,241.97) and Prairie City, whose two charters total 1,410
  [DER:virtual_charters/prairie_city_virtual_admw_2025_26] against 542.36 (sources below).
- The department lists 23 virtual charters for 2025-26 [DER:virtual_charters/virtual_charters_listed_2025_26]. The
  three that opened in September 2025 are not in the department's 2025-26 transparency report (its count of
  virtual charter students and weighted enrollment, dated April 27, 2026), so the totals on this page leave them out;
  they had 113 students on Oct. 1, 2025 [DER:virtual_charters/new_charters_fall_2025_students], a small undercount.
  Lower Columbia opened in 2026-27.
- **Other counts.** The Quality Education Model report doesn't say how it defines a virtual school or how it counts
  students; with 52 schools against 20 virtual charters [DER:virtual_charters/charter_count_2025_26] it likely
  includes non-charter online schools, so it is not comparable one-for-one with the charter student count. The
  Oregon Journalism Project's figures (about 31,000 students in "online programs", 76 virtual schools) are as of the
  article (November 2026) and use its own definitions. The three sets of numbers measure different things and are
  not in conflict.
- **The grant rate.** Across the sponsors the General Purpose Grant per extended weighted student runs from
  Mitchell's $10,801 to Paisley's $11,397. The "Charter Schools Rate" equals or exceeds the grant rate on each
  sponsor's page. For North Bend it equals the General Purpose Grant divided by the current-year weighted count,
  $11,514 [DER:virtual_charters/north_bend_gpg_per_current_admw], rather than the extended count; the same holds for
  Scio, $11,796 [DER:virtual_charters/scio_gpg_per_current_admw]. The department has since confirmed that
  calculation (sources below). Because the extended count is the greater of the two years' counts, a rate on the
  current-year count can't be lower than the grant rate.
- **Which rate the minimums use.** Despite its label, the Charter Schools Rate is not the base for the minimum
  payments a sponsoring district must pass on under ORS 338.155 (80% of the grant per weighted student for K-8, 95%
  for high school), the department says: that base is the grant per extended weighted student, the line titled
  "General Purpose Grant per Extended ADMw" on each district's estimate. The statute alone doesn't settle this,
  because it says "per ADMw" (per weighted student) without saying which year's count (sources below). The department
  has no part in the contracts, which are made at the district level.
- In our analysis, a contract that pays 80% and 95% of the Charter Schools Rate, as Baker's does, therefore pays at
  least the statutory minimum rate per weighted student. For Baker the two rates are equal, so its 80% and 95% match
  the statutory minimums. Where a sponsor's current-year count is below its extended count, terms like these would pay
  a higher rate: at North Bend, for example, the Charter Schools Rate is $11,514 against a grant rate of $11,129. The
  archive has no North Bend contract.
- **No dollar total from the department.** The department says it doesn't publish the dollars attributable to virtual
  schools (its term), because the money flows through the sponsoring districts, which pay the charters (sources
  below). Our estimate below multiplies each charter's weighted count by its sponsor's grant per extended weighted
  student. That is the rate the department names as the base for the minimums; the estimate itself wasn't put to the
  department.
- **The money.** Our estimate is about $257 million of formula revenue in 2025-26
  [DER:virtual_charters/gpg_attributable_2025_26], roughly 3.3% of the school district share
  [DER:virtual_charters/gpg_attributable_share_2025_26]. The denominator is wider than the estimate: the district
  share also pays transportation, high-cost disability grants and the educator advancement fund, which the estimate
  leaves out, so on a like-for-like basis the share would be a little higher. The estimate mixes state and local
  money and multiplies each charter's weighted count by its sponsor's grant per weighted student (method below).
- **The sponsors' share.** How much a sponsor keeps depends on each charter's contract. The archive has pass-through
  terms for only one virtual charter, Baker Web Academy, from the Baker School District 5J's 2025-26 service agreement
  rather than its charter contract (see "Baker School District 5J and Baker Web Academy" below). The transparency report has no grade split. A district sponsor keeps whatever it does not pass through. If every
  contract paid exactly the statutory minimum, sponsors would keep between 5% (all high school) and 20% (all K-8) of
  the grant, roughly $13 million [DER:virtual_charters/sponsor_keep_min_2025_26] to $51 million
  [DER:virtual_charters/sponsor_keep_max_2025_26]. Contracts may pay more than the minimum, which would lower
  that; the pass-through applies to the current-year weighted count while the estimate uses the extended count, which
  could raise it a little; and the lower special-education minimums (ORS 338.165) mean sponsors could keep more than
  the high end, though that part comes with the sponsor's duty to identify and serve those students, and the two sides
  may negotiate a different split.
- **With the grade split.** In fall 2025, 61.6% of the 20 report charters' students were in K-8
  [DER:virtual_charters/k8_share_fall_2025]. Using each school's own split in place of the all-K-8 and
  all-high-school bounds, sponsors would keep about $36 million at the statutory minimum
  [DER:virtual_charters/sponsor_keep_gradesplit_2025_26], with the same caveats. The department's High School Success
  figures are a check on the headcount stand-in: for the 18 charters with a row, high school is 48.0% of the 2024-25
  weighted count [DER:virtual_charters/hs_admw_share_2024_25] against 45.8% of fall 2025 headcount
  [DER:virtual_charters/hs_headcount_share_hss_charters_fall_2025]. The years differ, but the two splits are close. If the
  2024-25 split holds, the headcount split slightly understates high school, which would put the true figure a little
  below $36 million.
- **Santiam Canyon and Oregon Charter Academy.** At the statutory minimum, with Oregon Charter Academy's grade
  split, Santiam Canyon would keep about $3.9 million a year [DER:virtual_charters/orca_keep_at_minimum_2025_26].
  S&P Global Ratings' April 2026 rating update on the district says it has received "about $1.5 million for
  sponsoring the virtual charter school" in recent years, well below that; S&P doesn't say whether that is a yearly
  or a cumulative figure. Oregon Charter Academy's own report doesn't settle it either: it took in $32.1 million of State
  School Fund money in 2024-25, more than our $31.1 million estimate of the whole General Purpose Grant for its
  students [DER:virtual_charters/orca_formula_revenue_2025_26]. That mismatch mostly shows the two figures aren't like
  for like: the years differ, our estimate uses the 2024-25 weighted count at 2025-26 rates, and the academy's "State
  School Fund" line may include money our estimate leaves out (transportation, high-cost disability). S&P doesn't
  say how it counted either, so the contract is still needed to settle it.
- **Baker School District 5J and Baker Web Academy.** The district's 2025-26 service agreement set Baker Web Academy's
  payment, for the largest virtual charter by fall 2025 student count, at 80% (K-8) and 95% (9-12) of the department's
  Charter Schools Rate on its whole weighted count. Those are the general minimum percentages in ORS 338.155,
  applied to the Charter Schools Rate rather than the grant rate the minimums use (see "Which rate the minimums use"
  above). The agreement
  doesn't apply the lower special-education minimums in ORS 338.165. That law adds the special-education weight to a
  charter's weighted count [SRC:legislature/ors/ors338.html] (ORS 338.165(2)), so the rate the agreement set for those
  students is above the law's minimum. The district also agreed to provide those students' special-education
  services itself. The agreement calls those services consistent with ORS 338.165 but doesn't say whether it uses that
  law's option, in 338.165(4), to negotiate a different split case by case (sources below). For Baker the
  Charter Schools Rate equals its grant rate, $11,223 per weighted student
  [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.2]. So for this school the assumption behind the $36 million
  estimate above, that the contract pays the general minimums, holds.
- **What the district kept.** Our estimate is that the district kept about $5.6 million, 12.7%, of the General
  Purpose Grant money for the academy's students in 2025-26 [DER:virtual_charters/bwa_keep_under_agreement_2025_26]
  [DER:virtual_charters/bwa_keep_share_2025_26] and passed on about $38.3 million
  [DER:virtual_charters/bwa_passed_through_2025_26]. It uses the academy's fall 2025 headcount split by grade in place
  of its weighted split, and the April 2026 weighted count; the agreement reconciles payment adjustments in May of the
  following school year. Under the same agreement the district agreed to provide special-education services to the academy and to Baker
  Early College, another of its charters, estimated at $3,435,625 for 2025-26, plus state reporting, technology,
  printing, mail, internet and administrative support. The agreement doesn't split those costs between the two
  charters or say which money pays for them. It had the academy cover up to $56,100 of payroll for one new
  special-education position and says invoices for additional service-agreement items are paid within 10 business
  days, but it doesn't say which services are billed (sources below).
- **Which year.** The agreement covered 2025-26 and ran to June 30, 2026; the archive has no 2026-27 terms, and Baker
  Web Academy's charter contract isn't archived, so whether the contract sets these terms or defers to the service
  agreement is still open.
- **Contract terms.** The department's list gives Baker Web Academy's contract as Oct. 16, 2024, to June 30, 2032,
  about eight years, while Baker's financial report describes a 10-year agreement renewed annually for "Baker Charter
  School", which our analysis takes to be the two charters the report names, Baker Web Academy and Baker Early College
  (the 2025-26 service agreement is with "Baker Charter Schools", naming both); a rolling term renewed each
  year would fit both, but the contract is needed to say. S&P says Santiam Canyon's agreement with Oregon Charter
  Academy was renewed for seven years starting in 2025 [SRC:districts/santiam-canyon/audit_santiam-canyon-sd-129j.pdf p.1];
  the department gives a start of June 13, 2024, but an end of June 30, 2032, which fits a seven-year term from 2025.
- **Oversight fees.** The Secretary of State's 2017 audit tied sponsors' fees to an incentive to let the schools grow, while noting
  that district officials said the fees also help their other students and that one sponsor used them to pay for
  oversight. The 2019 follow-up found sponsor standards had not been raised (see "Secretary of State audits" below).
  No later status report is archived.
- **No official dollar total.** Neither audit gives a total of State School Fund dollars paid for virtual charter
  students (our review covered the 2017 report's online-schools section, pp. 34-40, and the 2019 follow-up's status
  table), and apart from the High School Success 9-12 weighted count (18 of 20 charters, 2024-25 data) no archived
  department document splits virtual charters' student or weighted counts by grade.
- **Nyssa.** Nyssa's online program, the Oregon Journalism Project's main example, is set up by the district with a
  for-profit company and isn't in the department's virtual charter report (sources below). If it is not a charter, the ORS 338.155 pass-through minimums would not govern that
  arrangement.
- **The Oregon Journalism Project's $11,000.** Its figure, that each student who leaves a brick-and-mortar school for
  a virtual one costs that school more than $11,000, is in line with the 2025-26 General Purpose Grant per weighted
  student ($10,801-$11,397 among virtual charter sponsors, above). It is mostly revenue that moves with the student
  between districts rather than a net cost to the system, though see (a)-(d) below.
- **Gov. Tina Kotek.** As of Nov. 20, 2026, no proposal from her on virtual schools is in the archive; her 2027-29 budget is
  due Dec. 1 (see `decisions.md#grb-2027-29`).
- **House Bill 3953** is about who may sponsor a charter, not about virtual charters or their funding, so it is left
  out of the bill list below. HB 3444 gives its sponsor only as Rep. Wright. The Legislature's member
  listing has one, Rep. Boomer Wright, R-District 9 (Coos Bay), so our analysis takes the sponsor to be him
  [SRC:legislature/members/representatives-all.html] [SRC:legislature/members/wright.html].
- **The bills.** Counting HB 3444's amendments, five of the six 2025 bills would have widened access to or funding
  for virtual charters. Under the 3% rule, a district may refuse a student's move to a virtual charter it doesn't
  sponsor once more than 3% of its resident students attend one; HB 2144 would have changed how the rule is
  administered and had the department collect the enrollment data. Three would have loosened the 3% rule. HB 2583 would have opened Student Investment Account grants
  to some or all virtual charters. HB 3444 as introduced was about brick-and-mortar charters; its -1 and -2
  amendments would have raised the virtual charter minimum to 95% and opened the account's grants to virtual
  charters. None left committee.
- **The statute's history.** The separate calculation for virtual charters dates from 2021 and was widened in
  2023 to cover a fall in either the student count or the weighted count. The 2021 act also had a two-year transition
  (2021-22 and 2022-23): where a virtual charter's student count fell, the sponsor kept the greater of its two years'
  weighted counts and the charter got its current weighted count plus 10% of the year-over-year difference. The 2025
  change (HB 3038) is about recovery schools, not virtual charters. None of the three changed the pass-through
  minimums.
- **What this means for other districts' State School Fund share.** A student who moves from a district school to a
  virtual charter mostly moves their weight from one district's count to the sponsor's rather than adding to the
  statewide total. Where other districts' shares can change: (a) students who were not in public school before
  (homeschooled or private) add new weight and spread the fixed state pool more thinly; (b) the extended-count
  hold-harmless can count the student in the resident district's prior-year figure while the sponsor counts them this
  year; (c) the charter borrows the sponsor's poverty share (ORS 338.157), so a sponsor with a higher poverty share
  than the students' home districts adds weight statewide, and a lower one subtracts it; (d) the same hold-harmless on
  the sponsor's side, which the separate calculation in ORS 338.155(1)(c)(C) limits. None of these can be sized from
  the archived documents.
- The larger questions are what the money buys: the share sponsors keep (above), what the charters' operators
  spend it on, and outcomes. Those are outside this issue; see open questions.

### Still to find

- Charter contracts for the largest virtual charters: the actual pass-through percentages. Baker's are archived in its
  2025-26 service agreement (sources below), but not the Baker Web Academy charter itself. Not found in Santiam
  Canyon's BoardBook (searched "charter contract" and "Oregon Charter Academy"), on Oregon Charter Academy's charter
  board and reporting pages, or on the Baker School District 5J's board and business office pages; the Fossil School
  District 21J's were not found by web search, and the district's site (`fossil.k12.or.us`) and the school's
  (`fossilschools.com`) blocked our browser with a bot check. A records request is #46.
- An official dollar total for State School Fund money paid for virtual charter students: none in the department's
  archived documents or the 2017 and 2019 Secretary of State reports, and the department says it doesn't publish
  one (#47, sources below). It pointed to its Fiscal Transparency Unit's School Level Expenditure Report Dashboard, which isn't
  archived or checked yet (#169).
- A 9-12 weighted count for Fossil Charter School and Paisley School: the High School Success allocations print only
  their sponsor districts' rows (Fossil School District 21J 25.53, Paisley School District 11 43.12), so this would
  have to come from the department. Issue #47 didn't ask for this count; it is an open question (`questions.csv`,
  `virtual-charter-hs-admw`).

## What the sources say

### The law (chapter 338 of the Oregon Revised Statutes)

- A "virtual public charter school" is a public charter school that provides online courses; it does not include a
  charter school that primarily serves students in a physical location [SRC:legislature/ors/ors338.html]
  (ORS 338.005(5)).
- **Students count where the charter is, not where they live.** For State School Fund purposes, charter students
  are treated as residents of the district in which the charter is located, and the State School Fund money for them
  is paid first to that district [SRC:legislature/ors/ors338.html] (ORS 338.155(1)(a)-(b)).
- **Sponsor's minimum pass-through.** A sponsoring district must contract to pay its charter at least 80% of the
  district's General Purpose Grant per weighted student (weighted average daily membership, ADMw: the student count with
  extra weight for students who cost more to serve) for students in K-8 and at least 95% for grades 9-12; the two
  sides may agree on more [SRC:legislature/ors/ors338.html] (ORS 338.155(2), (7)). For charters sponsored by the State
  Board the minimum is 90% (K-8) and 95% (9-12), and the district must send half of the unpaid portion to the Oregon
  Department of Education [SRC:legislature/ors/ors338.html] (ORS 338.155(3), (5)). For students eligible for special
  education, the payment per weighted student attributable to the student must be at least 40% (K-8) or 47.5% (9-12)
  of the grant, unless the district and the charter negotiate an alternative distribution case by case; the district
  in which the charter is located identifies, evaluates and serves those students [SRC:legislature/ors/ors338.html]
  (ORS 338.165(1), (2), (4)).
- **Which count.** The minimums are shares of the district's "General Purpose Grant per ADMw as calculated under ORS
  327.013" [SRC:legislature/ors/ors338.html] (ORS 338.155(2)). ORS 327.013 calculates the General Purpose Grant on
  the district's extended weighted count, its current or prior year's weighted count, whichever is greater
  [SRC:legislature/ors/ors327.html] (ORS 327.013(1), (1)(c)). Neither section says which count the grant is divided
  by to give the per-student figure. The department determines each district's estimated General Purpose Grant per
  weighted student each year and makes it available to all districts [SRC:legislature/ors/ors338.html] (ORS 338.155(4)).
- **Poverty weight is borrowed from the sponsor.** A charter's weighted count assumes the same share of children in
  poverty as the district where it is located [SRC:legislature/ors/ors338.html] (ORS 338.157).
- **Separate calculation for shrinking sponsors.** If a sponsoring district's own enrollment (leaving out the
  virtual charter) fell from the year before, the department calculates the virtual charter's weighted count
  separately from the district's when working out the district's extended weighted count
  [SRC:legislature/ors/ors338.html] (ORS 338.155(1)(c)(C)). The extended count is the higher of the current or prior
  year's weighted enrollment, a hold-harmless for districts whose enrollment is falling
  [SRC:ode/qec/2026_qem_report.pdf p.114]. The department publishes this calculation in a "Virtual
  Charter School Ext ADMw Transparency Report"
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1].
- **The 3% rule.** A student does not need the resident district's approval to enroll in a virtual charter, only to
  give notice of intent and of enrollment. But if more than 3% of a district's resident students already attend
  virtual charters the district does not sponsor, the district may refuse approval; it must then tell the family
  the current percentage, the right to appeal to the State Board, and other online options
  [SRC:legislature/ors/ors338.html] (ORS 338.125(4)-(5)). The department's guidance dates the option to deny to House
  Bill 2301 (2011), with timelines adjusted by House Bill 3204 (2023)
  [SRC:ode/charter/2026-08_virtual-charter-enrollment-guidance.pdf p.3].
- **No Student Investment Account money.** Virtual charters cannot apply for Student Investment Account grants under
  the Student Success Act, and the department removes their weighted counts from their sponsors' allocations; its
  September 2026 list for 2027-29 names the virtual charters and their sponsors
  [SRC:ode/charter/2027-29_sia-virtual-charter-list.pdf p.1].
- The history note for ORS 338.155 lists its 1999 enactment and amendments through 2025, the three most recent being
  2021 c.494, 2023 c.571 and 2025 c.386 [SRC:legislature/ors/ors338.html].
- **2021 (Senate Bill 743, chapter 494).** Added the separate weighted-count calculation for a virtual charter when
  the sponsoring district, leaving out the charter, "had a decrease in ADM compared to the previous school year". For
  the 2021-22 and 2022-23 school years only, for a sponsor of a virtual charter "that had a decrease in ADM for the
  current school year compared to the previous school year", it also set the sponsor's weighted count at the greater
  of its current or previous year's count (leaving out the charter) and the charter's at its current weighted count
  plus 10% of the difference between the two years. It applied from 2021-22 distributions
  [SRC:legislature/laws/2021orlaw0494.pdf p.1] [SRC:legislature/laws/2021orlaw0494.pdf p.2].
- **2023 (Senate Bill 278, chapter 571).** Made the trigger "a decrease in ADM or ADMw" (the student count or the weighted count), applying from 2022-23
  distributions [SRC:legislature/laws/2023orlaw0571.pdf p.1].
- **2025 (House Bill 3038, chapter 386).** Added ORS 338.155(1)(d): students of a charter that is an approved
  recovery school are not counted as residents of its district for State School Fund purposes and are funded under
  ORS 336.680. It made the same exception in ORS 338.165, first applying to 2024-25
  [SRC:legislature/laws/2025orlaw0386.pdf p.3] [SRC:legislature/laws/2025orlaw0386.pdf p.4]. The Legislative Policy
  and Research Office's 2025 summary describes the same change
  [SRC:legislature/lpro/2025_education-legislative-summary.pdf p.19].

### Enrollment and money (2025-26)

- The department's 2025-26 transparency report (second-period student count, dated April 27, 2026) lists each
  virtual charter, its sponsoring district, and its student count (ADMr, resident average daily membership) and weighted count (ADMw) for 2024-25 and
  2025-26 [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2]. The values are copied into
  `data/virtual_charters_2025-26.csv`.
- Baker Web Academy has a student count of 3,839.73 in 2025-26, Fossil Charter School 3,294.85 and Oregon Charter
  Academy 2,601.34 [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].
- The department's May 2026 estimate puts the statewide student count at 531,425 and the weighted count at 668,444
  for 2025-26 [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.1].
- The 2026 Quality Education Model report counts 52 virtual schools with 27,978 students (5.2%) in 2024-25
  [SRC:ode/qec/2026_qem_report.pdf p.16].
- The transparency report marks "No" for a separate calculation in Prairie City, Paisley, Fossil and Mitchell and
  "Yes" in the other sponsoring districts
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].
- The Fossil School District's charter has a weighted count of 3,347.06 in 2025-26 against 193.00 for the district
  itself; Prairie City's two virtual charters have 1,290.40 and 120.09 against 542.36; the Baker School District's has
  3,915.32 against 2,241.97 [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].
- The department's estimates give each sponsor's General Purpose Grant per extended weighted student: $10,801 for the
  Mitchell School District [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.191] and $11,397 for the Paisley
  School District [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.93] in 2025-26. Each district page also shows
  a "Charter Schools Rate (ORS 338.155)", which the department does not define on the page; for North Bend it is
  $11,514 against a General Purpose Grant per extended weighted student of $11,129
  [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.32].
- Asked by email, the department's State School Fund Coordinator, Jerod Nunn, replied on Nov. 24, 2026, that the
  Charter Schools Rate is the General Purpose Grant divided by the current-year weighted count, which, he wrote, helps the
  rate reflect the charter's current students [SRC:ode/correspondence/2026-11-24_ode-ssf-coordinator-reply_charter-schools-rate.txt].
- In the same reply he wrote: "This rate is not the 80% or 95% minimum referred to in ORS 338.155." The minimums
  apply to the district's General Purpose Grant per weighted student as calculated under ORS 327.013, the figure
  titled "General Purpose Grant per Extended ADMw" on the district estimates. Charter contracts are written at the
  district level; the department has no part in them, and districts are expected to follow the statute when
  contracting [SRC:ode/correspondence/2026-11-24_ode-ssf-coordinator-reply_charter-schools-rate.txt].
- The department does not publish the dollar amount attributable to virtual schools, the reply says, because those
  dollars flow through the school districts, which pay the charter schools. It pointed to the Fiscal Transparency
  Unit's School Level Expenditure Report Dashboard [SRC:ode/correspondence/2026-11-24_ode-ssf-coordinator-reply_charter-schools-rate.txt].
- North Bend's 2025-26 General Purpose Grant is $36,777,648.12, its 2025-26 weighted count 3,194.12 and its extended
  weighted count 3,304.67 [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.32].
- Scio's 2025-26 General Purpose Grant is $27,800,843.40, its 2025-26 weighted count 2,356.76, and its Charter
  Schools Rate $11,796 [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.118].
- The department's 2025-26 total revenue for formula is $8,248,519,310: state revenue for formula of $5,504,883,786
  (the $5,566,106,000 State School Fund appropriation less transfers and deductions) plus local revenue. The school
  district share is $7,877,335,941, from which high-cost disability grants ($55,000,000) and the district share of the
  educator advancement fund ($6,003,307) are taken before distribution
  [SRC:ode/ssf/2025-26_ssf-estimates_2026-05-01.pdf p.1].
- The transparency report does not split virtual charter students between K-8 and 9-12
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].

### The department's charter lists and enrollment by grade

- The department's 2025-26 charter school list (updated Jan. 21, 2026) has a sheet of virtual charters giving each
  one's opening date, contract dates, type of management organization, sponsor and grades served
  [SRC:ode/charter/2025-26_public-charter-schools.xlsx]. Values are copied into
  `data/virtual_charters_grades_2025-26.csv`.
- Applegate Valley Virtual Academy (Three Rivers School District) opened Sept. 1, 2025; Jefferson Classical Academy of
  Oregon (Spray School District) and Stellar Pines Virtual Academy (Colton School District) opened Sept. 2, 2025; all
  three contract with a for-profit education management organization
  [SRC:ode/charter/2025-26_public-charter-schools.xlsx]. The department's 2026-27 list adds Lower Columbia Virtual
  Charter Academy (Astoria School District 1C), opened Sept. 1, 2026 [SRC:ode/charter/2026-27_public-charter-schools.xlsx].
- On Oct. 1, 2025, Applegate Valley had 101 students, Jefferson Classical 10 and Stellar Pines two
  [SRC:ode/enrollment/fallmembershipreport_2025-26.xlsx].
- The department's fall membership report gives each school's Oct. 1, 2025, enrollment by grade, a headcount, not
  average daily membership [SRC:ode/enrollment/fallmembershipreport_2025-26.xlsx]. The transparency report gives each
  virtual charter's student count and extended weighted count as totals, with no grade breakdown
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1].
- The department's 2025-27 High School Success allocations, made "with 2024-25 State School Fund Data", print a 9-12
  weighted count for each district and most charter schools [SRC:ode/grants/2025-27_hss-allocations_2025-09-16.pdf p.1].
  Eighteen of the 20 report charters have their own row; Fossil Charter School and Paisley School do not, and only
  their sponsor districts' rows are printed [SRC:ode/grants/2025-27_hss-allocations_2025-09-16.pdf p.3]
  [SRC:ode/grants/2025-27_hss-allocations_2025-09-16.pdf p.7]. Oregon Charter Academy's row shows 1,383.64
  [SRC:ode/grants/2025-27_hss-allocations_2025-09-16.pdf p.8].
- Contracts for the three largest, per the department's list: Baker Web Academy (managed by a nonprofit charter
  management organization) began Oct. 16, 2024, and runs to June 30, 2032; Oregon Charter Academy June 13, 2024, to
  June 30, 2032; Fossil Charter School July 1, 2025, to June 30, 2030 [SRC:ode/charter/2025-26_public-charter-schools.xlsx].

### Sponsors' records

- The Baker School District 5J's 2024-25 financial report says the district receives revenue on behalf of Baker Web
  Academy and Baker Early College and passes it on to them, accounted for in its General Fund
  [SRC:districts/baker-5j/fy2024-25_annual-financial-report.pdf p.34]. Describing "Baker Charter School (Charter)", it
  refers to "the 10-year sponsorship agreement that is renewed annually"
  [SRC:districts/baker-5j/fy2024-25_annual-financial-report.pdf p.17]. The report gives no amount passed through or
  kept.
- The Baker School District 5J's 2025-26 service agreement is with Baker Charter Schools, the name it uses for Baker
  Web Academy and Baker Early College together
  [SRC:districts/baker-5j/2025-26_service-agreement_baker-charter-schools.pdf p.1]. Within 10 business days of each State
  School Fund payment the district passes on the charters' portion, based on the latest weighted-count report and the
  Charter Schools Rate (ORS 338.155) on the latest State School Fund estimate, with adjustments reconciled in May of
  the following school year. Baker Web Academy is paid 80% of that rate for its K-8 weighted count and 95% for 9-12; Baker Early
  College 95%. The agreement has invoices for additional service-agreement items paid within 10 business days of receipt
  [SRC:districts/baker-5j/2025-26_service-agreement_baker-charter-schools.pdf p.1].
- Under the same agreement, which calls its special-education services consistent with ORS 338.165, the district's
  special-education staff were to serve the charters' students, at an estimated cost
  of $3,435,625 in 2025-26 for 24.80 full-time equivalent staff. Baker Web Academy was to cover up to $56,100 of payroll for
  a new special-education position, to offset what it calls the Measure 98 (High School Success) special-education
  pass-through for the position. It says the district reimburses preapproved supplies, curriculum and services, and lists
  other district services: state reporting, technology, printing (at no cost to the charters), mail, internet and
  administrative support [SRC:districts/baker-5j/2025-26_service-agreement_baker-charter-schools.pdf p.1]
  [SRC:districts/baker-5j/2025-26_service-agreement_baker-charter-schools.pdf p.2].
- The agreement has the district pass Student Investment Account money to Baker Early College. The charters don't ask for the
  account's poverty pass-through, which the agreement says is because virtual schools don't qualify for it
  [SRC:districts/baker-5j/2025-26_service-agreement_baker-charter-schools.pdf p.1].
- The agreement runs through June 30, 2026, after which a 2026-27 agreement may be negotiated
  [SRC:districts/baker-5j/2025-26_service-agreement_baker-charter-schools.pdf p.2]. The charters' superintendent,
  Roland Hobson, dated it Oct. 1, 2025, and Baker's superintendent, Casey Hallgarth, Jan. 20, 2026
  [SRC:districts/baker-5j/2025-26_service-agreement_baker-charter-schools.pdf p.2]
  [SRC:districts/baker-5j/2025-26_service-agreement_baker-charter-schools.pdf p.3].
- S&P Global Ratings' April 7, 2026, rating update on the Santiam Canyon School District 129J says the district
  retains "a percentage based on a multiyear contract" with Oregon Charter Academy and "has received about $1.5
  million for sponsoring the virtual charter school" in recent years
  [SRC:districts/santiam-canyon/audit_santiam-canyon-sd-129j.pdf p.1]. It puts charter school payments at 72% of the
  district's fiscal 2026 budget [SRC:districts/santiam-canyon/audit_santiam-canyon-sd-129j.pdf p.2].
- Oregon Charter Academy's financial report for the year ended June 30, 2025 (a scan; read from the page image)
  shows State School Fund revenue of $32,090,872, up from $28,528,569 the year before, out of total revenue of
  $35,057,972 [SRC:districts/santiam-canyon/2025_oregon-charter-academy-financial-report.pdf p.20]. It lists
  among its principal revenue sources "payments of state school support from Santiam Canyon School District"
  [SRC:districts/santiam-canyon/2025_oregon-charter-academy-financial-report.pdf p.35]. It does not give the amount
  Santiam Canyon kept.

### Secretary of State audits

- The Secretary of State's December 2017 audit of alternative and online education (Report 2017-30) says online
  charters receive "a share of per-student payments from the State School Fund" from their sponsors
  [SRC:fiscal/sos/2017-30_alternative-and-online-education.pdf p.34]. It found that the department counts a
  full-time online student present for the week after two check-ins with a teacher, and that this attendance
  standard is the basis for State School Fund payments
  [SRC:fiscal/sos/2017-30_alternative-and-online-education.pdf p.35].
- It says the three statewide virtual charters that contracted with for-profit firms were sponsored by relatively
  small districts that received oversight fees of up to $1 million a year, which district officials told the auditors
  also benefit district students not attending the online schools
  [SRC:fiscal/sos/2017-30_alternative-and-online-education.pdf p.36]. The fees rise with the schools' enrollment,
  "providing an incentive for districts to allow the schools to grow"
  [SRC:fiscal/sos/2017-30_alternative-and-online-education.pdf p.37].
- It found district monitoring varied and was low for two of the three schools; the district with relatively
  strong oversight had annual outside reviews and used fee revenue to add district staff, in part for oversight
  [SRC:fiscal/sos/2017-30_alternative-and-online-education.pdf p.37]. The department generally agreed with the
  audit's recommendations [SRC:fiscal/sos/2017-30_alternative-and-online-education.pdf p.3].
- Its recommendations include strengthening "attendance and funding standards for virtual schools" (10) and
  increasing standards for sponsors of statewide and regional virtual charters (15)
  [SRC:fiscal/sos/2017-30_alternative-and-online-education.pdf p.39]
  [SRC:fiscal/sos/2017-30_alternative-and-online-education.pdf p.40].
- The March 2019 follow-up (Report 2019-12) rated recommendation 10 partially implemented: the department held work
  sessions in early 2018 but none of four proposals satisfied agency and stakeholder concerns
  [SRC:fiscal/sos/2019-12_alternative-and-online-education-follow-up.pdf p.7]. It rated 13 and 15 not
  implemented; the department said higher sponsor standards "would not be politically viable" in the 2019 session
  [SRC:fiscal/sos/2019-12_alternative-and-online-education-follow-up.pdf p.8].

### What the news reported

- The Oregon Journalism Project's investigation (published Nov. 3, 2026, in Willamette Week) says about 31,000
  students, roughly 6% of K-12, are in the state's online programs, that Oregon has 76 virtual schools, and that
  state money follows each student [NEWS:NEWS-20261103-wweek-1].
- Its main example, Nyssa's online program, is set up by the district with a for-profit company; under its
  contract Nyssa kept 40% of the per-student money and the company got 60% [NEWS:NEWS-20261103-wweek-1]. Nyssa
  does not appear in the department's virtual charter report
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.1]
  [SRC:ode/ssf/2025-26_virtual-charter-ext-admw-transparency_2026-04-27.pdf p.2].
- The article says each student who leaves a brick-and-mortar school for a virtual one costs that school more than
  $11,000 [NEWS:NEWS-20261103-wweek-1].
- The article also reports families who say online school works for them [NEWS:NEWS-20261103-wweek-1].
- Gov. Tina Kotek's statement to the Oregon Journalism Project said she "is actively reviewing the state's current
  approach to virtual education" [NEWS:NEWS-20261103-wweek-1].

### Bills (2025 and 2026 sessions)

- The Legislature's bill-tracking site lists each of the six 2025 bills below as still "In House Committee" or "In
  Senate Committee" with no chapter number [SRC:legislature/bills/2025R1_HB3444_overview.html] [SRC:legislature/bills/2025R1_HB2583_overview.html]
  [SRC:legislature/bills/2025R1_HB2144_overview.html] [SRC:legislature/bills/2025R1_SB562_overview.html]
  [SRC:legislature/bills/2025R1_SB633_overview.html] [SRC:legislature/bills/2025R1_SB647_overview.html].

- **House Bill 3444**, sponsored by Rep. Wright: As introduced, it would have raised the minimum pass-through to 95% for non-virtual charters only (virtual charters stay at 80% K-8 / 95% 9-12), loosened Student Investment Account eligibility for non-virtual charters only, let sponsors keep unpaid amounts but required them to be spent on charter administration, and entitled charters to local, state and federal moneys and transportation grants on the same basis as district schools, except that virtual charters would get no share of local revenues. The -1 and -2 amendments would have set 95% for all charters, virtual included, and opened Student Investment Account grants to virtual charters. The staff summary lists a House Education Committee meeting on March 12, 2025. [SRC:legislature/bills/2025R1_HB3444_introduced.pdf p.1] [SRC:legislature/olis/2025R1/294106_hb3444-staff-measure-summary.pdf p.1] [SRC:legislature/bills/2025R1_HB3444_overview.html]
- **House Bill 2583**, sponsored by Rep. Emily McIntire, R-District 56: It would have made virtual charters without a for-profit operator eligible for Student Investment Account grants; the -1 amendment would have opened the grants to all virtual charters that meet the demographic tests. The staff summary lists House Education Committee meetings on April 2 and April 7, 2025. [SRC:legislature/bills/2025R1_HB2583_introduced.pdf p.1] [SRC:legislature/olis/2025R1/297340_hb2583-staff-measure-summary.pdf p.1] [SRC:legislature/bills/2025R1_HB2583_overview.html] [SRC:legislature/members/mcintire.html]
- **House Bill 2144**, sponsored by Rep. McIntire: It would have changed timelines for the 3% rule and had the department collect virtual charter enrollment data for districts' calculations. [SRC:legislature/bills/2025R1_HB2144_introduced.pdf p.1] [SRC:legislature/bills/2025R1_HB2144_overview.html]
- **Senate Bill 562**, sponsored by Sen. Dick Anderson, R-District 5 (Lincoln City): It would have removed the 3% approval rule. [SRC:legislature/bills/2025R1_SB562_introduced.pdf p.1] [SRC:legislature/bills/2025R1_SB562_overview.html] [SRC:legislature/members/anderson.html]
- **Senate Bill 633**, sponsored by Sen. Daniel Bonham, R-District 26, who resigned from the Senate in 2025: It would have removed the 3% approval rule (same summary as SB 562). [SRC:legislature/bills/2025R1_SB633_introduced.pdf p.1] [SRC:legislature/bills/2025R1_SB633_overview.html] [SRC:legislature/bills/2025R1_SB562_introduced.pdf p.1] [SRC:legislature/press/2025-10-23_senate-republicans-drazan-appointed-sd26.pdf p.1]
- **Senate Bill 647**, sponsored by Bonham, at the request of former Sen. Dennis Linthicum, R-District 28 in 2021-22, whose Senate term ended in January 2025: It would have raised the 3% threshold to 5%. [SRC:legislature/bills/2025R1_SB647_introduced.pdf p.1] [SRC:legislature/bills/2025R1_SB647_overview.html] [SRC:legislature/members/2021-22_house-districts-to-senate-districts.pdf p.1] [SRC:legislature/press/2025-01-13_senate-republicans-new-senators-sworn-in.pdf p.1]

- The Legislature's 2025 education session summary marks HB 3444 and HB 2583 as not enacted
  [SRC:legislature/lpro/2025_education-legislative-summary.pdf p.12]
  [SRC:legislature/lpro/2025_education-legislative-summary.pdf p.1].
- 2026 session: none of the bill summaries on the Legislature's 2026 session bill list mentions charter, virtual or
  online schools [SRC:legislature/bills/2026R1_session-bills-list.html]. The department's summary of enacted 2026
  education legislation, searched across all 11 pages for "charter", "virtual" and "online", mentions no charter or
  virtual school bill
  [SRC:ode/legislation/2026_summary-enacted-education-legislation.pdf p.1] (cover page cited; the claim covers the
  whole document).
- The same page of the Legislative Policy and Research Office summary lists House Bill 3953 as enacted under "K-12:
  Charter Schools": federally recognized Tribes may apply to the State Board to sponsor a charter school
  [SRC:legislature/lpro/2025_education-legislative-summary.pdf p.12].

## Derived figures

Our own sums, shares and estimates; methods, inputs and assumptions are in `derived/virtual_charters.csv`.
Estimates ("est") rest on the assumptions listed there. In the table, ADMr is the student count (average daily
membership) and ADMw the weighted count.

| Figure | Value | Kind | Tag |
|---|---|---|---|
| Virtual charters in the department's 2025-26 report | 20 | derived | [DER:virtual_charters/charter_count_2025_26] |
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
| Formula revenue attributable to virtual charters, 2025-26 | about $257 million | est | [DER:virtual_charters/gpg_attributable_2025_26] |
| That estimate as a share of the school district share of formula revenue | 3.3% | est | [DER:virtual_charters/gpg_attributable_share_2025_26] |
| What sponsors would keep if contracts paid exactly the minimum, low end (all 9-12) | about $13 million | est | [DER:virtual_charters/sponsor_keep_min_2025_26] |
| Same, high end (all K-8) | about $51 million | est | [DER:virtual_charters/sponsor_keep_max_2025_26] |
| North Bend General Purpose Grant per current-year ADMw | $11,514 | derived | [DER:virtual_charters/north_bend_gpg_per_current_admw] |
| Scio General Purpose Grant per current-year ADMw | $11,796 | derived | [DER:virtual_charters/scio_gpg_per_current_admw] |
| Virtual charters on the department's 2025-26 charter list | 23 | derived | [DER:virtual_charters/virtual_charters_listed_2025_26] |
| Oct. 1, 2025, enrollment of the three listed charters missing from the report | 113 | derived | [DER:virtual_charters/new_charters_fall_2025_students] |
| K-8 enrollment, Oct. 1, 2025 (20 report charters) | 13,385 | derived | [DER:virtual_charters/k8_headcount_fall_2025] |
| Grades 9-12 enrollment, Oct. 1, 2025 (20 report charters) | 8,357 | derived | [DER:virtual_charters/hs_headcount_fall_2025] |
| K-8 share of that enrollment | 61.6% | derived | [DER:virtual_charters/k8_share_fall_2025] |
| What sponsors would keep at the statutory minimum, using each school's grade split | about $36 million | est | [DER:virtual_charters/sponsor_keep_gradesplit_2025_26] |
| What Santiam Canyon would keep from Oregon Charter Academy at the statutory minimum | about $3.9 million | est | [DER:virtual_charters/orca_keep_at_minimum_2025_26] |
| What the Baker School District 5J kept of the General Purpose Grant money for Baker Web Academy's students under its 2025-26 service agreement | about $5.6 million | est | [DER:virtual_charters/bwa_keep_under_agreement_2025_26] |
| The same as a share of that money | 12.7% | est | [DER:virtual_charters/bwa_keep_share_2025_26] |
| What it passed on to Baker Web Academy under that agreement | about $38.3 million | est | [DER:virtual_charters/bwa_passed_through_2025_26] |
| General Purpose Grant attributable to Oregon Charter Academy's students, 2025-26 | about $31.1 million | est | [DER:virtual_charters/orca_formula_revenue_2025_26] |
| Report charters with their own High School Success row | 18 | derived | [DER:virtual_charters/hss_listed_charters] |
| 9-12 share of those charters' 2024-25 ADMw | 48.0% | est | [DER:virtual_charters/hs_admw_share_2024_25] |
| 9-12 share of the same charters' Oct. 1, 2025, headcount | 45.8% | derived | [DER:virtual_charters/hs_headcount_share_hss_charters_fall_2025] |

The $257 million estimate multiplies each virtual charter's extended weighted count in the transparency report by
its sponsor's General Purpose Grant per extended weighted student. It mixes state and local money (the grant is
calculated before local revenue is subtracted), leaves out the transportation grant and high-cost disability grants,
and uses each sponsor's average rate. It is one year of state plus local formula revenue, not State School Fund
appropriation.
