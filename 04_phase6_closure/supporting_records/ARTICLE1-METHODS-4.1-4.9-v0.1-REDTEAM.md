# ARTICLE 1 — METHODS 4.1–4.9 v0.1 — ADVERSARIAL RED-TEAM REPORT

**Date:** 17 August 2026
**Object reviewed:** `ARTICLE1-METHODS-4.1-4.9-v0.1.md` (sha256 `0643837dbe6b78dab376247286f89b34f46f2fc7aa531557c955bae78f9d0713`, verified)
**Binding sources (Tier 1/2):** the 12 frozen v8.3 Python sources (12/12 sha-verified against `hashes-finais-dev.txt`, itself sha-verified against the pack manifest), FASE6 Formal Closure, Claim–Evidence Ledger v1.1, Article Architecture v2.1, Results v0.2, FASE6 Synthesis, Autopsy, WS1–WS5, C4 Status Resolution, Prior-Art Audit Closure.
**Pack integrity:** 43/43 files present verify against `SHA256SUMS-PACK.txt` (matched by basename; the manifest records a tiered directory layout, the delivered pack is flat — path-prefix discrepancy only, zero content mismatches). `prereg-A-final.zip` is listed in the manifest but absent from the delivered pack; the 12 extracted `.py` files it contains are present and hash-identical to the frozen manifest, so no Tier-1 fact used below depends on the zip. Recorded as an archival note (A-1), not a Methods defect.

**Role:** reviewer adversarial + consistency auditor + technical editor. No redesign, no C1″, no new analyses, no claim expansion.

---

## 1. Verification protocol and independent reconstructions

Every substantive statement in 4.1–4.9 was audited against the frozen sources. The mandate's independent-reconstruction items were executed as follows (all PASS; machine checks run with exact rational arithmetic, no floating point):

| Mandated check | Result | Source anchor |
|---|---|---|
| System I/II/III/E2 dynamics equations vs frozen code | PASS — 4.1 equations match `step_I`, `step_II`, `step_III`, `step_E2` term by term, including `c_{AB,t+1}=x_t`, `c_{BA,t+1}=y_t`, `v_t=π_{m_B}(c_{AB,t})`, `u_t=π_{m_A}(c_{BA,t})`, and `D_{i,t+1}=R_i(s^core_t)` with no feedback | `gerador.py` (step functions; `pack_core10`) |
| Target partitions and media table | PASS — 4.1 table reproduces `ALVOS` and `ALVOS_E2` exactly, comps and media, all five rows | `pontuacao.py` (`ALVOS`, `ALVOS_E2`) |
| θ contents and sampling | PASS — components and uniform sampling match `Theta` / `sample_theta_base`; π₀≠π₁ rejection; E2 extension only after acceptance (also enforced by `test_gerador.test_estrato2_extensao_so_apos_aceitacao`) | `gerador.py` |
| RNG-stream structure | PASS — `SeedSequence(root).spawn(4)`, positional assignment [0] θ, [1] export, [2] shuffle/IDs, [3] E2 | `gerador.gerar_lote` |
| Eligibility mapping E1–E6 | PASS — the five E1–E5 paraphrases in 4.2 map one-to-one to `cond1_memoria` … `cond5_sigma`; E6 to `cond6_remapeamento`; eligibility conjunction over I, II, III + E6(II); D modules excluded | `gerador.elegibilidade` |
| E1/E2 sizes | PASS — 50×3=150; 25×2=50 | `pontuacao.ESPERADO_E1/E2` |
| Blinding description | PASS — bit permutation + module-order permutation; boundaries and memory designations visible; `Q_k` identifiers; key contents (variant, perm, module order, family, θ-hash); procedural-not-cryptographic wording matches the frozen `nota_cegamento` clause for clause (key moved out, no rerun with confirmatory seed, opening only at prespecified step after SHA check) | `gerador.exportar_instancia`, manifest `nota_cegamento` |
| Intervention family and frozen order | PASS — I_A definition, null included, \|I_A\|=3^{\|B_A\|}; exact re-enumeration of `intervencoes([b0,b1])` reproduces the frozen order **null; b0:=0; b0:=1; b1:=0; b1:=1; c:=0,1,2,3** (9 for a 2-bit module; 27 confirmed for a 3-bit module); transient semantics (overwrite + ONE global transition) | `classificador.intervencoes`, module docstring |
| G_C definition | PASS — non-null intervention, orbit-reached context, difference vs null-intervention next state of B, no self-edges | `classificador.classificar` (EC loop) |
| C1′ fiber, profile, canonical weak rank, STATE rule | PASS — full fiber per reached memory value, aligned free axis; d_m(a)=Σ_r Ham_B; ρ as count of *distinct* strictly smaller values; STATE ⇔ identical canonical rank vectors across reached contexts | `classificador.estados_da_fibra`, `rank_canonico`, `c1_estado` |
| C2 / C3 definitions | PASS — C2: per-bit effective-intervention sets, complete (⊆, =) relation invariance; C3: per-bit signature-support invariance; C3 executed and scored but outside H_A | `classificador.c2_estado`, `c3_estado`; `pontuacao` |
| Media rule | PASS — SCC≥2, or memory-bearing singleton with eligibility-certified recurrence (Amendment 1, item 1a; σ/π cancellation rationale); memoryless modules never singleton media | `classificador.py` (meios block + comment) |
| Scale item | PASS — all S with 2≤\|S\|<n; A1 exact fiber consistency over every intervention on subsets of S; quotient construction; memory ∩ S; same frozen classifier; component-relation biconditional; E2 validity = ≥2 admissible projections of distinct granularities, failure ⇒ annulment | `escala.py`, `pontuacao.py` |
| Equivalence group and sizes | PASS — three generator families (same-form renamings, designation-respecting internal permutations, independent flips), conjugation of transition AND initial condition (rev. 8.1), S_{2^d} exclusion; sizes independently recomputed: **512 / 65,536 / 524,288** | `equivalencias.py`, `pontuacao.GRUPOS_ESPERADOS` |
| Scoring order and conjunction | PASS — integrity → E2 validity → canary → per-candidate items; pass = targets_E1 ∧ targets_E2 ∧ scale ∧ equivalences; all 200 micro instances count; "wrong but stable" is not success; H_A positive iff C1′ or C2; C3 outside H_A; **no C4 path** (CE-051, C4-STATUS-RESOLUTION) | `pontuacao.pontuar` |
| 4.6 pull-back lemma re-derivation | PASS — re-derived from `step_II`: response `M[r][π_m(c)]⊕σ[m]`; memory update (K/H) channel-independent at the current step; σ cancels in XOR; orientation τ=π₁∘π₀⁻¹ consistent with Synthesis/W̃ convention (WS1's ρ=π₀⁻¹∘π₁ is its documented conjugate; the manuscript is internally uniform) | `gerador.step_II`; Synthesis §9, §21.4 |
| 4.7 geometry and multiplicity | PASS — w_r, W_M, W̃_m re-derived; fiber 2^{n−1} states / 16 (r,c) cells ⇒ multiplicity **2^{n−5}** (32 for n=10, 128 for n=12; E2/E1 factor 4 = frozen lemma d_E2=4·d_E1) | Synthesis §9; `verifica_E1_E2` record |
| 4.8 class-level proposition | PASS — proof chain checked line by line; scope restricted to observables factoring through the cell-weight field; blindness ≠ aliasing guardrail present; invariance labeled standard mathematics | Ledger CE-014/CE-015; Architecture §4.2 |
| 4.9 six entries and 6×6 map | PASS — **independently reconstructed** from the frozen intervention order: A=w01+w23, B=w02+w13, V_γ = degree sums; the resulting L matches the draft's displayed matrix row by row |  frozen order + pair algebra |
| 4.9 rank/determinant | PASS — exact-fraction elimination gives **det L = −8, rank 6**; bit-only sub-lattice {A,B} rank **2**; full-channel sub-lattice {V₀..V₃} rank **4** — matching the draft and the frozen record | Synthesis §17.4; FASE6-FORMAL-CLOSURE §4.2 |
| 4.9 equivalence chain and scope | PASS — d₀=d₁ ⇔ W̃₀=W̃₁ ⇔ τ∈Iso(W_M) stated as **L1 only**; L2 explicitly separate (deferred to 4.10); determining-set argument explicitly not claimed as new mathematics | Ledger CE-016/CE-017; Architecture §4.3 |

No genuine ambiguity in the frozen source material was encountered; no unresolved blocker of the "archival evidence required" type exists.

---

## 2. Findings

Severity scale: BLOCKER / MAJOR / MINOR / COSMETIC. Every proposed correction below describes the frozen record only; none adds a scientific claim, empirical result, theorem, criterion, or epistemic promotion.

### RT-M1 — 4.3 omits the degenerate-context rule for memoryless receivers — **MAJOR**

**Defect.** The C1′/C2/C3 edge-labeling in 4.3 is defined only "for a receiver B with retained-memory coordinates M_B". The frozen classifier additionally fixes, for receivers **without** retained memory (interface modules; in E2 also D₁, D₂), a single degenerate context {⊥} whose fiber is the entire state space:

- `classificador.py:136` — `mem_reach[i] = [None]  # conjunto contextual singular {⊥}`;
- `classificador.py:163` — fiber = full `arange(1<<n)` when the context is `None`.

With one context, the cross-context invariance conditions of all three candidates hold trivially, so every G_C edge into a memoryless receiver is STATE — asserted by the frozen test suite (`test_classificador.py:51`, `test_receptor_sem_memoria_e_estado`, for all three candidates). This rule is not decorative: it is why the System-II processor→interface ring edges are always STATE, hence why a total core collapse under a candidate is decided exactly by the two channel→processor edges (Ledger CE-020; Synthesis §7/§9). Without it, Methods 4.3 does not reproduce the frozen G_S/SCC behavior, and the manuscript's own Results (2.1, 2.6) silently depend on it.

**Correction (v0.2).** Add one paragraph at the end of the "C2 and C3" subsection stating the degenerate-context rule and its ring consequence, in the exact scope of the frozen code and CE-020. No new claim: this is a description of frozen executable behavior already relied upon by frozen Results.

### RT-m2 — 4.3 integrity audit omits the G_C-conjugation annulment — **MINOR**

**Defect.** The audit sentence lists cardinalities/IDs, equivalence counts, E2 validity, and the canary, but the frozen integrity audit also annuls on any G_C discrepancy under the equivalence conjugations (`pontuacao.py:109`, `discrepancias_base != 0`; `equivalencias.comparar` returns `BASE`, documented as instrument failure, never candidate defeat — Amendment 1, item 3).

**Correction (v0.2).** Add the G_C-conjugation invariance to the audited list, marked as an instrument-level integrity condition.

### RT-m3 — 4.3 canary condition unspecified — **MINOR**

**Defect.** "The C3-specific canary condition" is named but not stated, so the annulment trigger is not reproducible from Methods alone. Frozen definition (`pontuacao.py:14–17`, `_canario`): in **all 75 confirmatory System-II instances (50 E1 + 25 E2)**, the edges C_AB→B and C_BA→A must exist in G_C and be labeled STATE by C3; an absent edge or a SIGNAL label annuls the execution.

**Correction (v0.2).** State the condition in one clause.

### RT-m4 — 4.5/4.6 provenance labels — **MINOR**

**Defect.** Section 4.4 opens the post-confirmatory block explicitly, but 4.5 and 4.6–4.9 do not restate their provenance. Architecture §0.9 requires the confirmatory/post-confirmatory chronology to remain visible; a reviewer reading 4.5 (strict realization) or 4.6–4.9 (formal analysis) in isolation could mistake them for parts of the frozen procedure.

**Correction (v0.2).** One sentence at the start of 4.5 and one at the start of 4.6 (covering 4.6–4.9) stating post-confirmatory provenance and that the frozen criterion is unchanged. Matches Ledger CE-005 and the claim-map boundary "the post-confirmatory response-field formalization does not modify C1′".

### RT-m5 — 4.3 scale item: strata coverage and projected media — **MINOR**

**Defect (two parts).** (i) The frozen scale executor runs in **both** confirmatory strata (`escala.py:19–22`, "COBERTURA POR ESTRATO: este executor corre nos DOIS estratos"), and the candidate scale item conjoins E1 and E2 stability (`pontuacao` `itens["escala"]` over `escala_e1` and `escala`); 4.3 does not say so. (ii) The classifier returns media for projected quotients, but Section 7 of the protocol compares **exclusively components**, and the executor neither interprets nor scores projected media (`escala.py:24–27`); 4.3's silence could be read as media entering the scale comparison.

**Correction (v0.2).** Add "in both confirmatory strata" and one sentence: projected media computed but not scored; component relation only.

### RT-m6 — 4.2 initial conditions' sampling law unstated — **MINOR**

**Defect.** 4.2 states uniform sampling for the base tables but not for the initial processor/memory/interface states, which are likewise sampled uniformly (`gerador.py:83–86`).

**Correction (v0.2).** Extend the sentence by one clause.

### RT-c7 — 4.2 "two independent forms of label destruction" — **COSMETIC**

**Defect.** Both randomizations are drawn from the single export stream; "independent" invites a formal-independence reading the source does not state. The two permutations are separate draws, not a declared independence property.

**Correction (v0.2).** "two separate label-destroying randomizations".

### A-1 — Archival note (not a Methods defect) — **COSMETIC / ARCHIVAL**

`prereg-A-final.zip` (sha `d77dbed4…`) is listed in `SHA256SUMS-PACK.txt` but absent from the delivered flat pack. All 12 extracted sources are present and hash-verified, and CE-051/C4-STATUS-RESOLUTION rest on the extracted sources plus the recorded manifest, so nothing in Methods is affected. Recommend restoring the zip to the archival pack before submission-stage packaging.

**No BLOCKER issues were found.**

---

## 3. Cross-document consistency audit (Methods v0.1 ↔ Results v0.2 ↔ Ledger v1.1 ↔ Architecture v2.1)

Checked sentence-level wherever the same object appears. **No mismatch found** in:

- **Notation:** pc₂, W_M, W̃_m, τ=π₁∘π₀⁻¹ (uniform orientation throughout the manuscript), sub_a(c), ρ (canonical weak rank), L1/L2/L3, (r,c).
- **Causal directions:** C_AB→B with M=G₀, r=y; C_BA→A with M=F₀, r=x — identical in 4.6 and Results 2.3.
- **Denominators/sizes:** 150/50/200; 75 System-II confirmatory instances; group sizes 512/65,536/524,288; 9 interventions; n=6/10/12; multiplicity 2^{n−5} and the ×4 E2 factor.
- **Theorem scope:** exact equivalence presented as **L1 only** in both Methods 4.9 and Results 2.5, with L2 separate (Results 2.6 / Methods 4.10 deferral); class-level proposition (4.8) restricted to cell-weight-factoring observables, identical to Results 2.4; ranks 2/4/6 and det −8 identical.
- **Provenance vocabulary:** blindness vs causal aliasing vs strictly realized (with the (r,c) qualification) used identically; confirmatory vs post-confirmatory boundaries aligned with the epistemic-provenance scheme; no "independent replication" language anywhere in 4.1–4.9.
- **C1′/C2/C3/C4 status:** identical to Results 2.1 and CE-001…CE-004, CE-051 (C4 bounded to absence from the final executable/scored instrument).

## 4. Forbidden-claims scan

Scanned v0.1 for every prohibited formulation: near-success readings of 199/200; modification of `passa=false`; C1″; new criteria; post→confirmatory promotion; "τ∈Iso(W) characterizes all C1′ blindness"; blindness=aliasing without independent X₀≠X₁; STATE/SIGNAL ontology; universal prevalence; consciousness; historical priority / "first ever". **None present.** The construct-validity guardrails (operational targets "by construction") are present in 4.1 as required by Architecture §0.5/§12.

## 5. Verdict

Corrections are justified: **1 MAJOR (RT-M1), 5 MINOR (RT-m2…RT-m6), 1 COSMETIC (RT-c7)**, plus one archival note (A-1) outside the manuscript. All are faithful descriptions of the frozen record; none expands any claim. A v0.2 is issued with exactly these corrections; the diff is audited in `ARTICLE1-METHODS-4.1-4.9-v0.2-FORMAL-VALIDATION.md`.

`ARTICLE 1 — METHODS 4.1–4.9 v0.1 — RED-TEAM COMPLETE — v0.2 REQUIRED`
