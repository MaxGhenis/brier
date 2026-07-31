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
  const chunks: string[] = [];
  serialize(value, chunks, new Set<object>());
  return chunks.join("");
}

/** Return the full lowercase SHA-256 digest of a canonical JSON value. */
export function sha256Hex(value: unknown): string {
  return createHash("sha256").update(canonicalStringify(value)).digest("hex");
}

// Appends into a shared chunk buffer rather than returning a string per
// node. The returning form rebuilt every nested value into an intermediate
// array and joined string at each level, so a deep object was copied once
// per level of depth. That cost dominated the catalog: projecting the real
// catalog issues ~304k digests over ~135MB of canonical bytes, and
// serialization alone was 63% of the projection's wall time.
//
// The emitted bytes are unchanged, and must stay that way -- these digests
// are content addresses. `tests/canonical-json*.test.ts` pins the grammar,
// the Python parity vector pins cross-language agreement, and the
// architecture hashing tests pin real-catalog digests.
function serialize(
  value: unknown,
  chunks: string[],
  ancestors: Set<object>,
): void {
  if (value === null) {
    chunks.push("null");
    return;
  }

  switch (typeof value) {
    case "string":
    case "boolean":
      chunks.push(JSON.stringify(value));
      return;
    case "number":
      if (!Number.isFinite(value)) {
        throw new TypeError(
          `Canonical JSON cannot serialize non-finite number: ${String(value)}`,
        );
      }
      chunks.push(JSON.stringify(value));
      return;
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
      chunks.push("[");
      for (let index = 0; index < value.length; index += 1) {
        if (index > 0) chunks.push(",");
        serialize(value[index], chunks, ancestors);
      }
      chunks.push("]");
      return;
    }

    // Sorting before the undefined check is equivalent to filtering first:
    // dropping keys never reorders the ones that remain.
    const record = value as Record<string, unknown>;
    const keys = Object.keys(record).sort(compareUtf16CodeUnits);
    chunks.push("{");
    let written = 0;
    for (const key of keys) {
      const entryValue = record[key];
      if (typeof entryValue === "undefined") continue;
      if (written > 0) chunks.push(",");
      written += 1;
      chunks.push(JSON.stringify(key), ":");
      serialize(entryValue, chunks, ancestors);
    }
    chunks.push("}");
  } finally {
    ancestors.delete(value);
  }
}

function compareUtf16CodeUnits(left: string, right: string): number {
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}
