/**
 * Kelly backtest over resolved forecasts.
 *
 * Construction: for each resolved paired target, a synthetic binary market
 * prices "outcome > t" at the persistence baseline's own probability
 * (p_market = 1 - F_baseline(t)); the agent bets its distribution's
 * probability with Kelly sizing and the position settles on the official
 * print. The baseline is the counterparty, not a real exchange — this
 * converts the paired-CRPS comparison into bankroll terms, nothing more.
 * Thresholds sit at baseline quantiles, so by construction the market
 * never thinks it has an edge on itself.
 */

export interface CdfPoint {
  value: number;
  probability: number;
}

export function cdfAt(points: CdfPoint[], x: number): number {
  if (points.length === 0) return Number.NaN;
  if (x <= points[0].value) return x < points[0].value ? 0 : points[0].probability;
  const last = points[points.length - 1];
  if (x >= last.value) return x > last.value ? 1 : last.probability;
  for (let index = 1; index < points.length; index += 1) {
    const prev = points[index - 1];
    const curr = points[index];
    if (x <= curr.value) {
      if (curr.value === prev.value) return curr.probability;
      const t = (x - prev.value) / (curr.value - prev.value);
      return prev.probability + t * (curr.probability - prev.probability);
    }
  }
  return 1;
}

export function quantileAt(points: CdfPoint[], p: number): number {
  if (points.length === 0) return Number.NaN;
  if (p <= points[0].probability) return points[0].value;
  const last = points[points.length - 1];
  if (p >= last.probability) return last.value;
  for (let index = 1; index < points.length; index += 1) {
    const prev = points[index - 1];
    const curr = points[index];
    if (p <= curr.probability) {
      if (curr.probability === prev.probability) return curr.value;
      const t = (p - prev.probability) / (curr.probability - prev.probability);
      return prev.value + t * (curr.value - prev.value);
    }
  }
  return last.value;
}

export interface KellyBet {
  side: "yes" | "no";
  fraction: number;
  edge: number;
}

/** Full-Kelly stake for a binary market priced at pMarket. */
export function kellyBet(
  pAgent: number,
  pMarket: number,
  minEdge = 0.005,
): KellyBet | null {
  if (
    !Number.isFinite(pAgent) ||
    !Number.isFinite(pMarket) ||
    pMarket <= 0 ||
    pMarket >= 1
  ) {
    return null;
  }
  const edge = pAgent - pMarket;
  if (Math.abs(edge) < minEdge) return null;
  if (edge > 0) {
    return { side: "yes", fraction: edge / (1 - pMarket), edge };
  }
  return { side: "no", fraction: -edge / pMarket, edge };
}

/** Log-wealth increment for a settled bet at the given Kelly scale. */
export function settleLogGrowth(
  bet: KellyBet,
  outcomeYes: boolean,
  pMarket: number,
  kellyScale: number,
  maxFraction = 0.25,
): number {
  const stake = Math.min(bet.fraction * kellyScale, maxFraction);
  const won = bet.side === "yes" ? outcomeYes : !outcomeYes;
  const price = bet.side === "yes" ? pMarket : 1 - pMarket;
  const payoutPerUnit = (1 - price) / price;
  return Math.log1p(won ? stake * payoutPerUnit : -stake);
}

export interface BacktestEntry {
  slug: string;
  resolutionDate: string;
  chronology: string;
  agentPoints: CdfPoint[];
  baselinePoints: CdfPoint[];
  observed: number;
}

export interface BacktestOptions {
  thresholds?: number[];
  kellyScale?: number;
  maxFraction?: number;
  minEdge?: number;
}

export interface BacktestBetRow {
  slug: string;
  resolutionDate: string;
  chronology: string;
  thresholdQuantile: number;
  threshold: number;
  pAgent: number;
  pMarket: number;
  side: "yes" | "no";
  stake: number;
  won: boolean;
  logGrowth: number;
}

export interface BacktestSummary {
  bets: number;
  targets: number;
  finalWealthMultiple: number;
  meanLogGrowthPerBet: number;
  hitRate: number;
  meanAbsEdge: number;
  maxDrawdown: number;
}

export function runKellyBacktest(
  entries: BacktestEntry[],
  options: BacktestOptions = {},
): { rows: BacktestBetRow[]; summary: BacktestSummary } {
  const thresholds = options.thresholds ?? [0.25, 0.5, 0.75];
  const kellyScale = options.kellyScale ?? 0.5;
  const maxFraction = options.maxFraction ?? 0.25;
  const rows: BacktestBetRow[] = [];
  const ordered = [...entries].sort(
    (a, b) =>
      a.resolutionDate.localeCompare(b.resolutionDate) ||
      a.slug.localeCompare(b.slug),
  );
  const targetsWithBets = new Set<string>();
  for (const entry of ordered) {
    for (const q of thresholds) {
      const threshold = quantileAt(entry.baselinePoints, q);
      if (!Number.isFinite(threshold)) continue;
      const pMarket = 1 - cdfAt(entry.baselinePoints, threshold);
      const pAgent = 1 - cdfAt(entry.agentPoints, threshold);
      const bet = kellyBet(pAgent, pMarket, options.minEdge);
      if (!bet) continue;
      const outcomeYes = entry.observed > threshold;
      const logGrowth = settleLogGrowth(
        bet,
        outcomeYes,
        pMarket,
        kellyScale,
        maxFraction,
      );
      targetsWithBets.add(entry.slug);
      rows.push({
        slug: entry.slug,
        resolutionDate: entry.resolutionDate,
        chronology: entry.chronology,
        thresholdQuantile: q,
        threshold,
        pAgent,
        pMarket,
        side: bet.side,
        stake: Math.min(bet.fraction * kellyScale, maxFraction),
        won: bet.side === "yes" ? outcomeYes : !outcomeYes,
        logGrowth,
      });
    }
  }
  let logWealth = 0;
  let peak = 0;
  let maxDrawdown = 0;
  for (const row of rows) {
    logWealth += row.logGrowth;
    peak = Math.max(peak, logWealth);
    maxDrawdown = Math.max(maxDrawdown, 1 - Math.exp(logWealth - peak));
  }
  const summary: BacktestSummary = {
    bets: rows.length,
    targets: targetsWithBets.size,
    finalWealthMultiple: Math.exp(logWealth),
    meanLogGrowthPerBet: rows.length > 0 ? logWealth / rows.length : 0,
    hitRate:
      rows.length > 0
        ? rows.filter((row) => row.won).length / rows.length
        : Number.NaN,
    meanAbsEdge:
      rows.length > 0
        ? rows.reduce((total, row) => total + Math.abs(row.pAgent - row.pMarket), 0) /
          rows.length
        : Number.NaN,
    maxDrawdown,
  };
  return { rows, summary };
}
