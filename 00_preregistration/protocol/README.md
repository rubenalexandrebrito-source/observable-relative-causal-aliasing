# Protocol — original pre-Amendment-2 instrument

*Archival packaging documentation.*

> **Archival scope note**
>
> The original prose preregistration document has not been recovered.
> The materials preserved in this directory constitute the surviving executable
> source snapshot from the preregistration-era, prior to Pre-data Amendment No. 2.
> They are preserved as historical provenance and must not be interpreted as a
> reconstruction of, or substitute for, the missing prose preregistration.
>
> The final post-Amendment-2 frozen confirmatory instrument is archived separately
> under `01_frozen_confirmatory_instrument/`.

This directory preserves the surviving executable source snapshot from the initial preregistration-era freeze, before Pre-data Amendment No. 2 (deterministic parallelization engineering fix) was applied.

## Contents

- 12 Python source files (`benchmark.py`, `classificador.py`, `dryrun.py`, `equivalencias.py`, `escala.py`, `gerador.py`, `pontuacao.py`, `test_classificador.py`, `test_equivalencias.py`, `test_escala.py`, `test_gerador.py`, `test_pontuacao.py`) — byte-identical to the corresponding files in `../development_records/`'s execution and to the original hash manifest below.
- `hashes-finais-dev.txt` — the original SHA-256 manifest, sha256 `8522625f4049d01b01bc52609eaaf3211e18769426dbfb561d3c37f828b50785`.
- `fases_0_3.py` — the confirmatory orchestrator, sha256 `3e171881f294194322f2ee76f456143c5a91da5cf431d936289d75c91a9b1814` (unchanged by Amendment 2; identical to the orchestrator used post-amendment in `02_confirmatory_execution/orchestrator/`).

## Relationship to `01_frozen_confirmatory_instrument/`

Nine of the twelve files are byte-identical between this original version and the final instrument that actually produced the confirmatory result: `benchmark.py`, `classificador.py`, `escala.py`, `gerador.py`, `pontuacao.py`, `test_classificador.py`, `test_escala.py`, `test_gerador.py`, `test_pontuacao.py`.

Three files differ, reflecting Pre-data Amendment No. 2: `dryrun.py`, `equivalencias.py`, `test_equivalencias.py`. The amendment introduced deterministic 3-way parallelization (`WORKERS_EQUIV=3`, fixed, no auto-tuning) of the exhaustive-equivalence check, with proof of scientific identity (SHA-256-identical outputs between sequential and parallel execution) required before adoption. No standalone prose text of Amendment 2 was located; see `../README.md` and `06_reproducibility/CHECKS.md`.

## On the nine byte-identical files (deliberate, not accidental duplication)

Nine source files are byte-identical between this preregistration snapshot and the final frozen confirmatory instrument (`../../01_frozen_confirmatory_instrument/`) because Amendment 2 did not modify those files. Both path-level copies are intentionally retained to preserve the completeness and independent auditability of the two historical snapshots — each directory is meant to be self-contained and verifiable on its own, without requiring a reader to reach into a shared external location. See `06_reproducibility/FILE-INVENTORY.csv`, column `duplicate_class = EXPECTED-CROSS-SNAPSHOT-IDENTITY`.

`fases_0_3.py` is retained in both this historical/protocol provenance location and the execution-context location (`../../02_confirmatory_execution/orchestrator/`). Identical content does not imply accidental duplication; the two paths encode distinct archival roles (`duplicate_class = EXPECTED-CROSS-CATEGORY-IDENTITY`).

## Do not

Do not treat this directory as the instrument that produced the confirmatory result. That is `01_frozen_confirmatory_instrument/`. This directory exists purely to preserve the original preregistered state for provenance and audit.
