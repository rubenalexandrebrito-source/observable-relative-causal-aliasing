# Gate E — Duplicate-content audit

**Rule:** zero-tolerance is on *unexplained* duplication, not on identical-content groups per se — identical bytes can legitimately occur across two distinct archival roles (a pre/post-amendment snapshot pair) or represent an intentional independent corroboration (multiple relay queries of the same public randomness round). The correct test is: every duplicate-content group must be individually classified; the count of **unclassified** duplicate groups must be zero.

## Result

```
Detected identical-content groups: 11

Classified intentional:
  1  independent drand relay corroboration group (3 files)
  9  unchanged-by-Amendment-2 files, preregistration snapshot <-> final frozen instrument
  1  fases_0_3.py, preregistration snapshot <-> execution-context orchestrator copy

Unexplained duplicate groups: 0

Gate E: PASS
```

Separately, `02_confirmatory_execution/dry_run/shared_payload/` physically deduplicates 206 files that are genuinely repeated data (both official gates' dry-run artifacts) — that transformation is documented in full in `../PROVENANCE.md` and `../../02_confirmatory_execution/dry_run/gate1_NAO_PASSA/PROVENANCE.md` / `gate2_PASSA/PROVENANCE.md`.

## Classification rationale

| Class | Why not deduplicated |
|---|---|
| `INTENTIONAL-INDEPENDENT-CORROBORATION` | The duplication *is* the evidence — three independent relay queries agreeing on the same drand round is the verification the frozen protocol required. |
| `EXPECTED-CROSS-SNAPSHOT-IDENTITY` | The same bytes occupy two epistemically distinct roles: "part of the preregistered state" vs. "part of the instrument that actually produced the confirmatory result." Each of `00_preregistration/protocol/` and `01_frozen_confirmatory_instrument/` must remain self-contained and independently verifiable without depending on a shared external location — especially `01_frozen_confirmatory_instrument/`, the repository's primary integrity-verification target. |
| `EXPECTED-CROSS-CATEGORY-IDENTITY` | Same reasoning, applied to `fases_0_3.py` across the preregistration-provenance and execution-context roles. |
| `DEDUPLICATED-SHARED-PAYLOAD` | Genuinely redundant data (the same dry-run generation event, recorded twice because two gate executions happened to reuse it) — physically stored once, per `../../02_confirmatory_execution/dry_run/README.md`. |

Every file's classification is machine-readable in `../FILE-INVENTORY.csv`, column `duplicate_class`.
