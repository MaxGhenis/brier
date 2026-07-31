"use client";

import { useState } from "react";
import { renderInline } from "@/lib/render-inline";
import type { StanceFold } from "@/lib/stances";

const stanceBadgeClass: Record<string, string> = {
  serves: "border-[#BFE3D2] bg-[#EAF7F0] text-[#1C6B4A]",
  opposes: "border-[#E5C8C0] bg-[#F9EFEC] text-[#93412A]",
  mixed: "border-[#F2DCAF] bg-[#FFF4DD] text-[#7A5C20]",
  orthogonal:
    "border-[var(--theme-border)] bg-transparent text-[var(--theme-text-dim)]",
  counts:
    "border-[var(--theme-border)] bg-transparent text-[var(--theme-text-muted)]",
};

function stanceLabel(stance: StanceFold): string {
  if (stance.kind !== "counts") {
    return stance.kind === "serves"
      ? "Serves confirmed goals"
      : stance.kind === "opposes"
        ? "Opposes confirmed goals"
        : stance.kind === "mixed"
          ? "Mixed vs confirmed goals"
          : "Orthogonal to confirmed goals";
  }
  const parts = [
    stance.serves > 0 ? `${stance.serves} serves` : null,
    stance.opposes > 0 ? `${stance.opposes} opposes` : null,
    stance.orthogonal > 0 ? `${stance.orthogonal} orthogonal` : null,
  ].filter(Boolean);
  return parts.length > 0 ? parts.join(" · ") : "No goals in force";
}

/**
 * Candidate-metric card with the long sourcing note clamped to a few
 * lines; the full text is a click away instead of a wall by default.
 */
export function MetricCard({
  kind,
  text,
  badgeLabel,
  badgeClass,
  rationale,
  stance,
}: {
  kind: string;
  text: string;
  badgeLabel: string;
  badgeClass: string;
  rationale?: string;
  stance?: StanceFold | null;
}) {
  const [expanded, setExpanded] = useState(false);
  const isLong = text.length > 220;

  return (
    <div className="rounded-lg border border-[var(--theme-border)] bg-[var(--theme-surface)] p-4">
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <span
          className={`inline-block rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] ${badgeClass}`}
        >
          {badgeLabel}
        </span>
        {stance && (
          <span
            className={`inline-block rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] ${stanceBadgeClass[stance.kind]}`}
          >
            {stanceLabel(stance)}
          </span>
        )}
        <span className="[font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] text-[var(--theme-text-dim)]">
          {kind}
        </span>
      </div>
      <p
        className={`m-0 text-[0.88rem] leading-[1.6] text-[var(--theme-text-muted)] ${
          isLong && !expanded ? "line-clamp-3" : ""
        }`}
      >
        {renderInline(text)}
      </p>
      {isLong && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="mt-2 cursor-pointer border-0 bg-transparent p-0 [font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.1em] text-[var(--color-accent)] hover:underline"
        >
          {expanded ? "Less ↑" : "Full sourcing ↓"}
        </button>
      )}
      {rationale && (
        <details className="mt-3 border-t border-[var(--theme-border)] pt-3">
          <summary className="cursor-pointer list-none [font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)] hover:text-[var(--color-accent)] [&::-webkit-details-marker]:hidden">
            Why this metric ▸
          </summary>
          <p className="mb-0 mt-2 text-[0.85rem] leading-[1.6] text-[var(--theme-text-muted)]">
            {renderInline(rationale)}
          </p>
        </details>
      )}
    </div>
  );
}
