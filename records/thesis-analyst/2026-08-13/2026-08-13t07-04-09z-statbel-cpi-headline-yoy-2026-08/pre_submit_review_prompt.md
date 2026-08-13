# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statbel.cpi.headline_yoy
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "belgium-cpi-annual-rate-august-2026"
- country: "BE"
- targetUnit: "percent"
- dataPointId: "statbel.cpi.headline_yoy.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-09-03", "start": "2026-08-26"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["statbel.fgov.be"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "statbel.cpi.headline_yoy", "releasePolicy": "first_print", "sourceSeriesId": "statbel.cpi.headline_yoy", "sourceUrl": "https://statbel.fgov.be/en/themes/consumer-prices/consumer-price-index", "table": "Statbel Consumer Price Index - Health Index release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-13-178d47ff0072910f71ec7e34bc98bbb14b3691dc1b0cfeaace4d40ed98a34ec0.json"
- targetContentHash: "178d47ff0072910f71ec7e34bc98bbb14b3691dc1b0cfeaace4d40ed98a34ec0"
- registrationCommit: "448b17e91d8ee0fa53f512a75460719c172b1358"
- registeredAtUtc: "2026-08-13T06:52:40Z"
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
630b54b4388cf16d71c23c45407e370436495a5453ff2021fe32d846f7bc37eb

# Draft forecast response
{"slug":"belgium-cpi-annual-rate-august-2026","country":"BE","type":"data","title":"Belgium CPI annual inflation, August 2026 first print","question":"What will Statbel's not-seasonally-adjusted headline consumer price index annual inflation rate (MS_CPI_INFL), base year 2025, for Belgium in August 2026 be on the first Consumer Price Index - Health Index print?","unit":"percent","pointEstimate":3.55,"ciLow":2.71,"ciHigh":4.4,"confidence":0.8,"resolutionDate":"2026-09-03","resolutionSource":"Statbel Consumer Price Index - Health Index release","resolutionSourceUrl":"https://statbel.fgov.be/en/themes/consumer-prices/consumer-price-index","resolutionRule":"Resolve to Statbel's Consumer Price Index - Health Index first print for m-2026-08: field MS_CPI_INFL for NM_YR=2026, NM_MTH=8, NM_BASE_YR=2025 in the official Consumer price index and health index open-data file or equivalent first release table. Use the first print only, in percent as published; ignore later revisions. The registered ledger target sets resolutionDate to 2026-09-03 even though the fetched Statbel 2026 calendar lists Consumptieprijsindex - Gezondheidsindex m-2026-08 on 2026-08-28.","dataPointId":"statbel.cpi.headline_yoy.2026-08.first_print","historicalContext":[{"label":"Statbel MS_CPI_INFL 2026-02","value":1.45},{"label":"Statbel MS_CPI_INFL 2026-03","value":1.65},{"label":"Statbel MS_CPI_INFL 2026-04","value":4.01},{"label":"Statbel MS_CPI_INFL 2026-05","value":4.08},{"label":"Statbel MS_CPI_INFL 2026-06","value":3.4},{"label":"Statbel MS_CPI_INFL 2026-07","value":3.56}],"drivers":["July first-print persistence at 3.56%","FPB August CPI forecast 3.35% before July print","FPB July path undercalled Statbel July by 0.19 pp","recent first-print changes have 0.659 pp sigma"],"sourceContext":["https://statbel.fgov.be/en/open-data?category=All","https://statbel.fgov.be/sites/default/files/files/opendata/Consumptieprijsindex%20en%20gezondheidsindex/CPI%20All%20base%20years.zip","https://statbel.fgov.be/nl/calendar/2026","https://www.plan.be/en/data/consumer-price-index-inflation-forecasts","https://app.thesisinstitute.org/specs.json"],"runAt":"2026-08-13T07:04:18Z","reasoning":[{"kind":"heading","text":"Belgium Statbel CPI headline annual inflation forecast"},{"kind":"text","text":"Framing: this target is Statbel's national not-seasonally-adjusted headline consumer price index annual inflation field MS_CPI_INFL for August 2026, base year 2025, first print. The series is not a human-adjudicated market outcome; it resolves mechanically from Statbel's CPI/health-index release or the matching official open-data file."},{"kind":"tool","tool":"official.open_data","call":"curl Statbel open-data page for CPI download links","result":"Fetched official Statbel open-data listing: 'Consumer price index and health index', period since 1920, TXT ZIP length 106388 and XLSX length 422150; also 'Indexes by product group' XLSX length 14536586 and ZIP length 5128865."},{"kind":"tool","tool":"official.open_data","call":"download and parse Statbel CPI All base years TXT from the official ZIP","result":"Fetched Statbel CPI All base years TXT rows for NM_BASE_YR=2025: 2026-02 CPI index 101.72 and MS_CPI_INFL 1.45%; 2026-03 101.84 and 1.65%; 2026-04 103.34 and 4.01%; 2026-05 103.26 and 4.08%; 2026-06 102.95 and 3.40%; 2026-07 103.60 and 3.56%."},{"kind":"tool","tool":"official.calendar","call":"curl Statbel 2026 calendar around CPI/health-index releases","result":"Fetched Statbel 2026 calendar rows: 2026-07-30 'De inflatie bedraagt 3,56%' for the July CPI release; 2026-08-28 'Consumptieprijsindex - Gezondheidsindex' with period m-2026-08; 2026-09-29 'Consumptieprijsindex - Gezondheidsindex' with period m-2026-09."},{"kind":"tool","tool":"official.forecast","call":"curl Federal Planning Bureau CPI inflation forecasts page dated 07/07/2026","result":"Fetched FPB national consumer price index path: Jan 2026 1.10%, Feb 1.45%, Mar 1.65%, Apr 4.01%, May 4.08%, Jun 3.40%, Jul forecast 3.37%, Aug forecast 3.35%, Sep forecast 3.55%, and average 2026 inflation 3.1%."},{"kind":"text","text":"Base rate/reference class: the last 24 Statbel MS_CPI_INFL first-print observations from 2024-08 through 2026-07 have mean 2.68%, range 1.10%-4.08%, and latest 3.56%; the last 12 are 1.91, 2.12, 2.00, 2.40, 2.06, 1.10, 1.45, 1.65, 4.01, 4.08, 3.40, 3.56. For this repeated rate series, last-print persistence at 3.56% is the default prior."},{"kind":"text","text":"Model candidates: persistence candidate point 3.56, p10 2.72, p50 3.56, p90 4.40, 80% interval [2.72, 4.40], 90% interval [2.47, 4.65], interval method recent-change Gaussian with calibration_n 23 and train cutoff 2026-07. Bias-adjusted FPB candidate uses FPB August 3.35 plus the July forecast miss of +0.19, giving point 3.54 with the same interval method."},{"kind":"math","text":"Prior/update/interval: persistence prior is 3.56 from Statbel July 2026. Historical sample is the last 24 fetched MS_CPI_INFL values ending 2026-07; successive monthly changes have sigma = 0.659 percentage points, so 1.28*sigma = 0.843 pp. Current update is the FPB August forecast 3.35, adjusted by its July undercall versus Statbel first print (3.56 - 3.37 = +0.19), giving 3.54. Weighting 70% persistence and 30% bias-adjusted FPB gives 0.70*3.56 + 0.30*3.54 = 3.55. Applying the 0.843 half-width gives [2.71, 4.40]."},{"kind":"text","text":"Resolution-date discipline: the registered ledger target fixes resolutionDate at 2026-09-03 and I keep that field. The official Statbel calendar fetched this run lists the m-2026-08 CPI/health-index release on 2026-08-28, so this appears to be a ledger-date discrepancy rather than evidence about the value."},{"kind":"text","text":"Counter-considerations: upside risk would land above the interval if August repeats an energy or administered-price jump like the March-to-April 2026 move and headline inflation exceeds 4.40%. Downside risk would land below the interval if the July rebound reverses sharply through energy, travel, or communication-price cuts and the first print falls below 2.71%."},{"kind":"text","text":"Slug check: a curl fetch of https://app.thesisinstitute.org/specs.json returned a 404 HTML page, so I checked the local generated ledger target and registration instead; both contain catalogSlug belgium-cpi-annual-rate-august-2026 and dataPointId statbel.cpi.headline_yoy.2026-08.first_print."},{"kind":"forecast","point":3.55,"ciLow":2.71,"ciHigh":4.4}]}
