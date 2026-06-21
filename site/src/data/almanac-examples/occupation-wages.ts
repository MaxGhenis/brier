import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";
import { requireLedgerTarget } from "../ledger-targets";
import type {
  ForecastCell,
  ForecastComparisonRun,
  PredictionPackSet,
} from "../forecast-cells";

const OCCUPATION_WAGE_NO_PACK_SET = {
  packSetId: "pack_set.occupation_wage_pressure_control.v1",
  label: "Occupation wage pressure control",
  mode: "none",
  packs: [],
  notes:
    "Control run using OEWS wage context and broad nominal wage-pressure signals without a BLS occupational wage projection pack.",
} satisfies PredictionPackSet;

const RECORDED_OCCUPATION_WAGE_RUN = {
  kind: "recorded-agent-run",
  runAt: "2026-06-21T13:35:00-04:00",
  agent: "brier-occupation-wage-pressure",
  model: "Codex recorded source-context synthesis",
  sourceContext: [
    "BLS OEWS May 2025 national annual median wage table",
    "BLS OEWS time-series API annual median wage datatype",
    "Employment Cost Index and average hourly earnings context",
    "SOC major occupational groups",
    "Task automation exposure literature",
  ],
  runLabel: "Occupation wage pressure - no projection pack",
  runDescription:
    "Control run over May 2026 OEWS median annual wages. BLS publishes current occupational wages but does not publish an official 2026 occupational wage projection.",
  packSet: OCCUPATION_WAGE_NO_PACK_SET,
} satisfies PredictionSeries["predictionRun"];

interface OccupationWageDefinition {
  socCode: string;
  slug: string;
  title: string;
  question: string;
  measure: string;
  whyItMatters: string;
  drivers: string[];
  latestMedianAnnualWage: number;
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  wageSignalResult: string;
  rationale: string;
}

const OCCUPATION_WAGE_DEFINITIONS: OccupationWageDefinition[] = [
  {
    socCode: "13-0000",
    slug: "oews-business-financial-median-wage-may-2026",
    title: "Business and financial median wage, May 2026",
    question:
      "What annual median wage will BLS first publish for SOC 13-0000 Business and Financial Operations Occupations in the May 2026 national OEWS release?",
    measure:
      "National annual median wage for business and financial operations occupations",
    whyItMatters:
      "This is a wage-side companion to the white-collar employment target: AI may compress routine analyst, compliance, bookkeeping, and claims work while leaving a higher-skill occupational mix.",
    drivers: [
      "Nominal wage growth",
      "Professional-services labor demand",
      "Finance and compliance skill mix",
      "AI-assisted back-office productivity",
    ],
    latestMedianAnnualWage: 82660,
    pointEstimate: 85800,
    ciLow: 82500,
    ciHigh: 89200,
    wageSignalResult:
      "{ base_median_wage_2025_usd: 82660, nominal_growth_assumption: 'about_3.8_percent', composition: 'higher_skill_mix_supports_median' }",
    rationale:
      "The point applies moderate nominal wage growth to the May 2025 OEWS median and allows a small positive mix effect from continued demand for analysts, compliance workers, and project management specialists. The lower tail covers weaker professional hiring and lower bonus-sensitive finance demand.",
  },
  {
    socCode: "15-0000",
    slug: "oews-computer-math-median-wage-may-2026",
    title: "Computer and mathematical median wage, May 2026",
    question:
      "What annual median wage will BLS first publish for SOC 15-0000 Computer and Mathematical Occupations in the May 2026 national OEWS release?",
    measure:
      "National annual median wage for computer and mathematical occupations",
    whyItMatters:
      "This is the cleanest wage target for whether AI tools are mainly labor-saving in software tasks or demand-expanding through AI infrastructure, security, data, and integration work.",
    drivers: [
      "Software labor demand",
      "AI infrastructure and security hiring",
      "Coding-assistant productivity",
      "Tech-sector pay normalization",
    ],
    latestMedianAnnualWage: 109280,
    pointEstimate: 112900,
    ciLow: 108600,
    ciHigh: 117800,
    wageSignalResult:
      "{ base_median_wage_2025_usd: 109280, nominal_growth_assumption: 'about_3.3_percent', demand_channel: 'ai_infrastructure_and_security', substitution_channel: 'coding_task_productivity' }",
    rationale:
      "The median should keep rising, but not at a breakout rate: AI demand, cloud infrastructure, and cybersecurity support the upper half of the distribution, while normalized tech hiring and coding-assistant productivity hold down the central wage path.",
  },
  {
    socCode: "31-0000",
    slug: "oews-healthcare-support-median-wage-may-2026",
    title: "Healthcare support median wage, May 2026",
    question:
      "What annual median wage will BLS first publish for SOC 31-0000 Healthcare Support Occupations in the May 2026 national OEWS release?",
    measure: "National annual median wage for healthcare support occupations",
    whyItMatters:
      "Healthcare support gives Thesis a low-wage, low-substitution wage target where staffing scarcity and minimum-wage pressure can matter more than software substitution.",
    drivers: [
      "Care staffing shortages",
      "Medicaid and Medicare utilization",
      "Low-wage service wage floor",
      "Limited physical-task automation",
    ],
    latestMedianAnnualWage: 38340,
    pointEstimate: 40100,
    ciLow: 38500,
    ciHigh: 41900,
    wageSignalResult:
      "{ base_median_wage_2025_usd: 38340, nominal_growth_assumption: 'about_4.6_percent', staffing_pressure: 'high', automation_substitution: 'low' }",
    rationale:
      "Healthcare support gets a faster median-wage update than most groups because care demand remains strong and low-wage service jobs face recruitment pressure. The lower tail reflects provider margin constraints and state-level Medicaid funding pressure.",
  },
  {
    socCode: "43-0000",
    slug: "oews-office-admin-median-wage-may-2026",
    title: "Office and administrative support median wage, May 2026",
    question:
      "What annual median wage will BLS first publish for SOC 43-0000 Office and Administrative Support Occupations in the May 2026 national OEWS release?",
    measure:
      "National annual median wage for office and administrative support occupations",
    whyItMatters:
      "Office and administrative support is the wage counterpart to the clearest clerical automation employment target, so it helps separate headcount decline from composition and wage-pressure effects.",
    drivers: [
      "Clerical automation",
      "Service-sector administrative demand",
      "Occupational composition",
      "Nominal wage growth",
    ],
    latestMedianAnnualWage: 47450,
    pointEstimate: 49000,
    ciLow: 47100,
    ciHigh: 51100,
    wageSignalResult:
      "{ base_median_wage_2025_usd: 47450, nominal_growth_assumption: 'about_3.3_percent', composition: 'routine_low_wage_roles_shrink_first' }",
    rationale:
      "The median rises even with declining clerical employment because nominal wage growth and composition can offset weaker headcount. If automation mainly removes lower-paid routine roles, the median wage can rise faster than the occupation group's employment path would suggest.",
  },
  {
    socCode: "51-0000",
    slug: "oews-production-median-wage-may-2026",
    title: "Production median wage, May 2026",
    question:
      "What annual median wage will BLS first publish for SOC 51-0000 Production Occupations in the May 2026 national OEWS release?",
    measure: "National annual median wage for production occupations",
    whyItMatters:
      "Production wages connect automation to manufacturing labor demand, robotics, reshoring, union contracts, and goods-sector cyclicality rather than only information-work substitution.",
    drivers: [
      "Manufacturing labor demand",
      "Union and shortage wage pressure",
      "Factory automation",
      "Goods-sector cycle",
    ],
    latestMedianAnnualWage: 46990,
    pointEstimate: 48700,
    ciLow: 46700,
    ciHigh: 50900,
    wageSignalResult:
      "{ base_median_wage_2025_usd: 46990, nominal_growth_assumption: 'about_3.6_percent', automation_channel: 'process_control_and_robotics', labor_market: 'tight_skilled_trades' }",
    rationale:
      "The central case is moderate nominal wage growth. Automation and mixed manufacturing demand limit upside, but shortages in skilled production roles and existing wage contracts keep the median from being a simple flat carry-forward.",
  },
  {
    socCode: "53-0000",
    slug: "oews-transport-material-moving-median-wage-may-2026",
    title: "Transportation and material moving median wage, May 2026",
    question:
      "What annual median wage will BLS first publish for SOC 53-0000 Transportation and Material Moving Occupations in the May 2026 national OEWS release?",
    measure:
      "National annual median wage for transportation and material moving occupations",
    whyItMatters:
      "This wage target tracks logistics, warehousing, driving, routing, and material movement where automation can change task mix before full autonomy changes employment.",
    drivers: [
      "Warehouse and logistics demand",
      "Routing and warehouse automation",
      "Driver wage pressure",
      "Goods movement volume",
    ],
    latestMedianAnnualWage: 44350,
    pointEstimate: 45900,
    ciLow: 44000,
    ciHigh: 48000,
    wageSignalResult:
      "{ base_median_wage_2025_usd: 44350, nominal_growth_assumption: 'about_3.5_percent', logistics_demand: 'positive', automation_channel: 'warehouse_and_routing' }",
    rationale:
      "Logistics wage growth should remain positive but not explosive. Warehouse automation and routing tools offset some labor scarcity, while driver and material-moving demand keep the median above the 2025 OEWS level.",
  },
];

function oewsWageDataPointId(socCode: string): string {
  return `bls.oews.national_occupation_median_annual_wage.soc_${socCode.replace("-", "_")}.may_2026.first_print`;
}

function oewsAnnualMedianWageSeriesId(socCode: string): string {
  return `OEUN0000000000000${socCode.replace("-", "")}13`;
}

function occupationWageSeriesFor(
  definition: OccupationWageDefinition,
): PredictionSeries {
  const target = requireLedgerTarget(oewsWageDataPointId(definition.socCode));
  const seriesId = oewsAnnualMedianWageSeriesId(definition.socCode);

  return {
    seriesId: target.dataPointId.replace(".may_2026.first_print", ""),
    title: definition.title,
    measure: definition.measure,
    unit: target.unit,
    source: target.source,
    sourceUrl: target.sourceUrl,
    cadence: "annual",
    priority: "P1",
    resolutionLatency: "~12 months",
    resolutionPolicy: target.resolutionPolicy,
    benchmark:
      "May 2025 OEWS national annual median wage plus nominal wage-growth and composition priors",
    chainableQuestions: [
      "next annual release",
      "mean wage",
      "percentile wages",
      "detailed SOC rows",
    ],
    whyItMatters: definition.whyItMatters,
    drivers: definition.drivers,
    history: [
      {
        label: "May 2025 OEWS median",
        value: definition.latestMedianAnnualWage,
      },
    ],
    historyTool: {
      tool: "bls.oews.api",
      call: `bls.oews.api({ seriesId: "${seriesId}", release: "May 2025", datatype: "Annual median wage" })`,
      result: `{ series_id: '${seriesId}', year: 2025, period: 'A01', annual_median_wage_usd: ${definition.latestMedianAnnualWage} }`,
    },
    predictionRun: RECORDED_OCCUPATION_WAGE_RUN,
    targets: [
      {
        slug: definition.slug,
        title: definition.title,
        question: definition.question,
        dataPointId: target.dataPointId,
        horizon: "next_release",
        horizonLabel: "May 2026 OEWS first print",
        periodLabel: target.periodLabel,
        resolutionDate: target.resolutionDate,
        resolutionRule: target.resolutionRule,
        resolutionSourceUrl: target.resolutionSourceUrl,
        pointEstimate: definition.pointEstimate,
        ciLow: definition.ciLow,
        ciHigh: definition.ciHigh,
        tools: [
          {
            tool: "bls.oews.source",
            call: `bls.oews.source({ release: "May 2026", geography: "national", occupation: "${definition.socCode}", field: "A_MEDIAN" })`,
            result:
              "Target registered in the Thesis ledger before forecasting; resolution uses the first-published BLS national OEWS annual median wage field.",
          },
          {
            tool: "wage_pressure.decompose",
            call: `wage_pressure.decompose({ soc_major_group: "${definition.socCode}", base_year: 2025, target_year: 2026 })`,
            result: definition.wageSignalResult,
          },
        ],
        rationale: definition.rationale,
      },
    ],
  };
}

export const OEWS_OCCUPATION_WAGE_PREDICTION_SERIES =
  OCCUPATION_WAGE_DEFINITIONS.map(occupationWageSeriesFor);

export const OCCUPATION_WAGE_EXAMPLES = buildForecastCellsFromSeries(
  OEWS_OCCUPATION_WAGE_PREDICTION_SERIES,
).map(withCurrentOewsWageBaselineRun);

function withCurrentOewsWageBaselineRun(forecast: ForecastCell): ForecastCell {
  const definition = OCCUPATION_WAGE_DEFINITIONS.find(
    (candidate) => candidate.slug === forecast.slug,
  );
  if (!definition) return forecast;

  return {
    ...forecast,
    comparisonRuns: [
      ...(forecast.comparisonRuns ?? []),
      buildCurrentOewsWageBaselineRun(forecast, definition),
    ],
  };
}

function buildCurrentOewsWageBaselineRun(
  forecast: ForecastCell,
  definition: OccupationWageDefinition,
): ForecastComparisonRun {
  const point = definition.latestMedianAnnualWage;
  const epsilon = 500;

  return {
    variantId: "may-2025-oews-carry-forward",
    label: "May 2025 OEWS carry-forward",
    description:
      "Baseline comparator: carry the latest published OEWS annual median wage forward unchanged.",
    pointEstimate: point,
    ciLow: point - epsilon,
    ciHigh: point + epsilon,
    drivers: [
      "Latest published OEWS annual median wage",
      "No explicit occupational wage projection",
      "Flat nominal carry-forward comparator",
    ],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-05-15T10:00:00-04:00",
      agent: "BLS OEWS current table",
      model: "May 2025 annual median wage carry-forward baseline",
      sourceContext: [
        "BLS OEWS May 2025 national annual median wage table",
        "BLS OEWS time-series API datatype 13 annual median wage",
      ],
      runLabel: "Current OEWS carry-forward",
      runDescription:
        "Not an official BLS forecast; a flat comparator because BLS does not publish projected occupational wage levels.",
    },
    reasoning: [
      {
        kind: "heading",
        text: "Current-wage comparator",
      },
      {
        kind: "text",
        text: "BLS publishes current OEWS occupational wages but not an official May 2026 occupational wage projection. This comparator carries the May 2025 median annual wage forward unchanged.",
      },
      {
        kind: "tool",
        tool: "bls.oews.api",
        call: `bls.oews.api({ target: "${forecast.dataPointId}", comparator: "latest_observed_a_median" })`,
        result: `{ latest_observed_year: 2025, annual_median_wage_usd: ${point}, source: 'BLS OEWS May 2025' }`,
      },
      {
        kind: "math",
        text: `Flat carry-forward baseline = ${formatUsd(point)}.`,
      },
      {
        kind: "forecast",
        point,
        ciLow: point - epsilon,
        ciHigh: point + epsilon,
      },
    ],
  };
}

function formatUsd(value: number): string {
  return `$${Math.round(value).toLocaleString("en-US")}`;
}
