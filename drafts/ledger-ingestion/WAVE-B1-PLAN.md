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

- [ ] 1. CDFI Fund (S. 2718): spec `usaspending.cdfi.program_obligations`
  + awarding-subtier assistance filter support in the fiscal-year POST
  builder + tests pinning the exact Wave-A body
  (usaspending-cdfi-fund-program-obligations.json; FY2025
  $319,455,176.00 anchor).
- [ ] 2. HIDTA (S. 767): spec `usaspending.ondcp.hidta_program_obligations`
  + sealed program_numbers filter (AL 95.001) + tests
  (usaspending-ondcp-hidta-program-obligations.json; FY2025
  $271,657,675.60).
- [ ] 3. NTIA broadband (H.R. 2449): spec
  `usaspending.ntia.broadband_program_obligations` reusing the
  program_numbers filter (AL 11.038) + tests
  (usaspending-ntia-broadband-program-obligations.json; FY2025
  $409,852,406.47).
- [ ] 4. Forest Service MN (H.R. 978): spec
  `usaspending.usfs.minnesota_obligations` + awarding-subagency +
  place-of-performance filter support + tests
  (usaspending-usfs-superior-nf-obligations.json; FY2025
  $46,832,556.79; label/docs must state MN-wide context, NOT Superior
  NF).
- [ ] 5. Docket entries for all four as fy2026 registered_query_snapshot
  annual seeds (us-dod pattern: cadence annual, one explicit period,
  capture window, sourceBinding template in extras, anchors = the
  FY2025 values); run
  `uv run --extra dev --extra challenge --extra bills pytest tests/test_roll_docket.py tests/test_docket_ledger_containment.py -q`.
- [ ] 6. Full verification: `uv run --extra dev --extra challenge --extra bills pytest tests/test_usaspending_adapter.py tests/test_resolve_pending.py tests/test_roll_docket.py -q`
  and `cd site && bun run test`; write WAVE-B1-REPORT.md — honest table:
  per transform, what is sealed, what the series is NOT (no bill
  attribution), suite results.
