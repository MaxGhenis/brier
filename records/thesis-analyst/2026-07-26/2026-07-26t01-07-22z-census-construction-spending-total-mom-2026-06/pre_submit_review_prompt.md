# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.construction_spending.total_mom
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-construction-spending-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.construction_spending.total_mom.2026_06.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-03", "start": "2026-08-03"}, "field": "TTLCONS", "releasePolicy": "first_print", "sourceSeriesId": "TTLCONS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TTLCONS", "table": "Value of Construction Put in Place Survey", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-9556fc5386456478cfc719b06a95f8b8a7e3afbff792293f2bb96d8d77565a3e.json"
- targetContentHash: "9556fc5386456478cfc719b06a95f8b8a7e3afbff792293f2bb96d8d77565a3e"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"
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
6ab1d71b41dae083dd9aaf317764045d3b7493fd25c2f873deb27b5d9208bbc1

# Draft forecast response
{"slug":"us-construction-spending-mom-june-2026","country":"US","type":"data","title":"US construction spending MoM, June 2026","question":"What will the U.S. Census Bureau first report as the month-over-month percent change in total construction spending, seasonally adjusted annual rate, for June 2026?","unit":"percent_growth","pointEstimate":0.05,"ciLow":-0.36,"ciHigh":0.46,"confidence":0.8,"resolutionDate":"2026-08-03","resolutionSource":"U.S. Census Bureau Monthly Construction Spending release","resolutionSourceUrl":"https://www.census.gov/construction/c30/current/index.html","resolutionRule":"Resolve to the first Census Monthly Construction Spending print for June 2026 total construction spending, seasonally adjusted annual rate. Use the headline month-over-month percent change versus the revised May 2026 estimate in that first release; if resolving from TTLCONS levels, compute 100*(June 2026 first-print SAAR / revised May 2026 SAAR in the same first-print release - 1), round to one decimal percentage point, and ignore later revisions.","dataPointId":"census.construction_spending.total_mom.2026_06.first_print","historicalContext":[{"label":"Feb 2026 revised MoM from TTLCONS levels","value":-0.271},{"label":"Mar 2026 revised MoM from TTLCONS levels","value":0.444},{"label":"Apr 2026 revised MoM from TTLCONS levels","value":0.348},{"label":"May 2026 revised MoM from TTLCONS levels","value":0.143}],"drivers":["Recent TTLCONS momentum is mildly positive but slowing","June housing starts rebounded while permits fell","Private residential spending remains rate-sensitive","Public construction is still a positive offset","May first print showed total spending only 0.1 percent higher"],"sourceContext":["https://www.census.gov/construction/c30/release.html","https://www.census.gov/construction/c30/current/index.html","https://fred.stlouisfed.org/series/TTLCONS","https://www.census.gov/construction/nrc/current/index.html"],"runAt":"2026-07-26T01:07:50Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 total construction spending MoM"},{"kind":"text","text":"Framing and exact resolver: this is the Census Value of Construction Put in Place total construction series, seasonally adjusted annual rate, first print for June 2026. The ledger binds dataPointId census.construction_spending.total_mom.2026_06.first_print and TTLCONS; the economic target is the headline percent change from revised May to June in the first Census release."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Construction Spending release schedule for the June 2026 reporting period.","result":"Census schedule lists the June reporting period release date as August 3, 2026 at 10:00 a.m.; nearby rows show May on July 1, 2026 and July on September 1, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest Census Monthly Construction Spending release for current total, private, residential, nonresidential, and public construction levels.","result":"May 2026 total construction spending was $2,210.2 billion SAAR, 0.1 percent above revised April at $2,207.1 billion; May 2025 was $2,244.4 billion; private was $1,669.0 billion, residential $930.2 billion, nonresidential $738.7 billion, and public $541.2 billion."},{"kind":"tool","tool":"fred.lookup","call":"Checked public FRED/TTLCONS mirror of Census total construction spending levels for recent reference-class calculations.","result":"TTLCONS levels fetched from the public series page were May 2026 2,210,214 million, Apr 2026 2,207,051 million, Mar 2026 2,199,399 million, Feb 2026 2,189,683 million, and Jan 2026 2,195,636 million."},{"kind":"tool","tool":"official.lookup","call":"Checked Census/HUD New Residential Construction June 2026 release for current residential construction signal.","result":"June 2026 permits were 1,367,000 SAAR, 3.0 percent below revised May 1,410,000; housing starts were 1,427,000 SAAR, 19.0 percent above revised May 1,199,000; completions were 1,392,000 SAAR, 3.3 percent above revised May 1,347,000."},{"kind":"text","text":"Reference class/base rate: using recent TTLCONS level-implied total construction spending MoM changes, Feb through May 2026 were -0.271, +0.444, +0.348, and +0.143 percent, averaging about +0.166 percent. The base rate is therefore mildly positive, but May's first-print headline was only +0.1 percent and year-to-date spending was reported 2.7 percent below the same 2025 period."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent Census/TTLCONS revised MoM history for Feb-May 2026, values -0.271, 0.444, 0.348, 0.143 percent. Adjustment components: -0.08 pp for falling June permits and still-soft private/residential conditions, +0.04 pp for the June starts/completions rebound, and -0.08 pp for slowing May total momentum versus the +0.166 base rate, giving a point near +0.05 percent. Interval method: sample dispersion of those four MoM values gives sigma = 0.317 percentage points; 1.28*sigma = 0.406 pp, so an 80 percent interval around 0.05 is about -0.36 to +0.46 percent after rounding."},{"kind":"text","text":"The variant is total construction spending, seasonally adjusted annual rate, not unadjusted monthly dollars and not a private-only, residential-only, or FRED-transformed growth variant. Public construction is a meaningful upside risk because May public spending was +0.5 percent MoM, while downside risk comes from private nonresidential weakness and permits down 3.0 percent in June. A broad public-construction surge with resilient private work would land above the interval; a sharp giveback in private residential or nonresidential work would land below the interval, outside the interval."},{"kind":"forecast","point":0.05,"ciLow":-0.36,"ciHigh":0.46}]}
