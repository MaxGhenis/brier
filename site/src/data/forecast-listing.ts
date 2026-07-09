import {
  formatValue,
  getForecastCountry,
  type CountryCode,
  type ForecastCell,
  type ForecastCellType,
} from "./forecast-cells";

/** The only catalog fields allowed across the /forecasts page boundary. */
export interface ForecastListingItem {
  slug: string;
  title: string;
  point: { value: number; label: string };
  interval: {
    lower: { value: number; label: string };
    upper: { value: number; label: string };
  };
  resolutionDate: string;
  status: "pending" | "resolved";
  country: CountryCode;
  type: ForecastCellType;
}

export function buildForecastListing(
  forecasts: ForecastCell[],
): ForecastListingItem[] {
  return forecasts.map((forecast) => ({
    slug: forecast.slug,
    title: forecast.title,
    point: {
      value: forecast.pointEstimate,
      label: formatValue(forecast.pointEstimate, forecast.unit),
    },
    interval: {
      lower: {
        value: forecast.ciLow,
        label: formatValue(forecast.ciLow, forecast.unit),
      },
      upper: {
        value: forecast.ciHigh,
        label: formatValue(forecast.ciHigh, forecast.unit),
      },
    },
    resolutionDate: forecast.resolutionDate,
    status: forecast.resolvedOutcome ? "resolved" : "pending",
    country: getForecastCountry(forecast),
    type: forecast.type,
  }));
}
