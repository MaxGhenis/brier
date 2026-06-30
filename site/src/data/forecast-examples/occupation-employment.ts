import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";
import { requireLedgerTarget } from "../ledger-targets";
import type {
  ForecastCell,
  ForecastComparisonRun,
  PredictionPackReference,
  PredictionPackSet,
} from "../forecast-cells";

const OCCUPATION_NO_PACK_SET = {
  packSetId: "pack_set.occupation_automation_control.v1",
  label: "Occupation automation control",
  mode: "none",
  packs: [],
  notes:
    "Control run using OEWS context and task-automation literature without the BLS Employment Projections pack.",
} satisfies PredictionPackSet;

const BLS_EMPLOYMENT_PROJECTIONS_PACK = {
  packId: "bls-employment-projections-baseline",
  version: "0.1.0",
  label: "BLS employment projections baseline",
  kind: "data",
  summary:
    "Adds BLS 2024-2034 occupational employment projections as a long-run baseline for OEWS occupation forecasts.",
} satisfies PredictionPackReference;

const BLS_EMPLOYMENT_PROJECTIONS_PACK_SET = {
  packSetId: "pack_set.bls_employment_projections_2024_2034.v1",
  label: "BLS 2024-2034 projections baseline",
  mode: "with_packs",
  packs: [BLS_EMPLOYMENT_PROJECTIONS_PACK],
  notes:
    "Uses BLS Employment Projections as a prior only; OEWS first-print employment remains the resolver.",
} satisfies PredictionPackSet;

const RECORDED_OCCUPATION_AUTOMATION_RUN = {
  kind: "recorded-agent-run",
  runAt: "2026-06-17T14:25:00-04:00",
  agent: "Occupation automation exposure source synthesis",
  model: "Codex recorded source-context synthesis",
  sourceContext: [
    "BLS Occupational Employment and Wage Statistics",
    "BLS May 2025 National Occupational Employment and Wage Estimates",
    "BLS OEWS technical notes",
    "SOC major occupational groups",
    "Task automation exposure literature",
  ],
  runLabel: "Occupation synthesis - no projection pack",
  runDescription:
    "Control run with OEWS history and task-automation context, before adding BLS Employment Projections as a prior.",
  packSet: OCCUPATION_NO_PACK_SET,
} satisfies PredictionSeries["predictionRun"];

const RECORDED_OCCUPATION_LONG_RUN_RUN = {
  kind: "recorded-agent-run",
  runAt: "2026-06-21T22:15:00-04:00",
  agent: "brier-occupation-automation-scenarios",
  model: "Codex recorded source-context synthesis",
  sourceContext: [
    "BLS Employment Projections Table 1.2, 2024-2034",
    "BLS National Employment Matrix base-year methodology",
    "BLS OEWS national occupational employment tables",
    "Task automation exposure literature",
    "AI adoption and labor-demand scenario notes",
  ],
  runLabel: "Brier long-run - no BLS pack",
  runDescription:
    "Brier occupation scenario without admitting the BLS 2024-2034 projection baseline as a pack.",
  packSet: OCCUPATION_NO_PACK_SET,
} satisfies PredictionSeries["predictionRun"];

interface BlsProjectionBaseline {
  socCode: string;
  employment2024: number;
  blsProjection2034: number;
  blsPercentChange: number;
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  projectionResult: string;
  rationale: string;
}

const BLS_PROJECTION_BASELINES: Record<string, BlsProjectionBaseline> = {
  "oews-business-financial-employment-may-2026": {
    socCode: "13-0000",
    employment2024: 11262.0,
    blsProjection2034: 11848.9,
    blsPercentChange: 5.2,
    pointEstimate: 10480,
    ciLow: 10130,
    ciHigh: 10860,
    projectionResult:
      "{ bls_projection_window: '2024-2034', occupation_group: '13-0000', long_run_signal: 'above-average white-collar growth', pack_adjustment_thousands: +60 }",
    rationale:
      "The BLS projection baseline nudges the center higher because business and financial occupations remain a positive-growth group over the decade, but the pack only modestly affects a May 2026 first-print OEWS target.",
  },
  "oews-computer-math-employment-may-2026": {
    socCode: "15-0000",
    employment2024: 5416.7,
    blsProjection2034: 5962.3,
    blsPercentChange: 10.1,
    pointEstimate: 5900,
    ciLow: 5620,
    ciHigh: 6210,
    projectionResult:
      "{ bls_projection_window: '2024-2034', occupation_group: '15-0000', long_run_signal: 'strong STEM and software demand', pack_adjustment_thousands: +50 }",
    rationale:
      "The projections pack raises the center slightly: BLS long-run computer and mathematical growth leans against a pure near-term automation-substitution story, while the interval remains wide for tech hiring cyclicality.",
  },
  "oews-healthcare-support-employment-may-2026": {
    socCode: "31-0000",
    employment2024: 7982.8,
    blsProjection2034: 8971.1,
    blsPercentChange: 12.4,
    pointEstimate: 7480,
    ciLow: 7120,
    ciHigh: 7860,
    projectionResult:
      "{ bls_projection_window: '2024-2034', occupation_group: '31-0000', long_run_signal: 'demographic healthcare demand', pack_adjustment_thousands: +60 }",
    rationale:
      "The BLS projection prior pushes healthcare support higher because long-run care demand is a strong outside-view anchor and near-term AI substitution is limited.",
  },
  "oews-office-admin-employment-may-2026": {
    socCode: "43-0000",
    employment2024: 19325.2,
    blsProjection2034: 18563.3,
    blsPercentChange: -3.9,
    pointEstimate: 17590,
    ciLow: 17140,
    ciHigh: 17980,
    projectionResult:
      "{ bls_projection_window: '2024-2034', occupation_group: '43-0000', long_run_signal: 'declining clerical employment', pack_adjustment_thousands: -60 }",
    rationale:
      "The BLS projection prior lowers the center: long-run BLS clerical projections reinforce the automation-exposure case for office and administrative support decline.",
  },
  "oews-production-employment-may-2026": {
    socCode: "51-0000",
    employment2024: 9001.2,
    blsProjection2034: 8901.6,
    blsPercentChange: -1.1,
    pointEstimate: 8500,
    ciLow: 8120,
    ciHigh: 8880,
    projectionResult:
      "{ bls_projection_window: '2024-2034', occupation_group: '51-0000', long_run_signal: 'flat-to-declining production employment', pack_adjustment_thousands: -20 }",
    rationale:
      "The projection pack has a small negative effect: BLS long-run production employment pressure is already aligned with the control forecast, so the pack mostly confirms rather than moves the center.",
  },
  "oews-transport-material-moving-employment-may-2026": {
    socCode: "53-0000",
    employment2024: 14204.6,
    blsProjection2034: 14784.4,
    blsPercentChange: 4.1,
    pointEstimate: 14110,
    ciLow: 13580,
    ciHigh: 14700,
    projectionResult:
      "{ bls_projection_window: '2024-2034', occupation_group: '53-0000', long_run_signal: 'continued logistics demand with automation offset', pack_adjustment_thousands: +60 }",
    rationale:
      "The BLS projection prior nudges transportation and material moving up because goods movement and logistics demand remain positive even with warehouse automation pressure.",
  },
};

interface Bls2034OccupationDefinition {
  socCode: string;
  slug: string;
  title: string;
  question: string;
  measure: string;
  whyItMatters: string;
  drivers: string[];
  employment2024: number;
  blsProjection2034: number;
  blsNumericChange: number;
  blsPercentChange: number;
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  packPointEstimate: number;
  packCiLow: number;
  packCiHigh: number;
  noPackRationale: string;
  packRationale: string;
  exposureResult: string;
}

interface CpsOccupationDefinition {
  key: string;
  slug: string;
  title: string;
  question: string;
  measure: string;
  whyItMatters: string;
  drivers: string[];
  may2025: number;
  may2026: number;
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  exposureResult: string;
  rationale: string;
}

const BLS_2034_OCCUPATION_DEFINITIONS: Bls2034OccupationDefinition[] = [
  {
    socCode: "13-0000",
    slug: "bls-business-financial-employment-2034",
    title: "Business and financial occupation employment, 2034",
    question:
      "What will BLS first publish as 2034 employment for SOC 13-0000 Business and Financial Operations Occupations in the National Employment Matrix?",
    measure:
      "National Employment Matrix employment in business and financial operations occupations",
    whyItMatters:
      "This is the apples-to-apples long-run target for analyst, compliance, accounting, and finance work: Brier and BLS are both forecasting the same 2034 BLS occupation employment surface.",
    drivers: [
      "Professional-services labor demand",
      "Finance and compliance workload",
      "AI-assisted analyst productivity",
      "Automation of bookkeeping and claims workflows",
    ],
    employment2024: 11262.0,
    blsProjection2034: 11848.9,
    blsNumericChange: 586.9,
    blsPercentChange: 5.2,
    pointEstimate: 11480,
    ciLow: 10350,
    ciHigh: 12800,
    packPointEstimate: 11710,
    packCiLow: 10650,
    packCiHigh: 12750,
    noPackRationale:
      "The no-pack forecast is below the BLS projection because Brier puts more weight on task absorption in back-office analysis, bookkeeping-adjacent work, claims workflows, and compliance review. Demand still grows, but headcount growth is muted relative to the official projection baseline.",
    packRationale:
      "The BLS pack moves the forecast back toward the official 2024-2034 projection, because the BLS matrix still expects broad demand growth for business operations, human resources, logistics, and management analysis despite task-level automation pressure.",
    exposureResult:
      "{ exposure: 'high_complementarity_and_substitution', bls_2034_projection_thousands: 11848.9, brier_no_pack_delta_vs_bls_thousands: -368.9 }",
  },
  {
    socCode: "15-0000",
    slug: "bls-computer-math-employment-2034",
    title: "Computer and mathematical occupation employment, 2034",
    question:
      "What will BLS first publish as 2034 employment for SOC 15-0000 Computer and Mathematical Occupations in the National Employment Matrix?",
    measure:
      "National Employment Matrix employment in computer and mathematical occupations",
    whyItMatters:
      "This target tests whether Brier expects AI to be mainly labor-saving in software work or demand-expanding through AI infrastructure, security, data, and integration work.",
    drivers: [
      "Software and data labor demand",
      "AI infrastructure buildout",
      "Coding-assistant productivity",
      "Cybersecurity and model-integration work",
    ],
    employment2024: 5416.7,
    blsProjection2034: 5962.3,
    blsNumericChange: 545.6,
    blsPercentChange: 10.1,
    pointEstimate: 6300,
    ciLow: 5000,
    ciHigh: 7600,
    packPointEstimate: 6120,
    packCiLow: 5120,
    packCiHigh: 7250,
    noPackRationale:
      "The no-pack forecast is above BLS because Brier's scenario assigns a larger demand-expansion effect to AI infrastructure, security, data engineering, and model-integration work than the official baseline appears to. The lower tail still allows direct coding automation and offshoring to dominate.",
    packRationale:
      "The BLS pack pulls the center closer to the official projection. It tempers the AI-demand upside by anchoring to BLS's 10.1 percent projected growth for the major group, while preserving a wider upside tail than BLS's point estimate.",
    exposureResult:
      "{ exposure: 'very_high', demand_expansion: 'large', bls_2034_projection_thousands: 5962.3, brier_no_pack_delta_vs_bls_thousands: +337.7 }",
  },
  {
    socCode: "31-0000",
    slug: "bls-healthcare-support-employment-2034",
    title: "Healthcare support occupation employment, 2034",
    question:
      "What will BLS first publish as 2034 employment for SOC 31-0000 Healthcare Support Occupations in the National Employment Matrix?",
    measure:
      "National Employment Matrix employment in healthcare support occupations",
    whyItMatters:
      "Healthcare support is the low-substitution benchmark for the automation slate: demand is demographic and physical-care intensive, so it checks whether Brier over-applies software automation to hands-on work.",
    drivers: [
      "Aging-driven care demand",
      "Home health and personal care aides",
      "Medicaid and Medicare utilization",
      "Limited physical-task automation",
    ],
    employment2024: 7982.8,
    blsProjection2034: 8971.1,
    blsNumericChange: 988.3,
    blsPercentChange: 12.4,
    pointEstimate: 9100,
    ciLow: 8100,
    ciHigh: 10350,
    packPointEstimate: 9020,
    packCiLow: 8150,
    packCiHigh: 9900,
    noPackRationale:
      "The no-pack forecast is slightly above BLS because Brier puts more weight on care demand and home-based support needs than on software substitution. The main uncertainty is staffing supply and public-payment pressure, not AI replacing the core work.",
    packRationale:
      "The BLS pack centers the forecast close to the official 12.4 percent projected growth path and trims some upside from unconstrained care demand.",
    exposureResult:
      "{ exposure: 'low_substitution', demographic_pressure: 'high', bls_2034_projection_thousands: 8971.1, brier_no_pack_delta_vs_bls_thousands: +128.9 }",
  },
  {
    socCode: "43-0000",
    slug: "bls-office-admin-employment-2034",
    title: "Office and administrative support employment, 2034",
    question:
      "What will BLS first publish as 2034 employment for SOC 43-0000 Office and Administrative Support Occupations in the National Employment Matrix?",
    measure:
      "National Employment Matrix employment in office and administrative support occupations",
    whyItMatters:
      "This is the largest clean long-run test for routine information-work automation: scheduling, records, billing, call handling, form processing, and clerical coordination all map directly to software and AI tools.",
    drivers: [
      "Clerical process automation",
      "AI scheduling and document tools",
      "Business-service employment demand",
      "Call-center and records workflow redesign",
    ],
    employment2024: 19325.2,
    blsProjection2034: 18563.3,
    blsNumericChange: -761.9,
    blsPercentChange: -3.9,
    pointEstimate: 17200,
    ciLow: 14500,
    ciHigh: 19400,
    packPointEstimate: 17850,
    packCiLow: 15300,
    packCiHigh: 19450,
    noPackRationale:
      "The no-pack forecast is materially below the BLS projection. Brier treats office and administrative support as the most exposed large group: document intake, scheduling, billing, customer-contact triage, and records work can be automated or bundled into higher-output roles.",
    packRationale:
      "The BLS pack raises the center because the official baseline already includes a decline but not a sharp automation break. The packed run still stays below BLS, preserving Brier's stronger substitution view.",
    exposureResult:
      "{ exposure: 'high_substitution', routine_information_task_share: 'high', bls_2034_projection_thousands: 18563.3, brier_no_pack_delta_vs_bls_thousands: -1363.3 }",
  },
  {
    socCode: "51-0000",
    slug: "bls-production-employment-2034",
    title: "Production occupation employment, 2034",
    question:
      "What will BLS first publish as 2034 employment for SOC 51-0000 Production Occupations in the National Employment Matrix?",
    measure:
      "National Employment Matrix employment in production occupations",
    whyItMatters:
      "Production work ties the task-automation literature to robotics, process control, reshoring, trade, and goods demand rather than only white-collar software substitution.",
    drivers: [
      "Manufacturing output",
      "Factory automation and robotics",
      "Trade and reshoring",
      "Goods-sector cyclicality",
    ],
    employment2024: 9001.2,
    blsProjection2034: 8901.6,
    blsNumericChange: -99.6,
    blsPercentChange: -1.1,
    pointEstimate: 8550,
    ciLow: 7600,
    ciHigh: 9650,
    packPointEstimate: 8750,
    packCiLow: 7800,
    packCiHigh: 9650,
    noPackRationale:
      "The no-pack forecast is below BLS because Brier expects robotics, process control, and software-mediated production planning to continue reducing labor intensity in routine production roles, even if reshoring supports output.",
    packRationale:
      "The BLS pack moderates that decline by anchoring to the official projection's near-flat production path, while still preserving Brier's downside skew from automation and goods-cycle risk.",
    exposureResult:
      "{ exposure: 'medium', automation_channel: 'robotics_and_process_control', bls_2034_projection_thousands: 8901.6, brier_no_pack_delta_vs_bls_thousands: -351.6 }",
  },
  {
    socCode: "53-0000",
    slug: "bls-transport-material-moving-employment-2034",
    title: "Transportation and material moving employment, 2034",
    question:
      "What will BLS first publish as 2034 employment for SOC 53-0000 Transportation and Material Moving Occupations in the National Employment Matrix?",
    measure:
      "National Employment Matrix employment in transportation and material moving occupations",
    whyItMatters:
      "Transportation and material moving tests whether warehouse automation, routing software, and partial autonomy reduce labor demand enough to offset logistics volume growth.",
    drivers: [
      "Goods movement and e-commerce volume",
      "Warehouse automation",
      "Trucking and delivery demand",
      "Autonomy deployment timelines",
    ],
    employment2024: 14204.6,
    blsProjection2034: 14784.4,
    blsNumericChange: 579.9,
    blsPercentChange: 4.1,
    pointEstimate: 14250,
    ciLow: 12500,
    ciHigh: 16100,
    packPointEstimate: 14580,
    packCiLow: 12800,
    packCiHigh: 16150,
    noPackRationale:
      "The no-pack forecast is below BLS because Brier expects warehouse automation, route optimization, and limited autonomy to lower labor per unit of goods movement. It does not assume full driver displacement by 2034.",
    packRationale:
      "The BLS pack raises the center toward the official projection's continued logistics growth, while keeping the forecast below BLS because automation pressure remains a meaningful offset.",
    exposureResult:
      "{ exposure: 'medium_high', logistics_demand: 'positive', bls_2034_projection_thousands: 14784.4, brier_no_pack_delta_vs_bls_thousands: -534.4 }",
  },
];

const CPS_JUNE_2026_OCCUPATION_DEFINITIONS: CpsOccupationDefinition[] = [
  {
    key: "business_financial_operations",
    slug: "cps-business-financial-employment-june-2026",
    title: "CPS business and financial employment, June 2026",
    question:
      "What will BLS first publish as June 2026 employed people in business and financial operations occupations in CPS Table A-19?",
    measure:
      "CPS employed people in business and financial operations occupations, not seasonally adjusted",
    whyItMatters:
      "This is the fast monthly proxy for the business and financial OEWS group, trading clean SOC annual measurement for a July 2026 read on analyst, accounting, compliance, and finance labor demand.",
    drivers: [
      "Monthly CPS sampling noise",
      "Professional-services labor demand",
      "Finance and compliance hiring",
      "AI-assisted analyst productivity",
    ],
    may2025: 10130,
    may2026: 10033,
    pointEstimate: 10040,
    ciLow: 9600,
    ciHigh: 10480,
    exposureResult:
      "{ cps_table: 'A-19', occupation_group: 'Business and financial operations occupations', may_2026_thousands: 10033, yoy_change_thousands: -97 }",
    rationale:
      "The June forecast stays near the May 2026 CPS table value because this monthly household-survey row is noisy and not seasonally adjusted. The point allows a small recovery from May but keeps the interval wide enough for sampling movement and month-specific occupation coding shifts.",
  },
  {
    key: "computer_mathematical",
    slug: "cps-computer-math-employment-june-2026",
    title: "CPS computer and mathematical employment, June 2026",
    question:
      "What will BLS first publish as June 2026 employed people in computer and mathematical occupations in CPS Table A-19?",
    measure:
      "CPS employed people in computer and mathematical occupations, not seasonally adjusted",
    whyItMatters:
      "This is the fastest BLS occupation readout for software, data, security, and quantitative work while the annual OEWS and long-run projection targets remain pending.",
    drivers: [
      "Tech and data hiring",
      "AI infrastructure labor demand",
      "Coding-assistant productivity",
      "Monthly CPS sampling noise",
    ],
    may2025: 6512,
    may2026: 6903,
    pointEstimate: 6920,
    ciLow: 6500,
    ciHigh: 7350,
    exposureResult:
      "{ cps_table: 'A-19', occupation_group: 'Computer and mathematical occupations', may_2026_thousands: 6903, yoy_change_thousands: +391 }",
    rationale:
      "The monthly CPS row already shows strong year-over-year growth in May. The forecast carries that signal into June while avoiding a precise trend extrapolation because CPS occupation cells can move several hundred thousand workers month to month.",
  },
  {
    key: "healthcare_support",
    slug: "cps-healthcare-support-employment-june-2026",
    title: "CPS healthcare support employment, June 2026",
    question:
      "What will BLS first publish as June 2026 employed people in healthcare support occupations in CPS Table A-19?",
    measure:
      "CPS employed people in healthcare support occupations, not seasonally adjusted",
    whyItMatters:
      "Healthcare support is the monthly low-substitution benchmark for the occupation automation slate, but the CPS row is noisier than OEWS and can diverge from payroll health-care momentum.",
    drivers: [
      "Care-demand pressure",
      "Hospital and long-term-care staffing",
      "Limited physical-task automation",
      "Monthly CPS sampling noise",
    ],
    may2025: 5868,
    may2026: 5786,
    pointEstimate: 5800,
    ciLow: 5400,
    ciHigh: 6200,
    exposureResult:
      "{ cps_table: 'A-19', occupation_group: 'Healthcare support occupations', may_2026_thousands: 5786, yoy_change_thousands: -82 }",
    rationale:
      "The forecast mostly repeats May because demographic demand is positive but the CPS row weakened year over year. The interval is wide relative to trend because this is a small monthly occupation cell rather than an establishment payroll series.",
  },
  {
    key: "office_administrative_support",
    slug: "cps-office-admin-employment-june-2026",
    title: "CPS office and administrative support employment, June 2026",
    question:
      "What will BLS first publish as June 2026 employed people in office and administrative support occupations in CPS Table A-19?",
    measure:
      "CPS employed people in office and administrative support occupations, not seasonally adjusted",
    whyItMatters:
      "This gives a near-term read on routine clerical and administrative work before the cleaner OEWS annual estimate resolves.",
    drivers: [
      "Back-office automation",
      "AI scheduling and document tools",
      "Service-sector hiring",
      "Monthly CPS sampling noise",
    ],
    may2025: 16115,
    may2026: 16335,
    pointEstimate: 16300,
    ciLow: 15650,
    ciHigh: 16950,
    exposureResult:
      "{ cps_table: 'A-19', occupation_group: 'Office and administrative support occupations', may_2026_thousands: 16335, yoy_change_thousands: +220 }",
    rationale:
      "The CPS row rose year over year in May despite the long-run automation concern. The June point stays just below May, treating the monthly increase as noisy rather than reversing the broader office/admin exposure thesis.",
  },
  {
    key: "production",
    slug: "cps-production-employment-june-2026",
    title: "CPS production employment, June 2026",
    question:
      "What will BLS first publish as June 2026 employed people in production occupations in CPS Table A-19?",
    measure:
      "CPS employed people in production occupations, not seasonally adjusted",
    whyItMatters:
      "Production occupations connect the fast monthly CPS proxy to manufacturing demand, robotics, process control, trade exposure, and goods-sector cyclicality.",
    drivers: [
      "Manufacturing output",
      "Factory automation and robotics",
      "Goods-sector demand",
      "Monthly CPS sampling noise",
    ],
    may2025: 7947,
    may2026: 7912,
    pointEstimate: 7900,
    ciLow: 7500,
    ciHigh: 8350,
    exposureResult:
      "{ cps_table: 'A-19', occupation_group: 'Production occupations', may_2026_thousands: 7912, yoy_change_thousands: -35 }",
    rationale:
      "The central case is essentially flat from May, consistent with a mixed manufacturing picture and modest automation pressure. The interval leaves room for CPS noise and goods-sector month-to-month volatility.",
  },
  {
    key: "transportation_material_moving",
    slug: "cps-transport-material-moving-employment-june-2026",
    title: "CPS transportation and material moving employment, June 2026",
    question:
      "What will BLS first publish as June 2026 employed people in transportation and material moving occupations in CPS Table A-19?",
    measure:
      "CPS employed people in transportation and material moving occupations, not seasonally adjusted",
    whyItMatters:
      "This is the fast monthly proxy for logistics, warehousing, routing, and autonomy exposure before the annual OEWS occupation table resolves.",
    drivers: [
      "Goods movement and e-commerce volume",
      "Warehouse automation",
      "Trucking and delivery demand",
      "Monthly CPS sampling noise",
    ],
    may2025: 11742,
    may2026: 12120,
    pointEstimate: 12100,
    ciLow: 11500,
    ciHigh: 12700,
    exposureResult:
      "{ cps_table: 'A-19', occupation_group: 'Transportation and material moving occupations', may_2026_thousands: 12120, yoy_change_thousands: +378 }",
    rationale:
      "The point holds close to May because logistics demand still looks positive, but warehouse automation and routing productivity keep the center from extrapolating the full year-over-year CPS gain.",
  },
];

function oewsDataPointId(socCode: string): string {
  return `bls.oews.national_occupation_employment.soc_${socCode.replace("-", "_")}.may_2026.first_print`;
}

function bls2034DataPointId(socCode: string): string {
  return `bls.employment_projections.national_occupation_employment.soc_${socCode.replace("-", "_")}.2034.actual_first_print`;
}

function cpsOccupationDataPointId(key: string): string {
  return `bls.cps.employed_people_by_occupation.${key}.june_2026.first_print`;
}

function occupationSeriesFor({
  socCode,
  slug,
  title,
  question,
  measure,
  whyItMatters,
  drivers,
  history,
  pointEstimate,
  ciLow,
  ciHigh,
  exposureResult,
  rationale,
}: {
  socCode: string;
  slug: string;
  title: string;
  question: string;
  measure: string;
  whyItMatters: string;
  drivers: string[];
  history: PredictionSeries["history"];
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  exposureResult: string;
  rationale: string;
}): PredictionSeries {
  const target = requireLedgerTarget(oewsDataPointId(socCode));

  return {
    seriesId: target.dataPointId.replace(".may_2026.first_print", ""),
    title,
    measure,
    unit: target.unit,
    source: target.source,
    sourceUrl: target.sourceUrl,
    cadence: "annual",
    priority: "P1",
    resolutionLatency: "~12 months",
    resolutionPolicy: target.resolutionPolicy,
    benchmark:
      "May 2025 OEWS national table plus payroll, openings, and automation-exposure priors",
    chainableQuestions: ["next annual release", "+12 months", "threshold"],
    whyItMatters,
    drivers,
    history,
    historyTool: {
      tool: "bls.oews.lookup",
      call: `bls.oews.lookup({ table: "national", occupation: "${socCode}", releases: ["May 2023", "May 2024", "May 2025"] })`,
      result:
        "Rounded national OEWS employment in thousands from source-context synthesis; replace with exact BLS table extraction once the OEWS download integration is wired into the ledger.",
    },
    predictionRun: RECORDED_OCCUPATION_AUTOMATION_RUN,
    targets: [
      {
        slug,
        title,
        question,
        dataPointId: target.dataPointId,
        horizon: "next_release",
        horizonLabel: "May 2026 OEWS first print",
        periodLabel: target.periodLabel,
        resolutionDate: target.resolutionDate,
        resolutionRule: target.resolutionRule,
        resolutionSourceUrl: target.resolutionSourceUrl,
        pointEstimate,
        ciLow,
        ciHigh,
        tools: [
          {
            tool: "bls.oews.source",
            call: `bls.oews.source({ release: "May 2026", geography: "national", occupation: "${socCode}" })`,
            result:
              "Target registered in the Thesis ledger before forecasting; resolution uses the first-published BLS national OEWS occupation employment table.",
          },
          {
            tool: "automation_exposure.map",
            call: `automation_exposure.map({ soc_major_group: "${socCode}", lens: "task_automation_literature" })`,
            result: exposureResult,
          },
        ],
        rationale,
      },
    ],
  };
}

export const OEWS_OCCUPATION_EMPLOYMENT_PREDICTION_SERIES = [
  occupationSeriesFor({
    socCode: "13-0000",
    slug: "oews-business-financial-employment-may-2026",
    title: "Business and financial occupation employment, May 2026",
    question:
      "How many people will BLS first publish as employed in SOC 13-0000 Business and Financial Operations Occupations in the May 2026 national OEWS release?",
    measure:
      "National employment in business and financial operations occupations",
    whyItMatters:
      "This group is a clean white-collar exposure target: analysts, compliance staff, accountants, and related roles face both AI substitution pressure and productivity-driven demand growth.",
    drivers: [
      "Professional and business-services hiring",
      "Finance and compliance demand",
      "AI-assisted analyst productivity",
      "Business formation and reporting burden",
    ],
    history: [
      { label: "2023 est.", value: 9800 },
      { label: "2024 est.", value: 10000 },
      { label: "2025 est.", value: 10300 },
    ],
    pointEstimate: 10420,
    ciLow: 10050,
    ciHigh: 10800,
    exposureResult:
      "{ exposure: 'high-complementarity', routine_task_share: 'medium', near_term_direction: 'modest_growth' }",
    rationale:
      "Professional services and finance hiring should keep this group growing, but the forecast discounts simple trend extrapolation because analyst, bookkeeping, and compliance workflows are exactly where generative AI can absorb task volume without an immediate headcount increase.",
  }),
  occupationSeriesFor({
    socCode: "15-0000",
    slug: "oews-computer-math-employment-may-2026",
    title: "Computer and mathematical occupation employment, May 2026",
    question:
      "How many people will BLS first publish as employed in SOC 15-0000 Computer and Mathematical Occupations in the May 2026 national OEWS release?",
    measure: "National employment in computer and mathematical occupations",
    whyItMatters:
      "Computer and mathematical occupations are the most direct labor-market readout for coding assistants, data-analysis tools, and the demand side of AI infrastructure buildout.",
    drivers: [
      "Software and data hiring",
      "AI infrastructure investment",
      "Productivity from coding assistants",
      "Interest-rate-sensitive tech demand",
    ],
    history: [
      { label: "2023 est.", value: 5300 },
      { label: "2024 est.", value: 5480 },
      { label: "2025 est.", value: 5725 },
    ],
    pointEstimate: 5850,
    ciLow: 5550,
    ciHigh: 6150,
    exposureResult:
      "{ exposure: 'very_high', substitution_channel: 'coding_task_automation', demand_channel: 'ai_capex_and_data_work' }",
    rationale:
      "The central case is continued growth, not collapse: AI tooling reduces some junior coding task demand but AI infrastructure, data engineering, security, and model-integration work keep total employment above the 2025 level. The interval keeps a wide lower tail for hiring freezes and offshoring.",
  }),
  occupationSeriesFor({
    socCode: "31-0000",
    slug: "oews-healthcare-support-employment-may-2026",
    title: "Healthcare support occupation employment, May 2026",
    question:
      "How many people will BLS first publish as employed in SOC 31-0000 Healthcare Support Occupations in the May 2026 national OEWS release?",
    measure: "National employment in healthcare support occupations",
    whyItMatters:
      "Healthcare support is a useful low-substitution benchmark: care work is labor intensive, demand is demographically strong, and AI effects mostly run through documentation and scheduling.",
    drivers: [
      "Aging-driven care demand",
      "Hospital and long-term-care staffing",
      "Medicaid and Medicare utilization",
      "Limited near-term physical-task automation",
    ],
    history: [
      { label: "2023 est.", value: 6900 },
      { label: "2024 est.", value: 7100 },
      { label: "2025 est.", value: 7250 },
    ],
    pointEstimate: 7420,
    ciLow: 7050,
    ciHigh: 7800,
    exposureResult:
      "{ exposure: 'low_substitution', complementarity: 'documentation_and_triage', demographic_pressure: 'high' }",
    rationale:
      "This group should keep expanding because demand for aides, assistants, and support staff is tied to care volume rather than information processing alone. The main downside risk is provider margin pressure and staffing shortages, not AI task substitution.",
  }),
  occupationSeriesFor({
    socCode: "43-0000",
    slug: "oews-office-admin-employment-may-2026",
    title: "Office and administrative support employment, May 2026",
    question:
      "How many people will BLS first publish as employed in SOC 43-0000 Office and Administrative Support Occupations in the May 2026 national OEWS release?",
    measure:
      "National employment in office and administrative support occupations",
    whyItMatters:
      "Office and administrative support is the clearest large SOC group for clerical automation: scheduling, records, call handling, forms, and back-office workflows are all direct software targets.",
    drivers: [
      "Back-office automation",
      "Administrative hiring in services",
      "Business formation and churn",
      "Adoption of AI scheduling and document tools",
    ],
    history: [
      { label: "2023 est.", value: 18300 },
      { label: "2024 est.", value: 18050 },
      { label: "2025 est.", value: 17850 },
    ],
    pointEstimate: 17650,
    ciLow: 17200,
    ciHigh: 18050,
    exposureResult:
      "{ exposure: 'high_substitution', routine_information_task_share: 'high', near_term_direction: 'decline' }",
    rationale:
      "The forecast keeps the downward trend intact. Even if overall service employment grows, routine clerical headcount is exposed to document automation, scheduling tools, and customer-contact software, so the central estimate is below the 2025 level.",
  }),
  occupationSeriesFor({
    socCode: "51-0000",
    slug: "oews-production-employment-may-2026",
    title: "Production occupation employment, May 2026",
    question:
      "How many people will BLS first publish as employed in SOC 51-0000 Production Occupations in the May 2026 national OEWS release?",
    measure: "National employment in production occupations",
    whyItMatters:
      "Production occupations connect task automation to robotics, manufacturing demand, trade exposure, and goods-sector cyclicality rather than only software substitution.",
    drivers: [
      "Manufacturing output",
      "Factory automation and robotics",
      "Interest-rate-sensitive goods demand",
      "Trade and reshoring effects",
    ],
    history: [
      { label: "2023 est.", value: 8700 },
      { label: "2024 est.", value: 8620 },
      { label: "2025 est.", value: 8600 },
    ],
    pointEstimate: 8520,
    ciLow: 8150,
    ciHigh: 8900,
    exposureResult:
      "{ exposure: 'medium', automation_channel: 'robotics_and_process_control', demand_channel: 'goods_cycle' }",
    rationale:
      "Production employment likely drifts down modestly as manufacturing demand stays mixed and automation continues to absorb routine tasks. The interval is symmetric enough to allow a reshoring or capex surprise, but the point stays below the 2025 context.",
  }),
  occupationSeriesFor({
    socCode: "53-0000",
    slug: "oews-transport-material-moving-employment-may-2026",
    title: "Transportation and material moving employment, May 2026",
    question:
      "How many people will BLS first publish as employed in SOC 53-0000 Transportation and Material Moving Occupations in the May 2026 national OEWS release?",
    measure:
      "National employment in transportation and material moving occupations",
    whyItMatters:
      "Logistics, warehousing, driving, and material movement are central to automation debates because warehouse software, routing, and autonomy can change task demand before fully replacing workers.",
    drivers: [
      "Goods movement and e-commerce volume",
      "Warehouse automation",
      "Trucking and delivery demand",
      "Autonomy timelines",
    ],
    history: [
      { label: "2023 est.", value: 13600 },
      { label: "2024 est.", value: 13850 },
      { label: "2025 est.", value: 13950 },
    ],
    pointEstimate: 14050,
    ciLow: 13500,
    ciHigh: 14650,
    exposureResult:
      "{ exposure: 'medium_high', near_term_substitution: 'warehouse_workflows', full_autonomy_effect: 'limited_by_2026' }",
    rationale:
      "Logistics employment should remain roughly flat-to-up through May 2026: warehouse automation and routing tools reduce marginal labor demand, but full vehicle autonomy is unlikely to materially cut national occupational employment by this release.",
  }),
] satisfies PredictionSeries[];

export const BLS_2034_OCCUPATION_EMPLOYMENT_PREDICTION_SERIES =
  BLS_2034_OCCUPATION_DEFINITIONS.map(bls2034OccupationSeriesFor);

export const CPS_JUNE_2026_OCCUPATION_EMPLOYMENT_PREDICTION_SERIES =
  CPS_JUNE_2026_OCCUPATION_DEFINITIONS.map(cpsOccupationSeriesFor);

export const OCCUPATION_EMPLOYMENT_PREDICTION_SERIES = [
  ...OEWS_OCCUPATION_EMPLOYMENT_PREDICTION_SERIES,
  ...CPS_JUNE_2026_OCCUPATION_EMPLOYMENT_PREDICTION_SERIES,
  ...BLS_2034_OCCUPATION_EMPLOYMENT_PREDICTION_SERIES,
] satisfies PredictionSeries[];

export const OCCUPATION_EMPLOYMENT_EXAMPLES = buildForecastCellsFromSeries(
  OCCUPATION_EMPLOYMENT_PREDICTION_SERIES,
)
  .map(withBlsProjectionBaselineRun)
  .map(withBls2034ComparisonRuns);

function bls2034OccupationSeriesFor(
  definition: Bls2034OccupationDefinition,
): PredictionSeries {
  const target = requireLedgerTarget(bls2034DataPointId(definition.socCode));

  return {
    seriesId: target.dataPointId.replace(".2034.actual_first_print", ""),
    title: definition.title,
    measure: definition.measure,
    unit: target.unit,
    source: target.source,
    sourceUrl: target.sourceUrl,
    cadence: "annual",
    priority: "P1",
    resolutionLatency: "~9 years",
    resolutionPolicy: target.resolutionPolicy,
    benchmark:
      "BLS Employment Projections Table 1.2, 2024-2034, plus task-automation scenarios",
    chainableQuestions: ["next projection vintage", "detailed SOC rows", "threshold"],
    whyItMatters: definition.whyItMatters,
    drivers: definition.drivers,
    history: [
      { label: "2024 BLS base", value: definition.employment2024 },
      { label: "2034 BLS projection", value: definition.blsProjection2034 },
    ],
    historyTool: {
      tool: "bls.employment_projections.lookup",
      call: `bls.employment_projections.lookup({ table: "1.2", window: "2024-2034", occupation: "${definition.socCode}" })`,
      result: formatBlsProjectionResult(definition),
    },
    predictionRun: RECORDED_OCCUPATION_LONG_RUN_RUN,
    targets: [
      {
        slug: definition.slug,
        title: definition.title,
        question: definition.question,
        dataPointId: target.dataPointId,
        horizon: "long_run",
        horizonLabel: "2034 base-year employment",
        periodLabel: target.periodLabel,
        resolutionDate: target.resolutionDate,
        resolutionRule: target.resolutionRule,
        resolutionSourceUrl: target.resolutionSourceUrl,
        pointEstimate: definition.pointEstimate,
        ciLow: definition.ciLow,
        ciHigh: definition.ciHigh,
        tools: [
          {
            tool: "automation_exposure.map",
            call: `automation_exposure.map({ soc_major_group: "${definition.socCode}", horizon: "2034", lens: "task_automation_literature" })`,
            result: definition.exposureResult,
          },
          {
            tool: "brier.target.check",
            call: `brier.target.check({ target: "${target.dataPointId}", comparator: "bls_2024_2034_projection" })`,
            result:
              "{ apples_to_apples: true, same_soc_group: true, same_unit: 'thousands', same_resolution_surface: 'future BLS National Employment Matrix 2034 base-year employment' }",
          },
        ],
        rationale: definition.noPackRationale,
      },
    ],
  };
}

function cpsOccupationSeriesFor(
  definition: CpsOccupationDefinition,
): PredictionSeries {
  const target = requireLedgerTarget(cpsOccupationDataPointId(definition.key));

  return {
    seriesId: target.dataPointId.replace(".june_2026.first_print", ""),
    title: definition.title,
    measure: definition.measure,
    unit: target.unit,
    source: target.source,
    sourceUrl: target.sourceUrl,
    cadence: "monthly",
    priority: "P0",
    resolutionLatency: "~2 weeks",
    resolutionPolicy: target.resolutionPolicy,
    benchmark:
      "BLS CPS Table A-19 May 2026 occupation row plus same-month labor-market context",
    chainableQuestions: ["next monthly release", "annual OEWS cross-check", "threshold"],
    whyItMatters: definition.whyItMatters,
    drivers: definition.drivers,
    history: [
      { label: "May 2025 CPS", value: definition.may2025 },
      { label: "May 2026 CPS", value: definition.may2026 },
    ],
    historyTool: {
      tool: "bls.cps.table_a19.lookup",
      call: `bls.cps.table_a19.lookup({ reference_months: ["May 2025", "May 2026"], row: "${definition.key}", columns: ["total_16_plus"] })`,
      result:
        `BLS CPS Table A-19, not seasonally adjusted, reports ${formatThousandsDisplay(definition.may2025)} in May 2025 and ${formatThousandsDisplay(definition.may2026)} in May 2026 for this occupation row.`,
    },
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-06-21T23:05:00-04:00",
      agent: "brier-cps-occupation-fast-proxy",
      model: "Codex recorded source-context synthesis",
      sourceContext: [
        "BLS Employment Situation release schedule",
        "BLS CPS Table A-19 employed people by occupation, sex, and age",
        "May 2026 Employment Situation Summary",
        "Task automation exposure literature",
      ],
      runLabel: "CPS fast proxy",
      runDescription:
        "Fast monthly CPS occupation forecast; noisy proxy for the cleaner annual OEWS occupation target.",
      packSet: OCCUPATION_NO_PACK_SET,
    },
    targets: [
      {
        slug: definition.slug,
        title: definition.title,
        question: definition.question,
        dataPointId: target.dataPointId,
        horizon: "next_release",
        horizonLabel: "June 2026 CPS Table A-19 first print",
        periodLabel: target.periodLabel,
        resolutionDate: target.resolutionDate,
        resolutionRule: target.resolutionRule,
        resolutionSourceUrl: target.resolutionSourceUrl,
        pointEstimate: definition.pointEstimate,
        ciLow: definition.ciLow,
        ciHigh: definition.ciHigh,
        tools: [
          {
            tool: "bls.release_schedule.lookup",
            call: 'bls.release_schedule.lookup({ release: "Employment Situation", reference_month: "June 2026" })',
            result:
              "BLS schedules the June 2026 Employment Situation release for July 2, 2026 at 8:30 AM ET.",
          },
          {
            tool: "automation_exposure.map",
            call: `automation_exposure.map({ cps_table: "A-19", occupation_row: "${definition.key}", lens: "fast_monthly_proxy" })`,
            result: definition.exposureResult,
          },
        ],
        rationale: definition.rationale,
      },
    ],
  };
}

function withBlsProjectionBaselineRun(forecast: ForecastCell): ForecastCell {
  const baseline = BLS_PROJECTION_BASELINES[forecast.slug];
  if (!baseline) return forecast;

  return {
    ...forecast,
    comparisonRuns: [
      ...(forecast.comparisonRuns ?? []),
      buildBlsProjectionBaselineRun(forecast, baseline),
      buildBlsImpliedAnnualBaselineRun(forecast, baseline),
    ],
  };
}

function buildBlsProjectionBaselineRun(
  forecast: ForecastCell,
  baseline: BlsProjectionBaseline,
): ForecastComparisonRun {
  const packAdjustment = baseline.pointEstimate - forecast.pointEstimate;

  return {
    variantId: "with-bls-employment-projections",
    label: "BLS projections pack",
    description:
      "Pack-enabled run using BLS 2024-2034 occupational projections as a long-run prior.",
    pointEstimate: baseline.pointEstimate,
    ciLow: baseline.ciLow,
    ciHigh: baseline.ciHigh,
    drivers: [
      ...forecast.drivers,
      "BLS 2024-2034 occupational employment projection baseline",
    ],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-06-17T14:40:00-04:00",
      agent: "brier-occupation-projection",
      model: "Codex recorded source-context synthesis",
      sourceContext: [
        "BLS Employment Projections: 2024-2034 Summary",
        "BLS Table 1.2 Occupational projections and worker characteristics",
        "BLS OEWS national occupational employment tables",
      ],
      runLabel: "BLS projections pack",
      runDescription:
        "Adds BLS long-run occupational projections as a prior while keeping OEWS first print as the resolution surface.",
      packSet: BLS_EMPLOYMENT_PROJECTIONS_PACK_SET,
    },
    reasoning: [
      {
        kind: "heading",
        text: "BLS Employment Projections pack",
      },
      {
        kind: "text",
        text: "This run treats BLS Employment Projections as an outside-view prior, not as the resolver. The target still resolves against the first-published May 2026 OEWS national occupation employment table.",
      },
      {
        kind: "tool",
        tool: "bls.employment_projections.lookup",
        call: `bls.employment_projections.lookup({ table: "1.2", window: "2024-2034", target: "${forecast.dataPointId}" })`,
        result: baseline.projectionResult,
      },
      {
        kind: "tool",
        tool: "brier.pack.apply",
        call: 'brier.pack.apply({ packs: ["bls-employment-projections-baseline@0.1.0"], role: "outside_view_prior" })',
        result: `{ admitted: 1, mode: 'with_packs', control_point_thousands: ${forecast.pointEstimate}, pack_adjustment_thousands: ${formatSignedPlain(packAdjustment)}, packed_point_thousands: ${baseline.pointEstimate}, resolver_unchanged: 'BLS OEWS first print' }`,
      },
      {
        kind: "math",
        text: `Control forecast ${formatThousandsDisplay(forecast.pointEstimate)} + BLS projections pack adjustment ${formatThousandsDisplay(packAdjustment)} = ${formatThousandsDisplay(baseline.pointEstimate)}.`,
      },
      {
        kind: "text",
        text: baseline.rationale,
      },
      {
        kind: "forecast",
        point: baseline.pointEstimate,
        ciLow: baseline.ciLow,
        ciHigh: baseline.ciHigh,
      },
    ],
  };
}

function buildBlsImpliedAnnualBaselineRun(
  forecast: ForecastCell,
  baseline: BlsProjectionBaseline,
): ForecastComparisonRun {
  const annualGrowthRate =
    (baseline.blsProjection2034 / baseline.employment2024) ** (1 / 10) - 1;
  const latestOews = forecast.historicalContext.at(-1)?.value ?? forecast.pointEstimate;
  const point = roundToNearestTen(latestOews * (1 + annualGrowthRate));
  const delta = point - forecast.pointEstimate;
  const epsilon = 0.1;

  return {
    variantId: "bls-implied-2026-annual-baseline",
    label: "BLS-implied 2026 baseline",
    description:
      "Derived near-term annual baseline: apply BLS 2024-2034 projected growth rate to the latest OEWS level.",
    pointEstimate: point,
    ciLow: point - epsilon,
    ciHigh: point + epsilon,
    confidence: 1,
    drivers: [
      "BLS 2024-2034 occupational projection growth rate",
      "Latest OEWS annual occupation level",
      "Linear near-term benchmark for annual OEWS comparison",
    ],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2025-08-28T10:00:00-04:00",
      agent: "BLS Employment Projections",
      model: "BLS 2024-2034 projection release, OEWS-compatible interpolation",
      sourceContext: [
        "BLS Employment Projections Table 1.2 occupational projections and worker characteristics",
        "BLS May 2025 National Occupational Employment and Wage Estimates",
      ],
      runLabel: "BLS-implied 2026 baseline",
      runDescription:
        "Not an official BLS 2026 point forecast; derived from BLS projected 2024-2034 growth applied to the latest OEWS annual level.",
    },
    reasoning: [
      {
        kind: "heading",
        text: "BLS-implied annual comparator",
      },
      {
        kind: "text",
        text:
          "BLS does not publish an official May 2026 OEWS forecast. This baseline keeps the annual OEWS resolver but uses the BLS 2024-2034 major-group growth rate as the outside-view annual path.",
      },
      {
        kind: "tool",
        tool: "bls.employment_projections.lookup",
        call: `bls.employment_projections.lookup({ table: "1.2", window: "2024-2034", occupation: "${baseline.socCode}" })`,
        result: `{ employment_2024_thousands: ${baseline.employment2024}, projected_2034_thousands: ${baseline.blsProjection2034}, projected_growth_percent: ${formatSignedPlain(baseline.blsPercentChange)}, annualized_growth_percent: ${formatSignedPlain(roundOneDecimal(annualGrowthRate * 100))} }`,
      },
      {
        kind: "math",
        text:
          `Latest OEWS context ${formatThousandsDisplay(latestOews)} * ` +
          `(1 + ${roundOneDecimal(annualGrowthRate * 100)}%) = ` +
          `${formatThousandsDisplay(point)}; delta versus Brier no-pack ${formatThousandsDisplay(delta)}.`,
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

function withBls2034ComparisonRuns(forecast: ForecastCell): ForecastCell {
  const definition = BLS_2034_OCCUPATION_DEFINITIONS.find(
    (candidate) => candidate.slug === forecast.slug,
  );
  if (!definition) return forecast;

  return {
    ...forecast,
    comparisonRuns: [
      ...(forecast.comparisonRuns ?? []),
      buildBls2034PackedRun(forecast, definition),
      buildBlsPublishedProjectionRun(forecast, definition),
    ],
  };
}

function buildBls2034PackedRun(
  forecast: ForecastCell,
  definition: Bls2034OccupationDefinition,
): ForecastComparisonRun {
  const packAdjustment = definition.packPointEstimate - forecast.pointEstimate;
  const blsDelta = definition.packPointEstimate - definition.blsProjection2034;

  return {
    variantId: "with-bls-employment-projections",
    label: "Brier long-run - BLS pack",
    description:
      "Same 2034 target after admitting the official BLS 2024-2034 projection as a baseline pack.",
    pointEstimate: definition.packPointEstimate,
    ciLow: definition.packCiLow,
    ciHigh: definition.packCiHigh,
    drivers: [
      ...forecast.drivers,
      "BLS 2024-2034 occupational employment projection baseline",
    ],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-06-21T22:35:00-04:00",
      agent: "brier-occupation-automation-scenarios",
      model: "Codex recorded source-context synthesis",
      sourceContext: [
        "BLS Employment Projections Table 1.2, 2024-2034",
        "BLS National Employment Matrix base-year methodology",
        "Task automation exposure literature",
        "AI adoption and labor-demand scenario notes",
      ],
      runLabel: "Brier long-run - BLS pack",
      runDescription:
        "Brier occupation scenario with the BLS 2024-2034 projection baseline admitted as a pack.",
      packSet: BLS_EMPLOYMENT_PROJECTIONS_PACK_SET,
    },
    reasoning: [
      {
        kind: "heading",
        text: "BLS projection pack on the 2034 target",
      },
      {
        kind: "text",
        text:
          "This run is apples-to-apples with the published BLS projection: same SOC major group, same employment-in-thousands unit, and same future BLS National Employment Matrix 2034 base-year resolver.",
      },
      {
        kind: "tool",
        tool: "bls.employment_projections.lookup",
        call: `bls.employment_projections.lookup({ table: "1.2", window: "2024-2034", occupation: "${definition.socCode}" })`,
        result: formatBlsProjectionResult(definition),
      },
      {
        kind: "tool",
        tool: "brier.pack.apply",
        call: 'brier.pack.apply({ packs: ["bls-employment-projections-baseline@0.1.0"], role: "same_target_baseline" })',
        result: `{ admitted: 1, mode: 'with_packs', no_pack_point_thousands: ${forecast.pointEstimate}, pack_adjustment_thousands: ${formatSignedPlain(packAdjustment)}, packed_point_thousands: ${definition.packPointEstimate}, packed_delta_vs_bls_projection_thousands: ${formatSignedPlain(blsDelta)} }`,
      },
      {
        kind: "math",
        text: `No-pack Brier ${formatThousandsDisplay(forecast.pointEstimate)} + BLS pack adjustment ${formatThousandsDisplay(packAdjustment)} = ${formatThousandsDisplay(definition.packPointEstimate)}.`,
      },
      {
        kind: "text",
        text: definition.packRationale,
      },
      {
        kind: "forecast",
        point: definition.packPointEstimate,
        ciLow: definition.packCiLow,
        ciHigh: definition.packCiHigh,
      },
    ],
  };
}

function buildBlsPublishedProjectionRun(
  forecast: ForecastCell,
  definition: Bls2034OccupationDefinition,
): ForecastComparisonRun {
  const point = definition.blsProjection2034;
  const epsilon = 0.1;

  return {
    variantId: "bls-published-2024-2034-projection",
    label: "BLS published projection",
    description:
      "BLS 2024-2034 Table 1.2 point projection recorded as a baseline forecast on the same 2034 target.",
    pointEstimate: point,
    ciLow: point - epsilon,
    ciHigh: point + epsilon,
    confidence: 1,
    drivers: [
      "BLS National Employment Matrix",
      "BLS 2024-2034 employment projection model",
      "Published Table 1.2 major occupational group baseline",
    ],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2025-08-28T10:00:00-04:00",
      agent: "BLS Employment Projections",
      model: "BLS 2024-2034 projection release",
      sourceContext: [
        "BLS Employment Projections Table 1.2 occupational projections and worker characteristics",
      ],
      runLabel: "BLS published projection",
      runDescription:
        "Official BLS 2024-2034 point projection, recorded for apples-to-apples comparison against Brier runs.",
    },
    reasoning: [
      {
        kind: "heading",
        text: "BLS published baseline",
      },
      {
        kind: "text",
        text:
          "BLS publishes a point projection, not a full public uncertainty distribution. Thesis records it with an effectively point-mass display interval so it can sit beside the Brier distributions and later be scored on the same target.",
      },
      {
        kind: "tool",
        tool: "bls.employment_projections.lookup",
        call: `bls.employment_projections.lookup({ table: "1.2", window: "2024-2034", occupation: "${definition.socCode}" })`,
        result: formatBlsProjectionResult(definition),
      },
      {
        kind: "math",
        text: `BLS projected ${formatThousandsDisplay(point)} in 2034, a ${formatThousandsDisplay(definition.blsNumericChange)} change from ${formatThousandsDisplay(definition.employment2024)} in 2024 (${formatSignedPlain(definition.blsPercentChange)}%).`,
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

function formatBlsProjectionResult(
  definition: Bls2034OccupationDefinition,
): string {
  return `{ occupation_group: '${definition.socCode}', employment_2024_thousands: ${definition.employment2024}, projected_2034_thousands: ${definition.blsProjection2034}, change_thousands: ${formatSignedPlain(definition.blsNumericChange)}, change_percent: ${formatSignedPlain(definition.blsPercentChange)} }`;
}

function formatSignedPlain(value: number) {
  if (value === 0) return "0";
  return `${value > 0 ? "+" : ""}${value}`;
}

function roundOneDecimal(value: number) {
  return Math.round(value * 10) / 10;
}

function roundToNearestTen(value: number) {
  return Math.round(value / 10) * 10;
}

function formatThousandsDisplay(value: number) {
  if (Math.abs(value) >= 1000) {
    return `${(value / 1000).toLocaleString(undefined, {
      maximumFractionDigits: 2,
      minimumFractionDigits: Math.abs(value) >= 10000 ? 2 : 1,
    })}m`;
  }
  return `${formatSignedPlain(value)}k`;
}
