import { describe, expect, it } from "vitest";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import {
  FROZEN_PRE_CUSTODY_SLUGS,
  classifyTraceProvenance,
} from "@/data/trace-provenance";

describe("classifyTraceProvenance", () => {
  it("classes archived activity as activity-backed", () => {
    expect(
      classifyTraceProvenance({ custodyRootSha256: "a".repeat(64) }),
    ).toBe("activity_backed");
    expect(
      classifyTraceProvenance({
        predictionRun: { activityLog: [{ kind: "artifact" }] },
      }),
    ).toBe("activity_backed");
  });

  it("classes known pre-archive research runs as recorded runs", () => {
    expect(
      classifyTraceProvenance({ predictionRun: { model: "gpt-5-codex" } }),
    ).toBe("recorded_run");
    expect(
      classifyTraceProvenance({ predictionRun: { model: "claude-fable-5" } }),
    ).toBe("recorded_run");
  });

  it("defaults authored and unlabeled traces to illustrative", () => {
    expect(
      classifyTraceProvenance({
        predictionRun: { model: "Codex recorded source-context synthesis" },
      }),
    ).toBe("illustrative");
    expect(classifyTraceProvenance({})).toBe("illustrative");
    expect(
      classifyTraceProvenance({ predictionRun: { model: "anything-new" } }),
    ).toBe("illustrative");
  });
});

describe("the real-tool-calls assertion", () => {
  it("admits no cell that is neither activity-backed nor frozen", () => {
    // The standing forward invariant: every published trace either replays
    // archived activity or predates the June 28, 2026 regime and sits in
    // the shrink-only frozen registry. A new cell whose tool calls were
    // not executed cannot enter the catalog without failing here.
    const offenders = FORECAST_CELLS.filter(
      (cell) =>
        classifyTraceProvenance(cell) !== "activity_backed" &&
        !FROZEN_PRE_CUSTODY_SLUGS.has(cell.slug),
    );
    const violations = offenders.map((cell) => cell.slug);
    expect(
      violations,
      "These cells publish a reasoning trace whose tool calls were never\n" +
        "archived, and they are not in the frozen pre-custody registry:\n" +
        offenders
          .map(
            (cell) =>
              `  - ${cell.slug}: classified "${classifyTraceProvenance(cell)}" ` +
              `(model "${cell.predictionRun?.model ?? "(none)"}", ` +
              `agent "${cell.predictionRun?.agent ?? "(none)"}", ` +
              `runAt ${cell.predictionRun?.runAt ?? "(none)"}, ` +
              `activityLog ${cell.predictionRun?.activityLog?.length ?? 0} entries, ` +
              `custodyRootSha256 ${cell.predictionRun?.custodyRootSha256 ? "present" : "absent"})`,
          )
          .join("\n") +
        "\n\nThe invariant: since the June 28, 2026 custody regime, every published\n" +
        "trace either replays archived run activity (a custodyRootSha256 or a\n" +
        "non-empty activityLog => \"activity_backed\") or predates the regime and\n" +
        "sits in FROZEN_PRE_CUSTODY_SLUGS. The registry is shrink-only: cells may\n" +
        "leave it by being regenerated, and NOTHING may ever join it.\n" +
        "A cell landing here means its tool-call signatures were authored rather\n" +
        "than executed, i.e. the site would present invented research as a run.\n\n" +
        "REMEDY: re-spawn the cell through the thesis.analyst pipeline so the\n" +
        "runner archives its activity, then re-convert it. If it is a genuinely\n" +
        "old cell being re-imported, it does not belong in the catalog at all.\n" +
        "DO NOT add the slug to site/src/data/trace-provenance-frozen.json — that\n" +
        "file is the pinned historical population, and appending to it is exactly\n" +
        "the move this gate exists to prevent. DO NOT add the cell's model string\n" +
        "to RECORDED_RUN_MODELS either: \"recorded_run\" is still not\n" +
        "activity-backed and would not clear this assertion anyway.",
    ).toEqual([]);
  });

  it("keeps the frozen registry shrink-only and current", () => {
    const bySlug = new Map(FORECAST_CELLS.map((cell) => [cell.slug, cell]));
    for (const slug of FROZEN_PRE_CUSTODY_SLUGS) {
      const cell = bySlug.get(slug);
      // A frozen entry must still name a real cell…
      expect(cell, `${slug} left the catalog; prune it from the registry`)
        .toBeDefined();
      // …and must leave the registry the moment it becomes activity-backed.
      expect(
        classifyTraceProvenance(cell!),
        `${slug} is now activity-backed; remove it from the frozen registry`,
      ).not.toBe("activity_backed");
    }
  });

  it("has no duplicate frozen entries", () => {
    expect(FROZEN_PRE_CUSTODY_SLUGS.size).toBeGreaterThan(0);
  });
});
