"use client";

import { useId, useState } from "react";
import type { TaskComparison } from "@/data/generated/thesis-lab";
import { deriveDensity } from "./density";
import { number, unit } from "./lab-ui";

/** Draw the sealed CDF or a binned density. Scores and quantiles come from the API. */
export function CdfChart({
  comparisons,
  outcome,
  unitName,
}: {
  comparisons: readonly TaskComparison[];
  outcome: number | null;
  unitName: string;
}) {
  const titleId = useId();
  const descriptionId = useId();
  const [focused, setFocused] = useState<string | null>(null);
  const [view, setView] = useState<"cdf" | "pdf">("cdf");
  const curves = comparisons.filter((row) => row.distribution !== null);
  if (curves.length === 0)
    return (
      <div className="lab-notice">
        No selected distribution is available for the loaded methods.
      </div>
    );
  let min = outcome ?? Infinity;
  let max = outcome ?? -Infinity;
  for (const row of curves)
    for (const point of row.distribution!.points) {
      min = Math.min(min, point.value);
      max = Math.max(max, point.value);
    }
  const padding = (max - min) * 0.035 || 1;
  const lower = min - padding;
  const upper = max + padding;
  const x = (value: number) => 68 + ((value - lower) / (upper - lower)) * 824;
  const densities = curves.map((row) =>
    deriveDensity(row.distribution!.points, 5),
  );
  const densityMax = densities.reduce(
    (peak, intervals) =>
      intervals?.reduce((max, p) => Math.max(max, p.density), peak) ?? peak,
    0,
  );
  const yMax = view === "pdf" && densityMax > 0 ? densityMax : 1;
  const y = (value: number) => 310 - (value / yMax) * 276;
  const densityUnit =
    unitName === "percent" ? "percentage point" : unit(unitName);
  return (
    <figure className="lab-chart">
      <div className="lab-chart-toolbar">
        <span>
          {view === "cdf"
            ? "Cumulative probability"
            : `Binned density · per ${densityUnit}`}
        </span>
        <div
          className="lab-chart-toggle"
          role="group"
          aria-label="Distribution view"
        >
          {(["cdf", "pdf"] as const).map((mode) => (
            <button
              key={mode}
              type="button"
              aria-pressed={view === mode}
              onClick={() => setView(mode)}
              title={
                mode === "cdf"
                  ? "Cumulative distribution function"
                  : "Probability density function"
              }
            >
              {mode.toUpperCase()}
            </button>
          ))}
        </div>
      </div>
      <svg
        role="img"
        aria-labelledby={`${titleId} ${descriptionId}`}
        viewBox="0 0 940 366"
      >
        <title id={titleId}>
          {view === "cdf"
            ? "Forecast cumulative distributions"
            : "Forecast probability densities"}
        </title>
        <desc id={descriptionId}>
          {view === "cdf"
            ? "Each curve plots all 201 original CDF points. The vertical axis is the probability the outcome is at or below the horizontal value."
            : `An approximate density in 40 bins, each averaging five adjacent CDF intervals to reduce rounding noise. Every bin preserves the probability between its stored endpoints. The vertical axis is density per ${densityUnit}.`}{" "}
          {curves.length} loaded methods.
          {outcome !== null && ` Official outcome: ${outcome} ${unitName}.`}
        </desc>
        {[0, 0.25, 0.5, 0.75, 1].map((p) => (
          <g key={p}>
            <line
              x1="68"
              x2="892"
              y1={y(p * yMax)}
              y2={y(p * yMax)}
              className="lab-chart-grid"
            />
            <text x="52" y={y(p * yMax) + 4} textAnchor="end">
              {view === "cdf" ? `${p * 100}%` : densityTick(p * yMax)}
            </text>
          </g>
        ))}
        {[0, 0.25, 0.5, 0.75, 1].map((share) => {
          const value = lower + share * (upper - lower);
          return (
            <text key={share} x={x(value)} y="338" textAnchor="middle">
              {number(value, 2)}
            </text>
          );
        })}
        <text x="480" y="362" textAnchor="middle">
          {unit(unitName)}
        </text>
        {curves.map((row, i) => {
          const intervals = densities[i];
          if (view === "pdf" && !intervals) return null;
          const path =
            view === "cdf"
              ? row
                  .distribution!.points.map(
                    (point, index) =>
                      `${index === 0 ? "M" : "L"}${x(point.value).toFixed(4)},${y(point.probability).toFixed(4)}`,
                  )
                  .join(" ")
              : [
                  `M${x(intervals![0].lower).toFixed(4)},${y(0).toFixed(4)}`,
                  ...intervals!.flatMap((interval) => [
                    `L${x(interval.lower).toFixed(4)},${y(interval.density).toFixed(4)}`,
                    `L${x(interval.upper).toFixed(4)},${y(interval.density).toFixed(4)}`,
                  ]),
                  `L${x(intervals!.at(-1)!.upper).toFixed(4)},${y(0).toFixed(4)}`,
                ].join(" ");
          return (
            <path
              key={row.task.id}
              data-testid={`${view}-${row.task.id}`}
              data-point-count={row.distribution!.points.length}
              data-segment-count={
                view === "pdf" ? intervals!.length : undefined
              }
              d={path}
              fill={view === "pdf" && !row.is_baseline ? "#783d68" : "none"}
              fillOpacity={0.07}
              stroke={row.is_baseline ? "#797780" : "#783d68"}
              strokeWidth={
                focused === row.task.id ? 3.5 : view === "pdf" ? 1.6 : 2.4
              }
              strokeDasharray={
                row.is_baseline ? "5 5" : i > 1 ? `${4 + i * 2} 3` : undefined
              }
              opacity={focused !== null && focused !== row.task.id ? 0.23 : 1}
              className="lab-curve"
            />
          );
        })}
        {outcome !== null && (
          <g>
            <line
              x1={x(outcome)}
              x2={x(outcome)}
              y1="24"
              y2="310"
              className="lab-outcome-line"
            />
            <text x={x(outcome)} y="16" textAnchor="middle">
              Observed {number(outcome)}
            </text>
          </g>
        )}
      </svg>
      {view === "pdf" &&
        curves.map(
          (row, i) =>
            densities[i] === null && (
              <p className="lab-notice" key={row.task.id}>
                {row.agent.label}: density is unavailable at this numeric scale.
                View the CDF.
              </p>
            ),
        )}
      <figcaption>
        <div className="lab-chart-legend">
          {curves.map((row, i) => (
            <button
              key={row.task.id}
              type="button"
              onMouseEnter={() => setFocused(row.task.id)}
              onMouseLeave={() => setFocused(null)}
              onFocus={() => setFocused(row.task.id)}
              onBlur={() => setFocused(null)}
              aria-label={`Emphasize ${row.agent.label}`}
            >
              <span
                className={
                  row.is_baseline
                    ? "lab-legend-line lab-baseline"
                    : "lab-legend-line"
                }
                style={i > 1 ? { borderTopStyle: "dashed" } : undefined}
              />
              {row.agent.label}
              {row.is_baseline && <small>baseline</small>}
            </button>
          ))}
        </div>
        <p>
          {view === "cdf"
            ? "Original 201-point distributions"
            : "40 bins · approximate density · each bin preserves its probability"}{" "}
          · {curves.length} loaded methods
        </p>
      </figcaption>
    </figure>
  );
}

function densityTick(value: number): string {
  if (value === 0) return "0";
  return value < 0.001 || value >= 1000
    ? value.toExponential(1)
    : String(Number(value.toPrecision(3)));
}
