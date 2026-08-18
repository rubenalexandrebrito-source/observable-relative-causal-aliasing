# Archival Checks — Missing / Ambiguous Artifact Register

*Archival packaging documentation. No entry in this file was resolved by inventing, reconstructing, or guessing content.*

States used: `FOUND` · `NOT FOUND` · `NOT APPLICABLE` · `DUPLICATE` · `ZENODO-ONLY`.

## Critical elements (per archival specification)

| Expected artifact | Status | Search performed | Consequence |
|---|---|---|---|
| Original preregistration protocol (prose document) | **NOT FOUND** | Searched the registered execution server (`/root/causal-A*`) and this author's local machine (filename patterns `*preregist*`, `*protocolo*`, `*guiao*`, `*v8.3*`) | The technical protocol exists only in executable form: the 12 frozen Python files + `fases_0_3.py` + scattered procedural records. `00_preregistration/protocol/README.md` states this explicitly. |
| Pre-data Amendment No. 1 | **NOT FOUND** | Same search as above; no standalone document, no indirect evidence located | Not reconstructed. No content from it is asserted anywhere in this repository. |
| Pre-data Amendment No. 2 (engineering: parallelization) | **NOT FOUND** as prose | Same search | Content is recoverable *indirectly* only, from the code diff between `00_preregistration/protocol/` and `01_frozen_confirmatory_instrument/` (3 files) and the gate-registry transition (NAO_PASSA → PASSA). Not reconstructed as prose. |
| Pre-data Amendment No. 3 (drand seeds) | **FOUND** | — | `00_preregistration/amendments/PRE-DATA-AMENDMENT-3.txt` |
| `hashes-finais-dev.txt` (both original and post-Amendment-2) | **FOUND**, both versions | Cross-verified against the server; see `PACKAGING-PROVENANCE-INCIDENT.md` | `00_preregistration/protocol/` (original) and `01_frozen_confirmatory_instrument/` (post-amendment) |
| 12 frozen Python files | **FOUND**, 12/12 hash-verified | Pulled directly from the immutable server directory | `01_frozen_confirmatory_instrument/` |
| Original confirmatory scoring | **FOUND** | — | `02_confirmatory_execution/scoring/resultado-pontuacao-A.txt` and supporting JSON |
| Original execution environment / timing record | **FOUND**, both official gates | — | `02_confirmatory_execution/dry_run/gate1_NAO_PASSA/` + `shared_payload/` (first, NAO_PASSA) and `02_confirmatory_execution/dry_run/gate2_PASSA/` + `shared_payload/` (second, PASSA) |
| Phase-6 final synthesis | **FOUND** | — | `04_phase6_closure/FASE6-MULTIAGENT-SYNTHESIS.md` |
| Phase-6 formal closure | **FOUND** | — | `04_phase6_closure/FASE6-FORMAL-CLOSURE.md` |
| Submission content freeze v1.0 (PDF) | **FOUND** | Local machine, `~/Downloads/` | `05_manuscript/ARTICLE1-SUBMISSION-CONTENT-FREEZE-v1.0.pdf` |
| Submission content freeze v1.0 (`.tex`) | **NOT FOUND** | Same search as PDF, plus recursive `*.tex` search of local machine | Not reconstructed from the PDF. |
| Submission content freeze v1.0 (`-FREEZE-NOTE.md`) | **NOT FOUND** | Same | Not invented. |
| Submission content freeze v1.0 (`-SHA256.txt`, originally issued) | **NOT FOUND** | Same | This repository's own `SHA256SUMS.txt` records a hash computed *during archival assembly*; it is not presented as an originally-issued freeze artifact. |
| Submission content freeze v1.0 (`-PACKAGE.zip`) | **NOT FOUND** | Same | Not invented. |
| `ARTICLE1-rev7.3-to-SUBMISSION-CONTENT-FREEZE-v1.0.diff` | **NOT FOUND** | Local recursive `*.diff`, `*rev7*` search | `05_manuscript/freeze_support/` left empty. |

## Non-critical gaps found during assembly

| Item | Status | Note |
|---|---|---|
| `ARTICLE1-RESULTS-v0.1-REDTEAM.md`, `ARTICLE1-RESULTS-v0.1-to-v0.2.diff` | **NOT FOUND** | Referenced by SHA-256 inside `ARTICLE1-RESULTS-v0.2-FREEZE-SHA256.txt` (a genuine, present file) but absent from every location searched. Not reconstructed. |
| `prereg-A-final.zip` | **DUPLICATE** (found, not separately archived) | Exists on the server (`causal-A/prereg-A-final.zip`, `causal-A-amd2-dev/prereg-A-final.zip`) as a zipped bundle of the same 12 files + manifest already archived individually in `00_preregistration/protocol/`. Not separately archived, to avoid duplicating already-archived content byte-for-byte in a different container format. |
| Theoretical consciousness-paper ("A consciência como interferência sedimentada") | **NOT APPLICABLE** (found, deliberately not archived) | Located locally (two sequential versions). By explicit decision of the repository owner, this is cited by title/author/date only in the root `README.md`, "Programme context and scope"; the file itself is not imported. Not a missing-artifact gap — a deliberate scope boundary. |
| Historical "50 tests across 5 suites" figure | **NOT RECONCILED** | Verified by direct execution + static inspection: pre-Amendment-2 snapshot (`00_preregistration/protocol/`) = 58 tests; final frozen instrument (`01_frozen_confirmatory_instrument/`) = 70 tests; neither equals 50. The 58→70 increase is fully accounted for (12 new tests in `test_equivalencias.py`, Amendment 2). The value 50 is not used as an identifier of either archived state. Full audit: `REPRODUCE.md`, "Historical test-count discrepancy". |

## Frozen instrument provenance

See `PACKAGING-PROVENANCE-INCIDENT.md` for the full investigation of a since-superseded local packaging error that briefly put three pre-Amendment-2 files under an incorrect "final" label in an unrelated working copy. Resolved before any file entered this repository.

## Privacy / hardware-identifier note

`fases_0_3.py` records one machine identifier field, `"node"`, computed via Python's `uuid.getnode()` (typically MAC-address-derived), appearing in `hardware.txt` and `registo-fases-0-3.json` in both `00_preregistration/development_records/` and `02_confirmatory_execution/`. Value: `0x920009ab165e`. This is a virtual-machine network-interface identifier on a rented cloud server, not a physically traceable personal device — but per the archival specification's explicit instruction, it is flagged here for the repository owner's decision before any public release, rather than silently kept or silently removed.

No API keys, passwords, private keys, credentials, cookies, authentication headers, or personal email addresses were found anywhere in the archived material (full scan log available on request; patterns checked: API/secret/private keys, bearer tokens, `ghp_`/`github_pat_`/`sk-` token prefixes, email addresses, IP addresses, and the specific known real server hostname/IP/root-password string).
