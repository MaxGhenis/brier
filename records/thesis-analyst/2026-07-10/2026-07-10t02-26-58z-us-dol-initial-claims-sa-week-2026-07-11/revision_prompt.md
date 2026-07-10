# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: us.dol.initial_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-11"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-11"
- sourceBinding: {"adapter": "alfred-fred", "expectedReleaseWindow": {"end": "2026-07-18", "start": "2026-07-14"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US initial jobless claims, week ending Jul 11","question":"What will the U.S. Department of Labor Employment and Training Administration report as the advance seasonally adjusted initial claims for unemployment insurance in the week ending July 11, 2026, in the first print?","unit":"thousands","pointEstimate":216,"ciLow":203,"ciHigh":229,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Employment and Training Administration UI Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260716","resolutionRule":"Resolve to the first DOL ETA UI Weekly Claims Report advance figure for seasonally adjusted Initial Claims (SA) for the week ending July 11, 2026. Record the agency-published count in thousands, rounded as shown by DOL to the nearest thousand. Use the first print released on July 16, 2026 and ignore later revisions or subsequent releases.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"latest_week_2026-07-04_sa_initial_claims","value":215},{"label":"prior_week_2026-06-27_sa_initial_claims","value":217},{"label":"week_2026-06-20_sa_initial_claims","value":216},{"label":"latest_4wk_average","value":218.75},{"label":"prior_year_comparable","value":228}],"drivers":["latest SA initial claims at 215 thousand","four-week average at 218.75 thousand","late-June claims spike faded from 230 to 215 thousand","insured unemployment steady at 1.2 percent","holiday-week and school-season adjustment noise"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260709","https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp"],"runAt":"2026-07-10T02:27:28Z","reasoning":[{"kind":"heading","text":"US initial claims first-print forecast for week ending July 11, 2026"},{"kind":"text","text":"Target is the DOL ETA advance seasonally adjusted Initial Claims (SA) figure for week ending July 11, 2026, reported in thousands. This uses the SA variant throughout; NSA state detail is used only as directional context, not as the target series."},{"kind":"tool","tool":"official.lookup","call":"Checked the DOL weekly claims archive publication schedule and latest-release link.","result":"DOL says the UI Weekly Claims News Release is published each week on Thursday at 8:30 AM EST, with the listed 2026 exception Wednesday November 25, 2026 at 8:30 AM EST. The page was updated July 9, 2026 and links the latest report showing 215,000 SA initial claims for week ending July 4, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the July 9, 2026 DOL UI Weekly Claims Report headline and summary table.","result":"For week ending July 4, 2026, advance SA initial claims were 215,000, down 2,000 from the revised prior week of 217,000; the four-week moving average was 218,750, down 3,750 from the revised prior average of 222,500."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL regular state programs table for recent SA national claims and insured unemployment.","result":"DOL table values in thousands: Initial Claims (SA) were 215 for July 4, 217 for June 27, and 216 for June 20; prior-year comparable was 228. Insured unemployment (SA) was 1,814,000 for June 27 versus 1,806,000 for June 20, and the insured unemployment rate was 1.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL one-year SA history panel for recent weekly initial claims values.","result":"Recent 2026 SA initial claims values in thousands included May 16 210, May 23 212, May 30 225, June 6 230, June 13 227, June 20 216, June 27 217, and July 4 215; the latest four-week average from those rows is 218.75."},{"kind":"text","text":"Reference class/base rate: for a stable weekly level series, the outside-view anchor is persistence plus the latest four-week mean. The last eight official SA prints average 219.0 thousand, while the latest print is 215 thousand, so the base rate is a mid-to-high 210s first print rather than a break into the 230s."},{"kind":"math","text":"Prior/update/interval: persistence prior = 215 from the July 4 first print; historical sample = 2026 DOL SA initial-claims weekly values from January 3 through July 4; adjustment components = +2.0 toward the 218.75 four-week average, -1.5 for the prior-year July post-holiday weekly drop pattern, and +0.5 for steady 1.2 percent insured unemployment, giving point = 216. For realized dispersion, successive 2026 weekly changes are -6, 9, 1, 19, 0, -22, 3, 3, -1, -8, 6, -8, 15, -10, 7, -25, 9, 13, -2, 2, 13, 5, -3, -11, 1, -2, so sigma = 10.4 thousand and 1.28*sigma = 13.3 thousand; 216 +/- 13 gives an 80 percent interval of 203 to 229 thousand."},{"kind":"text","text":"Level and momentum are mixed: the latest level is low at 215, but the four-week average remains 218.75 because the series touched 230 in early June. No official-source evidence points to a new layoff regime before the July 11 week, so I keep the point close to latest persistence."},{"kind":"text","text":"Upside risk: another education- or transportation-related filing bulge, or delayed holiday filings, would land above the interval if SA initial claims print above 229 thousand. Downside risk: a repeat of the late-April low-claims adjustment pattern would land below the interval if claims fall under 203 thousand. Outside the interval is most likely from seasonal-adjustment noise around the July holiday weeks rather than a genuine one-week labor-market regime shift."},{"kind":"forecast","point":216,"ciLow":203,"ciHigh":229}]}

# Reviewer critique
{"summary":"Draft is broadly publishable, but the resolver/source wording should be tightened to avoid a fragile future newsroom URL and to reconcile the DOL first-print rule with the ledger ALFRED binding.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The draft names a specific future DOL release URL, https://www.dol.gov/newsroom/releases/eta/eta20260716, which may not be the stable canonical resolver link; the ledger sourceBinding instead names ALFRED/FRED ICSA advance vintage while the reasoning uses DOL as the official agency source.","actionRequested":"State the resolver as the first DOL ETA UI Weekly Claims Report advance SA Initial Claims figure for week ending July 11, 2026, released July 16, 2026, and either use a stable DOL claims archive/latest-report source or explicitly note that the catalog binding may mirror the first print via ALFRED ICSA with factor 0.001."}],"optionalSuggestions":["In the prior/update/interval step, name the exact historical sample size or date range consistently with the listed weekly-difference vector.","Consider saying explicitly that the 80% interval is symmetric around the point after rounding to whole thousands."]}

Emit the final JSON object only.
