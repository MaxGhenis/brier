import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";

const RECORDED_US_DEFENSE_RUN: NonNullable<PredictionSeries["predictionRun"]> =
  {
    kind: "recorded-agent-run",
    runAt: "2026-06-29T14:35:00+01:00",
    agent: "brier-defense-public-data",
    model: "Codex recorded source-context synthesis",
    sourceContext: [
      "BLS public API, CES3133640001 aerospace product and parts employment",
      "BLS public API, CES3133660001 ship and boat building employment",
      "BLS public API, CES9091911001 federal Department of Defense employment",
      "Treasury FiscalData API, Monthly Treasury Statement table 5 line 5.12",
      "USAspending agency 097 obligations_by_award_category endpoint",
    ],
    runLabel: "Defense public-data batch",
    runDescription:
      "Forecasts official public targets that turn defense policy questions into resolvable funding, contract, personnel, and industrial-base series.",
  };

const US_DEFENSE_PREDICTION_SERIES_BASE = [
  {
    seriesId: "bls.ces.aerospace_product_and_parts_employment",
    country: "US",
    title: "US aerospace product and parts employment",
    measure:
      "Current Employment Statistics all employees, aerospace product and parts manufacturing, seasonally adjusted",
    unit: "thousands",
    source: "U.S. Bureau of Labor Statistics, Current Employment Statistics",
    sourceUrl: "https://api.bls.gov/publicAPI/v2/timeseries/data/CES3133640001",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "2 days",
    resolutionPolicy: "first_print",
    benchmark: "Last-print persistence and recent CES manufacturing momentum",
    chainableQuestions: [
      "next release",
      "+3 months",
      "shipbuilding comparison",
    ],
    whyItMatters:
      "Aerospace employment is a public, monthly proxy for defense-industrial-base capacity in aircraft, missiles, spacecraft, and major supplier networks.",
    drivers: [
      "Aircraft and missile backlog",
      "Defense procurement timing",
      "Commercial aerospace cycle",
      "Skilled manufacturing labor supply",
    ],
    history: [
      { label: "Jun 2025", value: 566.8 },
      { label: "Dec 2025", value: 577.6 },
      { label: "Feb 2026", value: 579.9 },
      { label: "Apr 2026", value: 585.4 },
    ],
    historyTool: {
      tool: "bls.public_api",
      call: 'bls.public_api({ seriesid: "CES3133640001", startyear: 2025, endyear: 2026 })',
      result:
        "{ jun2025: 566.8, dec2025: 577.6, feb2026: 579.9, mar2026: 583.5, apr2026_prelim: 585.4 }",
    },
    targets: [
      {
        slug: "us-defense-aerospace-employment-june-2026",
        title: "US aerospace products employment, June 2026",
        question:
          "What will BLS first report as seasonally adjusted aerospace product and parts manufacturing employment for June 2026?",
        dataPointId:
          "bls.ces.aerospace_product_and_parts_employment.june_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next Employment Situation release",
        periodLabel: "June 2026",
        resolutionDate: "2026-07-02",
        resolutionRule:
          "Resolves to the first-published June 2026 BLS CES all-employees value for CES3133640001 (Aerospace product and parts manufacturing), seasonally adjusted, in thousands of workers. Later benchmark revisions, seasonal-factor updates, or database refreshes do not change the resolved value unless BLS replaces the first July 2, 2026 release on that publication date.",
        pointEstimate: 589,
        ciLow: 583,
        ciHigh: 596,
        tools: [
          {
            tool: "brier.public_series_inventory",
            call: 'brier.public_series_inventory({ public_sources: ["BLS CES", "Treasury MTS", "USAspending"], themes: ["defense industrial base", "funding", "contract obligations"] })',
            result:
              "{ useful_public_series: ['BLS CES aerospace employment', 'BLS CES shipbuilding employment', 'Treasury MTS DoD outlays', 'USAspending DoD contract obligations'], selected_proxy: 'BLS CES aerospace employment' }",
          },
        ],
        rationale:
          "The latest public CES path is rising steadily, up 7.8k from June 2025 to April 2026 and 5.8k since January. The forecast extends that trend but shrinks toward persistence because aerospace hiring is lumpy and the CES first print can revise around survey timing.",
      },
    ],
  },
  {
    seriesId: "bls.ces.ship_and_boat_building_employment",
    country: "US",
    title: "US ship and boat building employment",
    measure:
      "Current Employment Statistics all employees, ship and boat building, seasonally adjusted",
    unit: "thousands",
    source: "U.S. Bureau of Labor Statistics, Current Employment Statistics",
    sourceUrl: "https://api.bls.gov/publicAPI/v2/timeseries/data/CES3133660001",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "2 days",
    resolutionPolicy: "first_print",
    benchmark: "Last-print persistence and shipyard labor trend",
    chainableQuestions: ["next release", "+3 months", "aerospace comparison"],
    whyItMatters:
      "Shipbuilding employment is a monthly public proxy for naval procurement capacity, yard bottlenecks, and defense supply-chain constraints.",
    drivers: [
      "Navy procurement and maintenance workload",
      "Shipyard labor availability",
      "Commercial vessel demand",
      "Defense industrial-base investment",
    ],
    history: [
      { label: "Jun 2024", value: 153.2 },
      { label: "Jun 2025", value: 149.4 },
      { label: "Dec 2025", value: 148.8 },
      { label: "Apr 2026", value: 148.5 },
    ],
    historyTool: {
      tool: "bls.public_api",
      call: 'bls.public_api({ seriesid: "CES3133660001", startyear: 2024, endyear: 2026 })',
      result:
        "{ jun2024: 153.2, jun2025: 149.4, dec2025: 148.8, feb2026: 148.6, mar2026: 148.6, apr2026_prelim: 148.5 }",
    },
    targets: [
      {
        slug: "us-defense-shipbuilding-employment-june-2026",
        title: "US ship and boat building employment, June 2026",
        question:
          "What will BLS first report as seasonally adjusted ship and boat building employment for June 2026?",
        dataPointId:
          "bls.ces.ship_and_boat_building_employment.june_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next Employment Situation release",
        periodLabel: "June 2026",
        resolutionDate: "2026-07-02",
        resolutionRule:
          "Resolves to the first-published June 2026 BLS CES all-employees value for CES3133660001 (Ship and boat building), seasonally adjusted, in thousands of workers. Later benchmark revisions, seasonal-factor updates, or database refreshes do not change the resolved value unless BLS replaces the first July 2, 2026 release on that publication date.",
        pointEstimate: 148.4,
        ciLow: 146.8,
        ciHigh: 150.1,
        rationale:
          "Ship and boat building employment has been almost flat through early 2026 and lower than mid-2024. The center is a persistence forecast with a slight downward drift, while the interval leaves room for small first-print noise and delayed yard hiring.",
      },
    ],
  },
  {
    seriesId: "bls.ces.federal_department_of_defense_employment",
    country: "US",
    title: "Federal Department of Defense employment",
    measure:
      "Current Employment Statistics all employees, federal government Department of Defense, seasonally adjusted",
    unit: "thousands",
    source: "U.S. Bureau of Labor Statistics, Current Employment Statistics",
    sourceUrl: "https://api.bls.gov/publicAPI/v2/timeseries/data/CES9091911001",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "2 days",
    resolutionPolicy: "first_print",
    benchmark: "Last-print persistence after late-2025 level shift",
    chainableQuestions: [
      "next release",
      "+3 months",
      "contract-obligation comparison",
    ],
    whyItMatters:
      "DoD civilian employment is a public personnel-capacity target for testing claims about acquisition reform, hiring authorities, and execution capacity.",
    drivers: [
      "Federal hiring policy",
      "DoD civilian workforce plans",
      "Reclassification or benchmark effects",
      "Appropriations and execution pressure",
    ],
    history: [
      { label: "Jun 2025", value: 560.0 },
      { label: "Dec 2025", value: 490.1 },
      { label: "Feb 2026", value: 478.2 },
      { label: "Apr 2026", value: 474.9 },
    ],
    historyTool: {
      tool: "bls.public_api",
      call: 'bls.public_api({ seriesid: "CES9091911001", startyear: 2025, endyear: 2026 })',
      result:
        "{ jun2025: 560.0, sep2025: 559.8, oct2025: 503.8, dec2025: 490.1, jan2026: 470.0, apr2026_prelim: 474.9 }",
    },
    targets: [
      {
        slug: "us-defense-dod-employment-june-2026",
        title: "Federal DoD employment, June 2026",
        question:
          "What will BLS first report as seasonally adjusted federal Department of Defense employment for June 2026?",
        dataPointId:
          "bls.ces.federal_department_of_defense_employment.june_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next Employment Situation release",
        periodLabel: "June 2026",
        resolutionDate: "2026-07-02",
        resolutionRule:
          "Resolves to the first-published June 2026 BLS CES all-employees value for CES9091911001 (Federal government, Department of Defense), seasonally adjusted, in thousands of workers. Later benchmark revisions, seasonal-factor updates, or database refreshes do not change the resolved value unless BLS replaces the first July 2, 2026 release on that publication date.",
        pointEstimate: 474,
        ciLow: 452,
        ciHigh: 501,
        tools: [
          {
            tool: "brier.public_series_inventory",
            call: 'brier.public_series_inventory({ public_sources: ["BLS CES"], themes: ["personnel capacity", "federal defense workforce"] })',
            result:
              "{ useful_public_series: ['BLS CES federal Department of Defense employment'], selected_proxy: 'BLS CES DoD employment', latest_public_history_points: 6 }",
          },
        ],
        rationale:
          "The series shows a large late-2025 level shift, then relative stability from January through April 2026. The center stays close to April's first print; the wide interval reflects uncertainty about whether the shift was administrative, policy-driven, or still passing through the first-print data.",
      },
    ],
  },
  {
    seriesId: "treasury.mts.dod_military_programs_gross_outlays",
    country: "US",
    title: "DoD military programs gross outlays",
    measure:
      "Monthly Treasury Statement table 5 line 5.12 current-month gross outlays",
    unit: "usd_billions",
    source:
      "U.S. Treasury Bureau of the Fiscal Service, Monthly Treasury Statement",
    sourceUrl:
      "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_5",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "13 days",
    resolutionPolicy: "first_print",
    benchmark: "Recent MTS DoD outlays and quarter-end execution seasonality",
    chainableQuestions: [
      "next release",
      "+3 months",
      "contract-obligation bridge",
    ],
    whyItMatters:
      "DoD outlays are the official cash-flow endpoint for defense resource allocation, showing how appropriated budget authority turns into government payments.",
    drivers: [
      "Quarter-end budget execution",
      "Procurement and RDT&E payment timing",
      "Military personnel outlays",
      "Contract invoice timing",
    ],
    history: [
      { label: "Dec 2025", value: 98.3 },
      { label: "Jan 2026", value: 70.7 },
      { label: "Mar 2026", value: 65.4 },
      { label: "Apr 2026", value: 73.3 },
      { label: "May 2026", value: 69.2 },
    ],
    historyTool: {
      tool: "treasury.fiscaldata",
      call: 'fiscaldata.mts_table_5({ record_fiscal_year: 2026, sequence_number_cd: "5.12", fields: ["record_calendar_month", "current_month_gross_outly_amt"] })',
      result:
        "{ dec2025: 98.275, jan2026: 70.652, feb2026: 67.006, mar2026: 65.379, apr2026: 73.261, may2026: 69.178 }",
    },
    targets: [
      {
        slug: "us-defense-dod-military-outlays-june-2026",
        title: "DoD military programs gross outlays, June 2026",
        question:
          "What will Treasury first report as Department of Defense military programs gross outlays for June 2026 in the Monthly Treasury Statement?",
        dataPointId:
          "treasury.mts.dod_military_programs_gross_outlays.june_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next MTS release",
        periodLabel: "June 2026",
        resolutionDate: "2026-07-13",
        resolutionRule:
          "Resolves to Monthly Treasury Statement table 5 line 5.12, Total--Department of Defense--Military Programs, current-month gross outlays for June 2026, divided by 1 billion dollars. The first published MTS table governs; later revisions or database refreshes do not change the resolved value unless Treasury replaces the first table on the same publication date.",
        pointEstimate: 72,
        ciLow: 62,
        ciHigh: 86,
        tools: [
          {
            tool: "brier.public_series_inventory",
            call: 'brier.public_series_inventory({ public_sources: ["Treasury MTS", "USAspending"], themes: ["appropriations", "outlays", "contract obligations"] })',
            result:
              "{ useful_public_series: ['Treasury MTS DoD military programs gross outlays', 'USAspending DoD contract obligations'], selected_proxy: 'MTS DoD military programs outlays', latest_public_history_points: 6 }",
          },
        ],
        rationale:
          "May was $69.18B after a $73.26B April and $65.38B March. June is a quarter-end month, so the forecast sits above May but well below the December surge, with a wider interval because procurement and RDT&E payment timing can move several billion dollars month to month.",
      },
    ],
  },
  {
    seriesId: "usaspending.dod.contract_obligations",
    country: "US",
    title: "DoD contract obligations",
    measure:
      "USAspending agency 097 obligations_by_award_category, contracts category",
    unit: "usd_billions",
    source: "USAspending.gov",
    sourceUrl:
      "https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/",
    cadence: "annual",
    priority: "P1",
    resolutionLatency: "91 days",
    resolutionPolicy: "fixed_vintage",
    benchmark:
      "FY2024-FY2025 final contract obligations and FY2026 partial-year reporting",
    chainableQuestions: [
      "next fiscal year",
      "quarterly vintage",
      "outlay comparison",
    ],
    whyItMatters:
      "Contract obligations are the public award-level bridge between defense appropriations and actual commitments to firms, which is the core measurable surface for acquisition-policy simulation.",
    drivers: [
      "FY2026 appropriations and continuing-resolution timing",
      "Fourth-quarter obligation surge",
      "Major procurement award timing",
      "DATA Act and FPDS reporting refreshes",
    ],
    history: [
      { label: "FY2024", value: 491.7 },
      { label: "FY2025", value: 446.0 },
      { label: "FY2026 partial", value: 207.5 },
    ],
    historyTool: {
      tool: "usaspending.api",
      call: 'usaspending.agency_obligations_by_award_category({ agency: "097", fiscal_years: [2024, 2025, 2026], category: "contracts" })',
      result:
        "{ fy2024_contracts: 491.715, fy2025_contracts: 445.996, fy2026_current_contracts: 207.527 }",
    },
    targets: [
      {
        slug: "us-defense-dod-contract-obligations-fy2026",
        title: "DoD contract obligations, FY2026",
        question:
          "What will USAspending report as Department of Defense FY2026 contract obligations in the fixed December 31, 2026 vintage?",
        dataPointId:
          "usaspending.dod.contract_obligations.fy2026.fixed_vintage_2026_12_31",
        horizon: "plus_3m",
        horizonLabel: "fixed post-year vintage",
        periodLabel: "FY 2026",
        resolutionDate: "2026-12-31",
        resolutionRule:
          "Resolves to USAspending agency 097 obligations_by_award_category for fiscal_year=2026, category=contracts, aggregated_amount divided by 1 billion dollars, using a data pull on December 31, 2026. This fixed-vintage rule avoids treating later FPDS or DATA Act refreshes as forecast revisions.",
        pointEstimate: 470,
        ciLow: 405,
        ciHigh: 535,
        tools: [
          {
            tool: "usaspending.api",
            call: "GET /api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026",
            result:
              "{ contracts: 207.527, total_aggregated_amount: 212.911, endpoint_accessed: '2026-06-29' }",
          },
        ],
        rationale:
          "The partial FY2026 contract total is not comparable to final-year values because defense obligations are back-loaded and reporting refreshes continue after fiscal year close. FY2024 and FY2025 bracket the outside view; the forecast centers between them with upside for a fourth-quarter award surge and downside for continuing-resolution or procurement delay.",
      },
    ],
  },
] satisfies Omit<PredictionSeries, "predictionRun">[];

export const US_DEFENSE_PREDICTION_SERIES =
  US_DEFENSE_PREDICTION_SERIES_BASE.map((series) => ({
    ...series,
    predictionRun: RECORDED_US_DEFENSE_RUN,
  })) satisfies PredictionSeries[];

export const US_DEFENSE_EXAMPLES = buildForecastCellsFromSeries(
  US_DEFENSE_PREDICTION_SERIES,
);
