import type { NextConfig } from "next";

const CANONICAL_HOST = "thesisinstitute.org";
const APP_HOST = "app.thesisinstitute.org";
const LEGACY_HOSTS = [
  "www.thesisinstitute.org",
  "brieralmanac.org",
  "www.brieralmanac.org",
  "farness.ai",
  "www.farness.ai",
];

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: "/forecasts",
        has: [{ type: "host" as const, value: APP_HOST }],
        destination: `https://${APP_HOST}`,
        permanent: true,
      },
      {
        source: "/forecasts/:path*",
        has: [{ type: "host" as const, value: APP_HOST }],
        destination: `https://${APP_HOST}/:path*`,
        permanent: true,
      },
      ...LEGACY_HOSTS.map((host) => ({
        source: "/:path*",
        has: [{ type: "host" as const, value: host }],
        destination: `https://${CANONICAL_HOST}/:path*`,
        permanent: true,
      })),
    ];
  },
  async rewrites() {
    return {
      beforeFiles: [
        {
          source: "/",
          has: [{ type: "host" as const, value: APP_HOST }],
          destination: "/forecasts",
        },
        {
          source: "/ledger",
          has: [{ type: "host" as const, value: APP_HOST }],
          destination: "/forecasts/ledger",
        },
        {
          source: "/ledger.json",
          has: [{ type: "host" as const, value: APP_HOST }],
          destination: "/forecasts/ledger.json",
        },
      ],
    };
  },
};

export default nextConfig;
