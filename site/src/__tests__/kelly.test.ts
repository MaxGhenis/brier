import { describe, expect, it } from "vitest";
import {
  cdfAt,
  kellyBet,
  quantileAt,
  runKellyBacktest,
  settleLogGrowth,
  type CdfPoint,
} from "@/data/kelly";

function uniformCdf(low: number, high: number): CdfPoint[] {
  return [
    { value: low, probability: 0 },
    { value: high, probability: 1 },
  ];
}

describe("cdfAt / quantileAt", () => {
  const points = uniformCdf(0, 10);

  it("interpolates piecewise-linearly and clamps outside support", () => {
    expect(cdfAt(points, 5)).toBeCloseTo(0.5);
    expect(cdfAt(points, 2.5)).toBeCloseTo(0.25);
    expect(cdfAt(points, -1)).toBe(0);
    expect(cdfAt(points, 11)).toBe(1);
  });

  it("inverts the CDF", () => {
    expect(quantileAt(points, 0.25)).toBeCloseTo(2.5);
    expect(quantileAt(points, 0.5)).toBeCloseTo(5);
    for (const p of [0.1, 0.37, 0.5, 0.83]) {
      expect(cdfAt(points, quantileAt(points, p))).toBeCloseTo(p);
    }
  });
});

describe("kellyBet", () => {
  it("bets yes with positive edge, no with negative, sized by Kelly", () => {
    // Agent 70% vs market 50%: f* = 0.2 / 0.5 = 0.4 on yes.
    expect(kellyBet(0.7, 0.5)).toEqual({
      side: "yes",
      fraction: expect.closeTo(0.4, 10),
      edge: expect.closeTo(0.2, 10),
    });
    // Agent 30% vs market 50%: symmetric no-side bet.
    expect(kellyBet(0.3, 0.5)).toEqual({
      side: "no",
      fraction: expect.closeTo(0.4, 10),
      edge: expect.closeTo(-0.2, 10),
    });
  });

  it("declines dead heats and degenerate prices", () => {
    expect(kellyBet(0.501, 0.5)).toBeNull();
    expect(kellyBet(0.9, 0)).toBeNull();
    expect(kellyBet(0.9, 1)).toBeNull();
    expect(kellyBet(Number.NaN, 0.5)).toBeNull();
  });
});

describe("settleLogGrowth", () => {
  it("grows on wins and shrinks on losses at even odds", () => {
    const bet = kellyBet(0.7, 0.5)!;
    // Half-Kelly stake 0.2 at even odds: win → ln(1.2), lose → ln(0.8).
    expect(settleLogGrowth(bet, true, 0.5, 0.5)).toBeCloseTo(Math.log(1.2));
    expect(settleLogGrowth(bet, false, 0.5, 0.5)).toBeCloseTo(Math.log(0.8));
  });

  it("caps the stake", () => {
    const bet = kellyBet(0.99, 0.5)!; // full Kelly 0.98
    expect(settleLogGrowth(bet, false, 0.5, 1, 0.25)).toBeCloseTo(
      Math.log(0.75),
    );
  });
});

describe("runKellyBacktest", () => {
  it("places no bets when the agent equals the market", () => {
    const { rows, summary } = runKellyBacktest([
      {
        slug: "same",
        resolutionDate: "2026-07-01",
        chronology: "claimed_time_verified",
        agentPoints: uniformCdf(0, 10),
        baselinePoints: uniformCdf(0, 10),
        observed: 4,
      },
    ]);
    expect(rows).toHaveLength(0);
    expect(summary.finalWealthMultiple).toBe(1);
  });

  it("rewards a sharper correct agent and punishes a wrong one", () => {
    // Baseline spans 0..10; agent concentrates on 4..6 around the truth.
    const sharpRight = runKellyBacktest([
      {
        slug: "right",
        resolutionDate: "2026-07-01",
        chronology: "claimed_time_verified",
        agentPoints: uniformCdf(4, 6),
        baselinePoints: uniformCdf(0, 10),
        observed: 5.5,
      },
    ]);
    expect(sharpRight.summary.bets).toBeGreaterThan(0);
    expect(sharpRight.summary.finalWealthMultiple).toBeGreaterThan(1);

    // Same sharp agent, but the outcome lands far outside its mass.
    const sharpWrong = runKellyBacktest([
      {
        slug: "wrong",
        resolutionDate: "2026-07-01",
        chronology: "claimed_time_verified",
        agentPoints: uniformCdf(4, 6),
        baselinePoints: uniformCdf(0, 10),
        observed: 9.5,
      },
    ]);
    expect(sharpWrong.summary.finalWealthMultiple).toBeLessThan(1);
  });

  it("tracks drawdown from the wealth peak", () => {
    const win = {
      slug: "a",
      resolutionDate: "2026-07-01",
      chronology: "claimed_time_verified",
      agentPoints: uniformCdf(4, 6),
      baselinePoints: uniformCdf(0, 10),
      observed: 5,
    };
    const lose = { ...win, slug: "b", resolutionDate: "2026-07-02", observed: 9.9 };
    const { summary } = runKellyBacktest([win, lose]);
    expect(summary.maxDrawdown).toBeGreaterThan(0);
    expect(summary.maxDrawdown).toBeLessThan(1);
  });
});
