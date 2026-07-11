# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-07-18
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-18"
- country: "US"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-18.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-08-01", "start": "2026-07-28"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-11-303f08a03edb98ea7f4d37396fa9d9285464d3539e074f49a39462ce133153f7.json"
- targetContentHash: "303f08a03edb98ea7f4d37396fa9d9285464d3539e074f49a39462ce133153f7"
- registrationCommit: "acccfc0a6925ff3385b5c0e29b544fb6310a3f73"
- registeredAtUtc: "2026-07-11T00:23:25Z"

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
{"slug":"continued-claims-week-2026-07-18","country":"US","type":"data","title":"US Continued Claims, July 18 Week","question":"What will the first-print U.S. seasonally adjusted continued claims level be for the week ending July 18, 2026?","unit":"millions","pointEstimate":1.828,"ciLow":1.806,"ciHigh":1.85,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print seasonally adjusted insured unemployment level for the week ending July 18, 2026, in the U.S. Department of Labor release scheduled for July 30, 2026, converted from persons to millions and rounded to 0.001 million. Ignore all subsequent revisions.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-18.first_print","historicalContext":[{"label":"week ending 2026-06-27 first print","value":1.814},{"label":"week ending 2026-06-20 first print","value":1.814},{"label":"week ending 2026-06-13 first print","value":1.821},{"label":"week ending 2026-06-06 first print","value":1.81},{"label":"week ending 2026-05-30 first print","value":1.795}],"drivers":["Recent continued-claims level near 1.81 million","Mild positive five-week momentum","Initial claims steady near 215,000","Holiday-period seasonal-adjustment uncertainty"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://www.dol.gov/sites/dolgov/files/OPA/newsreleases/ui-claims/20261132.pdf","https://www.dol.gov/sites/dolgov/files/OPA/newsreleases/ui-claims/20261092.pdf","https://alfred.stlouisfed.org/series?seid=CCSA","https://www.dol.gov/index.php/newsroom/releases/opa/opa20200701"],"runAt":"2026-07-11T00:26:09Z","reasoning":[{"kind":"heading","text":"Continued claims for the week ending July 18, 2026"},{"kind":"text","text":"The target is ETA series CCSA: advance first-print U.S. insured unemployment, seasonally adjusted, for the week ending July 18—not the NSA level, four-week average, or a later revised vintage. Resolution uses the July 30 release and reports millions."},{"kind":"tool","tool":"official.lookup","call":"Checked the Department of Labor's official release-timing announcement and the target's calendar window.","result":"DOL states that Weekly Claims is released each Thursday at 8:30 a.m. ET; Thursday following the established two-week reporting lag for the week ending 2026-07-18 is 2026-07-30, within the registered 2026-07-28 to 2026-08-01 window."},{"kind":"tool","tool":"official.lookup","call":"Read DOL Weekly Claims releases for the recent seasonally adjusted insured-unemployment reference class.","result":"Fetched first-print SA insured unemployment of 1,795,000 for 2026-05-30, 1,810,000 for 2026-06-06, and 1,821,000 for 2026-06-13; DOL also reported the insured unemployment rate at 1.2%."},{"kind":"tool","tool":"official.lookup","call":"Checked the July 2 DOL release and ALFRED CCSA advance-vintage history for the latest weeks.","result":"Fetched first-print SA insured unemployment of 1,814,000 for 2026-06-20 and 1,814,000 for 2026-06-27; recent SA initial claims were 215,000 for both 2026-06-20 and 2026-06-27."},{"kind":"text","text":"Base rate/reference class: persistence dominates this weekly level series. The five first prints from May 30 through June 27 averaged 1.811 million, while their net change was only +0.019 million; steady initial claims near 0.215 million argue against an abrupt break."},{"kind":"math","text":"Prior/update/interval: persistence prior = 1.814 million, using the five first-print observations 1.795, 1.810, 1.821, 1.814, 1.814. Successive changes are +0.015, +0.011, -0.007, and 0.000 million; their mean is +0.00475 and sample sigma = 0.0101 million. Three-week momentum adds 3×0.00475 = 0.01425, giving 1.82825, rounded to 1.828. For a three-step horizon, sigma scales to 0.0101×sqrt(3) = 0.0175; the 80% half-width is roughly 1.28×sigma = 0.0224, yielding final implied bounds 1.806 to 1.850 million."},{"kind":"text","text":"Level and momentum point mildly upward, while stable initial claims provide no strong deterioration signal. Holiday-related seasonal adjustment is the main one-off risk; no discrete policy mechanism warrants an additional shift."},{"kind":"text","text":"Upside risk: a broad rise in benefit duration or delayed hiring could land above 1.850 million. Downside risk: faster claimant exits or unusually favorable seasonal adjustment could land below 1.806 million. Either outcome would be outside the interval."},{"kind":"forecast","point":1.828,"ciLow":1.806,"ciHigh":1.85}]}

# Reviewer critique
{"summary":"The draft is mostly publishable, but the source URL should be made resolver-stable and the interval method should better justify relying on only four recent weekly changes.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The resolver text is clear about the July 30, 2026 DOL first print, but resolutionSourceUrl points to mutable current data.pdf while the ledger source binding is the ALFRED CCSA advance-vintage CSV with DOL as the official release source.","actionRequested":"Use the ledger-bound ALFRED graph CSV or a stable archived DOL July 30 release URL in the resolver/source fields, and keep the first-print DOL release language."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is derived from only four recent weekly changes, a very short calm sample for a three-week-ahead continued-claims forecast during a holiday adjustment period.","actionRequested":"Either widen the interval or explicitly justify why the last four changes are representative versus a longer recent realized-volatility sample."}],"optionalSuggestions":["Mention that as of run time the latest available continued-claims first print is for week ending 2026-06-27, so July 18 is a three-step horizon.","Clarify the initial-claims evidence as 'near 215k' rather than saying both recent weeks were exactly 215k if using revised July 9 release data."]}

Emit the final JSON object only.
