# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cpi.u.core_mom
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-core-cpi-mom-august-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.u.core_mom.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-16", "start": "2026-09-08"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-16", "start": "2026-09-08"}, "field": "bls.cpi.u.core_mom", "releasePolicy": "first_print", "sourceSeriesId": "bls.cpi.u.core_mom", "sourceUrl": "https://www.bls.gov/news.release/cpi.nr0.htm", "table": "U.S. Bureau of Labor Statistics Consumer Price Index news release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-7f06e063b1a3cfb4fc7b99061e8dd2223e358084787c4cee16f470e22eaf5e12.json"
- targetContentHash: "7f06e063b1a3cfb4fc7b99061e8dd2223e358084787c4cee16f470e22eaf5e12"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"
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
f76b0459167b252a8e61a6268d7981f9c53c2adc9b075a1e8d45218a5a58174f

# Draft forecast response
{"slug":"us-core-cpi-mom-august-2026","country":"US","type":"data","title":"US Core CPI MoM, Aug. 2026","question":"What will the BLS first print report for seasonally adjusted CPI-U all items less food and energy month-over-month percent change in August 2026?","unit":"percent_growth","pointEstimate":0.24,"ciLow":0.08,"ciHigh":0.40,"confidence":0.8,"resolutionDate":"2026-09-11","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index news release","resolutionSourceUrl":"https://www.bls.gov/news.release/cpi.nr0.htm","resolutionRule":"Resolve to the first BLS Consumer Price Index news release print for August 2026, Table A, CPI-U U.S. city average, seasonally adjusted percent change from preceding month for all items less food and energy, in percent, using the initially published value and not later seasonal-factor revisions.","dataPointId":"bls.cpi.u.core_mom.august_2026.first_print","historicalContext":[{"label":"2026-06 core CPI-U SA m/m","value":0.0},{"label":"2026-05 core CPI-U SA m/m","value":0.2},{"label":"2026-04 core CPI-U SA m/m","value":0.4},{"label":"2026-03 core CPI-U SA m/m","value":0.2},{"label":"2026-06 core CPI-U 12-month NSA","value":2.6}],"drivers":["June core CPI zero looks partly one-off and likely mean-reverts","Shelter slowed to 0.1 percent in June, limiting upside","Core goods and vehicle categories were soft in June","Services ex-energy were flat in June after 0.3 percent in May","Tariff or import-cost pass-through remains an upside risk"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.nr0.htm"],"runAt":"2026-08-11T12:55:31Z","reasoning":[{"kind":"heading","text":"US core CPI-U month-over-month forecast for August 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is CPI-U U.S. city average, all items less food and energy, seasonally adjusted, percent change from the preceding month for August 2026. The ledger window is 2026-09-08 to 2026-09-16; the BLS CPI release calendar gives the concrete August 2026 CPI release date as September 11, 2026 at 08:30 ET, so I use 2026-09-11 as the resolution date."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS CPI release schedule page for the August 2026 reference month.","result":"Fetched official schedule: August 2026 Consumer Price Index release date is Sep. 11, 2026 and release time is 08:30 AM; July 2026 is Aug. 12, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Read the current BLS CPI news release for June 2026 and Table A.","result":"Fetched Table A core CPI-U seasonally adjusted monthly changes: Dec. 2025 0.2, Jan. 2026 0.3, Feb. 2026 0.2, Mar. 2026 0.2, Apr. 2026 0.4, May 2026 0.2, Jun. 2026 0.0; 12-month core CPI through Jun. 2026 was 2.6."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS June 2026 release narrative for component momentum.","result":"Fetched June 2026 details: all items less food and energy was 0.0; shelter rose 0.1; owners' equivalent rent rose 0.2; rent rose 0.1; lodging away from home fell 2.3; motor vehicle insurance fell 2.0; communication fell 1.5; apparel fell 0.6; used cars and trucks fell 0.2."},{"kind":"text","text":"Reference class and base rate: for this change-flow target I anchor on the recent official BLS core CPI-U SA monthly changes themselves. The seven-month reference class average from Dec. 2025 through Jun. 2026 is 1.5 / 7 = 0.214 percent, and the 12-month core rate of 2.6 percent is consistent with a monthly pace near 0.21 percent."},{"kind":"text","text":"The target is the seasonally adjusted CPI-U core variant, not NSA CPI, chained CPI, all-items CPI, or a later revised seasonal-adjustment vintage; all anchors above are from the same BLS CPI-U core seasonally adjusted Table A variant except the separately labeled 12-month core context."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent BLS Table A reference class, Dec. 2025-Jun. 2026 core monthly values [0.2, 0.3, 0.2, 0.2, 0.4, 0.2, 0.0], mean 0.214. Adjustment components: +0.04 for mean reversion after June's unusually soft 0.0 and several one-off category declines, -0.02 for shelter cooling to 0.1 and soft core goods, net point about 0.24. Interval method uses the sample dispersion of those fetched monthly change values: sigma = 0.12, so 1.28*sigma = 0.15. Applying a roughly symmetric 80% band around 0.24 gives 0.24 - 0.16 = 0.08 and 0.24 + 0.16 = 0.40."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in motor vehicle insurance, lodging, communication, or tariff-sensitive core goods that would land above the interval if August core runs over 0.40. Downside risk is another month of shelter deceleration plus falling medical care, apparel, or used vehicles that would land below the interval if August core is under 0.08. An outside the interval outcome is most likely from broad services reacceleration or a second unusually weak one-off month."},{"kind":"forecast","point":0.24,"ciLow":0.08,"ciHigh":0.40}]}
