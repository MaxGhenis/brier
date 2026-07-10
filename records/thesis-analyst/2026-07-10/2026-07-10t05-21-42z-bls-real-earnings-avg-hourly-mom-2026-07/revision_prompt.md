# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.real_earnings.avg_hourly_mom
- period: 2026-07
- conditional_on: null

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

# Source hints
- Use the official agency release calendar, not inferred cadence.
- FRED may be used as a history mirror, but resolution cites the agency.
- For FOMC targets, resolve to the target range upper bound after the announcement.
- For DOL claims, name the week-ending date and cite the release date.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class.
- Anchor on the outside-view base rate before current-release adjustments.
- Separate level, momentum, one-off, and policy-mechanism effects before combining them.
- Include one public reasoning step beginning "Prior/update/interval:" that names the model or persistence prior, historical sample, adjustment components, interval method, and final implied bounds.
- For strict first-print or original-vintage targets, keep the ledger resolver in substance and do not add same-day correction or release-day grace exceptions unless the target rule includes them.
- Size the 80% interval from realized dispersion and SHOW the arithmetic in the Prior/update/interval step: compute sigma from the fetched history (successive changes for level/rate series; the values themselves for change/flow series), state it literally as "sigma = X", and derive the half-width as roughly 1.28*sigma. If you widen or narrow beyond about 0.75x-1.75x of that half-width, state the regime or mechanism reason in the same step. Never default to a round hedged band.
- When a release has variants (gross vs smoothed/synthetic, SA vs NSA, flash vs final), the resolution rule must name the variant and every anchor and historical value must come from that same variant; say so once in a text step.
- resolutionSourceUrl must be the most specific stable page for the exact series (release page, table, or databrowser query with the series code), never a portal or theme landing page; state the series code or table id in a text step when one exists.
- Name concrete upside, downside, and outside-the-interval scenarios, using the literal phrases "upside risk", "downside risk", and "outside the interval" (or "would land above/below the interval") so the falsification step is machine-checkable.

# Required JSON shape
{
  "slug": "kebab-case-unique-vs-catalog",
  "country": "US|UK|CA|AU|EA|JP",
  "type": "data",
  "title": "Short display title",
  "question": "Exact agency series, period, adjustment, first print",
  "unit": "percent|count|thousands|millions|usd|usd_billions|gbp_billions|ratio|percent_growth",
  "pointEstimate": 0,
  "ciLow": 0,
  "ciHigh": 0,
  "confidence": 0.8,
  "resolutionDate": "YYYY-MM-DD",
  "resolutionSource": "Official agency release",
  "resolutionSourceUrl": "https://official-source.example",
  "resolutionRule": "First-print rule with rounding and revision policy",
  "dataPointId": "agency.dataset.concept.period.first_print",
  "historicalContext": [
    {
      "label": "latest",
      "value": 0
    }
  ],
  "drivers": [
    "short driver phrases"
  ],
  "sourceContext": [
    "https://urls-actually-used"
  ],
  "runAt": "date -u +%Y-%m-%dT%H:%M:%SZ",
  "reasoning": [
    {
      "kind": "heading",
      "text": "Forecast title"
    },
    {
      "kind": "text",
      "text": "Framing and exact resolver"
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "source lookup description",
      "result": "fetched numbers"
    },
    {
      "kind": "math",
      "text": "point and 80% interval calculation"
    },
    {
      "kind": "forecast",
      "point": 0,
      "ciLow": 0,
      "ciHigh": 0
    }
  ]
}

# Validation rules
- Use confidence 0.8 exactly.
- ciLow < pointEstimate < ciHigh, except discrete policy-rate targets may put the modal point at an interval edge if needed.
- historicalContext must contain at least 3 numeric fetched points.
- sourceContext must contain at least 2 source URLs actually used.
- sourceContext, reasoning, drivers, and tool calls must not cite or use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or non-public local files.
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step (literally say "base rate" or "reference class"), one math step, one counter-consideration that states what would land outside the 80% interval (literally use "upside risk", "downside risk", or "outside the interval"), one step beginning Prior/update/interval:, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value — an actual statistic from the source, not just field names or identifiers. Definitional lookups (data dictionaries, field definitions, methodology pages) belong in text steps, as do other qualitative source notes. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.2.0, prompt 7ef119647b35, tools e15bf40583f8, promptMode fast)


# Pre-submit review loop

You already drafted the response below. A reviewer then checked the draft against the Thesis rubric. Produce the final JSON forecast now.

Rules for the final submission:
- Return exactly one JSON object and no Markdown.
- Use only pre-resolution public evidence available to the draft.
- Accept reviewer fixes only when they improve resolver clarity, source grounding, base-rate discipline, uncertainty calibration, or internal coherence.
- Add a public reasoning text step beginning with "Review disposition:" that states which critique items were accepted or rejected. Keep this concise; do not reveal hidden chain-of-thought.
- Put the Review disposition text step before the final forecast step.
- The final reasoning step must be the forecast step, and its numbers must exactly match pointEstimate, ciLow, and ciHigh.

# Draft forecast response
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real average hourly earnings MoM, July 2026","question":"What will BLS first report for July 2026 over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, in Real Earnings Table A-1?","unit":"percent","pointEstimate":-0.1,"ciLow":-0.7,"ciHigh":0.5,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"May 2025 real AHE MoM, Table A-1","value":0.4},{"label":"Mar 2026 real AHE MoM, Table A-1","value":-0.6},{"label":"Apr 2026 real AHE MoM, Table A-1","value":-0.5},{"label":"May 2026 real AHE MoM, Table A-1","value":-0.1},{"label":"May 2026 CPI-U SA MoM, Table A-1","value":0.5},{"label":"June 2026 nominal AHE MoM implied from BLS Table B-3","value":0.35}],"drivers":["Recent real hourly earnings prints are negative because CPI gains have exceeded nominal wage gains","June nominal average hourly earnings still rose about 0.35 percent, close to the recent 0.2-0.3 percent monthly wage pace","May CPI-U seasonally adjusted rose 0.5 percent and energy prices remained the main upside risk to CPI","July real earnings mechanically depend on July nominal hourly earnings minus July CPI-U inflation"],"sourceContext":["https://www.bls.gov/schedule/news_release/realer.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/empsit.t19.htm","https://www.bls.gov/news.release/cpi.t01.htm"],"runAt":"2026-07-10T05:22:15Z","reasoning":[{"kind":"heading","text":"US real average hourly earnings MoM, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the BLS Real Earnings Table A-1 series for real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, over-the-month percent change. The table says CPI-U is used to deflate the earnings series, so all anchors here use the same SA all-employees private payroll earnings variant and CPI-U deflator."},{"kind":"tool","tool":"official.lookup","call":"BLS Real Earnings release calendar lookup for July 2026 reference month","result":"BLS schedule lists Real Earnings July 2026 with release date Aug. 12, 2026 and release time 08:30 AM; the same schedule shows June 2026 on Jul. 14, 2026 and May 2026 on Jun. 10, 2026."},{"kind":"tool","tool":"official.lookup","call":"BLS Real Earnings Table A-1 current release lookup","result":"BLS Table A-1 reports real average hourly earnings over-the-month percent changes of 0.4 for May 2025, -0.6 for Mar. 2026, -0.5 for Apr. 2026, and -0.1 for May 2026; the same table reports CPI-U over-the-month changes of 0.1, 0.9, 0.6, and 0.5 for those columns."},{"kind":"tool","tool":"official.lookup","call":"BLS Employment Situation Table B-3 lookup for latest nominal average hourly earnings","result":"BLS Table B-3 reports total private average hourly earnings of $37.41 in Apr. 2026, $37.51 in May 2026, and $37.64 in June 2026, implying May nominal AHE growth of about 0.27% and June growth of about 0.35%."},{"kind":"tool","tool":"official.lookup","call":"BLS CPI Table 1 lookup for latest CPI-U inflation components","result":"BLS CPI Table 1 reports May 2026 all-items CPI-U unadjusted index 335.123, 12-month change 4.2%, seasonally adjusted all-items monthly changes of 0.9% Feb-Mar, 0.6% Mar-Apr, and 0.5% Apr-May, with energy up 3.9% Apr-May."},{"kind":"text","text":"Reference class and base rate: the directly fetched real-AHE over-the-month reference class from the current Table A-1 is 0.4, -0.6, -0.5, and -0.1 percent, averaging -0.2 percent; the recent base rate is therefore negative real wage growth when headline CPI is running above the nominal hourly earnings pace."},{"kind":"text","text":"Current-release adjustment: nominal wage momentum is still near 0.3 percent monthly, using June Table B-3's $37.64 versus $37.51 as a live wage anchor. CPI momentum is less favorable, with the latest all-items CPI-U monthly gains 0.9, 0.6, and 0.5 percent, but some May energy pressure could partly mean-revert by July. Combining a July nominal AHE assumption near +0.30 percent with a CPI-U assumption near +0.35 to +0.40 percent points to a small negative real hourly earnings print."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent BLS Table A-1 real-AHE MoM base rate using fetched values [0.4, -0.6, -0.5, -0.1], mean = -0.20. Adjustment components are +0.10 for steady nominal wage growth near 0.3% and -0.05 for CPI still elevated but not as extreme as May, giving point near -0.15, rounded to -0.1. Interval method uses realized dispersion of the fetched change values themselves because this is a change series: sigma = 0.45, so 80% half-width is roughly 1.28*sigma = 1.28*0.45 = 0.58; around -0.1 this gives about [-0.68, 0.48], rounded to [-0.7, 0.5]."},{"kind":"text","text":"Counter-consideration: upside risk is a July CPI relief print, especially an energy reversal, combined with another 0.3-0.4 percent nominal wage month, which would land above the interval. Downside risk is another gasoline or broad services CPI spike with only 0.2 percent nominal wage growth, which would land below the interval. Outside the interval would require roughly real AHE above +0.5 percent or below -0.7 percent on the first print."},{"kind":"forecast","point":-0.1,"ciLow":-0.7,"ciHigh":0.5}]}

# Reviewer critique
{
  "summary": "Draft is publication-ready with no blocking issues; resolver, prior/update/interval, tails, and JSON fields are coherent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider noting that the interval volatility estimate is based on only four recent Table A-1 observations, so the 80% interval is deliberately approximate.",
    "Consider adding the exact BLS schedule date in sourceContext or reasoning artifact if the publishing pipeline preserves source-level provenance."
  ]
}

Emit the final JSON object only.
