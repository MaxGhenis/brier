import { FORECAST_CELLS } from "@/data/forecast-cells";
import {
  buildThesisLogExport,
  loadPolicyEngineLedger,
  withResolvedOutcomes,
} from "@/data/thesis-log";

export const dynamic = "force-static";

export async function GET() {
  const ledger = await loadPolicyEngineLedger();
  return Response.json(
    buildThesisLogExport(withResolvedOutcomes(FORECAST_CELLS, ledger), ledger),
  );
}
