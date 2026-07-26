# Recurring docket seeds

Verified on 2026-07-25. Each row is the next reference period whose official
print had not yet been released, paired with the agency's published release
date for exactly that period. The registry stores these values as
`seedPeriod`, `releaseDates[seedPeriod]`, and `releaseCalendarUrl`.

The baseline dry-run printed 63 `no published cell to step from` messages, but
that message covered two different states. After recognizing the legacy
abbreviated-month slug for `bls.lns11300000`, 21 recurring entries have no
published cursor, while 42 already-published entries merely have no successor
inside the period horizon. Only the 21 genuinely cursorless entries below
receive recurring seeds. The six annual USAspending entries already use the
separate reviewed `registered_query_snapshot` seed contract.

| Series | Seed period | Release date | Official calendar |
|---|---:|---:|---|
| `fed.g17.manufacturing_production_mom` | `2026-07` | 2026-08-18 | [Federal Reserve G.17 release dates](https://www.federalreserve.gov/releases/g17/release_dates.htm) |
| `fed.g17.capacity_utilization.manufacturing` | `2026-07` | 2026-08-18 | [Federal Reserve G.17 release dates](https://www.federalreserve.gov/releases/g17/release_dates.htm) |
| `census.housing.permits_saar` | `2026-07` | 2026-08-18 | [Census Survey of Construction schedule](https://www.census.gov/construction/soc/schedule.html) |
| `census.housing.completions_saar` | `2026-07` | 2026-08-18 | [Census Survey of Construction schedule](https://www.census.gov/construction/soc/schedule.html) |
| `census.m3.durable_goods_new_orders_mom` | `2026-06` | 2026-07-27 | [Census M3 release schedule](https://www.census.gov/manufacturing/m3/release_schedule.html) |
| `census.m3.durable_goods_shipments_mom` | `2026-06` | 2026-07-27 | [Census M3 release schedule](https://www.census.gov/manufacturing/m3/release_schedule.html) |
| `census.construction_spending.total_mom` | `2026-06` | 2026-08-03 | [Census Construction Spending schedule](https://www.census.gov/construction/c30/release.html) |
| `bls.export_prices.all_commodities_mom` | `2026-07` | 2026-08-18 | [BLS Import/Export Price Index schedule](https://www.bls.gov/schedule/news_release/ximpim.htm) |
| `bls.eci.total_compensation_private_industry_qoq` | `2026-Q2` | 2026-07-31 | [BLS Employment Cost Index schedule](https://www.bls.gov/schedule/news_release/eci.htm) |
| `bls.eci.private_wages_salaries_qoq` | `2026-Q2` | 2026-07-31 | [BLS Employment Cost Index schedule](https://www.bls.gov/schedule/news_release/eci.htm) |
| `bls.productivity.nonfarm_unit_labor_costs_qoq_prelim` | `2026-Q2` | 2026-08-06 | [BLS Productivity and Costs schedule](https://www.bls.gov/schedule/news_release/prod2.htm) |
| `fed.g19.consumer_credit_total_annual_rate` | `2026-06` | 2026-08-07 | [Federal Reserve August 2026 calendar](https://www.federalreserve.gov/newsevents/2026-august.htm) |
| `fed.g19.consumer_credit_revolving_annual_rate` | `2026-06` | 2026-08-07 | [Federal Reserve August 2026 calendar](https://www.federalreserve.gov/newsevents/2026-august.htm) |
| `fed.g19.consumer_credit_nonrevolving_annual_rate` | `2026-06` | 2026-08-07 | [Federal Reserve August 2026 calendar](https://www.federalreserve.gov/newsevents/2026-august.htm) |
| `bls.cpi.shelter_mom` | `2026-07` | 2026-08-12 | [BLS Consumer Price Index schedule](https://www.bls.gov/schedule/news_release/cpi.htm) |
| `bls.cpi.rent_primary_residence_mom` | `2026-07` | 2026-08-12 | [BLS Consumer Price Index schedule](https://www.bls.gov/schedule/news_release/cpi.htm) |
| `bls.cpi.owners_equivalent_rent_mom` | `2026-07` | 2026-08-12 | [BLS Consumer Price Index schedule](https://www.bls.gov/schedule/news_release/cpi.htm) |
| `bls.cpi.services_less_energy_mom` | `2026-07` | 2026-08-12 | [BLS Consumer Price Index schedule](https://www.bls.gov/schedule/news_release/cpi.htm) |
| `bls.cpi.services_less_rent_shelter_mom` | `2026-07` | 2026-08-12 | [BLS Consumer Price Index schedule](https://www.bls.gov/schedule/news_release/cpi.htm) |
| `bls.jolts.hires_rate` | `2026-06` | 2026-08-04 | [BLS JOLTS schedule](https://www.bls.gov/schedule/news_release/jolts.htm) |
| `bls.cps.u6_underemployment_rate` | `2026-07` | 2026-08-07 | [BLS Employment Situation schedule](https://www.bls.gov/schedule/news_release/empsit.htm) |

## Calendar interpretation

- Census M3 rows use the 2026-07-27 advance report because it is the first
  print for both durable-goods new orders and shipments. Their registry
  bindings name that advance report explicitly.
- The BLS productivity row uses the preliminary (`P`) second-quarter release
  on 2026-08-06, matching the registry's `qoq_prelim` contract.
- The Federal Reserve's August calendar identifies G.19 on 2026-08-07 and
  G.17 on 2026-08-18. The dedicated G.17 schedule independently lists the
  same August date.

No cursorless recurring series was omitted for lack of a verifiable calendar.
`bls.lns11300000` is intentionally not seeded: the witnessed catalog already
contains its December 2026 published cell, whose `dec` slug is now recognized
by the ordinary cursor.
