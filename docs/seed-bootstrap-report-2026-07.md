# Recurring seed bootstrap report

## Outcome

The recurring docket now has a fail-closed bootstrap path for registry entries
that have no published cursor. On the 2026-07-25 witnessed Thesis Log snapshot,
the eligible target count rises from **5 to 26**: the same 5 cursor-driven
targets plus 21 reviewed recurring seeds.

The baseline's 63 `no published cell to step from` messages overstated the
cursorless population. The old message was also printed when a series had a
published cursor but its successor was outside the period horizon. The
witnessed catalog contains:

- 68 recurring registry entries;
- 47 with a published cursor, of which 5 are eligible on 2026-07-25;
- 21 with no published cursor, all 21 now seeded from official calendars;
- 6 annual USAspending entries, which retain their separate reviewed
  `registered_query_snapshot` path.

Recurring seeds therefore apply only to the actual no-cursor set. They do not
override or supplement any published cursor. The published
`labor-force-participation-dec-2026` cell is recognized through an explicit
abbreviated-month slug template and is not seeded.

## Implementation

`scripts/roll_docket.py` adds `recurring_seed_target`, which admits a target
only when all of these conditions hold:

- no slug matching the series template has been published;
- `seedPeriod` is canonical for the entry's cadence and inside the normal
  period horizon;
- `releaseDates[seedPeriod]` is a valid date strictly after the docket date
  and no more than 75 days ahead;
- `releaseCalendarUrl` is an HTTPS URL;
- the canonical seed slug is absent from the catalog.

The emitted target carries `expectedReleaseDate` and
`releaseCalendarUrl`. Its `seedPeriod` marker enters the immutable registration
content hash. The privileged bind step consequently rechecks the exact
one-day window, calendar URL, seed period, and source-binding template against
the committed registry after any rebase. No workflow authority or source
binding was weakened.

Once a seed slug appears in the live catalog, `recurring_seed_target` refuses
it and the existing published-period cursor produces the next period. The seed
is never cadence-stepped and cannot re-fire after publication. Before
selection is capped, recurring seeds sort by exact release date ahead of
ordinary cursor targets so a busy docket cannot defer them past release.

## Seed coverage

`docs/seed-verifications.md` records every series, seed period, exact future release date, and
official calendar URL. Coverage is complete for the 21 cursorless recurring
entries:

- 11 BLS series across ECI, JOLTS, Productivity and Costs, Employment
  Situation, CPI, and Import/Export Price Index schedules;
- 5 Census series across New Residential Construction, advance M3, and
  Construction Spending schedules;
- 5 Federal Reserve series across G.17 and G.19.

No date was inferred from cadence and no cursorless recurring series was
omitted for lack of an official calendar.

The two M3 seeds are due on Monday, 2026-07-27. Because this lane must not
commit, push, or dispatch workflows, the integrator must land and manually
dispatch them before that date; on or after release day the strict chronology
guard correctly refuses them rather than backfilling a forecast.

## Verification

- Required gate:
  `UV_NO_SYNC=1 uv run pytest tests/test_roll_docket.py
  tests/test_register_targets.py tests/test_resolve_pending.py
  tests/test_usaspending_adapter.py -q` — **231 passed**.
- Focused docket tests — **47 passed**. They cover initial admission, exact
  registration windows, post-publication handoff, capped release-date
  priority, malformed metadata, existing slugs, the legacy abbreviated-month
  cursor, and all 21 real registry rows.
- Registration tests include bind-level tamper cases for the seed period,
  one-day release window, calendar URL, source-binding template, and missing
  docket authority.
- Offline dry-run against the repository's latest witnessed Thesis Log
  snapshot:
  `python3 scripts/roll_docket.py --dry-run --max-targets 80` with only the
  catalog loader redirected to the witnessed bytes — **26 targets**, versus
  the **5-target baseline** from the same snapshot.
- The same witnessed snapshot under the workflow's production
  `--max-targets 10` cap selects the 10 earliest-due seeds first.
- Direct network dry-run — blocked before selection because this sandbox
  cannot resolve `app.thesisinstitute.org`; no fallback date or catalog state
  was guessed.
- `ruff check` over the changed Python and test files — passed.
- JSON parse of `scripts/docket_series.json` — passed.
- `git diff --check` — passed.
- No file under `records/` was modified. No commit or push was made.

---

# ALFRED US docket expansion report

## Outcome

The working tree now contains 31 draft series specifications: 28 monthly and
3 quarterly. If admitted, they would take the docket registry from 39 to 70
series, a 79% expansion. The drafting sandbox could not reach the vintage transport, so rows were
drafted `UNVERIFIED`; the integrating session then anchor-verified all 31
through the resolver's own alfredgraph vintage transport (25 at first-print
vintages, 6 with one flagged late-vintage anchor). See `docs/anchor-verifications.md`.

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
| Advance durable-goods variants | The initial draft incorrectly treated `DGORDER` and `AMDMVS` as full-report-only. The reviewed seed correction binds both to Census's 2026-07-27 advance report, which is their first print. |
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
- The recurring-seed review supersedes the draft's full-M3 assumption:
  `DGORDER` and `AMDMVS` now name the advance report that provides their first
  print. Permits remain a high-risk draft because Census publishes a separate
  revised-permits update.
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

---

# International resolver adapters report

## Outcome

This lane adds fail-closed native resolution infrastructure for Statistics
Canada, ABS, Eurostat, and ONS. Five unique series/adapter pairs, represented
by 12 data-point-id stems, pass the mandatory three-first-print fixture gate
and are executable. Unverified candidates remain visible but unclaimed in
`INTL_BLOCKED_ADAPTERS`.

The recurring path is operational for binding-compatible targets:

- the docket supplies an agency-calendar date for the exact reference period;
- registration refuses native targets without that date and its HTTPS calendar
  citation, creates an exact one-day window, and uses the canonical docket
  series as the new data-point-id stem;
- the resolver verifies contract bytes, response source identity, unit,
  release date/window, transform, and first-print status before producing a
  fact;
- the site accepts the one reviewed legacy descriptive id stem only under its
  exact target id and content hash, while its parser-derived projection still
  has to match the canonical registered series.

One of the five existing admitted-stem registrations has a separately
reviewed, exact-hash legacy executor. Four older registrations remain
deliberately blocked because their immutable contracts are contradictory or
cannot be satisfied. The lane does not weaken registration checks to make
them pass.

## Implementation

`scripts/resolve_pending.py` now provides:

- Statistics Canada WDS POST parsing for a single pinned vector;
- ABS SDMX-JSON parsing for one exact dataflow and full dimension key;
- Eurostat JSON-stat parsing for one exact dataset/key, including flash
  estimate flags;
- ONS time-series JSON parsing, including ONS three-letter monthly labels;
- candidate ABS/Eurostat release-page parsers, kept non-executable until their
  own fixture admission;
- exact unit/range/transform checks and correct two-row lineage for derived
  month-over-month and year-over-year values;
- HTTPS request and redirect allowlists, archived response bytes, and refusal
  when the registered seven-key source binding drifts;
- immutable fixture anchors for admission, while durable response identity,
  unit, release-window, and status checks gate recurring live execution. Fixed
  2026 anchors are not required to remain forever in bounded latest-N
  responses.

`scripts/roll_docket.py` now copies exact period-keyed official dates into
native targets, advances past periods whose release date has already passed,
and skips a period when the finite published schedule has no entry. This
prevents a post-release run from preregistering an already observed outcome.
`scripts/register_targets.py` refuses cadence-inferred native windows,
requires exactly one committed docket source-binding template whose calendar
agrees with the contract, and canonicalizes new native data-point ids.
`scripts/prospect_targets.py` and the site source-binding types recognize the
native adapter names.

## Executable coverage

| Agency | Admitted unique series | Native adapter | Executable stems |
| --- | --- | --- | ---: |
| Statistics Canada | CPI all-items YoY; monthly GDP growth | `statcan-wds` | 4 |
| ABS | Monthly CPI annual rate; seasonally adjusted unemployment rate | `abs-data-api` | 5 |
| Eurostat | Euro-area HICP flash annual rate | `eurostat-api` | 3 |
| ONS | None yet | Candidate `ons-timeseries` implementation only | 0 |
| Japan | None | Skipped: no keyless e-Stat JSON path | 0 |

## Anchor summary

The detailed expected-versus-got table and every official release link are in
`docs/anchor-verifications.md`. All results below are reproduced by the parser from real,
trimmed official response bytes whose original archive hashes are recorded in
`tests/fixtures/international/README.md`.

| Pair | Periods checked | Checks | Result |
| --- | --- | ---: | --- |
| Statistics Canada CPI all-items YoY | 2026-02 through 2026-05 | 4 | exact at published 0.1-point precision |
| Statistics Canada monthly GDP growth | 2026-02 through 2026-04 | 3 | exact at published 0.1-point precision |
| ABS monthly CPI annual rate | 2026-02 through 2026-05 | 4 | exact at published 0.1-point precision |
| ABS unemployment rate, SA | 2026-03 through 2026-05 | 3 | exact after published one-decimal rounding |
| Eurostat euro-area HICP flash YoY | 2026-04 through 2026-06 | 3 | exact; June retains estimate flag `e` |

The authentic ABS Labour Force response archived on 10 July ends at May.
June was dropped from admission rather than represented with synthetic API
bytes.

## Official release calendars

Each admitted registry series carries `releaseCalendarUrl` and a finite
`releaseDates` mapping:

- Statistics Canada CPI and GDP use the agency's 2026–27 release-date PDF;
- ABS CPI and Labour Force use their official release pages/calendars;
- Eurostat HICP flash uses the Euro indicators calendar.

The roller inserts `expectedReleaseDate`; registration makes
`expectedReleaseWindow.start == expectedReleaseWindow.end ==` that date.
Missing dates, a missing/ambiguous committed series entry, or a date that
disagrees with the committed docket fail closed. Already released periods are
advanced before target creation. This replaces monthly cadence extrapolation
for native international targets.

## Existing-registration audit

### Reviewed legacy executor

`abs.labour.unemployment_rate.australia.july_2026.first_print` is admitted
only under registration hash
`cf3a2f76bb15d9f5eb9f5ae19d2e96b55111cf6842a1c8c8412b915ae614a85b`.
The code checks the complete contract as well as the hash, fetches its exact
registered ABS Data API URL/key, parses the exact dimensions, and uses its
19–27 August window. The official 20 August release lies inside that window.
Any changed field, host, URL, period, unit, transform, or hash refuses.

### Still blocked

| Existing target | Why native execution is unsafe |
| --- | --- |
| `abs.cpi.all_groups.yoy.2026-07.first_print` | The immutable contract names a June release page and generic series identity for a July monthly target. |
| `abs.cpi.all_groups_annual_rate.australia.june_2026.first_print` | Its API identity is otherwise compatible, but the registered window ends 28 July while the official and forecast release date is 29 July; the resolver can never honestly satisfy both. |
| `statcan.36-10-0434-01.all_industries.month_to_month_percent_change.2026-06.first_print` | The contract pins a generic table page and generic field/series rather than one WDS vector and machine transform. |
| `statcan.36-10-0434-01.all_industries.month_to_month_percent_change.2026-07.first_print` | The URL pins the right vector, but the immutable machine transform says identity-style multiplication while the target requires month-over-month percent change. |

A trusted migration could mint replacement targets, but this lane does not
rewrite or reinterpret immutable registrations.

## Registry changes and removal audit

The docket upgrades four existing recurring templates to exact native
bindings:

- `eurostat.hicp.flash.yoy`
- `abs.cpi.all_groups.yoy`
- `abs.labour.unemployment_rate`
- `statcan.gdp_by_industry.monthly_growth`

It adds `statcan.cpi.allitems.yoy`.

Three recurring entries removed during the interrupted run were restored
unchanged:

- `eurostat.unemployment_rate`
- `statcan.employment_insurance.regular_beneficiaries`
- `statjp.cpi.tokyo_all_items_yoy`

Repository searches found published/catalog/registration references to all
three identities and no renamed successor. Their `generic-url` bindings remain
unchanged because their native candidates have not passed fixture admission.
The template-less waiver population remains 21 entries, matching its
21-entry manifest; no waiver was added or silently healed.

## Rejected and blocked work

| Source | Blocked items | Reason |
| --- | --- | --- |
| Statistics Canada | LFS unemployment, LFS employment change, EI regular beneficiaries | Exact WDS candidates exist, but no three-period release-vintage fixture set; each is revision-prone. |
| ABS | Employment change, quarterly CPI, building approvals | No three captured first-print payloads for each exact candidate; approvals has only one release-day snapshot. |
| Eurostat | Unemployment, industrial production, construction, retail trade | No three captured first-print payloads for each exact candidate. |
| ONS | CPI, claimant count, retail sales, PSNB | The parser/fetch contract exists, but no real captured JSON fixture set; candidates remain non-executable. |
| e-Stat / Statistics Bureau of Japan | Tokyo CPI, LFS, household spending | The official JSON API requires an application id. Per the brief, the lane skipped e-Stat implementation rather than substituting unverified XLSX/HTML parsing. |

## Verification and handoff

- Required gate,
  `uv run pytest tests/test_resolve_pending.py tests/test_register_targets.py -q`:
  **143 passed**
- Calendar integration included,
  `uv run pytest tests/test_resolve_pending.py tests/test_register_targets.py tests/test_roll_docket.py -q`:
  **161 passed**
- Waiver ratchet, `uv run pytest tests/test_waiver_ratchet.py -q`:
  **4 passed**
- Prospect workflow and USAspending compatibility:
  **38 passed**
- Ruff on all changed Python and test files: **passed**
- `jq -e . scripts/docket_series.json`: **passed**
- `git diff --check`: **passed**
- Site regressions for the exact reviewed legacy id alias, a different id
  alias, and the reviewed id under a different hash: **3 passed**
- Site TypeScript check, `bunx tsc --noEmit`: **passed**
- Site webpack compilation and TypeScript: **passed**. Static prerender then
  stopped only because the sandbox could not resolve
  `raw.githubusercontent.com`.
- Full site tests: **365 passed, 47 skipped, 12 failed**, all 12 failures plus
  one suite setup failure sharing the same blocked
  `raw.githubusercontent.com` DNS fetch.
- No file under `records/` was modified.

The checkout was 18 commits behind `origin/main` at final inspection. Per the
continuation instructions, this lane did not fetch, rebase, commit, push, or
otherwise alter Git history. The integrator must transplant these working-tree
changes onto current main while preserving upstream concept-routing changes.
