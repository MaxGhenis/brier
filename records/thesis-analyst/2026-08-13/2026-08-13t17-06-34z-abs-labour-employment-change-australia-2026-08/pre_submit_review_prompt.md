# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.labour.employment_change.australia
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "abs-labour-employment-change-australia-august-2026"
- country: "AU"
- targetUnit: "thousands"
- dataPointId: "abs.labour.employment_change.australia.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-24", "start": "2026-09-16"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["data.api.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-24", "start": "2026-09-16"}, "field": "LF/M3.3.1599.20.AUS.M", "releasePolicy": "first_print", "sourceSeriesId": "LF/M3.3.1599.20.AUS.M", "sourceUrl": "https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata", "table": "Labour Force, Australia (dataflow LF: employed persons, seasonally adjusted, Australia; month-over-month change)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-13-41d79da5a1eb87a3b2f27212a9afdd447b5f05fae331872be26a08d85af2175e.json"
- targetContentHash: "41d79da5a1eb87a3b2f27212a9afdd447b5f05fae331872be26a08d85af2175e"
- registrationCommit: "27d485d528684bbe8281fa349cfbb9587169dd5b"
- registeredAtUtc: "2026-08-13T16:32:19Z"
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
f118e1b7613bae9f1d954e89aaeae7fcfb864715bcf6ead8ea327c06d32fb2fa

# Draft forecast response
{
  "slug": "abs-labour-employment-change-australia-august-2026",
  "country": "AU",
  "type": "data",
  "title": "Australia Employment Change, August 2026",
  "question": "What will the Australian Bureau of Statistics first print for seasonally adjusted employed persons month-over-month change in Australia be for August 2026, in thousands, in Labour Force, Australia?",
  "unit": "thousands",
  "pointEstimate": 21.0,
  "ciLow": -29.8,
  "ciHigh": 71.8,
  "confidence": 0.8,
  "resolutionDate": "2026-09-24",
  "resolutionSource": "Australian Bureau of Statistics Data API, Labour Force LF/M3.3.1599.20.AUS.M",
  "resolutionSourceUrl": "https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata",
  "resolutionRule": "Resolve to the first observed August 2026 API observation for ABS Labour Force series LF/M3.3.1599.20.AUS.M: seasonally adjusted employed persons, Australia, month-over-month change, in thousands, computed as the August 2026 employed-persons level minus the July 2026 employed-persons level in the same first-print ABS release/API vintage. Use the value from the first official ABS release/API print scheduled for 2026-09-24, rounded to one decimal thousand if the source presents one decimal; ignore later revisions or corrections.",
  "dataPointId": "abs.labour.employment_change.australia.august_2026.first_print",
  "historicalContext": [
    {
      "label": "Feb-2026 SA employment change",
      "value": 22.9
    },
    {
      "label": "Mar-2026 SA employment change",
      "value": 20.3
    },
    {
      "label": "Apr-2026 SA employment change",
      "value": -38.6
    },
    {
      "label": "May-2026 SA employment change",
      "value": 44.0
    },
    {
      "label": "Jun-2026 SA employment change",
      "value": 76.3
    },
    {
      "label": "last-24-month mean SA employment change",
      "value": 20.9
    },
    {
      "label": "last-24-month sample sigma",
      "value": 39.7
    }
  ],
  "drivers": [
    "Recent mean beats last-print persistence in walk-forward error",
    "June employment gain was unusually high relative to last-24-month mean",
    "No official July print available at run time",
    "ABS Labour Force month-to-month changes remain volatile"
  ],
  "sourceContext": [
    "https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata",
    "https://www.abs.gov.au/release-calendar/future-releases/202609",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-08-13T17:08:21Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "Australia Labour Force Employment Change, August 2026"
    },
    {
      "kind": "text",
      "text": "Framing and resolver: the registered target is abs.labour.employment_change.australia for August 2026, unit thousands, dataPointId abs.labour.employment_change.australia.august_2026.first_print, and catalog slug abs-labour-employment-change-australia-august-2026. The canonical sourceBinding URL returns ABS employed-person levels in thousands for LF/M3.3.1599.20.AUS.M; the resolver family in the public repo defines this employment-change concept as the same-release month-over-month difference of those seasonally adjusted levels. I preserve the registered target identity and state that level-versus-change binding discrepancy explicitly rather than changing the target."
    },
    {
      "kind": "tool",
      "tool": "curl",
      "call": "curl -sSL https://www.abs.gov.au/release-calendar/future-releases/202609 and extract the Labour Force, Australia row",
      "result": "ABS release calendar excerpt fetched this run: time datetime=2026-09-24T01:30:00Z, displayed as Thursday 24 September 2026 11:30am AEST; product Labour Force, Australia; reference period August 2026."
    },
    {
      "kind": "tool",
      "tool": "curl",
      "call": "curl -sS 'https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata'",
      "result": "ABS Data API meta prepared 2026-08-13T17:07:32Z; latest seasonally adjusted employed-person levels in thousands were 2026-02 14721.205316, 2026-03 14741.551774, 2026-04 14702.952844, 2026-05 14746.946935, 2026-06 14823.289454."
    },
    {
      "kind": "tool",
      "tool": "python.compute",
      "call": "Parse fetched ABS levels and compute same-vintage month-over-month changes",
      "result": "Computed recent changes in thousands from fetched ABS LF/M3.3.1599.20.AUS.M levels: 2026-02 +22.9, 2026-03 +20.3, 2026-04 -38.6, 2026-05 +44.0, 2026-06 +76.3; last 24 changes had mean +20.9, median +32.0, sample sigma 39.7, min -74.8, max +104.0."
    },
    {
      "kind": "tool",
      "tool": "python.model_candidates",
      "call": "Compute thesis_model_candidate_v1 compact candidates from fetched changes through 2026-06",
      "result": "Model candidates for 2026-08 employment change, train_cutoff 2026-06, calibration_n 24: persistence point +76.3 with 80% interval +25.6 to +127.1; trailing12mean point +21.0 with 80% interval -29.8 to +71.8; last24mean point +20.9 with 80% interval -29.8 to +71.7. Walk-forward calibration over 17 observations: persistence MAE 56.7 RMSE 66.7; trailing12mean MAE 38.9 RMSE 47.8; expandingmean MAE 36.4 RMSE 46.7."
    },
    {
      "kind": "tool",
      "tool": "curl",
      "call": "curl -sSL -w HTTP_STATUS https://app.thesisinstitute.org/specs.json",
      "result": "Slug-check fetch for https://app.thesisinstitute.org/specs.json returned HTTP 404 with an HTML/Next error page; fallback local public generated ledger target contains catalogSlug abs-labour-employment-change-australia-august-2026 and resolutionDate 2026-09-24 for this dataPointId."
    },
    {
      "kind": "text",
      "text": "Base rate / reference class: using the last 24 fetched same-series month-over-month employment changes through June 2026, the distribution is mean +20.9 thousand, median +32.0 thousand, sample sigma 39.7 thousand, range -74.8 to +104.0 thousand. Last-print persistence at +76.3 thousand is a high-side June spike and had materially worse walk-forward error than recent-mean candidates, so I use the trailing/recent-mean model as the outside-view prior."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: selected prior = trailing12mean/last24mean blend centered at +21.0 thousand because trailing12mean point +21.0 and last24mean point +20.9 are effectively identical, with no official July print or direct August-specific signal fetched this run to justify a material deviation. Adjustment components: +0.0 thousand current-evidence update, since the June +76.3 spike is already in the fetched history and persistence underperformed in walk-forward tests. Interval method = normal wrapper from last-24 realized change dispersion; sigma = 39.7 thousand, 80% half-width = 1.28*sigma = 1.28*39.7 = 50.8 thousand, so 21.0 - 50.8 = -29.8 and 21.0 + 50.8 = 71.8."
    },
    {
      "kind": "text",
      "text": "Counter-consideration: upside risk outside the interval would be another broad hiring surge or survey rotation effect that keeps the August same-vintage employment gain above +71.8 thousand; downside risk outside the interval would be payback after June's unusually strong gain, weaker vacancies, or a participation/labour-demand softening that pulls the August change below -29.8 thousand."
    },
    {
      "kind": "forecast",
      "point": 21.0,
      "ciLow": -29.8,
      "ciHigh": 71.8
    }
  ]
}
