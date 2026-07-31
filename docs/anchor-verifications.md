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

## FSA CRP total enrolled acres (usda.fsa.crp.enrolled_acres_total)

Status: **VERIFIED** (integrator, 2026-07-31). Three anchors read directly
off the official FSA monthly summaries, live-fetched from the statistics
landing page (landing URL and page-1 TOTAL CRP row layout observed as
described below):

- 2025-11: 26,317,011 acres — https://www.fsa.usda.gov/sites/default/files/2026-03/CRPMonthlyNovember2025WithPageNumbers.pdf
- 2026-03: 26,203,615 acres — https://www.fsa.usda.gov/sites/default/files/2026-06/CRPMonthlyMarch2026WithPageNumbers.pdf
- 2026-04: 26,182,019 acres — https://www.fsa.usda.gov/sites/default/files/2026-07/CRPMonthlyApril2026WithPageNumbers.pdf

Protocol notes from the live check: anchor on the printed TOTAL CRP Acres
cell, never derived sums (March cross-foots one acre under the printed
total; FSA sums unrounded acreage). Publication lag is ~3 months (April's
summary posted under /files/2026-07/), which the resolution calendar must
respect. Landing page links dated per-month document pages that carry the
PDF URL, as the selector assumes.
Its `anchors` mapping contains three sentinel entries rather than asserted
acreage values, and the admission test skips while that status remains in
place.

Before changing the status to `VERIFIED`, the integrating session must verify
the FSA Conservation Reserve Program Statistics landing URL and Monthly
Summary total-row layout, capture at least three official published monthly
values, replace all three sentinels with `YYYY-MM`/numeric pairs, and record
the sources here. Runtime resolution will then re-fetch and exactly reproduce
every admitted anchor before it reads a target month.

## CPI-U annual average (bls.cpi.u.annual_pct_change)

The lane pinned 2022=8.0, 2023=4.1, 2024=2.9, 2025=2.6 (annual-average
percent change). The first three match BLS's published annual averages;
all four are recomputed from live monthly data by
`bls_annual_anchor_mismatches` at resolution time, which refuses on drift.

---

# Anchor verifications — ALFRED US docket expansion

Verified 2026-07-25 by the integrating session through the resolver's
own transport (alfredgraph.csv vintage CSV) after the drafting sandbox
could not reach ALFRED. Each series carries three anchors: the value the
adapter produces at a historical vintage inside (or, where flagged, just
after) the period's first-print window, alongside today's revised value.
Every anchor is reproducible by anyone from the same public vintages.
`VERIFIED-LATE-VINTAGE` = one of the three anchors was only reachable at
a vintage past the first-release window and may reflect a revised print;
the transport, series id, and transform are proven regardless, and
forward resolution always captures inside the release window.

| Series | ALFRED id | Status | Anchors (period → first-print @ vintage) |
|---|---|---|---|
| `bea.trade.goods_services_deficit` | `BOPGSTB` | VERIFIED | 2026-02→-57347.0@2026-04-20; 2026-03→-60307.0@2026-05-20; 2026-04→-55881.0@2026-06-20 |
| `bls.ces.average_hourly_earnings_private` | `CES0500000003` | VERIFIED | 2026-03→0.241352@2026-04-30; 2026-04→0.160643@2026-05-31; 2026-05→0.32077@2026-06-30 |
| `bls.cpi.owners_equivalent_rent_mom` | `CUSR0000SEHC` | VERIFIED | 2026-03→0.284067@2026-04-30; 2026-04→0.532661@2026-05-31; 2026-05→0.296783@2026-06-30 |
| `bls.cpi.rent_primary_residence_mom` | `CUSR0000SEHA` | VERIFIED | 2026-03→0.190103@2026-04-30; 2026-04→0.545058@2026-05-31; 2026-05→0.361927@2026-06-30 |
| `bls.cpi.services_less_energy_mom` | `CUSR0000SASLE` | VERIFIED | 2026-03→0.225476@2026-04-30; 2026-04→0.499602@2026-05-31; 2026-05→0.294706@2026-06-30 |
| `bls.cpi.services_less_rent_shelter_mom` | `CUSR0000SASL2RS` | VERIFIED | 2026-03→0.334302@2026-04-30; 2026-04→0.384796@2026-05-31; 2026-05→0.548374@2026-06-30 |
| `bls.cpi.shelter_mom` | `CUSR0000SAH1` | VERIFIED | 2026-03→0.266467@2026-04-30; 2026-04→0.606741@2026-05-31; 2026-05→0.317831@2026-06-30 |
| `bls.cps.u6_underemployment_rate` | `U6RATE` | VERIFIED | 2026-03→8.0@2026-04-30; 2026-04→8.2@2026-05-31; 2026-05→8.1@2026-06-30 |
| `bls.eci.private_wages_salaries_qoq` | `ECIWAG` | VERIFIED-LATE-VINTAGE | 2025-04→1.027939@2025-08-15; 2025-10→0.731049@2026-02-15; 2025-07→0.799696@2025-12-15 ⚠︎late |
| `bls.eci.total_compensation_private_industry_qoq` | `ECICOM` | VERIFIED-LATE-VINTAGE | 2025-04→0.964539@2025-08-15; 2025-10→0.732326@2026-02-15; 2025-07→0.795518@2025-12-15 ⚠︎late |
| `bls.export_prices.all_commodities_mom` | `IQ` | VERIFIED | 2026-03→1.641414@2026-04-30; 2026-04→3.29602@2026-05-31; 2026-05→1.261261@2026-06-30 |
| `bls.import_price_index.all_imports_mom` | `IR` | VERIFIED | 2026-03→0.766551@2026-04-30; 2026-04→1.933702@2026-05-31; 2026-05→1.895735@2026-06-30 |
| `bls.jolts.hires_rate` | `JTSHIR` | VERIFIED | 2026-02→3.1@2026-04-20; 2026-03→3.5@2026-05-20; 2026-04→3.2@2026-06-20 |
| `bls.lns11300000` | `CIVPART` | VERIFIED | 2026-03→61.9@2026-04-30; 2026-04→61.8@2026-05-31; 2026-05→61.8@2026-06-30 |
| `bls.ppi.final_demand_monthly_change` | `PPIFIS` | VERIFIED | 2026-03→0.512332@2026-04-30; 2026-04→1.375897@2026-05-31; 2026-05→1.056336@2026-06-30 |
| `bls.productivity.nonfarm_unit_labor_costs_qoq_prelim` | `PRS85006112` | VERIFIED-LATE-VINTAGE | 2025-04→1.0@2025-09-15; 2025-10→2.8@2026-03-15; 2025-07→-1.9@2026-01-14 ⚠︎late |
| `census.construction_spending.total_mom` | `TTLCONS` | VERIFIED-LATE-VINTAGE | 2026-03→0.564239@2026-05-20; 2026-04→0.366047@2026-06-20; 2026-02→-0.224922@2026-05-20 ⚠︎late |
| `census.housing.completions_saar` | `COMPUTSA` | VERIFIED | 2026-03→1366.0@2026-04-30; 2026-04→1449.0@2026-05-31; 2026-05→1313.0@2026-06-30 |
| `census.housing.permits_saar` | `PERMIT` | VERIFIED | 2026-03→1372.0@2026-04-30; 2026-04→1423.0@2026-05-31; 2026-05→1410.0@2026-06-30 |
| `census.housing_starts.saar` | `HOUST` | VERIFIED | 2026-03→1502.0@2026-04-30; 2026-04→1465.0@2026-05-31; 2026-05→1177.0@2026-06-30 |
| `census.m3.durable_goods_new_orders_mom` | `DGORDER` | VERIFIED | 2026-03→0.832891@2026-04-30; 2026-04→7.946631@2026-05-31; 2026-05→-4.478479@2026-06-30 |
| `census.m3.durable_goods_shipments_mom` | `AMDMVS` | VERIFIED | 2026-03→0.684932@2026-04-30; 2026-04→0.537878@2026-05-31; 2026-05→0.993027@2026-06-30 |
| `census.mtis.total_business_inventories_level` | `BUSINV` | VERIFIED-LATE-VINTAGE | 2026-03→2709734.0@2026-05-20; 2026-04→2726588.0@2026-06-20; 2026-02→2686792.0@2026-05-02 ⚠︎late |
| `census.new_residential_sales.new_single_family_houses_sold_saar` | `HSN1F` | VERIFIED-LATE-VINTAGE | 2026-04→622.0@2026-05-31; 2026-05→580.0@2026-06-30; 2026-02→635.0@2026-05-05 ⚠︎late |
| `fed.g17.capacity_utilization.manufacturing` | `MCUMFN` | VERIFIED | 2026-03→75.2054@2026-04-30; 2026-04→75.6621@2026-05-31; 2026-05→75.5701@2026-06-30 |
| `fed.g17.capacity_utilization.total_industry` | `TCU` | VERIFIED | 2026-03→75.6596@2026-04-30; 2026-04→76.1194@2026-05-31; 2026-05→76.1663@2026-06-30 |
| `fed.g17.industrial_production.total_index_mom` | `INDPRO` | VERIFIED | 2026-03→-0.541507@2026-04-30; 2026-04→0.678054@2026-05-31; 2026-05→0.13511@2026-06-30 |
| `fed.g17.manufacturing_production_mom` | `IPMAN` | VERIFIED | 2026-03→-0.167076@2026-04-30; 2026-04→0.615175@2026-05-31; 2026-05→0.048992@2026-06-30 |
| `fed.g19.consumer_credit_nonrevolving_annual_rate` | `NONREVSLAR` | VERIFIED | 2026-02→2.79@2026-04-20; 2026-03→4.69@2026-05-20; 2026-04→2.88@2026-06-20 |
| `fed.g19.consumer_credit_revolving_annual_rate` | `REVOLSLAR` | VERIFIED | 2026-02→0.64@2026-04-20; 2026-03→9.07@2026-05-20; 2026-04→10.44@2026-06-20 |
| `fed.g19.consumer_credit_total_annual_rate` | `TOTALSLAR` | VERIFIED | 2026-02→2.23@2026-04-20; 2026-03→5.83@2026-05-20; 2026-04→4.85@2026-06-20 |

Raw results: anchor_results.json (kept out of the commit; the table above is the record).

---

# USAspending FY2026 query anchors

Checked 2026-07-24. These are transaction-level, awarding-agency queries for
prime contract award type codes `A`, `B`, `C`, and `D`, with action dates from
2025-10-01 through 2026-09-30. The reviewed source bindings preserve these
query plans in `scripts/docket_series.json`; the resolver reconstructs the
requests from those bindings and refuses any seven-key registry drift.

The current official endpoint contracts confirm that
`/api/v2/search/spending_by_category/recipient/` is a POST endpoint with
recipient IDs and `page_metadata.hasNext`, and that
`/api/v2/search/spending_over_time/` is a POST endpoint returning
`aggregated_amount` by fiscal year:

- https://raw.githubusercontent.com/fedspendingtransparency/usaspending-api/master/usaspending_api/api_contracts/contracts/v2/search/spending_by_category/recipient.md
- https://raw.githubusercontent.com/fedspendingtransparency/usaspending-api/master/usaspending_api/api_contracts/contracts/v2/search/spending_over_time.md

The current official website mapping identifies `small_business` as the
API token for “Small Business”:

- https://github.com/fedspendingtransparency/usaspending-website/blob/master/src/js/dataMapping/search/recipientType.js

## Unique identifiable prime-contract recipients

Endpoint:
`https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/`

Canonical first-page body (subsequent bodies change only `page`):

```json
{"category":"recipient","filters":{"agencies":[{"name":"Department of Defense","tier":"toptier","type":"awarding"}],"award_type_codes":["A","B","C","D"],"time_period":[{"end_date":"2026-09-30","start_date":"2025-10-01"}]},"limit":100,"page":1,"spending_level":"transactions"}
```

Derivation: retrieve pages through the first response with `hasNext: false`,
then count distinct, non-null `results[].recipient_id` values. This excludes
the API’s null-ID aggregate such as `MULTIPLE RECIPIENTS`. The metric therefore
counts identifiable USAspending recipient-profile IDs, not adjudicated legal
entities.

Probe value: **not obtained**. At 2026-07-24T18:03:41Z the exact POST attempt
failed before connection with `Could not resolve host:
api.usaspending.gov`. The separate network runtime also returned `fetch
failed`, and no controllable signed-in browser session was available.

## Small-business share of prime-contract obligations

Endpoint:
`https://api.usaspending.gov/api/v2/search/spending_over_time/`

Canonical denominator body:

```json
{"filters":{"agencies":[{"name":"Department of Defense","tier":"toptier","type":"awarding"}],"award_type_codes":["A","B","C","D"],"time_period":[{"end_date":"2026-09-30","start_date":"2025-10-01"}]},"group":"fiscal_year","spending_level":"transactions"}
```

Canonical numerator body:

```json
{"filters":{"agencies":[{"name":"Department of Defense","tier":"toptier","type":"awarding"}],"award_type_codes":["A","B","C","D"],"recipient_type_names":["small_business"],"time_period":[{"end_date":"2026-09-30","start_date":"2025-10-01"}]},"group":"fiscal_year","spending_level":"transactions"}
```

Derivation: select the unique FY2026 `aggregated_amount` from each response and
compute `100 * numerator / denominator`. The resolver refuses missing,
duplicate, non-finite, negative, zero-denominator, or numerator-above-
denominator inputs.

Probe values:

- All DoD prime-contract obligations: **not obtained**
- Small-business DoD prime-contract obligations: **not obtained**
- Derived share: **not obtained**

The same 2026-07-24 network constraint blocked both exact POSTs. The
brief’s 2026-07-15 `$246.9B` FY2026-to-date reference is deliberately not
carried forward as a current value or substituted for the contract-only
denominator.

## Landing check

Before landing, rerun the three canonical POST bodies above in a networked
review environment and record the timestamped recipient count, numerator,
denominator, and derived percentage here. No code path treats an unverified
anchor as a resolved outcome: the production resolver will run only inside the
preregistered 2026-10-15 through 2026-10-22 snapshot window and archives every
request body and response.

---

# International adapter anchor verification

Verified on 25 July 2026. An adapter is executable only when its parser and
transform reproduce at least three recent official first prints from captured
official response bytes. The `got` column below is the value produced by
`scripts/resolve_pending.py` from the corresponding trimmed fixture in
`tests/fixtures/international/`; it is not copied from the expected value.
Fixture provenance and the SHA-256 of each full archived response are recorded
in `tests/fixtures/international/README.md`.

Aliases that share the same source identifier, parser, transform, and fixture
count as one `(series, adapter)` pair. Five unique pairs (12 data-point-id
stems) pass the admission rule. These fixed periods are immutable admission
evidence, not recurring live sentinels: bounded latest-N responses eventually
age them out. Live execution instead requires the exact response
vector/dataflow/dataset identity, registered unit and binding, official release
window, and (for Eurostat flash) estimate status.

| Pair | Executable stems | Official request | Release calendar |
| --- | --- | --- | --- |
| Statistics Canada CPI all-items YoY | `statcan.cpi.allitems.yoy`; `statcan.cpi.all_items_annual_rate.canada` | WDS vector `41690973` | [Statistics Canada 2026 release dates](https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf) |
| Statistics Canada monthly GDP growth | `statcan.gdp_by_industry.monthly_growth`; `statcan.36-10-0434-01.all_industries.month_to_month_percent_change` | WDS vector `65201210` | [Statistics Canada 2026 release dates](https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf) |
| ABS monthly CPI annual rate | `abs.cpi.all_groups.yoy`; `abs.cpi.all_groups_annual_rate.australia`; `abs.cpi_indicator.allgroups.yoy` | `CPI/3.10001.10.50.M` | [Consumer Price Index, Australia](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia) |
| ABS unemployment rate, seasonally adjusted | `abs.labour.unemployment_rate`; `abs.labour.unemployment_rate.australia` | `LF/M13.3.1599.20.AUS.M` | [Labour Force, Australia](https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia) |
| Eurostat euro-area HICP flash YoY | `eurostat.hicp.flash.yoy`; `eurostat.ea.hicp.flash.yoy`; `eurostat.hicp.all_items_annual_rate.euro_area` | `prc_hicp_minr/M.RCH_A.TOTAL.EA21` | [Euro indicators release calendar](https://ec.europa.eu/eurostat/news/euro-indicators/release-calendar) |

## Verified first prints

| Pair | Period | Expected | Got | Official first-print evidence |
| --- | --- | ---: | ---: | --- |
| Statistics Canada CPI all-items YoY | 2026-02 | 1.8 | 1.8 | [The Daily, 16 March 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260316/dq260316a-eng.htm) |
| Statistics Canada CPI all-items YoY | 2026-03 | 2.4 | 2.4 | [The Daily, 20 April 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260420/dq260420a-eng.htm) |
| Statistics Canada CPI all-items YoY | 2026-04 | 2.8 | 2.8 | [The Daily, 19 May 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260519/dq260519a-eng.htm) |
| Statistics Canada CPI all-items YoY | 2026-05 | 3.2 | 3.2 | [The Daily, 22 June 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260622/dq260622a-eng.htm) |
| Statistics Canada monthly GDP growth | 2026-02 | 0.2 | 0.2 | [The Daily, 30 April 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260430/dq260430a-eng.htm) |
| Statistics Canada monthly GDP growth | 2026-03 | -0.1 | -0.1 | [The Daily, 29 May 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260529/dq260529b-eng.htm) |
| Statistics Canada monthly GDP growth | 2026-04 | 0.5 | 0.5 | [The Daily, 30 June 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260630/dq260630a-eng.htm) |
| ABS monthly CPI annual rate | 2026-02 | 3.7 | 3.7 | [Monthly CPI, February 2026](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/feb-2026) |
| ABS monthly CPI annual rate | 2026-03 | 4.6 | 4.6 | [Monthly CPI, March 2026](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/mar-2026) |
| ABS monthly CPI annual rate | 2026-04 | 4.2 | 4.2 | [Monthly CPI, April 2026](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/apr-2026) |
| ABS monthly CPI annual rate | 2026-05 | 4.0 | 4.0 | [Monthly CPI, May 2026](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/may-2026) |
| ABS unemployment rate, seasonally adjusted | 2026-03 | 4.3 | 4.3 | [Labour Force, March 2026](https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/mar-2026) |
| ABS unemployment rate, seasonally adjusted | 2026-04 | 4.5 | 4.5 | [Labour Force, April 2026](https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/apr-2026) |
| ABS unemployment rate, seasonally adjusted | 2026-05 | 4.4 | 4.4 | [Labour Force, May 2026](https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/may-2026) |
| Eurostat euro-area HICP flash YoY | 2026-04 | 3.0 | 3.0 | [Eurostat flash estimate, 30 April 2026](https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/2-30042026-ap) |
| Eurostat euro-area HICP flash YoY | 2026-05 | 3.2 | 3.2 | [Eurostat flash estimate, 2 June 2026](https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/2-02062026-ap) |
| Eurostat euro-area HICP flash YoY | 2026-06 | 2.8 | 2.8 | [Eurostat flash estimate, 1 July 2026](https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/2-01072026-ap) |

Statistics Canada CPI and ABS original-series CPI are treated as non-revised
apart from explicit corrections. Statistics Canada GDP and ABS Labour Force
can revise: the archived API payload proves parser agreement, the period's
release page establishes the first print, and resolution is limited to the
registered first-print window. Eurostat flash resolution additionally requires
the target observation's estimate flag (`e`); the June fixture retains it.

For recurring docket targets, `scripts/docket_series.json` records exact
period-to-release-date mappings from the calendar linked above. The roller
copies that date into `expectedReleaseDate`; registration creates an exact
one-day release window and refuses native targets without a valid HTTPS
calendar citation. A period missing from the finite published schedule is
skipped rather than extrapolated from cadence.

## Explicitly unverified

ABS published a June 2026 seasonally adjusted unemployment rate of 4.4 on
[23 July 2026](https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/jun-2026),
but the real ABS API response archived on 10 July ends at May. Network access
to `data.api.abs.gov.au` was unavailable after the June release. June is
therefore **UNVERIFIED through the adapter**, has no `got` value, and is not in
the executable adapter's anchor set. No release-page value was projected into
synthetic API JSON.

The following candidate families are also **UNVERIFIED and not executable**.
Candidate metadata or values observed on a current page do not substitute for
three captured first-print payloads.

| Agency | Candidate series | Admission blocker |
| --- | --- | --- |
| Statistics Canada | LFS unemployment rate, LFS employment change, EI regular beneficiaries | Fewer than three captured release-vintage payloads proving first-print extraction for each revision-prone series |
| ABS | Employment change, quarterly CPI, total-dwellings building approvals | No three-period captured fixture set; the approvals release-page snapshot covers only one period |
| Eurostat | Unemployment, industrial production, construction production, retail volume | No three-period captured first-print fixture set for the exact candidate |
| ONS | CPI, claimant count, retail sales, public-sector net borrowing | No captured ONS JSON fixture set; current mutable series are insufficient for revision-prone first prints |
| Statistics Bureau of Japan / e-Stat | Tokyo CPI, national LFS, household spending | The e-Stat JSON API requires an application ID per the [official API documentation](https://www.e-stat.go.jp/api/api/api/index.php/en/api-dev/how_to_use). Per the lane contract, no e-Stat adapter or release-artifact parser was added. |
