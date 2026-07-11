# Local RFC 3161 test fixtures

Everything in this directory is **TEST ONLY**. The names `freetsa` and
`digicert` identify the production verifier slot that each local fixture stands
in for; these certificates are not issued by, affiliated with, or trusted by
either public TSA. Their private keys are deliberately committed and public.
Never add these roots to a system or application trust store.

`anchors/` is the verifier's trusted test anchor directory and intentionally
contains only the two independent local roots. `untrusted/root.pem` is kept
outside it so a receipt from the third signer exercises trust rejection. Each
receipt slot must remain mapped to its designated root: do not concatenate the
two roots into one permissive bundle for both suffixes, or one signer could fill
both nominally independent slots. Each signer certificate is directly issued by
its corresponding root and has critical
`CA:FALSE`, critical digital-signature key usage, and critical timestamping-only
extended key usage. Each root has critical `CA:TRUE,pathlen:0` and critical
certificate-signing/CRL-signing key usage.

OpenSSL increments `tsa-serial` whenever it mints a response. Tests should copy
this fixture tree to a temporary directory and run `openssl ts -reply` there,
rather than modifying the checked-in serial templates. For example, from the
repository root:

```sh
work="$(mktemp -d)"
cp -R tests/fixtures/release_tsa "$work/release_tsa"
printf '{"test":"manifest"}\n' > "$work/manifest.json"
openssl ts -query -data "$work/manifest.json" -sha256 -cert \
  -out "$work/request.tsq"
(
  cd "$work/release_tsa/freetsa"
  openssl ts -reply -config openssl-ts.cnf \
    -queryfile "$work/request.tsq" -out "$work/response.tsr"
)
digest="$(openssl dgst -sha256 -r "$work/manifest.json" | awk '{print $1}')"
openssl ts -verify -digest "$digest" -in "$work/response.tsr" \
  -CAfile "$work/release_tsa/anchors/freetsa-root-2016.pem"
```

Use the same commands with `digicert/` and
`anchors/digicert-trusted-root-g4.pem` for the second trusted response. A
response minted from `untrusted/` must fail verification against either trusted
anchor.
