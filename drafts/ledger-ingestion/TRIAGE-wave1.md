# Workbook triage — ingestion wave 1

Fetched evidence in this table was retrieved from the official publishers on
2026-08-06 UTC. Research copies stayed under `/tmp`; this file records only the
URLs, hashes, cells, and results needed to reproduce the ranking.

## Score

Each request receives `B + F + C` points:

- `B` (0–3): number of distinct `billSlugs` unblocked, capped at 3. Every
  request in this batch has one bill slug, so every row receives 1.
- `F` (0–4): parse feasibility. `4` means the exact cell works with the current
  IRS Table 3.3 claimant-count parser by changing only its spec; `3` means the
  same workbook/row/header idiom reaches the exact cell but the parser must be
  parameterized for an amount subcolumn and a series-specific transform; `2`
  means a modest layout extension inside the existing workbook family; `1`
  means an exact value is public but only in an incompatible or rolling
  artifact; `0` means no separate current field exists.
- `C` (0–2): release usefulness. `2` means at least quarterly publication with
  completed fiscal-year columns; `1` means a recurring annual tax-year print;
  `0` means no cadence for the exact requested field has yet been evidenced.

Ties use the request filename in ascending lexical order. This matters at the
top-five cutoff: all three SBA requests score 4, so the two `charge-off-*`
requests rank ahead of `post-charge-off-recovery`.

The top-five label is a mechanical triage rank, not an admission decision.
Ranks 4 and 5 score well on cadence but fail the existing-family constraint:
their only live artifacts are rolling PDFs with no authenticated first-print
archive. Therefore this cohort produces three clean admissions, not five.

## Ranking

| Rank | Top 5 | Request | B | F | C | Total | Fetched result and reason |
|---:|:---:|---|---:|---:|---:|---:|---|
| 1 | **TOP 5** | `irs-soi-credit-30d-total-claims.json` | 1 | 4 | 1 | **6** | Clean. TY2023 Table 3.3 `TBL33`, `All returns, total`, `AE10` prints **493,953** under `Clean vehicle credit / Number of returns`; three earlier tax-year files expose the same section under `Qualified plug-in electric vehicle credit`. |
| 2 | **TOP 5** | `irs-actc-total-credit-amount.json` | 1 | 3 | 1 | **5** | Clean. TY2023 Table 3.3 `TBL33`, `AN10` prints **34,533,251 thousand dollars**, or **34,533.251 USD millions**, under the same ACTC header and all-returns row already used by the admitted count series. |
| 3 | **TOP 5** | `irs-soi-credit-30d-total-credit-amount.json` | 1 | 3 | 1 | **5** | Clean. TY2023 Table 3.3 `TBL33`, `AF10` prints **3,231,102 thousand dollars**, or **3,231.102 USD millions**, beside the verified section 30D count cell. |
| 4 | **TOP 5** | `sba-disaster-loan-program-charge-off-amount.json` | 1 | 1 | 2 | **4** | Blocked for this wave. SBA Table 5 page 1 prints Disaster FY2024 **$299,971,326**, but the live product is a rolling ZIP of PDFs, not a workbook; it says prior years may be adjusted and exposes no first-print archive. The IRS `.xls` family cannot parse or authenticate it. |
| 5 | **TOP 5** | `sba-disaster-loan-program-charge-off-rate-upb.json` | 1 | 1 | 2 | **4** | Blocked for this wave. SBA Table 9 page 1 prints Disaster FY2024 **3.06%**, but it has the same rolling-PDF, revision, and first-print-custody mismatch as rank 4. |
| 6 |  | `sba-disaster-loan-program-post-charge-off-recovery.json` | 1 | 1 | 2 | **4** | Exact current value exists: SBA Table 7 page 1 prints Disaster FY2024 **$126,510,000**. It ranks below the equal-scoring cutoff by filename and needs the same new SBA PDF/custody family. |
| 7 |  | `irs-soi-credit-25e-total-claims.json` | 1 | 1 | 1 | **3** | Exact value exists, but not in the workbook family. TY2023 Table 3.3 footnote `A49` folds 25E into `Other nonrefundable credits`; the separately published Publication 4801 PDF prints Schedule 3 line 6m at **31,992 returns** on PDF page 31. A new PDF/custody parser would be required. |
| 8 |  | `irs-soi-credit-25e-total-credit-amount.json` | 1 | 1 | 1 | **3** | Publication 4801 separately prints Schedule 3 line 6m at **96,013 thousand dollars** on PDF page 32, but Table 3.3's `T10` is the combined **12,662,360 thousand dollars** aggregate. The exact field is annual but outside the admitted `.xls` parser. |
| 9 |  | `irs-soi-credit-45x-total-claims.json` | 1 | 1 | 1 | **3** | Exact but PDF-only. TY2022 Publication 5108 Form 3800 line 1b prints **9** returns for `Advanced manufacturing production (Form 7207)` on PDF page 167; the asterisk marks a small-sample estimate. The current Table 11 workbook has only aggregate `General business credit`. |
| 10 |  | `irs-soi-credit-45x-total-credit-amount.json` | 1 | 1 | 1 | **3** | TY2022 Publication 5108 Form 3800 line 1b prints **317,505 thousand dollars** on PDF page 168, again small-sample marked, while the workbook has no section-specific cell. This needs an IRS line-item PDF family, not a Table 3.3 spec. |
| 11 |  | `irs-soi-credit-45y-total-claims.json` | 1 | 0 | 0 | **1** | Latest fetched TY2022 corporation workbook has no separately printed section 45Y claim count. |
| 12 |  | `irs-soi-credit-45y-total-credit-amount.json` | 1 | 0 | 0 | **1** | Latest fetched TY2022 corporation workbook has no separately printed section 45Y amount. |
| 13 |  | `irs-soi-credit-48e-total-claims.json` | 1 | 0 | 0 | **1** | Latest fetched TY2022 corporation workbook has no separately printed section 48E claim count. |
| 14 |  | `irs-soi-credit-48e-total-credit-amount.json` | 1 | 0 | 0 | **1** | Latest fetched TY2022 corporation workbook has no separately printed section 48E amount. |
| 15 |  | `irs-soi-overtime-deduction-total-claims.json` | 1 | 0 | 0 | **1** | Latest fetched individual Table 3.3 is TY2023 and has no qualified-overtime deduction field; the guessed TY2024 workbook URL returned HTTP 404 this session. |
| 16 |  | `irs-soi-overtime-deduction-total-deduction-amount.json` | 1 | 0 | 0 | **1** | Latest fetched individual Table 3.3 has no qualified-overtime deduction amount or evidenced field cadence. |
| 17 |  | `irs-soi-senior-deduction-total-claims.json` | 1 | 0 | 0 | **1** | Latest fetched individual Table 3.3 has no senior-deduction claimant field. |
| 18 |  | `irs-soi-senior-deduction-total-deduction-amount.json` | 1 | 0 | 0 | **1** | Latest fetched individual Table 3.3 has no senior-deduction amount field. |
| 19 |  | `irs-soi-tip-deduction-total-claims.json` | 1 | 0 | 0 | **1** | Latest fetched individual Table 3.3 has no qualified-tips deduction claimant field. |
| 20 |  | `irs-soi-tip-deduction-total-deduction-amount.json` | 1 | 0 | 0 | **1** | Latest fetched individual Table 3.3 has no qualified-tips deduction amount field. |
| 21 |  | `irs-soi-vehicle-interest-deduction-total-claims.json` | 1 | 0 | 0 | **1** | Latest fetched individual Table 3.3 has no vehicle-loan-interest deduction claimant field. |
| 22 |  | `irs-soi-vehicle-interest-deduction-total-deduction-amount.json` | 1 | 0 | 0 | **1** | Latest fetched individual Table 3.3 has no vehicle-loan-interest deduction amount field. |

## Artifact pins

- IRS individual TY2023 Table 3.3:
  `https://www.irs.gov/pub/irs-soi/23in33ar.xls`, SHA-256
  `e749d3e9636d9784e2a5e8639f49ce5389a4ca0aaeedca6c671cee0b71264c04`,
  fetched `2026-08-06T20:01:23Z` (105,472 bytes).
- IRS Corporation TY2022 Table 11:
  `https://www.irs.gov/pub/irs-soi/22co11ccr.xlsx`, SHA-256
  `f12271cd6507efec4f4bd5b9ce4095e83d3c3ba1c4b5a797dc734c2be08c5fdc`,
  fetched `2026-08-06T20:01:23Z` (79,191 bytes). The prospective TY2023
  workbook URL returned HTTP 404; IRS schedules the TY2023 corporation tables
  for 2026-09-23.
- IRS individual TY2023 Line Item Estimates (Publication 4801):
  `https://www.irs.gov/pub/irs-pdf/p4801.pdf`, SHA-256
  `49686f6c909452bc775bed40f10a633629e8ce486d7f47ee131cb093d1d04d81`,
  fetched `2026-08-06T20:06:57Z` (4,228,018 bytes). This is the PDF-only 25E
  evidence; it is not an admission artifact for the workbook family.
- IRS Corporation TY2022 Line Item Estimates (Publication 5108):
  `https://www.irs.gov/pub/irs-pdf/p5108.pdf`, SHA-256
  `0c7516d5a784a24f51522bd3cf5358bbed735c031e54ba56c87bad831a873855`,
  fetched `2026-08-06T20:07:14Z` (4,639,023 bytes). This is the PDF-only 45X
  evidence; IRS schedules the TY2023 edition for 2026-09-30.
- SBA FY2025 Q3 container:
  `https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip`,
  SHA-256
  `51d5571d03d028d5efd4b8b9c8d7984f55285d36202eb8f67afe8a3476bb1242`,
  fetched `2026-08-06T20:01:23Z` (1,296,419 bytes). The embedded Table 5,
  Table 9, and Table 7 PDF hashes are respectively
  `b3f352425adcc3304cbcc406d63a2ced149bc8224f3b604c2b47403edc9070f3`,
  `23ab3dc1d37dc08be200b8076d07371b1ac901730e1828a697278bf279a1d762`,
  and `09616e8af327a6ea8e3bbc340e44392bbead98e581a9f85a7de99ef8b81e380f`.

The original `www.sba.gov` download link returned HTTP 404 during this
session; the official page redirects to `legacy.sba.gov`, where the identical
relative asset path returned the ZIP above.
