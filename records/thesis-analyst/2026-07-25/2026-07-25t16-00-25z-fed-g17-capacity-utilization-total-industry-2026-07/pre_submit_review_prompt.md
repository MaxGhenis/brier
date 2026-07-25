# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fed.g17.capacity_utilization.total_industry
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "fed-g17-capacity-utilization-total-industry-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "fed.g17.capacity_utilization.total_industry.2026-07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.federalreserve.gov"], "expectedReleaseWindow": {"end": "2026-08-21", "start": "2026-08-13"}, "field": "TCU", "releasePolicy": "first_print", "sourceSeriesId": "TCU", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TCU", "table": "G.17 Industrial Production and Capacity Utilization, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-a51d56b832ff97c356a370807bab06ccf4e39b9e37608915beb9eff4dac89265.json"
- targetContentHash: "a51d56b832ff97c356a370807bab06ccf4e39b9e37608915beb9eff4dac89265"
- registrationCommit: "add78fbd9af9ca9b0c7389a9a44a7ec839f2f4af"
- registeredAtUtc: "2026-07-25T15:18:08Z"
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
095df5383f9c9cd0ea4103ecdd76e1acb5d62c51f3c57ce7fbead359394ca7a2

# Draft forecast response
{"slug":"fed-g17-capacity-utilization-total-industry-july-2026","country":"US","type":"data","title":"US Total Industry Capacity Utilization, July 2026","question":"Federal Reserve G.17 Capacity Utilization: Total industry, July 2026, seasonally adjusted percent of capacity, first print","unit":"percent","pointEstimate":76.14,"ciLow":75.62,"ciHigh":76.66,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"Federal Reserve G.17 Industrial Production and Capacity Utilization, Table 7","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g17/20260818/table7.htm","resolutionRule":"Resolve to the first official Federal Reserve G.17 July 2026 value for Table 7 Capacity Utilization, Total industry, seasonally adjusted percent of capacity, as first published on the August 18, 2026 release. Use the first-print value in percent, without later revisions; if only the one-decimal table value is available, use that official rounded value, otherwise use the corresponding first-print TCU value from the official/FRED-ALFRED release binding.","dataPointId":"fed.g17.capacity_utilization.total_industry.2026-07.first_print","historicalContext":[{"label":"2026-06 latest TCU","value":76.0937},{"label":"2026-05 TCU","value":76.1019},{"label":"2026-04 TCU","value":76.0625},{"label":"2026-03 TCU","value":75.5313},{"label":"2026-02 TCU","value":75.8299},{"label":"2026-01 TCU","value":75.242}],"drivers":["June total industry utilization was flat at 76.1 percent and 3.3 percentage points below its 1972-2025 average","manufacturing utilization edged down while mining and utilities rose in June","recent monthly TCU changes imply about 0.41 percentage point one-month dispersion","capacity growth and modest IP momentum point to little net July movement","upside risk from stronger utilities demand or another mining gain","downside risk from softer manufacturing output or reversal in mining/utilities"],"sourceContext":["https://www.federalreserve.gov/releases/g17/","https://www.federalreserve.gov/releases/g17/20260717/default.htm","https://www.federalreserve.gov/releases/g17/20260717/table7.htm","https://fred.stlouisfed.org/series/TCU","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TCU"],"runAt":"2026-07-25T16:00:46Z","reasoning":[{"kind":"heading","text":"US Total Industry Capacity Utilization, July 2026 First Print"},{"kind":"text","text":"Framing and exact resolver: this forecast is for Federal Reserve G.17 Table 7, Capacity Utilization, Total industry, seasonally adjusted percent of capacity, July 2026 first print. The ledger target uses series code TCU and first_print policy; FRED/ALFRED can mirror the history, but resolution should cite the Federal Reserve G.17 release."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 release calendar for 2026 monthly release dates","result":"The Federal Reserve G.17 page lists 2026 monthly releases including July 17 as the most recent monthly release and August 18, 2026 as the next monthly release at 9:15 a.m.; this verifies resolutionDate 2026-08-18 for July 2026 data."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 July 17, 2026 current release summary and Table 7","result":"The July 17, 2026 G.17 release says total capacity utilization was unchanged at 76.1 percent in June, 3.3 percentage points below its 1972-2025 average of 79.4; Table 7 shows total industry 2026 Jan 75.2, Feb 75.8, Mar 75.5, Apr 76.1, May 76.1, June 76.1."},{"kind":"tool","tool":"fred.lookup","call":"FRED/ALFRED TCU recent observations used as detailed public history mirror for the official G.17 series","result":"FRED TCU shows Jun 2026 76.0937, May 2026 76.1019, Apr 2026 76.0625, Mar 2026 75.5313, and Feb 2026 75.8299; updated July 17, 2026, with next release date August 18, 2026."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 July 2026 sector detail for current-release adjustment","result":"The June 2026 release reports total IP up 0.1 percent, manufacturing output unchanged, mining output up 0.4 percent, utilities output up 0.4 percent, manufacturing utilization 75.7, mining utilization 87.4, and utilities utilization 69.5."},{"kind":"text","text":"Reference class/base rate: for a one-month-ahead level forecast of a rate series, I anchor on persistence of the latest official/FRED TCU level and the recent same-series monthly changes, not on the long-run 79.4 average, because capacity utilization gaps tend to close slowly absent a large output shock."},{"kind":"text","text":"Level, momentum, and mechanism: the level anchor is June TCU 76.0937. Momentum is mildly positive because April-June stayed near 76.1 after a March dip, total IP still rose 0.1 percent in June, and mining/utilities rose 0.4 percent each; the offset is flat manufacturing output and manufacturing utilization easing to 75.7. I add only +0.05 percentage point for July because the target is a monthly rate and capacity growth mechanically dampens a small output increase."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest TCU 76.0937 from the official/FRED history; historical sample = detailed monthly TCU Dec 2025-Jun 2026 values 75.6422, 75.2420, 75.8299, 75.5313, 76.0625, 76.1019, 76.0937; adjustment components = +0.03 for recent IP/utilization momentum, +0.02 for mining/utilities strength, -0.00 for flat manufacturing net, so point = 76.0937 + 0.05 = 76.1437, rounded to 76.14. Interval method = sample standard deviation of successive monthly changes -0.4002, +0.5879, -0.2986, +0.5312, +0.0394, -0.0082; sigma = 0.411 percentage point, 80 percent half-width = 1.28*sigma = 0.526, so interval = 76.1437 +/- 0.526 = 75.62 to 76.66 after rounding."},{"kind":"text","text":"Counter-consideration: upside risk would come from a hot July utilities month plus another mining gain, which could push utilization above 76.66; downside risk would be a broad manufacturing pullback or a reversal in mining/utilities that would land below the interval. Outside the interval requires about a 0.57 percentage point rise or a 0.47 percentage point drop from the June detailed level, larger than most recent non-shock monthly moves."},{"kind":"forecast","point":76.14,"ciLow":75.62,"ciHigh":76.66}]}
