# Confirmatory Execution

*Archival packaging documentation.*

This directory preserves the complete provenance chain of the **preregistered confirmatory execution**, post-Amendment-2, on the registered machine, using the instrument frozen in `../01_frozen_confirmatory_instrument/`.

## Confirmatory result

```
resultado_confirmatorio_A = "negativo"
C1′: E1 = 150/150, E2 = 49/50, total = 199/200, passa = false
Single C1′ error: instance 7bb0baab3a8ed7aa, family 20, System II, Stratum E2
C2: 74 confirmatory errors. C3: 75 confirmatory errors.
```

Full scoring detail: `scoring/resultado-pontuacao-A.txt`.

## Sequence

1. **`orchestrator/`** — `fases_0_3.py`, external to the 12 frozen files, driving environment/benchmark/dry-run.
2. **`environment/`**, **`benchmark/`** — pointer-only; content consolidated into `dry_run/` (see below), since `hardware.txt`/`benchmark-oficial.json` needed direct side-by-side comparison with the first (pre-Amendment-2) gate to establish what was and was not affected by the amendment.
3. **`dry_run/`** — **both** official 72-hour gates, side by side: `shared_payload/` (artifacts verified byte-identical across both gates — `hardware.txt`, the dry-run selection, and all 150+50 dry-run instances), `gate1_NAO_PASSA/` (first gate, pre-Amendment-2, failed at `T_total ≈ 102.14h`; see also `../00_preregistration/development_records/`), and `gate2_PASSA/` (second gate, post-Amendment-2, **passed** at `T_total ≈ 45.96h`). Each gate folder has its own `PROVENANCE.md` with the full file-by-file SHA-256 mapping.
4. **`blinded_generation/`** — the actual confirmatory E1 (150) and E2 (50) instances, generated once with the confirmatory seeds and immediately blinded.
5. **`scoring/`** — classification, scale, exhaustive-equivalence, and final scoring outputs.
6. **`seeds/`** — the confirmatory seed derivation record (drand-based, Pre-data Amendment No. 3) and the burned-seed audit trail.
7. **`integrity/`** — the unblinded keys (opened only after scoring) and the mechanical Fase 5 execution log.

## Epistemic status

`CONFIRMATORY`. Everything in this directory is the literal, unaltered confirmatory record. It is not reinterpreted anywhere in this repository; post-confirmatory analysis (`03_post_confirmatory/`) explains the single error mechanistically without changing any value here.
