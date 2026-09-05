import type { NumericCdf } from "@/data/generated/thesis-lab";

export type DensityInterval = {
  lower: number;
  upper: number;
  density: number;
};

/** Derivative of the validated, piecewise linear CDF; no smoothing or normalization. */
export function deriveDensity(
  points: NumericCdf["points"],
): DensityInterval[] | null {
  const intervals: DensityInterval[] = [];
  for (let i = 1; i < points.length; i++) {
    const previous = points[i - 1];
    const current = points[i];
    const width = current.value - previous.value;
    const mass = current.probability - previous.probability;
    const density = mass / width;
    // Even finite input coordinates can overflow or underflow during division.
    // Refuse an unrepresentable curve instead of dropping its probability mass.
    if (
      !Number.isFinite(width) ||
      width <= 0 ||
      !Number.isFinite(density) ||
      density < 0 ||
      (mass > 0 && density === 0)
    )
      return null;
    intervals.push({ lower: previous.value, upper: current.value, density });
  }
  return intervals.length > 0 ? intervals : null;
}
