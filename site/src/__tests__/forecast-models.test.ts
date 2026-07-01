import { describe, expect, it } from "vitest";
import {
  buildDampedLogTrendForecast,
  roundForecast,
} from "@/data/forecast-models";

describe("forecast models", () => {
  it("fits a damped log trend when enough history exists", () => {
    const forecast = buildDampedLogTrendForecast(
      [
        { period: 2022, value: 100 },
        { period: 2023, value: 106 },
        { period: 2024, value: 112 },
        { period: 2025, value: 118 },
      ],
      { damping: 0.5, residualStdDevFloor: 0.01 },
    );

    expect(forecast.modelId).toBe("damped_log_trend_v1");
    expect(forecast.status).toBe("fit");
    expect(forecast.historyPoints).toBe(4);
    expect(forecast.annualizedGrowth).toBeGreaterThan(0.02);
    expect(forecast.pointEstimate).toBeGreaterThan(118);
    expect(forecast.ciLow).toBeLessThan(forecast.pointEstimate);
    expect(forecast.ciHigh).toBeGreaterThan(forecast.pointEstimate);
  });

  it("annualizes growth when numeric periods are not adjacent", () => {
    const adjacent = buildDampedLogTrendForecast(
      [
        { period: 2023, value: 100 },
        { period: 2024, value: 110 },
        { period: 2025, value: 121 },
      ],
      { damping: 1, residualStdDevFloor: 0.01 },
    );
    const gapped = buildDampedLogTrendForecast(
      [
        { period: 2021, value: 100 },
        { period: 2023, value: 121 },
        { period: 2025, value: 146.41 },
      ],
      { damping: 1, residualStdDevFloor: 0.01 },
    );

    expect(gapped.annualizedGrowth).toBeCloseTo(adjacent.annualizedGrowth, 3);
  });

  it("declares fallback status rather than fitting a fake trend", () => {
    const forecast = roundForecast(
      buildDampedLogTrendForecast([{ period: 2025, value: 126520 }], {
        fallbackGrowth: Math.log(37.53 / 36.28),
        fallbackLabel:
          "BLS CES total private average hourly earnings, May 2025 to May 2026",
        residualStdDevFloor: 0.04,
      }),
      100,
    );

    expect(forecast.status).toBe("fallback");
    expect(forecast.pointEstimate).toBe(130900);
    expect(forecast.ciLow).toBe(124300);
    expect(forecast.ciHigh).toBe(137800);
    expect(forecast.diagnostics).toContain("only 1 target observation");
    expect(forecast.fallbackLabel).toContain("average hourly earnings");
  });
});
