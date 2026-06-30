import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";

export const AGENT_RUN_PREDICTION_SERIES = [
  {
    seriesId: "bls.ces.average_hourly_earnings_private_mom",
    title: "Average hourly earnings monthly change",
    measure:
      "Monthly percent change in average hourly earnings for all private employees",
    unit: "percent_growth",
    source: "Bureau of Labor Statistics, Employment Situation first release",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 day",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: ["next release", "+3 months", "threshold"],
    whyItMatters:
      "Average hourly earnings connects labor-market tightness to household income and price pressure, and resolves on the same schedule as payrolls and unemployment.",
    drivers: [
      "Nominal wage growth",
      "Industry composition",
      "Hours mix",
      "Labor-market slack",
    ],
    history: [
      { label: "Feb", value: 0.3 },
      { label: "Mar", value: 0.2 },
      { label: "Apr", value: 0.2 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ series: "CES0500000003", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_level: 37.15, feb_level: 37.27, mar_level: 37.35, apr_level: 37.41, apr_mom_percent: 0.2 }",
    },
    targets: [
      {
        slug: "average-hourly-earnings-mom-may-2026",
        title: "Average hourly earnings, May 2026 month-over-month",
        question:
          "What will BLS first report as the May 2026 monthly percent change in average hourly earnings for all private employees?",
        dataPointId:
          "bls.ces.average_hourly_earnings_private.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-05",
        resolutionRule:
          "Resolves to the first published percent change from April to May 2026 in average hourly earnings for all employees on private nonfarm payrolls in the BLS Employment Situation release. Later revisions do not change the resolved value.",
        pointEstimate: 0.2,
        ciLow: 0.0,
        ciHigh: 0.4,
        rationale:
          "April earnings rose 0.2% to $37.41 and recent monthly changes have stayed near 0.2%-0.3%. The agent keeps the center at 0.2% because claims and payroll context do not yet point to wage acceleration.",
      },
    ],
  },
  {
    seriesId: "bls.cpi.u.core_mom",
    title: "Core CPI month-over-month",
    measure:
      "Seasonally adjusted month-over-month percent change in CPI-U less food and energy",
    unit: "percent_growth",
    source: "Bureau of Labor Statistics, Consumer Price Index first release",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 week",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: ["next release", "+12 months", "threshold"],
    whyItMatters:
      "Core CPI is the cleaner inflation-pressure target behind tax bracket indexing, poverty guideline indexing, and real-income adjustments.",
    drivers: [
      "Shelter services",
      "Core goods",
      "Medical care services",
      "Tariff pass-through",
    ],
    history: [
      { label: "Feb", value: 0.2 },
      { label: "Mar", value: 0.2 },
      { label: "Apr", value: 0.4 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ series: "CUSR0000SA0L1E", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_index: 332.793, feb_index: 333.512, mar_index: 334.165, apr_index: 335.423, apr_mom_percent: 0.4 }",
    },
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-06-06T23:43:56+02:00",
      agent: "Three-agent CPI ensemble",
      model: "Codex recorded agent ensemble",
      sourceContext: [
        "BLS April 2026 CPI release",
        "BLS CPI release schedule",
        "Cleveland Fed inflation nowcast",
        "EIA gasoline price series",
        "Independent component-model CPI agent",
      ],
    },
    targets: [
      {
        slug: "core-cpi-mom-may-2026",
        title: "Core CPI, May 2026 month-over-month",
        question:
          "What will BLS first report as the May 2026 seasonally adjusted month-over-month percent change in CPI-U less food and energy?",
        dataPointId: "bls.cpi.u.core_mom.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-10",
        resolutionRule:
          "Resolves to the first published May 2026 seasonally adjusted month-over-month percent change in CPI-U less food and energy in the BLS CPI release. Later seasonal-adjustment revisions do not change the resolved value.",
        pointEstimate: 0.3,
        ciLow: 0.1,
        ciHigh: 0.4,
        tools: [
          {
            tool: "clevelandfed.nowcast",
            call: 'clevelandfed.nowcast({ release: "May 2026 CPI", date: "2026-06-05", fields: ["headline_cpi_mom", "core_cpi_mom"] })',
            result: "{ headline_cpi_mom: 0.46, core_cpi_mom: 0.23 }",
          },
          {
            tool: "agent_ensemble.combine",
            call: 'agent_ensemble.combine({ target: "core-cpi-mom-may-2026", agents: 3, method: "equal_weighted" })',
            result:
              "{ agent_points: [0.24, 0.23, 0.29], ensemble_unrounded_point: 0.25, ensemble_ci80: [0.10, 0.40], likely_rounded_print: 0.3 }",
          },
        ],
        rationale:
          "Core CPI rose 0.4% in April after two 0.2% readings. The ensemble puts the unrounded center near 0.25%: shelter and services remain sticky, but April's rent/OER contribution is expected to fade enough that the modal rounded print is between 0.2% and 0.3%.",
      },
    ],
  },
  {
    seriesId: "bls.jolts.job_openings_total",
    title: "JOLTS job openings",
    measure: "Seasonally adjusted total nonfarm job openings",
    unit: "thousands",
    source:
      "Bureau of Labor Statistics, Job Openings and Labor Turnover Survey",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~4 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: ["next release", "+3 months", "threshold"],
    whyItMatters:
      "JOLTS openings add a labor-demand target that resolves after payrolls but before many policy outcomes, giving agents a useful intermediate calibration signal.",
    drivers: [
      "Private labor demand",
      "Small-business hiring plans",
      "Payroll growth",
      "Quits and hires momentum",
    ],
    history: [
      { label: "Jan", value: 7240 },
      { label: "Feb", value: 6922 },
      { label: "Mar", value: 6887 },
      { label: "Apr", value: 7618 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ series: "JTS000000000000000JOL", months: ["2026-01", "2026-04"] })',
      result: "{ jan: 7240, feb: 6922, mar: 6887, apr_preliminary: 7618 }",
    },
    targets: [
      {
        slug: "jolts-job-openings-may-2026",
        title: "JOLTS job openings, May 2026",
        question:
          "How many total nonfarm job openings will BLS first report for May 2026 in the Job Openings and Labor Turnover Survey?",
        dataPointId: "bls.jolts.job_openings_total.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-30",
        resolutionRule:
          "Resolves to the first published seasonally adjusted total nonfarm job openings estimate for May 2026 in the BLS JOLTS release. Later monthly revisions do not change the resolved value.",
        pointEstimate: 7450,
        ciLow: 6800,
        ciHigh: 8150,
        rationale:
          "April's preliminary openings jumped to 7.618 million after softer February-March readings. The agent partially fades that jump while keeping a wide interval because JOLTS first prints are noisy.",
      },
    ],
  },
  {
    seriesId: "usda.fns.snap.maximum_allotment_4person_48dc",
    type: "policy",
    title: "SNAP maximum allotment for a four-person household",
    measure:
      "Maximum monthly SNAP allotment for a four-person household in the 48 states and DC",
    unit: "usd_monthly",
    source: "USDA Food and Nutrition Service SNAP COLA tables",
    cadence: "annual",
    priority: "P1",
    resolutionLatency: "~3 months",
    resolutionPolicy: "first_print",
    benchmark: "Thrifty Food Plan inflation path",
    chainableQuestions: ["threshold", "+12 months", "program-cost impact"],
    whyItMatters:
      "SNAP maximum allotments are policy settings that feed directly into household resources, SPM poverty, and benefit outlay predictions.",
    drivers: [
      "Thrifty Food Plan cost",
      "Food-at-home inflation",
      "USDA rounding conventions",
      "Household-size scaling",
    ],
    history: [
      { label: "FY2024", value: 973 },
      { label: "FY2025", value: 975 },
      { label: "FY2026", value: 994 },
    ],
    historyTool: {
      tool: "usda.fns.lookup",
      call: 'usda.fns.lookup({ table: "snap_cola", measure: "maximum_allotment", household_size: 4, region: "48dc", fiscal_years: [2024, 2026] })',
      result: "{ fy2024: 973, fy2025: 975, fy2026: 994 }",
    },
    policyParameter:
      "snap.maximum_allotment.household_size_4.48_states_dc.fy2027",
    targets: [
      {
        slug: "snap-max-allotment-four-person-fy2027",
        title: "SNAP four-person maximum allotment, FY2027",
        question:
          "What will the FY2027 maximum monthly SNAP allotment be for a four-person household in the 48 states and DC, resolving whether it exceeds $1,020?",
        dataPointId:
          "usda.fns.snap.maximum_allotment.household_size_4.48dc.fy2027",
        horizon: "threshold",
        horizonLabel: "threshold",
        periodLabel: "FY2027",
        resolutionDate: "2026-09-30",
        resolutionRule:
          "Resolves to the first USDA FNS FY2027 SNAP COLA table for maximum monthly allotments, using household size 4 in the 48 contiguous states and DC. If USDA later revises the table, the first posted FY2027 table governs.",
        pointEstimate: 1022,
        ciLow: 1005,
        ciHigh: 1045,
        rationale:
          "The FY2026 value is $994. Crossing $1,020 requires about a 2.6% increase; the agent assigns a central value just above the threshold because food-plan inflation makes that plausible but not assured.",
      },
    ],
  },
  {
    seriesId: "hhs.aspe.poverty_guideline_4person_48dc",
    type: "policy",
    title: "HHS poverty guideline for a four-person household",
    measure:
      "Annual HHS poverty guideline for a four-person household in the 48 states and DC",
    unit: "usd",
    source: "HHS ASPE poverty guidelines",
    cadence: "annual",
    priority: "P1",
    resolutionLatency: "~7 months",
    resolutionPolicy: "first_print",
    benchmark: "CPI-U-based poverty guideline computation",
    chainableQuestions: ["next release", "threshold", "program eligibility"],
    whyItMatters:
      "The poverty guideline is a policy setting used across Medicaid, marketplace subsidies, legal aid, and other eligibility thresholds.",
    drivers: [
      "Calendar-year CPI-U",
      "Census poverty threshold base",
      "ASPE rounding",
      "Household-size simplification",
    ],
    history: [
      { label: "2024", value: 31200 },
      { label: "2025", value: 32150 },
      { label: "2026", value: 33000 },
    ],
    historyTool: {
      tool: "hhs.aspe.lookup",
      call: 'hhs.aspe.lookup({ table: "poverty_guidelines", household_size: 4, region: "48dc", years: [2024, 2026] })',
      result: "{ y2024: 31200, y2025: 32150, y2026: 33000 }",
    },
    policyParameter: "hhs.poverty_guideline.household_size_4.48_states_dc.2027",
    targets: [
      {
        slug: "hhs-poverty-guideline-family-four-2027",
        title: "HHS poverty guideline, family of four, 2027",
        question:
          "What will the 2027 HHS poverty guideline be for a four-person household in the 48 contiguous states and DC?",
        dataPointId: "hhs.aspe.poverty_guideline.household_size_4.48dc.2027",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "2027 guidelines",
        resolutionDate: "2027-01-31",
        resolutionRule:
          "Resolves to ASPE's first posted 2027 poverty guideline table for four-person households in the 48 contiguous states and DC. Later errata do not change the resolved value unless ASPE withdraws the first table before it takes effect.",
        pointEstimate: 33920,
        ciLow: 33520,
        ciHigh: 34480,
        rationale:
          "The 2026 value is $33,000. A moderate CPI-U adjustment should lift the 2027 guideline by roughly $800-$1,400, with remaining uncertainty from the poverty-threshold base and rounding.",
      },
    ],
  },
  {
    seriesId: "irs.irc24.child_tax_credit.maximum",
    type: "policy",
    title: "Child Tax Credit maximum per qualifying child",
    measure: "Maximum Child Tax Credit per qualifying child",
    unit: "usd",
    source: "IRS annual tax inflation adjustments and IRC section 24",
    cadence: "annual",
    priority: "P1",
    resolutionLatency: "~4 months",
    resolutionPolicy: "first_print",
    benchmark: "IRS inflation-adjustment guidance",
    chainableQuestions: ["threshold", "+12 months", "poverty impact"],
    whyItMatters:
      "The Child Tax Credit maximum is a policy setting with direct consequences for tax liability, refundable credits, child poverty, and PolicyEngine baseline assumptions.",
    drivers: [
      "Statutory credit amount",
      "Inflation indexing",
      "IRS rounding",
      "Legislative amendments",
    ],
    history: [
      { label: "TY2021", value: 3000 },
      { label: "TY2025", value: 2000 },
      { label: "TY2026", value: 2200 },
    ],
    historyTool: {
      tool: "irs.lookup",
      call: 'irs.lookup({ guidance: "tax_inflation_adjustments", parameter: "child_tax_credit_maximum", tax_years: [2021, 2026] })',
      result: "{ ty2021_expanded: 3000, ty2025: 2000, ty2026: 2200 }",
    },
    policyParameter: "irs.irc24.child_tax_credit.maximum.ty2027",
    targets: [
      {
        slug: "ctc-maximum-per-child-ty2027",
        title: "Child Tax Credit maximum, TY2027",
        question:
          "What will the maximum Child Tax Credit per qualifying child be for tax year 2027, resolving whether it exceeds $2,250?",
        dataPointId: "irs.irc24.child_tax_credit.maximum.ty2027",
        horizon: "threshold",
        horizonLabel: "threshold",
        periodLabel: "Tax year 2027",
        resolutionDate: "2026-10-31",
        resolutionRule:
          "Resolves to the first official IRS tax year 2027 inflation-adjustment guidance for the IRC section 24 maximum Child Tax Credit per qualifying child. If Congress changes the statutory amount before the guidance takes effect, the first IRS guidance implementing that law governs.",
        pointEstimate: 2300,
        ciLow: 2200,
        ciHigh: 2500,
        rationale:
          "The agent centers on $2,300 because TY2026 guidance places the amount near $2,200 and inflation indexing plus rounding can move the TY2027 setting above $2,250. The interval leaves room for no upward rounding or a larger statutory change.",
      },
    ],
  },
  {
    seriesId: "usda.fns.snap.participation",
    title: "SNAP participation",
    measure: "National monthly SNAP persons count",
    unit: "millions",
    source: "USDA Food and Nutrition Service SNAP national data tables",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~3 months",
    resolutionPolicy: "fixed_vintage",
    benchmark: "Recent monthly administrative trend",
    chainableQuestions: ["next release", "+3 months", "program-cost impact"],
    whyItMatters:
      "SNAP participation is a direct administrative calibration target for eligibility, take-up, benefit outlay, and poverty-resource predictions.",
    drivers: [
      "Employment and earnings",
      "State recertification rules",
      "Eligibility changes",
      "Administrative reporting revisions",
    ],
    history: [
      { label: "Nov", value: 39.4 },
      { label: "Dec", value: 38.8 },
      { label: "Jan", value: 38.2 },
      { label: "Feb", value: 37.9 },
    ],
    historyTool: {
      tool: "usda.fns.lookup",
      call: 'usda.fns.lookup({ program: "snap", table: "national_view_summary", measure: "persons", months: ["2025-11", "2026-02"] })',
      result:
        "{ feb2026_persons: 37870817, data_as_of: '2026-05-08', preliminary: true }",
    },
    targets: [
      {
        slug: "snap-participation-march-2026",
        title: "SNAP participation, March 2026",
        question:
          "How many people will USDA FNS report participating in SNAP in March 2026 in the national monthly data tables?",
        dataPointId: "usda.fns.snap.participation.march_2026.fixed_vintage",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "March 2026",
        resolutionDate: "2026-07-31",
        resolutionRule:
          "Resolves to the national March 2026 SNAP persons count in the USDA FNS FY2026 National View Summary, using the first table update available by July 31, 2026. Later revisions do not change the resolved value.",
        pointEstimate: 37.1,
        ciLow: 36.4,
        ciHigh: 37.8,
        rationale:
          "February 2026 participation was about 37.87 million. The agent expects continued decline from recent administrative trend, with a wide enough interval for reporting revisions and state recertification noise.",
      },
    ],
  },
  {
    seriesId: "usda.fns.wic.total_participants",
    title: "WIC total participation",
    measure: "National monthly WIC total participants",
    unit: "millions",
    source: "USDA Food and Nutrition Service WIC program data",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~3 months",
    resolutionPolicy: "fixed_vintage",
    benchmark: "Recent monthly administrative trend",
    chainableQuestions: ["next release", "+3 months", "child participation"],
    whyItMatters:
      "WIC participation tests whether agents can track benefit-program take-up, recertification, birth-cohort effects, and program-operation changes.",
    drivers: [
      "Birth cohort size",
      "Child caseload retention",
      "Food package value",
      "State outreach",
    ],
    history: [
      { label: "Nov", value: 6.78 },
      { label: "Dec", value: 6.7 },
      { label: "Jan", value: 6.66 },
      { label: "Feb", value: 6.64 },
    ],
    historyTool: {
      tool: "usda.fns.lookup",
      call: 'usda.fns.lookup({ program: "wic", measure: "total_participants", months: ["2025-11", "2026-02"] })',
      result:
        "{ feb2026_total_participants: 6640819, data_as_of: '2026-05-08', preliminary: true }",
    },
    targets: [
      {
        slug: "wic-total-participation-march-2026",
        title: "WIC total participation, March 2026",
        question:
          "How many total WIC participants will USDA FNS report for March 2026 in the national monthly program data?",
        dataPointId: "usda.fns.wic.total_participants.march_2026.fixed_vintage",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "March 2026",
        resolutionDate: "2026-07-31",
        resolutionRule:
          "Resolves to the national March 2026 WIC total participants value in USDA FNS monthly program data, using the first table update available by July 31, 2026. Later revisions do not change the resolved value.",
        pointEstimate: 6.61,
        ciLow: 6.5,
        ciHigh: 6.75,
        rationale:
          "February 2026 total participation was 6.64 million. The agent splits the recent downward FY2026 trend against a possible March seasonal rebound.",
      },
    ],
  },
  {
    seriesId: "cms.medicaid_chip.monthly_enrollment",
    title: "Medicaid and CHIP monthly enrollment",
    measure: "Preliminary total Medicaid and CHIP enrollment",
    unit: "millions",
    source: "CMS Medicaid and CHIP monthly enrollment data",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~3 months",
    resolutionPolicy: "fixed_vintage",
    benchmark: "Recent monthly CMS trend",
    chainableQuestions: ["next release", "+3 months", "coverage impact"],
    whyItMatters:
      "Medicaid and CHIP enrollment is a near-term administrative bridge between eligibility rules, renewal operations, and later Census coverage outcomes.",
    drivers: [
      "Renewals and redeterminations",
      "State processing",
      "Labor-market income",
      "CHIP churn",
    ],
    history: [
      { label: "Nov", value: 76.2 },
      { label: "Dec", value: 75.6 },
      { label: "Jan", value: 75.1 },
      { label: "Feb", value: 74.9 },
    ],
    historyTool: {
      tool: "cms.lookup",
      call: 'cms.lookup({ dataset: "monthly_medicaid_chip_enrollment", measure: "total_enrollment", months: ["2025-11", "2026-02"] })',
      result:
        "{ feb2026_preliminary_total_enrollment: 74877742, last_updated: '2026-05-29' }",
    },
    targets: [
      {
        slug: "medicaid-chip-enrollment-march-2026",
        title: "Medicaid and CHIP enrollment, March 2026",
        question:
          "How many people will CMS report enrolled in Medicaid and CHIP for March 2026 in preliminary monthly enrollment data?",
        dataPointId:
          "cms.medicaid_chip.total_enrollment.march_2026.fixed_vintage",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "March 2026",
        resolutionDate: "2026-07-31",
        resolutionRule:
          "Resolves to CMS preliminary March 2026 total Medicaid and CHIP enrollment for the 50 states and DC, using the first monthly enrollment update available by July 31, 2026. Later revisions do not change the resolved value.",
        pointEstimate: 74.4,
        ciLow: 74.0,
        ciHigh: 74.8,
        rationale:
          "CMS preliminary February enrollment was 74.88 million. The agent expects another decline, with the unwinding tail still visible but slowing.",
      },
    ],
  },
  {
    seriesId: "irs.filing_season.total_refunds",
    title: "IRS cumulative refund amount",
    measure: "Total amount refunded in IRS filing-season statistics",
    unit: "usd_billions",
    source: "IRS Filing Season Statistics",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~4 months",
    resolutionPolicy: "first_print",
    benchmark: "Historical May-to-October refund additions",
    chainableQuestions: ["next release", "+3 months", "refundable-credit mix"],
    whyItMatters:
      "IRS cumulative refunds connect filing behavior, withholding, refundable credits, processing pace, and tax-year liability into a near-term administrative target.",
    drivers: [
      "Refund count",
      "Average refund",
      "Processing pace",
      "Refundable credits",
    ],
    history: [
      { label: "May 2023", value: 287 },
      { label: "May 2024", value: 294 },
      { label: "May 2025", value: 275 },
      { label: "May 2026", value: 324.8 },
    ],
    historyTool: {
      tool: "irs.lookup",
      call: 'irs.lookup({ dataset: "filing_season_statistics", measure: "total_amount_refunded", snapshots: ["2026-05-08", "october_prior_years"] })',
      result:
        "{ may_8_2026_refunds_billions: 324.757, average_refund: 3276, historical_may_to_october_addition_billions: 41.8 }",
    },
    targets: [
      {
        slug: "irs-total-refunds-october-2026",
        title: "IRS cumulative refunds, October 2026",
        question:
          "What total refund amount will IRS report in its first October 2026 filing-season statistics snapshot for current-year individual returns?",
        dataPointId:
          "irs.filing_season.total_amount_refunded.october_2026.first_print",
        horizon: "plus_3m",
        horizonLabel: "+3 months",
        periodLabel: "October 2026 snapshot",
        resolutionDate: "2026-10-31",
        resolutionRule:
          "Resolves to IRS Filing Season Statistics total amount refunded for current-year individual returns in the first October 2026 snapshot. If IRS publishes multiple October snapshots, the earliest October table governs.",
        pointEstimate: 370,
        ciLow: 360,
        ciHigh: 382,
        rationale:
          "IRS reported $324.757 billion refunded by May 8, 2026. Historical May-to-October additions average about $41.8 billion, and the larger 2026 refund pace nudges the estimate above that mechanical add-on.",
      },
    ],
  },
] satisfies PredictionSeries[];

export const AGENT_RUN_EXAMPLES = buildForecastCellsFromSeries(
  AGENT_RUN_PREDICTION_SERIES,
);
