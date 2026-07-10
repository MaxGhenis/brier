# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.real_earnings.avg_hourly_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-real-avg-hourly-earnings-mom-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.real_earnings.avg_hourly_mom.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-10"}, "field": "bls.real_earnings.avg_hourly_mom", "releasePolicy": "first_print", "sourceSeriesId": "bls.real_earnings.avg_hourly_mom", "sourceUrl": "https://www.bls.gov/news.release/realer.t01.htm", "table": "U.S. Bureau of Labor Statistics Real Earnings Table A-1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-8662209989befa5925d38419a847521e7a1076b91048aef177ca79c7544f4334.json"
- targetContentHash: "8662209989befa5925d38419a847521e7a1076b91048aef177ca79c7544f4334"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"
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
0ec95b17086d75db66581a7b7ef481403b8d57d71aae72e6b3bf0bf59c537098

# Draft forecast response
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real average hourly earnings MoM, July 2026","question":"What will BLS first report for July 2026 over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, in Real Earnings Table A-1?","unit":"percent","pointEstimate":-0.1,"ciLow":-0.7,"ciHigh":0.5,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"May 2025 real AHE MoM, Table A-1","value":0.4},{"label":"Mar 2026 real AHE MoM, Table A-1","value":-0.6},{"label":"Apr 2026 real AHE MoM, Table A-1","value":-0.5},{"label":"May 2026 real AHE MoM, Table A-1","value":-0.1},{"label":"May 2026 CPI-U SA MoM, Table A-1","value":0.5},{"label":"June 2026 nominal AHE MoM implied from BLS Table B-3","value":0.35}],"drivers":["Recent real hourly earnings prints are negative because CPI gains have exceeded nominal wage gains","June nominal average hourly earnings still rose about 0.35 percent, close to the recent 0.2-0.3 percent monthly wage pace","May CPI-U seasonally adjusted rose 0.5 percent and energy prices remained the main upside risk to CPI","July real earnings mechanically depend on July nominal hourly earnings minus July CPI-U inflation"],"sourceContext":["https://www.bls.gov/schedule/news_release/realer.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/empsit.t19.htm","https://www.bls.gov/news.release/cpi.t01.htm"],"runAt":"2026-07-10T05:22:15Z","reasoning":[{"kind":"heading","text":"US real average hourly earnings MoM, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the BLS Real Earnings Table A-1 series for real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, over-the-month percent change. The table says CPI-U is used to deflate the earnings series, so all anchors here use the same SA all-employees private payroll earnings variant and CPI-U deflator."},{"kind":"tool","tool":"official.lookup","call":"BLS Real Earnings release calendar lookup for July 2026 reference month","result":"BLS schedule lists Real Earnings July 2026 with release date Aug. 12, 2026 and release time 08:30 AM; the same schedule shows June 2026 on Jul. 14, 2026 and May 2026 on Jun. 10, 2026."},{"kind":"tool","tool":"official.lookup","call":"BLS Real Earnings Table A-1 current release lookup","result":"BLS Table A-1 reports real average hourly earnings over-the-month percent changes of 0.4 for May 2025, -0.6 for Mar. 2026, -0.5 for Apr. 2026, and -0.1 for May 2026; the same table reports CPI-U over-the-month changes of 0.1, 0.9, 0.6, and 0.5 for those columns."},{"kind":"tool","tool":"official.lookup","call":"BLS Employment Situation Table B-3 lookup for latest nominal average hourly earnings","result":"BLS Table B-3 reports total private average hourly earnings of $37.41 in Apr. 2026, $37.51 in May 2026, and $37.64 in June 2026, implying May nominal AHE growth of about 0.27% and June growth of about 0.35%."},{"kind":"tool","tool":"official.lookup","call":"BLS CPI Table 1 lookup for latest CPI-U inflation components","result":"BLS CPI Table 1 reports May 2026 all-items CPI-U unadjusted index 335.123, 12-month change 4.2%, seasonally adjusted all-items monthly changes of 0.9% Feb-Mar, 0.6% Mar-Apr, and 0.5% Apr-May, with energy up 3.9% Apr-May."},{"kind":"text","text":"Reference class and base rate: the directly fetched real-AHE over-the-month reference class from the current Table A-1 is 0.4, -0.6, -0.5, and -0.1 percent, averaging -0.2 percent; the recent base rate is therefore negative real wage growth when headline CPI is running above the nominal hourly earnings pace."},{"kind":"text","text":"Current-release adjustment: nominal wage momentum is still near 0.3 percent monthly, using June Table B-3's $37.64 versus $37.51 as a live wage anchor. CPI momentum is less favorable, with the latest all-items CPI-U monthly gains 0.9, 0.6, and 0.5 percent, but some May energy pressure could partly mean-revert by July. Combining a July nominal AHE assumption near +0.30 percent with a CPI-U assumption near +0.35 to +0.40 percent points to a small negative real hourly earnings print."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent BLS Table A-1 real-AHE MoM base rate using fetched values [0.4, -0.6, -0.5, -0.1], mean = -0.20. Adjustment components are +0.10 for steady nominal wage growth near 0.3% and -0.05 for CPI still elevated but not as extreme as May, giving point near -0.15, rounded to -0.1. Interval method uses realized dispersion of the fetched change values themselves because this is a change series: sigma = 0.45, so 80% half-width is roughly 1.28*sigma = 1.28*0.45 = 0.58; around -0.1 this gives about [-0.68, 0.48], rounded to [-0.7, 0.5]."},{"kind":"text","text":"Counter-consideration: upside risk is a July CPI relief print, especially an energy reversal, combined with another 0.3-0.4 percent nominal wage month, which would land above the interval. Downside risk is another gasoline or broad services CPI spike with only 0.2 percent nominal wage growth, which would land below the interval. Outside the interval would require roughly real AHE above +0.5 percent or below -0.7 percent on the first print."},{"kind":"forecast","point":-0.1,"ciLow":-0.7,"ciHigh":0.5}]}
