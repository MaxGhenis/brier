# /bills full-coverage — Wave A plan (existing adapter families)

Max's directive (2026-08-10): every /bills page gets actual forecasts.
No excuses. Wave A = ingestion requests for gap bills using EXISTING
adapter families (usaspending award transactions; ALFRED/FRED
first-print pins; the BEA official-release resolver). Wave-1 discipline
verbatim: every verification claim from a REAL fetch this session
(sha256 + byteLength + verbatim printed values + exact query recorded);
honest outcomes; DHS-Title-VI-precedent scoping (when the exact
bill-mapped concept can't be isolated, admit the NARROWER series the
data actually proves and say so — never the reverse); no records/**, no
docket edits, no code. Mirror the existing draft schema (exemplars:
drafts/ledger-ingestion/irs-actc-total-credit-amount.json for shape,
usaspending-dhs-title-vi… lineage for the usaspending family
conventions — read the DHS ADMITTED draft, not just proposed ones).

Work items (ONE per session; [x] when the request file is written):

- [x] 1. usaspending-cdfi-fund-program-obligations.json — bill
  stress-119s2718is (S. 2718, CDFI). Concept
  usaspending.cdfi_fund.award_transaction_obligations (usd, annual
  fiscal-year). Live-verify: USAspending advanced-search /
  spending_by_award or transaction endpoints filtered to Treasury CDFI
  Fund assistance listings (21.020 Financial Assistance / 21.021 BEA? —
  investigate which AL(s) are real via the API's autocomplete or
  assistance-listing endpoints and record what the DATA proves);
  capture a full FY (e.g. FY2025) obligations total with the exact
  request JSON + response sha. Scope honestly per DHS precedent.
- [x] 2. usaspending-ondcp-hidta-program-obligations.json — bill
  stress-119s767is (HIDTA Enhancement). Concept
  usaspending.ondcp.hidta.award_transaction_obligations (usd, annual).
  Wave-1 REJECTED the §707(s)-supplemental-specific series (AL 95.001
  cannot distinguish supplemental grants) — that rejection STANDS; this
  request is the BROADER honestly-scoped total HIDTA program
  obligations under AL 95.001, explicitly framed as the aggregate the
  data proves (cite the wave-1 rejection and the distinction).
- [x] 3. usaspending-ntia-broadband-program-obligations.json — bill
  stress-119hr2449ih (FUTURE Networks / FCC 6G Task Force). The bill's
  own metrics are report-deadline execution items with no recurring
  series, so this is a CONTEXT series, labeled as such: NTIA (or FCC)
  spectrum/advanced-communications account obligations — investigate
  live which NTIA/FCC account or AL gives a clean recurring annual
  total; record what you actually find; if NOTHING honest exists,
  write the request with outcome "rejected" and the precise reason
  (that is an acceptable result — but exhaust the account/AL search
  first).
- [x] 4. usaspending-nist-ai-safety-obligations.json — bill
  frontier-act-hr9925. Same context-series treatment: NIST (or
  Commerce ITA/BIS) AI-related account obligations — live
  investigation; honest scoping or honest rejection with the search
  trail.
- [x] 5. usaspending-usfs-superior-nf-obligations.json — bill
  stress-119hr978ih (Superior NF). Context: Forest Service obligations
  scoped to Minnesota / the Superior NF place-of-performance if the
  API's geographic filters prove it cleanly; else honest rejection
  with trail.
- [x] 6. alfred-qcew-childcare-employment.json — bill farm-bill-2-0
  (childcare title; the bill mapper names QCEW NAICS 624410). Concept
  bls.qcew.child_day_care_services.annual_avg_employment. Live-verify
  a FRED/ALFRED series for QCEW NAICS 624410 US annual average
  employment (search FRED; ENU-prefixed QCEW series exist); pin 2-3
  ALFRED vintages like the wave-1 BEA requests. If no FRED mirror
  exists, document and mark for a direct-BLS-QCEW family in Wave B
  (outcome proposed with that requiredWork).
- [x] 7. bea-ita-personal-transfer-payments-direct.json — bill
  stress-119hr5595ih (REMIT). The bill mapper names BEA ITA Table 5.1
  line 18 personal-transfer payments. Wave-1 rejected the FRED route
  (no exact mirror); this request uses the DIRECT BEA API (the
  existing bea-release adapter family already talks to the BEA API for
  NIPA — record the exact ITA dataset/table/line request and the
  printed value; note whether the existing family extends or a
  sibling ita variant is needed).
- [x] 8. WAVE-BILLS-A-REPORT.md — honest table: per request, outcome,
  strongest artifact, adapter-family disposition (existing / extend /
  new-family-needed / rejected), and the bill each serves. Plus open
  items list for Wave B (army-rdte-jbook-pdf for FLRAA; eia
  vented-flared for FLARE; cms-medicaid-enrollment for COVER +
  Safeguarding Medicaid; drought-monitor weekly for farm-bill water
  title).

Print exactly "BILLSA-STEP-DONE: <item>" after one item, or
"BILLSA-ALL-DONE" when every box is checked.
