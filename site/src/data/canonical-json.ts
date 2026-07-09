import { createHash } from "node:crypto";

/**
 * Serialize JSON data deterministically using the RFC 8785 ordering rule.
 *
 * Object keys are ordered by their UTF-16 code units (JavaScript's relational
 * string comparison), never by the host locale. Undefined object properties
 * are omitted, matching JSON.stringify. Values that JSON cannot represent are
 * rejected instead of being silently normalized.
 */
export function canonicalStringify(value: unknown): string {
  return serialize(value, new Set<object>());
}

/** Return the full lowercase SHA-256 digest of a canonical JSON value. */
export function sha256Hex(value: unknown): string {
  return createHash("sha256").update(canonicalStringify(value)).digest("hex");
}

function serialize(value: unknown, ancestors: Set<object>): string {
  if (value === null) return "null";

  switch (typeof value) {
    case "string":
    case "boolean":
      return JSON.stringify(value);
    case "number":
      if (!Number.isFinite(value)) {
        throw new TypeError(
          `Canonical JSON cannot serialize non-finite number: ${String(value)}`,
        );
      }
      return JSON.stringify(value);
    case "object":
      break;
    default:
      throw new TypeError(
        `Canonical JSON cannot serialize value of type ${typeof value}`,
      );
  }

  if (ancestors.has(value)) {
    throw new TypeError("Canonical JSON cannot serialize circular structures");
  }
  ancestors.add(value);

  try {
    if (Array.isArray(value)) {
      return `[${value.map((entry) => serialize(entry, ancestors)).join(",")}]`;
    }

    const entries = Object.keys(value)
      .filter((key) => {
        const entryType = typeof (value as Record<string, unknown>)[key];
        return entryType !== "undefined";
      })
      .sort(compareUtf16CodeUnits)
      .map((key) => {
        const entryValue = (value as Record<string, unknown>)[key];
        return `${JSON.stringify(key)}:${serialize(entryValue, ancestors)}`;
      });
    return `{${entries.join(",")}}`;
  } finally {
    ancestors.delete(value);
  }
}

function compareUtf16CodeUnits(left: string, right: string): number {
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}
