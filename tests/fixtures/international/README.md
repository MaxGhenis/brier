# International resolver fixtures

These files are losslessly trimmed from official response bytes already
archived by the resolver on 10 July 2026. Trimming removed unrelated periods,
dimensions, labels, and attributes; it did not change retained values, period
keys, status flags, or parser-relevant structure.

| Fixture | Official request | Archived raw SHA-256 |
| --- | --- | --- |
| `statcan_cpi_v41690973.json` | Statistics Canada WDS, vector 41690973 | `db53549e6a30801c55cd4c093f0d5b58bd2620d7a4ca87c8ed3125563029b2f1` |
| `statcan_gdp_v65201210.json` | Statistics Canada WDS, vector 65201210 | `a92f6e409305766c36f3c57e29ba8dd1d72f3dd36a0522a41db5e90400098829` |
| `abs_cpi_all_groups_yoy.json` | ABS Data API, `CPI/3.10001.10.50.M` | `32ddea1eeb483c20c052c7877248a1c2c8c7bbd4ce9928d13afed5332dceb368` |
| `abs_lfs_unemployment_rate.json` | ABS Data API, `LF/M13.3.1599.20.AUS.M` | `d90a6205ec82ea4344bcd33fbcd1cdf25a98d32f9bdaec21ed3c4cfa32ebe24a` |
| `eurostat_hicp_flash.json` | Eurostat API, `prc_hicp_minr/M.RCH_A.TOTAL.EA21` | `e370ff5d1f6f324466269ff7a3fdb82254b6621e13eda23b50d3d2ce964d0b65` |

The source archives remain under `records/resolutions/2026-07-10/`; this lane
only read them and did not modify anything under `records/`.

The 10 July ABS Labour Force archive predates the June 2026 release and ends at
May. June is therefore not included in the adapter's verified-anchor set:
this sandbox could not recapture a post-release response from
`data.api.abs.gov.au`, and no API-shaped bytes were synthesized from the later
release page.
