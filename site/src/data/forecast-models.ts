export interface TimeSeriesPoint {
  period: number | string;
  value: number;
}

export interface DampedTrendForecastOptions {
  horizonPeriods?: number;
  damping?: number;
  fallbackGrowth?: number;
  fallbackLabel?: string;
  minTrendPoints?: number;
  residualStdDevFloor?: number;
  intervalZ?: number;
}

export interface DampedTrendForecast {
  modelId: "damped_log_trend_v1";
  status: "fit" | "fallback";
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  latestValue: number;
  latestPeriod: number | string;
  historyPoints: number;
  horizonPeriods: number;
  annualizedGrowth: number;
  residualStdDev: number;
  fallbackLabel?: string;
  diagnostics: string[];
}

export function buildDampedLogTrendForecast(
  rawHistory: TimeSeriesPoint[],
  options: DampedTrendForecastOptions = {},
): DampedTrendForecast {
  const history = rawHistory
    .filter((point) => Number.isFinite(point.value) && point.value > 0)
    .sort((a, b) => String(a.period).localeCompare(String(b.period)));
  if (history.length === 0) {
    throw new Error("Cannot forecast an empty or non-positive time series");
  }

  const horizonPeriods = options.horizonPeriods ?? 1;
  const damping = options.damping ?? 0.5;
  const minTrendPoints = options.minTrendPoints ?? 3;
  const intervalZ = options.intervalZ ?? 1.2815515655446004;
  const residualStdDevFloor = options.residualStdDevFloor ?? 0.035;
  const latest = history.at(-1)!;
  const growthRates = logGrowthRates(history);
  const canFitTrend =
    history.length >= minTrendPoints && growthRates.length > 0;
  const meanGrowth = canFitTrend ? mean(growthRates) : undefined;
  const annualizedGrowth = canFitTrend
    ? damping * meanGrowth!
    : (options.fallbackGrowth ?? 0);
  const residualStdDev = Math.max(
    canFitTrend && growthRates.length > 1 ? standardDeviation(growthRates) : 0,
    residualStdDevFloor,
  );
  const pointEstimate =
    latest.value * Math.exp(annualizedGrowth * horizonPeriods);
  const intervalHalfWidth =
    intervalZ * residualStdDev * Math.sqrt(horizonPeriods);
  const ciLow =
    latest.value *
    Math.exp(annualizedGrowth * horizonPeriods - intervalHalfWidth);
  const ciHigh =
    latest.value *
    Math.exp(annualizedGrowth * horizonPeriods + intervalHalfWidth);

  return {
    modelId: "damped_log_trend_v1",
    status: canFitTrend ? "fit" : "fallback",
    pointEstimate,
    ciLow,
    ciHigh,
    latestValue: latest.value,
    latestPeriod: latest.period,
    historyPoints: history.length,
    horizonPeriods,
    annualizedGrowth,
    residualStdDev,
    fallbackLabel: canFitTrend ? undefined : options.fallbackLabel,
    diagnostics: canFitTrend
      ? [
          `fit on ${history.length} observations`,
          `damping ${formatPercent(damping)}`,
          `mean log growth ${formatPercent(meanGrowth!)}`,
        ]
      : [
          `only ${history.length} target observation${history.length === 1 ? "" : "s"}`,
          `fallback growth ${formatPercent(annualizedGrowth)}`,
          options.fallbackLabel ?? "fallback growth prior",
        ],
  };
}

export function roundForecast(
  forecast: DampedTrendForecast,
  increment: number,
): DampedTrendForecast {
  return {
    ...forecast,
    pointEstimate: roundToIncrement(forecast.pointEstimate, increment),
    ciLow: roundToIncrement(forecast.ciLow, increment),
    ciHigh: roundToIncrement(forecast.ciHigh, increment),
  };
}

export function roundToIncrement(value: number, increment: number): number {
  const rounded = Math.round(value / increment) * increment;
  return Number(rounded.toFixed(decimalPlaces(increment)));
}

function logGrowthRates(history: TimeSeriesPoint[]): number[] {
  const rates: number[] = [];
  for (let index = 1; index < history.length; index += 1) {
    const periodDistance = periodDistanceBetween(
      history[index - 1].period,
      history[index].period,
    );
    rates.push(
      Math.log(history[index].value / history[index - 1].value) /
        periodDistance,
    );
  }
  return rates;
}

function periodDistanceBetween(
  previousPeriod: TimeSeriesPoint["period"],
  currentPeriod: TimeSeriesPoint["period"],
): number {
  const previous = Number(previousPeriod);
  const current = Number(currentPeriod);
  if (!Number.isFinite(previous) || !Number.isFinite(current)) return 1;
  return Math.max(current - previous, 1);
}

function decimalPlaces(value: number): number {
  const text = value.toString().toLowerCase();
  if (!text.includes("e")) return text.split(".")[1]?.length ?? 0;
  const [, exponent = "0"] = text.split("e-");
  return Number(exponent);
}

function mean(values: number[]): number {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function standardDeviation(values: number[]): number {
  const average = mean(values);
  const variance =
    values.reduce((sum, value) => sum + (value - average) ** 2, 0) /
    (values.length - 1);
  return Math.sqrt(variance);
}

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(2)}%`;
}
