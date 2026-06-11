import type { ForecastCell } from "./forecast-cells";
import type {
  ForecastCellType,
  ForecastHorizon,
  ForecastSeriesMetadata,
  CountryCode,
  HistoricalPoint,
  PredictionCadence,
  PredictionRunMetadata,
  ReasoningStep,
  ResolutionPolicy,
  Unit,
} from "./forecast-cells";
import { buildNumericCdfFromInterval } from "./prediction-distribution";

export interface PredictionToolCall {
  tool: string;
  call: string;
  result: string;
}

export interface PredictionSeries {
  seriesId: string;
  type?: ForecastCellType;
  country?: CountryCode;
  title: string;
  measure: string;
  unit: Unit;
  source: string;
  sourceUrl?: string;
  cadence: PredictionCadence;
  priority: "P0" | "P1" | "P2";
  resolutionLatency: string;
  resolutionPolicy: ResolutionPolicy;
  benchmark?: string;
  chainableQuestions: string[];
  whyItMatters: string;
  drivers: string[];
  history: HistoricalPoint[];
  historyTool: PredictionToolCall;
  policyParameter?: string;
  predictionRun?: PredictionRunMetadata;
  targets: PredictionTarget[];
}

export interface PredictionTarget {
  slug: string;
  title: string;
  question: string;
  dataPointId: string;
  horizon: ForecastHorizon;
  horizonLabel: string;
  periodLabel: string;
  resolutionDate: string;
  resolutionRule: string;
  resolutionSourceUrl?: string;
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  tools?: PredictionToolCall[];
  rationale: string;
}

export function buildForecastCellsFromSeries(
  series: PredictionSeries[],
): ForecastCell[] {
  return series.flatMap((definition) =>
    definition.targets.map((target) =>
      buildForecastCellFromTarget(definition, target),
    ),
  );
}

function buildForecastCellFromTarget(
  series: PredictionSeries,
  target: PredictionTarget,
): ForecastCell {
  return {
    slug: target.slug,
    country: series.country ?? "US",
    type: series.type ?? "data",
    title: target.title,
    question: target.question,
    unit: series.unit,
    pointEstimate: target.pointEstimate,
    ciLow: target.ciLow,
    ciHigh: target.ciHigh,
    predictionDistribution: buildNumericCdfFromInterval({
      pointEstimate: target.pointEstimate,
      ciLow: target.ciLow,
      ciHigh: target.ciHigh,
    }),
    confidence: 0.8,
    resolutionDate: target.resolutionDate,
    resolutionSource: series.source,
    resolutionSourceUrl: target.resolutionSourceUrl ?? series.sourceUrl,
    resolutionRule: target.resolutionRule,
    dataPointId: target.dataPointId,
    policyParameter: series.policyParameter,
    historicalContext: series.history,
    drivers: series.drivers,
    series: buildSeriesMetadata(series, target),
    predictionRun: series.predictionRun,
    reasoning: buildReasoning(series, target),
  };
}

function buildSeriesMetadata(
  series: PredictionSeries,
  target: PredictionTarget,
): ForecastSeriesMetadata {
  return {
    seriesId: series.seriesId,
    country: series.country ?? "US",
    cadence: series.cadence,
    horizon: target.horizon,
    horizonLabel: target.horizonLabel,
    priority: series.priority,
    source: series.source,
    resolutionPolicy: series.resolutionPolicy,
    resolutionLatency: series.resolutionLatency,
    benchmark: series.benchmark,
    chainableQuestions: series.chainableQuestions,
  };
}

function buildReasoning(
  series: PredictionSeries,
  target: PredictionTarget,
): ReasoningStep[] {
  return [
    {
      kind: "heading",
      text: series.predictionRun
        ? `Recorded agent run · ${target.horizonLabel}`
        : `${capitalize(series.cadence)} ${target.horizonLabel} cell`,
    },
    {
      kind: "text",
      text:
        `${series.whyItMatters} This target resolves on ${target.resolutionDate} ` +
        `under a ${series.resolutionPolicy.replace("_", "-")} rule, with an expected ` +
        `${series.resolutionLatency} lag. The same series can also spawn ` +
        `${series.chainableQuestions.join(", ")} questions.`,
    },
    {
      kind: "tool",
      tool: series.historyTool.tool,
      call: series.historyTool.call,
      result: series.historyTool.result,
    },
    ...(target.tools ?? []).map<ReasoningStep>((tool) => ({
      kind: "tool",
      tool: tool.tool,
      call: tool.call,
      result: tool.result,
    })),
    {
      kind: "text",
      text: target.rationale,
    },
    {
      kind: "forecast",
      point: target.pointEstimate,
      ciLow: target.ciLow,
      ciHigh: target.ciHigh,
    },
  ];
}

function capitalize(value: string) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}
