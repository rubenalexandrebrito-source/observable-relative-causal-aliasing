# Dry run — both official 72-hour gates

*Archival packaging documentation.*

This directory documents **both** official executions of Fases 0–3 (environment/benchmark/dry-run/gate) side by side, structured to make explicit what Pre-data Amendment No. 2 did and did not change.

## Structure

- **`shared_payload/`** — artifacts verified SHA-256-identical between the two gates (`hardware.txt`, `dryrun-seleccao.json`, the two dry-run hidden keys, and all 150 + 50 blind dry-run instances with their manifests). Physically stored once. Byte identity was demonstrated file-by-file, not assumed — see `06_reproducibility/PACKAGING-PROVENANCE-INCIDENT.md`.
- **`gate1_NAO_PASSA/`** — the first gate's genuinely gate-specific artifacts (`hashes-codigo.txt`, `benchmark-oficial.json`, `dryrun-tempos.json`, `registo-fases-0-3.json`, full log) plus `PROVENANCE.md`, which records where this gate's shared artifacts physically live and confirms their byte identity.
- **`gate2_PASSA/`** — the same, for the second (successful) gate.

## Why this structure

Deduplicating only the artifacts genuinely proven byte-identical — never the artifacts that differ, and never the historical fact that both gates occurred — keeps a single physical copy of the payload while preserving two distinct historical provenances. See each gate's `PROVENANCE.md` for the full historical-path ↔ repository-path ↔ SHA-256 mapping.

## Do not

Do not conclude from `shared_payload/` that the two gates were identical overall — they were not: they ran under different states of the instrument (Amendment 2 changed `dryrun.py`, `equivalencias.py`, `test_equivalencias.py`) and reached different gate outcomes. Each gate's `PROVENANCE.md` states this explicitly.

## Epistemic status

`CONFIRMATORY` for Gate 2 and the shared payload (both feed directly into the confirmatory execution); `ARCHIVAL-METADATA` for Gate 1's gate-specific artifacts (superseded procedurally, preserved historically).
