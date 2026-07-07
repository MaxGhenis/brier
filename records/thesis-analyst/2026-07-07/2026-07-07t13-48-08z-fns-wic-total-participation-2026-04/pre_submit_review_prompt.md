# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.wic.total_participation
- period: 2026-04
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-april-2026"
- targetUnit: "millions"
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
ee2c29f11cba66be070cfcb7827cd2f85ec7227aa45e632cb81adb41f4551301

# Draft forecast response
{"slug":"wic-participation-april-2026","country":"US","type":"data","title":"WIC participation, Apr 2026","question":"USDA Food and Nutrition Service WIC Participation and Costs national monthly data, April 2026 Total Participants, preliminary FY2026 first print, converted to millions of participants.","unit":"millions","pointEstimate":6.724,"ciLow":6.648,"ciHigh":6.8,"confidence":0.8,"resolutionDate":"2026-07-11","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the first USDA FNS WIC Participation and Costs monthly national-data print that includes April 2026, using the Total Participants column for April 2026 in the preliminary FY2026 monthly table. Convert the published whole-participant count to millions by dividing by 1,000,000 and round to three decimals. Ignore later revisions, annual-summary updates, FRED, and mirrors.","dataPointId":"fns.wic.total_participation.2026-04.first_print","historicalContext":[{"label":"Mar 2026 latest official total participants, millions","value":6.701661},{"label":"Feb 2026 official total participants, millions","value":6.66458},{"label":"Apr 2025 official total participants, millions","value":6.877215},{"label":"Apr 2024 official total participants, millions","value":6.722042},{"label":"Apr 2023 official total participants, millions","value":6.612619}],"drivers":["March 2026 first print recovered modestly from February","April usually runs slightly above March in recent WIC monthly tables","FY2026 level remains below FY2025 same-month participation","Children participants are the largest component of total WIC participation","First-print administrative timing can move monthly totals by several tens of thousands"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-6.pdf","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-7.pdf"],"runAt":"2026-07-07T13:48:19Z","reasoning":[{"kind":"heading","text":"Forecast USDA FNS WIC total participation for April 2026"},{"kind":"text","text":"Framing and exact resolver: this targets USDA FNS WIC Participation and Costs national monthly data, preliminary FY2026, Total Participants for April 2026. This is the monthly national total-participants variant, not annual average participation, state-level category detail, or costs; all anchors below use the same Total Participants column."},{"kind":"tool","tool":"official.lookup","call":"Opened the USDA FNS WIC Data Tables page to verify the official source family and linked resource structure.","result":"Fetched official WIC Data Tables page showing Monthly Data - National Level as FY 2022 through November 2025, Monthly Data - State Level FY 2026 preliminary, Latest Available Month resource links, and Page updated February 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA FNS WIC Participation and Costs monthly PDF 37wic-monthly-6.pdf for the latest pre-target national monthly values.","result":"Fetched FY2026 preliminary Total Participants: Oct 2025 6,909,938; Nov 2025 6,771,734; Dec 2025 6,712,611; Jan 2026 6,696,300; Feb 2026 6,664,580; Mar 2026 6,701,661; the file states Data as of June 12, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read same-month and adjacent-month official history from the same FNS monthly table to form the seasonal reference class.","result":"Fetched Total Participants: Mar 2023 6,621,311 and Apr 2023 6,612,619; Mar 2024 6,680,974 and Apr 2024 6,722,042; Mar 2025 6,850,836 and Apr 2025 6,877,215."},{"kind":"tool","tool":"official.lookup","call":"Checked official monthly vintage timing using FNS WIC monthly PDFs and the WIC data-table source surface.","result":"Fetched prior monthly vintage evidence: 37wic-monthly-6.pdf is Data as of June 12, 2026 and includes Mar 2026 but not Apr 2026; 37wic-monthly-7.pdf is Data as of July 11, 2025 and includes Apr 2025, supporting a July 11 scheduled monthly vintage for the April monthly table target."},{"kind":"text","text":"Base rate/reference class: recent March-to-April changes in the same official Total Participants column were -0.008692 million in 2023, +0.041068 million in 2024, and +0.026379 million in 2025, an average April seasonal increment of +0.019585 million. The latest level is lower than FY2025, so I use a level-adjusted seasonal prior rather than the raw April average of 6.737 million across 2023-2025."},{"kind":"text","text":"Level, momentum, and mechanism: the level anchor is Mar 2026 at 6.701661 million. Momentum improved from Feb to Mar by +0.037081 million after declines from Oct through Feb, but Mar 2026 remained 0.149175 million below Mar 2025. Mechanically, children remain the largest component and rose from 3,808,769 in Feb 2026 to 3,824,372 in Mar 2026, while infant and women counts remain below 2025 levels."},{"kind":"math","text":"Prior/update/interval: model is seasonal persistence using official Total Participants history. Historical sample is FY2026 Oct-Mar successive changes plus 2023-2025 March-to-April changes: -0.138204, -0.059123, -0.016311, -0.031720, +0.037081, -0.008692, +0.041068, +0.026379 million. Adjustment components: March 2026 level 6.701661 + average March-to-April seasonal increment 0.019585 = 6.721246; year-over-year ratio anchor is Apr 2025 6.877215 * (Mar 2026 6.701661 / Mar 2025 6.850836) = 6.727466. Averaging gives 6.724356, rounded to 6.724. Interval method uses realized successive-change dispersion: sigma = 0.059650 million, so 1.28*sigma = 0.076352 million; 6.724 +/- 0.076 gives final implied bounds 6.648 to 6.800 million."},{"kind":"text","text":"Counter-consideration: upside risk would be a stronger administrative catch-up or broader spring recertification rebound, putting the first print above 6.800 million. Downside risk would be continued FY2026 participation erosion, weak infant/women counts, or reporting delays that leave April near March or below, which would land below the interval."},{"kind":"forecast","point":6.724,"ciLow":6.648,"ciHigh":6.8}]}
