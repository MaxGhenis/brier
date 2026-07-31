export interface NumericCdfPoint {
  value: number;
  probability: number;
}

export interface NumericQuantilePoint {
  probability: number;
  value: number;
}

export type DistributionProvenance = "agent_reported" | "interval_seeded";

export const INTERVAL_ANCHOR_TRANSFORM_VERSION = "interval_anchor_v1";
export const AGENT_CDF_TRANSFORM_VERSION = "agent_cdf_v1";

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
  provenance: DistributionProvenance;
  /**
   * Version of the immutable transform that produced the materialized CDF.
   * Older checked-in agent CDFs predate this field, so consumers resolve the
   * provenance-specific v1 default with getDistributionTransformVersion.
   */
  transformVersion?: string;
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
      pointEstimate: pointEstimate + 0,
      median: pointEstimate + 0,
      interval80: {
        lower: ciLow + 0,
        upper: ciHigh + 0,
      },
    },
    provenance,
    transformVersion:
      provenance === "interval_seeded"
        ? INTERVAL_ANCHOR_TRANSFORM_VERSION
        : AGENT_CDF_TRANSFORM_VERSION,
  };
}

/**
 * Materialize quantile knots with the same support rule and uniform 201-point
 * grid as scripts/run_thesis_analyst.py ladder_distribution (agent_cdf_v1).
 */
export function buildNumericCdfFromQuantiles({
  pointEstimate,
  quantiles,
}: {
  pointEstimate: number;
  quantiles: NumericQuantilePoint[];
}): NumericCdfDistribution {
  if (!Number.isFinite(pointEstimate) || quantiles.length < 3) {
    throw new TypeError("Quantile CDF requires a finite point and 3+ quantiles");
  }

  for (const [index, quantile] of quantiles.entries()) {
    const previous = quantiles[index - 1];
    if (
      !Number.isFinite(quantile.value) ||
      !Number.isFinite(quantile.probability) ||
      quantile.probability <= 0 ||
      quantile.probability >= 1 ||
      (previous &&
        (quantile.value <= previous.value ||
          quantile.probability <= previous.probability))
    ) {
      throw new TypeError(
        "Quantile CDF values and probabilities must be finite and strictly increasing",
      );
    }
  }

  const quantileAt = (probability: number) => {
    const match = quantiles.find(
      (quantile) => Math.abs(quantile.probability - probability) < 1e-12,
    );
    if (!match) {
      throw new TypeError(`Quantile CDF requires q${probability * 100}`);
    }
    return match.value;
  };
  const ciLow = quantileAt(0.1);
  const median = quantileAt(0.5);
  const ciHigh = quantileAt(0.9);
  if (Math.abs(pointEstimate - median) > 1e-12) {
    throw new TypeError("Quantile CDF point estimate must equal q50");
  }

  const lowerSpread = Math.max(Math.abs(median - ciLow), 1e-9);
  const upperSpread = Math.max(Math.abs(ciHigh - median), 1e-9);
  const supportLower = Math.min(
    ciLow - lowerSpread * 1.5,
    quantiles[0].value,
  );
  const supportUpper = Math.max(
    ciHigh + upperSpread * 1.5,
    quantiles.at(-1)!.value,
  );
  const knots = [
    { value: supportLower, probability: 0 },
    ...quantiles.map(({ probability, value }) => ({ probability, value })),
    { value: supportUpper, probability: 1 },
  ];
  const pointCount = 201 as const;
  const step = (supportUpper - supportLower) / (pointCount - 1);
  const points = Array.from({ length: pointCount }, (_, index) => {
    const value =
      index === pointCount - 1 ? supportUpper : supportLower + step * index;
    return {
      value: roundDistributionNumber(value),
      probability: roundDistributionNumber(
        interpolateCdfProbability(value, knots),
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
      pointEstimate: pointEstimate + 0,
      median: median + 0,
      interval80: {
        lower: ciLow + 0,
        upper: ciHigh + 0,
      },
    },
    provenance: "agent_reported",
    transformVersion: AGENT_CDF_TRANSFORM_VERSION,
  };
}

export function getDistributionTransformVersion(
  distribution: Pick<NumericCdfDistribution, "provenance" | "transformVersion">,
): string {
  return (
    distribution.transformVersion ??
    (distribution.provenance === "agent_reported"
      ? AGENT_CDF_TRANSFORM_VERSION
      : INTERVAL_ANCHOR_TRANSFORM_VERSION)
  );
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
  assertValidNumericCdfDistribution(distribution);
  if (!Number.isFinite(observedValue)) {
    throw new TypeError("Observed value must be finite");
  }

  const points = distribution.points;

  let crps = 0;
  for (let index = 1; index < points.length; index += 1) {
    const previous = points[index - 1];
    const current = points[index];
    if (previous.value < observedValue && observedValue < current.value) {
      const probabilityAtObservation = linearProbabilityAt(
        observedValue,
        previous,
        current,
      );
      crps += integrateSquaredLinear(
        observedValue - previous.value,
        previous.probability,
        probabilityAtObservation,
      );
      crps += integrateSquaredLinear(
        current.value - observedValue,
        probabilityAtObservation - 1,
        current.probability - 1,
      );
      continue;
    }

    const indicator = current.value <= observedValue ? 0 : 1;
    crps += integrateSquaredLinear(
      current.value - previous.value,
      previous.probability - indicator,
      current.probability - indicator,
    );
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

/**
 * Validate the piecewise-linear CDF contract used by scoring.
 * Returns all failures so quality-gate callers can report useful detail.
 */
export function validateNumericCdfDistribution(
  distribution: NumericCdfDistribution,
): string[] {
  const errors: string[] = [];
  const points = distribution.points;
  const tolerance = 1e-9;

  if (points.length < 2) errors.push("CDF must contain at least 2 points");
  if (distribution.pointCount !== points.length) {
    errors.push("CDF pointCount must equal points.length");
  }

  for (const [index, point] of points.entries()) {
    if (!Number.isFinite(point.value) || !Number.isFinite(point.probability)) {
      errors.push(`CDF point ${index} must contain finite values`);
      continue;
    }
    if (point.probability < -tolerance || point.probability > 1 + tolerance) {
      errors.push(`CDF probability ${index} must be between 0 and 1`);
    }
    if (index > 0) {
      const previous = points[index - 1];
      if (point.value <= previous.value) {
        errors.push("CDF point values must be strictly increasing");
      }
      if (point.probability < previous.probability) {
        errors.push("CDF probabilities must be monotone non-decreasing");
      }
    }
  }

  if (points.length > 0) {
    if (Math.abs(points[0].probability) > tolerance) {
      errors.push("CDF first probability must equal 0 within 1e-9");
    }
    if (Math.abs(points[points.length - 1].probability - 1) > tolerance) {
      errors.push("CDF final probability must equal 1 within 1e-9");
    }
  }

  return [...new Set(errors)];
}

export function assertValidNumericCdfDistribution(
  distribution: NumericCdfDistribution,
): void {
  const errors = validateNumericCdfDistribution(distribution);
  if (errors.length > 0) {
    throw new TypeError(`Malformed numeric CDF: ${errors.join("; ")}`);
  }
}

function linearProbabilityAt(
  value: number,
  lower: NumericCdfPoint,
  upper: NumericCdfPoint,
): number {
  const ratio = (value - lower.value) / (upper.value - lower.value);
  return lower.probability + ratio * (upper.probability - lower.probability);
}

// If an error term is linear from e0 to e1 across width w, its squared
// integral is w * (e0^2 + e0*e1 + e1^2) / 3.
function integrateSquaredLinear(
  width: number,
  errorAtLower: number,
  errorAtUpper: number,
): number {
  return (
    (width *
      (errorAtLower ** 2 + errorAtLower * errorAtUpper + errorAtUpper ** 2)) /
    3
  );
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
  // + 0 unifies IEEE signed zeros so the TS and Python ports emit identical
  // records: Python's json keeps "-0.0" while JSON.stringify drops the sign.
  return Number(value.toPrecision(12)) + 0;
}
