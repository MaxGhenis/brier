import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";

const RECORDED_GLOBAL_NEAR_TERM_RUN: NonNullable<
  PredictionSeries["predictionRun"]
> = {
  kind: "recorded-agent-run",
  runAt: "2026-06-06T14:42:00+02:00",
  agent: "Global near-term indicator source synthesis",
  model: "Codex recorded source-context synthesis",
  sourceContext: [
    "Statistics Canada major economic release calendar and The Daily",
    "Australian Bureau of Statistics future releases and latest releases",
    "Eurostat Euro indicators",
    "Statistics Bureau of Japan release schedules and latest indicators",
  ],
};

const GLOBAL_NEAR_TERM_PREDICTION_SERIES_BASE = [
  {
    seriesId: "statcan.retail_trade.sales_mom",
    country: "CA",
    title: "Canada retail sales growth",
    measure: "Monthly change in seasonally adjusted retail sales",
    unit: "percent_growth",
    source: "Statistics Canada Retail Trade",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~3 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Statistics Canada advance retail indicator",
    chainableQuestions: ["next release", "+3 months", "GDP contribution"],
    whyItMatters:
      "Retail sales are a fast official read on Canadian household demand, consumer credit stress, and sales-tax bases.",
    drivers: [
      "Advance retail indicator",
      "Gasoline station sales",
      "Motor vehicle and parts dealers",
      "Core retail demand",
    ],
    history: [
      { label: "Feb", value: 0.7 },
      { label: "Mar", value: 0.9 },
      { label: "Apr adv", value: 0.6 },
    ],
    historyTool: {
      tool: "statcan.lookup",
      call: 'statcan.lookup({ release: "Retail trade", series: "seasonally_adjusted_retail_sales_mom", months: ["2026-02", "2026-03"], advance_month: "2026-04" })',
      result:
        "{ feb: 0.7, mar: 0.9, apr_advance: 0.6, apr_release: '2026-06-19 08:30 ET' }",
    },
    targets: [
      {
        slug: "canada-retail-sales-growth-april-2026",
        title: "Canada retail sales growth, April 2026",
        question:
          "What will Statistics Canada first report as the monthly change in seasonally adjusted Canadian retail sales for April 2026?",
        dataPointId:
          "statcan.retail_trade.sales_mom.canada.april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "April 2026",
        resolutionDate: "2026-06-19",
        resolutionRule:
          "Resolves to the first published monthly percent change in seasonally adjusted Canadian retail sales for April 2026 in Statistics Canada's Retail trade release. Later revisions do not change the resolved value.",
        pointEstimate: 0.6,
        ciLow: -0.2,
        ciHigh: 1.4,
        tools: [
          {
            tool: "statcan.lookup",
            call: 'statcan.lookup({ release: "Retail trade, March 2026", fields: ["march_sales_mom", "march_volume_mom", "april_advance", "april_release"] })',
            result:
              "{ march_sales_mom: 0.9, march_volume_mom: -0.7, april_advance: 0.6, april_release: '2026-06-19' }",
          },
        ],
        rationale:
          "The advance indicator points to a 0.6% April increase after March's 0.9% current-dollar gain. The interval allows the early estimate to revise because the advance response rate was well below the final survey response rate and March volume sales were weaker than nominal sales.",
      },
    ],
  },
  {
    seriesId: "statcan.wholesale_trade.sales_mom",
    country: "CA",
    title: "Canada wholesale sales growth",
    measure:
      "Monthly change in seasonally adjusted wholesale sales excluding petroleum and oilseed/grain",
    unit: "percent_growth",
    source: "Statistics Canada Wholesale Trade",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Statistics Canada wholesale advance indicator",
    chainableQuestions: ["next release", "+3 months", "inventory ratio"],
    whyItMatters:
      "Wholesale trade is an early supply-chain and business-demand signal that feeds Canadian GDP by industry and inventory-cycle forecasts.",
    drivers: [
      "Advance wholesale indicator",
      "Machinery and equipment sales",
      "Building material and supplies sales",
      "Inventory-to-sales ratio",
    ],
    history: [
      { label: "Feb", value: 2.0 },
      { label: "Mar", value: 1.9 },
      { label: "Apr adv", value: 0.1 },
    ],
    historyTool: {
      tool: "statcan.lookup",
      call: 'statcan.lookup({ release: "Wholesale trade", series: "sales_mom_ex_petroleum_oilseed_grain", months: ["2026-02", "2026-03"], advance_month: "2026-04" })',
      result:
        "{ feb: 2.0, mar: 1.9, apr_advance: 0.1, apr_release: '2026-06-15 08:30 ET' }",
    },
    targets: [
      {
        slug: "canada-wholesale-sales-growth-april-2026",
        title: "Canada wholesale sales growth, April 2026",
        question:
          "What will Statistics Canada first report as the monthly change in Canadian wholesale sales for April 2026, excluding petroleum, petroleum products, other hydrocarbons, oilseed, and grain?",
        dataPointId:
          "statcan.wholesale_trade.sales_mom_exclusions.canada.april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "April 2026",
        resolutionDate: "2026-06-15",
        resolutionRule:
          "Resolves to the first published monthly percent change in seasonally adjusted wholesale sales excluding petroleum, petroleum products, other hydrocarbons, oilseed, and grain in Statistics Canada's April 2026 Wholesale trade release. Later revisions do not change the resolved value.",
        pointEstimate: 0.2,
        ciLow: -1.0,
        ciHigh: 1.4,
        tools: [
          {
            tool: "statcan.lookup",
            call: 'statcan.lookup({ release: "Wholesale trade: Advance indicator, April 2026", fields: ["advance_sales_mom", "weighted_response_rate", "regular_release"] })',
            result:
              "{ advance_sales_mom: 0.1, weighted_response_rate: 62.5, regular_release: '2026-06-15' }",
          },
        ],
        rationale:
          "The April advance indicator is barely positive at 0.1%, while February and March were both strong. The source synthesis keeps the point close to the advance value and widens the interval because advance wholesale indicators are explicitly subject to higher revision risk.",
      },
    ],
  },
  {
    seriesId: "statcan.employment_insurance.regular_beneficiaries",
    country: "CA",
    title: "Canada regular EI beneficiaries",
    measure: "Regular Employment Insurance beneficiaries, seasonally adjusted",
    unit: "thousands",
    source: "Statistics Canada Employment Insurance Statistics",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~3 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Statistics Canada EI trend and Labour Force Survey slack",
    chainableQuestions: ["next release", "+3 months", "unemployment linkage"],
    whyItMatters:
      "EI beneficiary counts are a direct administrative benefits-flow signal and a useful check on labour-market slack beyond the unemployment rate.",
    drivers: [
      "Labour Force Survey unemployment rate",
      "Seasonal benefit exhaustion",
      "New EI claims",
      "Regional unemployment thresholds",
    ],
    history: [
      { label: "Jan", value: 555 },
      { label: "Feb", value: 542 },
      { label: "Mar", value: 548 },
    ],
    historyTool: {
      tool: "statcan.lookup",
      call: 'statcan.lookup({ release: "Employment Insurance", series: "regular_beneficiaries_thousands", months: ["2026-01", "2026-03"] })',
      result:
        "{ jan: 555, feb: 542, mar: 548, apr_release: '2026-06-18 08:30 ET' }",
    },
    targets: [
      {
        slug: "canada-ei-regular-beneficiaries-april-2026",
        title: "Canada regular EI beneficiaries, April 2026",
        question:
          "What will Statistics Canada first report as the number of regular Employment Insurance beneficiaries in Canada for April 2026?",
        dataPointId:
          "statcan.employment_insurance.regular_beneficiaries.canada.april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "April 2026",
        resolutionDate: "2026-06-18",
        resolutionRule:
          "Resolves to the first published seasonally adjusted number of regular Employment Insurance beneficiaries for Canada in Statistics Canada's April 2026 Employment Insurance release, expressed in thousands. Later revisions do not change the resolved value.",
        pointEstimate: 552,
        ciLow: 536,
        ciHigh: 570,
        tools: [
          {
            tool: "statcan.lookup",
            call: 'statcan.lookup({ release: "Employment Insurance, March 2026", fields: ["march_regular_beneficiaries", "march_mom", "march_yoy", "april_release"] })',
            result:
              "{ march_regular_beneficiaries_thousands: 548, march_mom: 0.4, march_yoy: 8.7, april_release: '2026-06-18' }",
          },
        ],
        rationale:
          "March EI beneficiaries edged up after February's decline, and the April unemployment rate rose to 6.9%. The central estimate nudges higher while keeping most uncertainty within the recent 542,000 to 569,000 range.",
      },
    ],
  },
  {
    seriesId: "statcan.building_permits.total_value_mom",
    country: "CA",
    title: "Canada building permit value growth",
    measure:
      "Monthly change in seasonally adjusted total value of building permits",
    unit: "percent_growth",
    source: "Statistics Canada Building Permits",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Recent building-permit volatility and construction pipeline",
    chainableQuestions: ["next release", "+3 months", "housing supply"],
    whyItMatters:
      "Building permits are an early official signal for housing supply, non-residential investment, construction employment, and property-tax bases.",
    drivers: [
      "Multi-family residential permits",
      "Non-residential project timing",
      "Province-level construction cycles",
      "Interest-rate and financing conditions",
    ],
    history: [
      { label: "Feb", value: -8.4 },
      { label: "Mar", value: 10.3 },
    ],
    historyTool: {
      tool: "statcan.lookup",
      call: 'statcan.lookup({ release: "Building permits", series: "total_value_mom", months: ["2026-02", "2026-03"] })',
      result:
        "{ feb: -8.4, mar: 10.3, mar_residential: -3.3, mar_non_residential: 38.4, apr_release: '2026-06-11 08:30 ET' }",
    },
    targets: [
      {
        slug: "canada-building-permit-value-growth-april-2026",
        title: "Canada building permit value growth, April 2026",
        question:
          "What will Statistics Canada first report as the monthly change in the seasonally adjusted total value of Canadian building permits for April 2026?",
        dataPointId:
          "statcan.building_permits.total_value_mom.canada.april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "April 2026",
        resolutionDate: "2026-06-11",
        resolutionRule:
          "Resolves to the first published monthly percent change in the seasonally adjusted total value of Canadian building permits for April 2026 in Statistics Canada's Building permits release. Later revisions do not change the resolved value.",
        pointEstimate: -2.0,
        ciLow: -16.0,
        ciHigh: 13.0,
        tools: [
          {
            tool: "statcan.lookup",
            call: 'statcan.lookup({ release: "Building permits, March 2026", fields: ["total_value_mom", "residential_mom", "non_residential_mom", "april_release"] })',
            result:
              "{ total_value_mom: 10.3, residential_mom: -3.3, non_residential_mom: 38.4, april_release: '2026-06-11' }",
          },
        ],
        rationale:
          "March's gain was concentrated in volatile non-residential permit values, while residential permits fell. The synthesis expects some mean reversion in April and assigns a wide interval because large projects can dominate the monthly first print.",
      },
    ],
  },
  {
    seriesId: "eurostat.industrial_production.mom",
    country: "EA",
    title: "Euro area industrial production growth",
    measure:
      "Monthly change in calendar and seasonally adjusted industrial production",
    unit: "percent_growth",
    source: "Eurostat Industrial Production",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~6 weeks",
    resolutionPolicy: "first_print",
    benchmark: "Eurostat industrial production trend and member-state prints",
    chainableQuestions: ["next release", "+3 months", "GDP contribution"],
    whyItMatters:
      "Industrial production is a compact euro area output target that captures energy shocks, capital-goods demand, and manufacturing weakness.",
    drivers: [
      "Energy output volatility",
      "Capital goods orders",
      "Country-level production swings",
      "External demand and trade conditions",
    ],
    history: [
      { label: "Jan", value: -0.7 },
      { label: "Feb", value: 0.2 },
      { label: "Mar", value: 0.2 },
    ],
    historyTool: {
      tool: "eurostat.lookup",
      call: 'eurostat.lookup({ release: "Industrial production", series: "euro_area_total_industry_mom", months: ["2026-01", "2026-03"] })',
      result:
        "{ jan: -0.7, feb: 0.2, mar: 0.2, apr_release: '2026-06-15 11:00 CEST' }",
    },
    targets: [
      {
        slug: "euro-area-industrial-production-growth-april-2026",
        title: "Euro area industrial production growth, April 2026",
        question:
          "What will Eurostat first report as the monthly change in euro area industrial production for April 2026?",
        dataPointId:
          "eurostat.industrial_production.euro_area.april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "April 2026",
        resolutionDate: "2026-06-15",
        resolutionRule:
          "Resolves to Eurostat's first estimate of the calendar and seasonally adjusted monthly percent change in total euro area industrial production for April 2026. Later revisions do not change the resolved value.",
        pointEstimate: 0.0,
        ciLow: -1.1,
        ciHigh: 1.2,
        tools: [
          {
            tool: "eurostat.lookup",
            call: 'eurostat.lookup({ release: "Industrial production, March 2026", fields: ["euro_area_mom", "euro_area_yoy", "april_release"] })',
            result:
              "{ euro_area_mom: 0.2, euro_area_yoy: -2.1, apr_release: '2026-06-15' }",
          },
        ],
        rationale:
          "February and March were both mildly positive, but the annual rate remained negative and energy/non-durable components were weak. The forecast centers April near flat, with enough spread for country-level and energy-sector volatility.",
      },
    ],
  },
  {
    seriesId: "eurostat.retail_trade.volume_mom",
    country: "EA",
    title: "Euro area retail trade volume growth",
    measure: "Monthly change in seasonally adjusted retail trade volume",
    unit: "percent_growth",
    source: "Eurostat Retail Trade",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~1 month",
    resolutionPolicy: "first_print",
    benchmark:
      "Eurostat retail trend and inflation-adjusted consumption signals",
    chainableQuestions: ["next release", "+3 months", "household demand"],
    whyItMatters:
      "Retail trade volume gives a fast official read on euro area household consumption while inflation and real-income pressure remain central to policy.",
    drivers: [
      "Real wage growth",
      "Food and fuel volumes",
      "Consumer confidence",
      "Inflation pass-through",
    ],
    history: [
      { label: "Feb", value: 0.3 },
      { label: "Mar", value: -0.1 },
      { label: "Apr", value: -0.4 },
    ],
    historyTool: {
      tool: "eurostat.lookup",
      call: 'eurostat.lookup({ release: "Retail trade", series: "euro_area_volume_mom", months: ["2026-02", "2026-04"] })',
      result:
        "{ feb: 0.3, mar: -0.1, apr: -0.4, may_release: '2026-07-06 11:00 CEST' }",
    },
    targets: [
      {
        slug: "euro-area-retail-trade-volume-growth-may-2026",
        title: "Euro area retail trade volume growth, May 2026",
        question:
          "What will Eurostat first report as the monthly change in euro area retail trade volume for May 2026?",
        dataPointId:
          "eurostat.retail_trade.volume_mom.euro_area.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-07-06",
        resolutionRule:
          "Resolves to Eurostat's first estimate of the seasonally adjusted monthly percent change in euro area retail trade volume for May 2026. Later revisions do not change the resolved value.",
        pointEstimate: 0.1,
        ciLow: -0.7,
        ciHigh: 0.9,
        tools: [
          {
            tool: "eurostat.lookup",
            call: 'eurostat.lookup({ release: "Retail trade, April 2026", fields: ["euro_area_mom", "euro_area_yoy", "may_release"] })',
            result:
              "{ euro_area_mom: -0.4, euro_area_yoy: 1.0, may_release: '2026-07-06' }",
          },
        ],
        rationale:
          "April volume fell 0.4% after a smaller March decline, but the year-over-year rate remained positive. The synthesis expects a mild rebound or stabilization in May rather than a second large decline.",
      },
    ],
  },
  {
    seriesId: "abs.building_approvals.total_dwellings_mom",
    country: "AU",
    title: "Australia dwelling approvals growth",
    measure:
      "Monthly change in seasonally adjusted total dwelling units approved",
    unit: "percent_growth",
    source: "Australian Bureau of Statistics Building Approvals",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~1 month",
    resolutionPolicy: "first_print",
    benchmark:
      "ABS trend dwelling approvals and residential construction pipeline",
    chainableQuestions: ["next release", "+3 months", "housing supply"],
    whyItMatters:
      "Dwelling approvals are a leading indicator for Australian housing supply, construction activity, and affordability pressure.",
    drivers: [
      "Multi-unit approval volatility",
      "Private house approvals",
      "State-level approval cycles",
      "Mortgage-rate and financing conditions",
    ],
    history: [
      { label: "Feb", value: 29.7 },
      { label: "Mar", value: -10.5 },
      { label: "Apr", value: -3.4 },
    ],
    historyTool: {
      tool: "abs.lookup",
      call: 'abs.lookup({ release: "Building Approvals, Australia", series: "total_dwellings_approved_mom", months: ["2026-02", "2026-04"] })',
      result:
        "{ feb: 29.7, mar: -10.5, apr: -3.4, may_release: '2026-07-01 11:30 AEST' }",
    },
    targets: [
      {
        slug: "australia-dwelling-approvals-growth-may-2026",
        title: "Australia dwelling approvals growth, May 2026",
        question:
          "What will the Australian Bureau of Statistics first report as the monthly change in seasonally adjusted total dwelling units approved for May 2026?",
        dataPointId:
          "abs.building_approvals.total_dwellings_mom.australia.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-07-01",
        resolutionRule:
          "Resolves to the first published monthly percent change in seasonally adjusted total dwelling units approved for May 2026 in ABS Building Approvals, Australia. Later revisions do not change the resolved value.",
        pointEstimate: 2.0,
        ciLow: -12.0,
        ciHigh: 18.0,
        tools: [
          {
            tool: "abs.lookup",
            call: 'abs.lookup({ release: "Building Approvals, Australia", fields: ["march_total_dwellings_mom", "april_total_dwellings_mom", "may_release"] })',
            result:
              "{ march_total_dwellings_mom: -10.5, april_total_dwellings_mom: -3.4, may_release: '2026-07-01' }",
          },
        ],
        rationale:
          "Approvals fell in March and April after a large February rise, with multi-unit approvals especially volatile. The forecast expects partial stabilization in May but keeps a wide interval because total dwelling approvals can swing sharply month to month.",
      },
    ],
  },
  {
    seriesId: "statjp.household_spending.real_yoy",
    country: "JP",
    title: "Japan real household spending growth",
    measure:
      "Real year-over-year change in consumption expenditures for two-or-more-person households",
    unit: "percent_growth",
    source: "Statistics Bureau of Japan Family Income and Expenditure Survey",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "~1 month",
    resolutionPolicy: "first_print",
    benchmark: "Recent real consumption expenditure and wage/inflation context",
    chainableQuestions: ["next release", "+3 months", "consumption threshold"],
    whyItMatters:
      "Japan household spending is a direct consumption target for whether wage gains are translating into real demand while food and import prices pressure households.",
    drivers: [
      "Real wage growth",
      "Food and utility prices",
      "Yen import-price pressure",
      "Consumer sentiment",
    ],
    history: [
      { label: "Feb", value: -1.8 },
      { label: "Mar", value: -0.5 },
      { label: "Apr", value: -0.5 },
    ],
    historyTool: {
      tool: "statjp.lookup",
      call: 'statjp.lookup({ release: "Family Income and Expenditure Survey", series: "two_or_more_person_households_real_consumption_expenditure_yoy", months: ["2026-02", "2026-04"] })',
      result: "{ feb: -1.8, mar: -0.5, apr: -0.5, may_release: '2026-07-07' }",
    },
    targets: [
      {
        slug: "japan-real-household-spending-growth-may-2026",
        title: "Japan real household spending growth, May 2026",
        question:
          "What will the Statistics Bureau of Japan first report as the real year-over-year change in consumption expenditures for two-or-more-person households in May 2026?",
        dataPointId:
          "statjp.household_spending.real_yoy.two_or_more_person_households.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-07-07",
        resolutionRule:
          "Resolves to the first published real year-over-year change in consumption expenditures for two-or-more-person households for May 2026 in the Statistics Bureau of Japan Family Income and Expenditure Survey. Later revisions do not change the resolved value.",
        pointEstimate: -0.3,
        ciLow: -2.0,
        ciHigh: 1.4,
        tools: [
          {
            tool: "statjp.lookup",
            call: 'statjp.lookup({ release: "Family Income and Expenditure Survey, April 2026", fields: ["april_nominal_yoy", "april_real_yoy", "workers_household_real_income_yoy", "may_release"] })',
            result:
              "{ april_nominal_yoy: 1.0, april_real_yoy: -0.5, workers_household_real_income_yoy: 2.3, may_release: '2026-07-07' }",
          },
        ],
        rationale:
          "April real spending was still negative despite positive real income for workers' households. The synthesis predicts another slightly negative May print, with upside if wage gains finally lift consumption and downside if food and import-price pressure keep real spending weak.",
      },
    ],
  },
] satisfies Omit<PredictionSeries, "predictionRun">[];

export const GLOBAL_NEAR_TERM_PREDICTION_SERIES =
  GLOBAL_NEAR_TERM_PREDICTION_SERIES_BASE.map((series) => ({
    ...series,
    predictionRun: RECORDED_GLOBAL_NEAR_TERM_RUN,
  })) satisfies PredictionSeries[];

export const GLOBAL_NEAR_TERM_EXAMPLES = buildForecastCellsFromSeries(
  GLOBAL_NEAR_TERM_PREDICTION_SERIES,
);
