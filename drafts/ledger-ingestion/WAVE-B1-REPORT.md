# Wave B1: USAspending sealed transform extension report

Status as of 2026-08-11 UTC: complete. The four verified Wave A requests now
have sealed `usaspending-api` `fiscal_year_post_scalar` specs and annual FY2026
`registered_query_snapshot` docket entries. This wave changes no `records/**`
artifact.

Each series sums signed net `federal_action_obligation` over the prime award
transactions selected by its exact filters and groups the result by action-date
federal fiscal year. USAspending revises continuously, so the registered outcome
is the response to the pinned query inside the preregistered capture window; the
resolver preserves the full response bytes.

## Sealed transforms and scope limits

| Canonical series | What is sealed | Wave A FY2025 anchor and body check | What the series is not |
|---|---|---|---|
| `usaspending.cdfi.assistance_transaction_obligations` | Exact `spending_over_time` POST with the Community Development Financial Institutions Fund as awarding subtier, financial-assistance award type codes `02`–`11`, the complete fiscal-year date range, `group=fiscal_year`, and transaction-level spending. | `$319,455,176.00`. The generated body byte-matches [`usaspending-cdfi-fund-program-obligations.json`](usaspending-cdfi-fund-program-obligations.json): 315 canonical JSON bytes, SHA-256 `55b613d18a2f4763b68355f01d37a02f07700c0330320b658f2bd676a22b1543`. | Not all CDFI Fund financial-account obligations or outlays; not purchases, guarantees, loan-loss reserves, or other assistance authorized by S. 2718; not CDFI loan originations, liquidity, competitiveness, or other downstream outcomes; and no spending is attributed to the bill or amended section 113. |
| `usaspending.ondcp.hidta_al95001_obligations` | Exact `spending_over_time` POST with Assistance Listing `95.001`, financial-assistance award type codes `02`–`11`, the complete fiscal-year date range, `group=fiscal_year`, and transaction-level spending. No awarding-subagency filter is applied. | `$271,657,675.60`. The generated body byte-matches [`usaspending-ondcp-hidta-program-obligations.json`](usaspending-ondcp-hidta-program-obligations.json): 235 canonical JSON bytes, SHA-256 `df29835ff171f2649aaf7f33b4e6f2fc41f3efca5f8e92ae5e9e2ee16dec2c67`. | Not section 707(s) supplemental competitive grants or spending under a newly permitted purpose; not all HIDTA financial-account obligations, outlays, appropriations, budget authority, or authorization; and no spending is attributed to S. 767. |
| `usaspending.ntia.broadband_al11038_obligations` | Exact `spending_over_time` POST with Assistance Listing `11.038`, financial-assistance award type codes `02`–`11`, the complete fiscal-year date range, `group=fiscal_year`, and transaction-level spending. No agency, subagency, or Treasury-account filter is applied. | `$409,852,406.47`. The generated body byte-matches [`usaspending-ntia-broadband-program-obligations.json`](usaspending-ntia-broadband-program-obligations.json): 235 canonical JSON bytes, SHA-256 `232ff1c92f7ee2a962a8e54cc1779b1bee1e46976551fc71664b81a9dee5f205`. | Not the proposed 6G Task Force, its work, reports, recommendations, or outcomes; not all NTIA, NIST, Commerce, or FCC obligations or account `013-0565`; and no spending is attributed to or treated as caused or authorized by H.R. 2449. |
| `usaspending.usfs.minnesota_place_of_performance_obligations` | Exact `spending_over_time` POST with Forest Service as awarding subtier under the Department of Agriculture, the sealed assistance, contract, and IDV award type set, reported place of performance `{country: USA, state: MN}`, the complete fiscal-year date range, `group=fiscal_year`, and transaction-level spending. | `$46,832,556.79`. The generated body byte-matches [`usaspending-usfs-superior-nf-obligations.json`](usaspending-usfs-superior-nf-obligations.json): 475 canonical JSON bytes, SHA-256 `59c5a37d550b6d3cbff5a845d3e2b0f994056e81c7c506d71fcf81c55faa6f2a`. | Minnesota-wide context only, not Superior National Forest obligations or activity confined to the bill's covered lands; not H.R. 978 implementation, mineral instruments, or deadline compliance; and no spending is attributed to or treated as caused by H.R. 978. |

Each series is linked to its bill page through the explicit context-only
surface (`BILL_CONTEXT_SERIES_LINKS`): rendered under "Registered context
series — forecast regardless of this bill" with the scope boundary on the
page, never as a resolution of a bill metric.

The docket entries bind the canonical Chronicle identities, carry the same
scope caveats as `comment` keys, preserve these
FY2025 anchors in `usd_millions`, and use an explicit post-FY2026 capture window.
They do not put `resolutionDate` in calendar extras.

## Verification

- `uv run --extra dev --extra challenge --extra bills pytest tests/test_usaspending_adapter.py tests/test_resolve_pending.py tests/test_roll_docket.py -q`: **218 passed**.
- `cd site && bun run test`: **29 files passed; 811 tests passed**.

The adapter suite compares every generated body directly with its Wave A
request-file JSON, pins the canonical body hashes above, checks the captured
FY2025 response hashes and values, and asserts the scope caveats. The resolver
and docket suites cover execution, registration, rolling, and calendar-shape
invariants; the site suite remained green.
