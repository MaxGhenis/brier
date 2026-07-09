import { FORECAST_CELLS } from "./forecast-cells";
import { buildTargetArchitectureProjection } from "./thesis-target-architecture";
import { loadPolicyEngineLedger, withResolvedOutcomes } from "./thesis-log";

let targetArchitectureProjectionPromise: ReturnType<
  typeof buildTargetArchitectureProjectionOnce
> | null = null;

/** Share one projection across the manifest, table, and chunk static routes. */
export function loadTargetArchitectureProjection() {
  targetArchitectureProjectionPromise ??=
    buildTargetArchitectureProjectionOnce();
  return targetArchitectureProjectionPromise;
}

export function resetTargetArchitectureProjectionCache() {
  targetArchitectureProjectionPromise = null;
}

async function buildTargetArchitectureProjectionOnce() {
  const ledger = await loadPolicyEngineLedger();
  return buildTargetArchitectureProjection(
    withResolvedOutcomes(FORECAST_CELLS, ledger),
    ledger,
  );
}
