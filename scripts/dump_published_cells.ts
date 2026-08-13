// Emit the EVALUATED published-cell catalog as JSON: one row per cell
// with its slug and registration identity. This is the authoritative
// publication view for Python-side tooling (retry selection): it
// imports the same module the site builds from, so dynamically
// constructed entries (OEWS, SNAP) and filtered definitions are exactly
// what the site publishes — a regex over TS source is not (2026-08-13
// review of PR #181 measured 186 misses and 10 phantoms).
//
// Run with: bun scripts/dump_published_cells.ts
import { FORECAST_CELLS } from "../site/src/data/forecast-cells";

const rows = FORECAST_CELLS.map((cell) => ({
  slug: cell.slug,
  dataPointId: cell.dataPointId ?? null,
  type: cell.type,
}));

console.log(JSON.stringify(rows));
