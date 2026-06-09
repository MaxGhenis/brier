import { formatValue, type Unit } from "@/data/markets";

interface ForecastVizProps {
  point: number;
  ciLow: number;
  ciHigh: number;
  unit: Unit;
  history?: { label: string; value: number }[];
  size?: "compact" | "full";
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
        <div className="mt-1 flex justify-between [font-family:var(--font-mono)] text-[0.62rem] text-[var(--theme-text-dim)]">
          <span>{formatValue(ciLow, unit)}</span>
          <span className="text-[var(--color-accent)] font-medium">
            {formatValue(point, unit)}
          </span>
          <span>{formatValue(ciHigh, unit)}</span>
        </div>
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
      <div className="mt-2 flex justify-between [font-family:var(--font-mono)] text-[0.7rem] text-[var(--theme-text-dim)]">
        <span>{formatValue(ciLow, unit)}</span>
        <span className="text-[var(--color-accent)] font-medium">
          {formatValue(point, unit)}
        </span>
        <span>{formatValue(ciHigh, unit)}</span>
      </div>
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
