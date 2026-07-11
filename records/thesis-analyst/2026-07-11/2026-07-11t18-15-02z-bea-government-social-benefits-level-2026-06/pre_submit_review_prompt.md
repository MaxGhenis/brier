# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bea.government_social_benefits.level
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-government-social-benefits-level-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.government_social_benefits.level.june_2026.first_print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=A063RC1&vintage_date=2026-06-25"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "A063RC1", "releasePolicy": "first_print", "sourceSeriesId": "A063RC1", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=A063RC1&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-9ff32676acb57877e9b6c73c923544fceea7817cc4e300041781188cd157cc14.json"
- targetContentHash: "9ff32676acb57877e9b6c73c923544fceea7817cc4e300041781188cd157cc14"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"
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
1eb3933b25e5b42146612a619f2c5e4b1b58356bd7ab849a48825a0e46f0bfca

# Draft forecast response
{"slug":"bea-government-social-benefits-level-june-2026","country":"US","type":"data","title":"US government social benefits, June 2026","question":"What will BEA first report for June 2026 personal current transfer receipts: government social benefits to persons (A063RC1), monthly, seasonally adjusted at an annual rate, in billions of dollars?","unit":"usd_billions","pointEstimate":5028.3,"ciLow":5005.4,"ciHigh":5051.2,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays, Table 2.6","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=A063RC1&vintage_date=2026-06-25","resolutionRule":"Resolve to the June 2026 value of BEA series A063RC1, Personal current transfer receipts: government social benefits to persons, monthly seasonally adjusted annual rate, in billions of dollars, as first published in the July 30, 2026 Personal Income and Outlays release; use the displayed one-decimal value and ignore later revisions. The registered resolver has a concrete discrepancy: its ALFRED vintage_date=2026-06-25 predates the June release and cannot contain the June first print, while BEA's official calendar places the release on July 30 rather than within the registered July 21–29 window. This forecast remains tied to the registered dataPointId and resolver URL, but resolution machinery must correct that binding to the July 30 first-print vintage.","dataPointId":"bea.government_social_benefits.level.june_2026.first_print","historicalContext":[{"label":"January 2026","value":5002.8},{"label":"February 2026","value":4988.0},{"label":"March 2026","value":4991.0},{"label":"April 2026","value":4995.7},{"label":"May 2026","value":5024.4}],"drivers":["May level provides the persistence anchor","Recent monthly changes show modest underlying growth with occasional benefit-payment jumps","Social Security and Medicaid source-data revisions create first-print uncertainty","No identified June policy change warrants extrapolating May's unusually large increase"],"sourceContext":["https://fred.stlouisfed.org/series/A063RC1/","https://www.bea.gov/sites/default/files/2026-06/pi0526.pdf","https://www.bea.gov/news/schedule/"],"runAt":"2026-07-11T18:15:26Z","reasoning":[{"kind":"heading","text":"June 2026 government social benefits first-print forecast"},{"kind":"text","text":"The target is BEA account A063RC/A063RC1 in NIPA Table 2.6: monthly personal current transfer receipts from government social benefits, billions of dollars at a seasonally adjusted annual rate. It resolves on the first June 2026 print, not a later revised observation."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest published A063RC1 monthly observations and units from the BEA-sourced FRED series page.","result":"Fetched January 2026 5002.8, February 4988.0, March 4991.0, April 4995.7, and May 5024.4 billion dollars, monthly seasonally adjusted annual rate."},{"kind":"tool","tool":"official.lookup","call":"Inspect BEA's May 2026 Personal Income and Outlays release for contemporaneous aggregate-income conditions.","result":"BEA reported May personal income up 181.6 billion, disposable personal income up 164.9 billion, and PCE up 156.1 billion; the release also reported revisions to Social Security and Medicaid benefits."},{"kind":"tool","tool":"official.lookup","call":"Calculate the recent A063RC1 reference-class changes from the fetched monthly observations.","result":"Fetched-level successive changes were -14.8, +3.0, +4.7, and +28.7 billion from January through May 2026; their mean was +5.4 billion and sample standard deviation was 17.9 billion."},{"kind":"text","text":"The reference class and base rate are short-horizon monthly level forecasts for this same SAAR series. Persistence is the primary prior: May's 5024.4 level is more informative than extrapolating its exceptional +28.7 increase, while the four-change mean of +5.4 indicates a gently rising underlying path."},{"kind":"text","text":"BEA's official release calendar, corroborated by the May release itself, schedules Personal Income and Outlays for June 2026 at 8:30 a.m. on July 30, 2026. This conflicts with the registered expected window ending July 29 and with its June 25 ALFRED vintage, which is too early to resolve June."},{"kind":"math","text":"Prior/update/interval: persistence model prior = May 5024.4; historical sample = January–May 2026 levels with changes -14.8, +3.0, +4.7, +28.7. Adjustment components are +3.9 billion for the median recent monthly change, +0.0 for known one-offs, and +0.0 for identified June policy changes, giving 5024.4 + 3.9 = 5028.3. From the four successive changes, sample sigma = 17.9 billion; the normal-reference 80% half-width is 1.28*sigma = 1.28*17.9 = 22.9 billion. Thus the final implied bounds are 5028.3 - 22.9 = 5005.4 and 5028.3 + 22.9 = 5051.2."},{"kind":"text","text":"Upside risk comes from another discrete acceleration in Social Security, Medicare, Medicaid, veterans, or disaster-related benefits and would land above the interval if the June increase exceeds about 26.8 billion. Downside risk comes from payment timing, normalization after May, or adverse first-print source-data revisions and would land below the interval if June falls more than about 19.0 billion."},{"kind":"forecast","point":5028.3,"ciLow":5005.4,"ciHigh":5051.2}]}
