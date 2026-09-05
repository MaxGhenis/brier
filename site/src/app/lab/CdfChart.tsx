"use client";

import { useId, useState } from "react";
import type { TaskComparison } from "@/data/generated/thesis-lab";
import { number, unit } from "./lab-ui";

/** Draw every sealed point. Quantiles and scientific scores are supplied by the API. */
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
  const y = (value: number) => 310 - value * 276;
  return (
    <figure className="lab-chart">
      <svg
        role="img"
        aria-labelledby={`${titleId} ${descriptionId}`}
        viewBox="0 0 940 366"
      >
        <title id={titleId}>Forecast cumulative distributions</title>
        <desc id={descriptionId}>
          Each curve plots all 201 original CDF points. The vertical axis is the
          probability the outcome is at or below the horizontal value.{" "}
          {curves.length} loaded methods.
          {outcome !== null && ` Official outcome: ${outcome} ${unitName}.`}
        </desc>
        {[0, 0.25, 0.5, 0.75, 1].map((p) => (
          <g key={p}>
            <line
              x1="68"
              x2="892"
              y1={y(p)}
              y2={y(p)}
              className="lab-chart-grid"
            />
            <text x="52" y={y(p) + 4} textAnchor="end">
              {p * 100}%
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
        {curves.map((row, i) => (
          <path
            key={row.task.id}
            data-testid={`cdf-${row.task.id}`}
            data-point-count={row.distribution!.points.length}
            d={row
              .distribution!.points.map(
                (point, index) =>
                  `${index === 0 ? "M" : "L"}${x(point.value).toFixed(4)},${y(point.probability).toFixed(4)}`,
              )
              .join(" ")}
            fill="none"
            stroke={row.is_baseline ? "#797780" : "#783d68"}
            strokeWidth={focused === row.task.id ? 3.5 : 2.4}
            strokeDasharray={
              row.is_baseline ? "5 5" : i > 1 ? `${4 + i * 2} 3` : undefined
            }
            opacity={focused !== null && focused !== row.task.id ? 0.23 : 1}
            className="lab-curve"
          />
        ))}
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
          Cumulative probability · original 201-point distributions ·{" "}
          {curves.length} loaded methods
        </p>
      </figcaption>
    </figure>
  );
}
