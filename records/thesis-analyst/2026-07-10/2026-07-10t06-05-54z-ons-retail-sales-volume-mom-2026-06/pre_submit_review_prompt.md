# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.retail_sales.volume_mom
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-retail-sales-volume-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "ons.retail_sales.volume_mom.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-23", "start": "2026-07-15"}, "field": "official_release:ons:retail_sales:2026-05:volume_mom", "releasePolicy": "first_print", "sourceSeriesId": "ons.retail_sales.volume_mom", "sourceUrl": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026", "table": "Retail sales, Great Britain: May 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-c06ec0e3a9bd14e9983b654f0fce440dc106ef4863d6a5d7624e3ebfa0f49893.json"
- targetContentHash: "c06ec0e3a9bd14e9983b654f0fce440dc106ef4863d6a5d7624e3ebfa0f49893"
- registeredAtUtc: "2026-07-10T05:58:27Z"
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
77b10570c2bda3454309928ab358b6befd3bf1ae7f99aa3d6d58ec5ddf3c1378

# Draft forecast response
{"slug":"ons-retail-sales-volume-mom-june-2026","country":"UK","type":"data","title":"ONS retail sales volume m/m, June 2026","question":"ONS Retail Sales Index, Great Britain, all retailing quantity bought volume, seasonally adjusted month-on-month percentage growth for June 2026, first print","unit":"percent_growth","pointEstimate":0.2,"ciLow":-1.2,"ciHigh":1.6,"confidence":0.8,"resolutionDate":"2026-07-24","resolutionSource":"Office for National Statistics Retail sales, Great Britain: June 2026","resolutionSourceUrl":"https://www.ons.gov.uk/releases/retailsalesgreatbritainjune2026","resolutionRule":"Resolve to the first ONS-published estimate of seasonally adjusted all-retailing quantity bought retail sales volume month-on-month percentage growth for June 2026 in Retail sales, Great Britain: June 2026 or its linked Retail Sales Index time-series dataset. Use the first official print released on 24 July 2026 at 7:00am UK time; do not use later revisions. Values are percentage growth rates, recorded to the ONS published precision. The registered ledger source URL appears to point to May 2026 and its country field says US; this forecast remains tied to the June 2026 ONS target by slug and dataPointId, but the exact public resolver is the ONS June 2026 release page.","dataPointId":"ons.retail_sales.volume_mom.june_2026.first_print","historicalContext":[{"label":"May 2026 m/m first estimate in latest ONS bulletin","value":1.2},{"label":"April 2026 m/m revised in May bulletin","value":-1.0},{"label":"March 2026 m/m revised in May bulletin","value":0.7},{"label":"February 2026 m/m revised in March bulletin","value":-0.6},{"label":"January 2026 m/m revised in March bulletin","value":1.8},{"label":"December 2025 m/m in December bulletin","value":0.4}],"drivers":["May 2026 strength creates mean-reversion risk for June","Hot weather and promotions supported non-store and department-store volumes in May","Fuel-stockpiling reversal made April unusually weak and May partly rebound-driven","Seasonally adjusted all-retailing volumes are volatile month to month","ONS annual seasonal-adjustment improvements scheduled with the June release add first-print uncertainty"],"sourceContext":["https://www.ons.gov.uk/releases/retailsalesgreatbritainjune2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/april2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/march2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/february2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsales"],"runAt":"2026-07-10T06:06:10Z","reasoning":[{"kind":"heading","text":"June 2026 ONS retail sales volume m/m forecast"},{"kind":"text","text":"Framing and exact resolver: forecast the ONS Retail Sales Index all-retailing quantity bought volume, Great Britain, seasonally adjusted monthly percentage change for June 2026, first print. The public ledger registration appears internally inconsistent because the country is listed as US and the source URL/sourceBinding point to May 2026, while the question, slug, and dataPointId are for the ONS June 2026 Great Britain release."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS upcoming release page for Retail Sales; Great Britain: June 2026.","result":"ONS release page states Retail Sales; Great Britain: June 2026 release date is 24 July 2026 at 7:00am and describes it as a first estimate of retail sales in volume and value terms, seasonally and non-seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS Retail sales, Great Britain: May 2026 bulletin for latest all-retailing volume monthly growth and source variant.","result":"Latest bulletin released 19 June 2026 says retail sales volumes rose 1.2% in May 2026, following a fall of 1.0% in April 2026 and a rise of 0.7% in March 2026; three-month growth to May was 0.4%, year-on-year growth was 3.2%, survey response rate was 57.0%, and turnover coverage was 85.0%."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS March, February, January, and December retail-sales bulletins for recent official monthly reference points.","result":"ONS March 2026 bulletin reported March 2026 up 0.7%, February 2026 down 0.6%, and January 2026 up 1.8%; ONS January 2026 bulletin reported December 2025 up 0.4%; ONS December 2025 bulletin reported November 2025 down 0.1% and October 2025 down 0.8%."},{"kind":"text","text":"Reference class/base rate: the recent official same-variant reference class is the seasonally adjusted all-retailing volume monthly growth rate itself, not value sales, online-only sales, or non-seasonally adjusted volumes. The last six fetched values used for the base rate are 0.4, 1.8, -0.6, 0.7, -1.0, and 1.2, averaging about 0.42 percentage points."},{"kind":"tool","tool":"official.lookup","call":"Checked the ONS dataset and quality notes for variant and first-print context.","result":"Retail Sales Index time series dataset ID DRSI was released 19 June 2026 with next release 24 July 2026; the May bulletin says seasonal adjustment uses X-13ARIMA-SEATS, the June release will implement annual seasonal-adjustment improvements on 24 July 2026, and May 2026 response metrics were 57.0% returned forms and 85.0% turnover coverage."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is the six-month official same-variant mean, (0.4 + 1.8 - 0.6 + 0.7 - 1.0 + 1.2) / 6 = 0.42. Adjustment components: -0.30 for payback after May's 1.2% weather/promotion rebound and earlier fuel volatility, +0.10 for continued warm-weather support to summer and non-store demand, yielding 0.22 and rounded to 0.2. Interval method uses realized dispersion of monthly change values themselves for this change/flow target: sample sigma = 1.06 from [0.4, 1.8, -0.6, 0.7, -1.0, 1.2]; 80% half-width is roughly 1.28*sigma = 1.36, rounded to 1.4, so 0.2 +/- 1.4 gives -1.2 to 1.6."},{"kind":"text","text":"Counter-considerations: upside risk is a June heatwave, outdoor-goods demand, or online/non-store strength that keeps momentum near May's pace and would land above the interval if growth exceeds 1.6%. Downside risk is consumer caution, reversal of May promotion pull-forward, or another fuel/non-food setback that would land below the interval if growth is less than -1.2%."},{"kind":"forecast","point":0.2,"ciLow":-1.2,"ciHigh":1.6}]}
