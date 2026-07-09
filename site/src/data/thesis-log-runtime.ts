import { FORECAST_CELLS } from "./forecast-cells";
import {
  buildThesisLogData,
  loadPolicyEngineLedger,
  withResolvedOutcomes,
  type ThesisLogData,
} from "./thesis-log";

let thesisLogDataPromise: Promise<ThesisLogData> | null = null;

/** Share one expensive log projection across all static manifest/chunk routes. */
export function loadThesisLogData(): Promise<ThesisLogData> {
  thesisLogDataPromise ??= buildThesisLogDataOnce();
  return thesisLogDataPromise;
}

export function resetThesisLogDataCache() {
  thesisLogDataPromise = null;
}

async function buildThesisLogDataOnce(): Promise<ThesisLogData> {
  const ledger = await loadPolicyEngineLedger();
  return buildThesisLogData(
    withResolvedOutcomes(FORECAST_CELLS, ledger),
    ledger,
  );
}
