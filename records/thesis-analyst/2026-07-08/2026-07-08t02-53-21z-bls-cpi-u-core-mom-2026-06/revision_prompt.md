# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cpi.u.core_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-core-cpi-mom-june-2026"

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

# Threshold-ladder elicitation (promptMode ladder)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every fast-mode requirement above (sigma arithmetic, base rate, upside/downside/outside-the-interval risks). In the Prior/update/interval step, also state how the ladder-implied 80% width compares to the 1.28*sigma width.
- Add this top-level field to the cell JSON, with your actual rungs as two equal-length numeric arrays:
{
  "thresholdLadder": {
    "thresholds": [
      "strictly increasing numeric rungs"
    ],
    "cumulativeProbabilities": [
      "non-decreasing, within [0.01, 0.99]"
    ]
  }
}


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
{"slug":"us-core-cpi-mom-june-2026","country":"US","type":"data","title":"US core CPI June 2026 MoM","question":"BLS CPI-U all items less food and energy, June 2026, seasonally adjusted month-over-month percent change, first print","unit":"percent_growth","pointEstimate":0.3,"ciLow":0.1,"ciHigh":0.5,"confidence":0.8,"resolutionDate":"2026-07-14","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index news release","resolutionSourceUrl":"https://www.bls.gov/news.release/cpi.nr0.htm","resolutionRule":"Resolve to the first BLS-published seasonally adjusted percent change from the preceding month for CPI-U all items less food and energy for June 2026, as shown in the Consumer Price Index news release scheduled for July 14, 2026 at 08:30 ET. Use the first print rounded to BLS's reported one decimal place; ignore later seasonal-adjustment revisions or corrections.","dataPointId":"bls.cpi.u.core_mom.june_2026.first_print","historicalContext":[{"label":"Dec 2025 core CPI-U MoM SA first print","value":0.2},{"label":"Jan 2026 core CPI-U MoM SA first print","value":0.3},{"label":"Feb 2026 core CPI-U MoM SA first print","value":0.2},{"label":"Mar 2026 core CPI-U MoM SA first print","value":0.2},{"label":"Apr 2026 core CPI-U MoM SA first print","value":0.4},{"label":"May 2026 core CPI-U MoM SA first print","value":0.2}],"drivers":["Recent BLS core CPI-U prints are clustered around 0.2 to 0.3 percent","May core goods softness offsets part of the services pressure","Shelter and medical care services keep underlying services inflation sticky","Energy is excluded directly, but recent energy strength creates modest indirect upside risk","One-decimal first-print rounding makes 0.2, 0.3, and 0.4 the main probability mass"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.nr0.htm","https://www.bls.gov/news.release/archives/cpi_06102026.htm","https://fred.stlouisfed.org/series/CPILFESL"],"runAt":"2026-07-08T02:53:30Z","thresholdLadder":{"thresholds":[-0.1,0,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.6,0.7],"cumulativeProbabilities":[0.03,0.07,0.12,0.2,0.32,0.43,0.56,0.68,0.78,0.85,0.91,0.97,0.99]},"reasoning":[{"kind":"heading","text":"Forecast for June 2026 BLS core CPI-U month-over-month first print"},{"kind":"text","text":"The resolver is the first official BLS CPI Summary release for the June 2026 reference month, using CPI-U all items less food and energy, seasonally adjusted percent change from the preceding month. This is the core CPI-U variant, not headline CPI-U, not NSA CPI, and not a later revised database value."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Consumer Price Index release schedule for the June 2026 reference month.","result":"Fetched official BLS schedule: reference month June 2026, release date July 14, 2026, release time 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS May 2026 CPI Summary and Table A for recent core CPI-U monthly changes.","result":"Fetched BLS Table A numbers for all items less food and energy: Dec. 2025 = 0.2, Jan. 2026 = 0.3, Feb. 2026 = 0.2, Mar. 2026 = 0.2, Apr. 2026 = 0.4, May 2026 = 0.2, and May 2026 12-month core change = 2.9."},{"kind":"tool","tool":"official.lookup","call":"Read BLS May 2026 CPI Summary component details relevant to core CPI momentum.","result":"Fetched May 2026 component numbers: all items rose 0.5, energy rose 3.9, gasoline rose 7.0, all items less food and energy rose 0.2, shelter rose 0.3, services less energy services rose 0.3, commodities less food and energy commodities fell 0.1, medical care services rose 0.5, airline fares rose 2.7, and motor vehicle insurance fell 1.7."},{"kind":"tool","tool":"repo.lookup","call":"Checked local public Thesis artifact quoting the FRED CPILFESL mirror of the BLS seasonally adjusted core CPI-U index.","result":"Fetched public artifact values from FRED mirror CPILFESL: Jan. 2026 = 332.793, Feb. 2026 = 333.512, Mar. 2026 = 334.165, Apr. 2026 = 335.423, May 2026 = 336.121; computed MoM changes were Feb. 2026 = 0.216, Mar. 2026 = 0.196, Apr. 2026 = 0.376, and May 2026 = 0.208."},{"kind":"text","text":"Base rate/reference class: the recent official BLS first-print reference class is the six monthly core CPI-U changes from Dec. 2025 through May 2026: 0.2, 0.3, 0.2, 0.2, 0.4, and 0.2. The mean is 0.25 and the median is 0.2, so the base rate puts most mass on a first print that rounds to 0.2 or 0.3, with 0.4 plausible but not modal."},{"kind":"text","text":"Level, momentum, one-off, and mechanism split: the level is still firm at 2.9 percent year over year, but May momentum was only 0.2 after April's 0.4. Shelter at 0.3 and medical care services at 0.5 argue against a very soft core print; core commodities at -0.1, new vehicles at -0.3, and motor vehicle insurance at -1.7 argue against extrapolating April's 0.4. Energy is excluded directly, but gasoline and airfares can pass through indirectly at the margin."},{"kind":"math","text":"Ladder: P(X <= -0.1) = 0.03, P(X <= 0) = 0.07, P(X <= 0.1) = 0.12, P(X <= 0.15) = 0.20, P(X <= 0.2) = 0.32, P(X <= 0.25) = 0.43, P(X <= 0.3) = 0.56, P(X <= 0.35) = 0.68, P(X <= 0.4) = 0.78, P(X <= 0.45) = 0.85, P(X <= 0.5) = 0.91, P(X <= 0.6) = 0.97, P(X <= 0.7) = 0.99. Linear interpolation gives p10 at 0.06, p50 at 0.277, and p90 at 0.492; rounding to BLS one-decimal print precision gives ciLow 0.1, pointEstimate 0.3, and ciHigh 0.5."},{"kind":"text","text":"Prior/update/interval: use a persistence prior from the BLS first-print core CPI-U reference class for Dec. 2025-May 2026, centered at mean 0.25. Adjustment components are +0.03 for sticky shelter/services and indirect energy or airfare pass-through, -0.01 for core goods and vehicle-related softness, and +0.01 for rounding asymmetry around a 0.28 unrounded center, giving a rounded 0.3 point. For a change/flow series, sigma is computed from the values themselves: sigma = sqrt(((0.2-0.25)^2 + (0.3-0.25)^2 + (0.2-0.25)^2 + (0.2-0.25)^2 + (0.4-0.25)^2 + (0.2-0.25)^2) / 6) = 0.076, so 1.28*sigma = 0.097. The ladder-implied unrounded 80% half-width is roughly (0.492 - 0.06) / 2 = 0.216, wider than 1.28*sigma because the target is still one unreleased monthly first print with tariff/energy pass-through and services-price tail risk not fully represented in the short six-month sample."},{"kind":"text","text":"Counter-consideration: upside risk outside the interval would require a broad services re-acceleration, tariff-sensitive core goods rebound, and indirect fuel or airfare pass-through pushing the first print above 0.5. Downside risk outside the interval would be renewed goods deflation plus a sharper shelter/OER slowdown and another motor-vehicle-insurance decline pushing the print below 0.1. Those scenarios are possible but below 20 percent combined in the ladder."},{"kind":"forecast","point":0.3,"ciLow":0.1,"ciHigh":0.5}]}

# Reviewer critique
{
  "summary": "The draft is publishable after minor ordering/source-precision cleanup; no blocking leakage, resolver, unit, or coherence problem is apparent.",
  "requiredFixes": [
    {
      "rubricItem": "base_rate",
      "severity": "warning",
      "summary": "The base-rate paragraph is present, but it appears after several current-evidence/tool-result items and after driver bullets.",
      "actionRequested": "Move or duplicate the Dec 2025-May 2026 persistence prior before the inside-view driver/update discussion."
    },
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The resolver uses the live BLS CPI news-release URL, which will later roll forward and may not itself preserve the June 2026 first print.",
      "actionRequested": "Keep the official BLS release as resolver, but state that the first-print evidence should be taken from the July 14, 2026 CPI Summary or its BLS archive once posted."
    }
  ],
  "optionalSuggestions": [
    "In the compact Prior/update/interval step, explicitly label the historical sample as six observations and note that the wider ladder overrides the short-sample sigma.",
    "Tighten the energy-pass-through language since energy is excluded from core CPI and only indirect channels matter."
  ]
}

Emit the final JSON object only.
