import fs from "node:fs";
import path from "node:path";
import type { MetricStance } from "@/lib/stances";

// bill.json artifacts live at the repo root (bills/<slug>.json), written
// by scripts/ingest_bill.py — the site reads them at build time. Vercel
// must have "include files outside root directory" enabled and the
// ignored-build-step watching bills/ for artifact-only pushes to deploy
// (issue #43).
const BILLS_DIR = path.join(process.cwd(), "..", "bills");

export interface BillInfo {
  slug?: string;
  name: string;
  status: string;
  pages: number;
  analyzed: string;
  analysisDate: string;
  sourceUrl: string;
}

export interface BillEffect {
  mechanism: string;
  text: string;
}

export interface BillBarrier {
  actor: string;
  text: string;
}

export interface BillMetric {
  kind: string;
  text: string;
  series_hint?: string;
  /** Frozen analysis-day badge carried by ported artifacts. */
  registry?: string;
  /**
   * Why this metric was selected — considered alternatives, resolution
   * properties, known weaknesses. Additive contract field; rendered as
   * a disclosure when present.
   */
  rationale?: string;
  /**
   * Stance v1 (issue #43 micro-spec): one extraction-time
   * serves/opposes/orthogonal judgment per imputed goal, keyed by goal
   * index. The client folds this over the countersign store.
   */
  stances?: MetricStance[];
  /**
   * Layer addendum (issue #43): does the agency act, do people engage,
   * does the world change. Intrinsic to the metric; accepted now,
   * rendered when the intended/unintended/operational grouping lands.
   */
  layer?: "execution" | "participation" | "outcome";
  category?: string;
}

export interface BillCompute {
  model: string;
  reform: Record<string, unknown>;
  result_summary: string;
  /**
   * Provenance for the audited PolicyEngine call path (issue #45) —
   * additive contract fields carried by compute rows produced through
   * scripts/tools/policyengine.py. `certification` records whether the
   * model version matches the dataset build's certified pairing; an
   * uncertified row is inadmissible for a published number.
   */
  engine?: string;
  pe_us_version?: string;
  pe_core_version?: string;
  dataset?: string;
  certification?: {
    certified_model_version?: string;
    running_model_version?: string;
    certified: boolean;
  };
  year?: number;
  region?: string;
  status?: string;
  budgetary_impact?: number;
  ten_year_budgetary_impact?: number;
  ten_year_window?: string;
  poverty_child_pct_change?: number;
  beneficiaries_share?: number;
  note?: string;
  source?: string;
}

export interface BillProvision {
  title: string;
  heading: string;
  quote: string;
  goals: string[];
  effects: BillEffect[];
  barriers: BillBarrier[];
  metrics: BillMetric[];
  conditionals: string[];
  context?: string;
  compute?: BillCompute[];
}

export interface BillArtifact {
  slug: string;
  bill: BillInfo;
  provisions: BillProvision[];
}

export function loadBills(): BillArtifact[] {
  if (!fs.existsSync(BILLS_DIR)) return [];
  return fs
    .readdirSync(BILLS_DIR)
    .filter((name) => name.endsWith(".json"))
    .map((name) => {
      const raw = JSON.parse(
        fs.readFileSync(path.join(BILLS_DIR, name), "utf-8"),
      ) as Omit<BillArtifact, "slug">;
      return { slug: name.replace(/\.json$/, ""), ...raw };
    })
    .sort((a, b) =>
      (b.bill.analysisDate ?? "").localeCompare(a.bill.analysisDate ?? ""),
    );
}

export function getBill(slug: string): BillArtifact | undefined {
  return loadBills().find((bill) => bill.slug === slug);
}

export interface BillRawMeta {
  resolved_via?: string;
  source_url?: string;
  version_label?: string;
  axiomBillId?: string;
  axiomDashboardUrl?: string;
}

/** Provenance sidecar written by the fetcher — optional by design. */
export function loadBillMeta(slug: string): BillRawMeta | null {
  const file = path.join(BILLS_DIR, "raw", `${slug}.meta.json`);
  if (!fs.existsSync(file)) return null;
  try {
    return JSON.parse(fs.readFileSync(file, "utf-8")) as BillRawMeta;
  } catch {
    return null;
  }
}

export type RegistryStatus = "reachable" | "not-yet" | "no-series" | "unknown";

export const REGISTRY_LABEL: Record<RegistryStatus, string> = {
  reachable: "In Thesis registry",
  "not-yet": "Not yet in Thesis",
  "no-series": "No official series",
  unknown: "Unmapped",
};

/**
 * The registry seam. The live registry mapper (issue #43, Max's track)
 * computes candidate-metric status against the docket at build time;
 * until it lands, ported artifacts fall back to their frozen
 * analysis-day badge. `live` tells the UI whether the badge is computed
 * or frozen.
 */
export function metricRegistryStatus(metric: BillMetric): {
  status: RegistryStatus;
  live: boolean;
} {
  const frozen = metric.registry;
  if (frozen === "reachable" || frozen === "not-yet" || frozen === "no-series") {
    return { status: frozen, live: false };
  }
  return { status: "unknown", live: false };
}
