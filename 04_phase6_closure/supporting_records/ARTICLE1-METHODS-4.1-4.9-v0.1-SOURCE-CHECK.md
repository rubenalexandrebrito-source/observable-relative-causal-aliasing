# ARTICLE 1 — METHODS 4.1–4.9 v0.1 — INTERNAL SOURCE CHECK

This note records the source facts used to draft Methods 4.1–4.9.

## Frozen executable facts checked directly

### `gerador.py`
- v8.3 frozen generator.
- I: 6 bits; II/III: 10 bits; E2: 12 bits.
- Processor/memory/channel equations reproduced in Methods.
- E2 `D_i(t+1)=R_i(core_t)` with no core feedback.
- Eligibility exactly `E1:5(I) ∧ E1:5(II) ∧ E1:5(III) ∧ E6(II)`.
- Randomness: PCG64 with four spawned streams.
- Blind export: bit permutation, module permutation, anonymous `Qk` IDs.
- Hidden key contains variant, permutation, module order; family/theta hash added by lot generator.
- Procedural-blinding note: key moved before analysis; generator not rerun with confirmatory seed; key opened only at prespecified scoring step after SHA check.
- E1 generates I/II/III per family; E2 generates II/III per family.

### `classificador.py`
- Pure blinded instance→classification; never reads key.
- Complete coordinate intervention family; null included; `|I_A|=3^|bits|`.
- One-transition intervention semantics.
- `G_C` definition and no self-edges.
- Full aligned receiver-memory fibers.
- C1′ weak-order profile with tie preservation.
- C2 partial-order invariant.
- C3 support canary.
- STATE graph → SCC components.
- Media rule for unprojected accepted instances.

### `escala.py`
- Exact fiber-consistency admissibility over all interventions on `S`.
- All `2 <= |S| < n`.
- Quotient transition and projected initial state/module/memory structure.
- Same classifier applied to each admissible projection.
- Component-equivalence preservation among surviving modules.
- E2 validity requires >=2 admissible projections of distinct granularities.

### `equivalencias.py`
- Exhaustive confirmatory group.
- Module renamings within same form.
- Internal coordinate permutations respecting memory designation.
- Independent bit flips.
- Transition and initial-state conjugation.
- Arbitrary state bijections excluded because they destroy coordinate intervention semantics.

### `pontuacao.py`
- Exact E1/E2 counts and target partitions.
- Expected exhaustive group sizes 512 / 65536 / 524288.
- Integrity → E2 validity → C3 canary → candidate scoring order.
- Candidate pass = E1 targets AND E2 targets AND scale AND equivalences.
- Scientific result positive iff C1′ or C2 passes.
- C3 does not enter H_A.

## Post-confirmatory sources checked

- WS3: `(r,c)` causally sufficient local comparability; strict support and observational-witness definitions.
- WS1/WS2/Synthesis: System-II pull-back reduction, `W_M`, closed-form `d`, `W̃↔d` bijection.
- 6×6 matrix reconstructed from the six frozen measured quantities; determinant verified as `-8` and rank `6`.
- Architecture/Ledger: scope and wording guardrails.

No claim from Methods 4.10–4.15 was imported as a new result into this draft.
