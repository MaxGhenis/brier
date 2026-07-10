import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import {
  buildScoreId,
  classifyScoreChronology,
  evaluateResolvedForecastRun,
  loadPolicyEngineLedger,
  scoreResolvedForecastRun,
  scoreResolvedForecasts,
  targetNormalizationScale,
  withResolvedOutcomes,
  type ObservationRecordedLedgerEntry,
  type PolicyEngineLedgerEntry,
} from "@/data/thesis-log";
import { SEEDED_RUN_RECORDED_AT } from "@/data/prediction-specs";
import {
  buildPredictionSpecs,
  buildRecordedPredictionRunRecords,
} from "@/data/prediction-specs";
import { buildBrierRewardExport } from "@/data/brier-lab";
import {
  FORECAST_CELLS,
  getForecastRunEntries,
  type ForecastCell,
} from "@/data/forecast-cells";
import type { TargetRegisteredLedgerEntry } from "@/data/ledger-targets";
import { WITNESSED_CUSTODY_ROOTS } from "@/data/witnessed-timeline";

// The two scoring-integrity invariants: a score enters the headline only
// when its run provably predates the observation, and its CRPS denominator
// is a target-level scale no run can influence by widening itself.

describe("chronology gate", () => {
  const observedAt = "2026-07-01T12:30:00Z";

  it("claimed-time-verifies runs recorded strictly before the observation", () => {
    // The claimed-time classifier can never award the headline tier by
    // itself: witness_verified additionally requires publication proof
    // from the witnessed timeline (re-audit N1).
    expect(classifyScoreChronology("2026-06-28T09:00:00Z", observedAt)).toBe(
      "claimed_time_verified",
    );
  });

  it("flags runs recorded at or after the observation as violated", () => {
    expect(classifyScoreChronology(observedAt, observedAt)).toBe("violated");
    expect(classifyScoreChronology("2026-07-02T00:00:00Z", observedAt)).toBe(
      "violated",
    );
  });

  it("treats missing, seeded, or unparseable run times as unverified", () => {
    expect(classifyScoreChronology(undefined, observedAt)).toBe("unverified");
    expect(classifyScoreChronology(SEEDED_RUN_RECORDED_AT, observedAt)).toBe(
      "unverified",
    );
    expect(classifyScoreChronology("not-a-date", observedAt)).toBe(
      "unverified",
    );
    expect(classifyScoreChronology("2026-06-28T09:00:00Z", undefined)).toBe(
      "unverified",
    );
  });

  it("rejects the seeded instant in any equivalent spelling (X4)", () => {
    // SEEDED_RUN_RECORDED_AT is 2026-06-08T00:00:00+02:00 == this UTC form.
    expect(classifyScoreChronology("2026-06-07T22:00:00Z", observedAt)).toBe(
      "unverified",
    );
    expect(
      classifyScoreChronology("2026-06-07T22:00:00.000Z", observedAt),
    ).toBe("unverified");
  });

  it("resolves date-only observations at day granularity (X4)", () => {
    // Strictly earlier UTC date: claimed-time verified.
    expect(classifyScoreChronology("2026-06-28T09:00:00Z", "2026-07-01")).toBe(
      "claimed_time_verified",
    );
    // Same UTC date: sub-day ordering unknowable in either direction.
    expect(classifyScoreChronology("2026-07-01T02:00:00Z", "2026-07-01")).toBe(
      "unverified",
    );
    expect(classifyScoreChronology("2026-07-01T23:59:00Z", "2026-07-01")).toBe(
      "unverified",
    );
    // Strictly later UTC date: violated.
    expect(classifyScoreChronology("2026-07-02T00:01:00Z", "2026-07-01")).toBe(
      "violated",
    );
  });
});

describe("target normalization scale", () => {
  // Any real custody root the public chain witnessed with a complete,
  // headline-eligible inventory before the fixture outcome below. The
  // fixture run carries it so normalization and pairing mechanics are
  // exercised at the witness-verified headline tier.
  const witnessedRootSha256 = Object.entries(WITNESSED_CUSTODY_ROOTS).find(
    ([, entry]) =>
      entry.inventoryStatus === "complete" &&
      entry.headlineEligible &&
      entry.earliestWitnessedAt < "2026-08-01T00:00:00Z",
  )?.[0];
  if (!witnessedRootSha256) {
    throw new Error(
      "expected a witnessed, headline-eligible custody root in the timeline",
    );
  }

  const baseCell: ForecastCell = {
    slug: "test-cell",
    country: "US",
    type: "data",
    title: "Test",
    question: "?",
    unit: "percent",
    pointEstimate: 2,
    ciLow: 1,
    ciHigh: 3,
    confidence: 0.8,
    resolutionDate: "2026-08-01",
    resolutionSource: "Test",
    resolutionRule: "Test",
    dataPointId: "census.spm.child_poverty_rate.2025",
    historicalContext: [],
    drivers: [],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-04-11T00:00:00Z",
      agent: "test.agent",
      model: "test-model",
      sourceContext: [],
      custodyRootSha256: witnessedRootSha256,
    },
    reasoning: [{ kind: "forecast", point: 2, ciLow: 1, ciHigh: 3 }],
  };

  const target: TargetRegisteredLedgerEntry = {
    kind: "target_registered",
    dataPointId: baseCell.dataPointId!,
    observationId: `obs.${baseCell.dataPointId}`,
    country: "US",
    periodLabel: "April 2026",
    unit: "percent",
    resolutionDate: baseCell.resolutionDate,
    resolutionSource: "Test",
    resolutionRule: "Test",
    resolutionPolicy: "first_print",
    sourceKind: "official_release",
    source: "Test",
    note: "fixture",
    registeredAt: "2026-04-10T00:00:00Z",
  };

  function observation(
    period: string,
    value: number,
    observedAt: string,
  ): ObservationRecordedLedgerEntry {
    const dataPointId = `census.spm.child_poverty_rate.${period}`;
    return {
      kind: "observation_recorded",
      observationId: `obs.${dataPointId}`,
      dataPointId,
      periodLabel: period,
      unit: "percent",
      value,
      observedAt,
      resolvedAt: observedAt,
      // Normalization history requires ledger acceptance at the cutoff.
      acceptedAtUtc: observedAt,
      sourceKind: "official_release",
      source: "Test",
    };
  }

  const history = [
    observation("2022", 10, "2026-02-01T00:00:00Z"),
    observation("2023", 14, "2026-03-01T00:00:00Z"),
    observation("2024", 12, "2026-04-01T00:00:00Z"),
  ];
  // Observed AFTER the custody root's external witness so publication
  // proof holds for the fixture score.
  const outcome = observation("2025", 3, "2026-08-01T12:00:00Z");

  it("derives the correct scale from pre-registration ledger dispersion", () => {
    const ledger: PolicyEngineLedgerEntry[] = [
      target,
      ...history,
      observation("2026", 1_000_000, "2026-04-10T00:00:01Z"),
    ];
    const { scale, source, observationCount } = targetNormalizationScale(
      baseCell,
      ledger,
    );
    expect(source).toBe("ledger_dispersion");
    expect(observationCount).toBe(3);
    // Ledger changes 4, -2 -> sample standard deviation sqrt(18).
    expect(scale).toBeCloseTo(Math.sqrt(18), 8);
  });

  it("ignores fabricated forecast history completely", () => {
    const honest = {
      ...baseCell,
      historicalContext: [
        { label: "t-3", value: 10 },
        { label: "t-2", value: 14 },
        { label: "t-1", value: 12 },
      ],
    };
    const fabricated = {
      ...baseCell,
      historicalContext: [
        { label: "t-3", value: -1_000_000 },
        { label: "t-2", value: 0 },
        { label: "t-1", value: 1_000_000 },
      ],
    };
    const ledger: PolicyEngineLedgerEntry[] = [target, ...history];
    expect(targetNormalizationScale(fabricated, ledger)).toEqual(
      targetNormalizationScale(honest, ledger),
    );
  });

  it("publishes raw CRPS but excludes an unavailable scale from rewards", () => {
    const ledger: PolicyEngineLedgerEntry[] = [
      target,
      ...history.slice(0, 2),
      outcome,
    ];
    const run = getForecastRunEntries(baseCell)[0];
    const score = scoreResolvedForecastRun(baseCell, run, ledger);
    expect(score?.crps).toEqual(expect.any(Number));
    // Young-ledger targets have NO independent scale. Nothing a forecast
    // authors may stand in as denominator (re-audit X2: the frozen
    // primary-width fallback let a wider interval shrink its own
    // normalized error), so the scale is simply unavailable.
    expect(score?.normalizationScaleSource).toBe("unavailable");
    expect(score?.normalizationScale).toBeNull();
    expect(score?.normalizedCrps).toBeNull();
    expect(score?.normalizedAbsoluteError).toBeNull();
    expect(score?.sharpness).toBeNull();

    const specs = buildPredictionSpecs([baseCell]);
    const runs = buildRecordedPredictionRunRecords([baseCell], specs);
    const reward = buildBrierRewardExport({
      forecasts: [baseCell],
      specs,
      runs,
      ledger,
    });
    const primary = reward.rewardRows.find(
      (row) => row.runVariantId === "primary",
    );
    // Raw CRPS publishes; normalized reward does not exist without an
    // independent scale.
    expect(primary?.reward.components.crps).toEqual(expect.any(Number));
    expect(primary?.reward.components.normalizedCrps).toBeNull();
    expect(primary?.reward.value).toBeNull();
    expect(primary?.scoreEligibility).toBe("scored_witness_verified");
    expect(reward.counts.scoredRuns).toBe(0);
    // Primary plus its F9 persistence baseline both carry raw scores, so
    // the scale-free paired comparison still works.
    expect(reward.counts.rawScoredRuns).toBe(2);
    expect(reward.pairedComparison.pairedTargets).toBe(1);
    expect(reward.pairedComparison.crpsRatioGeomean).toEqual(
      expect.any(Number),
    );
  });
});

describe("chronology parser is host-timezone independent (X4 residual)", () => {
  it("compares timezone-less timestamps at day granularity only", () => {
    // Same written day, no offset on the run time: sub-day order is
    // unknowable without trusting the build host's timezone.
    expect(
      classifyScoreChronology(
        "2026-07-01T02:00:00",
        "2026-07-01T12:30:00Z",
      ),
    ).toBe("unverified");
    // Strictly earlier written day still verifies at the claimed tier.
    expect(
      classifyScoreChronology(
        "2026-06-30T23:00:00",
        "2026-07-01T12:30:00Z",
      ),
    ).toBe("claimed_time_verified");
  });

  it("supports date-only run seals at day granularity", () => {
    expect(classifyScoreChronology("2026-06-28", "2026-07-01T00:00:00Z")).toBe(
      "claimed_time_verified",
    );
    expect(classifyScoreChronology("2026-07-01", "2026-07-01T23:00:00Z")).toBe(
      "unverified",
    );
    expect(classifyScoreChronology("2026-07-02", "2026-07-01T23:00:00Z")).toBe(
      "violated",
    );
  });
});

describe("resolution contract gate (N6)", () => {
  const cell: ForecastCell = {
    slug: "contract-cell",
    country: "US",
    type: "data",
    title: "Contract test",
    question: "?",
    unit: "thousands",
    pointEstimate: 220,
    ciLow: 200,
    ciHigh: 240,
    confidence: 0.8,
    resolutionDate: "2026-08-01",
    resolutionSource: "Test",
    resolutionRule: "Test",
    dataPointId: "test.contract.series.2026",
    historicalContext: [],
    drivers: [],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-04-11T00:00:00Z",
      agent: "test.agent",
      model: "test-model",
      sourceContext: [],
    },
    reasoning: [{ kind: "forecast", point: 220, ciLow: 200, ciHigh: 240 }],
  };
  const registered: TargetRegisteredLedgerEntry = {
    kind: "target_registered",
    dataPointId: cell.dataPointId!,
    observationId: `obs.${cell.dataPointId}`,
    country: "US",
    periodLabel: "2026",
    unit: "thousands",
    resolutionDate: cell.resolutionDate,
    resolutionSource: "Test",
    resolutionRule: "Test",
    resolutionPolicy: "first_print",
    sourceKind: "official_release",
    source: "Test",
    note: "fixture",
    registeredAt: "2026-04-10T00:00:00Z",
  };
  const fact = (
    overrides: Partial<ObservationRecordedLedgerEntry>,
  ): ObservationRecordedLedgerEntry => ({
    kind: "observation_recorded",
    observationId: `obs.${cell.dataPointId}`,
    dataPointId: cell.dataPointId!,
    periodLabel: "2026",
    unit: "thousands",
    value: 225,
    observedAt: "2026-07-20T12:00:00Z",
    resolvedAt: "2026-07-20T12:00:00Z",
    sourceKind: "official_release",
    source: "Test",
    ...overrides,
  });

  it("refuses to score a fact whose unit contradicts the contract", () => {
    const run = getForecastRunEntries(cell)[0];
    const evaluation = evaluateResolvedForecastRun(cell, run, [
      registered,
      fact({ unit: "millions" as ObservationRecordedLedgerEntry["unit"] }),
    ]);
    expect(evaluation.score).toBeUndefined();
    expect(evaluation.exclusion?.reason).toBe("contract_violation");
    expect(evaluation.exclusion?.detail).toContain("millions");
  });

  it("scores a contract-conforming fact", () => {
    const run = getForecastRunEntries(cell)[0];
    const evaluation = evaluateResolvedForecastRun(cell, run, [
      registered,
      fact({}),
    ]);
    expect(evaluation.score?.crps).toEqual(expect.any(Number));
    expect(evaluation.exclusion).toBeUndefined();
  });

  it("selects the first print by parsed instant, not string order", () => {
    // +05:00 noon is 07:00Z — EARLIER than 08:00Z despite sorting later
    // lexically. The parsed-instant rule must pick it.
    const later = fact({
      observationId: `obs.${cell.dataPointId}.a`,
      value: 300,
      observedAt: "2026-07-20T08:00:00Z",
    });
    const earlier = fact({
      observationId: `obs.${cell.dataPointId}.b`,
      value: 225,
      observedAt: "2026-07-20T12:00:00+05:00",
    });
    const run = getForecastRunEntries(cell)[0];
    const evaluation = evaluateResolvedForecastRun(cell, run, [
      registered,
      later,
      earlier,
    ]);
    expect(evaluation.score?.observedValue).toBe(225);
  });
});

describe("contract-bound resolution (fail closed past the quarantine)", () => {
  const cell: ForecastCell = {
    slug: "bound-cell",
    country: "US",
    type: "data",
    title: "Bound contract test",
    question: "?",
    unit: "thousands",
    pointEstimate: 220,
    ciLow: 200,
    ciHigh: 240,
    confidence: 0.8,
    resolutionDate: "2026-08-01",
    resolutionSource: "Test",
    resolutionRule: "Test",
    dataPointId: "test.bound.series.2026",
    historicalContext: [],
    drivers: [],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-04-11T00:00:00Z",
      agent: "test.agent",
      model: "test-model",
      sourceContext: [],
    },
    reasoning: [{ kind: "forecast", point: 220, ciLow: 200, ciHigh: 240 }],
  };
  const binding = {
    adapter: "alfred-fred" as const,
    sourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TEST",
    sourceSeriesId: "TEST",
    field: "TEST",
    table: "ALFRED graph CSV",
    transform: { operation: "multiply", factor: 0.001 },
    releasePolicy: "advance_vintage" as const,
    allowedHosts: ["alfred.stlouisfed.org"],
    expectedReleaseWindow: { start: "2026-07-15", end: "2026-07-25" },
  };
  const registered: TargetRegisteredLedgerEntry = {
    kind: "target_registered",
    dataPointId: cell.dataPointId!,
    observationId: `obs.${cell.dataPointId}`,
    country: "US",
    periodLabel: "2026",
    unit: "thousands",
    resolutionDate: cell.resolutionDate,
    resolutionSource: "Test",
    resolutionRule: "Test",
    resolutionPolicy: "first_print",
    sourceKind: "official_release",
    source: "Test",
    note: "fixture",
    registrationState: "preregistered",
    registeredAt: "2026-04-10T00:00:00Z",
    targetContentHash: "a".repeat(64),
    series: "test.bound.series",
    period: "2026",
    catalogSlug: cell.slug,
    valueScale: 0.001,
    sourceBinding: binding,
    ledgerPinSha: "b".repeat(40),
    ledgerPinLineCount: 107,
  };
  const responseSha256 = "c".repeat(64);
  const boundFact = (
    overrides: Partial<ObservationRecordedLedgerEntry>,
  ): ObservationRecordedLedgerEntry => ({
    kind: "observation_recorded",
    observationId: `obs.${cell.dataPointId}`,
    dataPointId: cell.dataPointId!,
    periodLabel: "2026",
    unit: "thousands",
    value: 225,
    observedAt: "2026-07-20T12:00:00Z",
    resolvedAt: "2026-07-20T12:00:00Z",
    acceptedSequence: 110,
    acceptedAtUtc: "2026-07-20T13:00:00Z",
    legacyQuarantined: false,
    sourceKind: "official_release",
    source: "Test",
    sourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TEST",
    targetContentHash: registered.targetContentHash,
    ledgerRepoSha: "d".repeat(40),
    sourceVintage: "2026-07-20",
    retrievedAt: "2026-07-20T12:30:00Z",
    responseArchive: {
      path: "records/resolutions/test/responses/test.csv.gz",
      sha256: responseSha256,
      bytes: 100,
      gzipSha256: "e".repeat(64),
      gzipBytes: 60,
      contentEncoding: "gzip",
    },
    sourceBindingProjection: {
      series: "test.bound.series",
      period: "2026",
      releasePolicy: "advance_vintage",
      table: "ALFRED graph CSV",
      field: "TEST",
      transform: { operation: "multiply", factor: 0.001 },
      unit: "thousands",
      responseSha256,
    },
    ...overrides,
  });
  const run = () => getForecastRunEntries(cell)[0];

  it("scores a fully bound post-quarantine observation as contract_bound", () => {
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      boundFact({}),
    ]);
    expect(evaluation.exclusion).toBeUndefined();
    expect(evaluation.score?.contractBinding).toBe("contract_bound");
  });

  it("rejects a projection whose series contradicts the registration", () => {
    // Finding 1: the projection's declared series is checked against the
    // registration, not merely against its own copy.
    const fact = boundFact({});
    fact.sourceBindingProjection = {
      ...fact.sourceBindingProjection!,
      series: "unrelated.other.series",
    };
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      fact,
    ]);
    expect(evaluation.exclusion?.reason).toBe("contract_violation");
    expect(evaluation.exclusion?.detail).toContain("series");
  });

  it("rejects an observation fetched from a non-allowed publisher host", () => {
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      boundFact({ sourceUrl: "https://evil.example.com/data.csv" }),
    ]);
    expect(evaluation.exclusion?.reason).toBe("contract_violation");
    expect(evaluation.exclusion?.detail).toContain("host");
  });

  it("rejects a post-quarantine observation with no contract hash", () => {
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      boundFact({ targetContentHash: undefined }),
    ]);
    expect(evaluation.exclusion?.reason).toBe("contract_violation");
    expect(evaluation.exclusion?.detail).toContain("no target contract hash");
  });

  it("rejects a post-quarantine observation missing the binding projection", () => {
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      boundFact({ sourceBindingProjection: undefined }),
    ]);
    expect(evaluation.exclusion?.reason).toBe("contract_violation");
    expect(evaluation.exclusion?.detail).toContain(
      "source-binding projection",
    );
  });

  it("rejects a projection that contradicts the registered binding", () => {
    const fact = boundFact({});
    fact.sourceBindingProjection = {
      ...fact.sourceBindingProjection!,
      transform: { operation: "multiply", factor: 1000 },
    };
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      fact,
    ]);
    expect(evaluation.exclusion?.reason).toBe("contract_violation");
    expect(evaluation.exclusion?.detail).toContain("transform");
  });

  it("rejects a projection whose digest is not the archived response", () => {
    const fact = boundFact({});
    fact.sourceBindingProjection = {
      ...fact.sourceBindingProjection!,
      responseSha256: "f".repeat(64),
    };
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      fact,
    ]);
    expect(evaluation.exclusion?.reason).toBe("contract_violation");
    expect(evaluation.exclusion?.detail).toContain("digest");
  });

  it("rejects a print that was already inside the pinned ledger state", () => {
    // The target was registered against a pinned 107-row state; a resolving
    // observation at sequence 50 predates the registration — a backfill
    // grading a pre-registered target (N5 by construction).
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      boundFact({ acceptedSequence: 50 }),
    ]);
    expect(evaluation.exclusion?.reason).toBe("contract_violation");
    expect(evaluation.exclusion?.detail).toContain("pinned ledger state");
  });

  it("keeps grading quarantined legacy rows, flagged legacy_unbound", () => {
    const evaluation = evaluateResolvedForecastRun(cell, run(), [
      registered,
      boundFact({
        legacyQuarantined: true,
        acceptedSequence: 12,
        targetContentHash: undefined,
        sourceBindingProjection: undefined,
        responseArchive: undefined,
        retrievedAt: undefined,
        ledgerRepoSha: undefined,
        sourceVintage: undefined,
      }),
    ]);
    expect(evaluation.exclusion).toBeUndefined();
    expect(evaluation.score?.contractBinding).toBe("legacy_unbound");
  });
});

describe("Supabase projection compatibility (N10)", () => {
  it("emits only sources the migration CHECK admits, with matching null shape", async () => {
    const migration = readFileSync(
      join(__dirname, "../../supabase/migrations/20260709_ledger_normalization_scale.sql"),
      "utf8",
    );
    expect(migration).toContain("'ledger_dispersion'");
    expect(migration).toContain("'unavailable'");
    expect(migration).not.toContain("target_primary_width");

    const ledger = await loadPolicyEngineLedger();
    const prepared = withResolvedOutcomes(FORECAST_CELLS, ledger);
    const scores = scoreResolvedForecasts(prepared, ledger);
    expect(scores.length).toBeGreaterThan(0);
    for (const score of scores) {
      // Mirrors scores_normalization_availability_check exactly: the
      // TypeScript projection must be row-for-row ingestible.
      expect(["ledger_dispersion", "unavailable"]).toContain(
        score.normalizationScaleSource,
      );
      if (score.normalizationScaleSource === "ledger_dispersion") {
        expect(score.normalizationScale).toEqual(expect.any(Number));
        expect(score.normalizedCrps).toEqual(expect.any(Number));
        expect(score.normalizedAbsoluteError).toEqual(expect.any(Number));
        expect(score.sharpness).toEqual(expect.any(Number));
      } else {
        expect(score.normalizationScale).toBeNull();
        expect(score.normalizedCrps).toBeNull();
        expect(score.normalizedAbsoluteError).toBeNull();
        expect(score.sharpness).toBeNull();
      }
    }
  }, 60_000);
});

describe("condition identity in score IDs (N7)", () => {
  it("changes the score ID when the gating premise differs", () => {
    const payload = {
      runId: "run.test",
      resolutionEventId: "resolution_event.test",
      scoringRule: "numeric_cdf_crps_v3_ledger_scale" as const,
      transformVersion: "interval_anchor_v1",
      forecastOutput: { pointEstimate: 1 },
      outcome: { observedValue: 1 },
      normalizationScale: 1,
      normalizationScaleSource: "ledger_dispersion",
      normalizationScaleCutoff: "2026-06-01T00:00:00Z",
      normalizationScaleObservationCount: 3,
      observedAt: "2026-07-01T00:00:00Z",
      chronology: "witness_verified",
      chronologyPolicy: "test",
      contractBinding: "contract_bound",
      contractBindingPolicy: "test",
      conditionId: "cond.a",
      conditionStatus: "satisfied",
    };
    expect(buildScoreId(payload)).not.toBe(
      buildScoreId({ ...payload, conditionId: "cond.b" }),
    );
    expect(buildScoreId(payload)).not.toBe(
      buildScoreId({ ...payload, conditionStatus: "failed" }),
    );
  });
});
