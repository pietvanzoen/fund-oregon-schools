# What full funding is meant to buy: the Quality Education Model's practices and outcomes

How the Quality Education Commission links its Quality Education Model to practices in schools and to
student outcomes, and what research it cites for that link. The dollar figures are in `topics/quality-education-model.md`
and `data/qem_gap.csv`. Decisions this informs: `decisions.md#cost-model-2027`.

## Analysis

The Quality Education Model ties a staffing and program list to one outcome, a 90% four-year graduation rate, but the link is a
judgment, not a calculation. The commission itself says outcomes are not model inputs, and in 2022 said the model had
never statistically tied performance to cost. Its regressions of graduation on state funding per student since
2013-14 are a check on the estimate, not a derivation of it; they chart two trends that broadly rose over the same
years, which is consistent with funding mattering but does not by itself separate funding from other causes.

The strongest evidence the commission cites that money matters is outside research (Jackson's and Baker's reviews).
That research concerns spending in general rather than the model's particular practices, and research finding smaller
or no effects isn't archived yet (#63). What full funding "buys" in the
model is therefore best read as: the 2022 staffing list (smaller elementary
classes, counselors, nurses, librarians, summer school), priced at today's costs, plus an expectation that districts
use it on the recommended practices.

The counterfactual year for 90% graduation under full funding since 2012-13 moved from 2025-26 (2024 report) to
2027-28 (2026 report), and under current-service-level funding from 2027-28 to 2028-29, while the long-run trend year stayed at 2030-31. For five-year
completion the full-funding year moved from 2025-26 to 2027-28 and the long-run year from 2030-31 to 2033-34. The
2026 report doesn't explain the shift. The commission itself presents these paths as illustrating long-term impact, and a date
that moves two years in one report cycle supports reading them as illustrations rather than predictions.

The evaluators' $22,210 is aimed at a different, broader target than the model's (one standard deviation above the
statewide average on a combined measure), so the comparison shows direction (both say more is needed), not size. The
evaluators criticize the single outcome goal, and both they and the joint committee criticize prototypes that ignore
variation in need. In its 2026 report the commission agrees on the prototypes and is exploring broader outcome goals,
while saying it lacks the staff to act. With further changes to the model expected in 2027 (`decisions.md#cost-model-2027`), the
commission's direction overlaps with SB 141's terms: the extra goals it is exploring resemble the metrics its SB 141
fallback option names (reading proficiency, regular attenders, ninth grade on-track), and that option is framed around
SB 141 (sources below). The department's director has said the SB 141 targets don't require new money, a view some State Board
members doubted (`topics/results.md`).

## What the sources say

### What the model is
- The model is a professional judgment model, with a "Costing Model" component built on financial and other data the
  Oregon Department of Education has collected over 25 years [SRC:ode/qec/2026_qem_report.pdf p.92]. The commission defines the prototype schools'
  resources using professional judgment, research, statistical analysis of Oregon spending data, and a survey of
  public values [SRC:ode/qec/2026_qem_report.pdf p.94]. The model has nearly 500 inputs
  [SRC:ode/qec/2026_qem_report.pdf p.94].
- It gives two estimates: the status quo (the cost of continuing the prior two-year budget's services) and the full
  model (the status quo plus the resources to implement the commission's recommended best practices and improve outcomes)
  [SRC:ode/qec/2026_qem_report.pdf p.92].

### The prototype schools
- Since 1999 the model has costed three prototype schools, composites of an average elementary, middle and high
  school, not actual schools [SRC:ode/qec/2026_qem_report.pdf p.93]. The full model uses the commission's recommended
  ratios; the status quo uses actual staffing ratios from schools near the prototypes' size
  [SRC:ode/qec/2026_qem_report.pdf p.93].
- Elementary: 360 students, average class size 20, all-day kindergarten, a librarian, a nurse, a physical education and music
  specialist and a Family Resource staffer per school [SRC:ode/qec/2026_qem_report.pdf p.93].
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
  school adult, a librarian per school, Family Resource Center staff, physical education and music specialists, and lowered elementary
  class sizes from 23-24 to 20 [SRC:ode/qec/2022_qem_report.pdf p.12] [SRC:ode/qec/2022_qem_report.pdf p.13]. The
  2024 report added no inputs and evaluated no new assumptions, apart from "a small correction"
  [SRC:ode/qec/2024_qem_report.pdf p.63].
- The 2026 report made no discretionary changes to the inputs; staffing levels are identical to the 2024 model and
  the increase reflects market prices [SRC:ode/qec/2026_qem_report.pdf p.13] [SRC:ode/qec/2026_qem_report.pdf p.102].
  It excludes enhancements such as a 180-day school year [SRC:ode/qec/2026_qem_report.pdf p.102]. The report gives
  several reasons: time and financial limits after the American Institutes for Research evaluation [SRC:ode/qec/2026_qem_report.pdf p.13];
  the Legislature's work on a new way of estimating funding needs and "consensus about the shortcomings of the
  current model", which led commissioners to agree that significant changes should be informed by an improved model
  and process; and the state's acute fiscal challenges [SRC:ode/qec/2026_qem_report.pdf p.102]. It also says
  holding the judgment parameters steady across 2024 and 2026 keeps continuity with state budgeting
  [SRC:ode/qec/2026_qem_report.pdf p.108].

### The outcome the model is tied to
- The 2026 report says the practices it costs are expected to improve student outcomes "as measured in the 2025
  Education Accountability Act" (Senate Bill 141) [SRC:ode/qec/2026_qem_report.pdf p.13].
- The model assumes that with sustained full funding, and with districts implementing the recommended practices,
  90% of students would graduate within four years of entering ninth grade
  [SRC:ode/qec/2026_qem_report.pdf p.92]. Districts decide which practices they implement and how they spend
  [SRC:ode/qec/2026_qem_report.pdf p.92].
- The commission says the cost estimates "do not represent the exact amount of money needed to achieve exact
  educational outcomes" [SRC:ode/qec/2026_qem_report.pdf p.92] [SRC:ode/qec/2026_qem_report.pdf p.93]. Outcome measures inform commissioners' judgment
  but are not formal inputs to the model's arithmetic [SRC:ode/qec/2026_qem_report.pdf p.95]
  [SRC:ode/qec/2026_qem_report.pdf p.115].
- The 2024 report said the model "has not defined what dollars are needed to accelerate learning for all students in all
  schools", only what was needed to advance graduation rates to 90% [SRC:ode/qec/2024_qem_report.pdf p.18].
- The 2022 report said the model "has never statistically modeled performance changes directly tied to costs"; its
  projections came from literature syntheses [SRC:ode/qec/2022_qem_report.pdf p.6]. It described the assumption then
  as 90% of students meeting state standards, citing the 1999 model report
  [SRC:ode/qec/2022_qem_report.pdf p.11].
- The 1999 report assumed every school could reach the goal of 90% of students at benchmark standards, first
  in third grade and then at later benchmarks as that cohort moved up; a school not making progress would be at odds
  with the model's assumptions or using resources in ways that don't lead to learning
  [SRC:ode/qec/1999_qem_report.pdf p.17]. It called the model a tool to set a total budget, not a way to allocate
  money to districts [SRC:ode/qec/1999_qem_report.pdf p.17].

### The commission's own evidence: graduation regressions
- The 2024 and 2026 reports chart four-year graduation and five-year completer rates against State School Fund
  funding per weighted student from 2013-14, and say regression analyses show a statistically significant relationship between
  per-pupil spending and these rates over time [SRC:ode/qec/2024_qem_report.pdf p.58]
  [SRC:ode/qec/2024_qem_report.pdf p.60] [SRC:ode/qec/2026_qem_report.pdf p.95] [SRC:ode/qec/2026_qem_report.pdf p.96]
  [SRC:ode/qec/2026_qem_report.pdf p.98].
- The 2026 report says that had funding been at the full model's level since 2012-13, the state would be positioned to
  reach a 90% graduation rate, and a 90% five-year completer rate, by 2027-28
  [SRC:ode/qec/2026_qem_report.pdf p.95]. Its projected years for 90%: four-year graduation 2030-31 on the
  long-run trend, 2028-29 at current-service-level funding, 2027-28 at the full model; five-year completion 2033-34, 2030-31 and
  2027-28 [SRC:ode/qec/2026_qem_report.pdf p.95].
- The 2024 report's projected years were 2030-31, 2027-28 and 2025-26 for four-year graduation
  [SRC:ode/qec/2024_qem_report.pdf p.59], and 2030-31, 2030-31 and 2025-26 for five-year completion
  [SRC:ode/qec/2024_qem_report.pdf p.60]; its full-model years are likewise for funding at that level since 2012-13
  [SRC:ode/qec/2024_qem_report.pdf p.59] [SRC:ode/qec/2024_qem_report.pdf p.60]. The full-model years in
  both reports are counterfactuals (what full funding since 2012-13 would have produced), not projections of funding
  the model from now on [SRC:ode/qec/2024_qem_report.pdf p.59] [SRC:ode/qec/2026_qem_report.pdf p.95]. Both sets: `data/qem_outcome_forecasts.csv`.

### Research on funding and outcomes the commission cites
- The 2022 report cited research that student achievement rises when states invest in schools, especially for
  low-income students: a Center for American Progress report, Bruce Baker's review for the Learning Policy Institute,
  and C. Kirabo Jackson's review, which found 12 of 13 multi-state studies show a positive, statistically significant
  link between spending and student performance [SRC:ode/qec/2022_qem_report.pdf p.14].
- Two are archived: Baker's review [SRC:reference/2017-12_baker_how-money-matters-for-schools.pdf] and the Center for
  American Progress report, a policy organization's report, filed under `orgs/`
  [SRC:orgs/center-for-american-progress/2018-11-13_quality-approach-school-funding.html]. Jackson's review is cited
  here through the commission's report: its only public copy is a working paper marked not for quotation or distribution.
  Their own findings, alongside research that finds smaller effects, are for #63.
- The 2024 report's list of research articles includes Baker, Farrie and Sciarra (2016), "Mind the Gap: 20 Years of
  Progress and Retrenchment in School Funding and Achievement Gaps" (a 2016 research report), alongside studies of class size (Tennessee's Student Teacher
  Achievement Ratio project), early childhood programs and community schools [SRC:ode/qec/2024_qem_report.pdf p.112]
  [SRC:ode/qec/2024_qem_report.pdf p.113]. The 2026 report cites "Mind the Gap" too, for the
  statement that the impacts of socio-economic status on learning are well documented
  [SRC:ode/qec/2026_qem_report.pdf p.20]. It isn't archived yet (#79).
- The 2026 report presents its own regressions above and the American Institutes for Research's 2025 work below as evidence for its funding level [SRC:ode/qec/2026_qem_report.pdf p.95] [SRC:ode/qec/2026_qem_report.pdf p.100].

### The 2025 outside evaluation
- The American Institutes for Research submitted an evaluation of the model to the Legislative Policy and Research
  Office in January 2025 [SRC:legislature/lpro/2025-01_air_qem-evaluation.pdf p.1]. The evaluators found the model
  targets one goal, a 90% four-year graduation rate, though the goals in section 327.506 of the Oregon Revised
  Statutes are broader, and uses only three prototypes, so it doesn't show how
  costs vary with student need or locale [SRC:legislature/lpro/2025-01_air_qem-evaluation.pdf p.28]. It recommended
  more outcome goals and many more prototypes built from current Oregon data, noting the prototype sizes rest on
  research more than 25 years old [SRC:legislature/lpro/2025-01_air_qem-evaluation.pdf p.34].
- The evaluators wrote that their findings "do not invalidate the current QEM estimates": they found no omitted resources or
  inaccurate pricing [SRC:legislature/lpro/2025-01_air_qem-evaluation.pdf p.33].
- The evaluators' own cost model estimated adequate spending of $22,210 per pupil in 2022-23 against $17,136 actually spent
  from state and local sources, a 30% gap [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.40]
  [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.41] [SRC:ode/qec/2026_qem_report.pdf p.100]. Its target is
  raising achievement one standard deviation above the statewide average on a measure combining English language
  arts and math achievement, chronic absenteeism and graduation [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.41]
  [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.43]. The evaluators say their estimate being larger than
  the model's is
  "unsurprising" given its wider outcome target [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.45].
- The commission cites this to say its full-model target is conservative: $18,829 per pupil for 2022-23 against the
  evaluators' $22,210
  [SRC:ode/qec/2026_qem_report.pdf p.100].
- The evaluators say direct comparison is complicated because the two models include different funding and use different
  outcome goals [SRC:legislature/lpro/2025-01_air_cost-of-adequacy.pdf p.43].
- In response to the evaluation, the commission says it is exploring more adequacy goals (third grade English language arts
  proficiency, ninth grade on-track status, regular attendance) and agrees more prototype schools should be added but has
  lacked the staff to do so [SRC:ode/qec/2026_qem_report.pdf p.99]. It asks for 2.0 full-time-equivalent positions at the department in
  the next two-year budget to start, out of an estimated temporary build-up of 12.0-19.0 full-time equivalents over two to three budget periods [SRC:ode/qec/2026_qem_report.pdf p.116].

### A legislative committee's critique (November 2025)
- The Joint Committee on Public Education Appropriation's November 2025 report found that 2025-27 funding "effectively closes the funding gap and allows for the full
  implementation of the QEM" [SRC:legislature/olis/2025I1/310695_jpea.pdf p.4]; the 2026 model sets a higher bar for
  2027-29 (see `topics/quality-education-model.md`).
- The same report lists nine "opportunities for improvement" in the model
  [SRC:legislature/olis/2025I1/310695_jpea.pdf p.5]. Those bearing on practices and outcomes: the statutory goals
  behind the model "lack specificity"; the commission's use of the professional judgment model "does not
  guarantee that the QEC selects interventions that are proven to work"; some best practices in the report are not
  model inputs; the model schools don't account for variation in need; and there is "a notable lack of connection"
  among the model's best practices, districts' statutory requirements and what districts actually do
  [SRC:legislature/olis/2025I1/310695_jpea.pdf p.5].
- A legislative concept from the joint committee would move the cost model from the commission to the Legislative
  Policy and Research Office [SRC:legislature/olis/2025I1/311607_jpea-legislative-concepts.pdf p.1]. The joint
  committee introduced Senate Bill 1555 (2026) to
  carry out its recommendations [SRC:legislature/olis/2026R1/313103_sb1555-genesis-memo.pdf p.2], including that
  move [SRC:legislature/olis/2026R1/313691_sb1555-staff-measure-summary.pdf p.1]. A 2026 overhaul effort led by Rep.
  Ricki Ruiz, D-District 50 (Gresham), and Sen. Janeen Sollman, D-District 15 (Forest Grove, Cornelius, Hillsboro, Rock
  Creek), was unsuccessful [NEWS:NEWS-20260617-occ-1] [SRC:legislature/members/ruiz.html] [SRC:legislature/members/sollman.html]; SB 1555 did not pass [SRC:ode/qec/minutes/2026-10-21.pdf p.78].

### The practices the commission recommends (2026)
- The 2026 best-practices section is a synthesis of white papers by department and Educator Advancement Council
  experts, organized under the department's five Priorities for Student Success [SRC:ode/qec/2026_qem_report.pdf p.78]. The commission
  says many are better called "promising practices" whose success depends on local context
  [SRC:ode/qec/2026_qem_report.pdf p.76].
- Examples: culturally responsive high-quality instructional materials paired with curriculum-based coaching;
  formative assessment; multi-tiered systems of support and early warning systems; co-teaching for students with
  disabilities; mentoring through Regional Educator Networks [SRC:ode/qec/2026_qem_report.pdf p.79]
  [SRC:ode/qec/2026_qem_report.pdf p.80] [SRC:ode/qec/2026_qem_report.pdf p.81]
  [SRC:ode/qec/2026_qem_report.pdf p.84].
- The white papers, the cost-model workbook (Appendix C) and the survey results (Appendix D) are archived under
  `sources/ode/qec/` (`2026_white-papers/`, `2026_qem_appendix-c_cost-model.xlsx`,
  `2026_qem_appendix-d_best-practices-survey.pdf`); the report lists the white papers in Appendix E
  [SRC:ode/qec/2026_qem_report.pdf p.135].
- The model was not changed in 2026 to include the white papers' funding recommendations; the commission is reviewing
  them for future models [SRC:ode/qec/2026_qem_report.pdf p.87].
- Its 2026 survey of 200 self-selected respondents found practices rated effective were often not implemented,
  with staffing shortages and lack of time cited most; the commission calls this a convenience sample, not
  statewide evidence [SRC:ode/qec/2026_qem_report.pdf p.89] [SRC:ode/qec/2026_qem_report.pdf p.91].

### Recommendations beyond the dollar figure
- The primary recommendation is to fully fund the model [SRC:ode/qec/2026_qem_report.pdf p.109]. If that isn't
  possible, the commission advises against spreading money across small pilots and offers two alternatives under
  section 327.506(5) of the Oregon Revised Statutes [SRC:ode/qec/2026_qem_report.pdf p.109]:
  - **A holistic system of support**: wraparound services centered on districts (community provider and school
    coordination staff, housing support for families, space for services, family engagement grants, adult
    education), expected to improve school climate, regular attendance, student mental health and staff well-being
    [SRC:ode/qec/2026_qem_report.pdf p.109] [SRC:ode/qec/2026_qem_report.pdf p.110].
  - **Funding aimed at the SB 141 (Education Accountability Act) metrics**: for example, more for the Early Literacy Success
    Initiative (third grade reading), math support (eighth grade math, ninth grade on-track), early warning systems
    (attendance), early science, the English Learner Outcomes Program, and Secondary Career Pathway funding
    (graduation, career readiness), prioritizing the districts with greatest need [SRC:ode/qec/2026_qem_report.pdf p.110].
- Its nine 2026 recommendations also include avoiding isolated pilots, sustaining Student Success Act investments,
  expanding early learning, student mental health, community partnerships, fiscal transparency, a business case for an
  Educator Workforce Data System and a statewide data dashboard [SRC:ode/qec/2026_qem_report.pdf p.117]
  [SRC:ode/qec/2026_qem_report.pdf p.118].

## Derived figures

None: every figure under "What the sources say" is stated in a cited source.
