import { describe, expect, it } from "vitest";
import type { ForecastCell } from "@/data/forecast-cells";
import {
  isPreregisteredTargetWithinOrphanGrace,
  TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS,
  type TargetRegisteredLedgerEntry,
} from "@/data/ledger-targets";
import {
  getObservationForId,
  getResolvedObservationForForecast,
  type ObservationRecordedLedgerEntry,
} from "@/data/thesis-log";

describe("independent resolver binding", () => {
  it("keeps the earliest observedAt when a later revision shares a dataPointId", () => {
    const dataPointId = "test.series.2030_01.first_print";
    const observation = (
      value: number,
      observedAt: string,
    ): ObservationRecordedLedgerEntry => ({
      kind: "observation_recorded",
      observationId: `obs.${dataPointId}`,
      dataPointId,
      periodLabel: "2030-01",
      unit: "percent",
      value,
      observedAt,
      resolvedAt: observedAt,
      sourceKind: "official_release",
      source: "Official test release",
      sourceUrl: "https://example.gov/test",
      note: "Synthetic revision ordering fixture.",
    });
    const forecast = { dataPointId } as ForecastCell;

    const ledger = [
      observation(4.7, "2030-02-02T12:00:00Z"),
      observation(4.2, "2030-02-01T12:00:00Z"),
    ];
    const selected = getResolvedObservationForForecast(forecast, ledger);

    expect(selected?.value).toBe(4.2);
    expect(selected?.observedAt).toBe("2030-02-01T12:00:00Z");
    expect(getObservationForId(`obs.${dataPointId}`, ledger)?.value).toBe(4.2);
  });

  it("falls back to seven days when no release window is recorded", () => {
    const target = {
      registrationState: "preregistered",
      registeredAt: "2030-01-01T00:00:00Z",
    } as TargetRegisteredLedgerEntry;

    expect(
      isPreregisteredTargetWithinOrphanGrace(
        target,
        new Date("2030-01-08T00:00:00Z"),
      ),
    ).toBe(true);
    expect(
      isPreregisteredTargetWithinOrphanGrace(
        target,
        new Date("2030-01-08T00:00:01Z"),
      ),
    ).toBe(false);
    expect(TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS).toBe(7);
  });

  it("awaits the forecast until the release window opens, not a flat span", () => {
    const withWindow = (start: string) =>
      ({
        registrationState: "preregistered",
        registeredAt: "2030-01-01T00:00:00Z",
        sourceBinding: { expectedReleaseWindow: { start, end: start } },
      }) as unknown as TargetRegisteredLedgerEntry;

    // Long-dated: still awaiting at day 20, where a flat 7 days would have
    // expired it with a fortnight of legitimate forecasting time left.
    const longDated = withWindow("2030-02-01");
    expect(
      isPreregisteredTargetWithinOrphanGrace(
        longDated,
        new Date("2030-01-21T00:00:00Z"),
      ),
    ).toBe(true);

    // Expires the instant the window opens, not before and not after.
    expect(
      isPreregisteredTargetWithinOrphanGrace(
        longDated,
        new Date("2030-01-31T23:59:59Z"),
      ),
    ).toBe(true);
    expect(
      isPreregisteredTargetWithinOrphanGrace(
        longDated,
        new Date("2030-02-01T00:00:00Z"),
      ),
    ).toBe(false);

    // Short-dated: no grace beyond the window, even well inside seven days.
    const shortDated = withWindow("2030-01-03");
    expect(
      isPreregisteredTargetWithinOrphanGrace(
        shortDated,
        new Date("2030-01-04T00:00:00Z"),
      ),
    ).toBe(false);
  });
});
