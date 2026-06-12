import type {
  CountryCode,
  ForecastCellType,
  ForecastCell,
  ResolvedOutcome,
  Unit,
} from "./forecast-cells";
import {
  scoreNumericCdfDistribution,
  type NumericCdfScore,
  type PredictionDistribution,
} from "./prediction-distribution";
import {
  buildRecordedPredictionRunId,
  buildPredictionSpecs,
  buildResolutionRef,
  buildSpecVersionId,
  buildRecordedPredictionRunRecords,
  type PredictionRunRecord,
  type PredictionSpec,
} from "./prediction-specs";

export type PolicyEngineLedgerEntry = ObservationRecordedLedgerEntry;

export type ThesisLogEntry =
  | PredictionRecordedLogEntry
  | PredictionResolvedLogEntry;

export type LedgerSourceKind = "official_release";

export interface ObservationRecordedLedgerEntry extends ResolvedOutcome {
  kind: "observation_recorded";
  observationId: string;
  dataPointId: string;
  periodLabel: string;
  unit: Unit;
  observedAt: string;
  sourceKind: LedgerSourceKind;
}

export interface PredictionRecordedLogEntry {
  kind: "prediction_recorded";
  forecastSlug: string;
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
  distribution: PredictionDistribution;
  agent?: string;
  model?: string;
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
  resolutionEventId: string;
  scoringRule: "numeric_cdf_crps_v1";
  ledgerFactRef: string;
  forecastSlug: string;
  dataPointId: string;
  observationId: string;
  pointEstimate: number;
  unit: Unit;
  signedError: number;
  absoluteError: number;
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
    observations: number;
  };
  entries: PolicyEngineLedgerEntry[];
}

export interface ThesisLogExport {
  schemaVersion: "thesis_log_v1";
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
    resolutionLinks: number;
    resolutionEvents: number;
    pendingResolution: number;
  };
  entries: ThesisLogEntry[];
  specs: PredictionSpec[];
  runs: PredictionRunRecord[];
  resolutionLinks: PredictionResolutionLink[];
  resolutionEvents: PredictionResolutionEvent[];
  scores: ResolvedForecastScore[];
  resolutionQueue: PredictionResolutionQueueEntry[];
}

export const POLICYENGINE_LEDGER_FACTS_URL =
  process.env.POLICYENGINE_LEDGER_FACTS_URL ??
  "https://raw.githubusercontent.com/PolicyEngine/arch-data/codex/thesis-ledger-facts/ledger/official_observations.jsonl";

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
  };
}

async function fetchPolicyEngineLedger(): Promise<PolicyEngineLedgerEntry[]> {
  const response = await fetch(POLICYENGINE_LEDGER_FACTS_URL);
  if (!response.ok) {
    throw new Error(
      `PolicyEngine Ledger fetch failed with HTTP ${response.status}`,
    );
  }
  return parsePolicyEngineLedgerFacts(await response.text());
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
    observationId: "obs.bls.ppi.final_demand_monthly_change.may_2026.first_print",
  },
  {
    kind: "prediction_resolved",
    forecastSlug: "canada-building-permit-value-growth-april-2026",
    recordedAt: "2026-06-12T20:37:03+00:00",
    dataPointId: "statcan.building_permits.total_value_mom.canada.april_2026.first_print",
    observationId: "obs.statcan.building_permits.total_value_mom.canada.april_2026.first_print",
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

export function buildPredictionRecordedLogEntries(
  forecasts: ForecastCell[],
): PredictionRecordedLogEntry[] {
  return forecasts.flatMap((forecast) => {
    if (!forecast.predictionDistribution) return [];

    return [
      {
        kind: "prediction_recorded",
        forecastSlug: forecast.slug,
        type: forecast.type,
        title: forecast.title,
        question: forecast.question,
        country: forecast.country ?? "US",
        unit: forecast.unit,
        pointEstimate: forecast.pointEstimate,
        interval80: {
          lower: forecast.ciLow,
          upper: forecast.ciHigh,
        },
        resolutionDate: forecast.resolutionDate,
        resolutionSource: forecast.resolutionSource,
        resolutionSourceUrl: forecast.resolutionSourceUrl,
        resolutionRule: forecast.resolutionRule,
        resolutionPolicy: forecast.series?.resolutionPolicy,
        recordedAt: forecast.predictionRun?.runAt,
        dataPointId: forecast.dataPointId,
        distribution: forecast.predictionDistribution,
        agent: forecast.predictionRun?.agent,
        model: forecast.predictionRun?.model,
      },
    ];
  });
}

export function buildThesisLog(forecasts: ForecastCell[]): ThesisLogEntry[] {
  return [...buildPredictionRecordedLogEntries(forecasts), ...THESIS_LOG];
}

export function buildResolutionQueue(
  forecasts: ForecastCell[],
): PredictionResolutionQueueEntry[] {
  return forecasts
    .filter((forecast) => !getResolutionForForecast(forecast.slug))
    .map((forecast) => ({
      forecastSlug: forecast.slug,
      title: forecast.title,
      country: forecast.country ?? "US",
      dataPointId: forecast.dataPointId,
      resolutionDate: forecast.resolutionDate,
      resolutionSource: forecast.resolutionSource,
      resolutionSourceUrl: forecast.resolutionSourceUrl,
      resolutionPolicy: forecast.series?.resolutionPolicy,
      unit: forecast.unit,
      pointEstimate: forecast.pointEstimate,
      interval80: {
        lower: forecast.ciLow,
        upper: forecast.ciHigh,
      },
    }))
    .sort((a, b) =>
      a.resolutionDate === b.resolutionDate
        ? a.title.localeCompare(b.title)
        : a.resolutionDate.localeCompare(b.resolutionDate),
    );
}

export function buildPredictionResolutionLinks(
  forecasts: ForecastCell[],
  specs: PredictionSpec[] = buildPredictionSpecs(forecasts),
): PredictionResolutionLink[] {
  const specsByPredictionId = new Map(
    specs.map((spec) => [spec.predictionId, spec]),
  );

  return forecasts.map((forecast) => {
    const spec = specsByPredictionId.get(forecast.slug);
    return {
      resolutionRef: buildResolutionRef(forecast.slug),
      specVersionId: spec?.specVersionId ?? buildSpecVersionId(forecast.slug),
      predictionId: forecast.slug,
      forecastSlug: forecast.slug,
      targetFactRef: forecast.dataPointId,
      factLedger: "PolicyEngine Ledger",
      resolverRule: forecast.resolutionRule,
      status: getResolutionForForecast(forecast.slug) ? "linked" : "pending",
    };
  });
}

export function buildPredictionResolutionEvents(): PredictionResolutionEvent[] {
  return THESIS_LOG.map((entry) => ({
    resolutionEventId: entry.resolutionEventId,
    resolutionRef: entry.resolutionRef,
    forecastSlug: entry.forecastSlug,
    ledgerFactRef: entry.ledgerFactRef,
    observationId: entry.observationId,
    occurredAt: entry.recordedAt,
    payloadHash: buildStaticPayloadHash({
      resolutionEventId: entry.resolutionEventId,
      ledgerFactRef: entry.ledgerFactRef,
      observationId: entry.observationId,
    }),
    status: "linked",
  }));
}

export function buildPolicyEngineLedgerExport(
  entries: PolicyEngineLedgerEntry[],
): PolicyEngineLedgerExport {
  return {
    schemaVersion: "policyengine_ledger_v1",
    source: {
      name: "PolicyEngine Ledger",
      url: "https://github.com/PolicyEngine/arch-data",
      jsonMirrorUrl: "https://app.thesisinstitute.org/ledger.json",
    },
    counts: {
      facts: entries.length,
      observations: entries.filter(isObservationRecordedLedgerEntry).length,
    },
    entries,
  };
}

export function buildThesisLogExport(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): ThesisLogExport {
  const entries = buildThesisLog(forecasts);
  const specs = buildPredictionSpecs(forecasts);
  const runs = buildRecordedPredictionRunRecords(forecasts, specs);
  const resolutionLinks = buildPredictionResolutionLinks(forecasts, specs);
  const resolutionEvents = buildPredictionResolutionEvents();
  const scores = scoreResolvedForecasts(forecasts, ledger);
  const resolutionQueue = buildResolutionQueue(forecasts);

  return {
    schemaVersion: "thesis_log_v1",
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
      scored: scores.length,
      resolutionLinks: resolutionLinks.length,
      resolutionEvents: resolutionEvents.length,
      pendingResolution: resolutionQueue.length,
    },
    entries,
    specs,
    runs,
    resolutionLinks,
    resolutionEvents,
    scores,
    resolutionQueue,
  };
}

export function getObservationForId(
  observationId: string,
  ledger: PolicyEngineLedgerEntry[],
): ObservationRecordedLedgerEntry | undefined {
  return ledger.find((entry) => entry.observationId === observationId);
}

export function getObservationsForDataPoint(
  dataPointId: string,
  ledger: PolicyEngineLedgerEntry[],
): ObservationRecordedLedgerEntry[] {
  return ledger.filter((entry) => entry.dataPointId === dataPointId);
}

export function getResolutionForForecast(
  forecastSlug: string,
): PredictionResolvedLogEntry | undefined {
  return THESIS_LOG.find((entry) => entry.forecastSlug === forecastSlug);
}

export function getResolvedOutcomeForForecast(
  forecastSlug: string,
  ledger: PolicyEngineLedgerEntry[],
): ResolvedOutcome | undefined {
  const entry = getResolutionForForecast(forecastSlug);
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
  const resolution = getResolutionForForecast(forecast.slug);
  if (!resolution || !forecast.predictionDistribution) return undefined;

  const observation = getObservationForId(resolution.observationId, ledger);
  if (!observation) return undefined;

  const distributionScore = scoreNumericCdfDistribution(
    forecast.predictionDistribution,
    observation.value,
  );
  const signedError = observation.value - forecast.pointEstimate;
  const runId = buildRecordedPredictionRunId(forecast);
  const resolutionEventId = buildResolutionEventId(resolution);
  const scoringRule = "numeric_cdf_crps_v1";

  return {
    scoreId: `score.${runId}.${resolutionEventId}.${scoringRule}`,
    runId,
    resolutionEventId,
    scoringRule,
    ledgerFactRef: observation.dataPointId,
    forecastSlug: forecast.slug,
    dataPointId: resolution.dataPointId,
    observationId: observation.observationId,
    pointEstimate: forecast.pointEstimate,
    unit: observation.unit,
    signedError,
    absoluteError: Math.abs(signedError),
    interval80Covered:
      forecast.ciLow <= observation.value &&
      observation.value <= forecast.ciHigh,
    ...distributionScore,
  };
}

export function scoreResolvedForecasts(
  forecasts: ForecastCell[],
  ledger: PolicyEngineLedgerEntry[],
): ResolvedForecastScore[] {
  return forecasts.flatMap((forecast) => {
    const score = scoreResolvedForecast(forecast, ledger);
    return score ? [score] : [];
  });
}

export function withResolvedOutcome(
  forecast: ForecastCell,
  ledger: PolicyEngineLedgerEntry[],
): ForecastCell {
  return {
    ...forecast,
    resolvedOutcome:
      getResolvedOutcomeForForecast(forecast.slug, ledger) ??
      forecast.resolvedOutcome,
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

function buildStaticPayloadHash(value: unknown) {
  const serialized = JSON.stringify(value);
  let hash = 2166136261;
  for (let index = 0; index < serialized.length; index += 1) {
    hash ^= serialized.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return `static-hash-v1:${(hash >>> 0).toString(16).padStart(8, "0")}`;
}
