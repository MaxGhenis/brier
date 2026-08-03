import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

// The Unit union must cover every unit that appears in the generated
// registration surface: a registered target with an uncovered unit turns
// main build-red only AFTER its registration lands (2026-08-03, twice —
// first the adapter union, then unit "billions USD"). This test moves the
// failure to the change that introduces the unit.
describe("generated ledger targets use covered units", () => {
  it("every generated unit is a member of the Unit union", () => {
    const cells = readFileSync(
      join(__dirname, "../data/forecast-cells.ts"),
      "utf8",
    );
    const union = cells.match(/export type Unit =([\s\S]*?);/);
    expect(union).not.toBeNull();
    const covered = new Set(
      [...union![1].matchAll(/"([^"]+)"/g)].map((m) => m[1]),
    );

    const generated = readFileSync(
      join(__dirname, "../data/ledger-targets.generated.ts"),
      "utf8",
    );
    const used = new Set(
      [...generated.matchAll(/unit: "([^"]+)"/g)].map((m) => m[1]),
    );
    for (const unit of used) {
      expect(covered.has(unit), `unit "${unit}" missing from Unit union`).toBe(
        true,
      );
    }
  });
});
