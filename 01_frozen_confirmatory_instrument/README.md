# Frozen Confirmatory Instrument

*Archival packaging documentation.*

This directory preserves the exact source-code instrument that produced the preregistered confirmatory result, **post**-Amendment-2 (deterministic 3-way parallelization of the exhaustive-equivalence check).

The authoritative software identity is defined by the SHA-256 manifest recorded before confirmatory execution: `hashes-finais-dev.txt`, sha256 of the manifest file itself: `995d42dde0070310b6f214ce0398cf1cd89644bf8d79af56823c41bf31ed83d7`.

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

## Integrity rule

Files placed in this directory must match the manifest exactly. Verify with:

```
shasum -a 256 -c hashes-finais-dev.txt
```

Expected: `12/12 OK`.

No post-confirmatory modification, refactoring, cleanup, or correction belongs in this directory. Any later analysis code is archived separately under `03_post_confirmatory/`.

## Source provenance

Pulled directly from the registered execution server, path `causal-A-amd2-official/prereg-A/` — the directory protected by the filesystem immutable attribute (`chattr +i`) throughout the confirmatory execution and afterward. Verified 12/12 self-consistent against its own manifest, and 12/12 identical to `frozen-copy/`, the reference copy independently verified by all five post-confirmatory workstreams (WS1–WS5) before their own analyses.

**Note on the nine byte-identical files:** nine of these twelve files are also present, byte-identical, in `00_preregistration/protocol/` (Amendment 2 changed only `dryrun.py`, `equivalencias.py`, `test_equivalencias.py`). This is deliberate, not accidental duplication — see `00_preregistration/protocol/README.md` and `06_reproducibility/FILE-INVENTORY.csv` (`duplicate_class = EXPECTED-CROSS-SNAPSHOT-IDENTITY`). This directory remains fully self-contained regardless.

**Note on an earlier, superseded packaging attempt:** during final archival assembly, a separate local working copy (used for an unrelated prior manuscript-Methods review task) was found to contain three files — `dryrun.py`, `equivalencias.py`, `test_equivalencias.py` — from the *original, pre-Amendment-2* instrument (`00_preregistration/protocol/`) despite being labeled as the final v8.3 instrument. That copy was never used to identify or reproduce the confirmatory instrument for this archive; it played no role in the confirmatory execution or in any post-confirmatory analysis, all of which ran against the server-resident, immutable, AMD2-official tree verified here. Full investigation: `06_reproducibility/PACKAGING-PROVENANCE-INCIDENT.md`.
