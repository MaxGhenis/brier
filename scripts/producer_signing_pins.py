"""Code-pinned policy for Thesis record-snapshot producer signatures."""

from __future__ import annotations

# ``receipt`` is pinned by exact version and artifact hash in this repository.
# Any receipt upgrade must pass this repository's full suite and producer-signing
# tests at the new pin before the dependency bump lands.
SIGNATURE_DOMAIN = b"thesis-record-snapshot/v1\0"
SIGNATURE_SUFFIX = ".producer.sig"
PUBLIC_KEY_RELPATH = "records/trust/producer-ed25519.pem"

# Dormant until the separately reviewed trust-root ceremony. The ceremony sets
# both values in the same commit that adds PUBLIC_KEY_RELPATH.
PRODUCER_SPKI_SHA256: str | None = None
ACTIVATION_SNAPSHOT: str | None = None


def producer_signing_active() -> bool:
    """Return whether the producer-signing policy is consistently armed."""

    if PRODUCER_SPKI_SHA256 is None and ACTIVATION_SNAPSHOT is None:
        return False
    if PRODUCER_SPKI_SHA256 is not None and ACTIVATION_SNAPSHOT is not None:
        return True
    raise ValueError("producer signing pins are half-armed")
