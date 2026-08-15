# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usda.fsa.crp.enrolled_acres_total
- period: 2027-09
- conditional: No farm bill enacted by 2027-09-30 sets a CRP acreage ceiling for fiscal years 2027 through 2031; current law holds.


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-crp-enrolled-acres-september-2027-no-fy2027-31-ceiling-source-recovered-2026-08-13"
- country: "US"
- targetUnit: "count"
- dataPointId: "usda.fsa.crp.enrolled_acres_total.2027_09.first_print.no_fy2027_31_ceiling_source_recovered_2026_08_13"
- resolutionDate: "2027-12-31"
- resolutionDateBasis: "resolve-by-bound"
- expectedReleaseWindow: {"end": "2027-12-31", "start": "2027-12-01"}
- sourceBinding: {"adapter": "fsa-crp-monthly-summary", "allowedHosts": ["www.fsa.usda.gov"], "expectedReleaseWindow": {"end": "2027-12-31", "start": "2027-12-01"}, "field": "enrolled_acres_total", "releasePolicy": "first_print", "sourceSeriesId": "usda.fsa.crp.enrolled_acres_total", "sourceUrl": "https://www.fsa.usda.gov/tools/informational/reports/conservation-statistics/crp", "table": "USDA FSA Conservation Reserve Program Statistics, CRP Monthly Summary, total row", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-13-f5ea9392285b625e5558aa894a21a5107751b4cebd51e3f680726e3e476e5bbd.json"
- targetContentHash: "f5ea9392285b625e5558aa894a21a5107751b4cebd51e3f680726e3e476e5bbd"
- registrationCommit: "f816f33e1cea6e50d33bd0314c88a7e901b77e17"
- registeredAtUtc: "2026-08-13T22:43:51Z"
- conditional: "No farm bill enacted by 2027-09-30 sets a CRP acreage ceiling for fiscal years 2027 through 2031; current law holds."

# Resolve-by-bound target contract (machine checked)
- registeredResolveByBound: "2027-12-31"
- officialAnnouncementUrl: "https://www.fsa.usda.gov/tools/informational/reports/conservation-statistics/crp"
The bound and expected release window are Thesis lab commitments, not timing claims made by the announcement. The announcement authenticates methodology identity only; it does not establish the bound or expected release window. This is an outer bound, not a scheduled release day. resolutionDate must byte-echo the registered resolve-by bound; never infer a more specific day from cadence.
resolutionSourceUrl must byte-echo officialAnnouncementUrl. Call `thesis_announcement_fetch.fetch_official_announcement` with that exact URL. The publisher authenticates the structured draft/final tool event; a reasoning-token claim, search result, same-host page, or prose citation cannot substitute for it.
Base rate during a methodology transition: while NO official print under the announced revised methodology exists — including revised historical or backcast estimates — the CURRENT official series is the admissible base rate: fetch it from its official source, name its vintage explicitly, and state the announced transition as the regime consideration in the sigma step. Do not refuse for lack of the unpublished revised series, and do not fabricate or pre-apply revision adjustments. The moment any revised-methodology official print exists, revised prints are required and old-methodology history stops being admissible.

# Resolution-grade base-rate fetch (run this — do not substitute)
The registered adapter's own parser is runnable in this workspace, and its output IS the series this target resolves against: history fetched any other way (summaries, bulletins, line-item estimates, adjacent products) fails anchored validation even when it is a real official series. For each of the most recent published periods (fetch at least the latest six), run:
  python3 -c "import sys; sys.path.insert(0, 'scripts'); import resolve_pending as r; print(r.fsa_crp_fetch_period(r.FSA_CRP_ADAPTERS['usda.fsa.crp.enrolled_acres_total'], 'PERIOD')[0])"   # PERIOD = a month like 2026-04
# Rubric
Check these items and name concrete fixes when needed:
1. Exact resolver, source, first-print rule, and resolution date.
2. Base-rate or persistence prior stated before inside-view updates.
3. Time-series/model prior used or explicitly ruled out.
4. Current evidence justifies material movement from the prior.
5. Interval size comes from realized volatility or explicit uncertainty.
6. A compact Prior/update/interval step names the prior, historical sample, adjustment components, interval method, and implied bounds.
7. Tail scenarios are concrete and tied to the target.
8. Point, interval, final forecast step, and JSON fields are coherent.
9. No leakage, catalog point/interval circularity, subjective resolver, or unit ambiguity.

# Required response
Return JSON only, with this shape:
{
  "summary": "one sentence",
  "requiredFixes": [
    {
      "rubricItem": "resolver|base_rate|model_prior|update|interval|prior_update_interval|tails|coherence|leakage",
      "severity": "warning|blocking",
      "summary": "specific issue",
      "actionRequested": "specific change requested"
    }
  ],
  "optionalSuggestions": ["short suggestions"]
}

# Original forecaster prompt hash material
847575697b3de1bb1dcd33bc57ddbcf50e81c398439f8711079bbb24dc356c71

# Draft forecast response
{
  "slug": "us-crp-enrolled-acres-september-2027-no-fy2027-31-ceiling-source-recovered-2026-08-13",
  "country": "US",
  "type": "conditional",
  "title": "US CRP enrolled acres, Sep 2027, no FY2027-31 ceiling",
  "question": "What will USDA FSA Conservation Reserve Program Statistics, CRP Monthly Summary, TOTAL CRP row, Acres column report for total enrolled acres for September 2027, not seasonally adjusted administrative total, on the first print, conditional on no farm bill enacted by 2027-09-30 setting a CRP acreage ceiling for fiscal years 2027 through 2031?",
  "unit": "count",
  "pointEstimate": 26182019,
  "ciLow": 25619979,
  "ciHigh": 26744059,
  "confidence": 0.8,
  "resolutionDate": "2027-12-31",
  "resolutionSource": "USDA Farm Service Agency, Conservation Reserve Program Statistics, CRP Monthly Summary",
  "resolutionSourceUrl": "https://www.fsa.usda.gov/tools/informational/reports/conservation-statistics/crp",
  "resolutionRule": "Resolve from the first USDA FSA Conservation Reserve Program Statistics CRP Monthly Summary for September 2027, TOTAL CRP row, Acres column, reported as whole acres. Use the first print only; later corrections or revisions do not change the resolved value. The resolution date is the Thesis registered resolve-by bound 2027-12-31, not a scheduled release day. The conditional resolves only if no farm bill enacted by 2027-09-30 sets a CRP acreage ceiling for fiscal years 2027 through 2031 and current law holds; if that condition fails, mark this cell unresolved.",
  "dataPointId": "usda.fsa.crp.enrolled_acres_total.2027_09.first_print.no_fy2027_31_ceiling_source_recovered_2026_08_13",
  "conditionalOn": "No farm bill enacted by 2027-09-30 sets a CRP acreage ceiling for fiscal years 2027 through 2031; current law holds.",
  "historicalContext": [
    {
      "period": {
        "type": "month",
        "value": "2024-09"
      },
      "label": "September 2024",
      "value": 24601888
    },
    {
      "period": {
        "type": "month",
        "value": "2025-09"
      },
      "label": "September 2025",
      "value": 25766115
    },
    {
      "period": {
        "type": "month",
        "value": "2025-10"
      },
      "label": "October 2025",
      "value": 26316110
    },
    {
      "period": {
        "type": "month",
        "value": "2025-11"
      },
      "label": "November 2025",
      "value": 26317011
    },
    {
      "period": {
        "type": "month",
        "value": "2025-12"
      },
      "label": "December 2025",
      "value": 26279615
    },
    {
      "period": {
        "type": "month",
        "value": "2026-01"
      },
      "label": "January 2026",
      "value": 26255016
    },
    {
      "period": {
        "type": "month",
        "value": "2026-02"
      },
      "label": "February 2026",
      "value": 26231997
    },
    {
      "period": {
        "type": "month",
        "value": "2026-03"
      },
      "label": "March 2026",
      "value": 26203615
    },
    {
      "period": {
        "type": "month",
        "value": "2026-04"
      },
      "label": "April 2026",
      "value": 26182019
    }
  ],
  "drivers": [
    "April 2026 parser-backed latest print at 26,182,019 acres",
    "No direct fetched evidence for moving away from persistence",
    "Large 2024-09 to 2025-09 increase widens first-print volatility",
    "Recent monthly prints drifted down after October 2025",
    "No FY2027-31 ceiling condition limits policy-specific adjustment"
  ],
  "sourceContext": [
    "https://www.fsa.usda.gov/tools/informational/reports/conservation-statistics/crp",
    "https://www.fsa.usda.gov/sites/default/files/2026-07/CRPMonthlyApril2026WithPageNumbers.pdf",
    "https://www.fsa.usda.gov/sites/default/files/2026-06/CRPMonthlyMarch2026WithPageNumbers.pdf",
    "https://www.fsa.usda.gov/sites/default/files/2026-06/CRPMonthlyFebruary2026WithPageNumbers_0.pdf",
    "https://www.fsa.usda.gov/sites/default/files/2026-05/CRPMonthlyJanuary2026WithPageNumbers.pdf",
    "https://www.fsa.usda.gov/sites/default/files/2026-04/CRPMonthlyDecember2025WithPageNumbers.pdf",
    "https://www.fsa.usda.gov/sites/default/files/2026-03/CRPMonthlyNovember2025WithPageNumbers.pdf",
    "https://www.fsa.usda.gov/sites/default/files/2026-03/CRPMonthlyOctober2025WithPageNumbers.pdf",
    "https://www.fsa.usda.gov/sites/default/files/2026-03/CRPMonthlySeptember2025WithPageNumbers_0.pdf",
    "https://www.fsa.usda.gov/sites/default/files/2024-10/CRPMonthlySeptember2024WithPageNumbers.pdf",
    "https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title16-section3831",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-08-15T15:24:22Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "Resolution framing"
    },
    {
      "kind": "text",
      "text": "This is the registered resolve-by-bound CRP target. I byte-echo the Thesis lab bound 2027-12-31 and use the registered FSA CRP statistics page as the methodology identity URL only; it does not establish the expected release window or a scheduled release day. The target is the September 2027 first-print TOTAL CRP Acres cell."
    },
    {
      "kind": "tool",
      "tool": "thesis_announcement_fetch.fetch_official_announcement",
      "call": "fetch_official_announcement(url='https://www.fsa.usda.gov/tools/informational/reports/conservation-statistics/crp')",
      "result": "Fetched exact registered official announcement URL; statusCode=200, responseBytes=121042, responseSha256=45c92ae6feee72d538dbc367373f90960e431a18ea7a44d04c7f45e2064c57a9."
    },
    {
      "kind": "tool",
      "tool": "resolve_pending.fsa_crp_fetch_period",
      "call": "fsa_crp_fetch_period(enrolled_acres_total, periods 2026-04, 2026-03, 2026-02)",
      "result": "Official parser values from FSA CRP Monthly Summary PDFs: 2026-04=26182019; 2026-03=26203615; 2026-02=26231997."
    },
    {
      "kind": "tool",
      "tool": "resolve_pending.fsa_crp_fetch_period",
      "call": "fsa_crp_fetch_period(enrolled_acres_total, periods 2026-01, 2025-12, 2025-11)",
      "result": "Official parser values from FSA CRP Monthly Summary PDFs: 2026-01=26255016; 2025-12=26279615; 2025-11=26317011."
    },
    {
      "kind": "tool",
      "tool": "resolve_pending.fsa_crp_fetch_period",
      "call": "fsa_crp_fetch_period(enrolled_acres_total, periods 2025-10, 2025-09, 2024-09, plus 2026-05 to 2026-07 availability checks)",
      "result": "Official parser values: 2025-10=26316110; 2025-09=25766115; 2024-09=24601888. Later checked periods 2026-05, 2026-06, and 2026-07 returned value=None from the landing URL, so April 2026 is the latest parsed numeric print in this run."
    },
    {
      "kind": "tool",
      "tool": "curl uscode.house.gov",
      "call": "fetch 16 U.S.C. 3831 conservation reserve acreage text",
      "result": "Fetched U.S. Code text around 16 U.S.C. 3831(d)(1): fiscal year 2022 not more than 25500000 acres; fiscal year 2023 not more than 27000000 acres. The registry-supplied condition governs FY2027-31 no-ceiling status."
    },
    {
      "kind": "tool",
      "tool": "scripts/run_time_series_models.py",
      "call": "PYTHONPATH=. python3 scripts/run_time_series_models.py --models persistence --round-increment 1",
      "result": "thesis_model_candidate_v1 persistence.last_print: pointEstimate=26182019, p10=26150933, p50=26182019, p90=26916284, interval80 lower=26150933 upper=26916284, interval90 lower=26147778 upper=27131265, calibrationN=8, trainCutoff=2026-04, walk_forward meanAbsoluteError=231264.375."
    },
    {
      "kind": "tool",
      "tool": "curl app.thesisinstitute.org/specs.json",
      "call": "curl -sS -D - https://app.thesisinstitute.org/specs.json",
      "result": "Slug check endpoint returned HTTP 404 with content-length=11289 rather than JSON, so no published-spec match was available from that endpoint for slug us-crp-enrolled-acres-september-2027-no-fy2027-31-ceiling-source-recovered-2026-08-13."
    },
    {
      "kind": "text",
      "text": "Base rate / reference class: the 9 parser-backed official CRP enrolled-acre prints fetched this run span 24,601,888 to 26,317,011 acres. The latest print is 26,182,019 for April 2026, and the persistence model candidate uses that as the strongest benchmark. Because the no-FY2027-31-ceiling condition supplies no fetched numeric policy effect, the base rate remains the forecast point."
    },
    {
      "kind": "math",
      "text": "Successive changes from the fetched official history are +1164227, +549995, +901, -37396, -24599, -23019, -28382, and -21596 acres; mean change = 197516.375 acres. The sample standard deviation of those changes is 439093.781608 acres."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: selected prior is persistence at 26182019 from the 2026-04 official print, using the 2024-09 through 2026-04 parser-backed history. Adjustment components: 0 acres for momentum because recent monthly declines and the prior September-to-September increase point in opposite directions; 0 acres for policy because the condition is no farm bill FY2027-31 ceiling and no fetched numeric effect clears the material-update test. Interval method: realized first-print change dispersion; sigma = 439094 acres, so the 80% half-width is roughly 1.28*sigma = 562040 acres. Point = 26182019; ciLow = 26182019 - 562040 = 25619979; ciHigh = 26182019 + 562040 = 26744059."
    },
    {
      "kind": "text",
      "text": "Counter-consideration: downside risk would land below the interval if FY2027 expirations are large and FSA cannot replace acres under current law. Upside risk would land above the interval if FSA restores enrollments toward the prior statutory 27,000,000 acre neighborhood even without a FY2027-31 ceiling; either case would be outside the interval."
    },
    {
      "kind": "forecast",
      "point": 26182019,
      "ciLow": 25619979,
      "ciHigh": 26744059
    }
  ]
}
