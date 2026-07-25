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
