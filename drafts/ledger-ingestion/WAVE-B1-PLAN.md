# Wave B1: usaspending-api sealed transform extensions

One unchecked item per driver step. Source of truth for every sealed
query: the merged Wave-A request files in this directory (exact POST
bodies, endpoints, FY2025 values, SHA-256s). Adapter machinery:
scripts/resolve_pending.py — spec registry (~line 3136, the
usaspending.dod.* entries are the pattern), query-kind dispatch
(~line 10225), body builders (usaspending_fiscal_year_post_body,
_usaspending_advanced_filters, ~lines 3490-3720). Tests:
tests/test_usaspending_adapter.py (mirror its structure; every new
sealed body asserted byte-exact against the Wave-A captured body).
Docket entries: mirror the us-dod-*-fy2026 registered_query_snapshot
annual entries in scripts/docket_series.json — and NEVER add
extras.resolutionDate to a calendar entry (the docket lint refuses it).

- [x] 1. CDFI Fund (S. 2718): spec `usaspending.cdfi.program_obligations`
  + awarding-subtier assistance filter support in the fiscal-year POST
  builder + tests pinning the exact Wave-A body
  (usaspending-cdfi-fund-program-obligations.json; FY2025
  $319,455,176.00 anchor).
- [x] 2. HIDTA (S. 767): spec `usaspending.ondcp.hidta_program_obligations`
  + sealed program_numbers filter (AL 95.001) + tests
  (usaspending-ondcp-hidta-program-obligations.json; FY2025
  $271,657,675.60).
- [x] 3. NTIA broadband (H.R. 2449): spec
  `usaspending.ntia.broadband_program_obligations` reusing the
  program_numbers filter (AL 11.038) + tests
  (usaspending-ntia-broadband-program-obligations.json; FY2025
  $409,852,406.47).
- [x] 4. Forest Service MN (H.R. 978): spec
  `usaspending.usfs.minnesota_obligations` + awarding-subagency +
  place-of-performance filter support + tests
  (usaspending-usfs-superior-nf-obligations.json; FY2025
  $46,832,556.79; label/docs must state MN-wide context, NOT Superior
  NF).
- [ ] 5. FIRST re-freeze tests/fixtures/ledger_series_catalog.json from
  the merged ledger branch (chronicle#158 landed, catalog 216 series:
  fetch ledger/series_catalog.json from PolicyEngine/chronicle branch
  codex/thesis-ledger-facts at or after commit 89ae436 — the
  'Re-freeze the ledger catalog' precedent commit f5562a57 shows the
  shape). THEN docket entries for all four as fy2026
  registered_query_snapshot
  — BIND THE CHRONICLE IDENTITIES (PolicyEngine/chronicle#158):
  usaspending.cdfi.assistance_transaction_obligations
  (uuid from ledger/series_uuid_registry.jsonl on the ledger branch),
  usaspending.ondcp.hidta_al95001_obligations,
  usaspending.ntia.broadband_al11038_obligations,
  usaspending.usfs.minnesota_place_of_performance_obligations.
  The Wave-A request files' proposed_concept spellings are DRAFTS and
  differ — the chronicle names are canonical. Entries mirror
  annual seeds (us-dod pattern: cadence annual, one explicit period,
  capture window, sourceBinding template in extras, anchors = the
  FY2025 values); run
  `uv run --extra dev --extra challenge --extra bills pytest tests/test_roll_docket.py tests/test_docket_ledger_containment.py -q`.
- [ ] 6. Full verification: `uv run --extra dev --extra challenge --extra bills pytest tests/test_usaspending_adapter.py tests/test_resolve_pending.py tests/test_roll_docket.py -q`
  and `cd site && bun run test`; write WAVE-B1-REPORT.md — honest table:
  per transform, what is sealed, what the series is NOT (no bill
  attribution), suite results.
