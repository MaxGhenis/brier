# Lane B handoff: chain anchors, custody completeness, witnessed chronology

## What changed

- `scripts/build_genesis_enumeration.py` builds the canonical
  `records/GENESIS_RECORDS.json` from the exact Git tree fixed by the first
  chained snapshot:
  `0a57bfc58ea3578cf3c43b3edd2d414813566ce8`. The artifact enumerates 4,754
  regular files (635,115,664 bytes) by path, SHA-256, and size. The verifier
  binds the source commit and legacy tip to the already-chained first snapshot,
  code-pins the audited enumeration reference, and, when `.git` is present,
  compares membership, sizes, and blob bytes to the source Git tree.
- `records/2026-07-10/digest-genesis-enumeration-v1.json` is the unique
  enumeration cutover. It commits the enumeration, `CHAIN_GENESIS.json`, the
  immutable TSA bundle, all eight existing custody roots, and both registration
  snapshots. A second/replacement genesis cutover is rejected.
- TSA trust now starts from the immutable
  `records/trust/tsa-anchors-v1.json` bundle and
  `records/trust/freetsa-root-2016.pem`. The verifier code independently pins
  the bundle hash, root SPKI, and allowed signer SPKI; token-sidecar CA files
  are never trust input. It checks the CMS chain at signed `genTime`, exact
  signer identity, policy OID, SHA-256 message-imprint OID and length, creation
  claims, and a strict `genTime <= now` bound.
- Future TSA expansion is possible but not self-authorizing: add an immutable
  versioned bundle, add its audited hash/root/signer identities to the verifier
  code pins, and introduce it in a chain snapshot whose token verifies under an
  already active bundle. A public TSA timestamp alone cannot authorize a new
  trust root.
- The three existing available witness markers now record the immutable bundle
  ID/path/hash, anchor ID, policy, imprint algorithm, signed time, signer DER
  hash, and signer SPKI. Verification re-extracts these values from each token.
- Custody inventory v2 is exact and mode-specific. Analyst runs require the
  complete prompt/invocation/stdout/stderr/raw/parsed/normalized/distribution/
  validation/activity inventory, with complete Codex and review-stage bundles.
  Manifest and root hash/size claims must agree, every JSON artifact has a
  canonical hash, unsafe aliases and symlinks fail, and every directory file
  must be referenced exactly once. Failed or validation-incomplete analyst
  runs can have complete custody but are not verifier-side headline eligible.
- Legacy roots remain verifiable but are labeled `legacy-incomplete`; they are
  never headline eligible. `scripts/resolve_pending.py` now emits and
  self-verifies resolver-v2 roots over its exact archived source responses.
  `scripts/record_forecast_snapshot.py` enforces/self-verifies recorder-v2
  surface, live-forecast, and v3 log-chunk inventories and commits all current
  verified custody roots and registration snapshots into each new digest.
- `scripts/witnessed_timeline.py` emits deterministic canonical JSON at
  `records/witnessed-timeline.json`. It maps only externally witnessed run
  directories, custody roots, and registrations. Custody-root commitments are
  `direct`; run contents and manifest-derived registrations are `transitive`.
  Root rows also carry `custodyInventoryVersion`, `inventoryStatus`, and
  verifier-side `headlineEligible`.

## One-shot enumeration and cutover

The dirty tree already contains the output of this command. Do not append it a
second time:

```bash
UV_CACHE_DIR=/tmp/brier-uv-cache \
uv run --python 3.12 --no-project python \
  scripts/build_genesis_enumeration.py \
  --source-commit 0a57bfc58ea3578cf3c43b3edd2d414813566ce8 \
  --output records/GENESIS_RECORDS.json \
  --append-cutover \
  --cutover-recorded-at 2026-07-10T03:33:26Z
```

The integrator should run the reproducibility check before committing:

```bash
UV_CACHE_DIR=/tmp/brier-uv-cache \
uv run --python 3.12 --no-project python \
  scripts/build_genesis_enumeration.py \
  --source-commit 0a57bfc58ea3578cf3c43b3edd2d414813566ce8 \
  --output records/GENESIS_RECORDS.json \
  --check
```

Expected enumeration values:

- entries: `4754`
- total source bytes: `635115664`
- raw and canonical SHA-256:
  `b4d3d7033e3c5f81cbaf31c76ae1b029746f53803edbae228935899826a59f5d`
- pending cutover digest SHA-256:
  `7d298fb2c17a5d5f66f8cbfa6976f4048eb1f4b7adedb76562c30e5ac04dea8e`

## Independently audit the FreeTSA pins

The sandbox had no network. The committed root was initially recovered from
the identical CA sidecars beside the three existing tokens; the `.tsr` token
files themselves are different. Before merge, independently fetch the CA and
signer from FreeTSA's official HTTPS certificate endpoints, separately from
the timestamp request:

```bash
ANCHOR_AUDIT=$(mktemp -d)
curl -fsS https://freetsa.org/files/cacert.pem \
  -o "$ANCHOR_AUDIT/freetsa-root.pem"
curl -fsS https://freetsa.org/files/tsa.crt \
  -o "$ANCHOR_AUDIT/freetsa-tsa.crt"

shasum -a 256 "$ANCHOR_AUDIT/freetsa-root.pem"
openssl x509 -in "$ANCHOR_AUDIT/freetsa-root.pem" -outform DER \
  | openssl dgst -sha256
openssl x509 -in "$ANCHOR_AUDIT/freetsa-root.pem" -pubkey -noout \
  | openssl pkey -pubin -outform DER | openssl dgst -sha256

shasum -a 256 "$ANCHOR_AUDIT/freetsa-tsa.crt"
openssl x509 -in "$ANCHOR_AUDIT/freetsa-tsa.crt" -outform DER \
  | openssl dgst -sha256
openssl x509 -in "$ANCHOR_AUDIT/freetsa-tsa.crt" -pubkey -noout \
  | openssl pkey -pubin -outform DER | openssl dgst -sha256

cmp "$ANCHOR_AUDIT/freetsa-root.pem" records/trust/freetsa-root-2016.pem
```

Expected audited identities:

- root PEM SHA-256: `2151b61137ffa86bf664691ba67e7da0b19f98c758e3d228d5d8ebf27e044438`
- root DER SHA-256: `a6379e7cecc05faa3cbf076013d745e327bbbaa38c0b9af22469d4701d18aabc`
- root SPKI SHA-256: `52c54ba340885605314daa1857c8763b94087d05c636092938d4e2d1818e99b5`
- signer PEM SHA-256: `8bfb0305bb64e2571ca507552ef3245cb1c2fee8728e0ff8689225081ea13467`
- signer DER SHA-256: `32e841a95cc1164101ffde41298ef2fc75c1c4372ef095e88a6bbd47dfb191fc`
- signer SPKI SHA-256: `fa02bd555e3e483d62b4e70be6218692068d2b0b0a7525db58dcbf2901cdb072`
- signer serial: `C2E986160DA8E9CD`
- timestamp policy OID: `1.2.3.4.1`
- message-imprint OID (SHA-256): `2.16.840.1.101.3.4.2.1`
- immutable bundle raw SHA-256:
  `737bc9a149726f375edaebcd39b34116d90a5d29e9a043bcb0437998928e5791`

Repeat the fingerprint check from a second independently controlled network or
device if possible. If the live certificate differs, stop and establish
whether FreeTSA intentionally rotated it; do not silently rewrite the v1 pin.

## Obtain the external cutover witness

The cutover marker is intentionally `status: unavailable`. Request a standard
SHA-256 RFC 3161 token over the exact current digest bytes:

```bash
DIGEST=records/2026-07-10/digest-genesis-enumeration-v1.json
QUERY=$(mktemp)
openssl ts -query -data "$DIGEST" -sha256 -cert -out "$QUERY"
curl -fsS \
  -H 'Content-Type: application/timestamp-query' \
  --data-binary @"$QUERY" \
  https://freetsa.org/tsr \
  -o records/2026-07-10/digest-genesis-enumeration-v1.tsr

openssl ts -verify \
  -data "$DIGEST" \
  -in records/2026-07-10/digest-genesis-enumeration-v1.tsr \
  -CAfile records/trust/freetsa-root-2016.pem
```

Replace the unavailable witness marker with an available marker containing the
token path/hash plus `trustBundleId`, `trustBundlePath`, `trustBundleSha256`,
`tsaAnchorId`, `tsaPolicyOid`, `tsaImprintAlgorithmOid`, `tsaGenTime`, signer
certificate hash, and signer SPKI. Lane A must update its witness writer to
emit these fields and verify only against the committed root; a freshly
downloaded sibling CA must remain archival, never trusted. Do not change the
digest after requesting the token.

Then run:

```bash
UV_CACHE_DIR=/tmp/brier-uv-cache \
uv run --python 3.12 --no-project python scripts/verify_record_chain.py records

UV_CACHE_DIR=/tmp/brier-uv-cache \
uv run --python 3.12 --no-project python scripts/witnessed_timeline.py
```

Lane A should regenerate/check `records/witnessed-timeline.json` only after a
new digest has its witness marker. This lane intentionally did not edit
`.github/workflows/` or `scripts/docket_publication.py`.

## Verification performed

- Ruff on all changed Python and focused test files: passed.
- Python 3.12 `tests/test_record_integrity.py`: 26 passed.
- Python 3.12 `tests/test_resolve_pending.py`: 3 passed.
- Python 3.12 `tests/test_thesis_analyst_runner.py`: 21 passed, including
  sealed forecaster/reviewer process-start failures.
- Combined focused run: 50 passed.
- Offline chain: five snapshots, three available code-pinned witnesses, pending
  cutover head.
- Enumeration `--check`: 4,754 entries and the expected hash above.
- Committed timeline regeneration/check: canonical and empty while the cutover
  remains unwitnessed. A positive extractor fixture yields 218 run directories,
  eight roots, and two registrations, with direct/transitive labels checked.

The requested command with `--with pytest` was attempted, but uv tried to
contact PyPI and this sandbox has no DNS. The equivalent installed-Python 3.12
command used pytest 8.4.1:

```bash
UV_CACHE_DIR=/tmp/brier-uv-cache \
uv run --python /opt/homebrew/bin/python3.12 --no-project \
  python -m pytest tests/test_record_integrity.py -q
```

A broader suite run reached 282 passed and 1 skipped, with 17 setup errors
because the sandboxed Matplotlib figure generator aborted while building its
font cache; no Lane B test failed.

## Residual risk

- Until the cutover or a chained successor has a valid code-pinned external
  token, the enumeration and current roots have no externally proven time. The
  empty committed timeline is intentional fail-closed output.
- All eight current roots are v1 `legacy-incomplete`. A later witness proves
  when those bytes existed; it cannot make their inventories complete.
- Only one independent TSA is currently approved. Adding a second requires an
  independently audited immutable bundle, verifier-code pins, and an
  old-bundle-witnessed transition.
- Resolver v2 now seals the source response archives actually produced, but it
  still does not preserve the input Thesis log/chunks, ledger before/after,
  push response, or resulting ledger commit. Those require a future inventory
  version if they become eligibility requirements.
- Site headline enforcement remains in the site lane. It should require a
  matching timeline custody-root entry whose `inventoryStatus` is `complete`
  and `headlineEligible` is true; timeline absence is unproven chronology.
