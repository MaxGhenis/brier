import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: "/:path*",
        has: [{ type: "host", value: "farness.ai" }],
        destination: "https://app.thesisinstitute.org/:path*",
        permanent: true,
      },
      {
        source: "/:path*",
        has: [{ type: "host", value: "www.farness.ai" }],
        destination: "https://app.thesisinstitute.org/:path*",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
