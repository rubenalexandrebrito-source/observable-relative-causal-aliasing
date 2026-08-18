# Preregistration and Amendments

*Archival packaging documentation — not a historical scientific artifact itself.*

This directory preserves the preregistration record governing the confirmatory experiment (internally designated **Pré-registo A v8.3**, the first formal test of the **BOUNDARY** research programme, referred to in later documents as **BOUNDARY I**).

## Contents

- **`protocol/`** — the frozen preregistration instrument exactly as it existed before the pre-data engineering amendment described below: the twelve Python source files plus their SHA-256 manifest (`hashes-finais-dev.txt`), and the confirmatory orchestrator (`fases_0_3.py`). This is the technical protocol in the only form it exists: **executable code**, not prose. No standalone prose "Guião" document was located during archival assembly (see `06_reproducibility/CHECKS.md`).
- **`amendments/`** — original amendment records that exist as standalone artifacts. Only **Pre-data Amendment No. 3** (external verifiable randomness via the drand quicknet beacon, replacing physical coin-flip generation of the confirmatory seeds) exists as a standalone document and is archived here.
- **`development_records/`** — the first official execution of Fases 0–3 (benchmark, dry run, timing gate), which resulted in `NAO_PASSA_GATE_72H` (T_total ≈ 102.14h) under the original sequential implementation. This result directly motivated **Pre-data Amendment No. 2** (see below).

## What is *not* in this directory

**Pre-data Amendment No. 2** (engineering-only: deterministic parallelization of the exhaustive-equivalence check via `WORKERS_EQUIV=3`, applied to `equivalencias.py`, `dryrun.py`, and `test_equivalencias.py`) does **not** exist as a standalone prose document. Its content is recoverable only indirectly, from:

1. the code diff between `protocol/` (this directory, pre-amendment) and `01_frozen_confirmatory_instrument/` (post-amendment) for exactly those three files;
2. the gate registries showing the transition from `NAO_PASSA_GATE_72H` (`02_confirmatory_execution/dry_run/gate1_NAO_PASSA/registo-fases-0-3.json`, ≈102.14h) to `PASSA_GATE_72H` (`02_confirmatory_execution/dry_run/gate2_PASSA/registo-fases-0-3.json`, ≈45.96h).

This is recorded as a missing critical artifact in `06_reproducibility/CHECKS.md`, not reconstructed as prose.

**Pre-data Amendment No. 1** (procedural/scope decisions made before the first official execution) similarly has no standalone document; it is not separately evidenced in the recovered archive at all.

## Programme context and scope

The preregistered experiment archived here was originally designated **BOUNDARY I** within a broader multi-stage research programme concerning causal individuation and, in its later stages, questions about consciousness. That broader programme is described in a separate theoretical article by the same author ("A consciência como interferência sedimentada"), which is **not** archived in this repository. This repository concerns BOUNDARY I and the technical post-confirmatory analyses arising from it only; it does not constitute validation, audit, or empirical support for any later stage of that programme. See the root `README.md`, section "Programme context and scope", for the full statement.

## Epistemic status

Materials in this directory are part of the preregistration provenance. They must not be modified to incorporate knowledge obtained from the confirmatory results or from subsequent post-confirmatory analyses.

Post-confirmatory analyses are archived separately under `03_post_confirmatory/`. The instrument actually used for the confirmatory execution (post-Amendment-2) is archived separately under `01_frozen_confirmatory_instrument/`.
