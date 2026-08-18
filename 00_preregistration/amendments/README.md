# Amendments

*Archival packaging documentation.*

Only one pre-data amendment exists as a standalone original document.

## `PRE-DATA-AMENDMENT-3.txt`

Replaces the originally planned physical-coin-flip generation of the two confirmatory seeds (`S_E1`, `S_E2`) with an externally verifiable public randomness source: the drand League of Entropy `quicknet` beacon (`chain_hash 52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f6df89fa2c88a81848107`, genesis time 1692803367, period 3s). The amendment fixes the derivation rule (`round = 1 + ceil((TARGET_UNIX − genesis_time) / period)`), the pre-committed target round (31332238), and the collision check against the frozen 20-seed exclusion list, before any randomness was observed.

This document is also cross-referenced from `02_confirmatory_execution/seeds/`, where the resulting seed derivation records live.

## Amendments 1 and 2 — not archived as standalone documents

Neither Pre-data Amendment No. 1 nor Pre-data Amendment No. 2 exists as a standalone prose file in the recovered archive (server or local). Amendment 2's content (engineering-only deterministic parallelization) is recoverable only indirectly, via the code diff between `../protocol/` and `01_frozen_confirmatory_instrument/`. This is recorded as a missing critical artifact in `06_reproducibility/CHECKS.md`; it has not been reconstructed as prose.
