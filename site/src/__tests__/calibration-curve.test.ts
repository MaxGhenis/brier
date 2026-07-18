import { describe, expect, it } from "vitest";
import {
  COVERAGE_LEVELS,
  coverageCurve,
  pitHistogram,
} from "@/data/calibration-curve";

describe("coverageCurve", () => {
  it("recovers nominal coverage exactly for evenly spread PITs", () => {
    // 99 PITs at 0.01..0.99: the central interval of width c contains
    // round(99 * c) of them, so empirical coverage tracks nominal within
    // one grid step at every level.
    const pits = Array.from({ length: 99 }, (_, i) => (i + 1) / 100);
    for (const point of coverageCurve(pits)) {
      expect(point.n).toBe(99);
      // Exact set-counting on a 1/100 grid lands within two grid steps of
      // the nominal level everywhere.
      expect(Math.abs(point.empirical - point.nominal)).toBeLessThan(0.02);
    }
  });

  it("flags underdispersion and overdispersion asymmetrically", () => {
    // Every outcome at the median: intervals were far too wide — full
    // coverage at every nominal level.
    const central = coverageCurve([0.5, 0.5, 0.5, 0.5]);
    for (const point of central) expect(point.empirical).toBe(1);

    // Every outcome in the far tails: intervals were far too narrow —
    // zero coverage until the interval nearly spans the unit range.
    const tails = coverageCurve([0.005, 0.995, 0.002, 0.998]);
    for (const point of tails) {
      if (point.nominal <= 0.95) expect(point.empirical).toBe(0);
    }
  });

  it("counts the elicited 80% interval like the headline coverage stat", () => {
    // PIT inside [0.1, 0.9] is exactly "inside the stated 80% interval".
    const points = coverageCurve([0.09, 0.1, 0.5, 0.9, 0.91]);
    const eighty = points.find((point) => point.nominal === 0.8);
    expect(eighty?.covered).toBe(3);
    expect(eighty?.empirical).toBeCloseTo(3 / 5);
  });

  it("drops non-finite and out-of-range values instead of skewing", () => {
    const points = coverageCurve([0.5, Number.NaN, -0.2, 1.4, Infinity]);
    expect(points[0]?.n).toBe(1);
    expect(points[0]?.empirical).toBe(1);
  });

  it("returns NaN empirical coverage with no usable scores", () => {
    const points = coverageCurve([]);
    expect(points).toHaveLength(COVERAGE_LEVELS.length);
    for (const point of points) {
      expect(point.n).toBe(0);
      expect(Number.isNaN(point.empirical)).toBe(true);
    }
  });
});

describe("pitHistogram", () => {
  it("bins the unit interval with the top edge closed", () => {
    const bins = pitHistogram([0, 0.05, 0.1, 0.55, 0.999, 1], 10);
    expect(bins).toHaveLength(10);
    expect(bins.reduce((total, bin) => total + bin.count, 0)).toBe(6);
    expect(bins[0]?.count).toBe(2); // 0 and 0.05
    expect(bins[1]?.count).toBe(1); // 0.1 starts the second bin
    expect(bins[5]?.count).toBe(1); // 0.55
    expect(bins[9]?.count).toBe(2); // 0.999 and the closed edge at 1
  });

  it("reports shares that sum to one when data exists", () => {
    const bins = pitHistogram([0.2, 0.4, 0.6, 0.8]);
    expect(
      bins.reduce((total, bin) => total + bin.share, 0),
    ).toBeCloseTo(1);
  });

  it("stays all-zero on empty input", () => {
    for (const bin of pitHistogram([])) {
      expect(bin.count).toBe(0);
      expect(bin.share).toBe(0);
    }
  });
});
