# Ingestion wave 1 report

Status as of 2026-08-07: wave 1 is complete. Triage and request verification
are complete, and three IRS workbook series, one USAspending series, and two
BEA series are admitted. No `records/**` artifact is part of this work.

Wave-2 update, 2026-08-08: the three SBA Loan Program Performance
requests moved proposed → verified. The witnessed-capture custody
family merged (thesis#145), the first allowlisted-workflow capture is
sealed and externally witnessed, and the three series carry docket-only
placeholders in PolicyEngine/chronicle. Verified totals below reflect
wave 1 only; the SBA admissions are wave 2's opener.

## Outcome summary

The wave covered 30 requests: eight ALFRED/USAspending quick requests and 22
workbook-triage requests. Five requests verified cleanly, four received a
terminal rejection for the proposed adapter family, and 21 remain proposals
for a later source family or future official print. All five verified request
concepts are in the docket. A sixth, narrower DHS award-transaction series was
admitted from the fetched USAspending evidence; the broader account-obligations
request remains proposed.

### Quick requests

| Request | Outcome | Reason |
|---|---|---|
| `bea-ita-personal-transfer-payments.json` | Rejected | No exact current FRED/ALFRED series; the candidates are broader or discontinued. |
| `bea-private-nonresidential-fixed-investment.json` | Admitted | Official BEA NIPA Table 5.3.5 line 2 matches the concept, quarterly cadence, nominal SAAR basis, and unit; ALFRED `PNFI` carries three Q2-Q4 2025 first-print pins. |
| `bea-research-and-development-fixed-investment.json` | Admitted | Official BEA NIPA Table 5.3.5 line 18 matches the concept, quarterly cadence, nominal SAAR basis, and unit; ALFRED `Y006RC1Q027SBEA` carries three Q2-Q4 2025 first-print pins. |
| `eia-natural-gas-vented-flared-us-annual.json` | Rejected | The official EIA series is exact, but FRED/ALFRED has no mirror and therefore cannot provide first-print vintages. |
| `usaspending-dhs-title-vi-named-account-obligations.json` | Proposed | The six-component advanced-search query proves only award-transaction obligations. Full account obligations remain open on a financial-account submission/TAS path; the narrower award-transaction series is admitted separately. |
| `usaspending-energy-commerce-title-iv-named-account-obligations.json` | Rejected | Live identifiers do not cover all named Title IV programs, so the query would measure only part of the concept. |
| `usaspending-ondcp-hidta-supplemental-grant-obligations.json` | Rejected | Assistance Listing 95.001 cannot distinguish the section 707(s) supplemental grants from broader HIDTA activity. |
| `usaspending-usda-selected-rural-program-obligations.json` | Proposed | The official 2026 America First Trade Promotion Program notice identifies opportunity `USDA-FAS-AFTPP-2026`, Assistance Listing 10.618, and $285 million in program funding. USAspending labels 10.618 as Regional Agricultural Promotion Program and an exact-name FY2026 AFTPP query returns $0, leaving award isolation and reporting lag open. |

### Workbook requests

The detailed scoring, artifact hashes, exact cells, and tie-break rule are in
[`TRIAGE-wave1.md`](TRIAGE-wave1.md).

| Rank | Request | Outcome |
|---:|---|---|
| 1 | `irs-soi-credit-30d-total-claims.json` | Admitted from Table 3.3; the current TY2023 official workbook prints 493,953 returns. |
| 2 | `irs-actc-total-credit-amount.json` | Admitted from Table 3.3; the current TY2023 official workbook prints $34,533.251 million. |
| 3 | `irs-soi-credit-30d-total-credit-amount.json` | Admitted from Table 3.3; the current TY2023 official workbook prints $3,231.102 million. |
| 4 | `sba-disaster-loan-program-charge-off-amount.json` | Proposed; the SBA PDF/custody family is built, and admission awaits the first eligible capture from `.github/workflows/witness-sba-pdf.yml`. |
| 5 | `sba-disaster-loan-program-charge-off-rate-upb.json` | Proposed; the SBA PDF/custody family is built, and admission awaits the first eligible capture from `.github/workflows/witness-sba-pdf.yml`. |
| 6 | `sba-disaster-loan-program-post-charge-off-recovery.json` | Proposed; the SBA PDF/custody family is built, and admission awaits the first eligible capture from `.github/workflows/witness-sba-pdf.yml`. |
| 7 | `irs-soi-credit-25e-total-claims.json` | Deferred to an IRS line-item PDF family; the exact field is absent from Table 3.3. |
| 8 | `irs-soi-credit-25e-total-credit-amount.json` | Deferred to an IRS line-item PDF family; the exact field is absent from Table 3.3. |
| 9 | `irs-soi-credit-45x-total-claims.json` | Deferred to an IRS corporation line-item PDF family. |
| 10 | `irs-soi-credit-45x-total-credit-amount.json` | Deferred to an IRS corporation line-item PDF family. |
| 11 | `irs-soi-credit-45y-total-claims.json` | Deferred; the latest corporation workbook has no separate field. |
| 12 | `irs-soi-credit-45y-total-credit-amount.json` | Deferred; the latest corporation workbook has no separate field. |
| 13 | `irs-soi-credit-48e-total-claims.json` | Deferred; the latest corporation workbook has no separate field. |
| 14 | `irs-soi-credit-48e-total-credit-amount.json` | Deferred; the latest corporation workbook has no separate field. |
| 15 | `irs-soi-overtime-deduction-total-claims.json` | Deferred; the latest individual workbook predates the provision and has no field. |
| 16 | `irs-soi-overtime-deduction-total-deduction-amount.json` | Deferred; the latest individual workbook predates the provision and has no field. |
| 17 | `irs-soi-senior-deduction-total-claims.json` | Deferred; the latest individual workbook has no field. |
| 18 | `irs-soi-senior-deduction-total-deduction-amount.json` | Deferred; the latest individual workbook has no field. |
| 19 | `irs-soi-tip-deduction-total-claims.json` | Deferred; the latest individual workbook predates the provision and has no field. |
| 20 | `irs-soi-tip-deduction-total-deduction-amount.json` | Deferred; the latest individual workbook predates the provision and has no field. |
| 21 | `irs-soi-vehicle-interest-deduction-total-claims.json` | Deferred; the latest individual workbook predates the provision and has no field. |
| 22 | `irs-soi-vehicle-interest-deduction-total-deduction-amount.json` | Deferred; the latest individual workbook predates the provision and has no field. |

## Admissions and fixture custody

The final admitted count is **6**:

- `irs.soi.credit_30d.total_claims`
- `irs.actc.total_credit_amount`
- `irs.soi.credit_30d.total_credit_amount`
- `usaspending.dhs.title_vi.award_transaction_obligations`
- `bea.private_nonresidential_fixed_investment`
- `bea.research_and_development_fixed_investment`

The three IRS series each have an `irs-soi-pub1304` resolver spec and a 2027
annual docket entry using the reviewed `resolve-by-bound` contract. Their
tests use the real TY2020–TY2023 workbook bytes; the TY2023 fixture is 105,472
bytes with SHA-256
`e749d3e9636d9784e2a5e8639f49ce5389a4ca0aaeedca6c671cee0b71264c04`.
The fixed IRS workbook URLs are not versioned. These fixtures authenticate the
parser and values as retrieved, not release-time custody: future first-print
resolution must capture inside the registered window and refuses after it.
Late resolution would require future custody-backed adapter support.
The DHS award-transaction series has an exact `usaspending-api` POST plan and
FY2026 registered snapshot window. Its unmodified 1,146-byte fixture has SHA-256
`dd51e2eb947fc8b302fe9c33297c85989b542c933801dcb0729edf39ba157720`.
The two BEA series have official `bea-release` current-print resolvers and
quarterly release-calendar seeds. On the registered GDP advance-release day,
the resolver authenticates the exact BEA news page and reads NIPA Table 5.3.5
line 2 (nonresidential fixed investment) or line 18 (research and development)
from BEA's iTable response, then archives both responses together. The real Q2
2026 parser fixtures are hash-pinned at 52,640 bytes / SHA-256
`4636dc341d7cd1a53196fdf0ad529143b0e8b2d0db874f6086ca9b8ebf23cf5d`
for the release HTML and 46,905 bytes / SHA-256
`59e5f1ab0eeaa76cdca566383c66eab7787214216ffcbe35aa4c1793a894750d`
for the official table response. ALFRED remains the dated-vintage history
mirror. Its exact-period fixtures reproduce three first prints per BEA series:

- PNFI: 4,203.220 (2025 Q2, vintage 2025-07-30; SHA-256
  `9f550bc31dca1359e70ddf7e9588ef9b67c901ed3eed1c1da8b610aad37b890f`),
  4,291.558 (2025 Q3, vintage 2025-12-23;
  `b588e9e3e0735b6a145285c529c02344f037303249b175d33a301e39b7f38a52`),
  and 4,378.954 (2025 Q4, vintage 2026-02-20;
  `05b9718a7ab180b5f8aa5028dbdc04291f5e76c69ebacd0214239d5c57d4df92`).
- Private R&D: 821.083 (2025 Q2, vintage 2025-07-30; SHA-256
  `555e5af679223e3365edff09947b29e6d1e78e4ed978cd7553d15da3730ac61e`),
  855.863 (2025 Q3, vintage 2025-12-23;
  `25499799f3ed33b75e0a715248a83fa7d865a5ff84c323fd4f5cfceff3cee2c6`),
  and 885.955 (2025 Q4, vintage 2026-02-20;
  `1e7e49c3d4c3468182298f1ec511bb38cafbb1a96d0a83a3f62414b729de01f1`).

Official BEA first-release notices authenticate the three dates; Q3's
shutdown-delayed initial estimate was its first print. Fresh preceding-day
ALFRED parses found each target observation absent, and executable tests check
all six fixture hashes and values. The two BEA admissions now satisfy the
three-first-print gate; all six admissions have integrator-verified anchors.

## Bill pair readiness

At the ingestion layer, `stress-119hr1eh` is the only bill slug that gained
pair-capable outcomes in this wave: section 30D claim count, section 30D credit
amount, ACTC credit amount, private nonresidential fixed investment, and
private R&D fixed investment. The narrower DHS award-transaction series is not
counted as resolving the requested all-account obligations metric; that request
remains open for financial-account submission/TAS adapter and custody work.
This report does not claim that a conditional pair or forecast was registered;
bill-metric wiring, condition selection, and pair preregistration remain
separate reviewed steps.

No admitted series resulted for `stress-119hr1021ih`,
`stress-119hr5595ih`, `stress-119s1188is`, or `stress-119s767is`.

## Ranked next work

With wave 1 complete, the remaining source-family order is:

1. Run `.github/workflows/witness-sba-pdf.yml` until it publishes an eligible
   capture, obtain an available recorder-chain witness, and recheck admission
   for the three disaster-loan performance requests and `stress-119hr1021ih`.
2. Add an IRS individual line-item PDF family for the two section 25E
   requests.
3. Add an IRS corporation line-item PDF family for the two section 45X
   requests.
4. Recheck section 45Y and 48E when a corporation print can expose separate
   fields.
5. Recheck the four new individual deductions when the first applicable SOI
   tables publish.
