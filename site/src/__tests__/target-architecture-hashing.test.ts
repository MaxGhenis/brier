import { describe, expect, it } from "vitest";
import { sha256Hex } from "@/data/canonical-json";
import {
  FORECAST_CELLS,
  getForecastRunEntries,
  type ForecastCell,
  type PredictionRunActivityArtifact,
} from "@/data/forecast-cells";
import { THESIS_TARGET_LEDGER } from "@/data/ledger-targets";
import { buildRecordedPredictionRunId } from "@/data/prediction-specs";
import { buildTargetArchitectureProjection } from "@/data/thesis-target-architecture";
import {
  buildPredictionResolutionEvents,
  scoreResolvedForecastRun,
  type ObservationRecordedLedgerEntry,
} from "@/data/thesis-log";

const FULL_DIGEST = /^[0-9a-f]{64}$/;

describe("target architecture hashing", () => {
  it("builds the real catalog without collisions and guards its ID projection", () => {
    const projection = buildTargetArchitectureProjection(
      FORECAST_CELLS,
      THESIS_TARGET_LEDGER,
    );
    const identifierDigest = sha256Hex({
      targetIds: projection.targets.map((row) => row.targetId),
      sourceSeriesIds: projection.sourceSeries.map((row) => row.sourceSeriesId),
      runIds: projection.forecastRuns.map((row) => row.runId),
      artifactRefIds: projection.artifactRefs.map((row) => row.artifactRefId),
    });

    expect({
      counts: projection.counts,
      identifierDigest,
    }).toMatchInlineSnapshot(`
      {
        "counts": {
          "artifactRefs": 3164,
          "baselineCandidates": 423,
          "forecastDistributionPoints": 251451,
          "forecastRuns": 1251,
          "forecastStrategies": 9,
          "judgeRuns": 1849,
          "observationVintages": 1942,
          "observations": 1942,
          "packVersions": 14,
          "packs": 14,
          "reasoningEvents": 6328,
          "resolutionEvents": 0,
          "reviewRuns": 82,
          "runArtifactRefs": 3639,
          "runPackVersions": 97,
          "scores": 0,
          "sourceSeries": 653,
          "strategyVersions": 9,
          "targetObservationBindings": 1306,
          "targetVersions": 653,
          "targets": 653,
          "toolCalls": 2397,
        },
        "identifierDigest": "2f0ca5aa86c7453e10110101ce449b3358cfb7ef5d8ed4f693d4292fc83503d3",
      }
    `);
  });

  it("retains full payload digests while truncating public IDs to 16 hex", () => {
    const projection = buildTargetArchitectureProjection(
      FORECAST_CELLS,
      THESIS_TARGET_LEDGER,
    );

    expect(projection.observations.length).toBeGreaterThan(0);
    expect(
      projection.observations.every((row) => FULL_DIGEST.test(row.payloadHash)),
    ).toBe(true);
    expect(
      projection.observationVintages.every((row) =>
        FULL_DIGEST.test(row.normalizedPayloadHash),
      ),
    ).toBe(true);
    expect(
      projection.packVersions.every((row) =>
        FULL_DIGEST.test(row.promptContentHash),
      ),
    ).toBe(true);
    expect(
      projection.strategyVersions.every(
        (row) =>
          (!row.promptPolicyHash || FULL_DIGEST.test(row.promptPolicyHash)) &&
          (!row.toolPolicyHash || FULL_DIGEST.test(row.toolPolicyHash)),
      ),
    ).toBe(true);
    expect(
      projection.artifactRefs.every((row) => FULL_DIGEST.test(row.contentHash)),
    ).toBe(true);
    expect(
      projection.artifactRefs
        .filter((row) => /^artifact\.[0-9a-f]+$/.test(row.artifactRefId))
        .every((row) => /^artifact\.[0-9a-f]{16}$/.test(row.artifactRefId)),
    ).toBe(true);
  });

  it("throws with both payload digests when truncated artifact IDs collide", () => {
    const base = FORECAST_CELLS.find((forecast) => forecast.predictionRun);
    if (!base?.predictionRun) throw new Error("Expected a recorded forecast");
    const prefix = "0123456789abcdef";
    const firstDigest = `${prefix}${"0".repeat(48)}`;
    const secondDigest = `${prefix}${"f".repeat(48)}`;
    const activityLog: PredictionRunActivityArtifact[] = [
      {
        artifactType: "prompt",
        path: "collision/first.txt",
        sha256: firstDigest,
        bytes: 1,
        createdAt: base.predictionRun.runAt,
      },
      {
        artifactType: "stdout",
        path: "collision/second.txt",
        sha256: secondDigest,
        bytes: 1,
        createdAt: base.predictionRun.runAt,
      },
    ];
    const collidingForecast: ForecastCell = {
      ...base,
      predictionRun: { ...base.predictionRun, activityLog },
    };

    expect(() =>
      buildTargetArchitectureProjection([collidingForecast]),
    ).toThrow(new RegExp(`${firstDigest} and ${secondDigest}`));
  });

  it("commits run IDs to the forecast output distribution summary", () => {
    const forecast = FORECAST_CELLS[0];
    const run = getForecastRunEntries(forecast)[0];
    const originalId = buildRecordedPredictionRunId(
      forecast,
      run.predictionRun?.runAt,
      run.variantId,
      run,
    );
    const changedId = buildRecordedPredictionRunId(
      forecast,
      run.predictionRun?.runAt,
      run.variantId,
      { ...run, pointEstimate: run.pointEstimate + 1 },
    );

    expect(originalId).toMatch(/\.[0-9a-f]{16}$/);
    expect(changedId).not.toBe(originalId);
  });

  it("commits resolution hashes and score IDs to the observed value", () => {
    const forecast = FORECAST_CELLS.find((row) => row.dataPointId);
    if (!forecast?.dataPointId) throw new Error("Expected a ledger target");
    const run = getForecastRunEntries(forecast)[0];
    const observation: ObservationRecordedLedgerEntry = {
      kind: "observation_recorded",
      observationId: `obs.${forecast.dataPointId}`,
      dataPointId: forecast.dataPointId,
      periodLabel: forecast.resolutionDate,
      value: run.pointEstimate,
      unit: forecast.unit,
      observedAt: forecast.resolutionDate,
      resolvedAt: forecast.resolutionDate,
      sourceKind: "official_release",
      source: forecast.resolutionSource,
      sourceUrl: forecast.resolutionSourceUrl,
    };
    const changedObservation = { ...observation, value: observation.value + 1 };
    const originalEvent = buildPredictionResolutionEvents(
      [forecast],
      [observation],
    )[0];
    const changedEvent = buildPredictionResolutionEvents(
      [forecast],
      [changedObservation],
    )[0];
    const originalScore = scoreResolvedForecastRun(forecast, run, [
      observation,
    ]);
    const changedScore = scoreResolvedForecastRun(forecast, run, [
      changedObservation,
    ]);
    const scoreProjection = buildTargetArchitectureProjection(
      [forecast],
      [observation],
    );

    expect(originalEvent.payloadHash).toMatch(FULL_DIGEST);
    expect(changedEvent.payloadHash).not.toBe(originalEvent.payloadHash);
    expect(originalScore?.scoreId).toContain("numeric_cdf_crps_v2_target_scale");
    expect(originalScore?.scoreId).toMatch(/\.[0-9a-f]{16}$/);
    expect(changedScore?.scoreId).not.toBe(originalScore?.scoreId);
    expect(scoreProjection.scores.length).toBeGreaterThan(0);
    expect(
      scoreProjection.scores.every((score) =>
        FULL_DIGEST.test(score.scoreHash),
      ),
    ).toBe(true);
  });
});
