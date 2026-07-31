# Challenge inbox

External forecasters submit here: one PR adding
`inbox/<your-github-login>/<cell>.json` per forecast, schema
`thesis_challenge_submission_v1` (rules and full schema:
[docs/open-challenge.md](../docs/open-challenge.md)). Targets come from
the open registered docket; identity is the GitHub account that opens the
PR.

```json
{
  "schemaVersion": "thesis_challenge_submission_v1",
  "challenger": "github:your-login",
  "systemType": "ai",
  "systemName": "Your System 1.0",
  "dataPointId": "bls.jolts.hires_rate.2026_06.first_print",
  "pointEstimate": 3.3,
  "ciLow": 3.1,
  "ciHigh": 3.45,
  "generatedAtUtc": "2026-07-31T14:00:00Z",
  "notes": "optional, <=500 chars, rendered verbatim"
}
```

**Optional but recommended — sign your submission** so your two claims
(*this exact artifact*, *before the release*) verify without trusting this
repository ([docs/challenge-signing.md](../docs/challenge-signing.md)):

```bash
uvx --from sigstore sigstore sign inbox/<you>/<cell>.json
```

Commit the produced `<cell>.json.sigstore.json` bundle in the same PR.
Sign after your final edit — any byte change invalidates the signature.

This inbox is data-only staging: nothing reads it at build or score time.
Accepted submissions are published into `records/` by the attested
workflow path and scored identically to Thesis's own agents.
