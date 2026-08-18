# Frozen-instrument cross-check against the post-confirmatory workstream reference manifest

**Date of this verification:** during final archival assembly, 18 August 2026.

## What was checked

Every entry of `03_post_confirmatory/MANIFEST.txt` — the shared, read-only manifest that all five post-confirmatory workstreams (WS1–WS5) independently verified their `frozen-copy/` against before running any analysis — was cross-checked against the corresponding file as actually archived in this repository.

This manifest covers more than the 12 frozen instrument files: it also covers the confirmatory unblinded keys, classification/scale/equivalence scoring outputs, the blinded-generation manifests, the autopsy report, and the full prevalence-study code and data.

## Method

1. `sha256sum` of `causal-A-postconfirmatory-analysis/frozen-copy/*.py` freshly re-pulled from the registered execution server (not reused from earlier reconnaissance).
2. Every one of the 35 non-header entries in `03_post_confirmatory/MANIFEST.txt` mapped to its archived repository path.
3. Each archived file's SHA-256 recomputed directly from disk and compared against the manifest's recorded value.

## Result

```
35 / 35 MATCH
0 mismatches
0 missing
```

This independently confirms, from a source distinct from `01_frozen_confirmatory_instrument/hashes-finais-dev.txt` itself:

- the 12-file frozen instrument (`01_frozen_confirmatory_instrument/`) is identical to the exact copy that all five post-confirmatory workstreams verified and ran their analyses against;
- the confirmatory unblinded keys, scoring outputs, and blinded-generation manifests archived in `02_confirmatory_execution/` are unaltered since Phase 6;
- the autopsy report and prevalence-study materials archived in `03_post_confirmatory/00_autopsy/` and `03_post_confirmatory/01_prevalence/` are unaltered since Phase 6.

## Relationship to the packaging-provenance incident

This verification is independent of, and consistent with, the resolution documented in `../PACKAGING-PROVENANCE-INCIDENT.md`: the frozen instrument archived in this repository was sourced exclusively from the registered execution server's immutable `causal-A-amd2-official/prereg-A/` tree, never from the since-superseded local pack. This cross-check against `frozen-copy/` — the artifact the post-confirmatory scientific record was actually built on — closes the loop.
