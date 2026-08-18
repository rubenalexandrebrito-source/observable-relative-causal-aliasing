# Gate 1 — Historical pre-Amendment-2 gate

**Outcome:** `NAO_PASSA_GATE_72H` (`T_total_horas ≈ 102.14`)
**Not the final admissible gate for confirmatory execution.**

This is the *first* official execution of Fases 0–3, run against the original, pre-Amendment-2 instrument (`00_preregistration/protocol/`). Its failure to clear the 72-hour gate under the original sequential `equivalencias.py`/`dryrun.py`/`test_equivalencias.py` directly motivated Pre-data Amendment No. 2 (deterministic 3-way parallelization). It is preserved here in full, unaltered, as a historically real gate occurrence — not superseded or deleted, only superseded *procedurally* by Gate 2 below.

## Gate-specific artifacts (physically present in this directory)

These differ from Gate 2's corresponding files and are **not deduplicated**:

| File | SHA-256 |
|---|---|
| `hashes-codigo.txt` | `c02cc8a495e2b98056d0d40c9a18d8d809ed6b0b756778d2e006d9b5a1607158` |
| `benchmark-oficial.json` | `1bbc9ed7aae453fef47c98a2cccae2a846bd97a2f0bd8b3dd98737c123885a7e` |
| `dryrun-tempos.json` | `0c115071ae1f12c6195566e90a0353e2ffedc65ae1c40308bd1e4daed590c7bc` |
| `registo-fases-0-3.json` | `e7c7245688581c938931299d34fca6415f52c50801f1c260fa6a34c3ca9ce195` |
| `fases-0-3-oficial.log` | (full transcript of this gate's run) |

`hashes-codigo.txt` differs from Gate 2's precisely because it records the three files Amendment 2 changed — this is the expected, confirmed evidence that the two gates ran under genuinely different instrument states, not an inconsistency.

## Shared artifacts (byte-identical to Gate 2 — physically stored once, in `../shared_payload/`)

Verified SHA-256-identical between this gate and Gate 2 (see `06_reproducibility/PACKAGING-PROVENANCE-INCIDENT.md` for the full verification method): the dry-run selector produced the same 15-case sample, and the same seed generation (`gerador.py`, unaffected by Amendment 2) produced the same blind instances, because the amendment touched only the exhaustive-equivalence check, not the generator or the selector.

| Historical path (as it existed for this gate) | Repository representation | SHA-256 | Status |
|---|---|---|---|
| `hardware.txt` | `../shared_payload/hardware.txt` | `57758630eed557c21b4cf395d28f1a8948d61727e2c651e69ddf7f53121b44f8` | BYTE-IDENTICAL SHARED ARTIFACT |
| `dryrun-seleccao.json` | `../shared_payload/dryrun-seleccao.json` | `fa574828ba58c61aabd246acc3c712bdd480153e8e49c7ff89db6a11b97da9f4` | BYTE-IDENTICAL SHARED ARTIFACT |
| `dry-e1/manifesto.json` | `../shared_payload/dry-e1/manifesto.json` | `a757abca6894737b1917e4cf3ecb7454a676462893f96b68cc5c56e57f6a4ab6` | BYTE-IDENTICAL SHARED ARTIFACT |
| `dry-e1/instancias/` (150 files) | `../shared_payload/dry-e1/instancias/` | (150/150 individually verified identical) | BYTE-IDENTICAL SHARED ARTIFACT |
| `dry-e2/manifesto.json` | `../shared_payload/dry-e2/manifesto.json` | `3c18be2d64e8cf0983aca14205f551096d2c34985b9e8b56c3230d33309347c5` | BYTE-IDENTICAL SHARED ARTIFACT |
| `dry-e2/instancias/` (50 files) | `../shared_payload/dry-e2/instancias/` | (50/50 individually verified identical) | BYTE-IDENTICAL SHARED ARTIFACT |
| `dry-e1-CHAVE-NAO-ABRIR.json` | `../shared_payload/dry-e1-CHAVE-NAO-ABRIR.json` | `dea498d919247d64ba412eeb119c7cdec5f22227d3c73c82ef5e023e747e49d3` | BYTE-IDENTICAL SHARED ARTIFACT |
| `dry-e2-CHAVE-NAO-ABRIR.json` | `../shared_payload/dry-e2-CHAVE-NAO-ABRIR.json` | `1f95cdb427679da5db0f01ab918e72b110568c69741206af27a683f5d74d5e9e` | BYTE-IDENTICAL SHARED ARTIFACT |

**This deduplication is physical only.** It does not erase this gate's historical occurrence of these artifacts — this document is that occurrence's permanent record.

## Epistemic status

`ARCHIVAL-METADATA` / development record. This is not the confirmatory execution. The confirmatory execution ran under the instrument validated by Gate 2 (`../gate2_PASSA/`).
