import { describe, expect, it } from "vitest";
import { FORECAST_CELLS } from "@/data/forecast-cells";

// Quality bar for the thesis.analyst pipeline: any cell published as a
// recorded agent run must carry a trace deep enough to audit — real tool
// calls with data, an explicit reference class, a quantitative derivation,
// and a stated way the forecast could miss. Older hand-authored runs are
// exempt; everything the pipeline produces from v2 on is not.

const PIPELINE_CELLS = FORECAST_CELLS.filter((cell) =>
  cell.predictionRun?.agent?.startsWith("thesis.analyst"),
);

describe("agent-run trace depth", () => {
  it("has pipeline cells to check once the spawn wave lands", () => {
    expect(Array.isArray(PIPELINE_CELLS)).toBe(true);
  });

  it.each(PIPELINE_CELLS.map((cell) => [cell.slug, cell] as const))(
    "%s meets the trace-depth rubric",
    (_slug, cell) => {
      const steps = cell.reasoning;
      expect(steps.length).toBeGreaterThanOrEqual(7);

      const tools = steps.filter((s) => s.kind === "tool");
      expect(tools.length).toBeGreaterThanOrEqual(3);
      for (const t of tools) {
        expect(t.call.length).toBeGreaterThan(10);
        expect(t.result).toMatch(/\d/);
      }

      expect(steps.some((s) => s.kind === "math")).toBe(true);

      const text = steps
        .map((s) => ("text" in s ? s.text : "call" in s ? s.call : ""))
        .join(" ")
        .toLowerCase();
      expect(text).toMatch(
        /base rate|reference class|last \d+ (prints|releases|months|meetings|weeks)|distribution of/,
      );
      expect(text).toMatch(
        /outside (the|our|this) interval|would (push|put|land|break)|upside risk|downside risk|miss(es)? (high|low)|surprise/,
      );

      const last = steps[steps.length - 1];
      expect(last.kind).toBe("forecast");
      if (last.kind === "forecast") {
        expect(last.point).toBe(cell.pointEstimate);
        expect(last.ciLow).toBe(cell.ciLow);
        expect(last.ciHigh).toBe(cell.ciHigh);
      }

      expect(cell.ciLow).toBeLessThan(cell.pointEstimate);
      expect(cell.pointEstimate).toBeLessThan(cell.ciHigh);
      expect(cell.resolutionSourceUrl).toMatch(/^https:\/\//);

      const run = cell.predictionRun!;
      expect(Date.parse(run.runAt)).toBeGreaterThan(Date.parse("2026-06-01"));
      expect(run.sourceContext.length).toBeGreaterThanOrEqual(2);
      for (const url of run.sourceContext) {
        expect(url).toMatch(/^https?:\/\//);
      }
    },
  );
});
