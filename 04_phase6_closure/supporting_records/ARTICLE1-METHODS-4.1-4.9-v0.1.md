# ARTICLE 1 — METHODS 4.1–4.9 — v0.1

**Status:** manuscript draft derived from the frozen v8.3 instrument, frozen Article Architecture v2.1, frozen Claim–Evidence Ledger v1.1, and frozen Results v0.2  
**Date:** 17 August 2026  
**Scope:** Methods 4.1–4.9 only. Sections 4.10–4.15 remain outside this draft.

---

# 4. Methods

## 4.1 Operational targets and construct validity

### Synthetic systems and module structure

The study used deterministic finite-state systems designed as a controlled testbed for an operational distinction between two forms of interaction. The labels `STATE` and `SIGNAL` are therefore **classifier labels and preregistered design targets**, not claims that the synthetic systems instantiate a universal ontology of physical, biological, or communicative interaction.

The two processor modules were

\[
A=(x,m_A),\qquad B=(y,m_B),
\]

where \(x,y\in\{0,1,2,3\}\) are two-bit processor states and
\(m_A,m_B\in\{0,1\}\) are retained one-bit receiver states. Systems II and III additionally contained two two-bit interface modules,

\[
C_{AB}=c_{AB},\qquad C_{BA}=c_{BA},
\]

with \(c_{AB},c_{BA}\in\{0,1,2,3\}\). Thus System I had six state bits and Systems II/III had ten. The second confirmatory stratum (E2) appended two one-bit downstream modules \(D_1,D_2\), giving twelve bits. The downstream modules read the previous core state but did not feed back into the core:

\[
D_{i,t+1}=R_i(s^{\mathrm{core}}_t).
\]

For each sampled family \(\theta\), the common processor and memory maps were

\[
F_0,G_0:\{0,1,2,3\}^2\rightarrow\{0,1,2,3\},
\]

\[
H,K:\{0,1\}\times\{0,1,2,3\}\rightarrow\{0,1\},
\]

with memory-dependent additive terms
\(\sigma_A,\sigma_B:\{0,1\}\rightarrow\{0,1,2,3\}\).
System II additionally used two distinct permutations
\(\pi_0,\pi_1\in S_4\).

### Dynamics

System I implemented direct reciprocal processor input:

\[
u_t=y_t,\qquad v_t=x_t,
\]

\[
x_{t+1}=F_0(x_t,u_t)\oplus\sigma_A(m_{A,t}),
\qquad
m_{A,t+1}=H(m_{A,t},x_t),
\]

\[
y_{t+1}=G_0(y_t,v_t)\oplus\sigma_B(m_{B,t}),
\qquad
m_{B,t+1}=K(m_{B,t},y_t).
\]

Systems II and III used explicit interface variables, with

\[
c_{AB,t+1}=x_t,\qquad c_{BA,t+1}=y_t.
\]

In System III, the processors read the interface directly,

\[
v_t=c_{AB,t},\qquad u_t=c_{BA,t}.
\]

In System II, receiver memory contextually relabeled the incoming interface:

\[
v_t=\pi_{m_{B,t}}(c_{AB,t}),
\qquad
u_t=\pi_{m_{A,t}}(c_{BA,t}).
\]

The processor and memory update equations otherwise remained the same across the three systems.

### Preregistered operational partitions

The preregistered scoring target was defined at the level of the component partition induced by the classifier and, for unprojected systems, its corresponding set of causal media. The target was fixed by construction:

| Stratum / system | Target component partition | Target media |
|---|---|---|
| E1 / I | \(\{A,B\}\) | \(\{A,B\}\) |
| E1 / II | \(\{A\},\{B\},\{C_{AB}\},\{C_{BA}\}\) | \(\{A\},\{B\}\) |
| E1 / III | \(\{A,B,C_{AB},C_{BA}\}\) | \(\{A,B,C_{AB},C_{BA}\}\) |
| E2 / II | \(\{A\},\{B\},\{C_{AB}\},\{C_{BA}\},\{D_1\},\{D_2\}\) | \(\{A\},\{B\}\) |
| E2 / III | \(\{A,B,C_{AB},C_{BA}\},\{D_1\},\{D_2\}\) | \(\{A,B,C_{AB},C_{BA}\}\) |

These partitions are **pre-specified targets of the synthetic generative design**. The study asks whether a frozen interventional classifier preserves that designed mechanistic distinction under blinding, scale projections, and admissible representational equivalences. It does not establish that the labels System II/System III, STATE/SIGNAL, or the resulting partitions are a universal taxonomy of interactions in natural systems.

---

## 4.2 Preregistered protocol, generation, and blinding

### Family generation

A family \(\theta\) comprised \(F_0,G_0,H,K,\sigma_A,\sigma_B,\pi_0,\pi_1\), initial processor/memory/interface states, and, in E2, downstream lookup tables \(R_1,R_2\) and initial downstream bits. The base tables were sampled uniformly over their finite codomains. The two interface permutations were sampled independently and families with \(\pi_0=\pi_1\) were rejected.

Randomness was a deterministic function of the root seed using NumPy PCG64. Four child streams were assigned positionally to (i) nuclear family generation, (ii) export permutations, (iii) instance shuffling/identifiers, and (iv) E2 downstream extensions. E2 extensions were sampled only after the nuclear family passed eligibility, preventing rejected nuclear families from consuming downstream random draws.

Eligibility was assessed on the core dynamics before blind export. For every accepted family, Systems I, II, and III had to satisfy the preregistered conditions E1–E5, including visitation of both retained-memory contexts, efficacy of both incoming processor inputs, recurrence witnesses linking processor state and retained memory, sufficient local-state reachability, and non-degenerate memory-dependent additive effects. System II additionally had to satisfy E6, a witnessed memory-dependent remapping effect in both directions. Downstream E2 modules were excluded from eligibility because they had no feedback into the core.

### Confirmatory strata

The first confirmatory stratum E1 contained 50 accepted families. Each family generated one instance of System I, one of System II, and one of System III, for

\[
50\times 3=150
\]

instances.

The second stratum E2 contained 25 accepted extended families. Each generated one System-II and one System-III instance with downstream modules \(D_1,D_2\), for

\[
25\times 2=50
\]

instances.

The confirmatory root seeds were fixed before generation and each was used exactly once. Their values and the complete execution manifests are retained in the reproducibility record described in Section 4.15.

### Blind export

Before analysis, each instance underwent two independent forms of label destruction. First, the state-bit coordinates were randomly permuted. Second, module order was randomly permuted. Module boundaries and retained-memory bit designations remained visible because they were required by the classifier, but semantic module identities were replaced by anonymous identifiers \(Q_0,Q_1,\ldots\). No marker identified system type, family membership, or paired variants.

For each instance, the hidden key recorded the system variant, bit permutation, module-order permutation, family index, and a hash of the generating \(\theta\). The key was serialized separately from the blinded transition table. Blinding was procedural rather than cryptographic: code and seed could in principle regenerate the key. The frozen procedure therefore required that the key be moved outside the classifier-accessible directory before analysis, that the generator not be rerun with a confirmatory seed during analysis, and that the key be opened only at the prespecified scoring step after verification against its recorded SHA-256 digest.

The classifier itself was a pure map from a blinded instance to a classification and contained no key-reading path. Confirmatory output directories were required to be new, canonical JSON bytes were hashed at write time, and the post-confirmatory workflow left the official confirmatory artifacts unchanged.

---

## 4.3 Interventions, causal graph, C1′, and confirmatory scoring

### One-step intervention semantics

For a module \(A\) with coordinate set \(B_A\), the intervention family was complete over coordinate rewrites:

\[
\mathcal I_A
=
\left\{
do(J=\eta):
J\subseteq B_A,\;
\eta\in\{0,1\}^{|J|}
\right\}.
\]

The null intervention \(do(\varnothing)\) was included. Hence

\[
|\mathcal I_A|=3^{|B_A|}.
\]

Interventions were transient: the selected sender bits were overwritten and the system then underwent **one** global transition. For a two-bit channel this produced nine interventions, in the frozen order: null; low bit set to 0 or 1; high bit set to 0 or 1; and the full channel set to each of \(0,1,2,3\).

### Causal edge set \(G_C\)

Let \(\mathcal O(s_0)\) be the deterministic orbit from the initial state to first repetition. For distinct modules \(A\neq B\), an edge \(A\to B\) was placed in the pre-classification causal graph \(G_C\) when there existed a non-null intervention on \(A\) and an orbit-reached context for which the next state of \(B\) differed from the null-intervention next state. Self-edges were excluded.

Thus the subsequent STATE/SIGNAL decision was made only for edges with a witnessed one-step causal effect in \(G_C\).

### Counterfactual fibers and C1′

For a receiver \(B\) with retained-memory coordinates \(M_B\), let
\(\mathcal M_B^{\mathrm{reach}}\) denote the memory values reached on the orbit. For each reached value \(m\), the counterfactual fiber contained **all** global states with receiver memory fixed to \(m\). All remaining coordinates formed an aligned free axis \(r\), identical across memory contexts.

For an intervention \(a\in\mathcal I_A\), define the receiver response profile

\[
d_m(a)
=
\sum_r
\operatorname{Ham}_B
\left(
\Phi^a(r,m),\Phi^0(r,m)
\right),
\]

where \(\Phi^a(r,m)\) is the next receiver state after applying intervention \(a\) to the global state indexed by \((r,m)\), and \(\Phi^0\) is the null-intervention baseline.

C1′ does not require equality of the cardinal values \(d_m(a)\). It compares their **weak order with ties**. The canonical weak rank of profile entry \(a\) is

\[
\rho_m(a)
=
\left|
\left\{
d_m(a'):
d_m(a')<d_m(a)
\right\}
\right|,
\]

where duplicate smaller values count once. Two profiles have the same canonical rank vector if and only if they have the same weak order and the same tie structure.

A causal edge \(A\to B\) was labeled

\[
\mathrm{STATE}
\quad\Longleftrightarrow\quad
\rho_m=\rho_{m'}
\;\;\text{for all reached }m,m',
\]

and SIGNAL otherwise.

### C2 and C3

C2 used a different invariant. For each receiver output bit \(b_k\), it formed the set of interventions on the sender that were effective on that bit within a fixed memory context. C2 labeled an edge STATE when the complete partial-order relation of inclusion and equality among these effective-intervention sets was invariant across reached receiver-memory contexts.

C3 was an analytic implementation canary. For each receiver output bit it recorded whether the exact intervention-response signatures varied across interventions, producing a support set for each memory context. C3 labeled an edge STATE when this support set was invariant. C3 was executed and scored for audit purposes but was not a scientific \(H_A\) decision candidate.

### STATE graph, components, and media

For each candidate \(C\in\{\mathrm{C1'},\mathrm{C2},\mathrm{C3}\}\), the STATE graph \(G_S^C\) retained only those edges of \(G_C\) labeled STATE by \(C\). The component partition was the set of strongly connected components of \(G_S^C\).

For unprojected confirmatory systems, a causal medium was either (i) a strongly connected component containing at least two modules, or (ii) a singleton module carrying preregistered retained memory. For accepted unprojected instances, the recurrence requirement of such memory-bearing singletons had already been certified by eligibility and was not re-inferred from the net transition-table effect, because cancellation between \(\sigma\) and \(\pi_m\) can make that net effect misleading in System II. Modules without retained memory could not form singleton media.

### Scale-preservation item

The confirmatory score also required stability under admissible coordinate projections. For every subset \(S\) with

\[
2\le |S|<n,
\]

the scale executor first tested exact fiber consistency of the projected transition for **every intervention on subsets of \(S\)**. If the projection was admissible, it constructed the quotient transition \(T_S\), projected the initial state and surviving modules, projected retained-memory coordinates by intersection with \(S\), and applied the same frozen classifier. For each candidate, scale preservation required that every pair of surviving modules be in the same component after projection if and only if it was in the same component in the micro system.

In E2, execution validity additionally required at least two admissible projections of distinct granularities. Failure of this construction requirement annulled the execution rather than defeating a candidate.

### Representational-equivalence item

The final scientific invariance item exhaustively enumerated the preregistered group of coordinate representations that preserve modular form, memory designation, and the atomic intervention algebra:

1. module renamings only within equal module forms \((n_{\mathrm{bits}},n_{\mathrm{memory\ bits}})\);
2. within-module coordinate permutations with memory coordinates mapped to memory coordinates and non-memory coordinates to non-memory coordinates;
3. independent bit flips.

The transition table and initial condition were conjugated under each transformation. Arbitrary \(S_{2^d}\) state bijections were excluded because they do not preserve coordinate interventions. For every transformed instance, \(G_C\), edge labels, component partitions, and media were compared after the corresponding module renaming. Confirmatory enumeration was exhaustive; the expected group sizes were 512 for E1/System I, 65,536 for E1/Systems II and III, and 524,288 for E2/Systems II and III.

### Candidate and experiment-level decision rules

Before any scientific candidate was evaluated, the scoring program audited exact instance cardinalities and IDs, exhaustive equivalence counts, E2 scale validity, and the C3-specific canary condition. Integrity, E2-construction, or canary failures produced procedural annulment states rather than scientific candidate defeats.

For each of C1′, C2, and C3, a candidate-level pass required the conjunction of four items:

\[
\mathrm{targets}_{E1}
\land
\mathrm{targets}_{E2}
\land
\mathrm{scale}
\land
\mathrm{equivalences}.
\]

All 200 micro-level confirmatory instances counted toward the target items; a wrong partition that was stable under scale or equivalence transformations did not count as success.

The scientific confirmatory result \(H_A\) was positive if and only if C1′ **or** C2 passed all four items. C3 did not enter \(H_A\). The frozen executable contained no C4 scoring path.

---

## 4.4 Response-field definitions for the post-confirmatory analysis

The post-confirmatory analysis retained the frozen intervention semantics and classifier state fibers but made the pointwise response field explicit.

For a causal edge from sender \(A\) to receiver \(B\), fix a reached receiver-memory context \(m\). Let \(Z_m\) be the full aligned fiber of global states whose receiver-memory coordinates equal \(m\). For each free-axis index \(r\), write \(z(r,m)\in Z_m\).

Let \(e_B\) extract the receiver module from a global state and let
\(I_a\) denote the overwrite map for intervention \(a\). Define

\[
\Phi_m^a(r)
=
e_B\!\left[
T\!\left(I_a(z(r,m))\right)
\right],
\]

and the pointwise intervention response relative to the null intervention as

\[
X_m^a(r)
=
\Phi_m^a(r)\oplus \Phi_m^0(r).
\]

The frozen C1′ cardinal profile is therefore

\[
d_m(a)
=
\sum_r
\operatorname{pc}\!\left(X_m^a(r)\right).
\]

For the post-confirmatory cross-context analysis, pointwise memory dependence was defined by

\[
X_0^a(r)\neq X_1^a(r).
\]

The total pointwise dependence count for an edge was the number of intervention/free-axis pairs \((a,r)\) satisfying this inequality. This quantity is finer than C1′ because C1′ first converts the response pattern to Hamming weight and then aggregates over the full fiber before applying weak rank.

The post-confirmatory levels used throughout the analysis were:

\[
\mathrm{L1}:\quad d_0=d_1,
\]

\[
\mathrm{L2}:\quad d_0\neq d_1
\;\land\;
\rho_0=\rho_1,
\]

\[
\mathrm{L3}:\quad \rho_0\neq\rho_1.
\]

L1 and L2 are therefore distinct routes to the same C1′ STATE edge label; L3 is a SIGNAL edge.

---

## 4.5 Causally sufficient local-state comparability and strict realization

The full counterfactual fiber deliberately ranges over global states that need not all be visited by the orbit. To test whether a cross-context causal difference survived in realized dynamics, we separately defined realized support.

For a channel-to-processor edge in System II, let \(r\) denote the non-memory processor state of the receiver and let \(c\) denote the incoming channel symbol. For memory context \(m\), define

\[
\mathcal C_m
=
\left\{
(r,c):
(r,c,m)\ \text{occurs in a state on the deterministic orbit}
\right\}.
\]

The strict realized support is

\[
\mathcal I
=
\mathcal C_0\cap\mathcal C_1.
\]

### Local sufficiency

For the frozen one-step System-II channel-to-processor contrast, conditional on receiver memory \(m\), the pointwise response to a channel intervention is a function only of \((r,c)\). All other global coordinates are irrelevant to that response at the current step. Consequently, \((r,c)\) is the coarsest causally sufficient comparability state for this contrast:

- refining \((r,c)\) with additional global coordinates can only reduce the observed support intersection by demanding equality of coordinates that do not affect the response;
- coarsening \((r,c)\) can merge states that have different one-step responses.

A **strictly realized dependency site** was therefore an intervention/cell pair

\[
(a,(r,c)),\qquad (r,c)\in\mathcal I,
\]

for which

\[
X_0^a(r,c)\neq X_1^a(r,c).
\]

This definition does not require the complete global state to be identical across contexts; it requires equality of the local state that is sufficient for the causal contrast being tested.

### Realized-transition observational witness

As a complementary check requiring no counterfactual overwrite, for two channel values \(c_1,c_2\) realized with the same receiver state \(r\) under both memory contexts, we defined

\[
O_m(r;c_1,c_2)
=
e_B[T(s(r,c_1,m))]
\oplus
e_B[T(s(r,c_2,m))].
\]

A realized-transition witness exists when

\[
O_0(r;c_1,c_2)\neq O_1(r;c_1,c_2).
\]

This test asks whether the context-dependent interface effect can be seen directly in transitions that the deterministic trajectory actually visits.

---

## 4.6 Contextual pull-back lemma for System II

Consider a decisive System-II channel-to-processor edge and condition on receiver memory \(m\).

For \(C_{AB}\to B\), write the receiver processor state as \(r=y\), the incoming channel value as \(c=c_{AB}\), and \(M=G_0\). The next processor state is

\[
M[r][\pi_m(c)]\oplus\sigma[m].
\]

The receiver memory update \(K[m][r]\) is independent of the channel value \(c\). Thus a channel intervention changes neither the current-step receiver-memory update nor any other component of the receiver module except through the processor response.

For \(C_{BA}\to A\), the same form holds with \(r=x\), \(c=c_{BA}\), \(M=F_0\), and the receiver-memory update \(H[m][r]\).

Let \(\mathrm{sub}_a(c)\) denote the channel symbol obtained after applying the bit-rewrite intervention \(a\). The XOR intervention response is

\[
\begin{aligned}
X_m(a;r,c)
&=
\left(
M[r][\pi_m(\mathrm{sub}_a(c))]
\oplus \sigma[m]
\right)
\\
&\qquad\oplus
\left(
M[r][\pi_m(c)]
\oplus \sigma[m]
\right)
\\[2mm]
&=
M[r][\pi_m(\mathrm{sub}_a(c))]
\oplus
M[r][\pi_m(c)].
\end{aligned}
\]

Hence \(\sigma[m]\) cancels exactly. Receiver memory remains causal in this contrast through its selection of \(\pi_m\), not through the additive term.

Define the context-free response tensor

\[
X_\star(a;r,c)
=
M[r][\mathrm{sub}_a(c)]
\oplus M[r][c].
\]

Then the context-specific field is the pull-back of the same receiver mechanism by \(\pi_m\): memory changes which interface symbol is presented to \(M\), while the receiver table itself is fixed. The relative contextual transport is

\[
\tau
=
\pi_1\circ\pi_0^{-1}.
\]

This reduction is specific to the proven one-step comparison class: aligned full fibers, contextual interface relabeling, channel-independent current-step memory update, and XOR differencing. It is not assumed for arbitrary dynamics or arbitrary temporal horizons.

---

## 4.7 Mechanism-dependent response geometry

For a fixed receiver table \(M\), define the row-resolved pairwise response weight

\[
w_r(p,q)
=
\operatorname{pc}_2
\left(
M[r][p]\oplus M[r][q]
\right),
\]

where \(\operatorname{pc}_2\) is Hamming popcount on the two processor-output bits. The aggregate receiver-response geometry is

\[
W_M(p,q)
=
\sum_{r=0}^{3} w_r(p,q)
=
\sum_{r=0}^{3}
\operatorname{pc}_2
\left(
M[r][p]\oplus M[r][q]
\right).
\]

\(W_M\) is symmetric with zero diagonal and depends on the concrete receiver mechanism \(M\).

The memory-context pull-back of this geometry is

\[
\widetilde W_m(c_1,c_2)
=
W_M\!\left(
\pi_m(c_1),\pi_m(c_2)
\right).
\]

Using the lemma in Section 4.6 and summing over the aligned full fiber, the frozen C1′ cardinal statistic on a channel intervention \(a\) has the exact form

\[
d_m(a)
=
2^{n-5}
\sum_{c=0}^{3}
\widetilde W_m
\left(
c,\mathrm{sub}_a(c)
\right).
\]

The factor \(2^{n-5}\) is a context-independent multiplicity contributed by the remaining free coordinates of the full fiber. Thus the same core statistic is multiplied by \(32\) for \(n=10\) and by \(128\) for \(n=12\). In particular, the two downstream E2 bits multiply the corresponding E1 channel statistic by four without changing its weak order.

Define

\[
\operatorname{Iso}(W_M)
=
\left\{
g\in S_4:
W_M(gp,gq)=W_M(p,q)
\;\;\forall p,q
\right\}.
\]

This is the group of interface permutations invisible to the aggregate receiver-response geometry.

---

## 4.8 Class-level symmetry-blindness proposition

The mechanism above can be stated without reference to the particular generator.

Let \(C\) be a finite interface alphabet and suppose two contexts \(m\in\{0,1\}\) act on a fixed response mechanism only by interface relabelings \(\pi_m\). Let \(W\) be the pairwise response geometry induced by that fixed mechanism, and define

\[
\widetilde W_m(c_1,c_2)
=
W(\pi_m(c_1),\pi_m(c_2)).
\]

Let

\[
\tau=\pi_1\circ\pi_0^{-1}.
\]

Consider any observable \(F\) whose contextual input factors only through the cell-weight field \(\widetilde W_m\). If

\[
\tau\in\operatorname{Iso}(W),
\]

then for every pair \(c_1,c_2\),

\[
\begin{aligned}
\widetilde W_1(c_1,c_2)
&=
W(\pi_1(c_1),\pi_1(c_2))
\\
&=
W(\tau\pi_0(c_1),\tau\pi_0(c_2))
\\
&=
W(\pi_0(c_1),\pi_0(c_2))
\\
&=
\widetilde W_0(c_1,c_2).
\end{aligned}
\]

Therefore,

\[
\boxed{
\tau\in\operatorname{Iso}(W)
\;\Longrightarrow\;
F(\widetilde W_0)=F(\widetilde W_1)
}.
\]

This proposition establishes **blindness of the observable class**, not by itself a causal difference between contexts. The invariance is a case of standard symmetry/invariance mathematics. It becomes causal aliasing only when a difference in the underlying response fields is independently established, as done for the confirmatory counterexample in Section 2.2.

The proposition is deliberately restricted to observables that factor through the cell-weight field. Row-resolved, multiset-resolved, or full-pattern observables need not share the same blind set.

---

## 4.9 Exact characterization of the L1 metric blind route

The frozen two-bit channel intervention set makes the cell-weight condition exact.

Let the six independent off-diagonal entries of a context-specific geometry \(\widetilde W\) be

\[
\mathbf w
=
(w_{01},w_{02},w_{03},w_{12},w_{13},w_{23})^\top.
\]

The nine channel interventions occur in the order

\[
\varnothing,\;
b_0{:=}0,\;
b_0{:=}1,\;
b_1{:=}0,\;
b_1{:=}1,\;
c{:=}0,\;
c{:=}1,\;
c{:=}2,\;
c{:=}3.
\]

After division by the common multiplicity \(2^{n-5}\), their aggregate profile has the form

\[
(0,A,A,B,B,V_0,V_1,V_2,V_3),
\]

where

\[
A=w_{01}+w_{23},
\qquad
B=w_{02}+w_{13},
\]

and

\[
\begin{aligned}
V_0&=w_{01}+w_{02}+w_{03},\\
V_1&=w_{01}+w_{12}+w_{13},\\
V_2&=w_{02}+w_{12}+w_{23},\\
V_3&=w_{03}+w_{13}+w_{23}.
\end{aligned}
\]

Thus the six measured quantities
\(\mathbf s=(A,B,V_0,V_1,V_2,V_3)^\top\)
are related to \(\mathbf w\) by

\[
\mathbf s
=
L\mathbf w,
\]

with

\[
L=
\begin{pmatrix}
1&0&0&0&0&1\\
0&1&0&0&1&0\\
1&1&1&0&0&0\\
1&0&0&1&1&0\\
0&1&0&1&0&1\\
0&0&1&0&1&1
\end{pmatrix}.
\]

Direct calculation gives

\[
\operatorname{rank}(L)=6,
\qquad
\det L=-8.
\]

Hence \(L\) is invertible. Equality of the complete frozen cardinal profiles is therefore equivalent to equality of the context-specific cell-weight geometries:

\[
d_0=d_1
\quad\Longleftrightarrow\quad
\widetilde W_0=\widetilde W_1.
\]

The converse is non-trivial for this instrument because the nine interventions directly probe only two of the three perfect matchings on four channel symbols. The third matching is recovered indirectly through the four degree sums \(V_0,\ldots,V_3\). The two restricted sub-lattices examined in the analysis have ranks 2 and 4, respectively, and do not determine all six entries of \(\widetilde W\).

Finally, because

\[
\widetilde W_m(c_1,c_2)
=
W_M(\pi_m(c_1),\pi_m(c_2)),
\]

we have

\[
\widetilde W_0=\widetilde W_1
\quad\Longleftrightarrow\quad
\pi_1\pi_0^{-1}\in\operatorname{Iso}(W_M).
\]

Combining the two equivalences yields the exact characterization of the frozen **L1 metric blind route**:

\[
\boxed{
d_0=d_1
\quad\Longleftrightarrow\quad
\widetilde W_0=\widetilde W_1
\quad\Longleftrightarrow\quad
\tau\in\operatorname{Iso}(W_M)
}.
\]

This theorem is specific to L1. C1′ subsequently coarsens \(d_m\) to its weak-order representation, so equality of weak ranks can also occur when \(d_0\neq d_1\); that separate L2 ordinal route is treated in Section 4.10.

The invertibility of \(L\) is a determining-set property of the frozen intervention design and is not presented as a new general mathematical principle.

---

## Methods-stage boundary

Sections 4.10–4.15 are intentionally not drafted here. They will cover, in order:

- 4.10 L2 / alignment theorem;
- 4.11 strict-realization execution and witness extraction;
- 4.12 information-loss refinement hierarchy;
- 4.13 post-confirmatory prevalence study;
- 4.14 temporal-composition analysis;
- 4.15 internal verification, software environment, seeds, hashes, and reproducibility record.

`ARTICLE 1 — METHODS 4.1–4.9 v0.1 — READY FOR RED-TEAM`
