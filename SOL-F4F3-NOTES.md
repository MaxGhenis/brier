# F4+F3 implementation notes

## Design

The recorder now creates one immutable `digest-<workflowRunId>-<attempt>.json`
per invocation. It archives every fetched JSON response as deterministic gzip,
records raw and compressed hashes, links the immediately preceding invocation,
and updates a separately mutable head commitment. Day indexes are convenience
lists only and are not accepted as chain evidence.

Before recording, the workflow fetches `/build.json`, fetches the referenced
commit, and requires `git merge-base --is-ancestor <deployed> <attested>` to
succeed. It also archives the live build payload and the GitHub API response
for the `PolicyEngine/arch-data` `codex/thesis-ledger-facts` branch, including
that branch's commit SHA.

The analyst runner now writes `custody_root.json` after all run artifacts and
then writes the manifest once with `custodyRootSha256` as the final field. Raw
hashes bind exact bytes; canonical hashes bind JSON content across Python and
TypeScript. The manifest self hash excludes only its own artifact entry and
the custody-root field, as declared by `manifestHashSemantics`.

Generated waves dated 2026-07-10 or later must record their input batch
manifests in the generated header. CI reconstructs the newest such wave and
requires byte-for-byte equality. Earlier modules are grandfathered because
their complete input-batch provenance was not retained consistently; no
historical module was modified by this package.

## Genesis contents

`records/CHAIN_GENESIS.json` names
`records/2026-07-09/digest-f4f3-genesis.json`. That cutover node explicitly
does not claim a new live fetch. The genesis enumerates all 28 legacy daily
digests and their exact hashes: 2026-06-11 through 2026-06-29, then 2026-07-01
through 2026-07-09. There is no 2026-06-30 digest. Legacy membership is exact:
an added, removed, or changed `digest.json` fails verification.

The cutover was prepared in the network-disabled sandbox, so its sibling
witness marker explicitly says `unavailable`. All workflow-created successors
attempt an RFC 3161 witness.

## RFC 3161 verification

Verify a token with the CA and signer certificates archived beside it:

```bash
sha256sum records/YYYY-MM-DD/digest-RUN.json
openssl ts -reply -in records/YYYY-MM-DD/digest-RUN.tsr -text
openssl ts -verify \
  -data records/YYYY-MM-DD/digest-RUN.json \
  -in records/YYYY-MM-DD/digest-RUN.tsr \
  -CAfile records/YYYY-MM-DD/digest-RUN.tsa-ca.pem \
  -untrusted records/YYYY-MM-DD/digest-RUN.tsa.crt
```

The digest must match the witness JSON and OpenSSL must print
`Verification: OK`. Confirm the archived certificate hashes match the witness
JSON, then review their fingerprints and dates.

## Integrator verification requiring network or writable git metadata

This sandbox has no network and `.git` is read-only. The integrator must:

1. Dispatch `record-forecasts.yml` once as a recorder dry run and confirm the
   deployed build SHA passes the ancestry gate, all gzip bodies decompress,
   the ledger API commit is present, and a new per-run digest links the
   cutover/head.
2. Exercise the FreeTSA call from the Actions runner. Confirm an available
   `.tsr` verifies with OpenSSL. Also simulate an unreachable TSA and confirm
   the workflow commits an explicit `status: unavailable` witness instead of
   silently omitting it.
3. Run the full GitHub Actions suite, including the new
   `wave-reproducibility` job, and a real post-marker `register_wave.py` flow so
   the non-skipping byte-diff path is exercised.
4. Confirm the deployed `/log.json` and `/brier/reward.json` expose
   `custodyRootSha256` for the first promoted custody-era run.

## Deliberately deferred

Historical analyst runs and generated modules were not rewritten or
retroactively rooted. Their old self-invalidating manifest entries remain
historical facts; enforcement begins with newly produced runs/waves. FreeTSA
certificate pinning is also deferred: the workflow records and validates the
RFC 3161 response structure, while third-party verification supplies the
current trust chain and inspects its fingerprints.
