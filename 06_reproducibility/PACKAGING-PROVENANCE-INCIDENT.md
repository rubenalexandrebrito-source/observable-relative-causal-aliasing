# Packaging Provenance Incident — Frozen Instrument Mismatch

**Status:** investigated and resolved during archival assembly of this repository. Discovered before any public release. Retained here permanently as a transparency record — it is not hidden, deleted, or corrected retroactively.

## Summary

A local working copy used for an earlier, unrelated task (an adversarial review of manuscript Methods sections 4.1–4.9, conducted in a different session on this author's machine, folder `DEVIN-METHODS-4.1-4.9-REVIEW-PACK`) was found, during this archival assembly, to contain **three of the twelve "frozen confirmatory instrument" files in the wrong provenance state**: the *original pre-Amendment-2* content, despite that pack's own `README.md` explicitly describing its instrument folder as "final v8.3 source archive … final development hash manifest."

This mismatch was caught by cross-verifying every file in this repository's `01_frozen_confirmatory_instrument/` directly against the registered execution server, per the mandatory rule: *"if any divergence exists: STOP, do not fix the instrument, do not substitute the manifest, do not choose an approximately-similar version, report the divergence."* It was reported, investigated, and resolved with the repository owner before any file was placed in `01_frozen_confirmatory_instrument/`.

## What was found

| File | Old local pack (actual bytes) | Server `causal-A/prereg-A/` (pre-Amendment-2) | Server `causal-A-amd2-official/prereg-A/` (post-Amendment-2, `chattr +i`) |
|---|---|---|---|
| `benchmark.py` | `19d0baf0e3a8…` | `19d0baf0e3a8…` (same) | `19d0baf0e3a8…` (same) |
| `classificador.py` | `ecaa40c6fa2a…` | same | same |
| `dryrun.py` | `43473e07e65d…` | **same as pack** | `595c400bcdb2…` **← differs** |
| `equivalencias.py` | `c87cdb38da3b…` | **same as pack** | `f3b31124c961…` **← differs** |
| `escala.py` | `40ccd532e583…` | same | same |
| `gerador.py` | `6389c5615fd8…` | same | same |
| `pontuacao.py` | `028f5a0327c3…` | same | same |
| `test_classificador.py` | `fb42d9f14bd5…` | same | same |
| `test_equivalencias.py` | `461521efe3b3…` | **same as pack** | `4a41de63b913…` **← differs** |
| `test_escala.py` | `98a7543423757…` | same | same |
| `test_gerador.py` | `ebfda4d8967c…` | same | same |
| `test_pontuacao.py` | `905db9b5077a…` | same | same |

The old pack's own manifest file (`hashes-finais-dev.txt`) is *also* the pre-Amendment-2 manifest: sha256 of the manifest file itself is `8522625f4049d01b01bc52609eaaf3211e18769426dbfb561d3c37f828b50785`, identical to `causal-A/hashes-finais-dev.txt` on the server, and **different** from `causal-A-amd2-official/hashes-finais-dev.txt` (`995d42dde0070310b6f214ce0398cf1cd89644bf8d79af56823c41bf31ed83d7`). The old pack is therefore **internally self-consistent** — its manifest text correctly describes its own actual file bytes — but it is a consistent snapshot of the **wrong provenance stage**: the original, pre-engineering-amendment instrument, not the instrument that actually ran the confirmatory execution.

## Investigation performed

1. **Content comparison.** All 12 files, three independent sources, full SHA-256 (table above; complete hashes recomputed independently, not read from any single manifest).
2. **Self-consistency check.** The old pack's manifest hash was recomputed from the manifest *file itself* (not trusted from its own text) and compared against both server manifests.
3. **Stated intent check.** The old pack's own `README.md` (line 11) reads: *"`06_FROZEN_INSTRUMENT/` — final v8.3 source archive, extracted 12 Python files, and final development hash manifest."* The word "final" is unambiguous evidence that the pack's assembler *intended* to capture the post-Amendment-2 instrument — ruling out the alternative explanation that the pack was deliberately built to represent the original v8.3 state.
4. **Timestamp analysis.** All 12 `.py` files in the old pack share an identical local modification timestamp to the second (`2026-08-14 09:59:48`), and the manifest file's timestamp (`09:57:32`) is about two minutes earlier — consistent with a single batch-copy event, clustered very early in the project's timeline, before Pre-data Amendment No. 2 existed (Amendment 2 was only proposed after the *first* official 72-hour gate failed at ≈102.14h; see `00_preregistration/development_records/`).
5. **Session-log search.** No command history, session transcript, or log was found (`~/.devin`, `~/.cache/devin`, `~/.config/devin`) that records which server path was used to assemble the old pack. This line of investigation reached a dead end; the conclusion below rests on (1)–(4), not on a recovered command log.
6. **Independent cross-check against a third source.** `frozen-copy/`, the reference copy that all five post-confirmatory workstreams (WS1–WS5) independently verified against before their own analyses, matches `causal-A-amd2-official/prereg-A/` 12/12 (freshly re-verified, not reused from earlier reconnaissance — see `verification/frozen-instrument-crosscheck.md` for the full 35-file cross-check, which additionally confirms the confirmatory keys, scoring outputs, autopsy, and prevalence materials archived in this repository against the same authoritative manifest). The post-confirmatory scientific record was therefore built on the correct tree throughout, regardless of the old pack's error.

## Conclusion

The old pack is a **packaging/archival error** in a since-superseded local working copy — never the confirmatory instrument itself, never used on the execution server, and never referenced by the post-confirmatory scientific record. The confirmatory execution and all post-confirmatory analyses in this repository ran against `causal-A-amd2-official/prereg-A/` on the registered server, which is:

- protected by the filesystem immutable attribute (`chattr +i`) since the confirmatory execution;
- internally self-consistent, 12/12, against its own manifest;
- identical, 12/12, to `frozen-copy/`, cross-verified independently by all five post-confirmatory workstreams.

**`01_frozen_confirmatory_instrument/` in this repository is built exclusively from the server-resident, immutable tree — never from the old local pack.**

## Disposition of the old pack

Per the repository owner's explicit instruction, the erroneous pack is:

- **not** deleted or silently corrected at its original location (outside this repository, on this author's local machine);
- **not** imported into this repository, to avoid placing admittedly-wrong file content alongside the canonical instrument;
- fully documented here instead, so the discrepancy is auditable rather than hidden.

The scientific conclusions of the earlier Methods-review task that used the old pack are not believed to be affected: that task's mathematical verification (rank/determinant reconstruction, equation re-derivation) concerned `classificador.py` and `gerador.py`, which were not among the three mismatched files, and none of the task's findings depended on the specific bytes of `dryrun.py`, `equivalencias.py`, or `test_equivalencias.py`. This is a scoped observation about that specific prior task, not a re-audit of it; a full re-audit is not part of this archival-assembly task.

## Verification commands

```bash
# 1. This repository's frozen instrument matches its own manifest:
cd 01_frozen_confirmatory_instrument && shasum -a 256 -c hashes-finais-dev.txt
# Expected: 12/12 OK

# 2. This repository's frozen instrument matches the original preregistration instrument
#    only on the 9 files unaffected by Amendment 2 (see 00_preregistration/protocol/README.md
#    for the itemized list of the 3 files that legitimately differ).
```
