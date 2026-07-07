# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.quits_rate
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-quits-rate-june-2026"

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
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
{"slug":"jolts-quits-rate-june-2026","country":"US","type":"data","title":"US JOLTS quits rate, Jun 2026","question":"BLS Job Openings and Labor Turnover Survey Table 4 total nonfarm quits rate, seasonally adjusted, June 2026, first print","unit":"percent","pointEstimate":1.9,"ciLow":1.8,"ciHigh":2.0,"confidence":0.8,"resolutionDate":"2026-08-04","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t04.htm","resolutionRule":"Resolve to the first BLS-published seasonally adjusted total nonfarm quits rate for June 2026 in JOLTS Table 4, released on 2026-08-04 at 10:00 AM ET. Use the preliminary first-print rate as reported to one decimal percent; ignore later monthly revisions, benchmark updates, or annual seasonal-adjustment updates.","dataPointId":"bls.jolts.quits_rate.2026-06.first_print","historicalContext":[{"label":"May 2026 quits rate, SA total nonfarm","value":1.9},{"label":"Apr 2026 quits rate, SA total nonfarm","value":1.9},{"label":"Mar 2026 quits rate, SA total nonfarm","value":2.0},{"label":"Feb 2026 quits rate, SA total nonfarm","value":1.9},{"label":"Jan 2026 quits rate, SA total nonfarm","value":2.0}],"drivers":["Quits rate has been range-bound at 1.9 to 2.0 percent in early 2026","May 2026 total quits rate was unchanged at 1.9 percent","June payroll growth slowed to 57,000, limiting upside pressure on voluntary quits","Unemployment stayed low at 4.2 percent, preventing a sharp downside adjustment","BLS reports the target to one decimal, so small latent moves often round to no change"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/news.release/jolts.t04.htm","https://fred.stlouisfed.org/series/JTSQUR","https://www.bls.gov/news.release/empsit.nr0.htm","https://www.bls.gov/news.release/jolts.t02.htm"],"runAt":"2026-07-07T14:01:13Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 BLS JOLTS quits rate"},{"kind":"text","text":"Framing and exact resolver: the target is the BLS JOLTS Table 4 seasonally adjusted total nonfarm quits rate for June 2026, not the quits level, not total private, and not a not-seasonally-adjusted variant. The first print in the August 4, 2026 release governs."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS JOLTS release calendar for the June 2026 reference month.","result":"Fetched official schedule: May 2026 JOLTS is listed for Jun. 30, 2026 at 10:00 AM; June 2026 is listed for Aug. 04, 2026 at 10:00 AM; July 2026 is listed for Sep. 01, 2026 at 10:00 AM."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Table 4 for the latest official seasonally adjusted total nonfarm quits rates and levels.","result":"Fetched Table 4 total row: quits levels were 3,287 thousand in May 2025, 3,046 in Feb 2026, 3,160 in Mar 2026, 3,043 in Apr 2026, and 3,065 in May 2026; quits rates were 2.1, 1.9, 2.0, 1.9, and 1.9 percent, with Apr-May rate change 0.0."},{"kind":"tool","tool":"history.lookup","call":"Checked FRED mirror of BLS series JTSQUR for the recent total nonfarm quits-rate history.","result":"Fetched FRED/BLS JTSQUR recent observations: Jan 2026 2.0, Feb 2026 1.9, Mar 2026 2.0, Apr 2026 1.9, May 2026 1.9 percent; units are Rate, seasonally adjusted, monthly; next release date shown as Aug 4, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Employment Situation for near-contemporaneous June labor-market context.","result":"Fetched June 2026 Employment Situation: total nonfarm payroll employment +57,000, unemployment rate 4.2 percent, labor force participation 61.5 percent, April payroll revision +148,000, May payroll revision +129,000, and April-May combined revisions -74,000."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Table 2 for hires-rate context relevant to quits momentum.","result":"Fetched Table 2 total row: hires levels were 4,899 thousand in Feb 2026, 5,535 in Mar 2026, 5,215 in Apr 2026, and 5,170 in May 2026; hires rates were 3.1, 3.5, 3.3, and 3.3 percent, with Apr-May rate change 0.0."},{"kind":"text","text":"Base-rate/reference class: for the one-month-ahead first print of a rounded JOLTS rate, persistence is the base rate. The recent official-source reference class is the early-2026 total nonfarm quits-rate run of 2.0, 1.9, 2.0, 1.9, and 1.9 percent, which averages 1.94 percent and rounds to 1.9 percent."},{"kind":"text","text":"Level, momentum, and mechanism split: the level effect is stable because May quits were 3,065 thousand and the total quits rate stayed at 1.9 percent. Momentum is flat after Apr-May showed 0.0 rate change. The policy and labor-market mechanism is mixed: June payroll growth softened, but unemployment remained low enough that voluntary quits should not collapse."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the latest official May 2026 quits rate of 1.9 percent and the Jan-May reference-class mean of (2.0 + 1.9 + 2.0 + 1.9 + 1.9) / 5 = 1.94 percent; adjustment components are -0.03 point for slower June payroll growth, +0.01 point for still-low 4.2 percent unemployment, and -0.02 point for flat May hires and quits, leaving 1.90 percent after rounding. Interval method uses successive changes from fetched Jan-May history: -0.1, +0.1, -0.1, 0.0, so sample sigma = 0.096 percentage point and 1.28*sigma = 0.123. Applying 1.90 +/- 0.123 gives 1.78 to 2.02, rounded to the BLS one-decimal reporting grid as 1.8 to 2.0."},{"kind":"text","text":"Counter-consideration and falsification: upside risk is a June rebound in accommodation, retail, or professional-services quits that would land above the interval at 2.1 percent or higher. Downside risk is a broader cooling in worker confidence after weak payroll growth that would land below the interval at 1.7 percent or lower. Central case is another 1.9 percent print because BLS rounding absorbs small latent changes."},{"kind":"forecast","point":1.9,"ciLow":1.8,"ciHigh":2.0}]}

# Reviewer critique
{"summary":"Draft is publishable with no blocking issues; resolver, prior, update, interval, tails, and JSON fields are mostly coherent.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on only four rounded month-to-month changes, which may understate uncertainty for a first-print JOLTS rate.","actionRequested":"State that the interval uses a short rounded recent-volatility sample and either justify why that is adequate or widen/check it against a longer realized-volatility sample."},{"rubricItem":"resolver","severity":"warning","summary":"The source URL is the rolling BLS current-release Table 4 page, which will later point to newer months rather than preserving the June 2026 first print.","actionRequested":"Add that resolution should capture the August 4, 2026 first-print Table 4 or use the BLS archived release/table for that release when available."}],"optionalSuggestions":["Clarify that FRED is used only as a history mirror, not as the resolver.","Name the interval as an 80% central interval to match confidence 0.8.","Consider adding a one-line note that payroll and unemployment evidence are contextual inputs, not direct components of the JOLTS release."]}

Emit the final JSON object only.
