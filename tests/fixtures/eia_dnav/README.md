# EIA dnav natural-gas venting and flaring fixtures

These files are unmodified response bodies fetched from official EIA hosts on
2026-08-13 UTC. They freeze the current retrieval and parser surfaces for EIA
series `N9040US2`, not a claim that Thesis witnessed the historical values on
their original release dates. The workbook is the keyless, recurring artifact
that a CI resolver can fetch. The API response records why the resolver must
not depend on an API credential.

## Fetch inventory

| Fixture | Request and final URL | Retrieved (UTC) | HTTP and content type | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| `n9040us2a.html` | `https://www.eia.gov/dnav/ng/hist/n9040us2a.htm` | 2026-08-13T18:53:10Z | 200; `text/html` | 7,615 | `00b6c41be70b9f52463fd4536344372e50dcf96b25b0b58078e989bbf6362e6a` |
| `N9040US2a.xls` | `https://www.eia.gov/dnav/ng/hist_xls/N9040US2a.xls` | 2026-08-13T18:53:10Z | 200; `application/vnd.ms-excel` | 31,232 | `2097906a434f257678ed09ab34cb1a5bb6bd070b9430e0edfed3a32b738b3a92` |
| `natural-gas-annual.html` | `https://www.eia.gov/naturalgas/annual/` | 2026-08-13T18:53:10Z | 200; `text/html; charset=UTF-8` | 114,290 | `1ca09dbac466614e868819999454d38f85c5699eea1e20a739c5d3f9976b022f` |
| `natural-gas-annual-summary.html` | `https://www.eia.gov/dnav/ng/ng_sum_lsum_dcu_nus_a.htm` | 2026-08-13T19:17:37Z | 200; `text/html` | 59,307 | `19990844a4f4b1b961292eaed8e59e87e2a8b3b4d065db691eb1e74f23f9eb9a` |
| `upcoming-reports.html` | `https://www.eia.gov/reports/upcoming.php` | 2026-08-13T18:54:30Z | 200; `text/html; charset=UTF-8` | 75,148 | `08abcd52aa620b33ab3170f95b964df9162438e9edf5a93021f8545e8f682e3c` |
| `api-no-key.json` | `https://api.eia.gov/v2/seriesid/NG.N9040US2.A` | 2026-08-13T18:54:04Z | 403; `application/json` | 163 | `b71fb384d31b5e7ccc66d279785c9e6cd51fa51f07820a3363c849034b9608bd` |

No request redirected, so each final URL equals the request URL shown above.
EIA returned `Last-Modified: Tue, 28 Jul 2026 17:21:06 GMT` and ETag
`"02d1079b51edd1:0"` for the series history page and workbook. The workbook's
own Contents sheet says `Release Date: 7/31/2026`, `Next Release Date:
8/31/2026`, and latest data year 2024. The frozen evidence is therefore an
as-of-2026-08-13 current vintage; its historical rows may include revisions.

The Natural Gas Annual summary page returned `Last-Modified: Tue, 28 Jul 2026
16:58:04 GMT` and ETag `"0b65341b21edd1:0"`. The annual landing page links
this exact summary table, whose `Vented and Flared` row links the exact
`n9040us2a.htm` history page and displays the same five 2020-2024 values.
That freezes the product-to-series bridge used to apply the annual schedule
to `N9040US2`, rather than inferring it from the measure's name alone.

## Workbook identity and selector

`N9040US2a.xls` is a BIFF8/Compound File Binary workbook with two worksheets,
`Contents` and `Data 1`. It authenticates all of the fields the adapter needs:

- `Contents!B3` and `Contents!C7` are `U.S. Natural Gas Vented and Flared
  (MMcf)`; `Contents!E7` is `Annual`; and `Contents!F7` is 2024.
- `Data 1!B1` is `Data 1: U.S. Natural Gas Vented and Flared (MMcf)`,
  `Data 1!B2` is the source key `N9040US2`, and `Data 1!B3` repeats the series
  title and unit.
- Select the row in `Data 1` whose column A cell displays the requested
  four-digit year under its `YYYY` Excel number format, then read the numeric
  MMcf value from column B. The frozen anchor cells are `A90:B90` for
  2022/271682, `A91:B91` for 2023/324207, and `A92:B92` for 2024/335163.

The selector uses the workbook's displayed annual year rather than treating
the underlying serial date as an observation day. For example, `A92` is a
date-formatted numeric cell that displays `2024`; the annual observation is
2024, not the cell's hidden month and day. No unit conversion or value scaling
is required: the source and target unit are both MMcf.

## Cadence and the 2025 release bound

The dnav transport is refreshed on the Natural Gas Monthly cycle: the frozen
dnav page says release 2026-07-31 and next release 2026-08-31, while EIA's
upcoming-reports page describes the Natural Gas Monthly schedule as the last
business day of each month. Those recurring refreshes do not create a new
annual observation; the annual workbook still ends at 2024.

For the next annual observation, the frozen Natural Gas Annual landing page
says `With Data for 2024`, gives its 2025-11-28 release date, and says `Next
Release: October 2026`. That landing page links the frozen summary table,
which in turn binds its `Vented and Flared` row to the exact `N9040US2`
history page. The independently frozen upcoming-reports page lists `Natural
Gas Annual` under `October 2026`. Because EIA publishes no day, the honest
window for the next edition is **2026-10-01 through 2026-10-31**, with
2026-10-31 as the conservative resolve-by bound. The next annual edition
advances the table from 2024 to 2025; neither official schedule page supplies
a more precise day, so the docket must not invent one. A resolver should poll
the exact keyless XLS in that window and accept the first authenticated
workbook containing annual row 2025.

## API-key verdict

The exact v2 compatibility route for legacy series `NG.N9040US2.A`, requested
without credentials, returned HTTP 403 and `API_KEY_MISSING`; the 163-byte
fixture intentionally has no final newline. EIA's API documentation likewise
states that every API call must carry a registered user's key. The dnav XLS
returned HTTP 200 without a cookie, key, or authorization header, so it is the
appropriate CI transport and the API is not a valid keyless fallback.
