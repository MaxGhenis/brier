import fs from "node:fs";
import path from "node:path";

/**
 * Slice full section text for a provision out of the cached raw bill
 * text (bills/raw/<slug>.txt). Interim implementation: keyed on the
 * federal "SEC. NNNN." headings and the section numbers named in the
 * provision heading; replaced by ingest-emitted provision spans once
 * the chunker lands (issue #43). Returns null rather than guessing —
 * never show the wrong text.
 */

const RAW_DIR = path.join(process.cwd(), "..", "bills", "raw");

// Committee-print page furniture: bare page numbers and draft stamps
// ("RYA26731 1TW [file 1 of 2]  S.L.C."), plus trailing line-number
// gutters PDF extraction leaves at line ends.
function cleanForDisplay(slice: string): string {
  return slice
    .split("\n")
    .filter((line) => !/^\s*\d+\s*$/.test(line))
    .filter((line) => !/\[file \d+ of \d+\]|S\.L\.C\./.test(line))
    .map((line) => line.replace(/\s+\d{1,2}\s*$/, ""))
    .join("\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

export function loadRawBillText(slug: string): string | null {
  const file = path.join(RAW_DIR, `${slug}.txt`);
  if (!fs.existsSync(file)) return null;
  return fs.readFileSync(file, "utf-8");
}

/** Section numbers named in a provision heading, e.g. "§§2101, 2105, and 2401(1)" → ["2101","2105","2401"]. */
export function parseSectionNumbers(heading: string, title: string): string[] {
  const source = `${title} ${heading}`;
  const cited = source.match(/§§?[\d\s,()–\-and]+/g)?.join(" ") ?? "";
  // Negative lookbehind/ahead drop parenthesized subsection designators
  // — the (1) in "2401(1)" is not a section number.
  const numbers = [...cited.matchAll(/(?<!\()\b(\d{1,4})\b(?!\))/g)].map(
    (m) => m[1],
  );
  const unique = [...new Set(numbers)];
  if (unique.length > 0) return unique;
  const plain = title.match(/^Section\s+(\d{1,4})$/i);
  return plain ? [plain[1]] : [];
}

export function extractSections(
  rawText: string,
  sectionNumbers: string[],
): string | null {
  const slices: string[] = [];
  for (const num of sectionNumbers) {
    const start = rawText.search(
      new RegExp(`^SEC(?:TION)?\\.?\\s*${num}\\.`, "m"),
    );
    if (start === -1) continue;
    const rest = rawText.slice(start);
    const next = rest.slice(6).search(/^SEC(?:TION)?\.?\s*\d{1,4}\./m);
    const slice = next === -1 ? rest : rest.slice(0, next + 6);
    slices.push(cleanForDisplay(slice));
  }
  // Partial coverage is fine (a provision citing §§2101 and 2105 shows
  // both found sections); zero coverage means our slicer failed — show
  // nothing rather than something wrong.
  return slices.length > 0 ? slices.join("\n\n· · ·\n\n") : null;
}

export function fullSectionText(
  slug: string,
  heading: string,
  title: string,
): string | null {
  const raw = loadRawBillText(slug);
  if (!raw) return null;
  const numbers = parseSectionNumbers(heading, title);
  if (numbers.length === 0) return null;
  return extractSections(raw, numbers);
}
