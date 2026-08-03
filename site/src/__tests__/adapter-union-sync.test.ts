import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

// The TargetSourceAdapter union must mirror scripts/register_targets.py
// SOURCE_ADAPTERS exactly: any adapter python can register appears in
// ledger-targets.generated.ts, and a missing union member breaks the next
// site build only AFTER a registration lands (2026-08-03: the S.3596 wave
// registered "irs-soi-pub1304" and main went build-red). This test moves
// that failure to the PR that adds the adapter.
describe("adapter union stays in sync with the registration allowlist", () => {
  it("matches scripts/register_targets.py SOURCE_ADAPTERS", () => {
    const py = readFileSync(
      join(__dirname, "../../../scripts/register_targets.py"),
      "utf8",
    );
    const block = py.match(/SOURCE_ADAPTERS = \{([^}]+)\}/);
    expect(block).not.toBeNull();
    const pythonAdapters = [...block![1].matchAll(/"([^"]+)"/g)]
      .map((m) => m[1])
      .sort();

    const ts = readFileSync(join(__dirname, "../data/ledger-targets.ts"), "utf8");
    const union = ts.match(
      /export type TargetSourceAdapter =([\s\S]*?);/,
    );
    expect(union).not.toBeNull();
    const tsAdapters = [...union![1].matchAll(/"([^"]+)"/g)]
      .map((m) => m[1])
      .sort();

    expect(tsAdapters).toEqual(pythonAdapters);
  });
});
