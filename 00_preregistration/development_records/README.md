# Development records — first official Fases 0–3 execution (NAO_PASSA)

*Archival packaging documentation. This directory holds no data files of its own — see below.*

The **first** official execution of Fases 0–3, under the original pre-Amendment-2 sequential instrument (`../protocol/`), resulted in:

```
estado: NAO_PASSA_GATE_72H
T_total_horas: 102.14…
```

This result is what motivated Pre-data Amendment No. 2 (see `../amendments/README.md` and `../README.md`).

## Where this gate's records actually live

To keep this first gate directly comparable, file-by-file, with the second (successful) gate — and because several of its artifacts are byte-identical to the second gate's — all of its records have been consolidated at:

```
../../02_confirmatory_execution/dry_run/gate1_NAO_PASSA/    (gate-specific: hashes-codigo.txt, benchmark-oficial.json,
                                                               dryrun-tempos.json, registo-fases-0-3.json, full log,
                                                               and PROVENANCE.md)
../../02_confirmatory_execution/dry_run/shared_payload/     (byte-identical to gate 2: hardware.txt, dryrun-seleccao.json,
                                                               dry-e1/, dry-e2/, hidden keys)
```

See `../../02_confirmatory_execution/dry_run/README.md` for the full rationale, and `../../06_reproducibility/PACKAGING-PROVENANCE-INCIDENT.md` for the file-by-file SHA-256 verification that established which artifacts are genuinely shared and which are gate-specific.

## Epistemic status

`ARCHIVAL-METADATA` / development record. This is not the confirmatory execution. The confirmatory execution (post-Amendment-2, seeds `3786434918`/`3786434919`) is archived under `../../02_confirmatory_execution/`.
