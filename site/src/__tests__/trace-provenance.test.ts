import { describe, expect, it } from "vitest";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import {
  FROZEN_PRE_CUSTODY_SLUGS,
  classifyTraceProvenance,
} from "@/data/trace-provenance";
import frozen from "@/data/trace-provenance-frozen.json";

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
    const violations = FORECAST_CELLS.filter(
      (cell) =>
        classifyTraceProvenance(cell) !== "activity_backed" &&
        !FROZEN_PRE_CUSTODY_SLUGS.has(cell.slug),
    ).map((cell) => cell.slug);
    expect(violations).toEqual([]);
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
    // Read the raw array, not FROZEN_PRE_CUSTODY_SLUGS: that is a Set built
    // from these slugs, so it silently absorbs duplicates and cannot witness
    // the thing this test is named for. Asserting on its .size passed
    // unconditionally while a duplicated entry sat in the JSON.
    const slugs: string[] = frozen.slugs;
    expect(slugs.length).toBeGreaterThan(0);

    const counts = new Map<string, number>();
    for (const slug of slugs) counts.set(slug, (counts.get(slug) ?? 0) + 1);
    const duplicated = [...counts.entries()]
      .filter(([, n]) => n > 1)
      .map(([slug, n]) => `${slug} (x${n})`);

    expect(
      duplicated,
      "site/src/data/trace-provenance-frozen.json lists these slugs more " +
        "than once. The registry is a pinned census of the pre-custody " +
        "population and is shrink-only, so a repeated entry means an edit " +
        "re-added a slug that was already there — which inflates the " +
        "apparent size of the frozen population and hides whether the list " +
        "is really shrinking. Delete the extra occurrences; do not " +
        "de-duplicate by widening the Set, which is what masked this.",
    ).toEqual([]);
    expect(FROZEN_PRE_CUSTODY_SLUGS.size).toBe(slugs.length);
  });
});
