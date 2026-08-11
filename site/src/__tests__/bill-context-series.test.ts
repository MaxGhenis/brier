import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import {
  BILL_CONTEXT_SERIES_LINKS,
  getBillContextSeriesLinks,
} from "@/data/bill-forecasts";

const REPO_ROOT = path.resolve(__dirname, "../../..");

const docket = JSON.parse(
  fs.readFileSync(
    path.join(REPO_ROOT, "scripts", "docket_series.json"),
    "utf8",
  ),
) as {
  series: Array<{
    series: string;
    comment?: string;
    ledger?: { uuid: string; concept: string };
  }>;
};

describe("bill context-series links", () => {
  it("names real bill analyses and admitted docket concepts only", () => {
    for (const link of BILL_CONTEXT_SERIES_LINKS) {
      const billFile = path.join(REPO_ROOT, "bills", `${link.billSlug}.json`);
      expect(fs.existsSync(billFile), link.billSlug).toBe(true);
      const entry = docket.series.find(
        (row) => row.series === link.seriesConcept,
      );
      expect(entry, `${link.seriesConcept} is not an admitted series`)
        .toBeDefined();
      expect(entry?.ledger?.concept).toBe(link.seriesConcept);
      // Confident prefix (the resolver requires ≥3 dotted segments).
      expect(
        link.seriesConcept.split(".").filter(Boolean).length,
      ).toBeGreaterThanOrEqual(3);
    }
  });

  it("carries the scope boundary on every link, not just in comments", () => {
    for (const link of BILL_CONTEXT_SERIES_LINKS) {
      expect(link.scopeNote.length).toBeGreaterThan(80);
      expect(link.scopeNote.toLowerCase()).toContain("not ");
      expect(link.scopeNote.toLowerCase()).toContain("attributed");
    }
    const bySlug = new Map(
      BILL_CONTEXT_SERIES_LINKS.map((l) => [l.seriesConcept, l]),
    );
    // The Wave A caveats that reviews flagged as load-bearing:
    expect(
      bySlug.get("usaspending.cdfi.assistance_transaction_obligations")
        ?.scopeNote,
    ).toContain("downstream outcomes");
    expect(
      bySlug.get(
        "usaspending.usfs.minnesota_place_of_performance_obligations",
      )?.scopeNote,
    ).toContain("NOT Superior National Forest");
    expect(
      bySlug.get("usaspending.ondcp.hidta_al95001_obligations")?.scopeNote,
    ).toContain("707(s)");
  });

  it("stays in lockstep with the bill-context docket admissions", () => {
    // Every context-linked docket entry (identified by its scope comment
    // naming a bill page) must have exactly one link, and vice versa —
    // an admission without a page link would repeat the round-1 gap.
    const contextAdmissions = docket.series.filter((row) =>
      (row.comment ?? "").startsWith("Context series for the"),
    );
    const admitted = new Set(contextAdmissions.map((row) => row.series));
    const linked = new Set(
      BILL_CONTEXT_SERIES_LINKS.map((l) => l.seriesConcept),
    );
    expect([...linked].sort()).toEqual([...admitted].sort());
    expect(BILL_CONTEXT_SERIES_LINKS.length).toBe(
      new Set(BILL_CONTEXT_SERIES_LINKS.map((l) => l.seriesConcept)).size,
    );
  });

  it("filters by bill slug", () => {
    const links = getBillContextSeriesLinks("cdfi-fund-s2718-119");
    expect(links).toHaveLength(1);
    expect(links[0].seriesConcept).toBe(
      "usaspending.cdfi.assistance_transaction_obligations",
    );
    expect(getBillContextSeriesLinks("no-such-bill")).toHaveLength(0);
  });
});
