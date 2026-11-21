# What full funding is meant to buy: the QEM's practices and outcomes

How the Quality Education Commission (QEC) links its Quality Education Model (QEM) to practices in schools and to
student outcomes, and what research it cites for that link. The dollar figures are in `BRIEFING.md` (section d) and
`data/qem_gap.csv`.

## What the sources say

### What the model is
- The QEM is a professional judgment model, with a "Costing Model" component built on financial and other data ODE
  has collected over 25 years [SRC:ode/qec/2026_qem_report.pdf p.92]. The commission defines the prototype schools'
  resources using professional judgment, research, statistical analysis of Oregon spending data, and a survey of
  public values [SRC:ode/qec/2026_qem_report.pdf p.94]. The model has nearly 500 inputs
  [SRC:ode/qec/2026_qem_report.pdf p.94].
- It gives two estimates: the Status Quo (the cost of continuing the prior biennium's services) and the Full QEM (the
  status quo plus the resources to implement the commission's recommended best practices and improve outcomes)
  [SRC:ode/qec/2026_qem_report.pdf p.92].

### The prototype schools
- Since 1999 the model has costed three prototype schools, composites of an average elementary, middle and high
  school, not actual schools [SRC:ode/qec/2026_qem_report.pdf p.93]. The Full QEM uses the commission's recommended
  ratios; the Status Quo uses actual staffing ratios from schools near the prototypes' size
  [SRC:ode/qec/2026_qem_report.pdf p.93].
- Elementary: 360 students, average class size 20, all-day kindergarten, a librarian, a nurse, physical education and music
  specialists and a Family Resource staffer per school [SRC:ode/qec/2026_qem_report.pdf p.93].
- Middle: 500 students, average class size 17.7, 1.5 additional math, English and science teachers, alternative
  programs, one counselor per 250 students, a volunteer coordinator and community outreach worker
  [SRC:ode/qec/2026_qem_report.pdf p.93].
- High: 1,000 students, average class size 20.7, 3.0 additional math, English and science teachers, one counselor per
  250 students, a school-to-work coordinator [SRC:ode/qec/2026_qem_report.pdf p.93]. Full list:
  `data/qem_prototype_schools.csv`.
- The commission cites an Education Northwest synthesis for effective elementary (300-400) and middle school
  (400-800) sizes, and Lee and Smith (1997) for an ideal high school of 600-900 students
  [SRC:ode/qec/2026_qem_report.pdf p.93]. The synthesis it cites, Kathleen Cotton's 1996 review, gives 300-400 for an
  elementary school and 400-800 for "a secondary school", quoting another researcher's average of the research
  [SRC:reference/1996-05_cotton_school-size-climate-performance.pdf p.3].
- The current practices were last changed in the 2022 report, which added nurses (1:750), counselors (1:250), summer
  school, lower English learner staffing ratios, three professional development days, one device per student and
  school adult, a librarian per school, Family Resource Center staff, physical education and music specialists, and cut elementary
  class sizes from 23-24 to 20 [SRC:ode/qec/2022_qem_report.pdf p.12] [SRC:ode/qec/2022_qem_report.pdf p.13].
- The 2026 report made no discretionary changes to the inputs; staffing levels are identical to the 2024 model and
  the increase reflects market prices [SRC:ode/qec/2026_qem_report.pdf p.13] [SRC:ode/qec/2026_qem_report.pdf p.102].
  It excludes enhancements such as a 180-day school year [SRC:ode/qec/2026_qem_report.pdf p.102].

### The outcome the model is tied to
- The model assumes that with sustained full funding, and with districts implementing the recommended practices,
  90 percent of students would graduate within four years of entering ninth grade
  [SRC:ode/qec/2026_qem_report.pdf p.92]. Districts decide which practices they implement and how they spend
  [SRC:ode/qec/2026_qem_report.pdf p.92].
- The commission says the cost estimates "do not represent the exact amount of money needed to achieve exact
  educational outcomes" [SRC:ode/qec/2026_qem_report.pdf p.92]. Outcome measures inform commissioners' judgment
  but are not formal inputs to the model's arithmetic [SRC:ode/qec/2026_qem_report.pdf p.95]
  [SRC:ode/qec/2026_qem_report.pdf p.115].
- The 2024 report said the model "has not defined what dollars are needed to accelerate learning for all students",
  only what was needed to advance graduation rates to 90% [SRC:ode/qec/2024_qem_report.pdf p.18].
- The 2022 report said the QEM "has never statistically modeled performance changes directly tied to costs"; its
  projections came from literature syntheses [SRC:ode/qec/2022_qem_report.pdf p.6]. It described the assumption then
  as 90 percent of students meeting state standards, citing the 1999 model report
  [SRC:ode/qec/2022_qem_report.pdf p.11].
- The 1999 report assumed every school could reach the goal of 90 percent of students at benchmark standards, first
  in third grade and then at later benchmarks as that cohort moved up; a school not making progress would be at odds
  with the model's assumptions or using resources in ways that don't lead to learning
  [SRC:ode/qec/1999_qem_report.pdf p.17]. It called the model a tool to set a total budget, not a way to allocate
  money to districts [SRC:ode/qec/1999_qem_report.pdf p.17].

### The commission's own evidence: graduation regressions
- The 2024 and 2026 reports chart four-year graduation and five-year completer rates against State School Fund
  funding per ADMw from 2013-14, and say regression analyses show a statistically significant relationship between
  per-pupil spending and these rates over time [SRC:ode/qec/2024_qem_report.pdf p.58]
  [SRC:ode/qec/2026_qem_report.pdf p.95] [SRC:ode/qec/2026_qem_report.pdf p.96].
- The 2026 report says that had funding been at the Full QEM level since 2012-13, the state would be positioned to
  reach a 90 percent graduation rate, and a 90 percent five-year completer rate, by 2027-28
  [SRC:ode/qec/2026_qem_report.pdf p.95]. Its projected years for 90 percent: four-year graduation 2030-31 on the
  long-run trend, 2028-29 at CSL funding, 2027-28 at the Full QEM; five-year completion 2033-34, 2030-31 and
  2027-28 [SRC:ode/qec/2026_qem_report.pdf p.95].
- The 2024 report's projected years for four-year graduation were 2030-31, 2027-28 and 2025-26
  [SRC:ode/qec/2024_qem_report.pdf p.59]. Both sets: `data/qem_outcome_forecasts.csv`.

### Research on funding and outcomes the commission cites
- The 2022 report cited research that student achievement rises when states invest in schools, especially for
  low-income students: a Center for American Progress report, Bruce Baker's review for the Learning Policy Institute,
  and C. Kirabo Jackson's review, which found 12 of 13 multi-state studies show a positive, statistically significant
  link between spending and student performance [SRC:ode/qec/2022_qem_report.pdf p.14].
- All three are archived: Jackson's review in its public working-paper version, which gives the same 12-of-13 count
  [SRC:reference/2019-01_jackson_does-school-spending-matter.pdf p.10]; Baker's review
  [SRC:reference/2017-12_baker_how-money-matters-for-schools.pdf]; and the Center for American Progress report, an
  advocacy think tank's work [SRC:orgs/center-for-american-progress/2018-11-13_quality-approach-school-funding.html].
  Their own findings, alongside research that finds smaller effects, are for #63.
- The 2024 report's list of research articles includes Baker, Farrie and Sciarra (2016), "Mind the Gap: 20 Years of
  Progress and Retrenchment in School Funding and Achievement Gaps", alongside studies of class size (Tennessee's Student Teacher
  Achievement Ratio (STAR) project), early childhood programs and community schools [SRC:ode/qec/2024_qem_report.pdf p.112]
  [SRC:ode/qec/2024_qem_report.pdf p.113]. "Mind the Gap" isn't archived yet (#79).
- The 2026 report presents its own regressions above and AIR's 2025 work below as evidence for its funding level [SRC:ode/qec/2026_qem_report.pdf p.95] [SRC:ode/qec/2026_qem_report.pdf p.100].

### The 2025 AIR evaluation
- The Legislative Policy and Research Office contracted the American Institutes for Research (AIR) to evaluate the
  QEM [SRC:legislature/lpro/2025-01_air_qem-evaluation.pdf p.1]. AIR found the QEM targets one goal, a 90% four-year
  graduation rate, though the goals in ORS 327.506 are broader, and uses only three prototypes, so it doesn't show how
  costs vary with student need or locale [SRC:legislature/lpro/2025-01_air_qem-evaluation.pdf p.28]. It recommended
  more outcome goals and many more prototypes built from current Oregon data, noting the prototype sizes rest on
  research more than 25 years old [SRC:legislature/lpro/2025-01_air_qem-evaluation.pdf p.34].
- AIR wrote that its findings "do not invalidate the current QEM estimates": it found no omitted resources or
  inaccurate pricing [SRC:legislature/lpro/2025-01_air_qem-evaluation.pdf p.33].
- AIR's own cost model estimated adequate spending of $22,210 per pupil in 2022-23 against $17,136 actually spent
  from state and local sources, a 30% gap [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.41]. Its target is
  raising achievement one standard deviation above the statewide average on a measure combining ELA and math
  achievement, chronic absenteeism and graduation [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.41]
  [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.43]. AIR says its estimate being larger than the QEM's is
  "unsurprising" given its wider outcome target [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.45].
- The QEC cites this to say its Full QEM target is conservative: $18,829 per pupil for 2022-23 against AIR's $22,210
  [SRC:ode/qec/2026_qem_report.pdf p.100].
- The commission says it is exploring more outcome goals (3rd grade ELA proficiency, 9th grade on-track, regular
  attendance) and agrees more prototypes should be added but has lacked staff to do so
  [SRC:ode/qec/2026_qem_report.pdf p.99]. It asks for 2.0 FTE at ODE in the upcoming biennium to start, out of an estimated
  12.0-19.0 FTE build-out over two to three biennia [SRC:ode/qec/2026_qem_report.pdf p.116].

### The practices the commission recommends (2026)
- The 2026 best-practices section is a synthesis of white papers by ODE and Educator Advancement Council experts,
  organized under ODE's five Priorities for Student Success [SRC:ode/qec/2026_qem_report.pdf p.78]. The commission
  says many are better called "promising practices" whose success depends on local context
  [SRC:ode/qec/2026_qem_report.pdf p.76].
- Examples: culturally responsive high-quality instructional materials paired with curriculum-based coaching;
  formative assessment; multi-tiered systems of support and early warning systems; co-teaching for students with
  disabilities; mentoring through Regional Educator Networks [SRC:ode/qec/2026_qem_report.pdf p.79]
  [SRC:ode/qec/2026_qem_report.pdf p.80] [SRC:ode/qec/2026_qem_report.pdf p.81]
  [SRC:ode/qec/2026_qem_report.pdf p.84].
- The model was not changed in 2026 to include the white papers' funding recommendations; the commission is reviewing
  them for future models [SRC:ode/qec/2026_qem_report.pdf p.87].
- Its 2026 survey of 200 self-selected respondents found practices rated effective were often not implemented,
  with staffing shortages and lack of time cited most; the commission calls this a convenience sample, not
  statewide evidence [SRC:ode/qec/2026_qem_report.pdf p.89] [SRC:ode/qec/2026_qem_report.pdf p.91].

### Recommendations beyond the dollar figure
- The primary recommendation is to fully fund the QEM [SRC:ode/qec/2026_qem_report.pdf p.109]. If that isn't
  possible, the commission advises against spreading money across small pilots and offers two alternatives under
  ORS 327.506(5) [SRC:ode/qec/2026_qem_report.pdf p.109]:
  - **A holistic system of support**: wraparound services centered on districts (community provider and school
    coordination staff, housing support for families, space for services, family engagement grants, adult
    education), expected to improve school climate, regular attendance, student mental health and staff well-being
    [SRC:ode/qec/2026_qem_report.pdf p.109] [SRC:ode/qec/2026_qem_report.pdf p.110].
  - **Funding aimed at the SB 141 (Education Accountability Act) metrics**: e.g. more for the Early Literacy Success
    Initiative (3rd grade reading), math support (8th grade math, 9th grade on-track), early warning systems
    (attendance), early science, the English Learner Outcomes Program, and Secondary Career Pathway funding
    (graduation, career readiness), prioritizing the districts with greatest need [SRC:ode/qec/2026_qem_report.pdf p.110].
- Its nine 2026 recommendations also include avoiding isolated pilots, sustaining Student Success Act investments,
  expanding early learning, student mental health, community partnerships, fiscal transparency, an educator workforce
  data system and a statewide data dashboard [SRC:ode/qec/2026_qem_report.pdf p.117]
  [SRC:ode/qec/2026_qem_report.pdf p.118].

## Derived figures

None: every figure above is stated in a cited source.

## Analysis

The QEM ties a staffing and program list to one outcome, a 90% four-year graduation rate, but the link is a
judgment, not a calculation. The commission itself says outcomes are not model inputs, and in 2022 said the model had
never statistically tied performance to cost. Its regressions of graduation on state funding per student since
2013-14 are a check on the estimate, not a derivation of it; they chart two trends that both rose over the same
years, which is consistent with funding mattering but does not by itself separate funding from other causes.

The strongest evidence the commission cites that money matters is outside research (Jackson's review of
quasi-experimental studies, Baker's review), which concerns spending in general rather than the QEM's particular
practices. What full funding "buys" in the QEM is therefore best read as: the 2022 staffing list (smaller elementary
classes, counselors, nurses, librarians, summer school), priced at today's costs, plus an expectation that districts
use it on the recommended practices.

The projected year for 90% graduation under full funding moved from 2025-26 (2024 report) to 2027-28 (2026 report),
and under CSL funding from 2027-28 to 2028-29, while the long-run trend year stayed at 2030-31. The 2026 report
doesn't explain the shift; a forecast that slides two years in one report cycle is a reason to treat these dates as
illustrations rather than predictions.

AIR's $22,210 is aimed at a different and higher target than the QEM's (one standard deviation above the statewide
average on a combined measure), so the QEC's reading of it as showing the Full QEM is "conservative" holds only in
the loose sense that both say more money is needed. Under the 2027 debate over replacing the QEM (`BRIEFING.md`
section c), the commission's alternatives aimed at SB 141 metrics are the part of its report that already speaks the
language of the new accountability system.
