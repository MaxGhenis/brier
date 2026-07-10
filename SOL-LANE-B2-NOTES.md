# Lane B2 handoff: second independent RFC 3161 anchor

## Result

Lane B2 adds DigiCert as the second independent timestamp authority. The
immutable `tsa-anchors-v2` bundle is additive: it repeats the unchanged FreeTSA
anchor from v1 and adds DigiCert Trusted Root G4. The existing v1 bundle, root,
markers, and tokens are untouched.

The current checked-in chain still has only v1 active. Merely adding and
code-pinning v2 does not authorize it. The first recorder snapshot made after
this change must carry the exact v2 bundle reference and must be successfully
witnessed under already-active v1. Only then does replay activate v2.

## TSA selection and live-token evidence

DigiCert was selected over Sectigo. Both candidates granted SHA-256 RFC 3161
sample requests, but DigiCert returned consistently across repeated requests,
its independently sourced root was straightforward to establish, and its real
`-cert` response verified offline without any fetched intermediate or system
trust input. DigiCert HTTPS timed out during the probe; its documented public
HTTP endpoint worked consistently. HTTP transport affects availability and
privacy, not trust: every returned token is verified against the committed
root, code-pinned root and signer SPKIs, signed imprint, policy, and signed
time before it is recorded.

Probe environment:

```text
OpenSSL 3.6.3 9 Jun 2026 (Library: OpenSSL 3.6.3 9 Jun 2026)
platform: darwin64-arm64-cc
```

One representative request used:

```bash
OPENSSL_CONF=/dev/null openssl ts -query \
  -config /dev/null \
  -data payload.txt \
  -sha256 \
  -cert \
  -out request.tsq

curl -fsS \
  -H 'Content-Type: application/timestamp-query' \
  --data-binary @request.tsq \
  http://timestamp.digicert.com \
  -o digicert.tsr
```

The response was:

```text
HTTP 200
Content-Type: application/timestamp-reply
Status: Granted
Policy OID: 2.16.840.1.114412.7.1
Hash Algorithm: sha256
genTime: Jul 10 16:05:52 2026 GMT
Imprint algorithm OID: 2.16.840.1.101.3.4.2.1
```

Four separately requested tokens used the same policy and signer identity.
The repository verifier also accepted a fifth live token through the new
`verify_timestamp_token` path.

The exact offline check used the signed `genTime` as `-attime`, an empty CA
directory, `/dev/null` for `SSL_CERT_FILE`, and only the separately fetched
self-signed root as `-CAfile`:

```bash
export OPENSSL_CONF=/dev/null
export LC_ALL=C
export SSL_CERT_DIR="$PWD/empty-ca"
export SSL_CERT_FILE=/dev/null

openssl ts -verify \
  -config /dev/null \
  -data payload.txt \
  -in digicert.tsr \
  -CAfile digicert-root-official.pem \
  -CApath empty-ca \
  -attime 1783699552
```

```text
Using configuration from /dev/null
Verification: OK
```

The separate CMS purpose check was:

```bash
openssl ts -reply \
  -config /dev/null \
  -in digicert.tsr \
  -token_out \
  -out digicert-token.der

openssl cms -verify \
  -inform DER \
  -in digicert-token.der \
  -CAfile digicert-root-official.pem \
  -no-CApath \
  -no-CAstore \
  -purpose timestampsign \
  -attime 1783699552 \
  -signer digicert-signer.pem \
  -out tst-info.der
```

```text
CMS Verification successful
```

This keeps the existing Ubuntu OpenSSL 3.0 compatibility constraint: do not
add `-CAstore file:/dev/null`. Ubuntu 3.0 rejects that store URI. The pinned
`-CAfile` plus empty `-CApath` is used for `ts`; `cms` uses `-no-CApath
-no-CAstore`.

The token embeds the complete untrusted chain needed by OpenSSL:

1. `DigiCert SHA256 RSA4096 Timestamp Responder 2025 1`;
2. `DigiCert Trusted G4 TimeStamping RSA4096 SHA256 2025 CA1`;
3. a DigiCert Trusted Root G4 cross-certificate issued by DigiCert Assured ID
   Root CA.

OpenSSL builds that chain to the separately fetched, self-signed DigiCert
Trusted Root G4 in the pinned CA file. No AIA fetch, system root, token-adjacent
CA file, or downloaded sidecar is trust input.

## Independent root acquisition

Channel 1 was DigiCert's official certificate endpoint:

```text
https://cacerts.digicert.com/DigiCertTrustedRootG4.crt.pem
```

Channel 2 was the Mozilla CCADB Included CA report, independently listing the
root fingerprint and linking the crt.sh object downloaded here:

```text
https://ccadb.my.salesforce-sites.com/mozilla/IncludedCACertificateReport
https://crt.sh/?d=552F7BDCF1A7AF9E6CE672017F4F12ABF77240C78E761AC203D1D9D20AC89988
```

The official and CCADB/crt.sh downloads were both 1,988 bytes and matched
byte-for-byte:

```text
PEM SHA-256   ce7d6b44f5d510391be98c8d76b18709400a30cd87659bfebe1c6f97ff5181ee
DER SHA-256   552f7bdcf1a7af9e6ce672017f4f12abf77240c78e761ac203d1d9d20ac89988
SPKI SHA-256  59df317bfa9f4f0ab7ca514d7772296aa2c765b87664d08b96e57399e364729c
Serial        059B1B579E8E2132E23907BDA777755C
Subject       CN=DigiCert Trusted Root G4,OU=www.digicert.com,O=DigiCert Inc,C=US
Issuer        CN=DigiCert Trusted Root G4,OU=www.digicert.com,O=DigiCert Inc,C=US
Validity      2013-08-01T12:00:00Z through 2038-01-15T12:00:00Z
```

crt.sh was intermittently unavailable with HTTP 502, but a successful
uppercase-fingerprint request returned HTTP 200, `application/pkix-cert`, and
the exact official bytes. As a third independent check, the certificate
extracted from `https://curl.se/ca/cacert.pem` (generated from Mozilla's root
store) used different 76-column PEM wrapping:

```text
Mozilla-derived PEM SHA-256  affe31abf15cee77a2e194496278ac6a86915666de6e49fa3934d44849413640
DER SHA-256                  552f7bdcf1a7af9e6ce672017f4f12abf77240c78e761ac203d1d9d20ac89988
SPKI SHA-256                 59df317bfa9f4f0ab7ca514d7772296aa2c765b87664d08b96e57399e364729c
Serial                       059B1B579E8E2132E23907BDA777755C
Subject                      CN=DigiCert Trusted Root G4,OU=www.digicert.com,O=DigiCert Inc,C=US
```

The channel results therefore agree on the certificate. The committed PEM is
the byte-identical official/CCADB-crt.sh form.

## Real signer pins

The allowed policy and signer came from the live tokens, not documentation:

```text
Policy OID              2.16.840.1.114412.7.1
Signer PEM SHA-256      f8ecbaae3ef6421377063a31d238b1cee48060528791854d3d3fcda965d565e6
Signer DER SHA-256      4aa03fa22cd75c84c55c938f828e676b9caecab33fe36d269aa334f146110a33
Signer SPKI SHA-256     7abda95ed7301ac94bded350babc319903d0b4f16c4e7e39346dba5f9e992b72
Signer serial           0A80EF184B8DF10582D1C476A7957468
Signer subject          CN=DigiCert SHA256 RSA4096 Timestamp Responder 2025 1,O=DigiCert\, Inc.,C=US
Signer validity         2025-06-04 through 2036-09-03
```

The signer has critical `CA:FALSE`, critical digital-signature key usage, and
critical time-stamping EKU. The embedded timestamping intermediate has DER
SHA-256 `ca0b1554ecd901ea19dcad8749e9f2648c8d6dfcea1add9d2c2109415bb82ccd`.

## Immutable v2 bundle

Committed bundle values:

```text
Path                   records/trust/tsa-anchors-v2.json
Bundle ID              tsa-anchors-v2
Raw SHA-256            b8ece84adcc354f413f10f1b3999ac99679196b9391d76a9967369047b7d7716
Canonical JSON SHA-256 036737fdd779f5add77b79262d9967e4bac450ff3ab7132eb929dbf893a4c396
Size                   1916 bytes
```

The file is canonical JSON according to `scripts/canonical_json.py`. v1 remains
the genesis bootstrap and remains active after v2 activation; the verifier
requires new witnesses to use the highest active version, so subsequent
markers use v2 rather than falling back to v1.

The genesis enumeration checks the fixed source Git tree and the bytes of its
enumerated files. It does not reject additional post-cutover files. The normal
chain verifier passed with both new `records/trust/` files present, confirming
that these additions do not mutate or invalidate the cutover enumeration.

## Multi-token witness schema

Historical `thesis_rfc3161_witness_v1` markers keep their original parser and
continue to verify unchanged. New markers use `thesis_rfc3161_witness_v2`:

- top-level bundle fields identify the newest already-active evidence bundle;
- `anchorOutcomes` contains exactly one outcome for every anchor in that
  bundle;
- an `available` outcome carries a token path/hash and optional extracted
  claims, all of which are re-derived and checked;
- an `unavailable` outcome carries a reason and is forbidden from carrying any
  token-evidence field;
- top-level `available` requires at least one verified authoritative token;
- a claimed invalid token rejects the complete marker even when another token
  verifies;
- one verified outcome plus one explicit unavailable outcome is accepted as a
  degraded witness, while an omitted anchor outcome is rejected;
- `validate_token_time` and all root, signer, policy, imprint, CMS-purpose, and
  code-pin checks run independently for every claimed token.

For the transition only, `supplementalOutcomes` records newly introduced TSA
requests. A supplemental available token is still fully pin-verified, but it
cannot make the marker available and cannot activate its own bundle. Thus run
#1 requests both services while only the already-active FreeTSA/v1 token can
authorize v2. After v2 activates, both services move into authoritative
`anchorOutcomes`.

`WitnessEvidence` retains the full verified token tuple and uses the earliest
authoritative signed time as its scalar chronology time. The witnessed timeline
normalizes v1 and v2 through that evidence and never uses supplemental time as
authority.

## Transition and producer mechanics

`verify_chain` now returns both active bundle references and replay-pending
updates. The recorder uses that verifier-owned state rather than duplicating
the activation algorithm. It emits the exact v2 reference only if the bundle
has not already been introduced. An unavailable transition leaves the existing
update pending, so later snapshots do not duplicate it; the next available
old-bundle witness covers and activates the pending update.

The witness writer uses the verifier's pending-tail mode. That mode validates
the new snapshot as the unique direct child of the committed head while
replaying and verifying the committed prefix normally. It therefore knows the
actual active set before the new snapshot without temporarily moving files or
reimplementing trust replay.

The activation order remains fail-closed:

1. verify the current marker only against bundles active before its snapshot;
2. parse its code-pinned bundle updates;
3. activate pending updates only when that marker is `available`.

A v2 token on the snapshot that introduces v2 is rejected. An unavailable
FreeTSA transition does not activate v2. Once a FreeTSA/v1 token successfully
covers the transition, the next snapshot must select v2 and must record one
outcome for each of FreeTSA and DigiCert.

## Exact integrator sequence

1. Review the dirty tree, run the verification commands below, commit the code,
   bundle, root, tests, workflow, and this handoff, then push that commit to
   `main`. Do not add or edit any historical record artifact.
2. Dispatch the recorder once from that pushed `main`. Recorder run #1 must:
   - create a snapshot whose `trustBundleUpdates` is a one-element list exactly
     equal to the code-pinned `tsa-anchors-v2` reference above;
   - write a v2 witness marker whose top-level `trustBundleId` is
     `tsa-anchors-v1`;
   - show FreeTSA in `anchorOutcomes` and DigiCert in
     `supplementalOutcomes` with role `pending_trust_bundle`;
   - have `status: available` because the FreeTSA token verified under v1;
   - pass the full chain verifier, which should report v2 active at the head.
3. Wait for recorder run #1's record commit to reach `main`, then dispatch the
   recorder again from that new head. Recorder run #2 must:
   - omit `trustBundleUpdates`;
   - write a v2 marker whose top-level `trustBundleId` is `tsa-anchors-v2`;
   - have exactly two `anchorOutcomes`, one for FreeTSA and one for DigiCert;
   - show both outcomes `available` to complete the two-authority integration;
   - have an empty `supplementalOutcomes` list and pass full chain verification.

If FreeTSA is unavailable on run #1, the committed marker must be
`unavailable`, v2 must remain pending, and the next recorder run must still use
v1 authoritatively while retrying both TSAs. Do not interpret a successful
supplemental DigiCert token as activation. Repeat until an available FreeTSA/v1
witness covers the pending transition; only then perform the v2 follow-up run.
After v2 activation, a one-token marker is verifier-valid and may be committed
as explicitly degraded. It does not complete this integration handoff. If run
#2 lacks either token, repeat the recorder until a descendant has successful
FreeTSA and DigiCert outcomes on the same digest.

Useful inspection commands after each run:

```bash
jq '{trustBundleUpdates}' records/YYYY-MM-DD/digest-RUN.json
jq '{schemaVersion,status,trustBundleId,anchorOutcomes,supplementalOutcomes}' \
  records/YYYY-MM-DD/digest-RUN.witness.json

UV_CACHE_DIR=/tmp/brier-uv-cache \
uv run --python 3.12 --no-project python \
  scripts/verify_record_chain.py records
```

## Verification

- The official and CCADB/crt.sh root downloads matched byte-for-byte; the
  Mozilla-derived bundle copy matched their DER and SPKI.
- Five independent DigiCert live tokens used the pinned signer and policy. A
  fresh token passed the repository's `verify_timestamp_token` path.
- A temporary real v2 marker containing fresh FreeTSA and DigiCert tokens over
  one digest passed `verify_witness` with two `TokenEvidence` rows.
- `scripts/canonical_json.py` reproduced the committed v2 bytes and canonical
  hash.
- `actionlint .github/workflows/record-forecasts.yml`: passed.
- Ruff check and Black 26.3.1 formatting/check on all changed Python: passed.
- Focused record-integrity and synthetic transition/writer suite: 42 passed.
- The exact requested full-suite command ran every test. The only errors were
  the 17 known `tests/test_figures.py` setup errors: the sandboxed Matplotlib
  font-cache subprocess exited by signal 6. No test body failed; 421 passed and
  one was skipped.
- The full suite with only that known figure module excluded: 421 passed and
  one skipped.
- `scripts/verify_record_chain.py records`: eight snapshots, seven available
  historical witnesses, v1 active, v2 not pending, current head verified.
- `scripts/witnessed_timeline.py --check`: 277 runs, 67 custody roots, and 28
  registration snapshots; generated artifacts current.
- `git diff --check`: passed.

## Residual risks

- The live DigiCert signer expires in September 2036 and the pinned root in
  January 2038. Any signer rotation needs an audited successor bundle and an
  already-active-bundle-witnessed transition; silently widening the signer set
  is not acceptable.
- A public TSA can be unavailable or rate-limited. One verified token is enough
  for chronology, but a one-token marker is explicitly degraded and lacks
  same-snapshot corroboration from the other authority.
- Until an available FreeTSA/v1 witness covers run #1, FreeTSA is a single point
  of transition liveness. Its permanent disappearance before that event would
  prevent v2 activation and require a separately reviewed recovery design; a
  DigiCert supplemental token cannot self-authorize the new bundle.
- The two authorities are organizationally and cryptographically independent,
  but this design does not require a two-of-two quorum. It follows the required
  availability rule that either independently pinned token can witness a
  digest.
- The current repository head does not activate v2. The two live recorder runs
  above are part of integration, not something this disposable implementation
  clone can pre-authorize.
- Synthetic tests exercise full RFC 3161 verification with locally generated
  root-to-signer chains, while DigiCert's real response uses a three-level,
  cross-certified chain. That real chain passed local OpenSSL 3.6.3, but no
  binary live-token fixture is committed for CI. Run #2 must show DigiCert
  `available` under Ubuntu OpenSSL 3.0 before Lane B2 is considered integrated.
- Sidecar certificate downloads, if a later workflow adds them for archival
  context, must never become `-CAfile`, chain, signer, or identity input.
