export interface NumericCdfPoint {
  value: number;
  probability: number;
}

export interface NumericCdfDistribution {
  format: "numeric_cdf_v1";
  pointCount: 201;
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

export interface NumericCdfScore {
  crps: number;
  probabilityIntegralTransform: number;
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

  const pointCount = 201 as const;
  const step = (supportUpper - supportLower) / (pointCount - 1);
  const points = Array.from({ length: pointCount }, (_, index) => {
    const value =
      index === pointCount - 1 ? supportUpper : supportLower + step * index;
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
    pointCount,
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

export function scoreNumericCdfDistribution(
  distribution: NumericCdfDistribution,
  observedValue: number,
): NumericCdfScore {
  const points = distribution.points;
  if (points.length < 2) {
    return {
      crps: 0,
      probabilityIntegralTransform: observedValue <= points[0]?.value ? 1 : 0,
    };
  }

  let crps = 0;
  for (let index = 1; index < points.length; index += 1) {
    const previous = points[index - 1];
    const current = points[index];
    const width = current.value - previous.value;
    if (width <= 0) continue;

    const previousError = cdfScoreError(previous, observedValue);
    const currentError = cdfScoreError(current, observedValue);
    crps += ((previousError ** 2 + currentError ** 2) / 2) * width;
  }

  const lower = points[0];
  const upper = points[points.length - 1];
  if (observedValue < lower.value) {
    crps += lower.value - observedValue;
  }
  if (observedValue > upper.value) {
    crps += observedValue - upper.value;
  }

  return {
    crps: roundDistributionNumber(crps),
    probabilityIntegralTransform: roundDistributionNumber(
      interpolateCdfProbability(observedValue, points),
    ),
  };
}

function cdfScoreError(point: NumericCdfPoint, observedValue: number): number {
  const empiricalCdf = point.value >= observedValue ? 1 : 0;
  return point.probability - empiricalCdf;
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

function roundDistributionNumber(value: number): number {
  return Number(value.toPrecision(12));
}
