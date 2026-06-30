import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";

const RECORDED_EURO_JAPAN_AGENT_RUN: NonNullable<
  PredictionSeries["predictionRun"]
> = {
  kind: "recorded-agent-run",
  runAt: "2026-06-06T05:41:31+01:00",
  agent: "Euro area/Japan indicator agent ensemble",
  model: "Codex recorded agent runs",
  sourceContext: [
    "ECB monetary policy meeting schedule and April 2026 decision",
    "Eurostat flash HICP and unemployment releases",
    "Bank of Japan monetary policy meeting schedule and April 2026 statement",
    "Statistics Bureau of Japan CPI and Labour Force Survey release schedules",
  ],
};

const EURO_JAPAN_PREDICTION_SERIES_BASE = [
  {
    seriesId: "ecb.deposit_facility_rate",
    country: "EA",
    type: "policy",
    title: "ECB deposit facility rate",
    measure: "Deposit facility rate after the Governing Council decision",
    unit: "percent",
    source: "European Central Bank monetary policy decisions",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~1 week",
    resolutionPolicy: "first_print",
    benchmark: "Market-implied euro short-rate path and analyst consensus",
    chainableQuestions: ["next decision", "+3 months", "inflation reaction"],
    whyItMatters:
      "The ECB deposit facility rate is the euro area's main short-rate policy setting and directly shapes borrowing costs, exchange-rate pressure, and fiscal-debt-interest forecasts.",
    drivers: [
      "May flash HICP at 3.2%",
      "Energy-price shock and services inflation",
      "April decision to hold rates",
      "June staff macroeconomic projections",
    ],
    history: [
      { label: "Mar", value: 2.0 },
      { label: "Apr", value: 2.0 },
    ],
    historyTool: {
      tool: "ecb.lookup",
      call: 'ecb.lookup({ series: "deposit_facility_rate", decisions: ["2026-03-19", "2026-04-30"], next_decision: "2026-06-11 14:15 CET" })',
      result:
        "{ mar_2026: 2.00, apr_2026: 2.00, main_refi_apr: 2.15, marginal_lending_apr: 2.40, next_decision: '2026-06-11 14:15 CET' }",
    },
    policyParameter: "ecb.deposit_facility_rate.after_june_2026",
    targets: [
      {
        slug: "euro-area-ecb-deposit-facility-rate-june-2026",
        title: "ECB deposit facility rate, June 2026",
        question:
          "What will the ECB deposit facility rate be immediately after the monetary policy decisions published on June 11, 2026?",
        dataPointId: "ecb.deposit_facility_rate.after_june_2026",
        horizon: "next_release",
        horizonLabel: "next decision",
        periodLabel: "June 2026 Governing Council",
        resolutionDate: "2026-06-11",
        resolutionRule:
          "Resolves to the deposit facility rate stated in the ECB monetary policy decisions published on June 11, 2026. If the ECB posts a same-day correction before market close, the corrected value governs.",
        pointEstimate: 2.0,
        ciLow: 2.0,
        ciHigh: 2.25,
        tools: [
          {
            tool: "agent.run",
            call: 'euroJapanIndicatorAgent.predict({ slugs: ["euro-area-ecb-deposit-facility-rate-june-2026"], sources: ["ECB April 2026 decision", "Eurostat May 2026 flash HICP", "ECB weekly calendar"], runAt: "2026-06-06T05:41:31+01:00" })',
            result:
              "{ point: 2.00, ci80: [2.00, 2.25], context: ['April decision held deposit facility at 2.00%', 'May flash HICP 3.2%; energy 10.9%; services 3.5%', 'June decisions scheduled for 2026-06-11 14:15 CET'] }",
          },
        ],
        rationale:
          "The ECB held in April and framed policy as data-dependent. May inflation moved above target with energy and services pressure, so the agent rules out a cut in the central interval and gives the main tail to a 25 basis point hike, but keeps a hold as the modal outcome.",
      },
    ],
  },
  {
    seriesId: "eurostat.hicp.annual_rate",
    country: "EA",
    title: "Euro area HICP annual inflation",
    measure: "Harmonised Index of Consumer Prices all-items annual rate",
    unit: "percent",
    source: "Eurostat Harmonised Index of Consumer Prices",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Eurostat flash estimate and ECB inflation monitoring",
    chainableQuestions: ["next release", "+3 months", "ECB reaction"],
    whyItMatters:
      "HICP is the ECB's headline inflation measure and a high-frequency input for real-income, benefit-indexation, and monetary-policy predictions.",
    drivers: [
      "Energy inflation",
      "Services inflation",
      "Food, alcohol and tobacco",
      "Flash-to-final revision pattern",
    ],
    history: [
      { label: "Jan", value: 1.7 },
      { label: "Feb", value: 1.9 },
      { label: "Mar", value: 2.6 },
      { label: "Apr", value: 3.0 },
      { label: "May flash", value: 3.2 },
    ],
    historyTool: {
      tool: "eurostat.lookup",
      call: 'eurostat.lookup({ release: "HICP flash estimate", series: "euro_area_all_items_annual_rate", months: ["2026-01", "2026-05"] })',
      result:
        "{ jan: 1.7, feb: 1.9, mar: 2.6, apr_final: 3.0, may_flash: 3.2, may_flash_energy: 10.9, may_flash_services: 3.5, final_release: '2026-06-17' }",
    },
    targets: [
      {
        slug: "euro-area-hicp-annual-rate-may-2026-final",
        title: "Euro area HICP annual inflation, May 2026 final",
        question:
          "What will Eurostat first report as the final euro area all-items HICP annual inflation rate for May 2026?",
        dataPointId:
          "eurostat.hicp.all_items_annual_rate.euro_area.may_2026.final_first_print",
        horizon: "next_release",
        horizonLabel: "final release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-17",
        resolutionRule:
          "Resolves to Eurostat's first final all-items HICP annual inflation rate for the euro area for May 2026. The flash estimate is input context; later revisions do not change the resolved value.",
        pointEstimate: 3.2,
        ciLow: 3.1,
        ciHigh: 3.3,
        tools: [
          {
            tool: "agent.run",
            call: 'euroJapanIndicatorAgent.predict({ slugs: ["euro-area-hicp-annual-rate-may-2026-final"], sources: ["Eurostat May 2026 flash HICP", "Eurostat April 2026 final HICP"], runAt: "2026-06-06T05:41:31+01:00" })',
            result:
              "{ point: 3.2, ci80: [3.1, 3.3], context: ['May flash all-items HICP 3.2%', 'April final HICP 3.0%', 'flash-to-final revisions are usually small'] }",
          },
        ],
        rationale:
          "Eurostat's May flash already gives the all-items rate at 3.2%. The final release can move by a tenth if national detail revises, but the agent treats 3.2% as the overwhelmingly modal final first print.",
      },
      {
        slug: "euro-area-hicp-annual-rate-june-2026-flash",
        title: "Euro area HICP annual inflation, June 2026 flash",
        question:
          "What will Eurostat first estimate as the euro area all-items HICP annual inflation rate for June 2026 in the flash release?",
        dataPointId:
          "eurostat.hicp.all_items_annual_rate.euro_area.june_2026.flash",
        horizon: "next_release",
        horizonLabel: "flash release",
        periodLabel: "June 2026",
        resolutionDate: "2026-07-01",
        resolutionRule:
          "Resolves to Eurostat's first flash estimate of the euro area all-items HICP annual inflation rate for June 2026. The later final HICP release does not change the resolved value.",
        pointEstimate: 3.1,
        ciLow: 2.8,
        ciHigh: 3.4,
        tools: [
          {
            tool: "agent.run",
            call: 'euroJapanIndicatorAgent.predict({ slugs: ["euro-area-hicp-annual-rate-june-2026-flash"], sources: ["Eurostat May 2026 flash HICP", "energy futures", "ECB June monitoring"], runAt: "2026-06-06T05:41:31+01:00" })',
            result:
              "{ point: 3.1, ci80: [2.8, 3.4], context: ['May flash HICP 3.2%', 'energy annual rate 10.9%', 'services 3.5%', 'next flash release 2026-07-01'] }",
          },
        ],
        rationale:
          "May's 3.2% reading was pushed up by energy and services. The agent expects only mild easing in June because the energy shock remains visible, but assigns a wider interval than the May final forecast because the June flash is not yet observed.",
      },
    ],
  },
  {
    seriesId: "eurostat.unemployment_rate",
    country: "EA",
    title: "Euro area unemployment rate",
    measure: "Seasonally adjusted unemployment rate",
    unit: "percent",
    source: "Eurostat monthly unemployment",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~1 month",
    resolutionPolicy: "first_print",
    benchmark: "Eurostat monthly unemployment trend and ECB labour-market monitoring",
    chainableQuestions: ["next release", "+3 months", "slack threshold"],
    whyItMatters:
      "Euro area unemployment anchors labour-income, social-benefit, fiscal, and monetary-policy forecasts across member states.",
    drivers: [
      "April unemployment at 6.3%",
      "Youth unemployment improvement",
      "Country-level revisions",
      "Growth slowdown from energy shock",
    ],
    history: [
      { label: "Jan", value: 6.1 },
      { label: "Feb", value: 6.2 },
      { label: "Mar", value: 6.3 },
      { label: "Apr", value: 6.3 },
    ],
    historyTool: {
      tool: "eurostat.lookup",
      call: 'eurostat.lookup({ release: "Monthly unemployment", series: "euro_area_seasonally_adjusted_unemployment_rate", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 6.1, feb: 6.2, mar_revised: 6.3, apr: 6.3, apr_unemployed_millions: 11.075, next_release: '2026-07-02' }",
    },
    targets: [
      {
        slug: "euro-area-unemployment-rate-may-2026",
        title: "Euro area unemployment rate, May 2026",
        question:
          "What will Eurostat first report as the euro area seasonally adjusted unemployment rate for May 2026?",
        dataPointId:
          "eurostat.unemployment_rate.euro_area.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-07-02",
        resolutionRule:
          "Resolves to the first published seasonally adjusted euro area unemployment rate for May 2026 in Eurostat's monthly unemployment release. Later revisions do not change the resolved value.",
        pointEstimate: 6.3,
        ciLow: 6.2,
        ciHigh: 6.4,
        tools: [
          {
            tool: "agent.run",
            call: 'euroJapanIndicatorAgent.predict({ slugs: ["euro-area-unemployment-rate-may-2026"], sources: ["Eurostat April 2026 unemployment", "Eurostat EU-LFS release calendar"], runAt: "2026-06-06T05:41:31+01:00" })',
            result:
              "{ point: 6.3, ci80: [6.2, 6.4], context: ['April unemployment 6.3%', 'March revised to 6.3%', 'April unemployed count 11.075m', 'next monthly release 2026-07-02'] }",
          },
        ],
        rationale:
          "Monthly euro area unemployment has been stable around 6.2%-6.3% even as inflation and growth risks shifted. The agent centers May at 6.3% and keeps the interval tight because one-month changes in the harmonised rate are usually one tenth or less.",
      },
    ],
  },
  {
    seriesId: "boj.policy_rate_guideline",
    country: "JP",
    type: "policy",
    title: "Bank of Japan policy-rate guideline",
    measure: "Uncollateralized overnight call rate guideline after the MPM",
    unit: "percent",
    source: "Bank of Japan Statement on Monetary Policy",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Policy Board vote split and market-implied yen rate path",
    chainableQuestions: ["next decision", "+3 months", "inflation reaction"],
    whyItMatters:
      "The BOJ policy-rate guideline is Japan's central monetary-policy setting and connects inflation, wages, yen pressure, and public-debt-service forecasts.",
    drivers: [
      "April 6-3 vote split",
      "Upside price-risk dissents",
      "June JGB purchase-plan assessment",
      "Tokyo and national CPI path",
    ],
    history: [
      { label: "Jan", value: 0.75 },
      { label: "Mar", value: 0.75 },
      { label: "Apr", value: 0.75 },
    ],
    historyTool: {
      tool: "boj.lookup",
      call: 'boj.lookup({ release: "Statement on Monetary Policy", decisions: ["2026-01-23", "2026-03-19", "2026-04-28"], next_meeting: "2026-06-15/16" })',
      result:
        "{ apr_guideline: 0.75, apr_vote: '6-3', dissent_guideline: 1.00, next_mpm: '2026-06-15/16' }",
    },
    policyParameter: "boj.policy_rate_guideline.after_june_2026",
    targets: [
      {
        slug: "japan-boj-policy-rate-june-2026",
        title: "Bank of Japan policy-rate guideline, June 2026",
        question:
          "What will the Bank of Japan guideline for the uncollateralized overnight call rate be immediately after its June 2026 Monetary Policy Meeting?",
        dataPointId: "boj.policy_rate_guideline.after_june_2026",
        horizon: "next_release",
        horizonLabel: "next decision",
        periodLabel: "June 2026 MPM",
        resolutionDate: "2026-06-16",
        resolutionRule:
          "Resolves to the guideline for money market operations stated in the Bank of Japan Statement on Monetary Policy released after the June 15-16, 2026 Monetary Policy Meeting. If the Bank posts a same-day correction before market close, the corrected value governs.",
        pointEstimate: 0.75,
        ciLow: 0.75,
        ciHigh: 1.0,
        tools: [
          {
            tool: "agent.run",
            call: 'euroJapanIndicatorAgent.predict({ slugs: ["japan-boj-policy-rate-june-2026"], sources: ["BOJ April 2026 statement", "BOJ June 2026 meeting schedule", "Statistics Bureau CPI"], runAt: "2026-06-06T05:41:31+01:00" })',
            result:
              "{ point: 0.75, ci80: [0.75, 1.00], context: ['April guideline around 0.75%', 'April vote 6-3; three members preferred 1.00%', 'June meeting June 15-16', 'April national CPI 1.4%'] }",
          },
        ],
        rationale:
          "Three April dissents wanted a 1.0% guideline, but the majority held at 0.75%. The agent keeps a hold as the modal outcome because national CPI is still modest, while the dissent pattern and upside price-risk language keep a live hike tail.",
      },
    ],
  },
  {
    seriesId: "statjp.cpi.annual_rate",
    country: "JP",
    title: "Japan CPI annual inflation",
    measure: "National all-items CPI annual rate",
    unit: "percent",
    source: "Statistics Bureau of Japan Consumer Price Index",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~3 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Tokyo preliminary CPI and BOJ inflation outlook",
    chainableQuestions: ["next release", "+3 months", "BOJ reaction"],
    whyItMatters:
      "Japan's national CPI is the official inflation read behind BOJ policy-rate decisions, wage bargaining, and real-income forecasts.",
    drivers: [
      "April national CPI at 1.4%",
      "Tokyo preliminary CPI signal",
      "Energy and food prices",
      "Yen import-price pass-through",
    ],
    history: [
      { label: "Feb", value: 1.7 },
      { label: "Mar", value: 1.5 },
      { label: "Apr", value: 1.4 },
    ],
    historyTool: {
      tool: "statjp.lookup",
      call: 'statjp.lookup({ release: "Consumer Price Index", series: "national_all_items_annual_rate", months: ["2026-02", "2026-04"], next_release: "2026-06-19" })',
      result:
        "{ feb: 1.7, mar: 1.5, apr: 1.4, may_release: '2026-06-19' }",
    },
    targets: [
      {
        slug: "japan-cpi-annual-rate-may-2026",
        title: "Japan CPI annual inflation, May 2026",
        question:
          "What will the Statistics Bureau of Japan first report as the national all-items CPI annual inflation rate for May 2026?",
        dataPointId:
          "statjp.cpi.all_items_annual_rate.japan.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-19",
        resolutionRule:
          "Resolves to the first published national all-items CPI annual rate for May 2026 in the Statistics Bureau of Japan Consumer Price Index release. Later revisions do not change the resolved value.",
        pointEstimate: 1.5,
        ciLow: 1.1,
        ciHigh: 1.9,
        tools: [
          {
            tool: "agent.run",
            call: 'euroJapanIndicatorAgent.predict({ slugs: ["japan-cpi-annual-rate-may-2026"], sources: ["Statistics Bureau Japan CPI April 2026", "Tokyo CPI May 2026 preliminary"], runAt: "2026-06-06T05:41:31+01:00" })',
            result:
              "{ point: 1.5, ci80: [1.1, 1.9], context: ['April national all-items CPI 1.4%', 'May national CPI release scheduled for 2026-06-19', 'Tokyo preliminary CPI usually leads national CPI'] }",
          },
        ],
        rationale:
          "April national CPI was 1.4%. The agent expects a small May rebound from food, energy, and yen pass-through risk, but keeps the interval wide because Tokyo-to-national translation and subsidy effects can shift the first print.",
      },
    ],
  },
  {
    seriesId: "statjp.cpi.tokyo_annual_rate",
    country: "JP",
    title: "Tokyo CPI annual inflation",
    measure: "Ku-area of Tokyo preliminary all-items CPI annual rate",
    unit: "percent",
    source: "Statistics Bureau of Japan Consumer Price Index",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~4 weeks",
    resolutionPolicy: "first_print",
    benchmark: "National CPI nowcast and Tokyo preliminary CPI history",
    chainableQuestions: ["next release", "national CPI nowcast", "BOJ reaction"],
    whyItMatters:
      "Tokyo CPI is Japan's fastest official inflation indicator and gives agents an early signal before national CPI resolves.",
    drivers: [
      "National CPI April trend",
      "Utility and food-price changes",
      "Tokyo service prices",
      "Month-end release timing",
    ],
    history: [
      { label: "Apr", value: 1.5 },
      { label: "May", value: 1.4 },
    ],
    historyTool: {
      tool: "statjp.lookup",
      call: 'statjp.lookup({ release: "Consumer Price Index, Ku-area of Tokyo preliminary", series: "all_items_annual_rate", months: ["2026-04", "2026-05"], next_release: "2026-06-26" })',
      result:
        "{ apr_prelim: 1.5, may_prelim: 1.4, june_prelim_release: '2026-06-26' }",
    },
    targets: [
      {
        slug: "japan-tokyo-cpi-annual-rate-june-2026-prelim",
        title: "Tokyo CPI annual inflation, June 2026 preliminary",
        question:
          "What will the Statistics Bureau of Japan first report as the Ku-area of Tokyo preliminary all-items CPI annual inflation rate for June 2026?",
        dataPointId:
          "statjp.cpi.tokyo_all_items_annual_rate.june_2026.preliminary",
        horizon: "next_release",
        horizonLabel: "preliminary release",
        periodLabel: "June 2026",
        resolutionDate: "2026-06-26",
        resolutionRule:
          "Resolves to the first published Ku-area of Tokyo preliminary all-items CPI annual inflation rate for June 2026 in the Statistics Bureau of Japan Consumer Price Index release. Later revisions do not change the resolved value.",
        pointEstimate: 1.6,
        ciLow: 1.2,
        ciHigh: 2.0,
        tools: [
          {
            tool: "agent.run",
            call: 'euroJapanIndicatorAgent.predict({ slugs: ["japan-tokyo-cpi-annual-rate-june-2026-prelim"], sources: ["Statistics Bureau Tokyo CPI May 2026 preliminary", "Japan national CPI April 2026"], runAt: "2026-06-06T05:41:31+01:00" })',
            result:
              "{ point: 1.6, ci80: [1.2, 2.0], context: ['Tokyo May preliminary CPI around 1.4%', 'national April CPI 1.4%', 'June Tokyo release scheduled 2026-06-26'] }",
          },
        ],
        rationale:
          "Tokyo preliminary CPI is close to the national trend but can move first on administered prices and services. The agent predicts a modest June increase while leaving room for unchanged inflation if utility subsidies dominate.",
      },
    ],
  },
  {
    seriesId: "statjp.lfs.unemployment_rate",
    country: "JP",
    title: "Japan unemployment rate",
    measure: "Labour Force Survey unemployment rate, seasonally adjusted",
    unit: "percent",
    source: "Statistics Bureau of Japan Labour Force Survey",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~1 month",
    resolutionPolicy: "first_print",
    benchmark: "Recent Labour Force Survey and employment conditions",
    chainableQuestions: ["next release", "+3 months", "wage pressure"],
    whyItMatters:
      "Japan's unemployment rate is a compact labour-market slack target for wage, consumption, and monetary-policy forecasts.",
    drivers: [
      "April unemployment at 2.5%",
      "Low structural unemployment",
      "Monthly survey volatility",
      "Wage and vacancy indicators",
    ],
    history: [
      { label: "Feb", value: 2.6 },
      { label: "Mar", value: 2.7 },
      { label: "Apr", value: 2.5 },
    ],
    historyTool: {
      tool: "statjp.lookup",
      call: 'statjp.lookup({ release: "Labour Force Survey", series: "seasonally_adjusted_unemployment_rate", months: ["2026-02", "2026-04"], next_release: "2026-06-30" })',
      result:
        "{ feb: 2.6, mar: 2.7, apr: 2.5, may_release: '2026-06-30' }",
    },
    targets: [
      {
        slug: "japan-unemployment-rate-may-2026",
        title: "Japan unemployment rate, May 2026",
        question:
          "What will the Statistics Bureau of Japan first report as Japan's seasonally adjusted unemployment rate for May 2026?",
        dataPointId:
          "statjp.lfs.unemployment_rate.japan.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-30",
        resolutionRule:
          "Resolves to the first published seasonally adjusted unemployment rate for May 2026 in the Statistics Bureau of Japan Labour Force Survey basic tabulation. Later revisions do not change the resolved value.",
        pointEstimate: 2.5,
        ciLow: 2.3,
        ciHigh: 2.8,
        tools: [
          {
            tool: "agent.run",
            call: 'euroJapanIndicatorAgent.predict({ slugs: ["japan-unemployment-rate-may-2026"], sources: ["Statistics Bureau Labour Force Survey April 2026", "Statistics Bureau release schedule"], runAt: "2026-06-06T05:41:31+01:00" })',
            result:
              "{ point: 2.5, ci80: [2.3, 2.8], context: ['April unemployment 2.5%', 'March 2.7%', 'May release scheduled for 2026-06-30'] }",
          },
        ],
        rationale:
          "The April rate fell to 2.5% after March's 2.7%. Japan's unemployment rate usually moves slowly, so the agent holds the central estimate at 2.5% with a two-to-three-tenths uncertainty band.",
      },
    ],
  },
] satisfies Omit<PredictionSeries, "predictionRun">[];

export const EURO_JAPAN_PREDICTION_SERIES =
  EURO_JAPAN_PREDICTION_SERIES_BASE.map((series) => ({
    ...series,
    predictionRun: RECORDED_EURO_JAPAN_AGENT_RUN,
  })) satisfies PredictionSeries[];

export const EURO_JAPAN_EXAMPLES = buildForecastCellsFromSeries(
  EURO_JAPAN_PREDICTION_SERIES,
);
