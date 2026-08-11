# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.ces.nonfarm_payrolls.change
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "nonfarm-payrolls-august-2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "bls.ces.total_nonfarm.payroll_employment.change.sa.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-09-11", "start": "2026-09-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "bls.ces.nonfarm_payrolls.change", "releasePolicy": "first_print", "sourceSeriesId": "bls.ces.nonfarm_payrolls.change", "sourceUrl": "https://www.bls.gov/news.release/empsit.nr0.htm", "table": "Official agency release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-54376e2b403296fbe00a7087626388a7b47b6967974cb1856a1d50f1ce4cdda2.json"
- targetContentHash: "54376e2b403296fbe00a7087626388a7b47b6967974cb1856a1d50f1ce4cdda2"
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
7d6736566cef4d9f6caeaada19ecedd35dc932206830946c8b3dc02bfe90fab0

# Draft forecast response
{"slug":"nonfarm-payrolls-august-2026","country":"US","type":"data","title":"US Nonfarm Payrolls, August 2026","question":"What will the U.S. Bureau of Labor Statistics report as the first-print seasonally adjusted month-over-month change in total nonfarm payroll employment for August 2026, in thousands?","unit":"thousands","pointEstimate":35,"ciLow":-92,"ciHigh":162,"confidence":0.8,"resolutionDate":"2026-09-04","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.bls.gov/news.release/empsit.nr0.htm","resolutionRule":"Resolve to the first official BLS Employment Situation print for August 2026, Table B-1 total nonfarm seasonally adjusted change from July 2026 to August 2026, in thousands. Use the initially published preliminary value and do not apply later revisions, benchmark updates, same-day corrections, or subsequent monthly releases unless BLS replaces the first release before publication at the same official URL.","dataPointId":"bls.ces.total_nonfarm.payroll_employment.change.sa.2026-08.first_print","historicalContext":[{"label":"July 2026 first print","value":-23},{"label":"June 2026 latest revised","value":20},{"label":"May 2026 latest revised","value":63},{"label":"May 2026 first print","value":172},{"label":"April 2026 revised in May release","value":179}],"drivers":["July first print was negative at -23k, pointing to weak near-term momentum","BLS reported only 34k average monthly payroll gains over the prior 12 months","Private payrolls were still positive in July at +30k while public education was the main drag","Recent large downward revisions argue for a lower center than the 2024-2026 current-vintage mean","Low layoff/high health-care hiring pattern keeps the modal forecast above zero"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1","https://www.bls.gov/news.release/empsit.nr0.htm","https://www.bls.gov/news.release/empsit.t17.htm","https://download.bls.gov/pub/time.series/ce/ce.data.00a.TotalNonfarm.Employment","https://download.bls.gov/pub/time.series/ce/ce.series","https://www.bls.gov/news.release/archives/empsit_06052026.htm"],"runAt":"2026-08-11T00:00:00Z","reasoning":[{"kind":"heading","text":"August 2026 BLS total nonfarm payrolls first print"},{"kind":"text","text":"Resolver: use BLS CES total nonfarm, all employees, seasonally adjusted, first-print month-over-month change for August 2026, in thousands, from Employment Situation Table B-1. The ledger window ending 2026-09-11 conflicts with the official BLS Employment Situation schedule, which states August 2026 is released on 2026-09-04 at 08:30 ET; I keep the same slug and dataPointId but use the official scheduled release day as the resolution date."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS schedule for Employment Situation releases.","result":"Fetched official schedule: reference month August 2026 has release date Sep. 04, 2026 and release time 08:30 AM; July 2026 was Aug. 07, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Opened current BLS Employment Situation Summary for July 2026.","result":"Fetched July 2026 first-print total nonfarm payroll employment change of -23,000, unemployment rate 4.1 percent, prior-12-month average payroll gain 34,000, May revised to +63,000, June revised to +20,000, and combined May-June revision of -103,000."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Table B-1 for the July 2026 Employment Situation.","result":"Fetched Table B-1 total nonfarm seasonally adjusted levels: May 2026 158,861, June 2026 158,881, July 2026 158,858, with June-to-July change -23; total private changed +30 and local government education declined -50 in the release narrative."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS CES time-series flat file and series metadata for CES0000000001.","result":"Fetched series CES0000000001 defined as all employees, thousands, total nonfarm, seasonally adjusted, ending 2026 M07; recent levels include 2026 M03 158,650, M04 158,798, M05 158,861, M06 158,881, M07 158,858, implying changes +214, +148, +63, +20, -23 from current-vintage levels."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS archived May 2026 Employment Situation release.","result":"Fetched May 2026 first print: total nonfarm payroll employment increased by 172,000; the same release revised March to +214,000 and April to +179,000, and showed May seasonally adjusted total nonfarm level 159,001 in Table B-1."},{"kind":"text","text":"Base rate/reference class: using current-vintage CES0000000001 changes from January 2024 through July 2026 gives a mean near +61k, but the more relevant recent state is much weaker: the latest three revised changes are +63k, +20k, and -23k, averaging +20k, while the BLS release itself reports a +34k prior-12-month average."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent three-month average of +20k, cross-checked against the BLS stated prior-12-month average of +34k and the 2024-2026 current-vintage reference class mean near +61k. I adjust +15k from the +20k recent pace for expected partial rebound from July's local-government-education and retail drag, but cap the point at +35k because May-June revisions were -103k and private July hiring was only +30k. For dispersion, I used 30 fetched current-vintage monthly changes from 2024 M02 through 2026 M07: sigma = 99 thousand; 1.28*sigma = 127 thousand, so 35 +/- 127 gives an 80% interval of -92 to +162 thousand."},{"kind":"text","text":"Variant check: every payroll anchor above is seasonally adjusted CES total nonfarm all employees, thousands, matching CES0000000001 and Table B-1; the target is the first-print change, so current-vintage levels are used only for reference-class dispersion, not as the resolving vintage."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in state/local education seasonal adjustment, continued health-care hiring, and stronger construction/manufacturing that would land above the interval if the first print exceeds +162k. Downside risk is another broad hiring stall, additional retail/government losses, or a low survey response first print; that would land below the interval if payrolls fall by more than 92k."},{"kind":"forecast","point":35,"ciLow":-92,"ciHigh":162}]}
