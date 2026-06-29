# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usda.fns.snap.maximum_allotment.household_size_4.48dc.fy2027
- period: FY2027
- conditional_on: null

# Source hints
- Use USDA FNS program-data pages, official data tables, and the FNS data release calendar.
- For SNAP, WIC, and QC targets, distinguish annual fiscal-year quality-control releases from monthly participation tables.
- If the catalog unit is millions, convert official person counts to millions in the emitted cell.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class.
- Anchor on the outside-view base rate before current-release adjustments.
- Separate level, momentum, one-off, and policy-mechanism effects before combining them.
- Size the 80% interval from realized first-print dispersion, then widen or skew only for stated reasons.
- Name concrete upside, downside, and outside-the-interval scenarios.

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
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step, one math step, one counter-consideration, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.1.0, prompt 9435029c5fb9, tools e15bf40583f8, promptMode fast)


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
{"slug":"snap-max-allotment-family-4-fy2027","country":"US","type":"data","title":"SNAP family-4 max allotment FY2027","question":"What will the first USDA FNS FY2027 maximum monthly SNAP allotment for a household of 4 in the 48 contiguous states and DC be, in dollars per month?","unit":"usd","pointEstimate":1021,"ciLow":1000,"ciHigh":1055,"confidence":0.8,"resolutionDate":"2026-09-30","resolutionSource":"USDA Food and Nutrition Service SNAP FY2027 Cost-of-Living Adjustments","resolutionSourceUrl":"https://www.fns.usda.gov/snap/fy-2027-cola","resolutionRule":"Resolve to the first USDA FNS FY2027 SNAP COLA table or memorandum value for maximum monthly allotments, household size 4, 48 contiguous states and DC. Use the first posted FY2027 table even if later revised; record the dollar amount as published, with no conversion beyond treating it as dollars per month. If the table is posted before 2026-09-30, that first post still governs.","dataPointId":"usda.fns.snap.maximum_allotment.household_size_4.48dc.fy2027.first_print","historicalContext":[{"label":"FY2023 official first print","value":939},{"label":"FY2024 official/catalog reference","value":973},{"label":"FY2025 official/catalog reference","value":975},{"label":"FY2026 catalog anchor","value":994}],"drivers":["June 2026 Thrifty Food Plan cost","Food-at-home CPI running 2.7 percent year over year in May 2026","ERS 2026 food-at-home forecast midpoint 2.8 percent","Annual FNS COLA table effective October 1","Low but nonzero policy-change risk around TFP rules"],"sourceContext":["https://www.fns.usda.gov/snap/fy-2023-cola","https://www.usda.gov/guidance-documents/snap/fns/snap-fy-2024-cost-living-adjustments-0","https://www.usda.gov/guidance-documents/snap/fns/snap-fy-2025-cost-living-adjustments","https://www.bls.gov/news.release/cpi.nr0.htm","https://www.ers.usda.gov/data-products/food-price-outlook/summary-findings","https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273/subpart-D/section-273.10"],"runAt":"2026-06-27T23:13:24Z","reasoning":[{"kind":"heading","text":"SNAP FY2027 maximum allotment, household of 4"},{"kind":"text","text":"Resolver is the first USDA FNS FY2027 SNAP COLA table for the household-size-4 maximum monthly allotment in the 48 contiguous states and DC. The repo already registers the canonical slug snap-max-allotment-family-4-fy2027 and target date 2026-09-30, so I reuse that rather than creating a near-duplicate."},{"kind":"tool","tool":"local.repo","call":"rg and sed over forecast-cells.ts and ledger-targets.generated.ts for the target registration","result":"Fetched canonical slug snap-max-allotment-family-4-fy2027; catalog values include FY2024 973, FY2025 975, FY2026e 994, prior point 1010, prior CI 975 to 1045, and ledger resolutionDate 2026-09-30."},{"kind":"tool","tool":"official.fns.lookup","call":"Open USDA FNS SNAP FY2023 COLA page for an official inline reference point and effective-date mechanics","result":"Fetched FY2023 memorandum date August 9, 2022, effective Oct. 1, 2022, and household-of-4 48 states/DC maximum allotment 939 dollars."},{"kind":"tool","tool":"official.usda.guidance.lookup","call":"Open USDA Guidance Portal entries for FY2024 and FY2025 SNAP COLA issue dates","result":"Fetched FY2024 issued date August 3, 2023 and FY2025 issued date August 2, 2024; FNS pages show FY2024 page updated March 16, 2026 and FY2025 page updated March 6, 2026."},{"kind":"tool","tool":"official.ecfr.lookup","call":"Open 7 CFR 273.10 maximum SNAP allotment rule","result":"Fetched 7 CFR 273.10 current as of 6/24/2026; maximum allotments are adjusted annually, posted in an FNS web table, effective October 1, and based on 100% of the preceding June TFP rounded down to the nearest lower dollar."},{"kind":"tool","tool":"official.bls.lookup","call":"Open BLS May 2026 CPI release for current food-at-home momentum","result":"Fetched BLS May 2026 CPI: all items +0.5 percent monthly and +4.2 percent year over year; food at home +0.1 percent monthly and +2.7 percent year over year; June 2026 CPI scheduled for July 14, 2026."},{"kind":"tool","tool":"official.ers.lookup","call":"Open USDA ERS June 2026 Food Price Outlook summary","result":"Fetched ERS June 2026 forecast: food-at-home prices predicted +2.8 percent in 2026 with 95 percent prediction interval 1.4 to 4.4 percent; all food +3.2 percent with interval 2.2 to 4.2 percent."},{"kind":"text","text":"Base-rate/reference class: recent first-print household-of-4 values moved 939 to 973 to 975, and the local FY2026 anchor is 994. The year-to-year changes are about +3.6 percent, +0.2 percent, and +1.9 percent, with the current inflation evidence closer to the upper part of that recent range than to the FY2025 near-flat COLA."},{"kind":"text","text":"Level, momentum, and mechanism: the best level anchor is the FY2026 catalog anchor of 994 dollars. Current grocery inflation has not collapsed; BLS shows 2.7 percent year-over-year food-at-home inflation in May 2026 and ERS puts 2026 food-at-home inflation at 2.8 percent. The eCFR rule makes this a mechanical TFP/June-cost update unless Congress or USDA changes the TFP basis before the FY2027 table."},{"kind":"math","text":"Point: 994 dollars FY2026 anchor x 1.027 May food-at-home momentum = 1020.8, rounded to about 1021 dollars as an expected first-print value. Interval: apply ERS-like food-at-home uncertainty and policy/mechanical rounding around the FY2026 anchor: low roughly 994 x 1.006 = 1000, high roughly 994 x 1.061 = 1055, allowing extra upside for June food/TFP category strength and modest downside for a cooler June or lower TFP basket movement."},{"kind":"text","text":"Counter-consideration: outside the lower bound if June 2026 TFP costs soften sharply or legislation freezes/rebases SNAP maximum allotments before the FY2027 table; outside the upper bound if a fresh TFP reevaluation, commodity shock, or food-at-home spike pushes the June TFP several points above current CPI signals."},{"kind":"forecast","point":1021,"ciLow":1000,"ciHigh":1055}]}

# Reviewer critique
{"summary":"The draft is mostly publishable, but it needs tighter resolver timing/source wording and a more defensible interval derivation tied to the actual SNAP/TFP mechanism.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The resolver rule is clear, but the `resolutionDate` of 2026-09-30 reads like a latest-by/effective-date boundary rather than the expected first-print publication date, and the FY2027 URL appears to be a future placeholder.","actionRequested":"Clarify that 2026-09-30 is the resolution deadline or catalog date, not necessarily the publication date, and state that the first official USDA FNS FY2027 SNAP COLA memorandum/table controls once posted."},{"rubricItem":"interval","severity":"warning","summary":"The interval math is only loosely connected to the cited ERS uncertainty and the statutory TFP June-cost mechanism; the low/high implied growth rates do not directly match the cited ERS 1.4%-4.4% interval.","actionRequested":"Explain the interval as explicit forecast uncertainty around June 2026 TFP movement, rounding, and policy risk, or revise the bounds/math so they follow the cited volatility or prediction interval more directly."},{"rubricItem":"coherence","severity":"warning","summary":"The reasoning mentions a local prior point of 1010 and prior CI 975-1045, but the final forecast moves to 1021 with interval 1000-1055 without explicitly reconciling the catalog prior with the new evidence.","actionRequested":"Add one sentence explaining the final forecast step from the catalog prior or FY2026 anchor to the published point and interval."}],"optionalSuggestions":["Replace the driver phrase `June 2026 Thrifty Food Plan cost` with wording that makes clear the June 2026 TFP value is not yet observed at run time.","Make the tail scenarios more quantitative, for example specifying what TFP percentage change would put the result below 1000 or above 1055."]}

Emit the final JSON object only.
