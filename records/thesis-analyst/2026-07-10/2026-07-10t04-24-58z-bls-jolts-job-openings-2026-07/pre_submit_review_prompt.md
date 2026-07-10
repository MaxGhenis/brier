# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.jolts.job_openings
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-openings-july-2026"
- targetUnit: "millions"
- dataPointId: "bls.jolts.job_openings.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "bls.jolts.job_openings", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.job_openings", "sourceUrl": "https://www.bls.gov/news.release/jolts.nr0.htm", "table": "U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey", "transform": {"factor": 0.001, "operation": "multiply"}}
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
f6f9bcb4d42197fda7975b4e19a73872c598ebef2d229661c932427d7b6024bd

# Draft forecast response
{"slug":"jolts-openings-july-2026","country":"US","type":"data","title":"July 2026 JOLTS Job Openings","question":"What will the U.S. Bureau of Labor Statistics first report as total nonfarm job openings, seasonally adjusted, for July 2026 in the Job Openings and Labor Turnover Survey?","unit":"millions","pointEstimate":7.45,"ciLow":6.67,"ciHigh":8.23,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey, Table 1","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t01.htm","resolutionRule":"Resolve to the first BLS-published July 2026 seasonally adjusted Total job openings level in Table 1, Job openings levels and rates by industry and region, seasonally adjusted. The BLS table reports levels in thousands; divide by 1000 and report in millions. Use the first print released on September 1, 2026, and do not use later revisions or annual re-estimates.","dataPointId":"bls.jolts.job_openings.july_2026.first_print","historicalContext":[{"label":"May 2026 total job openings SA first/current table","value":7.594},{"label":"Apr 2026 total job openings SA","value":7.585},{"label":"Mar 2026 total job openings SA","value":6.887},{"label":"Feb 2026 total job openings SA","value":6.922},{"label":"Jan 2026 total job openings SA from FRED mirror","value":7.24}],"drivers":["May openings held near April's elevated level","June payroll growth slowed to 57,000","May hires slipped to 5.170 million","Quits rate remained low at 1.9 percent","Layoffs rose modestly but stayed contained"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/news.release/jolts.t01.htm","https://www.bls.gov/news.release/jolts.t02.htm","https://www.bls.gov/news.release/jolts.t04.htm","https://www.bls.gov/news.release/jolts.t05.htm","https://www.bls.gov/news.release/empsit.nr0.htm","https://fred.stlouisfed.org/series/JTSJOL"],"runAt":"2026-07-10T04:25:14Z","reasoning":[{"kind":"heading","text":"Forecast for BLS JOLTS total job openings, July 2026 first print"},{"kind":"text","text":"The target is the seasonally adjusted Total job openings level in BLS JOLTS Table 1 for July 2026, reported in thousands and converted to millions. The BLS JOLTS release schedule verifies the July 2026 reference month is scheduled for Sep. 01, 2026 at 10:00 AM, which I use as the resolutionDate. This is the SA Total variant throughout; the series is mirrored by FRED as JTSJOL, but resolution is to BLS Table 1."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Table 1 for current job openings levels and rates, seasonally adjusted.","result":"BLS Table 1 Total job openings levels in thousands: May 2025 7,310; Feb 2026 6,922; Mar 2026 6,887; Apr 2026 7,585; May 2026 preliminary 7,594; Apr-to-May change +9; May 2026 openings rate 4.6 percent."},{"kind":"tool","tool":"official.lookup","call":"Read FRED JTSJOL as a BLS-source history mirror for the same seasonally adjusted total nonfarm job openings series.","result":"FRED JTSJOL showed May 2026 7,594 thousand, Apr 2026 7,585 thousand, Mar 2026 6,887 thousand, Feb 2026 6,922 thousand, and Jan 2026 7,240 thousand; units are Level in Thousands, Seasonally Adjusted, updated Jun 30, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Table 2 for hires, seasonally adjusted, as a current labor-demand confirmation signal.","result":"BLS Table 2 Total hires levels in thousands: May 2025 5,328; Feb 2026 4,899; Mar 2026 5,535; Apr 2026 5,215; May 2026 preliminary 5,170; Apr-to-May change -45; May 2026 hires rate 3.3 percent."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Tables 4 and 5 for quits and layoffs/discharges, seasonally adjusted.","result":"BLS Table 4 Total quits were 3,065 thousand in May 2026 with a 1.9 percent quits rate, up 22 thousand from Apr 2026; BLS Table 5 layoffs and discharges were 1,708 thousand in May 2026 with a 1.1 percent rate, up 41 thousand from Apr 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Employment Situation for June 2026 as a same-labor-market nowcast signal between the May JOLTS release and July target month.","result":"BLS Employment Situation for June 2026 reported total nonfarm payroll employment +57,000, unemployment rate 4.2 percent, unemployed people 7.1 million, labor force participation 61.5 percent, and prior-12-month average payroll change +36,000."},{"kind":"text","text":"Base rate/reference class: for a two-month-ahead level forecast on JOLTS openings, a persistence/random-walk prior usually beats a strong directional call unless payrolls, hires, or layoffs show a decisive break. The latest level is 7.594 million, but the April-to-May plateau after a large March-to-April jump and softer June payroll signal argue for modest mean reversion rather than extrapolating the April surge."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 openings 7.594 million. Historical sample for volatility = fetched Jan-May 2026 same-series levels 7.240, 6.922, 6.887, 7.585, 7.594 million, giving monthly changes -0.318, -0.035, +0.698, +0.009. Sample sigma = 0.431 million. Adjustment components: -0.06 million for May hires falling to 5.170 million, -0.04 million for quits still low at 1.9 percent and layoffs up to 1.708 million, -0.04 million for June payroll slowing to +57,000, -0.004 rounding/level judgment, so point = 7.594 - 0.144 = 7.45 million. For a two-month horizon, half-width = 1.28 * sqrt(2) * sigma = 1.28 * 1.414 * 0.431 = 0.78 million, so 80 percent interval = 7.45 +/- 0.78 = [6.67, 8.23]."},{"kind":"text","text":"Counter-considerations: upside risk is that April's professional-and-business-services openings rebound persists and July postings remain above 8 million; downside risk is a retrenchment from weak hires and slow payroll growth that pulls openings toward early-2026 levels. A broad white-collar reopening plus low layoffs would land above the interval; a summer demand shock with hires and openings both falling would land below the interval."},{"kind":"forecast","point":7.45,"ciLow":6.67,"ciHigh":8.23}]}
