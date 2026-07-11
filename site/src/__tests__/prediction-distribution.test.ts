import { describe, expect, it } from "vitest";
import {
  scoreNumericCdfDistribution,
  validateNumericCdfDistribution,
  type NumericCdfDistribution,
  type NumericCdfPoint,
} from "@/data/prediction-distribution";

function distribution(points: NumericCdfPoint[]): NumericCdfDistribution {
  return {
    format: "numeric_cdf_v1",
    pointCount: points.length as 201,
    support: {
      lower: points[0]?.value ?? 0,
      upper: points.at(-1)?.value ?? 0,
    },
    points,
    summary: {
      pointEstimate: 0.5,
      median: 0.5,
      interval80: { lower: 0.1, upper: 0.9 },
    },
    provenance: "agent_reported",
    transformVersion: "agent_cdf_v1",
  };
}

describe("exact piecewise-linear CRPS", () => {
  it("scores a uniform CDF on [0, 1] at its median", () => {
    const score = scoreNumericCdfDistribution(
      distribution([
        { value: 0, probability: 0 },
        { value: 1, probability: 1 },
      ]),
      0.5,
    );

    expect(score.crps).toBeCloseTo(1 / 12, 12);
    expect(score.probabilityIntegralTransform).toBe(0.5);
  });

  it("scores a degenerate near-step by its exact ramp area", () => {
    const epsilon = 1e-6;
    const score = scoreNumericCdfDistribution(
      distribution([
        { value: 0, probability: 0 },
        { value: 1 - epsilon, probability: 0 },
        { value: 1, probability: 1 },
      ]),
      1,
    );

    expect(score.crps).toBeCloseTo(epsilon / 3, 12);
  });

  it("includes exact tails when the observation is outside support", () => {
    const uniform = distribution([
      { value: 0, probability: 0 },
      { value: 1, probability: 1 },
    ]);

    expect(scoreNumericCdfDistribution(uniform, -1).crps).toBeCloseTo(
      4 / 3,
      11,
    );
    expect(scoreNumericCdfDistribution(uniform, 2).crps).toBeCloseTo(4 / 3, 11);
  });

  it("splits the observation segment in an asymmetric CDF", () => {
    // Knots (0,0), (1,1/4), (3,1), y=2. The exact pieces are:
    // [0,1]: 1/48; [1,2]: 13/64; [2,3]: 3/64; total = 13/48.
    const score = scoreNumericCdfDistribution(
      distribution([
        { value: 0, probability: 0 },
        { value: 1, probability: 0.25 },
        { value: 3, probability: 1 },
      ]),
      2,
    );

    expect(score.crps).toBeCloseTo(13 / 48, 12);
    expect(score.probabilityIntegralTransform).toBe(0.625);
  });
});

describe("numeric CDF validation", () => {
  it("accepts endpoint probabilities within the 1e-9 tolerance", () => {
    const candidate = distribution([
      { value: 0, probability: 5e-10 },
      { value: 1, probability: 1 - 5e-10 },
    ]);
    expect(validateNumericCdfDistribution(candidate)).toEqual([]);
  });

  it.each([
    ["too few points", [{ value: 0, probability: 0 }]],
    [
      "non-increasing values",
      [
        { value: 0, probability: 0 },
        { value: 0, probability: 1 },
      ],
    ],
    [
      "decreasing probabilities",
      [
        { value: 0, probability: 0 },
        { value: 1, probability: 0.8 },
        { value: 2, probability: 0.7 },
        { value: 3, probability: 1 },
      ],
    ],
    [
      "nonzero first probability",
      [
        { value: 0, probability: 0.01 },
        { value: 1, probability: 1 },
      ],
    ],
    [
      "final probability below one",
      [
        { value: 0, probability: 0 },
        { value: 1, probability: 0.99 },
      ],
    ],
    [
      "non-finite value",
      [
        { value: 0, probability: 0 },
        { value: Number.POSITIVE_INFINITY, probability: 1 },
      ],
    ],
  ])("rejects %s before scoring", (_label, points) => {
    const candidate = distribution(points as NumericCdfPoint[]);
    expect(validateNumericCdfDistribution(candidate).length).toBeGreaterThan(0);
    expect(() => scoreNumericCdfDistribution(candidate, 0.5)).toThrow(
      /Malformed numeric CDF/,
    );
  });
});

describe("signed-zero normalization", () => {
  it("never emits IEEE -0 anywhere in a built distribution", async () => {
    const { buildNumericCdfFromInterval } = await import(
      "@/data/prediction-distribution"
    );
    // An agent may forecast "-0.0"; JSON.parse preserves the sign while
    // JSON.stringify drops it, so a signed zero splits serialized surfaces
    // from in-memory values. The builder must normalize to +0 (the Python
    // port does the same).
    const built = buildNumericCdfFromInterval({
      pointEstimate: -0,
      ciLow: -0.1,
      ciHigh: 0.1,
    });
    expect(Object.is(built.summary.pointEstimate, -0)).toBe(false);
    expect(built.summary.pointEstimate).toBe(0);
    expect(Object.is(built.summary.median, -0)).toBe(false);
    for (const point of built.points) {
      expect(Object.is(point.value, -0)).toBe(false);
      expect(Object.is(point.probability, -0)).toBe(false);
    }
    expect(Object.is(built.support.lower, -0)).toBe(false);
    expect(Object.is(built.support.upper, -0)).toBe(false);
  });
});

describe("timeline label parsing for proportional trend spacing", () => {
  it("parses every label format observed in the catalog", async () => {
    const { parseTimelineLabel } = await import("@/components/ForecastViz");
    const zoo: Array<[string, boolean]> = [
      ["Mar 2026", true],
      ["March 2026", true],
      ["19 March 2026", true],
      ["2026-04", true],
      ["2026-04 MoM", true],
      ["Week 2026-06-06 (latest)", true],
      ["2024-11-08", true],
      ["01/26", true],
      ["2025 Q2 revised, BLS/FRED PRS85006092", true],
      ["2023-Q4 first-flash qoq", true],
      ["FY2019", true],
      ["FY 2024", true],
      ["SY2026-27", true],
      ["SY 2026-27", true],
      ["2021 first print age 65+ SPM poverty rate", true],
      ["no time here", false],
    ];
    for (const [label, expected] of zoo) {
      expect(parseTimelineLabel(label) !== null, label).toBe(expected);
    }
  });

  it("orders fiscal years, school years, and months consistently", async () => {
    const { parseTimelineLabel } = await import("@/components/ForecastViz");
    const sequence = [
      "FY2019",
      "FY2022",
      "FY2023",
      "FY2024",
      "SY 2026-27",
    ].map((label) => parseTimelineLabel(label)!);
    for (let index = 1; index < sequence.length; index += 1) {
      expect(sequence[index]).toBeGreaterThan(sequence[index - 1]);
    }
    // FY2019 -> FY2022 must span three times the FY2022 -> FY2023 gap.
    const bigGap = sequence[1] - sequence[0];
    const smallGap = sequence[2] - sequence[1];
    expect(bigGap / smallGap).toBeCloseTo(3, 1);
  });
});
