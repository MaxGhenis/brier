import { mkdir, writeFile } from "node:fs/promises";
import { dirname } from "node:path";
import { FORECAST_CELLS } from "../site/src/data/forecast-cells";
import { buildTargetArchitectureBackfillSql } from "../site/src/data/thesis-target-architecture-sql";
import { assertValidTargetArchitectureProjection } from "../site/src/data/thesis-target-architecture";
import {
  loadPolicyEngineLedger,
  withResolvedOutcomes,
} from "../site/src/data/thesis-log";

interface Args {
  out: string;
  sqlOut: string;
}

function parseArgs(argv: string[]): Args {
  const args: Args = {
    out: "",
    sqlOut: "",
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];
    if (arg === "--out") {
      args.out = requireValue(arg, next);
      index += 1;
    } else if (arg === "--sql-out") {
      args.sqlOut = requireValue(arg, next);
      index += 1;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!args.out) {
    throw new Error("--out is required");
  }
  if (!args.sqlOut) {
    throw new Error("--sql-out is required");
  }
  return args;
}

function requireValue(arg: string, value: string | undefined): string {
  if (!value) {
    throw new Error(`${arg} requires a value`);
  }
  return value;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const ledger = await loadPolicyEngineLedger();
  const forecasts = withResolvedOutcomes(FORECAST_CELLS, ledger);
  const backfill = buildTargetArchitectureBackfillSql({
    forecasts,
    ledger,
  });
  assertValidTargetArchitectureProjection(backfill.projection);
  await mkdir(dirname(args.out), { recursive: true });
  await mkdir(dirname(args.sqlOut), { recursive: true });
  await writeFile(
    args.out,
    `${JSON.stringify(backfill.projection, null, 2)}\n`,
  );
  await writeFile(args.sqlOut, backfill.sql);
  console.log(
    [
      `wrote ${args.out}`,
      `wrote ${args.sqlOut}`,
      `${backfill.counts.targets} targets`,
      `${backfill.counts.forecastRuns} target-architecture runs`,
      `${backfill.counts.forecastDistributionPoints} distribution points`,
    ].join(" · "),
  );
}

main();
