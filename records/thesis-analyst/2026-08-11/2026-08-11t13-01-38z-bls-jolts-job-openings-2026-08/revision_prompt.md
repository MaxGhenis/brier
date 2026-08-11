# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.job_openings
- period: 2026-08
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-openings-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.jolts.job_openings.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-10-05", "start": "2026-09-27"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-10-05", "start": "2026-09-27"}, "field": "bls.jolts.job_openings", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.job_openings", "sourceUrl": "https://www.bls.gov/news.release/jolts.nr0.htm", "table": "U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-66a38cce6c472dec90f4d80d7b32fa5be061746652b89c5733473d64ef4b6218.json"
- targetContentHash: "66a38cce6c472dec90f4d80d7b32fa5be061746652b89c5733473d64ef4b6218"
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
{"slug":"jolts-openings-august-2026","country":"US","type":"data","title":"US JOLTS Job Openings, August 2026","question":"What will the U.S. Bureau of Labor Statistics first report for seasonally adjusted total nonfarm job openings in the Job Openings and Labor Turnover Survey for August 2026, in millions?","unit":"millions","pointEstimate":7.1,"ciLow":6.45,"ciHigh":7.75,"confidence":0.8,"resolutionDate":"2026-09-29","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey, Table 1","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t01.htm","resolutionRule":"Resolve to the first official BLS Job Openings and Labor Turnover Survey release for August 2026, Table 1, seasonally adjusted Total job openings level. Use the level in thousands multiplied by 0.001 to report millions, rounded to three decimals if needed. Do not use later revisions or corrected subsequent releases unless BLS replaces the first-print page before ordinary revisions.","dataPointId":"bls.jolts.job_openings.august_2026.first_print","historicalContext":[{"label":"2026-06 SA total job openings","value":7.359},{"label":"2026-05 SA total job openings","value":7.537},{"label":"2026-04 SA total job openings","value":7.585},{"label":"2026-03 SA total job openings","value":6.887},{"label":"2026-02 SA total job openings","value":6.882}],"drivers":["June openings fell 178,000 to 7.359 million","July payroll employment was -23,000 with unemployment at 4.1 percent","Recent openings remain volatile around 7.0-7.6 million","Low-hire low-fire labor market argues for drift lower rather than collapse"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/news.release/jolts.nr0.htm","https://www.bls.gov/news.release/jolts.t01.htm","https://www.bls.gov/news.release/archives/jolts_03312026.htm","https://www.bls.gov/news.release/archives/jolts_05052026.htm","https://www.bls.gov/news.release/empsit.nr0.htm"],"runAt":"2026-08-11T13:02:49Z","reasoning":[{"kind":"heading","text":"US JOLTS job openings for August 2026"},{"kind":"text","text":"Resolver framing: this is BLS JOLTS Table 1 seasonally adjusted Total job openings, levels in thousands converted to millions. The ledger window ends 2026-10-05, but the official BLS JOLTS release schedule fetched this run lists August 2026 for September 29, 2026 at 10:00 AM, so I use 2026-09-29 as the verified release-calendar resolution date while keeping the registered slug and dataPointId."},{"kind":"tool","tool":"official.lookup","call":"BLS JOLTS release schedule lookup for reference month August 2026","result":"Fetched official schedule: July 2026 JOLTS release date Sep. 01, 2026 at 10:00 AM; August 2026 JOLTS release date Sep. 29, 2026 at 10:00 AM; September 2026 release date Nov. 03, 2026 at 10:00 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS current JOLTS summary and Table 1 for June 2026","result":"Fetched June 2026 release: total job openings 7.4 million in text; Table 1 Total levels were June 2025 7,204 thousand, March 2026 6,887 thousand, April 2026 7,585 thousand, May 2026 7,537 thousand, June 2026 7,359 thousand; June change from May was -178 thousand and the openings rate was 4.4 percent."},{"kind":"tool","tool":"official.lookup","call":"BLS archived JOLTS release for February 2026","result":"Fetched February 2026 archive: Total job openings were 7,240 thousand in January 2026 and 6,882 thousand in February 2026; hires were 5,347 thousand in January and 4,849 thousand in February."},{"kind":"tool","tool":"official.lookup","call":"BLS archived JOLTS release for March 2026","result":"Fetched March 2026 archive: Total job openings were 6,922 thousand in February 2026 and 6,866 thousand in March 2026 first print; Table A also showed March 2025 at 6,952 thousand."},{"kind":"tool","tool":"official.lookup","call":"BLS Employment Situation for July 2026 as labor-market context","result":"Fetched July 2026 Employment Situation: nonfarm payroll employment was -23,000; unemployment rate was 4.1 percent; May payrolls were revised to +63,000 and June to +20,000, a combined 103,000 lower than previously reported."},{"kind":"text","text":"Base rate/reference class: for a two-month-ahead forecast of a level series, the strongest outside-view prior is persistence around the latest official JOLTS level. The recent official reference class is January-June 2026 total job openings around 6.9-7.6 million, with a current value of 7.359 million and no evidence of a large layoff shock."},{"kind":"math","text":"Prior/update/interval: persistence prior starts at June 2026 current-vintage 7.359 million. Updates are -0.18 million for the June down move continuing, -0.12 million for weak July payrolls and downward revisions, +0.04 million because openings are noisy and layoffs remain contained, giving 7.359 - 0.18 - 0.12 + 0.04 = 7.099, rounded to 7.10 million. Historical sample uses successive changes in current/official 2026 levels: Jan 7.240, Feb 6.882, Mar 6.887, Apr 7.585, May 7.537, Jun 7.359 million, so changes are -0.358, +0.005, +0.698, -0.048, -0.178 and sigma = 0.40 million. The one-month 80% half-width is 1.28*sigma = 1.28*0.40 = 0.51 million; I widen to 0.65 million for the two-month horizon to August, giving 7.10 +/- 0.65 = [6.45, 7.75]."},{"kind":"text","text":"Upside risk: a rebound in professional services, retail, or transportation postings after June's drop would land above the interval if openings print above 7.75 million. Downside risk: the July payroll contraction and weak revisions could mark a sharper employer retrenchment, and an August openings fall below 6.45 million would land outside the interval on the low side."},{"kind":"forecast","point":7.1,"ciLow":6.45,"ciHigh":7.75}]}

# Reviewer critique
{"summary":"The draft is substantively well-formed, but publication should block until the resolver fields align with the registered ledger target contract or the ledger discrepancy is handled explicitly without changing the target fields.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft uses resolutionDate 2026-09-29 and resolutionSourceUrl jolts.t01.htm, while the registered target contract supplied for review binds the target to the ledger registration/sourceBinding with window end 2026-10-05 and sourceUrl https://www.bls.gov/news.release/jolts.nr0.htm.","actionRequested":"Set the published JSON resolver fields to the registered target contract values, or if treating the BLS calendar date as a ledger error, keep the target tied to the registered slug/dataPointId and state the discrepancy in reasoning without silently substituting incompatible resolver fields."},{"rubricItem":"coherence","severity":"warning","summary":"The reasoning says the ledger window ends 2026-10-05 but the JSON uses 2026-09-29, creating ambiguity about whether this is a release-calendar target or a resolve-by-bound registered target.","actionRequested":"Make the final forecast step and JSON fields use one target contract consistently, with any ledger/date discrepancy called out as a note rather than changing the target identity."}],"optionalSuggestions":["The prior/update/interval step is compact and names the persistence prior, sample, adjustments, sigma method, and bounds.","Tail scenarios are concrete enough; adding one sentence on why two-month widening from 0.51 to 0.65 is calibrated would strengthen the interval rationale."]}

Emit the final JSON object only.
