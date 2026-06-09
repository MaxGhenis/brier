# Thesis forecast API

Small Vercel-deployable backend for live forecast traces, deployed as the
`thesis-api` Vercel project behind `api.thesisinstitute.org`. Production
deploys go through `~/thesis-institute` ops tooling — never a bare
`vercel --prod` from an unreviewed checkout.

## Local development

```bash
bun install
bun run dev -- --hostname 127.0.0.1 --port 3002
```

The static site reads from `http://127.0.0.1:3002` on local hosts unless
`NEXT_PUBLIC_BRIER_API_BASE_URL` is set.

AI Gateway is optional locally. Without `AI_GATEWAY_API_KEY`,
`VERCEL_OIDC_TOKEN`, or a Vercel runtime, live endpoints still stream public
data/tool traces plus deterministic or calibration fallback forecasts.

## Endpoints

- `GET /health`
- `GET /forecasts/spm-child-poverty-2025/stream`
- `GET /forecasts/cpi-u-annual-2026/stream`
- `GET /forecasts/ctc-expansion-cost-ty2026/stream`
- `GET /forecasts/ctc-current-law-outlays-ty2026/stream`

## CORS

Allowed browser origins default to the thesisinstitute.org surfaces plus the
legacy brieralmanac.org/farness.ai domains and localhost (`src/lib/cors.ts`).
Override with `THESIS_SITE_ORIGINS` (or legacy `BRIER_SITE_ORIGINS`) as a
comma-separated list.
