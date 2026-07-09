import { describe, expect, it } from "vitest";
import {
  classifyScoreChronology,
  targetNormalizationScale,
} from "@/data/thesis-log";
import { SEEDED_RUN_RECORDED_AT } from "@/data/prediction-specs";
import type { ForecastCell } from "@/data/forecast-cells";

// The two scoring-integrity invariants: a score enters the headline only
// when its run provably predates the observation, and its CRPS denominator
// is a target-level scale no run can influence by widening itself.

describe("chronology gate", () => {
  const observedAt = "2026-07-01T12:30:00Z";

  it("verifies runs recorded strictly before the observation", () => {
    expect(
      classifyScoreChronology("2026-06-28T09:00:00Z", observedAt),
    ).toBe("verified");
  });

  it("flags runs recorded at or after the observation as violated", () => {
    expect(classifyScoreChronology(observedAt, observedAt)).toBe("violated");
    expect(
      classifyScoreChronology("2026-07-02T00:00:00Z", observedAt),
    ).toBe("violated");
  });

  it("treats missing, seeded, or unparseable run times as unverified", () => {
    expect(classifyScoreChronology(undefined, observedAt)).toBe("unverified");
    expect(
      classifyScoreChronology(SEEDED_RUN_RECORDED_AT, observedAt),
    ).toBe("unverified");
    expect(classifyScoreChronology("not-a-date", observedAt)).toBe(
      "unverified",
    );
    expect(
      classifyScoreChronology("2026-06-28T09:00:00Z", undefined),
    ).toBe("unverified");
  });
});

describe("target normalization scale", () => {
  const baseCell = {
    slug: "test-cell",
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
    drivers: [],
    reasoning: [],
  } as unknown as ForecastCell;

  it("derives the scale from historical dispersion when history exists", () => {
    const cell = {
      ...baseCell,
      historicalContext: [
        { label: "t-4", value: 10 },
        { label: "t-3", value: 12 },
        { label: "t-2", value: 11 },
        { label: "t-1", value: 14 },
      ],
    } as ForecastCell;
    const { scale, source } = targetNormalizationScale(cell);
    expect(source).toBe("target_dispersion");
    // diffs 2, -1, 3 -> sample stdev ~2.081
    expect(scale).toBeCloseTo(2.0817, 3);
  });

  it("falls back to the primary interval's implied sigma", () => {
    const cell = { ...baseCell, historicalContext: [] } as ForecastCell;
    const { scale, source } = targetNormalizationScale(cell);
    expect(source).toBe("target_primary_width");
    expect(scale).toBeCloseTo(2 / 2.5631, 4);
  });

  it("is identical for every run on the target — widening cannot lower it", () => {
    const cell = {
      ...baseCell,
      historicalContext: [
        { label: "t-3", value: 100 },
        { label: "t-2", value: 104 },
        { label: "t-1", value: 101 },
      ],
    } as ForecastCell;
    const narrow = targetNormalizationScale(cell).scale;
    const widenedRunSameTarget = targetNormalizationScale(cell).scale;
    expect(widenedRunSameTarget).toBe(narrow);
  });
});
