import type { CountryCode, ResolutionPolicy, Unit } from "./forecast-cells";
import { GENERATED_FORECAST_TARGETS } from "./ledger-targets.generated";

export interface TargetRegisteredLedgerEntry {
  kind: "target_registered";
  dataPointId: string;
  observationId: string;
  country: CountryCode;
  periodLabel: string;
  unit: Unit;
  resolutionDate: string;
  resolutionSource: string;
  resolutionSourceUrl?: string;
  resolutionRule: string;
  resolutionPolicy: ResolutionPolicy;
  sourceKind: "official_release";
  source: string;
  sourceUrl?: string;
  note: string;
}

const OEWS_SOURCE =
  "U.S. Bureau of Labor Statistics, Occupational Employment and Wage Statistics";
const OEWS_TABLES_URL = "https://www.bls.gov/oes/tables.htm";
const BLS_EMPLOYMENT_PROJECTIONS_SOURCE =
  "U.S. Bureau of Labor Statistics, Employment Projections";
const BLS_EMPLOYMENT_PROJECTIONS_TABLE_URL =
  "https://www.bls.gov/emp/tables/occupational-projections-and-characteristics.htm";
const BLS_EMPLOYMENT_SITUATION_SOURCE =
  "U.S. Bureau of Labor Statistics, Employment Situation";
const BLS_CPS_A19_URL = "https://www.bls.gov/web/empsit/cpseea19.htm";

function oewsMajorOccupationTarget({
  socCode,
  label,
  note,
}: {
  socCode: string;
  label: string;
  note: string;
}): TargetRegisteredLedgerEntry {
  const dataPointId = `bls.oews.national_occupation_employment.soc_${socCode.replace("-", "_")}.may_2026.first_print`;
  return {
    kind: "target_registered",
    dataPointId,
    observationId: `obs.${dataPointId}`,
    country: "US",
    periodLabel: "May 2026",
    unit: "thousands",
    resolutionDate: "2027-05-14",
    resolutionSource: OEWS_SOURCE,
    resolutionSourceUrl: OEWS_TABLES_URL,
    resolutionRule:
      `Resolves to the first-published national OEWS employment estimate ` +
      `for SOC ${socCode} ${label} in the BLS May 2026 National Occupational ` +
      `Employment and Wage Estimates table, divided by 1,000 and rounded to ` +
      `the nearest thousand workers. Later revisions or table corrections do ` +
      `not change the resolved value unless BLS replaces the first table on ` +
      `the same publication date.`,
    resolutionPolicy: "first_print",
    sourceKind: "official_release",
    source: OEWS_SOURCE,
    sourceUrl: OEWS_TABLES_URL,
    note,
  };
}

function oewsMajorOccupationWageTarget({
  socCode,
  label,
  note,
}: {
  socCode: string;
  label: string;
  note: string;
}): TargetRegisteredLedgerEntry {
  const dataPointId = `bls.oews.national_occupation_median_annual_wage.soc_${socCode.replace("-", "_")}.may_2026.first_print`;
  return {
    kind: "target_registered",
    dataPointId,
    observationId: `obs.${dataPointId}`,
    country: "US",
    periodLabel: "May 2026",
    unit: "usd",
    resolutionDate: "2027-05-14",
    resolutionSource: OEWS_SOURCE,
    resolutionSourceUrl: OEWS_TABLES_URL,
    resolutionRule:
      `Resolves to the first-published national OEWS annual median wage ` +
      `estimate for SOC ${socCode} ${label} in the BLS May 2026 National ` +
      `Occupational Employment and Wage Estimates table, in nominal dollars. ` +
      `This uses the A_MEDIAN/annual median wage field for the national, ` +
      `cross-industry row. Later revisions or table corrections do not change ` +
      `the resolved value unless BLS replaces the first table on the same ` +
      `publication date.`,
    resolutionPolicy: "first_print",
    sourceKind: "official_release",
    source: OEWS_SOURCE,
    sourceUrl: OEWS_TABLES_URL,
    note,
  };
}

export const OEWS_OCCUPATION_EMPLOYMENT_TARGETS = [
  oewsMajorOccupationTarget({
    socCode: "13-0000",
    label: "Business and Financial Operations Occupations",
    note: "White-collar analytical and compliance work; useful for tracking AI-assisted office-task substitution and complementarity.",
  }),
  oewsMajorOccupationTarget({
    socCode: "15-0000",
    label: "Computer and Mathematical Occupations",
    note: "Core software, data, and quantitative occupations; a direct exposure group for generative-AI coding and analysis tools.",
  }),
  oewsMajorOccupationTarget({
    socCode: "31-0000",
    label: "Healthcare Support Occupations",
    note: "Hands-on care and support work; useful as a lower-automation benchmark with strong demographic labor-demand pressure.",
  }),
  oewsMajorOccupationTarget({
    socCode: "43-0000",
    label: "Office and Administrative Support Occupations",
    note: "Routine clerical, back-office, scheduling, and records tasks; one of the cleanest occupation groups for task-automation exposure.",
  }),
  oewsMajorOccupationTarget({
    socCode: "51-0000",
    label: "Production Occupations",
    note: "Factory and production work; connects software automation, robotics, and trade-sensitive manufacturing demand.",
  }),
  oewsMajorOccupationTarget({
    socCode: "53-0000",
    label: "Transportation and Material Moving Occupations",
    note: "Logistics, warehousing, driving, and material movement; relevant for warehouse automation, routing, and autonomy exposure.",
  }),
] satisfies TargetRegisteredLedgerEntry[];

export const OEWS_OCCUPATION_WAGE_TARGETS = [
  oewsMajorOccupationWageTarget({
    socCode: "13-0000",
    label: "Business and Financial Operations Occupations",
    note: "Median annual wage target for white-collar analytical and compliance work exposed to both AI productivity and skill-mix shifts.",
  }),
  oewsMajorOccupationWageTarget({
    socCode: "15-0000",
    label: "Computer and Mathematical Occupations",
    note: "Median annual wage target for software, data, security, and quantitative roles where AI can raise productivity while changing labor demand.",
  }),
  oewsMajorOccupationWageTarget({
    socCode: "31-0000",
    label: "Healthcare Support Occupations",
    note: "Median annual wage target for a low-wage, high-demand care support group with strong staffing pressure and limited physical-task automation.",
  }),
  oewsMajorOccupationWageTarget({
    socCode: "43-0000",
    label: "Office and Administrative Support Occupations",
    note: "Median annual wage target for routine clerical and administrative work, where automation may affect composition as well as employment.",
  }),
  oewsMajorOccupationWageTarget({
    socCode: "51-0000",
    label: "Production Occupations",
    note: "Median annual wage target for production workers, connecting manufacturing labor demand, union/shortage pressure, and process automation.",
  }),
  oewsMajorOccupationWageTarget({
    socCode: "53-0000",
    label: "Transportation and Material Moving Occupations",
    note: "Median annual wage target for logistics, warehousing, driving, and material-moving work affected by routing software and warehouse automation.",
  }),
] satisfies TargetRegisteredLedgerEntry[];

function blsEmploymentProjectionOccupationTarget({
  socCode,
  label,
  note,
}: {
  socCode: string;
  label: string;
  note: string;
}): TargetRegisteredLedgerEntry {
  const dataPointId = `bls.employment_projections.national_occupation_employment.soc_${socCode.replace("-", "_")}.2034.actual_first_print`;
  return {
    kind: "target_registered",
    dataPointId,
    observationId: `obs.${dataPointId}`,
    country: "US",
    periodLabel: "2034 base-year employment",
    unit: "thousands",
    resolutionDate: "2035-09-15",
    resolutionSource: BLS_EMPLOYMENT_PROJECTIONS_SOURCE,
    resolutionSourceUrl: BLS_EMPLOYMENT_PROJECTIONS_TABLE_URL,
    resolutionRule:
      `Resolves to the first BLS Employment Projections/National Employment ` +
      `Matrix table that uses 2034 as the base year, for SOC ${socCode} ` +
      `${label}, measured as employment in thousands. The published 2024-2034 ` +
      `projection is only a comparison forecast; the resolved value is the ` +
      `first official 2034 base-year employment estimate in that later BLS ` +
      `projection vintage or successor table.`,
    resolutionPolicy: "first_print",
    sourceKind: "official_release",
    source: BLS_EMPLOYMENT_PROJECTIONS_SOURCE,
    sourceUrl: BLS_EMPLOYMENT_PROJECTIONS_TABLE_URL,
    note,
  };
}

export const BLS_2034_OCCUPATION_EMPLOYMENT_TARGETS = [
  blsEmploymentProjectionOccupationTarget({
    socCode: "13-0000",
    label: "Business and Financial Operations Occupations",
    note: "Long-run occupation forecast target for comparing Brier automation scenarios against the BLS 2024-2034 baseline on the same resolver.",
  }),
  blsEmploymentProjectionOccupationTarget({
    socCode: "15-0000",
    label: "Computer and Mathematical Occupations",
    note: "Long-run occupation forecast target for software, data, and quantitative work under AI adoption scenarios.",
  }),
  blsEmploymentProjectionOccupationTarget({
    socCode: "31-0000",
    label: "Healthcare Support Occupations",
    note: "Long-run occupation forecast target for a demographically driven, lower-substitution benchmark group.",
  }),
  blsEmploymentProjectionOccupationTarget({
    socCode: "43-0000",
    label: "Office and Administrative Support Occupations",
    note: "Long-run occupation forecast target for the largest routine clerical automation-exposure group.",
  }),
  blsEmploymentProjectionOccupationTarget({
    socCode: "51-0000",
    label: "Production Occupations",
    note: "Long-run occupation forecast target for manufacturing, robotics, and goods-sector automation exposure.",
  }),
  blsEmploymentProjectionOccupationTarget({
    socCode: "53-0000",
    label: "Transportation and Material Moving Occupations",
    note: "Long-run occupation forecast target for logistics, warehouse automation, routing, and autonomy exposure.",
  }),
] satisfies TargetRegisteredLedgerEntry[];

function cpsOccupationEmploymentTarget({
  key,
  label,
  note,
}: {
  key: string;
  label: string;
  note: string;
}): TargetRegisteredLedgerEntry {
  const dataPointId = `bls.cps.employed_people_by_occupation.${key}.june_2026.first_print`;
  return {
    kind: "target_registered",
    dataPointId,
    observationId: `obs.${dataPointId}`,
    country: "US",
    periodLabel: "June 2026 CPS first print",
    unit: "thousands",
    resolutionDate: "2026-07-02",
    resolutionSource: BLS_EMPLOYMENT_SITUATION_SOURCE,
    resolutionSourceUrl: BLS_CPS_A19_URL,
    resolutionRule:
      `Resolves to the first-published June 2026 Employment Situation ` +
      `household-survey Table A-19 count of employed people, not seasonally ` +
      `adjusted, for ${label}, in thousands. Later revisions, database ` +
      `refreshes, or monthly table replacements do not change the resolved ` +
      `value unless BLS replaces the first July 2, 2026 table on the same ` +
      `publication date.`,
    resolutionPolicy: "first_print",
    sourceKind: "official_release",
    source: BLS_EMPLOYMENT_SITUATION_SOURCE,
    sourceUrl: BLS_CPS_A19_URL,
    note,
  };
}

export const CPS_JUNE_2026_OCCUPATION_EMPLOYMENT_TARGETS = [
  cpsOccupationEmploymentTarget({
    key: "business_financial_operations",
    label: "Business and financial operations occupations",
    note: "Fast monthly CPS proxy for the business and financial OEWS/SOC occupation group; noisy but resolves weeks after forecast registration.",
  }),
  cpsOccupationEmploymentTarget({
    key: "computer_mathematical",
    label: "Computer and mathematical occupations",
    note: "Fast monthly CPS proxy for software, data, and quantitative labor demand.",
  }),
  cpsOccupationEmploymentTarget({
    key: "healthcare_support",
    label: "Healthcare support occupations",
    note: "Fast monthly CPS proxy for lower-substitution, care-demand-sensitive occupations.",
  }),
  cpsOccupationEmploymentTarget({
    key: "office_administrative_support",
    label: "Office and administrative support occupations",
    note: "Fast monthly CPS proxy for routine clerical and administrative automation exposure.",
  }),
  cpsOccupationEmploymentTarget({
    key: "production",
    label: "Production occupations",
    note: "Fast monthly CPS proxy for manufacturing and process-automation exposure.",
  }),
  cpsOccupationEmploymentTarget({
    key: "transportation_material_moving",
    label: "Transportation and material moving occupations",
    note: "Fast monthly CPS proxy for logistics, warehouse automation, routing, and autonomy exposure.",
  }),
] satisfies TargetRegisteredLedgerEntry[];

export const THESIS_TARGET_LEDGER = dedupeTargetLedger([
  ...OEWS_OCCUPATION_EMPLOYMENT_TARGETS,
  ...OEWS_OCCUPATION_WAGE_TARGETS,
  ...BLS_2034_OCCUPATION_EMPLOYMENT_TARGETS,
  ...CPS_JUNE_2026_OCCUPATION_EMPLOYMENT_TARGETS,
  ...GENERATED_FORECAST_TARGETS,
]);

function dedupeTargetLedger(
  targets: TargetRegisteredLedgerEntry[],
): TargetRegisteredLedgerEntry[] {
  const seen = new Set<string>();
  return targets.filter((target) => {
    if (seen.has(target.dataPointId)) return false;
    seen.add(target.dataPointId);
    return true;
  });
}

export function getLedgerTargetByDataPointId(
  dataPointId: string,
): TargetRegisteredLedgerEntry | undefined {
  return THESIS_TARGET_LEDGER.find(
    (entry) => entry.dataPointId === dataPointId,
  );
}

export function requireLedgerTarget(
  dataPointId: string,
): TargetRegisteredLedgerEntry {
  const target = getLedgerTargetByDataPointId(dataPointId);
  if (!target) {
    throw new Error(`Missing Thesis target ledger entry for ${dataPointId}`);
  }
  return target;
}
