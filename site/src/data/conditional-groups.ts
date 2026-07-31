import { getForecastCell, type ForecastCell } from "./forecast-cells";

export interface ConditionalGroup {
  slug: string;
  title: string;
  question: string;
  eventLabel: string;
  trueArmSlug: string;
  /** Absent for single-arm registrations (enacted-conditional only). */
  falseArmSlug?: string;
  probabilitySlug?: string;
  unconditionalSlug?: string;
  gapNote?: string;
}

export const CONDITIONAL_GROUPS: ConditionalGroup[] = [
  {
    slug: "s3596-actc-ty2027-threshold-one-dollar",
    title: "ACTC claimant returns under S.3596's phase-in provision",
    question:
      "How many families claim the refundable child tax credit for tax year 2027, and what does S.3596's first-dollar phase-in do to that number?",
    eventLabel:
      "No legislation enacted by 2027-12-31 changes the IRC \u00a724(d)(1)(B)(i) earned-income threshold for tax year 2027 \u2014 current law holds",
    trueArmSlug: "additional-child-tax-credit-total-claims-ty2027-current-law",
    gapNote:
      "The enacted arm is in the pre-submit review loop \u2014 the rubric has rejected two drafts today for missing falsification phrasing. It publishes when it passes, not before.",
  },

  {
    slug: "medicaid-work-req-wait-mar-2027",
    title: "Medicaid hold times under the work-requirement deadline",
    question:
      "What does the December 31, 2026 community-engagement compliance deadline do to the national average Medicaid call-center wait in March 2027?",
    eventLabel:
      "Deadline in effect as of 2027-03-31 (no statutory delay, no nationwide stay)",
    trueArmSlug: "medicaid-call-wait-mar-2027-work-req-deadline-holds",
    falseArmSlug: "medicaid-call-wait-mar-2027-work-req-deadline-delayed",
    probabilitySlug: "medicaid-work-req-deadline-in-effect-2027q1",
    unconditionalSlug: "medicaid-call-wait-mar-2027",
    gapNote:
      "At roughly 10 million calls a month, the 11-minute gap between arms is about 1.8 million person-hours of waiting per month riding on this one policy state.",
  },
  {
    slug: "snap-cost-share-error-rate-fy2026",
    title: "SNAP payment accuracy under the cost-share provision",
    question:
      "What does the 2025 reconciliation law's state cost-share provision do to the national SNAP payment error rate in FY 2026?",
    eventLabel:
      "Cost-share provision in effect through 2027-06-30 (no repeal or delay enacted)",
    trueArmSlug: "snap-error-rate-fy2026-cost-share-in-effect",
    falseArmSlug: "snap-error-rate-fy2026-cost-share-repealed",
    gapNote:
      "The 0.9-point gap between arms is the forecasted effect of the cost-share incentive on payment accuracy — published before the policy question is settled.",
  },
];

export interface ResolvedConditionalGroup {
  group: ConditionalGroup;
  trueArm: ForecastCell;
  falseArm?: ForecastCell;
  probability?: ForecastCell;
  unconditional?: ForecastCell;
}

export function getConditionalGroup(
  slug: string,
): ResolvedConditionalGroup | undefined {
  const group = CONDITIONAL_GROUPS.find((g) => g.slug === slug);
  if (!group) return undefined;
  const trueArm = getForecastCell(group.trueArmSlug);
  const falseArm = group.falseArmSlug
    ? getForecastCell(group.falseArmSlug)
    : undefined;
  if (!trueArm) return undefined;
  // A named-but-missing baseline arm is a data error — fail closed.
  if (group.falseArmSlug && !falseArm) return undefined;
  return {
    group,
    trueArm,
    falseArm,
    probability: group.probabilitySlug
      ? getForecastCell(group.probabilitySlug)
      : undefined,
    unconditional: group.unconditionalSlug
      ? getForecastCell(group.unconditionalSlug)
      : undefined,
  };
}
