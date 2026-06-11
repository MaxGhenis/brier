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
    expect(params).toHaveLength(FORECAST_CELLS.length);
    const slugs = new Set(params.map((p) => p.slug));
    expect(slugs.size).toBe(FORECAST_CELLS.length);
  });
});
