# Provenance Chain

*Archival packaging documentation.*

## Programme lineage

```
broader theoretical research programme (consciousness / causal individuation)
        ↓  [not archived in this repository — cited only, see root README.md]
BOUNDARY I designated as its first formal test
        ↓
preregistration frozen  (00_preregistration/protocol/)
        ↓
pre-data engineering Amendment No. 2 (parallelization fix, motivated by the
first gate's NAO_PASSA at ~102.14h — 00_preregistration/development_records/)
        ↓
final frozen confirmatory instrument  (01_frozen_confirmatory_instrument/)
        ↓
second official 72h gate: PASSA (~45.96h)  (02_confirmatory_execution/dry_run/)
        ↓
pre-data Amendment No. 3 (drand-based verifiable confirmatory seeds)
        ↓
Phase 4 freeze  (02_confirmatory_execution/seeds/congelamento.txt)
        ↓
confirmatory execution: blinded generation → scoring  (02_confirmatory_execution/)
        ↓
CONFIRMATORY RESULT: NEGATIVE  (resultado_confirmatorio_A = "negativo")
        ↓
post-confirmatory autopsy of the single C1′ error  (03_post_confirmatory/00_autopsy/)
        ↓
post-confirmatory mechanism characterization: algebra, information loss,
strict realization, System-III specificity, failure-class structure,
prevalence  (03_post_confirmatory/01_prevalence/ … 09_coordinator/)
        ↓
Phase 6 synthesis and formal closure  (04_phase6_closure/)
        ↓
interpretive-epistemology fixing (BOUNDARY I — PASSO 2)
        ↓
prior-art audit (BOUNDARY I — PASSO 3)  (03_post_confirmatory/08_prior_art/)
        ↓
article architecture + claim–evidence ledger + Methods/Results freeze
(BOUNDARY I — PASSO 4 / 4A)  (04_phase6_closure/supporting_records/)
        ↓
manuscript scientific-content freeze v1.0  (05_manuscript/)
        ↓
this repository — archival packaging
```

**Post-confirmatory analysis never alters the confirmatory decision.** No step below the "CONFIRMATORY RESULT: NEGATIVE" line changes any value above it. No replacement criterion ("C1″") exists anywhere in this chain.

## Independence taxonomy used throughout this repository

- **Data independence** — a new, pre-committed random seed disjoint from all previously used/burned seeds.
- **Implementation independence** — a distinct code path/formula/route to the same quantity.
- **Internal-analytic independence** — a derivation produced under an internal firewall (no access to the prior derivation), attested at the workflow level (WS1 is the only instance of this in the archive).
- **Internal reproduction** — an agent with access to the shared repository reproducing or auditing another agent's result (the default mode for WS2–WS5, the coordinator, and run1→run2 comparisons).
- **External scientific replication** — an independent group, independent infrastructure, outside this research workflow. **This has not occurred for any result in this repository.** No document in this repository describes internal agreement as external replication.

## Dry-run gate deduplication (`02_confirmatory_execution/dry_run/`)

Both official 72-hour gates (first, pre-Amendment-2, `NAO_PASSA_GATE_72H` at ≈102.14h; second, post-Amendment-2, `PASSA_GATE_72H` at ≈45.96h) produced overlapping records: some artifacts are genuinely gate-specific, others are byte-identical between the two gates because Amendment 2 did not touch `gerador.py` or the fixed dry-run selector seed (`777000300`).

**Method:** every file was compared pairwise by SHA-256 before any restructuring — nothing was deduplicated on the basis of expected/assumed scientific equivalence alone.

**Result, physical-file-count and content-hash-set accounting (identical directory scope measured before and after):**

| | physical files | unique content hashes |
|---|---|---|
| Before | 422 | 216 |
| After | 216 | 216 |

Content hashes missing after the transformation: **0**. Unexplained new content hashes after the transformation: **0**. The 206-file reduction is fully accounted for: it equals the count of pre-existing exact duplicates (150 `dry-e1` instances + 1 `dry-e1/manifesto.json` + 50 `dry-e2` instances + 1 `dry-e2/manifesto.json` + 2 hidden-key files + `hardware.txt` + `dryrun-seleccao.json` = 206), each of which is now stored physically once, in `dry_run/shared_payload/`.

**Gate-specific artifacts** (10 total = 5 per gate, physically distinct, never deduplicated): for each gate, `hashes-codigo.txt`, `benchmark-oficial.json`, `dryrun-tempos.json`, `registo-fases-0-3.json`, and — the fifth, previously undernamed in summary form — the gate's **full stdout/stderr transcript log** (`fases-0-3-oficial.log` for Gate 1, `fases-0-3-amd2-oficial.log` for Gate 2). All five differ genuinely between the two gates; `hashes-codigo.txt` differing is the expected, confirmed fingerprint of Amendment 2's three changed files.

Full file-by-file historical-path ↔ repository-path ↔ SHA-256 mapping: `../02_confirmatory_execution/dry_run/gate1_NAO_PASSA/PROVENANCE.md` and `.../gate2_PASSA/PROVENANCE.md`.

**Status: approved and frozen for packaging purposes.** This structure is not to be modified further during archival assembly, only in response to an objective audit discrepancy.

## Frozen-instrument provenance

See `PACKAGING-PROVENANCE-INCIDENT.md` for the full investigation establishing that `01_frozen_confirmatory_instrument/` is sourced exclusively from the registered execution server's immutable `causal-A-amd2-official/prereg-A/` tree, and that a separate, since-superseded local working copy (used for an unrelated earlier task) played no role in the confirmatory execution or in any post-confirmatory analysis archived here.
