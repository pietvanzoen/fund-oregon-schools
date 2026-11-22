# The Student Investment Account: what the money funds and what ODE reports it did

Decisions this informs: standing research (what the money buys). Figures copied from sources: `data/sia_spending.csv`.
Our sums: `derived/sia.csv`. Audits and outside reviews are still to come (#103).

## What the sources say

### What it is and what it can pay for

- The Student Investment Account (SIA) was created by the Student Success Act in 2019. It gives school districts,
  eligible charter schools and youth corrections and juvenile detention education programs non-competitive grants
  once they meet the application requirements, and it receives at least 50% of the money deposited in the Fund for
  Student Success [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.3].
- The grants are paid in addition to the State School Fund. Their purposes in law are to meet students' mental or
  behavioral health needs, and to increase academic achievement, including reducing academic disparities for the
  student groups the law names [SRC:legislature/ors/ors327.html]. ODE calls those groups "focal student groups":
  students of color, students with disabilities, emerging bilingual students, and students navigating poverty,
  homelessness and foster care, among others [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.3].
- The money may be used only for four kinds of things: more instructional time (longer days or years, summer and
  before- or after-school programs); students' health or safety (social-emotional learning, mental and behavioral
  health, school health professionals, trauma-informed practices, facility improvements directly related to health
  or safety); smaller classes or caseloads; and well-rounded learning (early literacy, middle school supports, art,
  music, physical education, science, technology, engineering and math, career and technical education, electives, college credit, dropout prevention,
  talented and gifted programs, library media educators) [SRC:legislature/ors/ors327.html].
- Each grant is a recipient's share of the money available, by its weighted enrollment (ADMw), with the poverty
  weight set at 0.5; virtual charter schools are taken out of the count [SRC:legislature/ors/ors327.html].

### How districts report and are held to it

- Each grant recipient must run a yearly financial audit of the grant money, post it and present it at a public
  meeting, and send it to ODE. ODE then decides each year whether the money was used as the grant agreement says;
  if not, it works with the recipient on interventions and technical assistance [SRC:legislature/ors/ors327.html].
- Grantees with at least 80 students must set Longitudinal Performance Growth Targets (LPGTs) for five common
  metrics: four-year graduation, five-year completion, 9th grade on-track, regular attendance and 3rd grade English
  language arts proficiency. The targets are co-developed with ODE, and "gap-closing" targets are set for a combined
  group of focal students [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.26]. The first set was agreed in 2023 for
  2023-24 through 2027-28 and written into grant agreements approved by each grantee's board
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.27] [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.39].
- In 2025 ODE paused adding more years of targets because of the Education Accountability Act (SB 141); grantees are
  to set new Performance Growth Targets with ODE in spring 2026, adding K-2 regular attenders and 8th grade math
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.27].
- Grantees also rate themselves each quarter on 15 "progress markers" (a 0-4 scale) and file a yearly narrative
  report [SRC:ode/sia/2025-09_progress-markers-annual-reporting-2023-24.pdf p.4]. Grantees are not required or
  expected to meet all progress markers; ODE uses them to target technical assistance and coaching
  [SRC:ode/sia/2025-09_progress-markers-annual-reporting-2023-24.pdf p.5].
- The SIA is now part of ODE's Integrated Programs, which combine several grant programs in one application.
  Grantees first applied in spring 2023 and again in spring 2025, for 2025-29
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.3] [SRC:ode/sia/2025-09_progress-markers-annual-reporting-2023-24.pdf p.4].

### How much was spent, by year

ODE's yearly legislative reports give each year's allocation and what grantees reported spending (copied into
`data/sia_spending.csv`) [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.23]:

| School year | Allocated | Reported spent | Source |
|---|---|---|---|
| 2020-21 | $150 million | $147,632,073 (98.4%) | [SRC:ode/sia/2022-01_sia-legislative-report.pdf p.13] |
| 2021-22 | $437,080,000 | $430,076,715 (98.4%) | [SRC:ode/sia/2023-01_sia-legislative-report.pdf p.16] |
| 2022-23 | $455,404,000 | $452,796,619 (99.4%) | [SRC:ode/sia/2024-01_sia-legislative-report.pdf p.22] |
| 2023-24 | $532,558,921 | $522,627,700 (98.1%) | [SRC:ode/sia/2025-01_sia-legislative-report.pdf p.19] |
| 2024-25 | $559,688,049 | $551,495,257 (98.6% of the 559,508,530 claimed) | [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.23] |

- About $472 million had been projected for the first year; the Legislature cut it to $150 million in an August 2020
  special session because of COVID-19's effect on the Corporate Activity Tax
  [SRC:ode/sia/2022-01_sia-legislative-report.pdf p.13].
- **Health and safety has been the largest category every year:** 41.7% in 2020-21, 33.9% in 2021-22, 36.7% in
  2022-23, 35.7% in 2023-24 and 33.5% ($184.9M) in 2024-25. Well-rounded education and smaller classes come next
  [SRC:ode/sia/2022-01_sia-legislative-report.pdf p.13] [SRC:ode/sia/2023-01_sia-legislative-report.pdf p.17]
  [SRC:ode/sia/2024-01_sia-legislative-report.pdf p.23] [SRC:ode/sia/2025-01_sia-legislative-report.pdf p.19]
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.23].
- **Most of it pays for people.** Salaries and benefits were 75.7% of spending in 2021-22, 81.7% in 2022-23 and in
  2023-24, and 85.8% ($473.3M) in 2024-25 [SRC:ode/sia/2023-01_sia-legislative-report.pdf p.17]
  [SRC:ode/sia/2024-01_sia-legislative-report.pdf p.23] [SRC:ode/sia/2025-01_sia-legislative-report.pdf p.19]
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.24]. In 2024-25, $282.7M went to licensed salaries; ODE notes its
  benefits figure is an underestimate, because some benefits were reported as salaries
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.24].
- The 2024-25 report prints the total spent as $551,495,257 in two places and as $551,495,297 once
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.23].

### What ODE reports about results

- **2024-25 targets (second year).** Of grantees required to set each target, these met their baseline target:
  9th grade on-track 124 of 167 (74.3%); regular attendance 93 of 187 (49.7%); 3rd grade English language arts 66 of
  171 (38.6%) [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.39] [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.40].
- For gap-closing targets: 9th grade on-track 85 of 137 (62.0%), regular attendance 122 of 182 (67.0%), 3rd grade
  English language arts 55 of 131 (42.0%) [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.39]
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.40].
- The median grantee's change from 2023-24 to 2024-25 for all students was 2.21 points in 9th grade on-track, 1.78
  in 3rd grade English language arts and 0.01 in regular attendance
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.39] [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.40].
- For 2023-24, more than half of grantees met their four-year graduation baseline and gap-closing targets; half met
  their five-year completion baseline target and 46.5% the gap-closing one; graduation and completion data for
  2024-25 come out later [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.28]
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.39].
- ODE calls the 9th grade on-track change "substantial" and says the larger median gains for focal students in
  attendance and on-track indicate "progress is being made to close the gaps"
  [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.41].
- ODE says targets vary a great deal among grantees, and that small grantees can see large jumps or drops when one
  student changes a metric by several points [SRC:ode/sia/2026-01_sia-legislative-report.pdf p.27].
- In grantees' 2023-24 self-ratings, ODE found most had made "lower order systemic changes" and were making steady
  progress toward higher-order changes; hiring, especially of mental and behavioral health professionals in rural
  areas, and 9th grade on-track and course scheduling were areas of ongoing work
  [SRC:ode/sia/2025-09_progress-markers-annual-reporting-2023-24.pdf p.4].

## Derived figures

| Figure | Value | Tag |
|---|---|---|
| SIA spending reported by grantees, 2020-21 to 2024-25 (our sum) | $2.105B | [DER:sia/spent_total_2020_25] |
| SIA allocations, 2020-21 to 2024-25 (our sum) | $2.135B | [DER:sia/allocated_total_2020_25] |
| Change in yearly spending, 2021-22 to 2024-25, not adjusted for inflation | 28.2% | [DER:sia/spent_growth_2021_22_to_2024_25] |
| Share of 2024-25 spending on health and safety, well-rounded education and smaller classes | 88.4% | [DER:sia/big3_share_2024_25] |

Each year's spending is as ODE extracted it for that year's report; later corrections are not included.

## Analysis

The spending picture is clear and consistent: districts spend almost all of their SIA money, mostly on staff, in
the same three categories every year. Health and safety leads every year. By the law's list, that category covers student mental and
behavioral health and school health professionals, which fits the first of the law's two purposes.

The results picture is much weaker, for three reasons in ODE's own reports. First, the targets measure grantees
against their own co-developed targets, not against what would have happened without the money, so meeting a
target doesn't show the SIA caused the change. Second, there are only two years of target data (2023-24 and
2024-25), and the target system is being replaced under SB 141. Third, the progress markers are self-ratings that
grantees are not expected to meet in full. On ODE's figures, about three in four grantees met their 9th grade on-track
target in 2024-25, about half met their attendance target, and fewer than two in five met their 3rd grade reading
target. Whether that is good depends on how ambitious the targets were, which ODE says varied a great deal.

So the archive can say what SIA money paid for, and how grantees did against their own targets in two recent years.
It can't yet say whether the SIA changed outcomes statewide. Outside audits and reviews (#103), outcomes over time
(#58) and the research on whether funding changes outcomes (#63) bear on that.
