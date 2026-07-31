/**
 * Registrations that expired without a forecast — a terminal, explicit
 * record, never a silent exemption.
 *
 * A preregistered target awaits its forecast until its release window opens
 * (see isPreregisteredTargetWithinOrphanGrace). When generation failed and
 * the release window passed, forecasting it afterward would fabricate
 * chronology, so the
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
  // 2026-07-22 prospect registrations (commit e6214345) whose analyst leg
  // never produced a cell. Both of these are past their release window —
  // BEA printed July 29, JOLTS August 3 — so no forecast can be honest.
  //
  // ons.vacancies.total_3m_sa.2026_06 was listed here too and has been
  // REMOVED. Its first print is not due until 2026-08-18, so it is still
  // inside its window and the exactness test below now rejects listing it.
  // The original reason for expiring it was capability, not legitimacy: the
  // docket does not roll that series, so nothing could produce the forecast.
  // The awaiting-forecast lane is that missing capability. The registration's
  // resolver binding is unchanged and its ledger pin only guards backfill, so
  // a run against it now forecasts a genuinely unknown future print. If the
  // lane does not land, this id must come back here before 2026-08-18.
  "bea.wages_and_salaries.level.june_2026.first_print",
  "bls.jolts.job_openings_total.june_2026.first_print",
  // 2026-07-25 roll registrations that were never forecastable at all: each
  // was registered AFTER its release window had already closed (Census MTIS
  // May 2026 closed 07-21, BLS CES June 2026 closed 07-09), so the first
  // print was public before the preregistration existed. The flat 7-day
  // timer hid this until 2026-08-01; bounding grace by the release window
  // surfaces it immediately, which is the honest reading. The selection
  // guard in register_targets.py now refuses to create these.
  "bls.ces.average_hourly_earnings_private.june_2026.first_print",
  "census.mtis.total_business_inventories_level.may_2026.first_print",
] as const;

export const EXPIRED_UNFORECAST_SET: ReadonlySet<string> = new Set(
  EXPIRED_UNFORECAST_REGISTRATIONS,
);
