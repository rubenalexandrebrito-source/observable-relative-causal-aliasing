# ARTICLE 1 — METHODS 4.1–4.9 v0.2 — CLAIM / SOURCE MAP

**Purpose:** internal audit companion to `ARTICLE1-METHODS-4.1-4.9-v0.2.md`; not manuscript prose.
**Supersedes:** `ARTICLE1-METHODS-4.1-4.9-v0.1-CLAIM-MAP.md` (kept intact as historical record).

## Section map (unchanged structure from v0.1)

| Methods section | Frozen claims / status | Principal source basis |
|---|---|---|
| 4.1 | CE-006; preregistered operational targets | `gerador.py`; `pontuacao.py`; Architecture v2.1 |
| 4.2 | CE-005, CE-051; generation/blinding provenance | `gerador.py`; C4 Status Resolution; Formal Closure |
| 4.3 | CE-001–CE-007, CE-018–CE-020, CE-051; frozen classifier and scoring logic | `classificador.py`; `escala.py`; `equivalencias.py`; `pontuacao.py` |
| 4.4 | CE-012/013/018/019 definitions used by post-confirmatory analysis | frozen classifier; WS1/WS2/Synthesis |
| 4.5 | CE-026–CE-028 | WS3 Strict Realized Dynamics; Synthesis |
| 4.6 | CE-008–CE-010 | frozen `gerador.py`; WS1/WS5/Synthesis |
| 4.7 | CE-011–CE-013 | WS1/WS2/Synthesis |
| 4.8 | CE-014–CE-015 | Synthesis §17; frozen Architecture / Ledger |
| 4.9 | CE-016–CE-017 | WS1; WS2; Synthesis; independently reconstructed 6×6 map (rank 6, det −8, re-verified in red-team with exact arithmetic) |

## v0.1 → v0.2 delta map

Every v0.2 addition is a description of the frozen record; **no ledger row is expanded and no new claim is introduced.**

| Red-team item | v0.2 change (location) | Exact source basis | Ledger anchor |
|---|---|---|---|
| RT-M1 (MAJOR) | 4.3: degenerate-context rule for memoryless receivers ({⊥}, full-space fiber, trivially STATE) + ring consequence | `classificador.py:136` (`mem_reach[i]=[None]  # conjunto contextual singular {⊥}`), `:163` (full-space fiber); `test_classificador.py` `test_receptor_sem_memoria_e_estado` (all three candidates) | CE-018–CE-020 (edge event and instance-level collapse condition; frozen-code fact) |
| RT-m2 (MINOR) | 4.3: integrity audit list now includes G_C invariance under equivalence conjugations (instrument-level annulment) | `pontuacao.py:109` (`discrepancias_base != 0` ⇒ violation); `equivalencias.comparar` → `BASE` (Amendment 1, item 3) | CE-001/CE-005 provenance frame; frozen-code fact |
| RT-m3 (MINOR) | 4.3: canary condition stated (both channel→processor edges in G_C and C3-STATE in all 75 confirmatory System-II instances, 50 E1 + 25 E2) | `pontuacao.py` `_canario` + docstring lines 14–17 | CE-004 (C3 role); frozen-code fact |
| RT-m4 (MINOR) | 4.5 and 4.6: explicit post-confirmatory provenance sentences (covering 4.5 and 4.6–4.9) | Architecture v2.1 §0.9 (visible chronology); claim-map boundary "post-confirmatory formalization does not modify C1′" | CE-005 |
| RT-m5 (MINOR) | 4.3: scale item "in both confirmatory strata" + "projected media computed but not scored; component relation only" | `escala.py:19–22` (COBERTURA POR ESTRATO), `:24–27` (compares EXCLUSIVAMENTE componentes; media não pontuados); `pontuacao` scale item over `escala_e1` and `escala` | CE-002 context; frozen-code fact |
| RT-m6 (MINOR) | 4.2: initial processor/memory/interface states sampled uniformly | `gerador.py:83–86` (`sample_theta_base`) | CE-006 context; frozen-code fact |
| RT-c7 (COSMETIC) | 4.2: "two independent forms of label destruction" → "two separate label-destroying randomizations" | `gerador.exportar_instancia` (two draws from the export stream; no independence property asserted by source) | — |
| — (admin) | Title/status header and footer tag updated to v0.2 | version bookkeeping only | — |

## Boundaries preserved (re-affirmed for v0.2)

- STATE/SIGNAL are operational targets, not natural-system ontology.
- The confirmatory outcome is not reinterpreted in Methods; `passa=false` untouched.
- C3 is a canary; C4 is absent from the final scored executable (CE-051 wording bounds respected).
- The post-confirmatory response-field formalization (4.4–4.9) does not modify C1′ — now stated explicitly in 4.5 and 4.6.
- `(r,c)` is used only for the separately labeled strict-realization analysis.
- The class-level symmetry result proves blindness, not automatically causal aliasing.
- The exact equivalence with `Iso(W_M)` is L1 only; L2 remains separate (4.10).
- The 6×6 determinant is a determining-set fact, not a novelty claim.
- L2, prevalence, temporal composition, and internal replication remain deferred to 4.10–4.15.
- No historical-priority, universality, or consciousness claim anywhere.

## Items deliberately deferred to 4.15 (unchanged)

The exact confirmatory root seed values, machine/software environment, complete file-hash manifest, one-use seed record, key-movement audit, exhaustive-run timing, and immutability details remain consolidated in 4.15.

`METHODS 4.1–4.9 v0.2 — SOURCE MAP — UPDATED AFTER RED-TEAM`
