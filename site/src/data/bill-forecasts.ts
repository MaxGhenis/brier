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
  /**
   * True when the pair is a real registered group from ANOTHER policy
   * state, linked purely to demonstrate the view. Rendered with an
   * explicit example banner; remove once real bill-anchored pairs are
   * registered. Never omit this flag on a pair that is not
   * provision-anchored to billSlug.
   */
  example?: boolean;
}

export const BILL_FORECAST_LINKS: BillForecastLink[] = [
  {
    billSlug: "farm-bill-2-0",
    metricLabel: "Medicaid call wait",
    groupSlug: "medicaid-work-req-wait-mar-2027",
    example: true,
  },
  {
    billSlug: "farm-bill-2-0",
    metricLabel: "SNAP error rate",
    groupSlug: "snap-cost-share-error-rate-fy2026",
    example: true,
  },
];

export interface BillForecastGroup {
  metricLabel: string;
  resolved: ResolvedConditionalGroup;
  example: boolean;
}

export function getBillForecastGroups(billSlug: string): BillForecastGroup[] {
  return BILL_FORECAST_LINKS.filter((link) => link.billSlug === billSlug)
    .map((link) => {
      const resolved = getConditionalGroup(link.groupSlug);
      return resolved
        ? {
            metricLabel: link.metricLabel,
            resolved,
            example: link.example === true,
          }
        : undefined;
    })
    .filter((group): group is BillForecastGroup => group !== undefined);
}
