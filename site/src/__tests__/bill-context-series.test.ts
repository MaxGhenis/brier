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
    billSlugs?: string[];
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
    // The Wave A boundaries reviews flagged as load-bearing — each must
    // survive verbatim in the canonical note:
    const cdfi = bySlug.get(
      "usaspending.cdfi.assistance_transaction_obligations",
    )?.scopeNote;
    expect(cdfi).toContain("downstream outcomes");
    expect(cdfi).toContain("amended section 113");
    const hidta = bySlug.get(
      "usaspending.ondcp.hidta_al95001_obligations",
    )?.scopeNote;
    expect(hidta).toContain("707(s)");
    expect(hidta).toContain("authorization");
    const ntia = bySlug.get(
      "usaspending.ntia.broadband_al11038_obligations",
    )?.scopeNote;
    expect(ntia).toContain("013-0565");
    expect(ntia).toContain("NIST");
    expect(ntia).toContain("caused or authorized");
    const usfs = bySlug.get(
      "usaspending.usfs.minnesota_place_of_performance_obligations",
    )?.scopeNote;
    expect(usfs).toContain("not Superior National Forest");
    expect(usfs).toContain("covered lands");
  });

  it("stays in lockstep with the bill-context docket admissions", () => {
    // Structured marker, not free text: every docket entry declaring
    // billSlugs must have exactly one page link per declared bill, and
    // every link must trace back to a declaring entry — an admission
    // without its page linkage (the round-1 gap) fails here.
    const declaring = docket.series.filter(
      (row) => (row.billSlugs ?? []).length > 0,
    );
    const admittedPairs = declaring
      .flatMap((row) =>
        (row.billSlugs ?? []).map((slug) => `${slug}::${row.series}`),
      )
      .sort();
    const linkedPairs = BILL_CONTEXT_SERIES_LINKS.map(
      (l) => `${l.billSlug}::${l.seriesConcept}`,
    ).sort();
    expect(linkedPairs).toEqual(admittedPairs);
    expect(BILL_CONTEXT_SERIES_LINKS.length).toBe(
      new Set(BILL_CONTEXT_SERIES_LINKS.map((l) => l.seriesConcept)).size,
    );
  });

  it("keeps the docket comment and the page scope note identical", () => {
    // One canonical scope note per series: the docket comment is the
    // page scopeNote behind a fixed page-naming prefix, so the two
    // surfaces cannot drift apart (the round-2 weakening).
    for (const link of BILL_CONTEXT_SERIES_LINKS) {
      const entry = docket.series.find(
        (row) => row.series === link.seriesConcept,
      );
      expect(entry?.comment).toBe(
        `Context series for the ${link.billSlug} bill page ` +
          `(thesis#159 Wave A). ${link.scopeNote}`,
      );
    }
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
