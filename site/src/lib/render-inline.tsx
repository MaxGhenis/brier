import type { ReactNode } from "react";

/** Render the light markdown the analysis text uses: **bold** and `code`. */
export function renderInline(text: string): ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={i}
          className="[font-family:var(--font-mono)] text-[0.82em] text-[var(--theme-text)]"
        >
          {part.slice(1, -1)}
        </code>
      );
    }
    return part;
  });
}

/**
 * Drop the analysis-day registry note some ported metric texts end with
 * ("**Registry: … Not yet in Thesis …**") — the live badge on the card
 * states the same thing. Render-time only; the artifact stays verbatim.
 */
export function stripRegistryNote(text: string): string {
  return text
    .replace(/\s*\*\*Registry:[^*]*\*\*\.?\s*$/i, "")
    .replace(/\s*Registry:[^.]*\.\s*$/i, "")
    .trim();
}
