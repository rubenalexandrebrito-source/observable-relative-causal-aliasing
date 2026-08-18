# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — coordenador Fase 6.
# coord_d_fresh_III.py — amostra fresca III, seed 910000051, N=250 aceites
# (precommit-coordinator.txt, analises k-m). Reexecucao critica de WS4.
import sys, json, time
sys.path.insert(0, "/root/causal-A-postconfirmatory-analysis/frozen-copy")
import gerador as g, classificador as cl
import numpy as np

SEED = 910000051; NFAM = 250
t0 = time.time()
def pc2(v): return bin(v).count("1")
PC2 = [pc2(i) for i in range(4)]

rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(SEED).spawn(4)[0]))
fams = []; tent = 0
while len(fams) < NFAM:
    th = g.sample_theta_base(rng); tent += 1
    if th.pi[0] == th.pi[1]:
        continue
    if g.elegibilidade(th, False)[0]:
        fams.append((tent, th))

EDGES = (("B", dict(abits=[6,7], bbits=[3,4,5], mem=[5])),
         ("A", dict(abits=[8,9], bbits=[0,1,2], mem=[2])))

h1_dep_pos = 0; h1_dneq = 0; h1_formula_bad = 0
h2_dep_pos = 0; h2_lvls = {"L1":0,"L2":0,"L3":0}
h2_zeros = []
n_edges = 0
dep2_vals = []

for tent_i, th in fams:
    tab, n, lay = g.tabela_transicao("III", th, False)
    T = np.asarray(tab, dtype=np.int64)
    T2 = T[T]  # T o T
    for ename, e in EDGES:
        n_edges += 1
        M = th.G0 if ename == "B" else th.F0
        Ktab = th.K if ename == "B" else th.H
        eB = cl.extractor(e["bbits"], n); popB = cl.popcount_tab(3)
        ints = cl.intervencoes(e["abits"])
        lo = e["abits"][0]
        subs = [[(((c << lo) & ~mk) | vl) >> lo for c in range(4)] for (mk,vl) in ints]
        # ---- h1 ----
        ds = {}; Fs = {}
        for m in (0,1):
            Z = cl.estados_da_fibra(n, e["mem"], m)
            nx0 = eB[T[Z]]; F=[]; d=[]
            for (mk,vl) in ints:
                xr = eB[T[(Z & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
                F.append(xr); d.append(int(popB[xr].sum()))
            ds[m]=d; Fs[m]=F
        dep = sum(int(np.count_nonzero(Fs[0][ki] ^ Fs[1][ki])) for ki in range(9))
        if dep > 0: h1_dep_pos += 1
        if ds[0] != ds[1]: h1_dneq += 1
        Wm = [[sum(PC2[M[r][p] ^ M[r][q]] for r in range(4)) for q in range(4)] for p in range(4)]
        dh = [32*sum(Wm[c][s[c]] for c in range(4)) for s in subs]
        if dh != ds[0] or dh != ds[1]: h1_formula_bad += 1
        # ---- h2 (T o T) ----
        d2 = {}; F2 = {}
        for m in (0,1):
            Z = cl.estados_da_fibra(n, e["mem"], m)
            nx0 = eB[T2[Z]]; F=[]; d=[]
            for (mk,vl) in ints:
                xr = eB[T2[(Z & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
                F.append(xr); d.append(int(popB[xr].sum()))
            d2[m]=d; F2[m]=F
        dep2 = sum(int(np.count_nonzero(F2[0][ki] ^ F2[1][ki])) for ki in range(9))
        dep2_vals.append(dep2)
        if dep2 > 0: h2_dep_pos += 1
        lvl2 = "L1" if d2[0]==d2[1] else ("L2" if cl.rank_canonico(d2[0])==cl.rank_canonico(d2[1]) else "L3")
        h2_lvls[lvl2] += 1
        if dep2 == 0:
            mem_rows_dif = sum(1 for w in range(4) if Ktab[0][w] != Ktab[1][w])
            h2_zeros.append({"tent": tent_i, "aresta": ename, "nivel2": lvl2,
                             "mem_rows_dif": mem_rows_dif})

dep2_vals.sort()
out = {
 "rotulo": "POST-CONFIRMATORY / EXPLORATORY", "script": "coord_d_fresh_III.py",
 "seed": SEED, "N_aceites": NFAM, "tentativas": tent, "n_arestas": n_edges,
 "duracao_s": round(time.time()-t0, 1),
 "h1": {"arestas_dep>0": h1_dep_pos, "arestas_d0!=d1": h1_dneq,
        "formula_divergencias": h1_formula_bad,
        "teorema_III1": "OK" if (h1_dep_pos==0 and h1_dneq==0 and h1_formula_bad==0) else "VIOLADO"},
 "h2": {"arestas_dep2>0": h2_dep_pos, "fraccao": round(h2_dep_pos/n_edges, 4),
        "niveis2": h2_lvls,
        "dep2_mediana": dep2_vals[len(dep2_vals)//2], "dep2_max": dep2_vals[-1],
        "dep2_min_nao_nulo": next((v for v in dep2_vals if v > 0), None),
        "zeros": h2_zeros},
}
print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
