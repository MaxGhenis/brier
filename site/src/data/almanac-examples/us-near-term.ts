import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";

const RECORDED_US_NEAR_TERM_RUN: NonNullable<
  PredictionSeries["predictionRun"]
> = {
  kind: "recorded-agent-run",
  runAt: "2026-06-06T23:38:51+02:00",
  agent: "US near-term public outcomes agent",
  model: "Codex recorded agent run",
  sourceContext: [
    "BLS Producer Price Index",
    "BLS Import and Export Price Indexes",
    "Federal Reserve Industrial Production and Capacity Utilization",
    "Census/HUD new residential construction",
    "Census Manufacturing and Trade Inventories and Sales",
    "BEA personal income and outlays",
    "BEA gross domestic product",
    "Treasury Monthly Treasury Statement",
  ],
};

const US_NEAR_TERM_PREDICTION_SERIES_BASE = [
  {
    seriesId: "bls.cpi_u.monthly_change",
    country: "US",
    title: "US CPI-U monthly inflation",
    measure:
      "Consumer Price Index for All Urban Consumers, seasonally adjusted monthly percent change",
    unit: "percent_growth",
    source: "U.S. Bureau of Labor Statistics, Consumer Price Index",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "4 days",
    resolutionPolicy: "first_print",
    benchmark: "Economist consensus and market-implied inflation nowcasts",
    chainableQuestions: ["next release", "+3 months", "core comparison"],
    whyItMatters:
      "CPI is the fastest official inflation read and directly affects policy rates, indexed benefits, tax parameters, and real-income forecasts.",
    drivers: [
      "Gasoline and energy prices",
      "Shelter inflation",
      "Food prices",
      "Vehicle and airfare volatility",
    ],
    history: [
      { label: "Jan", value: 0.2 },
      { label: "Feb", value: 0.3 },
      { label: "Mar", value: 0.9 },
      { label: "Apr", value: 0.6 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ release: "CPI", series: "CPI-U all items, SA", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 0.2, feb: 0.3, mar: 0.9, apr: 0.6, apr_yoy: 3.8, may_release: '2026-06-10 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-cpi-u-mom-may-2026",
        title: "US CPI-U monthly inflation, May 2026",
        question:
          "What will BLS first report as the seasonally adjusted monthly percent change in CPI-U for May 2026?",
        dataPointId: "bls.cpi_u.monthly_change.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-10",
        resolutionRule:
          "Resolves to the first published BLS seasonally adjusted percent change from April 2026 to May 2026 for CPI-U all items. Later revisions or seasonal-factor updates do not change the resolved value.",
        pointEstimate: 0.3,
        ciLow: 0.0,
        ciHigh: 0.7,
        tools: [
          {
            tool: "bls.lookup",
            call: 'bls.lookup({ release: "CPI April 2026", fields: ["all_items_mom", "all_items_yoy", "energy_mom", "gasoline_mom", "next_release"] })',
            result:
              "{ all_items_mom: 0.6, all_items_yoy: 3.8, energy_mom: 3.8, gasoline_mom: 5.4, next_release: '2026-06-10' }",
          },
        ],
        rationale:
          "April's 0.6% increase was energy-heavy, with gasoline and shelter doing much of the work. The estimate fades that impulse while keeping upside risk because energy inflation and shelter remain capable of another above-trend print.",
      },
    ],
  },
  {
    seriesId: "bls.core_cpi.monthly_change",
    country: "US",
    title: "US core CPI monthly inflation",
    measure:
      "CPI-U all items less food and energy, seasonally adjusted monthly percent change",
    unit: "percent_growth",
    source: "U.S. Bureau of Labor Statistics, Consumer Price Index",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "4 days",
    resolutionPolicy: "first_print",
    benchmark: "Economist consensus and Federal Reserve inflation monitoring",
    chainableQuestions: ["next release", "+3 months", "services threshold"],
    whyItMatters:
      "Core CPI is a high-frequency read on underlying inflation pressure, especially shelter and services, before slower PCE and income data resolve.",
    drivers: [
      "Shelter rent indexes",
      "Core services ex shelter",
      "Vehicle prices",
      "Airfares and medical care services",
    ],
    history: [
      { label: "Jan", value: 0.3 },
      { label: "Feb", value: 0.2 },
      { label: "Mar", value: 0.2 },
      { label: "Apr", value: 0.4 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ release: "CPI", series: "all_items_less_food_energy, SA", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 0.3, feb: 0.2, mar: 0.2, apr: 0.4, apr_yoy: 2.8, may_release: '2026-06-10 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-core-cpi-mom-may-2026",
        title: "US core CPI monthly inflation, May 2026",
        question:
          "What will BLS first report as the seasonally adjusted monthly percent change in core CPI for May 2026?",
        dataPointId: "bls.core_cpi.monthly_change.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-10",
        resolutionRule:
          "Resolves to the first published BLS seasonally adjusted percent change from April 2026 to May 2026 for CPI-U all items less food and energy. Later revisions or seasonal-factor updates do not change the resolved value.",
        pointEstimate: 0.3,
        ciLow: 0.1,
        ciHigh: 0.5,
        tools: [
          {
            tool: "bls.lookup",
            call: 'bls.lookup({ release: "CPI April 2026", fields: ["core_mom", "core_yoy", "shelter_mom", "services_less_energy_mom"] })',
            result:
              "{ core_mom: 0.4, core_yoy: 2.8, shelter_mom: 0.6, services_less_energy_mom: 0.5 }",
          },
        ],
        rationale:
          "Core CPI stepped up in April after two 0.2% months, led by shelter and services. The center returns to 0.3% because durable goods are not adding much pressure, but the 80% interval keeps a 0.5% upper tail for another shelter-heavy month.",
      },
    ],
  },
  {
    seriesId: "bls.ppi.final_demand_monthly_change",
    country: "US",
    title: "US PPI final demand monthly inflation",
    measure:
      "Producer Price Index final demand, seasonally adjusted monthly percent change",
    unit: "percent_growth",
    source: "U.S. Bureau of Labor Statistics, Producer Price Index",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "5 days",
    resolutionPolicy: "first_print",
    benchmark: "Economist consensus and CPI/PCE goods-price pass-through",
    chainableQuestions: ["next release", "+3 months", "PCE pass-through"],
    whyItMatters:
      "PPI is a timely input to goods, services, and trade-margin inflation and helps explain the producer side of later PCE price estimates.",
    drivers: [
      "Energy goods prices",
      "Trade-services margins",
      "Transportation and warehousing services",
      "Input-cost pass-through",
    ],
    history: [
      { label: "Feb", value: 0.6 },
      { label: "Mar", value: 0.7 },
      { label: "Apr", value: 1.4 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ release: "PPI", series: "final_demand, SA", months: ["2026-02", "2026-04"] })',
      result:
        "{ feb: 0.6, mar: 0.7, apr: 1.4, apr_yoy: 6.0, may_release: '2026-06-11 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-ppi-final-demand-mom-may-2026",
        title: "US PPI final demand inflation, May 2026",
        question:
          "What will BLS first report as the seasonally adjusted monthly percent change in the PPI final demand index for May 2026?",
        dataPointId: "bls.ppi.final_demand_monthly_change.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-11",
        resolutionRule:
          "Resolves to the first published BLS seasonally adjusted percent change from April 2026 to May 2026 for the PPI final demand index. Later revisions do not change the resolved value.",
        pointEstimate: 0.5,
        ciLow: -0.2,
        ciHigh: 1.3,
        tools: [
          {
            tool: "bls.lookup",
            call: 'bls.lookup({ release: "PPI April 2026", fields: ["final_demand_mom", "goods_mom", "services_mom", "next_release"] })',
            result:
              "{ final_demand_mom: 1.4, goods_mom: 2.0, services_mom: 1.2, next_release: '2026-06-11' }",
          },
        ],
        rationale:
          "April's 1.4% final-demand jump was unusually broad, with goods, energy, and trade margins all elevated. The forecast assumes partial mean reversion but keeps a wide interval because PPI energy and trade-margin components are highly volatile.",
      },
    ],
  },
  {
    seriesId: "dol.initial_claims",
    country: "US",
    title: "US initial unemployment insurance claims",
    measure: "Seasonally adjusted initial claims, advance weekly figure",
    unit: "thousands",
    source: "U.S. Department of Labor, Unemployment Insurance Weekly Claims",
    cadence: "weekly",
    priority: "P0",
    resolutionLatency: "5 days",
    resolutionPolicy: "first_print",
    benchmark: "Claims nowcasts and weekly labor-market monitoring",
    chainableQuestions: ["next release", "+3 months", "continued claims"],
    whyItMatters:
      "Initial claims are the fastest official labor-market stress indicator and connect directly to benefit flows and income-support forecasts.",
    drivers: [
      "Layoff announcements",
      "Seasonal adjustment around holidays",
      "State processing backlogs",
      "Continuing-claims trend",
    ],
    history: [
      { label: "May 16", value: 210 },
      { label: "May 23", value: 212 },
      { label: "May 30", value: 225 },
    ],
    historyTool: {
      tool: "dol.lookup",
      call: 'dol.lookup({ release: "Unemployment Insurance Weekly Claims", weeks_ending: ["2026-05-16", "2026-05-30"] })',
      result:
        "{ may16_initial_claims_sa_thousands: 210, may23_initial_claims_sa_thousands: 212, may30_initial_claims_sa_thousands: 225, may30_4wk_average_thousands: 214.75 }",
    },
    targets: [
      {
        slug: "us-initial-claims-week-ending-2026-06-06",
        title: "US initial unemployment claims, week ending June 6, 2026",
        question:
          "What will DOL first report as seasonally adjusted initial unemployment insurance claims for the week ending June 6, 2026?",
        dataPointId: "dol.initial_claims.week_ending_2026_06_06.first_print",
        horizon: "next_release",
        horizonLabel: "next weekly release",
        periodLabel: "Week ending June 6, 2026",
        resolutionDate: "2026-06-11",
        resolutionRule:
          "Resolves to the advance seasonally adjusted initial claims figure for the week ending June 6, 2026 in the DOL Unemployment Insurance Weekly Claims release. Later revisions do not change the resolved value.",
        pointEstimate: 223,
        ciLow: 204,
        ciHigh: 246,
        tools: [
          {
            tool: "dol.lookup",
            call: 'dol.lookup({ release: "UI Weekly Claims June 4 2026", fields: ["initial_claims_sa", "prior_week_revised", "insured_unemployment_sa"] })',
            result:
              "{ week_ending_may30_initial_claims_sa_thousands: 225, prior_week_revised_thousands: 212, insured_unemployment_sa_thousands: 1777 }",
          },
        ],
        rationale:
          "Claims rose to 225,000 after a low-200,000 run, while insured unemployment stayed near 1.78 million. The estimate holds near the latest print rather than chasing the one-week jump, with a lower tail for seasonal-adjustment reversal.",
      },
    ],
  },
  {
    seriesId: "fed.g17.industrial_production.total_index_mom",
    country: "US",
    title: "US industrial production growth",
    measure: "Industrial production total index monthly percent change",
    unit: "percent_growth",
    source:
      "Federal Reserve Industrial Production and Capacity Utilization - G.17",
    sourceUrl:
      "https://www.federalreserve.gov/releases/g17/current/default.htm",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "8 days",
    resolutionPolicy: "first_print",
    benchmark: "Manufacturing output, utilities weather effects, and ISM data",
    chainableQuestions: ["next release", "+3 months", "manufacturing split"],
    whyItMatters:
      "Industrial production is the fastest official read on goods-sector output, manufacturing capacity pressure, and recession-sensitive activity outside services.",
    drivers: [
      "Manufacturing output and vehicle assemblies",
      "Utilities output and weather",
      "Mining and energy production",
      "Manufacturing survey momentum",
    ],
    history: [
      { label: "Jan", value: 0.0 },
      { label: "Feb", value: 0.6 },
      { label: "Mar", value: -0.3 },
      { label: "Apr", value: 0.7 },
    ],
    historyTool: {
      tool: "fed.g17.lookup",
      call: 'fed.g17.lookup({ release: "Industrial Production and Capacity Utilization", series: "total_index_mom", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 0.0, feb: 0.6, mar: -0.3, apr: 0.7, apr_index: 102.5, apr_yoy: 1.4, may_release: '2026-06-15 09:15 ET' }",
    },
    targets: [
      {
        slug: "us-industrial-production-mom-may-2026",
        title: "US industrial production growth, May 2026",
        question:
          "What will the Federal Reserve first report as the monthly percent change in total U.S. industrial production for May 2026?",
        dataPointId:
          "fed.g17.industrial_production.total_index_mom.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-15",
        resolutionRule:
          "Resolves to the first published monthly percent change in the Federal Reserve G.17 total industrial production index for May 2026. Later revisions and the autumn 2026 annual revision do not change the resolved value.",
        pointEstimate: 0.2,
        ciLow: -0.5,
        ciHigh: 0.9,
        tools: [
          {
            tool: "fed.g17.lookup",
            call: 'fed.g17.lookup({ release: "G.17 April 2026", fields: ["total_ip_mom", "manufacturing_mom", "mining_mom", "utilities_mom", "may_release"] })',
            result:
              "{ total_ip_mom: 0.7, manufacturing_mom: 0.6, mining_mom: -0.1, utilities_mom: 1.9, may_release: '2026-06-15' }",
          },
        ],
        rationale:
          "April's 0.7% gain was helped by manufacturing, motor vehicles, and utilities. The May forecast fades the utilities impulse and keeps the center modestly positive because manufacturing excluding vehicles still grew in April, while mining and survey data keep a meaningful downside tail.",
      },
    ],
  },
  {
    seriesId: "fed.g17.capacity_utilization.total_industry",
    country: "US",
    title: "US total industry capacity utilization",
    measure:
      "Capacity utilization for total industry, percent of capacity, seasonally adjusted",
    unit: "percent",
    source:
      "Federal Reserve Industrial Production and Capacity Utilization - G.17",
    sourceUrl:
      "https://www.federalreserve.gov/releases/g17/current/default.htm",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "8 days",
    resolutionPolicy: "first_print",
    benchmark:
      "Industrial production, manufacturing output, and capacity trend",
    chainableQuestions: ["next release", "+3 months", "manufacturing split"],
    whyItMatters:
      "Capacity utilization measures how much productive slack remains in goods-producing sectors, connecting output pressure to inflation, investment, and labor demand.",
    drivers: [
      "Total industrial production",
      "Manufacturing output and vehicle assemblies",
      "Utilities output and weather",
      "Slow-moving industrial capacity growth",
    ],
    history: [
      { label: "Jan", value: 75.6 },
      { label: "Feb", value: 76.0 },
      { label: "Mar", value: 75.7 },
      { label: "Apr", value: 76.1 },
    ],
    historyTool: {
      tool: "fed.g17.lookup",
      call: 'fed.g17.lookup({ release: "Industrial Production and Capacity Utilization", series: "total_industry_capacity_utilization", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 75.5658, feb: 75.9598, mar: 75.6716, apr: 76.1194, apr_release_rounded: 76.1, may_release: '2026-06-15 09:15 ET' }",
    },
    targets: [
      {
        slug: "us-capacity-utilization-may-2026",
        title: "US capacity utilization, May 2026",
        question:
          "What will the Federal Reserve first report as total U.S. industry capacity utilization for May 2026, seasonally adjusted?",
        dataPointId:
          "fed.g17.capacity_utilization.total_industry.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-15",
        resolutionRule:
          "Resolves to the first published May 2026 value for total industry capacity utilization in the Federal Reserve G.17 release, expressed as percent of capacity and seasonally adjusted. Later revisions and the autumn 2026 annual revision do not change the resolved value.",
        pointEstimate: 76.3,
        ciLow: 75.6,
        ciHigh: 76.9,
        tools: [
          {
            tool: "fed.g17.lookup",
            call: 'fed.g17.lookup({ release: "G.17 April 2026", fields: ["total_capacity_utilization", "total_ip_mom", "manufacturing_mom", "utilities_mom", "may_release"] })',
            result:
              "{ total_capacity_utilization_percent: 76.1194, rounded_release_value: 76.1, total_ip_mom: 0.7, manufacturing_mom: 0.6, utilities_mom: 1.9, may_release: '2026-06-15' }",
          },
          {
            tool: "agent.ensemble",
            call: 'agent.ensemble({ task: "forecast May 2026 total capacity utilization", independent_agents: 2 })',
            result:
              "{ agent_1_point: 76.2, agent_1_p10: 75.5, agent_1_p50: 76.2, agent_1_p90: 76.9, agent_2_point: 76.3, agent_2_p10: 75.7, agent_2_p50: 76.3, agent_2_p90: 76.8, ensemble_point: 76.3 }",
          },
        ],
        rationale:
          "April utilization was 76.1194%, rounded to 76.1% in the release, after total industrial production rose 0.7%. Two independent agent estimates centered at 76.2% and 76.3%; the catalog records the rounded ensemble center of 76.3% while keeping a lower tail for weather-sensitive utilities, vehicles, and mining volatility.",
      },
    ],
  },
  {
    seriesId: "bls.import_price_index.all_imports_mom",
    country: "US",
    title: "US import price inflation",
    measure: "All imports price index monthly percent change",
    unit: "percent_growth",
    source: "U.S. Bureau of Labor Statistics, Import and Export Price Indexes",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "9 days",
    resolutionPolicy: "first_print",
    benchmark: "Fuel import prices, dollar moves, and nonfuel goods prices",
    chainableQuestions: ["next release", "+3 months", "nonfuel split"],
    whyItMatters:
      "Import prices are an early official signal for tradable-goods inflation, tariff pass-through, and foreign-price pressure before CPI and PCE fully absorb it.",
    drivers: [
      "Fuel import prices",
      "Nonfuel industrial supplies",
      "Capital and consumer goods import prices",
      "Exchange-rate pass-through",
    ],
    history: [
      { label: "Jan", value: 0.5 },
      { label: "Feb", value: 1.0 },
      { label: "Mar", value: 0.9 },
      { label: "Apr", value: 1.9 },
    ],
    historyTool: {
      tool: "bls.lookup",
      call: 'bls.lookup({ release: "Import and Export Price Indexes", series: "all_imports_mom", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 0.5, feb: 1.0, mar: 0.9, apr: 1.9, apr_fuel_imports_mom: 16.3, apr_nonfuel_imports_mom: 0.8, may_release: '2026-06-16 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-import-price-index-mom-may-2026",
        title: "US import price inflation, May 2026",
        question:
          "What will BLS first report as the monthly percent change in the U.S. all-import price index for May 2026?",
        dataPointId:
          "bls.import_price_index.all_imports_mom.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-16",
        resolutionRule:
          "Resolves to the first published BLS monthly percent change in the all-import price index for May 2026. Later revisions within the three-month revision window do not change the resolved value.",
        pointEstimate: 0.6,
        ciLow: -0.3,
        ciHigh: 1.5,
        tools: [
          {
            tool: "bls.lookup",
            call: 'bls.lookup({ release: "Import and Export Price Indexes April 2026", fields: ["all_imports_mom", "fuel_imports_mom", "nonfuel_imports_mom", "may_release"] })',
            result:
              "{ all_imports_mom: 1.9, fuel_imports_mom: 16.3, nonfuel_imports_mom: 0.8, may_release: '2026-06-16' }",
          },
        ],
        rationale:
          "April's all-import price increase was fuel-led and unusually hot. The forecast assumes some fuel-price mean reversion but keeps a positive center because nonfuel import prices were also firm and the latest three-month sequence points to broad imported inflation pressure.",
      },
    ],
  },
  {
    seriesId: "census.housing_starts.saar",
    country: "US",
    title: "US housing starts",
    measure: "Privately owned housing starts, seasonally adjusted annual rate",
    unit: "millions",
    source:
      "U.S. Census Bureau and U.S. Department of Housing and Urban Development, New Residential Construction",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "10 days",
    resolutionPolicy: "first_print",
    benchmark: "Housing-starts consensus and permit/backlog indicators",
    chainableQuestions: ["next release", "+3 months", "single-family split"],
    whyItMatters:
      "Housing starts are a fast official read on construction, rates-sensitive investment, and future shelter supply.",
    drivers: [
      "Building permits",
      "Mortgage rates",
      "Builder sentiment",
      "Multifamily project timing",
    ],
    history: [
      { label: "Jan", value: 1.385 },
      { label: "Feb", value: 1.346 },
      { label: "Mar", value: 1.507 },
      { label: "Apr", value: 1.465 },
    ],
    historyTool: {
      tool: "census.lookup",
      call: 'census.lookup({ release: "New Residential Construction", series: "housing_starts_saar", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan: 1.385, feb: 1.346, mar: 1.507, apr: 1.465, may_release: '2026-06-16 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-housing-starts-may-2026",
        title: "US housing starts, May 2026",
        question:
          "What will Census and HUD first report as privately owned housing starts in May 2026, seasonally adjusted annual rate?",
        dataPointId: "census.housing_starts.saar.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-16",
        resolutionRule:
          "Resolves to the first published seasonally adjusted annual rate of privately owned housing starts for May 2026 in the New Residential Construction release. Later revisions do not change the resolved value.",
        pointEstimate: 1.42,
        ciLow: 1.22,
        ciHigh: 1.62,
        tools: [
          {
            tool: "census.lookup",
            call: 'census.lookup({ release: "New Residential Construction April 2026", fields: ["starts_saar", "permits_saar", "next_release"] })',
            result:
              "{ starts_saar_millions: 1.465, permits_saar_millions: 1.442, starts_mom: -2.8, permits_mom: 5.8, next_release: '2026-06-16' }",
          },
        ],
        rationale:
          "Starts fell modestly in April while permits rose, giving mixed short-run signals. The forecast centers slightly below April because mortgage-rate pressure and single-family softness outweigh the permit rebound, but survey noise keeps the band wide.",
      },
    ],
  },
  {
    seriesId: "census.retail_sales.monthly_change",
    country: "US",
    title: "US advance retail and food services sales",
    measure:
      "Advance retail and food services sales, seasonally adjusted monthly percent change",
    unit: "percent_growth",
    source: "U.S. Census Bureau, Advance Monthly Retail Trade Survey",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "11 days",
    resolutionPolicy: "first_print",
    benchmark: "Card-spending trackers and retail-sales consensus",
    chainableQuestions: ["next release", "+3 months", "ex autos and gas"],
    whyItMatters:
      "Advance retail sales are a fast official read on consumer demand before broader personal consumption expenditure data resolve.",
    drivers: [
      "Auto dealer sales",
      "Gasoline-station receipts",
      "Nonstore retail",
      "Food services spending",
    ],
    history: [
      { label: "Feb", value: 2.2 },
      { label: "Mar", value: 1.6 },
      { label: "Apr", value: 0.5 },
    ],
    historyTool: {
      tool: "census.lookup",
      call: 'census.lookup({ release: "Advance Monthly Retail Trade", series: "retail_food_services_mom", months: ["2026-02", "2026-04"] })',
      result:
        "{ feb: 2.2, mar: 1.6, apr: 0.5, apr_sales_billions: 757.1, may_release: '2026-06-17 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-advance-retail-sales-mom-may-2026",
        title: "US advance retail sales, May 2026",
        question:
          "What will Census first report as the monthly percent change in advance retail and food services sales for May 2026?",
        dataPointId: "census.retail_sales.monthly_change.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-17",
        resolutionRule:
          "Resolves to the first published monthly percent change in seasonally adjusted advance retail and food services sales for May 2026. Later revisions do not change the resolved value.",
        pointEstimate: 0.3,
        ciLow: -0.4,
        ciHigh: 0.9,
        tools: [
          {
            tool: "census.lookup",
            call: 'census.lookup({ release: "Advance Monthly Retail Trade April 2026", fields: ["sales", "mom", "prior_month_revision", "next_release"] })',
            result:
              "{ apr_sales_billions: 757.1, apr_mom: 0.5, mar_mom_revised: 1.6, next_release: '2026-06-17' }",
          },
        ],
        rationale:
          "Retail sales slowed from March's revised 1.6% gain to 0.5% in April. The forecast expects continued but cooler nominal spending, with gasoline and autos creating most of the near-term asymmetry.",
      },
    ],
  },
  {
    seriesId: "census.mtis.total_business_inventories_level",
    country: "US",
    title: "US total business inventories",
    measure:
      "Manufacturing and trade inventories, seasonally adjusted end-of-month level",
    unit: "usd_billions",
    source: "U.S. Census Bureau, Manufacturing and Trade Inventories and Sales",
    cadence: "monthly",
    priority: "P1",
    resolutionLatency: "11 days",
    resolutionPolicy: "first_print",
    benchmark: "Advance retail inventories, wholesale inventories, and M3 data",
    chainableQuestions: ["next release", "+3 months", "inventory-sales ratio"],
    whyItMatters:
      "Business inventories connect goods demand, supply-chain buffers, nominal GDP source data, and inventory-cycle pressure on production.",
    drivers: [
      "Retail inventory revisions",
      "Wholesale inventory trend",
      "Manufacturers' inventories",
      "Sales pace and inventory-sales ratio",
    ],
    history: [
      { label: "Feb", value: 2686.3 },
      { label: "Mar", value: 2709.7 },
    ],
    historyTool: {
      tool: "census.lookup",
      call: 'census.lookup({ release: "Manufacturing and Trade Inventories and Sales", series: "total_business_inventories_level", months: ["2026-02", "2026-03"], component_inputs: ["M3 manufacturing", "Advance wholesale", "Advance retail"] })',
      result:
        "{ feb_level_billions: 2686.3, mar_level_billions: 2709.7, mar_inventory_sales_ratio: 1.32, apr_m3_manufacturing_inventories_billions: 959.125, apr_advance_wholesale_inventories_billions: 938.640, apr_advance_retail_inventories_billions: 827.304, apr_release: '2026-06-17 10:00 ET' }",
    },
    targets: [
      {
        slug: "us-total-business-inventories-april-2026",
        title: "US total business inventories, April 2026",
        question:
          "What will Census first report as the seasonally adjusted end-of-month level of U.S. total manufacturing and trade inventories for April 2026?",
        dataPointId:
          "census.mtis.total_business_inventories_level.april_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "April 2026",
        resolutionDate: "2026-06-17",
        resolutionRule:
          "Resolves to the first published preliminary April 2026 value for adjusted total business inventories in Census Manufacturing and Trade Inventories and Sales Table 1, expressed in billions of dollars. Later revisions do not change the resolved value.",
        pointEstimate: 2725.0,
        ciLow: 2716.5,
        ciHigh: 2732.5,
        tools: [
          {
            tool: "census.lookup",
            call: 'census.lookup({ release: "MTIS March 2026 plus April component inputs", fields: ["march_total_business_inventories", "april_manufacturing_inventories", "april_advance_wholesale_inventories", "april_advance_retail_inventories", "april_release"] })',
            result:
              "{ march_total_business_inventories_billions: 2709.734, april_manufacturing_inventories_billions: 959.125, april_advance_wholesale_inventories_billions: 938.640, april_advance_retail_inventories_billions: 827.304, mechanical_sum_billions: 2725.069, april_release: '2026-06-17' }",
          },
        ],
        rationale:
          "The available April component inputs imply a mechanical total near $2,725.1 billion: manufacturing inventories at $959.1 billion, advance wholesale inventories at $938.6 billion, and advance retail inventories at $827.3 billion. The interval mainly allows for wholesale and retail revisions before the MTIS first print.",
      },
    ],
  },
  {
    seriesId: "bea.government_social_benefits.level",
    country: "US",
    title: "US government social benefits to persons",
    measure:
      "Government social benefits to persons, seasonally adjusted annual rate",
    unit: "usd_billions",
    source: "U.S. Bureau of Economic Analysis, Personal Income and Outlays",
    sourceUrl: "https://www.bea.gov/data/income-saving/personal-income",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark:
      "BEA Table 2.6, Treasury outlay timing, and benefit-program caseload trends",
    chainableQuestions: ["next release", "+3 months", "Medicaid split"],
    whyItMatters:
      "Government social benefits are the official monthly income-account counterpart to major transfer programs, making them a direct calibration target for benefit and poverty simulations.",
    drivers: [
      "Social Security benefit level",
      "Medicare and Medicaid payment timing",
      "Unemployment insurance claims and benefit duration",
      "Other government social benefits and program-specific timing",
    ],
    history: [
      { label: "Jan", value: 4994.5 },
      { label: "Feb", value: 4976.2 },
      { label: "Mar", value: 4975.5 },
      { label: "Apr", value: 4984.8 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ dataset: "NIPA Table 2.6", series: "A063RC government social benefits to persons", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_billions_saar: 4994.5, feb_billions_saar: 4976.2, mar_billions_saar: 4975.5, apr_billions_saar: 4984.8, may_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-government-social-benefits-may-2026",
        title: "US government social benefits, May 2026",
        question:
          "What will BEA first report as government social benefits to persons in May 2026, seasonally adjusted annual rate?",
        dataPointId:
          "bea.government_social_benefits.level.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published May 2026 value for government social benefits to persons in BEA NIPA Table 2.6, line 17, converted from millions to billions of current dollars at a seasonally adjusted annual rate. Later revisions do not change the resolved value.",
        pointEstimate: 4997,
        ciLow: 4955,
        ciHigh: 5045,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "Personal Income and Outlays April 2026", table: "NIPA 2.6", line: "Government social benefits to persons", fields: ["jan", "feb", "mar", "apr", "next_release"] })',
            result:
              "{ jan_billions_saar: 4994.5, feb_billions_saar: 4976.2, mar_billions_saar: 4975.5, apr_billions_saar: 4984.8, next_release: '2026-06-25' }",
          },
        ],
        rationale:
          "The series has hovered just below $5.0 trillion SAAR since February, with April at $4,984.8 billion after a small increase from March. The estimate follows the independent benefits-target agent's $4,997 billion center because Social Security and health-program payments continue to trend upward, while the interval allows for payment-timing noise in Medicare, Medicaid, unemployment insurance, and other benefits.",
      },
    ],
  },
  {
    seriesId: "bea.government_social_benefits.social_security",
    country: "US",
    title: "US Social Security benefits in personal income",
    measure:
      "Government social benefits to persons: Social Security, seasonally adjusted annual rate",
    unit: "usd_billions",
    source: "U.S. Bureau of Economic Analysis, Personal Income and Outlays",
    sourceUrl: "https://www.bea.gov/data/income-saving/personal-income",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark:
      "BEA Table 2.6 line 18, SSA benefit rolls, COLA, and Treasury benefit-payment timing",
    chainableQuestions: ["next release", "+3 months", "aggregate benefits"],
    whyItMatters:
      "Social Security is the largest cash-transfer component in personal income, so it anchors retirement-income, poverty, and fiscal calibration forecasts.",
    drivers: [
      "OASDI beneficiary count",
      "Annual COLA already embedded in 2026 checks",
      "Benefit-payment calendar timing",
      "Retirement and disability claiming flow",
    ],
    history: [
      { label: "Jan", value: 1623.2 },
      { label: "Feb", value: 1628.6 },
      { label: "Mar", value: 1636.9 },
      { label: "Apr", value: 1643.7 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ dataset: "NIPA Table 2.6", series: "W823RC Social security", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_billions_saar: 1623.2, feb_billions_saar: 1628.6, mar_billions_saar: 1636.9, apr_billions_saar: 1643.7, may_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-social-security-benefits-may-2026",
        title: "US Social Security benefits, May 2026",
        question:
          "What will BEA first report as Social Security government social benefits to persons in May 2026, seasonally adjusted annual rate?",
        dataPointId:
          "bea.government_social_benefits.social_security.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published May 2026 value for Social Security in BEA NIPA Table 2.6, line 18, converted from millions to billions of current dollars at a seasonally adjusted annual rate. Later revisions do not change the resolved value.",
        pointEstimate: 1650,
        ciLow: 1638,
        ciHigh: 1662,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "Personal Income and Outlays April 2026", table: "NIPA 2.6", line: "Social security", fields: ["jan", "feb", "mar", "apr", "next_release"] })',
            result:
              "{ jan_billions_saar: 1623.2, feb_billions_saar: 1628.6, mar_billions_saar: 1636.9, apr_billions_saar: 1643.7, next_release: '2026-06-25' }",
          },
        ],
        rationale:
          "The line has risen every month in 2026, from $1,623.2 billion SAAR in January to $1,643.7 billion in April. The forecast extends that smooth trend to $1,650 billion, with a narrow interval because Social Security benefit flows are large, regular, and less volatile than health-program payment timing.",
      },
    ],
  },
  {
    seriesId: "bea.government_social_benefits.medicare",
    country: "US",
    title: "US Medicare benefits in personal income",
    measure:
      "Government social benefits to persons: Medicare, seasonally adjusted annual rate",
    unit: "usd_billions",
    source: "U.S. Bureau of Economic Analysis, Personal Income and Outlays",
    sourceUrl: "https://www.bea.gov/data/income-saving/personal-income",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark:
      "BEA Table 2.6 line 19, CMS enrollment, Medicare Advantage payments, and provider payment updates",
    chainableQuestions: ["next release", "+3 months", "aggregate benefits"],
    whyItMatters:
      "Medicare benefit flows are a major public-transfer and health-spending calibration target, connecting beneficiary mix and payment rules to household income accounts.",
    drivers: [
      "Medicare beneficiary count",
      "Medicare Advantage benchmark and rebate payments",
      "Provider payment updates",
      "Prescription-drug and outpatient utilization",
    ],
    history: [
      { label: "Jan", value: 1290.6 },
      { label: "Feb", value: 1301.0 },
      { label: "Mar", value: 1311.4 },
      { label: "Apr", value: 1321.7 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ dataset: "NIPA Table 2.6", series: "W824RC Medicare", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_billions_saar: 1290.6, feb_billions_saar: 1301.0, mar_billions_saar: 1311.4, apr_billions_saar: 1321.7, may_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-medicare-benefits-may-2026",
        title: "US Medicare benefits, May 2026",
        question:
          "What will BEA first report as Medicare government social benefits to persons in May 2026, seasonally adjusted annual rate?",
        dataPointId:
          "bea.government_social_benefits.medicare.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published May 2026 value for Medicare in BEA NIPA Table 2.6, line 19, converted from millions to billions of current dollars at a seasonally adjusted annual rate. Later revisions do not change the resolved value.",
        pointEstimate: 1332,
        ciLow: 1318,
        ciHigh: 1346,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "Personal Income and Outlays April 2026", table: "NIPA 2.6", line: "Medicare", fields: ["jan", "feb", "mar", "apr", "next_release"] })',
            result:
              "{ jan_billions_saar: 1290.6, feb_billions_saar: 1301.0, mar_billions_saar: 1311.4, apr_billions_saar: 1321.7, next_release: '2026-06-25' }",
          },
        ],
        rationale:
          "Medicare has advanced by roughly $10 billion SAAR each month in 2026, ending April at $1,321.7 billion. The forecast extends that trend to $1,332 billion while allowing a wider band than Social Security because health-program claims and plan payments are more timing-sensitive.",
      },
    ],
  },
  {
    seriesId: "bea.government_social_benefits.medicaid",
    country: "US",
    title: "US Medicaid benefits in personal income",
    measure:
      "Government social benefits to persons: Medicaid, seasonally adjusted annual rate",
    unit: "usd_billions",
    source: "U.S. Bureau of Economic Analysis, Personal Income and Outlays",
    sourceUrl: "https://www.bea.gov/data/income-saving/personal-income",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark:
      "BEA Table 2.6 line 20, CMS Medicaid enrollment, FMAP, and state payment timing",
    chainableQuestions: ["next release", "+3 months", "aggregate benefits"],
    whyItMatters:
      "Medicaid is the cleanest near-term BEA bridge from public benefit rules and enrollment operations into official household income accounts.",
    drivers: [
      "Medicaid and CHIP enrollment trend",
      "FMAP and state payment timing",
      "Managed-care capitation payments",
      "Post-unwinding caseload normalization",
    ],
    history: [
      { label: "Jan", value: 1050.4 },
      { label: "Feb", value: 1049.6 },
      { label: "Mar", value: 1045.8 },
      { label: "Apr", value: 1039.0 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ dataset: "NIPA Table 2.6", series: "W729RC Medicaid", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_billions_saar: 1050.4, feb_billions_saar: 1049.6, mar_billions_saar: 1045.8, apr_billions_saar: 1039.0, may_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-medicaid-benefits-may-2026",
        title: "US Medicaid benefits, May 2026",
        question:
          "What will BEA first report as Medicaid government social benefits to persons in May 2026, seasonally adjusted annual rate?",
        dataPointId:
          "bea.government_social_benefits.medicaid.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published May 2026 value for Medicaid in BEA NIPA Table 2.6, line 20, converted from millions to billions of current dollars at a seasonally adjusted annual rate. Later revisions do not change the resolved value.",
        pointEstimate: 1041,
        ciLow: 1029,
        ciHigh: 1057,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "Personal Income and Outlays April 2026", table: "NIPA 2.6", line: "Medicaid", fields: ["jan", "feb", "mar", "apr", "next_release"] })',
            result:
              "{ jan_billions_saar: 1050.4, feb_billions_saar: 1049.6, mar_billions_saar: 1045.8, apr_billions_saar: 1039.0, next_release: '2026-06-25' }",
          },
          {
            tool: "agent.ensemble",
            call: 'agent.ensemble({ task: "forecast May 2026 BEA Medicaid benefits", independent_agents: 2 })',
            result:
              "{ agent_1_point: 1039.5, agent_1_p10: 1029.0, agent_1_p25: 1034.0, agent_1_p50: 1039.5, agent_1_p75: 1045.0, agent_1_p90: 1053.0, agent_2_point: 1042.0, agent_2_p10: 1029.0, agent_2_p50: 1042.0, agent_2_p90: 1057.0, ensemble_point: 1041.0 }",
          },
        ],
        rationale:
          "Medicaid benefits declined from $1,050.4 billion SAAR in January to $1,039.0 billion in April, consistent with continued post-unwinding normalization and payment-timing noise. Two independent agents centered May at $1,039.5 billion and $1,042.0 billion; the catalog records the rounded ensemble center of $1,041 billion with a combined $1,029-$1,057 billion 80% interval.",
      },
    ],
  },
  {
    seriesId: "bea.wages_and_salaries.level",
    country: "US",
    title: "US wages and salaries in personal income",
    measure: "Wages and salaries, seasonally adjusted annual rate",
    unit: "usd_billions",
    source: "U.S. Bureau of Economic Analysis, Personal Income and Outlays",
    sourceUrl: "https://www.bea.gov/data/income-saving/personal-income",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark:
      "BEA Table 2.6 line 3, BLS payroll employment, average hourly earnings, and hours",
    chainableQuestions: ["next release", "+3 months", "tax receipts bridge"],
    whyItMatters:
      "Wages and salaries are the main labor-income bridge between payroll data, tax receipts, benefit eligibility, and household disposable-income forecasts.",
    drivers: [
      "Nonfarm payroll employment",
      "Average hourly earnings",
      "Aggregate weekly hours",
      "Industry mix and bonus timing",
    ],
    history: [
      { label: "Jan", value: 13214.7 },
      { label: "Feb", value: 13231.5 },
      { label: "Mar", value: 13278.7 },
      { label: "Apr", value: 13311.1 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ dataset: "NIPA Table 2.6", series: "A034RC wages and salaries", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_billions_saar: 13214.7, feb_billions_saar: 13231.5, mar_billions_saar: 13278.7, apr_billions_saar: 13311.1, may_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-wages-and-salaries-may-2026",
        title: "US wages and salaries, May 2026",
        question:
          "What will BEA first report as wages and salaries in May 2026, seasonally adjusted annual rate?",
        dataPointId: "bea.wages_and_salaries.level.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published May 2026 value for wages and salaries in BEA NIPA Table 2.6, line 3, converted from millions to billions of current dollars at a seasonally adjusted annual rate. Later revisions do not change the resolved value.",
        pointEstimate: 13350,
        ciLow: 13300,
        ciHigh: 13405,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "Personal Income and Outlays April 2026", table: "NIPA 2.6", line: "Wages and salaries", fields: ["jan", "feb", "mar", "apr", "next_release"] })',
            result:
              "{ jan_billions_saar: 13214.7, feb_billions_saar: 13231.5, mar_billions_saar: 13278.7, apr_billions_saar: 13311.1, next_release: '2026-06-25' }",
          },
          {
            tool: "bls.lookup",
            call: 'bls.lookup({ release: "Employment Situation May 2026", fields: ["payroll_change", "average_hourly_earnings_mom"] })',
            result:
              "{ payroll_change_thousands: 172, average_hourly_earnings_mom: 0.3 }",
          },
        ],
        rationale:
          "Wages and salaries rose steadily through April, and the resolved May payroll report showed 172,000 additional jobs with average hourly earnings up 0.3%. The forecast extends the recent trend to $13,350 billion SAAR while allowing downside from hours or composition and upside from stronger aggregate payroll income.",
      },
    ],
  },
  {
    seriesId: "bea.personal_current_taxes.level",
    country: "US",
    title: "US personal current taxes",
    measure: "Personal current taxes, seasonally adjusted annual rate",
    unit: "usd_billions",
    source: "U.S. Bureau of Economic Analysis, Personal Income and Outlays",
    sourceUrl: "https://www.bea.gov/data/income-saving/personal-income",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark:
      "BEA Table 2.6 line 26, Treasury individual receipts, payroll income, and withheld-tax timing",
    chainableQuestions: [
      "next release",
      "+3 months",
      "disposable-income bridge",
    ],
    whyItMatters:
      "Personal current taxes are the official monthly household-tax line, connecting income growth and withholding to disposable-income and fiscal forecasts.",
    drivers: [
      "Withheld individual income taxes",
      "Payroll-taxable wage base",
      "Nonwithheld tax-payment timing",
      "Tax refund and settlement timing",
    ],
    history: [
      { label: "Jan", value: 3214.2 },
      { label: "Feb", value: 3215.8 },
      { label: "Mar", value: 3230.4 },
      { label: "Apr", value: 3250.3 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ dataset: "NIPA Table 2.6", series: "W055RC personal current taxes", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_billions_saar: 3214.2, feb_billions_saar: 3215.8, mar_billions_saar: 3230.4, apr_billions_saar: 3250.3, may_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-personal-current-taxes-may-2026",
        title: "US personal current taxes, May 2026",
        question:
          "What will BEA first report as personal current taxes in May 2026, seasonally adjusted annual rate?",
        dataPointId: "bea.personal_current_taxes.level.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published May 2026 value for less personal current taxes in BEA NIPA Table 2.6, line 26, converted from millions to billions of current dollars at a seasonally adjusted annual rate. Later revisions do not change the resolved value.",
        pointEstimate: 3266.8,
        ciLow: 3247.5,
        ciHigh: 3301,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "Personal Income and Outlays April 2026", table: "NIPA 2.6", line: "Less: Personal current taxes", fields: ["jan", "feb", "mar", "apr", "next_release"] })',
            result:
              "{ jan_billions_saar: 3214.2, feb_billions_saar: 3215.8, mar_billions_saar: 3230.4, apr_billions_saar: 3250.3, next_release: '2026-06-25' }",
          },
          {
            tool: "agent.ensemble",
            call: 'agent.ensemble({ task: "forecast May 2026 BEA personal current taxes", independent_agents: 2 })',
            result:
              "{ completed_agents: 2, point_estimates_billions_saar: [3266.5, 3267.0], ensemble_point_billions_saar: 3266.8, ensemble_interval80_billions_saar: [3247.5, 3301], agent_quantiles: [{ p05: 3239, p10: 3248, p25: 3258.5, p50: 3266.5, p75: 3277, p90: 3292, p95: 3305 }, { p10: 3247, p25: 3257, p50: 3266, p75: 3284, p90: 3305 }] }",
          },
        ],
        rationale:
          "Two independent agents centered near $3,267 billion SAAR after comparing April's $3,250.3 billion first-print level with recent April-to-May tax increments, Jan-Apr year-over-year growth, and the resolved May payroll report. The ensemble keeps a wider right tail for withholding, refund, and nonwithheld-payment timing around the first BEA estimate.",
      },
    ],
  },
  {
    seriesId: "bea.disposable_personal_income.level",
    country: "US",
    title: "US disposable personal income",
    measure: "Disposable personal income, seasonally adjusted annual rate",
    unit: "usd_billions",
    source: "U.S. Bureau of Economic Analysis, Personal Income and Outlays",
    sourceUrl: "https://www.bea.gov/data/income-saving/personal-income",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark:
      "BEA Table 2.6 line 27, personal income, taxes, wages, and government transfers",
    chainableQuestions: ["next release", "+3 months", "real DPI comparison"],
    whyItMatters:
      "Disposable personal income is the official after-tax household income line, directly connecting labor income, taxes, transfers, inflation, and consumption capacity.",
    drivers: [
      "Wages and salaries",
      "Government social benefits",
      "Personal current taxes",
      "Interest, dividend, and proprietors' income",
    ],
    history: [
      { label: "Jan", value: 23389.2 },
      { label: "Feb", value: 23374.6 },
      { label: "Mar", value: 23492.1 },
      { label: "Apr", value: 23472.2 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ dataset: "NIPA Table 2.6", series: "A067RC disposable personal income", months: ["2026-01", "2026-04"] })',
      result:
        "{ jan_billions_saar: 23389.2, feb_billions_saar: 23374.6, mar_billions_saar: 23492.1, apr_billions_saar: 23472.2, apr_percent_change: -0.1, may_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-disposable-personal-income-may-2026",
        title: "US disposable personal income, May 2026",
        question:
          "What will BEA first report as disposable personal income in May 2026, seasonally adjusted annual rate?",
        dataPointId:
          "bea.disposable_personal_income.level.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published May 2026 value for disposable personal income in BEA NIPA Table 2.6, line 27, converted from millions to billions of current dollars at a seasonally adjusted annual rate. Later revisions do not change the resolved value.",
        pointEstimate: 23512,
        ciLow: 23445,
        ciHigh: 23615,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "Personal Income and Outlays April 2026", table: "NIPA 2.6", line: "Disposable personal income", fields: ["jan", "feb", "mar", "apr", "next_release"] })',
            result:
              "{ jan_billions_saar: 23389.2, feb_billions_saar: 23374.6, mar_billions_saar: 23492.1, apr_billions_saar: 23472.2, next_release: '2026-06-25' }",
          },
        ],
        rationale:
          "April disposable personal income slipped to $23,472.2 billion SAAR after March's jump. The May forecast moves back above April because wages, Social Security, and Medicare benefits are expected to rise, partly offset by higher personal current taxes.",
      },
    ],
  },
  {
    seriesId: "bea.pce_price_index.monthly_change",
    country: "US",
    title: "US PCE price index monthly inflation",
    measure: "PCE price index monthly percent change",
    unit: "percent_growth",
    source: "U.S. Bureau of Economic Analysis, Personal Income and Outlays",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark: "CPI/PPI mapping and Federal Reserve inflation monitoring",
    chainableQuestions: ["next release", "+3 months", "core PCE"],
    whyItMatters:
      "The PCE price index is the Federal Reserve's preferred inflation gauge and bridges CPI, PPI, and income-spending data.",
    drivers: [
      "CPI source data",
      "PPI services components",
      "Health care and financial-services imputations",
      "Energy and food prices",
    ],
    history: [
      { label: "Mar", value: 0.7 },
      { label: "Apr", value: 0.4 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ release: "Personal Income and Outlays", series: "PCE price index monthly percent change", months: ["2026-03", "2026-04"] })',
      result:
        "{ mar: 0.7, apr: 0.4, apr_yoy: 3.8, may_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-pce-price-index-mom-may-2026",
        title: "US PCE price index inflation, May 2026",
        question:
          "What will BEA first report as the monthly percent change in the PCE price index for May 2026?",
        dataPointId: "bea.pce_price_index.monthly_change.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published BEA monthly percent change in the PCE price index for May 2026 in the Personal Income and Outlays release. Later revisions do not change the resolved value.",
        pointEstimate: 0.3,
        ciLow: 0.1,
        ciHigh: 0.6,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "Personal Income and Outlays April 2026", fields: ["pce_price_mom", "core_pce_price_mom", "pce_price_yoy", "next_release"] })',
            result:
              "{ pce_price_mom: 0.4, core_pce_price_mom: 0.2, pce_price_yoy: 3.8, next_release: '2026-06-25' }",
          },
        ],
        rationale:
          "April's headline PCE inflation was hotter than core PCE, consistent with energy and goods pressure. The May estimate uses expected CPI/PPI moderation but keeps the upper tail because PCE source data can preserve some energy and services pass-through.",
      },
    ],
  },
  {
    seriesId: "bea.real_gdp.saar",
    country: "US",
    title: "US real GDP growth",
    measure: "Real GDP percent change, seasonally adjusted annual rate",
    unit: "percent_growth",
    source: "U.S. Bureau of Economic Analysis, Gross Domestic Product",
    cadence: "quarterly",
    priority: "P0",
    resolutionLatency: "19 days",
    resolutionPolicy: "first_print",
    benchmark: "BEA second estimate, source-data revisions, and GDP nowcasts",
    chainableQuestions: ["next release", "+3 months", "GDI comparison"],
    whyItMatters:
      "GDP is the headline official output measure and anchors fiscal receipts, benefit demand, labor-market pressure, and monetary-policy forecasts.",
    drivers: [
      "Consumer spending revisions",
      "Inventory investment",
      "Net exports",
      "Government spending",
    ],
    history: [
      { label: "2025 Q4", value: 0.5 },
      { label: "Q1 adv", value: 2.0 },
      { label: "Q1 2nd", value: 1.6 },
    ],
    historyTool: {
      tool: "bea.lookup",
      call: 'bea.lookup({ release: "GDP", series: "real_gdp_saar", vintages: ["2025-Q4", "2026-Q1 advance", "2026-Q1 second"] })',
      result:
        "{ q4_2025: 0.5, q1_2026_advance: 2.0, q1_2026_second: 1.6, q1_third_release: '2026-06-25 08:30 ET' }",
    },
    targets: [
      {
        slug: "us-real-gdp-q1-2026-third-estimate",
        title: "US real GDP growth, Q1 2026 third estimate",
        question:
          "What will BEA first report as real GDP growth in the third estimate for Q1 2026, seasonally adjusted annual rate?",
        dataPointId: "bea.real_gdp.saar.q1_2026.third_estimate",
        horizon: "next_release",
        horizonLabel: "third estimate",
        periodLabel: "Q1 2026",
        resolutionDate: "2026-06-25",
        resolutionRule:
          "Resolves to the first published BEA third estimate of real GDP percent change for Q1 2026, seasonally adjusted annual rate. Later annual-update or benchmark revisions do not change the resolved value.",
        pointEstimate: 1.5,
        ciLow: 1.1,
        ciHigh: 1.9,
        tools: [
          {
            tool: "bea.lookup",
            call: 'bea.lookup({ release: "GDP second estimate Q1 2026", fields: ["real_gdp", "advance_real_gdp", "revision_reason", "next_release"] })',
            result:
              "{ real_gdp_second_estimate: 1.6, advance_real_gdp: 2.0, revision: -0.4, next_release: '2026-06-25' }",
          },
        ],
        rationale:
          "The second estimate already revised Q1 growth down by 0.4 percentage point, mainly from investment and consumer-spending source data. Third estimates usually move less, so the forecast centers just below 1.6% with a tight but nontrivial revision band.",
      },
    ],
  },
  {
    seriesId: "treasury.mts.monthly_deficit",
    country: "US",
    title: "US federal monthly deficit",
    measure:
      "Monthly Treasury Statement deficit, positive for deficit and negative for surplus",
    unit: "usd_billions",
    source:
      "U.S. Treasury Bureau of the Fiscal Service, Monthly Treasury Statement",
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "4 days",
    resolutionPolicy: "first_print",
    benchmark: "Daily Treasury Statement and prior-year MTS seasonality",
    chainableQuestions: ["next release", "+3 months", "outlay category split"],
    whyItMatters:
      "The Monthly Treasury Statement is the official cash-flow ledger for federal receipts, outlays, and deficit timing, which makes it a direct policy-cost calibration target.",
    drivers: [
      "Individual income tax receipts",
      "Refund timing",
      "Social Security and Medicare outlays",
      "Debt-interest payments",
    ],
    history: [
      { label: "Jan", value: 94.6 },
      { label: "Feb", value: 307.5 },
      { label: "Mar", value: 164.1 },
      { label: "Apr", value: -215.0 },
      { label: "May 2025", value: 315.7 },
    ],
    historyTool: {
      tool: "treasury.lookup",
      call: 'treasury.lookup({ dataset: "Monthly Treasury Statement table 1", series: "current_month_deficit_surplus", fiscal_year: 2026, months: ["2026-01", "2026-04"], prior_year_month: "2025-05" })',
      result:
        "{ jan2026: 94.6, feb2026: 307.5, mar2026: 164.1, apr2026: -215.0, may2025: 315.7, mts_release_rule: '8th business day after month end' }",
    },
    targets: [
      {
        slug: "us-mts-deficit-may-2026",
        title: "US federal monthly deficit, May 2026",
        question:
          "What will Treasury first report as the federal deficit or surplus for May 2026 in the Monthly Treasury Statement?",
        dataPointId: "treasury.mts.monthly_deficit.may_2026.first_print",
        horizon: "next_release",
        horizonLabel: "next release",
        periodLabel: "May 2026",
        resolutionDate: "2026-06-10",
        resolutionRule:
          "Resolves to the May 2026 current-month deficit/surplus amount in Monthly Treasury Statement table 1, divided by 1 billion dollars, with deficits positive and surpluses negative. The first published MTS table governs.",
        pointEstimate: 305,
        ciLow: 240,
        ciHigh: 380,
        tools: [
          {
            tool: "treasury.lookup",
            call: 'treasury.lookup({ dataset: "FiscalData MTS table 1", record_date: "2026-04-30", lines: ["FY2026 Jan-Apr", "FY2025 May"] })',
            result:
              "{ fy2026_ytd_through_apr_deficit_billions: 953.6, apr2026_surplus_billions: 215.0, may2025_deficit_billions: 315.7 }",
          },
        ],
        rationale:
          "April is tax-season surplus month; May usually returns to a large deficit. FY2026 was running below the FY2025 deficit path through April, so the center is slightly below May 2025 while preserving upside for benefit, Medicare, and interest-payment timing.",
      },
    ],
  },
] satisfies Omit<PredictionSeries, "predictionRun">[];

const INCLUDED_US_NEAR_TERM_SERIES_IDS = new Set<string>([
  "bls.ppi.final_demand_monthly_change",
  "fed.g17.industrial_production.total_index_mom",
  "fed.g17.capacity_utilization.total_industry",
  "bls.import_price_index.all_imports_mom",
  "census.housing_starts.saar",
  "census.mtis.total_business_inventories_level",
  "bea.pce_price_index.monthly_change",
  "bea.real_gdp.saar",
  "bea.government_social_benefits.level",
  "bea.government_social_benefits.social_security",
  "bea.government_social_benefits.medicare",
  "bea.government_social_benefits.medicaid",
  "bea.wages_and_salaries.level",
  "bea.personal_current_taxes.level",
  "bea.disposable_personal_income.level",
  "treasury.mts.monthly_deficit",
]);

export const US_NEAR_TERM_PREDICTION_SERIES =
  US_NEAR_TERM_PREDICTION_SERIES_BASE.filter((series) =>
    INCLUDED_US_NEAR_TERM_SERIES_IDS.has(series.seriesId),
  ).map((series) => ({
    ...series,
    predictionRun: RECORDED_US_NEAR_TERM_RUN,
  })) satisfies PredictionSeries[];

export const US_NEAR_TERM_EXAMPLES = buildForecastCellsFromSeries(
  US_NEAR_TERM_PREDICTION_SERIES,
);
