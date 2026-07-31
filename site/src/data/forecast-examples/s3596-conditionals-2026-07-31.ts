import type { ForecastCell } from "../forecast-cells";

// S.3596 conditional wave — 2026-07-31 hackathon. Claimed tier; runner-generated
// (gpt-5.6-sol, full prompt mode, run artifacts under thesis-wave-0731/s3596 on
// the operator machine). Condition drafted by the runner itself after refusing a
// non-mechanical phrasing; two sibling runs refused on resolution-date grounds
// and are documented in issue #91.
export const S3596_CONDITIONALS_2026_07_31: ForecastCell[] = [
{
  "slug": "irs-actc-total-claims-ty2027-threshold-one-dollar",
  "country": "US",
  "type": "conditional",
  "title": "ACTC claimant returns, TY2027, $1 threshold",
  "question": "Conditional on legislation enacted by 2027-12-31 making the IRC §24(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027, how many U.S. individual income tax returns will claim the refundable child tax credit or Additional Child Tax Credit for tax year 2027 in the first IRS Statistics of Income Complete Report table 3.3, without seasonal adjustment?",
  "unit": "millions",
  "pointEstimate": 19.0,
  "ciLow": 16.4,
  "ciHigh": 21.6,
  "confidence": 0.8,
  "resolutionDate": "2029-12-31",
  "resolutionSource": "IRS Statistics of Income Individual Income Tax Returns Complete Report, table 3.3",
  "resolutionSourceUrl": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3",
  "resolutionRule": "First evaluate the condition at the end of 2027-12-31: qualifying legislation must have been enacted and must make the IRC §24(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027. If that condition fails, mark the forecast unresolved. If it holds, resolve to the first IRS Statistics of Income Individual Income Tax Returns Complete Report table 3.3 for tax year 2027, row 'All returns, total', number of returns for 'Refundable child tax credit or additional child tax credit', divided by 1,000,000 and rounded to 0.1 million. Use that first SOI estimate only and ignore later revisions. The canonical ledger deadline is retained; IRS had not posted an exact TY2027 Complete Report release date at run time.",
  "dataPointId": "irs.soi.additional_child_tax_credit_returns.ty2027.conditional_threshold_1",
  "conditionalOn": "Legislation enacted by 2027-12-31 makes the IRC §24(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027; condition fails means unresolved.",
  "historicalContext": [
    {
      "label": "TY2019 ACTC claimant returns, millions",
      "value": 19.65807
    },
    {
      "label": "TY2020 ACTC claimant returns, millions",
      "value": 18.84684
    },
    {
      "label": "TY2021 refundable CTC/ACTC claimant returns under ARPA, millions",
      "value": 37.48751
    },
    {
      "label": "TY2022 ACTC claimant returns, millions",
      "value": 17.69145
    },
    {
      "label": "TY2023 refundable CTC/ACTC claimant returns, millions",
      "value": 17.626084
    }
  ],
  "drivers": [
    "Last-print persistence at 17.6 million",
    "Near-zero earned-income threshold adds very-low-earnings claimants",
    "PolicyEngine finds a broad but modest-dollar affected population",
    "Filing take-up limits conversion of eligibility into claims",
    "2021 is an upper-tail precedent with several additional expansions"
  ],
  "sourceContext": [
    "https://www.irs.gov/pub/irs-soi/19in55cmcsv.csv",
    "https://www.irs.gov/pub/irs-soi/20in55cmcsv.csv",
    "https://www.irs.gov/pub/irs-soi/21in55cmcsv.csv",
    "https://www.irs.gov/pub/irs-soi/22in55cmcsv.csv",
    "https://www.irs.gov/pub/irs-soi/23in33ar.xls",
    "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3",
    "https://www.irs.gov/statistics/soi-tax-stats-upcoming-data-releases",
    "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title26-section24&num=0&edition=prelim",
    "https://api.policyengine.org/us/policy/2",
    "https://www.policyengine.org/us/research/stronger-start-working-families-act",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-07-31T20:39:39Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "TY2027 ACTC claims conditional on a near-zero earnings threshold"
    },
    {
      "kind": "text",
      "text": "Framing: the target is the first IRS SOI Complete Report table 3.3 count of tax-year 2027 returns with refundable child tax credit or ACTC, in millions, conditional on enacted law setting the IRC §24(d)(1)(B)(i) earned-income threshold at no more than $1 by 2027-12-31. The count is not seasonally adjusted. A local canonical registration for this new series was not present; the closest public ledger target uses millions and the first SOI table, so those bindings are preserved in substance. IRS had not scheduled the TY2027 report at run time, so the canonical 2029-12-31 deadline is retained rather than represented as an agency-scheduled day."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Fetch IRS Historic Table 2 CSV files for tax years 2019-2022 and read US, AGI_STUB=0, field N11070.",
      "result": "Official IRS CSV values fetched this run: TY2019 19,658,070; TY2020 18,846,840; TY2021 37,487,510; TY2022 17,691,450 returns with additional child tax credit."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Fetch IRS TY2023 Complete Report table 3.3 XLS and inspect the All returns, total row.",
      "result": "Official IRS TY2023 table 3.3 fetched this run: All returns total 160,602,107; refundable child tax credit or additional child tax credit number of returns 17,626,084; refundable portion number of returns 16,638,574; used to offset other taxes number of returns 1,509,231."
    },
    {
      "kind": "tool",
      "tool": "law.lookup",
      "call": "Fetch current 26 U.S.C. §24 from the Office of the Law Revision Counsel.",
      "result": "Fetched statutory text this run: §24(d)(1)(B)(i) specifies 15 percent of earned income exceeding $3,000, while §24(h)(6) substitutes $2,500 for $3,000. The conditional threshold of no more than $1 therefore changes the phase-in base by at least $2,499 relative to the fetched current-law substitution."
    },
    {
      "kind": "tool",
      "tool": "policyengine.lookup",
      "call": "Fetch PolicyEngine current-law policy metadata and its published threshold-elimination analysis.",
      "result": "PolicyEngine API policy 2 returned current law, API version 0.654.1. PolicyEngine's January 2026 threshold-elimination analysis reports a $2,500 baseline threshold, a 15% phase-in rate, a maximum $375 household gain, $1.6 billion static 2026 cost, $14.6 billion 2026-2035 cost, and 5.9% of Americans benefiting."
    },
    {
      "kind": "tool",
      "tool": "model.candidates",
      "call": "Run thesis_model_candidate_v1 persistence and statsmodels local-level candidates on TY2019-TY2023 official history.",
      "result": "Persistence candidate: point 17.6, p10/p50/p90 3.5/17.6/30.7, 80% interval 3.5-30.7, 90% interval 0.7-33.5, residual-quantile method, calibration_n 4, train cutoff 2023, walk-forward MAE 9.8283315. Statsmodels local-level with drift: point 17.2, p10/p50/p90 -2.9/17.2/37.3, 80% interval -2.9-37.3, 90% interval -8.6-43.0, native state-space method, calibration_n 4, walk-forward MAE 19.476401358540063 and 80% coverage 0.5."
    },
    {
      "kind": "tool",
      "tool": "calendar.lookup",
      "call": "Fetch the IRS SOI upcoming data releases page and check the Thesis specs slug endpoint.",
      "result": "The IRS page fetched with 123,232 bytes but contained no exact TY2027 Complete Report release date. The required https://app.thesisinstitute.org/specs.json slug check returned HTTP 404 with an 11,289-byte response, so uniqueness could not be confirmed remotely; the proposed slug was also absent from the local public catalog."
    },
    {
      "kind": "text",
      "text": "Base-rate/reference-class: excluding TY2021 because ARPA simultaneously made the credit fully refundable, raised credit amounts, expanded child age eligibility, and prepaid part of the credit, the four comparable official prints are 19.658070, 18.846840, 17.691450, and 17.626084 million. Their mean is 18.455611 million, sample standard deviation 0.978268 million, and range 17.626084-19.658070 million. The last-print persistence benchmark is 17.626084 million. The corresponding comparable changes are -0.811230, -1.155390, and -0.065366 million."
    },
    {
      "kind": "text",
      "text": "Candidate selection and update test: persistence beats the local-level candidate in the all-history walk-forward comparison, but both candidate intervals are distorted by the one-year ARPA regime. I select the 17.6 million persistence point as the unconditional benchmark and override only its interval. The direct current signal is the stipulated threshold change, supported by PolicyEngine's modeled 5.9% affected-population share and $1.6 billion annual static cost. It is not priced into the post-2021 history because those years retained the $2,500 threshold."
    },
    {
      "kind": "math",
      "text": "Point: persistence 17.626084 million + policy increment 1.4 million = 19.026084 million, rounded to 19.0. The 1.4 million increment is a deliberately shrunken 7.5% of the fetched 19.031899 million gap between the TY2021 count (37.487510) and the 18.455611 million comparable-year mean: 0.075 × 19.031899 = 1.427392 million. This uses TY2021 only as an upper-bound mechanism precedent because threshold elimination was one of several ARPA changes. Interval: comparable-print 80% half-width = 1.28 × 0.978268 = 1.252183 million. Add a full 1.4 million policy-effect error allowance for take-up and low-earnings composition: 1.252183 + 1.4 = 2.652183 million. Thus 19.0 ± 2.652183 gives 16.347817-21.652183, rounded inward to the registered 0.1-million precision as 16.4-21.6. Three of four comparable non-ARPA prints fall inside an interval of this width around their mean; the missed print is only 0.003 million above the analogous upper edge."
    },
    {
      "kind": "text",
      "text": "Prior/update/interval: prior = selected 17.6 million last-print persistence candidate using official TY2019-TY2023 history; benchmark = 17.626084 million; adjustment components = +1.4 million for the stipulated near-zero earnings threshold and +0.0 for unsupported demographic or behavioral narratives; interval method = comparable-current-law sample standard deviation scaled by 1.28 plus a full policy-effect error allowance; implied 80% bounds = 16.4-21.6 million."
    },
    {
      "kind": "text",
      "text": "Counter-consideration and tails: below 16.4 million if eligible-child counts or filing take-up fall enough that threshold expansion fails to offset the recent downward claimant trend; above 21.6 million if legislation pairs the $1 threshold with broader refundability, age, or per-child changes, or outreach converts substantially more newly eligible very-low-earnings families into filers. A repeat of the broader TY2021 regime would be far above the upper bound, which is why TY2021 is not treated as a comparable persistence print."
    },
    {
      "kind": "forecast",
      "point": 19.0,
      "ciLow": 16.4,
      "ciHigh": 21.6
    }
  ]
},
{
  "slug": "irs-actc-total-claims-ty2027-threshold-2500",
  "country": "US",
  "type": "conditional",
  "title": "ACTC claimant returns, TY2027, current-law threshold",
  "question": "Conditional on no legislation enacted by 2027-12-31 changing the IRC §24(d)(1)(B)(i) earned-income threshold of $2,500 for tax year 2027, how many U.S. individual income tax returns will claim the refundable child tax credit or Additional Child Tax Credit for tax year 2027 in the first IRS Statistics of Income Individual Income Tax Returns Complete Report table 3.3, without seasonal adjustment?",
  "unit": "millions",
  "pointEstimate": 17.6,
  "ciLow": 16.4,
  "ciHigh": 18.9,
  "confidence": 0.8,
  "resolutionDate": "2029-12-31",
  "resolutionSource": "IRS Statistics of Income Individual Income Tax Returns Complete Report, table 3.3",
  "resolutionSourceUrl": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3",
  "resolutionRule": "First evaluate the condition at the end of 2027-12-31: no legislation enacted by then may change the IRC §24(d)(1)(B)(i) earned-income threshold of $2,500 for tax year 2027. If the condition fails, mark the forecast unresolved. If it holds, resolve to the first IRS Statistics of Income Individual Income Tax Returns Complete Report table 3.3 for tax year 2027, row 'All returns, total', number of returns for 'Refundable child tax credit or additional child tax credit', divided by 1,000,000 and rounded to 0.1 million. Use that first SOI estimate only and ignore later revisions. The canonical ledger deadline is retained; IRS had not posted an exact TY2027 Complete Report release date at run time.",
  "dataPointId": "irs.soi.additional_child_tax_credit_returns.ty2027.conditional_threshold_2500",
  "conditionalOn": "No legislation enacted by 2027-12-31 changes the IRC §24(d)(1)(B)(i) earned-income threshold of $2,500 for tax year 2027; condition fails means unresolved.",
  "historicalContext": [
    {
      "label": "TY2019 ACTC claimant returns, millions",
      "value": 19.65807
    },
    {
      "label": "TY2020 ACTC claimant returns, millions",
      "value": 18.84684
    },
    {
      "label": "TY2021 refundable CTC/ACTC claimant returns under ARPA, millions",
      "value": 37.48751
    },
    {
      "label": "TY2022 ACTC claimant returns, millions",
      "value": 17.69145
    },
    {
      "label": "TY2023 refundable CTC/ACTC claimant returns, millions",
      "value": 17.626084
    }
  ],
  "drivers": [
    "Last-print persistence at 17.6 million",
    "Current-law $2,500 earned-income threshold",
    "Recent non-ARPA claimant-count dispersion",
    "Eligible-child population and filing take-up",
    "Broader refundability changes are an upper-tail risk"
  ],
  "sourceContext": [
    "https://www.irs.gov/pub/irs-soi/19in55cmcsv.csv",
    "https://www.irs.gov/pub/irs-soi/20in55cmcsv.csv",
    "https://www.irs.gov/pub/irs-soi/21in55cmcsv.csv",
    "https://www.irs.gov/pub/irs-soi/22in55cmcsv.csv",
    "https://www.irs.gov/pub/irs-soi/23in33ar.xls",
    "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3",
    "https://www.irs.gov/statistics/soi-tax-stats-upcoming-data-releases",
    "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title26-section24&num=0&edition=prelim",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-07-31T20:46:04Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "TY2027 ACTC claims conditional on the current-law earnings threshold"
    },
    {
      "kind": "text",
      "text": "Framing: the target is the first IRS SOI Complete Report table 3.3 count of tax-year 2027 returns with refundable child tax credit or ACTC, in millions and not seasonally adjusted, conditional on the $2,500 earned-income threshold remaining unchanged through 2027-12-31. The repository did not expose a committed registration for this exact arm; I retained the supplied target identity and the public sibling target's IRS table, millions unit, first-print rule, and canonical 2029-12-31 deadline. IRS had not scheduled the TY2027 report at run time."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Fetch IRS Historic Table 2 CSV files for tax years 2019-2022 and read US, AGI_STUB=0, field N11070.",
      "result": "Official IRS CSV values fetched this run: TY2019 19,658,070; TY2020 18,846,840; TY2021 37,487,510; TY2022 17,691,450 returns with additional child tax credit."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Fetch IRS TY2023 Complete Report table 3.3 XLS and inspect the All returns, total row and refundable-child-credit columns.",
      "result": "Official IRS TY2023 table 3.3 fetched this run: All returns total 160,602,107; total refundable child tax credit or additional child tax credit number of returns 17,626,084; refundable portion number of returns 16,638,574; used to offset other taxes number of returns 1,509,231."
    },
    {
      "kind": "tool",
      "tool": "law.lookup",
      "call": "Fetch current 26 U.S.C. §24 from the Office of the Law Revision Counsel.",
      "result": "Fetched statutory text this run: §24(d)(1)(B)(i) specifies a 15 percent phase-in for earned income exceeding $3,000, and §24(h)(6) substitutes $2,500 for $3,000. The forecast condition holds only if enacted legislation does not change that $2,500 threshold for tax year 2027 by 2027-12-31."
    },
    {
      "kind": "tool",
      "tool": "model.candidates",
      "call": "Construct thesis_model_candidate_v1 persistence candidate from the four comparable official non-ARPA prints, with fallback-prior intervals from their sample dispersion.",
      "result": "Persistence candidate: point/p50 17.626084 million; p10 16.373901; p90 18.878267; 80% interval 16.373901-18.878267; 90% interval 16.016833-19.235335; interval method fallback-prior sample standard deviation; calibration_n 4; train cutoff TY2023; walk-forward MAE 0.677329 million across 3 comparable transitions. Rounded benchmark point is 17.6 million."
    },
    {
      "kind": "tool",
      "tool": "calendar.lookup",
      "call": "Fetch the IRS SOI upcoming-data-releases page and check the required Thesis specs endpoint for slug uniqueness.",
      "result": "The IRS upcoming-releases page fetched with 123,232 bytes but listed no exact TY2027 Individual Income Tax Returns Complete Report release date. The required Thesis specs URL returned HTTP 404 with an 11,289-byte response; the proposed slug was absent from the local public catalog, but remote uniqueness could not be confirmed."
    },
    {
      "kind": "text",
      "text": "Base-rate/reference-class: excluding TY2021 because ARPA changed refundability, credit amounts, child-age eligibility, and payment timing together, the four comparable official prints are 19.658070, 18.846840, 17.691450, and 17.626084 million. Their mean is 18.455611 million, sample standard deviation 0.978268 million, and range 17.626084-19.658070 million. The last-print persistence benchmark is 17.626084 million; comparable changes are -0.811230, -1.155390, and -0.065366 million, with mean absolute change 0.677329 million."
    },
    {
      "kind": "text",
      "text": "Candidate selection and update test: persistence is selected because this is a sparse annual series with a clear TY2021 regime break, and no fetched current evidence supports moving materially from the latest comparable print. The condition itself preserves the current-law $2,500 threshold, so its policy adjustment is zero rather than an extra effect. TY2021 is retained only as a structural upper-tail precedent, not as a comparable baseline observation."
    },
    {
      "kind": "math",
      "text": "Point = selected persistence candidate 17.626084 + current-law threshold adjustment 0.000000 = 17.626084 million, rounded to 17.6. Comparable-print sample standard deviation is 0.978268 million; normal 80% half-width = 1.28 × 0.978268 = 1.252183 million. Centered on persistence, implied bounds are 17.626084 ± 1.252183 = 16.373901 to 18.878267 million, rounded to agency-aligned 0.1-million precision as 16.4 to 18.9. Three of the four comparable prints fall within an analogous band around their mean; the oldest print misses the upper edge by only about 0.003 million."
    },
    {
      "kind": "text",
      "text": "Prior/update/interval: prior = selected 17.626084 million last-print persistence candidate using official TY2019-TY2023 history with TY2021 excluded from comparable dispersion; benchmark = 17.626084 million; adjustment components = +0.0 million for unchanged threshold, +0.0 for unsupported demographic or take-up narratives; interval method = comparable-current-law sample standard deviation multiplied by 1.28; implied 80% bounds = 16.4-18.9 million."
    },
    {
      "kind": "text",
      "text": "Counter-consideration and tails: below 16.4 million if eligible-child counts, low-income employment, or filing take-up fall enough to extend the recent decline; above 18.9 million if claimant take-up or the eligible-child population rebounds sharply without a statutory threshold change. A broader enacted refundability or credit expansion would instead make this conditional unresolved; if such a change escaped the condition's wording, the TY2021 precedent shows the outcome could lie far above the interval."
    },
    {
      "kind": "forecast",
      "point": 17.6,
      "ciLow": 16.4,
      "ciHigh": 18.9
    }
  ]
}
];
