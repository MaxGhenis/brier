import type { ForecastCell } from "../forecast-cells";

export const HEALTH_COVERAGE_EXAMPLES = [
  {
    slug: "medicaid-chip-enrollment-dec-2026",
    type: "data",
    title: "Medicaid and CHIP enrollment, Dec 2026",
    question:
      "How many people will be enrolled in Medicaid and CHIP in December 2026 according to CMS monthly enrollment data?",
    unit: "millions",
    pointEstimate: 79.4,
    ciLow: 75.8,
    ciHigh: 83.8,
    confidence: 0.8,
    resolutionDate: "2027-06-30",
    resolutionSource:
      "CMS Medicaid and CHIP monthly enrollment data, December 2026",
    resolutionRule:
      "Resolves to the national Medicaid and CHIP enrollment total for December 2026 in CMS monthly enrollment data. If CMS publishes preliminary and updated files, the first updated national file posted by June 30, 2027 governs.",
    dataPointId: "cms.medicaid_chip.enrollment.dec_2026",
    historicalContext: [
      { label: "Dec 2021", value: 86.7 },
      { label: "Dec 2022", value: 91.3 },
      { label: "Dec 2023", value: 85.9 },
      { label: "Dec 2024", value: 79.7 },
      { label: "Dec 2025e", value: 78.9 },
    ],
    drivers: [
      "Post-unwinding renewal policy",
      "Child and adult eligibility thresholds",
      "Employment and income growth",
      "State ex parte renewal performance",
    ],
    reasoning: [
      { kind: "heading", text: "Coverage calibration target" },
      {
        kind: "text",
        text: "This near-term enrollment cell gives Thesis Institute agents a clean administrative check on Medicaid participation before slower Census health-insurance outcomes resolve.",
      },
      {
        kind: "tool",
        tool: "cms.lookup",
        call: 'cms.lookup({ dataset: "medicaid_chip_monthly_enrollment", measure: "total_enrollment", months: ["2021-12", "2025-12"] })',
        result:
          "{ dec2021: 86.7, dec2022: 91.3, dec2023: 85.9, dec2024: 79.7, dec2025_estimate: 78.9 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ year: 2026, month: "december", output: "medicaid_chip_enrollment", map_to: "person", renewal_policy: "post_unwinding" })',
        result:
          '{ point: 79.1, ci80: [75.7, 83.3], drivers: ["income_eligibility", "state_renewals", "take_up"] }',
      },
      {
        kind: "text",
        text: "The forecast expects the unwinding decline to level off by late 2026. The upper tail reflects states improving renewal automation and the lower tail reflects continued procedural disenrollment.",
      },
      { kind: "forecast", point: 79.4, ciLow: 75.8, ciHigh: 83.8 },
    ],
  },

  {
    slug: "direct-purchase-health-coverage-rate-2025",
    type: "data",
    title: "Direct-purchase health coverage rate, 2025",
    question:
      "What share of people will have direct-purchase health insurance coverage in calendar year 2025 according to the Census health insurance report?",
    unit: "percent",
    pointEstimate: 10.6,
    ciLow: 9.9,
    ciHigh: 11.4,
    confidence: 0.8,
    resolutionDate: "2026-09-15",
    resolutionSource:
      "U.S. Census Bureau, Health Insurance Coverage in the United States: 2025",
    resolutionRule:
      "Resolves to the direct-purchase health insurance coverage rate for all people in the Census health insurance report covering calendar year 2025. The headline direct-purchase category governs, including marketplace and non-marketplace nongroup coverage.",
    dataPointId: "census.asec.direct_purchase_coverage_rate.2025",
    historicalContext: [
      { label: "2020", value: 10.5 },
      { label: "2021", value: 10.2 },
      { label: "2022", value: 10.2 },
      { label: "2023", value: 10.9 },
      { label: "2024e", value: 10.8 },
    ],
    drivers: [
      "Marketplace enrollment growth",
      "Enhanced premium tax credits",
      "Medicaid-to-marketplace transitions",
      "ASEC coverage measurement",
    ],
    reasoning: [
      { kind: "heading", text: "Census coverage target" },
      {
        kind: "text",
        text: "Direct-purchase coverage is the Census-side counterpart to marketplace enrollment. It tests whether agents can reconcile administrative sign-ups with survey-reported insurance categories.",
      },
      {
        kind: "tool",
        tool: "census.lookup",
        call: 'census.lookup({ report: "Health Insurance Coverage in the United States", series: "direct_purchase_coverage_rate", years: [2020, 2024] })',
        result:
          "{ y2020: 10.5, y2021: 10.2, y2022: 10.2, y2023: 10.9, y2024_estimate: 10.8 }",
      },
      {
        kind: "tool",
        tool: "cms.lookup",
        call: 'cms.lookup({ program: "marketplace", measure: "effectuated_enrollment", year: 2025 })',
        result:
          "{ high_marketplace_enrollment: true, offsetting_medicaid_transition: true }",
      },
      {
        kind: "text",
        text: "The forecast holds the rate near 2023-2024 despite strong marketplace sign-ups because Census direct-purchase coverage includes classification noise and because some Medicaid transitions replace, rather than add, covered people.",
      },
      { kind: "forecast", point: 10.6, ciLow: 9.9, ciHigh: 11.4 },
    ],
  },

  {
    slug: "marketplace-new-consumers-oep-2027",
    type: "data",
    title: "Marketplace new consumers, OEP 2027",
    question:
      "How many new consumers will select ACA Marketplace plans during the 2027 open enrollment period according to CMS?",
    unit: "millions",
    pointEstimate: 3.2,
    ciLow: 2.4,
    ciHigh: 4.4,
    confidence: 0.8,
    resolutionDate: "2027-03-31",
    resolutionSource:
      "CMS Marketplace Open Enrollment Period public use files for plan year 2027",
    resolutionRule:
      "Resolves to the CMS national count of new consumers selecting Marketplace plans during the 2027 open enrollment period. If CMS reports HealthCare.gov and state-based marketplace totals separately, the national total combining both governs.",
    dataPointId: "cms.marketplace.new_consumers.oep_2027",
    historicalContext: [
      { label: "OEP 2023", value: 3.6 },
      { label: "OEP 2024", value: 5.2 },
      { label: "OEP 2025", value: 5.6 },
      { label: "OEP 2026e", value: 4.1 },
    ],
    drivers: [
      "Enhanced PTC policy state",
      "Medicaid redetermination spillover",
      "Premium growth",
      "Navigator and broker activity",
    ],
    reasoning: [
      { kind: "heading", text: "New-consumer target" },
      {
        kind: "text",
        text: "Total Marketplace selections mix retention and acquisition. New consumers are the sharper calibration target for coverage-transition models because they reflect households entering or re-entering nongroup coverage.",
      },
      {
        kind: "tool",
        tool: "cms.lookup",
        call: 'cms.lookup({ dataset: "marketplace_oep_public_use_files", measure: "new_consumers", plan_years: [2023, 2026] })',
        result:
          "{ oep2023: 3.6, oep2024: 5.2, oep2025: 5.6, oep2026_estimate: 4.1 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ program: "aca_marketplace", plan_year: 2027, output: "new_consumer_selections", policy: "enhanced_ptc_uncertain" })',
        result:
          '{ point: 3.3, ci80: [2.4, 4.3], drivers: ["subsidy_schedule", "medicaid_churn", "premium_growth"] }',
      },
      {
        kind: "text",
        text: "The central forecast declines from the unwinding-driven surge. It keeps a broad interval because subsidy policy and broker behavior can move new sign-ups quickly.",
      },
      { kind: "forecast", point: 3.2, ciLow: 2.4, ciHigh: 4.4 },
    ],
  },

  {
    slug: "infant-mortality-rate-2026-current-law",
    type: "conditional",
    title: "Infant mortality 2026 | current-law CTC",
    question:
      "Conditional on no materially equivalent $3,000 fully refundable Child Tax Credit being in effect for tax year 2026, what will the U.S. infant mortality rate be for calendar year 2026?",
    unit: "per_1000_live_births",
    pointEstimate: 5.5,
    ciLow: 5.34,
    ciHigh: 5.72,
    confidence: 0.8,
    resolutionDate: "2028-12-15",
    resolutionSource:
      "CDC/NCHS National Vital Statistics System linked birth/infant death records",
    resolutionSourceUrl: "https://www.cdc.gov/nchs/nvss/linked-birth.htm",
    resolutionRule:
      "Resolves to the final U.S. infant mortality rate for calendar year 2026, in infant deaths per 1,000 live births, from CDC/NCHS NVSS linked birth/infant death records, conditional on no materially equivalent $3,000 fully refundable Child Tax Credit being in effect for TY2026. If such a policy is in effect, this baseline scenario is marked unresolved.",
    conditionalOn:
      "No materially equivalent $3,000 fully refundable Child Tax Credit in effect for TY2026",
    dataPointId: "cdc.nchs.nvss.infant_mortality_rate.2026.final",
    policyParameter: "irc.24.current_law.2026",
    historicalContext: [
      { label: "2019", value: 5.58 },
      { label: "2020", value: 5.42 },
      { label: "2021", value: 5.44 },
      { label: "2022", value: 5.6 },
      { label: "2023", value: 5.6 },
      { label: "2024", value: 5.53 },
    ],
    drivers: [
      "Recent NVSS infant mortality plateau",
      "Maternal health and preterm birth trends",
      "Medicaid postpartum coverage and prenatal care access",
      "No large refundable CTC income shock",
    ],
    reasoning: [
      { kind: "heading", text: "Official mortality target" },
      {
        kind: "text",
        text: "This cell targets the final NCHS/NVSS linked birth/infant death rate: deaths under age 1 per 1,000 live births. The baseline scenario is current-law CTC policy, so a $3,000 fully refundable CTC would make this scenario unresolved rather than wrong.",
      },
      {
        kind: "tool",
        tool: "nchs.lookup",
        call: 'nchs.lookup({ dataset: "linked_birth_infant_death", series: "infant_mortality_rate", years: [2019, 2024], unit: "per_1000_live_births" })',
        result:
          "{ y2019: 5.58, y2020: 5.42, y2021: 5.44, y2022: 5.60, y2023: 5.60, y2024: 5.53 }",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ scenario: "current_law_ctc", year: 2026, output: "after_tax_income_for_households_with_infants", map_to: "household" })',
        result:
          '{ median_change_vs_2025: "small", low_income_infant_household_cash_shock: "none", mortality_adjustment_per_1000: 0.00 }',
      },
      {
        kind: "text",
        text: "The recent U.S. series has flattened after the 2022 increase. The forecast modestly improves from 2023-2024 but does not return to the 2020 low because preterm birth and maternal morbidity indicators remain elevated.",
      },
      { kind: "forecast", point: 5.5, ciLow: 5.34, ciHigh: 5.72 },
    ],
  },

  {
    slug: "infant-mortality-rate-2026-ctc-3000-refundable",
    type: "conditional",
    title: "Infant mortality 2026 | $3,000 fully refundable CTC",
    question:
      "Conditional on a $3,000 fully refundable Child Tax Credit being in effect for tax year 2026, what will the U.S. infant mortality rate be for calendar year 2026?",
    unit: "per_1000_live_births",
    pointEstimate: 5.4,
    ciLow: 5.16,
    ciHigh: 5.66,
    confidence: 0.8,
    resolutionDate: "2028-12-15",
    resolutionSource:
      "CDC/NCHS National Vital Statistics System linked birth/infant death records",
    resolutionSourceUrl: "https://www.cdc.gov/nchs/nvss/linked-birth.htm",
    resolutionRule:
      "Resolves to the final U.S. infant mortality rate for calendar year 2026, in infant deaths per 1,000 live births, from CDC/NCHS NVSS linked birth/infant death records, conditional on a materially equivalent $3,000 fully refundable Child Tax Credit being in effect for TY2026. If the policy is not in effect, this scenario is marked unresolved.",
    conditionalOn:
      "$3,000 fully refundable Child Tax Credit in effect for TY2026",
    dataPointId: "cdc.nchs.nvss.infant_mortality_rate.2026.final",
    policyParameter: "irc.24.ctc_3000_fully_refundable.2026",
    historicalContext: [
      { label: "2019", value: 5.58 },
      { label: "2020", value: 5.42 },
      { label: "2021", value: 5.44 },
      { label: "2022", value: 5.6 },
      { label: "2023", value: 5.6 },
      { label: "2024", value: 5.53 },
      { label: "CTC sim", value: 5.4 },
    ],
    drivers: [
      "Refundable CTC cash to infant households",
      "Prenatal stress and material hardship channels",
      "Birthweight and preterm-birth response uncertainty",
      "Take-up among very low-income families",
    ],
    reasoning: [
      { kind: "heading", text: "Policy scenario" },
      {
        kind: "text",
        text: "This scenario asks about the observed national infant mortality rate if the $3,000 fully refundable CTC is actually in force for TY2026. The official NCHS rate still resolves the value; the condition determines whether this scenario is active.",
      },
      {
        kind: "tool",
        call: 'policyengine.simulate({ reform: "ctc_3000_fully_refundable", year: 2026, output: "cash_transfer_to_households_with_infants", map_to: "household" })',
        result:
          '{ low_income_infant_household_mean_gain: 2450, broad_infant_household_mean_gain: 1320, takeup_risk: "moderate" }',
      },
      {
        kind: "tool",
        tool: "evidence.lookup",
        call: 'evidence.lookup({ domain: "cash_transfers_birth_outcomes", policies: ["expanded_ctc", "eitc"], outcomes: ["low_birth_weight", "infant_mortality"] })',
        result:
          '{ birthweight_effect: "small positive", low_birth_weight_effect: "negative", direct_infant_mortality_evidence: "thin", national_imr_effect_per_1000: [-0.20, -0.02] }',
      },
      {
        kind: "math",
        text: "Baseline 5.50 minus central income-support effect 0.10 deaths per 1,000 = 5.40.",
      },
      {
        kind: "text",
        text: "The CTC lowers the central estimate, but the interval overlaps the current-law baseline because the direct causal evidence for national infant mortality is much thinner than the evidence for low birth weight and maternal stress.",
      },
      { kind: "forecast", point: 5.4, ciLow: 5.16, ciHigh: 5.66 },
    ],
  },
] satisfies ForecastCell[];
