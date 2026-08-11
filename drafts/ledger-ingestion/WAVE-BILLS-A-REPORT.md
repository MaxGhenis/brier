# Bills full-coverage Wave A report

Status as of 2026-08-11 UTC: all seven Wave A ingestion requests are
complete. Five have outcome `verified`, one remains `proposed`, and one is
`rejected`. These are request outcomes, not admissions: this wave changes no
docket, adapter, bill, site, or `records/**` artifact.

The linked requests preserve the exact HTTP method, URL, query or request
body, retrieval time, response SHA-256, byte length, and verbatim source
values. A verified outcome means that the official response proves the
narrowly stated series; it does not widen that series to the bill's full
concept or make it bill-attributable.

## Requests and strongest captured evidence

| Request | Bill served | Outcome | Strongest verification artifact captured | Adapter-family disposition |
|---|---|---|---|---|
| [`usaspending-cdfi-fund-program-obligations.json`](usaspending-cdfi-fund-program-obligations.json) | `stress-119s2718is` (S. 2718, CDFI) | Verified | The exact FY2025 USAspending `spending_over_time` POST for CDFI Fund awarding-subagency assistance transactions returned `$319,455,176.00` (1,137 bytes; SHA-256 `ed1225baa11ce0e294590cab40927060f62ebea1df9ea094909b797a0f06f0f1`). This is a CDFI Fund award-transaction context total, not all account obligations and not the assistance S. 2718 would authorize. | **Extend** `usaspending-api`: allow the sealed awarding-subtier filter in `fiscal_year_post_scalar`; no new source family. |
| [`usaspending-ondcp-hidta-program-obligations.json`](usaspending-ondcp-hidta-program-obligations.json) | `stress-119s767is` (S. 767, HIDTA Enhancement) | Verified | The exact FY2025 USAspending POST with `program_numbers=["95.001"]` returned `$271,657,675.60` (1,130 bytes; SHA-256 `5caa8207b4160327a16411454468ccf7383dbde16f47312e311ac7a798898b95`). It is the whole AL 95.001 award-transaction aggregate; the Wave-1 rejection of a section 707(s)-supplemental-specific series still stands. | **Extend** `usaspending-api`: add a sealed `programNumbers` transform and series binding; no new source family. |
| [`usaspending-ntia-broadband-program-obligations.json`](usaspending-ntia-broadband-program-obligations.json) | `stress-119hr2449ih` (H.R. 2449, FUTURE Networks) | Verified | The exact FY2025 USAspending POST with `program_numbers=["11.038"]` returned `$409,852,406.47` (1,132 bytes; SHA-256 `bcda917cb217ca7fb442ff3b32aa291e11696326043d3a33205b66b9ef13cf64`). This is context from an advanced-wireless grant listing, not a 6G Task Force, report, NTIA-subagency, or account-obligation metric. | **Extend** `usaspending-api`: add the sealed program-number transform and series binding; no new source family. |
| [`usaspending-nist-ai-safety-obligations.json`](usaspending-nist-ai-safety-obligations.json) | `frontier-act-hr9925` (Frontier AI Act) | Rejected | The complete FY2025 Commerce federal-account response contained 52 rows and no AI-specific account name (45,002 bytes; SHA-256 `684dec440c360b015fe9129bb191111b09195701c2bfbbc15d76ffdd717d03c8`); both program-activity pages likewise covered all 122 rows with no recorded AI-term match. The only result of the `keywords:["AI safety"]` description-keyword query (USAspending keyword search is Elasticsearch prefix-phrase matching on award text, not an exact-phrase guarantee) was one `$106,412.26` NIST grant under broad AL 11.620, so mutable award-description text cannot define a recurring series. | **Rejected** for `usaspending-api`; reconsider only if a stable structured NIST, ITA, or BIS classifier appears. |
| [`usaspending-usfs-superior-nf-obligations.json`](usaspending-usfs-superior-nf-obligations.json) | `stress-119hr978ih` (H.R. 978, Superior National Forest) | Verified | The exact FY2025 USAspending POST for Forest Service awards with Minnesota place of performance returned `$46,832,556.79` (1,150 bytes; SHA-256 `685c55dd28dc9824d018ce6ebb960d612e3a1d66fb9beb77862b381b47282f20`). USAspending exposes neither a named-forest nor polygon filter, so this is Minnesota-wide context and not Superior National Forest obligations. | **Extend** `usaspending-api`: add sealed awarding-subagency and place-of-performance transforms; no new source family. |
| [`alfred-qcew-childcare-employment.json`](alfred-qcew-childcare-employment.json) | `farm-bill-2-0` (child-care title) | Proposed | The official BLS annual 2025 NAICS 624410 CSV prints `991735` for `annual_avg_emplvl` at `area_fips=US000`, `own_code=5` (537,503 bytes; SHA-256 `a4ebb81ec1159b1c3faa1670a32dc77598cf51178d9e17c630cb289ea568c3a9`). No exact FRED/ALFRED mirror exists, and this current print is not first-print custody. The value is U.S. private employment, not the bill's rural-county panel, all ownerships, slots, or affordability. | **Extend** the existing direct `bls-qcew` family with an annual industry-slice variant, release authentication, first-print custody, and anchors in Wave B. |
| [`bea-ita-personal-transfer-payments-direct.json`](bea-ita-personal-transfer-payments-direct.json) | `stress-119hr5595ih` (H.R. 5595, REMIT) | Verified | The exact official BEA `GetStep` POST for app 62, product 1, Table 5.1, line 18 prints `18,511` million dollars for seasonally adjusted 2026 Q1 personal transfers (16,089 bytes; SHA-256 `d482e10713b19c01824882b6e6f7ee01d06619222d35b27cb6f97fa95fdf0f35`). This is a broad flow proxy, not the bill's taxable base or liability. | **Extend** `bea-release` with an `ita-itable` sibling variant; the NIPA parser cannot be reused unchanged. |

No request fits the **existing** category without follow-up work, and none of
the seven needs an entirely new source family: six need bounded extensions of
reviewed families and the remaining request is rejected. Every proposed
extension still needs implementation, source-linked tests, integrator-verified
anchors, and reviewed docket admission before it can support preregistration
and forecasting.

## Open Wave B work

- **`army-rdte-jbook-pdf` — FLRAA (`stress-119s2075is`).** Fetch and preserve
  at least three official Army RDT&E budget-justification prints; verify PE
  0605241A, project DG5, the exact FLRAA MEDEVAC row, header scale, fiscal-year
  semantics, row continuity, and publication timing; then build the PDF or
  workbook adapter and custody path. Keep it labeled as an execution proxy,
  not delivered capability, cost reduction, or bill attribution.
- **Native EIA vented/flared — FLARE (`stress-119s1188is`).** The official EIA
  series `N9040US2` is exact, but the ALFRED route is rejected because no
  mirror exists. Add an EIA-native API or authenticated-workbook family with
  first-print custody for the annual U.S. vented-and-flared volume.
- **`cms-medicaid-enrollment` — COVER and Safeguarding Medicaid
  (`stress-119hr608ih`, `stress-119s1082is`).** Establish the current official
  Data.Medicaid.gov schema, aggregation and missing-state rules, preliminary
  versus updated vintage policy, release timing, and three first-print anchors
  before admitting any enrollment or eligibility-operation series. Treat a
  broad enrollment series as context only; do not relabel it as COVER
  demonstration enrollment, asset checks, savings, or a bill-caused change.
- **U.S. Drought Monitor weekly — `farm-bill-2-0` water title.** Identify the
  exact recurring official weekly measure and unit, preserve the exact source
  query or artifact, authenticate release timing and first prints, and add a
  reviewed weekly resolver family. Do not substitute a broad drought headline
  or infer a release day from cadence.
- **Direct BLS QCEW annual slice — `farm-bill-2-0` child-care title.** Complete
  the annual `/a/industry/624410.csv` extension and first-print custody listed
  in the request table; preserve the narrower U.S.-private-employment scope.

Wave B admission work must also finish the bounded USAspending and BEA family
extensions listed in the table. Nothing in this report claims that any bill
pair has been registered or forecast.
