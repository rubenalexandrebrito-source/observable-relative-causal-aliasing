# Gate 2 — Post-Amendment-2 gate

**Outcome:** `PASSA_GATE_72H` (`T_total_horas ≈ 45.96`)
**Final successful pre-confirmatory execution gate.**

This is the *second* official execution of Fases 0–3, run against the post-Amendment-2 instrument (`01_frozen_confirmatory_instrument/`). Its success authorized proceeding to Phase 4 (freeze) and Phase 5 (confirmatory execution, `../../blinded_generation/` and `../../scoring/`).

## Gate-specific artifacts (physically present in this directory)

These differ from Gate 1's corresponding files and are **not deduplicated**:

| File | SHA-256 |
|---|---|
| `hashes-codigo.txt` | `e371ace92974e241cd69f696d1ce823db46b90553ed1f4740ddfc55c9b71bf77` |
| `benchmark-oficial.json` | `76ba6cf846e3338399e41909c70e84a962c018fc46c03d796f936a0138ffad30` |
| `dryrun-tempos.json` | `de795f2069bd0f38f85879ff204eccb5ee528e6e88b247f0adbf5c070479a40a` |
| `registo-fases-0-3.json` | `604116946e676033e1b62f47c589f9544c4d6e1339911696bd93aef070eb3140` |
| `fases-0-3-amd2-oficial.log` | (full transcript of this gate's run) |

`hashes-codigo.txt` differs from Gate 1's precisely because it records the three files Amendment 2 changed (`dryrun.py`, `equivalencias.py`, `test_equivalencias.py`) — matches `01_frozen_confirmatory_instrument/hashes-finais-dev.txt` exactly.

## Shared artifacts (byte-identical to Gate 1 — physically stored once, in `../shared_payload/`)

Same table as `../gate1_NAO_PASSA/PROVENANCE.md`, from this gate's side:

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

Empirically, this demonstrates precisely what Amendment 2 did and did not change: **same** deterministic dry-run selection + **same** generated E1/E2 dry-run instances + **same** hidden keys, but **different** code manifest, benchmark timing, dry-run timing, and gate record — invariance of the generated payload, separated cleanly from the change in the instrument's and gate's formal state.

**This deduplication is physical only.** It does not erase this gate's historical occurrence of these artifacts — this document is that occurrence's permanent record.

## Epistemic status

`CONFIRMATORY`. This gate's success is what the confirmatory execution (`../../blinded_generation/`, `../../scoring/`) rests on.
