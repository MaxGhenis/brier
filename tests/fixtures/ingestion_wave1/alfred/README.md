# ALFRED wave-1 fixtures

These are unmodified, exact-period responses from the official ALFRED graph
endpoint. Each file freezes the first vintage in which its observation
appeared.

| Fixture | Series | Observation | First vintage | Value (USD billions, SAAR) | Bytes | SHA-256 |
|---|---|---|---|---:|---:|---|
| `pnfi-2025-q2-first-print.csv` | `PNFI` | 2025 Q2 (`2025-04-01`) | 2025-07-30 | 4,203.220 | 51 | `9f550bc31dca1359e70ddf7e9588ef9b67c901ed3eed1c1da8b610aad37b890f` |
| `pnfi-2025-q3-first-print.csv` | `PNFI` | 2025 Q3 (`2025-07-01`) | 2025-12-23 | 4,291.558 | 51 | `b588e9e3e0735b6a145285c529c02344f037303249b175d33a301e39b7f38a52` |
| `pnfi-2025-q4-first-print.csv` | `PNFI` | 2025 Q4 (`2025-10-01`) | 2026-02-20 | 4,378.954 | 51 | `05b9718a7ab180b5f8aa5028dbdc04291f5e76c69ebacd0214239d5c57d4df92` |
| `bea-rd-2025-q2-first-print.csv` | `Y006RC1Q027SBEA` | 2025 Q2 (`2025-04-01`) | 2025-07-30 | 821.083 | 61 | `555e5af679223e3365edff09947b29e6d1e78e4ed978cd7553d15da3730ac61e` |
| `bea-rd-2025-q3-first-print.csv` | `Y006RC1Q027SBEA` | 2025 Q3 (`2025-07-01`) | 2025-12-23 | 855.863 | 61 | `25499799f3ed33b75e0a715248a83fa7d865a5ff84c323fd4f5cfceff3cee2c6` |
| `bea-rd-2025-q4-first-print.csv` | `Y006RC1Q027SBEA` | 2025 Q4 (`2025-10-01`) | 2026-02-20 | 885.955 | 61 | `1e7e49c3d4c3468182298f1ec511bb38cafbb1a96d0a83a3f62414b729de01f1` |

The exact fetch URL for each row is:

`https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series}&vintage_date={first-vintage}&cosd={observation-date}&coed={observation-date}`

Q2 was first published in BEA's 2025-07-30 GDP advance estimate. The
2025-12-23 GDP initial estimate was the first Q3 print because the federal
shutdown canceled the usual advance and second estimates. Q4 was first
published in BEA's 2026-02-20 GDP advance estimate.

A fresh 2026-08-07 UTC check also parsed each preceding-day ALFRED response
and confirmed that the exact observation date was absent. ALFRED returns the
full then-available history when a constrained observation does not yet exist,
so absence is tested by row membership rather than payload emptiness. The
request verification blocks record those preceding-day response hashes and
last available dates. `tests/test_resolve_pending.py` hash-checks and parses
all six frozen first-print fixtures.
