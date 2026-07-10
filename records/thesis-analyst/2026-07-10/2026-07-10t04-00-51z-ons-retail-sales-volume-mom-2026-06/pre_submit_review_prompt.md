# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.retail_sales.volume_mom
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-retail-sales-volume-mom-june-2026"
- targetUnit: "percent_growth"
- dataPointId: "ons.retail_sales.volume_mom.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-23", "start": "2026-07-15"}, "field": "official_release:ons:retail_sales:2026-05:volume_mom", "releasePolicy": "first_print", "sourceSeriesId": "ons.retail_sales.volume_mom", "sourceUrl": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026", "table": "Retail sales, Great Britain: May 2026", "transform": {"factor": 1, "operation": "identity"}}
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
4b5be6dfaf042a3dcda6d5b92e1c34fafb1df7cb735e4624bf5ad3c45ac057ea

# Draft forecast response
{"slug":"ons-retail-sales-volume-mom-june-2026","country":"UK","type":"data","title":"UK Retail Sales Volume MoM, Jun 2026","question":"What will the Office for National Statistics report as the first-print month-on-month percentage change in seasonally adjusted retail sales volumes, Great Britain, for June 2026?","unit":"percent_growth","pointEstimate":0.1,"ciLow":-1.4,"ciHigh":1.6,"confidence":0.8,"resolutionDate":"2026-07-24","resolutionSource":"Office for National Statistics Retail sales, Great Britain statistical bulletin","resolutionSourceUrl":"https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026","resolutionRule":"Resolve to the first ONS print of the seasonally adjusted all-retailing retail sales volume month-on-month percentage change for June 2026, in percentage points, as published in the Retail sales, Great Britain bulletin or Retail Sales Index dataset on 2026-07-24. Use the initial published value only; ignore later revisions. The ledger URL currently points to the May 2026 bulletin even though the period is June 2026; keep the target tied to dataPointId ons.retail_sales.volume_mom.june_2026.first_print and resolve against the June first-print value when released.","dataPointId":"ons.retail_sales.volume_mom.june_2026.first_print","historicalContext":[{"label":"2026-05 first-estimate/revised current bulletin","value":1.2},{"label":"2026-04 revised in May bulletin","value":-1.0},{"label":"2026-03 revised in May bulletin","value":0.7}],"drivers":["May weather-and-promotion boost creates payback risk","June heat can support seasonal goods and non-store demand","Recent monthly retail-volume growth is volatile around a modest positive base rate","Use seasonally adjusted all-retailing volume variant only"],"sourceContext":["https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexreferencetables","https://www.ons.gov.uk/releasecalendar"],"runAt":"2026-07-10T04:01:56Z","reasoning":[{"kind":"heading","text":"ONS retail sales volume MoM, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the ONS Retail Sales Index all-retailing quantity bought, seasonally adjusted, month-on-month volume percentage change for Great Britain. The canonical ledger target is June 2026 first print, but the supplied resolutionSourceUrl and sourceBinding field point to the May 2026 bulletin and 2026-05; that appears to be a ledger discrepancy, so I keep the same slug, dataPointId, and resolver substance while noting that the June first-print value is the target."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Retail sales, Great Britain: May 2026 bulletin for latest same-variant monthly volume movements and next-release notice.","result":"Fetched numbers: release date 19 June 2026; next release 24 July 2026; May 2026 retail sales volumes +1.2% month on month; April 2026 -1.0% month on month; March 2026 +0.7% month on month; three months to May 2026 +0.4%; year to May 2026 +3.2%."},{"kind":"tool","tool":"official.lookup","call":"Checked the ONS Retail Sales Index dataset page linked from the bulletin for dataset identity and release timing.","result":"Fetched numbers: dataset release date 19 June 2026; next release 24 July 2026; dataset covers retail sales in value and volume terms, seasonally and non-seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"Checked ONS release-calendar surface and bulletin announcement schedule for the resolution date rather than inferring from cadence.","result":"Fetched numbers: ONS release-calendar page showed 338 upcoming releases and recent entries at 9:30am; the ONS retail-sales bulletin specifically states next release 24 July 2026, which I use as the verified resolutionDate."},{"kind":"tool","tool":"official.lookup","call":"Read ONS same-release quality and component notes for May 2026 to condition the June forecast.","result":"Fetched numbers: May 2026 Retail Sales Index survey response rate was 57.0%; returned-form response was 3.9 percentage points below the past-12-month average; turnover coverage was 85.0%; non-store retailers rose 6.1% month on month; online spending values rose 3.3% month on month; online share rose from 28.1% in April to 28.8% in May."},{"kind":"text","text":"Base rate/reference class: for this change/flow series, the latest same-variant ONS monthly values are +0.7, -1.0, and +1.2, averaging +0.3%. That outside-view base rate is mildly positive but dominated by noise and one-off weather/promotional effects."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is the recent ONS same-variant monthly sample for all-retailing seasonally adjusted volume growth, values [0.7, -1.0, 1.2], mean = 0.3. Adjustment components: -0.3 percentage point payback after May's hot-weather and promotion-led +1.2; +0.1 percentage point from continued summer/heat-sensitive demand and event-related discretionary spending; 0.0 percentage point from quality/timing because the first print should still capture the standard monthly survey. Final point = 0.3 - 0.3 + 0.1 = 0.1. Interval method: because this is a change series, compute dispersion from the fetched values themselves; sample sigma = 1.15, so 80% half-width is roughly 1.28*sigma = 1.47, rounded to 1.5. Interval = 0.1 +/- 1.5 = [-1.4, 1.6]."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: the recent level is not recessionary, with May up 3.2% on a year earlier, but month-to-month momentum alternates sharply. The key one-off is possible reversal of May's promotion and hot-weather boost, partly offset by June heat and summer goods. I do not see a direct policy mechanism large enough to move June retail volumes by more than normal monthly volatility."},{"kind":"text","text":"Counter-considerations: upside risk is another heat-driven or event-driven surge in non-store, department, clothing, outdoor, and electronics spending, which would land above the interval if broad store categories repeat May-scale gains. Downside risk is payback from May pull-forward, household caution, or disrupted shopping patterns, which would land below the interval if food and non-food both fall sharply. Outside the interval would require a monthly move below -1.4% or above +1.6%, larger than the fitted recent 80% band."},{"kind":"forecast","point":0.1,"ciLow":-1.4,"ciHigh":1.6}]}
