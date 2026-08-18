# WS5 — Failure-class structure

> POST-CONFIRMATORY / EXPLORATORY

Characterizes whether the 46/10,000 collapses form one mechanistic class or several, derives the alignment theorem governing when the ordinal (L2) route is possible at all, and explains the ~2.1–2.4× excess correlation between the two decisive edges of a collapsed instance.

## Key results

- One mechanistic class, with an *analytic* (not empirical-cluster) internal stratification into the exact (L1) and ordinal (L2) routes.
- **Alignment theorem:** if the induced action on the three perfect matchings of the channel alphabet fixes the unprobed matching, an L2 collapse is impossible on that edge — verified with zero exceptions across 21,390 aligned-cell edges (in-sample + OOS + RAW).
- The inter-edge correlation is fully explained (no unexplained residual beyond ~0.3–0.6σ) by the shared transport `τ` with independent per-edge geometries.

This is a **two-pass** report, like WS4: the first pass is preserved in `run1-snapshot/`; the final report adds a second-pass independent audit (a from-scratch reimplementation, 29/29 checks PASS) and an additional population-level assignment check (F4-bis).

## Contents

- `WS5-FAILURE-CLASS-STRUCTURE.md` — final (two-pass) report.
- `ws5_replay.py`, `ws5_analise46.py`, `ws5_correlacao.py`, `ws5_oos.py`, `ws5_taucheck.py`, `ws5_audit_agent2.py` and their outputs/logs — population replay, the 46-case analysis, the correlation model, out-of-sample/RAW validation, a sanity check of the transport-class sampling law, and the independent second-pass audit.
- `precommit-ws5-oos.txt`, `precommit-ws5-taucheck.txt`, `precommit-ws5-audit.txt` — pre-commitments.
- `run1-snapshot/` — the frozen first-pass report and raw outputs, plus `PRESERVATION-NOTE.txt`.
- `SHAS.txt` — manifest of this workstream's own files.

## Epistemic status

`POST-CONFIRMATORY`.
