import {
  coverageCurve,
  pitHistogram,
  type CoveragePoint,
} from "@/data/calibration-curve";

/**
 * Server-rendered calibration graphics: a coverage curve (stated central
 * interval vs share of outcomes inside, against the diagonal) and one PIT
 * histogram per chronology tier. Same conventions as ForecastViz: accent
 * for the headline series, horizon-600 for the tier below it, recessive
 * theme-border grid, mono labels, native <title> tooltips.
 */

const WIDTH = 480;
const HEIGHT = 340;
const PAD = { top: 16, right: 18, bottom: 44, left: 52 };
const PLOT_W = WIDTH - PAD.left - PAD.right;
const PLOT_H = HEIGHT - PAD.top - PAD.bottom;

const toX = (value: number) => PAD.left + value * PLOT_W;
const toY = (value: number) => PAD.top + (1 - value) * PLOT_H;

function curvePath(points: CoveragePoint[]): string {
  return points
    .map(
      (point, index) =>
        `${index === 0 ? "M" : "L"}${toX(point.nominal).toFixed(1)} ${toY(point.empirical).toFixed(1)}`,
    )
    .join(" ");
}

function percent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

function CoverageSeries({
  points,
  stroke,
  dashed,
  label,
}: {
  points: CoveragePoint[];
  stroke: string;
  dashed?: boolean;
  label: string;
}) {
  if (points.length === 0 || points[0].n === 0) return null;
  return (
    <g>
      <path
        d={curvePath(points)}
        fill="none"
        stroke={stroke}
        strokeWidth={2}
        strokeDasharray={dashed ? "5 4" : undefined}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {points.map((point) => (
        <circle
          key={point.nominal}
          cx={toX(point.nominal)}
          cy={toY(point.empirical)}
          r={point.nominal === 0.8 ? 5 : 3.5}
          fill={stroke}
          stroke="var(--theme-bg-elevated)"
          strokeWidth={1.5}
        >
          <title>
            {`${label}: ${point.covered} of ${point.n} outcomes (${percent(point.empirical)}) inside the stated ${percent(point.nominal)} central interval`}
          </title>
        </circle>
      ))}
    </g>
  );
}

function PitPanel({
  title,
  pits,
  fill,
  emptyNote,
}: {
  title: string;
  pits: number[];
  fill: string;
  emptyNote: string;
}) {
  const bins = pitHistogram(pits);
  const total = bins.reduce((sum, bin) => sum + bin.count, 0);
  const maxShare = Math.max(...bins.map((bin) => bin.share), 0.15);
  const width = 220;
  const height = 128;
  const pad = { top: 8, right: 6, bottom: 22, left: 6 };
  const plotWidth = width - pad.left - pad.right;
  const plotHeight = height - pad.top - pad.bottom;
  const barWidth = plotWidth / bins.length;
  const uniformY = pad.top + (1 - 0.1 / maxShare) * plotHeight;

  return (
    <div>
      <div
        className="[font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.12em]"
        style={{ color: "var(--theme-text-muted)" }}
      >
        {title}
      </div>
      {total === 0 ? (
        <p
          className="mt-2 max-w-[220px] text-[0.72rem] leading-[1.5]"
          style={{ color: "var(--theme-text-dim)" }}
        >
          {emptyNote}
        </p>
      ) : (
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="mt-1 w-full max-w-[240px]"
          role="img"
          aria-label={`${title}: histogram of ${total} probability integral transforms`}
        >
          <line
            x1={pad.left}
            y1={height - pad.bottom}
            x2={width - pad.right}
            y2={height - pad.bottom}
            stroke="var(--theme-border)"
          />
          {bins.map((bin, index) => {
            const barHeight = (bin.share / maxShare) * plotHeight;
            return (
              <rect
                key={bin.binStart}
                x={pad.left + index * barWidth + 1}
                y={height - pad.bottom - barHeight}
                width={barWidth - 2}
                height={barHeight}
                rx={2}
                fill={fill}
              >
                <title>
                  {`PIT ${bin.binStart.toFixed(1)}–${bin.binEnd.toFixed(1)}: ${bin.count} of ${total} outcomes`}
                </title>
              </rect>
            );
          })}
          <line
            x1={pad.left}
            y1={uniformY}
            x2={width - pad.right}
            y2={uniformY}
            stroke="var(--theme-border-strong)"
            strokeDasharray="3 3"
            strokeWidth={1}
          >
            <title>Uniform reference: a calibrated forecaster fills each bin equally</title>
          </line>
          {[0, 0.5, 1].map((tick) => (
            <text
              key={tick}
              x={pad.left + tick * plotWidth}
              y={height - 6}
              textAnchor={tick === 0 ? "start" : tick === 1 ? "end" : "middle"}
              fontSize={9}
              fill="var(--theme-text-dim)"
              style={{ fontFamily: "var(--font-mono)" }}
            >
              {tick}
            </text>
          ))}
        </svg>
      )}
    </div>
  );
}

export function CalibrationPlot({
  witnessedPits,
  claimedPits,
}: {
  witnessedPits: number[];
  claimedPits: number[];
}) {
  const witnessed = coverageCurve(witnessedPits);
  const claimed = coverageCurve(claimedPits);
  const witnessedN = witnessed[0]?.n ?? 0;
  const claimedN = claimed[0]?.n ?? 0;
  const ticks = [0, 0.2, 0.4, 0.6, 0.8, 1];

  return (
    <div className="flex flex-wrap items-start gap-10">
      <figure className="min-w-[300px] max-w-[520px] flex-1">
        <svg
          viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
          className="w-full"
          role="img"
          aria-label="Coverage curve: stated central interval versus share of outcomes observed inside it, by chronology tier"
        >
          {ticks.map((tick) => (
            <g key={tick}>
              <line
                x1={toX(tick)}
                y1={PAD.top}
                x2={toX(tick)}
                y2={HEIGHT - PAD.bottom}
                stroke="var(--theme-border)"
                strokeWidth={tick === 0 ? 1 : 0.5}
              />
              <line
                x1={PAD.left}
                y1={toY(tick)}
                x2={WIDTH - PAD.right}
                y2={toY(tick)}
                stroke="var(--theme-border)"
                strokeWidth={tick === 0 ? 1 : 0.5}
              />
              <text
                x={toX(tick)}
                y={HEIGHT - PAD.bottom + 16}
                textAnchor="middle"
                fontSize={10}
                fill="var(--theme-text-dim)"
                style={{ fontFamily: "var(--font-mono)" }}
              >
                {percent(tick)}
              </text>
              <text
                x={PAD.left - 8}
                y={toY(tick) + 3}
                textAnchor="end"
                fontSize={10}
                fill="var(--theme-text-dim)"
                style={{ fontFamily: "var(--font-mono)" }}
              >
                {percent(tick)}
              </text>
            </g>
          ))}
          <line
            x1={toX(0)}
            y1={toY(0)}
            x2={toX(1)}
            y2={toY(1)}
            stroke="var(--theme-border-strong)"
            strokeDasharray="4 4"
            strokeWidth={1}
          >
            <title>Perfect calibration: observed coverage equals stated coverage</title>
          </line>
          <line
            x1={toX(0.8)}
            y1={PAD.top}
            x2={toX(0.8)}
            y2={HEIGHT - PAD.bottom}
            stroke="var(--color-mist-400)"
            strokeDasharray="2 4"
            strokeWidth={1}
          />
          <text
            x={toX(0.8)}
            y={PAD.top - 4}
            textAnchor="middle"
            fontSize={9}
            fill="var(--theme-text-dim)"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            elicited 80%
          </text>
          <CoverageSeries
            points={claimed}
            stroke="var(--color-horizon-600)"
            dashed
            label="Claimed-time tier"
          />
          <CoverageSeries
            points={witnessed}
            stroke="var(--color-accent)"
            label="Witness-verified"
          />
          <text
            x={PAD.left + PLOT_W / 2}
            y={HEIGHT - 4}
            textAnchor="middle"
            fontSize={10}
            fill="var(--theme-text-muted)"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            stated central interval
          </text>
          <text
            x={12}
            y={PAD.top + PLOT_H / 2}
            textAnchor="middle"
            fontSize={10}
            fill="var(--theme-text-muted)"
            style={{ fontFamily: "var(--font-mono)" }}
            transform={`rotate(-90 12 ${PAD.top + PLOT_H / 2})`}
          >
            outcomes inside
          </text>
        </svg>
        <figcaption className="mt-2 flex flex-wrap gap-x-6 gap-y-1">
          {[
            {
              label: `Witness-verified (n=${witnessedN})`,
              color: "var(--color-accent)",
              dashed: false,
              show: true,
            },
            {
              label: `Claimed-time tier (n=${claimedN})`,
              color: "var(--color-horizon-600)",
              dashed: true,
              show: true,
            },
          ]
            .filter((entry) => entry.show)
            .map((entry) => (
              <span
                key={entry.label}
                className="inline-flex items-center gap-2 text-[0.72rem]"
                style={{ color: "var(--theme-text-muted)" }}
              >
                <svg viewBox="0 0 24 6" className="h-[6px] w-6">
                  <line
                    x1={1}
                    y1={3}
                    x2={23}
                    y2={3}
                    stroke={entry.color}
                    strokeWidth={2}
                    strokeDasharray={entry.dashed ? "5 4" : undefined}
                    strokeLinecap="round"
                  />
                </svg>
                {entry.label}
              </span>
            ))}
        </figcaption>
      </figure>
      <div className="flex min-w-[220px] flex-col gap-6">
        <PitPanel
          title="PIT — witness-verified"
          pits={witnessedPits}
          fill="var(--color-accent)"
          emptyNote="Fills as custody-v2 runs resolve; the headline tier starts at zero by construction."
        />
        <PitPanel
          title="PIT — claimed-time tier"
          pits={claimedPits}
          fill="var(--color-horizon-600)"
          emptyNote="No claimed-time scores."
        />
      </div>
    </div>
  );
}
