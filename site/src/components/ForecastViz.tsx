import { formatValue, type Unit } from "@/data/forecast-cells";

type HistoricalPoint = { label: string; value: number };

interface ForecastVizProps {
  point: number;
  ciLow: number;
  ciHigh: number;
  unit: Unit;
  history?: HistoricalPoint[];
  size?: "compact" | "full";
}

interface ForecastTrendProps {
  point: number;
  ciLow: number;
  ciHigh: number;
  unit: Unit;
  history: HistoricalPoint[];
  targetLabel: string;
  actual?: {
    label: string;
    value: number;
  };
}

/**
 * CI-and-density visualization for a forecast.
 *
 * "compact" mode draws a horizontal range bar suitable for a card.
 * "full" mode draws a wider range bar with axis ticks, historical anchors,
 * and a normal-shaped density underlay.
 */
export function ForecastViz({
  point,
  ciLow,
  ciHigh,
  unit,
  history,
  size = "full",
}: ForecastVizProps) {
  const allValues = [
    ciLow,
    ciHigh,
    point,
    ...(history?.map((h) => h.value) ?? []),
  ];
  const dataMin = Math.min(...allValues);
  const dataMax = Math.max(...allValues);
  const pad = (dataMax - dataMin) * 0.18 || Math.abs(point) * 0.1 || 1;
  const min = dataMin - pad;
  const max = dataMax + pad;
  const span = max - min || 1;

  const pct = (v: number) => ((v - min) / span) * 100;
  // Labels sit at the true axis position of the value they name. The domain
  // is wider than the interval whenever history extends past it, so pinning
  // labels to the edges misplaced them relative to the markers.
  const labelPct = (v: number) => Math.min(94, Math.max(6, pct(v)));

  const axisLabels = (textSize: string) => (
    <div className={`relative mt-1 h-4 w-full [font-family:var(--font-mono)] ${textSize} text-[var(--theme-text-dim)]`}>
      <span
        className="absolute -translate-x-1/2"
        style={{ left: `${labelPct(ciLow)}%` }}
      >
        {formatValue(ciLow, unit)}
      </span>
      <span
        className="absolute -translate-x-1/2 font-medium text-[var(--color-accent)]"
        style={{ left: `${labelPct(point)}%` }}
      >
        {formatValue(point, unit)}
      </span>
      <span
        className="absolute -translate-x-1/2"
        style={{ left: `${labelPct(ciHigh)}%` }}
      >
        {formatValue(ciHigh, unit)}
      </span>
    </div>
  );

  if (size === "compact") {
    return (
      <div className="w-full">
        <div className="relative h-2 w-full rounded-full bg-[var(--theme-bg-surface)]">
          <div
            className="absolute h-2 rounded-full bg-[var(--color-horizon-300)] opacity-70"
            style={{
              left: `${pct(ciLow)}%`,
              width: `${pct(ciHigh) - pct(ciLow)}%`,
            }}
          />
          <div
            className="absolute top-1/2 h-3 w-[2px] -translate-y-1/2 bg-[var(--color-accent)]"
            style={{ left: `${pct(point)}%` }}
          />
        </div>
        {axisLabels("text-[0.62rem]")}
      </div>
    );
  }

  // Full mode: bell curve underlay + range bar + history anchors
  const densityWidth = pct(ciHigh) - pct(ciLow);
  const densityCenter = pct(point);
  const densityPath = buildDensityPath(densityCenter, densityWidth);

  return (
    <div className="w-full">
      <div className="relative h-32 w-full">
        <svg
          viewBox="0 0 100 32"
          preserveAspectRatio="none"
          className="absolute inset-0 h-full w-full"
        >
          <defs>
            <linearGradient id="density-fill" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="var(--color-rose-300)" stopOpacity="0.55" />
              <stop offset="100%" stopColor="var(--color-rose-300)" stopOpacity="0.05" />
            </linearGradient>
          </defs>
          <path
            d={`${densityPath} L 100 32 L 0 32 Z`}
            fill="url(#density-fill)"
          />
          <path
            d={densityPath}
            stroke="var(--color-accent)"
            strokeWidth="0.4"
            fill="none"
          />
          {history?.map((h, i) => (
            <line
              key={i}
              x1={pct(h.value)}
              x2={pct(h.value)}
              y1="22"
              y2="32"
              stroke="var(--color-mist-400)"
              strokeWidth="0.3"
              strokeDasharray="0.5 0.5"
            />
          ))}
          <line
            x1={pct(point)}
            x2={pct(point)}
            y1="2"
            y2="32"
            stroke="var(--color-accent)"
            strokeWidth="0.5"
          />
        </svg>
      </div>
      <div className="relative h-3 w-full rounded-full bg-[var(--theme-bg-surface)]">
        <div
          className="absolute h-3 rounded-full bg-[var(--color-horizon-300)] opacity-70"
          style={{
            left: `${pct(ciLow)}%`,
            width: `${pct(ciHigh) - pct(ciLow)}%`,
          }}
        />
        <div
          className="absolute top-1/2 h-5 w-[3px] -translate-y-1/2 bg-[var(--color-accent)]"
          style={{ left: `${pct(point)}%` }}
        />
        {history?.map((h, i) => (
          <div
            key={i}
            className="absolute top-1/2 h-2 w-[2px] -translate-y-1/2 bg-[var(--color-mist-600)] opacity-70"
            style={{ left: `${pct(h.value)}%` }}
            title={`${h.label}: ${formatValue(h.value, unit)}`}
          />
        ))}
      </div>
      {axisLabels("text-[0.7rem]")}
      {history && history.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-x-4 gap-y-1 [font-family:var(--font-mono)] text-[0.65rem] text-[var(--theme-text-dim)]">
          <span className="text-[var(--theme-text-muted)]">history:</span>
          {history.map((h) => (
            <span key={h.label}>
              {h.label}:{" "}
              <span className="text-[var(--theme-text)]">
                {formatValue(h.value, unit)}
              </span>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function buildDensityPath(center: number, width: number): string {
  // Construct a smooth open bell-curve path in the [0,100] x-range mapped to
  // the CI window; callers close it against the baseline for the area fill.
  const half = Math.max(width / 2, 4);
  const steps = 48;
  const points: [number, number][] = [];
  const peakY = 4;
  const baseY = 32;
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps - 0.5) * 2; // -1..1
    const x = center + t * half * 1.5;
    const y = baseY - (baseY - peakY) * Math.exp(-3 * t * t);
    points.push([x, y]);
  }
  return points
    .map(([x, y], i) => `${i === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`)
    .join(" ");
}

const MONTH_INDEX: Record<string, number> = {
  jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5,
  jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11,
};

/**
 * Best-effort UTC timestamp for a history/target label, for proportional
 * x-axis spacing. Returns null when no time token is recognizable; callers
 * fall back to index spacing, so a miss can never break a chart. Anchors
 * are period midpoints (month → 15th, FY → Apr 1, SY → Jan 15) — only
 * monotone, roughly proportional placement matters.
 */
export function parseTimelineLabel(label: string): number | null {
  const text = label.trim();
  let match = /(\d{4})-(\d{2})-(\d{2})/.exec(text);
  if (match) return Date.UTC(+match[1], +match[2] - 1, +match[3]);
  match = /(\d{4})[ -]?Q([1-4])/i.exec(text);
  if (match) return Date.UTC(+match[1], (+match[2] - 1) * 3 + 1, 15);
  match = /Q([1-4])[ -]?(\d{4})/i.exec(text);
  if (match) return Date.UTC(+match[2], (+match[1] - 1) * 3 + 1, 15);
  match = /(\d{4})-(\d{2})(?!\d)/.exec(text);
  if (match && +match[2] >= 1 && +match[2] <= 12) {
    return Date.UTC(+match[1], +match[2] - 1, 15);
  }
  match =
    /(?:(\d{1,2})\s+)?(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{4})/i.exec(
      text,
    );
  if (match) {
    return Date.UTC(
      +match[3],
      MONTH_INDEX[match[2].slice(0, 3).toLowerCase()],
      match[1] ? +match[1] : 15,
    );
  }
  match = /^(\d{2})\/(\d{2})$/.exec(text);
  if (match && +match[1] >= 1 && +match[1] <= 12) {
    return Date.UTC(2000 + +match[2], +match[1] - 1, 15);
  }
  match = /SY\s?(\d{4})[-–_]\d{2,4}/i.exec(text);
  if (match) return Date.UTC(+match[1] + 1, 0, 15);
  match = /FY\s?(\d{4})/i.exec(text);
  if (match) return Date.UTC(+match[1], 3, 1);
  match = /^(\d{4})\b/.exec(text);
  if (match) return Date.UTC(+match[1], 6, 1);
  return null;
}

export function ForecastTrend({
  actual,
  ciHigh,
  ciLow,
  history,
  point,
  targetLabel,
  unit,
}: ForecastTrendProps) {
  if (history.length === 0) return null;

  const yValues = [
    ...history.map((item) => item.value),
    point,
    ciLow,
    ciHigh,
    ...(actual ? [actual.value] : []),
  ];
  const yMin = Math.min(...yValues);
  const yMax = Math.max(...yValues);
  const yPad = (yMax - yMin) * 0.16 || Math.abs(point) * 0.1 || 1;
  const min = yMin - yPad;
  const max = yMax + yPad;
  const span = max - min || 1;

  const width = 640;
  const height = 248;
  const margin = { top: 22, right: 30, bottom: 54, left: 62 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const forecastIndex = history.length;
  const denominator = Math.max(forecastIndex, 1);
  // Space the x-axis proportionally to time when every label carries a
  // recognizable time token and the sequence strictly increases toward the
  // target; otherwise keep index spacing (uneven history gaps — FY2019 to
  // FY2022 to FY2023 — previously drew as equal steps).
  const times = [...history.map((item) => parseTimelineLabel(item.label))];
  const targetTime = parseTimelineLabel(targetLabel);
  const timeline = [...times, targetTime];
  const proportional =
    targetTime !== null &&
    times.every((time) => time !== null) &&
    timeline.every(
      (time, index) => index === 0 || (time as number) > (timeline[index - 1] as number),
    );
  const x = (index: number) => {
    if (proportional) {
      const t0 = timeline[0] as number;
      const t1 = targetTime as number;
      const t = timeline[index] as number;
      return margin.left + (plotWidth * (t - t0)) / (t1 - t0);
    }
    return margin.left + (plotWidth * index) / denominator;
  };
  const y = (value: number) =>
    margin.top + plotHeight - ((value - min) / span) * plotHeight;

  const historyPath = history
    .map(
      (item, index) =>
        `${index === 0 ? "M" : "L"} ${x(index).toFixed(1)} ${y(item.value).toFixed(1)}`,
    )
    .join(" ");
  const forecastConnector =
    history.length > 0
      ? `M ${x(history.length - 1).toFixed(1)} ${y(history.at(-1)?.value ?? point).toFixed(1)} L ${x(forecastIndex).toFixed(1)} ${y(point).toFixed(1)}`
      : "";
  const targetX = x(forecastIndex);
  const targetY = y(point);
  const intervalY1 = y(ciHigh);
  const intervalY2 = y(ciLow);
  const yTicks = buildTicks(min, max, 4);

  return (
    <div className="w-full">
      <svg
        role="img"
        aria-label={`Historical trend ending with forecast ${formatValue(point, unit)}`}
        viewBox={`0 0 ${width} ${height}`}
        className="h-auto w-full overflow-visible"
      >
        <line
          x1={margin.left}
          x2={margin.left + plotWidth}
          y1={margin.top + plotHeight}
          y2={margin.top + plotHeight}
          stroke="var(--theme-border)"
          strokeWidth="1"
        />
        {yTicks.map((tick) => (
          <g key={tick}>
            <line
              x1={margin.left}
              x2={margin.left + plotWidth}
              y1={y(tick)}
              y2={y(tick)}
              stroke="var(--theme-border)"
              strokeWidth="1"
              opacity="0.65"
            />
            <text
              x={margin.left - 10}
              y={y(tick) + 4}
              textAnchor="end"
              className="[font-family:var(--font-mono)] text-[11px] fill-[var(--theme-text-dim)]"
            >
              {formatTick(tick, unit)}
            </text>
          </g>
        ))}

        <path
          d={historyPath}
          fill="none"
          stroke="var(--color-horizon-600)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d={forecastConnector}
          fill="none"
          stroke="var(--color-accent)"
          strokeDasharray="6 6"
          strokeLinecap="round"
          strokeWidth="3"
        />

        <line
          x1={targetX}
          x2={targetX}
          y1={intervalY1}
          y2={intervalY2}
          stroke="var(--color-accent)"
          strokeWidth="8"
          strokeLinecap="round"
          opacity="0.2"
        />
        <line
          x1={targetX}
          x2={targetX}
          y1={intervalY1}
          y2={intervalY2}
          stroke="var(--color-accent)"
          strokeWidth="2"
          strokeLinecap="round"
        />

        {history.map((item, index) => (
          <g key={`${item.label}-${index}`}>
            <circle
              cx={x(index)}
              cy={y(item.value)}
              r="4.5"
              fill="var(--theme-bg-elevated)"
              stroke="var(--color-horizon-600)"
              strokeWidth="2"
            />
            {(index === 0 || index === history.length - 1) && (
              <text
                x={x(index)}
                y={margin.top + plotHeight + 25}
                textAnchor={index === 0 ? "start" : "middle"}
                className="[font-family:var(--font-mono)] text-[11px] fill-[var(--theme-text-dim)]"
              >
                {item.label}
              </text>
            )}
          </g>
        ))}

        <circle
          cx={targetX}
          cy={targetY}
          r="6"
          fill="var(--color-accent)"
          stroke="var(--theme-bg-elevated)"
          strokeWidth="2"
        />
        <text
          x={targetX}
          y={margin.top + plotHeight + 25}
          textAnchor="middle"
          className="[font-family:var(--font-mono)] text-[11px] fill-[var(--theme-text-dim)]"
        >
          {targetLabel}
        </text>
        <text
          x={targetX}
          y={Math.max(14, targetY - 12)}
          textAnchor="middle"
          className="[font-family:var(--font-mono)] text-[12px] font-medium fill-[var(--color-accent)]"
        >
          {formatValue(point, unit)}
        </text>

        {actual && (
          <g>
            {/* What actually happened, continuing the history line into the
                target period at the same x as the forecast it grades. */}
            <line
              x1={x(history.length - 1)}
              y1={y(history.at(-1)?.value ?? actual.value)}
              x2={targetX}
              y2={y(actual.value)}
              stroke="var(--color-horizon-600)"
              strokeWidth="3"
              strokeLinecap="round"
            />
            <circle
              cx={targetX}
              cy={y(actual.value)}
              r="5"
              fill="var(--color-horizon-600)"
              stroke="var(--theme-bg-elevated)"
              strokeWidth="2"
            />
            <text
              x={targetX - 12}
              y={y(actual.value) + (y(actual.value) < targetY ? -8 : 14)}
              textAnchor="end"
              className="[font-family:var(--font-mono)] text-[11px] fill-[var(--color-horizon-700)]"
            >
              actual {formatValue(actual.value, unit)}
            </text>
          </g>
        )}
      </svg>

      <div className="mt-2 flex flex-wrap gap-x-5 gap-y-2 [font-family:var(--font-mono)] text-[0.64rem] uppercase tracking-[0.08em] text-[var(--theme-text-dim)]">
        <span className="inline-flex items-center gap-2">
          <span className="h-[2px] w-5 rounded-full bg-[var(--color-horizon-600)]" />
          history
        </span>
        <span className="inline-flex items-center gap-2">
          <span className="h-[2px] w-5 rounded-full border-t-2 border-dashed border-[var(--color-accent)]" />
          forecast path
        </span>
        <span className="inline-flex items-center gap-2">
          <span className="h-4 w-[3px] rounded-full bg-[var(--color-accent)] opacity-70" />
          80% interval
        </span>
        {actual && (
          <span className="inline-flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-[var(--color-horizon-600)]" />
            {actual.label}
          </span>
        )}
      </div>
    </div>
  );
}

function buildTicks(min: number, max: number, count: number): number[] {
  if (count <= 1) return [min];
  return Array.from({ length: count }, (_, index) => {
    const value = min + ((max - min) * index) / (count - 1);
    return Number(value.toPrecision(4));
  });
}

function formatTick(value: number, unit: Unit): string {
  if (unit === "usd" && Math.abs(value) >= 1000) {
    return `$${Math.round(value).toLocaleString()}`;
  }
  if (
    unit === "percent" ||
    unit === "percent_growth" ||
    unit === "ratio" ||
    Math.abs(value) < 10
  ) {
    return Number(value.toFixed(1)).toString();
  }
  return Math.round(value).toLocaleString();
}
