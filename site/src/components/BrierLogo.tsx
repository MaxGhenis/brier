/**
 * Brier logo mark — "The Vanishing Point"
 *
 * Two perspective lines converging toward a luminous focal point.
 * Updated for the "Clear Horizon" palette:
 * - Lines use Mist-400 (#9FB6C6) — visible on light backgrounds
 * - Dot uses Rose-600 (#A94E80) — brand accent
 */
export function BrierLogoMark({
  size = 28,
  className = "",
}: {
  size?: number;
  className?: string;
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 28 28"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-label="Thesis"
    >
      {/* Glow halo — rose at low opacity */}
      <circle
        cx="21.5"
        cy="14"
        r="5.5"
        fill="#A94E80"
        opacity="0.10"
      />
      {/* Upper perspective rail */}
      <line
        x1="2"
        y1="4.5"
        x2="17"
        y2="12"
        stroke="#9FB6C6"
        strokeWidth="1.2"
        strokeLinecap="round"
        opacity="0.55"
      />
      {/* Lower perspective rail */}
      <line
        x1="2"
        y1="23.5"
        x2="17"
        y2="16"
        stroke="#9FB6C6"
        strokeWidth="1.5"
        strokeLinecap="round"
        opacity="0.65"
      />
      {/* Focal point — Rose-600 vanishing point */}
      <circle cx="21.5" cy="14" r="3.2" fill="#A94E80" />
    </svg>
  );
}

/**
 * Full wordmark: logo mark + "brier" text.
 * Newsreader SemiBold, lowercase.
 */
export function BrierWordmark({ size = 28 }: { size?: number }) {
  return (
    <span className="inline-flex items-center gap-[0.4em]">
      <BrierLogoMark size={size} />
      <span className="tracking-[0.02em] lowercase">thesis</span>
    </span>
  );
}
