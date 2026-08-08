# Ledger catalog fixture

`series_catalog.json` is the complete frozen PolicyEngine/chronicle PR #128
catalog snapshot supplied for Thesis issue #112. It contains 201 rows from
`generator_version` 3, with one row per (concept, geography level/id/vintage,
entity) identity. UUID authority is the append-only
`ledger/series_uuid_registry.jsonl`. Keeping the full snapshot preserves its
generator metadata and observation hash while making mapper tests portable.
