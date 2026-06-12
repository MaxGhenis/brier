import { generateObject } from "ai";
import { z } from "zod";
import type { CpiDataset } from "@/lib/bls";
import type { SpmChildPovertyDataset } from "@/lib/census";
import type { CtcExpansionDataset } from "@/lib/policyengine";
import {
  AgentNumericCdfDistributionSchema,
  buildNumericCdfFromInterval,
  normalizeNumericCdfDistribution,
  summarizeNumericCdfDistribution,
  type NumericCdfDistribution,
} from "@/lib/prediction-distribution";

const ForecastSchema = z.object({
  distribution: AgentNumericCdfDistributionSchema,
  publicTrace: z.array(z.string().min(20).max(700)).min(3).max(6),
  assumptions: z.array(z.string().min(8).max(240)).min(2).max(6),
  dataCaveats: z.array(z.string().min(8).max(240)).min(1).max(4),
  drivers: z.array(z.string().min(4).max(80)).min(2).max(5),
});

const CtcExpansionForecastSchema = z.object({
  distribution: AgentNumericCdfDistributionSchema,
  publicTrace: z.array(z.string().min(20).max(700)).min(3).max(7),
  assumptions: z.array(z.string().min(8).max(240)).min(2).max(6),
  dataCaveats: z.array(z.string().min(8).max(240)).min(1).max(5),
  drivers: z.array(z.string().min(4).max(90)).min(2).max(5),
});

const SpmChildPovertyForecastSchema = z.object({
  distribution: AgentNumericCdfDistributionSchema,
  publicTrace: z.array(z.string().min(20).max(700)).min(3).max(7),
  assumptions: z.array(z.string().min(8).max(240)).min(2).max(6),
  dataCaveats: z.array(z.string().min(8).max(260)).min(1).max(5),
  drivers: z.array(z.string().min(4).max(90)).min(2).max(5),
});

export interface CpiForecast {
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  confidence: 0.8;
  distribution: NumericCdfDistribution;
  publicTrace: string[];
  assumptions: string[];
  dataCaveats: string[];
  drivers: string[];
  source: "ai_gateway" | "deterministic_fallback";
  model?: string;
  generatedAt: string;
}

export interface CtcExpansionForecast {
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  confidence: 0.8;
  distribution: NumericCdfDistribution;
  publicTrace: string[];
  assumptions: string[];
  dataCaveats: string[];
  drivers: string[];
  source: "ai_gateway" | "calibration_fallback";
  model?: string;
  generatedAt: string;
}

export interface SpmChildPovertyForecast {
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  confidence: 0.8;
  distribution: NumericCdfDistribution;
  publicTrace: string[];
  assumptions: string[];
  dataCaveats: string[];
  drivers: string[];
  source: "ai_gateway" | "census_calibration_fallback";
  model?: string;
  generatedAt: string;
}

export async function generateCpiForecast(
  dataset: CpiDataset,
): Promise<CpiForecast> {
  if (!shouldTryGateway()) {
    return fallbackForecast(
      dataset,
      "AI Gateway credentials are not configured.",
    );
  }

  const model =
    process.env.THESIS_AI_MODEL ??
    process.env.BRIER_AI_MODEL ??
    "anthropic/claude-sonnet-4.6";

  try {
    const result = await generateObject({
      model,
      schema: ForecastSchema,
      temperature: 0.2,
      system:
        "You are a Thesis Institute public forecasting agent. Produce concise, audit-ready reasoning for public readers. Your public trace must name an explicit base rate or reference class (the distribution of recent comparable prints), state the mechanism behind the point estimate, and include at least one disconfirming consideration that would land the outcome outside your interval. Do not reveal hidden chain-of-thought; provide a public trace with evidence, assumptions, and uncertainty.",
      prompt: [
        "Forecast this public prediction cell:",
        "What will the annual average percent change in CPI-U for calendar year 2026 versus the 2025 annual average be, as published by BLS?",
        "",
        "Use the live BLS CPI-U data summary below. Return the predictive distribution as numeric_cdf_v1: exactly 201 evenly spaced CDF points over an explicit support, probability 0 at the first point, probability 1 at the last point, and monotone nondecreasing probabilities. Do not return pointEstimate, ciLow, or ciHigh as top-level fields; the server derives the median and 80% interval from the CDF. Keep the public trace factual, calibrated, and specific about data caveats.",
        "",
        JSON.stringify(dataset.summary, null, 2),
      ].join("\n"),
    });

    return normalizeForecast({
      ...result.object,
      confidence: 0.8,
      source: "ai_gateway",
      model,
      generatedAt: new Date().toISOString(),
    });
  } catch (error) {
    return fallbackForecast(
      dataset,
      error instanceof Error
        ? `AI Gateway call failed: ${error.message}`
        : "AI Gateway call failed.",
    );
  }
}

export async function generateCtcExpansionForecast(
  dataset: CtcExpansionDataset,
): Promise<CtcExpansionForecast> {
  if (!shouldTryGateway()) {
    return fallbackCtcExpansionForecast(
      dataset,
      "AI Gateway credentials are not configured.",
    );
  }

  const model =
    process.env.THESIS_AI_MODEL ??
    process.env.BRIER_AI_MODEL ??
    "anthropic/claude-sonnet-4.6";

  try {
    const result = await generateObject({
      model,
      schema: CtcExpansionForecastSchema,
      temperature: 0.2,
      system:
        "You are a Thesis Institute public forecasting agent. Forecast in billions of nominal dollars. Use public, audit-ready reasoning only. Your public trace must name an explicit base rate or reference class (the distribution of recent comparable prints), state the mechanism behind the point estimate, and include at least one disconfirming consideration that would land the outcome outside your interval. Treat PolicyEngine as an explicit model input, not as ground truth, and describe calibration adjustments without hidden chain-of-thought.",
      prompt: [
        "Forecast this public prediction cell:",
        dataset.summary.question,
        "",
        "Use the live PolicyEngine API result and the calibration prior below. Return the predictive distribution in billions of nominal dollars as numeric_cdf_v1: exactly 201 evenly spaced CDF points over an explicit support, probability 0 at the first point, probability 1 at the last point, and monotone nondecreasing probabilities. Do not return pointEstimate, ciLow, or ciHigh as top-level fields; the server derives the median and 80% interval from the CDF.",
        "If the PolicyEngine economy endpoint is still queued, errored, or timed out, explicitly widen uncertainty and explain that the calibration fallback is carrying the run.",
        "",
        JSON.stringify(
          {
            policyEngine: dataset.summary,
            economyStatus: dataset.economy,
          },
          null,
          2,
        ),
      ].join("\n"),
    });

    return normalizeUsdBillionsForecast({
      ...result.object,
      confidence: 0.8,
      source: "ai_gateway",
      model,
      generatedAt: new Date().toISOString(),
    });
  } catch (error) {
    return fallbackCtcExpansionForecast(
      dataset,
      error instanceof Error
        ? `AI Gateway call failed: ${error.message}`
        : "AI Gateway call failed.",
    );
  }
}

export async function generateSpmChildPovertyForecast(
  dataset: SpmChildPovertyDataset,
): Promise<SpmChildPovertyForecast> {
  if (!shouldTryGateway()) {
    return fallbackSpmChildPovertyForecast(
      dataset,
      "AI Gateway credentials are not configured.",
    );
  }

  const model =
    process.env.THESIS_AI_MODEL ??
    process.env.BRIER_AI_MODEL ??
    "anthropic/claude-sonnet-4.6";

  try {
    const result = await generateObject({
      model,
      schema: SpmChildPovertyForecastSchema,
      temperature: 0.2,
      system:
        "You are a Thesis Institute public forecasting agent. Forecast in percentage points. Use public, audit-ready reasoning only. Your public trace must name an explicit base rate or reference class (the distribution of recent comparable prints), state the mechanism behind the point estimate, and include at least one disconfirming consideration that would land the outcome outside your interval. Treat Census history and PolicyEngine current-law inputs as explicit model inputs, not as ground truth, and describe calibration adjustments without hidden chain-of-thought.",
      prompt: [
        "Forecast this public prediction cell:",
        dataset.summary.question,
        "",
        "Target: the Census-published Supplemental Poverty Measure child poverty rate for calendar-year 2025, expected in the September 2026 income and poverty release.",
        "Use the live Census page evidence, historical SPM child-poverty series, PolicyEngine current-law policy check, and calibration prior below. Return the predictive distribution in percentage points as numeric_cdf_v1: exactly 201 evenly spaced CDF points over an explicit support, probability 0 at the first point, probability 1 at the last point, and monotone nondecreasing probabilities. Do not return pointEstimate, ciLow, or ciHigh as top-level fields; the server derives the median and 80% interval from the CDF.",
        "If the PolicyEngine check or Census page fetch is unavailable, explicitly widen or qualify uncertainty instead of pretending the data path is complete.",
        "",
        JSON.stringify(dataset.summary, null, 2),
      ].join("\n"),
    });

    return normalizeSpmPercentForecast({
      ...result.object,
      confidence: 0.8,
      source: "ai_gateway",
      model,
      generatedAt: new Date().toISOString(),
    });
  } catch (error) {
    return fallbackSpmChildPovertyForecast(
      dataset,
      error instanceof Error
        ? `AI Gateway call failed: ${error.message}`
        : "AI Gateway call failed.",
    );
  }
}

function fallbackForecast(dataset: CpiDataset, reason: string): CpiForecast {
  const { summary } = dataset;
  const carryForward = summary.carryForwardAnnualAverageInflationPct;
  const recent = summary.recentAnnualizedPct;
  const ytd = summary.targetYtdVsPriorObservedAveragePct;
  const pointEstimate = clamp(
    0.58 * carryForward + 0.27 * ytd + 0.15 * clamp(recent, 0.5, 5.5),
    1.2,
    5.5,
  );
  const upside = Math.max(
    0.65,
    0.32 * Math.max(recent - pointEstimate, 0) + 0.8,
  );
  const downside = Math.max(
    0.55,
    0.25 * Math.max(pointEstimate - ytd, 0) + 0.6,
  );

  return normalizeForecast({
    distribution: buildNumericCdfFromInterval({
      pointEstimate,
      ciLow: pointEstimate - downside,
      ciHigh: pointEstimate + upside,
    }),
    confidence: 0.8,
    publicTrace: [
      `Live BLS data put ${summary.targetYear} CPI-U ${ytd.toFixed(2)}% above the observed ${summary.priorYear} average so far.`,
      `A carry-forward calculation, holding the latest CPI-U level through December, implies ${carryForward.toFixed(2)}% annual-average inflation.`,
      `The deterministic fallback blends the carry-forward path, the observed annual-average gap, and recent monthly momentum because the AI Gateway call was unavailable: ${reason}`,
    ],
    assumptions: [
      "Remaining 2026 CPI-U levels do not sharply reverse the current-year gain.",
      "The observed 2025 monthly average is a usable proxy until BLS annual-average resolution data are finalized.",
      "Recent monthly volatility should widen the upper half of the interval.",
    ],
    dataCaveats:
      summary.caveats.length > 0
        ? summary.caveats
        : [
            "BLS data are first-print public API observations and may later revise.",
          ],
    drivers: [
      "Shelter disinflation",
      "Recent monthly CPI momentum",
      "Goods and tariff pass-through",
      "Energy price volatility",
    ],
    source: "deterministic_fallback",
    generatedAt: new Date().toISOString(),
  });
}

function fallbackSpmChildPovertyForecast(
  dataset: SpmChildPovertyDataset,
  reason: string,
): SpmChildPovertyForecast {
  const { summary } = dataset;
  const policy =
    summary.currentLawPolicy.status === "ok"
      ? `PolicyEngine current-law policy ${summary.currentLawPolicy.id} (${summary.currentLawPolicy.label}) was verified live.`
      : `PolicyEngine current-law policy ${summary.currentLawPolicy.id} was unavailable: ${summary.currentLawPolicy.error}`;

  return normalizeSpmPercentForecast({
    distribution: buildNumericCdfFromInterval({
      pointEstimate: summary.calibratedPointEstimatePct,
      ciLow: summary.calibratedCiLowPct,
      ciHigh: summary.calibratedCiHighPct,
    }),
    confidence: 0.8,
    publicTrace: [
      `Census release evidence was fetched from the income/poverty schedule and SPM tables pages; the target is the calendar-year ${summary.targetYear} SPM child poverty rate expected in ${summary.expectedRelease}.`,
      `The recent Census history seed is ${summary.latestHistoricalChildPovertyRatePct.toFixed(1)}% in ${summary.latestHistoricalYear}, with a ${summary.postExpansionAveragePct.toFixed(1)}% average over 2022-2024 after the expanded-CTC year.`,
      `${policy} The calibration fallback blends that current-law prior with recent SPM history and carries this run because ${reason}`,
    ],
    assumptions: [
      "Calendar-year 2025 policy is closer to the 2022-2024 current-law regime than to the 2021 expanded Child Tax Credit regime.",
      "Labor-market and real-earnings conditions keep the central estimate near, but slightly below, the latest published child SPM rate.",
      "ASEC sampling error and SPM expense adjustments justify an asymmetric interval around the point estimate.",
    ],
    dataCaveats: [
      ...summary.caveats,
      reason,
    ],
    drivers: [
      "Current-law CTC and EITC parameters",
      "Employment and earnings",
      "Housing and medical expense adjustments",
      "SNAP and other in-kind resources",
    ],
    source: "census_calibration_fallback",
    generatedAt: new Date().toISOString(),
  });
}

function fallbackCtcExpansionForecast(
  dataset: CtcExpansionDataset,
  reason: string,
): CtcExpansionForecast {
  const { summary } = dataset;
  const raw =
    summary.rawPolicyEngineEstimateUsdBillions == null
      ? "not returned yet"
      : `$${summary.rawPolicyEngineEstimateUsdBillions.toFixed(1)}B`;

  return normalizeUsdBillionsForecast({
    distribution: buildNumericCdfFromInterval({
      pointEstimate: summary.calibratedPointEstimateUsdBillions,
      ciLow: summary.calibratedCiLowUsdBillions,
      ciHigh: summary.calibratedCiHighUsdBillions,
    }),
    confidence: 0.8,
    publicTrace: [
      `PolicyEngine policy ${summary.reformPolicyId} models a $3,000 fully refundable CTC against current law policy ${summary.baselinePolicyId} for ${summary.targetYear}.`,
      `The live economy endpoint returned status=${summary.policyEngineStatus}; raw budget impact=${raw}.`,
      `The calibration layer applies the stored ratio/additive prior, then widens the interval when the PolicyEngine run is queued or unavailable. This fallback carried the run because ${reason}`,
    ],
    assumptions: [
      "The public PolicyEngine policy definition is the operative reform design for this prototype forecast.",
      "Historical score deltas between PolicyEngine-style static impacts and later official scores are informative about the adjustment direction.",
      "A queued or errored economy run increases variance more than it changes the central estimate.",
    ],
    dataCaveats: [
      summary.policyEngineMessage ??
        "PolicyEngine economy runs can return computing/error before a cached population result is available.",
      summary.calibration.source,
    ],
    drivers: [
      "Refundability and phase-in design",
      "Eligible child population",
      "Take-up and filing behavior",
      "Official score calibration",
    ],
    source: "calibration_fallback",
    generatedAt: new Date().toISOString(),
  });
}

function normalizeSpmPercentForecast(
  forecast: Omit<
    SpmChildPovertyForecast,
    "confidence" | "pointEstimate" | "ciLow" | "ciHigh"
  > & {
    confidence: 0.8;
  },
) {
  const distribution = normalizeNumericCdfDistribution({
    distribution: forecast.distribution,
    min: 0,
    max: 35,
    decimals: 1,
  });
  const summary = summarizeNumericCdfDistribution(distribution);

  return {
    ...forecast,
    ...summary,
    distribution,
    confidence: 0.8 as const,
  };
}

function shouldTryGateway() {
  if (process.env.BRIER_DISABLE_AI === "1") return false;
  return Boolean(
    process.env.AI_GATEWAY_API_KEY ||
    process.env.VERCEL_OIDC_TOKEN ||
    process.env.VERCEL === "1",
  );
}

function normalizeForecast(
  forecast: Omit<
    CpiForecast,
    "confidence" | "pointEstimate" | "ciLow" | "ciHigh"
  > & {
    confidence: 0.8;
  },
) {
  const distribution = normalizeNumericCdfDistribution({
    distribution: forecast.distribution,
    min: -2,
    max: 15,
    decimals: 1,
  });
  const summary = summarizeNumericCdfDistribution(distribution);

  return {
    ...forecast,
    ...summary,
    distribution,
    confidence: 0.8 as const,
  };
}

function normalizeUsdBillionsForecast(
  forecast: Omit<
    CtcExpansionForecast,
    "confidence" | "pointEstimate" | "ciLow" | "ciHigh"
  > & {
    confidence: 0.8;
  },
) {
  const distribution = normalizeNumericCdfDistribution({
    distribution: forecast.distribution,
    min: 0,
    max: 500,
    decimals: 1,
  });
  const summary = summarizeNumericCdfDistribution(distribution);

  return {
    ...forecast,
    ...summary,
    distribution,
    confidence: 0.8 as const,
  };
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function round(value: number, decimals: number) {
  const factor = 10 ** decimals;
  return Math.round(value * factor) / factor;
}
