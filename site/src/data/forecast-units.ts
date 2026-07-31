// Unit vocabulary and value formatters, split out of forecast-cells.ts.
//
// These are pure functions over a string union -- no catalog data. They live
// in their own module so that presentation code needing only a formatter
// (ForecastViz) does not transitively import the ~19 MB generated catalog.
// forecast-cells.ts re-exports everything here, so existing importers are
// unaffected.

export type Unit =
  | "count"
  | "percent"
  | "gbp_billions"
  | "usd"
  | "usd_billions"
  | "usd_monthly"
  | "thousands"
  | "millions"
  | "per_1000_live_births"
  | "ratio"
  | "minutes"
  | "percent_growth"
  | "index_points";

export function formatValue(value: number, unit: Unit): string {
  switch (unit) {
    case "count":
      return value.toLocaleString(undefined, { maximumFractionDigits: 0 });
    case "percent":
      return `${formatPercent(value)}%`;
    case "percent_growth":
      return `${value >= 0 ? "+" : ""}${value.toFixed(1)}%`;
    case "gbp_billions":
      return `£${value.toLocaleString(undefined, { maximumFractionDigits: 1 })}B`;
    case "usd":
      if (Math.abs(value) >= 1000) {
        return `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
      }
      return `$${value.toFixed(2)}`;
    case "usd_billions":
      return `$${value.toLocaleString(undefined, { maximumFractionDigits: 1 })}B`;
    case "usd_monthly":
      return `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}/mo`;
    case "thousands":
      if (Math.abs(value) >= 1000) {
        return `${formatScaledThousandsAsMillions(value)}m`;
      }
      return `${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}k`;
    case "millions":
      return `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })}M`;
    case "per_1000_live_births":
      return `${value.toFixed(2)} per 1,000`;
    case "ratio":
      return value.toFixed(2);
    case "index_points":
      // Survey balances (NBB barometer, consumer confidence) print signed.
      return `${value >= 0 ? "+" : ""}${value.toFixed(1)}`;
    case "minutes":
      return `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })} min`;
    default:
      return value.toString();
  }
}

function formatScaledThousandsAsMillions(value: number): string {
  const millions = value / 1000;
  return millions.toLocaleString(undefined, {
    maximumFractionDigits: 2,
    minimumFractionDigits: Math.abs(millions) >= 10 ? 2 : 1,
  });
}

function formatPercent(value: number): string {
  const roundedToTenth = Math.round(value * 10) / 10;
  return Math.abs(value - roundedToTenth) < 1e-9
    ? value.toFixed(1)
    : value.toFixed(2);
}

export function formatValueShort(value: number, unit: Unit): string {
  if (unit === "usd" && Math.abs(value) >= 1000) {
    return `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}B`;
  }
  return formatValue(value, unit);
}
