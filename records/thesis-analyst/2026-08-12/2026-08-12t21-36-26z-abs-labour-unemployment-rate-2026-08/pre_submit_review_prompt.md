# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.labour.unemployment_rate
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-unemployment-rate-august-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.labour.unemployment_rate.2026_08.first_print"
- expectedReleaseWindow: {"end": "2026-09-24", "start": "2026-09-24"}
- sourceBinding: {"adapter": "abs-data-api", "allowedHosts": ["data.api.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-24", "start": "2026-09-24"}, "field": "LF/M13.3.1599.20.AUS.M", "releasePolicy": "first_print", "sourceSeriesId": "LF/M13.3.1599.20.AUS.M", "sourceUrl": "https://data.api.abs.gov.au/rest/data/LF/M13.3.1599.20.AUS.M?lastNObservations=30&format=jsondata", "table": "Labour Force, Australia (dataflow LF: unemployment rate, persons, total age, seasonally adjusted, Australia)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-12-2412e4199fb3442c941d9215beee8083062b680f4531f5fb6cbb6280f387eae0.json"
- targetContentHash: "2412e4199fb3442c941d9215beee8083062b680f4531f5fb6cbb6280f387eae0"
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
549341f13543b84281f4ae0ac446a8384a2381f17f4e292cc320a03427d60dff

# Draft forecast response
{"slug":"australia-unemployment-rate-august-2026","country":"AU","type":"data","title":"Australia unemployment rate, August 2026","question":"What will the Australian Bureau of Statistics Labour Force dataflow LF series LF/M13.3.1599.20.AUS.M, unemployment rate for persons aged total, seasonally adjusted, Australia, monthly percent, report for August 2026 on the first print?","unit":"percent","pointEstimate":4.4,"ciLow":4.2,"ciHigh":4.6,"confidence":0.8,"resolutionDate":"2026-09-24","resolutionSource":"Australian Bureau of Statistics, Labour Force, Australia","resolutionSourceUrl":"https://data.api.abs.gov.au/rest/data/LF/M13.3.1599.20.AUS.M?lastNObservations=30&format=jsondata","resolutionRule":"Resolve from the ABS Data API dataflow LF series LF/M13.3.1599.20.AUS.M, Labour Force, Australia: unemployment rate (M13), persons (3), total age (1599), seasonally adjusted (20), Australia (AUS), monthly frequency, for TIME_PERIOD 2026-08. Use the first print released for the August 2026 reference period, report the value in percent rounded to one decimal as published by ABS, and ignore later revisions.","dataPointId":"abs.labour.unemployment_rate.2026_08.first_print","targetRegistrationPath":"records/targets/2026-08-12-2412e4199fb3442c941d9215beee8083062b680f4531f5fb6cbb6280f387eae0.json","targetContentHash":"2412e4199fb3442c941d9215beee8083062b680f4531f5fb6cbb6280f387eae0","registrationCommit":"d50ffb7c957ea27fad25c6e0c6fee0aa2471bc84","registeredAtUtc":"2026-08-12T21:16:44Z","historicalContext":[{"label":"ABS LF/M13.3.1599.20.AUS.M 2026-06 raw","value":4.42834371},{"label":"ABS LF/M13.3.1599.20.AUS.M 2026-05 raw","value":4.37134808},{"label":"ABS LF/M13.3.1599.20.AUS.M 2026-04 raw","value":4.49048465},{"label":"ABS LF/M13.3.1599.20.AUS.M 2026-03 raw","value":4.27833862},{"label":"ABS LF/M13.3.1599.20.AUS.M 2026-02 raw","value":4.30162554},{"label":"ABS LF/M13.3.1599.20.AUS.M 2026-01 raw","value":4.07986795}],"drivers":["last-print persistence at 4.4 percent","last-three-print average rounds to 4.4 percent","recent month-to-month sigma is 0.1201 percentage points","no direct August-specific official signal before the July print"],"sourceContext":["https://data.api.abs.gov.au/rest/data/LF/M13.3.1599.20.AUS.M?lastNObservations=30&format=jsondata","https://www.abs.gov.au/release-calendar/future-releases/202609/rcc_labour","https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release","https://app.thesisinstitute.org/specs.json"],"runAt":"2026-08-12T21:36:42Z","reasoning":[{"kind":"heading","text":"Australia Labour Force first-print forecast"},{"kind":"text","text":"Framing: the registered target is ABS dataflow LF/M13.3.1599.20.AUS.M for August 2026, unemployment rate, persons, total age, seasonally adjusted, Australia, monthly percent, first print. The canonical ledger context binds slug australia-unemployment-rate-august-2026, unit percent, dataPointId abs.labour.unemployment_rate.2026_08.first_print, and the registered ABS Data API resolver."},{"kind":"tool","tool":"abs.release_calendar","call":"curl -sS https://www.abs.gov.au/release-calendar/future-releases/202609/rcc_labour and strip HTML around Labour Force, Australia","result":"ABS future releases page excerpt contained: Thursday 24 September 2026 11:30am AEST; Labour Force, Australia; Reference period August 2026. This verifies resolutionDate 2026-09-24 for the first print."},{"kind":"tool","tool":"abs.data_api","call":"curl -sS https://data.api.abs.gov.au/rest/data/LF/M13.3.1599.20.AUS.M?lastNObservations=30&format=jsondata and parse SDMX JSON observations","result":"Fetched ABS LF/M13.3.1599.20.AUS.M values include 2026-06=4.42834371, 2026-05=4.37134808, 2026-04=4.49048465, 2026-03=4.27833862, 2026-02=4.30162554, 2026-01=4.07986795 percent; ABS metadata says DECIMALS=1 and Unit of Measure Percent."},{"kind":"tool","tool":"abs.latest_release","call":"curl -sS https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release and strip HTML excerpts","result":"Latest ABS Labour Force page showed Reference period June 2026, Released 23/07/2026, Release date and time 23/07/2026 11:30am AEST, and in seasonally adjusted terms the unemployment rate was 4.4%. It also listed Next Release 24/09/2026 Labour Force, Australia, August 2026."},{"kind":"tool","tool":"thesis.model_candidates","call":"PYTHONPATH=. python3 scripts/run_time_series_models.py --target-id abs.labour.unemployment_rate.2026_08.first_print --target-period 2026-08 --models persistence --round-increment 0.1 using the fetched 2024-01 through 2026-06 ABS history","result":"thesis_model_candidate_v1 persistence.last_print generatedAt 2026-08-12T21:37:23Z: pointEstimate 4.4, p10 4.3, p50 4.4, p90 4.6, interval80 lower 4.3 upper 4.6, interval90 lower 4.2 upper 4.6, calibrationN 29, trainCutoff 2026-06, walk_forward_1_step meanAbsoluteError 0.10970723586206897."},{"kind":"tool","tool":"thesis.specs_slug_check","call":"curl -sS -D - https://app.thesisinstitute.org/specs.json","result":"Attempted required public specs slug check at 2026-08-12T21:36Z; HTTP status was 404 and the returned HTML body length was 11289 bytes, so no successful specs JSON slug list was available this run."},{"kind":"text","text":"Base rate / reference class: last 24 fetched ABS monthly unemployment-rate levels, 2024-07 through 2026-06, had n=24, mean 4.1991, median 4.1633, min 3.9370, max 4.4905, level std 0.1507. The last 23 successive month-to-month changes had mean +0.0100 percentage points, sigma 0.1201, min -0.2062, max +0.2218. Last-print persistence is 2026-06 raw 4.42834371, published as 4.4, and the last-three average is 4.4301, also rounding to 4.4."},{"kind":"math","text":"Prior/update/interval: prior is the thesis_model_candidate_v1 persistence.last_print benchmark from the fetched ABS history through 2026-06, point 4.4 after one-decimal publication rounding. Adjustment components: +0.0 for current official evidence because the latest ABS release only confirms June at 4.4 and the August print is still two monthly releases away; +0.0 for policy/one-off because no fetched official source identified an August-specific measurement change. For a level/rate series, compute interval dispersion from successive changes: sigma = 0.1201 percentage points over the last 23 fetched changes; 1.28*sigma = 0.1537. Around point 4.4 this implies 4.2463 to 4.5537 before publication rounding; rounding outward to one decimal gives an 80% interval of 4.2 to 4.6 percent. Implied bounds: point 4.4, ciLow 4.2, ciHigh 4.6."},{"kind":"text","text":"Counter-consideration: upside risk outside the interval would require unemployment to rise above 4.6 if July and August labour-force prints both weakened or participation rose faster than employment. Downside risk outside the interval would require a drop below 4.2 if employment growth reaccelerated while participation stopped adding unemployed persons."},{"kind":"forecast","point":4.4,"ciLow":4.2,"ciHigh":4.6}]}
