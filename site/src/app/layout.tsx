import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Thesis — open forecasts on government data",
  description:
    "Open forecast cells for public policy, tax, benefit, poverty, and government data, with agent reasoning traces and calibrated uncertainty.",
  openGraph: {
    type: "website",
    title: "Thesis",
    description:
      "Open forecast cells for public policy, tax, benefit, poverty, and government data, with agent reasoning traces and calibrated uncertainty.",
    url: "https://app.thesisinstitute.org",
    siteName: "Thesis",
    images: [
      {
        url: "https://app.thesisinstitute.org/og-image.png",
        width: 1200,
        height: 630,
        alt: "Thesis — open forecasts for public policy and government data",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Thesis",
    description:
      "Open forecast cells for public policy, tax, benefit, poverty, and government data.",
    images: ["https://app.thesisinstitute.org/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
