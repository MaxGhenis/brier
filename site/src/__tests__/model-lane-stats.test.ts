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
      const rows = MODEL_LANE_STATS.filter((row) => row.model === model);
      const passed = rows.reduce((sum, row) => sum + row.passed, 0);
      expect(
        passed,
        `Lane stats under-count model "${model}".\n` +
          `Published comparison rows for this model: ${published}\n` +
          `Lane stats say passed: ${passed}` +
          (rows.length
            ? ` (from ${rows.length} lane row(s): ${rows
                .map((row) => `${row.lane} ${row.passed}/${row.attempted}`)
                .join(", ")})`
            : " — this model has NO rows in MODEL_LANE_STATS at all") +
          `\nModels present in stats: ${
            [...new Set(MODEL_LANE_STATS.map((row) => row.model))].join(", ") ||
            "(none)"
          }\n\n` +
          "Lane stats must cover at least the runs the site publishes. They may\n" +
          "legitimately be LARGER (they also count runs outside the comparison\n" +
          "corpus), never smaller. Smaller means the site is showing comparison\n" +
          "rows the pass-rate denominator does not know about, so the published\n" +
          "attempt/pass rate understates how many runs that model really took —\n" +
          "the exact number a reader uses to judge selection effects.\n\n" +
          "Usual cause: a new model string appeared in\n" +
          "STRATEGY_COMPARISON_RUN_AUGMENTS but\n" +
          "site/src/data/model-lane-stats.generated.ts was not regenerated, or\n" +
          "the two spell the model differently (check the list above).\n\n" +
          "REMEDY: regenerate the lane stats. DO NOT hand-edit the generated file\n" +
          "and DO NOT drop the comparison row to make the counts line up.",
      ).toBeGreaterThanOrEqual(published);
    }
  });
});
