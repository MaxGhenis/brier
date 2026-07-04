import { roundToIncrement } from "./forecast-models";
import {
  buildNumericCdfFromInterval,
  type PredictionDistribution,
} from "./prediction-distribution";
import type {
  ForecastCell,
  ForecastComparisonRun,
  ForecastRunEntry,
  HistoricalPoint,
  Unit,
} from "./forecast-cells";

export const TIME_SERIES_PRIOR_VARIANT_ID = "time-series-prior";

export interface TimeSeriesPriorAdjustmentRow {
  forecastSlug: string;
  title: string;
  dataPointId?: string;
  unit: Unit;
  priorLabel: string;
  priorModel: string;
  historyPoints: number;
  latestHistoricalLabel: string;
  latestHistoricalValue: number;
  priorPointEstimate: number;
  priorCiLow: number;
  priorCiHigh: number;
  priorIntervalWidth: number;
  agentPointEstimate: number;
  agentCiLow: number;
  agentCiHigh: number;
  adjustment: number;
  absoluteAdjustment: number;
  relativeAdjustment: number | null;
  adjustmentShareOfPriorInterval: number | null;
  direction: "up" | "down" | "flat";
}

export interface TimeSeriesPriorAdjustmentReport {
  schemaVersion: "time_series_prior_adjustment_report_v1";
  rows: TimeSeriesPriorAdjustmentRow[];
  counts: {
    forecastsWithPrior: number;
    adjustedUp: number;
    adjustedDown: number;
    flat: number;
  };
  summary: {
    meanAdjustment: number | null;
    meanAbsoluteAdjustment: number | null;
    medianAbsoluteAdjustment: number | null;
    meanAbsoluteShareOfPriorInterval: number | null;
    medianAbsoluteShareOfPriorInterval: number | null;
  };
  largestAbsoluteAdjustments: TimeSeriesPriorAdjustmentRow[];
  largestPriorIntervalShareAdjustments: TimeSeriesPriorAdjustmentRow[];
}

interface PriorInterval {
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  increment: number;
  historyPoints: number;
  latest: HistoricalPoint;
  intervalMethod: "historical_step_change" | "fallback_fraction";
}

export function buildTimeSeriesPriorComparisonRun(
  forecast: ForecastCell,
): ForecastComparisonRun | null {
  if (!forecast.predictionRun) return null;
  if (!isBrierAgentRun(forecast.predictionRun.agent)) return null;
  if (
    forecast.comparisonRuns?.some(
      (run) => run.variantId === TIME_SERIES_PRIOR_VARIANT_ID,
    )
  ) {
    return null;
  }

  const prior = buildLastPrintPriorInterval(forecast);
  if (!prior) return null;

  const distribution = buildNumericCdfFromInterval({
    pointEstimate: prior.pointEstimate,
    ciLow: prior.ciLow,
    ciHigh: prior.ciHigh,
  });

  return {
    variantId: TIME_SERIES_PRIOR_VARIANT_ID,
    label: "Time-series prior",
    description:
      "Last observed public print carried forward before the agent applies target-specific evidence.",
    pointEstimate: prior.pointEstimate,
    ciLow: prior.ciLow,
    ciHigh: prior.ciHigh,
    confidence: forecast.confidence,
    drivers: [
      "Latest official historical value",
      prior.intervalMethod === "historical_step_change"
        ? "Historical one-step changes"
        : "Fallback uncertainty floor",
      "No target-specific agent judgment",
    ],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: forecast.predictionRun.runAt,
      agent: "brier.time_series_prior",
      model: "persistence.last_print",
      sourceContext: forecast.predictionRun.sourceContext,
      runLabel: "Time-series prior",
      runDescription:
        "Deterministic last-print baseline generated from the same historical context available to the agent.",
      activityLog: [
        {
          artifactType: "model_candidates",
          path: `generated://time-series-priors/${forecast.slug}.json`,
          sha256: "generated",
          bytes: 0,
          createdAt: forecast.predictionRun.runAt,
        },
      ],
    },
    predictionDistribution: distribution,
    reasoning: buildPriorReasoning(forecast, prior),
  };
}

function isBrierAgentRun(agent: string) {
  return (
    agent.startsWith("thesis.analyst") ||
    agent.startsWith("brier-") ||
    agent.startsWith("scout-")
  );
}

export function buildTimeSeriesPriorAdjustmentReport(
  forecasts: ForecastCell[],
): TimeSeriesPriorAdjustmentReport {
  const rows = forecasts
    .flatMap((forecast) => buildPriorAdjustmentRow(forecast) ?? [])
    .sort(
      (left, right) =>
        right.absoluteAdjustment - left.absoluteAdjustment ||
        left.forecastSlug.localeCompare(right.forecastSlug),
    );
  const shareRows = rows
    .filter((row) => row.adjustmentShareOfPriorInterval !== null)
    .sort(
      (left, right) =>
        Math.abs(right.adjustmentShareOfPriorInterval ?? 0) -
          Math.abs(left.adjustmentShareOfPriorInterval ?? 0) ||
        left.forecastSlug.localeCompare(right.forecastSlug),
    );

  return {
    schemaVersion: "time_series_prior_adjustment_report_v1",
    rows,
    counts: {
      forecastsWithPrior: rows.length,
      adjustedUp: rows.filter((row) => row.direction === "up").length,
      adjustedDown: rows.filter((row) => row.direction === "down").length,
      flat: rows.filter((row) => row.direction === "flat").length,
    },
    summary: {
      meanAdjustment: meanOrNull(rows.map((row) => row.adjustment)),
      meanAbsoluteAdjustment: meanOrNull(
        rows.map((row) => row.absoluteAdjustment),
      ),
      medianAbsoluteAdjustment: quantileOrNull(
        rows.map((row) => row.absoluteAdjustment),
        0.5,
      ),
      meanAbsoluteShareOfPriorInterval: meanOrNull(
        rows
          .map((row) => row.adjustmentShareOfPriorInterval)
          .filter((value): value is number => value !== null)
          .map((value) => Math.abs(value)),
      ),
      medianAbsoluteShareOfPriorInterval: quantileOrNull(
        rows
          .map((row) => row.adjustmentShareOfPriorInterval)
          .filter((value): value is number => value !== null)
          .map((value) => Math.abs(value)),
        0.5,
      ),
    },
    largestAbsoluteAdjustments: rows.slice(0, 12),
    largestPriorIntervalShareAdjustments: shareRows.slice(0, 12),
  };
}

function buildPriorAdjustmentRow(
  forecast: ForecastCell,
): TimeSeriesPriorAdjustmentRow | null {
  const prior = forecast.comparisonRuns?.find(
    (run) => run.variantId === TIME_SERIES_PRIOR_VARIANT_ID,
  );
  if (!prior) return null;
  const latest = getLatestFinitePoint(getComparableHistoricalPoints(forecast));
  if (!latest) return null;

  return buildPriorAdjustmentRowFromRun({ forecast, prior, latest });
}

function buildPriorAdjustmentRowFromRun({
  forecast,
  prior,
  latest,
}: {
  forecast: ForecastCell;
  prior: ForecastComparisonRun | ForecastRunEntry;
  latest: HistoricalPoint;
}): TimeSeriesPriorAdjustmentRow {
  const adjustment = roundComparable(
    forecast.pointEstimate - prior.pointEstimate,
  );
  const priorIntervalWidth = Math.abs(prior.ciHigh - prior.ciLow);
  const relativeAdjustment =
    Math.abs(prior.pointEstimate) > 1e-9
      ? adjustment / Math.abs(prior.pointEstimate)
      : null;
  const adjustmentShareOfPriorInterval =
    priorIntervalWidth > 1e-9 ? adjustment / priorIntervalWidth : null;

  return {
    forecastSlug: forecast.slug,
    title: forecast.title,
    dataPointId: forecast.dataPointId,
    unit: forecast.unit,
    priorLabel: prior.label,
    priorModel: prior.predictionRun?.model ?? "persistence.last_print",
    historyPoints: forecast.historicalContext.filter((point) =>
      Number.isFinite(point.value),
    ).length,
    latestHistoricalLabel: latest.label,
    latestHistoricalValue: latest.value,
    priorPointEstimate: prior.pointEstimate,
    priorCiLow: prior.ciLow,
    priorCiHigh: prior.ciHigh,
    priorIntervalWidth,
    agentPointEstimate: forecast.pointEstimate,
    agentCiLow: forecast.ciLow,
    agentCiHigh: forecast.ciHigh,
    adjustment,
    absoluteAdjustment: Math.abs(adjustment),
    relativeAdjustment,
    adjustmentShareOfPriorInterval,
    direction: classifyDirection(adjustment),
  };
}

function buildLastPrintPriorInterval(
  forecast: ForecastCell,
): PriorInterval | null {
  const history = getComparableHistoricalPoints(forecast);
  const latest = history.at(-1);
  if (!latest) return null;

  const increment = inferIncrement(forecast, history);
  const pointEstimate = roundToIncrement(latest.value, increment);
  const diffs = buildStepChanges(history);
  const fallbackHalfWidth = getFallbackHalfWidth({
    pointEstimate,
    unit: forecast.unit,
    increment,
  });
  const halfWidth =
    diffs.length > 0
      ? Math.max(quantile(diffs.map((diff) => Math.abs(diff)), 0.8), increment)
      : fallbackHalfWidth;
  const intervalMethod =
    diffs.length > 0 ? "historical_step_change" : "fallback_fraction";
  const rawLow = pointEstimate - Math.max(halfWidth, fallbackHalfWidth);
  const rawHigh = pointEstimate + Math.max(halfWidth, fallbackHalfWidth);

  return {
    pointEstimate,
    ciLow: roundToIncrement(rawLow, increment),
    ciHigh: roundToIncrement(rawHigh, increment),
    increment,
    historyPoints: history.length,
    latest,
    intervalMethod,
  };
}

function buildPriorReasoning(forecast: ForecastCell, prior: PriorInterval) {
  const formattedLatest = formatCompact(prior.latest.value, forecast.unit);
  const formattedPoint = formatCompact(prior.pointEstimate, forecast.unit);
  const formattedLow = formatCompact(prior.ciLow, forecast.unit);
  const formattedHigh = formatCompact(prior.ciHigh, forecast.unit);

  return [
    {
      kind: "heading" as const,
      text: "Time-series prior",
    },
    {
      kind: "tool" as const,
      tool: "brier.timeseries.prior",
      call: `brier.timeseries.prior({ target: "${forecast.dataPointId ?? forecast.slug}", model: "persistence.last_print" })`,
      result: `latest=${formattedLatest} (${prior.latest.label}); history_points=${prior.historyPoints}; interval_method=${prior.intervalMethod}`,
    },
    {
      kind: "math" as const,
      text: `Prior point = latest observed value = ${formattedPoint}; 80% interval = [${formattedLow}, ${formattedHigh}].`,
    },
    {
      kind: "text" as const,
      text: "This run stops before target-specific agent updates; the primary forecast records the adjustment away from this prior.",
    },
    {
      kind: "forecast" as const,
      point: prior.pointEstimate,
      ciLow: prior.ciLow,
      ciHigh: prior.ciHigh,
    },
  ];
}

function getComparableHistoricalPoints(forecast: ForecastCell) {
  return forecast.historicalContext.filter(
    (point) =>
      Number.isFinite(point.value) && !isNonTargetContextLabel(point.label),
  );
}

function getLatestFinitePoint(history: HistoricalPoint[]) {
  return history.at(-1);
}

function isNonTargetContextLabel(label: string) {
  return /\b(implied|probability|odds)\b|p\(/i.test(label);
}

function buildStepChanges(history: HistoricalPoint[]) {
  const diffs: number[] = [];
  for (let index = 1; index < history.length; index += 1) {
    diffs.push(history[index].value - history[index - 1].value);
  }
  return diffs;
}

function getFallbackHalfWidth({
  pointEstimate,
  unit,
  increment,
}: {
  pointEstimate: number;
  unit: Unit;
  increment: number;
}) {
  const rateByUnit: Record<Unit, number> = {
    count: 0.05,
    percent: 0.1,
    gbp_billions: 0.08,
    usd: 0.04,
    usd_billions: 0.08,
    usd_monthly: 0.05,
    thousands: 0.05,
    millions: 0.05,
    per_1000_live_births: 0.05,
    ratio: 0.05,
    minutes: 0.05,
    percent_growth: 0.5,
    // Survey balances move in absolute points, not relative to the level
    // (which sits near zero) — the increment floor below does the work.
    index_points: 0.1,
  };
  return Math.max(Math.abs(pointEstimate) * rateByUnit[unit], increment);
}

function inferIncrement(forecast: ForecastCell, history: HistoricalPoint[]) {
  const unit = forecast.unit;
  if (unit === "percent" && isQuarterPointPercentSeries(forecast, history)) {
    return 0.25;
  }

  const increments: Record<Unit, number> = {
    count: 1,
    percent: 0.1,
    gbp_billions: 0.1,
    usd: 100,
    usd_billions: 0.1,
    usd_monthly: 1,
    thousands: 0.1,
    millions: 0.01,
    per_1000_live_births: 0.1,
    ratio: 0.01,
    minutes: 1,
    percent_growth: 0.1,
    index_points: 1,
  };
  return increments[unit];
}

function isQuarterPointPercentSeries(
  forecast: ForecastCell,
  history: HistoricalPoint[],
) {
  const values = [
    forecast.pointEstimate,
    forecast.ciLow,
    forecast.ciHigh,
    ...history.map((point) => point.value),
  ].filter((value) => Number.isFinite(value));
  if (values.length === 0 || Math.max(...values.map(Math.abs)) > 25) {
    return false;
  }
  return values.every((value) => isNearInteger(value * 4));
}

function isNearInteger(value: number) {
  return Math.abs(value - Math.round(value)) < 1e-9;
}

function classifyDirection(
  adjustment: number,
): TimeSeriesPriorAdjustmentRow["direction"] {
  if (Math.abs(adjustment) < 1e-9) return "flat";
  return adjustment > 0 ? "up" : "down";
}

function quantile(values: number[], probability: number) {
  const finiteValues = values
    .filter((value) => Number.isFinite(value))
    .sort((left, right) => left - right);
  if (finiteValues.length === 0) return 0;
  if (finiteValues.length === 1) return finiteValues[0];

  const index = (finiteValues.length - 1) * probability;
  const lowerIndex = Math.floor(index);
  const upperIndex = Math.ceil(index);
  const lower = finiteValues[lowerIndex];
  const upper = finiteValues[upperIndex];
  if (lowerIndex === upperIndex) return lower;
  return lower + (upper - lower) * (index - lowerIndex);
}

function quantileOrNull(values: number[], probability: number) {
  const finiteValues = values.filter((value) => Number.isFinite(value));
  if (finiteValues.length === 0) return null;
  return quantile(finiteValues, probability);
}

function meanOrNull(values: number[]) {
  const finiteValues = values.filter((value) => Number.isFinite(value));
  if (finiteValues.length === 0) return null;
  return (
    finiteValues.reduce((total, value) => total + value, 0) /
    finiteValues.length
  );
}

function roundComparable(value: number) {
  return Number(value.toPrecision(12));
}

function formatCompact(value: number, unit: Unit) {
  const fractionDigits =
    unit === "percent" || unit === "percent_growth" || unit === "millions"
      ? 1
      : 0;
  return value.toLocaleString(undefined, {
    maximumFractionDigits: fractionDigits,
  });
}

export function buildPriorDistributionForTest(
  forecast: ForecastCell,
): PredictionDistribution | null {
  const prior = buildLastPrintPriorInterval(forecast);
  if (!prior) return null;
  return buildNumericCdfFromInterval({
    pointEstimate: prior.pointEstimate,
    ciLow: prior.ciLow,
    ciHigh: prior.ciHigh,
  });
}
