import type { ForecastCell } from "./forecast-cells";

/**
 * Topic views are standing, rule-based collections over the forecast
 * catalog. A topic never lists cells by hand: membership is computed from
 * `dataPointId` prefixes, so when the spawn pipeline or the auto-roll loop
 * publishes the next period of a series (same agency.program.metric prefix,
 * new period suffix), the new cell joins its topics with no edit here.
 *
 * `includeSlugs`/`excludeSlugs` are escape hatches for cells that lack a
 * dataPointId or that a prefix rule captures incorrectly. Prefer adding a
 * prefix over enumerating slugs; enumerated slugs go stale as waves roll.
 */
export interface TopicDefinition {
  slug: string;
  title: string;
  /** One-line label used in chips and breadcrumbs. */
  shortLabel: string;
  /** Public-facing standfirst for the topic page and index. */
  description: string;
  /**
   * A cell joins the topic when its dataPointId starts with any prefix.
   * Keep prefixes at the agency.program.metric level — never include the
   * period suffix.
   */
  dataPointIdPrefixes: string[];
  /** Cells without a dataPointId (or outside the prefix rules) to include. */
  includeSlugs?: string[];
  /** Cells a prefix rule captures that do not belong. */
  excludeSlugs?: string[];
}

export const TOPICS: TopicDefinition[] = [
  {
    slug: "aging-disability",
    title: "Aging & disability",
    shortLabel: "aging & disability",
    description:
      "Standing view of every live forecast on aging and disability policy: " +
      "Social Security administration and benefits (SSI, SSDI, hearings, " +
      "COLA), veterans' disability claims, Medicaid coverage for older " +
      "adults, older-worker labor-market outcomes, and senior poverty — " +
      "plus outcomes conditional on pending policy deadlines. New cells " +
      "that forecast these series join this page automatically when they " +
      "are published.",
    dataPointIdPrefixes: [
      // Social Security Administration: SSI (65+ cut and program total),
      // OASDI disabled-worker benefits, hearings backlog, DDS initial
      // disability applications (conditional pair), annual COLA.
      "ssa.ssi.",
      "ssa.oasdi.",
      "ssa.hearings.",
      "ssa.dds.",
      "ssa.cola.",
      // VA Veterans Benefits Administration workload (pending claims).
      "va.vba.",
      // Medi-Cal certified eligibles ages 50-64 (conditional pair).
      "ca.dhcs.medi_cal_certified_eligibles.ages_50_64",
      // Older-worker labor force participation and disability EPOP (CPS).
      "bls.cps.lfpr_55_plus",
      "bls.cps.LNU02374597",
      // Census SPM poverty rate, 65 and older.
      "census.spm.poverty_rate_65_plus",
      // CMS Care Compare nursing-home staffing (PBJ-based national HPRD).
      "cms.nursing_home_compare.",
      // BLS CES home health care services employment (care workforce).
      "bls.ces.home_health_care_services.",
      // Census ACS broadband subscription among the 65+ population.
      "census.acs.broadband_subscription_65_plus",
      // USDA FNS SNAP participation among adults 60+ (annual QC characteristics).
      "usda.fns.snap.participants_age_60_plus",
    ],
  },
];

export function getTopic(slug: string): TopicDefinition | undefined {
  return TOPICS.find((topic) => topic.slug === slug);
}

export function cellMatchesTopic(
  cell: ForecastCell,
  topic: TopicDefinition,
): boolean {
  if (topic.excludeSlugs?.includes(cell.slug)) return false;
  if (topic.includeSlugs?.includes(cell.slug)) return true;
  const dataPointId = cell.dataPointId;
  if (!dataPointId) return false;
  return topic.dataPointIdPrefixes.some((prefix) =>
    dataPointId.startsWith(prefix),
  );
}

export function cellsForTopic(
  topic: TopicDefinition,
  cells: ForecastCell[],
): ForecastCell[] {
  return cells.filter((cell) => cellMatchesTopic(cell, topic));
}

export function topicsForCell(cell: ForecastCell): TopicDefinition[] {
  return TOPICS.filter((topic) => cellMatchesTopic(cell, topic));
}
