# Lane: resolver debt — CES industry detail, annual periods, QCEW

Goal: clear three known resolver gaps so already-registered cells stop
rotting. Adapter/parser work only — never touch `records/`, never push,
never commit; leave changes in the working tree.

## The three gaps (all previously diagnosed, 2026-07-18 notes)

1. **CES industry detail via the BLS API** (`BLS_API_ADAPTERS` family
   exists — read it): three defense CES cells (aerospace products & parts,
   ship & boat building, DoD-adjacent industry employment) refuse with "not
   yet published" even though June data has been out since 2026-07-02 —
   the bls_api rows are missing the period. Diagnose the actual API
   response for the affected series ids (api.bls.gov/publicAPI/v2/timeseries,
   registration key BLS_API_KEY may be in env; the v2 API works keyless at
   low volume), fix the period-matching/latest-period logic, and add fixture
   tests reproducing the exact failing payload shape.
2. **Annual-period references**: `parse_ref_period` cannot parse
   dataPointIds like `bls.cpi.u.annual_pct_change.2026` (year kind). Add the
   `year` period kind end-to-end (parse, window logic, resolver match) with
   tests; grep the registry/catalog for every annual-form dataPointId and
   make sure each parses.
3. **QCEW aircraft establishments** (`us-qcew-aircraft-manufacturing-establishments-q1-2026`,
   registered 2026-07-15, still unpublished): QCEW Q1 2026 first release is
   scheduled ~2026-08-20 per the BLS QCEW release calendar — build the QCEW
   resolver adapter now (data.bls.gov/cew/data/api/ CSV endpoints, NAICS
   336411, establishment counts) so the cell resolves the day the data
   lands. Anchor-verify against published Q3/Q4 2025 values.

## Anchor-verification protocol (MANDATORY)

Same rule as everywhere in this repo: an adapter ships only if it reproduces
at least 3 published values for its series from the live source, recorded in
ANCHORS.md (period, expected, got, URL). Mark UNVERIFIED honestly if the
network blocks you; never fabricate.

## Gates

- `uv run pytest tests/test_resolve_pending.py -q` green, plus your new tests.
- REPORT.md: what was wrong in the CES path (root cause, not just the fix),
  the year-kind design, QCEW adapter status + anchors.

Read CLAUDE.md and AGENTS.md first.
