import { describe, expect, it } from "vitest";
import { generateStaticParams } from "@/app/topics/[slug]/page";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import {
  cellMatchesTopic,
  cellsForTopic,
  getTopic,
  TOPICS,
  topicsForCell,
  type TopicDefinition,
} from "@/data/topics";

const AGING_DISABILITY_FOUNDING_SLUGS = [
  "va-pending-disability-claims-2026-07-13",
  "ssi-recipients-aged-65-plus-june-2026",
  "ssdi-disabled-worker-beneficiaries-june-2026",
  "ssa-hearings-average-processing-time-june-2026",
  "us-lfpr-55-plus-july-2026",
  "us-disability-employment-population-ratio-july-2026",
  "spm-senior-poverty-2025",
  "social-security-cola-2027",
  "ssdi-initial-applications-april-2027-work-req-deadline-holds",
  "ssdi-initial-applications-april-2027-work-req-deadline-delayed",
  "ca-medicaid-enrollment-50-64-april-2027-work-req-deadline-holds",
  "ca-medicaid-enrollment-50-64-april-2027-work-req-deadline-delayed",
];

describe("topic registry", () => {
  it("has unique kebab-case slugs that do not shadow forecast cells", () => {
    const slugs = TOPICS.map((topic) => topic.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
    const cellSlugs = new Set(FORECAST_CELLS.map((cell) => cell.slug));
    for (const slug of slugs) {
      expect(slug).toMatch(/^[a-z0-9]+(-[a-z0-9]+)*$/);
      expect(cellSlugs.has(slug)).toBe(false);
    }
    expect(cellSlugs.has("topics")).toBe(false);
  });

  it("keeps every prefix live: each matches at least one published cell", () => {
    for (const topic of TOPICS) {
      for (const prefix of topic.dataPointIdPrefixes) {
        const matches = FORECAST_CELLS.filter((cell) =>
          cell.dataPointId?.startsWith(prefix),
        );
        expect(
          matches.length,
          `dead prefix ${prefix} in topic ${topic.slug}`,
        ).toBeGreaterThan(0);
      }
    }
  });

  it("only references real cell slugs in include/exclude lists", () => {
    const cellSlugs = new Set(FORECAST_CELLS.map((cell) => cell.slug));
    for (const topic of TOPICS) {
      for (const slug of [
        ...(topic.includeSlugs ?? []),
        ...(topic.excludeSlugs ?? []),
      ]) {
        expect(cellSlugs.has(slug), `unknown slug ${slug}`).toBe(true);
      }
    }
  });

  it("never lists a slug as both included and excluded", () => {
    for (const topic of TOPICS) {
      const included = new Set(topic.includeSlugs ?? []);
      for (const slug of topic.excludeSlugs ?? []) {
        expect(included.has(slug)).toBe(false);
      }
    }
  });
});

describe("aging-disability topic", () => {
  const topic = getTopic("aging-disability")!;

  it("exists", () => {
    expect(topic).toBeDefined();
  });

  it("contains every founding aging/disability cell", () => {
    const memberSlugs = new Set(
      cellsForTopic(topic, FORECAST_CELLS).map((cell) => cell.slug),
    );
    for (const slug of AGING_DISABILITY_FOUNDING_SLUGS) {
      expect(memberSlugs.has(slug), `missing founding cell ${slug}`).toBe(
        true,
      );
    }
  });

  it("auto-includes rolled cells on matching series (SSI program total)", () => {
    const members = cellsForTopic(topic, FORECAST_CELLS);
    const rolledSsi = members.filter((cell) =>
      cell.dataPointId?.startsWith("ssa.ssi.total_recipients"),
    );
    expect(rolledSsi.length).toBeGreaterThan(0);
    expect(members.length).toBeGreaterThan(
      AGING_DISABILITY_FOUNDING_SLUGS.length - 1,
    );
  });

  it("produces no duplicate members", () => {
    const memberSlugs = cellsForTopic(topic, FORECAST_CELLS).map(
      (cell) => cell.slug,
    );
    expect(new Set(memberSlugs).size).toBe(memberSlugs.length);
  });
});

describe("topic matching semantics", () => {
  const base: TopicDefinition = {
    slug: "test-topic",
    title: "Test",
    shortLabel: "test",
    description: "test",
    dataPointIdPrefixes: ["agency.program."],
  };
  const cell = FORECAST_CELLS.find(
    (candidate) => candidate.dataPointId,
  )!;

  it("excludeSlugs wins over prefixes and includeSlugs", () => {
    const topic: TopicDefinition = {
      ...base,
      dataPointIdPrefixes: [cell.dataPointId!],
      includeSlugs: [cell.slug],
      excludeSlugs: [cell.slug],
    };
    expect(cellMatchesTopic(cell, topic)).toBe(false);
  });

  it("includeSlugs admits cells outside every prefix rule", () => {
    const topic: TopicDefinition = { ...base, includeSlugs: [cell.slug] };
    expect(cellMatchesTopic(cell, topic)).toBe(true);
  });

  it("cells without a dataPointId only match via includeSlugs", () => {
    const bare = FORECAST_CELLS.find((candidate) => !candidate.dataPointId);
    if (!bare) return;
    expect(
      cellMatchesTopic(bare, {
        ...base,
        dataPointIdPrefixes: [""],
      }),
    ).toBe(false);
    expect(
      cellMatchesTopic(bare, { ...base, includeSlugs: [bare.slug] }),
    ).toBe(true);
  });

  it("topicsForCell agrees with cellsForTopic", () => {
    for (const topic of TOPICS) {
      const members = new Set(
        cellsForTopic(topic, FORECAST_CELLS).map((member) => member.slug),
      );
      for (const candidate of FORECAST_CELLS) {
        const inTopic = topicsForCell(candidate).some(
          (matched) => matched.slug === topic.slug,
        );
        expect(inTopic).toBe(members.has(candidate.slug));
      }
    }
  });
});

describe("topic routes", () => {
  it("prerenders exactly one page per topic", () => {
    const params = generateStaticParams();
    expect(params).toHaveLength(TOPICS.length);
    const slugs = new Set(params.map((param) => param.slug));
    for (const topic of TOPICS) {
      expect(slugs.has(topic.slug)).toBe(true);
    }
  });
});
