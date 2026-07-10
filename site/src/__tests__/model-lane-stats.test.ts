import { describe, expect, it } from "vitest";
import { MODEL_LANE_STATS } from "@/data/model-lane-stats.generated";
import { STRATEGY_COMPARISON_RUN_AUGMENTS } from "@/data/thesis-strategy-comparisons";

describe("model lane stats", () => {
  it("is internally coherent", () => {
    expect(MODEL_LANE_STATS.length).toBeGreaterThan(0);
    for (const row of MODEL_LANE_STATS) {
      expect(row.model.length).toBeGreaterThan(0);
      expect(row.lane.length).toBeGreaterThan(0);
      expect(Number.isInteger(row.attempted)).toBe(true);
      expect(Number.isInteger(row.passed)).toBe(true);
      expect(row.passed).toBeGreaterThanOrEqual(0);
      expect(row.passed).toBeLessThanOrEqual(row.attempted);
    }
  });

  it("accounts for every published comparison run's model", () => {
    // Every model that appears on a published comparison row must have lane
    // stats, and its total passed count must cover at least those rows
    // (stats also count runs outside the comparison corpus, never fewer).
    const publishedByModel = new Map<string, number>();
    for (const runs of Object.values(STRATEGY_COMPARISON_RUN_AUGMENTS)) {
      for (const run of runs) {
        const model = run.predictionRun?.model;
        if (!model) continue;
        publishedByModel.set(model, (publishedByModel.get(model) ?? 0) + 1);
      }
    }
    expect(publishedByModel.size).toBeGreaterThan(0);
    for (const [model, published] of publishedByModel) {
      const passed = MODEL_LANE_STATS.filter(
        (row) => row.model === model,
      ).reduce((sum, row) => sum + row.passed, 0);
      expect(passed).toBeGreaterThanOrEqual(published);
    }
  });
});
