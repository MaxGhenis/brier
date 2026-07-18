/**
 * Registrations that expired without a forecast — a terminal, explicit
 * record, never a silent exemption.
 *
 * A preregistered target gets TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS to
 * receive its forecast. When generation failed and the release window
 * passed, forecasting it afterward would fabricate chronology, so the
 * registration ends here instead: enumerated by exact dataPointId,
 * surfaced on the calibration page, and enforced exact by tests — every
 * listed id must truly be registered, unforecast, and out of grace, and an
 * id that ever gains a forecast must be removed. Additions to this list
 * are reviewed commits; nothing lands here automatically.
 */
export const EXPIRED_UNFORECAST_REGISTRATIONS = [
  // 2026-07-10 roll registrations whose generation leg failed before the
  // step-shape and publication fixes landed; their June 2026 first prints
  // (Statcan LFS July 10, ONS retail sales July 18) arrived unforecast.
  "ons.retail_sales.volume_mom.june_2026.first_print",
  "statcan.lfs.employment_change.canada.june_2026.first_print",
  "statcan.lfs.unemployment_rate.canada.june_2026.first_print",
] as const;

export const EXPIRED_UNFORECAST_SET: ReadonlySet<string> = new Set(
  EXPIRED_UNFORECAST_REGISTRATIONS,
);
