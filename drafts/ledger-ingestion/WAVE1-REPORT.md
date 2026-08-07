# Ingestion wave 1 report

Status as of 2026-08-06: triage and request verification are complete, three
IRS workbook series, one USAspending series, and one BEA series are admitted;
one verified quick-series admission remains to close the mission. No
`records/**` artifact is part of this work.

## Outcome summary

The wave covered 30 requests: eight ALFRED/USAspending quick requests and 22
workbook-triage requests. Six requests verified cleanly, seven received a
terminal rejection for the proposed adapter family, and 17 remain proposals
for a later source family or future official print. Of the six verified
requests, five are in the docket today and one still needs admission wiring.

### Quick requests

| Request | Outcome | Reason |
|---|---|---|
| `bea-ita-personal-transfer-payments.json` | Rejected | No exact current FRED/ALFRED series; the candidates are broader or discontinued. |
| `bea-private-nonresidential-fixed-investment.json` | Admitted | `PNFI` matches the concept, quarterly cadence, nominal SAAR basis, and unit; its first-print fixture and BEA release date are hash-pinned. |
| `bea-research-and-development-fixed-investment.json` | Verified; admission pending | `Y006RC1Q027SBEA` matches the concept, quarterly cadence, nominal SAAR basis, and unit, with an ALFRED vintage observation and a dated BEA release. |
| `eia-natural-gas-vented-flared-us-annual.json` | Rejected | The official EIA series is exact, but FRED/ALFRED has no mirror and therefore cannot provide first-print vintages. |
| `usaspending-dhs-title-vi-named-account-obligations.json` | Admitted | The exact six-component Treasury-account query returned a reproducible FY2026 total of $32,171,899,636.26. |
| `usaspending-energy-commerce-title-iv-named-account-obligations.json` | Rejected | Live identifiers do not cover all named Title IV programs, so the query would measure only part of the concept. |
| `usaspending-ondcp-hidta-supplemental-grant-obligations.json` | Rejected | Assistance Listing 95.001 cannot distinguish the section 707(s) supplemental grants from broader HIDTA activity. |
| `usaspending-usda-selected-rural-program-obligations.json` | Rejected | The requested Supplemental Agricultural Trade Promotion identifier is absent; the available similarly named program is a different concept. |

### Workbook requests

The detailed scoring, artifact hashes, exact cells, and tie-break rule are in
[`TRIAGE-wave1.md`](TRIAGE-wave1.md).

| Rank | Request | Outcome |
|---:|---|---|
| 1 | `irs-soi-credit-30d-total-claims.json` | Admitted from Table 3.3; TY2023 first print is 493,953 returns. |
| 2 | `irs-actc-total-credit-amount.json` | Admitted from Table 3.3; TY2023 first print is $34,533.251 million. |
| 3 | `irs-soi-credit-30d-total-credit-amount.json` | Admitted from Table 3.3; TY2023 first print is $3,231.102 million. |
| 4 | `sba-disaster-loan-program-charge-off-amount.json` | Rejected for this family: the exact value is in a rolling, revisable PDF bundle without first-print custody. |
| 5 | `sba-disaster-loan-program-charge-off-rate-upb.json` | Rejected for this family for the same rolling-PDF and first-print-custody mismatch. |
| 6 | `sba-disaster-loan-program-post-charge-off-recovery.json` | Deferred to a new SBA PDF/custody family. |
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

The current admitted count is **5**:

- `irs.soi.credit_30d.total_claims`
- `irs.actc.total_credit_amount`
- `irs.soi.credit_30d.total_credit_amount`
- `usaspending.dhs.title_vi.named_account_obligations`
- `bea.private_nonresidential_fixed_investment`

The three IRS series each have an `irs-soi-pub1304` resolver spec and a 2027
annual docket entry using the reviewed `resolve-by-bound` contract. Their
tests use the real TY2020–TY2023 workbook bytes; the TY2023 fixture is 105,472
bytes with SHA-256
`e749d3e9636d9784e2a5e8639f49ce5389a4ca0aaeedca6c671cee0b71264c04`.
The DHS series has an exact `usaspending-api` POST plan and FY2026 registered
snapshot window. Its unmodified 1,146-byte fixture has SHA-256
`dd51e2eb947fc8b302fe9c33297c85989b542c933801dcb0729edf39ba157720`.
The BEA series has an identity `alfred-fred` resolver spec and a quarterly
release-calendar seed. Its unmodified 51-byte first-print fixture has SHA-256
`05b9718a7ab180b5f8aa5028dbdc04291f5e76c69ebacd0214239d5c57d4df92`.
All five admissions have integrator-verified anchors.

The following verified requests are not included in that admitted count and
remain wave-1 closure work:

1. `bea.research_and_development_fixed_investment`

## Bill pair readiness

At the ingestion layer, `stress-119hr1eh` is the only bill slug that gained
pair-capable outcomes in this wave: section 30D claim count, section 30D credit
amount, ACTC credit amount, DHS Title VI named-account obligations, and private
nonresidential fixed investment. This report does not claim that a conditional
pair or forecast was registered;
bill-metric wiring, condition selection, and pair preregistration remain
separate reviewed steps.

No admitted series resulted for `stress-119hr1021ih`,
`stress-119hr5595ih`, `stress-119s1188is`, or `stress-119s767is`.

## Ranked next work

Before declaring wave 1 complete, admit the verified BEA research and
development fixed-investment series. It still needs a real hash-pinned ALFRED
fixture plus registry, adapter, anchor, and selection tests.

After that closure work, the next source-family order is:

1. Add reviewed SBA PDF parsing and first-print custody, covering the three
   disaster-loan performance requests and `stress-119hr1021ih`.
2. Add an IRS individual line-item PDF family for the two section 25E
   requests.
3. Add an IRS corporation line-item PDF family for the two section 45X
   requests.
4. Recheck section 45Y and 48E when a corporation print can expose separate
   fields.
5. Recheck the four new individual deductions when the first applicable SOI
   tables publish.
