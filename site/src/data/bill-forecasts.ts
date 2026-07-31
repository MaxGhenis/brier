import {
  getConditionalGroup,
  type ResolvedConditionalGroup,
} from "./conditional-groups";

/**
 * Links bill analyses (bills/<slug>.json) to registered conditional
 * forecast groups. One link per forecast metric: the group's true arm
 * is the outcome conditional on the bill's provision surviving into
 * enacted law, the false arm is the baseline (not enacted).
 *
 * Populated through the privileged registration path — the ingest lane
 * auto-drafts cell specs into drafts/, and links land here only when
 * the pair is actually registered. Never link a group whose condition
 * is not provision-anchored to the bill named by billSlug.
 */
export interface BillForecastLink {
  billSlug: string;
  /** Short label for the metric selector, e.g. "CRP enrolled acres". */
  metricLabel: string;
  groupSlug: string;
}

export const BILL_FORECAST_LINKS: BillForecastLink[] = [];

export interface BillForecastGroup {
  metricLabel: string;
  resolved: ResolvedConditionalGroup;
}

export function getBillForecastGroups(billSlug: string): BillForecastGroup[] {
  return BILL_FORECAST_LINKS.filter((link) => link.billSlug === billSlug)
    .map((link) => {
      const resolved = getConditionalGroup(link.groupSlug);
      return resolved
        ? { metricLabel: link.metricLabel, resolved }
        : undefined;
    })
    .filter((group): group is BillForecastGroup => group !== undefined);
}
