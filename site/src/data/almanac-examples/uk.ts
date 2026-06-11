import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";

const RECORDED_UK_AGENT_RUN: NonNullable<PredictionSeries["predictionRun"]> = {
  kind: "recorded-agent-run",
  runAt: "2026-06-04T10:32:04+01:00",
  agent: "UK indicator agent ensemble",
  model: "Codex recorded agent runs",
  sourceContext: [
    "ONS GDP monthly estimate",
    "ONS consumer price inflation",
    "ONS/HMRC labour market and PAYE RTI",
    "ONS retail sales",
    "ONS public sector finances",
    "Bank of England MPC minutes",
  ],
};

const UK_PREDICTION_SERIES_BASE = [
  {
    seriesId: "ons.gdp.monthly_growth",
    country: "UK",
    title: "UK monthly GDP growth",
    measure: "Monthly real GDP growth, seasonally adjusted",
    unit: "percent_growth",
    source: "Office for National Statistics, GDP monthly estimate",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 week",
    resolutionPolicy: "first_print",
    benchmark: "City economist nowcasts and ONS real-time indicators",
    chainableQuestions: ["next release", "+3 months", "threshold"],
    whyItMatters:
      "Monthly GDP is the fastest official read on UK growth and feeds directly into fiscal, labour-market, and monetary-policy predictions.",
    drivers: [
      "Services output",
      "Retail and consumer demand",
      "Construction output",
      "Production volatility",
    ],
    history: [
      { label: "Jan", value: 0.0 },
      { label: "Feb", value: 0.4 },
      { label: "Mar", value: 0.3 },
    ],
    historyTool: {
      tool: "ons.lookup",
      call: 'ons.lookup({ release: "GDP monthly estimate", series: "monthly_real_gdp_growth", months: ["2026-01", "2026-03"] })',
      result:
        "{ jan: 0.0, feb: 0.4, mar: 0.3, next_release: '2026-06-12 07:00' }",
    },
    targets: [
      {
        slug: "uk-monthly-gdp-growth-april-2026",
        title: "UK monthly GDP growth, April 2026",
        question:
          "What will ONS first report as UK real GDP growth in April 2026, measured as the seasonally adjusted month-over-month change?",
        dataPointId: "ons.gdp.monthly_growth.april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "April 2026",
        resolutionDate: "2026-06-12",
        resolutionRule:
          "Resolves to the first published ONS monthly real GDP growth estimate for April 2026 in the GDP monthly estimate release. Later revisions do not change the resolved value.",
        pointEstimate: -0.1,
        ciLow: -0.5,
        ciHigh: 0.3,
        tools: [
          {
            tool: "agent.run",
            call: 'ukIndicatorAgent.predict({ slugs: ["uk-monthly-gdp-growth-april-2026"], sources: ["ONS GDP monthly estimate", "ONS retail sales", "ONS real-time indicators"], runAt: "2026-06-04T10:32:04+01:00" })',
            result:
              "{ point: -0.1, ci80: [-0.5, 0.3], context: ['March GDP +0.3%; February +0.4%; January 0.0%', 'April retail sales volumes -1.3%', '27% of trading businesses reported lower turnover'] }",
          },
        ],
        rationale:
          "March grew 0.3% after 0.4% in February, but the April look-ahead points to softer consumer demand: retail footfall was broadly unchanged, fuel prices jumped, and retail sales volumes later fell sharply in April. The agent therefore fades the Q1 strength.",
      },
    ],
  },
  {
    seriesId: "ons.cpi.annual_rate",
    country: "UK",
    title: "UK CPI annual inflation",
    measure: "Consumer Prices Index 12-month rate",
    unit: "percent",
    source: "Office for National Statistics, consumer price inflation",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Economist consensus and Bank of England monitoring",
    chainableQuestions: ["next release", "+3 months", "Bank Rate reaction"],
    whyItMatters:
      "CPI is the key UK monetary-policy and cost-of-living indicator, especially while energy-price shocks and services inflation are in the news.",
    drivers: [
      "Energy and motor fuel prices",
      "Services inflation",
      "Food prices",
      "Base effects from 2025 bill changes",
    ],
    history: [
      { label: "Jan", value: 3.0 },
      { label: "Feb", value: 3.0 },
      { label: "Mar", value: 3.3 },
      { label: "Apr", value: 2.8 },
    ],
    historyTool: {
      tool: "ons.lookup",
      call: 'ons.lookup({ release: "Consumer price inflation", series: "CPI 12-month rate", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 3.0, feb: 3.0, mar: 3.3, apr: 2.8, next_release: '2026-06-17 07:00' }",
    },
    targets: [
      {
        slug: "uk-cpi-annual-rate-may-2026",
        title: "UK CPI annual inflation, May 2026",
        question:
          "What will ONS first report as the UK Consumer Prices Index 12-month inflation rate for May 2026?",
        dataPointId: "ons.cpi.annual_rate.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-17",
        resolutionRule:
          "Resolves to the first published ONS CPI 12-month rate for May 2026 in the consumer price inflation release. Later revisions do not change the resolved value.",
        pointEstimate: 2.9,
        ciLow: 2.6,
        ciHigh: 3.2,
        tools: [
          {
            tool: "agent.run",
            call: 'ukIndicatorAgent.predict({ slugs: ["uk-cpi-annual-rate-may-2026"], sources: ["ONS consumer price inflation April 2026", "ONS CPI May 2025"], runAt: "2026-06-04T10:32:04+01:00" })',
            result:
              "{ point: 2.9, ci80: [2.6, 3.2], context: ['April CPI 2.8% y/y; monthly CPI +0.7%', 'May 2025 monthly CPI +0.2%', 'motor fuels up; electricity and gas down in April'] }",
          },
        ],
        rationale:
          "April CPI fell to 2.8% from 3.3%, largely because electricity, gas, food, recreation, and air fares eased. The agent expects a modest May rebound because the May 2025 base month was only +0.2%, while fuel and vehicle-tax base effects lean upward.",
      },
    ],
  },
  {
    seriesId: "ons.labour.unemployment_rate",
    country: "UK",
    title: "UK unemployment rate",
    measure: "LFS unemployment rate for people aged 16 and over",
    unit: "percent",
    source: "Office for National Statistics, UK labour market overview",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Economist consensus and HMRC PAYE nowcasts",
    chainableQuestions: ["next release", "+3 months", "claimant threshold"],
    whyItMatters:
      "The UK labour market is currently one of the clearest stress points: unemployment is up, payroll employment is falling, and wage growth remains central to Bank of England decisions.",
    drivers: [
      "PAYE payroll employee changes",
      "Claimant Count",
      "Vacancy decline",
      "LFS survey uncertainty",
    ],
    history: [
      { label: "Oct-Dec", value: 5.2 },
      { label: "Nov-Jan", value: 5.2 },
      { label: "Dec-Feb", value: 5.2 },
      { label: "Jan-Mar", value: 5.0 },
    ],
    historyTool: {
      tool: "ons.lookup",
      call: 'ons.lookup({ release: "UK labour market", series: "LFS unemployment rate 16+", periods: ["2025-10:2025-12", "2026-01:2026-03"] })',
      result:
        "{ jan_to_mar_2026: 5.0, april_claimant_count_millions: 1.699, april_paye_early_employees_millions: 30.2, next_release: '2026-06-18 07:00' }",
    },
    targets: [
      {
        slug: "uk-unemployment-rate-feb-apr-2026",
        title: "UK unemployment rate, Feb-Apr 2026",
        question:
          "What will ONS first report as the UK unemployment rate for people aged 16 and over in February to April 2026?",
        dataPointId:
          "ons.labour.unemployment_rate.february_to_april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "February to April 2026",
        resolutionDate: "2026-06-18",
        resolutionRule:
          "Resolves to the first published ONS LFS unemployment rate for people aged 16 and over for February to April 2026 in the UK Labour Market June 2026 release. Later revisions do not change the resolved value.",
        pointEstimate: 5.1,
        ciLow: 4.8,
        ciHigh: 5.4,
        tools: [
          {
            tool: "agent.run",
            call: 'codexAgent.predict({ slugs: ["uk-unemployment-rate-feb-apr-2026"], sources: ["ONS UK labour market: May 2026", "ONS/HMRC PAYE RTI", "ONS vacancies"], runAt: "2026-06-04T10:32:04+01:00" })',
            result:
              "{ point: 5.1, ci80: [4.8, 5.4], context: ['Jan-Mar unemployment rate 5.0%', 'April claimant count 1.699m', 'vacancies fell to 705k, lowest since Feb-Apr 2021', 'LFS estimates remain volatile'] }",
          },
        ],
        rationale:
          "The January-March unemployment rate was 5.0%, but the provisional April PAYE estimate fell by 100,000 on the month and vacancies reached their lowest level since early 2021. The agent nudges the rate up while respecting LFS sampling volatility.",
      },
    ],
  },
  {
    seriesId: "ons.hmrc.paye_payrolled_employees",
    country: "UK",
    title: "UK PAYE payrolled employees",
    measure: "Early estimate of seasonally adjusted payrolled employees",
    unit: "millions",
    source:
      "HMRC Pay As You Earn Real Time Information via ONS labour market release",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "HMRC RTI administrative trend",
    chainableQuestions: [
      "next release",
      "+3 months",
      "labour-market threshold",
    ],
    whyItMatters:
      "PAYE payrolls are a timely administrative labour-market signal, often cleaner for near-term movement than the survey unemployment rate.",
    drivers: [
      "Employer payroll submissions",
      "April tax-year revision pattern",
      "Sector hiring",
      "Redundancy notices",
    ],
    history: [
      { label: "Jan", value: 30.34 },
      { label: "Feb", value: 30.33 },
      { label: "Mar", value: 30.3 },
      { label: "Apr", value: 30.2 },
    ],
    historyTool: {
      tool: "ons.hmrc.lookup",
      call: 'ons.hmrc.lookup({ dataset: "PAYE RTI", measure: "payrolled_employees_early_estimate", months: ["2026-01", "2026-04"] })',
      result:
        "{ apr2026_early_millions: 30.2, apr_month_change_thousands: -100, early_tax_year_estimate: true }",
    },
    targets: [
      {
        slug: "uk-paye-payrolled-employees-may-2026",
        title: "UK PAYE payrolled employees, May 2026",
        question:
          "What will ONS and HMRC first report as the early estimate of seasonally adjusted UK payrolled employees for May 2026?",
        dataPointId: "ons.hmrc.paye_payrolled_employees.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-18",
        resolutionRule:
          "Resolves to the first published early estimate of seasonally adjusted UK payrolled employees for May 2026 in the ONS/HMRC PAYE RTI release. Later revisions do not change the resolved value.",
        pointEstimate: 30.15,
        ciLow: 29.98,
        ciHigh: 30.3,
        tools: [
          {
            tool: "agent.run",
            call: 'codexAgent.predict({ slugs: ["uk-paye-payrolled-employees-may-2026"], sources: ["ONS/HMRC PAYE RTI: May 2026 labour market release"], runAt: "2026-06-04T10:32:04+01:00" })',
            result:
              "{ point: 30.15, ci80: [29.98, 30.30], context: ['April early estimate 30.2m', 'April down 100k on month', 'early tax-year estimates often revise upward'] }",
          },
        ],
        rationale:
          "April's early estimate dropped to 30.2 million, down 100,000 on the month. Early tax-year estimates often revise upward, but the agent still expects a lower May first print given weakening labour-demand indicators.",
      },
    ],
  },
  {
    seriesId: "ons.retail_sales.volume_mom",
    country: "UK",
    title: "Great Britain retail sales volume growth",
    measure: "Retail sales quantity bought, monthly percent change",
    unit: "percent_growth",
    source: "Office for National Statistics, Retail sales Great Britain",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Retail footfall and card-spending indicators",
    chainableQuestions: ["next release", "+3 months", "GDP contribution"],
    whyItMatters:
      "Retail sales are a fast consumer-demand read and one of the most visible components behind short-run GDP surprises.",
    drivers: [
      "Weather-sensitive store spending",
      "Fuel prices and volumes",
      "Non-food store demand",
      "Online retail share",
    ],
    history: [
      { label: "Feb", value: -0.8 },
      { label: "Mar", value: 0.6 },
      { label: "Apr", value: -1.3 },
    ],
    historyTool: {
      tool: "ons.lookup",
      call: 'ons.lookup({ release: "Retail sales, Great Britain", series: "volume_mom", months: ["2026-02", "2026-04"] })',
      result:
        "{ feb: -0.8, mar: 0.6, apr: -1.3, next_release: '2026-06-19 07:00' }",
    },
    targets: [
      {
        slug: "uk-retail-sales-volume-mom-may-2026",
        title: "Great Britain retail sales, May 2026 month-over-month",
        question:
          "What will ONS first report as the monthly percent change in Great Britain retail sales volumes for May 2026?",
        dataPointId: "ons.retail_sales.volume_mom.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-19",
        resolutionRule:
          "Resolves to the first published ONS monthly percent change in the quantity bought in all retailing for May 2026. Later revisions do not change the resolved value.",
        pointEstimate: 0.5,
        ciLow: -0.6,
        ciHigh: 1.6,
        tools: [
          {
            tool: "agent.run",
            call: 'ukIndicatorAgent.predict({ slugs: ["uk-retail-sales-volume-mom-may-2026"], sources: ["ONS retail sales April 2026", "ONS real-time indicators"], runAt: "2026-06-04T10:32:04+01:00" })',
            result:
              "{ point: 0.5, ci80: [-0.6, 1.6], context: ['April volumes -1.3%', 'automotive fuel volumes -10.2%', 'retail footfall flat month-over-month'] }",
          },
        ],
        rationale:
          "April's 1.3% fall looks partly fuel-driven after March stock-up behaviour, with automotive fuel volumes down 10.2%. The agent expects partial rebound in May as that distortion fades, while weak footfall and non-fuel softness keep the interval wide.",
      },
    ],
  },
  {
    seriesId: "ons.public_sector_net_borrowing_ex_banks",
    country: "UK",
    title: "UK public sector net borrowing",
    measure: "Public sector net borrowing excluding public sector banks",
    unit: "gbp_billions",
    source:
      "Office for National Statistics, Public sector finances time series J5II",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~3 weeks",
    resolutionPolicy: "first_print",
    benchmark: "OBR monthly profiles and gilt-market expectations",
    chainableQuestions: ["next release", "+3 months", "debt-to-GDP impact"],
    whyItMatters:
      "Borrowing is central to the UK's fiscal room, gilt supply, and the credibility of policy-cost forecasts.",
    drivers: [
      "Income tax and VAT receipts",
      "Inflation-linked benefits",
      "Debt interest costs",
      "OBR monthly profile",
    ],
    history: [
      { label: "Jan", value: -14.1 },
      { label: "Feb", value: 10.8 },
      { label: "Mar", value: 16.4 },
      { label: "Apr", value: 24.3 },
    ],
    historyTool: {
      tool: "ons.lookup",
      call: 'ons.lookup({ release: "Public sector finances", series: "J5II", transform: "-value / 1000", months: ["2026-04", "2025-05"], obr_profile: "March 2026 EFO monthly profiles" })',
      result:
        "{ apr2026_gbp_billions: 24.343, may2025_gbp_billions: 18.203, obr_may2026_profile_gbp_billions: 17.665, next_release: '2026-06-19 07:00' }",
    },
    targets: [
      {
        slug: "uk-public-sector-net-borrowing-may-2026",
        title: "UK public sector net borrowing, May 2026",
        question:
          "What will ONS first report as UK public sector net borrowing excluding public sector banks in May 2026?",
        dataPointId:
          "ons.pusf.j5ii.public_sector_net_borrowing_ex_banks.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-19",
        resolutionRule:
          "Resolves to the first official ONS value for May 2026 in Public Sector Finances time series J5II, transformed as -J5II / 1000 so borrowing is positive in GBP billions. Later revisions do not change the resolved value.",
        pointEstimate: 18.5,
        ciLow: 13.0,
        ciHigh: 24.0,
        tools: [
          {
            tool: "agent.run",
            call: 'codexAgent.predict({ slugs: ["uk-public-sector-net-borrowing-may-2026"], sources: ["ONS Public sector finances: April 2026", "OBR monthly profiles"], runAt: "2026-06-04T10:32:04+01:00" })',
            result:
              "{ point: 18.5, ci80: [13.0, 24.0], context: ['April borrowing £24.343bn', 'May 2025 borrowing £18.203bn using -J5II / 1000', 'OBR March 2026 monthly profile for May 2026 £17.665bn', 'May release due 2026-06-19'] }",
          },
        ],
        rationale:
          "The OBR monthly profile gives a strong May baseline near £17.7 billion and May 2025 was £18.2 billion. April 2026 was £3.4 billion above the OBR profile, but early-year spending estimates can unwind, so the agent shades modestly above the baseline rather than carrying the full April overshoot forward.",
      },
    ],
  },
  {
    seriesId: "boe.bank_rate",
    country: "UK",
    type: "policy",
    title: "Bank of England Bank Rate",
    measure: "Bank Rate after the Monetary Policy Committee decision",
    unit: "percent",
    source: "Bank of England Monetary Policy Committee summary and minutes",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "MPC vote split and market-implied policy rate",
    chainableQuestions: ["next decision", "+3 months", "inflation reaction"],
    whyItMatters:
      "Bank Rate is the UK policy setting that ties together inflation, labour-market slack, mortgage costs, and fiscal debt-interest forecasts.",
    drivers: [
      "CPI and services inflation",
      "Energy-price shock risk",
      "Labour-market loosening",
      "MPC vote split",
    ],
    history: [
      { label: "Feb", value: 3.75 },
      { label: "Mar", value: 3.75 },
      { label: "Apr", value: 3.75 },
    ],
    historyTool: {
      tool: "boe.lookup",
      call: 'boe.lookup({ release: "MPC minutes", decisions: ["2026-02", "2026-03", "2026-04"], next_decision: "2026-06-18" })',
      result:
        "{ apr2026_bank_rate: 3.75, apr_vote: '8-1 hold, one vote to raise to 4.00', next_decision: '2026-06-18' }",
    },
    policyParameter: "boe.bank_rate.after_mpc_june_2026",
    targets: [
      {
        slug: "uk-bank-rate-june-2026-mpc",
        title: "Bank of England Bank Rate, June 2026 MPC",
        question:
          "What will Bank Rate be immediately after the Bank of England Monetary Policy Committee decision published on June 18, 2026?",
        dataPointId: "boe.bank_rate.after_mpc_june_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next decision",
        periodLabel: "June 2026 MPC",
        resolutionDate: "2026-06-18",
        resolutionRule:
          "Resolves to the Bank Rate stated in the Bank of England Monetary Policy Summary and minutes published on June 18, 2026. If the Bank publishes a correction the same day before market close, the corrected value governs.",
        pointEstimate: 3.75,
        ciLow: 3.75,
        ciHigh: 4.0,
        tools: [
          {
            tool: "agent.run",
            call: 'codexAgent.predict({ slugs: ["uk-bank-rate-june-2026-mpc"], sources: ["Bank of England April 2026 MPC minutes", "ONS CPI/labour context"], runAt: "2026-06-04T10:32:04+01:00" })',
            result:
              "{ point: 3.75, ci80: [3.75, 4.00], context: ['April MPC voted 8-1 to hold at 3.75%', 'one member voted to raise to 4.00%', 'energy-price uncertainty raises inflation risk', 'labour market continues to loosen'] }",
          },
        ],
        rationale:
          "The April MPC voted 8-1 to hold Bank Rate at 3.75%, with one member voting to raise. Inflation and energy risks argue against cuts, while labour-market loosening argues against a broad hiking majority, so the agent centers on another hold.",
      },
    ],
  },
] satisfies Omit<PredictionSeries, "predictionRun">[];

export const UK_PREDICTION_SERIES = UK_PREDICTION_SERIES_BASE.map((series) => ({
  ...series,
  predictionRun: RECORDED_UK_AGENT_RUN,
})) satisfies PredictionSeries[];

export const UK_EXAMPLES = buildForecastCellsFromSeries(UK_PREDICTION_SERIES);
