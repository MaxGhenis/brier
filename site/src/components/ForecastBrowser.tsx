"use client";

import type { ReactNode } from "react";
import { useMemo, useState } from "react";
import {
  COUNTRY_LABEL,
  TYPE_LABEL,
  TYPE_DESCRIPTION,
  getForecastCountry,
  type CountryCode,
  type ForecastCell,
  type ForecastCellType,
} from "@/data/forecast-cells";
import { ForecastCard } from "./ForecastCard";

type Filter = "all" | ForecastCellType;
type CountryFilter = "all" | CountryCode;

interface ForecastBrowserProps {
  forecasts: ForecastCell[];
}

const FILTERS: { key: Filter; label: string; description: string }[] = [
  {
    key: "all",
    label: "All forecasts",
    description: "All three forecast types.",
  },
  {
    key: "data",
    label: TYPE_LABEL.data + " cells",
    description: TYPE_DESCRIPTION.data,
  },
  {
    key: "policy",
    label: TYPE_LABEL.policy + " parameters",
    description: TYPE_DESCRIPTION.policy,
  },
  {
    key: "conditional",
    label: TYPE_LABEL.conditional,
    description: TYPE_DESCRIPTION.conditional,
  },
];

const COUNTRY_FILTERS: { key: CountryFilter; label: string }[] = [
  { key: "all", label: "All geographies" },
  { key: "US", label: COUNTRY_LABEL.US },
  { key: "UK", label: COUNTRY_LABEL.UK },
  { key: "CA", label: COUNTRY_LABEL.CA },
  { key: "AU", label: COUNTRY_LABEL.AU },
  { key: "EA", label: COUNTRY_LABEL.EA },
  { key: "JP", label: COUNTRY_LABEL.JP },
  { key: "BE", label: COUNTRY_LABEL.BE },
];

export function ForecastBrowser({ forecasts }: ForecastBrowserProps) {
  const [filter, setFilter] = useState<Filter>("all");
  const [countryFilter, setCountryFilter] = useState<CountryFilter>("all");
  const sortedForecasts = useMemo(
    () => [...forecasts].sort(compareByResolutionDate),
    [forecasts],
  );
  const filtered = useMemo(
    () => filterForecasts(sortedForecasts, filter, countryFilter),
    [filter, countryFilter, sortedForecasts],
  );
  const description =
    FILTERS.find((f) => f.key === filter)?.description ??
    FILTERS[0].description;

  return (
    <div>
      <div className="mb-6 grid gap-3">
        <FilterBar>
          {COUNTRY_FILTERS.map((f) => (
            <FilterButton
              key={f.key}
              active={countryFilter === f.key}
              count={countForecasts(sortedForecasts, filter, f.key)}
              label={f.label}
              onClick={() => setCountryFilter(f.key)}
            />
          ))}
        </FilterBar>
        <FilterBar>
          {FILTERS.map((f) => (
            <FilterButton
              key={f.key}
              active={filter === f.key}
              count={countForecasts(sortedForecasts, f.key, countryFilter)}
              label={f.label}
              onClick={() => setFilter(f.key)}
            />
          ))}
        </FilterBar>
      </div>
      <p className="mb-8 max-w-[640px] text-[0.9rem] text-[var(--theme-text-muted)]">
        {description} Showing {filtered.length} predictions, sorted by earliest
        expected resolution.
      </p>
      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map((forecast: ForecastCell) => (
          <ForecastCard key={forecast.slug} forecast={forecast} />
        ))}
      </div>
    </div>
  );
}

function FilterBar({ children }: { children: ReactNode }) {
  return (
    <div
      className="flex flex-wrap items-center gap-1 rounded-xl border bg-[var(--theme-bg-elevated)] p-1.5"
      style={{ borderColor: "var(--theme-border)" }}
    >
      {children}
    </div>
  );
}

function FilterButton({
  active,
  count,
  label,
  onClick,
}: {
  active: boolean;
  count: number;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 rounded-lg px-3 py-1.5 [font-family:var(--font-body)] text-[0.85rem] transition-colors ${
        active
          ? "bg-[var(--theme-text)] text-[var(--theme-bg)]"
          : "text-[var(--theme-text-muted)] hover:text-[var(--theme-text)]"
      }`}
    >
      <span>{label}</span>
      <span
        className={`[font-family:var(--font-mono)] text-[0.7rem] ${
          active ? "opacity-80" : "text-[var(--theme-text-dim)]"
        }`}
      >
        {count}
      </span>
    </button>
  );
}

function countForecasts(
  forecasts: ForecastCell[],
  filter: Filter,
  countryFilter: CountryFilter,
) {
  return filterForecasts(forecasts, filter, countryFilter).length;
}

function filterForecasts(
  forecasts: ForecastCell[],
  filter: Filter,
  countryFilter: CountryFilter,
) {
  return forecasts.filter((forecast) => {
    const matchesType = filter === "all" || forecast.type === filter;
    const matchesCountry =
      countryFilter === "all" || getForecastCountry(forecast) === countryFilter;
    return matchesType && matchesCountry;
  });
}

function compareByResolutionDate(a: ForecastCell, b: ForecastCell): number {
  return (
    new Date(a.resolutionDate).getTime() - new Date(b.resolutionDate).getTime()
  );
}
