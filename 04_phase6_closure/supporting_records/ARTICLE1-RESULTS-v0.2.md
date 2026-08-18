# ARTICLE 1 — RESULTS — v0.2

**Status:** post-red-team manuscript draft derived from frozen Article Architecture v2.1 and Claim–Evidence Ledger v1.1  
**Date:** 17 August 2026  
**Scope:** Results 2.1–2.8 only. Temporal-composition result (P7 / III-2) and the M3 edge-correlation model are intentionally held for Extended Results/Supplement at this stage.

---

# 2. Results

## 2.1 The preregistered evaluation is negative

We preregistered a blinded confirmatory evaluation of causal-individuation candidates on synthetic systems assigned by construction to prespecified operational interaction classes. The final frozen v8.3 executable instrument scored C1′, C2, and C3. C1′ and C2 were the candidates capable of making the scientific hypothesis \(H_A\) positive; C3 was an implementation canary and did not enter \(H_A\). No C4 path was executable or scored in the frozen confirmatory instrument.

The confirmatory outcome was negative. For C1′, all 150 E1 instances matched their preregistered targets, whereas 49 of 50 E2 instances did so. Thus C1′ yielded 199/200 target matches overall, but failed the preregistered conjunctive success requirement because E2 was not perfect. The official result therefore remained `passa = false`; the numerical proportion is not interpreted as a near-positive result. C2 disagreed with its preregistered target in 74/200 instances, and C3 in 75/200. Both also disagreed on the instance that produced the single C1′ error. C2 and C3 are reported for completeness but were not subjected to the mechanistic post-confirmatory autopsy developed below.

The single C1′ confirmatory counterexample was instance `7bb0baab3a8ed7aa`, family 20, a System-II instance in E2/Stratum 2. C1′ fused the core \(\{A,B,C_{AB},C_{BA}\}\) into one strongly connected STATE component, producing the operational partition associated with System III rather than the preregistered System-II target. This classification was a genuine confirmatory error under the frozen target and was not altered after scoring.

All analyses from this point onward are post-confirmatory. They were performed after the official result had been closed, without changing the criterion, targets, thresholds, scoring, or confirmatory artifacts. No replacement criterion C1″ was formulated. The question addressed by the autopsy was therefore explanatory rather than corrective: **why did C1′ fail on a system constructed under the preregistered System-II target?**

**[Figure 1 near here: preregistered target, blind workflow, complete confirmatory scoring, and the conjunctive reason the result is NEGATIVE.]**

---

## 2.2 The C1′ counterexample contains a real, strictly realized causal difference

A first possibility was that the System-II construction differed from System III only architecturally, while the causal distinction required by the target was absent from the realized dynamics of family 20. The post-confirmatory analysis rejected this explanation.

For each of the two decisive channel-to-processor edges, \(C_{AB}\!\to B\) and \(C_{BA}\!\to A\), the full interventional response field contained 4,608 sites whose response depended on receiver memory. Both memory contexts were reached in the realized orbit: the orbit contained 15 versus 10 states for the two \(B\)-memory contexts on \(C_{AB}\!\to B\), and 12 versus 13 states for the two \(A\)-memory contexts on \(C_{BA}\!\to A\). Thus the memory contexts responsible for the comparison were not inaccessible counterfactual states.

To ask whether the difference occurred in causally comparable states actually visited under both contexts, we used the local state \((r,c)\), where \(r\) is the receiver's non-memory processor state and \(c\) is the channel value. Conditional on receiver memory, the one-step interventional response is a function only of \((r,c)\). Consequently, \((r,c)\) is a causally sufficient local-state granularity for this contrast: refining it with globally irrelevant bits can remove overlap between contexts without changing the response being compared, whereas coarsening it would merge locally distinct responses.

At this granularity, both decisive edges contained strictly realized memory-dependent differences. For \(C_{AB}\!\to B\), four \((r,c)\) cells were visited under both receiver-memory contexts and nine intervention-by-cell sites differed across those contexts. For \(C_{BA}\!\to A\), five shared cells likewise contained nine differing sites. The result did not rely on full global configurations being identical across contexts.

The distinction was also visible using realized transitions alone. On each decisive edge, pairs of realized transitions with matched local receiver state yielded different observational contrasts across memory contexts. Therefore, the C1′ collapse cannot be explained by an absence of realized separating causal information. A causal difference existed below the aggregate that C1′ used.

This establishes the empirical premise required for the interpretation below. Equality of an observable is only **blindness**. It becomes **causal aliasing** only when an underlying causal difference has independently been shown to exist. Family 20 satisfies this stronger condition, including at the causally sufficient local-state granularity.

**[Figure 2 near here: family-20 ring, realized orbit, \((r,c)\) comparability, and strict/observational witnesses.]**

---

## 2.3 Receiver state induces a contextual pull-back of the response field

The failure can be reduced analytically to how receiver memory enters the frozen one-step channel-to-processor contrast under the aligned full-fiber comparison. For the relevant System-II dynamics, the receiver response can be written in the form

\[
M[r][\pi_m(c)] \oplus \sigma[m],
\]

where \(m\in\{0,1\}\) is receiver memory, \(r\) is the receiver's non-memory processor state, \(c\) is the channel symbol, \(\pi_m\) is a memory-dependent relabeling of the interface, and \(\sigma[m]\) is an additive context term.

For an intervention \(a\) that replaces \(c\) by \(\mathrm{sub}_a(c)\), the XOR response contrast is therefore

\[
X_m(a;r,c)
=
M[r][\pi_m(c)]
\oplus
M[r][\pi_m(\mathrm{sub}_a(c))],
\]

with \(M=G_0\) for \(C_{AB}\!\to B\) and \(M=F_0\) for \(C_{BA}\!\to A\). The additive term \(\sigma[m]\) cancels from the XOR contrast. The receiver-memory update is independent of the intervened channel at the current step and consequently does not contribute to the one-step response difference. Memory nevertheless remains causally relevant because it changes the interface relabeling \(\pi_m\).

For this one-step contrast, the two memory contexts are therefore pull-backs of a common response mechanism under different relabelings of the same finite interface. Their relative transport is

\[
\tau = \pi_1\circ\pi_0^{-1}.
\]

This is the key structural reduction. The relevant question is no longer simply whether memory changes the pointwise response—it does in family 20—but whether the observable used by C1′ is sensitive to the particular relabeling induced by that memory change.

---

## 2.4 Mechanism-dependent symmetry creates metric blindness

Define the pairwise response geometry induced by receiver mechanism \(M\) as

\[
W_M(p,q)
=
\sum_r
\operatorname{pc}_2
\left(
M[r][p]\oplus M[r][q]
\right),
\]

where \(\operatorname{pc}_2\) is the Hamming popcount on the two-bit response. Receiver memory acts on this geometry by relabeling its arguments through \(\pi_m\).

This yields a class-level blindness proposition under the comparison conditions used here. Suppose two aligned contextual response fields are pull-backs of the same finite response tensor under relabelings \(\pi_0\) and \(\pi_1\), and suppose the observable factors through the cell-weight geometry induced by that response tensor. If the relative relabeling

\[
\tau=\pi_1\circ\pi_0^{-1}
\]

is an isometry of that geometry,

\[
\tau\in \operatorname{Iso}(W_M),
\]

then the observable is invariant across the two contexts. This is a symmetry statement about the representation measured by the observable; by itself it does not establish that the underlying fields differ.

A minimal post-confirmatory toy illustrates the logical distinction between blindness and causal equality without relying on the confirmatory generator. Let \(C=\{0,1,2\}\), with two receiver rows and one-bit outputs,
\[
M[0]=(0,0,1),\qquad M[1]=(0,1,0),
\]
and let \(\pi_0=\mathrm{id}\), \(\pi_1=(12)\). The induced geometry has
\[
W(0,1)=1,\qquad W(0,2)=1,\qquad W(1,2)=2,
\]
so \(\operatorname{Iso}(W)=\{\mathrm{id},(12)\}\) and the relative transport \(\tau=(12)\) is the non-trivial isometry. Nevertheless, the pointwise response fields differ—for example, one matched intervention/site changes from response pattern \((0,1)\) to \((1,0)\)—while the aggregate profiles are identical:
\[
d_0=d_1=(2,3,3).
\]
The toy is illustrative only; it is not confirmatory evidence and does not establish realized dynamics for family 20.

Family 20 supplies the confirmatory counterexample in which the same logical structure coexists with an independently established, strictly realized causal difference. On \(C_{BA}\!\to A\), all off-diagonal distances in \(W_M\) equal 4, so

\[
\operatorname{Iso}(W_M)=S_4.
\]

Every permutation of the four interface symbols is therefore invisible at this geometric level. On \(C_{AB}\!\to B\),

\[
W_M=
\begin{pmatrix}
0&4&5&5\\
4&0&3&3\\
5&3&0&4\\
5&3&4&0
\end{pmatrix},
\]

for which

\[
\operatorname{Iso}(W_M)=\{\mathrm{id},(23)\}.
\]

The relative transport realized by family 20 is exactly the non-trivial transposition \((23)\). Thus the same contextual transport lies in the isometry group of both decisive receiver geometries: trivially on the equidistant edge and selectively on the second edge. Yet Section 2.2 established that the underlying pointwise response fields differ and that those differences are strictly realized.

Family 20 therefore realizes **observable-relative causal aliasing**: a receiver-state-dependent causal modulation is present, but the relabeling through which it acts lies inside a symmetry of the mechanism-dependent response geometry retained by the aggregate.

**[Figure 3A/C near here: \(m\to\pi_m\to\tau\to W_M\), the two family-20 geometries, and \(\tau=(23)\).]**

---

## 2.5 The frozen intervention set makes the metric blind route exact

The symmetry condition is not only sufficient for metric blindness in the frozen instrument. The nine-intervention lattice is determining for the six independent entries of the induced pairwise geometry.

Let

\[
\widetilde W_m(c_1,c_2)
=
W_M(\pi_m(c_1),\pi_m(c_2)).
\]

For the frozen statistic,

\[
d_m(a)
=
2^{n-5}
\sum_c
\widetilde W_m\!\left(c,\mathrm{sub}_a(c)\right).
\]

Equivalently, after factoring out the common multiplicity, the nine-component profile has the structural form

\[
d
=
2^{n-5}(0,A,A,B,B,V),
\]

where \(V=(V_0,V_1,V_2,V_3)\) denotes the four row-sum components; together with the two bit-intervention pairing sums, these provide six independent measured degrees of freedom. The resulting linear map between \(\widetilde W_m\) and \(d_m\) is invertible. The full system has rank 6 and determinant \(-8\); the two restricted intervention sub-lattices examined have ranks 2 and 4 and do not support the converse.

Consequently, for the frozen determining intervention set,

\[
\boxed{
d_0=d_1
\iff
\widetilde W_0=\widetilde W_1
\iff
\tau\in\operatorname{Iso}(W_M)
}
\]

for the relevant channel-to-processor edges.

We call this equality event **L1**, or the metric blind route. The result is exact for this instrument: once the response has been reduced to \(\widetilde W\), the map from \(\widetilde W\) to \(d\) introduces no additional L1 information loss. The theorem does **not** characterize every STATE decision made by C1′, because C1′ subsequently replaces cardinal profiles by their weak order. That second route is addressed next.

---

## 2.6 Beyond exact isometry: C1′ has an additional ordinal blind route

C1′ does not compare \(d_0\) and \(d_1\) directly. It assigns the relevant edge to STATE when their canonical weak ranks coincide. This yields two distinct cases:

\[
\text{L1}: d_0=d_1,
\]

and

\[
\text{L2}: d_0\neq d_1
\quad\text{but}\quad
\operatorname{rank}(d_0)=\operatorname{rank}(d_1).
\]

Both produce the same STATE edge label under C1′. An instance-level System-II collapse requires both decisive channel-to-processor edges to receive that label, with either edge allowed to reach it through L1 or L2.

L2 is not a weakened version of the exact isometry condition. In the primary 10,000-family population, 225 of 20,000 decisive edges were L2. Among the 24 L2 edges contained in the 46 total-collapse instances, 17 had a trivial exact isometry group \(\operatorname{Iso}(W_M)\). Their cardinal profiles changed; what remained invariant was the weak-order representation consumed by C1′.

The ordinal blind zone can nevertheless be characterized relative to the frozen intervention geometry. The four interface symbols have three perfect matchings, while the bit interventions directly probe only two. Let

\[
\psi:S_4\rightarrow S_3
\]

be the action of interface relabelings on those three matchings, with kernel \(V_4\), and let \(\lambda\) denote the unprobed matching. If \(\psi(\tau)\) fixes \(\lambda\), L2 is impossible on that edge: any C1′ STATE event in the aligned cell must already be L1. L2 is therefore restricted to misaligned cells in which the contextual transport can move the unprobed pairing into a measured position while preserving the resulting weak order.

The predicted signature was observed in all 225 L2 edges of the primary population: exactly one duplicated probed-pairing sum changed, while the full-intervention \(do(c=\gamma)\) block remained pointwise unchanged. This is an instrument-specific ordinal aliasing mechanism; it is distinct from exact metric isometry and should not be interpreted as a new general group-theoretic result.

**[Figure 3B near here: separate L1 and L2 paths to the same C1′ STATE label.]**

---

## 2.7 The blind set shrinks under observable refinement

The family-20 failure is not an intrinsic absence of identifying information. It emerges along a sequence of representations, several of which are many-to-one. For the frozen contrast, the relevant chain is

\[
\text{full response pattern}
\rightarrow
\text{pointwise popcount}
\rightarrow
\text{row-resolved field}
\rightarrow
\text{within-block multiset}
\rightarrow
\widetilde W
\rightarrow
d
\rightarrow
\text{weak rank}.
\]

The \(\widetilde W\to d\) step is an exception to the lossy stages in this chain: for the frozen nine-intervention lattice it is bijective, as shown in Section 2.5.

The L1 route can be localized more precisely. Equality of \(d_0\) and \(d_1\) is already equality of \(\widetilde W_0\) and \(\widetilde W_1\); L1 is not produced by cancellation between different measured blocks. Across 22,560 non-null blocks from the studied L1 edges, 0 required cross-block compensation. Metric blindness is therefore resolved locally within the aggregation cells.

The information can disappear at several earlier stages. Among the 698 L1 edges that retained pointwise dependence, 29 (4.2%) became indistinguishable already at pointwise popcount, 174 (24.9%) became indistinguishable when response locations were discarded but within-block multisets were retained, and 495 (70.9%) required strict within-cell arithmetic aggregation: the response multisets differed while their sums agreed. Family 20 lies in this last, dominant mode on both decisive edges.

The same result can be expressed as a hierarchy of blind sets under progressively coarser observables. In the studied 20,000 System-II decisive edges,

\[
B_{\mathrm{pattern}}
\subset
B_{\mathrm{row}}
\subset
B_{\mathrm{multiset}}
\subset
B_W,
\]

with observed cardinalities

\[
7
\subset
36
\subset
210
\subset
705.
\]

The nesting expresses the refinement relation; the numerical cardinalities are properties of the frozen generator population, not universal constants. The central implication is that finer observables can strictly recover distinctions lost by coarser ones. The demonstrated blindness is therefore **observable-relative**. It does not imply that the underlying causal system is non-identifiable from all available causal information.

**[Figure 4A near here: nested blind sets and the location of family 20 in the within-cell arithmetic-cancellation mode.]**

---

## 2.8 Population scope under the frozen generator

To assess whether family 20 recurred within the frozen generator, we conducted a post-confirmatory prevalence study in which two System-II batches were precommitted before their own generation and analysis. Together they comprised 10,000 eligible families and 20,000 decisive channel-to-processor edges. At the edge level, 705/20,000 (3.53%) were L1, 225/20,000 (1.13%) were L2, and 19,070/20,000 (95.35%) were L3, in which the weak rank changed across receiver-memory contexts. Point-to-point memory dependence was present in 19,993/20,000 edges.

At the instance level, total C1′ collapse occurred in 46/10,000 System-II families,

\[
0.46\%,
\]

with an approximate 95% confidence interval of 0.345%–0.613%. The 46 collapses comprised 29 L1/L1 instances, 10 mixed L1/L2 instances, and 7 L2/L2 instances. Thus exact metric blindness was the modal route, but ordinal aliasing contributed materially to the complete failure class.

Additional precommitted or internally reproduced batches yielded collapse estimates of the same order, approximately 0.32%–0.50% under the frozen generator. These data support recurrence of the mechanism within that generator family; they are not an estimate of a natural or universal frequency, and the internal reproductions do not constitute external scientific replication.

Family 20 is not a separate mechanistic class within this population. It belongs to the modal L1/L1 subtype: one decisive edge has a maximally symmetric equidistant geometry, while the other has a smaller isometry group containing exactly the realized transport. The more detailed correlation analysis between the two decisive edges is reserved for Extended Results/Supplement.

Taken together, the confirmatory counterexample and the population analysis support a bounded conclusion. The preregistered criterion failed. Post-confirmatory analysis showed that one edge-level blind route contributing to that failure is exactly characterized by a receiver-state-dependent relabeling falling inside a symmetry of the receiver's response geometry; a second route arises from ordinal coarsening. In the confirmatory counterexample, the resulting invariance hid a causal difference that remained present in realized local dynamics. The frequency with which these routes occur outside the frozen synthetic generator remains an open empirical question.

**[Figure 4B/C near here: L1/L2/L3 population structure, 46/10,000 collapse subtypes, and generator-specific robustness across batches.]**

---

## Results-stage boundary

The temporal-composition findings for System III (\(h=1\) exact null; failure of the first-order cancellation to generally iterate under \(T^2\); 3996/4000 empirical \(h=2\) dependence) are deliberately excluded from the main Results draft at this stage. Under the frozen article architecture, they remain an Extended Results/Supplementary result unless their inclusion is later shown to improve the interpretation of the central P3/P4 mechanism without broadening the paper's headline claim.

