import { describe, expect, it } from "vitest";
import { resolveMetricCell } from "@/lib/metric-cells";

describe("resolveMetricCell (live metric → cell join)", () => {
  it("fails closed on missing or vague hints", () => {
    expect(resolveMetricCell(undefined)).toBeNull();
    expect(resolveMetricCell("")).toBeNull();
    expect(resolveMetricCell("irs")).toBeNull();
    expect(resolveMetricCell("irs.soi")).toBeNull();
  });

  it("returns null for a confident hint with no registered series", () => {
    expect(resolveMetricCell("usda.fsa.no_such_series")).toBeNull();
  });

  it("joins the SPM child poverty hint to a live cell", () => {
    const match = resolveMetricCell("census.spm.child_poverty_rate");
    expect(match).not.toBeNull();
    expect(match!.slug).toMatch(/spm-child-poverty/);
    expect(match!.pointLabel).toBeTruthy();
    expect(match!.ciLabel).toContain("–");
  });

  it("joins the ACTC hint to the ty2026 cell", () => {
    const match = resolveMetricCell(
      "irs.soi.additional_child_tax_credit_returns",
    );
    expect(match).not.toBeNull();
    expect(match!.resolutionDate).toBeTruthy();
  });

  it("picks the nearest unresolved period and counts the rest", () => {
    const match = resolveMetricCell("census.spm.child_poverty_rate", "2026-07-31");
    expect(match).not.toBeNull();
    // 2025-2028 cells exist; the chosen one resolves on/after today.
    expect(match!.resolutionDate >= "2026-07-31").toBe(true);
    expect(match!.moreCount).toBeGreaterThan(0);
  });

  it("falls back to the latest cell when the series is fully resolved", () => {
    const match = resolveMetricCell("census.spm.child_poverty_rate", "2099-01-01");
    expect(match).not.toBeNull();
    expect(match!.resolutionDate <= "2099-01-01").toBe(true);
  });
});

describe("conditional arms never satisfy unconditional metric hints", () => {
  it("excludes type=conditional cells from hint resolution", () => {
    // The FY27-NDAA pair shares the usaspending.dod.prime_award_obligations
    // series with OBBBA's unconditional Title II metric; the bill card
    // must keep resolving to unconditional cells only.
    const match = resolveMetricCell("usaspending.dod.prime_award_obligations");
    expect(match).not.toBeNull();
    expect(match?.slug).not.toContain("ndaa");
  });
});
