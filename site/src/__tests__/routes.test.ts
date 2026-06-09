import { describe, expect, it } from "vitest";
import nextConfig from "../../next.config";
import { MARKETS } from "@/data/markets";
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

  it("prerenders exactly one page per forecast cell", () => {
    const params = generateStaticParams();
    expect(params).toHaveLength(MARKETS.length);
    const slugs = new Set(params.map((p) => p.slug));
    expect(slugs.size).toBe(MARKETS.length);
  });
});
