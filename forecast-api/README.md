# Thesis Forecast API

Small Vercel-deployable backend for live forecast traces.

## Local development

```bash
bun install
bun run dev -- --hostname 127.0.0.1 --port 3002
```

The static site reads from `http://127.0.0.1:3002` on local hosts unless
`NEXT_PUBLIC_THESIS_API_BASE_URL` or the legacy
`NEXT_PUBLIC_BRIER_API_BASE_URL` is set.

AI Gateway is optional locally. Without `AI_GATEWAY_API_KEY`,
`VERCEL_OIDC_TOKEN`, or a Vercel runtime, live endpoints still stream public
data/tool traces plus deterministic or calibration fallback forecasts.

## Endpoints

- `GET /health`
- `GET /forecasts/cpi-u-annual-2026/stream`
- `GET /forecasts/ctc-expansion-cost-ty2026/stream`
- `GET /forecasts/ctc-current-law-outlays-ty2026/stream`
