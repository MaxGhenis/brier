import { describe, expect, it } from "vitest";
import nextConfig from "../../next.config";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import {
  buildPublisherFacet,
  publisherForCell,
  publisherSlugForDataPointId,
} from "@/data/forecast-publishers";
import {
  buildForecastListing,
  filterForecastListing,
} from "@/data/forecast-listing";

describe("publisher derivation", () => {
  it("is total: every cell with a dataPointId derives a publisher", () => {
    for (const cell of FORECAST_CELLS) {
      if (!cell.dataPointId) continue;
      const publisher = publisherForCell(cell);
      expect(publisher, cell.slug).not.toBeNull();
      expect(publisher!.slug).toMatch(/^[a-z0-9_]+$/);
      expect(publisher!.label.length).toBeGreaterThan(0);
    }
  });

  it("flattens same-organization spellings", () => {
    expect(publisherSlugForDataPointId("us.dol.initial_claims.sa.w")).toBe(
      "dol",
    );
    expect(publisherSlugForDataPointId("usda.fns.snap.x.fy2025")).toBe("fns");
    expect(publisherSlugForDataPointId("fns.snap.total_persons.2026-05")).toBe(
      "fns",
    );
    expect(publisherSlugForDataPointId("hhs.acf.liheap.x")).toBe("acf");
    expect(publisherSlugForDataPointId("us.frb.industrial_production.x")).toBe(
      "fed",
    );
    expect(publisherSlugForDataPointId("fed.g17.capacity.x")).toBe("fed");
    expect(publisherSlugForDataPointId("estat.cpi.x")).toBe("statjp");
  });

  it("falls back to the raw token for unknown agencies", () => {
    expect(publisherSlugForDataPointId("newagency.series.x")).toBe(
      "newagency",
    );
  });

  it("builds a facet where every entry is backed by cells", () => {
    const facet = buildPublisherFacet(FORECAST_CELLS);
    expect(facet.length).toBeGreaterThan(10);
    const total = facet.reduce((sum, entry) => sum + entry.count, 0);
    const withId = FORECAST_CELLS.filter((cell) => cell.dataPointId).length;
    expect(total).toBe(withId);
    for (const entry of facet) {
      expect(entry.count).toBeGreaterThan(0);
    }
    // Largest-first ordering.
    for (let i = 1; i < facet.length; i++) {
      expect(facet[i - 1].count).toBeGreaterThanOrEqual(facet[i].count);
    }
  });
});

describe("listing filters", () => {
  const listing = buildForecastListing(FORECAST_CELLS);

  it("passes everything through an empty filter", () => {
    expect(filterForecastListing(listing, {})).toHaveLength(listing.length);
  });

  it("filters by derived publisher", () => {
    const ssa = filterForecastListing(listing, { publisher: "ssa" });
    expect(ssa.length).toBeGreaterThan(0);
    for (const item of ssa) {
      expect(item.publisher?.slug).toBe("ssa");
    }
  });

  it("composes publisher, country, status, and title query", () => {
    const filtered = filterForecastListing(listing, {
      publisher: "cms",
      country: "US",
      status: "pending",
      query: "nursing",
    });
    for (const item of filtered) {
      expect(item.publisher?.slug).toBe("cms");
      expect(item.country).toBe("US");
      expect(item.status).toBe("pending");
      expect(item.title.toLowerCase()).toContain("nursing");
    }
    expect(filtered.some((item) => item.slug === "nursing-home-staffing-hprd-july-2026")).toBe(
      true,
    );
  });

  it("title query is case-insensitive and trims", () => {
    const upper = filterForecastListing(listing, { query: "  NURSING " });
    const lower = filterForecastListing(listing, { query: "nursing" });
    expect(upper.map((i) => i.slug)).toEqual(lower.map((i) => i.slug));
  });
});

describe("topics retirement", () => {
  it("redirects /topics/* home", async () => {
    const redirects = await nextConfig.redirects!();
    const topics = redirects.find((r) => r.source === "/topics/:path*");
    expect(topics).toMatchObject({ destination: "/", permanent: false });
  });
});
