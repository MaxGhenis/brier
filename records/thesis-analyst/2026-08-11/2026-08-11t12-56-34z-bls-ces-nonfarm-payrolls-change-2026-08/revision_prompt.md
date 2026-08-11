# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.ces.nonfarm_payrolls.change
- period: 2026-08
- conditionalOn: null

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
  "unit": "percent|count|thousands|millions|usd|usd_millions|usd_billions|gbp_billions|ratio|percent_growth",
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

Emit the final JSON object only. (agent thesis.analyst v2.5.7, prompt a954cfd8c691, tools 024388e49298, promptMode fast)


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
{"slug":"nonfarm-payrolls-august-2026","country":"US","type":"data","title":"US Nonfarm Payrolls, August 2026","question":"What will the U.S. Bureau of Labor Statistics report as the first-print seasonally adjusted month-over-month change in total nonfarm payroll employment for August 2026, in thousands?","unit":"thousands","pointEstimate":35,"ciLow":-92,"ciHigh":162,"confidence":0.8,"resolutionDate":"2026-09-04","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.bls.gov/news.release/empsit.nr0.htm","resolutionRule":"Resolve to the first official BLS Employment Situation print for August 2026, Table B-1 total nonfarm seasonally adjusted change from July 2026 to August 2026, in thousands. Use the initially published preliminary value and do not apply later revisions, benchmark updates, same-day corrections, or subsequent monthly releases unless BLS replaces the first release before publication at the same official URL.","dataPointId":"bls.ces.total_nonfarm.payroll_employment.change.sa.2026-08.first_print","historicalContext":[{"label":"July 2026 first print","value":-23},{"label":"June 2026 latest revised","value":20},{"label":"May 2026 latest revised","value":63},{"label":"May 2026 first print","value":172},{"label":"April 2026 revised in May release","value":179}],"drivers":["July first print was negative at -23k, pointing to weak near-term momentum","BLS reported only 34k average monthly payroll gains over the prior 12 months","Private payrolls were still positive in July at +30k while public education was the main drag","Recent large downward revisions argue for a lower center than the 2024-2026 current-vintage mean","Low layoff/high health-care hiring pattern keeps the modal forecast above zero"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1","https://www.bls.gov/news.release/empsit.nr0.htm","https://www.bls.gov/news.release/empsit.t17.htm","https://download.bls.gov/pub/time.series/ce/ce.data.00a.TotalNonfarm.Employment","https://download.bls.gov/pub/time.series/ce/ce.series","https://www.bls.gov/news.release/archives/empsit_06052026.htm"],"runAt":"2026-08-11T00:00:00Z","reasoning":[{"kind":"heading","text":"August 2026 BLS total nonfarm payrolls first print"},{"kind":"text","text":"Resolver: use BLS CES total nonfarm, all employees, seasonally adjusted, first-print month-over-month change for August 2026, in thousands, from Employment Situation Table B-1. The ledger window ending 2026-09-11 conflicts with the official BLS Employment Situation schedule, which states August 2026 is released on 2026-09-04 at 08:30 ET; I keep the same slug and dataPointId but use the official scheduled release day as the resolution date."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS schedule for Employment Situation releases.","result":"Fetched official schedule: reference month August 2026 has release date Sep. 04, 2026 and release time 08:30 AM; July 2026 was Aug. 07, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Opened current BLS Employment Situation Summary for July 2026.","result":"Fetched July 2026 first-print total nonfarm payroll employment change of -23,000, unemployment rate 4.1 percent, prior-12-month average payroll gain 34,000, May revised to +63,000, June revised to +20,000, and combined May-June revision of -103,000."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Table B-1 for the July 2026 Employment Situation.","result":"Fetched Table B-1 total nonfarm seasonally adjusted levels: May 2026 158,861, June 2026 158,881, July 2026 158,858, with June-to-July change -23; total private changed +30 and local government education declined -50 in the release narrative."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS CES time-series flat file and series metadata for CES0000000001.","result":"Fetched series CES0000000001 defined as all employees, thousands, total nonfarm, seasonally adjusted, ending 2026 M07; recent levels include 2026 M03 158,650, M04 158,798, M05 158,861, M06 158,881, M07 158,858, implying changes +214, +148, +63, +20, -23 from current-vintage levels."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS archived May 2026 Employment Situation release.","result":"Fetched May 2026 first print: total nonfarm payroll employment increased by 172,000; the same release revised March to +214,000 and April to +179,000, and showed May seasonally adjusted total nonfarm level 159,001 in Table B-1."},{"kind":"text","text":"Base rate/reference class: using current-vintage CES0000000001 changes from January 2024 through July 2026 gives a mean near +61k, but the more relevant recent state is much weaker: the latest three revised changes are +63k, +20k, and -23k, averaging +20k, while the BLS release itself reports a +34k prior-12-month average."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent three-month average of +20k, cross-checked against the BLS stated prior-12-month average of +34k and the 2024-2026 current-vintage reference class mean near +61k. I adjust +15k from the +20k recent pace for expected partial rebound from July's local-government-education and retail drag, but cap the point at +35k because May-June revisions were -103k and private July hiring was only +30k. For dispersion, I used 30 fetched current-vintage monthly changes from 2024 M02 through 2026 M07: sigma = 99 thousand; 1.28*sigma = 127 thousand, so 35 +/- 127 gives an 80% interval of -92 to +162 thousand."},{"kind":"text","text":"Variant check: every payroll anchor above is seasonally adjusted CES total nonfarm all employees, thousands, matching CES0000000001 and Table B-1; the target is the first-print change, so current-vintage levels are used only for reference-class dispersion, not as the resolving vintage."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in state/local education seasonal adjustment, continued health-care hiring, and stronger construction/manufacturing that would land above the interval if the first print exceeds +162k. Downside risk is another broad hiring stall, additional retail/government losses, or a low survey response first print; that would land below the interval if payrolls fall by more than 92k."},{"kind":"forecast","point":35,"ciLow":-92,"ciHigh":162}]}

# Reviewer critique
{"summary":"Draft is publishable: resolver, first-print handling, priors, evidence updates, uncertainty method, tails, and JSON fields are coherent with the target.","requiredFixes":[],"optionalSuggestions":["Consider noting that the 80% interval uses current-vintage monthly-change volatility as a proxy rather than a first-print-only volatility sample."]}

Emit the final JSON object only.
