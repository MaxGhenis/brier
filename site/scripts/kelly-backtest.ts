/**
 * Kelly backtest over resolved paired forecasts.
 *
 * Synthetic market: the ledger persistence baseline prices binary
 * "outcome > t" contracts at its own CDF; the agent bets Kelly-sized
 * stakes from its recorded distribution; positions settle on official
 * prints. Pairs exist only where the ledger held at least two pre-cutoff
 * observations for the series, so the universe grows as series repeat.
 *
 * Run: bun scripts/kelly-backtest.ts [--json out.json]
 */
import { FORECAST_CELLS } from "@/data/forecast-cells";
import {
  hasVerifiedClaimedChronology,
  loadPolicyEngineLedger,
  scoreResolvedForecasts,
  withResolvedOutcomes,
} from "@/data/thesis-log";
import { runKellyBacktest, type BacktestEntry } from "@/data/kelly";

const ledger = await loadPolicyEngineLedger();
const forecasts = withResolvedOutcomes(FORECAST_CELLS, ledger);
const scoreBySlug = new Map(
  scoreResolvedForecasts(forecasts, ledger)
    .filter((score) => hasVerifiedClaimedChronology(score.chronology))
    .map((score) => [score.forecastSlug, score]),
);

const entries: BacktestEntry[] = [];
for (const cell of forecasts) {
  const baseline = cell.persistenceBaseline as
    | { status?: string; variantId?: string }
    | undefined;
  if (!baseline || baseline.status !== "available") continue;
  const score = scoreBySlug.get(cell.slug);
  if (!score) continue;
  const agentPoints = (cell as any).predictionDistribution?.points;
  const baselineRun = ((cell as any).comparisonRuns ?? []).find(
    (run: any) => run.variantId === baseline.variantId,
  );
  const baselinePoints = baselineRun?.predictionDistribution?.points;
  if (!agentPoints?.length || !baselinePoints?.length) continue;
  entries.push({
    slug: cell.slug,
    resolutionDate: cell.resolutionDate,
    chronology: score.chronology,
    agentPoints,
    baselinePoints,
    observed: score.observedValue,
  });
}

console.log(`paired entries: ${entries.length}`);
for (const scale of [1, 0.5, 0.25]) {
  const { summary } = runKellyBacktest(entries, { kellyScale: scale });
  console.log(
    `kelly x${scale}: bets=${summary.bets} targets=${summary.targets} ` +
      `wealth=${summary.finalWealthMultiple.toFixed(3)} ` +
      `hit=${(summary.hitRate * 100).toFixed(0)}% ` +
      `meanEdge=${summary.meanAbsEdge.toFixed(3)} ` +
      `maxDD=${(summary.maxDrawdown * 100).toFixed(0)}%`,
  );
}
const { rows } = runKellyBacktest(entries, { kellyScale: 0.5 });
for (const row of rows) {
  console.log(
    `  ${row.resolutionDate} ${row.slug} q${row.thresholdQuantile} ` +
      `${row.side} stake=${(row.stake * 100).toFixed(1)}% ` +
      `pA=${row.pAgent.toFixed(2)} pM=${row.pMarket.toFixed(2)} ` +
      `${row.won ? "WON" : "lost"}`,
  );
}

const jsonFlag = process.argv.indexOf("--json");
if (jsonFlag !== -1 && process.argv[jsonFlag + 1]) {
  const output = {
    generatedNote:
      "Synthetic market: persistence baseline as counterparty at its own CDF prices; not exchange prices.",
    entries: entries.length,
    variants: Object.fromEntries(
      [1, 0.5, 0.25].map((scale) => [
        `kelly_x${scale}`,
        runKellyBacktest(entries, { kellyScale: scale }).summary,
      ]),
    ),
    rows,
  };
  await Bun.write(process.argv[jsonFlag + 1], JSON.stringify(output, null, 1));
  console.log(`wrote ${process.argv[jsonFlag + 1]}`);
}
