import { readFileSync } from "node:fs";
import { beforeAll, describe, expect, it } from "vitest";
import { AGENT_RUN_PREDICTION_SERIES } from "@/data/almanac-examples/agent-runs";
import { CANADA_AUSTRALIA_PREDICTION_SERIES } from "@/data/almanac-examples/canada-australia";
import { EURO_JAPAN_PREDICTION_SERIES } from "@/data/almanac-examples/euro-japan";
import { GLOBAL_NEAR_TERM_PREDICTION_SERIES } from "@/data/almanac-examples/global-near-term";
import { LAUNCH_PREDICTION_SERIES } from "@/data/almanac-examples/launch-cadence";
import { UK_PREDICTION_SERIES } from "@/data/almanac-examples/uk";
import { US_NEAR_TERM_PREDICTION_SERIES } from "@/data/almanac-examples/us-near-term";
import {
  FORECAST_CELLS,
  LIVE_FORECAST_SLUGS,
  getForecastCountry,
  getForecastRuntimeKind,
  getResolutionResult,
  type ForecastCell,
} from "@/data/forecast-cells";
import {
  buildPredictionSpecExport,
  buildPredictionSpecs,
  buildRecordedPredictionRunRecords,
} from "@/data/prediction-specs";
import {
  THESIS_LOG,
  buildPolicyEngineLedgerExport,
  buildResolutionQueue,
  buildThesisLog,
  buildThesisLogExport,
  getObservationForId,
  getObservationsForDataPoint,
  isObservationRecordedLedgerEntry,
  isPredictionRecordedLogEntry,
  isPredictionResolvedLogEntry,
  loadPolicyEngineLedger,
  scoreResolvedForecasts,
  withResolvedOutcomes,
  type ObservationRecordedLedgerEntry,
  type PolicyEngineLedgerEntry,
  type PredictionRecordedLogEntry,
  type PredictionResolvedLogEntry,
} from "@/data/thesis-log";

describe("forecast catalog", () => {
  let policyEngineLedger: PolicyEngineLedgerEntry[] = [];
  let resolvedForecastCells: ForecastCell[] = [];

  beforeAll(async () => {
    policyEngineLedger = await loadPolicyEngineLedger();
    resolvedForecastCells = withResolvedOutcomes(
      FORECAST_CELLS,
      policyEngineLedger,
    );
  });

  it("has unique slugs", () => {
    const slugs = FORECAST_CELLS.map((forecast) => forecast.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
  });

  it("has valid 80% intervals", () => {
    for (const forecast of FORECAST_CELLS) {
      expect(forecast.confidence).toBe(0.8);
      expect(forecast.ciLow).toBeLessThanOrEqual(forecast.pointEstimate);
      expect(forecast.pointEstimate).toBeLessThanOrEqual(forecast.ciHigh);
    }
  });

  it("exports a numeric CDF for every scalar prediction", () => {
    for (const forecast of FORECAST_CELLS) {
      const distribution = forecast.predictionDistribution;
      expect(distribution?.format).toBe("numeric_cdf_v1");
      expect(distribution?.pointCount).toBe(201);
      expect(distribution?.points).toHaveLength(201);
      expect(distribution?.summary.pointEstimate).toBe(forecast.pointEstimate);
      expect(distribution?.summary.median).toBe(forecast.pointEstimate);
      expect(distribution?.summary.interval80.lower).toBe(forecast.ciLow);
      expect(distribution?.summary.interval80.upper).toBe(forecast.ciHigh);
      expect(distribution?.points[0]?.probability).toBe(0);
      expect(distribution?.points.at(-1)?.probability).toBe(1);

      const points = distribution?.points ?? [];
      for (let index = 1; index < points.length; index += 1) {
        expect(points[index].value).toBeGreaterThan(points[index - 1].value);
        expect(points[index].probability).toBeGreaterThanOrEqual(
          points[index - 1].probability,
        );
      }
    }
  });

  it("builds a Thesis Log with one recorded prediction per forecast", () => {
    const log = buildThesisLog(FORECAST_CELLS);
    const recordedPredictions = log.filter(
      (entry): entry is PredictionRecordedLogEntry =>
        isPredictionRecordedLogEntry(entry),
    );

    expect(recordedPredictions).toHaveLength(FORECAST_CELLS.length);
    expect(
      new Set(recordedPredictions.map((entry) => entry.forecastSlug)).size,
    ).toBe(recordedPredictions.length);

    for (const entry of recordedPredictions) {
      const forecast = FORECAST_CELLS.find(
        (cell) => cell.slug === entry.forecastSlug,
      );
      expect(forecast).toBeTruthy();
      expect(entry.type).toBe(forecast?.type);
      expect(entry.title).toBe(forecast?.title);
      expect(entry.question).toBe(forecast?.question);
      expect(entry.country).toBe(forecast?.country ?? "US");
      expect(entry.unit).toBe(forecast?.unit);
      expect(entry.pointEstimate).toBe(forecast?.pointEstimate);
      expect(entry.interval80.lower).toBe(forecast?.ciLow);
      expect(entry.interval80.upper).toBe(forecast?.ciHigh);
      expect(entry.resolutionDate).toBe(forecast?.resolutionDate);
      expect(entry.resolutionSource).toBe(forecast?.resolutionSource);
      expect(entry.resolutionSourceUrl).toBe(forecast?.resolutionSourceUrl);
      expect(entry.resolutionRule).toBe(forecast?.resolutionRule);
      expect(entry.dataPointId).toBe(forecast?.dataPointId);
      expect(entry.distribution.format).toBe("numeric_cdf_v1");
      expect(entry.distribution.pointCount).toBe(201);
      expect(entry.distribution.summary.pointEstimate).toBe(
        forecast?.pointEstimate,
      );
      expect(entry.distribution.summary.interval80.lower).toBe(forecast?.ciLow);
      expect(entry.distribution.summary.interval80.upper).toBe(
        forecast?.ciHigh,
      );
    }
  });

  it("exports a normalized Thesis Log payload with scores and a resolution queue", () => {
    const exportPayload = buildThesisLogExport(
      resolvedForecastCells,
      policyEngineLedger,
    );
    const resolutionQueue = buildResolutionQueue(FORECAST_CELLS);

    expect(exportPayload.schemaVersion).toBe("thesis_log_v1");
    expect(exportPayload.source.name).toBe("Thesis Log");
    expect(exportPayload.source.url).toBe(
      "https://app.thesisinstitute.org/log",
    );
    expect(exportPayload.source.jsonUrl).toBe(
      "https://app.thesisinstitute.org/log.json",
    );
    expect(exportPayload.source.factLedger.name).toBe("PolicyEngine Ledger");
    expect(exportPayload.counts.predictions).toBe(FORECAST_CELLS.length);
    expect(exportPayload.counts.specs).toBe(FORECAST_CELLS.length);
    expect(exportPayload.counts.runs).toBe(FORECAST_CELLS.length);
    expect(exportPayload.counts.resolutions).toBeGreaterThan(0);
    expect(exportPayload.counts.resolutionLinks).toBe(FORECAST_CELLS.length);
    expect(exportPayload.counts.resolutionEvents).toBe(
      exportPayload.counts.resolutions,
    );
    expect(exportPayload.counts.scored).toBeGreaterThan(0);
    expect(exportPayload.counts.pendingResolution).toBe(resolutionQueue.length);
    expect(exportPayload.entries.some(isObservationRecordedLedgerEntry)).toBe(
      false,
    );
    expect(exportPayload.entries.length).toBeGreaterThan(FORECAST_CELLS.length);
    expect(exportPayload.specs).toHaveLength(exportPayload.counts.specs);
    expect(exportPayload.runs).toHaveLength(exportPayload.counts.runs);
    expect(exportPayload.runs[0].schemaVersion).toBe(
      "thesis_prediction_run_v1",
    );
    expect(exportPayload.resolutionLinks).toHaveLength(
      exportPayload.counts.resolutionLinks,
    );
    expect(exportPayload.resolutionEvents).toHaveLength(
      exportPayload.counts.resolutionEvents,
    );
    expect(exportPayload.resolutionLinks[0].resolutionRef).toMatch(
      /^resolution\./,
    );
    expect(exportPayload.resolutionEvents[0].resolutionEventId).toMatch(
      /^resolution_event\./,
    );
    expect(exportPayload.scores).toHaveLength(exportPayload.counts.scored);
    expect(exportPayload.resolutionQueue).toHaveLength(
      exportPayload.counts.pendingResolution,
    );

    for (let index = 1; index < resolutionQueue.length; index += 1) {
      expect(
        resolutionQueue[index].resolutionDate >=
          resolutionQueue[index - 1].resolutionDate,
      ).toBe(true);
    }
  });

  it("exports a facts-only PolicyEngine Ledger payload", () => {
    const exportPayload = buildPolicyEngineLedgerExport(policyEngineLedger);

    expect(exportPayload.schemaVersion).toBe("policyengine_ledger_v1");
    expect(exportPayload.source.name).toBe("PolicyEngine Ledger");
    expect(exportPayload.source.url).toBe(
      "https://github.com/PolicyEngine/arch-data",
    );
    expect(exportPayload.source.jsonMirrorUrl).toBe(
      "https://app.thesisinstitute.org/ledger.json",
    );
    expect(exportPayload.counts.facts).toBe(policyEngineLedger.length);
    expect(exportPayload.counts.observations).toBe(policyEngineLedger.length);
    expect(exportPayload.entries).toHaveLength(policyEngineLedger.length);
    expect(exportPayload.entries.every(isObservationRecordedLedgerEntry)).toBe(
      true,
    );
  });

  it("builds a production prediction spec for every forecast", () => {
    const exportPayload = buildPredictionSpecExport(FORECAST_CELLS);
    const specs = exportPayload.specs;

    expect(exportPayload.schemaVersion).toBe("thesis_prediction_specs_v1");
    expect(exportPayload.counts.specs).toBe(FORECAST_CELLS.length);
    expect(exportPayload.counts.withResolutionTarget).toBe(
      FORECAST_CELLS.filter((forecast) => forecast.dataPointId).length,
    );
    expect(specs).toHaveLength(FORECAST_CELLS.length);
    expect(new Set(specs.map((spec) => spec.predictionId)).size).toBe(
      specs.length,
    );
    expect(new Set(specs.map((spec) => spec.specId)).size).toBe(specs.length);
    expect(new Set(specs.map((spec) => spec.specVersionId)).size).toBe(
      specs.length,
    );

    for (const spec of specs) {
      const forecast = FORECAST_CELLS.find(
        (cell) => cell.slug === spec.predictionId,
      );
      expect(forecast).toBeTruthy();
      expect(spec.schemaVersion).toBe("thesis_prediction_spec_v1");
      expect(spec.specId).toBe(`spec.${spec.predictionId}`);
      expect(spec.specVersionId).toBe(`spec.${spec.predictionId}.v20260609`);
      expect(spec.specHash).toMatch(/^static-hash-v1:/);
      expect(spec.publishedAt).toBe("2026-06-09T00:00:00+02:00");
      expect(spec.question).toBe(forecast?.question);
      expect(spec.resolution.factLedger).toBe("PolicyEngine Ledger");
      expect(spec.resolution.expectedAt).toBe(forecast?.resolutionDate);
      expect(spec.resolution.targetFactRef).toBe(forecast?.dataPointId);
      expect("factId" in spec.resolution).toBe(false);
      expect(spec.distribution.format).toBe("numeric_cdf_v1");
      expect(spec.distribution.pointCount).toBe(201);
      expect(spec.distribution.elicitation).toBe("full_cdf");
      expect(spec.tools.allowed).toContain("distribution.validate");
      expect(spec.tools.required).toContain("thesis-log.write");
      expect(spec.agent.publicTraceOnly).toBe(true);
      expect(spec.qualityGates).toContain("resolution_source_defined");
    }
  });

  it("builds immutable run records from prediction specs", () => {
    const specs = buildPredictionSpecs(resolvedForecastCells);
    const runs = buildRecordedPredictionRunRecords(
      resolvedForecastCells,
      specs,
    );

    expect(runs).toHaveLength(resolvedForecastCells.length);
    expect(new Set(runs.map((run) => run.runId)).size).toBe(runs.length);

    for (const run of runs) {
      const forecast = resolvedForecastCells.find(
        (cell) => cell.slug === run.predictionId,
      );
      expect(forecast).toBeTruthy();
      expect(run.schemaVersion).toBe("thesis_prediction_run_v1");
      expect(run.runner.id).toBe("thesis.recorded-agent-runner");
      expect(run.runId).toMatch(/^run\./);
      expect(run.specId).toBe(`spec.${run.predictionId}`);
      expect(run.specVersionId).toBe(`spec.${run.predictionId}.v20260609`);
      expect(run.agentId).toMatch(/^agent\./);
      expect(run.idempotencyKey).toMatch(/^static-hash-v1:/);
      expect(run.createdAt).toMatch(/^2026-/);
      expect(run.promptHash).toMatch(/^static-hash-v1:/);
      expect(run.toolPolicyHash).toMatch(/^static-hash-v1:/);
      expect(run.inputBundleHash).toMatch(/^static-hash-v1:/);
      expect(run.status).toBe("published");
      expect(run.input.specId).toBe(run.specId);
      expect(run.input.specVersionId).toBe(run.specVersionId);
      expect(run.input.targetFactRef).toBe(forecast?.dataPointId);
      expect(run.input.allowedTools).toContain("distribution.validate");
      expect(run.output.distribution.format).toBe("numeric_cdf_v1");
      expect(run.output.distribution.pointCount).toBe(201);
      expect(run.output.publicTrace.length).toBeGreaterThanOrEqual(3);
      expect(run.output.publicTraceMetadata.redactionStatus).toBe(
        "public_only",
      );
      expect(run.output.publicTraceMetadata.traceHash).toMatch(
        /^static-hash-v1:/,
      );
      for (const toolCall of run.output.toolCalls) {
        expect(toolCall.toolCallId).toMatch(/^run\..+\.tool\.[0-9]+$/);
        expect(toolCall.allowedTool).toBe(true);
        expect(toolCall.requestHash).toMatch(/^static-hash-v1:/);
        expect(toolCall.responseHash).toMatch(/^static-hash-v1:/);
      }
      expect(run.qualityGates.some((gate) => gate.status === "failed")).toBe(
        false,
      );
      expect(run.resolution.factLedger).toBe("PolicyEngine Ledger");
      expect(run.resolution.resolutionRef).toBe(
        `resolution.${run.predictionId}`,
      );
      expect(run.resolution.targetFactRef).toBe(forecast?.dataPointId);
    }
  });

  it("defines the first normalized Supabase tables for Thesis Log", () => {
    const sql = readFileSync(
      `${process.cwd()}/supabase/migrations/20260609_thesis_log.sql`,
      "utf8",
    );
    const tableNames = [
      "prediction_specs",
      "spec_versions",
      "prediction_runs",
      "cdf_points",
      "public_traces",
      "tool_calls",
      "resolution_links",
      "resolution_events",
      "scores",
      "quality_gate_results",
      "audit_events",
    ];

    for (const tableName of tableNames) {
      expect(sql).toContain(`create table if not exists ${tableName}`);
      expect(sql).toContain(
        `alter table ${tableName} enable row level security`,
      );
    }
    expect(sql).toContain(
      "unique (spec_version_id, agent_id, idempotency_key)",
    );
    expect(sql).toContain("unique (run_id, artifact_type)");
    expect(sql).toContain("confidence_mass_check_status");
    expect(sql).toContain("thesis_prevent_update_delete");
    expect(sql).toContain("previous_event_hash");
    expect(sql).toContain("event_hash text not null unique");
  });

  it("has enough public context to stand alone", () => {
    for (const forecast of FORECAST_CELLS) {
      expect(forecast.question.length).toBeGreaterThan(40);
      expect(forecast.resolutionRule.length).toBeGreaterThan(60);
      expect(forecast.drivers.length).toBeGreaterThanOrEqual(3);
      expect(forecast.reasoning.length).toBeGreaterThanOrEqual(5);
    }
  });

  it("uses prediction language in user-facing forecast labels", () => {
    for (const forecast of FORECAST_CELLS) {
      expect(forecast.title).not.toMatch(/\bmarkets?\b/i);
      expect(forecast.question).not.toMatch(/\bmarkets?\b/i);
    }
  });

  it("only marks known forecast cells as live API paths", () => {
    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    for (const slug of LIVE_FORECAST_SLUGS) {
      expect(slugs.has(slug)).toBe(true);
    }
  });

  it("uses public data point terminology for government data forecasts", () => {
    for (const forecast of FORECAST_CELLS) {
      if (forecast.type === "data") {
        expect(forecast.dataPointId).toBeTruthy();
      }
    }
  });

  it("classifies every prediction by country", () => {
    for (const forecast of FORECAST_CELLS) {
      expect(getForecastCountry(forecast)).toMatch(/US|UK|CA|AU|EA|JP/);
    }
  });

  it("prioritizes near-term 2025 Census release targets", () => {
    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("spm-child-poverty-2025")).toBe(true);
    expect(LIVE_FORECAST_SLUGS.has("spm-child-poverty-2025")).toBe(true);
    expect(slugs.has("spm-poverty-rate-2025")).toBe(true);
    expect(slugs.has("official-poverty-rate-2025")).toBe(true);
    expect(slugs.has("median-household-income-2025")).toBe(true);
    expect(slugs.has("federal-spm-poverty-rate-2026")).toBe(false);
  });

  it("includes near-term calibration examples across tax, health, and benefits", () => {
    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("individual-income-tax-refunds-fy2026")).toBe(true);
    expect(slugs.has("net-premium-tax-credit-reconciliation-ty2025")).toBe(
      true,
    );
    expect(slugs.has("savers-credit-claimant-returns-ty2025")).toBe(true);
    expect(slugs.has("medicaid-chip-enrollment-dec-2026")).toBe(true);
    expect(slugs.has("direct-purchase-health-coverage-rate-2025")).toBe(true);
    expect(slugs.has("marketplace-new-consumers-oep-2027")).toBe(true);
    expect(slugs.has("infant-mortality-rate-2026-current-law")).toBe(true);
    expect(slugs.has("infant-mortality-rate-2026-ctc-3000-refundable")).toBe(
      true,
    );
    expect(slugs.has("snap-cumulative-benefit-redemptions-fy2026")).toBe(true);
    expect(slugs.has("wic-child-participation-fy2026")).toBe(true);
    expect(slugs.has("ccdf-average-monthly-payment-per-child-fy2026")).toBe(
      true,
    );
  });

  it("includes high-cadence launch examples from the working indicator slate", () => {
    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("initial-jobless-claims-week-ending-2026-06-06")).toBe(
      true,
    );
    expect(slugs.has("nonfarm-payrolls-may-2026")).toBe(true);
    expect(slugs.has("unemployment-rate-may-2026-first-print")).toBe(true);
    expect(slugs.has("cpi-headline-mom-may-2026")).toBe(true);
    expect(slugs.has("retail-sales-mom-may-2026")).toBe(true);
    expect(slugs.has("us-capacity-utilization-may-2026")).toBe(true);
    expect(slugs.has("us-government-social-benefits-may-2026")).toBe(true);
    expect(slugs.has("us-social-security-benefits-may-2026")).toBe(true);
    expect(slugs.has("us-medicare-benefits-may-2026")).toBe(true);
    expect(slugs.has("us-medicaid-benefits-may-2026")).toBe(true);
    expect(slugs.has("us-wages-and-salaries-may-2026")).toBe(true);
    expect(slugs.has("us-personal-current-taxes-may-2026")).toBe(true);
    expect(slugs.has("us-disposable-personal-income-may-2026")).toBe(true);
    expect(slugs.has("core-pce-mom-may-2026")).toBe(true);
    expect(slugs.has("snap-participation-april-2026")).toBe(true);
    expect(slugs.has("medicaid-chip-enrollment-april-2026")).toBe(true);
  });

  it("carries official source URLs into the resolution queue when available", () => {
    const queue = buildResolutionQueue(FORECAST_CELLS);
    const capacityUtilization = queue.find(
      (entry) => entry.forecastSlug === "us-capacity-utilization-may-2026",
    );
    const governmentBenefits = queue.find(
      (entry) =>
        entry.forecastSlug === "us-government-social-benefits-may-2026",
    );

    expect(capacityUtilization?.resolutionSourceUrl).toBe(
      "https://www.federalreserve.gov/releases/g17/current/default.htm",
    );
    expect(governmentBenefits?.resolutionSourceUrl).toBe(
      "https://www.bea.gov/data/income-saving/personal-income",
    );
  });

  it("generates launch cells from structured prediction series", () => {
    expect(LAUNCH_PREDICTION_SERIES.length).toBeGreaterThanOrEqual(8);

    const launchSeriesIds = new Set(
      LAUNCH_PREDICTION_SERIES.map((series) => series.seriesId),
    );
    const launchCells = FORECAST_CELLS.filter(
      (forecast) =>
        forecast.series && launchSeriesIds.has(forecast.series.seriesId),
    );

    expect(launchCells.length).toBeGreaterThanOrEqual(
      LAUNCH_PREDICTION_SERIES.length,
    );
    for (const forecast of launchCells) {
      expect(forecast.series?.cadence).toMatch(/weekly|monthly/);
      expect(forecast.series?.horizon).toMatch(/next_release|plus_3m/);
      expect(forecast.series?.resolutionPolicy).toMatch(
        /first_print|fixed_vintage/,
      );
      expect(forecast.series?.chainableQuestions.length).toBeGreaterThan(1);
    }
  });

  it("includes agent-run predictions across indicators and policy settings", () => {
    expect(AGENT_RUN_PREDICTION_SERIES.length).toBeGreaterThanOrEqual(10);

    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("average-hourly-earnings-mom-may-2026")).toBe(true);
    expect(slugs.has("core-cpi-mom-may-2026")).toBe(true);
    expect(slugs.has("jolts-job-openings-may-2026")).toBe(true);
    expect(slugs.has("snap-participation-march-2026")).toBe(true);
    expect(slugs.has("wic-total-participation-march-2026")).toBe(true);
    expect(slugs.has("medicaid-chip-enrollment-march-2026")).toBe(true);
    expect(slugs.has("irs-total-refunds-october-2026")).toBe(true);
    expect(slugs.has("snap-max-allotment-four-person-fy2027")).toBe(true);
    expect(slugs.has("hhs-poverty-guideline-family-four-2027")).toBe(true);
    expect(slugs.has("ctc-maximum-per-child-ty2027")).toBe(true);

    const policySettings = FORECAST_CELLS.filter((forecast) =>
      forecast.series
        ? AGENT_RUN_PREDICTION_SERIES.some(
            (series) =>
              series.seriesId === forecast.series?.seriesId &&
              series.type === "policy",
          )
        : false,
    );
    expect(policySettings.length).toBeGreaterThanOrEqual(3);
    for (const forecast of policySettings) {
      expect(forecast.type).toBe("policy");
      expect(forecast.policyParameter).toBeTruthy();
      expect(forecast.series?.horizon).toMatch(/threshold|next_release/);
    }
  });

  it("includes quick-resolution UK indicators", () => {
    expect(UK_PREDICTION_SERIES.length).toBeGreaterThanOrEqual(7);

    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("uk-monthly-gdp-growth-april-2026")).toBe(true);
    expect(slugs.has("uk-cpi-annual-rate-may-2026")).toBe(true);
    expect(slugs.has("uk-unemployment-rate-feb-apr-2026")).toBe(true);
    expect(slugs.has("uk-paye-payrolled-employees-may-2026")).toBe(true);
    expect(slugs.has("uk-retail-sales-volume-mom-may-2026")).toBe(true);
    expect(slugs.has("uk-public-sector-net-borrowing-may-2026")).toBe(true);
    expect(slugs.has("uk-bank-rate-june-2026-mpc")).toBe(true);

    const ukSeriesIds = new Set(
      UK_PREDICTION_SERIES.map((series) => series.seriesId),
    );
    const ukCells = FORECAST_CELLS.filter(
      (forecast) =>
        forecast.series && ukSeriesIds.has(forecast.series.seriesId),
    );
    expect(ukCells.length).toBeGreaterThanOrEqual(UK_PREDICTION_SERIES.length);
    for (const forecast of ukCells) {
      expect(forecast.resolutionDate).toMatch(/^2026-06-/);
      expect(getForecastCountry(forecast)).toBe("UK");
      expect(forecast.predictionRun?.kind).toBe("recorded-agent-run");
      expect(getForecastRuntimeKind(forecast)).toBe("agent-run");
      expect(forecast.series?.source).toMatch(
        /Office for National Statistics|Bank of England|HMRC/,
      );
    }
  });

  it("includes quick-resolution Canada and Australia indicators", () => {
    expect(CANADA_AUSTRALIA_PREDICTION_SERIES.length).toBeGreaterThanOrEqual(9);

    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("canada-unemployment-rate-may-2026")).toBe(true);
    expect(slugs.has("canada-employment-change-may-2026")).toBe(true);
    expect(slugs.has("canada-cpi-annual-rate-may-2026")).toBe(true);
    expect(slugs.has("canada-monthly-gdp-growth-april-2026")).toBe(true);
    expect(slugs.has("canada-overnight-rate-june-2026-boc")).toBe(true);
    expect(slugs.has("australia-unemployment-rate-may-2026")).toBe(true);
    expect(slugs.has("australia-employment-change-may-2026")).toBe(true);
    expect(slugs.has("australia-cpi-annual-rate-may-2026")).toBe(true);
    expect(slugs.has("australia-cash-rate-june-2026-rba")).toBe(true);

    const internationalSeriesIds = new Set(
      CANADA_AUSTRALIA_PREDICTION_SERIES.map((series) => series.seriesId),
    );
    const internationalCells = FORECAST_CELLS.filter(
      (forecast) =>
        forecast.series && internationalSeriesIds.has(forecast.series.seriesId),
    );
    expect(internationalCells.length).toBeGreaterThanOrEqual(
      CANADA_AUSTRALIA_PREDICTION_SERIES.length,
    );
    for (const forecast of internationalCells) {
      expect(forecast.resolutionDate).toMatch(/^2026-06-/);
      expect(["CA", "AU"]).toContain(getForecastCountry(forecast));
      expect(forecast.predictionRun?.kind).toBe("recorded-agent-run");
      expect(getForecastRuntimeKind(forecast)).toBe("agent-run");
      expect(forecast.series?.source).toMatch(
        /Statistics Canada|Bank of Canada|Australian Bureau of Statistics|Reserve Bank of Australia/,
      );
    }
  });

  it("includes quick-resolution euro area and Japan indicators", () => {
    expect(EURO_JAPAN_PREDICTION_SERIES.length).toBeGreaterThanOrEqual(7);

    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("euro-area-ecb-deposit-facility-rate-june-2026")).toBe(
      true,
    );
    expect(slugs.has("euro-area-hicp-annual-rate-may-2026-final")).toBe(true);
    expect(slugs.has("euro-area-hicp-annual-rate-june-2026-flash")).toBe(true);
    expect(slugs.has("euro-area-unemployment-rate-may-2026")).toBe(true);
    expect(slugs.has("japan-boj-policy-rate-june-2026")).toBe(true);
    expect(slugs.has("japan-cpi-annual-rate-may-2026")).toBe(true);
    expect(slugs.has("japan-tokyo-cpi-annual-rate-june-2026-prelim")).toBe(
      true,
    );
    expect(slugs.has("japan-unemployment-rate-may-2026")).toBe(true);

    const seriesIds = new Set(
      EURO_JAPAN_PREDICTION_SERIES.map((series) => series.seriesId),
    );
    const cells = FORECAST_CELLS.filter(
      (forecast) => forecast.series && seriesIds.has(forecast.series.seriesId),
    );
    expect(cells.length).toBeGreaterThanOrEqual(
      EURO_JAPAN_PREDICTION_SERIES.length,
    );
    for (const forecast of cells) {
      expect(forecast.resolutionDate).toMatch(/^2026-0[67]-/);
      expect(["EA", "JP"]).toContain(getForecastCountry(forecast));
      expect(forecast.predictionRun?.kind).toBe("recorded-agent-run");
      expect(getForecastRuntimeKind(forecast)).toBe("agent-run");
      expect(forecast.series?.source).toMatch(
        /European Central Bank|Eurostat|Bank of Japan|Statistics Bureau of Japan/,
      );
    }
  });

  it("includes additional near-term US official-data indicators", () => {
    expect(US_NEAR_TERM_PREDICTION_SERIES.length).toBeGreaterThanOrEqual(8);

    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("us-ppi-final-demand-mom-may-2026")).toBe(true);
    expect(slugs.has("us-industrial-production-mom-may-2026")).toBe(true);
    expect(slugs.has("us-import-price-index-mom-may-2026")).toBe(true);
    expect(slugs.has("us-housing-starts-may-2026")).toBe(true);
    expect(slugs.has("us-total-business-inventories-april-2026")).toBe(true);
    expect(slugs.has("us-pce-price-index-mom-may-2026")).toBe(true);
    expect(slugs.has("us-real-gdp-q1-2026-third-estimate")).toBe(true);
    expect(slugs.has("us-mts-deficit-may-2026")).toBe(true);

    const seriesIds = new Set(
      US_NEAR_TERM_PREDICTION_SERIES.map((series) => series.seriesId),
    );
    const cells = FORECAST_CELLS.filter(
      (forecast) => forecast.series && seriesIds.has(forecast.series.seriesId),
    );
    expect(cells.length).toBe(US_NEAR_TERM_PREDICTION_SERIES.length);
    for (const forecast of cells) {
      expect(getForecastCountry(forecast)).toBe("US");
      expect(forecast.predictionRun?.kind).toBe("recorded-agent-run");
      expect(getForecastRuntimeKind(forecast)).toBe("agent-run");
    }
  });

  it("includes additional near-term international official-data indicators", () => {
    expect(GLOBAL_NEAR_TERM_PREDICTION_SERIES.length).toBeGreaterThanOrEqual(8);

    const slugs = new Set(FORECAST_CELLS.map((forecast) => forecast.slug));
    expect(slugs.has("canada-retail-sales-growth-april-2026")).toBe(true);
    expect(slugs.has("canada-wholesale-sales-growth-april-2026")).toBe(true);
    expect(slugs.has("canada-ei-regular-beneficiaries-april-2026")).toBe(true);
    expect(slugs.has("canada-building-permit-value-growth-april-2026")).toBe(
      true,
    );
    expect(slugs.has("euro-area-industrial-production-growth-april-2026")).toBe(
      true,
    );
    expect(slugs.has("euro-area-retail-trade-volume-growth-may-2026")).toBe(
      true,
    );
    expect(slugs.has("australia-dwelling-approvals-growth-may-2026")).toBe(
      true,
    );
    expect(slugs.has("japan-real-household-spending-growth-may-2026")).toBe(
      true,
    );

    const seriesIds = new Set(
      GLOBAL_NEAR_TERM_PREDICTION_SERIES.map((series) => series.seriesId),
    );
    const cells = FORECAST_CELLS.filter(
      (forecast) => forecast.series && seriesIds.has(forecast.series.seriesId),
    );
    expect(cells.length).toBe(GLOBAL_NEAR_TERM_PREDICTION_SERIES.length);
    for (const forecast of cells) {
      expect(["CA", "AU", "EA", "JP"]).toContain(getForecastCountry(forecast));
      expect(forecast.predictionRun?.kind).toBe("recorded-agent-run");
      expect(getForecastRuntimeKind(forecast)).toBe("agent-run");
    }
  });

  it("records official outcomes for resolved labor-market predictions", () => {
    const forecastsBySlug = new Map(
      resolvedForecastCells.map((forecast) => [forecast.slug, forecast]),
    );
    const resolutionEntries = THESIS_LOG.filter(
      (entry): entry is PredictionResolvedLogEntry =>
        isPredictionResolvedLogEntry(entry),
    );
    const observationEntries = policyEngineLedger.filter(
      (entry): entry is ObservationRecordedLedgerEntry =>
        isObservationRecordedLedgerEntry(entry),
    );
    const resolutionSlugs = resolutionEntries.map(
      (entry) => entry.forecastSlug,
    );
    expect(new Set(resolutionSlugs).size).toBe(resolutionSlugs.length);
    expect(
      new Set(observationEntries.map((entry) => entry.observationId)).size,
    ).toBe(observationEntries.length);

    const resolvedPredictions = [
      {
        slug: "nonfarm-payrolls-may-2026",
        dataPointId:
          "bls.ces.total_nonfarm_payroll_change.may_2026.first_print",
        value: 172,
        unit: "thousands",
        result: "inside",
        source: /Bureau of Labor Statistics/,
      },
      {
        slug: "unemployment-rate-may-2026-first-print",
        dataPointId: "bls.cps.unemployment_rate.may_2026.first_print",
        value: 4.3,
        unit: "percent",
        result: "inside",
        source: /Bureau of Labor Statistics/,
      },
      {
        slug: "average-hourly-earnings-mom-may-2026",
        dataPointId:
          "bls.ces.average_hourly_earnings_private.may_2026.first_print",
        value: 0.3,
        unit: "percent_growth",
        result: "inside",
        source: /Bureau of Labor Statistics/,
      },
      {
        slug: "canada-unemployment-rate-may-2026",
        dataPointId:
          "statcan.lfs.unemployment_rate.canada.may_2026.first_print",
        value: 6.6,
        unit: "percent",
        result: "outside",
        source: /Statistics Canada/,
      },
      {
        slug: "canada-employment-change-may-2026",
        dataPointId:
          "statcan.lfs.employment_change.canada.may_2026.first_print",
        value: 88,
        unit: "thousands",
        result: "outside",
        source: /Statistics Canada/,
      },
    ] as const;

    for (const expected of resolvedPredictions) {
      const forecast = forecastsBySlug.get(expected.slug);
      const logEntry = resolutionEntries.find(
        (entry) => entry.forecastSlug === expected.slug,
      );
      expect(logEntry?.dataPointId).toBe(expected.dataPointId);
      const observation = logEntry
        ? getObservationForId(logEntry.observationId, policyEngineLedger)
        : undefined;
      expect(observation?.sourceKind).toBe("official_release");
      expect(observation?.dataPointId).toBe(expected.dataPointId);
      expect(observation?.value).toBe(expected.value);
      expect(observation?.unit).toBe(expected.unit);
      expect(
        getObservationsForDataPoint(
          expected.dataPointId,
          policyEngineLedger,
        ).map((entry) => entry.observationId),
      ).toContain(observation?.observationId);
      expect(forecast).toBeTruthy();
      expect(forecast?.resolvedOutcome?.value).toBe(expected.value);
      expect(forecast?.resolvedOutcome?.resolvedAt).toBe("2026-06-05");
      expect(forecast?.resolvedOutcome?.source).toMatch(expected.source);
      expect(forecast?.resolvedOutcome?.sourceUrl).toMatch(/^https:\/\//);
      expect(getResolutionResult(forecast!)).toBe(expected.result);
    }

    const scores = scoreResolvedForecasts(
      resolvedForecastCells,
      policyEngineLedger,
    );
    expect(scores).toHaveLength(resolvedPredictions.length);

    for (const expected of resolvedPredictions) {
      const score = scores.find(
        (entry) => entry.forecastSlug === expected.slug,
      );
      expect(score?.dataPointId).toBe(expected.dataPointId);
      expect(score?.ledgerFactRef).toBe(expected.dataPointId);
      expect(score?.runId).toMatch(/^run\./);
      expect(score?.resolutionEventId).toMatch(/^resolution_event\./);
      expect(score?.scoreId).toMatch(/^score\.run\./);
      expect(score?.scoringRule).toBe("numeric_cdf_crps_v1");
      if (score) expect("observedValue" in score).toBe(false);
      expect(score?.unit).toBe(expected.unit);
      expect(score?.absoluteError).toBeGreaterThanOrEqual(0);
      expect(score?.crps).toBeGreaterThanOrEqual(0);
      expect(score?.probabilityIntegralTransform).toBeGreaterThanOrEqual(0);
      expect(score?.probabilityIntegralTransform).toBeLessThanOrEqual(1);
      expect(score?.interval80Covered).toBe(expected.result === "inside");
    }
  });
});
