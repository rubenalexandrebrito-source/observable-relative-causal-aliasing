# BOUNDARY I — OPEN-01 RESOLUTION: C4 STATUS

**Date:** 17-08-2026  
**Question:** Was C4 an executable/scored confirmatory candidate in the final frozen v8.3 instrument?  
**Verdict:** **NO. OPEN-01 CLOSED.**

## Evidence recovered

The Library contains `prereg-A-final.zip`, created on 14-08-2026, containing the 12-file final instrument. The archive was materialized and inspected directly.

### `classificador.py`

Header: `Pré-registo A v8.3. Marco 3.`  
It states that the classifier **implements exclusively the frozen definitions**, then enumerates:
- C1′;
- C2;
- C3, explicitly described as an analytic canary.

No C4 implementation is present.

### `dryrun.py`

The official dry-run harness states that it runs **C1′, C2 and C3** internally and discards their classifications.

### `escala.py`

All candidate export/comparison loops are over:

`("C1p", "C2", "C3")`.

### `equivalencias.py`

Candidate discrepancy structures and comparisons are over:

`C1p`, `C2`, `C3`.

### `pontuacao.py`

The scoring loop is:

`for cand in ("C1p", "C2", "C3")`.

The final confirmatory decision is:

`positivo` iff `veredicto["C1p"]["passa"] OR veredicto["C2"]["passa"]`.

The returned note explicitly states:

`C3 é canário e não entra em H_A.`

An exact-token scan across all 12 Python files found **zero occurrences of `C4`**.

## Integrity

Key source hashes recovered from the final archive:

- `classificador.py`  
  `ecaa40c6fa2abf84751811cbe5490073bb68e790ab1d5e135ea9342256b046a3`
- `pontuacao.py`  
  `028f5a0327c3e3437ffc6df03d10d45d9a06c3d0ff267795caa6f9e751fe0f57`
- `dryrun.py`  
  `43473e07e65d268a285208a410edc14ae69dc93a7a6e572ca74a3957dd54fd21`
- `escala.py`  
  `40ccd532e583b05665b2fbed8bd2a63f18a4300615f6dba7fb3eaaa73e05cca7`
- `equivalencias.py`  
  `c87cdb38da3b468488671dc7f752cd9d7e06effaf9485ece937e9fa2716ec389`

These match the recorded final development manifest.

Archive SHA-256:

`d77dbed47779f47b11e365b375504fb124585e140f20b06e66e0094309627aa6  prereg-A-final.zip`

## Narrow conclusion

> **C4 was not an executable or scored confirmatory candidate in the final frozen v8.3 instrument. C1′ and C2 were the candidates capable of making H_A positive; C3 was an implementation canary and did not enter H_A.**

This resolves the selective-reporting concern for the manuscript: Results/Methods should report C1′, C2 and C3 with those exact roles, and should not invent a confirmatory C4 result.

## Historical caution

This recovery does not establish the exact prose used for C4 in older drafts. If an earlier protocol version contained a conceptual C4 fallback, that belongs to development history. It is not part of the final executable/scored confirmatory instrument established above.

`OPEN-01 — CLOSED`
