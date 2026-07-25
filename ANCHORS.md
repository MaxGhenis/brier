# Anchor verifications — resolver-debt lane

## QCEW aircraft manufacturing establishments (bls.qcew.aircraft_manufacturing.establishments)

Verified 2026-07-25 (UTC) by the integrating session against the live
official source, after the lane's sandbox could not reach data.bls.gov.
Row filter: area_fips=US000, own_code=5, agglvl_code=18, size_code=0,
industry_code=336411, field=qtrly_estabs.

| Quarter | Canonical key | qtrly_estabs | Source |
|---|---|---|---|
| 2024 Q3 | 2024-07 | 1314 | https://data.bls.gov/cew/data/api/2024/3/industry/336411.csv |
| 2024 Q4 | 2024-10 | 1332 | https://data.bls.gov/cew/data/api/2024/4/industry/336411.csv |
| 2025 Q1 | 2025-01 | 1379 | https://data.bls.gov/cew/data/api/2025/1/industry/336411.csv |

The runtime gate (`qcew_anchor_mismatches`) re-fetches every anchor at
resolution time and refuses the adapter on any mismatch, so these pins are
self-checking, not trusted literals.

## CPI-U annual average (bls.cpi.u.annual_pct_change)

The lane pinned 2022=8.0, 2023=4.1, 2024=2.9, 2025=2.6 (annual-average
percent change). The first three match BLS's published annual averages;
all four are recomputed from live monthly data by
`bls_annual_anchor_mismatches` at resolution time, which refuses on drift.
