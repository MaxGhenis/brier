# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.new_residential_sales.new_single_family_houses_sold_saar
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-new-home-sales-saar-june-2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "census.new_residential_sales.new_single_family_houses_sold_saar.2026_06.first_print"
- resolutionSourceUrl: "https://www.census.gov/construction/nrs/current/index.html"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.census.gov"], "expectedReleaseWindow": {"end": "2026-07-24", "start": "2026-07-24"}, "field": "Sales of new single-family houses, United States, seasonally-adjusted annual rate", "releasePolicy": "first_print", "sourceSeriesId": "RESSALES.SOLD.TOTAL.US.SAAR", "sourceUrl": "https://www.census.gov/construction/nrs/current/index.html", "table": "Monthly New Residential Sales, Table 1: New Houses Sold and For Sale", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-ac8614c86d2fa983f323f64f18c92df648f3ed58f35faa09e85b571954df9ae8.json"
- targetContentHash: "ac8614c86d2fa983f323f64f18c92df648f3ed58f35faa09e85b571954df9ae8"
- registeredAtUtc: "2026-07-10T05:58:27Z"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.

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
{"slug":"us-new-home-sales-saar-june-2026","country":"US","type":"data","title":"US New Home Sales SAAR, June 2026","question":"What will the U.S. Census Bureau and HUD first report for sales of new single-family houses in the United States in June 2026, seasonally adjusted annual rate, in thousands?","unit":"thousands","pointEstimate":590,"ciLow":525,"ciHigh":655,"confidence":0.8,"resolutionDate":"2026-07-24","resolutionSource":"U.S. Census Bureau and U.S. Department of Housing and Urban Development Monthly New Residential Sales release","resolutionSourceUrl":"https://www.census.gov/construction/nrs/current/index.html","resolutionRule":"Resolve to the first-print value in Monthly New Residential Sales, Table 1, New Houses Sold and For Sale, for Sold during period, United States, seasonally adjusted annual rate, June 2026. Record the published value in thousands of houses at an annual rate; do not apply later revisions or same-day corrections unless the Census first-print release itself republishes the table before the initial public value is captured.","dataPointId":"census.new_residential_sales.new_single_family_houses_sold_saar.2026_06.first_print","historicalContext":[{"label":"May 2026 HSN1F SAAR","value":580},{"label":"Apr 2026 HSN1F SAAR","value":626},{"label":"Mar 2026 HSN1F SAAR","value":664},{"label":"Feb 2026 HSN1F SAAR","value":630},{"label":"Jan 2026 HSN1F SAAR","value":576}],"drivers":["May first-print sales fell to 580 thousand SAAR from revised April 626 thousand","Recent Jan-May values show large month-to-month noise around a roughly 600 thousand level","May new-home inventory was high at 496 thousand and 10.3 months of supply","Single-family starts and permits were soft but not collapsing","Mortgage rates around late June and early July remained near 6.5 percent"],"sourceContext":["https://www.census.gov/construction/nrs/current/index.html","https://www.census.gov/construction/soc/schedule.html","https://fred.stlouisfed.org/series/HSN1F","https://www.census.gov/construction/nrc/current/index.html","https://fred.stlouisfed.org/series/MORTGAGE30US"],"runAt":"2026-07-10T06:12:44Z","reasoning":[{"kind":"heading","text":"US June 2026 new single-family houses sold SAAR first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets Census/HUD Monthly New Residential Sales, Table 1, Sold during period, United States, seasonally adjusted annual rate, source series HSN1F / RESSALES.SOLD.TOTAL.US.SAAR, for June 2026. The variant is SAAR, not NSA, and the resolution rule is strict first print."},{"kind":"tool","tool":"official.lookup","call":"Opened Census Survey of Construction release schedule for the New Residential Sales release date.","result":"The official schedule lists the June 2026 survey month New Residential Sales release on July 24, 2026 at 10:00 a.m.; it also lists May 2026 New Residential Sales on June 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened Census current Monthly New Residential Sales press release for the latest official first-print facts.","result":"The May 2026 release reported sales of new single-family houses at 580,000 SAAR, 7.3 percent below the April 2026 rate of 626,000 and 6.8 percent below the May 2025 rate of 622,000; for-sale inventory was 496,000 and months' supply was 10.3."},{"kind":"tool","tool":"public.history_mirror","call":"Opened FRED HSN1F, which cites Census/HUD as source, to read recent monthly history for the same SAAR United States series.","result":"Recent HSN1F observations were May 2026 580, Apr 2026 626, Mar 2026 664, Feb 2026 630, and Jan 2026 576, all in thousands at a seasonally adjusted annual rate."},{"kind":"tool","tool":"official.lookup","call":"Opened Census New Residential Construction May 2026 release for supply-side housing indicators.","result":"May 2026 privately owned housing starts were 1,177,000 SAAR, down 15.4 percent from April; single-family starts were 882,000, down 1.9 percent from April; single-family authorizations were 886,000, up 0.6 percent from April."},{"kind":"tool","tool":"public.lookup","call":"Opened FRED MORTGAGE30US, sourced to Freddie Mac PMMS, for current mortgage-rate context.","result":"The 30-year fixed mortgage rate was 6.49 percent on 2026-07-09, 6.43 percent on 2026-07-02, 6.49 percent on 2026-06-25, 6.47 percent on 2026-06-18, and 6.52 percent on 2026-06-11."},{"kind":"text","text":"Base rate / reference class: for a one-month-ahead forecast of a volatile level series, persistence from the latest same-variant official print is the base rate. The latest observed level is 580 thousand, while the Jan-May 2026 run is 576, 630, 664, 626, 580, so a central June value near the high-500s to low-600s is the outside-view anchor."},{"kind":"text","text":"Adjustment components: level starts from May's 580; momentum gets a small positive offset because a 46 thousand May drop followed a 38 thousand April drop and some mean reversion is common; high inventory of 496 thousand and 10.3 months' supply offsets that rebound; mortgage rates near 6.5 percent and soft single-family starts argue against a sharp upside breakout."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 HSN1F 580. Historical sample = fetched Jan-May 2026 HSN1F values 576, 630, 664, 626, 580. Successive changes are +54, +34, -38, -46; their sample mean is +1 and sigma = 50.4 thousand. Adjustment components are +15 thousand mean reversion after the May drop, -5 thousand for high months' supply and affordability, and 0 thousand for starts/rate context, giving point = 580 + 10 = 590. The 80% half-width is roughly 1.28*sigma = 1.28*50.4 = 64.5, rounded to 65, so bounds are 590 - 65 = 525 and 590 + 65 = 655."},{"kind":"text","text":"Counter-considerations: upside risk is a builder-incentive or rate-relief rebound that would land above the interval if June first-print sales exceed about 655 thousand; downside risk is another demand freeze or regional pullback that would land below the interval if the first print is under about 525 thousand. A value outside the interval would most likely reflect a large regional swing, especially in the South or West, rather than normal national noise."},{"kind":"forecast","point":590,"ciLow":525,"ciHigh":655}]}

# Reviewer critique
{
  "summary": "The draft is publishable on resolver, units, prior/update structure, and coherence, but the interval support is thin because it estimates 80% uncertainty from only four recent month-to-month changes.",
  "requiredFixes": [
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval is based on Jan-May 2026 changes only, giving just four deltas and likely under-supporting realized volatility for this noisy series.",
      "actionRequested": "Either expand the volatility sample to a longer same-series monthly history or explicitly state that the short-sample sigma is a rough uncertainty proxy and justify why the 525-655 bounds remain appropriate."
    }
  ],
  "optionalSuggestions": [
    "Clarify whether recent historical values from FRED are latest-vintage/revised history while the target resolves to the Census first print.",
    "Keep the resolver wording aligned with the ledger by emphasizing the Census Table 1 first public June 2026 SAAR value in thousands."
  ]
}

Emit the final JSON object only.
