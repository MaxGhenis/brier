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
      expect(tools.length).toBeGreaterThanOrEqual(2);
      for (const t of tools) {
        expect(t.call.length).toBeGreaterThan(10);
        expect(t.result).toMatch(/\d/);
      }

      expect(steps.some((s) => s.kind === "math")).toBe(true);

      // Cells spawned on/after 2026-07-05 must SHOW the interval derivation
      // (sigma or the 1.28 z-multiplier) in a math step — width from realized
      // dispersion, not a hedged template. Byte-identical regex lives in
      // scripts/spawned_cells_to_ts.py; keep them in sync.
      const runAt = cell.predictionRun?.runAt ?? "";
      // Leakage gate: the resolution must postdate the run (same cutoff and
      // semantics as scripts/spawned_cells_to_ts.py).
      if (runAt >= "2026-07-07") {
        expect(cell.resolutionDate > runAt.slice(0, 10)).toBe(true);
      }
      if (runAt >= "2026-07-05") {
        const mathText = steps
          .filter((s) => s.kind === "math")
          .map((s) => ("text" in s ? s.text : ""))
          .join(" ");
        expect(mathText).toMatch(/sigma\s*[=≈:]|1\.28/i);
      }

      const text = steps
        .map((s) =>
          "text" in s ? s.text : "result" in s ? `${s.call} ${s.result}` : "",
        )
        .join(" ")
        .toLowerCase();
      expect(text).toMatch(
        /base rate|reference class|last \d+ (prints|releases|months|meetings|weeks|weekly|monthly|obs)|distribution of|(trailing|past|realized) \d+|\d+-(week|month) (range|distribution|history)|realized (volatility|distribution)|historical (range|distribution)|trailing-?\d+|month-to-month volatility|std_samp|modal outcome|market-implied|implied probabilit|p_hold/,
      );
      expect(text).toMatch(
        /outside (the|our|this) interval|outside \[|would (push|put|land|break)|upside risk|downside risk|miss(es)? (high|low)|surprise|tail (scenario|risk)|break (the|this) (model|forecast)|breach|lands? (above|below)|(above|below) the (interval|band|range)|forecast (high|low)|probability would (fall|rise)|would (fail|flip)|fails? (only )?if|wrong if|blow past|revert (into|to)|exceed (my|the) central|right-skewed|saturation tail/,
      );

      const last = steps[steps.length - 1];
      expect(last.kind).toBe("forecast");
      if (last.kind === "forecast") {
        expect(last.point).toBe(cell.pointEstimate);
        expect(last.ciLow).toBe(cell.ciLow);
        expect(last.ciHigh).toBe(cell.ciHigh);
      }

      // Discrete-outcome cells (rate decisions) may sit at an interval edge.
      expect(cell.ciLow).toBeLessThanOrEqual(cell.pointEstimate);
      expect(cell.pointEstimate).toBeLessThanOrEqual(cell.ciHigh);
      expect(cell.ciLow).toBeLessThan(cell.ciHigh);
      expect(cell.resolutionSourceUrl).toMatch(/^https:\/\//);

      const run = cell.predictionRun!;
      expect(Date.parse(run.runAt)).toBeGreaterThan(Date.parse("2026-06-01"));
      expect(run.sourceContext.length).toBeGreaterThanOrEqual(2);
      for (const url of run.sourceContext) {
        expect(url).toMatch(/^https?:\/\//);
      }

      // Versioned-agent attribution: every pipeline run names the exact
      // agent definition (semver + content hashes) that produced it.
      expect(run.agentVersion).toMatch(/^\d+\.\d+\.\d+$/);
      expect(run.promptHash).toMatch(/^[0-9a-f]{64}$/);
      expect(run.toolPolicyHash).toMatch(/^[0-9a-f]{64}$/);
    },
  );
});
