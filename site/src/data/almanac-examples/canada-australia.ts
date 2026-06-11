import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";

const RECORDED_CA_AU_AGENT_RUN: NonNullable<
  PredictionSeries["predictionRun"]
> = {
  kind: "recorded-agent-run",
  runAt: "2026-06-04T11:36:25+01:00",
  agent: "Canada/Australia indicator agent ensemble",
  model: "Codex recorded agent runs",
  sourceContext: [
    "Statistics Canada Labour Force Survey",
    "Statistics Canada Consumer Price Index",
    "Statistics Canada GDP by industry",
    "Bank of Canada policy interest rate schedule",
    "Australian Bureau of Statistics Labour Force",
    "Australian Bureau of Statistics monthly CPI",
    "Reserve Bank of Australia cash rate target",
  ],
};

const CANADA_AUSTRALIA_PREDICTION_SERIES_BASE = [
  {
    seriesId: "statcan.lfs.unemployment_rate",
    country: "CA",
    title: "Canada unemployment rate",
    measure: "Labour Force Survey unemployment rate, seasonally adjusted",
    unit: "percent",
    source: "Statistics Canada Labour Force Survey",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 day",
    resolutionPolicy: "first_print",
    benchmark: "Canadian economist consensus and recent LFS trend",
    chainableQuestions: ["next release", "+3 months", "rate-decision reaction"],
    whyItMatters:
      "The unemployment rate is the fastest official read on Canadian labour-market slack and feeds directly into household-income, poverty, and Bank of Canada predictions.",
    drivers: [
      "Recent unemployment-rate drift",
      "Labour-force participation",
      "Full-time employment changes",
      "Job-vacancy and wage-growth context",
    ],
    history: [
      { label: "Jan", value: 6.5 },
      { label: "Feb", value: 6.7 },
      { label: "Mar", value: 6.7 },
      { label: "Apr", value: 6.9 },
    ],
    historyTool: {
      tool: "statcan.lookup",
      call: 'statcan.lookup({ release: "Labour Force Survey", series: "unemployment_rate", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 6.5, feb: 6.7, mar: 6.7, apr: 6.9, next_release: '2026-06-05 08:30 ET' }",
    },
    targets: [
      {
        slug: "canada-unemployment-rate-may-2026",
        title: "Canada unemployment rate, May 2026",
        question:
          "What will Statistics Canada first report as Canada's seasonally adjusted unemployment rate for May 2026?",
        dataPointId:
          "statcan.lfs.unemployment_rate.canada.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-05",
        resolutionRule:
          "Resolves to the first published seasonally adjusted Canada unemployment rate in the Statistics Canada Labour Force Survey for May 2026. Later revisions do not change the resolved value.",
        pointEstimate: 7.0,
        ciLow: 6.7,
        ciHigh: 7.3,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["canada-unemployment-rate-may-2026"], sources: ["Statistics Canada LFS January-April 2026", "Statistics Canada SEPH and job vacancies"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: 7.0, ci80: [6.7, 7.3], context: ['April unemployment 6.9%', 'April employment -18k', 'first four months of 2026 net employment -112k', 'March job vacancies held at 503k'] }",
          },
        ],
        rationale:
          "The April rate rose to 6.9% while employment was little changed for a second month after a weak February. The agent centers May at 7.0% because participation and job-search behavior can keep unemployment elevated even if employment does not fall sharply.",
      },
    ],
  },
  {
    seriesId: "statcan.lfs.employment_change",
    country: "CA",
    title: "Canada employment change",
    measure: "Monthly change in total employment, seasonally adjusted",
    unit: "thousands",
    source: "Statistics Canada Labour Force Survey",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 day",
    resolutionPolicy: "first_print",
    benchmark: "Canadian labour-market consensus and LFS sampling error",
    chainableQuestions: ["next release", "+3 months", "unemployment threshold"],
    whyItMatters:
      "Employment change is a high-cadence calibration target for labour income, payroll tax bases, and poverty forecasts.",
    drivers: [
      "Full-time versus part-time mix",
      "Ontario and Quebec employment swings",
      "Manufacturing and construction softness",
      "LFS monthly sampling variability",
    ],
    history: [
      { label: "Jan", value: -25 },
      { label: "Feb", value: -84 },
      { label: "Mar", value: 14 },
      { label: "Apr", value: -18 },
    ],
    historyTool: {
      tool: "statcan.lookup",
      call: 'statcan.lookup({ release: "Labour Force Survey", series: "employment_change_thousands", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: -25, feb: -84, mar: 14, apr: -18, apr_level_thousands: 21034, next_release: '2026-06-05 08:30 ET' }",
    },
    targets: [
      {
        slug: "canada-employment-change-may-2026",
        title: "Canada employment change, May 2026",
        question:
          "What will Statistics Canada first report as the May 2026 monthly change in seasonally adjusted employment for Canada?",
        dataPointId:
          "statcan.lfs.employment_change.canada.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-05",
        resolutionRule:
          "Resolves to the first published monthly change in seasonally adjusted total employment for Canada in the May 2026 Labour Force Survey. Later revisions do not change the resolved value.",
        pointEstimate: -10,
        ciLow: -60,
        ciHigh: 50,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["canada-employment-change-may-2026"], sources: ["Statistics Canada LFS April 2026", "Statistics Canada payroll employment and job vacancies"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: -10, ci80: [-60, 50], context: ['January-April net employment -112k', 'March +14k after February -84k', 'April -18k and full-time -47k', 'monthly LFS first prints are noisy'] }",
          },
        ],
        rationale:
          "The first four months of 2026 show soft but noisy employment, with two small prints around one large February decline. The agent expects another slightly negative May first print while keeping a wide interval around zero.",
      },
    ],
  },
  {
    seriesId: "statcan.cpi.annual_rate",
    country: "CA",
    title: "Canada CPI annual inflation",
    measure: "All-items Consumer Price Index 12-month change",
    unit: "percent",
    source: "Statistics Canada Consumer Price Index",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~3 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Canadian CPI consensus and Bank of Canada monitoring",
    chainableQuestions: ["next release", "+3 months", "BoC reaction"],
    whyItMatters:
      "Canadian CPI is the key official inflation target for rate decisions, real-income forecasts, and benefit indexation checks.",
    drivers: [
      "Gasoline and energy base effects",
      "Food and shelter inflation",
      "2026 basket-weight update",
      "Core inflation measures",
    ],
    history: [
      { label: "Jan", value: 2.3 },
      { label: "Feb", value: 1.8 },
      { label: "Mar", value: 2.4 },
      { label: "Apr", value: 2.8 },
    ],
    historyTool: {
      tool: "statcan.lookup",
      call: 'statcan.lookup({ release: "Consumer Price Index", series: "all_items_12_month_change", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 2.3, feb: 1.8, mar: 2.4, apr: 2.8, basket_weights_update: '2026-06-15', next_release: '2026-06-22' }",
    },
    targets: [
      {
        slug: "canada-cpi-annual-rate-may-2026",
        title: "Canada CPI annual inflation, May 2026",
        question:
          "What will Statistics Canada first report as Canada's all-items CPI 12-month inflation rate for May 2026?",
        dataPointId:
          "statcan.cpi.all_items_annual_rate.canada.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-22",
        resolutionRule:
          "Resolves to the first published all-items CPI 12-month change for Canada in the May 2026 Consumer Price Index release. Later revisions or table updates do not change the resolved value.",
        pointEstimate: 2.7,
        ciLow: 2.3,
        ciHigh: 3.1,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["canada-cpi-annual-rate-may-2026"], sources: ["Statistics Canada CPI January-April 2026", "Statistics Canada CPI basket update note"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: 2.7, ci80: [2.3, 3.1], context: ['April CPI 2.8% y/y', 'March 2.4%; February 1.8%', 'May CPI uses updated 2025 basket weights', 'gasoline base effects remain important'] }",
          },
        ],
        rationale:
          "April's acceleration to 2.8% was driven by energy and carbon-levy base effects. The agent expects those pressures to remain visible but not intensify materially in May, centering slightly below April with basket-update uncertainty in the interval.",
      },
    ],
  },
  {
    seriesId: "statcan.gdp_by_industry.monthly_growth",
    country: "CA",
    title: "Canada monthly GDP growth",
    measure: "Real GDP by industry monthly percent change",
    unit: "percent_growth",
    source: "Statistics Canada GDP by industry",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~4 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Statistics Canada advance estimate and nowcast consensus",
    chainableQuestions: ["next release", "+3 months", "recession threshold"],
    whyItMatters:
      "Monthly GDP is the quickest official output measure for Canada and helps anchor fiscal revenue, labour demand, and central-bank predictions.",
    drivers: [
      "Manufacturing and transportation rebound",
      "Oil and gas extraction",
      "Retail and construction softness",
      "Advance-estimate revision risk",
    ],
    history: [
      { label: "Jan", value: 0.1 },
      { label: "Feb", value: 0.2 },
      { label: "Mar", value: -0.1 },
      { label: "Apr adv", value: 0.4 },
    ],
    historyTool: {
      tool: "statcan.lookup",
      call: 'statcan.lookup({ release: "GDP by industry", series: "monthly_real_gdp_growth", months: ["2026-01", "2026-03"], advance_month: "2026-04" })',
      result:
        "{ jan: 0.1, feb: 0.2, mar: -0.1, apr_advance: 0.4, next_release: '2026-06-30' }",
    },
    targets: [
      {
        slug: "canada-monthly-gdp-growth-april-2026",
        title: "Canada monthly GDP growth, April 2026",
        question:
          "What will Statistics Canada first report as Canada's real GDP by industry monthly growth rate for April 2026?",
        dataPointId:
          "statcan.gdp_by_industry.monthly_growth.april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "April 2026",
        resolutionDate: "2026-06-30",
        resolutionRule:
          "Resolves to the first official Statistics Canada real GDP by industry monthly percent change for April 2026. The May 29 advance estimate is treated as input, not the resolved value.",
        pointEstimate: 0.4,
        ciLow: 0.1,
        ciHigh: 0.7,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["canada-monthly-gdp-growth-april-2026"], sources: ["Statistics Canada GDP by industry March 2026", "Statistics Canada April 2026 advance estimate"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: 0.4, ci80: [0.1, 0.7], context: ['March GDP -0.1%', 'April advance estimate +0.4%', 'growth indicated in mining, manufacturing, transportation and warehousing'] }",
          },
        ],
        rationale:
          "Statistics Canada's advance estimate points to 0.4% April growth. The agent uses that as the modal first official print but keeps room for revision because March's goods-sector contraction and agriculture weakness could shift the final industry mix.",
      },
    ],
  },
  {
    seriesId: "bank_of_canada.overnight_rate_target",
    country: "CA",
    type: "policy",
    title: "Bank of Canada overnight rate target",
    measure: "Target for the overnight rate after the fixed announcement date",
    unit: "percent",
    source: "Bank of Canada interest rate announcement",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 week",
    resolutionPolicy: "first_print",
    benchmark: "Overnight-index-swap pricing and economist calls",
    chainableQuestions: ["next decision", "+3 months", "inflation reaction"],
    whyItMatters:
      "The overnight-rate target is Canada's central monetary-policy setting and connects inflation, labour slack, debt-service costs, and exchange-rate forecasts.",
    drivers: [
      "April CPI acceleration",
      "Rising unemployment rate",
      "GDP advance estimate",
      "Bank of Canada fixed announcement cadence",
    ],
    history: [
      { label: "Jan", value: 2.25 },
      { label: "Mar", value: 2.25 },
      { label: "Apr", value: 2.25 },
    ],
    historyTool: {
      tool: "bank_of_canada.lookup",
      call: 'bank_of_canada.lookup({ series: "target_overnight_rate", decisions: ["2026-01-28", "2026-03-18", "2026-04-29"], next_decision: "2026-06-10" })',
      result:
        "{ jan_28: 2.25, mar_18: 2.25, apr_29: 2.25, next_decision: '2026-06-10 09:45 ET' }",
    },
    policyParameter: "bank_of_canada.overnight_rate_target.after_june_2026",
    targets: [
      {
        slug: "canada-overnight-rate-june-2026-boc",
        title: "Bank of Canada overnight rate, June 2026",
        question:
          "What will the Bank of Canada target for the overnight rate be immediately after its June 10, 2026 interest rate announcement?",
        dataPointId: "bank_of_canada.overnight_rate.after_june_2026",
        horizon: "next_release",
        horizonLabel: "next decision",
        periodLabel: "June 2026 decision",
        resolutionDate: "2026-06-10",
        resolutionRule:
          "Resolves to the target for the overnight rate stated in the Bank of Canada interest rate announcement on June 10, 2026. If the Bank posts a same-day correction before market close, the corrected value governs.",
        pointEstimate: 2.25,
        ciLow: 2.0,
        ciHigh: 2.25,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["canada-overnight-rate-june-2026-boc"], sources: ["Bank of Canada policy interest rate schedule", "Statistics Canada CPI and LFS"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: 2.25, ci80: [2.00, 2.25], context: ['overnight target held at 2.25% on Jan 28, Mar 18, and Apr 29', 'April CPI 2.8%', 'April unemployment 6.9%', 'June 10 fixed announcement date'] }",
          },
        ],
        rationale:
          "The Bank has held at 2.25% for three decisions. Inflation has moved back above 2% while labour slack has risen, so the agent puts most mass on another hold with a smaller cut tail rather than a hike.",
      },
    ],
  },
  {
    seriesId: "abs.labour.unemployment_rate",
    country: "AU",
    title: "Australia unemployment rate",
    measure: "Seasonally adjusted unemployment rate",
    unit: "percent",
    source: "Australian Bureau of Statistics Labour Force",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~3 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Australian economist consensus and ABS trend estimates",
    chainableQuestions: ["next release", "+3 months", "RBA reaction"],
    whyItMatters:
      "The unemployment rate is a central near-term input for Australian monetary policy, household-income forecasts, and benefit-pressure predictions.",
    drivers: [
      "April unemployment jump",
      "Participation rate movement",
      "Labour Force Survey modernisation",
      "Hours-worked and underemployment signals",
    ],
    history: [
      { label: "Mar", value: 4.3 },
      { label: "Apr", value: 4.5 },
      { label: "Trend Apr", value: 4.3 },
    ],
    historyTool: {
      tool: "abs.lookup",
      call: 'abs.lookup({ release: "Labour Force, Australia", series: "seasonally_adjusted_unemployment_rate", months: ["2026-03", "2026-04"], next_release: "2026-06-25" })',
      result:
        "{ mar: 4.3, apr: 4.5, apr_trend: 4.3, next_release: '2026-06-25 11:30 AEST', transition_delay: true }",
    },
    targets: [
      {
        slug: "australia-unemployment-rate-may-2026",
        title: "Australia unemployment rate, May 2026",
        question:
          "What will the Australian Bureau of Statistics first report as Australia's seasonally adjusted unemployment rate for May 2026?",
        dataPointId:
          "abs.labour.unemployment_rate.australia.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published seasonally adjusted unemployment rate in Labour Force, Australia for May 2026. Later revisions do not change the resolved value.",
        pointEstimate: 4.5,
        ciLow: 4.2,
        ciHigh: 4.8,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["australia-unemployment-rate-may-2026"], sources: ["ABS Labour Force April 2026", "ABS Labour Force modernisation note"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: 4.5, ci80: [4.2, 4.8], context: ['April unemployment 4.5%; trend 4.3%', 'April employment -18.6k', 'May release delayed to June 25 for quality assurance during survey modernisation'] }",
          },
        ],
        rationale:
          "April's seasonally adjusted rate rose to 4.5% while the trend rate remained 4.3%. The agent centers on 4.5% because a reversal is possible, but survey transition risk and the April rise argue against aggressively fading it.",
      },
    ],
  },
  {
    seriesId: "abs.labour.employment_change",
    country: "AU",
    title: "Australia employment change",
    measure: "Monthly change in seasonally adjusted employment",
    unit: "thousands",
    source: "Australian Bureau of Statistics Labour Force",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~3 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Australian economist consensus and ABS trend estimates",
    chainableQuestions: ["next release", "+3 months", "unemployment threshold"],
    whyItMatters:
      "Employment change is a fast, noisy target that helps calibrate household income, tax receipts, and welfare-demand predictions.",
    drivers: [
      "April employment decline",
      "Trend employment growth",
      "Hours worked",
      "Survey transition quality checks",
    ],
    history: [
      { label: "Apr SA", value: -18.6 },
      { label: "Apr trend", value: 22.1 },
    ],
    historyTool: {
      tool: "abs.lookup",
      call: 'abs.lookup({ release: "Labour Force, Australia", series: "employment_change_thousands", months: ["2026-04"], next_release: "2026-06-25" })',
      result:
        "{ apr_seasonally_adjusted: -18.6, apr_trend: 22.1, apr_level_thousands: 14737.4, next_release: '2026-06-25 11:30 AEST' }",
    },
    targets: [
      {
        slug: "australia-employment-change-may-2026",
        title: "Australia employment change, May 2026",
        question:
          "What will the Australian Bureau of Statistics first report as Australia's May 2026 monthly change in seasonally adjusted employment?",
        dataPointId:
          "abs.labour.employment_change.australia.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published monthly change in seasonally adjusted employment in Labour Force, Australia for May 2026. Later revisions do not change the resolved value.",
        pointEstimate: 15,
        ciLow: -45,
        ciHigh: 75,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["australia-employment-change-may-2026"], sources: ["ABS Labour Force April 2026", "ABS survey modernisation note"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: 15, ci80: [-45, 75], context: ['April seasonally adjusted employment -18.6k', 'April trend employment +22.1k', 'hours worked +16m', 'May collection has two incoming rotation groups'] }",
          },
        ],
        rationale:
          "The April seasonally adjusted drop contrasts with a positive trend estimate and higher hours worked. The agent expects partial reversion in May but keeps a wide interval because rotation-group and modernisation effects raise first-print uncertainty.",
      },
    ],
  },
  {
    seriesId: "abs.cpi.annual_rate",
    country: "AU",
    title: "Australia CPI annual inflation",
    measure: "Monthly CPI all-groups annual movement",
    unit: "percent",
    source: "Australian Bureau of Statistics Consumer Price Index",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~3 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Australian CPI consensus and RBA inflation outlook",
    chainableQuestions: ["next release", "+3 months", "RBA reaction"],
    whyItMatters:
      "Monthly CPI is the fastest official Australian inflation read and directly informs cash-rate, real-income, and indexation forecasts.",
    drivers: [
      "Housing and transport inflation",
      "Monthly fuel-price volatility",
      "Trimmed mean inflation",
      "Monthly CPI transition history",
    ],
    history: [
      { label: "Jan", value: 3.8 },
      { label: "Feb", value: 3.7 },
      { label: "Mar", value: 4.6 },
      { label: "Apr", value: 4.2 },
    ],
    historyTool: {
      tool: "abs.lookup",
      call: 'abs.lookup({ release: "Consumer Price Index, Australia", series: "all_groups_annual_movement", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 3.8, feb: 3.7, mar: 4.6, apr: 4.2, trimmed_mean_apr: 3.4, next_release: '2026-06-24 11:30 AEST' }",
    },
    targets: [
      {
        slug: "australia-cpi-annual-rate-may-2026",
        title: "Australia CPI annual inflation, May 2026",
        question:
          "What will the Australian Bureau of Statistics first report as Australia's all-groups CPI annual inflation rate for May 2026?",
        dataPointId:
          "abs.cpi.all_groups_annual_rate.australia.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-24",
        resolutionRule:
          "Resolves to the first published all-groups annual CPI movement in Consumer Price Index, Australia for May 2026. Later revisions do not change the resolved value.",
        pointEstimate: 4.1,
        ciLow: 3.7,
        ciHigh: 4.5,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["australia-cpi-annual-rate-may-2026"], sources: ["ABS CPI April 2026", "ABS CPI March 2026"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: 4.1, ci80: [3.7, 4.5], context: ['April CPI 4.2% y/y; March 4.6%', 'April monthly CPI +0.4% original, -0.1% seasonally adjusted', 'trimmed mean 3.4%'] }",
          },
        ],
        rationale:
          "April CPI cooled from March but remained well above the RBA target band, with housing and transport still elevated. The agent expects a small further easing in May while keeping upside risk from fuel and administered-price categories.",
      },
    ],
  },
  {
    seriesId: "rba.cash_rate_target",
    country: "AU",
    type: "policy",
    title: "Reserve Bank of Australia cash rate target",
    measure: "Cash rate target after the monetary policy decision",
    unit: "percent",
    source: "Reserve Bank of Australia cash rate target",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Market-implied cash-rate path and economist calls",
    chainableQuestions: ["next decision", "+3 months", "inflation reaction"],
    whyItMatters:
      "The RBA cash rate target is Australia's main monetary-policy setting and links inflation, mortgage costs, labour-market slack, and government fiscal forecasts.",
    drivers: [
      "April CPI at 4.2%",
      "Trimmed mean above target",
      "April unemployment at 4.5%",
      "June Board communication",
    ],
    history: [
      { label: "May", value: 4.35 },
    ],
    historyTool: {
      tool: "rba.lookup",
      call: 'rba.lookup({ series: "cash_rate_target", current_effective_date: "2026-05-06", next_update: "2026-06-16 14:30" })',
      result:
        "{ current_target: 4.35, effective_date: '2026-05-06', next_update: '2026-06-16 14:30 AEST' }",
    },
    policyParameter: "rba.cash_rate_target.after_june_2026",
    targets: [
      {
        slug: "australia-cash-rate-june-2026-rba",
        title: "RBA cash rate target, June 2026",
        question:
          "What will the Reserve Bank of Australia cash rate target be immediately after the monetary policy decision updated on June 16, 2026?",
        dataPointId: "rba.cash_rate_target.after_june_2026",
        horizon: "next_release",
        horizonLabel: "next decision",
        periodLabel: "June 2026 decision",
        resolutionDate: "2026-06-16",
        resolutionRule:
          "Resolves to the RBA cash rate target shown in the Reserve Bank of Australia cash rate target update on June 16, 2026. If the RBA posts a same-day correction before market close, the corrected value governs.",
        pointEstimate: 4.35,
        ciLow: 4.35,
        ciHigh: 4.6,
        tools: [
          {
            tool: "agent.run",
            call: 'canadaAustraliaIndicatorAgent.predict({ slugs: ["australia-cash-rate-june-2026-rba"], sources: ["RBA cash rate target overview", "ABS CPI April 2026", "ABS Labour Force April 2026"], runAt: "2026-06-04T11:36:25+01:00" })',
            result:
              "{ point: 4.35, ci80: [4.35, 4.60], context: ['cash rate target 4.35% effective 2026-05-06', 'next update 2026-06-16 14:30', 'April CPI 4.2%', 'April unemployment 4.5%'] }",
          },
        ],
        rationale:
          "Inflation is still above target and trimmed mean remains elevated, while the unemployment rise argues against over-tightening. The agent centers on a hold, with the main tail being a 25 basis point increase rather than a cut.",
      },
    ],
  },
] satisfies Omit<PredictionSeries, "predictionRun">[];

export const CANADA_AUSTRALIA_PREDICTION_SERIES =
  CANADA_AUSTRALIA_PREDICTION_SERIES_BASE.map((series) => ({
    ...series,
    predictionRun: RECORDED_CA_AU_AGENT_RUN,
  })) satisfies PredictionSeries[];

export const CANADA_AUSTRALIA_EXAMPLES = buildForecastCellsFromSeries(
  CANADA_AUSTRALIA_PREDICTION_SERIES,
);
