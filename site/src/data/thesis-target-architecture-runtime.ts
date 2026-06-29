import { FORECAST_CELLS } from "./forecast-cells";
import { buildTargetArchitectureProjection } from "./thesis-target-architecture";
import { loadPolicyEngineLedger, withResolvedOutcomes } from "./thesis-log";

export async function loadTargetArchitectureProjection() {
  const ledger = await loadPolicyEngineLedger();
  return buildTargetArchitectureProjection(
    withResolvedOutcomes(FORECAST_CELLS, ledger),
    ledger,
  );
}
