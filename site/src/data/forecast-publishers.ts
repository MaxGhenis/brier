import type { ForecastCell } from "./forecast-cells";

/**
 * Publisher is a DERIVED attribute: the leading agency token of a cell's
 * dataPointId (`agency.program.metric.period`). Nothing here assigns cells
 * to publishers by hand — the only code below is (1) flattening of
 * provably-same-organization spellings that appear in recorded ids and
 * (2) display labels for known tokens. Unknown tokens still derive: they
 * render under their raw token, so new agencies need no edit to ship.
 */
export interface PublisherInfo {
  slug: string;
  label: string;
}

/** Same-organization spelling flattening, all verifiable from the ids:
 * `us.<agency>.` country-prefixed ids collapse to the agency token;
 * `usda.fns.` is FNS; `hhs.acf.` is ACF; `frb` and `fed` are both the
 * Federal Reserve; `estat` is the Statistics Bureau of Japan's portal. */
export function publisherSlugForDataPointId(dataPointId: string): string {
  const tokens = dataPointId.split(".");
  let token = tokens[0];
  if (token === "us" && tokens.length > 1) token = tokens[1];
  if (token === "usda" && tokens[1] === "fns") token = "fns";
  if (token === "hhs" && tokens[1] === "acf") token = "acf";
  if (token === "frb") token = "fed";
  if (token === "estat") token = "statjp";
  return token;
}

const PUBLISHER_LABELS: Record<string, string> = {
  bls: "Bureau of Labor Statistics",
  fns: "USDA Food and Nutrition Service",
  cms: "Centers for Medicare & Medicaid Services",
  census: "U.S. Census Bureau",
  bea: "Bureau of Economic Analysis",
  ons: "Office for National Statistics",
  statcan: "Statistics Canada",
  ssa: "Social Security Administration",
  treasury: "U.S. Department of the Treasury",
  eurostat: "Eurostat",
  abs: "Australian Bureau of Statistics",
  irs: "Internal Revenue Service",
  acf: "HHS Administration for Children and Families",
  dol: "U.S. Department of Labor",
  statjp: "Statistics Bureau of Japan",
  nbb: "National Bank of Belgium",
  fed: "Federal Reserve",
  hud: "Department of Housing and Urban Development",
  ed: "Department of Education",
  ca: "State of California",
  va: "Department of Veterans Affairs",
  hhs: "Department of Health and Human Services",
  boe: "Bank of England",
  cdc: "Centers for Disease Control and Prevention",
  statbel: "Statbel",
  bank_of_canada: "Bank of Canada",
  rba: "Reserve Bank of Australia",
  ecb: "European Central Bank",
  boj: "Bank of Japan",
  usaspending: "USAspending",
  usda: "U.S. Department of Agriculture",
};

export function publisherForCell(cell: ForecastCell): PublisherInfo | null {
  if (!cell.dataPointId) return null;
  const slug = publisherSlugForDataPointId(cell.dataPointId);
  return { slug, label: PUBLISHER_LABELS[slug] ?? slug };
}

export interface PublisherFacetEntry extends PublisherInfo {
  count: number;
}

/** Distinct publishers present in `cells`, largest first, ties by slug. */
export function buildPublisherFacet(
  cells: ForecastCell[],
): PublisherFacetEntry[] {
  const counts = new Map<string, PublisherFacetEntry>();
  for (const cell of cells) {
    const publisher = publisherForCell(cell);
    if (!publisher) continue;
    const existing = counts.get(publisher.slug);
    if (existing) {
      existing.count += 1;
    } else {
      counts.set(publisher.slug, { ...publisher, count: 1 });
    }
  }
  return [...counts.values()].sort(
    (a, b) => b.count - a.count || a.slug.localeCompare(b.slug),
  );
}
