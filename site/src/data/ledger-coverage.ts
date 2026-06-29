import type { ForecastCell } from "./forecast-cells";
import type { ObservationRecordedLedgerEntry } from "./thesis-log";

export interface LedgerObservationCoverageRule {
  observationDataPointId: string;
  coveredByForecastDataPointIds: string[];
  reason: string;
}

export const LEDGER_OBSERVATION_COVERAGE_RULES = [
  {
    observationDataPointId:
      "fns.snap.total_payment_error_rate.us.fy2024.official_release",
    coveredByForecastDataPointIds: [
      "fns.snap.total_payment_error_rate.us.fy2026",
    ],
    reason:
      "FY 2024 national total PER is historical context for the national FY 2026 total PER target.",
  },
  {
    observationDataPointId:
      "fns.snap.overpayment_payment_error_rate.us.fy2024.official_release",
    coveredByForecastDataPointIds: [
      "fns.snap.overpayment_payment_error_rate.us.fy2026",
    ],
    reason:
      "FY 2024 national overpayment PER is historical context for the national FY 2026 overpayment target.",
  },
  {
    observationDataPointId:
      "fns.snap.underpayment_payment_error_rate.us.fy2024.official_release",
    coveredByForecastDataPointIds: [
      "fns.snap.underpayment_payment_error_rate.us.fy2026",
    ],
    reason:
      "FY 2024 national underpayment PER is historical context for the national FY 2026 underpayment target.",
  },
  {
    observationDataPointId:
      "fns.snap.application_processing_timeliness.california.fy2024.official_release",
    coveredByForecastDataPointIds: [
      "fns.snap.application_processing_timeliness.ca.fy2025",
    ],
    reason:
      "The ledger records California with a full state name while the forecast target uses the canonical CA jurisdiction code.",
  },
  {
    observationDataPointId:
      "cms.medicaid_pi.beneficiaries_renewed_total.california.feb_2026.original_submission",
    coveredByForecastDataPointIds: [
      "cms.medicaid_pi.ex_parte_renewal_share.ca.aug_2026",
    ],
    reason:
      "Renewed-total counts are denominator inputs for the California ex parte renewal share target.",
  },
  {
    observationDataPointId:
      "cms.medicaid_pi.beneficiaries_renewed_ex_parte.california.feb_2026.original_submission",
    coveredByForecastDataPointIds: [
      "cms.medicaid_pi.ex_parte_renewal_share.ca.aug_2026",
    ],
    reason:
      "Ex parte renewal counts are numerator inputs for the California ex parte renewal share target.",
  },
  {
    observationDataPointId:
      "cms.medicaid_pi.beneficiaries_disenrolled_total.california.feb_2026.original_submission",
    coveredByForecastDataPointIds: [
      "cms.medicaid_pi.procedural_disenrollment_share.california.aug_2026",
      "cms.medicaid_pi.procedural_disenrollment_share.ca.aug_2026.conditional",
    ],
    reason:
      "Disenrolled-total counts are denominator inputs for California procedural disenrollment share targets.",
  },
  {
    observationDataPointId:
      "cms.medicaid_pi.beneficiaries_disenrolled_procedural.california.feb_2026.original_submission",
    coveredByForecastDataPointIds: [
      "cms.medicaid_pi.procedural_disenrollment_share.california.aug_2026",
      "cms.medicaid_pi.procedural_disenrollment_share.ca.aug_2026.conditional",
    ],
    reason:
      "Procedural disenrollment counts are numerator inputs for California procedural disenrollment share targets.",
  },
] satisfies LedgerObservationCoverageRule[];

export function findUncoveredLedgerObservationSeries(
  observations: ObservationRecordedLedgerEntry[],
  forecasts: ForecastCell[],
): ObservationRecordedLedgerEntry[] {
  const forecastDataPointIds = new Set(
    forecasts.flatMap((forecast) =>
      forecast.dataPointId ? [forecast.dataPointId] : [],
    ),
  );

  return observations.filter(
    (observation) =>
      !forecastDataPointIds.has(observation.dataPointId) &&
      !isObservationCoveredByForecastFamily(
        observation.dataPointId,
        forecastDataPointIds,
      ),
  );
}

export function getLedgerObservationCoverageRule(
  dataPointId: string,
): LedgerObservationCoverageRule | undefined {
  return LEDGER_OBSERVATION_COVERAGE_RULES.find(
    (rule) => rule.observationDataPointId === dataPointId,
  );
}

function isObservationCoveredByForecastFamily(
  dataPointId: string,
  forecastDataPointIds: Set<string>,
): boolean {
  const rule = getLedgerObservationCoverageRule(dataPointId);
  if (!rule) return false;
  return rule.coveredByForecastDataPointIds.some((forecastDataPointId) =>
    forecastDataPointIds.has(forecastDataPointId),
  );
}
