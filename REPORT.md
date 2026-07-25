# ALFRED US docket expansion report

## Outcome

The working tree now contains 31 draft series specifications: 28 monthly and
3 quarterly. If admitted, they would take the docket registry from 39 to 70
series, a 79% expansion. The drafting sandbox could not reach the vintage transport, so rows were
drafted `UNVERIFIED`; the integrating session then anchor-verified all 31
through the resolver's own alfredgraph vintage transport (25 at first-print
vintages, 6 with one flagged late-vintage anchor). See `ANCHORS.md`.

No forecasts were run, no `records/` files were changed, and no release date
was guessed. The code changes are deliberately left uncommitted in the
working tree and must not be merged until every retained row has three exact
first-print anchors.

## Drafted series

| Series | Cadence | ALFRED ID | Anchor status | Official release calendar |
|---|---|---:|---|---|
| `fed.g17.industrial_production.total_index_mom` | monthly | `INDPRO` | UNVERIFIED | [Federal Reserve G.17][g17] |
| `fed.g17.manufacturing_production_mom` | monthly | `IPMAN` | UNVERIFIED | [Federal Reserve G.17][g17] |
| `fed.g17.capacity_utilization.total_industry` | monthly | `TCU` | UNVERIFIED | [Federal Reserve G.17][g17] |
| `fed.g17.capacity_utilization.manufacturing` | monthly | `MCUMFN` | UNVERIFIED | [Federal Reserve G.17][g17] |
| `census.housing_starts.saar` | monthly | `HOUST` | UNVERIFIED | [Census economic indicators][census-calendar] |
| `census.housing.permits_saar` | monthly | `PERMIT` | UNVERIFIED | [Census economic indicators][census-calendar] |
| `census.housing.completions_saar` | monthly | `COMPUTSA` | UNVERIFIED | [Census economic indicators][census-calendar] |
| `census.new_residential_sales.new_single_family_houses_sold_saar` | monthly | `HSN1F` | UNVERIFIED | [Census economic indicators][census-calendar] |
| `census.m3.durable_goods_new_orders_mom` | monthly | `DGORDER` | UNVERIFIED | [Census economic indicators][census-calendar] |
| `census.m3.durable_goods_shipments_mom` | monthly | `AMDMVS` | UNVERIFIED | [Census economic indicators][census-calendar] |
| `census.construction_spending.total_mom` | monthly | `TTLCONS` | UNVERIFIED | [Census economic indicators][census-calendar] |
| `census.mtis.total_business_inventories_level` | monthly | `BUSINV` | UNVERIFIED | [Census economic indicators][census-calendar] |
| `bea.trade.goods_services_deficit` | monthly | `BOPGSTB` | UNVERIFIED | [BEA release schedule][bea-calendar] |
| `bls.import_price_index.all_imports_mom` | monthly | `IR` | UNVERIFIED | [BLS import/export prices][bls-ximpim] |
| `bls.export_prices.all_commodities_mom` | monthly | `IQ` | UNVERIFIED | [BLS import/export prices][bls-ximpim] |
| `bls.ppi.final_demand_monthly_change` | monthly | `PPIFIS` | UNVERIFIED | [BLS PPI][bls-ppi] |
| `bls.eci.total_compensation_private_industry_qoq` | quarterly | `ECICOM` | UNVERIFIED | [BLS ECI][bls-eci] |
| `bls.eci.private_wages_salaries_qoq` | quarterly | `ECIWAG` | UNVERIFIED | [BLS ECI][bls-eci] |
| `bls.productivity.nonfarm_unit_labor_costs_qoq_prelim` | quarterly | `PRS85006112` | UNVERIFIED | [BLS Productivity and Costs][bls-productivity] |
| `fed.g19.consumer_credit_total_annual_rate` | monthly | `TOTALSLAR` | UNVERIFIED | [Federal Reserve G.19][g19] |
| `fed.g19.consumer_credit_revolving_annual_rate` | monthly | `REVOLSLAR` | UNVERIFIED | [Federal Reserve G.19][g19] |
| `fed.g19.consumer_credit_nonrevolving_annual_rate` | monthly | `NONREVSLAR` | UNVERIFIED | [Federal Reserve G.19][g19] |
| `bls.cpi.shelter_mom` | monthly | `CUSR0000SAH1` | UNVERIFIED | [BLS CPI][bls-cpi] |
| `bls.cpi.rent_primary_residence_mom` | monthly | `CUSR0000SEHA` | UNVERIFIED | [BLS CPI][bls-cpi] |
| `bls.cpi.owners_equivalent_rent_mom` | monthly | `CUSR0000SEHC` | UNVERIFIED | [BLS CPI][bls-cpi] |
| `bls.cpi.services_less_energy_mom` | monthly | `CUSR0000SASLE` | UNVERIFIED | [BLS CPI][bls-cpi] |
| `bls.cpi.services_less_rent_shelter_mom` | monthly | `CUSR0000SASL2RS` | UNVERIFIED | [BLS CPI][bls-cpi] |
| `bls.jolts.hires_rate` | monthly | `JTSHIR` | UNVERIFIED | [BLS JOLTS][bls-jolts] |
| `bls.ces.average_hourly_earnings_private` | monthly | `CES0500000003` | UNVERIFIED | [BLS Employment Situation][bls-empsit] |
| `bls.lns11300000` | monthly | `CIVPART` | UNVERIFIED | [BLS Employment Situation][bls-empsit] |
| `bls.cps.u6_underemployment_rate` | monthly | `U6RATE` | UNVERIFIED | [BLS Employment Situation][bls-empsit] |

## Other rejected candidates

| Candidate | Reason |
|---|---|
| Existing-home sales (`EXHOSLUSM495S`) | NAR-licensed series with a rolling history; a mechanically auditable official first-print vintage was not demonstrated. |
| Retail-sales control group | No single official FRED/ALFRED series represents the true control group under the existing one-series adapter. `RSFSXMV` is only ex-motor vehicles; `RSXFS` is retail trade; `RSAFS` is total retail and food services. |
| Advance durable-goods variants | `DGORDER` and `AMDMVS` metadata update on the full M3 release. The drafts explicitly target full M3; using them for the earlier advance report is rejected. |
| JOLTS quits rate | Already registered as `bls.jolts.quits_rate`. |
| Nonfarm productivity | Already registered as `bls.productivity.nonfarm_qoq_prelim`. |
| Unit labor cost index (`ULCNFB`) | Its index percent change is not the official annualized quarterly headline. The draft uses direct annual-rate series `PRS85006112` instead. |
| Average weekly hours (`AWHAETP`) | The forecast-cell schema has no semantically correct `hours` unit, and the lane is registry/spec work only. |

## Registry conventions inferred

- A registry-owned source binding has exactly seven template keys:
  `adapter`, `sourceUrl`, `sourceSeriesId`, `field`, `table`, `transform`,
  and `releasePolicy`. Runtime code adds `allowedHosts` and
  `expectedReleaseWindow`.
- The source-binding transform records only the unit multiplier
  (`identity` is represented as `multiply` by 1). The temporal dialect
  (`level`, `mom_diff`, or `pct_change_1d`) remains in
  `ALFRED_ADAPTERS`.
- These monthly and quarterly releases use `first_print`, not the weekly
  claims adapter's `advance_vintage` policy.
- Existing Thesis data-point stems and catalog units were preserved where
  they already existed. In particular, `HOUST` is scaled from thousands to
  millions, `BUSINV` from millions to USD billions, and the negative
  `BOPGSTB` balance is multiplied by `-0.001` to retain Thesis's positive
  trade-deficit convention.
- Registration canonicalizes a new monthly period such as `2030-06` to the
  data-point tail `2030_06`. The resolver parser previously accepted only
  the hyphenated or month-name forms; it now accepts the canonical underscore
  form, and the routing test uses the exact ID produced by registration.
- Durable-goods drafts name the full M3 report rather than the earlier
  advance release. Permits remain a high-risk draft because Census publishes
  a separate revised-permits update.
- Calendar URLs are recorded per series above. No static
  `expectedReleaseDate` was introduced; a future registration must take its
  actual date from the applicable calendar.

## Validation

- `uv run pytest tests/test_resolve_pending.py tests/test_register_targets.py
  tests/test_usaspending_adapter.py -q`: 140 passed. The successful run used
  `UV_NO_SYNC=1` because a normal `uv` sync could not resolve PyPI in the
  network-restricted environment; the same three files also passed directly
  under the installed pytest.
- `python3 -c "import json; json.load(open('scripts/docket_series.json'))"`:
  passed.
- Ruff on the three changed Python files: passed (the repository emitted its
  existing top-level-linter-settings deprecation warning).
- Python syntax plus custom uniqueness, 31-entry agreement, and exact
  seven-key-template checks: passed.
- `git diff --check`: passed.

[g17]: https://www.federalreserve.gov/releases/g17/
[g19]: https://www.federalreserve.gov/releases/g19/
[census-calendar]: https://www.census.gov/economic-indicators/calendar-listview.html
[bea-calendar]: https://www.bea.gov/news/schedule
[bls-cpi]: https://www.bls.gov/schedule/news_release/cpi.htm
[bls-ppi]: https://www.bls.gov/schedule/news_release/ppi.htm
[bls-ximpim]: https://www.bls.gov/schedule/news_release/ximpim.htm
[bls-empsit]: https://www.bls.gov/schedule/news_release/empsit.htm
[bls-jolts]: https://www.bls.gov/schedule/news_release/jolts.htm
[bls-eci]: https://www.bls.gov/schedule/news_release/eci.htm
[bls-productivity]: https://www.bls.gov/schedule/news_release/prod2.htm
