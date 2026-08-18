# Confirmatory seeds

*Archival packaging documentation.*

## Seed values

```
S_E1 = 3786434918
S_E2 = 3786434919   (= S_E1 + 1, per the frozen derivation rule)
```

Both consumed **exactly once**, for the confirmatory generation now preserved in `../blinded_generation/`. Neither seed is ever reused anywhere in this repository, including in post-confirmatory exploratory work (`03_post_confirmatory/`), which draws exclusively on a disjoint, separately audited pool of seeds.

## Derivation (Pre-data Amendment No. 3)

The seeds were derived from the drand League of Entropy `quicknet` public randomness beacon rather than physical coin flips (see `../../00_preregistration/amendments/PRE-DATA-AMENDMENT-3.txt`).

- `precommit-ronda-drand.txt` — pre-committed target round (31332238) and derivation rule, written and hashed before the round's randomness was public.
- `drand-31332238-api.json`, `drand-31332238-api2.json`, `drand-31332238-cloudflare.json` — the round's randomness as independently retrieved from three official relays, cross-checked for agreement. These three files are byte-identical to each other by design, not by accidental duplication: they are independent observations of the same public randomness round, and their agreement is itself the intended verification (`duplicate_class = INTENTIONAL-INDEPENDENT-CORROBORATION` in `06_reproducibility/FILE-INVENTORY.csv`). Had any relay disagreed, the frozen protocol required recording the divergence and stopping.
- `congelamento.txt` — the formal Phase-4 freeze record ("Congelado nos termos da secção 11.2 do Pré-registo A v8.3").
- `sementes-confirmatorias.txt` — the final derived seed values and derivation arithmetic.

## Burned-seed audit

- `convencao-sementes-PRE-COMMIT.txt` — the pre-committed convention for what counts as a "used" seed (development, dry-run/selector, tests — union of all).
- `sementes-ja-usadas-auditoria.txt` / `-.CONGELAMENTO.txt` — the frozen 20-value exclusion-list audit, checked against the candidate confirmatory seeds before freezing, to rule out collision with any previously burned seed.
- `suplemento-lancamento-ambiguo-PRE-COMMIT.txt` — operational tie-break rule, fixed before any randomness was drawn (superseded in practice by the drand method, preserved for provenance).

Epistemic status: `CONFIRMATORY`.
