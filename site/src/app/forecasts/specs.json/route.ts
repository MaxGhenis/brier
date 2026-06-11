import { FORECAST_CELLS } from "@/data/forecast-cells";
import { buildPredictionSpecExport } from "@/data/prediction-specs";

export const dynamic = "force-static";

export function GET() {
  return Response.json(buildPredictionSpecExport(FORECAST_CELLS));
}
