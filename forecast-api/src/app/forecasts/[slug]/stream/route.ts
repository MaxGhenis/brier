import {
  CPI_MARKET_SLUG,
  CPI_SERIES_ID,
  CPI_TARGET_YEAR,
  formatCpiSummary,
} from "@/lib/bls";
import { optionsResponse } from "@/lib/cors";
import {
  formatSpmChildPovertySummary,
  policySnapshotFromPolicy,
  serializeSpmCalibrationToolResult,
  SPM_CHILD_POVERTY_2025_SLUG,
  SPM_TARGET_YEAR,
  unavailablePolicySnapshot,
} from "@/lib/census";
import {
  DATA_POINT_IDS,
  getDataPointSnapshot,
  serializeDataPointSnapshot,
} from "@/lib/data-points";
import {
  generateCpiForecast,
  generateCtcExpansionForecast,
  generateSpmChildPovertyForecast,
} from "@/lib/forecast";
import {
  CTC_3000_FULLY_REFUNDABLE_POLICY_ID,
  CTC_CURRENT_LAW_OUTLAYS_SLUG,
  CTC_EXPANSION_COST_SLUG,
  CTC_TARGET_YEAR,
  CURRENT_LAW_POLICY_ID,
  fetchCtcExpansionDataset,
  fetchPolicy,
  formatCtcExpansionSummary,
  serializeEconomyToolResult,
  serializePolicyToolResult,
} from "@/lib/policyengine";
import { buildNumericCdfFromInterval } from "@/lib/prediction-distribution";
import { createSseResponse, pause, type SendEvent } from "@/lib/sse";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export function OPTIONS(request: Request) {
  return optionsResponse(request);
}

export async function GET(
  request: Request,
  context: { params: Promise<{ slug: string }> },
) {
  const { slug } = await context.params;
  if (slug === CPI_MARKET_SLUG) {
    return createSseResponse(request, async (send) => {
      await streamCpiForecast(send);
    });
  }

  if (slug === CTC_EXPANSION_COST_SLUG) {
    return createSseResponse(request, async (send) => {
      await streamCtcExpansionForecast(send);
    });
  }

  if (slug === CTC_CURRENT_LAW_OUTLAYS_SLUG) {
    return createSseResponse(request, async (send) => {
      await streamCtcCurrentLawOutlaysForecast(send);
    });
  }

  if (slug === SPM_CHILD_POVERTY_2025_SLUG) {
    return createSseResponse(request, async (send) => {
      await streamSpmChildPovertyForecast(send);
    });
  }

  return Response.json(
    { error: `No live forecaster is configured for ${slug}.` },
    { status: 404 },
  );
}

async function streamSpmChildPovertyForecast(send: SendEvent) {
  await sendStep(send, {
    kind: "heading",
    text: "Identifying the question",
  });
  await sendStep(send, {
    kind: "text",
    text: "This stream forecasts the calendar-year 2025 Supplemental Poverty Measure child poverty rate that Census is expected to publish in the September 2026 income and poverty release. The live run verifies the PolicyEngine current-law policy, runs the public data-point processor for the Census target, and applies an explicit calibration fallback before the forecast step.",
  });

  const policyCall = `policyengine.policy.get({ id: ${CURRENT_LAW_POLICY_ID} })`;
  send("status", {
    state: "tool_running",
    label: "Querying PolicyEngine current law",
  });
  send("tool_start", {
    tool: "policyengine.policy",
    call: policyCall,
  });

  const currentLawPolicy = await fetchPolicy(CURRENT_LAW_POLICY_ID)
    .then((policy) => {
      send("tool_result", {
        tool: "policyengine.policy",
        call: policyCall,
        result: serializePolicyToolResult(policy),
      });
      return policySnapshotFromPolicy(policy);
    })
    .catch((error: unknown) => {
      const snapshot = unavailablePolicySnapshot(
        CURRENT_LAW_POLICY_ID,
        error,
      );
      send("tool_result", {
        tool: "policyengine.policy",
        call: policyCall,
        result: JSON.stringify(snapshot, null, 2),
      });
      return snapshot;
    });

  const censusCall = [
    `census.releaseSchedule({ survey: "CPS ASEC", targetYear: ${SPM_TARGET_YEAR}, measure: "SPM child poverty" })`,
    'census.spm.history({ population: "children_under_18", years: [2021, 2024] })',
  ].join("\n");
  send("status", {
    state: "tool_running",
    label: "Running public data-point processor",
  });
  send("tool_start", {
    tool: "data-point.processor",
    call: censusCall,
  });

  const dataPoint = await getDataPointSnapshot(
    DATA_POINT_IDS.SPM_CHILD_POVERTY_RATE_2025,
    { currentLawPolicy },
  );
  const dataset = dataPoint.dataset;

  send("tool_result", {
    tool: "data-point.processor",
    call: censusCall,
    result: serializeDataPointSnapshot(dataPoint),
  });
  await pause(180);

  await sendStep(send, {
    kind: "heading",
    text: "Census and current-law read",
  });
  await sendStep(send, {
    kind: "text",
    text: formatSpmChildPovertySummary(dataset.summary),
  });

  const calibrationCall =
    'brier.calibration.lookup({ domain: "poverty_forecasts", outcome: "spm_child_poverty_rate", targetYear: 2025 })';
  send("status", {
    state: "tool_running",
    label: "Looking up SPM calibration prior",
  });
  send("tool_start", {
    tool: "brier.calibration",
    call: calibrationCall,
  });
  send("tool_result", {
    tool: "brier.calibration",
    call: calibrationCall,
    result: serializeSpmCalibrationToolResult(dataset),
  });

  await sendStep(send, {
    kind: "heading",
    text: "Calibration adjustment",
  });
  await sendStep(send, {
    kind: "math",
    text: [
      "point = ",
      `${dataset.summary.calibration.policyEngineWeight.toFixed(2)} × ${dataset.summary.policyEnginePriorPct.toFixed(1)}% + `,
      `${dataset.summary.calibration.postExpansionHistoryWeight.toFixed(2)} × ${dataset.summary.postExpansionAveragePct.toFixed(1)}% + `,
      `${dataset.summary.calibration.latestPublishedWeight.toFixed(2)} × ${dataset.summary.latestHistoricalChildPovertyRatePct.toFixed(1)}% `,
      `${dataset.summary.calibration.macroAdjustmentPct >= 0 ? "+" : "-"} ${Math.abs(dataset.summary.calibration.macroAdjustmentPct).toFixed(2)}pp = `,
      `${dataset.summary.calibratedPointEstimatePct.toFixed(1)}%`,
    ].join(""),
  });
  await sendStep(send, {
    kind: "text",
    text: "The adjustment layer is deliberately explicit: PolicyEngine supplies law and population structure, Census supplies the resolution target and recent history, and the forecast optimizes for accuracy against the eventual Census publication rather than copying either input mechanically.",
  });

  send("status", {
    state: "model_running",
    label: "Generating calibrated forecast",
  });
  await sendStep(send, {
    kind: "heading",
    text: "Forecast model",
  });

  const forecast = await generateSpmChildPovertyForecast(dataset);
  for (const trace of forecast.publicTrace) {
    await sendStep(send, {
      kind: "text",
      text: trace,
    });
  }

  if (forecast.assumptions.length > 0) {
    await sendStep(send, {
      kind: "heading",
      text: "Assumptions and caveats",
    });
    await sendStep(send, {
      kind: "text",
      text: [
        ...forecast.assumptions.map(
          (assumption) => `Assumption: ${assumption}`,
        ),
        ...forecast.dataCaveats.map((caveat) => `Caveat: ${caveat}`),
      ].join(" "),
    });
  }

  send("forecast", forecast);
  send("status", {
    state: "complete",
    label:
      forecast.source === "ai_gateway"
        ? "AI Gateway forecast complete"
        : "Calibration fallback complete",
  });
  send("done", { ok: true });
}

async function streamCpiForecast(send: SendEvent) {
  await sendStep(send, {
    kind: "heading",
    text: "Identifying the question",
  });
  await sendStep(send, {
    kind: "text",
    text: "This stream forecasts annual-average CPI-U inflation for calendar year 2026 versus the 2025 annual average. The live run starts from BLS series CUUR0000SA0 and computes current-year annual-average pressure from monthly observations.",
  });

  const call = `bls.timeseries({ series: "${CPI_SERIES_ID}", startYear: ${
    CPI_TARGET_YEAR - 7
  }, endYear: ${CPI_TARGET_YEAR} })`;

  send("status", {
    state: "tool_running",
    label: "Running public data-point processor",
  });
  send("tool_start", {
    tool: "data-point.processor",
    call,
  });

  const dataPoint = await getDataPointSnapshot(
    DATA_POINT_IDS.CPI_U_ANNUAL_PCT_CHANGE_2026,
  );
  const dataset = dataPoint.dataset;

  send("tool_result", {
    tool: "data-point.processor",
    call,
    result: serializeDataPointSnapshot(dataPoint),
  });
  await pause(180);

  await sendStep(send, {
    kind: "heading",
    text: "Live CPI-U read",
  });
  await sendStep(send, {
    kind: "text",
    text: formatCpiSummary(dataset.summary),
  });

  send("status", {
    state: "model_running",
    label: "Generating calibrated forecast",
  });
  await sendStep(send, {
    kind: "heading",
    text: "Forecast model",
  });

  const forecast = await generateCpiForecast(dataset);
  for (const trace of forecast.publicTrace) {
    await sendStep(send, {
      kind: "text",
      text: trace,
    });
  }

  if (forecast.assumptions.length > 0) {
    await sendStep(send, {
      kind: "heading",
      text: "Assumptions and caveats",
    });
    await sendStep(send, {
      kind: "text",
      text: [
        ...forecast.assumptions.map(
          (assumption) => `Assumption: ${assumption}`,
        ),
        ...forecast.dataCaveats.map((caveat) => `Caveat: ${caveat}`),
      ].join(" "),
    });
  }

  send("forecast", forecast);
  send("status", {
    state: "complete",
    label:
      forecast.source === "ai_gateway"
        ? "AI Gateway forecast complete"
        : "Fallback forecast complete",
  });
  send("done", { ok: true });
}

async function streamCtcCurrentLawOutlaysForecast(send: SendEvent) {
  await sendStep(send, {
    kind: "heading",
    text: "Identifying the question",
  });
  await sendStep(send, {
    kind: "text",
    text: "This stream forecasts tax-year 2026 Child Tax Credit outlays under current law. The live call verifies the PolicyEngine current-law policy object; the outlay estimate uses a prototype calibration fallback until an absolute CTC-outlay economy result is available through the public API.",
  });

  const policyCall = `policyengine.policy.get({ id: ${CURRENT_LAW_POLICY_ID} })`;
  send("status", {
    state: "tool_running",
    label: "Querying PolicyEngine current law",
  });
  send("tool_start", {
    tool: "policyengine.policy",
    call: policyCall,
  });

  const policy = await fetchPolicy(CURRENT_LAW_POLICY_ID);
  send("tool_result", {
    tool: "policyengine.policy",
    call: policyCall,
    result: serializePolicyToolResult(policy),
  });

  await sendStep(send, {
    kind: "heading",
    text: "Calibration fallback",
  });
  await sendStep(send, {
    kind: "text",
    text: "Absolute CTC outlays need a variable-specific population total, not a reform-vs-baseline delta. For this prototype, the live stream treats the public PolicyEngine policy object as the law input and applies a stored calibration fallback for the CTC outlay target.",
  });

  const calibrationCall =
    'brier.calibration.lookup({ domain: "policyengine_budget_scores", policy_area: "ctc", outcome: "current_law_outlays" })';
  send("status", {
    state: "tool_running",
    label: "Looking up CTC outlay calibration",
  });
  send("tool_start", {
    tool: "brier.calibration",
    call: calibrationCall,
  });

  const rawEstimate = 58.8;
  const ratio = 1.02;
  const additive = 0.5;
  const pointEstimate = 60.5;
  const ciLow = 52.0;
  const ciHigh = 70.0;
  send("tool_result", {
    tool: "brier.calibration",
    call: calibrationCall,
    result: JSON.stringify(
      {
        rawEstimateUsdBillions: rawEstimate,
        rawEstimateSource:
          "prototype PolicyEngine current-law microsimulation seed",
        rawToFinalRatio: ratio,
        additiveUsdBillions: additive,
        target: "IRS/Treasury CTC outlay table",
      },
      null,
      2,
    ),
  });

  await sendStep(send, {
    kind: "math",
    text: `calibrated outlays = $${rawEstimate.toFixed(1)}B × ${ratio.toFixed(2)} + $${additive.toFixed(1)}B = $${pointEstimate.toFixed(1)}B`,
  });
  await sendStep(send, {
    kind: "text",
    text: "The AI should update this estimate as soon as real calibration observations accumulate: compare PolicyEngine CTC totals with IRS/Treasury tables, learn the residual by credit type and tax year, and let that residual move both the point estimate and interval width.",
  });

  send("forecast", {
    pointEstimate,
    ciLow,
    ciHigh,
    confidence: 0.8,
    distribution: buildNumericCdfFromInterval({
      pointEstimate,
      ciLow,
      ciHigh,
    }),
    publicTrace: [
      `PolicyEngine current law policy ${policy.id} loaded successfully with API version ${policy.api_version}.`,
      "The current live public API path does not yet expose an absolute CTC outlay total, so the stream uses the calibrated current-law fallback.",
      "The adjustment layer is explicit and replaceable once CTC outlay calibration records are available.",
    ],
    assumptions: [
      "The public PolicyEngine current-law object reflects the operative policy baseline for this prototype.",
      "IRS/Treasury CTC outlay classification will be close to recent pre-expansion tax-year reporting.",
      "Tax-year timing differences are wider than the central current-law policy uncertainty.",
    ],
    dataCaveats: [
      "This stream verifies the policy object live but does not yet fetch an absolute CTC outlay result from PolicyEngine.",
      "The outlay calibration fallback is a prototype prior, not an observed backtest table.",
    ],
    drivers: [
      "Qualifying-child population",
      "Refundability cap",
      "Filing and take-up behavior",
      "IRS/Treasury reporting classification",
    ],
    source: "calibration_fallback",
    generatedAt: new Date().toISOString(),
  });
  send("status", {
    state: "complete",
    label: "Calibration fallback complete",
  });
  send("done", { ok: true });
}

async function streamCtcExpansionForecast(send: SendEvent) {
  await sendStep(send, {
    kind: "heading",
    text: "Identifying the question",
  });
  await sendStep(send, {
    kind: "text",
    text: "This stream forecasts the federal budget cost of a $3,000 fully refundable Child Tax Credit in tax year 2026, relative to current law. PolicyEngine supplies the raw microsimulation input; the forecast layer then adjusts that raw model output using an explicit calibration prior.",
  });

  const policyEngineCall = [
    `policyengine.policy.get({ id: ${CURRENT_LAW_POLICY_ID} })`,
    `policyengine.policy.get({ id: ${CTC_3000_FULLY_REFUNDABLE_POLICY_ID} })`,
    `policyengine.economy({ policy: ${CTC_3000_FULLY_REFUNDABLE_POLICY_ID}, baseline: ${CURRENT_LAW_POLICY_ID}, region: "us", time_period: ${CTC_TARGET_YEAR} })`,
  ].join("\n");

  send("status", {
    state: "tool_running",
    label: "Querying PolicyEngine API",
  });
  send("tool_start", {
    tool: "policyengine.api",
    call: policyEngineCall,
  });

  const dataset = await fetchCtcExpansionDataset();

  send("tool_result", {
    tool: "policyengine.api",
    call: policyEngineCall,
    result: [
      "baseline policy:",
      serializePolicyToolResult(dataset.baselinePolicy),
      "reform policy:",
      serializePolicyToolResult(dataset.reformPolicy),
      "economy impact:",
      serializeEconomyToolResult(dataset.economy),
    ].join("\n"),
  });
  await pause(180);

  await sendStep(send, {
    kind: "heading",
    text: "Raw PolicyEngine estimate",
  });
  await sendStep(send, {
    kind: "text",
    text: formatCtcExpansionSummary(dataset.summary),
  });

  const calibrationCall =
    'brier.calibration.lookup({ domain: "policyengine_budget_scores", policy_area: "ctc", outcome: "federal_budget_cost" })';
  send("status", {
    state: "tool_running",
    label: "Looking up calibration prior",
  });
  send("tool_start", {
    tool: "brier.calibration",
    call: calibrationCall,
  });
  send("tool_result", {
    tool: "brier.calibration",
    call: calibrationCall,
    result: JSON.stringify(dataset.calibration, null, 2),
  });

  await sendStep(send, {
    kind: "heading",
    text: "Calibration adjustment",
  });
  await sendStep(send, {
    kind: "math",
    text: `calibrated cost = raw_or_prior × ${dataset.calibration.rawToFinalRatio.toFixed(2)} + $${dataset.calibration.additiveUsdBillions.toFixed(1)}B = $${dataset.summary.calibratedPointEstimateUsdBillions.toFixed(1)}B`,
  });
  await sendStep(send, {
    kind: "text",
    text: "The point estimate starts from PolicyEngine because it encodes the law and population model. The calibration layer exists because the target is the most accurate public forecast, not loyalty to any one simulator: it can learn systematic score differences by policy area, variable, population, and time horizon.",
  });

  send("status", {
    state: "model_running",
    label: "Generating calibrated forecast",
  });
  await sendStep(send, {
    kind: "heading",
    text: "Forecast model",
  });

  const forecast = await generateCtcExpansionForecast(dataset);
  for (const trace of forecast.publicTrace) {
    await sendStep(send, {
      kind: "text",
      text: trace,
    });
  }

  if (forecast.assumptions.length > 0) {
    await sendStep(send, {
      kind: "heading",
      text: "Assumptions and caveats",
    });
    await sendStep(send, {
      kind: "text",
      text: [
        ...forecast.assumptions.map(
          (assumption) => `Assumption: ${assumption}`,
        ),
        ...forecast.dataCaveats.map((caveat) => `Caveat: ${caveat}`),
      ].join(" "),
    });
  }

  send("forecast", forecast);
  send("status", {
    state: "complete",
    label:
      forecast.source === "ai_gateway"
        ? "AI Gateway forecast complete"
        : "Calibration fallback complete",
  });
  send("done", { ok: true });
}

async function sendStep(
  send: SendEvent,
  step:
    | { kind: "heading"; text: string }
    | { kind: "text"; text: string }
    | { kind: "math"; text: string },
) {
  send("step", step);
  await pause(step.kind === "heading" ? 180 : 260);
}
