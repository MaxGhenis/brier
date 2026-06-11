// Forecast-cell definitions and AI analyst reasoning scripts.
// Each cell is a self-contained record with a pre-written reasoning stream
// that the AgentReasoning component plays back with simulated streaming.
//
// The reasoning is illustrative — numbers and tool-call results are
// constructed to demonstrate the integrated stack (encoded law,
// PolicyEngine microsim, public data cells) rather than to be live forecasts.

import { BENEFITS_DELIVERY_MARKETS } from "./benefitsDeliveryMarkets";

export type MarketType = "data" | "policy" | "conditional";

export type Unit =
  | "percent"
  | "usd"
  | "usd_billions"
  | "usd_monthly"
  | "millions"
  | "ratio"
  | "percent_growth";

export interface HistoricalPoint {
  label: string;
  value: number;
}

export type ReasoningStep =
  | { kind: "heading"; text: string }
  | { kind: "text"; text: string }
  | {
      kind: "tool"; // call to PolicyEngine microsim or other data lookup
      call: string;
      result: string;
      tool?: string; // optional tool name override; defaults to policyengine.simulate
    }
  | { kind: "math"; text: string } // styled equation/weighting line
  | { kind: "forecast"; point: number; ciLow: number; ciHigh: number };

export interface Market {
  slug: string;
  type: MarketType;
  title: string;
  question: string;
  unit: Unit;
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  confidence: number; // 0.80 etc.
  resolutionDate: string; // ISO date, e.g. "2027-09-15"
  resolutionSource: string;
  resolutionRule: string;
  historicalContext: HistoricalPoint[];
  drivers: string[];
  dataPointId?: string; // for published public-data forecast cells
  policyParameter?: string; // for policy forecast cells
  conditionalOn?: string; // for conditional forecast cells
  reasoning: ReasoningStep[];
}

export type ForecastRuntimeKind = "live-api" | "static-mock";

export const LIVE_FORECAST_SLUGS = new Set([
  "spm-child-poverty-2025",
  "cpi-u-annual-2026",
  "ctc-expansion-cost-ty2026",
  "ctc-current-law-outlays-ty2026",
]);

export function getForecastRuntimeKind(slug: string): ForecastRuntimeKind {
  return LIVE_FORECAST_SLUGS.has(slug) ? "live-api" : "static-mock";
}

export function getForecastRuntimeLabel(slug: string): string {
  return getForecastRuntimeKind(slug) === "live-api"
    ? "Live API path"
    : "Static mock trace";
}

export const MARKETS: Market[] = [
  // ─── Government data cells ───────────────────────────────────────────────
  {
    slug: "spm-child-poverty-2025",
    type: "data",
    title: "SPM child poverty rate, 2025",
    question:
      "What will the Supplemental Poverty Measure child poverty rate be for calendar year 2025 as published by the U.S. Census Bureau?",
    unit: "percent",
    pointEstimate: 13.1,
    ciLow: 12.0,
    ciHigh: 14.4,
    confidence: 0.8,
    resolutionDate: "2026-09-15",
    resolutionSource: "U.S. Census Bureau, Poverty in the United States: 2025",
    resolutionRule:
      "Resolves to the official SPM child poverty rate (children under 18) for calendar year 2025 in the Census Poverty in the United States report, expected in September 2026. If Census publishes multiple SPM variants, this uses the main published SPM table.",
    dataPointId: "census.spm.child_poverty_rate.2025",
    historicalContext: [
      { label: "2021", value: 5.2 },
      { label: "2022", value: 12.4 },
      { label: "2023", value: 13.7 },
      { label: "2024", value: 13.4 },
    ],
    drivers: [
      "CTC and EITC current-law parameters",
      "2025 labor-market strength",
      "Shelter and medical out-of-pocket costs",
      "SNAP and school-meals resources",
    ],
    reasoning: [
      { kind: "heading", text: "Near-term Census target" },
      {
        kind: "text",
        text: "This is deliberately near-term: Census typically releases annual income, poverty, health insurance, and SPM estimates in September for the prior calendar year. The 2025 SPM child poverty rate should therefore resolve in September 2026, making it a useful early calibration target.",
      },
      { kind: "heading", text: "PolicyEngine baseline" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "current_law", year: 2025, output: "spm_child_poverty_rate", map_to: "person", population: "microplex.us.2025" })',
        result:
          '{ point: 13.0, ci80: [12.1, 14.1], drivers: ["ctc_refundability", "earnings", "housing_costs"] }',
      },
      {
        kind: "tool",
        tool: "census.lookup",
        call: 'census.lookup({ report: "Poverty in the United States", series: "spm_child_poverty_rate", years: [2021, 2024] })',
        result:
          "{ ty2021_expanded_ctc: 5.2, ty2022: 12.4, ty2023: 13.7, ty2024: 13.4 }",
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The 2025 law and macro environment look much closer to 2022-2024 than to the 2021 expanded-CTC year. The point estimate sits slightly below 2024 because employment and real earnings improved, while the upper tail keeps room for housing and medical expense pressure in the SPM resource calculation.",
      },
      { kind: "forecast", point: 13.1, ciLow: 12.0, ciHigh: 14.4 },
    ],
  },

  {
    slug: "official-poverty-rate-2025",
    type: "data",
    title: "Official poverty rate, 2025",
    question:
      "What will the official U.S. poverty rate be for calendar year 2025 as published by the U.S. Census Bureau?",
    unit: "percent",
    pointEstimate: 10.4,
    ciLow: 9.8,
    ciHigh: 11.1,
    confidence: 0.8,
    resolutionDate: "2026-09-15",
    resolutionSource: "U.S. Census Bureau, Poverty in the United States: 2025",
    resolutionRule:
      "Resolves to the official poverty rate for all people in calendar year 2025 in the Census Poverty in the United States report, expected in September 2026. This uses the official poverty measure, not the Supplemental Poverty Measure.",
    dataPointId: "census.official_poverty_rate.2025",
    historicalContext: [
      { label: "2021", value: 11.6 },
      { label: "2022", value: 11.5 },
      { label: "2023", value: 11.1 },
      { label: "2024", value: 10.6 },
    ],
    drivers: [
      "Pretax cash income growth",
      "Employment and hours worked",
      "Household composition",
      "CPI-U poverty-threshold indexation",
    ],
    reasoning: [
      { kind: "heading", text: "Cash-income target" },
      {
        kind: "text",
        text: "The official poverty measure excludes taxes, refundable credits, and noncash benefits, so it is a cleaner near-term read on cash-income and labor-market strength than SPM.",
      },
      {
        kind: "tool",
        tool: "census.lookup",
        call: 'census.lookup({ report: "Poverty in the United States", series: "official_poverty_rate", years: [2021, 2024] })',
        result: "{ y2021: 11.6, y2022: 11.5, y2023: 11.1, y2024: 10.6 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "current_law", year: 2025, output: "official_poverty_rate", map_to: "person", income_definition: "cash_income" })',
        result:
          '{ point: 10.5, ci80: [9.9, 11.0], drivers: ["earnings", "social_security_income", "threshold_indexation"] }',
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The central path continues the 2023-2024 improvement but slows it. A recession would have shown more clearly in the 2025 labor market by now, so the upper tail is moderate rather than extreme.",
      },
      { kind: "forecast", point: 10.4, ciLow: 9.8, ciHigh: 11.1 },
    ],
  },

  {
    slug: "median-household-income-2025",
    type: "data",
    title: "Median household income, 2025",
    question:
      "What will real median household income be for calendar year 2025 as published by the U.S. Census Bureau?",
    unit: "usd",
    pointEstimate: 80600,
    ciLow: 78600,
    ciHigh: 82900,
    confidence: 0.8,
    resolutionDate: "2026-09-15",
    resolutionSource: "U.S. Census Bureau, Income in the United States: 2025",
    resolutionRule:
      "Resolves to the real median household income for calendar year 2025 in the Census Income in the United States report, expected in September 2026, expressed in 2025 dollars or the headline real-dollar basis used by Census.",
    dataPointId: "census.asec.median_household_income.2025",
    historicalContext: [
      { label: "2021", value: 76330 },
      { label: "2022", value: 77540 },
      { label: "2023", value: 80610 },
      { label: "2024", value: 80100 },
    ],
    drivers: [
      "Real wage growth",
      "Employment-to-population ratio",
      "Household composition",
      "ASEC sampling error",
    ],
    reasoning: [
      { kind: "heading", text: "Near-term income benchmark" },
      {
        kind: "text",
        text: "Median household income is one of the fastest-resolving economic well-being targets in the catalog. The 2025 ASEC release gives a near-term check on the income side of the poverty forecasts.",
      },
      {
        kind: "tool",
        tool: "census.lookup",
        call: 'census.lookup({ report: "Income in the United States", series: "real_median_household_income", years: [2021, 2024] })',
        result:
          "{ y2021: 76330, y2022: 77540, y2023: 80610, y2024_estimate: 80100 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_macro", year: 2025, output: "median_household_income_real", source: "asec" })',
        result:
          '{ point: 80700, ci80: [78900, 82700], drivers: ["real_wages", "employment", "household_composition"] }',
      },
      {
        kind: "text",
        text: "The central estimate is nearly flat versus 2024: real wage gains help, but household composition and ASEC sampling noise can move the published median by more than the underlying economic trend.",
      },
      { kind: "forecast", point: 80600, ciLow: 78600, ciHigh: 82900 },
    ],
  },

  {
    slug: "spm-child-poverty-2027",
    type: "data",
    title: "SPM child poverty rate, 2027",
    question:
      "What will the Supplemental Poverty Measure child poverty rate be for calendar year 2027 as published by the U.S. Census Bureau?",
    unit: "percent",
    pointEstimate: 11.8,
    ciLow: 10.5,
    ciHigh: 13.4,
    confidence: 0.8,
    resolutionDate: "2028-09-15",
    resolutionSource: "U.S. Census Bureau, SPM annual release",
    resolutionRule:
      "Resolves to the official SPM child poverty rate (children under 18) published in the Census Poverty in the United States report covering CY2027.",
    dataPointId: "census.spm.child_poverty_rate.2027",
    historicalContext: [
      { label: "2021", value: 5.2 },
      { label: "2022", value: 12.4 },
      { label: "2023", value: 13.7 },
      { label: "2024", value: 13.4 },
      { label: "2025e", value: 12.9 },
    ],
    drivers: [
      "TCJA extension status (CTC, EITC)",
      "Unemployment trajectory",
      "SNAP benefit levels",
      "Refundable credit phase-ins",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "The SPM child poverty rate for 2027 is dominated by the configuration of refundable credits under whatever tax regime is in force, plus the labor market. The CTC is the single largest policy lever — it directly raised the CTC sensitivity of SPM child poverty by roughly 4 percentage points during the 2021 expansion. The 2027 reading depends critically on how TCJA-extension legislation resolves.",
      },
      { kind: "heading", text: "Running the PolicyEngine microsim" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "current_law_scheduled", year: 2027, output: "spm_child_poverty_rate", population: "microplex.us.2027" })',
        result:
          '{ point: 13.1, ci80: [12.2, 14.0], drivers: ["CTC reverts to $1,000 / child", "EITC expansions sunset", "CTC phase-in unchanged"] }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "tcja_extended_full", year: 2027, output: "spm_child_poverty_rate", population: "microplex.us.2027" })',
        result:
          '{ point: 11.4, ci80: [10.5, 12.4], drivers: ["CTC remains $2,000 / child", "$1,700 refundable portion preserved", "EITC parameters unchanged"] }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "tcja_extended_partial", year: 2027, output: "spm_child_poverty_rate", population: "microplex.us.2027" })',
        result:
          '{ point: 12.2, ci80: [11.3, 13.1], drivers: ["CTC at $1,500 / child", "refundability cap retained", "EITC reverts"] }',
      },
      { kind: "heading", text: "Macro and external inputs" },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "budget_economic_outlook_2026", series: "unemployment_rate", year: 2027 })',
        result: "{ baseline: 4.2%, range: [3.8%, 4.7%] }",
      },
      {
        kind: "text",
        text: "Labor-market path is close to neutral for child poverty at this baseline — the 4.2% projected 2027 unemployment rate is near the historical average and the simulation shows ±0.3pp on child poverty over the [3.8%, 4.7%] band.",
      },
      { kind: "heading", text: "Legislative weighting" },
      {
        kind: "text",
        text: "House passed a TCJA extension package in March. Senate markup is expected Q3. Conditional on the Senate moving a vehicle, full extension is the modal outcome but partial scaling (especially on CTC refundability) is a live possibility. Weighting:",
      },
      {
        kind: "math",
        text: "P(full TCJA extension) = 0.65 · P(partial extension) = 0.20 · P(expiration) = 0.15",
      },
      {
        kind: "math",
        text: "E[SPM child poverty 2027] = 0.65·11.4 + 0.20·12.2 + 0.15·13.1 = 11.83",
      },
      { kind: "heading", text: "Forecast" },
      { kind: "forecast", point: 11.8, ciLow: 10.5, ciHigh: 13.4 },
    ],
  },

  {
    slug: "unemployment-dec-2026",
    type: "data",
    title: "Unemployment rate, December 2026",
    question:
      "What will the seasonally-adjusted U.S. civilian unemployment rate be for December 2026 as published in the BLS Employment Situation release?",
    unit: "percent",
    pointEstimate: 4.3,
    ciLow: 3.9,
    ciHigh: 4.8,
    confidence: 0.8,
    resolutionDate: "2027-01-09",
    resolutionSource: "BLS Employment Situation (CES/CPS)",
    resolutionRule:
      "Resolves to the first-print seasonally-adjusted U-3 unemployment rate for December 2026, released on the first Friday of January 2027 (subject to revision; first print is the resolution value).",
    dataPointId: "bls.lns14000000.2026-12",
    historicalContext: [
      { label: "Dec 2022", value: 3.5 },
      { label: "Dec 2023", value: 3.7 },
      { label: "Dec 2024", value: 4.1 },
      { label: "Dec 2025", value: 4.2 },
    ],
    drivers: [
      "Fed funds rate path",
      "Goods-sector labor demand",
      "Immigration-adjusted labor force growth",
      "AI-driven displacement vs. productivity",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "Single-month U-3 print, first release. Historically the median absolute monthly change in U-3 is roughly 0.1pp; six-month windows have a median absolute change of 0.3pp. The interesting dispersion is whether 2026 ends in a normal late-cycle drift (4.2 → 4.4) or whether there is enough labor-demand softening to push past 4.6.",
      },
      { kind: "heading", text: "Calling structural and reduced-form models" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_macro", year: 2026, output: "unemployment_rate_monthly", month: 12, model: "structural_var" })',
        result: "{ point: 4.31, ci80: [3.92, 4.74] }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_macro", year: 2026, output: "unemployment_rate_monthly", month: 12, model: "reduced_form_phillips" })',
        result: "{ point: 4.27, ci80: [3.95, 4.61] }",
      },
      { kind: "heading", text: "External baselines" },
      {
        kind: "tool",
        tool: "fed.lookup",
        call: 'fed.lookup({ source: "SEP_dec_2025", variable: "unemployment_rate", year: 2026, statistic: "median" })',
        result: "{ value: 4.3, central_tendency: [4.1, 4.5] }",
      },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "budget_economic_outlook_2026", series: "unemployment_rate", year: 2026 })',
        result: "{ value: 4.4, range: [4.0, 4.8] }",
      },
      {
        kind: "text",
        text: "The FOMC SEP median, CBO projection, and the brier structural-VAR all cluster between 4.27 and 4.40 for full-year 2026. December prints tend to run very slightly below the annual mean in expansions due to seasonal adjustment behavior in the household survey.",
      },
      { kind: "heading", text: "Risk distribution" },
      {
        kind: "text",
        text: "Upside-risk asymmetry is real: cycle endings tend to look like normal drift right up until a discontinuity. The 80% CI should be slightly wider on the high side to reflect that.",
      },
      { kind: "heading", text: "Forecast" },
      { kind: "forecast", point: 4.3, ciLow: 3.9, ciHigh: 4.8 },
    ],
  },

  {
    slug: "cpi-u-annual-2026",
    type: "data",
    title: "CPI-U annual average inflation, 2026",
    question:
      "What will the annual average percent change in CPI-U for calendar year 2026 (vs. 2025 annual average) be, as published by BLS?",
    unit: "percent",
    pointEstimate: 2.6,
    ciLow: 2.1,
    ciHigh: 3.2,
    confidence: 0.8,
    resolutionDate: "2027-01-15",
    resolutionSource: "BLS CPI-U release",
    resolutionRule:
      "Resolves to the percent change in CPI-U annual average for 2026 over 2025 (BLS series CUUR0000SA0, annual average), first-published value.",
    dataPointId: "bls.cpi.u.annual_pct_change.2026",
    historicalContext: [
      { label: "2022", value: 8.0 },
      { label: "2023", value: 4.1 },
      { label: "2024", value: 2.9 },
      { label: "2025e", value: 2.7 },
    ],
    drivers: [
      "Shelter disinflation trajectory",
      "Goods price pass-through from tariffs",
      "Wage growth and unit labor costs",
      "Energy prices",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "Annual-average year-over-year for 2026. Different from December-to-December — the annual-average measure carries more weight on early-year readings (since the level is averaged across 12 months). The H1 2026 trajectory is largely baked in by the time we get to Q3 2026 reads.",
      },
      { kind: "heading", text: "Component decomposition" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_macro", year: 2026, output: "cpi_components", decomposition: true })',
        result:
          "{ shelter: 3.4, services_ex_shelter: 3.1, core_goods: 0.8, food: 2.5, energy: 1.9, weighted_total: 2.62 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "tariff_passthrough_central", year: 2026, output: "cpi_u_annual" })',
        result: "{ point: 2.63, ci80: [2.18, 3.15] }",
      },
      { kind: "heading", text: "Cross-checks" },
      {
        kind: "tool",
        tool: "fed.lookup",
        call: 'fed.lookup({ source: "SEP_dec_2025", variable: "core_pce_inflation", year: 2026, statistic: "median" })',
        result: "{ value: 2.4 }",
      },
      {
        kind: "tool",
        tool: "fed.lookup",
        call: 'fed.lookup({ source: "consensus_blue_chip", variable: "cpi_u_yoy", year: 2026 })',
        result: "{ point: 2.6, dispersion_iqr: [2.4, 2.8] }",
      },
      {
        kind: "text",
        text: "CPI-U typically runs 0.2-0.4pp above core PCE due to shelter weights. A 2.4 core-PCE median translates to roughly 2.7 CPI-U headline before tariff effects. Tariff pass-through to core goods is modest in the central case but is the principal upside-risk channel.",
      },
      { kind: "heading", text: "Skew and forecast" },
      {
        kind: "text",
        text: "Distribution is mildly right-skewed: more upside risk from tariff escalation and energy shocks than downside risk from a sudden disinflationary collapse. CI reflects this.",
      },
      { kind: "forecast", point: 2.6, ciLow: 2.1, ciHigh: 3.2 },
    ],
  },

  {
    slug: "median-household-income-2026",
    type: "data",
    title: "Median household income, 2026",
    question:
      "What will the real (2026 dollars) median household income for the United States be in calendar year 2026, as published in the Census ASEC?",
    unit: "usd",
    pointEstimate: 81200,
    ciLow: 79100,
    ciHigh: 83400,
    confidence: 0.8,
    resolutionDate: "2027-09-15",
    resolutionSource: "Census ASEC (Current Population Survey)",
    resolutionRule:
      "Resolves to the real median household income for 2026 as published in the Census income report, expressed in 2026 dollars.",
    dataPointId: "census.asec.median_household_income.2026",
    historicalContext: [
      { label: "2022", value: 77540 },
      { label: "2023", value: 80610 },
      { label: "2024", value: 80100 },
      { label: "2025e", value: 80600 },
    ],
    drivers: [
      "Real wage growth",
      "Employment-to-population ratio",
      "Household composition shifts",
      "Top-end income trajectory",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "Real median household income, ASEC measure. Tracks real labor earnings of the typical household closely. ASEC sample noise is meaningful at the median (standard error ~$700 historically).",
      },
      { kind: "heading", text: "Decomposed simulation" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_macro", year: 2026, output: "median_household_income_real", source: "asec" })',
        result: "{ point: 81230, ci80: [79140, 83370] }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_macro", year: 2026, output: "real_wage_growth", deciles: true })',
        result: "{ p10: 0.4, p25: 0.6, p50: 0.8, p75: 0.9, p90: 1.0 }",
      },
      { kind: "heading", text: "External anchors" },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "budget_economic_outlook_2026", series: "real_disposable_income_pc", year: 2026 })',
        result: "{ growth: 1.6% }",
      },
      {
        kind: "text",
        text: "Real per-capita disposable income growth in the CBO baseline maps to roughly 0.7–1.0% growth in real median household income (household composition trends are a slight drag). $80,600 base × ~1.0% growth → ~$81,400. The simulation result is consistent.",
      },
      { kind: "heading", text: "Forecast" },
      { kind: "forecast", point: 81200, ciLow: 79100, ciHigh: 83400 },
    ],
  },

  {
    slug: "irs-individual-income-tax-fy2027",
    type: "data",
    title: "Federal individual income tax revenue, FY2027",
    question:
      "What will total federal individual income tax revenue be for fiscal year 2027 in nominal dollars, as published in the Monthly Treasury Statement?",
    unit: "usd",
    pointEstimate: 2740,
    ciLow: 2580,
    ciHigh: 2910,
    confidence: 0.8,
    resolutionDate: "2027-10-20",
    resolutionSource:
      "U.S. Treasury Monthly Statement (final September FY2027)",
    resolutionRule:
      "Resolves to total individual income tax receipts for FY2027 as reported in the Monthly Treasury Statement covering September 2027, in billions of nominal dollars.",
    dataPointId: "treasury.mts.individual_income_tax.fy2027",
    historicalContext: [
      { label: "FY2023", value: 2176 },
      { label: "FY2024", value: 2426 },
      { label: "FY2025e", value: 2520 },
      { label: "FY2026e", value: 2640 },
    ],
    drivers: [
      "TCJA extension status",
      "Capital gains realizations",
      "Nominal income growth",
      "Withholding vs. nonwithheld mix",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "FY2027 means October 2026 through September 2027. The April 2027 final-payment surge dominates the year-over-year variance — that print captures TY2026 returns, which are filed under whatever tax law is in force for TY2026.",
      },
      { kind: "heading", text: "Microsim under each legislative path" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "current_law_scheduled", year: 2027, output: "individual_income_tax_receipts_fy", policy_year: 2026 })',
        result:
          '{ point: 2810, ci80: [2640, 2980], note: "assumes TCJA expires end-2025 → TY2026 under post-TCJA brackets" }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "tcja_extended_full", year: 2027, output: "individual_income_tax_receipts_fy", policy_year: 2026 })',
        result:
          '{ point: 2680, ci80: [2520, 2840], note: "TCJA-permanent brackets, $24K standard deduction, SALT cap" }',
      },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "budget_outlook_2026", series: "individual_income_tax", year: "FY2027", policy: "current_law" })',
        result: "{ value: 2790 }",
      },
      { kind: "heading", text: "Legislative weighting" },
      {
        kind: "math",
        text: "P(TCJA extended fully retroactive to 2026) = 0.55 · P(extended w/ modifications) = 0.25 · P(expiration / partial) = 0.20",
      },
      {
        kind: "math",
        text: "E[FY2027 IIT receipts] = 0.55·2680 + 0.25·2740 + 0.20·2810 = 2735",
      },
      { kind: "heading", text: "Realizations risk" },
      {
        kind: "text",
        text: "Capital-gains realizations are the biggest residual variance — a sustained equity drawdown into 2026 would reduce nonwithheld revenue by $40-90bn. Reflected in the wider downside tail.",
      },
      { kind: "forecast", point: 2740, ciLow: 2580, ciHigh: 2910 },
    ],
  },

  {
    slug: "real-gdp-growth-2026",
    type: "data",
    title: "Real GDP growth, 2026 (Q4/Q4)",
    question:
      "What will real GDP growth be from Q4 2025 to Q4 2026 (year-over-year, fourth-quarter basis), as published by BEA?",
    unit: "percent_growth",
    pointEstimate: 1.9,
    ciLow: 0.9,
    ciHigh: 2.8,
    confidence: 0.8,
    resolutionDate: "2027-01-28",
    resolutionSource: "BEA GDP advance estimate (Q4 2026)",
    resolutionRule:
      "Resolves to the Q4/Q4 real GDP growth rate for 2026 as published in the BEA Q4 2026 advance estimate (late January 2027).",
    dataPointId: "bea.gdpc1.q4q4.2026",
    historicalContext: [
      { label: "2022", value: 0.6 },
      { label: "2023", value: 3.2 },
      { label: "2024", value: 2.5 },
      { label: "2025e", value: 2.1 },
    ],
    drivers: [
      "Business investment in AI / data center buildout",
      "Consumer spending resilience",
      "Net exports under tariff regime",
      "Government spending trajectory",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "Q4/Q4 is the standard FOMC and CBO horizon. Less noisy than single-quarter prints but still subject to substantial revision. Advance estimate is what resolves — the second and third releases come later.",
      },
      { kind: "heading", text: "Structural model + nowcast blend" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_macro", year: 2026, output: "real_gdp_q4q4", model: "structural_neoclassical" })',
        result: "{ point: 1.86, ci80: [1.05, 2.69] }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_macro", year: 2026, output: "real_gdp_q4q4", model: "bayesian_var" })',
        result: "{ point: 1.92, ci80: [0.85, 2.99] }",
      },
      {
        kind: "tool",
        tool: "fed.lookup",
        call: 'fed.lookup({ source: "SEP_dec_2025", variable: "real_gdp_growth", year: 2026, statistic: "median" })',
        result: "{ value: 1.8, central_tendency: [1.5, 2.1] }",
      },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "budget_economic_outlook_2026", series: "real_gdp_q4q4", year: 2026 })',
        result: "{ value: 2.0 }",
      },
      { kind: "heading", text: "Composition" },
      {
        kind: "text",
        text: "Investment composition is unusual — AI-related capex is contributing roughly 0.5pp to real GDP growth on its own. That makes the upside tail wider than typical late-cycle distributions and the downside tail heavier (sudden capex pullback).",
      },
      { kind: "forecast", point: 1.9, ciLow: 0.9, ciHigh: 2.8 },
    ],
  },

  {
    slug: "uninsured-rate-2026",
    type: "data",
    title: "Uninsured rate (under 65), 2026",
    question:
      "What will the uninsured rate among the U.S. population under 65 be for calendar year 2026, as published in the Census ASEC?",
    unit: "percent",
    pointEstimate: 10.1,
    ciLow: 9.2,
    ciHigh: 11.2,
    confidence: 0.8,
    resolutionDate: "2027-09-15",
    resolutionSource: "Census ASEC health insurance report",
    resolutionRule:
      "Resolves to the uninsured rate (any point during the year) for the population under 65 as published in the Census ASEC health insurance coverage report covering CY2026.",
    dataPointId: "census.asec.uninsured_rate_under_65.2026",
    historicalContext: [
      { label: "2021", value: 9.6 },
      { label: "2022", value: 8.6 },
      { label: "2023", value: 8.0 },
      { label: "2024", value: 8.2 },
      { label: "2025e", value: 8.9 },
    ],
    drivers: [
      "ACA enhanced subsidy status",
      "Medicaid unwinding completion",
      "Employer-sponsored coverage trajectory",
      "ACA marketplace enrollment",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "2026 is the first full year after the scheduled expiration of the ACA enhanced premium tax credits (ARPA/IRA). The marketplace-coverage response is the dominant driver. Medicaid unwinding has largely run its course by 2026; ESI is fairly stable.",
      },
      { kind: "heading", text: "Policy-state branches" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "ept_expired", year: 2026, output: "uninsured_rate_under_65" })',
        result:
          '{ point: 10.4, ci80: [9.5, 11.4], drivers: ["~3.8M coverage loss", "net of churn into ESI/Medicaid"] }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "ept_extended", year: 2026, output: "uninsured_rate_under_65" })',
        result: "{ point: 9.0, ci80: [8.2, 9.9] }",
      },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "health_insurance_baseline_2026", series: "uninsured_rate_under_65", year: 2026, policy: "ept_expire" })',
        result: "{ value: 10.6 }",
      },
      { kind: "heading", text: "Legislative weighting" },
      {
        kind: "text",
        text: "Subsidy extension is contested. Standalone-extension bills have not advanced; vehicle is most likely a year-end omnibus or reconciliation. We weight: 25% extension via vehicle, 65% expiration as scheduled, 10% partial extension.",
      },
      {
        kind: "math",
        text: "E[uninsured 2026] = 0.65·10.4 + 0.10·9.7 + 0.25·9.0 = 9.97",
      },
      { kind: "forecast", point: 10.1, ciLow: 9.2, ciHigh: 11.2 },
    ],
  },

  {
    slug: "labor-force-participation-dec-2026",
    type: "data",
    title: "Labor force participation rate, December 2026",
    question:
      "What will the seasonally-adjusted civilian labor force participation rate be for December 2026 as published in the BLS Employment Situation release?",
    unit: "percent",
    pointEstimate: 62.4,
    ciLow: 61.9,
    ciHigh: 62.8,
    confidence: 0.8,
    resolutionDate: "2027-01-09",
    resolutionSource: "BLS Employment Situation",
    resolutionRule:
      "Resolves to the first-print seasonally-adjusted civilian labor force participation rate for December 2026 (BLS series LNS11300000).",
    dataPointId: "bls.lns11300000.2026-12",
    historicalContext: [
      { label: "Dec 2022", value: 62.3 },
      { label: "Dec 2023", value: 62.5 },
      { label: "Dec 2024", value: 62.6 },
      { label: "Dec 2025", value: 62.5 },
    ],
    drivers: [
      "Prime-age participation trend",
      "55+ retirement timing",
      "Immigration-adjusted denominator",
      "Disability and long-COVID trends",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "Aggregate LFPR is mechanically dragged down by demographic aging (~0.15pp/year) and pushed up by rising prime-age participation. The net has been roughly flat at 62.5 for two years. The interesting question is whether 2026 holds the line or starts to slip on demographics.",
      },
      { kind: "heading", text: "Decomposition" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_demographics", year: 2026, output: "lfpr_decomposition_dec" })',
        result:
          "{ prime_age_25_54: 83.6, age_55_plus: 38.2, aggregate: 62.42, aging_drag_yoy: -0.13 }",
      },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "budget_economic_outlook_2026", series: "labor_force_participation_rate", year: 2026 })',
        result: "{ value: 62.3 }",
      },
      {
        kind: "text",
        text: "CBO baseline implies a small slip from 62.5 to 62.3. Our prime-age trajectory is slightly more optimistic — recent vintages of the BLS data show 25-54 LFPR holding above 83.5. Net: 62.4 is the central case for December.",
      },
      { kind: "heading", text: "Forecast" },
      { kind: "forecast", point: 62.4, ciLow: 61.9, ciHigh: 62.8 },
    ],
  },

  {
    slug: "snap-payment-error-rate-fy2025",
    type: "data",
    title: "SNAP payment error rate, FY 2025",
    question:
      "What will the national SNAP payment error rate be for fiscal year 2025, as published in the USDA FNS quality control release?",
    unit: "percent",
    pointEstimate: 10.2,
    ciLow: 9.3,
    ciHigh: 11.2,
    confidence: 0.8,
    resolutionDate: "2026-06-30",
    resolutionSource: "USDA FNS, SNAP Quality Control Payment Error Rates, FY 2025",
    resolutionRule:
      "Resolves to the national combined SNAP payment error rate (overpayments plus underpayments) for fiscal year 2025 in the official FNS QC release, first print. FNS released the FY 2024 rate on June 30, 2025; the FY 2025 release is expected around June 2026.",
    dataPointId: "fns.snap.total_payment_error_rate.us.fy2025",
    historicalContext: [
      { label: "FY 2023", value: 11.68 },
      { label: "FY 2024", value: 10.93 },
    ],
    drivers: [
      "OBBBA ties future state cost share to error rates, raising state stakes",
      "State QC investment and corrective action plans",
      "High-error states (Alaska, South Carolina) on steep improvement paths",
      "Caseload churn and policy volatility during FY 2025",
    ],
    reasoning: [
      { kind: "heading", text: "Why this number now moves state budgets" },
      {
        kind: "text",
        text: "The 2025 reconciliation law ties future state cost sharing for SNAP benefits to each state's payment error rate, converting a once-obscure QC statistic into a direct budget exposure. States responded with corrective action plans and QC staffing. This cell is the accuracy pillar of the benefits delivery scorecard.",
      },
      {
        kind: "tool",
        tool: "ledger.lookup",
        call: 'ledger.lookup({ source_record_id: "fns.snap.total_payment_error_rate.us.fy2024.official_release" })',
        result:
          '{ value: 10.93, unit: "percent", observed_at: "2025-06-30", source: "FNS SNAP Payment Error Rates, FY 2024" }',
      },
      {
        kind: "tool",
        tool: "fns.lookup",
        call: 'fns.lookup({ series: "national_payment_error_rate", years: ["fy2023", "fy2024"] })',
        result: "{ fy2023: 11.68, fy2024: 10.93 }",
      },
      {
        kind: "math",
        text: "Trend: 11.68 → 10.93 (−0.75pp). Cost-share incentive adds state-level downward pressure; QC arbitration disputes add first-print noise in both directions.",
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "Continued decline is the modal path: the FY 2024 drop predates the strongest incentives, and several high-error states have already demonstrated large single-year improvements. The upper tail covers QC sampling noise and caseload churn; sub-9 would require improvement at a pace no recent year has shown.",
      },
      { kind: "forecast", point: 10.2, ciLow: 9.3, ciHigh: 11.2 },
    ],
  },

  {
    slug: "ca-medicaid-procedural-disenrollment-share-aug-2026",
    type: "data",
    title: "California Medicaid procedural disenrollment share, August 2026",
    question:
      "What share of California Medicaid beneficiaries disenrolled at renewal in the August 2026 reporting period will be disenrolled for procedural reasons, per the CMS eligibility processing dataset?",
    unit: "percent",
    pointEstimate: 93.0,
    ciLow: 88.5,
    ciHigh: 95.5,
    confidence: 0.8,
    resolutionDate: "2026-12-15",
    resolutionSource:
      "CMS, State Medicaid and CHIP Eligibility Processing Data (data.medicaid.gov)",
    resolutionRule:
      "Resolves to beneficiaries disenrolled for procedural reasons divided by total beneficiaries disenrolled at renewal, California, August 2026 reporting period, original (O) submission row in CMS dataset 5abea2e0-3f8e-4b49-a50d-d63d5fd9103c, computed when CMS first publishes the row (expected roughly three to four months after the period).",
    dataPointId: "cms.medicaid_pi.procedural_disenrollment_share.california.aug_2026",
    historicalContext: [
      { label: "May 25", value: 62.9 },
      { label: "Aug 25", value: 83.8 },
      { label: "Nov 25", value: 89.7 },
      { label: "Feb 26", value: 92.7 },
    ],
    drivers: [
      "Ex parte renewal expansion via CalSAWS data matching",
      "Composition: automation clears the determinably eligible, so residual disenrollments skew procedural",
      "Notice redesign and renewal outreach efforts",
      "Month-to-month renewal cohort mix",
    ],
    reasoning: [
      { kind: "heading", text: "The churn metric" },
      {
        kind: "text",
        text: "Procedural disenrollment is the canonical churn statistic: people losing coverage over paperwork rather than ineligibility. It is the trust-and-power pillar of the benefits delivery scorecard, and California is the largest single series in the CMS eligibility processing data.",
      },
      {
        kind: "tool",
        tool: "ledger.lookup",
        call: 'ledger.lookup({ source_record_id: "cms.medicaid_pi.beneficiaries_disenrolled_procedural.california.feb_2026.original_submission" })',
        result: '{ value: 197693, unit: "count", period: "2026-02" }',
      },
      {
        kind: "tool",
        tool: "ledger.lookup",
        call: 'ledger.lookup({ source_record_id: "cms.medicaid_pi.beneficiaries_disenrolled_total.california.feb_2026.original_submission" })',
        result: '{ value: 213206, unit: "count", period: "2026-02" }',
      },
      {
        kind: "math",
        text: "February 2026: 197,693 / 213,206 = 92.7%. Trailing series: 62.9 (May 25) → 83.8 (Aug 25) → 89.7 (Nov 25) → 92.7 (Feb 26) — rising, decelerating.",
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The mechanism is compositional: as ex parte automation renews the determinably eligible without paperwork, the people who still lose coverage are increasingly those who missed a form. That pushes the share toward an asymptote in the mid-90s. The downside tail covers notice reforms or an eligibility-policy change that grows the determined-ineligible denominator.",
      },
      { kind: "forecast", point: 93.0, ciLow: 88.5, ciHigh: 95.5 },
    ],
  },

  // ─── Policy state forecast cells ─────────────────────────────────────────
  {
    slug: "ctc-monthly-max-ty2027",
    type: "policy",
    title: "CTC monthly maximum per child, TY2027",
    question:
      "What will the maximum federal Child Tax Credit per qualifying child be in tax year 2027, on a monthly equivalent basis?",
    unit: "usd_monthly",
    pointEstimate: 183,
    ciLow: 83,
    ciHigh: 250,
    confidence: 0.8,
    resolutionDate: "2027-04-15",
    resolutionSource: "Internal Revenue Code §24 as enacted",
    resolutionRule:
      "Resolves to the maximum federal CTC per qualifying child in effect for TY2027, divided by 12. Resolution snapshot is taken as of the IRS Form 1040 instructions published for TY2027 returns (April 2028).",
    policyParameter: "irc.24.maximum_per_child.2027",
    historicalContext: [
      { label: "2021", value: 300 },
      { label: "2022", value: 167 },
      { label: "2024", value: 167 },
      { label: "2025", value: 167 },
      { label: "2026e", value: 167 },
    ],
    drivers: [
      "TCJA permanence package status",
      "Refundability provisions in extension bill",
      "Bipartisan child-credit deal trajectory",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "Maximum is the headline parameter — refundability and phase-in are separate forecast cells. Current law: $2,000/child through TY2025, reverting to $1,000/child in TY2026 absent legislation. Any TCJA extension would lock at $2,000 (= $167/mo) or higher.",
      },
      { kind: "heading", text: "Law-encoded policy paths" },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.24", parameter: "maximum_per_child", year: 2027, branch: "current_law" })',
        result: '{ value: 1000, source: "PL 115-97 §11022 sunset" }',
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.24", parameter: "maximum_per_child", year: 2027, branch: "tcja_permanent_house_pass" })',
        result: '{ value: 2000, source: "HR 1234 §103" }',
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.24", parameter: "maximum_per_child", year: 2027, branch: "bipartisan_expansion_b" })',
        result:
          '{ value: 2500, source: "draft S amendment, Wyden-Crapo framework" }',
      },
      { kind: "heading", text: "Legislative probability weighting" },
      {
        kind: "math",
        text: "P(TCJA extended at $2,000) = 0.55 · P(expanded to $2,500+) = 0.20 · P(reversion to $1,000) = 0.20 · P(other) = 0.05",
      },
      {
        kind: "math",
        text: "E[max CTC TY2027 monthly] = (0.55·2000 + 0.20·2500 + 0.20·1000 + 0.05·1500) / 12 = $183/mo",
      },
      { kind: "heading", text: "Distribution shape" },
      {
        kind: "text",
        text: "Bimodal in spirit — mass at $1,000 (revert) and $2,000 (extend), with thin tails. Single-number CI obscures this; the 80% CI is wide to reflect the bimodality.",
      },
      { kind: "forecast", point: 183, ciLow: 83, ciHigh: 250 },
    ],
  },

  {
    slug: "ctc-expansion-cost-ty2026",
    type: "policy",
    title: "Cost of a $3,000 fully refundable CTC, TY2026",
    question:
      "What will official scorers estimate as the federal budget cost of a $3,000 fully refundable Child Tax Credit for tax year 2026, relative to current law?",
    unit: "usd_billions",
    pointEstimate: 109.6,
    ciLow: 78.8,
    ciHigh: 140.4,
    confidence: 0.8,
    resolutionDate: "2027-12-31",
    resolutionSource:
      "Joint Committee on Taxation or Congressional Budget Office",
    resolutionRule:
      "Resolves to the first official JCT or CBO estimate, in billions of nominal dollars, for the tax-year 2026 federal budget effect of a materially equivalent $3,000 fully refundable Child Tax Credit scored against current law.",
    policyParameter: "gov.irs.credits.ctc.refundable.fully_refundable",
    historicalContext: [
      { label: "PE prior", value: 102 },
      { label: "Calibrated", value: 109.6 },
    ],
    drivers: [
      "PolicyEngine raw economy impact",
      "Official-score calibration",
      "Refundability and phase-in design",
      "Eligible child population and filing behavior",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "This cell asks for the official-score cost of a concrete CTC design, not just PolicyEngine's raw microsimulation output. The forecast starts from PolicyEngine because it encodes the law and the population model, then adjusts that result toward the target that will actually resolve.",
      },
      { kind: "heading", text: "Calling PolicyEngine" },
      {
        kind: "tool",
        tool: "policyengine.api",
        call: 'policyengine.economy({ policy: 29093, baseline: 2, region: "us", time_period: 2026 })',
        result:
          '{ policy: "$3,000 Fully Refundable Child Tax Credit", baseline: "Current law", status: "computing", raw_budget_impact_billions: null }',
      },
      { kind: "heading", text: "Calibration layer" },
      {
        kind: "tool",
        tool: "brier.calibration",
        call: 'brier.calibration.lookup({ domain: "policyengine_budget_scores", policy_area: "ctc", outcome: "federal_budget_cost" })',
        result:
          "{ raw_to_final_ratio: 1.04, additive_billions: 3.5, queued_uncertainty_multiplier: 1.4 }",
      },
      {
        kind: "math",
        text: "calibrated cost = raw_or_prior × 1.04 + $3.5B = $109.6B",
      },
      {
        kind: "text",
        text: "The key move is calibration: the AI is allowed to learn where PolicyEngine tends to differ from official scores by policy area, variable, population, and time horizon. That turns PolicyEngine into a disciplined input rather than an oracle.",
      },
      { kind: "heading", text: "Forecast" },
      { kind: "forecast", point: 109.6, ciLow: 78.8, ciHigh: 140.4 },
    ],
  },

  {
    slug: "ctc-current-law-outlays-ty2026",
    type: "policy",
    title: "CTC outlays under current law, TY2026",
    question:
      "What will federal Child Tax Credit outlays be for tax year 2026 under current law, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 60.5,
    ciLow: 52.0,
    ciHigh: 70.0,
    confidence: 0.8,
    resolutionDate: "2028-08-31",
    resolutionSource:
      "IRS Statistics of Income and Treasury tax expenditure tables",
    resolutionRule:
      "Resolves to federal outlays/refundable-credit cost attributable to the Child Tax Credit for tax year 2026, in billions of nominal dollars, using the first official IRS/Treasury table that separately identifies the CTC.",
    policyParameter: "gov.irs.credits.ctc",
    historicalContext: [
      { label: "TY2021", value: 150 },
      { label: "TY2022", value: 68 },
      { label: "TY2024", value: 59 },
      { label: "TY2025e", value: 61 },
    ],
    drivers: [
      "Qualifying-child population",
      "Refundable portion and phase-in",
      "Filing and take-up behavior",
      "Income distribution around phase-outs",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "This is the baseline CTC outlay cell the expansion-cost forecast compares against. It needs a tax-year measure, not a fiscal-year cash-flow proxy, because official outlay timing can shift refunds across fiscal years.",
      },
      { kind: "heading", text: "PolicyEngine baseline" },
      {
        kind: "tool",
        tool: "policyengine.simulate",
        call: 'policyengine.simulate({ policy: "current_law", year: 2026, output: "ctc_outlays", unit: "billions" })',
        result:
          '{ point: 58.8, ci80: [54.0, 64.5], drivers: ["eligible children", "refundability cap", "phase-in earnings"] }',
      },
      {
        kind: "tool",
        tool: "brier.calibration",
        call: 'brier.calibration.lookup({ domain: "policyengine_budget_scores", policy_area: "ctc", target: "irs_soi_outlays" })',
        result:
          "{ ratio: 1.02, additive_billions: 0.5, widened_for_reporting_lag: true }",
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The raw model sits just below the public tax-expenditure trend. Calibration nudges the point estimate upward and keeps the interval wide enough for filing-year timing and SOI classification differences.",
      },
      { kind: "forecast", point: 60.5, ciLow: 52.0, ciHigh: 70.0 },
    ],
  },

  {
    slug: "eitc-outlays-ty2026",
    type: "policy",
    title: "EITC outlays, TY2026",
    question:
      "What will federal Earned Income Tax Credit outlays be for tax year 2026, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 74.0,
    ciLow: 65.0,
    ciHigh: 84.0,
    confidence: 0.8,
    resolutionDate: "2028-08-31",
    resolutionSource:
      "IRS Statistics of Income and Treasury tax expenditure tables",
    resolutionRule:
      "Resolves to federal outlays/refundable-credit cost attributable to the Earned Income Tax Credit for tax year 2026, in billions of nominal dollars, using the first official IRS/Treasury table that separately identifies the EITC.",
    policyParameter: "gov.irs.credits.eitc",
    historicalContext: [
      { label: "TY2021", value: 63 },
      { label: "TY2022", value: 60 },
      { label: "TY2024", value: 69 },
      { label: "TY2025e", value: 72 },
    ],
    drivers: [
      "Low-wage employment",
      "Number of qualifying children",
      "Self-employment income reporting",
      "Indexation of credit schedules",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "EITC outlays are a high-signal calibration target for PolicyEngine because the law is mechanical but eligibility, earnings reporting, and family composition create persistent model error.",
      },
      { kind: "heading", text: "Microsimulation and calibration" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "current_law", year: 2026, output: "eitc_outlays", unit: "billions" })',
        result:
          '{ point: 72.5, ci80: [66.4, 80.1], drivers: ["wage distribution", "children by tax unit", "phase-in earnings"] }',
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ table: "soi_historical_refundable_credits", credit: "eitc", years: [2021, 2024] })',
        result:
          '{ trend: "nominal growth with stable recipient count", model_gap_prior: "+1.5B" }',
      },
      {
        kind: "math",
        text: "forecast = PolicyEngine baseline + historical SOI calibration = $72.5B + $1.5B = $74.0B",
      },
      { kind: "forecast", point: 74.0, ciLow: 65.0, ciHigh: 84.0 },
    ],
  },

  {
    slug: "salt-40k-cap-revenue-cost-ty2027",
    type: "policy",
    title: "Revenue cost of a $40k SALT cap, TY2027",
    question:
      "If the SALT deduction cap is set at $40,000 for joint filers in tax year 2027, what will the federal individual income tax revenue loss be relative to a $10,000 cap?",
    unit: "usd_billions",
    pointEstimate: 38.0,
    ciLow: 25.0,
    ciHigh: 55.0,
    confidence: 0.8,
    resolutionDate: "2028-12-31",
    resolutionSource:
      "Joint Committee on Taxation or Congressional Budget Office",
    resolutionRule:
      "Resolves to the first official JCT or CBO estimate of the federal individual-income-tax revenue loss, in billions of nominal dollars, from raising the TY2027 joint SALT cap from $10,000 to $40,000 under otherwise comparable law.",
    policyParameter: "irc.164.b.6.cap_joint.2027",
    historicalContext: [
      { label: "$10k cap", value: 0 },
      { label: "$20k est.", value: 18 },
      { label: "$40k est.", value: 38 },
      { label: "no cap est.", value: 93 },
    ],
    drivers: [
      "High-income itemizer distribution",
      "State and local tax growth",
      "Interaction with AMT and standard deduction",
      "Behavioral response in state tax planning",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the policy counterfactual" },
      {
        kind: "text",
        text: "The cell isolates the marginal federal revenue cost of moving from a $10k cap to a $40k cap. It is not the cost of full repeal, and it is highly concentrated among high-income itemizers in high-tax states.",
      },
      { kind: "heading", text: "PolicyEngine score" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ reform: "salt_cap_40k_joint", baseline: "salt_cap_10k_joint", year: 2027, output: "iit_revenue_delta", unit: "billions" })',
        result:
          '{ point: -36.5, ci80: [-49.0, -25.5], drivers: ["AGI distribution", "itemization share", "state tax growth"] }',
      },
      {
        kind: "tool",
        tool: "jct.lookup",
        call: 'jct.lookup({ topic: "salt_cap_options", cap_joint: 40000, year: 2027 })',
        result:
          '{ anchor_range_billions: [34, 44], note: "static score before behavioral uncertainty" }',
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The final forecast takes the magnitude of the PolicyEngine revenue delta, anchors to public score ranges, and widens the upper tail for state-tax behavior and capital-gains sensitivity.",
      },
      { kind: "forecast", point: 38.0, ciLow: 25.0, ciHigh: 55.0 },
    ],
  },

  {
    slug: "federal-minimum-wage-jan-2027",
    type: "policy",
    title: "Federal minimum wage on Jan 1, 2027",
    question:
      "What will the federal minimum wage under FLSA §6(a)(1) be on January 1, 2027?",
    unit: "usd",
    pointEstimate: 7.25,
    ciLow: 7.25,
    ciHigh: 9.5,
    confidence: 0.8,
    resolutionDate: "2027-01-01",
    resolutionSource: "29 U.S.C. §206(a)(1) as enacted",
    resolutionRule:
      "Resolves to the cash wage value of the federal minimum wage on January 1, 2027 under the Fair Labor Standards Act, regardless of any tipped-credit or sub-minimum provisions.",
    policyParameter: "usc.29.206.a.1.2027-01-01",
    historicalContext: [
      { label: "Last increase", value: 7.25 },
      { label: "Since", value: 2009 },
      { label: "2025", value: 7.25 },
      { label: "2026", value: 7.25 },
    ],
    drivers: [
      "Senate filibuster math",
      "Standalone-bill viability",
      "Reconciliation eligibility",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "Federal minimum has been $7.25 since July 2009. Multiple proposals (Raise the Wage Act variants) have failed in Senate cloture. Any change requires 60 votes (it's been ruled non-reconciliation-compliant per Byrd) or filibuster reform.",
      },
      { kind: "heading", text: "Legislative status" },
      {
        kind: "tool",
        tool: "congress.lookup",
        call: 'congress.lookup({ topic: "minimum_wage", session: 119, status: "active" })',
        result:
          '{ bills: [ {id: "HR.42", title: "Raise the Wage Act of 2025", status: "passed_house"}, {id: "S.215", title: "Common Sense Wage Increase Act", status: "committee"} ] }',
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "29 USC 206(a)(1)", parameter: "minimum_wage", date: "2027-01-01", branch: "current_law" })',
        result: '{ value: 7.25, effective_since: "2009-07-24" }',
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "29 USC 206(a)(1)", parameter: "minimum_wage", date: "2027-01-01", branch: "hr42_enacted_as_passed_house" })',
        result: '{ value: 9.50, effective: "2027-01-01" }',
      },
      { kind: "heading", text: "Cloture probability" },
      {
        kind: "text",
        text: "HR.42 passed the House but Senate vote-count is well short of 60. Filibuster reform is conceivable but not in this Congress's calendar. Path to enactment requires either a bipartisan compromise version (lower number, possibly indexed, longer phase-in) or Senate procedural change.",
      },
      {
        kind: "math",
        text: "P(no change, $7.25) = 0.82 · P(modest increase, $8.50–9.00) = 0.10 · P(larger increase, $9.50–11.00) = 0.06 · P(other / indexation only) = 0.02",
      },
      { kind: "heading", text: "Distribution and forecast" },
      {
        kind: "text",
        text: "Strongly right-skewed: 82% probability of exact status quo. Reporting the modal value as the point estimate is more honest than the mean given the discrete nature of the legislative outcome. CI reflects the small but non-trivial right tail.",
      },
      { kind: "forecast", point: 7.25, ciLow: 7.25, ciHigh: 9.5 },
    ],
  },

  {
    slug: "standard-deduction-joint-ty2027",
    type: "policy",
    title: "Standard deduction, joint filers, TY2027",
    question:
      "What will the federal standard deduction for married couples filing jointly be in tax year 2027?",
    unit: "usd",
    pointEstimate: 32000,
    ciLow: 16000,
    ciHigh: 35000,
    confidence: 0.8,
    resolutionDate: "2027-12-31",
    resolutionSource: "IRS inflation-adjusted tax parameters",
    resolutionRule:
      "Resolves to the standard deduction for married couples filing jointly for TY2027 as published by the IRS in the official inflation-adjusted tax parameter release.",
    policyParameter: "gov.irs.deductions.standard.amount.JOINT.2027",
    historicalContext: [
      { label: "TY2017", value: 12700 },
      { label: "TY2024", value: 29200 },
      { label: "TY2025", value: 30000 },
      { label: "TY2026e", value: 31000 },
    ],
    drivers: [
      "TCJA extension status",
      "Inflation indexing",
      "Budget package offsets",
      "Filing-status parity politics",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the parameter" },
      {
        kind: "text",
        text: "This is a policy-state forecast: whether the post-TCJA higher standard deduction remains in force dominates the interval, with inflation indexing determining the exact value if extended.",
      },
      { kind: "heading", text: "Statutory branches" },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.63", parameter: "standard_deduction_joint", year: 2027, branch: "current_law_post_sunset" })',
        result:
          '{ value: 16000, note: "approximate inflation-indexed pre-TCJA regime" }',
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.63", parameter: "standard_deduction_joint", year: 2027, branch: "tcja_extended" })',
        result:
          '{ value: 32000, note: "higher deduction retained and indexed" }',
      },
      {
        kind: "math",
        text: "P(extended higher deduction) = 0.72 · P(reversion) = 0.18 · P(modified higher deduction) = 0.10",
      },
      {
        kind: "text",
        text: "The modal outcome is extension of the higher deduction. The lower interval endpoint preserves the real reversion scenario because it remains a discrete legislative branch.",
      },
      { kind: "forecast", point: 32000, ciLow: 16000, ciHigh: 35000 },
    ],
  },

  {
    slug: "top-marginal-income-tax-rate-ty2027",
    type: "policy",
    title: "Top individual income tax rate, TY2027",
    question:
      "What will the top federal individual income tax marginal rate be for tax year 2027?",
    unit: "percent",
    pointEstimate: 37.0,
    ciLow: 37.0,
    ciHigh: 39.6,
    confidence: 0.8,
    resolutionDate: "2027-12-31",
    resolutionSource: "Internal Revenue Code and IRS tax tables",
    resolutionRule:
      "Resolves to the highest statutory federal individual income tax marginal rate applicable for TY2027, excluding surtaxes such as NIIT or Medicare taxes.",
    policyParameter: "gov.irs.income.bracket.rates.top.2027",
    historicalContext: [
      { label: "Pre-TCJA", value: 39.6 },
      { label: "TY2018", value: 37.0 },
      { label: "TY2024", value: 37.0 },
      { label: "TY2025", value: 37.0 },
    ],
    drivers: [
      "TCJA rate extension",
      "Revenue needs in budget package",
      "High-income tax politics",
      "Surtax substitution",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the discrete rate" },
      {
        kind: "text",
        text: "This is a discrete statutory forecast. Current post-sunset law points to 39.6%, but the political baseline for a broader tax package strongly favors retaining the 37% top rate or replacing rate increases with narrower base broadeners.",
      },
      { kind: "heading", text: "Policy-state weighting" },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.1", parameter: "top_rate", year: 2027, branches: ["tcja_extended", "post_sunset"] })',
        result:
          "{ tcja_extended: 37.0, post_sunset: 39.6, modified_high_income_package: 39.6 }",
      },
      {
        kind: "math",
        text: "P(37%) = 0.68 · P(39.6%) = 0.27 · P(other) = 0.05",
      },
      {
        kind: "text",
        text: "The point estimate reports the modal statutory rate rather than the mean because resolution is categorical in practice. The 80% interval spans the two dominant statutory branches.",
      },
      { kind: "forecast", point: 37.0, ciLow: 37.0, ciHigh: 39.6 },
    ],
  },

  {
    slug: "salt-cap-ty2027",
    type: "policy",
    title: "SALT deduction cap, TY2027",
    question:
      "What will the maximum federal state-and-local tax deduction (for joint filers) be in tax year 2027?",
    unit: "usd",
    pointEstimate: 22000,
    ciLow: 10000,
    ciHigh: 80000,
    confidence: 0.8,
    resolutionDate: "2027-12-31",
    resolutionSource: "Internal Revenue Code §164(b)(6)",
    resolutionRule:
      "Resolves to the cap on the deduction for state and local taxes under IRC §164(b)(6) applicable to joint filers in TY2027. If no cap is in force, resolves at the projected average itemizer SALT amount in the SOI distribution (functionally 'no cap').",
    policyParameter: "irc.164.b.6.cap_joint.2027",
    historicalContext: [
      { label: "Pre-TCJA", value: 100000 },
      { label: "TCJA cap", value: 10000 },
      { label: "2024", value: 10000 },
      { label: "2025", value: 10000 },
    ],
    drivers: [
      "TCJA extension package details",
      "Blue-state House Republican leverage",
      "Joint Committee scoring constraints",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "SALT cap is the highest-leverage knob in the TCJA-extension negotiation because the affected constituencies are concentrated in House districts with thin majorities. The TCJA cap sunsets after TY2025; current-law TY2026+ means no cap. Any extension package must affirmatively reimpose or modify the cap.",
      },
      { kind: "heading", text: "Law-encoded scenarios" },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.164.b.6", parameter: "cap_joint", year: 2027, branch: "current_law_post_sunset" })',
        result:
          '{ value: null, note: "TCJA cap expired; no cap in effect under current law" }',
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.164.b.6", parameter: "cap_joint", year: 2027, branch: "house_passed_extension" })',
        result:
          '{ value: 20000, note: "doubled cap for joint filers, phased above $500k AGI" }',
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.164.b.6", parameter: "cap_joint", year: 2027, branch: "senate_alternative" })',
        result: '{ value: 40000, note: "negotiated higher cap, $40k joint" }',
      },
      { kind: "heading", text: "Microsim revenue impact" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "salt_cap_22k_joint", year: 2027, output: "iit_revenue_delta_vs_no_cap_billions" })',
        result: "{ point: -88, ci80: [-110, -68] }",
      },
      { kind: "heading", text: "Probability weighting" },
      {
        kind: "math",
        text: "P($10k cap retained) = 0.10 · P($20k doubled joint) = 0.35 · P($40k joint) = 0.25 · P(no cap / full repeal) = 0.20 · P(other) = 0.10",
      },
      {
        kind: "math",
        text: "E[SALT cap TY2027] ≈ 0.10·10000 + 0.35·20000 + 0.25·40000 + 0.20·80000 + 0.10·30000 = $22,000",
      },
      { kind: "heading", text: "Distribution caveat" },
      {
        kind: "text",
        text: "Multi-modal distribution; the point estimate is the expected value but the modal value is $20k. Use the CI as a range, not a posterior interval.",
      },
      { kind: "forecast", point: 22000, ciLow: 10000, ciHigh: 80000 },
    ],
  },

  {
    slug: "snap-max-allotment-family-4-fy2027",
    type: "policy",
    title: "SNAP maximum allotment, family of 4, FY2027",
    question:
      "What will the maximum monthly SNAP benefit for a household of 4 in the 48 contiguous states and DC be for fiscal year 2027?",
    unit: "usd",
    pointEstimate: 1010,
    ciLow: 975,
    ciHigh: 1045,
    confidence: 0.8,
    resolutionDate: "2026-10-01",
    resolutionSource: "USDA FNS",
    resolutionRule:
      "Resolves to the FY2027 maximum allotment for a 4-person household in the 48 contiguous states and DC, as published by USDA in the annual Cost-of-Living Adjustment notice (typically August preceding the fiscal year).",
    policyParameter: "usda.snap.max_allotment.hh4.48_dc.fy2027",
    historicalContext: [
      { label: "FY2024", value: 973 },
      { label: "FY2025", value: 975 },
      { label: "FY2026e", value: 994 },
    ],
    drivers: [
      "Thrifty Food Plan inflation",
      "Farm Bill reauthorization status",
      "Discretionary TFP reevaluation",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the question" },
      {
        kind: "text",
        text: "Under current law, the SNAP maximum is set as 100% of the Thrifty Food Plan for a 4-person household, indexed to June-of-prior-year food-at-home CPI. The 2021 USDA TFP reevaluation raised the base; the 2018 Farm Bill required additional reevaluation by 2027. Two paths: (1) routine annual inflation adjustment, or (2) discretionary TFP reset under FY2027 reauthorization.",
      },
      { kind: "heading", text: "Routine inflation path" },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "7 USC 2017(a)", parameter: "max_allotment_hh4", year: "FY2027", branch: "current_law_inflation_only" })',
        result:
          '{ formula: "TFP_value × food_at_home_cpi_June_2026_June_2025", projected_value: 1012 }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "snap_inflation_only", year: "FY2027", output: "max_allotment_hh4_48states" })',
        result: "{ point: 1010, ci80: [992, 1029] }",
      },
      { kind: "heading", text: "Farm Bill scenarios" },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "Farm Bill reauthorization", parameter: "snap_tfp_treatment", year: "FY2027", branch: "house_ag_committee_markup" })',
        result:
          '{ change: "freeze_tfp_at_2024_baseline", projected_value: 975 }',
      },
      {
        kind: "text",
        text: "House Ag Committee markup includes language that would constrain future TFP increases. Senate Ag chair has indicated unwillingness to advance any package that cuts SNAP benefits relative to current law. Standoff has lasted three Farm Bill cycles already.",
      },
      { kind: "heading", text: "Weighting" },
      {
        kind: "math",
        text: "P(continuing resolution / inflation-only) = 0.70 · P(SNAP reduced) = 0.20 · P(SNAP modestly raised) = 0.10",
      },
      {
        kind: "math",
        text: "E[max allotment hh4 FY2027] = 0.70·1010 + 0.20·975 + 0.10·1040 = 1010",
      },
      { kind: "forecast", point: 1010, ciLow: 975, ciHigh: 1045 },
    ],
  },

  {
    slug: "snap-benefit-outlays-fy2027",
    type: "data",
    title: "SNAP benefit outlays, FY2027",
    question:
      "What will federal SNAP benefit outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 128.0,
    ciLow: 116.0,
    ciHigh: 143.0,
    confidence: 0.8,
    resolutionDate: "2027-11-30",
    resolutionSource: "USDA FNS and Monthly Treasury Statement",
    resolutionRule:
      "Resolves to federal SNAP benefit outlays for FY2027, excluding administrative costs, in billions of nominal dollars, using the first official USDA FNS or Treasury fiscal-year table that identifies SNAP benefits.",
    dataPointId: "usda.fns.snap.benefit_outlays.fy2027",
    historicalContext: [
      { label: "FY2021", value: 108 },
      { label: "FY2022", value: 119 },
      { label: "FY2023", value: 113 },
      { label: "FY2024", value: 100 },
      { label: "FY2026e", value: 121 },
    ],
    drivers: [
      "Food-at-home inflation",
      "Caseload and unemployment",
      "Farm Bill benefit rules",
      "State administrative churn",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the statistic" },
      {
        kind: "text",
        text: "SNAP benefit outlays combine an eligibility/take-up model with a food-price-indexed benefit schedule. It is a good public-data cell because USDA and Treasury both publish outcome tables, but the forecast benefits from a PolicyEngine eligibility model.",
      },
      { kind: "heading", text: "Benefit and caseload model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "snap_current_law", year: 2027, output: "snap_benefits_total", unit: "billions" })',
        result:
          '{ point: 126.5, ci80: [117.0, 140.0], drivers: ["TFP indexation", "caseload", "net income tests"] }',
      },
      {
        kind: "tool",
        tool: "usda.lookup",
        call: 'usda.lookup({ table: "snap_fiscal_year_costs", series: "benefits", years: [2021, 2026] })',
        result:
          '{ pandemic_peak_unwound: true, fy2026_run_rate_billions: 121, food_price_risk: "upside" }',
      },
      {
        kind: "math",
        text: "E[SNAP benefits FY2027] ≈ caseload path × indexed maximum allotment × net-income adjustment = $128B",
      },
      { kind: "forecast", point: 128.0, ciLow: 116.0, ciHigh: 143.0 },
    ],
  },

  {
    slug: "aca-premium-tax-credit-outlays-fy2027",
    type: "data",
    title: "ACA premium tax credit outlays, FY2027",
    question:
      "What will federal ACA premium tax credit outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 94.0,
    ciLow: 62.0,
    ciHigh: 132.0,
    confidence: 0.8,
    resolutionDate: "2027-11-30",
    resolutionSource: "Monthly Treasury Statement and CBO baseline tables",
    resolutionRule:
      "Resolves to federal outlays for refundable premium tax credits under the Affordable Care Act for FY2027, in billions of nominal dollars, using the first official Treasury or CBO table that separately identifies the credit.",
    dataPointId: "treasury.mts.aca_premium_tax_credit_outlays.fy2027",
    historicalContext: [
      { label: "FY2021", value: 60 },
      { label: "FY2023", value: 82 },
      { label: "FY2025e", value: 105 },
      { label: "FY2026e", value: 112 },
    ],
    drivers: [
      "Enhanced subsidy extension status",
      "Marketplace enrollment",
      "Benchmark-premium growth",
      "Income reconciliation at filing",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the fiscal cell" },
      {
        kind: "text",
        text: "Premium tax credit outlays are a bridge between policy state and administrative behavior: the statutory subsidy schedule determines generosity, but enrollment and benchmark premiums determine the actual fiscal path.",
      },
      { kind: "heading", text: "Policy branches" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "enhanced_ptc_expire", year: 2027, output: "aca_premium_tax_credit_outlays", unit: "billions" })',
        result:
          '{ point: 72, ci80: [58, 92], drivers: ["lower enrollment", "original ACA subsidy schedule"] }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "enhanced_ptc_extended", year: 2027, output: "aca_premium_tax_credit_outlays", unit: "billions" })',
        result:
          '{ point: 124, ci80: [101, 151], drivers: ["higher enrollment", "zero-premium silver availability"] }',
      },
      {
        kind: "math",
        text: "E[outlays] = 0.55·72 + 0.35·124 + 0.10·105 = $93.5B",
      },
      {
        kind: "text",
        text: "The central forecast weights expiration as the modal path but leaves a large upper tail because a one- or two-year extension can be attached to a broader budget vehicle.",
      },
      { kind: "forecast", point: 94.0, ciLow: 62.0, ciHigh: 132.0 },
    ],
  },

  {
    slug: "medicaid-chip-enrollment-dec-2027",
    type: "data",
    title: "Medicaid and CHIP enrollment, Dec 2027",
    question:
      "What will total Medicaid and CHIP enrollment be in December 2027, as reported by CMS?",
    unit: "millions",
    pointEstimate: 82.0,
    ciLow: 77.0,
    ciHigh: 88.0,
    confidence: 0.8,
    resolutionDate: "2028-06-30",
    resolutionSource: "CMS Medicaid and CHIP enrollment reports",
    resolutionRule:
      "Resolves to total Medicaid and CHIP enrollment for December 2027 in the CMS monthly enrollment report, in millions of people, using the first report that includes all-state December data.",
    dataPointId: "cms.medicaid_chip.enrollment.2027-12",
    historicalContext: [
      { label: "Dec 2021", value: 87 },
      { label: "Dec 2022", value: 93 },
      { label: "Dec 2023", value: 85 },
      { label: "Dec 2025e", value: 81 },
    ],
    drivers: [
      "Post-unwinding churn",
      "Unemployment and income eligibility",
      "State renewal automation",
      "ACA subsidy and marketplace substitution",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the enrollment target" },
      {
        kind: "text",
        text: "The pandemic continuous-coverage peak has unwound, so the 2027 question is whether enrollment stabilizes near the post-unwinding floor or rises again with weaker labor income and state renewal reforms.",
      },
      { kind: "heading", text: "Eligibility and churn model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ year: 2027, output: "medicaid_chip_enrollment", unit: "millions", renewal_churn: "central" })',
        result:
          '{ point: 81.5, ci80: [77.8, 86.4], drivers: ["income eligibility", "children retained", "redetermination churn"] }',
      },
      {
        kind: "tool",
        tool: "cms.lookup",
        call: 'cms.lookup({ series: "medicaid_chip_enrollment", months: ["2021-12", "2025-12"] })',
        result:
          "{ peak_unwound: true, post_unwinding_floor_millions: 79, child_share_stabilizing: true }",
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The interval is asymmetric: downside is bounded by the post-unwinding floor, while upside comes from recession risk, state auto-renewal improvements, and marketplace affordability changes.",
      },
      { kind: "forecast", point: 82.0, ciLow: 77.0, ciHigh: 88.0 },
    ],
  },

  {
    slug: "spm-poverty-rate-2025",
    type: "data",
    title: "SPM poverty rate, 2025",
    question:
      "What will the overall Supplemental Poverty Measure poverty rate be for calendar year 2025 as published by the U.S. Census Bureau?",
    unit: "percent",
    pointEstimate: 12.7,
    ciLow: 12.0,
    ciHigh: 13.5,
    confidence: 0.8,
    resolutionDate: "2026-09-15",
    resolutionSource: "U.S. Census Bureau, Poverty in the United States: 2025",
    resolutionRule:
      "Resolves to the official Supplemental Poverty Measure poverty rate for all people in calendar year 2025, as published in the Census Poverty in the United States report expected in September 2026.",
    dataPointId: "census.spm.all_people_poverty_rate.2025",
    historicalContext: [
      { label: "2021", value: 7.8 },
      { label: "2022", value: 12.4 },
      { label: "2023", value: 12.9 },
      { label: "2024", value: 12.9 },
    ],
    drivers: [
      "Refundable credit policy in 2025",
      "Rent and medical out-of-pocket costs",
      "Employment and wage growth",
      "SNAP and housing assistance",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the Census target" },
      {
        kind: "text",
        text: "Overall SPM poverty is less CTC-sensitive than child poverty but more exposed to housing, medical, SNAP, and labor-market inputs. This 2025 target resolves roughly a year earlier than the prior 2026 SPM cell, making it a better near-term calibration target.",
      },
      { kind: "heading", text: "PolicyEngine baseline" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "current_law", year: 2025, output: "spm_poverty_rate", map_to: "person" })',
        result:
          '{ point: 12.6, ci80: [12.0, 13.3], drivers: ["tax credits", "housing costs", "medical expenses"] }',
      },
      {
        kind: "tool",
        tool: "census.lookup",
        call: 'census.lookup({ series: "spm_poverty_rate", years: [2021, 2024] })',
        result:
          "{ expanded_credit_low: 7.8, post_expansion_plateau: [12.4, 12.9] }",
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The model stays close to the 2022-2024 post-expansion plateau. Improved employment and real earnings pull down slightly; shelter and medical expense pressure keep the rate near the 2024 level.",
      },
      { kind: "forecast", point: 12.7, ciLow: 12.0, ciHigh: 13.5 },
    ],
  },

  {
    slug: "unemployment-insurance-outlays-fy2027",
    type: "data",
    title: "Unemployment insurance outlays, FY2027",
    question:
      "What will federal unemployment insurance benefit outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 49.0,
    ciLow: 32.0,
    ciHigh: 78.0,
    confidence: 0.8,
    resolutionDate: "2027-11-30",
    resolutionSource: "Monthly Treasury Statement and Department of Labor ETA",
    resolutionRule:
      "Resolves to federal unemployment insurance benefit outlays for FY2027, in billions of nominal dollars, using the first official Treasury or Department of Labor fiscal-year table that reports UI benefits.",
    dataPointId: "treasury.mts.unemployment_insurance_outlays.fy2027",
    historicalContext: [
      { label: "FY2020", value: 477 },
      { label: "FY2022", value: 36 },
      { label: "FY2024", value: 34 },
      { label: "FY2026e", value: 42 },
    ],
    drivers: [
      "Unemployment rate path",
      "Initial and continued claims",
      "Average weekly benefit",
      "Extended-benefit triggers",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the fiscal target" },
      {
        kind: "text",
        text: "UI outlays are highly cyclical and right-skewed. The central case is a normal late-cycle claims path, but recession risk creates a much fatter upper tail than for most transfer programs.",
      },
      { kind: "heading", text: "Labor-market model" },
      {
        kind: "tool",
        tool: "bls.lookup",
        call: 'bls.lookup({ series: ["unemployment_rate", "insured_unemployment_rate"], horizon: "FY2027" })',
        result:
          "{ unemployment_rate_mean: 4.5, insured_unemployment_rate_mean: 1.4, recession_tail_probability: 0.18 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "baseline_labor_market", year: 2027, output: "ui_benefit_outlays", unit: "billions" })',
        result:
          '{ point: 46, ci80: [34, 71], drivers: ["claims duration", "weekly benefit", "covered employment"] }',
      },
      {
        kind: "math",
        text: "central path = normal claims cost; upper tail = recession-triggered duration and extended benefits",
      },
      { kind: "forecast", point: 49.0, ciLow: 32.0, ciHigh: 78.0 },
    ],
  },

  {
    slug: "ssi-federal-payments-fy2027",
    type: "data",
    title: "SSI federal payments, FY2027",
    question:
      "What will federal Supplemental Security Income benefit payments be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 75.0,
    ciLow: 68.0,
    ciHigh: 84.0,
    confidence: 0.8,
    resolutionDate: "2027-11-30",
    resolutionSource:
      "Social Security Administration and Monthly Treasury Statement",
    resolutionRule:
      "Resolves to federal SSI benefit payments for FY2027, excluding state supplements, in billions of nominal dollars, using the first official SSA or Treasury fiscal-year table that reports SSI federal payments.",
    dataPointId: "ssa.ssi.federal_payments.fy2027",
    historicalContext: [
      { label: "FY2021", value: 57 },
      { label: "FY2023", value: 61 },
      { label: "FY2025e", value: 68 },
      { label: "FY2026e", value: 72 },
    ],
    drivers: [
      "COLA inflation index",
      "Aged and disabled recipient counts",
      "Deeming and earned-income offsets",
      "SSA redetermination workload",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the program total" },
      {
        kind: "text",
        text: "SSI federal payments are less cyclical than UI or SNAP; the main uncertainty is inflation indexing plus slow-moving recipient counts and redetermination outcomes.",
      },
      { kind: "heading", text: "Eligibility and benefit model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "ssi_current_law", year: 2027, output: "ssi_federal_benefits", unit: "billions" })',
        result:
          '{ point: 74.2, ci80: [69.0, 82.0], drivers: ["federal benefit rate", "countable income", "recipient count"] }',
      },
      {
        kind: "tool",
        tool: "ssa.lookup",
        call: 'ssa.lookup({ table: "ssi_annual_statistical_report", series: "federal_payments", years: [2021, 2026] })',
        result:
          "{ nominal_growth: 'steady', recipient_count_trend: 'flat-to-up' }",
      },
      {
        kind: "text",
        text: "The forecast stays close to the indexed current-law path; the upper interval mostly reflects higher COLA and reduced redetermination churn.",
      },
      { kind: "forecast", point: 75.0, ciLow: 68.0, ciHigh: 84.0 },
    ],
  },

  {
    slug: "medicaid-federal-outlays-fy2027",
    type: "data",
    title: "Federal Medicaid outlays, FY2027",
    question:
      "What will federal Medicaid outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 655.0,
    ciLow: 600.0,
    ciHigh: 720.0,
    confidence: 0.8,
    resolutionDate: "2027-11-30",
    resolutionSource: "Monthly Treasury Statement and CMS financial reports",
    resolutionRule:
      "Resolves to federal Medicaid outlays for FY2027, in billions of nominal dollars, using the first official Treasury or CMS fiscal-year table that reports federal Medicaid payments.",
    dataPointId: "cms.medicaid.federal_outlays.fy2027",
    historicalContext: [
      { label: "FY2021", value: 521 },
      { label: "FY2023", value: 616 },
      { label: "FY2024", value: 617 },
      { label: "FY2026e", value: 635 },
    ],
    drivers: [
      "Enrollment after unwinding",
      "FMAP and expansion-state mix",
      "Managed-care rate growth",
      "Long-term services and supports",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the outlay cell" },
      {
        kind: "text",
        text: "Federal Medicaid outlays combine enrollment, service intensity, FMAP, and state payment policy. It is a public finance cell where PolicyEngine-style eligibility modeling informs the caseload denominator, but medical cost growth drives much of the dollar risk.",
      },
      { kind: "heading", text: "Eligibility and spending model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "medicaid_current_law", year: 2027, output: "federal_medicaid_outlays", unit: "billions" })',
        result:
          '{ point: 648, ci80: [608, 704], drivers: ["enrollment", "FMAP", "medical cost growth"] }',
      },
      {
        kind: "tool",
        tool: "cms.lookup",
        call: 'cms.lookup({ table: "medicaid_financial_management_report", series: "federal_share", years: [2021, 2026] })',
        result:
          '{ unwinding_effect: "mostly complete", managed_care_growth: "above CPI" }',
      },
      {
        kind: "text",
        text: "The forecast centers slightly above the eligibility model because federal medical outlays have run hot relative to simple caseload forecasts.",
      },
      { kind: "forecast", point: 655.0, ciLow: 600.0, ciHigh: 720.0 },
    ],
  },

  {
    slug: "ctc-recipient-children-ty2026",
    type: "data",
    title: "Children receiving the CTC, TY2026",
    question:
      "How many children will be claimed for the federal Child Tax Credit in tax year 2026?",
    unit: "millions",
    pointEstimate: 48.0,
    ciLow: 45.0,
    ciHigh: 51.0,
    confidence: 0.8,
    resolutionDate: "2028-08-31",
    resolutionSource: "IRS Statistics of Income",
    resolutionRule:
      "Resolves to the number of qualifying children claimed for the federal Child Tax Credit for tax year 2026, in millions, using the first IRS Statistics of Income table that reports CTC child counts or the closest directly comparable official count.",
    dataPointId: "irs.soi.ctc.qualifying_children.ty2026",
    historicalContext: [
      { label: "TY2019", value: 48 },
      { label: "TY2021", value: 61 },
      { label: "TY2022", value: 49 },
      { label: "TY2024e", value: 48 },
    ],
    drivers: [
      "Child population",
      "Filing participation",
      "Eligibility documentation",
      "Refundability and outreach",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the count" },
      {
        kind: "text",
        text: "This cell forecasts a count, not dollars. It helps calibrate CTC outlay and poverty forecasts because model error often comes from who files and claims the credit, not just the statutory amount.",
      },
      { kind: "heading", text: "Population and filing model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "ctc_current_law", year: 2026, output: "ctc_qualifying_children", unit: "millions" })',
        result:
          '{ point: 47.6, ci80: [45.4, 50.2], drivers: ["child population", "filing units", "eligibility tests"] }',
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ table: "soi_child_tax_credit", series: "qualifying_children", years: [2019, 2024] })',
        result:
          "{ pre_expansion_anchor_millions: 48, expansion_outreach_peak_millions: 61 }",
      },
      {
        kind: "text",
        text: "The interval keeps a small upside tail for outreach or refundability changes that pull non-filers into the tax system.",
      },
      { kind: "forecast", point: 48.0, ciLow: 45.0, ciHigh: 51.0 },
    ],
  },

  {
    slug: "housing-choice-voucher-outlays-fy2027",
    type: "data",
    title: "Housing Choice Voucher outlays, FY2027",
    question:
      "What will federal Housing Choice Voucher program outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 36.0,
    ciLow: 32.0,
    ciHigh: 42.0,
    confidence: 0.8,
    resolutionDate: "2027-11-30",
    resolutionSource:
      "HUD budget execution reports and Monthly Treasury Statement",
    resolutionRule:
      "Resolves to federal tenant-based rental assistance outlays for the Housing Choice Voucher program for FY2027, in billions of nominal dollars, using the first official HUD or Treasury table that separately identifies the program.",
    dataPointId: "hud.hcv.outlays.fy2027",
    historicalContext: [
      { label: "FY2021", value: 23 },
      { label: "FY2023", value: 29 },
      { label: "FY2025e", value: 33 },
      { label: "FY2026e", value: 35 },
    ],
    drivers: [
      "Fair Market Rent growth",
      "Voucher utilization",
      "Congressional appropriations",
      "Tenant income and rent contribution",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the housing cell" },
      {
        kind: "text",
        text: "Voucher outlays are constrained by appropriations but driven mechanically by rents, utilization, and tenant income. They matter for poverty forecasts because housing assistance is counted in SPM resources.",
      },
      { kind: "heading", text: "Housing assistance model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "housing_assistance_current_law", year: 2027, output: "housing_choice_voucher_outlays", unit: "billions" })',
        result:
          '{ point: 35.4, ci80: [32.5, 40.2], drivers: ["FMR growth", "utilization", "tenant income"] }',
      },
      {
        kind: "tool",
        tool: "hud.lookup",
        call: 'hud.lookup({ table: "tenant_based_rental_assistance_outlays", years: [2021, 2026] })',
        result:
          '{ rent_growth_pressure: "elevated", utilization: "high", appropriation_risk: "binding" }',
      },
      {
        kind: "text",
        text: "The forecast is modestly right-skewed because rental inflation and higher utilization can raise renewal needs faster than appropriations forecasts expect.",
      },
      { kind: "forecast", point: 36.0, ciLow: 32.0, ciHigh: 42.0 },
    ],
  },

  {
    slug: "payroll-tax-receipts-fy2027",
    type: "data",
    title: "Federal payroll tax receipts, FY2027",
    question:
      "What will total federal payroll tax receipts be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 1860.0,
    ciLow: 1760.0,
    ciHigh: 1985.0,
    confidence: 0.8,
    resolutionDate: "2027-10-20",
    resolutionSource: "U.S. Treasury Monthly Statement",
    resolutionRule:
      "Resolves to total federal social insurance and retirement receipts for FY2027, in billions of nominal dollars, as reported in the final September FY2027 Monthly Treasury Statement.",
    dataPointId: "treasury.mts.social_insurance_receipts.fy2027",
    historicalContext: [
      { label: "FY2021", value: 1312 },
      { label: "FY2023", value: 1614 },
      { label: "FY2025e", value: 1735 },
      { label: "FY2026e", value: 1800 },
    ],
    drivers: [
      "Aggregate wage growth",
      "Employment level",
      "Taxable maximum indexation",
      "Self-employment income",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the receipts cell" },
      {
        kind: "text",
        text: "Payroll tax receipts are a clean macro-policy bridge: the tax rate is stable, so the forecast mostly depends on covered wages, employment, and the Social Security taxable maximum.",
      },
      { kind: "heading", text: "PolicyEngine wage-tax base" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "current_law", year: 2027, output: "payroll_tax_revenue", unit: "billions" })',
        result:
          '{ point: 1850, ci80: [1775, 1960], drivers: ["covered wages", "taxable maximum", "self-employment income"] }',
      },
      {
        kind: "tool",
        tool: "treasury.lookup",
        call: 'treasury.lookup({ table: "monthly_statement", series: "social_insurance_receipts", years: ["FY2021", "FY2026"] })',
        result:
          '{ trend: "wage-growth driven", sensitivity: "roughly 1:1 to taxable payroll" }',
      },
      {
        kind: "text",
        text: "The forecast sits slightly above the pure wage-base model because the taxable maximum and nominal wage growth tend to raise collections even with stable employment.",
      },
      { kind: "forecast", point: 1860.0, ciLow: 1760.0, ciHigh: 1985.0 },
    ],
  },

  {
    slug: "oasdi-benefit-outlays-fy2027",
    type: "data",
    title: "Social Security OASDI benefit outlays, FY2027",
    question:
      "What will federal Old-Age, Survivors, and Disability Insurance benefit outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 1605.0,
    ciLow: 1540.0,
    ciHigh: 1685.0,
    confidence: 0.8,
    resolutionDate: "2027-11-30",
    resolutionSource:
      "Social Security Administration and Monthly Treasury Statement",
    resolutionRule:
      "Resolves to OASDI benefit payments for FY2027, in billions of nominal dollars, using the first official SSA or Treasury fiscal-year table that reports Old-Age, Survivors, and Disability Insurance benefits.",
    dataPointId: "ssa.oasdi.benefit_outlays.fy2027",
    historicalContext: [
      { label: "FY2021", value: 1135 },
      { label: "FY2023", value: 1354 },
      { label: "FY2025e", value: 1495 },
      { label: "FY2026e", value: 1550 },
    ],
    drivers: [
      "COLA inflation index",
      "Beneficiary count",
      "Average indexed monthly earnings",
      "Disability incidence",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the entitlement path" },
      {
        kind: "text",
        text: "OASDI benefit outlays are highly persistent. The main uncertainty is COLA inflation and beneficiary count growth, not legislative risk over this near-term horizon.",
      },
      { kind: "heading", text: "Benefit roll-forward" },
      {
        kind: "tool",
        tool: "ssa.lookup",
        call: 'ssa.lookup({ series: "oasdi_benefit_payments", years: ["FY2021", "FY2026"], projection: "FY2027" })',
        result:
          '{ beneficiary_growth: "aging-driven", cola_path: "moderate", point_billions: 1600 }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ year: 2027, output: "social_security_benefits_total", unit: "billions" })',
        result:
          '{ point: 1608, ci80: [1548, 1678], drivers: ["beneficiary count", "COLA", "claiming age mix"] }',
      },
      {
        kind: "text",
        text: "The interval is relatively tight because benefit formulas and beneficiary rolls evolve slowly; inflation is the primary residual risk.",
      },
      { kind: "forecast", point: 1605.0, ciLow: 1540.0, ciHigh: 1685.0 },
    ],
  },

  {
    slug: "aotc-refundable-outlays-ty2026",
    type: "policy",
    title: "Refundable AOTC outlays, TY2026",
    question:
      "What will federal refundable American Opportunity Tax Credit outlays be for tax year 2026, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 6.2,
    ciLow: 4.8,
    ciHigh: 7.8,
    confidence: 0.8,
    resolutionDate: "2028-08-31",
    resolutionSource:
      "IRS Statistics of Income and Treasury tax expenditure tables",
    resolutionRule:
      "Resolves to refundable American Opportunity Tax Credit outlays for TY2026, in billions of nominal dollars, using the first official IRS SOI or Treasury table that separately identifies the refundable AOTC amount.",
    policyParameter:
      "gov.irs.credits.education.american_opportunity.refundable",
    historicalContext: [
      { label: "TY2019", value: 5.6 },
      { label: "TY2021", value: 5.9 },
      { label: "TY2023", value: 5.8 },
      { label: "TY2025e", value: 6.0 },
    ],
    drivers: [
      "College enrollment",
      "Tuition and qualified expenses",
      "Refundability cap",
      "Income phase-outs",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the refundable-credit target" },
      {
        kind: "text",
        text: "The AOTC has a stable statutory design, so the forecast is mostly about enrollment and claiming behavior. This is a useful smaller-dollar calibration target for education-credit modeling.",
      },
      { kind: "heading", text: "Tax credit model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "current_law", year: 2026, output: "refundable_aotc", unit: "billions" })',
        result:
          '{ point: 6.1, ci80: [5.0, 7.4], drivers: ["student count", "qualified expenses", "phase-outs"] }',
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ table: "soi_refundable_education_credits", credit: "aotc", years: [2019, 2025] })',
        result:
          '{ nominal_path: "flat-to-slightly-up", reporting_lag: "tax-year table" }',
      },
      {
        kind: "text",
        text: "The forecast remains near the pre-2026 trend, with a wide enough interval for enrollment and tuition-cost variation.",
      },
      { kind: "forecast", point: 6.2, ciLow: 4.8, ciHigh: 7.8 },
    ],
  },

  {
    slug: "wic-average-monthly-participation-fy2027",
    type: "data",
    title: "WIC average monthly participation, FY2027",
    question:
      "What will average monthly participation in WIC be in fiscal year 2027, as reported by USDA FNS?",
    unit: "millions",
    pointEstimate: 6.9,
    ciLow: 6.3,
    ciHigh: 7.6,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "USDA Food and Nutrition Service WIC data tables",
    resolutionRule:
      "Resolves to average monthly WIC participation for FY2027, in millions of participants, using the first USDA FNS annual WIC participation and costs table that reports FY2027.",
    dataPointId: "usda.fns.wic.average_monthly_participation.fy2027",
    historicalContext: [
      { label: "FY2019", value: 6.4 },
      { label: "FY2021", value: 6.2 },
      { label: "FY2023", value: 6.6 },
      { label: "FY2025e", value: 6.9 },
    ],
    drivers: [
      "Birth cohort size",
      "Infant formula and food costs",
      "State outreach and certification",
      "Income eligibility among families with young children",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the USDA target" },
      {
        kind: "text",
        text: "WIC participation is not just eligibility; certification friction, outreach, and food-package value determine take-up. The target is USDA FNS average monthly participation.",
      },
      { kind: "heading", text: "Eligibility and take-up model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "wic_current_law", year: 2027, output: "wic_participation", unit: "millions" })',
        result:
          '{ point: 6.8, ci80: [6.4, 7.5], drivers: ["eligible infants", "certification", "take-up"] }',
      },
      {
        kind: "tool",
        tool: "usda.lookup",
        call: 'usda.lookup({ table: "wic_program_participation_and_costs", years: [2019, 2025] })',
        result:
          '{ recent_trend: "participation recovered after 2021", official_source: "FNS program data tables" }',
      },
      {
        kind: "text",
        text: "The forecast keeps participation near recent elevated levels but allows downside if birth counts soften or certification churn rises.",
      },
      { kind: "forecast", point: 6.9, ciLow: 6.3, ciHigh: 7.6 },
    ],
  },

  {
    slug: "national-school-lunch-participation-sy2026-27",
    type: "data",
    title: "National School Lunch participation, SY2026-27",
    question:
      "What will average daily participation in the National School Lunch Program be in school year 2026-27?",
    unit: "millions",
    pointEstimate: 30.4,
    ciLow: 28.8,
    ciHigh: 32.3,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource:
      "USDA Food and Nutrition Service child nutrition data tables",
    resolutionRule:
      "Resolves to average daily participation in the National School Lunch Program for school year 2026-27, in millions of students, using the first USDA FNS annual child nutrition table that reports the school-year total.",
    dataPointId: "usda.fns.nslp.average_daily_participation.sy2026_27",
    historicalContext: [
      { label: "SY2018-19", value: 29.6 },
      { label: "SY2021-22", value: 30.1 },
      { label: "SY2023-24", value: 28.9 },
      { label: "SY2025-26e", value: 30.0 },
    ],
    drivers: [
      "School enrollment",
      "Community eligibility adoption",
      "Meal price and reimbursement policy",
      "State universal-meals policies",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the child nutrition count" },
      {
        kind: "text",
        text: "School lunch participation is a benefits participation forecast. It resolves to USDA FNS program data and is influenced by state policy, federal reimbursement, and school enrollment.",
      },
      { kind: "heading", text: "Participation model" },
      {
        kind: "tool",
        tool: "usda.lookup",
        call: 'usda.lookup({ table: "child_nutrition_program_data", program: "nslp", metric: "average_daily_participation" })',
        result:
          '{ post_universal_meals_baseline_millions: 29, state_universal_meals_tail: "upside" }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "school_meals_current_law", year: 2027, output: "nslp_participation", unit: "millions" })',
        result:
          '{ point: 30.2, ci80: [28.9, 32.0], drivers: ["free/reduced eligibility", "community eligibility", "state supplements"] }',
      },
      {
        kind: "text",
        text: "The upper tail reflects continued state universal-meals expansion and community eligibility take-up; the lower tail reflects enrollment softness and paid-meal price sensitivity.",
      },
      { kind: "forecast", point: 30.4, ciLow: 28.8, ciHigh: 32.3 },
    ],
  },

  {
    slug: "aca-exchange-plan-selections-oep-2027",
    type: "data",
    title: "ACA exchange plan selections, OEP 2027",
    question:
      "How many Qualified Health Plans will be selected through ACA exchanges during the 2027 Open Enrollment Period?",
    unit: "millions",
    pointEstimate: 19.8,
    ciLow: 14.0,
    ciHigh: 25.0,
    confidence: 0.8,
    resolutionDate: "2027-04-30",
    resolutionSource: "CMS Health Insurance Exchanges Open Enrollment report",
    resolutionRule:
      "Resolves to total Qualified Health Plan selections across HealthCare.gov and state-based exchanges during the 2027 Open Enrollment Period, in millions, using the first final CMS Open Enrollment report for plan year 2027.",
    dataPointId: "cms.aca.exchange_qhp_selections.oep_2027",
    historicalContext: [
      { label: "OEP 2023", value: 16.4 },
      { label: "OEP 2024", value: 21.4 },
      { label: "OEP 2025", value: 24.2 },
      { label: "OEP 2026", value: 23.0 },
    ],
    drivers: [
      "Enhanced premium tax credit status",
      "Benchmark-premium growth",
      "Auto-renewal policy",
      "Medicaid churn into exchange coverage",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the CMS enrollment target" },
      {
        kind: "text",
        text: "The target is CMS plan selections during OEP, not effectuated enrollment later in the year. The 2027 value is highly sensitive to enhanced premium tax credit policy and premium increases visible before open enrollment.",
      },
      { kind: "heading", text: "Policy branches" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "enhanced_ptc_expire", year: 2027, output: "exchange_plan_selections", unit: "millions" })',
        result:
          '{ point: 16.2, ci80: [13.8, 19.8], drivers: ["net premium shock", "reduced zero-premium plans"] }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "enhanced_ptc_extended", year: 2027, output: "exchange_plan_selections", unit: "millions" })',
        result:
          '{ point: 24.0, ci80: [21.0, 26.5], drivers: ["continued subsidy generosity", "auto-renewal"] }',
      },
      {
        kind: "math",
        text: "E[selections] = 0.55·16.2 + 0.35·24.0 + 0.10·20.5 = 19.4M; rounded after CMS-report calibration",
      },
      { kind: "forecast", point: 19.8, ciLow: 14.0, ciHigh: 25.0 },
    ],
  },

  {
    slug: "medicare-benefit-outlays-fy2027",
    type: "data",
    title: "Medicare benefit outlays, FY2027",
    question:
      "What will federal Medicare benefit outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 1110.0,
    ciLow: 1035.0,
    ciHigh: 1210.0,
    confidence: 0.8,
    resolutionDate: "2027-11-30",
    resolutionSource: "Monthly Treasury Statement, CMS, or CBO baseline tables",
    resolutionRule:
      "Resolves to federal Medicare benefit outlays for FY2027, in billions of nominal dollars, using the first official Treasury, CMS, or CBO fiscal-year table that reports Medicare benefit payments.",
    dataPointId: "cms.medicare.benefit_outlays.fy2027",
    historicalContext: [
      { label: "FY2021", value: 696 },
      { label: "FY2023", value: 839 },
      { label: "FY2025e", value: 1015 },
      { label: "FY2026e", value: 1065 },
    ],
    drivers: [
      "Beneficiary count",
      "Medicare Advantage penetration",
      "Provider payment updates",
      "Part D drug spending",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the Medicare total" },
      {
        kind: "text",
        text: "Medicare outlays are a large, persistent budget cell. Near-term uncertainty is dominated by payment updates, beneficiary mix, Medicare Advantage benchmarks, and prescription-drug spending.",
      },
      { kind: "heading", text: "Benefit outlay model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ year: 2027, output: "medicare_benefit_outlays", unit: "billions" })',
        result:
          '{ point: 1102, ci80: [1048, 1192], drivers: ["beneficiary count", "MA benchmarks", "Part D spending"] }',
      },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "budget_baseline", series: "medicare", year: "FY2027" })',
        result:
          '{ trend: "above nominal GDP growth", residual_risk: "payment updates and drug spending" }',
      },
      {
        kind: "text",
        text: "The point estimate is slightly above the simple roll-forward because recent Medicare spending has run hot in Medicare Advantage and outpatient components.",
      },
      { kind: "forecast", point: 1110.0, ciLow: 1035.0, ciHigh: 1210.0 },
    ],
  },

  {
    slug: "tanf-federal-outlays-fy2027",
    type: "data",
    title: "TANF federal outlays, FY2027",
    question:
      "What will federal Temporary Assistance for Needy Families outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 17.0,
    ciLow: 15.0,
    ciHigh: 19.5,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource:
      "HHS ACF TANF financial data and Monthly Treasury Statement",
    resolutionRule:
      "Resolves to federal TANF outlays for FY2027, in billions of nominal dollars, using the first official HHS ACF or Treasury table that reports federal TANF fiscal-year spending.",
    dataPointId: "acf.tanf.federal_outlays.fy2027",
    historicalContext: [
      { label: "FY2019", value: 16.5 },
      { label: "FY2021", value: 17.0 },
      { label: "FY2023", value: 16.8 },
      { label: "FY2025e", value: 16.9 },
    ],
    drivers: [
      "Block grant level",
      "Contingency fund use",
      "State transfer behavior",
      "Caseload and benefit policy",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the TANF spending cell" },
      {
        kind: "text",
        text: "TANF federal spending is relatively flat because the core block grant is nominally fixed. The main risk is reauthorization, contingency funding, and state transfer behavior rather than caseload alone.",
      },
      { kind: "heading", text: "Program finance model" },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ table: "tanf_financial_data", series: "federal_outlays", years: ["FY2019", "FY2026"] })',
        result:
          '{ block_grant_nominally_flat: true, transfers_to_ccdf: "variable", contingency_fund_risk: "small" }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "tanf_current_law", year: 2027, output: "tanf_federal_outlays", unit: "billions" })',
        result:
          '{ point: 16.8, ci80: [15.4, 18.8], drivers: ["block grant", "state transfers", "caseload"] }',
      },
      {
        kind: "text",
        text: "The forecast stays near the nominal block-grant path, with a modest upper tail for reauthorization or contingency-fund use.",
      },
      { kind: "forecast", point: 17.0, ciLow: 15.0, ciHigh: 19.5 },
    ],
  },

  {
    slug: "ccdf-outlays-fy2027",
    type: "data",
    title: "Child Care and Development Fund outlays, FY2027",
    question:
      "What will Child Care and Development Fund outlays be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 12.5,
    ciLow: 9.0,
    ciHigh: 17.0,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "HHS ACF CCDF expenditure data",
    resolutionRule:
      "Resolves to total Child Care and Development Fund expenditures for FY2027, in billions of nominal dollars, using the first official ACF-696-based HHS ACF expenditure data release for FY2027.",
    dataPointId: "acf.ccdf.outlays.fy2027",
    historicalContext: [
      { label: "FY2019", value: 9.5 },
      { label: "FY2021", value: 13.0 },
      { label: "FY2023", value: 11.8 },
      { label: "FY2025e", value: 12.0 },
    ],
    drivers: [
      "Discretionary appropriations",
      "State subsidy rates",
      "Eligible child care demand",
      "TANF transfers into CCDF",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the child-care finance cell" },
      {
        kind: "text",
        text: "CCDF is a program-finance cell where appropriations and state spending rules matter as much as eligible-family demand. ACF-696 expenditure data provide the resolution surface.",
      },
      { kind: "heading", text: "Eligibility and appropriation model" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "ccdf_current_law", year: 2027, output: "child_care_subsidy_outlays", unit: "billions" })',
        result:
          '{ point: 12.1, ci80: [9.4, 16.2], drivers: ["appropriations", "eligible children", "state copay policy"] }',
      },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ table: "ccdf_acf_696_expenditures", years: ["FY2019", "FY2026"] })',
        result:
          '{ pandemic_supplement_unwound: true, tanf_transfer_variance: "meaningful" }',
      },
      {
        kind: "text",
        text: "The interval is wider than TANF because appropriations and state rate-setting can move subsidy spending more than the underlying eligible population.",
      },
      { kind: "forecast", point: 12.5, ciLow: 9.0, ciHigh: 17.0 },
    ],
  },

  {
    slug: "estate-gift-tax-receipts-fy2027",
    type: "data",
    title: "Estate and gift tax receipts, FY2027",
    question:
      "What will federal estate and gift tax receipts be in fiscal year 2027, in nominal dollars?",
    unit: "usd_billions",
    pointEstimate: 45.0,
    ciLow: 28.0,
    ciHigh: 72.0,
    confidence: 0.8,
    resolutionDate: "2027-10-20",
    resolutionSource: "U.S. Treasury Monthly Statement",
    resolutionRule:
      "Resolves to federal estate and gift tax receipts for FY2027, in billions of nominal dollars, as reported in the final September FY2027 Monthly Treasury Statement.",
    dataPointId: "treasury.mts.estate_gift_tax_receipts.fy2027",
    historicalContext: [
      { label: "FY2021", value: 27 },
      { label: "FY2023", value: 34 },
      { label: "FY2025e", value: 38 },
      { label: "FY2026e", value: 40 },
    ],
    drivers: [
      "Estate tax exemption level",
      "Asset prices",
      "Mortality and filing timing",
      "Pre-sunset gift planning",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the receipts cell" },
      {
        kind: "text",
        text: "Estate and gift tax receipts are volatile and policy-sensitive. The scheduled exemption path and taxpayer planning around any TCJA-extension package dominate the 2027 distribution.",
      },
      { kind: "heading", text: "Policy and asset-price branches" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "estate_tax_current_law", year: 2027, output: "estate_gift_tax_receipts", unit: "billions" })',
        result:
          '{ point: 52, ci80: [35, 78], drivers: ["exemption sunset", "asset values", "gift timing"] }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "tcja_estate_exemption_extended", year: 2027, output: "estate_gift_tax_receipts", unit: "billions" })',
        result:
          '{ point: 34, ci80: [24, 51], drivers: ["high exemption retained", "planning behavior"] }',
      },
      {
        kind: "math",
        text: "E[receipts] = 0.55·34 + 0.35·52 + 0.10·78 ≈ $45B",
      },
      { kind: "forecast", point: 45.0, ciLow: 28.0, ciHigh: 72.0 },
    ],
  },

  {
    slug: "eitc-claimant-returns-ty2027",
    type: "data",
    title: "EITC claimant returns, TY2027",
    question:
      "How many individual income tax returns will claim the Earned Income Tax Credit for tax year 2027?",
    unit: "millions",
    pointEstimate: 23.4,
    ciLow: 21.6,
    ciHigh: 25.5,
    confidence: 0.8,
    resolutionDate: "2029-12-31",
    resolutionSource: "IRS Statistics of Income individual tax return data",
    resolutionRule:
      "Resolves to the number of TY2027 individual income tax returns claiming the Earned Income Tax Credit, in millions, using the first official IRS Statistics of Income table covering TY2027 individual returns.",
    dataPointId: "irs.soi.eitc_claimant_returns.ty2027",
    historicalContext: [
      { label: "TY2019", value: 25.0 },
      { label: "TY2021", value: 27.5 },
      { label: "TY2023e", value: 23.0 },
      { label: "TY2025e", value: 23.2 },
    ],
    drivers: [
      "Low-wage employment",
      "EITC parameter indexation",
      "Filing and take-up rates",
      "Dependent-child claiming patterns",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the claimant target" },
      {
        kind: "text",
        text: "This cell forecasts returns claiming EITC, not dollars paid. It gives the EITC outlay forecast a separate take-up target that can be calibrated against IRS administrative data.",
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ dataset: "statistics_of_income", series: "eitc_claimant_returns", tax_years: [2019, 2025] })',
        result:
          "{ ty2019: 25.0, ty2021: 27.5, ty2023_estimate: 23.0, ty2025_estimate: 23.2 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ credit: "eitc", year: 2027, output: "claimant_tax_units", takeup: "calibrated" })',
        result:
          '{ point: 23.5, ci80: [21.8, 25.3], drivers: ["earnings distribution", "children", "filing take-up"] }',
      },
      {
        kind: "math",
        text: "Stable low-wage employment plus indexed thresholds keeps claims near the post-pandemic plateau: central case 23.4M.",
      },
      { kind: "forecast", point: 23.4, ciLow: 21.6, ciHigh: 25.5 },
    ],
  },

  {
    slug: "corporate-income-tax-receipts-fy2027",
    type: "data",
    title: "Corporate income tax receipts, FY2027",
    question:
      "How much will the federal government collect in corporation income tax receipts during fiscal year 2027?",
    unit: "usd_billions",
    pointEstimate: 570,
    ciLow: 430,
    ciHigh: 730,
    confidence: 0.8,
    resolutionDate: "2027-10-20",
    resolutionSource: "U.S. Treasury Monthly Statement",
    resolutionRule:
      "Resolves to total corporation income tax receipts for FY2027, in billions of nominal dollars, as reported in the final September FY2027 Monthly Treasury Statement.",
    dataPointId: "treasury.mts.corporation_income_tax_receipts.fy2027",
    historicalContext: [
      { label: "FY2021", value: 372 },
      { label: "FY2022", value: 425 },
      { label: "FY2023", value: 420 },
      { label: "FY2024", value: 530 },
    ],
    drivers: [
      "Corporate profits",
      "Bonus depreciation phaseout or extension",
      "International tax changes",
      "Estimated-payment timing",
    ],
    reasoning: [
      { kind: "heading", text: "Separating profits from policy" },
      {
        kind: "text",
        text: "Corporation income tax receipts are more volatile than wage-based receipts because profits, loss carryforwards, bonus depreciation, and estimated-payment timing all move the cash series.",
      },
      { kind: "heading", text: "Baseline receipts projection" },
      {
        kind: "tool",
        tool: "treasury.lookup",
        call: 'treasury.lookup({ dataset: "monthly_treasury_statement", series: "corporation_income_tax_receipts", fiscal_years: [2021, 2024] })',
        result:
          "{ fy2021: 372, fy2022: 425, fy2023: 420, fy2024: 530, volatility: 'high' }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "business_tax_baseline_2027", output: "corporate_income_tax_receipts", unit: "billions" })',
        result:
          '{ point: 565, ci80: [440, 710], drivers: ["profits", "depreciation", "international minimum taxes"] }',
      },
      {
        kind: "math",
        text: "Central case rounds the fiscal cash forecast to $570B with a wide profit-cycle interval.",
      },
      { kind: "forecast", point: 570, ciLow: 430, ciHigh: 730 },
    ],
  },

  {
    slug: "snap-average-monthly-participation-fy2027",
    type: "data",
    title: "SNAP average monthly participation, FY2027",
    question:
      "How many people will participate in SNAP in an average month of fiscal year 2027?",
    unit: "millions",
    pointEstimate: 40.6,
    ciLow: 37.4,
    ciHigh: 44.1,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "USDA FNS SNAP Data Tables",
    resolutionRule:
      "Resolves to average monthly SNAP persons for FY2027, in millions, using the first USDA FNS national annual participation table that includes all months of fiscal year 2027.",
    dataPointId: "fns.snap.average_monthly_persons.fy2027",
    historicalContext: [
      { label: "FY2021", value: 41.5 },
      { label: "FY2022", value: 41.2 },
      { label: "FY2023", value: 42.1 },
      { label: "FY2024", value: 41.7 },
    ],
    drivers: [
      "Low-income population",
      "Administrative recertification churn",
      "Benefit adequacy and take-up",
      "Employment and wage growth",
    ],
    reasoning: [
      { kind: "heading", text: "Participation target" },
      {
        kind: "text",
        text: "This cell forecasts average monthly persons, not annual unique participants and not benefit dollars. It gives the outlay forecast a separate take-up and caseload calibration target.",
      },
      {
        kind: "tool",
        tool: "fns.lookup",
        call: 'fns.lookup({ program: "SNAP", series: "average_monthly_persons", fiscal_years: [2021, 2024] })',
        result: "{ fy2021: 41.5, fy2022: 41.2, fy2023: 42.1, fy2024: 41.7 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "snap", year: 2027, output: "recipient_persons", map_to: "person", takeup: "calibrated" })',
        result:
          '{ point: 40.4, ci80: [37.6, 43.7], drivers: ["eligibility", "take-up", "recertification"] }',
      },
      {
        kind: "math",
        text: "Caseload drift = 41.7M · (1 - 0.009 annual net decline)^3 ≈ 40.6M",
      },
      { kind: "forecast", point: 40.6, ciLow: 37.4, ciHigh: 44.1 },
    ],
  },

  {
    slug: "pell-grant-recipients-ay2027",
    type: "data",
    title: "Pell Grant recipients, award year 2027-28",
    question:
      "How many students will receive a Federal Pell Grant during award year 2027-28?",
    unit: "millions",
    pointEstimate: 7.2,
    ciLow: 6.4,
    ciHigh: 8.2,
    confidence: 0.8,
    resolutionDate: "2029-02-28",
    resolutionSource: "U.S. Department of Education Pell Grant Program data",
    resolutionRule:
      "Resolves to unduplicated Federal Pell Grant recipients for award year 2027-28, in millions, using the first official Department of Education Pell Grant program data table or budget justification table with final award-year recipients.",
    dataPointId: "ed.pell.recipients.award_year_2027",
    historicalContext: [
      { label: "AY2020", value: 6.2 },
      { label: "AY2022", value: 6.1 },
      { label: "AY2024e", value: 6.8 },
      { label: "AY2026e", value: 7.0 },
    ],
    drivers: [
      "FAFSA simplification take-up",
      "Maximum Pell award and eligibility formula",
      "College enrollment",
      "Student income distribution",
    ],
    reasoning: [
      { kind: "heading", text: "Benefit-access target" },
      {
        kind: "text",
        text: "Pell recipients are an access target for low-income students. The 2027-28 value is driven by FAFSA simplification, enrollment, and whether appropriations maintain eligibility generosity.",
      },
      {
        kind: "tool",
        tool: "education.lookup",
        call: 'education.lookup({ program: "Federal Pell Grant", series: "recipients", award_years: ["2023-24", "2024-25"] })',
        result:
          "{ ay2024_estimate: 6.8, note: 'FAFSA simplification raised maximum-award eligibility' }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "pell", year: 2027, output: "recipient_students", takeup: "fafsa_simplification" })',
        result:
          '{ point: 7.15, ci80: [6.45, 8.05], drivers: ["SAI formula", "enrollment", "completion rate"] }',
      },
      {
        kind: "math",
        text: "Base 6.8M + 0.25M simplification take-up + 0.15M enrollment drift ≈ 7.2M",
      },
      { kind: "forecast", point: 7.2, ciLow: 6.4, ciHigh: 8.2 },
    ],
  },

  {
    slug: "head-start-funded-enrollment-fy2027",
    type: "data",
    title: "Head Start funded enrollment, FY2027",
    question:
      "How many Head Start and Early Head Start funded enrollment slots will be authorized for fiscal year 2027?",
    unit: "millions",
    pointEstimate: 0.82,
    ciLow: 0.74,
    ciHigh: 0.9,
    confidence: 0.8,
    resolutionDate: "2028-06-30",
    resolutionSource: "ACF Office of Head Start Program Information Report",
    resolutionRule:
      "Resolves to funded enrollment for Head Start and Early Head Start in FY2027, in millions of slots, using the first ACF Office of Head Start Program Information Report or annual fact sheet covering fiscal year 2027.",
    dataPointId: "acf.head_start.funded_enrollment.fy2027",
    historicalContext: [
      { label: "FY2019", value: 0.89 },
      { label: "FY2021", value: 0.84 },
      { label: "FY2023", value: 0.8 },
      { label: "FY2025e", value: 0.81 },
    ],
    drivers: [
      "Annual appropriations",
      "Cost-per-slot inflation",
      "Teacher staffing constraints",
      "Conversion between Head Start and Early Head Start slots",
    ],
    reasoning: [
      { kind: "heading", text: "Program-capacity target" },
      {
        kind: "text",
        text: "Funded enrollment measures capacity rather than actual attendance. It is a clean public resolution target for early-childhood benefit access because ACF reports it through Head Start program data.",
      },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ program: "Head Start", series: "funded_enrollment", fiscal_years: [2019, 2025] })',
        result:
          "{ fy2019: 0.89, fy2021: 0.84, fy2023: 0.80, fy2025_estimate: 0.81 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "head_start", year: 2027, output: "funded_slots", budget: "appropriations_baseline" })',
        result:
          '{ point: 0.82, ci80: [0.75, 0.89], drivers: ["appropriations", "cost per slot", "workforce"] }',
      },
      {
        kind: "math",
        text: "Stable nominal funding with 3-4% cost-per-slot growth keeps funded slots roughly flat: central case 0.82M.",
      },
      { kind: "forecast", point: 0.82, ciLow: 0.74, ciHigh: 0.9 },
    ],
  },

  {
    slug: "tanf-average-monthly-families-fy2027",
    type: "data",
    title: "TANF average monthly families, FY2027",
    question:
      "How many families will receive TANF or SSP-MOE cash assistance in an average month of fiscal year 2027?",
    unit: "millions",
    pointEstimate: 0.72,
    ciLow: 0.62,
    ciHigh: 0.85,
    confidence: 0.8,
    resolutionDate: "2028-06-30",
    resolutionSource: "ACF TANF caseload data",
    resolutionRule:
      "Resolves to the fiscal-year average number of families receiving TANF or Separate State Program Maintenance-of-Effort cash assistance in FY2027, in millions, using the first ACF TANF caseload table covering all FY2027 months.",
    dataPointId: "acf.tanf.average_monthly_families.fy2027",
    historicalContext: [
      { label: "FY2019", value: 1.1 },
      { label: "FY2021", value: 0.87 },
      { label: "FY2023", value: 0.74 },
      { label: "FY2024", value: 0.72 },
    ],
    drivers: [
      "State work and diversion rules",
      "Block-grant funding pressure",
      "Low-income families with children",
      "Administrative take-up and sanctions",
    ],
    reasoning: [
      { kind: "heading", text: "Separating caseload from spending" },
      {
        kind: "text",
        text: "TANF outlays can stay roughly flat even while cash-assistance caseloads change, because states can move funds into work supports, child care, or other allowable activities. This cell resolves the family cash-assistance caseload directly.",
      },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ table: "tanf_caseload_data", series: "families", fiscal_years: [2019, 2024] })',
        result: "{ fy2019: 1.10, fy2021: 0.87, fy2023: 0.74, fy2024: 0.72 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "tanf", year: 2027, output: "cash_assistance_families", takeup: "state_rules_calibrated" })',
        result:
          '{ point: 0.71, ci80: [0.63, 0.83], drivers: ["state diversion", "sanctions", "need"] }',
      },
      {
        kind: "math",
        text: "Trend case holds the FY2024 plateau with a mild recession tail: central case 0.72M families.",
      },
      { kind: "forecast", point: 0.72, ciLow: 0.62, ciHigh: 0.85 },
    ],
  },

  {
    slug: "ccdf-average-monthly-children-served-fy2027",
    type: "data",
    title: "CCDF average monthly children served, FY2027",
    question:
      "How many children will receive Child Care and Development Fund subsidized child care in an average month of fiscal year 2027?",
    unit: "millions",
    pointEstimate: 1.36,
    ciLow: 1.05,
    ciHigh: 1.75,
    confidence: 0.8,
    resolutionDate: "2029-03-31",
    resolutionSource: "ACF CCDF data tables",
    resolutionRule:
      "Resolves to the average monthly adjusted number of children served by CCDF in FY2027, in millions, using the first ACF-800/ACF-801 CCDF data table covering fiscal year 2027.",
    dataPointId: "acf.ccdf.average_monthly_children_served.fy2027",
    historicalContext: [
      { label: "FY2019", value: 1.35 },
      { label: "FY2021", value: 1.21 },
      { label: "FY2022", value: 1.32 },
      { label: "FY2023", value: 1.42 },
    ],
    drivers: [
      "CCDF appropriations and transfers",
      "Child care prices",
      "State reimbursement rates",
      "Parent employment and eligibility churn",
    ],
    reasoning: [
      { kind: "heading", text: "Service count target" },
      {
        kind: "text",
        text: "The service-count target captures whether dollars become slots. It is especially important for evaluating child care policy because higher provider reimbursement can raise cost per child while reducing waiting lists.",
      },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ table: "ccdf_data_tables", series: "average_monthly_children_served", fiscal_years: [2019, 2023] })',
        result:
          "{ fy2019: 1.35, fy2021: 1.21, fy2022: 1.32, fy2023_preliminary: 1.42 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "ccdf", year: 2027, output: "children_served", takeup: "waiting_list_constrained" })',
        result:
          '{ point: 1.34, ci80: [1.08, 1.71], drivers: ["appropriations", "prices", "eligibility"] }',
      },
      {
        kind: "math",
        text: "Central case lets pandemic-era funding unwind but assumes states preserve some rate increases: 1.36M children.",
      },
      { kind: "forecast", point: 1.36, ciLow: 1.05, ciHigh: 1.75 },
    ],
  },

  {
    slug: "liheap-households-assisted-fy2027",
    type: "data",
    title: "LIHEAP households assisted, FY2027",
    question:
      "How many households will receive Low Income Home Energy Assistance Program assistance during fiscal year 2027?",
    unit: "millions",
    pointEstimate: 5.1,
    ciLow: 3.4,
    ciHigh: 6.9,
    confidence: 0.8,
    resolutionDate: "2029-09-30",
    resolutionSource: "ACF LIHEAP Household Report",
    resolutionRule:
      "Resolves to total households receiving at least one type of LIHEAP assistance for FY2027, in millions, using the first ACF LIHEAP Household Report or LIHEAP data warehouse release covering fiscal year 2027.",
    dataPointId: "acf.liheap.households_assisted.fy2027",
    historicalContext: [
      { label: "FY2019", value: 5.2 },
      { label: "FY2021", value: 5.4 },
      { label: "FY2023", value: 6.0 },
      { label: "FY2025e", value: 5.3 },
    ],
    drivers: [
      "Annual LIHEAP appropriations",
      "Energy prices and weather",
      "State benefit-size choices",
      "Eligible household take-up",
    ],
    reasoning: [
      { kind: "heading", text: "Program access target" },
      {
        kind: "text",
        text: "LIHEAP is a useful stress-test cell because household counts can move in opposite directions from average benefit size. A cold winter or high energy prices may raise applications while fixed funding limits the number served.",
      },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ program: "LIHEAP", series: "households_assisted", fiscal_years: [2019, 2025] })',
        result:
          "{ fy2019: 5.2, fy2021: 5.4, fy2023_estimate: 6.0, fy2025_estimate: 5.3 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "liheap", year: 2027, output: "households_assisted", benefit_allocation: "state_plans" })',
        result:
          '{ point: 5.0, ci80: [3.6, 6.7], drivers: ["appropriations", "energy prices", "weather"] }',
      },
      {
        kind: "math",
        text: "Funding risk dominates: elimination or deep reduction creates the lower tail; normal block-grant funding keeps households near 5M.",
      },
      { kind: "forecast", point: 5.1, ciLow: 3.4, ciHigh: 6.9 },
    ],
  },

  {
    slug: "school-breakfast-participation-sy2026-27",
    type: "data",
    title: "School Breakfast participation, SY2026-27",
    question:
      "How many children will participate in the School Breakfast Program on an average school day during school year 2026-27?",
    unit: "millions",
    pointEstimate: 15.2,
    ciLow: 14.0,
    ciHigh: 16.7,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "USDA FNS Child Nutrition Tables",
    resolutionRule:
      "Resolves to average daily School Breakfast Program participation for school year 2026-27, in millions, using USDA FNS participation data with summer months excluded where FNS publishes a school-year table.",
    dataPointId: "fns.sbp.average_daily_participation.sy2026_27",
    historicalContext: [
      { label: "FY2019", value: 14.7 },
      { label: "FY2022", value: 14.9 },
      { label: "FY2023", value: 15.4 },
      { label: "FY2024", value: 15.0 },
    ],
    drivers: [
      "Community Eligibility Provision adoption",
      "Universal meals in states",
      "School enrollment",
      "Attendance and breakfast-after-the-bell models",
    ],
    reasoning: [
      { kind: "heading", text: "Participation target" },
      {
        kind: "text",
        text: "Breakfast participation is a separate nutrition access indicator from lunch because many districts have different delivery models, stigma effects, and state universal-meals supplements.",
      },
      {
        kind: "tool",
        tool: "fns.lookup",
        call: 'fns.lookup({ program: "School Breakfast Program", series: "average_daily_participation", fiscal_years: [2019, 2024] })',
        result: "{ fy2019: 14.7, fy2022: 14.9, fy2023: 15.4, fy2024: 15.0 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "school_breakfast", school_year: "2026-27", output: "average_daily_participants", takeup: "cep_and_state_universal_meals" })',
        result:
          '{ point: 15.3, ci80: [14.1, 16.6], drivers: ["CEP", "state supplements", "attendance"] }',
      },
      {
        kind: "math",
        text: "Stable school enrollment plus modest CEP expansion lifts the central estimate to 15.2M.",
      },
      { kind: "forecast", point: 15.2, ciLow: 14.0, ciHigh: 16.7 },
    ],
  },

  {
    slug: "ssi-recipients-dec-2027",
    type: "data",
    title: "SSI recipients, December 2027",
    question:
      "How many people will receive Supplemental Security Income in December 2027?",
    unit: "millions",
    pointEstimate: 7.35,
    ciLow: 7.05,
    ciHigh: 7.7,
    confidence: 0.8,
    resolutionDate: "2028-02-28",
    resolutionSource: "SSA Monthly Statistical Snapshot",
    resolutionRule:
      "Resolves to total SSI recipients in December 2027, in millions, as reported in the Social Security Administration Monthly Statistical Snapshot or SSI Monthly Statistics release for December 2027.",
    dataPointId: "ssa.ssi.recipients.2027-12",
    historicalContext: [
      { label: "Dec 2021", value: 7.71 },
      { label: "Dec 2023", value: 7.47 },
      { label: "Dec 2024", value: 7.42 },
      { label: "Dec 2025", value: 7.39 },
    ],
    drivers: [
      "Disability incidence and awards",
      "Continuing disability reviews",
      "Aged SSI eligibility",
      "COLA and income-offset effects",
    ],
    reasoning: [
      { kind: "heading", text: "Recipient-count target" },
      {
        kind: "text",
        text: "SSI federal payments already forecast dollars; this cell forecasts people receiving SSI. It lets an agent separate caseload from benefit-level and COLA effects.",
      },
      {
        kind: "tool",
        tool: "ssa.lookup",
        call: 'ssa.lookup({ table: "monthly_statistical_snapshot", series: "ssi_recipients", months: ["2021-12", "2025-12"] })',
        result:
          "{ dec2021: 7.71, dec2023: 7.47, dec2024: 7.42, dec2025: 7.39 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "ssi", year: 2027, month: "december", output: "recipients", takeup: "administrative_trend" })',
        result:
          '{ point: 7.34, ci80: [7.08, 7.66], drivers: ["awards", "reviews", "aging"] }',
      },
      {
        kind: "math",
        text: "Recent trend decline of roughly 0.2-0.4% per year implies 7.33-7.36M by December 2027.",
      },
      { kind: "forecast", point: 7.35, ciLow: 7.05, ciHigh: 7.7 },
    ],
  },

  {
    slug: "snap-average-monthly-households-fy2027",
    type: "data",
    title: "SNAP average monthly households, FY2027",
    question:
      "How many households will participate in SNAP in an average month of fiscal year 2027?",
    unit: "millions",
    pointEstimate: 21.7,
    ciLow: 19.8,
    ciHigh: 23.8,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "USDA FNS SNAP Data Tables",
    resolutionRule:
      "Resolves to average monthly SNAP households for FY2027, in millions, using the first USDA FNS national annual participation table that includes all months of fiscal year 2027.",
    dataPointId: "fns.snap.average_monthly_households.fy2027",
    historicalContext: [
      { label: "FY2021", value: 21.7 },
      { label: "FY2022", value: 21.6 },
      { label: "FY2023", value: 22.4 },
      { label: "FY2024", value: 22.0 },
    ],
    drivers: [
      "Low-income household count",
      "Benefit adequacy and take-up",
      "Recertification churn",
      "Household composition",
    ],
    reasoning: [
      { kind: "heading", text: "Household-count target" },
      {
        kind: "text",
        text: "SNAP persons and benefit dollars can move for different reasons. Household participation is the administrative count closest to caseload pressure and state operations.",
      },
      {
        kind: "tool",
        tool: "fns.lookup",
        call: 'fns.lookup({ program: "SNAP", series: "average_monthly_households", fiscal_years: [2021, 2024] })',
        result: "{ fy2021: 21.7, fy2022: 21.6, fy2023: 22.4, fy2024: 22.0 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "snap", year: 2027, output: "recipient_households", takeup: "calibrated" })',
        result:
          '{ point: 21.6, ci80: [20.0, 23.5], drivers: ["eligibility", "take-up", "household size"] }',
      },
      {
        kind: "math",
        text: "Persons forecast of 40.6M divided by a projected recipient household size of 1.87 gives 21.7M households.",
      },
      { kind: "forecast", point: 21.7, ciLow: 19.8, ciHigh: 23.8 },
    ],
  },

  {
    slug: "medicaid-chip-child-enrollment-dec-2027",
    type: "data",
    title: "Medicaid and CHIP child enrollment, December 2027",
    question:
      "How many children will be enrolled in Medicaid or CHIP in December 2027?",
    unit: "millions",
    pointEstimate: 36.8,
    ciLow: 34.5,
    ciHigh: 39.4,
    confidence: 0.8,
    resolutionDate: "2028-04-30",
    resolutionSource: "CMS Medicaid and CHIP monthly enrollment data",
    resolutionRule:
      "Resolves to Medicaid child and CHIP enrollment for December 2027, in millions, using the first CMS monthly Medicaid and CHIP enrollment report or data.Medicaid.gov release that reports the child-enrollment series for that month.",
    dataPointId: "cms.medicaid_chip.child_enrollment.2027-12",
    historicalContext: [
      { label: "Dec 2021", value: 40.0 },
      { label: "Sep 2024", value: 37.6 },
      { label: "Dec 2025e", value: 36.9 },
      { label: "Dec 2026e", value: 36.7 },
    ],
    drivers: [
      "Post-unwinding renewals",
      "Continuous eligibility for children",
      "State CHIP premiums",
      "Low-income child population",
    ],
    reasoning: [
      { kind: "heading", text: "Child coverage target" },
      {
        kind: "text",
        text: "Total Medicaid and CHIP enrollment mixes adults and children. The child count is the cleaner policy target for poverty and family-benefit forecasting because children face different eligibility and continuity rules.",
      },
      {
        kind: "tool",
        tool: "cms.lookup",
        call: 'cms.lookup({ dataset: "medicaid_chip_monthly_enrollment", series: "children_medicaid_plus_chip", months: ["2024-09", "2025-12"] })',
        result:
          "{ sep2024: 37.6, post_unwinding_trend: 'stabilizing', continuous_eligibility: true }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "medicaid_chip", year: 2027, month: "december", output: "child_enrollment", takeup: "renewal_churn" })',
        result:
          '{ point: 36.7, ci80: [34.8, 39.1], drivers: ["eligibility", "renewals", "CHIP premiums"] }',
      },
      {
        kind: "math",
        text: "Post-unwinding floor plus demographic drift: 37.6M · (1 - 0.7% annual net decline)^3 ≈ 36.8M.",
      },
      { kind: "forecast", point: 36.8, ciLow: 34.5, ciHigh: 39.4 },
    ],
  },

  {
    slug: "housing-choice-voucher-households-leased-dec-2027",
    type: "data",
    title: "Housing Choice Voucher households leased, December 2027",
    question:
      "How many households will be leased under the Housing Choice Voucher program in December 2027?",
    unit: "millions",
    pointEstimate: 2.34,
    ciLow: 2.18,
    ciHigh: 2.52,
    confidence: 0.8,
    resolutionDate: "2028-06-30",
    resolutionSource: "HUD Housing Choice Voucher Data Dashboard",
    resolutionRule:
      "Resolves to Housing Choice Voucher households leased for December 2027, in millions, using the HUD HCV Data Dashboard or the first official HUD utilization table that reports national leased households for that month.",
    dataPointId: "hud.hcv.households_leased.2027-12",
    historicalContext: [
      { label: "Dec 2019", value: 2.28 },
      { label: "Dec 2021", value: 2.32 },
      { label: "Dec 2023", value: 2.34 },
      { label: "Dec 2025e", value: 2.35 },
    ],
    drivers: [
      "Tenant-based rental assistance appropriations",
      "Per-unit cost inflation",
      "PHA lease-up rates",
      "Emergency voucher wind-down",
    ],
    reasoning: [
      { kind: "heading", text: "Leasing target" },
      {
        kind: "text",
        text: "Voucher outlays are already in the catalog; leased households isolate whether appropriations and rent inflation translate into families actually housed.",
      },
      {
        kind: "tool",
        tool: "hud.lookup",
        call: 'hud.lookup({ dashboard: "hcv", series: "households_leased", months: ["2019-12", "2025-12"] })',
        result:
          "{ dec2019: 2.28, dec2021: 2.32, dec2023: 2.34, dec2025_estimate: 2.35 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "housing_choice_voucher", year: 2027, month: "december", output: "households_leased", budget: "appropriations_baseline" })',
        result:
          '{ point: 2.33, ci80: [2.20, 2.49], drivers: ["appropriations", "rents", "lease-up"] }',
      },
      {
        kind: "math",
        text: "Central case is near-flat leasing: appropriations offset rent inflation enough to hold 2.3-2.4M households.",
      },
      { kind: "forecast", point: 2.34, ciLow: 2.18, ciHigh: 2.52 },
    ],
  },

  {
    slug: "school-breakfast-federal-outlays-fy2027",
    type: "data",
    title: "School Breakfast federal outlays, FY2027",
    question:
      "How much will the federal government spend on the School Breakfast Program in fiscal year 2027?",
    unit: "usd_billions",
    pointEstimate: 6.7,
    ciLow: 5.8,
    ciHigh: 7.8,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "USDA FNS Child Nutrition Tables",
    resolutionRule:
      "Resolves to federal School Breakfast Program cost for FY2027, in billions of nominal dollars, using the first USDA FNS child nutrition program table that reports fiscal-year federal cost.",
    dataPointId: "fns.sbp.federal_cost.fy2027",
    historicalContext: [
      { label: "FY2019", value: 4.5 },
      { label: "FY2022", value: 5.7 },
      { label: "FY2023", value: 5.5 },
      { label: "FY2024", value: 5.9 },
    ],
    drivers: [
      "Average daily participation",
      "Federal reimbursement rates",
      "Free and reduced-price share",
      "State universal-meals policies",
    ],
    reasoning: [
      { kind: "heading", text: "Cost target" },
      {
        kind: "text",
        text: "This pairs with the School Breakfast participation cell. The difference between the two is the reimbursement-rate and meal-mix channel.",
      },
      {
        kind: "tool",
        tool: "fns.lookup",
        call: 'fns.lookup({ program: "School Breakfast Program", series: "federal_cost", fiscal_years: [2019, 2024] })',
        result: "{ fy2019: 4.5, fy2022: 5.7, fy2023: 5.5, fy2024: 5.9 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "school_breakfast", year: 2027, output: "federal_cost", unit: "billions", reimbursement_rates: "indexed" })',
        result:
          '{ point: 6.6, ci80: [5.9, 7.6], drivers: ["participation", "meal mix", "rate indexation"] }',
      },
      {
        kind: "math",
        text: "15.2M participants × projected meals per year × indexed reimbursement yields roughly $6.7B.",
      },
      { kind: "forecast", point: 6.7, ciLow: 5.8, ciHigh: 7.8 },
    ],
  },

  {
    slug: "child-support-distributed-collections-fy2027",
    type: "data",
    title: "Child support distributed collections, FY2027",
    question:
      "How much child support will state and tribal programs distribute during fiscal year 2027?",
    unit: "usd_billions",
    pointEstimate: 27.8,
    ciLow: 25.0,
    ciHigh: 31.0,
    confidence: 0.8,
    resolutionDate: "2028-12-31",
    resolutionSource: "ACF Office of Child Support Services annual report",
    resolutionRule:
      "Resolves to total distributed child support collections for FY2027, in billions of nominal dollars, using the first ACF Office of Child Support Services preliminary or annual report covering fiscal year 2027.",
    dataPointId: "acf.ocss.distributed_collections.fy2027",
    historicalContext: [
      { label: "FY2019", value: 28.8 },
      { label: "FY2021", value: 27.9 },
      { label: "FY2022", value: 26.6 },
      { label: "FY2024e", value: 27.0 },
    ],
    drivers: [
      "Noncustodial-parent earnings",
      "Caseload size",
      "Enforcement collections",
      "Pass-through and distribution rules",
    ],
    reasoning: [
      { kind: "heading", text: "Family-resource target" },
      {
        kind: "text",
        text: "Child support collections are not a federal benefit outlay, but they are a measured family-resource flow that matters for poverty forecasts and policy simulations of custodial families.",
      },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ office: "OCSS", series: "distributed_collections", fiscal_years: [2019, 2024] })',
        result:
          "{ fy2019: 28.8, fy2021: 27.9, fy2022: 26.6, fy2024_estimate: 27.0 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "child_support", year: 2027, output: "distributed_collections", unit: "billions", earnings_model: "low_wage_workers" })',
        result:
          '{ point: 27.7, ci80: [25.2, 30.7], drivers: ["earnings", "caseload", "enforcement"] }',
      },
      {
        kind: "math",
        text: "Nominal earnings growth offsets caseload decline: $27.0B × 1.03^3 ≈ $29.5B, haircut for enforcement/caseload risk gives $27.8B.",
      },
      { kind: "forecast", point: 27.8, ciLow: 25.0, ciHigh: 31.0 },
    ],
  },

  {
    slug: "pell-grant-outlays-fy2027",
    type: "data",
    title: "Federal Pell Grant outlays, FY2027",
    question:
      "How much will the federal government spend on Federal Pell Grants during fiscal year 2027?",
    unit: "usd_billions",
    pointEstimate: 34.5,
    ciLow: 28.0,
    ciHigh: 43.0,
    confidence: 0.8,
    resolutionDate: "2028-06-30",
    resolutionSource:
      "U.S. Department of Education Federal Student Aid and budget data",
    resolutionRule:
      "Resolves to Federal Pell Grant program outlays or obligations for FY2027, in billions of nominal dollars, using the first official Department of Education Federal Student Aid annual report, budget justification, or Pell Grant program data table that reports fiscal-year spending.",
    dataPointId: "ed.pell.outlays.fy2027",
    historicalContext: [
      { label: "FY2019", value: 28.2 },
      { label: "FY2021", value: 26.0 },
      { label: "FY2023", value: 29.6 },
      { label: "FY2025e", value: 33.0 },
    ],
    drivers: [
      "Maximum Pell award",
      "Recipient count",
      "FAFSA simplification take-up",
      "Discretionary and mandatory funding rules",
    ],
    reasoning: [
      { kind: "heading", text: "Pairing recipients with dollars" },
      {
        kind: "text",
        text: "The catalog already forecasts Pell recipients. This cell forecasts fiscal cost, which can diverge if the maximum award or average Student Aid Index changes faster than enrollment.",
      },
      {
        kind: "tool",
        tool: "education.lookup",
        call: 'education.lookup({ program: "Federal Pell Grant", series: "program_cost", fiscal_years: [2019, 2025] })',
        result:
          "{ fy2019: 28.2, fy2021: 26.0, fy2023: 29.6, fy2025_estimate: 33.0 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "pell", year: 2027, output: "grant_outlays", unit: "billions", takeup: "fafsa_simplification" })',
        result:
          '{ point: 34.2, ci80: [28.6, 41.8], drivers: ["recipients", "maximum_award", "SAI distribution"] }',
      },
      {
        kind: "math",
        text: "7.2M recipients × roughly $4,800 average award ≈ $34.6B.",
      },
      { kind: "forecast", point: 34.5, ciLow: 28.0, ciHigh: 43.0 },
    ],
  },

  {
    slug: "wic-federal-outlays-fy2027",
    type: "data",
    title: "WIC federal outlays, FY2027",
    question:
      "How much will the federal government spend on WIC during fiscal year 2027?",
    unit: "usd_billions",
    pointEstimate: 8.5,
    ciLow: 7.2,
    ciHigh: 10.0,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "USDA FNS WIC program participation and costs data",
    resolutionRule:
      "Resolves to total federal WIC program cost for FY2027, in billions of nominal dollars, using the first USDA FNS WIC participation and cost table that reports fiscal-year total cost.",
    dataPointId: "usda.fns.wic.federal_cost.fy2027",
    historicalContext: [
      { label: "FY2019", value: 5.3 },
      { label: "FY2021", value: 5.0 },
      { label: "FY2023", value: 6.7 },
      { label: "FY2025e", value: 7.8 },
    ],
    drivers: [
      "Average monthly participation",
      "Food package costs",
      "Infant formula rebates",
      "Fruit and vegetable benefit levels",
    ],
    reasoning: [
      { kind: "heading", text: "Participation-cost bridge" },
      {
        kind: "text",
        text: "WIC dollars are driven by participants, food costs, and rebates. This provides a fiscal counterpart to the existing participation cell and gives agents a way to test whether cost growth comes from people served or per-person cost.",
      },
      {
        kind: "tool",
        tool: "fns.lookup",
        call: 'fns.lookup({ program: "WIC", series: "total_cost", fiscal_years: [2019, 2025] })',
        result:
          "{ fy2019: 5.3, fy2021: 5.0, fy2023: 6.7, fy2025_estimate: 7.8 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "wic", year: 2027, output: "federal_cost", unit: "billions", food_inflation: "cbo_food_at_home" })',
        result:
          '{ point: 8.4, ci80: [7.3, 9.8], drivers: ["participation", "food_package", "rebates"] }',
      },
      {
        kind: "math",
        text: "Participation near 6.9M and nominal food-package inflation put central cost near $8.5B.",
      },
      { kind: "forecast", point: 8.5, ciLow: 7.2, ciHigh: 10.0 },
    ],
  },

  {
    slug: "liheap-federal-funding-fy2027",
    type: "data",
    title: "LIHEAP federal funding, FY2027",
    question:
      "How much federal funding will be made available for LIHEAP during fiscal year 2027?",
    unit: "usd_billions",
    pointEstimate: 4.1,
    ciLow: 2.4,
    ciHigh: 6.8,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "ACF Office of Community Services LIHEAP funding tables",
    resolutionRule:
      "Resolves to total federal LIHEAP funding made available for FY2027, including regular block grant and contingency or supplemental funding, in billions of nominal dollars, using ACF Office of Community Services funding tables or LIHEAP Clearinghouse funding history.",
    dataPointId: "acf.liheap.federal_funding.fy2027",
    historicalContext: [
      { label: "FY2019", value: 3.7 },
      { label: "FY2021", value: 8.3 },
      { label: "FY2024", value: 4.1 },
      { label: "FY2026e", value: 4.0 },
    ],
    drivers: [
      "Annual appropriations",
      "Contingency funding",
      "Energy-price shocks",
      "Weather and emergency declarations",
    ],
    reasoning: [
      { kind: "heading", text: "Funding target" },
      {
        kind: "text",
        text: "The existing LIHEAP cell forecasts households assisted. This cell forecasts the federal funding envelope, which determines whether states serve more households or increase benefit amounts.",
      },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ program: "LIHEAP", series: "federal_funding", fiscal_years: [2019, 2026] })',
        result:
          "{ fy2019: 3.7, fy2021: 8.3, fy2024: 4.1, fy2026_estimate: 4.0 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "liheap", year: 2027, output: "federal_funding", unit: "billions", appropriation: "baseline_plus_tail" })',
        result:
          '{ point: 4.0, ci80: [2.6, 6.4], drivers: ["appropriations", "energy_prices", "weather"] }',
      },
      {
        kind: "math",
        text: "Regular funding near $4B with a disaster/energy-price supplemental tail gives a wide upper interval.",
      },
      { kind: "forecast", point: 4.1, ciLow: 2.4, ciHigh: 6.8 },
    ],
  },

  {
    slug: "oasdi-beneficiaries-dec-2027",
    type: "data",
    title: "OASDI beneficiaries, December 2027",
    question:
      "How many people will receive Old-Age, Survivors, and Disability Insurance benefits in December 2027?",
    unit: "millions",
    pointEstimate: 70.0,
    ciLow: 68.8,
    ciHigh: 71.4,
    confidence: 0.8,
    resolutionDate: "2028-02-28",
    resolutionSource: "SSA Monthly Statistical Snapshot",
    resolutionRule:
      "Resolves to total OASDI beneficiaries in current-payment status for December 2027, in millions, as reported in the Social Security Administration Monthly Statistical Snapshot or comparable SSA monthly beneficiary data.",
    dataPointId: "ssa.oasdi.beneficiaries.2027-12",
    historicalContext: [
      { label: "Dec 2021", value: 65.0 },
      { label: "Dec 2023", value: 67.1 },
      { label: "Dec 2025e", value: 68.4 },
      { label: "Dec 2026e", value: 69.2 },
    ],
    drivers: [
      "Population aging",
      "Retirement claiming age",
      "Disability incidence",
      "Mortality",
    ],
    reasoning: [
      { kind: "heading", text: "Caseload target" },
      {
        kind: "text",
        text: "The catalog already forecasts OASDI benefit outlays. Beneficiary count isolates the demographic component from COLA and average-benefit growth.",
      },
      {
        kind: "tool",
        tool: "ssa.lookup",
        call: 'ssa.lookup({ table: "monthly_statistical_snapshot", series: "oasdi_beneficiaries", months: ["2021-12", "2026-12"] })',
        result:
          "{ dec2021: 65.0, dec2023: 67.1, dec2025_estimate: 68.4, dec2026_estimate: 69.2 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "oasdi", year: 2027, month: "december", output: "beneficiaries", demographic_projection: "trustees_intermediate" })',
        result:
          '{ point: 70.0, ci80: [68.9, 71.2], drivers: ["aging", "claiming", "mortality"] }',
      },
      {
        kind: "math",
        text: "Recent growth of roughly 0.8M beneficiaries per year implies about 70.0M by December 2027.",
      },
      { kind: "forecast", point: 70.0, ciLow: 68.8, ciHigh: 71.4 },
    ],
  },

  {
    slug: "dependent-care-credit-claimant-returns-ty2026",
    type: "data",
    title: "Child and dependent care credit returns, TY2026",
    question:
      "How many individual income tax returns will claim the federal child and dependent care credit for tax year 2026?",
    unit: "millions",
    pointEstimate: 5.9,
    ciLow: 5.0,
    ciHigh: 7.0,
    confidence: 0.8,
    resolutionDate: "2028-12-31",
    resolutionSource: "IRS Statistics of Income individual tax return data",
    resolutionRule:
      "Resolves to the number of TY2026 individual income tax returns claiming the federal child and dependent care credit, in millions, using the first official IRS Statistics of Income individual income tax table that reports this credit.",
    dataPointId: "irs.soi.child_dependent_care_credit_returns.ty2026",
    historicalContext: [
      { label: "TY2019", value: 6.3 },
      { label: "TY2020", value: 5.6 },
      { label: "TY2021", value: 6.5 },
      { label: "TY2023e", value: 5.8 },
    ],
    drivers: [
      "Child care use among working parents",
      "Credit generosity and phaseout",
      "Filing and documentation behavior",
      "Labor force participation of parents",
    ],
    reasoning: [
      { kind: "heading", text: "Tax-credit take-up target" },
      {
        kind: "text",
        text: "The child and dependent care credit is a direct PolicyEngine-relevant tax unit output. Claimant returns are useful because the nonrefundable credit can have stable claims even when revenue cost changes with income and tax liability.",
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ dataset: "statistics_of_income", series: "child_dependent_care_credit_returns", tax_years: [2019, 2023] })',
        result:
          "{ ty2019: 6.3, ty2020: 5.6, ty2021: 6.5, ty2023_estimate: 5.8 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ credit: "child_dependent_care", year: 2026, output: "claimant_tax_units", takeup: "tax_filing_calibrated" })',
        result:
          '{ point: 5.9, ci80: [5.1, 6.8], drivers: ["childcare_expenses", "earned_income", "tax_liability"] }',
      },
      {
        kind: "math",
        text: "Parent employment and child-care cost growth keep claims near the post-2021 plateau: central case 5.9M.",
      },
      { kind: "forecast", point: 5.9, ciLow: 5.0, ciHigh: 7.0 },
    ],
  },

  {
    slug: "premium-tax-credit-claimant-returns-ty2026",
    type: "data",
    title: "Premium tax credit claimant returns, TY2026",
    question:
      "How many individual income tax returns will claim the federal premium tax credit for tax year 2026?",
    unit: "millions",
    pointEstimate: 10.8,
    ciLow: 7.4,
    ciHigh: 15.2,
    confidence: 0.8,
    resolutionDate: "2028-12-31",
    resolutionSource: "IRS Statistics of Income individual tax return data",
    resolutionRule:
      "Resolves to the number of TY2026 individual income tax returns claiming the premium tax credit or reconciling advance premium tax credits on Form 8962, in millions, using the first official IRS Statistics of Income table covering TY2026 individual returns.",
    dataPointId: "irs.soi.premium_tax_credit_claimant_returns.ty2026",
    historicalContext: [
      { label: "TY2019", value: 5.8 },
      { label: "TY2021", value: 8.9 },
      { label: "TY2023e", value: 11.2 },
      { label: "TY2025e", value: 13.2 },
    ],
    drivers: [
      "Enhanced premium tax credit status",
      "Exchange plan selections",
      "Advance credit reconciliation",
      "Household income distribution",
    ],
    reasoning: [
      { kind: "heading", text: "Tax-return access target" },
      {
        kind: "text",
        text: "This cell turns ACA coverage policy into an IRS administrative count. It should move with exchange enrollment but not one-for-one because family members aggregate onto tax returns and some households only reconcile advance credits.",
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ dataset: "statistics_of_income", series: "premium_tax_credit_claimant_returns", tax_years: [2019, 2025] })',
        result:
          "{ ty2019: 5.8, ty2021: 8.9, ty2023_estimate: 11.2, ty2025_estimate: 13.2 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ credit: "premium_tax_credit", year: 2026, output: "claimant_tax_units", takeup: "exchange_enrollment_calibrated" })',
        result:
          '{ point: 10.7, ci80: [7.8, 14.8], drivers: ["subsidy schedule", "exchange enrollment", "filing behavior"] }',
      },
      {
        kind: "math",
        text: "0.60·9.0M expiration branch + 0.35·14.0M extension branch + 0.05·10.5M partial branch ≈ 10.8M.",
      },
      { kind: "forecast", point: 10.8, ciLow: 7.4, ciHigh: 15.2 },
    ],
  },

  {
    slug: "additional-child-tax-credit-claimant-returns-ty2026",
    type: "data",
    title: "Additional Child Tax Credit returns, TY2026",
    question:
      "How many individual income tax returns will claim the refundable Additional Child Tax Credit for tax year 2026?",
    unit: "millions",
    pointEstimate: 16.2,
    ciLow: 13.2,
    ciHigh: 19.6,
    confidence: 0.8,
    resolutionDate: "2028-12-31",
    resolutionSource: "IRS Statistics of Income individual tax return data",
    resolutionRule:
      "Resolves to the number of TY2026 individual income tax returns claiming the refundable Additional Child Tax Credit, in millions, using the first official IRS Statistics of Income table covering TY2026 individual returns.",
    dataPointId: "irs.soi.additional_child_tax_credit_returns.ty2026",
    historicalContext: [
      { label: "TY2019", value: 17.6 },
      { label: "TY2021", value: 35.2 },
      { label: "TY2023e", value: 16.1 },
      { label: "TY2025e", value: 16.4 },
    ],
    drivers: [
      "CTC refundability formula",
      "Eligible child population",
      "Low-earnings phase-in",
      "Filing take-up among families with children",
    ],
    reasoning: [
      { kind: "heading", text: "Refundability target" },
      {
        kind: "text",
        text: "ACTC claimant returns isolate the refundable part of the CTC. That is the channel that matters most for child poverty and for whether a CTC expansion reaches low-income families.",
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ dataset: "statistics_of_income", series: "additional_child_tax_credit_returns", tax_years: [2019, 2025] })',
        result:
          "{ ty2019: 17.6, ty2021_expanded_ctc: 35.2, ty2023_estimate: 16.1, ty2025_estimate: 16.4 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ credit: "additional_child_tax_credit", year: 2026, output: "claimant_tax_units", takeup: "calibrated" })',
        result:
          '{ point: 16.1, ci80: [13.6, 19.2], drivers: ["phase_in", "refundability_cap", "eligible_children"] }',
      },
      {
        kind: "math",
        text: "Current-law and TCJA-extension branches both stay far below the 2021 expanded-CTC claimant spike; central case 16.2M.",
      },
      { kind: "forecast", point: 16.2, ciLow: 13.2, ciHigh: 19.6 },
    ],
  },

  {
    slug: "charitable-contributions-deduction-ty2026",
    type: "data",
    title: "Itemized charitable contributions, TY2026",
    question:
      "How much will individual income tax filers deduct for charitable contributions on itemized returns for tax year 2026?",
    unit: "usd_billions",
    pointEstimate: 305,
    ciLow: 245,
    ciHigh: 375,
    confidence: 0.8,
    resolutionDate: "2028-12-31",
    resolutionSource: "IRS Statistics of Income individual tax return data",
    resolutionRule:
      "Resolves to total charitable contributions deducted on TY2026 itemized individual income tax returns, in billions of nominal dollars, using the first official IRS Statistics of Income Schedule A or itemized-deductions table covering TY2026.",
    dataPointId: "irs.soi.itemized_charitable_contributions.ty2026",
    historicalContext: [
      { label: "TY2019", value: 236 },
      { label: "TY2020", value: 258 },
      { label: "TY2021", value: 283 },
      { label: "TY2023e", value: 285 },
    ],
    drivers: [
      "Itemizer count",
      "High-income capital gains",
      "Deduction law after TCJA",
      "Noncash giving and bunching",
    ],
    reasoning: [
      { kind: "heading", text: "Itemized deduction target" },
      {
        kind: "text",
        text: "Charitable deductions connect tax policy to nonprofit funding behavior. The forecast is sensitive to whether itemization remains constrained by a high standard deduction and SALT cap.",
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ dataset: "statistics_of_income", table: "itemized_deductions", series: "charitable_contributions", tax_years: [2019, 2023] })',
        result:
          "{ ty2019: 236, ty2020: 258, ty2021: 283, ty2023_estimate: 285 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ deduction: "charitable_contributions", year: 2026, output: "itemized_amount", unit: "billions", behavior: "giving_elasticity_central" })',
        result:
          '{ point: 302, ci80: [252, 365], drivers: ["itemizers", "asset_prices", "deduction_law"] }',
      },
      {
        kind: "math",
        text: "Nominal giving growth plus itemization-policy uncertainty: $285B · 1.023^3 ≈ $305B.",
      },
      { kind: "forecast", point: 305, ciLow: 245, ciHigh: 375 },
    ],
  },

  {
    slug: "medicare-total-enrollment-dec-2027",
    type: "data",
    title: "Medicare total enrollment, December 2027",
    question: "How many people will be enrolled in Medicare in December 2027?",
    unit: "millions",
    pointEstimate: 70.7,
    ciLow: 69.2,
    ciHigh: 72.3,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "CMS Medicare Monthly Enrollment data",
    resolutionRule:
      "Resolves to total Medicare beneficiaries for December 2027, in millions, using the first CMS Medicare Monthly Enrollment dataset or Medicare Enrollment Report that includes national December 2027 enrollment.",
    dataPointId: "cms.medicare.total_beneficiaries.2027-12",
    historicalContext: [
      { label: "Dec 2021", value: 64.5 },
      { label: "Dec 2023", value: 66.7 },
      { label: "Jan 2026", value: 68.8 },
      { label: "Dec 2026e", value: 69.7 },
    ],
    drivers: [
      "Population aging into Medicare",
      "Disability enrollment",
      "Mortality",
      "Medicare Advantage and original Medicare retention",
    ],
    reasoning: [
      { kind: "heading", text: "Enrollment target" },
      {
        kind: "text",
        text: "Medicare benefit outlays combine enrollment, benefit mix, and health-care prices. Total enrollment gives the demographic denominator for those spending forecasts.",
      },
      {
        kind: "tool",
        tool: "cms.lookup",
        call: 'cms.lookup({ dataset: "medicare_monthly_enrollment", series: "total_beneficiaries", months: ["2021-12", "2026-01"] })',
        result:
          "{ dec2021: 64.5, dec2023: 66.7, jan2026: 68.8, trend: 'aging-driven growth' }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "medicare", year: 2027, month: "december", output: "total_beneficiaries", demographic_projection: "trustees_intermediate" })',
        result:
          '{ point: 70.6, ci80: [69.4, 72.0], drivers: ["age_65_entries", "mortality", "disability"] }',
      },
      {
        kind: "math",
        text: "Recent 0.9-1.1M annual growth from the January 2026 base implies about 70.7M by December 2027.",
      },
      { kind: "forecast", point: 70.7, ciLow: 69.2, ciHigh: 72.3 },
    ],
  },

  {
    slug: "retired-worker-average-benefit-dec-2027",
    type: "data",
    title: "Retired-worker average benefit, December 2027",
    question:
      "What will the average monthly Social Security retired-worker benefit be in December 2027?",
    unit: "usd_monthly",
    pointEstimate: 2190,
    ciLow: 2110,
    ciHigh: 2285,
    confidence: 0.8,
    resolutionDate: "2028-02-28",
    resolutionSource: "SSA Monthly Statistical Snapshot",
    resolutionRule:
      "Resolves to the average monthly benefit for retired workers in current-payment status for December 2027, in nominal dollars, as reported in the Social Security Administration Monthly Statistical Snapshot.",
    dataPointId: "ssa.oasdi.retired_worker_average_benefit.2027-12",
    historicalContext: [
      { label: "Dec 2021", value: 1658 },
      { label: "Dec 2023", value: 1848 },
      { label: "Dec 2025e", value: 2010 },
      { label: "Dec 2026e", value: 2090 },
    ],
    drivers: [
      "COLA path",
      "New retired-worker benefit levels",
      "Claiming-age composition",
      "Mortality and cohort replacement",
    ],
    reasoning: [
      { kind: "heading", text: "Benefit-level target" },
      {
        kind: "text",
        text: "OASDI outlays are a product of beneficiary count and average benefit. This cell gives a clean check on the benefit-level side, especially COLA and cohort replacement.",
      },
      {
        kind: "tool",
        tool: "ssa.lookup",
        call: 'ssa.lookup({ table: "monthly_statistical_snapshot", series: "retired_worker_average_benefit", months: ["2021-12", "2026-12"] })',
        result:
          "{ dec2021: 1658, dec2023: 1848, dec2025_estimate: 2010, dec2026_estimate: 2090 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "oasdi", year: 2027, month: "december", output: "retired_worker_average_benefit", cola: "cpi_w_forecast" })',
        result:
          '{ point: 2185, ci80: [2120, 2270], drivers: ["cola", "new_awards", "claiming_age"] }',
      },
      {
        kind: "math",
        text: "$2,090 base × 1.035 COLA/benefit-mix growth ≈ $2,163, with new-award cohort replacement lifting the central estimate to $2,190.",
      },
      { kind: "forecast", point: 2190, ciLow: 2110, ciHigh: 2285 },
    ],
  },

  {
    slug: "ctc-refundable-amount-ty2027",
    type: "policy",
    title: "Refundable CTC amount, TY2027",
    question:
      "What will the maximum refundable portion of the federal Child Tax Credit be per qualifying child in tax year 2027?",
    unit: "usd",
    pointEstimate: 1800,
    ciLow: 1000,
    ciHigh: 2500,
    confidence: 0.8,
    resolutionDate: "2027-12-31",
    resolutionSource: "Internal Revenue Code section 24 and IRS instructions",
    resolutionRule:
      "Resolves to the maximum refundable federal Child Tax Credit amount per qualifying child for TY2027, using IRC section 24 and the first IRS Form 1040 instructions or inflation-adjusted tax parameter release that identifies the refundable amount.",
    policyParameter: "irc.24.refundable_amount_per_child.2027",
    historicalContext: [
      { label: "TY2021", value: 3000 },
      { label: "TY2022", value: 1500 },
      { label: "TY2024", value: 1700 },
      { label: "TY2025e", value: 1700 },
    ],
    drivers: [
      "TCJA extension package",
      "Refundability politics",
      "Inflation indexation",
      "Budget score of low-income family provisions",
    ],
    reasoning: [
      { kind: "heading", text: "Separating amount from eligibility" },
      {
        kind: "text",
        text: "The maximum refundable CTC amount is the policy parameter that drives outlays and child-poverty effects for low-income families. It is distinct from the headline maximum credit because families with low earnings can be limited by the refundable cap and phase-in.",
      },
      { kind: "heading", text: "Law branches" },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.24", parameter: "refundable_amount_per_child", year: 2027, branch: "post_sunset_current_law" })',
        result:
          '{ value: 1000, note: "credit reverts and refundable structure narrows under scheduled law" }',
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.24", parameter: "refundable_amount_per_child", year: 2027, branch: "tcja_extended_indexed" })',
        result:
          '{ value: 1800, note: "current refundable amount retained and indexed" }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ reform: "ctc_refundable_amount_1800", year: 2027, output: ["ctc_outlays", "spm_child_poverty_rate"], unit: "billions" })',
        result:
          '{ outlays: 64.0, child_poverty_rate: 11.6, sensitivity: "about $5B per additional $100 refundable cap near the phase-in margin" }',
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "math",
        text: "P(indexed current cap) = 0.55; P($1,000 reversion) = 0.20; P(larger refundable expansion) = 0.20; P(other) = 0.05.",
      },
      {
        kind: "text",
        text: "The modal outcome is retaining the current refundable design with indexation. The lower tail remains real because the scheduled-law branch is a discrete cliff; the upper tail reflects a child-credit compromise that expands refundability without restoring the full 2021 policy.",
      },
      { kind: "forecast", point: 1800, ciLow: 1000, ciHigh: 2500 },
    ],
  },

  {
    slug: "eitc-max-credit-three-children-ty2027",
    type: "policy",
    title: "Maximum EITC, 3+ children, TY2027",
    question:
      "What will the maximum federal Earned Income Tax Credit be for tax units with three or more qualifying children in tax year 2027?",
    unit: "usd",
    pointEstimate: 8500,
    ciLow: 8050,
    ciHigh: 9100,
    confidence: 0.8,
    resolutionDate: "2026-10-31",
    resolutionSource: "IRS inflation-adjusted tax parameters",
    resolutionRule:
      "Resolves to the maximum EITC for taxpayers with three or more qualifying children for TY2027, using the IRS annual inflation-adjusted tax parameter release or equivalent official IRS table.",
    policyParameter: "irc.32.max_credit.three_or_more_children.2027",
    historicalContext: [
      { label: "TY2021", value: 6728 },
      { label: "TY2023", value: 7430 },
      { label: "TY2025e", value: 8046 },
      { label: "TY2026e", value: 8260 },
    ],
    drivers: [
      "CPI-U chained tax indexation",
      "Low-income tax package changes",
      "Interaction with childless-worker EITC politics",
    ],
    reasoning: [
      { kind: "heading", text: "Parameter target" },
      {
        kind: "text",
        text: "This cell forecasts a core EITC schedule parameter. The baseline is mostly mechanical indexation, but it is worth tracking because small parameter changes cascade into EITC outlays, marginal tax rates, and poverty forecasts.",
      },
      {
        kind: "tool",
        tool: "irs.lookup",
        call: 'irs.lookup({ table: "inflation_adjusted_tax_parameters", parameter: "eitc_max_credit_3plus_children", years: [2021, 2026] })',
        result:
          "{ ty2021: 6728, ty2023: 7430, ty2025_estimate: 8046, ty2026_estimate: 8260 }",
      },
      {
        kind: "tool",
        tool: "axiom.query",
        call: 'axiom.query({ statute: "IRC.32", parameter: "max_credit_3plus_children", year: 2027, branch: "indexed_current_law" })',
        result:
          '{ formula: "prior_year_amount indexed by chained CPI-U", projected_value: 8500 }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ policy: "current_law", year: 2027, output: "eitc_outlays", perturbation: "max_credit_3plus_children_plus_100" })',
        result:
          '{ marginal_outlay_per_100: 0.9, note: "billions of dollars before take-up calibration" }',
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The central estimate follows inflation indexation from the TY2026 estimate. The upper tail allows for a family-credit package that modestly raises EITC parameters; the lower tail is mainly lower CPI and rounding, not repeal.",
      },
      { kind: "forecast", point: 8500, ciLow: 8050, ciHigh: 9100 },
    ],
  },

  {
    slug: "snap-average-benefit-per-person-fy2027",
    type: "data",
    title: "SNAP average benefit per person, FY2027",
    question:
      "What will the average monthly SNAP benefit per person be in fiscal year 2027?",
    unit: "usd_monthly",
    pointEstimate: 232,
    ciLow: 216,
    ciHigh: 252,
    confidence: 0.8,
    resolutionDate: "2028-03-31",
    resolutionSource: "USDA FNS SNAP Data Tables",
    resolutionRule:
      "Resolves to average monthly SNAP benefits per person for FY2027, in nominal dollars, using the first USDA FNS national SNAP annual table that reports benefits per person for all months of fiscal year 2027.",
    dataPointId: "usda.fns.snap.average_benefit_per_person.fy2027",
    historicalContext: [
      { label: "FY2019", value: 130 },
      { label: "FY2021", value: 230 },
      { label: "FY2023", value: 213 },
      { label: "FY2024", value: 211 },
    ],
    drivers: [
      "Thrifty Food Plan indexation",
      "Net income distribution among recipients",
      "Household-size mix",
      "Farm Bill benefit formula changes",
    ],
    reasoning: [
      { kind: "heading", text: "Benefit intensity target" },
      {
        kind: "text",
        text: "SNAP caseload and total outlays are already separate cells. Average monthly benefit per person isolates the benefit-formula and income-composition channel, which is the piece PolicyEngine can forecast from household resources.",
      },
      {
        kind: "tool",
        tool: "fns.lookup",
        call: 'fns.lookup({ program: "SNAP", series: "average_monthly_benefit_per_person", fiscal_years: [2019, 2024] })',
        result:
          '{ fy2019: 130, fy2021: 230, fy2023: 213, fy2024: 211, emergency_allotments: "ended" }',
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "snap", year: 2027, output: "monthly_benefit_per_person", map_to: "person", benefit_formula: "fy2027_indexed" })',
        result:
          '{ point: 231, ci80: [218, 249], drivers: ["max allotment", "net income", "household size"] }',
      },
      {
        kind: "math",
        text: "Total benefits / person-months cross-check: $128B / (46M persons x 12) = $232/mo.",
      },
      { kind: "forecast", point: 232, ciLow: 216, ciHigh: 252 },
    ],
  },

  {
    slug: "ptc-average-subsidy-per-enrollee-fy2027",
    type: "data",
    title: "ACA PTC average subsidy per enrollee, FY2027",
    question:
      "What will the average monthly ACA premium tax credit subsidy per subsidized marketplace enrollee be in fiscal year 2027?",
    unit: "usd_monthly",
    pointEstimate: 690,
    ciLow: 560,
    ciHigh: 860,
    confidence: 0.8,
    resolutionDate: "2028-06-30",
    resolutionSource: "CMS marketplace and Treasury outlay tables",
    resolutionRule:
      "Resolves to average monthly premium tax credit subsidy per subsidized marketplace enrollee for FY2027, computed from official CMS enrollment and Treasury/CMS PTC outlay tables when both are available.",
    dataPointId: "cms.marketplace.ptc.average_subsidy_per_enrollee.fy2027",
    historicalContext: [
      { label: "FY2020", value: 520 },
      { label: "FY2022", value: 575 },
      { label: "FY2024", value: 650 },
      { label: "FY2026e", value: 720 },
    ],
    drivers: [
      "Enhanced PTC extension status",
      "Benchmark silver premiums",
      "Income mix of remaining enrollees",
      "Plan switching and silver loading",
    ],
    reasoning: [
      { kind: "heading", text: "Why average subsidy matters" },
      {
        kind: "text",
        text: "PTC outlays can fall because enrollment falls or because the subsidy per enrollee falls. This cell isolates the per-enrollee subsidy, which is the clean target for modeling premium growth and subsidy formula changes.",
      },
      {
        kind: "tool",
        tool: "cms.lookup",
        call: 'cms.lookup({ program: "marketplace", series: ["subsidized_enrollment", "average_aptc"], years: [2020, 2026] })',
        result:
          "{ fy2020: 520, fy2022: 575, fy2024: 650, fy2026_estimate: 720 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "aca_ptc", year: 2027, output: "average_monthly_subsidy_per_subsidized_enrollee", policy: "enhanced_ptc_expires" })',
        result:
          '{ point: 680, ci80: [560, 840], drivers: ["premium growth", "income mix", "subsidy cliff"] }',
      },
      {
        kind: "text",
        text: "If enhanced subsidies expire, lower-subsidy marginal enrollees leave first, mechanically raising average subsidy among those who remain. That composition effect offsets part of the statutory subsidy reduction.",
      },
      { kind: "forecast", point: 690, ciLow: 560, ciHigh: 860 },
    ],
  },

  // ─── Conditional forecast cells ──────────────────────────────────────────
  {
    slug: "child-poverty-2028-given-tcja-extended-q2-2026",
    type: "conditional",
    title: "Child poverty 2028 | TCJA extension passes by Q2 2026",
    question:
      "Conditional on a full TCJA extension package (CTC at $2,000, current refundability, current EITC) being enacted by June 30, 2026, what will the SPM child poverty rate be in 2028?",
    unit: "percent",
    pointEstimate: 11.5,
    ciLow: 10.3,
    ciHigh: 12.8,
    confidence: 0.8,
    resolutionDate: "2029-09-15",
    resolutionSource: "Census SPM annual release",
    resolutionRule:
      "Resolves to the official Census SPM child poverty rate for 2028, conditional on the event 'a TCJA extension package matching at least the House-passed framework on CTC and EITC is enacted by 2026-06-30.' If the conditioning event does not occur, the forecast cell is marked unresolved.",
    conditionalOn:
      "TCJA extension package matching House framework enacted by 2026-06-30",
    dataPointId: "census.spm.child_poverty_rate.2028",
    historicalContext: [
      { label: "2022", value: 12.4 },
      { label: "2023", value: 13.7 },
      { label: "2024", value: 13.4 },
      { label: "2025e", value: 12.9 },
      { label: "2027e (cond.)", value: 11.8 },
    ],
    drivers: [
      "Conditional CTC parameters",
      "Labor-force trajectory under stable policy",
      "Refundability phase-in",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the conditional" },
      {
        kind: "text",
        text: "Conditional resolution: only meaningful if a TCJA-extension package matching the House framework is enacted by June 30, 2026. Under that conditioning event, the CTC ($2,000/child, $1,700 refundable) and EITC are stable through 2028. Question is the residual SPM child-poverty path under stable policy.",
      },
      { kind: "heading", text: "Microsim under the conditioning policy" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "tcja_extended_full", year: 2028, output: "spm_child_poverty_rate", population: "microplex.us.2028" })',
        result: "{ point: 11.3, ci80: [10.4, 12.3] }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "tcja_extended_full", year: 2028, output: "spm_child_poverty_rate", population: "microplex.us.2028", macro: "cbo_baseline_2028" })',
        result: "{ point: 11.5, ci80: [10.3, 12.7] }",
      },
      { kind: "heading", text: "Compounding effects" },
      {
        kind: "text",
        text: "Two years of stable policy compound modestly: real-wage growth at the lower end of the distribution lifts roughly 0.2pp of children out of measured poverty. Refundable-credit take-up rates also drift up slightly as IRS outreach matures.",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "tcja_extended_full", year: 2028, output: "spm_child_poverty_rate", population: "microplex.us.2028", takeup_adjustment: "trend" })',
        result: "{ point: 11.4, ci80: [10.3, 12.5] }",
      },
      { kind: "heading", text: "Residual uncertainty" },
      {
        kind: "text",
        text: "The conditioning event removes most policy uncertainty but does not remove macro uncertainty (labor market, food/shelter inflation in SPM thresholds). CI reflects macro distribution only.",
      },
      { kind: "forecast", point: 11.5, ciLow: 10.3, ciHigh: 12.8 },
    ],
  },

  {
    slug: "child-poverty-2026-given-ctc-3000-refundable",
    type: "conditional",
    title: "Child poverty 2026 | $3,000 fully refundable CTC",
    question:
      "Conditional on a $3,000 fully refundable Child Tax Credit being in effect for tax year 2026, what will the Supplemental Poverty Measure child poverty rate be for calendar year 2026?",
    unit: "percent",
    pointEstimate: 7.2,
    ciLow: 5.8,
    ciHigh: 9.0,
    confidence: 0.8,
    resolutionDate: "2027-09-15",
    resolutionSource: "U.S. Census Bureau, SPM annual release",
    resolutionRule:
      "Resolves to the official Census SPM child poverty rate for calendar year 2026, conditional on a materially equivalent $3,000 fully refundable CTC being in effect for TY2026. If the policy is not in effect, the forecast cell is marked unresolved.",
    conditionalOn:
      "$3,000 fully refundable Child Tax Credit in effect for tax year 2026",
    dataPointId: "census.spm.child_poverty_rate.2026",
    historicalContext: [
      { label: "2021", value: 5.2 },
      { label: "2022", value: 12.4 },
      { label: "2023", value: 13.7 },
      { label: "2024", value: 13.4 },
      { label: "Policy sim", value: 7.0 },
    ],
    drivers: [
      "Refundable CTC take-up",
      "Macro labor-market path",
      "SPM poverty thresholds",
      "Tax-unit to SPM-unit mapping",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the conditional" },
      {
        kind: "text",
        text: "This cell asks what the observed SPM child poverty rate would be if the $3,000 fully refundable CTC policy is actually in force for TY2026. Policy uncertainty is removed; macro and measurement uncertainty remain.",
      },
      { kind: "heading", text: "PolicyEngine anti-poverty effect" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ reform: "ctc_3000_fully_refundable", year: 2026, output: "spm_child_poverty_rate", map_to: "person" })',
        result:
          "{ point: 6.9, ci80: [5.9, 8.3], poverty_reduction_pp_vs_current_law: -5.1 }",
      },
      {
        kind: "tool",
        tool: "census.lookup",
        call: 'census.lookup({ series: "spm_child_poverty_rate", years: [2021, 2024], note: "expanded CTC anchor" })',
        result:
          "{ ctc_expansion_anchor_2021: 5.2, post_expansion_range: [12.4, 13.7] }",
      },
      { kind: "heading", text: "Forecast" },
      {
        kind: "text",
        text: "The 2021 expanded-CTC anchor prevents over-shrinking toward current-law poverty, while the 2026 macro path and take-up uncertainty keep the interval above the raw simulation lower tail.",
      },
      { kind: "forecast", point: 7.2, ciLow: 5.8, ciHigh: 9.0 },
    ],
  },

  {
    slug: "iit-revenue-fy2028-given-salt-fully-repealed",
    type: "conditional",
    title:
      "Federal individual income tax revenue FY2028 | SALT cap fully repealed",
    question:
      "Conditional on the SALT deduction cap being repealed in full (no cap) for tax years 2026 and later, what will federal individual income tax revenue be in FY2028 (in billions of nominal dollars)?",
    unit: "usd",
    pointEstimate: 2790,
    ciLow: 2630,
    ciHigh: 2960,
    confidence: 0.8,
    resolutionDate: "2028-10-20",
    resolutionSource:
      "U.S. Treasury Monthly Statement (final September FY2028)",
    resolutionRule:
      "Resolves to total individual income tax receipts for FY2028 as reported in the Monthly Treasury Statement covering September 2028, conditional on the SALT deduction cap under IRC §164(b)(6) being fully eliminated for TY2026 and later. If the cap is not fully eliminated, the forecast cell is marked unresolved.",
    conditionalOn:
      "IRC §164(b)(6) SALT cap fully eliminated for TY2026 and later",
    dataPointId: "treasury.mts.individual_income_tax.fy2028",
    historicalContext: [
      { label: "FY2024", value: 2426 },
      { label: "FY2025e", value: 2520 },
      { label: "FY2026e", value: 2640 },
      { label: "FY2027e", value: 2740 },
    ],
    drivers: [
      "Itemizer redistribution effect",
      "Behavioral response (state tax migration, charitable shifts)",
      "Underlying nominal income growth",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the conditional" },
      {
        kind: "text",
        text: "Conditional on no cap, the principal effect on FY2028 IIT receipts is a static revenue loss of roughly $90–110bn relative to a $10k-cap counterfactual. Dynamic effects (more itemization, slightly more state/local tax-raising behavior at the state level) are second order.",
      },
      { kind: "heading", text: "Microsim under no-cap" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "no_salt_cap_with_tcja_extended", year: 2028, output: "individual_income_tax_receipts_fy", policy_year: 2027 })',
        result:
          "{ point: 2785, ci80: [2620, 2960], static_revenue_loss_vs_10k_cap: -98 }",
      },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "budget_outlook_2026", series: "salt_cap_repeal_revenue_effect", year: "FY2028" })',
        result: "{ static_effect: -107, dynamic_effect: -118 }",
      },
      { kind: "heading", text: "Behavioral adjustments" },
      {
        kind: "text",
        text: "Behavioral effects increase the dynamic revenue loss by ~10%. Itemization rates rise from current ~10% back toward the pre-TCJA ~30%. State and local tax-raising behavior responds modestly at the margin.",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "no_salt_cap_with_tcja_extended", year: 2028, output: "individual_income_tax_receipts_fy", behavioral: "central" })',
        result: "{ point: 2790, ci80: [2630, 2960] }",
      },
      { kind: "heading", text: "Forecast" },
      { kind: "forecast", point: 2790, ciLow: 2630, ciHigh: 2960 },
    ],
  },

  {
    slug: "uninsured-2028-given-ept-expire",
    type: "conditional",
    title: "Uninsured rate (under 65) 2028 | ACA enhanced subsidies expire",
    question:
      "Conditional on the ACA enhanced premium tax credits (ARPA/IRA expansion) expiring as scheduled at end of 2025 and not being restored through 2028, what will the uninsured rate (under 65) be in calendar year 2028?",
    unit: "percent",
    pointEstimate: 11.3,
    ciLow: 10.2,
    ciHigh: 12.4,
    confidence: 0.8,
    resolutionDate: "2029-09-15",
    resolutionSource: "Census ASEC health insurance report",
    resolutionRule:
      "Resolves to the uninsured rate among people under 65 as reported by the Census ASEC for calendar year 2028, conditional on no restoration of the enhanced ACA premium tax credits (above the original ACA-baseline subsidies) through 2028. If subsidies are restored at any point, the forecast cell is marked unresolved.",
    conditionalOn:
      "Enhanced ACA premium tax credits remain expired through end of 2028",
    dataPointId: "census.asec.uninsured_rate_under_65.2028",
    historicalContext: [
      { label: "2021", value: 9.6 },
      { label: "2022", value: 8.6 },
      { label: "2023", value: 8.0 },
      { label: "2024", value: 8.2 },
      { label: "2025e", value: 8.9 },
      { label: "2026e (cond.)", value: 10.4 },
    ],
    drivers: [
      "Marketplace coverage attrition trajectory",
      "Medicaid take-up among newly-priced-out",
      "ESI coverage churn",
    ],
    reasoning: [
      { kind: "heading", text: "Identifying the conditional" },
      {
        kind: "text",
        text: "By 2028, the post-expiration equilibrium will largely have settled. Initial-year coverage loss is sharp; subsequent years see partial reabsorption through Medicaid (for those whose new effective premiums exceed thresholds) and back-to-ESI churn. The 2028 uninsured-rate question is about the equilibrium, not the transient.",
      },
      { kind: "heading", text: "Microsim equilibrium" },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "ept_expired_persistent", year: 2028, output: "uninsured_rate_under_65", model: "demand_aces" })',
        result:
          "{ point: 11.2, ci80: [10.3, 12.2], coverage_loss_marketplace: -3.4M, medicaid_reabsorption: +0.8M, esi_pickup: +0.2M }",
      },
      {
        kind: "tool",
        tool: "cbo.lookup",
        call: 'cbo.lookup({ table: "health_insurance_baseline_2026", series: "uninsured_rate_under_65", year: 2028, policy: "ept_permanent_expiration" })',
        result: "{ value: 11.5 }",
      },
      { kind: "heading", text: "Compounding factors" },
      {
        kind: "text",
        text: "Two compounding factors push the 2028 number slightly above the 2026 conditional number: (a) marketplace plans become less attractive as some insurers exit subsidy-dependent regions, (b) underlying premium growth makes unsubsidized coverage less affordable for the 200-400% FPL population.",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "ept_expired_persistent", year: 2028, output: "uninsured_rate_under_65", model: "demand_aces", insurer_exit: "central" })',
        result: "{ point: 11.3, ci80: [10.2, 12.4] }",
      },
      { kind: "heading", text: "Forecast" },
      { kind: "forecast", point: 11.3, ciLow: 10.2, ciHigh: 12.4 },
    ],
  },

  ...BENEFITS_DELIVERY_MARKETS,
];

export function getMarket(slug: string): Market | undefined {
  return MARKETS.find((m) => m.slug === slug);
}

export function formatValue(value: number, unit: Unit): string {
  switch (unit) {
    case "percent":
      return `${value.toFixed(1)}%`;
    case "percent_growth":
      return `${value >= 0 ? "+" : ""}${value.toFixed(1)}%`;
    case "usd":
      if (Math.abs(value) >= 1000) {
        return `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
      }
      return `$${value.toFixed(2)}`;
    case "usd_billions":
      return `$${value.toLocaleString(undefined, { maximumFractionDigits: 1 })}B`;
    case "usd_monthly":
      return `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}/mo`;
    case "millions":
      return `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })}M`;
    case "ratio":
      return value.toFixed(2);
    default:
      return value.toString();
  }
}

export function formatValueShort(value: number, unit: Unit): string {
  if (unit === "usd" && Math.abs(value) >= 1000) {
    return `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}B`;
  }
  return formatValue(value, unit);
}

export const TYPE_LABEL: Record<MarketType, string> = {
  data: "Government data",
  policy: "Policy",
  conditional: "Conditional",
};

export const TYPE_DESCRIPTION: Record<MarketType, string> = {
  data: "Forecast cell on a published government data point.",
  policy: "Forecast cell on a law-encoded policy parameter.",
  conditional: "Outcome forecast conditional on a policy state.",
};
