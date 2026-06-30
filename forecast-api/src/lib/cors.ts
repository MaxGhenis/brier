const DEFAULT_ORIGINS = [
  "https://thesisinstitute.org",
  "https://www.thesisinstitute.org",
  "https://app.thesisinstitute.org",
  "http://localhost:3000",
  "http://127.0.0.1:3000",
  "http://localhost:3001",
  "http://127.0.0.1:3001",
];

export function corsHeaders(request: Request): HeadersInit {
  const origin = request.headers.get("origin");
  const allowedOrigins = (
    process.env.THESIS_SITE_ORIGINS?.split(",") ?? DEFAULT_ORIGINS
  ).map((value) => value.trim());
  const allowOrigin =
    origin && allowedOrigins.includes(origin) ? origin : allowedOrigins[0];

  return {
    "Access-Control-Allow-Origin": allowOrigin,
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

export function optionsResponse(request: Request) {
  return new Response(null, {
    status: 204,
    headers: corsHeaders(request),
  });
}
