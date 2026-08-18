# Environment

*Archival packaging documentation. This directory holds no data files of its own — see below.*

`hardware.txt` (identical across both official gates) and `hashes-codigo.txt` (gate-specific — differs between the two gates, since it records the code hashes that Amendment 2 changed) are consolidated inside `../dry_run/`, alongside the rest of the two-gate comparison:

```
../dry_run/shared_payload/hardware.txt              (identical both gates)
../dry_run/gate1_NAO_PASSA/hashes-codigo.txt         (pre-Amendment-2)
../dry_run/gate2_PASSA/hashes-codigo.txt             (post-Amendment-2; = 01_frozen_confirmatory_instrument/hashes-finais-dev.txt content)
```

See `../dry_run/README.md`.
