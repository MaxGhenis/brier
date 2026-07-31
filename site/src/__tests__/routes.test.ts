import { describe, expect, it } from "vitest";
import nextConfig from "../../next.config";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import { generateStaticParams } from "@/app/forecasts/[slug]/page";

describe("route configuration", () => {
  it("permanently redirects the legacy /markets tree to /forecasts", async () => {
    const redirects = await nextConfig.redirects!();
    const markets = redirects.find((r) => r.source === "/markets/:path*");
    expect(markets).toBeDefined();
    expect(markets).toMatchObject({
      destination: "/forecasts/:path*",
      permanent: true,
    });
  });

  it("redirects retired /about to /thesis without shadowing the thesis page", async () => {
    const redirects = await nextConfig.redirects!();
    const about = redirects.find((r) => r.source === "/about");
    expect(about).toMatchObject({ destination: "/thesis" });
    const thesisShadow = redirects.find((r) => r.source === "/thesis");
    expect(thesisShadow).toBeUndefined();
  });

  it("prerenders exactly one page per forecast cell", () => {
    const params = generateStaticParams();
    expect(
      params,
      "generateStaticParams() and FORECAST_CELLS disagree on how many forecast\n" +
        `pages exist: ${params.length} params vs ${FORECAST_CELLS.length} cells.\n` +
        "Every cell must prerender exactly one page — a cell with no param is a\n" +
        "forecast that 404s in production even though the browser links to it.\n" +
        "REMEDY: fix the mapping in site/src/app/forecasts/[slug]/page.ts so it\n" +
        "enumerates FORECAST_CELLS directly. DO NOT relax this to a >= check.",
    ).toHaveLength(FORECAST_CELLS.length);
    // Projection: report the duplicated slugs, not just the count gap.
    const counts = new Map<string, number>();
    for (const cell of FORECAST_CELLS) {
      counts.set(cell.slug, (counts.get(cell.slug) ?? 0) + 1);
    }
    const duplicates = [...counts.entries()]
      .filter(([, count]) => count > 1)
      .map(([slug, count]) => `${slug} (x${count})`);
    expect(
      duplicates,
      "Two or more forecast cells share a slug. The slug is the page URL and\n" +
        "the join key used by the ledger, scoring, and comparison surfaces, so a\n" +
        "collision means one forecast's page silently renders the other's data\n" +
        "and one of the two becomes unreachable and unscorable.\n" +
        "REMEDY: rename the newer cell in site/src/data/forecast-examples/ and\n" +
        "re-run the converter. If the duplicate is an accidental re-import of an\n" +
        "existing cell, delete it. DO NOT dedupe at render time — the collision\n" +
        "needs to be resolved in the data, or resolution binds to the wrong cell.",
    ).toEqual([]);
    const slugs = new Set(params.map((p) => p.slug));
    expect(slugs.size).toBe(FORECAST_CELLS.length);
  });
});
