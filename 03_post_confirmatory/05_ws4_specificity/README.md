# WS4 — System-III structural specificity (incl. horizon-2)

> POST-CONFIRMATORY / EXPLORATORY

Tests whether System III (the true "SIGNAL" architecture) can produce a symmetric false positive under the frozen statistic, and whether that safety extends beyond the frozen one-step horizon.

## Key results

- **Theorem III-1** (h=1, exact): the XOR-interventional field is identically null for System III at the frozen horizon; `P(memory dependence | III) = 0` analytically, `0/4000` edges empirically. No symmetric failure mode exists at h=1.
- **Theorem III-2** (h=2, composition): this first-order cancellation is **not** stable under direct composition (`T∘T`). Empirically, `dep2 > 0` in 3,996/4,000 System-III edges (99.90%); 4/4,000 exceptions. See `../07_temporal_horizon2/` for the dedicated synthesis of this result.

This is a **two-pass** report: the first pass (h=1 only) is preserved separately in `run1-snapshot/` (frozen at 14:15:44 UTC, before the h=2 extension); the final report supersedes it with the h=2 analysis added, and explicitly narrows the first pass's over-strong framing (it originally implied full-class safety; the true boundary is horizon-1-exact).

## Contents

- `WS4-CLASSIII-SPECIFICITY.md` — final (two-pass) report.
- `medicao_ws4_classIII.py`, `contraste_II_ws4.py`, `auditoria_ws4_2a.py`, `horizonte2_ws4.py` and their outputs — h=1 measurement, System-II contrast reference, second-pass audit, and h=2 measurement.
- `precommit-ws4-classIII-especificidade.txt`, `precommit-ws4-adenda-h2-auditoria.txt` — pre-commitments for each pass.
- `run1-snapshot/` — the frozen first-pass report and its raw outputs, plus `PRESERVATION-NOTE.txt` explaining the snapshot timing.
- `SHAS.txt` — manifest of this workstream's own files.

## Epistemic status

`POST-CONFIRMATORY`.
