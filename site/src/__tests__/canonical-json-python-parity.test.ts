import { execFileSync } from "node:child_process";
import { describe, expect, it } from "vitest";
import { canonicalStringify, sha256Hex } from "@/data/canonical-json";

describe("Python/TypeScript canonical JSON parity", () => {
  it("matches for UTF-16-sensitive keys, astral text, escapes, and numbers", () => {
    const value = {
      "\ue000": 3,
      "😀": 2,
      "\ud7ff": 1,
      nested: {
        quote: 'a"b\\c\n',
        negativeZero: -0,
        fixedSmall: 1e-6,
        scientificSmall: 1e-7,
        fixedLarge: 1e20,
        scientificLarge: 1e21,
        roundedUnsafeInteger: 9007199254740993,
      },
    };
    const input = JSON.stringify(value);
    // This vector exists to catch UTF-16 ordering drift, so it is exactly
    // the input a locale-dependent stdin decoder corrupts. Python reads
    // stdin in the host ANSI codepage on Windows (cp1252), which mangles
    // the astral and private-use keys and reorders them -- the test could
    // never pass on a Windows checkout. PYTHONUTF8 pins UTF-8 everywhere;
    // it is already the default on the POSIX runners, so CI is unchanged.
    const python = { ...process.env, PYTHONUTF8: "1" };
    const pythonCanonical = execFileSync(
      "python3",
      ["../scripts/canonical_json.py"],
      { input, encoding: "utf8", env: python },
    ).trimEnd();
    const pythonSha = execFileSync(
      "python3",
      ["../scripts/canonical_json.py", "--sha256"],
      { input, encoding: "utf8", env: python },
    ).trim();

    expect(pythonCanonical).toBe(canonicalStringify(value));
    expect(pythonSha).toBe(sha256Hex(value));
  });
});
