# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.pusf.j5ii.public_sector_net_borrowing_ex_banks
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-pusf-j5ii-public-sector-net-borrowing-ex-banks-june-2026"
- country: "UK"
- targetUnit: "gbp_billions"
- dataPointId: "ons.pusf.j5ii.public_sector_net_borrowing_ex_banks.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-23", "start": "2026-07-15"}, "field": "official_release:ons:public_sector_finances:2026-05:j5ii", "releasePolicy": "first_print", "sourceSeriesId": "ons.pusf.j5ii", "sourceUrl": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026", "table": "Public sector finances, UK: May 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-d5d0a8776dcdb7739f0aa1d0a24ecbdecf6cbbe3593a2c616a571c1f091ec4e8.json"
- targetContentHash: "d5d0a8776dcdb7739f0aa1d0a24ecbdecf6cbbe3593a2c616a571c1f091ec4e8"
- registeredAtUtc: "2026-07-10T05:58:27Z"
# Rubric
Check these items and name concrete fixes when needed:
1. Exact resolver, source, first-print rule, and resolution date.
2. Base-rate or persistence prior stated before inside-view updates.
3. Time-series/model prior used or explicitly ruled out.
4. Current evidence justifies material movement from the prior.
5. Interval size comes from realized volatility or explicit uncertainty.
6. A compact Prior/update/interval step names the prior, historical sample, adjustment components, interval method, and implied bounds.
7. Tail scenarios are concrete and tied to the target.
8. Point, interval, final forecast step, and JSON fields are coherent.
9. No leakage, catalog point/interval circularity, subjective resolver, or unit ambiguity.

# Required response
Return JSON only, with this shape:
{
  "summary": "one sentence",
  "requiredFixes": [
    {
      "rubricItem": "resolver|base_rate|model_prior|update|interval|prior_update_interval|tails|coherence|leakage",
      "severity": "warning|blocking",
      "summary": "specific issue",
      "actionRequested": "specific change requested"
    }
  ],
  "optionalSuggestions": ["short suggestions"]
}

# Original forecaster prompt hash material
e9ed38f879d678b1bc6d6290a732b6ea51701865ad0ee3cfa0d717201a0beba9

# Draft forecast response
{"slug":"ons-pusf-j5ii-public-sector-net-borrowing-ex-banks-june-2026","country":"UK","type":"data","title":"UK PSNB ex Banks, June 2026","question":"ONS Public sector finances series J5II / bulletin -J5II, public sector net borrowing excluding public sector banks, June 2026, current-price not seasonally adjusted, first print","unit":"gbp_billions","pointEstimate":24.8,"ciLow":13.8,"ciHigh":35.8,"confidence":0.8,"resolutionDate":"2026-07-21","resolutionSource":"Office for National Statistics Public sector finances, UK","resolutionSourceUrl":"https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026","resolutionRule":"Resolve on the first ONS print for June 2026 public sector net borrowing excluding public sector banks. Use the Public sector finances June 2026 bulletin/table value for code -J5II, or equivalently convert raw J5II time-series £m to £ billions with the bulletin borrowing sign convention, where positive means borrowing/deficit. Do not use later revisions, superseded versions, or same-day corrections unless the first-print bulletin itself is replaced before release publication is complete.","dataPointId":"ons.pusf.j5ii.public_sector_net_borrowing_ex_banks.june_2026.first_print","historicalContext":[{"label":"latest_may_2026_bulletin_borrowing","value":23.3},{"label":"april_2026_j5ii_converted","value":23.033},{"label":"june_2025_first_print_borrowing","value":20.7},{"label":"june_2024_first_print_borrowing","value":14.1},{"label":"june_2023_current_timeseries_converted","value":19.085}],"drivers":["May 2026 borrowing was already elevated at GBP 23.3bn versus an OBR forecast of GBP 17.7bn","Financial year to May 2026 borrowing was GBP 46.3bn, GBP 7.7bn above OBR forecast","June is exposed to volatile index-linked gilt debt-interest accruals","Recent June reference class has shifted higher than the pre-pandemic norm","Receipts growth partly offsets higher debt interest, benefits, and departmental spending"],"sourceContext":["https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/j5ii/pusf","https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026","https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/june2025","https://obr.uk/efo/economic-and-fiscal-outlook-march-2026/"],"runAt":"2026-07-10T06:04:37Z","reasoning":[{"kind":"heading","text":"June 2026 UK Public Sector Net Borrowing Forecast"},{"kind":"text","text":"Framing and exact resolver: the target is ONS public sector net borrowing excluding public sector banks for June 2026, first print, in GBP billions. The ONS time-series page is J5II in GBP millions with the raw accounting sign, while bulletin charts/tables use -J5II so positive numbers indicate a deficit; I forecast the registered borrowing concept in the bulletin convention, positive = borrowing. The ledger URL points to the May 2026 bulletin even though the target month is June 2026; I keep that registered URL, and use its official next-release statement plus the J5II series page to tie the target to the 21 July 2026 first print."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS J5II time-series page for PUSF and read metadata and latest values.","result":"Fetched: release date 19 June 2026, next release 21 July 2026, Series ID J5II, units GBP m, 2026 APR raw J5II -23033 and 2026 MAY raw J5II -23294, which convert to GBP 23.033bn and GBP 23.294bn borrowing under the bulletin -J5II convention."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Public sector finances, UK: May 2026 bulletin for current-release drivers and forecast comparison.","result":"Fetched: May 2026 borrowing was GBP 23.3bn, GBP 5.4bn more than May 2025 and GBP 5.6bn above the OBR forecast of GBP 17.7bn; central government debt interest payable was GBP 11.7bn; financial-year-to-May borrowing was GBP 46.3bn versus OBR forecast GBP 38.6bn."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Public sector finances, UK: June 2025 bulletin for the prior same-month first-print and debt-interest mechanics.","result":"Fetched: June 2025 borrowing was GBP 20.7bn, GBP 6.6bn more than June 2024 and GBP 3.5bn above the OBR forecast of GBP 17.1bn; June 2025 central government debt interest was GBP 16.4bn; capital uplift was GBP 10.9bn reflecting a 1.7% RPI rise between March and April 2025."},{"kind":"tool","tool":"official.lookup","call":"Read ONS J5II monthly history for June reference class and converted raw J5II signs to positive borrowing.","result":"Fetched June converted values, GBP bn: 2013 8.310, 2014 7.930, 2015 7.705, 2016 4.876, 2017 6.458, 2018 4.103, 2019 6.791, 2020 32.165, 2021 18.721, 2022 18.871, 2023 19.085, 2024 14.617, 2025 23.878."},{"kind":"text","text":"The reference class base rate is same-month June borrowing. The full 2013-2025 June sample averages about GBP 13.35bn, but the post-2021 regime averages about GBP 19.0bn and the 2025 first print was GBP 20.7bn. Because May 2026 is already GBP 5.6bn above the OBR monthly profile and FY-to-May is GBP 7.7bn above profile, I weight the recent June regime and current-year miss more heavily than the long pre-pandemic base rate."},{"kind":"math","text":"Prior/update/interval: persistence prior = June 2025 first print GBP 20.7bn and 2021-2025 June reference-class mean about GBP 19.0bn; adjustments = +GBP 3.0bn for the current FY-to-May overshoot and higher May run rate, +GBP 1.1bn for June debt-interest and spending risk after May debt interest of GBP 11.7bn, giving point GBP 24.8bn. Interval method uses the 2013-2025 June converted values themselves because this is a monthly flow series: sample sigma = 8.6, so 80% half-width is about 1.28*sigma = 1.28*8.6 = 11.0. Final implied bounds are 24.8 - 11.0 = 13.8 and 24.8 + 11.0 = 35.8."},{"kind":"text","text":"Counter-considerations: upside risk would come from another large index-linked gilt capital-uplift month, weaker PAYE/VAT/corporation tax receipts, or local-government/public-corporation estimates adding to central-government borrowing; a repeat of June 2020-style stress would land above the interval. Downside risk would come from a sharp fall in RPI-linked debt interest, stronger accrued receipts, or unusually low net investment; a clean reversal toward the 2016-2019 June range would land below the interval."},{"kind":"forecast","point":24.8,"ciLow":13.8,"ciHigh":35.8}]}
