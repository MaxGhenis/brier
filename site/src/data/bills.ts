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
}

export interface BillCompute {
  model: string;
  reform: Record<string, unknown>;
  result_summary: string;
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
