import { FORECAST_CELLS } from "../site/src/data/forecast-cells";
import { THESIS_TARGET_LEDGER } from "../site/src/data/ledger-targets";

interface Args {
  out: string;
  limit: number;
  skip: number;
  prefix?: string;
  dateFrom: string;
  includeFy2025: boolean;
}

function parseArgs(argv: string[]): Args {
  const args: Args = {
    out: "",
    limit: 8,
    skip: 0,
    dateFrom: "2026-06-27",
    includeFy2025: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];
    if (arg === "--out") {
      args.out = requireValue(arg, next);
      index += 1;
    } else if (arg === "--limit") {
      args.limit = Number.parseInt(requireValue(arg, next), 10);
      index += 1;
    } else if (arg === "--skip") {
      args.skip = Number.parseInt(requireValue(arg, next), 10);
      index += 1;
    } else if (arg === "--prefix") {
      args.prefix = requireValue(arg, next);
      index += 1;
    } else if (arg === "--date-from") {
      args.dateFrom = requireValue(arg, next);
      index += 1;
    } else if (arg === "--include-fy2025") {
      args.includeFy2025 = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!args.out) {
    throw new Error("--out is required");
  }
  if (!Number.isFinite(args.limit) || args.limit <= 0) {
    throw new Error("--limit must be a positive integer");
  }
  if (!Number.isFinite(args.skip) || args.skip < 0) {
    throw new Error("--skip must be a non-negative integer");
  }
  return args;
}

function requireValue(arg: string, value: string | undefined): string {
  if (!value) {
    throw new Error(`${arg} requires a value`);
  }
  return value;
}

function derivePeriod(target: (typeof THESIS_TARGET_LEDGER)[number]): string {
  const reportingMatch = target.resolutionRule.match(
    /for the ([^,.]+ reporting period)/i,
  );
  if (reportingMatch) {
    return reportingMatch[1];
  }
  if (target.periodLabel && !/^\d{4}-\d{2}-\d{2}$/.test(target.periodLabel)) {
    return target.periodLabel;
  }
  return target.resolutionDate;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const cellsById = new Map(
    FORECAST_CELLS.filter((cell) => cell.dataPointId).map((cell) => [
      cell.dataPointId,
      cell,
    ]),
  );
  const rows = THESIS_TARGET_LEDGER.map((target) => {
    const cell = cellsById.get(target.dataPointId);
    const recordedRuns =
      cell?.comparisonRuns?.filter(
        (run) => run.predictionRun?.kind === "recorded-agent-run",
      ) ?? [];
    return { target, cell, recordedRuns };
  })
    .filter(({ target, cell, recordedRuns }) => {
      if (!cell?.slug) {
        return false;
      }
      if (target.resolutionDate < args.dateFrom) {
        return false;
      }
      if (!args.includeFy2025 && target.dataPointId.includes("fy2025")) {
        return false;
      }
      if (args.prefix && !cell.slug.startsWith(args.prefix)) {
        return false;
      }
      return recordedRuns.length === 0;
    })
    .sort((left, right) => {
      const dateCompare = left.target.resolutionDate.localeCompare(
        right.target.resolutionDate,
      );
      if (dateCompare !== 0) {
        return dateCompare;
      }
      return left.target.dataPointId.localeCompare(right.target.dataPointId);
    })
    .slice(args.skip, args.skip + args.limit);

  const targets = rows.map(({ target, cell }) => {
    const output: Record<string, unknown> = {
      series: target.dataPointId,
      period: derivePeriod(target),
      catalogSlug: cell?.slug,
      targetUnit: target.unit,
      dataPointId: target.dataPointId,
      resolutionDate: target.resolutionDate,
      resolutionSource: target.resolutionSource,
      resolutionRule: target.resolutionRule,
      resolutionPolicy: target.resolutionPolicy,
    };
    if (target.resolutionSourceUrl) {
      output.resolutionSourceUrl = target.resolutionSourceUrl;
    }
    if (cell?.conditionalOn) {
      output.conditional = cell.conditionalOn;
    }
    return output;
  });

  Bun.write(args.out, `${JSON.stringify({ targets }, null, 2)}\n`);
  console.log(`wrote ${targets.length} targets -> ${args.out}`);
}

main();
