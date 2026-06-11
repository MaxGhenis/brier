import type { ForecastCell } from "../forecast-cells";

export const TAX_CREDIT_EXAMPLES = [
  {
    slug: "individual-income-tax-refunds-fy2026",
    type: "data",
    title: "Individual income tax refunds, FY2026",
    question:
      "What will total federal individual income tax refunds be in fiscal year 2026 as reported by the U.S. Treasury?",
    unit: "usd_billions",
    pointEstimate: 486,
    ciLow: 455,
    ciHigh: 525,
    confidence: 0.8,
    resolutionDate: "2026-10-20",
    resolutionSource:
      "U.S. Treasury Monthly Treasury Statement, September 2026",
    resolutionRule:
      "Resolves to total individual income tax refunds for fiscal year 2026 in the final Monthly Treasury Statement for September 2026. If Treasury revises the table after the initial final MTS release, the first final fiscal-year table governs.",
    dataPointId: "treasury.mts.individual_income_tax_refunds.fy2026",
    historicalContext: [
      { label: "FY2021", value: 402 },
      { label: "FY2022", value: 369 },
      { label: "FY2023", value: 458 },
      { label: "FY2024", value: 493 },
      { label: "FY2025e", value: 474 },
    ],
    drivers: [
      "Withholding and estimated-tax overpayment",
      "Refundable tax credit claiming",
      "IRS processing timing",
      "Nominal wage and liability growth",
    ],
    reasoning: [
      { kind: "heading", text: "Near-term cash-flow target" },
      {
        kind: "text",
        text: "Refunds resolve quickly through the Monthly Treasury Statement and give Thesis Institute agents a tax-administration target that connects filing behavior, withholding, and refundable-credit policy.",
      },
      {
        kind: "tool",
        tool: "treasury.lookup",
        call: 'treasury.lookup({ table: "monthly_treasury_statement", series: "individual_income_tax_refunds", fiscal_years: [2021, 2025] })',
        result:
          "{ fy2021: 402, fy2022: 369, fy2023: 458, fy2024: 493, fy2025_estimate: 474 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ year: 2026, output: "individual_income_tax_refunds_cash", timing: "fiscal_year", map_to: "tax_unit" })',
        result:
          '{ point: 482, ci80: [454, 520], drivers: ["ctc_refundability", "eitc_claiming", "withholding_gap"] }',
      },
      {
        kind: "text",
        text: "The central estimate keeps refunds slightly below the FY2024 spike but above FY2025. The interval widens for filing-season timing because a few weeks of delayed refunds can move dollars across fiscal years without changing tax-year liability.",
      },
      { kind: "forecast", point: 486, ciLow: 455, ciHigh: 525 },
    ],
  },

  {
    slug: "net-premium-tax-credit-reconciliation-ty2025",
    type: "data",
    title: "Net PTC reconciliation amount, TY2025",
    question:
      "What will the net premium tax credit reconciliation amount be for tax year 2025 as estimated by IRS Statistics of Income?",
    unit: "usd_billions",
    pointEstimate: 8.6,
    ciLow: 6.4,
    ciHigh: 11.2,
    confidence: 0.8,
    resolutionDate: "2027-08-31",
    resolutionSource:
      "IRS Statistics of Income, Affordable Care Act individual income tax items",
    resolutionRule:
      "Resolves to the IRS SOI tax-year 2025 estimate for net premium tax credit reconciliation on individual income tax returns, defined as additional net PTC claimed minus excess advance PTC repaid. If IRS publishes separate line-item and ACA-statistics estimates, the ACA-statistics table governs.",
    dataPointId: "irs.soi.net_premium_tax_credit_reconciliation.ty2025",
    historicalContext: [
      { label: "TY2021", value: 5.0 },
      { label: "TY2022", value: 6.8 },
      { label: "TY2023", value: 7.4 },
      { label: "TY2024e", value: 8.0 },
    ],
    drivers: [
      "Marketplace enrollment with advance PTC",
      "Income volatility among subsidized households",
      "Enhanced PTC schedule",
      "Reconciliation repayment limits",
    ],
    reasoning: [
      { kind: "heading", text: "Reconciliation target" },
      {
        kind: "text",
        text: "This cell isolates a tax-return outcome that health coverage models often miss: how much advance subsidy remains after households reconcile actual income on their returns.",
      },
      {
        kind: "tool",
        tool: "irs.soi.lookup",
        call: 'irs.soi.lookup({ table: "aca_individual_items", series: "net_ptc_reconciliation", tax_years: [2021, 2024] })',
        result:
          "{ ty2021: 5.0, ty2022: 6.8, ty2023: 7.4, ty2024_estimate: 8.0 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "aca_ptc", year: 2025, output: "net_ptc_reconciliation", map_to: "tax_unit", income_volatility: "central" })',
        result:
          '{ point: 8.4, ci80: [6.2, 10.9], drivers: ["marketplace_growth", "income_reconciliation", "repayment_caps"] }',
      },
      {
        kind: "text",
        text: "The enhanced PTC schedule keeps enrollment high, but reconciliation depends on income surprises. The forecast centers near the model estimate and adds right-tail risk for larger-than-expected income gains among subsidized households.",
      },
      { kind: "forecast", point: 8.6, ciLow: 6.4, ciHigh: 11.2 },
    ],
  },

  {
    slug: "savers-credit-claimant-returns-ty2025",
    type: "data",
    title: "Saver's Credit claimant returns, TY2025",
    question:
      "How many individual income tax returns will claim the Saver's Credit for tax year 2025 in IRS Statistics of Income data?",
    unit: "millions",
    pointEstimate: 5.9,
    ciLow: 5.3,
    ciHigh: 6.6,
    confidence: 0.8,
    resolutionDate: "2027-08-31",
    resolutionSource:
      "IRS Statistics of Income, Individual Income Tax Returns line-item estimates",
    resolutionRule:
      "Resolves to the IRS SOI tax-year 2025 estimate of the number of returns claiming the Retirement Savings Contributions Credit. If IRS reports both preliminary and complete-report values, the complete-report line-item estimate governs.",
    dataPointId: "irs.soi.savers_credit_claimant_returns.ty2025",
    historicalContext: [
      { label: "TY2020", value: 6.1 },
      { label: "TY2021", value: 5.8 },
      { label: "TY2022", value: 5.6 },
      { label: "TY2023", value: 5.7 },
      { label: "TY2024e", value: 5.8 },
    ],
    drivers: [
      "Low- and moderate-income retirement contributions",
      "Earnings growth and eligibility thresholds",
      "Tax software prompting",
      "Refund size salience",
    ],
    reasoning: [
      { kind: "heading", text: "Claiming behavior target" },
      {
        kind: "text",
        text: "The Saver's Credit is small in budget terms but useful for testing whether agents can forecast tax-credit take-up rather than only statutory eligibility.",
      },
      {
        kind: "tool",
        tool: "irs.soi.lookup",
        call: 'irs.soi.lookup({ table: "line_item_estimates", line: "retirement_savings_contributions_credit", metric: "claimant_returns", tax_years: [2020, 2024] })',
        result:
          "{ ty2020: 6.1, ty2021: 5.8, ty2022: 5.6, ty2023: 5.7, ty2024_estimate: 5.8 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ year: 2025, output: "savers_credit_claimant_returns", map_to: "tax_unit", takeup: "observed_credit_claiming" })',
        result:
          '{ point: 5.9, ci80: [5.3, 6.5], drivers: ["eligible_contributors", "tax_software_take_up", "income_thresholds"] }',
      },
      {
        kind: "text",
        text: "The forecast expects mild growth as real earnings stabilize and contribution rates recover, but it keeps the lower tail near the recent trough because the credit remains nonrefundable and low-salience.",
      },
      { kind: "forecast", point: 5.9, ciLow: 5.3, ciHigh: 6.6 },
    ],
  },
] satisfies ForecastCell[];
