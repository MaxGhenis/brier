import { describe, expect, it } from "vitest";
import { foldStances, type MetricStance } from "@/lib/stances";

const matrix: MetricStance[] = [
  { goal: 0, stance: "serves" },
  { goal: 1, stance: "opposes" },
  { goal: 2, stance: "orthogonal" },
];

describe("foldStances (Stance v1 micro-spec)", () => {
  it("returns null when the metric has no matrix", () => {
    expect(foldStances(undefined, {})).toBeNull();
    expect(foldStances([], {})).toBeNull();
  });

  it("shows raw matrix counts when zero goals are confirmed", () => {
    expect(foldStances(matrix, {})).toEqual({
      kind: "counts",
      serves: 1,
      opposes: 1,
      orthogonal: 1,
    });
  });

  it("serves when at least one confirmed goal is served and none opposed", () => {
    expect(foldStances(matrix, { 0: "confirmed" })).toEqual({
      kind: "serves",
    });
  });

  it("opposes when at least one confirmed goal is opposed and none served", () => {
    expect(foldStances(matrix, { 1: "confirmed" })).toEqual({
      kind: "opposes",
    });
  });

  it("mixed when confirmed goals are both served and opposed", () => {
    expect(foldStances(matrix, { 0: "confirmed", 1: "confirmed" })).toEqual({
      kind: "mixed",
    });
  });

  it("orthogonal when confirmed goals are neither served nor opposed", () => {
    expect(foldStances(matrix, { 2: "confirmed" })).toEqual({
      kind: "orthogonal",
    });
  });

  it("struck goals drop out of the confirmed fold", () => {
    expect(
      foldStances(matrix, { 0: "confirmed", 1: "struck" }),
    ).toEqual({ kind: "serves" });
  });

  it("struck goals drop out of the zero-confirmed counts", () => {
    expect(foldStances(matrix, { 1: "struck" })).toEqual({
      kind: "counts",
      serves: 1,
      opposes: 0,
      orthogonal: 1,
    });
  });

  it("all goals struck yields empty counts, not a fake neutral", () => {
    expect(
      foldStances(matrix, { 0: "struck", 1: "struck", 2: "struck" }),
    ).toEqual({ kind: "counts", serves: 0, opposes: 0, orthogonal: 0 });
  });
});
