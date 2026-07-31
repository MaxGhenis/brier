# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.export_prices.all_commodities_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-export-prices-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.export_prices.all_commodities_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-18"}, "field": "IQ", "releasePolicy": "first_print", "sourceSeriesId": "IQ", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=IQ", "table": "U.S. Export Price Indexes, Table 2", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-c70ae67705958d569fcfb915e8c6947a4a000bc066bab9653ace68c2518960c6.json"
- targetContentHash: "c70ae67705958d569fcfb915e8c6947a4a000bc066bab9653ace68c2518960c6"
- registrationCommit: "0249a6f266d1d202c43782056e77403612358765"
- registeredAtUtc: "2026-07-31T14:48:09Z"
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
bbfe321b3042cee037c9012ddee27dd6efaad0c8dba97ae880ac9507a8536ca8

# Draft forecast response
{"slug":"us-export-prices-mom-july-2026","country":"US","type":"data","title":"US export prices MoM, Jul 2026","question":"What will the U.S. Bureau of Labor Statistics first report for the July 2026 monthly percent change in the not seasonally adjusted Export Price Index (End Use): All commodities?","unit":"percent_growth","pointEstimate":0.4,"ciLow":-1.1,"ciHigh":1.9,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"U.S. Bureau of Labor Statistics U.S. Import and Export Price Indexes news release, Table 2","resolutionSourceUrl":"https://www.bls.gov/news.release/ximpim.t02.htm","resolutionRule":"Resolve to the first BLS U.S. Import and Export Price Indexes release for July 2026, Table 2, Export Price Indexes by End Use, row All commodities, monthly percent change for June 2026 to July 2026. Use the first published one-decimal percent change, not seasonally adjusted, and ignore later revisions.","dataPointId":"bls.export_prices.all_commodities_mom.2026_07.first_print","historicalContext":[{"label":"2026-06 m/m, all exports","value":-0.6},{"label":"2026-05 m/m, all exports","value":1.2},{"label":"2026-04 m/m, all exports","value":3.5},{"label":"2026-03 m/m, all exports","value":1.7},{"label":"2026-02 m/m, all exports","value":1.9}],"drivers":["June decline followed several unusually strong spring prints","nonagricultural industrial supplies were the main June drag","finished-goods export prices were still rising in June","July energy-price strength adds upside risk to industrial-supplies exports","80% interval is sized from recent realized monthly dispersion"],"sourceContext":["https://www.bls.gov/schedule/2026/08_sched.htm","https://www.bls.gov/news.release/ximpim.nr0.htm","https://www.bls.gov/news.release/ximpim.t02.htm","https://fred.stlouisfed.org/series/IQ","https://www.eia.gov/dnav/pet/PET_PRI_SPT_S1_D.htm"],"runAt":"2026-07-31T14:53:13Z","reasoning":[{"kind":"heading","text":"Forecast for BLS all-commodities export prices, July 2026 first print"},{"kind":"text","text":"The resolver is the BLS not seasonally adjusted Export Price Index (End Use): All commodities, Table 2, first-print monthly percent change for July 2026. The BLS August 2026 release calendar lists U.S. Import and Export Price Indexes for July 2026 on August 18, 2026 at 08:30 Eastern, matching the ledger date."},{"kind":"tool","tool":"official.lookup","call":"BLS June 2026 U.S. Import and Export Price Indexes news release summary","result":"Fetched BLS summary: U.S. export prices decreased 0.6 percent in June 2026 after rising 1.2 percent in May; export prices were up 10.2 percent from June 2025 to June 2026."},{"kind":"tool","tool":"official.lookup","call":"BLS Table 2, Export Price Indexes by End Use","result":"Fetched Table 2 all-commodities row: May 2026 index 168.8, June 2026 index 167.8, annual change 10.2 percent, monthly changes were Feb-Mar 1.7, Mar-Apr 3.5, Apr-May 1.2, May-Jun -0.6."},{"kind":"tool","tool":"history.lookup","call":"FRED/ALFRED mirror for BLS series IQ, Export Price Index (End Use): All Commodities","result":"Fetched IQ index levels: Jun 2026 167.8, May 2026 168.8, Apr 2026 166.8, Mar 2026 161.1, Feb 2026 158.4; the Jun change from 168.8 to 167.8 is -0.592 percent, rounded by BLS to -0.6 percent."},{"kind":"tool","tool":"official.lookup","call":"EIA spot petroleum prices for July energy context","result":"Fetched EIA spot table: WTI Cushing was 69.60 dollars per barrel on 2026-07-06 and 79.20 on 2026-07-13; Brent was 69.56 on 2026-07-06 and 81.62 on 2026-07-13."},{"kind":"text","text":"Base rate / reference class: use the nonmissing BLS all-export monthly percent changes shown in the latest release table from June 2025 through June 2026: 0.5, 0.3, 0.1, 0.0, 0.6, 0.5, 1.9, 1.7, 3.5, 1.2, -0.6. The sample mean is 0.88 percent and the median is 0.5 percent; October and November 2025 were not usable for this row because the BLS release notes missing values during the appropriations lapse."},{"kind":"text","text":"The same not seasonally adjusted all-commodities export variant is used throughout: BLS Table 2 row All commodities, series IQ in the FRED mirror. I am not using FRED as the resolver, only as a public mirror of the BLS index levels."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent reference-class median of +0.5 percent, with the mean +0.88 pulled down because the spring surge of +1.9, +1.7, +3.5, and +1.2 was followed by a June reversal of -0.6. I apply -0.2 percentage point for mean reversion after the spring spike and +0.1 percentage point for July energy/industrial-supplies upside, giving a point forecast of +0.4 percent. For the 80% interval, use the values themselves for this change series; from the 11 nonmissing BLS monthly changes, sigma = 1.14 percentage points, so 1.28*sigma = 1.46 percentage points. Rounding the half-width to 1.5 gives +0.4 +/- 1.5, or [-1.1, 1.9]."},{"kind":"text","text":"Upside risk: another July jump in petroleum, natural gas, metals, or industrial supplies would land above the interval if it pushed all-commodities exports above about +1.9 percent. Downside risk: a renewed reversal in nonagricultural industrial supplies or a broad commodity selloff would land below the interval if the first print were below -1.1 percent."},{"kind":"forecast","point":0.4,"ciLow":-1.1,"ciHigh":1.9}]}
