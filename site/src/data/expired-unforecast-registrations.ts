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
  // 2026-07-22 prospect registrations (commit e6214345) whose analyst leg
  // never produced a cell. The BEA first print (July 29) has passed. The
  // JOLTS (Aug 3) and ONS vacancies (Aug 18) prints have not, but these end
  // here for the same reason: each registration pins ledger 02b1747916 and
  // an information set from July 22, and the docket no longer rolls them —
  // bls.jolts.job_openings_total, bea.wages_and_salaries.level, and
  // ons.vacancies.total_3m_sa are not the registry series/slugs the roll
  // advances. Forecasting them now would record a run against a ten-day
  // stale pin, which is the chronology the grace window exists to protect.
  "bea.wages_and_salaries.level.june_2026.first_print",
  "bls.jolts.job_openings_total.june_2026.first_print",
  "ons.vacancies.total_3m_sa.2026_06.first_print",
  // The 2026-07-29 UK PPI registration crossed its seven-day orphan grace
  // without a forecast. Its August 19 first print remains in the future, but
  // generating against the stale registration now would violate the same
  // chronology guarantee, so the registration terminates explicitly here.
  "ons.ppi.output_all_manufactured_yoy.2026_07.first_print",
  // The 2026-07-31 hackathon-day seeds crossed the seven-day orphan grace
  // on 2026-08-07 without a forecast. The MTIS May and CES June first
  // prints are already public, so forecasting them now would be hindsight;
  // the ECI 2026 Q3 print remains in the future but terminates here for
  // the PPI precedent's reason — a run against a week-stale registration
  // breaks the chronology the grace window exists to protect.
  "census.mtis.total_business_inventories_level.may_2026.first_print",
  "bls.ces.average_hourly_earnings_private.june_2026.first_print",
  "bls.eci.total_compensation_private_industry_qoq.2026_q3.first_print",
] as const;

export const EXPIRED_UNFORECAST_SET: ReadonlySet<string> = new Set(
  EXPIRED_UNFORECAST_REGISTRATIONS,
);
