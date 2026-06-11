import type { ForecastCell } from "../forecast-cells";

export const BENEFIT_PROGRAM_EXAMPLES = [
  {
    slug: "snap-cumulative-benefit-redemptions-fy2026",
    type: "data",
    title: "SNAP cumulative redemptions, FY2026",
    question:
      "What will total SNAP benefit redemptions be in fiscal year 2026 according to USDA Food and Nutrition Service program data?",
    unit: "usd_billions",
    pointEstimate: 111.5,
    ciLow: 103.0,
    ciHigh: 122.0,
    confidence: 0.8,
    resolutionDate: "2027-01-31",
    resolutionSource:
      "USDA Food and Nutrition Service, SNAP national level annual summary",
    resolutionRule:
      "Resolves to the fiscal year 2026 total SNAP benefit redemption amount in USDA FNS national-level annual summary data. If USDA reports issuance and redemption separately, the redemption amount governs.",
    dataPointId: "usda.fns.snap.benefit_redemptions.fy2026",
    historicalContext: [
      { label: "FY2021", value: 112.6 },
      { label: "FY2022", value: 119.4 },
      { label: "FY2023", value: 112.8 },
      { label: "FY2024", value: 100.1 },
      { label: "FY2025e", value: 106.0 },
    ],
    drivers: [
      "Average monthly participation",
      "Thrifty Food Plan indexation",
      "Household income and deductions",
      "Emergency-allotment aftereffects",
    ],
    reasoning: [
      { kind: "heading", text: "Benefits-flow target" },
      {
        kind: "text",
        text: "Redemptions are the administrative spending flow that reaches retailers and households. They give the Almanac a near-term benefits target that can calibrate both eligibility and benefit-formula simulations.",
      },
      {
        kind: "tool",
        tool: "usda.fns.lookup",
        call: 'usda.fns.lookup({ program: "snap", table: "national_level_annual_summary", series: "benefit_redemptions", fiscal_years: [2021, 2025] })',
        result:
          "{ fy2021: 112.6, fy2022: 119.4, fy2023: 112.8, fy2024: 100.1, fy2025_estimate: 106.0 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "snap", fiscal_year: 2026, output: "benefit_redemptions", map_to: "spm_unit", food_plan: "fy2026_indexed" })',
        result:
          '{ point: 110.8, ci80: [102.5, 121.0], drivers: ["caseload", "net_income", "maximum_allotment"] }',
      },
      {
        kind: "text",
        text: "The central path rises from FY2024 after cost-of-food indexation and elevated caseload persistence, but it remains below the pandemic-era peak because emergency allotments have fully expired.",
      },
      { kind: "forecast", point: 111.5, ciLow: 103.0, ciHigh: 122.0 },
    ],
  },

  {
    slug: "wic-child-participation-fy2026",
    type: "data",
    title: "WIC child participation, FY2026",
    question:
      "How many children will participate in WIC on average each month in fiscal year 2026 according to USDA FNS data?",
    unit: "millions",
    pointEstimate: 3.9,
    ciLow: 3.6,
    ciHigh: 4.2,
    confidence: 0.8,
    resolutionDate: "2027-01-31",
    resolutionSource:
      "USDA Food and Nutrition Service, WIC program data by participant category",
    resolutionRule:
      "Resolves to the average monthly number of child participants in WIC during fiscal year 2026 in USDA FNS program data. Infant and pregnant/postpartum/breastfeeding participant categories are excluded.",
    dataPointId: "usda.fns.wic.child_participation.fy2026",
    historicalContext: [
      { label: "FY2020", value: 3.3 },
      { label: "FY2021", value: 3.4 },
      { label: "FY2022", value: 3.6 },
      { label: "FY2023", value: 3.8 },
      { label: "FY2024e", value: 3.9 },
    ],
    drivers: [
      "Child eligibility and certification",
      "State outreach and remote recertification",
      "Food-package attractiveness",
      "Birth cohort size",
    ],
    reasoning: [
      { kind: "heading", text: "Participant-category target" },
      {
        kind: "text",
        text: "Overall WIC participation mixes infants, children, and mothers. Child participation is the sharper target for family-resource forecasting because it connects to toddler nutrition support and certification churn.",
      },
      {
        kind: "tool",
        tool: "usda.fns.lookup",
        call: 'usda.fns.lookup({ program: "wic", series: "average_monthly_child_participants", fiscal_years: [2020, 2024] })',
        result:
          "{ fy2020: 3.3, fy2021: 3.4, fy2022: 3.6, fy2023: 3.8, fy2024_estimate: 3.9 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "wic", fiscal_year: 2026, output: "child_participation", map_to: "person", takeup: "category_specific" })',
        result:
          '{ point: 3.9, ci80: [3.6, 4.2], drivers: ["eligible_children", "certification_retention", "state_outreach"] }',
      },
      {
        kind: "text",
        text: "The forecast keeps participation near the recent elevated level. The upper tail comes from improved retention technology; the lower tail comes from smaller birth cohorts feeding into the child category.",
      },
      { kind: "forecast", point: 3.9, ciLow: 3.6, ciHigh: 4.2 },
    ],
  },

  {
    slug: "ccdf-average-monthly-payment-per-child-fy2026",
    type: "data",
    title: "CCDF payment per child, FY2026",
    question:
      "What will the average monthly CCDF subsidy payment per child served be in fiscal year 2026 according to ACF child care data?",
    unit: "usd_monthly",
    pointEstimate: 690,
    ciLow: 610,
    ciHigh: 800,
    confidence: 0.8,
    resolutionDate: "2027-12-31",
    resolutionSource:
      "HHS Administration for Children and Families, CCDF administrative data",
    resolutionRule:
      "Resolves to average monthly CCDF subsidy payments per child served in fiscal year 2026, computed from ACF CCDF administrative data as total subsidy payments divided by average monthly children served and months. If ACF publishes the metric directly, the direct metric governs.",
    dataPointId: "hhs.acf.ccdf.average_monthly_payment_per_child.fy2026",
    historicalContext: [
      { label: "FY2020", value: 520 },
      { label: "FY2021", value: 560 },
      { label: "FY2022", value: 610 },
      { label: "FY2023", value: 650 },
      { label: "FY2024e", value: 670 },
    ],
    drivers: [
      "Provider reimbursement rates",
      "State copayment policy",
      "Age mix of children served",
      "Child care price growth",
    ],
    reasoning: [
      { kind: "heading", text: "Subsidy-depth target" },
      {
        kind: "text",
        text: "The existing catalog tracks children served and CCDF outlays. Payment per child isolates subsidy depth, which matters for whether a benefit actually buys care at local prices.",
      },
      {
        kind: "tool",
        tool: "acf.lookup",
        call: 'acf.lookup({ program: "ccdf", series: "average_monthly_payment_per_child", fiscal_years: [2020, 2024] })',
        result:
          "{ fy2020: 520, fy2021: 560, fy2022: 610, fy2023: 650, fy2024_estimate: 670 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "ccdf", fiscal_year: 2026, output: "average_monthly_payment_per_child", map_to: "person", provider_rates: "state_weighted" })',
        result:
          '{ point: 685, ci80: [610, 790], drivers: ["state_reimbursement_rates", "infant_toddler_mix", "copayments"] }',
      },
      {
        kind: "text",
        text: "Payment depth keeps rising with provider rates and child care prices, but the interval allows states to ration funds through lower reimbursement growth or narrower eligibility.",
      },
      { kind: "forecast", point: 690, ciLow: 610, ciHigh: 800 },
    ],
  },
] satisfies ForecastCell[];
