# BOUNDARY I — PASSO 4A: CLAIM–EVIDENCE LEDGER — v1.1

**Data:** 17-08-2026  
**Base canónica:** `ARTICLE1-SCIENTIFIC-ARCHITECTURE-v2.1.md` (FROZEN)  
**Alteração face à v1:** resolução de `OPEN-01 — C4 STATUS`; nenhuma claim científica anterior foi ampliada.  
**Função:** atomizar as afirmações admissíveis antes da redação do Artigo 1.  
**Estado:** `CANDIDATE FOR FREEZE`

> Este ledger não altera o protocolo, o scoring confirmatório, a Fase 6, a arquitetura v2.1 ou a auditoria de prior art.

## Taxonomia de evidência

- **A** — proven analytically.
- **B** — exhaustively verified in a finite domain.
- **C** — empirically validated OOS / precommitted sample within the workflow.
- **D** — internally reproduced by a distinct implementation/workstream in the same research workflow.
- **E** — supported/conjectured.
- **CONF** — immutable confirmatory fact from the preregistered run.
- **FROZEN-CODE + HASH-AUDIT** — fact about the pre-data executable instrument established directly from the frozen source archive and its recorded hashes.

**Important:** `C` and `D` are not external scientific replication.

## Regra de uso

A coluna **Exact wording / maximum claim** é o teto autorizado pelo estado atual da evidência.  
A coluna **Forbidden stronger wording** é vinculativa para o primeiro manuscrito.  
Uma claim só pode ser ampliada após nova evidência ou reabertura formal do ledger.


## A. Confirmatory outcome, provenance, construct validity and candidate status

| ID | Exact wording / maximum claim | Domain | Epistemic status | Evidence | Phase | Canonical source | Prior-art status | Allowed wording | Forbidden stronger wording | Placement | Independent-validation gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CE-001 | The preregistered confirmatory outcome is negative (`resultado_confirmatorio_A = "negativo"`; `passa=false`). | Pré-registo A v8.3, confirmatory Battery A | Immutable confirmatory fact | CONF | CONFIRMATORY | FASE6-FORMAL-CLOSURE §1; FASE6-MULTIAGENT-SYNTHESIS §1 | N/A | Use `confirmatory outcome was negative` without qualification. | `almost positive`; `essentially passed`; reinterpretation by post-confirmatory work. | Results 2.1; Abstract; Fig. 1 | No. |
| CE-002 | For C1′, E1 was 150/150 and E2 was 49/50, for 199/200 total; the conjunctive preregistered target therefore failed. | Confirmatory C1′ scoring | Immutable confirmatory fact | CONF | CONFIRMATORY | FASE6-FORMAL-CLOSURE §1; SYNTHESIS §1 | N/A | Report counts and the conjunctive decision together. | Use 99.5% as evidence that C1′ was validated. | Results 2.1; Fig. 1 | No. |
| CE-003 | The single C1′ confirmatory error was instance `7bb0baab3a8ed7aa`, family 20, System II, E2/Stratum 2. | Confirmatory instance identity | Immutable confirmatory fact | CONF | CONFIRMATORY | FASE6-FORMAL-CLOSURE §1; AUTOPSY §1; SYNTHESIS §1 | N/A | Call it `the single C1′ confirmatory counterexample`. | Call it noise, a bug, or a non-error. | Results 2.1–2.2 | No. |
| CE-004 | C2 made 74 confirmatory errors and C3 made 75; both also fail on family 20, and neither was mechanistically autopsied in Phase 6. | Confirmatory scoring + scope of autopsy | Confirmatory facts + post-confirmatory scope statement | CONF + provenance | MIXED | SYNTHESIS §§1,12; Architecture v2.1 §0.6 | N/A | Report them for completeness and state that the paper mechanistically analyzes C1′. | Invent a mechanism for C2/C3 or omit their confirmatory failures. | Results 2.1; Methods 4.3; Limitations | No. |
| CE-005 | All mechanistic analyses after scoring are post-confirmatory; they did not alter the official scoring, criteria, targets, thresholds, or confirmatory artifacts, and no C1″ was formulated. | Epistemic provenance / workflow | Closed provenance fact | D / audit trail | POST-CONFIRMATORY | FASE6-FORMAL-CLOSURE §§2–3; SYNTHESIS §§1,8 | N/A | Use an explicit epistemic-provenance timeline. | Present later analyses as preregistered predictions. | Main/Extended provenance box; Methods | No. |
| CE-006 | System-II/System-III and STATE/SIGNAL are pre-specified operational targets of a controlled synthetic generative design, not a universal ontology of physical or biological interaction. | Construct validity | Methodological scope statement | N/A | DESIGN/INTERPRETATION | Architecture v2.1 §§0.5,12 | N/A | `target by construction`; `operational class`. | `ground-truth causal individuation`; `genuinely STATE/SIGNAL` in an ontological sense. | Introduction; Methods 4.1; Limitations | No. |
| CE-007 | The project has internal reproduction and OOS validation, but no external scientific replication has occurred. | Evidence provenance | Closed limitation | D + C present; external replication absent | POST-CONFIRMATORY | SYNTHESIS §§12,21,23; Architecture freeze | N/A | `internally reproduced`; `validated OOS within the workflow`. | `independently replicated` or `external replication`. | Methods 4.15; Limitations | No; must disclose absence. |
| CE-051 | The frozen v8.3 confirmatory implementation contains no C4 execution or scoring path. It executes C1′, C2 and C3; the confirmatory result can be positive through C1′ or C2, while C3 is an implementation canary and does not enter H_A. Accordingly, C4 was not a scored confirmatory candidate in the final executable instrument. | Frozen preregistered v8.3 confirmatory implementation / Battery A | Pre-data frozen implementation/protocol-status fact | FROZEN-CODE + HASH-AUDIT | PREREGISTERED IMPLEMENTATION | prereg-A-final.zip::classificador.py, dryrun.py, escala.py, equivalencias.py, pontuacao.py; hashes-finais-dev.txt | N/A | `C4 was not executed or scored by the final frozen v8.3 confirmatory instrument`; `C1′ and C2 were the H_A decision candidates; C3 was the canary`. | Do not reconstruct the wording or role of an earlier historical C4 from memory; do not claim that the final confirmatory run omitted a required C4; do not describe C3 as a positive H_A candidate. | Results 2.1; Methods 4.2–4.3; epistemic-provenance note | No blocker for ledger freeze. Archival protocol-text cross-check is recommended before submission, but it cannot override the frozen executable record without documenting a protocol/implementation discrepancy. |

## B. Formal mechanism and metric blind route

| ID | Exact wording / maximum claim | Domain | Epistemic status | Evidence | Phase | Canonical source | Prior-art status | Allowed wording | Forbidden stronger wording | Placement | Independent-validation gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CE-008 | For the relevant System-II channel→processor contrast, the receiver response has the form `R[r][π_m(c)] ⊕ σ[m]`, with receiver-memory update independent of the channel at the current step. | Frozen System II, one-step channel→processor edges | Post-confirmatory analytic lemma | A+B+D | POST-ANALYTIC | SYNTHESIS §§9,13,17; WS5 §3.1 | P3 ingredient; not independently novel | Use as Lemma 1 / realization of the abstract pull-back hypotheses. | Generalize to arbitrary dynamics or memory updates. | Results 2.3; Methods 4.6 | No for this bounded domain; yes if generalized outside assumptions. |
| CE-009 | Under the frozen XOR contrast, `σ[m]` and the current-step memory-update term cancel; receiver memory enters the contrast through `π_m`. | Frozen System II, h=1 XOR-interventional field | Post-confirmatory analytic fact | A+B+D | POST-ANALYTIC | SYNTHESIS §§9,13; WS5 §3.1 | Generic cancellation is known/T2 | State exactly which terms cancel and why. | `memory has no causal effect` or cancellation for arbitrary observables/horizons. | Results 2.3; Methods 4.6 | No. |
| CE-010 | The relative contextual relabeling is `τ = π₁ ∘ π₀⁻¹`. | Finite interface relabelings | Definition | N/A | POST-FORMALIZATION | SYNTHESIS §§9,17; Architecture v2.1 | N/A | Use consistently; distinguish from abstraction maps in prior work. | Conflate this τ with Xia & Bareinboim's low→high abstraction map. | Results/Methods notation | No. |
| CE-011 | The receiver mechanism induces the pairwise response geometry `W_M(p,q)=Σ_r pc2(M[r][p]⊕M[r][q])` for the frozen Hamming kernel. | Frozen receiver-response geometry | Post-confirmatory definition/analytic construction | A+B+D | POST-ANALYTIC | SYNTHESIS §§9,13,17; WS5 §3.1 | Pairwise geometry/isometry mathematics T2 | `mechanism-dependent response geometry`. | Imply W is a universal causal metric. | Results 2.4; Methods 4.7 | No. |
| CE-012 | For the frozen System-II statistic, `d_m(a)=2^(n-5)·Σ_c W̃_m(c,sub_a(c))`, equivalently `d=2^(n-5)·(0,A,A,B,B,V)`. | Frozen one-step statistic / 9 interventions | Post-confirmatory analytic result | A+B+D | POST-ANALYTIC | SYNTHESIS §§3–4,9,13; WS5 §3.1 | Specific application; no broad novelty | Call it the exact closed form for the frozen statistic. | Generalize the numerical form to other lattices/alphabets without derivation. | Results 2.5; Methods 4.9 | No. |
| CE-013 | Within the frozen lattice, `d` is a linear bijection of `W̃`; therefore L1 introduces no additional information loss after `W̃`. | Frozen 9-intervention lattice | Post-confirmatory analytic result | A+B+D | POST-ANALYTIC | SYNTHESIS §4 and §13 | T2-style determining-set ancestry | `d↔W̃ is bijective for the frozen lattice`. | `d preserves all causal information` or any claim about finer fields. | Results 2.5/2.7; Methods 4.9 | No. |
| CE-014 | For any observable in the stated cell-factorizing class, `τ∈Iso(W)` implies equality across contexts at that observable. | Abstract finite contextual-pullback class | Post-confirmatory analytic proposition | A | POST-ANALYTIC | SYNTHESIS §17.1–17.3; Architecture v2.1 Proposition 1 | T2 / known group-invariance mathematics | Present as a class-level blindness proposition with explicit assumptions. | Claim new mathematics of invariance/isometries or extend to arbitrary finer observables. | Results 2.4; Methods 4.8 | No for theorem; external validation relevant only to empirical applicability. |
| CE-015 | Observable equality is `blindness`; it constitutes causal aliasing/false invariance only when an underlying causal difference `X₀≠X₁` is independently established. | Logical interpretation of observable equality | Epistemic/definitional guardrail | N/A | INTERPRETATION | Architecture v2.1 §§0.3,5 | N/A | Keep blindness and aliasing separate. | `τ∈Iso(W)` proves false invariance by itself. | Introduction; Results 2.4; Discussion | No. |
| CE-016 | For channel→processor edges under the frozen determining intervention set, `d₀=d₁ ⇔ W̃₀=W̃₁ ⇔ τ∈Iso(W_M)`. | Frozen System II/III-compatible channel→processor statistic, h=1 | Exact post-confirmatory theorem | A+B+C+D | POST-ANALYTIC | SYNTHESIS §§3–4,13,17,19; WS1 Theorem 5 / WS5 §3.2 | P2 math ancestry T2; causal composition part of P3 candidate | `exact characterization of the metric blind route (L1)`. | `exact characterization of all C1′ blindness/STATE decisions`. | Headline Results 2.5; Methods 4.9 | No for bounded theorem; recommended independent derivation before very strong/general framing. |
| CE-017 | The converse in CE-016 is non-trivial for the instrument: the full six-degree system has rank 6 and determinant −8, whereas the two restricted sub-lattices have ranks 2 and 4 and do not support the converse. | Frozen 9-intervention lattice | Exact analytic instrument property | A+B+D | POST-ANALYTIC | SYNTHESIS §§3,8,17.4 | T2 / determining-set mathematics; no independent novelty claim | Call the full lattice `determining` for W̃. | Claim rank/determinacy as new general mathematics. | Results 2.5; Methods 4.9; Supplement proof | No. |
| CE-018 | C1′ marks a relevant edge STATE exactly when the canonical weak ranks of `d₀` and `d₁` coincide. | Frozen C1′ decision rule | Analytic/implementation equivalence | A+B | POST-ANALYTIC | SYNTHESIS §§3,13; WS1 Prop. 8; WS5 §3.3 | Instrument-specific | Use to define the complete C1′ edge event. | Reduce STATE to `d₀=d₁`. | Results 2.6; Methods 4.3/4.10 | No. |
| CE-019 | L1 means `d₀=d₁`; L2 means `d₀≠d₁` but equal weak rank; both are STATE under C1′. | Frozen C1′ taxonomy | Post-confirmatory analytic taxonomy | A+B+C+D | POST-CONFIRMATORY | Architecture v2.1 §§0.2,4.4; SYNTHESIS §§7,13 | P5 partly; weak-order math known | `metric aliasing` for L1 and `ordinal aliasing` for L2. | Treat L2 as a smaller exact isometry. | Results 2.6; Fig. 3 | No. |
| CE-020 | A total C1′ collapse of the System-II ring requires both decisive channel→processor edges to be classified STATE, via either L1 or L2. | Frozen System-II ring and SCC decision | Analytic/implementation fact | A+B | POST-CONFIRMATORY | SYNTHESIS §§7,13; WS5 | Instrument-specific | Describe the instance-level event separately from edge-level L1/L2. | Equate one L1 edge with total instance collapse. | Results 2.6/2.8; Methods | No. |

## C. Confirmatory counterexample and realized witness

| ID | Exact wording / maximum claim | Domain | Epistemic status | Evidence | Phase | Canonical source | Prior-art status | Allowed wording | Forbidden stronger wording | Placement | Independent-validation gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CE-021 | In family 20, the `C_BA→A` response geometry is equidistant off-diagonal and has `Iso(W)=S₄`. | Confirmatory family 20, one decisive edge | Post-confirmatory reconstruction | B+D | POST-DEMONSTRATED | SYNTHESIS §§9,18.3; WS5 F12 | Specific witness; no general prior-art claim | Use as exact witness geometry. | Call equidistance typical or universal. | Results 2.4; Fig. 3 | No. |
| CE-022 | In family 20, the `C_AB→B` response geometry has `Iso(W)={id,(23)}`, and the realized relative transport is exactly the non-trivial isometry `(23)`; the same transport is trivially in `S₄` on the opposite edge. | Confirmatory family 20 | Post-confirmatory reconstruction | B+D | POST-DEMONSTRATED | SYNTHESIS §§9,18.3; WS5 F12 | Specific P3 witness | Use as exact mechanism of the confirmatory counterexample. | Generalize the particular transposition to the whole failure class. | Results 2.4; Fig. 3 | No. |
| CE-023 | C1′ classifies the family-20 core `{A,B,C_AB,C_BA}` as one component, matching the System-III operational partition although the preregistered target is System II. | Confirmatory family 20 / C1′ SCC output | Confirmatory error + post-confirmatory description | CONF+B+D | MIXED | AUTOPSY §§1–2; SYNTHESIS §§1,8–9 | P4 specific consequence; general aggregation claim conceded | Use `target by construction` and `C1′-produced partition`. | `the true causal boundary is III` or ontological language. | Results 2.1–2.2; Fig. 1–3 | No. |
| CE-024 | Family 20 has point-to-point memory-dependent response differences at 4608 sites on each decisive edge. | Confirmatory family 20, n=12 | Post-confirmatory measured fact | B+D | POST-DEMONSTRATED | AUTOPSY §2; SYNTHESIS §§2,8–9 | P3/P4 witness | `4608 point-to-point dependent sites per edge`. | Use the count as a universal magnitude. | Results 2.2; Fig. 2 | No. |
| CE-025 | Both receiver-memory contexts are reached in the realized orbit of family 20. | Confirmatory family 20 orbit | Post-confirmatory measured fact | B+D | POST-DEMONSTRATED | AUTOPSY §2; SYNTHESIS §§2,5 | P3/P4 witness | Use to rule out inaccessible-memory explanations. | Claim all full configurations are shared across contexts. | Results 2.2 | No. |
| CE-026 | Conditional on receiver memory, the relevant interventional response is a function only of local `(r,c)`, making `(r,c)` a causally sufficient comparability granularity for this contrast. | Frozen one-step receiver contrast | Post-confirmatory analytic proposition | A+B+D | POST-ANALYTIC | SYNTHESIS §5; WS3 Prop. 1 | Specific analytic result | `causally sufficient local-state granularity (r,c)`. | `same complete state under both contexts` or arbitrary coarse-graining. | Results 2.2; Methods 4.5 | No. |
| CE-027 | At the `(r,c)` granularity, family 20 has 9 strictly realized differing sites on each decisive edge. | Confirmatory family 20 orbit/support | Post-confirmatory demonstrated fact | A+B+D | POST-DEMONSTRATED | SYNTHESIS §§5,8,19; WS3 | P3/P4 witness | `9 strict sites per edge at the causally sufficient local-state granularity`. | Use `strictly realized` without defining the granularity. | Results 2.2; Fig. 2 | No. |
| CE-028 | Family 20 admits observational witnesses of the context-dependent difference on both decisive edges; the collapse is therefore not explained by absence of realized separating information. | Confirmatory family 20 | Post-confirmatory demonstrated inference | B+D (+A for local sufficiency) | POST-DEMONSTRATED | SYNTHESIS §§5,8–9; WS3 | P4 specific consequence | Say `not explained by unrealized support` within the analyzed contrast. | Claim observational data alone universally identifies the boundary. | Results 2.2; Discussion | No. |

## D. Information loss, ordinal route and population structure

| ID | Exact wording / maximum claim | Domain | Epistemic status | Evidence | Phase | Canonical source | Prior-art status | Allowed wording | Forbidden stronger wording | Placement | Independent-validation gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CE-029 | For L1, `B4=0`: equality of the aggregate is cell/block-wise; compensation between blocks is not the mechanism. | Frozen L1 edges | Post-confirmatory theorem | A+B+D | POST-ANALYTIC | SYNTHESIS §§4,13 | Instrument-specific | `no between-block compensation in L1`. | Generalize B4=0 to L2 or arbitrary observables. | Results 2.7; Methods 4.12 | No. |
| CE-030 | Among the 698 L1 edges with pointwise dependence, 29 (4.2%) lose distinguishability at the pointwise-popcount level, 174 (24.9%) at the multiset/location stage, and 495 (70.9%) by within-cell arithmetic aggregation. | Studied II population, L1 edges with dep>0 | Post-confirmatory census | B+D | POST-EXPLORATORY/CENSUS | SYNTHESIS §4; WS2 | Generator-specific distribution | Use exact denominators and label as population-specific. | Call 70.9% a universal mechanism frequency. | Results 2.7; Supplement | No if bounded; yes before extrapolation. |
| CE-031 | For the studied 20,000 II edges, the nested blind sets satisfy `B_pattern ⊂ B_row ⊂ B_multiset ⊂ B_W` with cardinalities `7 ⊂ 36 ⊂ 210 ⊂ 705`. | Studied II population / observable refinement | Post-confirmatory structural nesting + empirical cardinalities | A partial+B+D | POST-CONFIRMATORY | SYNTHESIS §§4,17.3,19 | General refinement idea T2; exact hierarchy specific | Separate structural nesting from generator-specific counts. | Present 7/36/210/705 as universal constants. | Results 2.7; Fig. 4 | No if bounded. |
| CE-032 | Finer observables can strictly shrink the blind set; therefore the demonstrated non-identifiability is observable-relative rather than intrinsic to all available causal information. | Observable hierarchy within studied class | Post-confirmatory inference from analytic/census results | A partial+B+D | INTERPRETATION BOUNDED BY RESULTS | SYNTHESIS §§17.3,19; Architecture v2.1 | Generic ancestry T1/T2 | `blind set shrinks under refinement`. | `the system is fundamentally non-identifiable`. | Results 2.7; Discussion | No. |
| CE-033 | Family 20 belongs to the dominant within-cell arithmetic-cancellation mode of L1, not to the rare full-pattern-invariance extreme. | Family 20 within WS2 taxonomy | Post-confirmatory classification | B+D | POST-DEMONSTRATED | SYNTHESIS §4; WS2 | Specific witness | Use as mechanistic placement of family 20. | Call family 20 representative of all forms of blindness. | Results 2.7/Supplement | No. |
| CE-034 | In the primary 20,000-edge II population, 225 edges are L2 (`d₀≠d₁` with equal weak rank). | Studied II population | Post-confirmatory census | B+D | POST-EXPLORATORY/CENSUS | SYNTHESIS §§2,8; WS5 | Generator-specific | Use 225/20,000 with explicit population. | Generalize L2 frequency outside generator. | Results 2.6/2.8 | No if bounded. |
| CE-035 | Among the 24 L2 edges inside the 46 primary collapse instances, 17 have trivial `Iso(W)`; L2 is therefore not merely a weaker exact isometry. | Primary collapse cases | Post-confirmatory census + inference | B+D | POST-CONFIRMATORY | SYNTHESIS §7; WS5 F4 | P5-supporting | `17/24 had trivial exact isometry group`. | `L2 has no symmetry structure`—it has ordinal/profile symmetry. | Results 2.6 | No. |
| CE-036 | Alignment theorem: if the action `ψ(τ)` fixes the unprobed perfect matching `λ`, an ordinal L2 collapse is impossible; any collapse in that aligned cell is L1. | Frozen 2-bit intervention geometry / S4 action | Post-confirmatory analytic theorem | A+B+C+D | POST-ANALYTIC | SYNTHESIS §§7,13; WS5 §3.4 | P5 secondary novelty candidate; S4→S3/V4 math itself T2 | Use as the instrument-specific alignment theorem. | Claim new group theory or generalize beyond the defined instrument. | Results 2.6; Methods 4.10; Supplement proof | No for bounded theorem. |
| CE-037 | The observed L2 signatures match the predicted blind-zone mechanism in all 225 primary L2 edges: the probed pairing block changes as predicted while the D block remains unchanged. | Primary II population / L2 | Post-confirmatory analytic + census support | A+B+C+D | POST-CONFIRMATORY | SYNTHESIS §7; WS5 F4-bis | P5 supporting | State the exact 225/225 signature and its instrument dependence. | Claim this is the only possible ordinal-aliasing mechanism in arbitrary instruments. | Results 2.6; Supplement | No. |
| CE-038 | The primary generator-specific System-II collapse prevalence was 46/10,000 = 0.46% (95% CI approximately 0.345%–0.613%). | Frozen eligible System-II generator law | Post-confirmatory exploratory prevalence | C+D | POST-EXPLORATORY | SYNTHESIS §§2,19; AUTOPSY prevalence | N/A as novelty; empirical support only | Always qualify `under the frozen generator law`. | `the failure rate is 0.46%` universally. | Results 2.8; Fig. 4 | No if bounded; yes before external-frequency claims. |
| CE-039 | Across the reported internal/OOS samples, collapse estimates were of the same order, approximately 0.32%–0.50%; this range is not a universal rate. | Frozen-generator internal/OOS samples | Post-confirmatory empirical support | C+D | POST-EXPLORATORY | SYNTHESIS §§8.4,19 | N/A | Use only as robustness within the frozen generator. | Use as external replication or natural prevalence. | Results 2.8/Supplement | No if bounded. |
| CE-040 | Family 20 is not a separate mechanism; it is an L1/L1 member of the modal collapse subtype, with one equidistant edge and one τ-selected edge. | Primary collapse population / family 20 | Post-confirmatory classification | B+C+D | POST-CONFIRMATORY | SYNTHESIS §7; WS5 F12 | N/A | `family 20 is typical of the modal L1/L1 subtype` within this generator. | `typical of causal systems generally`. | Results 2.8/Supplement | No. |
| CE-041 | The excess correlation between the two decisive edges is quantitatively accounted for by the shared `(τ,λ)` structure and exact family geometry: parameter-free M3 gives residuals within about 0.6σ in the reported sets. | Frozen-generator correlation analysis | Post-confirmatory formula + empirical validation | A(formula)+C+D | POST-EXPLORATORY | SYNTHESIS §7/§19; WS5 §§3.6–3.7 | N/A | Use as supplementary explanation of within-generator dependence. | `proved independent conditional on all possible structure`; `no residual exists` literally. | Extended/Supplement | No if bounded. |

## E. Temporal boundary

| ID | Exact wording / maximum claim | Domain | Epistemic status | Evidence | Phase | Canonical source | Prior-art status | Allowed wording | Forbidden stronger wording | Placement | Independent-validation gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CE-042 | For eligible System III at horizon 1, the frozen full-fiber XOR-interventional field on channel→processor edges is exactly memory-independent; `dep≡0` and `d₀≡d₁` analytically. | Frozen System III, h=1 | Post-confirmatory analytic theorem III-1 | A+B+C+D | POST-ANALYTIC | SYNTHESIS §§6,13,19; WS4 D1 | P6 system-specific result; generic cancellation not novel | Use `exact at horizon 1 under the frozen semantics`. | Generalize to all XOR observables or all horizons. | Extended Results/Methods | No. |
| CE-043 | System-III receiver memory is nevertheless causally active outside that h=1 contrast, including the baseline; the h=1 null is a property of the observable, not memory inactivity. | Frozen System III | Post-confirmatory analytic/empirical contrast | A+C+D | POST-CONFIRMATORY | SYNTHESIS §6; WS4 D3/E6 | Supports bounded interpretation | Use to prevent interpreting III-1 as causal inactivity. | `memory is irrelevant in III`. | Extended/Discussion | No. |
| CE-044 | Under direct composition to `T²`, the first-order cancellation does not generally iterate: memory survives inside response-row indices and memory-update selectors in the exact h=2 expression. | Frozen System III, h=2 | Post-confirmatory analytic proposition III-2a | A | POST-ANALYTIC | WS4 D6; SYNTHESIS §§6,13 | P7 narrow technical novelty candidate; generic horizon effects T2 | Call it `the first-order identity is not algebraically stable under direct composition`. | `all multi-horizon extensions fail` or `dep2 is always nonzero`. | Extended/Supplement | No for bounded derivation. |
| CE-045 | In the studied h=2 sample, `dep2>0` in 3996/4000 System-III edges; 4/4000 were zero. | Frozen System III sample, h=2 | Post-confirmatory exploratory empirical result | C+D | POST-EXPLORATORY | WS4 F9–F10/E7; SYNTHESIS §6 | P7 supporting; rate not theorem | Always report both 3996/4000 and the four exceptions. | `III is always memory-dependent at h=2`; treat 99.9% as theorem. | Extended/Supplement | No if labeled exploratory; yes before universal promotion. |
| CE-046 | The generic proposition that distinguishability can depend on temporal horizon is prior art; the article may claim only the narrow system-specific h1→h2 mechanism established here. | Prior-art positioning for P7 | Closed prior-art restriction | N/A | PRIOR-ART | PRIOR-ART-AUDIT-CLOSURE §§10–12 | Generic horizon claim = T2; narrow P7 no T0 found | `our narrow composition mechanism was not matched by a T0 in the audit`. | `we discovered that horizon matters`. | Prior Work; Discussion; Extended | Recheck literature immediately before submission if P7 is highlighted. |

## F. Prior-art and interpretation guardrails

| ID | Exact wording / maximum claim | Domain | Epistemic status | Evidence | Phase | Canonical source | Prior-art status | Allowed wording | Forbidden stronger wording | Placement | Independent-validation gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CE-047 | The article must concede as known: group/isometry invariance, symmetry-induced unobservability, determining/quotient ideas, lossy causal abstraction, micro-realization dependence, endogenous context mechanisms, causal equivalence classes, and generic finite-horizon distinguishability. | Prior-art concessions | Closed prior-art mapping | N/A | PRIOR-ART | PRIOR-ART-AUDIT-CLOSURE §§4–13 | T1/T2 ancestry | Explicitly position the work against these ancestors. | Claim any generic ingredient as novel. | Prior Work; Discussion | Recheck fast-moving 2025–2026 literature before submission. |
| CE-048 | The prior-art audit found no T0 antecedent for the specific P3 composition; P3 remains a primary novelty candidate, not a proven historical priority claim. | Prior-art status of P3 | Closed audit conclusion | N/A | PRIOR-ART | PRIOR-ART-AUDIT-CLOSURE §§6,12,19–23 | P3 = primary novelty candidate; no T0 found | `we did not identify an equivalent antecedent in our adversarial audit`. | `first ever`; `proved novel`; `no previous work exists`. | Prior Work; Discussion; possibly Abstract wording only cautiously | Independent expert/literature recheck recommended before submission. |
| CE-049 | The alignment/L2 result is a secondary technical novelty candidate, while the narrow h1→h2 composition result is a narrow technical novelty candidate; neither is the paper's primary headline. | Prior-art/editorial status of P5/P7 | Closed audit/editorial classification | N/A | PRIOR-ART/EDITORIAL | PRIOR-ART-AUDIT-CLOSURE §§8–12,16–17; Architecture v2.1 §17 | P5 secondary; P7 narrow | Keep P5 supporting and P7 extended by default. | Promote generic S4 mathematics or horizon dependence as headline novelty. | Results supporting / Extended | Literature recheck if either is promoted. |
| CE-050 | Any statement that observed individuation generally equals a function of `{system, observable, horizon}` is a conceptual/programmatic hypothesis, not a theorem of this study; the article makes no claim about consciousness. | Broad interpretation / scope | Interpretation only | E / N/A | INTERPRETATION | PRIOR-ART-AUDIT-CLOSURE P8; Architecture v2.1 Discussion/Limitations | P8 conceptual only; broad ancestry | Use only as a clearly labeled hypothesis or future-program statement. | `causal individuation necessarily depends on observable/horizon`; any consciousness conclusion. | Discussion/Limitations only | Yes before elevating to a scientific theorem; consciousness claims require separate work. |

## RESOLUTION OF OPEN-01 — C4 STATUS

`OPEN-01` is **CLOSED**.

The final pre-data executable archive `prereg-A-final.zip` contains the 12-file v8.3 instrument. Direct inspection establishes:

1. `classificador.py` states that it **implements exclusively the frozen definitions** and enumerates C1′, C2 and C3; C3 is explicitly a canary.
2. `dryrun.py` states that the official harness runs **C1′, C2 and C3** internally.
3. `escala.py` exports and checks only `("C1p", "C2", "C3")`.
4. `equivalencias.py` initializes and compares only `C1p`, `C2`, `C3`.
5. `pontuacao.py` scores candidates only over `("C1p", "C2", "C3")`.
6. The final confirmatory decision is:
   `positivo` iff `C1p.passa OR C2.passa`; otherwise `negativo`.
7. The same scoring code states that **C3 is a canary and does not enter H_A**.
8. An exact-token scan over all 12 Python files returns **zero occurrences of `C4`**.
9. The key source-file hashes match the recorded frozen manifest, including:
   - `classificador.py` — `ecaa40c6fa2abf84751811cbe5490073bb68e790ab1d5e135ea9342256b046a3`
   - `pontuacao.py` — `028f5a0327c3e3437ffc6df03d10d45d9a06c3d0ff267795caa6f9e751fe0f57`
   - `dryrun.py` — `43473e07e65d268a285208a410edc14ae69dc93a7a6e572ca74a3957dd54fd21`

### Scientific/protocol interpretation

The evidence supports the narrow statement:

> **C4 was not an executable or scored confirmatory candidate in the final frozen v8.3 instrument.**

It does **not** reconstruct the exact wording or conceptual role of C4 in older protocol drafts. If an earlier draft contained a C4 fallback, that is historical development and must not be retroactively inserted into the final confirmatory Battery A.

The absence of the archival prose protocol from the currently retrievable corpus is therefore no longer a blocker to reporting what the final confirmatory implementation actually executed. A prose-protocol cross-check remains advisable before journal submission as archival housekeeping; if it ever revealed a genuine discrepancy with the frozen implementation, that discrepancy would have to be reported explicitly rather than silently reconciled.

---

## Cross-check against the frozen architecture

The 51 claims preserve the frozen hierarchy:

- **Headline:** CE-001/002, CE-016/017, CE-024–028, CE-031/032.
- **Supporting:** CE-018–020, CE-034–041.
- **Extended:** CE-042–046.
- **Prior-art/interpretation guardrails:** CE-047–050.
- **Protocol-status guardrail:** CE-051.

No ledger row authorizes:
- reinterpretation of the negative confirmatory result;
- C1″;
- `τ∈Iso(W)` as a characterization of all C1′ STATE decisions;
- causal aliasing without independently established `X₀≠X₁`;
- STATE/SIGNAL as universal ontology;
- universal prevalence;
- universal temporal impossibility;
- new general mathematics of symmetry/isometry;
- historical-priority claims stronger than the closed prior-art audit;
- consciousness claims.

---

`BOUNDARY I — PASSO 4A — CLAIM–EVIDENCE LEDGER v1.1 — CANDIDATE FOR FREEZE`
