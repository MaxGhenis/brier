# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: irs.irc24.child_tax_credit.maximum.ty2027
- period: tax year 2027
- conditional_on: null

# Source hints
- Use IRS filing-season statistics, annual inflation-adjustment revenue procedures, and official IRS release pages.
- For threshold targets, resolve to the first official IRS value for the named tax year and parameter, not an inferred estimate once the official figure is available.
- Match the catalog unit, usually nominal dollars or billions of nominal dollars.

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
{"slug":"ctc-maximum-per-child-ty2027","country":"US","type":"data","title":"CTC maximum per child, TY2027","question":"IRS first official inflation-adjusted maximum Child Tax Credit per qualifying child under IRC section 24(a) and 24(h)(2) for tax year 2027, in nominal dollars, first print.","unit":"usd","pointEstimate":2300,"ciLow":2200,"ciHigh":2400,"confidence":0.8,"resolutionDate":"2026-09-11","resolutionSource":"IRS annual inflation-adjustment revenue procedure for tax year 2027, with BLS August 2026 CPI release fixing the statutory formula input","resolutionSourceUrl":"https://www.irs.gov/pub/irs-drop/rp-25-32.pdf","resolutionRule":"Resolve to the first official IRS published value for the maximum amount of the Child Tax Credit under IRC section 24(a), as modified by section 24(h)(2), for taxable years beginning in 2027. Use the nominal dollar amount per qualifying child in the first IRS annual inflation-adjustment revenue procedure or equivalent IRS release for tax year 2027. If later IRS forms or instructions revise the amount, ignore them unless the first IRS release is formally corrected. The statutory formula uses section 1(f)(3) chained-CPI cost-of-living adjustment with 2024 substituted for 2016 and rounds any increase down to the next lowest multiple of $100.","dataPointId":"irs.irc24.child_tax_credit.maximum.ty2027.first_print","historicalContext":[{"label":"TY2026 IRS maximum CTC per child","value":2200},{"label":"TY2025 statutory maximum CTC per child","value":2200},{"label":"TY2024 pre-OBBBA maximum CTC per child","value":2000},{"label":"TY2021 ARPA maximum for age 6-17","value":3000},{"label":"TY2021 ARPA maximum for under age 6","value":3600}],"drivers":["OBBBA made the expanded child tax credit permanent and raised the 2025 base amount to $2,200","IRC section 24(i)(2) indexes the $2,200 maximum after 2025 using chained CPI with 2024 as the base year","Rounding down to the next lowest $100 creates a discrete threshold near 4.545 percent cumulative inflation from the 2024 base","BLS May 2026 CPI shows renewed energy-driven inflation, making the $2,300 threshold more likely than a no-change $2,200 outcome","The main downside risk is disinflation or data revision leaving the September 2025-August 2026 average below the statutory threshold"],"sourceContext":["https://www.govinfo.gov/content/pkg/PLAW-119publ21/pdf/PLAW-119publ21.pdf","https://www.irs.gov/pub/irs-drop/rp-25-32.pdf","https://www.bls.gov/news.release/cpi.nr0.htm","https://www.bls.gov/schedule/2026/09_sched.htm"],"runAt":"2026-06-27T23:29:48Z","reasoning":[{"kind":"heading","text":"Forecast for TY2027 maximum Child Tax Credit per child"},{"kind":"text","text":"The resolver is the first official IRS dollar value for the maximum Child Tax Credit per qualifying child for tax year 2027. This is the headline nonrefundable-plus-refundable maximum under IRC section 24(a) as modified by section 24(h)(2), not the refundable cap, phase-in rate, phaseout threshold, or monthly equivalent."},{"kind":"tool","tool":"repo.lookup","call":"Searched the local catalog and records for existing CTC targets and canonical slugs.","result":"Fetched existing related catalog cell ctc-monthly-max-ty2027 with historical monthly values 2021 = 300, 2022 = 167, 2024 = 167, 2025 = 167, and 2026e = 167; records also showed ctc-maximum-per-child-ty2027 as the obvious canonical maximum-per-child slug."},{"kind":"tool","tool":"official.lookup","call":"Opened GovInfo Public Law 119-21, section 70104, Extension and enhancement of increased child tax credit.","result":"Fetched statutory values: section 70104 changes IRC section 24(h)(2) from $2,000 to $2,200, applies after December 31, 2024, and section 24(i)(2) indexes the $2,200 amount after 2025 using section 1(f)(3) with 2024 substituted for 2016; section 24(i)(3) rounds any increase down to the next lowest multiple of $100."},{"kind":"tool","tool":"official.lookup","call":"Opened IRS Rev. Proc. 2025-32 for tax year 2026 annual inflation adjustments.","result":"Fetched IRS first-print context: Rev. Proc. 2025-32 says OBBBA provides a maximum Child Tax Credit of $2,200 for taxable years beginning in 2025, adjusted for inflation after December 31, 2025; for taxable years beginning in 2026, section 4.05 lists maximum credit amount = $2,200 and refundable portion = $1,700."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS May 2026 CPI release for inflation momentum relevant to the remaining statutory chained-CPI months.","result":"Fetched inflation context: CPI-U rose 0.5 percent in May 2026 and 4.2 percent over 12 months; April 2026 12-month CPI-U was 3.8 percent; energy rose 23.5 percent over 12 months; C-CPI-U rose 4.0 percent over 12 months and 0.6 percent in May on a not seasonally adjusted basis."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS September 2026 release calendar to verify when the final August CPI input becomes public.","result":"Fetched release schedule: Consumer Price Index for August 2026 is scheduled for September 11, 2026 at 08:30 AM Eastern; this is the official release that fixes the last month in the September 2025-August 2026 CPI window used for calendar-year 2027 tax inflation adjustments."},{"kind":"text","text":"Base-rate/reference class: recent official IRS annual inflation adjustments for this exact parameter show the base moving from the old $2,000 regime to $2,200 under OBBBA, with TY2026 still $2,200 because the first year of chained-CPI growth over the 2024 base did not produce a full $100 rounded-down increase. The outside-view prior is therefore sticky at $2,200 or a one-notch move to $2,300, not a continuous estimate."},{"kind":"text","text":"Mechanism decomposition: level is the statutory $2,200 base; momentum comes from elevated 2026 inflation, especially the May 2026 C-CPI-U 4.0 percent 12-month increase; the one-off component is energy-price pressure that may fade before August; policy risk is small because OBBBA already made the credit permanent, but Congress could still amend section 24 before the IRS print."},{"kind":"text","text":"Counter-consideration: the no-change $2,200 case remains plausible if June-August chained CPI is soft enough, if preliminary C-CPI-U revisions lower the 12-month average, or if IRS applies a technical convention that leaves the cumulative adjustment just below the $100 threshold. An upside outside the interval would require a legislative expansion or unusually high inflation producing a $2,500-or-higher official value; a downside outside the interval would require repeal or a statutory cut."},{"kind":"math","text":"Threshold math: under section 24(i)(2)-(3), the TY2027 increase is floor_to_$100(2200 * COLA_2027_with_2024_base). The first $100 increment requires COLA >= 100 / 2200 = 4.545 percent. TY2026 remained $2,200, implying the one-year 2025-over-2024 COLA generated less than $100 after rounding. By May 2026, BLS reported C-CPI-U +4.0 percent over 12 months and CPI-U +4.2 percent, so the two-year 2026-over-2024 window is very likely above 4.545 percent by August 2026. Central calculation: $2,200 + $100 = $2,300. I use an 80 percent interval of $2,200 to $2,400 to cover a near-threshold miss and a two-notch inflation surprise or technical treatment."},{"kind":"forecast","point":2300,"ciLow":2200,"ciHigh":2400}]}

# Reviewer critique
{"summary":"Draft is directionally coherent but has a blocking resolver/date/source problem because it resolves on the BLS CPI input date while the target asks for the IRS first official dollar print.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"Resolution date is set to 2026-09-11, the scheduled August 2026 CPI release, but the resolver is the first IRS TY2027 inflation-adjustment revenue procedure or equivalent IRS release.","actionRequested":"Change resolutionDate to the expected IRS first-print release date or a justified IRS release placeholder, and state that BLS September 11 only fixes an input, not the resolving publication."},{"rubricItem":"resolver","severity":"blocking","summary":"resolutionSourceUrl points to Rev. Proc. 2025-32 for TY2026, not the future TY2027 first-print source.","actionRequested":"Use a stable IRS annual inflation-adjustments/irs-drop source as the expected resolver placeholder, and specify that the final resolved URL must be the TY2027 IRS revenue procedure or formal IRS correction if issued."},{"rubricItem":"model_prior","severity":"warning","summary":"The draft gives threshold math but does not clearly state a quantitative time-series/model prior or explicitly rule out using one.","actionRequested":"Add one sentence saying whether a simple chained-CPI persistence/nowcast model was used, with approximate probabilities for $2,200/$2,300/$2,400, or explicitly state why no time-series model is used."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is plausible but not tied to realized volatility or a quantified uncertainty distribution.","actionRequested":"Anchor the $2,200-$2,400 interval to a concrete uncertainty calculation, such as remaining June-August chained-CPI scenarios, historical forecast errors, or discrete probability mass by rounded credit amount."}],"optionalSuggestions":["Clarify whether the target is the nonrefundable maximum under IRC 24(a)/(h)(2), not the refundable portion under 24(h)(5).","Separate statutory citations from forecast drivers so the JSON drivers do not depend on shorthand like OBBBA without defining the law in-source."]}

Emit the final JSON object only.
