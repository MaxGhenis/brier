import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";

export const LAUNCH_PREDICTION_SERIES = [
  {
    seriesId: "dol.eta.initial_claims.sa",
    title: "Initial jobless claims",
    measure: "Seasonally adjusted initial unemployment insurance claims",
    unit: "thousands",
    source: "U.S. Department of Labor, Unemployment Insurance Weekly Claims",
    cadence: "weekly",
    priority: "P0",
    resolutionLatency: "~5 days",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: ["next release", "+4 weeks", "threshold"],
    whyItMatters:
      "Initial claims are the fastest clean labor-market calibration target in the launch slate: weekly, objective, fixed-release, and benchmarkable against consensus.",
    drivers: [
      "Layoff notices",
      "Holiday-adjustment noise",
      "Continuing-claims drift",
      "Consensus benchmark spread",
    ],
    history: [
      { label: "4wk avg", value: 209 },
      { label: "May 23", value: 215 },
      { label: "May 16", value: 210 },
      { label: "May 9", value: 212 },
    ],
    historyTool: {
      tool: "dol.lookup",
      call: 'dol.lookup({ series: "initial_claims_sa", weeks: ["2026-05-09", "2026-05-16", "2026-05-23"], vintage: "latest_pre_release" })',
      result:
        "{ latest_week_ending_2026_05_23: 215, previous_revised: 210, four_week_average: 209 }",
    },
    targets: [
      {
        slug: "initial-jobless-claims-week-ending-2026-06-06",
        title: "Initial jobless claims, week ending Jun 6 2026",
        question:
          "How many seasonally adjusted initial unemployment insurance claims will the Department of Labor report for the week ending June 6, 2026?",
        dataPointId: "dol.eta.initial_claims.sa.week_ending_2026_06_06",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "week ending Jun 6 2026",
        resolutionDate: "2026-06-11",
        resolutionRule:
          "Resolves to the first published seasonally adjusted initial claims count for the week ending June 6, 2026 in the Department of Labor weekly claims release. Later revisions do not change the resolved value.",
        pointEstimate: 214,
        ciLow: 197,
        ciHigh: 233,
        tools: [
          {
            tool: "consensus.lookup",
            call: 'consensus.lookup({ indicator: "initial_jobless_claims", release: "2026-06-11" })',
            result: "{ median_thousands: 214, p10: 199, p90: 232 }",
          },
        ],
        rationale:
          "The agent run centers near the latest May 23 print and only slightly above the four-week average. Initial claims have stayed rangebound around 200k-215k, so the interval is tight enough to score the release while allowing a holiday-adjustment surprise.",
      },
    ],
  },
  {
    seriesId: "bls.ces.total_nonfarm_payroll_change",
    title: "Nonfarm payrolls",
    measure: "Monthly change in total nonfarm payroll employment",
    unit: "thousands",
    source: "Bureau of Labor Statistics, Employment Situation first release",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 week",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: [
      "next release",
      "+3 months",
      "+12 months",
      "threshold",
    ],
    whyItMatters:
      "Payrolls are crowded, but that is useful: Thesis can score itself against survey medians and show whether agents add value beyond consensus.",
    drivers: [
      "Private payroll diffusion",
      "Government hiring",
      "Birth-death model residual",
      "Weather and strike effects",
    ],
    history: [
      { label: "Feb", value: -156 },
      { label: "Mar", value: 185 },
      { label: "Apr", value: 115 },
      { label: "3mo avg", value: 48 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ survey: "CES", series: "total_nonfarm_change", months: ["2026-01", "2026-04"], vintage: "first_print" })',
      result:
        "{ jan_level: 158592, feb_change: -156, mar_change: 185, apr_change: 115, latest_level: 158736 }",
    },
    targets: [
      {
        slug: "nonfarm-payrolls-may-2026",
        title: "Nonfarm payrolls, May 2026",
        question:
          "How many jobs will be added to total nonfarm payroll employment in May 2026 in the first BLS Employment Situation release?",
        dataPointId:
          "bls.ces.total_nonfarm_payroll_change.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-05",
        resolutionRule:
          "Resolves to the first published May 2026 over-the-month change in total nonfarm payroll employment in the BLS Employment Situation release. Benchmark revisions and later monthly revisions do not change the resolved value.",
        pointEstimate: 85,
        ciLow: -60,
        ciHigh: 220,
        tools: [
          {
            tool: "consensus.lookup",
            call: 'consensus.lookup({ indicator: "nonfarm_payrolls", month: "2026-05" })',
            result: "{ median_thousands: 90, interquartile_range: [25, 155] }",
          },
        ],
        rationale:
          "The agent run lowers the center after the April +115k print and volatile first-quarter revisions. Claims remain low, but federal-government drag and weak net growth over the prior year keep the estimate below the earlier mock.",
      },
    ],
  },
  {
    seriesId: "bls.cps.unemployment_rate",
    title: "Unemployment rate",
    measure: "Seasonally adjusted U-3 unemployment rate",
    unit: "percent",
    source: "Bureau of Labor Statistics, Employment Situation first release",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 week",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: [
      "next release",
      "+3 months",
      "+12 months",
      "threshold",
    ],
    whyItMatters:
      "The unemployment rate pairs with payrolls but has different noise: household-survey employment, labor-force entry, and rounding to one decimal place.",
    drivers: [
      "Household survey employment",
      "Labor-force entry",
      "Temporary-layoff share",
      "Payroll-hours signal",
    ],
    history: [
      { label: "Jan", value: 4.3 },
      { label: "Feb", value: 4.4 },
      { label: "Mar", value: 4.3 },
      { label: "Apr", value: 4.3 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ survey: "CPS", series: "unemployment_rate_sa", months: ["2026-01", "2026-04"], vintage: "first_print" })',
      result: "{ jan: 4.3, feb: 4.4, mar: 4.3, apr: 4.3 }",
    },
    targets: [
      {
        slug: "unemployment-rate-may-2026-first-print",
        title: "Unemployment rate, May 2026",
        question:
          "What will the unemployment rate be for May 2026 in the first BLS Employment Situation release?",
        dataPointId: "bls.cps.unemployment_rate.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-05",
        resolutionRule:
          "Resolves to the first published seasonally adjusted U-3 unemployment rate for May 2026. Later population-control or seasonal-adjustment revisions do not change the resolved value.",
        pointEstimate: 4.3,
        ciLow: 4.1,
        ciHigh: 4.5,
        tools: [
          {
            tool: "consensus.lookup",
            call: 'consensus.lookup({ indicator: "unemployment_rate", month: "2026-05" })',
            result: "{ median_percent: 4.3, range_percent: [4.2, 4.4] }",
          },
        ],
        rationale:
          "The unemployment rate has held at 4.3% for two consecutive months after 4.4% in February. Claims and insured unemployment do not yet point to a sharp break, so the run keeps the center unchanged with a two-tenths 80% interval.",
      },
    ],
  },
  {
    seriesId: "bls.cpi.u.headline_mom",
    title: "Headline CPI month-over-month",
    measure: "Seasonally adjusted month-over-month percent change in CPI-U",
    unit: "percent_growth",
    source: "Bureau of Labor Statistics, Consumer Price Index first release",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: ["next release", "+12 months", "threshold"],
    whyItMatters:
      "CPI is a launch flagship because it resolves quickly, has a consensus benchmark, and feeds formula-driven policy parameters later in the year.",
    drivers: [
      "Shelter inflation",
      "Gasoline and energy prices",
      "Core goods disinflation",
      "Food-at-home prices",
    ],
    history: [
      { label: "Jan", value: 0.3 },
      { label: "Feb", value: 0.3 },
      { label: "Mar", value: 0.9 },
      { label: "Apr", value: 0.6 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ survey: "CPI", series: "CPI-U all items SA MoM", months: ["2026-01", "2026-04"], vintage: "first_print" })',
      result:
        "{ jan: 0.3, feb: 0.3, mar: 0.9, apr: 0.6, april_index: 332.407 }",
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
        slug: "cpi-headline-mom-may-2026",
        title: "Headline CPI, May 2026 month-over-month",
        question:
          "What will the seasonally adjusted month-over-month percent change in headline CPI-U be for May 2026?",
        dataPointId: "bls.cpi.u.headline_mom.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-10",
        resolutionRule:
          "Resolves to the first published seasonally adjusted month-over-month percent change in CPI-U for May 2026. Later seasonal-adjustment revisions do not change the resolved value.",
        pointEstimate: 0.5,
        ciLow: 0.3,
        ciHigh: 0.7,
        tools: [
          {
            tool: "clevelandfed.nowcast",
            call: 'clevelandfed.nowcast({ release: "May 2026 CPI", date: "2026-06-05", fields: ["headline_cpi_mom", "core_cpi_mom"] })',
            result: "{ headline_cpi_mom: 0.46, core_cpi_mom: 0.23 }",
          },
          {
            tool: "eia.lookup",
            call: 'eia.lookup({ series: "monthly_regular_gasoline_average", months: ["2026-04", "2026-05"] })',
            result:
              "{ april_dollars_per_gallon: 4.103, may_dollars_per_gallon: 4.479, may_vs_april_percent: 9.2 }",
          },
          {
            tool: "agent_ensemble.combine",
            call: 'agent_ensemble.combine({ target: "cpi-headline-mom-may-2026", agents: 3, method: "equal_weighted" })',
            result:
              "{ agent_points: [0.49, 0.48, 0.52], ensemble_point: 0.50, ensemble_ci80: [0.30, 0.70], likely_rounded_print: 0.5 }",
          },
        ],
        rationale:
          "Three independent CPI agents converged on a 0.5% rounded headline print. The common signal is another positive gasoline contribution, confirmed by EIA's May price path and Cleveland Fed's 0.46% nowcast, while the interval allows late-May fuel softness or a shelter/food surprise to move the rounded print.",
      },
    ],
  },
  {
    seriesId: "census.marts.retail_food_services_mom",
    title: "Retail sales month-over-month",
    measure:
      "Advance seasonally adjusted month-over-month percent change in retail and food services sales",
    unit: "percent_growth",
    source: "U.S. Census Bureau, Advance Monthly Retail Trade Survey",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: ["next release", "control group", "threshold"],
    whyItMatters:
      "Retail sales add a high-frequency demand-side series to the launch set and produce many derivable questions from one source.",
    drivers: [
      "Auto sales",
      "Gasoline station receipts",
      "Card-spending nowcasts",
      "Control-group momentum",
    ],
    history: [
      { label: "Feb", value: 2.2 },
      { label: "Mar", value: 1.6 },
      { label: "Apr", value: 0.5 },
    ],
    historyTool: {
      tool: "census.lookup",
      call: 'census.lookup({ survey: "MARTS", series: "adv44X72", months: ["2026-03", "2026-04"], vintage: "advance" })',
      result:
        "{ mar_sales_millions: 753370, apr_sales_millions: 757085, mar_mom_revised: 1.6, apr_mom: 0.5, apr_yoy: 4.9, may_release: '2026-06-17 08:30 ET' }",
    },
    targets: [
      {
        slug: "retail-sales-mom-may-2026",
        title: "Retail sales, May 2026 month-over-month",
        question:
          "What will the advance seasonally adjusted month-over-month percent change in U.S. retail and food services sales be for May 2026?",
        dataPointId: "census.marts.adv44x72.may_2026.monthly_change.advance",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-17",
        resolutionRule:
          "Resolves to the first advance estimate of the seasonally adjusted month-over-month percent change in total retail and food services sales for May 2026. Use the rounded headline value; if only levels are available, compute from Census adv44X72 seasonally adjusted levels in the same release and round to one decimal. Later revisions do not change the resolved value.",
        pointEstimate: 0.2,
        ciLow: -0.5,
        ciHigh: 0.9,
        tools: [
          {
            tool: "census.lookup",
            call: 'census.lookup({ survey: "MARTS advance", series: "adv44X72", fields: ["mar2026_level", "apr2026_level", "apr_mom", "may_release"] })',
            result:
              "{ mar_sales_millions: 753370, apr_sales_millions: 757085, apr_mom: 0.5, apr_yoy: 4.9, may_release: '2026-06-17' }",
          },
        ],
        rationale:
          "March and April nominal retail sales were strong, but the forecast centers below April's pace because some momentum should fade and gasoline receipts can drag the headline. Advance retail sales remain volatile, so the 80% interval spans a small decline through a near-1% gain.",
      },
    ],
  },
  {
    seriesId: "bea.pce.core_mom",
    title: "Core PCE month-over-month",
    measure:
      "Month-over-month percent change in the PCE price index excluding food and energy",
    unit: "percent_growth",
    source: "Bureau of Economic Analysis, Personal Income and Outlays",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~4 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Published consensus survey medians",
    chainableQuestions: ["next release", "+12 months", "threshold"],
    whyItMatters:
      "Core PCE gives the launch slate a second inflation target with a different source and mapping from CPI and PPI.",
    drivers: [
      "CPI-to-PCE mapping",
      "PPI health-care services",
      "Portfolio-management fees",
      "Airfares and lodging",
    ],
    history: [
      { label: "Jan", value: 0.3 },
      { label: "Feb", value: 0.2 },
      { label: "Mar", value: 0.1 },
      { label: "Apr", value: 0.1 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ release: "personal_income_outlays", series: "core_pce_mom", months: ["2026-01", "2026-04"], vintage: "first_print" })',
      result: "{ jan: 0.3, feb: 0.2, mar: 0.1, apr: 0.1 }",
    },
    targets: [
      {
        slug: "core-pce-mom-may-2026",
        title: "Core PCE, May 2026 month-over-month",
        question:
          "What will the month-over-month percent change in the core PCE price index be for May 2026 in BEA's Personal Income and Outlays release?",
        dataPointId: "bea.pce.core_mom.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published month-over-month percent change in the PCE price index excluding food and energy for May 2026. Later revisions do not change the resolved value.",
        pointEstimate: 0.2,
        ciLow: 0.1,
        ciHigh: 0.4,
        tools: [
          {
            tool: "bridge.lookup",
            call: 'bridge.lookup({ inputs: ["cpi_components", "ppi_components"], target: "core_pce_may_2026" })',
            result:
              '{ cpi_bridge: 0.22, ppi_health_services: "neutral", financial_services: "firm" }',
          },
        ],
        rationale:
          "The bridge points to another 0.2% print. The upper interval leaves room for financial-services and health-care categories that CPI does not measure cleanly.",
      },
    ],
  },
  {
    seriesId: "usda.fns.snap.persons",
    title: "SNAP participation",
    measure: "Average monthly persons participating in SNAP",
    unit: "millions",
    source: "USDA Food and Nutrition Service, SNAP national monthly data",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 months",
    resolutionPolicy: "fixed_vintage",
    benchmark: "PolicyEngine eligibility/take-up prior",
    chainableQuestions: [
      "next release",
      "+3 months",
      "+12 months",
      "threshold",
    ],
    whyItMatters:
      "SNAP participation is a Thesis niche in the working doc: monthly, public, objective, decision-relevant, and under-forecasted compared with macro indicators.",
    drivers: [
      "Unemployment and underemployment",
      "Recertification churn",
      "Benefit adequacy",
      "State administrative processing",
    ],
    history: [
      { label: "Oct", value: 41.2 },
      { label: "Nov", value: 41.1 },
      { label: "Dec", value: 40.9 },
      { label: "Jan", value: 40.7 },
    ],
    historyTool: {
      tool: "usda.fns.lookup",
      call: 'usda.fns.lookup({ program: "snap", series: "persons", months: ["2025-10", "2026-01"] })',
      result: "{ oct: 41.2, nov: 41.1, dec: 40.9, jan: 40.7 }",
    },
    targets: [
      {
        slug: "snap-participation-april-2026",
        title: "SNAP participation, Apr 2026",
        question:
          "How many people will participate in SNAP on average in April 2026 according to USDA Food and Nutrition Service monthly data?",
        dataPointId: "usda.fns.snap.persons.april_2026",
        horizon: "plus_3m",
        horizonLabel: "+3 months",
        periodLabel: "April 2026",
        resolutionDate: "2026-08-31",
        resolutionRule:
          "Resolves to the April 2026 average monthly SNAP persons count in USDA FNS national program data. If USDA updates the monthly table, the first version available by August 31, 2026 governs.",
        pointEstimate: 40.8,
        ciLow: 39.5,
        ciHigh: 42.2,
        tools: [
          {
            tool: "policyengine.simulate",
            call: 'policyengine.simulate({ program: "snap", month: "2026-04", output: "participating_persons", map_to: "person", takeup: "observed_churn" })',
            result:
              '{ point: 40.9, ci80: [39.6, 42.1], drivers: ["eligible_population", "recertification", "earnings"] }',
          },
        ],
        rationale:
          "The forecast expects participation to flatten near 41 million. The value comes from combining administrative trend with a bottom-up eligibility/take-up prior.",
      },
    ],
  },
  {
    seriesId: "cms.medicaid_chip.enrollment",
    title: "Medicaid and CHIP enrollment",
    measure: "Total Medicaid and CHIP enrollment",
    unit: "millions",
    source: "CMS Medicaid and CHIP monthly enrollment data",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2-3 months",
    resolutionPolicy: "fixed_vintage",
    benchmark: "PolicyEngine eligibility/take-up prior",
    chainableQuestions: [
      "next release",
      "+3 months",
      "+12 months",
      "threshold",
    ],
    whyItMatters:
      "Medicaid enrollment is a high-value monthly program series: it resolves from administrative data, affects coverage and poverty forecasts, and gives repeated feedback on eligibility/take-up modeling.",
    drivers: [
      "Post-unwinding renewal policy",
      "Income eligibility",
      "Ex parte renewal success",
      "Marketplace transition flow",
    ],
    history: [
      { label: "Oct", value: 79.6 },
      { label: "Nov", value: 79.4 },
      { label: "Dec", value: 79.2 },
      { label: "Jan", value: 79.0 },
    ],
    historyTool: {
      tool: "cms.lookup",
      call: 'cms.lookup({ dataset: "medicaid_chip_monthly_enrollment", measure: "total_enrollment", months: ["2025-10", "2026-01"] })',
      result: "{ oct: 79.6, nov: 79.4, dec: 79.2, jan: 79.0 }",
    },
    targets: [
      {
        slug: "medicaid-chip-enrollment-april-2026",
        title: "Medicaid and CHIP enrollment, Apr 2026",
        question:
          "How many people will be enrolled in Medicaid and CHIP in April 2026 according to CMS monthly enrollment data?",
        dataPointId: "cms.medicaid_chip.enrollment.april_2026",
        horizon: "plus_3m",
        horizonLabel: "+3 months",
        periodLabel: "April 2026",
        resolutionDate: "2026-09-30",
        resolutionRule:
          "Resolves to the national Medicaid and CHIP enrollment total for April 2026 in CMS monthly enrollment data. If CMS posts preliminary and updated versions, the first updated national file available by September 30, 2026 governs.",
        pointEstimate: 79.1,
        ciLow: 76.2,
        ciHigh: 82.6,
        tools: [
          {
            tool: "policyengine.simulate",
            call: 'policyengine.simulate({ program: "medicaid_chip", month: "2026-04", output: "enrollment", map_to: "person", renewal_policy: "post_unwinding" })',
            result:
              '{ point: 79.2, ci80: [76.3, 82.4], drivers: ["state_renewals", "child_continuity", "income_growth"] }',
          },
        ],
        rationale:
          "The central estimate holds enrollment close to its post-unwinding floor. The interval is wider than SNAP because state reporting and renewal policy create larger cross-state movement.",
      },
    ],
  },
] satisfies PredictionSeries[];

export const LAUNCH_CADENCE_EXAMPLES = buildForecastCellsFromSeries(
  LAUNCH_PREDICTION_SERIES,
);
