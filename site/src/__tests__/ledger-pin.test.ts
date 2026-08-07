import { createHash } from "node:crypto";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  fetchPinnedPolicyEngineLedgerBytes,
  type PolicyEngineLedgerPin,
} from "@/data/thesis-log";

const OBSERVATIONS = '{"source_record_id":"series.test.2030","value":1}\n';
const CATALOG = '{"generator_version":1,"series":[]}\n';

function sha256(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

function pin(
  overrides: Partial<PolicyEngineLedgerPin> = {},
): PolicyEngineLedgerPin {
  return {
    schemaVersion: "thesis_ledger_pin_v1",
    repo: "PolicyEngine/ledger",
    branch: "codex/thesis-ledger-facts",
    sha: "a".repeat(40),
    jsonlSha256: sha256(OBSERVATIONS),
    jsonlBytes: Buffer.byteLength(OBSERVATIONS),
    lineCount: 1,
    pinnedAtUtc: "2030-01-01T00:00:00Z",
    ...overrides,
  };
}

function installFetch(files: ReadonlyMap<string, string>) {
  const mock = vi.fn(async (input: RequestInfo | URL) => {
    const body = files.get(String(input));
    return body === undefined
      ? new Response("missing", { status: 404 })
      : new Response(body, { status: 200 });
  });
  vi.stubGlobal("fetch", mock);
  return mock;
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("PolicyEngine ledger pin", () => {
  it("keeps legacy pins compatible without fetching a series catalog", async () => {
    const legacyPin = pin();
    const observationsUrl =
      `https://raw.githubusercontent.com/${legacyPin.repo}/${legacyPin.sha}/` +
      "ledger/official_observations.jsonl";
    const fetchMock = installFetch(new Map([[observationsUrl, OBSERVATIONS]]));

    const raw = await fetchPinnedPolicyEngineLedgerBytes(legacyPin);

    expect(raw.equals(Buffer.from(OBSERVATIONS))).toBe(true);
    expect(fetchMock).toHaveBeenCalledOnce();
    expect(fetchMock).toHaveBeenCalledWith(observationsUrl);
  });

  it("fetches and verifies catalog bytes at the same exact commit", async () => {
    const catalogPin = pin({
      catalogSha256: sha256(CATALOG),
      catalogBytes: Buffer.byteLength(CATALOG),
    });
    const baseUrl = `https://raw.githubusercontent.com/${catalogPin.repo}/${catalogPin.sha}/ledger/`;
    const observationsUrl = `${baseUrl}official_observations.jsonl`;
    const catalogUrl = `${baseUrl}series_catalog.json`;
    const fetchMock = installFetch(
      new Map([
        [observationsUrl, OBSERVATIONS],
        [catalogUrl, CATALOG],
      ]),
    );

    await fetchPinnedPolicyEngineLedgerBytes(catalogPin);

    expect(fetchMock).toHaveBeenNthCalledWith(1, observationsUrl);
    expect(fetchMock).toHaveBeenNthCalledWith(2, catalogUrl);
  });

  it("rejects catalog bytes that disagree with their pin", async () => {
    const catalogPin = pin({
      catalogSha256: sha256(CATALOG),
      catalogBytes: Buffer.byteLength(CATALOG),
    });
    const baseUrl = `https://raw.githubusercontent.com/${catalogPin.repo}/${catalogPin.sha}/ledger/`;
    installFetch(
      new Map([
        [`${baseUrl}official_observations.jsonl`, OBSERVATIONS],
        [`${baseUrl}series_catalog.json`, '{"tampered":true}\n'],
      ]),
    );

    await expect(
      fetchPinnedPolicyEngineLedgerBytes(catalogPin),
    ).rejects.toThrow("refusing to build against an unpinned ledger catalog");
  });

  it.each([{ catalogSha256: "b".repeat(64) }, { catalogBytes: 123 }])(
    "rejects a partial catalog commitment before fetching",
    async (partial) => {
      const fetchMock = installFetch(new Map());

      await expect(
        fetchPinnedPolicyEngineLedgerBytes(pin(partial)),
      ).rejects.toThrow("catalogSha256 and catalogBytes together");
      expect(fetchMock).not.toHaveBeenCalled();
    },
  );
});
