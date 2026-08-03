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

export const BILL_FORECAST_LINKS: BillForecastLink[] = [];

/**
 * Registered conditional questions whose runs have not produced a cell:
 * either the runner refused (fail-closed epistemics — shown with its
 * verbatim reasoning) or the run is still in flight. Nothing here is a
 * forecast; it is the honest state of the machine.
 */
export interface PendingConditional {
  billSlug: string;
  question: string;
  status: "refused" | "pending";
  /** Verbatim runner reasoning for a refusal. */
  note?: string;
}

export const PENDING_CONDITIONALS: PendingConditional[] = [
  {
    billSlug: "farm-bill-2-0",
    question:
      "USDA FSA total CRP enrolled acres in the September 2027 CRP Monthly Summary — conditional on enactment of a 27,000,000-acre FY2027–31 ceiling versus no enacted FY2027–31 ceiling by 2027-09-30.",
    status: "pending",
    note: "Both arms were preregistered through the trusted docket on 2026-08-03 — chronology witnessed before any forecasting. The first wave's drafts were refused by validation (thesis#115); the registration and the refusal are immutable records, and the pair publishes when a draft passes.",
  },
  {
    billSlug: "s3596-119",
    question:
      "Census SPM child poverty rate, CY2026 — conditional on the CTC phase-in provision (IRC §24(d)(1)(B)(i) earned-income threshold ≤ $1) being enacted in substantially similar form by 2027-12-31.",
    status: "refused",
    note: "Runner refused under its resolution-date rule, verbatim: “No valid forecast cell can be produced yet because the Census Bureau has not published an official release date… Census announced on 2026-07-17 that its 2019–2024 SPM estimates will be revised, so the currently published history is not a stable calibration set.”",
  },
  {
    billSlug: "s3596-119",
    question:
      "IRS Additional Child Tax Credit total claims, TY2027 — conditional on IRC §24(d)(1)(B)(i) earned-income threshold ≤ $1 for TY2027, enacted by 2027-12-31.",
    status: "pending",
    note: "Both arms were preregistered through the trusted docket on 2026-08-03 (registration 966f199f) — chronology witnessed before any forecasting. Four CI waves since were refused by validation: schema-incomplete drafts, and wrong-series fetches caught by the anchor gate (thesis#115). The registration and every refusal are immutable records; the pair publishes when a draft passes, not before.",
  },
];

export function getPendingConditionals(billSlug: string): PendingConditional[] {
  return PENDING_CONDITIONALS.filter((p) => p.billSlug === billSlug);
}

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
