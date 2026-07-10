import { describe, expect, it } from "vitest";
import {
  classifyScoreChronology,
  scoreResolvedForecastRun,
  targetNormalizationScale,
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
  getForecastRunEntries,
  type ForecastCell,
} from "@/data/forecast-cells";
import type { TargetRegisteredLedgerEntry } from "@/data/ledger-targets";

// The two scoring-integrity invariants: a score enters the headline only
// when its run provably predates the observation, and its CRPS denominator
// is a target-level scale no run can influence by widening itself.

describe("chronology gate", () => {
  const observedAt = "2026-07-01T12:30:00Z";

  it("verifies runs recorded strictly before the observation", () => {
    expect(classifyScoreChronology("2026-06-28T09:00:00Z", observedAt)).toBe(
      "verified",
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
    // Strictly earlier UTC date: verified.
    expect(classifyScoreChronology("2026-06-28T09:00:00Z", "2026-07-01")).toBe(
      "verified",
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
      sourceKind: "official_release",
      source: "Test",
    };
  }

  const history = [
    observation("2022", 10, "2026-02-01T00:00:00Z"),
    observation("2023", 14, "2026-03-01T00:00:00Z"),
    observation("2024", 12, "2026-04-01T00:00:00Z"),
  ];
  const outcome = observation("2025", 3, "2026-05-01T00:00:00Z");

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
    // Young-ledger targets fall back to the frozen primary width — a
    // fixed, later-run-immune denominator — rather than dropping out.
    expect(score?.normalizationScaleSource).toBe("target_primary_width");
    expect(score?.normalizationScale).toBeCloseTo(
      Math.abs(baseCell.ciHigh - baseCell.ciLow) / 2.5631,
      6,
    );
    // With the frozen-primary-width tier the normalized metrics exist
    // and are computed against the shared target denominator.
    expect(score?.normalizedCrps).toEqual(expect.any(Number));
    expect(score?.normalizedAbsoluteError).toEqual(expect.any(Number));
    expect(score?.sharpness).toBeCloseTo(2.5631, 3);

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
    expect(primary?.reward.components.crps).toEqual(expect.any(Number));
    // Frozen-primary-width scores participate in rewards; only a truly
    // unavailable scale (no interval either) is excluded.
    expect(primary?.reward.components.normalizedCrps).toEqual(
      expect.any(Number),
    );
    expect(primary?.reward.value).toEqual(expect.any(Number));
    // Primary plus its F9 persistence baseline both score.
    expect(reward.counts.scoredRuns).toBe(2);
  });
});
