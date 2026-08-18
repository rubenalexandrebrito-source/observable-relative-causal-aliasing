# Observable-Relative Causal Aliasing

Reproducibility repository for the study:

**Observable-Relative Causal Aliasing**

Author: **Ruben Brito**

## Scientific status

```
CONFIRMATORY RESULT: NEGATIVE
```

```
C1′: 199/200   (E1: 150/150 · E2: 49/50)
passa = false
```

The single C1′ confirmatory error is instance `7bb0baab3a8ed7aa` (family 20, System II, Stratum E2). The two other scored confirmatory candidates also failed: C2 with 74 errors, C3 (a canary, outside the scientific hypothesis) with 75 errors.

Post-confirmatory analyses characterize the mechanism and scope of that single failure. **They do not alter, reinterpret, rescue, or retroactively validate the preregistered confirmatory result.** No replacement criterion ("C1″") exists anywhere in this repository. `199/200` is never presented as a near-positive or essentially-passed outcome.

## Epistemic chronology

| Stage | Status |
|---|---|
| Preregistration + amendments | `PREREGISTERED` |
| Confirmatory E1 / E2 | `CONFIRMATORY` |
| Negative scoring result | `CONFIRMATORY` |
| Failure autopsy | `POST-CONFIRMATORY` |
| Mechanism analyses (WS1–WS5) | `POST-CONFIRMATORY` |
| Prevalence study | `POST-CONFIRMATORY` |
| Temporal h=2 analysis | `POST-CONFIRMATORY` |
| Prior-art audit | `POST-CONFIRMATORY` |
| Manuscript scientific-content freeze | `MANUSCRIPT` |

Full chain, with every intermediate step: `06_reproducibility/PROVENANCE.md`.

## Repository map

| Directory | Contents |
|---|---|
| `00_preregistration/` | The preregistration protocol (executable form only — no separate prose document exists), the one recovered amendment, and the first (failed) official gate's development records. |
| `01_frozen_confirmatory_instrument/` | The exact 12-file instrument that produced the confirmatory result, with its authoritative SHA-256 manifest. |
| `02_confirmatory_execution/` | The complete confirmatory run: orchestrator, environment, benchmark, dry-run/gate, blinded E1/E2 generation, scoring, seeds, integrity (unblinded keys). |
| `03_post_confirmatory/` | Autopsy, prevalence study, five independent workstreams (WS1–WS5), temporal horizon-2 synthesis, prior-art audit, and coordinator/red-team verification. |
| `04_phase6_closure/` | Phase 6 synthesis and formal closure, the interpretive-epistemology notes, article architecture, claim–evidence ledger, and frozen Methods/Results sections. |
| `05_manuscript/` | The canonical frozen manuscript, `ARTICLE1-SUBMISSION-CONTENT-FREEZE-v1.0`. |
| `06_reproducibility/` | This documentation: reproduction guide, provenance chain, file inventory, missing-artifact register, and the packaging-provenance incident record. |

## Scope limitation

**System I / System II / System III** and the **STATE / SIGNAL** classifier labels are pre-specified operational targets of a controlled synthetic testbed. They are not, by themselves, a claim of universal ontology for physical, biological, communicative, or conscious systems. The study asks whether a frozen interventional classifier preserves a designed mechanistic distinction under blinding, scale projections, and admissible representational equivalences — nothing in this repository establishes that these labels are a universal taxonomy of interaction in natural systems.

## Programme context and scope

The preregistered experiment archived here was originally designated **BOUNDARY I** within a broader multi-stage research programme concerning causal individuation and, ultimately, questions about consciousness. The present repository concerns BOUNDARY I and the technical post-confirmatory analyses arising from it only.

It does not constitute validation, audit, or empirical support for BOUNDARY II–V or for the broader claims about consciousness discussed elsewhere in that research programme.

BOUNDARY I produced a negative preregistered confirmatory result. The subsequent work archived here characterizes the identifiable mechanism underlying that failure and does not convert the negative confirmatory outcome into a positive result.

The broader programme's originating theoretical article is not archived in this repository; it is cited here only by title, author, and date, per the repository owner's explicit decision (see `06_reproducibility/CHECKS.md`).

## Reproducibility

See `06_reproducibility/REPRODUCE.md` for integrity verification, unit/instrument test re-execution, and the scientific-replay policy.

## Citation

See `CITATION.cff`.

## Archival release

Version 1.0.0 has been permanently archived on Zenodo.

**Version DOI:** 10.5281/zenodo.21995651
**Concept DOI (all versions):** 10.5281/zenodo.21995650
**GitHub release:** v1.0.0

<https://doi.org/10.5281/zenodo.21995651>

The immutable archival release is identified by Git tag `v1.0.0`.
The `main` branch may contain subsequent non-scientific metadata or documentation updates; the archived v1.0.0 scientific package remains unchanged.

## Licensing

Original project code: MIT (`LICENSE-CODE`). Original documentation, data, and derived scientific artifacts: CC BY 4.0 (`LICENSE-DATA`). See `LICENSE` for the full breakdown, including third-party material.

## Repository release status

The archival release for version 1.0.0 is complete: Git tag `v1.0.0`, GitHub Release `v1.0.0`, and the corresponding Zenodo deposit have all been published under the DOIs above. See `06_reproducibility/CHECKS.md` for the current repository-visibility status.
