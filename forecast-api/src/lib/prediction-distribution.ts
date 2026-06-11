import { z } from "zod";

export const NUMERIC_CDF_POINT_COUNT = 201;

export interface NumericCdfPoint {
  value: number;
  probability: number;
}

export interface NumericCdfDistribution {
  format: "numeric_cdf_v1";
  pointCount: typeof NUMERIC_CDF_POINT_COUNT;
  support: {
    lower: number;
    upper: number;
  };
  points: NumericCdfPoint[];
  summary: {
    pointEstimate: number;
    median: number;
    interval80: {
      lower: number;
      upper: number;
    };
  };
  provenance: "agent_reported" | "interval_seeded";
}

export type PredictionDistribution = NumericCdfDistribution;

export const AgentNumericCdfDistributionSchema = numericCdfDistributionSchema(
  "agent_reported",
);

export function numericCdfDistributionSchema(
  provenance: NumericCdfDistribution["provenance"],
) {
  return z
    .object({
      format: z.literal("numeric_cdf_v1"),
      pointCount: z.literal(NUMERIC_CDF_POINT_COUNT),
      support: z.object({
        lower: z.number(),
        upper: z.number(),
      }),
      points: z
        .array(
          z.object({
            value: z.number(),
            probability: z.number().min(0).max(1),
          }),
        )
        .length(NUMERIC_CDF_POINT_COUNT),
      summary: z.object({
        pointEstimate: z.number(),
        median: z.number(),
        interval80: z.object({
          lower: z.number(),
          upper: z.number(),
        }),
      }),
      provenance: z.literal(provenance),
    })
    .superRefine((distribution, context) => {
      if (distribution.support.upper <= distribution.support.lower) {
        context.addIssue({
          code: "custom",
          path: ["support"],
          message: "support.upper must be greater than support.lower",
        });
      }

      const first = distribution.points[0];
      const last = distribution.points.at(-1);
      if (!first || !last) return;

      if (Math.abs(first.value - distribution.support.lower) > 1e-9) {
        context.addIssue({
          code: "custom",
          path: ["points", 0, "value"],
          message: "first point value must equal support.lower",
        });
      }
      if (Math.abs(last.value - distribution.support.upper) > 1e-9) {
        context.addIssue({
          code: "custom",
          path: ["points", NUMERIC_CDF_POINT_COUNT - 1, "value"],
          message: "last point value must equal support.upper",
        });
      }
      if (first.probability !== 0) {
        context.addIssue({
          code: "custom",
          path: ["points", 0, "probability"],
          message: "first point probability must be 0",
        });
      }
      if (last.probability !== 1) {
        context.addIssue({
          code: "custom",
          path: ["points", NUMERIC_CDF_POINT_COUNT - 1, "probability"],
          message: "last point probability must be 1",
        });
      }

      const expectedStep =
        (distribution.support.upper - distribution.support.lower) /
        (NUMERIC_CDF_POINT_COUNT - 1);
      for (let index = 1; index < distribution.points.length; index += 1) {
        const previous = distribution.points[index - 1];
        const current = distribution.points[index];
        if (current.value <= previous.value) {
          context.addIssue({
            code: "custom",
            path: ["points", index, "value"],
            message: "CDF point values must strictly increase",
          });
        }
        if (current.probability < previous.probability) {
          context.addIssue({
            code: "custom",
            path: ["points", index, "probability"],
            message: "CDF probabilities must be monotone nondecreasing",
          });
        }

        const actualStep = current.value - previous.value;
        const tolerance = Math.max(Math.abs(expectedStep) * 1e-6, 1e-9);
        if (Math.abs(actualStep - expectedStep) > tolerance) {
          context.addIssue({
            code: "custom",
            path: ["points", index, "value"],
            message: "CDF point values must use an evenly spaced grid",
          });
        }
      }
    });
}

export function buildNumericCdfFromInterval({
  ciHigh,
  ciLow,
  pointEstimate,
  provenance = "interval_seeded",
}: {
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  provenance?: NumericCdfDistribution["provenance"];
}): NumericCdfDistribution {
  const lowerSpread = Math.max(Math.abs(pointEstimate - ciLow), 1e-9);
  const upperSpread = Math.max(Math.abs(ciHigh - pointEstimate), 1e-9);
  let supportLower = ciLow - lowerSpread * 1.5;
  let supportUpper = ciHigh + upperSpread * 1.5;

  if (!Number.isFinite(supportLower) || !Number.isFinite(supportUpper)) {
    supportLower = pointEstimate - 1;
    supportUpper = pointEstimate + 1;
  }
  if (supportUpper <= supportLower) {
    const spread = Math.max(Math.abs(pointEstimate), 1) * 0.1;
    supportLower = pointEstimate - spread;
    supportUpper = pointEstimate + spread;
  }

  const step = (supportUpper - supportLower) / (NUMERIC_CDF_POINT_COUNT - 1);
  const points = Array.from({ length: NUMERIC_CDF_POINT_COUNT }, (_, index) => {
    const value =
      index === NUMERIC_CDF_POINT_COUNT - 1
        ? supportUpper
        : supportLower + step * index;
    return {
      value: roundDistributionNumber(value),
      probability: roundDistributionNumber(
        interpolateCdfProbability(value, [
          { value: supportLower, probability: 0 },
          { value: ciLow, probability: 0.1 },
          { value: pointEstimate, probability: 0.5 },
          { value: ciHigh, probability: 0.9 },
          { value: supportUpper, probability: 1 },
        ]),
      ),
    };
  });

  return {
    format: "numeric_cdf_v1",
    pointCount: NUMERIC_CDF_POINT_COUNT,
    support: {
      lower: roundDistributionNumber(supportLower),
      upper: roundDistributionNumber(supportUpper),
    },
    points,
    summary: {
      pointEstimate,
      median: pointEstimate,
      interval80: {
        lower: ciLow,
        upper: ciHigh,
      },
    },
    provenance,
  };
}

export function normalizeNumericCdfDistribution({
  decimals,
  distribution,
  max,
  min,
}: {
  distribution: NumericCdfDistribution;
  min: number;
  max: number;
  decimals: number;
}): NumericCdfDistribution {
  const supportLower = clamp(distribution.support.lower, min, max);
  const supportUpper = clamp(distribution.support.upper, min, max);
  const pointEstimate = round(
    clamp(inverseCdf(distribution, 0.5), min, max),
    decimals,
  );
  const ciLow = round(clamp(inverseCdf(distribution, 0.1), min, max), decimals);
  const ciHigh = round(
    clamp(inverseCdf(distribution, 0.9), min, max),
    decimals,
  );

  return {
    ...distribution,
    support: {
      lower: roundDistributionNumber(supportLower),
      upper: roundDistributionNumber(supportUpper),
    },
    summary: {
      pointEstimate,
      median: pointEstimate,
      interval80: {
        lower: ciLow,
        upper: ciHigh,
      },
    },
  };
}

export function summarizeNumericCdfDistribution(
  distribution: NumericCdfDistribution,
) {
  return {
    pointEstimate: distribution.summary.pointEstimate,
    ciLow: distribution.summary.interval80.lower,
    ciHigh: distribution.summary.interval80.upper,
  };
}

function inverseCdf(
  distribution: NumericCdfDistribution,
  probability: number,
): number {
  const points = distribution.points;
  if (probability <= points[0].probability) return points[0].value;

  for (let index = 1; index < points.length; index += 1) {
    const previous = points[index - 1];
    const current = points[index];
    if (probability <= current.probability) {
      const height = current.probability - previous.probability;
      if (height <= 0) return current.value;
      const ratio = (probability - previous.probability) / height;
      return previous.value + ratio * (current.value - previous.value);
    }
  }

  return points.at(-1)?.value ?? distribution.support.upper;
}

function interpolateCdfProbability(
  value: number,
  rawKnots: NumericCdfPoint[],
): number {
  const knots = coalesceCdfKnots(rawKnots);
  if (value <= knots[0].value) return knots[0].probability;

  for (let index = 1; index < knots.length; index += 1) {
    const previous = knots[index - 1];
    const current = knots[index];
    if (value <= current.value) {
      const width = current.value - previous.value;
      if (width <= 0) return current.probability;
      const ratio = (value - previous.value) / width;
      return (
        previous.probability +
        ratio * (current.probability - previous.probability)
      );
    }
  }

  return knots.at(-1)?.probability ?? 1;
}

function coalesceCdfKnots(rawKnots: NumericCdfPoint[]): NumericCdfPoint[] {
  const sortedKnots = [...rawKnots].sort((a, b) =>
    a.value === b.value ? a.probability - b.probability : a.value - b.value,
  );
  const knots: NumericCdfPoint[] = [];

  for (const knot of sortedKnots) {
    const previous = knots.at(-1);
    if (previous && Math.abs(previous.value - knot.value) < 1e-12) {
      previous.probability = Math.max(previous.probability, knot.probability);
    } else {
      knots.push({ ...knot });
    }
  }

  return knots;
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function round(value: number, decimals: number) {
  const factor = 10 ** decimals;
  return Math.round(value * factor) / factor;
}

function roundDistributionNumber(value: number): number {
  return Number(value.toPrecision(12));
}
