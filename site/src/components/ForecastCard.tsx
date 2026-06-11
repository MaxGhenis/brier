import Link from "next/link";
import {
  type ForecastCell,
  COUNTRY_LABEL,
  TYPE_LABEL,
  formatValue,
  getForecastCountry,
  getResolutionResult,
  getForecastRuntimeKind,
  getForecastRuntimeLabel,
} from "@/data/forecast-cells";
import { ForecastViz } from "./ForecastViz";

const typeBadgeClass: Record<ForecastCell["type"], string> = {
  data: "bg-[var(--color-mist-100)] text-[var(--color-horizon-700)] border-[var(--color-mist-200)]",
  policy:
    "bg-[var(--color-accent-subtle)] text-[var(--color-rose-700)] border-[var(--color-rose-100)]",
  conditional: "bg-[#FFF4DD] text-[#7A5C20] border-[#F2DCAF]",
};

interface ForecastCardProps {
  forecast: ForecastCell;
}

export function ForecastCard({ forecast }: ForecastCardProps) {
  const resolutionLabel = formatResolutionLabel(forecast.resolutionDate);
  const runtimeKind = getForecastRuntimeKind(forecast);
  const country = getForecastCountry(forecast);
  const resolutionResult = getResolutionResult(forecast);
  return (
    <Link
      href={`/${forecast.slug}`}
      className="group flex flex-col gap-4 rounded-xl border bg-[var(--theme-bg-elevated)] p-6 no-underline transition-all duration-200 hover:no-underline hover:translate-y-[-2px] hover:shadow-md"
      style={{
        borderColor: "var(--theme-border)",
        color: "var(--theme-text)",
      }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-wrap gap-2">
          <span
            className={`inline-block rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] ${typeBadgeClass[forecast.type]}`}
          >
            {TYPE_LABEL[forecast.type]}
          </span>
          <span className="inline-block rounded-full border border-[var(--theme-border)] bg-[var(--theme-bg-surface)] px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            {COUNTRY_LABEL[country]}
          </span>
          <span
            className={`inline-block rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] ${
              runtimeKind === "live-api"
                ? "border-[var(--color-horizon-300)] bg-[var(--color-horizon-50)] text-[var(--color-horizon-700)]"
                : runtimeKind === "agent-run"
                  ? "border-[var(--color-rose-100)] bg-[var(--color-accent-subtle)] text-[var(--color-rose-700)]"
                  : "border-[var(--theme-border)] bg-[var(--theme-bg-surface)] text-[var(--theme-text-dim)]"
            }`}
          >
            {getForecastRuntimeLabel(forecast)}
          </span>
          {forecast.series && (
            <span className="inline-block rounded-full border border-[var(--theme-border)] bg-[var(--theme-bg-surface)] px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              {forecast.series.cadence} · {forecast.series.horizonLabel}
            </span>
          )}
          {forecast.resolvedOutcome && (
            <span
              className={`inline-block rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] ${
                resolutionResult === "inside"
                  ? "border-[var(--color-horizon-300)] bg-[var(--color-horizon-50)] text-[var(--color-horizon-700)]"
                  : "border-[#F2DCAF] bg-[#FFF4DD] text-[#7A5C20]"
              }`}
            >
              Resolved
            </span>
          )}
        </div>
        <span className="[font-family:var(--font-mono)] text-[0.62rem] text-[var(--theme-text-dim)]">
          {forecast.resolvedOutcome ? "resolved" : "resolves"} {resolutionLabel}
        </span>
      </div>
      <h3 className="[font-family:var(--font-display)] text-[1.05rem] font-semibold leading-[1.3] tracking-[-0.01em] text-[var(--theme-text)] group-hover:text-[var(--color-accent)] transition-colors">
        {forecast.title}
      </h3>
      <div className="mt-auto">
        <div className="mb-2 flex items-baseline justify-between">
          <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            forecast · 80% CI
          </span>
          <span className="[font-family:var(--font-display)] text-[1.15rem] font-semibold text-[var(--color-accent)]">
            {formatValue(forecast.pointEstimate, forecast.unit)}
          </span>
        </div>
        <ForecastViz
          point={forecast.pointEstimate}
          ciLow={forecast.ciLow}
          ciHigh={forecast.ciHigh}
          unit={forecast.unit}
          size="compact"
        />
        {forecast.resolvedOutcome && (
          <div className="mt-2 flex items-center justify-between gap-3 [font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.08em]">
            <span className="text-[var(--theme-text-dim)]">
              actual{" "}
              <span className="text-[var(--theme-text)]">
                {formatValue(forecast.resolvedOutcome.value, forecast.unit)}
              </span>
            </span>
            <span
              className={
                resolutionResult === "inside"
                  ? "text-[var(--color-horizon-700)]"
                  : "text-[#7A5C20]"
              }
            >
              {resolutionResult === "inside" ? "inside CI" : "outside CI"}
            </span>
          </div>
        )}
      </div>
    </Link>
  );
}

function formatResolutionLabel(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", year: "numeric" });
}
