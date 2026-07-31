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
    // The browser's only publisher facet is DERIVED from the dataPointId's
    // agency token — there is deliberately no hand-curated registry, so a
    // cell that derives nothing is a cell no publisher filter can reach.
    const DERIVATION =
      "Publisher is derived from the leading agency token of the dataPointId\n" +
      "(site/src/data/forecast-publishers.ts). New agencies are supposed to\n" +
      "work with zero registry edits, so a failure here means the dataPointId\n" +
      "itself is malformed, not that the agency is missing from a list.\n" +
      "REMEDY: fix the dataPointId to lead with a lowercase agency token.\n" +
      "Add to PUBLISHER_LABELS only to give an unreadable token a display name.";
    for (const cell of FORECAST_CELLS) {
      if (!cell.dataPointId) continue;
      const publisher = publisherForCell(cell);
      expect(
        publisher,
        `No publisher could be derived for cell "${cell.slug}"\n` +
          `dataPointId: ${cell.dataPointId}\n${DERIVATION}`,
      ).not.toBeNull();
      expect(
        publisher!.slug,
        `Derived publisher slug is not URL-safe for cell "${cell.slug}"\n` +
          `dataPointId: ${cell.dataPointId} -> slug "${publisher!.slug}"\n` +
          "The slug goes straight into the /forecasts?publisher=… query, so it\n" +
          `must match /^[a-z0-9_]+$/.\n${DERIVATION}`,
      ).toMatch(/^[a-z0-9_]+$/);
      expect(
        publisher!.label.length,
        `Derived publisher for cell "${cell.slug}" has an empty label\n` +
          `dataPointId: ${cell.dataPointId} -> slug "${publisher!.slug}"\n` +
          "An empty label renders as a blank, unclickable facet row.\n" +
          `${DERIVATION}`,
      ).toBeGreaterThan(0);
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
    expect(
      total,
      "The publisher facet does not account for every cell exactly once:\n" +
        `facet counts sum to ${total}, but ${withId} cells carry a dataPointId.\n` +
        `Facet as built: ${facet
          .map((entry) => `${entry.slug}=${entry.count}`)
          .join(", ")}\n` +
        "Under-counting means cells are invisible behind every publisher filter;\n" +
        "over-counting means a cell is being attributed to two agencies.\n" +
        "REMEDY: fix buildPublisherFacet in site/src/data/forecast-publishers.ts\n" +
        "so each cell contributes to exactly one bucket. DO NOT compare against\n" +
        "the facet's own sum — that would make the accounting check vacuous.",
    ).toBe(withId);
    expect(
      facet.filter((entry) => entry.count <= 0).map((entry) => entry.slug),
      "The publisher facet contains empty buckets. Every facet row is a\n" +
        "clickable filter, and a zero-count row leads to an empty results page.\n" +
        "This usually means a publisher was enumerated from a registry rather\n" +
        "than derived from the cells actually present.\n" +
        "REMEDY: build the facet only from cells that exist.",
    ).toEqual([]);
    // Largest-first ordering.
    const misordered = facet
      .map((entry, i) => ({ entry, i }))
      .filter(({ i }) => i > 0 && facet[i - 1].count < facet[i].count)
      .map(
        ({ entry, i }) =>
          `position ${i - 1} ${facet[i - 1].slug}=${facet[i - 1].count} < ` +
          `position ${i} ${entry.slug}=${entry.count}`,
      );
    expect(
      misordered,
      "The publisher facet is not sorted largest-first. The browser renders\n" +
        "facet rows in array order, so an unsorted facet buries the agencies\n" +
        "with the most forecasts below one-off publishers.\n" +
        `Full facet order: ${facet
          .map((entry) => `${entry.slug}=${entry.count}`)
          .join(", ")}\n` +
        "REMEDY: sort in buildPublisherFacet. DO NOT sort at render time — the\n" +
        "facet is consumed by more than one surface.",
    ).toEqual([]);
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
    const COMPOSED = {
      publisher: "cms",
      country: "US",
      status: "pending" as const,
      query: "nursing",
    };
    const filtered = filterForecastListing(listing, COMPOSED);
    for (const item of filtered) {
      expect(item.publisher?.slug).toBe("cms");
      expect(item.country).toBe("US");
      expect(item.status).toBe("pending");
      expect(item.title.toLowerCase()).toContain("nursing");
    }
    const WITNESS = "nursing-home-staffing-hprd-july-2026";
    expect(
      filtered.map((item) => item.slug),
      `The composed filter ${JSON.stringify(COMPOSED)} no longer returns the\n` +
        `witness cell "${WITNESS}".\n` +
        "The list above is what the filter did return.\n" +
        "This assertion proves the four filters COMPOSE (AND, not OR) against a\n" +
        "known-matching cell; without a witness, the test would still pass if the\n" +
        "filter returned nothing at all.\n" +
        "Two very different causes, and they need opposite fixes:\n" +
        "  1. filterForecastListing regressed (e.g. a facet now ORs, or the\n" +
        "     status/publisher derivation changed) — fix\n" +
        "     site/src/data/forecast-listing.ts.\n" +
        "  2. The witness cell simply resolved and is no longer \"pending\", or it\n" +
        "     left the catalog — then pick a new witness that is currently\n" +
        "     pending, CMS-published, US, and has \"nursing\" in the title, and\n" +
        "     update WITNESS here.\n" +
        "Check cause 1 first. DO NOT delete this assertion to get green: the\n" +
        "surrounding for-loop asserts nothing when `filtered` is empty.",
    ).toContain(WITNESS);
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
