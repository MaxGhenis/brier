import Link from "next/link";
import {
  TYPE_DESCRIPTION,
  TYPE_LABEL,
  type ForecastCellType,
} from "@/data/forecast-cells";
import type { ForecastListingItem } from "@/data/forecast-listing";
import { ForecastCard } from "./ForecastCard";

interface ForecastBrowserProps {
  forecasts: ForecastListingItem[];
}

const SECTIONS: {
  key: ForecastCellType;
  label: string;
  description: string;
}[] = [
  {
    key: "data",
    label: `${TYPE_LABEL.data} cells`,
    description: TYPE_DESCRIPTION.data,
  },
  {
    key: "policy",
    label: `${TYPE_LABEL.policy} parameters`,
    description: TYPE_DESCRIPTION.policy,
  },
  {
    key: "conditional",
    label: TYPE_LABEL.conditional,
    description: TYPE_DESCRIPTION.conditional,
  },
];

export function ForecastBrowser({ forecasts }: ForecastBrowserProps) {
  const sortedForecasts = [...forecasts].sort(compareByResolutionDate);

  return (
    <div>
      <nav
        aria-label="Forecast sections"
        className="mb-8 flex flex-wrap items-center gap-1 rounded-xl border bg-[var(--theme-bg-elevated)] p-1.5"
        style={{ borderColor: "var(--theme-border)" }}
      >
        {SECTIONS.map((section) => (
          <Link
            key={section.key}
            href={`#${section.key}-forecasts`}
            className="flex items-center gap-2 rounded-lg px-3 py-1.5 [font-family:var(--font-body)] text-[0.85rem] text-[var(--theme-text-muted)] no-underline transition-colors hover:text-[var(--theme-text)] hover:no-underline"
          >
            <span>{section.label}</span>
            <span className="[font-family:var(--font-mono)] text-[0.7rem] text-[var(--theme-text-dim)]">
              {
                sortedForecasts.filter(
                  (forecast) => forecast.type === section.key,
                ).length
              }
            </span>
          </Link>
        ))}
      </nav>

      {SECTIONS.map((section) => {
        const sectionForecasts = sortedForecasts.filter(
          (forecast) => forecast.type === section.key,
        );
        return (
          <section
            className="mb-14 scroll-mt-6"
            id={`${section.key}-forecasts`}
            key={section.key}
          >
            <div className="mb-6 max-w-[680px]">
              <h2 className="mb-2 [font-family:var(--font-display)] text-[1.25rem] font-semibold tracking-[-0.01em] text-[var(--theme-text)]">
                {section.label}
              </h2>
              <p className="text-[0.9rem] text-[var(--theme-text-muted)]">
                {section.description} Showing {sectionForecasts.length}
                predictions, sorted by earliest expected resolution.
              </p>
            </div>
            <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
              {sectionForecasts.map((forecast) => (
                <ForecastCard key={forecast.slug} forecast={forecast} />
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}

function compareByResolutionDate(
  a: ForecastListingItem,
  b: ForecastListingItem,
) {
  return a.resolutionDate.localeCompare(b.resolutionDate);
}
