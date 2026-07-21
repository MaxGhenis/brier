# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: us.dol.initial_claims.sa
- period: week_2026-07-25
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-25"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-25"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-08-01", "start": "2026-07-28"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-20-14230433262478cb1134d42fc94b9c1eab391028cc750beb6151ad05ce20889a.json"
- targetContentHash: "14230433262478cb1134d42fc94b9c1eab391028cc750beb6151ad05ce20889a"
- registrationCommit: "134572ec0e53debeec96716bf346510a889628ee"
- registeredAtUtc: "2026-07-20T18:27:38Z"

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
{"slug":"initial-claims-week-2026-07-25","country":"US","type":"data","title":"US initial claims, week ending July 25","question":"What will the advance first print of US seasonally adjusted initial unemployment insurance claims be for the week ending July 25, 2026?","unit":"thousands","pointEstimate":212,"ciLow":202,"ciHigh":222,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance figure for seasonally adjusted initial claims for the week ending July 25, 2026, published by the U.S. Department of Labor on July 30, 2026, expressed in thousands and rounded to the nearest thousand. Use that first official print only; ignore subsequent revisions.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-25","historicalContext":[{"label":"week ending 2026-07-11","value":208},{"label":"week ending 2026-07-04","value":216},{"label":"week ending 2026-06-27","value":217},{"label":"week ending 2026-06-20","value":216},{"label":"week ending 2026-06-13","value":227}],"drivers":["Recent claims level near 208 thousand","Partial mean reversion toward the five-week average","Low recent week-to-week dispersion","Holiday-related seasonal-adjustment uncertainty"],"sourceContext":["https://alfred.stlouisfed.org/series?seid=ICSA","https://oui.doleta.gov/unemploy/archive.asp","https://fred.stlouisfed.org/releases/calendar?m=&ob=n&od=asc&rid=180&ve=2026-12-31&vs=2026-01-01&y="],"runAt":"2026-07-21T01:02:00Z","reasoning":[{"kind":"heading","text":"Advance initial claims forecast for the week ending July 25, 2026"},{"kind":"text","text":"The target is the advance first print of national seasonally adjusted initial claims, series ICSA, for the week ending Saturday, July 25, 2026. The DOL publication schedule says the report is issued Thursday at 8:30 a.m. Eastern and lists only November 25 as a 2026 exception; the release calendar confirms July 30. Resolution therefore uses the July 30 DOL report without later revisions."},{"kind":"tool","tool":"official.lookup","call":"Inspect the DOL Employment and Training Administration UI claims archive and publication schedule.","result":"The schedule states weekly publication on Thursday at 8:30 a.m. Eastern and identifies 1 exceptional 2026 release date, November 25; therefore the July 25 reference week is scheduled for July 30, 2026."},{"kind":"tool","tool":"alfred.lookup","call":"Fetch recent ICSA observations from the public ALFRED history mirror.","result":"Seasonally adjusted ICSA values, in thousands, were 227 on 2026-06-13, 216 on 2026-06-20, 217 on 2026-06-27, 216 on 2026-07-04, and 208 on 2026-07-11."},{"kind":"tool","tool":"calendar.lookup","call":"Check the published Unemployment Insurance Weekly Claims Report release calendar.","result":"The calendar lists releases on July 23 and July 30, 2026, both at 7:30 a.m. Central, equivalent to 8:30 a.m. Eastern."},{"kind":"text","text":"The five-week reference class has a 216.8-thousand mean and a 208-thousand latest observation. The base rate is short-horizon persistence with modest mean reversion: the level is low relative to that recent mean, while the sequence 227, 216, 217, 216, 208 does not show an accelerating rise."},{"kind":"text","text":"Level contributes a 208-thousand anchor; momentum is mildly negative; mean reversion contributes about +4 thousand; no verified policy mechanism warrants a large displacement. Holiday-related seasonal adjustment around early July is the main one-off uncertainty. All anchors refer to the same seasonally adjusted advance ICSA variant."},{"kind":"math","text":"Prior/update/interval: The model is persistence plus partial mean reversion, using the five fetched observations 227, 216, 217, 216, and 208. Successive changes are -11, +1, -1, and -8 thousand; their sample standard deviation is sigma = sqrt(96.75/3) = 5.7 thousand per week. The unseen July 18 release makes this effectively a two-step forecast, so the horizon-adjusted sigma is 5.7*sqrt(2) = 8.1 and the 80% half-width is roughly 1.28*sigma = 10.4 thousand. The 208 persistence prior plus a +4-thousand mean-reversion adjustment and approximately zero net momentum, one-off, and policy adjustments gives 212; rounding 212 ± 10.4 to whole thousands implies bounds of 202 and 222."},{"kind":"text","text":"Upside risk comes from a renewed burst of layoffs or unusually adverse seasonal adjustment and would land above the interval if the first print exceeds 222 thousand. Downside risk comes from continued unusually low filings or favorable seasonal adjustment and would land below the interval if the first print is under 202 thousand."},{"kind":"forecast","point":212,"ciLow":202,"ciHigh":222}]}

# Reviewer critique
{"summary":"The draft is publishable after tightening one evidence-coherence issue about revised historical observations versus advance first-print wording.","requiredFixes":[{"rubricItem":"coherence","severity":"warning","summary":"The reasoning says all anchors use the same seasonally adjusted advance ICSA variant, but several historical values appear to be revised/current ALFRED observations rather than the original advance first prints.","actionRequested":"Clarify that the recent-history inputs are latest available/revised seasonally adjusted ICSA levels used as forecasting evidence, while the target itself resolves only to the July 30, 2026 advance first print for week ending July 25."}],"optionalSuggestions":["Mention that the July 18, 2026 release is not yet observed at run time, which is why the forecast is treated as a two-step horizon.","If retaining the DOL PDF URL, ensure the publication record also preserves a stable archive/calendar reference for the July 30, 2026 first print."]}

Emit the final JSON object only.
