# Orchestrator

`fases_0_3.py` — drives Fases 0–3 (environment check, benchmark, dry-run timing selection, 72-hour gate decision) using the frozen instrument. It is intentionally external to the 12 frozen files (`../../01_frozen_confirmatory_instrument/`) and is byte-identical across the pre- and post-Amendment-2 trees (Amendment 2 touched only `equivalencias.py`, `dryrun.py`, `test_equivalencias.py`; sha256 `3e171881f294194322f2ee76f456143c5a91da5cf431d936289d75c91a9b1814`).

Epistemic status: `CONFIRMATORY` (procedural instrument, not itself a scientific result).
