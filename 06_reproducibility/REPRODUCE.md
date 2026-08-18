# Reproduction Guide

*Archival packaging documentation.*

Environment used throughout: Python 3.14.4, NumPy 2.5.2 (see `02_confirmatory_execution/dry_run/shared_payload/hardware.txt`). No other third-party dependency was used by the frozen instrument.

## A. Integrity verification

Verify every archived file against this repository's root manifest:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

Verify only the frozen confirmatory instrument against its own authoritative manifest:

```bash
cd 01_frozen_confirmatory_instrument
shasum -a 256 -c hashes-finais-dev.txt
# Expected: 12/12 OK
```

## B. Unit / instrument verification

The frozen instrument ships five test suites (`test_classificador.py`, `test_equivalencias.py`, `test_escala.py`, `test_gerador.py`, `test_pontuacao.py`). During final archival assembly, all five were re-run in an isolated environment (Python 3.14.7 — the closest available patch to the confirmatory environment's recorded 3.14.4 — with NumPy 2.5.2, the exact recorded version), executed individually from inside `01_frozen_confirmatory_instrument/` (no repository-wide discovery): **70 tests, 0 failures, 0 errors.**

### Historical test-count discrepancy

A prior project summary referred to "50 tests across 5 suites". No surviving source snapshot examined during archival reconstruction yields exactly 50 tests.

Direct execution and static inspection (`grep -c "^    def test_"` per file) establish:

- preregistration-era pre-Amendment-2 snapshot (`00_preregistration/protocol/`): **58 tests** (9+13+8+17+11), executed and verified 58/58 OK;
- final post-Amendment-2 frozen instrument (`01_frozen_confirmatory_instrument/`): **70 tests** (9+25+8+17+11), executed and verified 70/70 OK.

The increase from 58 to 70 is fully accounted for by 12 additional deterministic tests introduced in `test_equivalencias.py` with Pre-data Amendment No. 2 (`test_workers_fixo_em_tres`, `test_workers1_igual_workers3_estruturalmente`, `test_paralelo_repetido_e_identico`, `test_agregador_paralelo_igual_referencia_sequencial`, `test_excepcao_de_worker_nao_e_silenciada`, `test_selector_dryrun_regra_pcg64_intacta`, `test_formula_T_equiv_inalterada`, and 5 others); the other four test files are byte-identical between the two snapshots.

The earlier value of 50 is therefore retained only as an unreconciled historical reference and is not used as an identifier of either archived source state:

```
Verified preregistration-era snapshot: 58 tests
Verified final frozen instrument:      70 tests
Historical reference to "50 tests":    NOT RECONCILED
```

To re-run the final frozen instrument's suite yourself in an isolated environment:

```bash
python3.14 -m venv /tmp/repro-env
/tmp/repro-env/bin/pip install numpy==2.5.2
cd 01_frozen_confirmatory_instrument
/tmp/repro-env/bin/python -m unittest test_classificador test_equivalencias test_escala test_gerador test_pontuacao -v
```

This exercises the *code*, not the confirmatory data — it does not consume any seed and produces no scientific result.

## C. Scientific replay

Any later replay of the confirmatory generation using the confirmatory seeds (`S_E1 = 3786434918`, `S_E2 = 3786434919`, see `02_confirmatory_execution/seeds/README.md`) or of any post-confirmatory precommitted seed listed in `03_post_confirmatory/` is a **reproduction of an already-completed experiment**, run for verification purposes on an existing, closed, immutable record — **it is not, and cannot become, a new confirmatory execution.** The preregistered confirmatory decision (`resultado_confirmatorio_A = "negativo"`) is closed and does not change based on any replay.

Post-confirmatory results retain **exploratory** epistemic status even when they had their own pre-commitment (fixed sample size, fixed seeds, fixed acceptance criteria declared before running). Pre-commitment strengthens an exploratory result's internal validity; it does not promote it to confirmatory status, and it does not constitute external scientific replication (see `PROVENANCE.md`).

No confirmatory or post-confirmatory generation was executed as part of preparing this repository. This guide documents how to do so, for a future reader, without doing so here.
