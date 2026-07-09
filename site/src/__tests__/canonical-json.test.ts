import { describe, expect, it } from "vitest";
import { canonicalStringify, sha256Hex } from "@/data/canonical-json";

describe("canonical JSON", () => {
  it("is deterministic across key insertion order and nested structures", () => {
    const left = {
      z: [{ second: 2, first: 1 }, true, null],
      a: { beta: "b", alpha: "a", omitted: undefined },
    };
    const right = {
      a: { alpha: "a", omitted: undefined, beta: "b" },
      z: [{ first: 1, second: 2 }, true, null],
    };

    expect(canonicalStringify(left)).toBe(
      '{"a":{"alpha":"a","beta":"b"},"z":[{"first":1,"second":2},true,null]}',
    );
    expect(canonicalStringify(right)).toBe(canonicalStringify(left));
    expect(sha256Hex(right)).toBe(sha256Hex(left));
  });

  it("sorts keys by UTF-16 code units instead of locale collation", () => {
    // English locale collation places lowercase a before Z, while the RFC
    // 8785 ordering rule compares their UTF-16 code units and places Z first.
    const value = { a: 2, "\u00e4": 3, Z: 1 };

    expect(["Z", "a", "\u00e4"].sort(new Intl.Collator("en").compare)[0]).toBe(
      "a",
    );
    expect(canonicalStringify(value)).toBe('{"Z":1,"a":2,"\u00e4":3}');
  });

  it("uses stable JSON number formatting and rejects non-finite numbers", () => {
    expect(canonicalStringify({ negativeZero: -0, small: 1e-7 })).toBe(
      '{"negativeZero":0,"small":1e-7}',
    );
    expect(() => canonicalStringify(Number.NaN)).toThrow(/non-finite/);
    expect(() => canonicalStringify(Number.POSITIVE_INFINITY)).toThrow(
      /non-finite/,
    );
    expect(() => canonicalStringify({ nested: [-Infinity] })).toThrow(
      /non-finite/,
    );
  });

  it("returns the full SHA-256 digest", () => {
    expect(sha256Hex({ b: 2, a: 1 })).toBe(
      "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
    );
    expect(sha256Hex({ b: 2, a: 1 })).toMatch(/^[0-9a-f]{64}$/);
  });
});
