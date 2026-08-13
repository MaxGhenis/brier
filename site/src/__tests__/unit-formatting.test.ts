import { describe, expect, it } from "vitest";
import { formatValue } from "@/data/forecast-cells";

describe("forecast unit formatting", () => {
  it("renders million cubic feet with the EIA MMcf abbreviation", () => {
    expect(formatValue(1_234.5, "million_cubic_feet")).toBe("1,234.5 MMcf");
  });
});
