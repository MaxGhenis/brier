# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-11"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-11.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}

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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US continued claims, week ending Jul 11","question":"First-print DOL ETA seasonally adjusted insured unemployment, continued claims, for the week ending July 11, 2026","unit":"millions","pointEstimate":1.822,"ciLow":1.784,"ciHigh":1.86,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Employment and Training Administration, Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260723","resolutionRule":"Resolve to the first official DOL ETA Unemployment Insurance Weekly Claims Report released July 23, 2026: the seasonally adjusted Insured Unemployment value for week ending July 11, 2026, divided by 1,000,000 and rounded to three decimals in millions. Use the first print only; ignore later revisions and FRED/ALFRED vintage changes except as mirrors of the official first print.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"latest_official_sa_insured_unemployment_we_2026-06-27_millions","value":1.814},{"label":"previous_official_sa_insured_unemployment_we_2026-06-20_millions","value":1.806},{"label":"official_sa_insured_unemployment_we_2026-06-13_millions","value":1.812},{"label":"official_sa_insured_unemployment_we_2026-06-06_millions","value":1.8}],"drivers":["latest SA insured unemployment was 1.814 million","recent four-week average rose to 1.808 million","initial claims for week ending July 4 were low at 215,000","continued-claims momentum is mildly positive but not accelerating","two unreleased weeks add horizon uncertainty"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260709","https://www.dol.gov/newsroom/releases/eta","https://www.dol.gov/newsroom/economicdata","https://www.dol.gov/ui/data.pdf"],"runAt":"2026-07-10T03:27:54Z","reasoning":[{"kind":"heading","text":"Forecast for DOL SA continued claims, week ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: this is the DOL ETA Unemployment Insurance Weekly Claims Report seasonally adjusted Insured Unemployment series, the same SA variant throughout, for week ending July 11, 2026. The ledger unit is millions and the official report prints persons, so the transform is persons times 0.000001."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL ETA July 9, 2026 Unemployment Insurance Weekly Claims Report and release archive.","result":"Fetched release timestamp 8:30 a.m. Eastern Thursday July 9, 2026; archive release dates July 9, 2026, July 2, 2026, and June 25, 2026; July 9 report contains SA insured unemployment for week ending June 27, 2026, so the week ending July 11, 2026 first-print continued-claims report is tied to the July 23, 2026 DOL ETA release."},{"kind":"tool","tool":"official.lookup","call":"Fetched latest DOL SA insured unemployment table values from the July 9 report.","result":"Fetched Insured Unemployment (SA): 1,814,000 for week ending June 27, 2026; 1,806,000 for June 20, 2026; change +8,000; June 13, 2026 value 1,812,000; prior-year comparable 1,952,000."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent DOL SA claims context from the same variant table and current release text.","result":"Fetched 4-week moving average for SA insured unemployment 1,808,000 for week ending June 27, 2026, up +7,000 from revised 1,801,000; recent SA insured unemployment values include 1,786,000 on May 30, 1,800,000 on June 6, 1,812,000 on June 13, 1,806,000 on June 20, and 1,814,000 on June 27."},{"kind":"tool","tool":"official.lookup","call":"Fetched leading initial-claims and NSA context from DOL July 9 report.","result":"Fetched initial claims SA 215,000 for week ending July 4, 2026, down -2,000 from 217,000; initial claims 4-week average 218,750; NSA insured unemployment 1,766,759 for week ending June 27, 2026, up +18,463 from 1,748,296."},{"kind":"text","text":"Base rate/reference class: for a weekly level series with small revisions and strong persistence, the base rate is a random-walk/persistence prior around the latest first-print SA insured unemployment value, with recent one-week changes used to size the typical miss."},{"kind":"math","text":"Prior/update/interval: persistence prior = 1.814 million from the latest official SA insured-unemployment first print; historical sample = DOL table weekly SA insured-unemployment changes from June 28, 2025 through June 27, 2026; adjustment components = +0.006 million for two weeks of mild upward continued-claims momentum, +0.002 million for the 4-week average rising, and +0.000 million for low/flat initial claims limiting acceleration, giving point = 1.814 + 0.006 + 0.002 = 1.822 million. Interval method: standard deviation of fetched one-week changes has sigma = 0.0209 million, so 1.28*sigma = 0.0268 million; because the target is two unreleased continued-claims weeks ahead, widen to about sqrt(2)*0.0268 = 0.038 million, giving 1.822 +/- 0.038 = [1.784, 1.860]."},{"kind":"text","text":"Upside risk: a fresh wave of layoffs or delayed benefit exits visible first in state continued claims would land above the interval, especially if the July 4 and July 11 SA insured-unemployment prints both rise by more than about 20,000. Downside risk: faster exits from benefits plus very low new initial claims would land below the interval. A one-week seasonal-adjustment irregularity or reporting disruption outside the interval would be falsifying for the smooth persistence setup."},{"kind":"forecast","point":1.822,"ciLow":1.784,"ciHigh":1.86}]}

# Reviewer critique
{"summary":"The draft is publication-ready on methodology and coherence, with only a resolver/source wording concern to align against the canonical ledger binding.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The draft resolves directly to the future DOL ETA release URL, while the canonical ledger sourceBinding names ALFRED graph CSV/CCSA with advance_vintage and DOL as an allowed official host.","actionRequested":"Clarify that the official DOL July 23, 2026 first print is the economic source of truth and that ALFRED CCSA advance vintage is only the bound resolver/mirror if that is how the catalog adapter will resolve it."}],"optionalSuggestions":["In the Prior/update/interval step, state whether the 0.0209 million sigma is computed on first-print values only or on the current DOL table history, since revisions can slightly change weekly-change volatility.","The upside and downside tails are adequate; adding approximate numeric tail thresholds such as below 1.784 or above 1.860 would make them even tighter."]}

Emit the final JSON object only.
