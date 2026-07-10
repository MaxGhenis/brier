import type {
  CountryCode,
  ForecastCellType,
  ForecastCell,
  ForecastRunEntry,
  PredictionPackSet,
  PredictionPackSetMode,
  PredictionPreSubmitReviewWorkflow,
  PredictionRunActivityArtifact,
  ResolvedOutcome,
  Unit,
} from "./forecast-cells";
import { getForecastRunEntries } from "./forecast-cells";
import { conditionStatusFor, type ConditionStatus } from "./conditions";
export type { ConditionStatus } from "./conditions";
import {
  getDistributionTransformVersion,
  scoreNumericCdfDistribution,
  type DistributionProvenance,
  type NumericCdfScore,
  type PredictionDistribution,
} from "./prediction-distribution";
import {
  buildRecordedPredictionRunId,
  buildPredictionSpecs,
  buildResolutionRef,
  buildSpecId,
  buildSpecVersionId,
  buildRecordedPredictionRunRecords,
  SEEDED_RUN_RECORDED_AT,
  type PredictionRunRecord,
  type PredictionSpec,
} from "./prediction-specs";
import {
  buildForecastJudgeExport,
  type ForecastJudgeCalibrationReport,
  type ForecastJudgeExport,
} from "./forecast-judges";
import {
  THESIS_TARGET_LEDGER,
  requireLedgerTarget,
  type TargetRegisteredLedgerEntry,
} from "./ledger-targets";
import { sha256Hex } from "./canonical-json";
import {
  buildLedgerPersistenceBaseline,
  TIME_SERIES_PRIOR_VARIANT_ID,
} from "./time-series-priors";

export type PolicyEngineLedgerEntry =
  | TargetRegisteredLedgerEntry
  | ObservationRecordedLedgerEntry;

export type ThesisLogEntry =
  | PredictionRecordedLogEntry
  | PredictionResolvedLogEntry;

export type LedgerSourceKind = "official_release";

export type RecordedPredictionDistribution = Pick<
  PredictionDistribution,
  "format" | "pointCount" | "summary" | "provenance"
> & { transformVersion: string };

export interface ObservationRecordedLedgerEntry extends ResolvedOutcome {
  kind: "observation_recorded";
  observationId: string;
  dataPointId: string;
  periodLabel: string;
  unit: Unit;
  observedAt: string;
  sourceKind: LedgerSourceKind;
  targetContentHash?: string;
  ledgerRepoSha?: string;
  sourceVintage?: string;
  retrievedAt?: string;
  responseArchive?: {
    path: string;
    sha256: string;
    bytes: number;
    gzipSha256: string;
    gzipBytes: number;
    contentEncoding: "gzip";
  };
}

export interface PredictionRecordedLogEntry {
  kind: "prediction_recorded";
  forecastSlug: string;
  runId: string;
  specId: string;
  type: ForecastCellType;
  title: string;
  question: string;
  country: CountryCode;
  unit: Unit;
  pointEstimate: number;
  interval80: {
    lower: number;
    upper: number;
  };
  resolutionDate: string;
  resolutionSource: string;
  resolutionSourceUrl?: string;
  resolutionRule: string;
  resolutionPolicy?: string;
  recordedAt?: string;
  dataPointId?: string;
  distribution: RecordedPredictionDistribution;
  agent?: string;
  model?: string;
  runLabel: string;
  runDescription?: string;
  packSet?: PredictionPackSet;
  preSubmitReview?: PredictionPreSubmitReviewWorkflow;
  activityLog?: PredictionRunActivityArtifact[];
  custodyRootSha256?: string;
}

export interface PredictionResolvedLogEntry {
  kind: "prediction_resolved";
  resolutionRef: string;
  resolutionEventId: string;
  forecastSlug: string;
  recordedAt: string;
  dataPointId: string;
  ledgerFactRef: string;
  observationId: string;
}

export interface ResolvedForecastScore extends NumericCdfScore {
  scoreId: string;
  runId: string;
  runLabel: string;
  runAt?: string;
  agent?: string;
  model?: string;
  packSet?: PredictionPackSet;
  packMode: PredictionPackSetMode | "primary";
  packCount: number;
  resolutionEventId: string;
  scoringRule: "numeric_cdf_crps_v2_target_scale";
  distributionProvenance: DistributionProvenance;
  transformVersion: string;
  chronology: "verified" | "unverified" | "violated";
  observedAt: string;
  normalizationScale: number;
  normalizationScaleSource: "target_dispersion" | "target_primary_width";
  sharpness: number;
  ledgerFactRef: string;
  forecastSlug: string;
  dataPointId: string;
  observationId: string;
  pointEstimate: number;
  observedValue: number;
  unit: Unit;
  interval80: {
    lower: number;
    upper: number;
    width: number;
  };
  signedError: number;
  absoluteError: number;
  normalizedCrps: number;
  normalizedAbsoluteError: number;
  interval80Covered: boolean;
}

export interface PredictionResolutionLink {
  resolutionRef: string;
  specVersionId: string;
  predictionId: string;
  forecastSlug: string;
  targetFactRef?: string;
  factLedger: "PolicyEngine Ledger";
  resolverRule: string;
  status: "linked" | "pending";
}

export interface PredictionResolutionEvent {
  resolutionEventId: string;
  resolutionRef: string;
  forecastSlug: string;
  ledgerFactRef: string;
  observationId: string;
  occurredAt: string;
  payloadHash: string;
  status: "linked";
}

export interface PredictionResolutionQueueEntry {
  forecastSlug: string;
  title: string;
  country: CountryCode;
  dataPointId?: string;
  resolutionDate: string;
  resolutionSource: string;
  resolutionSourceUrl?: string;
  resolutionPolicy?: string;
  unit: Unit;
  pointEstimate: number;
  interval80: {
    lower: number;
    upper: number;
  };
}

export interface PolicyEngineLedgerExport {
  schemaVersion: "policyengine_ledger_v1";
  source: {
    name: "PolicyEngine Ledger";
    url: "https://github.com/PolicyEngine/arch-data";
    jsonMirrorUrl: "https://app.thesisinstitute.org/ledger.json";
  };
  counts: {
    facts: number;
    targets: number;
    observations: number;
  };
  entries: PolicyEngineLedgerEntry[];
}

export const THESIS_LOG_CHUNK_SIZE = 100;

export const THESIS_LOG_CHUNK_COLLECTIONS = [
  "entries",
  "specs",
  "runs",
  "scores",
] as const;

export type ThesisLogChunkCollection =
  (typeof THESIS_LOG_CHUNK_COLLECTIONS)[number];

export interface ThesisLogChunkReference {
  index: number;
  count: number;
  url: string;
  sha256: string;
}

export interface ThesisLogCollectionManifest {
  count: number;
  chunkCount: number;
  chunks: ThesisLogChunkReference[];
}

export interface ThesisLogExport {
  schemaVersion: "thesis_log_v3";
  source: {
    name: "Thesis Log";
    url: "https://app.thesisinstitute.org/log";
    jsonUrl: "https://app.thesisinstitute.org/log.json";
    factLedger: {
      name: "PolicyEngine Ledger";
      url: "https://github.com/PolicyEngine/arch-data";
      jsonUrl: "https://app.thesisinstitute.org/ledger.json";
    };
  };
  counts: {
    predictions: number;
    specs: number;
    runs: number;
    resolutions: number;
    scored: number;
    scoredUnverifiedChronology: number;
    scoredViolatedChronology: number;
    resolutionLinks: number;
    resolutionEvents: number;
    pendingResolution: number;
    preSubmitReviews: number;
    judgeTraceEvals: number;
    judgePairwiseEvals: number;
    judgePostResolutionEvals: number;
  };
  collections: Record<ThesisLogChunkCollection, ThesisLogCollectionManifest>;
  resolutionLinks: PredictionResolutionLink[];
  resolutionEvents: PredictionResolutionEvent[];
  judgeResults: ForecastJudgeLogSummary;
  resolutionQueue: PredictionResolutionQueueEntry[];
}

export interface ThesisLogData extends Omit<
  ThesisLogExport,
  "schemaVersion" | "collections"
> {
  schemaVersion: "thesis_log_v3";
  entries: ThesisLogEntry[];
  specs: PredictionSpec[];
  runs: ThesisLogRunRecord[];
  scores: ResolvedForecastScore[];
}

export interface ThesisLogChunkExport {
  schemaVersion: "thesis_log_chunk_v1";
  logSchemaVersion: "thesis_log_v3";
  collection: ThesisLogChunkCollection;
  chunkIndex: number;
  count: number;
  rows: ThesisLogData[ThesisLogChunkCollection];
}

export interface ForecastJudgeLogSummary {
  schemaVersion: "thesis_forecast_judges_summary_v1";
  generatedAt: string;
  policy: ForecastJudgeExport["policy"];
  calibration: ForecastJudgeCalibrationReport;
  fullExportJsonUrl: "https://app.thesisinstitute.org/forecasts/judges.json";
}

export const POLICYENGINE_LEDGER_FACTS_URL =
  process.env.POLICYENGINE_LEDGER_FACTS_URL ??
  "https://github.com/PolicyEngine/arch-data/raw/refs/heads/codex/thesis-ledger-facts/ledger/official_observations.jsonl";

interface PolicyEngineAggregateFactRow {
  value: number;
  observed_at: string;
  period: {
    type: string;
    value: string | number;
  };
  measure: {
    unit: string;
    concept_evidence_notes?: string;
  };
  source: {
    source_name?: string;
    source_table?: string;
    url?: string;
  };
  source_record_id: string;
  targetContentHash?: string;
  ledgerRepoSha?: string;
  sourceVintage?: string;
  retrievedAt?: string;
  responseArchive?: {
    path: string;
    sha256: string;
    bytes: number;
    gzipSha256: string;
    gzipBytes: number;
    contentEncoding: "gzip";
  };
}

let policyEngineLedgerPromise: Promise<PolicyEngineLedgerEntry[]> | null = null;

export async function loadPolicyEngineLedger(): Promise<
  PolicyEngineLedgerEntry[]
> {
  policyEngineLedgerPromise ??= fetchPolicyEngineLedger();
  return policyEngineLedgerPromise;
}

export function resetPolicyEngineLedgerCache() {
  policyEngineLedgerPromise = null;
}

export function parsePolicyEngineLedgerFacts(
  jsonl: string,
): PolicyEngineLedgerEntry[] {
  return jsonl
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => mapPolicyEngineAggregateFactToObservation(JSON.parse(line)));
}

function mapPolicyEngineAggregateFactToObservation(
  fact: PolicyEngineAggregateFactRow,
): PolicyEngineLedgerEntry {
  assertPolicyEngineFactShape(fact);

  return {
    kind: "observation_recorded",
    observationId: `obs.${fact.source_record_id}`,
    dataPointId: fact.source_record_id,
    periodLabel: formatLedgerPeriodLabel(fact.period),
    value: fact.value,
    unit: fact.measure.unit,
    observedAt: fact.observed_at,
    resolvedAt: fact.observed_at,
    sourceKind: "official_release",
    source: formatLedgerSource(fact.source),
    sourceUrl: fact.source.url,
    note: fact.measure.concept_evidence_notes,
    targetContentHash: fact.targetContentHash,
    ledgerRepoSha: fact.ledgerRepoSha,
    sourceVintage: fact.sourceVintage,
    retrievedAt: fact.retrievedAt,
    responseArchive: fact.responseArchive,
  };
}

async function fetchPolicyEngineLedger(): Promise<PolicyEngineLedgerEntry[]> {
  const response = await fetch(POLICYENGINE_LEDGER_FACTS_URL);
  if (!response.ok) {
    throw new Error(
      `PolicyEngine Ledger fetch failed with HTTP ${response.status}`,
    );
  }
  return [
    ...THESIS_TARGET_LEDGER,
    ...parsePolicyEngineLedgerFacts(await response.text()),
  ];
}

function assertPolicyEngineFactShape(
  fact: PolicyEngineAggregateFactRow,
): asserts fact is PolicyEngineAggregateFactRow & {
  measure: { unit: Unit; concept_evidence_notes?: string };
} {
  if (!fact.source_record_id) {
    throw new Error("PolicyEngine Ledger fact is missing source_record_id");
  }
  if (!fact.observed_at) {
    throw new Error(
      `Ledger fact ${fact.source_record_id} is missing observed_at`,
    );
  }
  if (typeof fact.value !== "number") {
    throw new Error(
      `Ledger fact ${fact.source_record_id} has non-numeric value`,
    );
  }
  if (!isUnit(fact.measure.unit)) {
    throw new Error(
      `Ledger fact ${fact.source_record_id} has unsupported unit ${fact.measure.unit}`,
    );
  }
}

function isUnit(unit: string): unit is Unit {
  return [
    "percent",
    "count",
    "gbp_billions",
    "usd",
    "usd_billions",
    "usd_monthly",
    "thousands",
    "millions",
    "per_1000_live_births",
    "ratio",
    "percent_growth",
  ].includes(unit);
}

function formatLedgerSource(source: PolicyEngineAggregateFactRow["source"]) {
  const publisher =
    source.source_name === "bls"
      ? "Bureau of Labor Statistics"
      : source.source_name === "statcan"
        ? "Statistics Canada"
        : source.source_name;
  return [publisher, source.source_table].filter(Boolean).join(" ");
}

function formatLedgerPeriodLabel(
  period: PolicyEngineAggregateFactRow["period"],
) {
  if (
    period.type === "month" &&
    typeof period.value === "string" &&
    /^\d{4}-\d{2}$/.test(period.value)
  ) {
    const [year, month] = period.value.split("-").map(Number);
    return new Intl.DateTimeFormat("en", {
      month: "long",
      year: "numeric",
      timeZone: "UTC",
    }).format(new Date(Date.UTC(year, month - 1, 1)));
  }
  return String(period.value);
}

const PREDICTION_RESOLUTION_FACT_LINKS = [
  {
    kind: "prediction_resolved",
    forecastSlug: "nonfarm-payrolls-may-2026",
    recordedAt: "2026-06-06T05:44:00+01:00",
    dataPointId: "bls.ces.total_nonfarm_payroll_change.may_2026.first_print",
    observationId:
      "obs.bls.ces.total_nonfarm_payroll_change.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "unemployment-rate-may-2026-first-print",
    recordedAt: "2026-06-06T05:44:00+01:00",
    dataPointId: "bls.cps.unemployment_rate.may_2026.first_print",
    observationId: "obs.bls.cps.unemployment_rate.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "average-hourly-earnings-mom-may-2026",
    recordedAt: "2026-06-06T05:44:00+01:00",
    dataPointId: "bls.ces.average_hourly_earnings_private.may_2026.first_print",
    observationId:
      "obs.bls.ces.average_hourly_earnings_private.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "canada-unemployment-rate-may-2026",
    recordedAt: "2026-06-06T05:44:00+01:00",
    dataPointId: "statcan.lfs.unemployment_rate.canada.may_2026.first_print",
    observationId:
      "obs.statcan.lfs.unemployment_rate.canada.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "canada-employment-change-may-2026",
    recordedAt: "2026-06-06T05:44:00+01:00",
    dataPointId: "statcan.lfs.employment_change.canada.may_2026.first_print",
    observationId:
      "obs.statcan.lfs.employment_change.canada.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "cpi-headline-mom-may-2026",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "bls.cpi.u.headline_mom.may_2026.first_print",
    observationId: "obs.bls.cpi.u.headline_mom.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "core-cpi-mom-may-2026",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "bls.cpi.u.core_mom.may_2026.first_print",
    observationId: "obs.bls.cpi.u.core_mom.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "canada-overnight-rate-june-2026-boc",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "bank_of_canada.overnight_rate.after_june_2026",
    observationId: "obs.bank_of_canada.overnight_rate.after_june_2026",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "us-mts-deficit-may-2026",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "treasury.mts.monthly_deficit.may_2026.first_print",
    observationId: "obs.treasury.mts.monthly_deficit.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "initial-jobless-claims-week-ending-2026-06-06",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "dol.eta.initial_claims.sa.week_ending_2026_06_06",
    observationId: "obs.dol.eta.initial_claims.sa.week_ending_2026_06_06",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "euro-area-ecb-deposit-facility-rate-june-2026",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "ecb.deposit_facility_rate.after_june_2026",
    observationId: "obs.ecb.deposit_facility_rate.after_june_2026",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "us-ppi-final-demand-mom-may-2026",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "bls.ppi.final_demand_monthly_change.may_2026.first_print",
    observationId:
      "obs.bls.ppi.final_demand_monthly_change.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "canada-building-permit-value-growth-april-2026",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId:
      "statcan.building_permits.total_value_mom.canada.april_2026.first_print",
    observationId:
      "obs.statcan.building_permits.total_value_mom.canada.april_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "uk-monthly-gdp-growth-april-2026",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "ons.gdp.monthly_growth.april_2026.first_print",
    observationId: "obs.ons.gdp.monthly_growth.april_2026.first_print",
  },
] satisfies Array<
  Omit<
    PredictionResolvedLogEntry,
    "resolutionRef" | "resolutionEventId" | "ledgerFactRef"
  >
>;

// Historical seed snapshot retained for migration compatibility. Active
// resolution is derived from the PolicyEngine Ledger by dataPointId.
export const THESIS_LOG: PredictionResolvedLogEntry[] =
  PREDICTION_RESOLUTION_FACT_LINKS.map((entry) => ({
    ...entry,
    resolutionRef: buildResolutionRef(entry.forecastSlug),
    resolutionEventId: buildResolutionEventId(entry),
    ledgerFactRef: entry.dataPointId,
  }));

export function isObservationRecordedLedgerEntry(
  entry: PolicyEngineLedgerEntry | ThesisLogEntry,
): entry is ObservationRecordedLedgerEntry {
  return entry.kind === "observation_recorded";
}

export function isTargetRegisteredLedgerEntry(
  entry: PolicyEngineLedgerEntry | ThesisLogEntry,
): entry is TargetRegisteredLedgerEntry {
  return entry.kind === "target_registered";
}

export function isPredictionResolvedLogEntry(
  entry: ThesisLogEntry,
): entry is PredictionResolvedLogEntry {
  return entry.kind === "prediction_resolved";
}

export function isPredictionRecordedLogEntry(
  entry: ThesisLogEntry,
): entry is PredictionRecordedLogEntry {
  return entry.kind === "prediction_recorded";
}

export function getResolvedObservationForForecast(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
): ObservationRecordedLedgerEntry | undefined {
  if (!forecast.dataPointId) return undefined;
  const observations = getObservationsForDataPoint(
    forecast.dataPointId,
    ledger,
  );
  if (observations.length === 0) return undefined;

  return [...observations].sort(compareFirstPrintObservations)[0];
}

function compareFirstPrintObservations(
  left: ObservationRecordedLedgerEntry,
  right: ObservationRecordedLedgerEntry,
): number {
  return left.observedAt === right.observedAt
    ? left.observationId.localeCompare(right.observationId)
    : left.observedAt.localeCompare(right.observedAt);
}

function buildPredictionResolvedLogEntry(
  forecast: ForecastCell,
  observation: ObservationRecordedLedgerEntry,
): PredictionResolvedLogEntry {
  return {
    kind: "prediction_resolved",
    resolutionRef: buildResolutionRef(forecast.slug),
    resolutionEventId: buildResolutionEventId({
      forecastSlug: forecast.slug,
      observationId: observation.observationId,
    }),
    forecastSlug: forecast.slug,
    recordedAt: observation.resolvedAt,
    dataPointId: observation.dataPointId,
    ledgerFactRef: observation.dataPointId,
    observationId: observation.observationId,
  };
}

export function buildResolvedPredictionLogEntries(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): PredictionResolvedLogEntry[] {
  return forecasts
    .flatMap((forecast) => {
      const observation = getResolvedObservationForForecast(forecast, ledger);
      return observation
        ? [buildPredictionResolvedLogEntry(forecast, observation)]
        : [];
    })
    .sort((a, b) =>
      a.recordedAt === b.recordedAt
        ? a.forecastSlug.localeCompare(b.forecastSlug)
        : a.recordedAt.localeCompare(b.recordedAt),
    );
}

export function buildPredictionRecordedLogEntries(
  forecasts: ForecastCell[],
): PredictionRecordedLogEntry[] {
  return forecasts.flatMap((forecast) => {
    const ledgerTarget = forecast.dataPointId
      ? requireLedgerTarget(forecast.dataPointId)
      : undefined;
    return getForecastRunEntries(forecast).flatMap((run) => {
      if (!run.predictionDistribution) return [];
      const runId = buildRecordedPredictionRunId(
        forecast,
        run.predictionRun?.runAt,
        run.variantId,
        run,
      );

      return [
        {
          kind: "prediction_recorded",
          forecastSlug: forecast.slug,
          runId,
          specId: buildSpecId(forecast.slug),
          type: forecast.type,
          title: forecast.title,
          question: forecast.question,
          country: forecast.country ?? "US",
          unit: forecast.unit,
          pointEstimate: run.pointEstimate,
          interval80: {
            lower: run.ciLow,
            upper: run.ciHigh,
          },
          resolutionDate:
            ledgerTarget?.resolutionDate ?? forecast.resolutionDate,
          resolutionSource:
            ledgerTarget?.resolutionSource ?? forecast.resolutionSource,
          resolutionSourceUrl:
            ledgerTarget?.resolutionSourceUrl ?? forecast.resolutionSourceUrl,
          resolutionRule:
            ledgerTarget?.resolutionRule ?? forecast.resolutionRule,
          resolutionPolicy:
            ledgerTarget?.resolutionPolicy ?? forecast.series?.resolutionPolicy,
          recordedAt: run.predictionRun?.runAt,
          dataPointId: ledgerTarget?.dataPointId ?? forecast.dataPointId,
          distribution: {
            format: run.predictionDistribution.format,
            pointCount: run.predictionDistribution.pointCount,
            summary: run.predictionDistribution.summary,
            provenance: run.predictionDistribution.provenance,
            transformVersion: getDistributionTransformVersion(
              run.predictionDistribution,
            ),
          },
          agent: run.predictionRun?.agent,
          model: run.predictionRun?.model,
          runLabel: run.label,
          runDescription: run.description,
          packSet: run.packSet,
          preSubmitReview: run.predictionRun?.preSubmitReview,
          activityLog: run.predictionRun?.activityLog,
          custodyRootSha256: run.predictionRun?.custodyRootSha256,
        },
      ];
    });
  });
}

export function buildThesisLog(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): ThesisLogEntry[] {
  return [
    ...buildPredictionRecordedLogEntries(forecasts),
    ...buildResolvedPredictionLogEntries(forecasts, ledger),
  ];
}

export function buildResolutionQueue(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): PredictionResolutionQueueEntry[] {
  return forecasts
    .filter((forecast) => !getResolutionForForecast(forecast, ledger))
    .map((forecast) => {
      const ledgerTarget = forecast.dataPointId
        ? requireLedgerTarget(forecast.dataPointId)
        : undefined;
      return {
        forecastSlug: forecast.slug,
        title: forecast.title,
        country: forecast.country ?? "US",
        dataPointId: ledgerTarget?.dataPointId ?? forecast.dataPointId,
        resolutionDate: ledgerTarget?.resolutionDate ?? forecast.resolutionDate,
        resolutionSource:
          ledgerTarget?.resolutionSource ?? forecast.resolutionSource,
        resolutionSourceUrl:
          ledgerTarget?.resolutionSourceUrl ?? forecast.resolutionSourceUrl,
        resolutionPolicy:
          ledgerTarget?.resolutionPolicy ?? forecast.series?.resolutionPolicy,
        unit: forecast.unit,
        pointEstimate: forecast.pointEstimate,
        interval80: {
          lower: forecast.ciLow,
          upper: forecast.ciHigh,
        },
      };
    })
    .sort((a, b) =>
      a.resolutionDate === b.resolutionDate
        ? a.title.localeCompare(b.title)
        : a.resolutionDate.localeCompare(b.resolutionDate),
    );
}

export function buildPredictionResolutionLinks(
  forecasts: ForecastCell[],
  specs: PredictionSpec[] = buildPredictionSpecs(forecasts),
  ledger: PolicyEngineLedgerEntry[] = [],
): PredictionResolutionLink[] {
  const specsByPredictionId = new Map(
    specs.map((spec) => [spec.predictionId, spec]),
  );

  return forecasts.map((forecast) => {
    const spec = specsByPredictionId.get(forecast.slug);
    const ledgerTarget = forecast.dataPointId
      ? requireLedgerTarget(forecast.dataPointId)
      : undefined;
    return {
      resolutionRef: buildResolutionRef(forecast.slug),
      specVersionId: spec?.specVersionId ?? buildSpecVersionId(forecast.slug),
      predictionId: forecast.slug,
      forecastSlug: forecast.slug,
      targetFactRef: ledgerTarget?.dataPointId ?? forecast.dataPointId,
      factLedger: "PolicyEngine Ledger",
      resolverRule: ledgerTarget?.resolutionRule ?? forecast.resolutionRule,
      status: getResolutionForForecast(forecast, ledger) ? "linked" : "pending",
    };
  });
}

export function buildPredictionResolutionEvents(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): PredictionResolutionEvent[] {
  return buildResolvedPredictionLogEntries(forecasts, ledger).map((entry) => {
    const observation = getObservationForId(entry.observationId, ledger);
    if (!observation) {
      throw new Error(
        `Missing observation payload for resolution event ${entry.resolutionEventId}`,
      );
    }
    return {
      resolutionEventId: entry.resolutionEventId,
      resolutionRef: entry.resolutionRef,
      forecastSlug: entry.forecastSlug,
      ledgerFactRef: entry.ledgerFactRef,
      observationId: entry.observationId,
      occurredAt: entry.recordedAt,
      payloadHash: sha256Hex({
        resolutionEventId: entry.resolutionEventId,
        ledgerFactRef: entry.ledgerFactRef,
        observationId: entry.observationId,
        observedValue: observation.value,
        unit: observation.unit,
      }),
      status: "linked" as const,
    };
  });
}

export function buildPolicyEngineLedgerExport(
  entries: PolicyEngineLedgerEntry[],
): PolicyEngineLedgerExport {
  const targets = entries.filter(isTargetRegisteredLedgerEntry);
  const observations = entries.filter(isObservationRecordedLedgerEntry);

  return {
    schemaVersion: "policyengine_ledger_v1",
    source: {
      name: "PolicyEngine Ledger",
      url: "https://github.com/PolicyEngine/arch-data",
      jsonMirrorUrl: "https://app.thesisinstitute.org/ledger.json",
    },
    counts: {
      facts: entries.length,
      targets: targets.length,
      observations: observations.length,
    },
    entries,
  };
}

// Run records omit their 201-point CDFs. The full distributions are served by
// the target-architecture chunks and shown on each cell page.
export type ThesisLogRunRecord = Omit<PredictionRunRecord, "output"> & {
  output: Omit<PredictionRunRecord["output"], "distribution"> & {
    distribution: {
      format: PredictionRunRecord["output"]["distribution"]["format"];
      pointCount: number;
      pointsUrl: string;
      provenance: DistributionProvenance;
      transformVersion: string;
    };
  };
};

function toLogRunRecord(run: PredictionRunRecord): ThesisLogRunRecord {
  return {
    ...run,
    output: {
      ...run.output,
      distribution: {
        format: run.output.distribution.format,
        pointCount: run.output.distribution.pointCount,
        pointsUrl: "/forecasts/targets/forecastDistributions/manifest.json",
        provenance: run.output.distribution.provenance,
        transformVersion: getDistributionTransformVersion(
          run.output.distribution,
        ),
      },
    },
  };
}

export function buildThesisLogData(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): ThesisLogData {
  const entries = buildThesisLog(forecasts, ledger);
  const specs = buildPredictionSpecs(forecasts);
  const runs = buildRecordedPredictionRunRecords(forecasts, specs);
  const resolutionLinks = buildPredictionResolutionLinks(
    forecasts,
    specs,
    ledger,
  );
  const resolutionEvents = buildPredictionResolutionEvents(forecasts, ledger);
  const scores = scoreResolvedForecasts(forecasts, ledger);
  const judgeResults = buildForecastJudgeExport({ forecasts, scores });
  const judgeSummary = buildForecastJudgeLogSummary(judgeResults);
  const resolutionQueue = buildResolutionQueue(forecasts, ledger);

  return {
    schemaVersion: "thesis_log_v3",
    source: {
      name: "Thesis Log",
      url: "https://app.thesisinstitute.org/log",
      jsonUrl: "https://app.thesisinstitute.org/log.json",
      factLedger: {
        name: "PolicyEngine Ledger",
        url: "https://github.com/PolicyEngine/arch-data",
        jsonUrl: "https://app.thesisinstitute.org/ledger.json",
      },
    },
    counts: {
      predictions: entries.filter(isPredictionRecordedLogEntry).length,
      specs: specs.length,
      runs: runs.length,
      resolutions: entries.filter(isPredictionResolvedLogEntry).length,
      // Headline scored count = chronology-verified only. Unverified
      // (no trustworthy run time) and violated (run time at/after the
      // observation) scores stay in `scores` for transparency but are
      // outside the official track record.
      scored: scores.filter((score) => score.chronology === "verified").length,
      scoredUnverifiedChronology: scores.filter(
        (score) => score.chronology === "unverified",
      ).length,
      scoredViolatedChronology: scores.filter(
        (score) => score.chronology === "violated",
      ).length,
      resolutionLinks: resolutionLinks.length,
      resolutionEvents: resolutionEvents.length,
      pendingResolution: resolutionQueue.length,
      preSubmitReviews: runs.filter((run) => run.preSubmitReview).length,
      judgeTraceEvals: judgeResults.traceQuality.length,
      judgePairwiseEvals: judgeResults.pairwise.length,
      judgePostResolutionEvals: judgeResults.postResolution.length,
    },
    entries,
    specs,
    runs: runs.map(toLogRunRecord),
    resolutionLinks,
    resolutionEvents,
    scores,
    judgeResults: judgeSummary,
    resolutionQueue,
  };
}

export function buildThesisLogExport(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): ThesisLogExport {
  return buildThesisLogManifest(buildThesisLogData(forecasts, ledger));
}

export function buildThesisLogManifest(data: ThesisLogData): ThesisLogExport {
  const {
    entries: _entries,
    specs: _specs,
    runs: _runs,
    scores: _scores,
    ...slim
  } = data;
  return {
    ...slim,
    collections: Object.fromEntries(
      THESIS_LOG_CHUNK_COLLECTIONS.map((collection) => [
        collection,
        buildThesisLogCollectionManifest(data, collection),
      ]),
    ) as ThesisLogExport["collections"],
  };
}

export function buildThesisLogChunk(
  data: ThesisLogData,
  collection: ThesisLogChunkCollection,
  chunkIndex: number,
): ThesisLogChunkExport {
  const rows = data[collection];
  const start = chunkIndex * THESIS_LOG_CHUNK_SIZE;
  const chunkRows = rows.slice(
    start,
    start + THESIS_LOG_CHUNK_SIZE,
  ) as ThesisLogChunkExport["rows"];
  return {
    schemaVersion: "thesis_log_chunk_v1",
    logSchemaVersion: "thesis_log_v3",
    collection,
    chunkIndex,
    count: chunkRows.length,
    rows: chunkRows,
  };
}

export function isThesisLogChunkCollection(
  value: string,
): value is ThesisLogChunkCollection {
  return THESIS_LOG_CHUNK_COLLECTIONS.includes(
    value as ThesisLogChunkCollection,
  );
}

function buildThesisLogCollectionManifest(
  data: ThesisLogData,
  collection: ThesisLogChunkCollection,
): ThesisLogCollectionManifest {
  const count = data[collection].length;
  const chunkCount = Math.ceil(count / THESIS_LOG_CHUNK_SIZE);
  return {
    count,
    chunkCount,
    chunks: Array.from({ length: chunkCount }, (_, index) => {
      const chunk = buildThesisLogChunk(data, collection, index);
      return {
        index,
        count: chunk.count,
        url: `/log/${collection}/${index}.json`,
        sha256: sha256Hex(chunk),
      };
    }),
  };
}

export function buildForecastJudgeLogSummary(
  judgeResults: ForecastJudgeExport,
): ForecastJudgeLogSummary {
  return {
    schemaVersion: "thesis_forecast_judges_summary_v1",
    generatedAt: judgeResults.generatedAt,
    policy: judgeResults.policy,
    calibration: judgeResults.calibration,
    fullExportJsonUrl: "https://app.thesisinstitute.org/forecasts/judges.json",
  };
}

export function getObservationForId(
  observationId: string,
  ledger: PolicyEngineLedgerEntry[],
): ObservationRecordedLedgerEntry | undefined {
  return ledger
    .filter(isObservationRecordedLedgerEntry)
    .filter((entry) => entry.observationId === observationId)
    .sort(compareFirstPrintObservations)[0];
}

export function getObservationsForDataPoint(
  dataPointId: string,
  ledger: PolicyEngineLedgerEntry[],
): ObservationRecordedLedgerEntry[] {
  return ledger
    .filter(isObservationRecordedLedgerEntry)
    .filter((entry) => entry.dataPointId === dataPointId);
}

export function getResolutionForForecast(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
): PredictionResolvedLogEntry | undefined {
  const observation = getResolvedObservationForForecast(forecast, ledger);
  return observation
    ? buildPredictionResolvedLogEntry(forecast, observation)
    : undefined;
}

export function getResolvedOutcomeForForecast(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
): ResolvedOutcome | undefined {
  const entry = getResolutionForForecast(forecast, ledger);
  if (!entry) return undefined;
  const observation = getObservationForId(entry.observationId, ledger);
  if (!observation) return undefined;
  return {
    value: observation.value,
    resolvedAt: observation.resolvedAt,
    source: observation.source,
    sourceUrl: observation.sourceUrl,
    note: observation.note,
  };
}

export function scoreResolvedForecast(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
): ResolvedForecastScore | undefined {
  const primaryRun = getForecastRunEntries(forecast)[0];
  if (!primaryRun) return undefined;
  return scoreResolvedForecastRun(forecast, primaryRun, ledger);
}

// A score enters the headline track record only when the run's recorded
// time verifiably precedes the observation. Runs with no usable run time
// (including the legacy seeded placeholder) are "unverified"; runs whose
// recorded time is at or after the observation are "violated". Both stay
// published for transparency but never count toward headline calibration.
export type ScoreChronology = "verified" | "unverified" | "violated";

export function classifyScoreChronology(
  runAt: string | undefined,
  observedAt: string | undefined,
): ScoreChronology {
  if (!runAt || runAt === SEEDED_RUN_RECORDED_AT) return "unverified";
  const runTime = Date.parse(runAt);
  const observedTime = observedAt ? Date.parse(observedAt) : Number.NaN;
  if (!Number.isFinite(runTime) || !Number.isFinite(observedTime)) {
    return "unverified";
  }
  return runTime < observedTime ? "verified" : "violated";
}

// The CRPS denominator is a per-target scale every run on the target
// shares, derived from the primary run's fetched history — successive
// changes for three or more points, else the primary interval's implied
// sigma. A run cannot lower its own normalized score by widening, because
// the denominator is fixed by the target, not the run.
export function targetNormalizationScale(forecast: ForecastCell): {
  scale: number;
  source: "target_dispersion" | "target_primary_width";
} {
  const values = (forecast.historicalContext ?? [])
    .map((point) => point.value)
    .filter((value): value is number => typeof value === "number");
  if (values.length >= 3) {
    const diffs = values.slice(1).map((value, index) => value - values[index]);
    const mean = diffs.reduce((total, diff) => total + diff, 0) / diffs.length;
    const variance =
      diffs.reduce((total, diff) => total + (diff - mean) ** 2, 0) /
      Math.max(diffs.length - 1, 1);
    const sigma = Math.sqrt(variance);
    if (sigma > 0) return { scale: sigma, source: "target_dispersion" };
  }
  const primaryWidth = Math.abs(forecast.ciHigh - forecast.ciLow);
  // 2 * 1.28155 converts an 80% interval width into an implied sigma.
  const implied = primaryWidth / 2.5631;
  return {
    scale: implied > 0 ? implied : 1,
    source: "target_primary_width",
  };
}

export function scoreResolvedForecastRun(
  forecast: ForecastCell,
  run: ForecastRunEntry,
  ledger: PolicyEngineLedgerEntry[],
  conditionOverrides?: Map<string, ConditionStatus>,
): ResolvedForecastScore | undefined {
  // A conditional branch is graded only when its registered condition
  // actually occurred: both branches of a pair resolve against the same
  // official print, and scoring the counterfactual branch would grade a
  // hypothesis whose premise never happened (review finding F6).
  if (forecast.type === "conditional") {
    const gate = conditionStatusFor(forecast, conditionOverrides);
    if (gate !== "satisfied") return undefined;
  }
  const resolution = getResolutionForForecast(forecast, ledger);
  if (!resolution || !run.predictionDistribution) return undefined;

  const observation = getObservationForId(resolution.observationId, ledger);
  if (!observation) return undefined;

  const distributionScore = scoreNumericCdfDistribution(
    run.predictionDistribution,
    observation.value,
  );
  const signedError = observation.value - run.pointEstimate;
  const runId = buildRecordedPredictionRunId(
    forecast,
    run.predictionRun?.runAt,
    run.variantId,
    run,
  );
  const resolutionEventId = buildResolutionEventId(resolution);
  const scoringRule = "numeric_cdf_crps_v2_target_scale";
  const distributionProvenance = run.predictionDistribution.provenance;
  const transformVersion = getDistributionTransformVersion(
    run.predictionDistribution,
  );
  const interval80Width = Math.abs(run.ciHigh - run.ciLow);
  const normalization = targetNormalizationScale(forecast);
  const chronology = classifyScoreChronology(
    run.predictionRun?.runAt,
    observation.observedAt,
  );

  return {
    scoreId: buildScoreId({
      runId,
      resolutionEventId,
      scoringRule,
      transformVersion,
      forecastOutput: {
        pointEstimate: run.pointEstimate,
        interval80: { lower: run.ciLow, upper: run.ciHigh },
        distribution: run.predictionDistribution,
      },
      outcome: {
        observationId: observation.observationId,
        observedValue: observation.value,
        unit: observation.unit,
      },
    }),
    runId,
    runLabel: run.label,
    runAt: run.predictionRun?.runAt,
    agent: run.predictionRun?.agent,
    model: run.predictionRun?.model,
    packSet: run.packSet,
    packMode: run.packSet?.mode ?? "primary",
    packCount: run.packSet?.packs.length ?? 0,
    resolutionEventId,
    scoringRule,
    distributionProvenance,
    transformVersion,
    chronology,
    observedAt: observation.observedAt,
    ledgerFactRef: observation.dataPointId,
    forecastSlug: forecast.slug,
    dataPointId: resolution.dataPointId,
    observationId: observation.observationId,
    pointEstimate: run.pointEstimate,
    observedValue: observation.value,
    unit: observation.unit,
    interval80: {
      lower: run.ciLow,
      upper: run.ciHigh,
      width: interval80Width,
    },
    signedError,
    absoluteError: Math.abs(signedError),
    normalizationScale: normalization.scale,
    normalizationScaleSource: normalization.source,
    normalizedCrps: distributionScore.crps / normalization.scale,
    normalizedAbsoluteError: Math.abs(signedError) / normalization.scale,
    sharpness: interval80Width / normalization.scale,
    interval80Covered:
      run.ciLow <= observation.value && observation.value <= run.ciHigh,
    ...distributionScore,
  };
}

export function scoreResolvedForecasts(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): ResolvedForecastScore[] {
  return forecasts.flatMap((forecast) => {
    return getForecastRunEntries(forecast).flatMap((run) => {
      const score = scoreResolvedForecastRun(forecast, run, ledger);
      return score ? [score] : [];
    });
  });
}

export function withResolvedOutcome(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
): ForecastCell {
  const resolvedForecast: ForecastCell = {
    ...forecast,
    comparisonRuns: forecast.comparisonRuns?.filter(
      (run) => run.variantId !== TIME_SERIES_PRIOR_VARIANT_ID,
    ),
    persistenceBaseline: undefined,
    resolvedOutcome:
      getResolvedOutcomeForForecast(forecast, ledger) ??
      forecast.resolvedOutcome,
  };
  const primaryRun = getForecastRunEntries(resolvedForecast)[0];
  const primaryScore = primaryRun
    ? scoreResolvedForecastRun(resolvedForecast, primaryRun, ledger)
    : undefined;
  if (!primaryScore || primaryScore.chronology !== "verified") {
    return resolvedForecast;
  }

  const baseline = buildLedgerPersistenceBaseline(resolvedForecast, ledger);
  return {
    ...resolvedForecast,
    persistenceBaseline: baseline.record,
    comparisonRuns: baseline.comparisonRun
      ? [...(resolvedForecast.comparisonRuns ?? []), baseline.comparisonRun]
      : resolvedForecast.comparisonRuns,
  };
}

export function withResolvedOutcomes(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): ForecastCell[] {
  return forecasts.map((forecast) => withResolvedOutcome(forecast, ledger));
}

function buildResolutionEventId({
  forecastSlug,
  observationId,
}: {
  forecastSlug: string;
  observationId: string;
}) {
  return `resolution_event.${forecastSlug}.${observationId
    .replace(/^obs\./, "")
    .replace(/[^A-Za-z0-9]+/g, "-")}`;
}

export function buildScoreId(payload: {
  runId: string;
  resolutionEventId: string;
  scoringRule: ResolvedForecastScore["scoringRule"];
  transformVersion: string;
  forecastOutput: unknown;
  outcome: unknown;
}) {
  const payloadDigest = sha256Hex(payload);
  return `score.${payload.runId}.${payload.resolutionEventId}.${payload.scoringRule}.${payloadDigest.slice(0, 16)}`;
}
