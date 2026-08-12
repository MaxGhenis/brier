# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.cpi.all_groups.yoy
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-cpi-annual-rate-august-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups.yoy.2026_08.first_print"
- expectedReleaseWindow: {"end": "2026-09-30", "start": "2026-09-30"}
- sourceBinding: {"adapter": "abs-data-api", "allowedHosts": ["data.api.abs.gov.au", "www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-30", "start": "2026-09-30"}, "field": "CPI/3.10001.10.50.M", "releasePolicy": "first_print", "sourceSeriesId": "CPI/3.10001.10.50.M", "sourceUrl": "https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata", "table": "Monthly Consumer Price Index (complete monthly CPI, dataflow CPI: annual change, all groups, original, weighted average of eight capital cities)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-12-650c901b54d028abbe844a2bbf05bb06f0c149744ffc369a6d6e96214936ac3b.json"
- targetContentHash: "650c901b54d028abbe844a2bbf05bb06f0c149744ffc369a6d6e96214936ac3b"
- registrationCommit: "d50ffb7c957ea27fad25c6e0c6fee0aa2471bc84"
- registeredAtUtc: "2026-08-12T21:16:44Z"
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
5a19fbe470d93e70a9fe870922c6066f623779f6e60d7b2cc2cb1d72f9063120

# Draft forecast response
{
  "slug": "australia-cpi-annual-rate-august-2026",
  "country": "AU",
  "type": "data",
  "title": "Australia CPI annual rate, August 2026",
  "question": "What will the Australian Bureau of Statistics report as the FIRST PRINT August 2026 annual percentage change for CPI/3.10001.10.50.M: Consumer Price Index (CPI), percentage change from previous year, All groups CPI, Original, Australia, Monthly?",
  "unit": "percent",
  "pointEstimate": 3.8,
  "ciLow": 3.0,
  "ciHigh": 4.6,
  "confidence": 0.8,
  "resolutionDate": "2026-09-30",
  "resolutionSource": "Australian Bureau of Statistics, Consumer Price Index, Australia",
  "resolutionSourceUrl": "https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata",
  "resolutionRule": "Resolve from the ABS data API field CPI/3.10001.10.50.M, described in the registration as Monthly Consumer Price Index (complete monthly CPI, dataflow CPI: annual change, all groups, original, weighted average of eight capital cities). Use the first print for period 2026-08 only; later revisions do not count. Unit is percent and rounding is to one decimal place, matching ABS publication precision. The ABS September 2026 future-release calendar listed Consumer Price Index, Australia for reference period August 2026 on Wednesday 30 September 2026 at 11:30am AEST.",
  "dataPointId": "abs.cpi.all_groups.yoy.2026_08.first_print",
  "historicalContext": [
    {
      "label": "2026-06 ABS CPI annual change",
      "value": 3.8
    },
    {
      "label": "2026-05 ABS CPI annual change",
      "value": 4.0
    },
    {
      "label": "2026-04 ABS CPI annual change",
      "value": 4.2
    },
    {
      "label": "2026-03 ABS CPI annual change",
      "value": 4.6
    },
    {
      "label": "2025-08 ABS CPI annual change",
      "value": 3.2
    }
  ],
  "drivers": [
    "Last-print persistence at 3.8 percent",
    "June-to-August two-step horizon",
    "Recent pullback from March peak",
    "No direct pre-release August signal fetched"
  ],
  "sourceContext": [
    "https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata",
    "https://www.abs.gov.au/release-calendar/future-releases/202609",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-08-12T21:34:21Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "Australia August 2026 CPI annual-rate forecast"
    },
    {
      "kind": "text",
      "text": "Target identity is tied to the registered ledger slug australia-cpi-annual-rate-august-2026, unit percent, and dataPointId abs.cpi.all_groups.yoy.2026_08.first_print. The public specs.json check returned a 404 page during this run, so I used the local generated ledger target and target registration for slug identity rather than inventing a replacement."
    },
    {
      "kind": "tool",
      "tool": "abs.calendar.fetch",
      "call": "curl -sSL https://www.abs.gov.au/release-calendar/future-releases/202609 and extract Consumer Price Index entry",
      "result": "ABS September 2026 future releases excerpt: Wednesday 30 September 2026 11:30am AEST Consumer Price Index, Australia; reference period August 2026. Numeric date used: 2026-09-30 and time 11:30am AEST."
    },
    {
      "kind": "tool",
      "tool": "abs.data_api.fetch",
      "call": "curl -sS https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata",
      "result": "ABS CPI/3.10001.10.50.M returned observations: 2025-04=2.4, 2025-05=2.1, 2025-06=1.9, 2025-07=3.0, 2025-08=3.2, 2025-09=3.6, 2025-10=3.8, 2025-11=3.4, 2025-12=3.8, 2026-01=3.8, 2026-02=3.7, 2026-03=4.6, 2026-04=4.2, 2026-05=4.0, 2026-06=3.8."
    },
    {
      "kind": "tool",
      "tool": "abs.structure.fetch",
      "call": "read dimensions in same ABS JSON response for CPI/3.10001.10.50.M",
      "result": "Same ABS response identifies MEASURE=3 Percentage change from previous year, INDEX=10001 All groups CPI, TSEST=10 Original, REGION=50 Australia, FREQ=M Monthly, unit=PCT Percent; latest numeric value is 2026-06=3.8."
    },
    {
      "kind": "tool",
      "tool": "model_candidates.local",
      "call": "compute benchmark candidates from fetched ABS values only",
      "result": "thesis_model_candidate_v1 benchmarks: persistence point=3.8, p10=3.0, p50=3.8, p90=4.6, 80_interval=[3.0,4.6], 90_interval=[2.7,4.9], interval_method=two-step residual sigma from 14 successive changes, calibration_n=14, train_cutoff=2026-06, walk_forward_MAE=0.3571; mean-change candidate point=4.0, interval=[3.2,4.8], calibration_n=14, train_cutoff=2026-06, in-sample MAE proxy=0.3714."
    },
    {
      "kind": "text",
      "text": "Base rate/reference class: the 15 fetched monthly ABS annual-change prints from 2025-04 to 2026-06 have mean 3.42, sample std of values 0.772, range 1.9 to 4.6, and last print 3.8. The reference class is short because the registered complete monthly CPI API series only returned 15 observations."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: prior = last-print persistence from 2026-06 at 3.8 because its fetched walk-forward absolute-change proxy MAE 0.3571 is slightly better than the mean-change rule's 0.3714. Adjustment components: no direct August pre-release signal fetched, so update = 0.0 and point = 3.8. Successive changes are -0.3, -0.2, +1.1, +0.2, +0.4, +0.2, -0.4, +0.4, 0.0, -0.1, +0.9, -0.4, -0.2, -0.2; one-month sigma = 0.466, two-month sigma = sqrt(2)*0.466 = 0.659, and 80% half-width = 1.28*sigma = 1.28*0.659 = 0.844, rounded to 0.8. Implied bounds: 3.8 - 0.8 = 3.0 and 3.8 + 0.8 = 4.6."
    },
    {
      "kind": "text",
      "text": "Sanity check: with a 0.8-point half-width around persistence, 12 of the 14 one-step historical moves were inside the band; the two misses were +1.1 in 2025-07 and +0.9 in 2026-03. For a two-month August target this coverage check supports, but does not narrow, the interval."
    },
    {
      "kind": "text",
      "text": "Downside risk outside the interval: a faster disinflation sequence like another pair of -0.4 monthly changes would land below the interval. Upside risk outside the interval: a renewed price shock comparable to the +1.1 or +0.9 historical jumps would land above the interval."
    },
    {
      "kind": "forecast",
      "point": 3.8,
      "ciLow": 3.0,
      "ciHigh": 4.6
    }
  ]
}
