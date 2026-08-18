# Prevalence study

> POST-CONFIRMATORY / EXPLORATORY

Exploratory estimate of how often the family-20 failure mode recurs under the frozen generator law, using a sample size fixed *before* results were observed (anti optional-stopping).

## Result

```
N = 10,000 eligible System-II families (two pre-declared batches of 5,000)
System-II total collapses = 46/10,000 ≈ 0.46%   (95% CI ≈ [0.345%, 0.613%])
Seeds: 910000001 (batch 1), 910000002 (batch 2)
```

This is **not** confirmation of the original preregistered hypothesis, and is not a universal or natural-system prevalence — it is specific to the frozen generator law.

## Contents

- `prevalencia_cancelamento.py`, `prevalencia_cancelamento_lote2.py` — batch generation/measurement scripts.
- `prevalencia-cancelamento-II.json`, `prevalencia-cancelamento-II-lote2.json` — per-batch raw outputs.
- `prevalencia-combinada-N10000.json` — combined result.
- `precommit-lote2.txt` — pre-commitment of batch 2's parameters before running it.
- `verifica_E1_E2.py` / `.out` — verification of the `d_E2 = 4·d_E1` transfer lemma (downstream D-modules causally inert for the statistic), letting n=10 measurements transfer exactly to the confirmatory n=12 regime.
- `condicao_L1.py` → `condicao-L1-insample.json`, `condicao_L1_oos.py` → `condicao-L1-oos.json`, `precommit-oos-condicaoL1.txt` — the algebraic condition K for L1, verified in-sample and on a pre-committed out-of-sample draw.
- `combina_prevalencia.py` — combination utility.

## Epistemic status

`POST-CONFIRMATORY`, exploratory. See `../../04_phase6_closure/` for how this feeds the closed synthesis.
