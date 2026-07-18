/**
 * Calibration-curve math over probability integral transforms.
 *
 * Every resolved score carries F(observed) — the forecast CDF evaluated at
 * the official print. For a central interval with nominal coverage c the
 * outcome lands inside exactly when (1-c)/2 <= PIT <= (1+c)/2, so one PIT
 * per score yields the whole coverage curve, not just the elicited 80%
 * point. A calibrated forecaster's curve tracks the diagonal; PITs are
 * uniform. U-shaped PIT mass means overconfident (too narrow), a central
 * hump means underconfident (too wide).
 */

export interface CoveragePoint {
  nominal: number;
  empirical: number;
  covered: number;
  n: number;
}

export interface PitBin {
  binStart: number;
  binEnd: number;
  count: number;
  share: number;
}

export const COVERAGE_LEVELS = [
  0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95,
] as const;

function cleanPits(pits: number[]): number[] {
  return pits.filter((pit) => Number.isFinite(pit) && pit >= 0 && pit <= 1);
}

export function coverageCurve(
  pits: number[],
  levels: readonly number[] = COVERAGE_LEVELS,
): CoveragePoint[] {
  const usable = cleanPits(pits);
  return levels.map((nominal) => {
    const halfWidth = nominal / 2;
    const covered = usable.filter(
      (pit) => Math.abs(pit - 0.5) <= halfWidth + 1e-12,
    ).length;
    return {
      nominal,
      empirical: usable.length > 0 ? covered / usable.length : Number.NaN,
      covered,
      n: usable.length,
    };
  });
}

export function pitHistogram(pits: number[], binCount = 10): PitBin[] {
  const usable = cleanPits(pits);
  const counts = new Array<number>(binCount).fill(0);
  for (const pit of usable) {
    const index = Math.min(Math.floor(pit * binCount), binCount - 1);
    counts[index] += 1;
  }
  return counts.map((count, index) => ({
    binStart: index / binCount,
    binEnd: (index + 1) / binCount,
    count,
    share: usable.length > 0 ? count / usable.length : 0,
  }));
}
