import { canonicalStringify, sha256Hex } from "./canonical-json";
import {
  buildNumericCdfFromInterval,
  type PredictionDistribution,
} from "./prediction-distribution";
import type {
  ForecastCell,
  ForecastComparisonRun,
  ForecastRunEntry,
  LedgerObservationReference,
  PersistenceBaselineRecord,
  Unit,
} from "./forecast-cells";
import type {
  ObservationRecordedLedgerEntry,
  PolicyEngineLedgerEntry,
} from "./thesis-log";

export const TIME_SERIES_PRIOR_VARIANT_ID = "time-series-prior";
export const PERSISTENCE_BASELINE_AGENT = "brier.time_series_prior";
export const PERSISTENCE_BASELINE_ALGORITHM_VERSION =
  "ledger_last_print_realized_change_p80_v1";

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
  historyPoints: number;
  latest: LedgerObservationReference;
  observations: LedgerObservationReference[];
  seriesId: string;
  intervalMethod: "ledger_realized_step_change_p80";
}

export function buildTimeSeriesPriorComparisonRun(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
): ForecastComparisonRun | null {
  return buildLedgerPersistenceBaseline(forecast, ledger).comparisonRun;
}

export interface LedgerPersistenceBaselineResult {
  record: PersistenceBaselineRecord;
  comparisonRun: ForecastComparisonRun | null;
}

export function buildLedgerPersistenceBaseline(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
): LedgerPersistenceBaselineResult {
  const cutoff = forecast.predictionRun?.runAt;
  const unavailable = (
    reason: string,
    observationRefs: LedgerObservationReference[] = [],
    seriesId?: string,
  ): LedgerPersistenceBaselineResult => ({
    record: {
      status: "unavailable",
      variantId: TIME_SERIES_PRIOR_VARIANT_ID,
      cutoff: cutoff ?? "",
      targetDataPointId: forecast.dataPointId,
      seriesId,
      observationRefs,
      reason,
    },
    comparisonRun: null,
  });

  if (!cutoff || !forecast.dataPointId) {
    return unavailable("missing recordedAt cutoff or target dataPointId");
  }

  const prior = buildLastPrintPriorInterval(forecast, ledger, cutoff);
  if (!prior) {
    const candidates = ledgerHistoryAtCutoff(forecast, ledger, cutoff);
    return unavailable(
      candidates.length === 0
        ? "ledger has no pre-cutoff observations for the target series"
        : "ledger has fewer than two pre-cutoff observations, so realized volatility is unavailable",
      candidates.map(toObservationReference),
      candidates[0] ? ledgerSeriesId(candidates[0]) : undefined,
    );
  }

  const distribution = buildNumericCdfFromInterval({
    pointEstimate: prior.pointEstimate,
    ciLow: prior.ciLow,
    ciHigh: prior.ciHigh,
  });
  const inputPayload = {
    schemaVersion: "thesis_persistence_baseline_inputs_v1",
    algorithmVersion: PERSISTENCE_BASELINE_ALGORITHM_VERSION,
    targetDataPointId: forecast.dataPointId,
    seriesId: prior.seriesId,
    cutoff,
    observations: prior.observations,
  };
  const inputDigest = sha256Hex(inputPayload);
  const inputBytes = new TextEncoder().encode(
    canonicalStringify(inputPayload),
  ).byteLength;
  const sourceContext = ledgerHistoryAtCutoff(forecast, ledger, cutoff)
    .map((entry) => entry.sourceUrl)
    .filter((url): url is string => Boolean(url));

  const comparisonRun: ForecastComparisonRun = {
    variantId: TIME_SERIES_PRIOR_VARIANT_ID,
    label: "Ledger persistence baseline",
    description:
      "Last official ledger print at the primary run cutoff, with an interval derived only from realized same-series ledger changes.",
    pointEstimate: prior.pointEstimate,
    ciLow: prior.ciLow,
    ciHigh: prior.ciHigh,
    confidence: forecast.confidence,
    drivers: [
      "Latest official historical value",
      "Ledger-archived realized one-step changes",
      "No target-specific agent judgment",
    ],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: cutoff,
      agent: PERSISTENCE_BASELINE_AGENT,
      model: "persistence.last_print",
      sourceContext: [...new Set(sourceContext)],
      runLabel: "Ledger persistence baseline",
      runDescription:
        "Deterministic last-print baseline generated exclusively from observations archived in the PolicyEngine Ledger before the primary run cutoff.",
      inputBundleHash: inputDigest,
      activityLog: [
        {
          artifactType: "baseline_inputs",
          path: `ledger://persistence-baselines/${inputDigest}.json`,
          sha256: inputDigest,
          bytes: inputBytes,
          createdAt: cutoff,
          observationRefs: prior.observations,
        },
      ],
    },
    predictionDistribution: distribution,
    reasoning: buildPriorReasoning(forecast, prior),
  };

  return {
    record: {
      status: "available",
      variantId: TIME_SERIES_PRIOR_VARIANT_ID,
      cutoff,
      targetDataPointId: forecast.dataPointId,
      seriesId: prior.seriesId,
      observationRefs: prior.observations,
    },
    comparisonRun,
  };
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
  const latest = prior.predictionRun.activityLog
    ?.find((artifact) => artifact.artifactType === "baseline_inputs")
    ?.observationRefs?.at(-1);
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
  latest: LedgerObservationReference;
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
    historyPoints:
      prior.predictionRun?.activityLog?.find(
        (artifact) => artifact.artifactType === "baseline_inputs",
      )?.observationRefs?.length ?? 0,
    latestHistoricalLabel: latest.periodLabel,
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
  ledger: PolicyEngineLedgerEntry[],
  cutoff: string,
): PriorInterval | null {
  const history = ledgerHistoryAtCutoff(forecast, ledger, cutoff);
  if (history.length < 2) return null;
  const latest = history.at(-1);
  if (!latest) return null;

  const observations = history.map(toObservationReference);
  const pointEstimate = latest.value;
  const diffs = buildStepChanges(observations);
  const halfWidth = quantile(
    diffs.map((diff) => Math.abs(diff)),
    0.8,
  );

  return {
    pointEstimate,
    ciLow: roundComparable(pointEstimate - halfWidth),
    ciHigh: roundComparable(pointEstimate + halfWidth),
    historyPoints: history.length,
    latest: toObservationReference(latest),
    observations,
    seriesId: ledgerSeriesId(latest),
    intervalMethod: "ledger_realized_step_change_p80",
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
      result: `latest=${formattedLatest} (${prior.latest.periodLabel}); history_points=${prior.historyPoints}; interval_method=${prior.intervalMethod}; ledger_refs=${prior.observations.map((observation) => observation.dataPointId).join(",")}`,
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

function buildStepChanges(history: LedgerObservationReference[]) {
  const diffs: number[] = [];
  for (let index = 1; index < history.length; index += 1) {
    diffs.push(history[index].value - history[index - 1].value);
  }
  return diffs;
}

export function ledgerHistoryAtCutoff(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
  cutoff: string,
): ObservationRecordedLedgerEntry[] {
  if (!forecast.dataPointId) return [];
  const targetSeriesId = ledgerSeriesId(forecast.dataPointId);
  const cutoffTime = Date.parse(cutoff);
  if (!Number.isFinite(cutoffTime)) return [];

  const observations = ledger.filter(
    (entry): entry is ObservationRecordedLedgerEntry =>
      entry.kind === "observation_recorded" &&
      entry.unit === forecast.unit &&
      ledgerSeriesId(entry) === targetSeriesId &&
      Date.parse(entry.observedAt) <= cutoffTime,
  );
  const byObservationId = new Map(
    observations.map((observation) => [observation.observationId, observation]),
  );
  return [...byObservationId.values()].sort((left, right) => {
    const timeDelta =
      Date.parse(left.observedAt) - Date.parse(right.observedAt);
    return timeDelta || left.observationId.localeCompare(right.observationId);
  });
}

export function ledgerSeriesId(
  observation: ObservationRecordedLedgerEntry | string,
): string {
  const dataPointId =
    typeof observation === "string" ? observation : observation.dataPointId;
  return dataPointId
    .replace(
      /\.(?:(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)_\d{4}|fy\d{4}|q[1-4]_?\d{4}|week(?:_ending)?_\d{4}(?:[-_]\d{2}){2}|\d{4}[-_]\d{2}(?:[-_]\d{2})?|\d{4})(?=\.|$)/i,
      "",
    )
    .replace(
      /\.(?:first_print|final_first_print|official_release|original_submission|advance|final)$/,
      "",
    );
}

function toObservationReference(
  observation: ObservationRecordedLedgerEntry,
): LedgerObservationReference {
  return {
    observationId: observation.observationId,
    dataPointId: observation.dataPointId,
    periodLabel: observation.periodLabel,
    observedAt: observation.observedAt,
    value: observation.value,
    unit: observation.unit,
  };
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
  ledger: PolicyEngineLedgerEntry[] = [],
): PredictionDistribution | null {
  const cutoff = forecast.predictionRun?.runAt;
  if (!cutoff) return null;
  const prior = buildLastPrintPriorInterval(forecast, ledger, cutoff);
  if (!prior) return null;
  return buildNumericCdfFromInterval({
    pointEstimate: prior.pointEstimate,
    ciLow: prior.ciLow,
    ciHigh: prior.ciHigh,
  });
}
