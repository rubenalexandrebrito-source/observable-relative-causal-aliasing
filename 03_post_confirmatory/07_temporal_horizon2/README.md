# Temporal horizon-2 (III-2) — synthesis and pointer

> POST-CONFIRMATORY / EXPLORATORY

This directory contains no files of its own. The underlying scripts, precommit, and outputs live inside `../05_ws4_specificity/` (`auditoria_ws4_2a.py`, `horizonte2_ws4.py`, `ws4-auditoria-2a.json/.out`, `ws4-horizonte2.json/.out`, `precommit-ws4-adenda-h2-auditoria.txt`) and are **not duplicated here**, per the repository's no-unnecessary-duplication rule (`06_reproducibility/CHECKS.md`). This file exists to give the h=2 result its own entry point, as requested by the archival specification.

## Result

Seed `910000020` (shared with the rest of WS4's h=1 analysis).

```
h=2, memory-dependent decisive edges: 3,996 / 4,000  (dependency-null: 4/4,000)
Level distribution at h=2: L3 3,334 · L2 632 · L1 34
```

## Two distinct claims — kept separate

- **III-2a (analytic):** the h=1 cancellation identity is **not** algebraically stable under direct composition to `T²`; memory reappears inside response-row indices and memory-update selectors of the second-order expression. This is a proof, not a rate.
- **III-2b (empirical, exploratory):** in the studied sample, `dep2 > 0` in 3,996/4,000 System-III edges. This is a sample statistic, reported alongside its 4 exceptions, and is **never** presented as a theorem or as "III is always memory-dependent at h=2."

## Epistemic status

`POST-CONFIRMATORY`, exploratory for III-2b; analytic (III-2a) with empirical support. See `../05_ws4_specificity/README.md` for full provenance.
