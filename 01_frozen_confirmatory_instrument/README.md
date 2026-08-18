# Frozen Confirmatory Instrument

This directory preserves the exact source-code instrument used for the preregistered confirmatory experiment.

The authoritative software identity is defined by the SHA-256 manifest recorded before confirmatory execution.

The frozen instrument consists of twelve Python source files:

- `benchmark.py`
- `classificador.py`
- `dryrun.py`
- `equivalencias.py`
- `escala.py`
- `gerador.py`
- `pontuacao.py`
- `test_classificador.py`
- `test_equivalencias.py`
- `test_escala.py`
- `test_gerador.py`
- `test_pontuacao.py`

The corresponding authoritative manifest is:

- `hashes-finais-dev.txt`

## Integrity rule

Files placed in this directory must match the preregistered SHA-256 manifest exactly.

No post-confirmatory modification, refactoring, cleanup, or correction belongs in this directory.

Any later analysis code must be archived separately under `03_post_confirmatory/`.
