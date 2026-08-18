# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — coordenador Fase 6.
# coord_c_fresh_II.py — amostra fresca II, seed 910000050, N=400 aceites
# (precommit-coordinator.txt, analises a-j). Reexecucao critica de WS1/WS2/WS3/WS5.
import sys, json, hashlib, itertools, dataclasses, time
sys.path.insert(0, "/root/causal-A-postconfirmatory-analysis/frozen-copy")
import gerador as g, classificador as cl
import numpy as np

SEED = 910000050; NFAM = 400
t0 = time.time()

def pc2(v): return bin(v).count("1")
PC2 = [pc2(i) for i in range(4)]
S4 = list(itertools.permutations(range(4)))

def cyc(p):
    seen=set(); lens=[]
    for i in range(4):
        if i in seen: continue
        l=0; j=i
        while j not in seen: seen.add(j); j=p[j]; l+=1
        lens.append(l)
    return tuple(sorted(lens, reverse=True))

CLASSNAME = {(2,1,1):"T",(2,2):"DT",(3,1):"C3",(4,):"FC",(1,1,1,1):"id"}

def pairing_img(p, pairing):
    return frozenset(frozenset(p[a] for a in blk) for blk in pairing)
P_LO = frozenset([frozenset([0,1]), frozenset([2,3])])
P_HI = frozenset([frozenset([0,2]), frozenset([1,3])])
P_BL = frozenset([frozenset([0,3]), frozenset([1,2])])

# amostragem (loop do gerador)
rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(SEED).spawn(4)[0]))
fams = []
tent = 0
while len(fams) < NFAM:
    th = g.sample_theta_base(rng); tent += 1
    if th.pi[0] == th.pi[1]:
        continue
    if g.elegibilidade(th, False)[0]:
        fams.append((tent, th))

EDGES = (("B", dict(abits=[6,7], bbits=[3,4,5], mem=[5], rsh=3, csh=6)),
         ("A", dict(abits=[8,9], bbits=[0,1,2], mem=[2], rsh=0, csh=8)))

viol = {k: [] for k in ["formula","K_vs_L1","fingerprint","multiset","transporte",
                        "celula_L1","quantum64","L2_alinhada","L2_assinatura",
                        "M3_inconsistente","B4_em_L1"]}
cnt = {"L1":0,"L2":0,"L3":0}
cnt_edge = {"B":{"L1":0,"L2":0,"L3":0}, "A":{"L1":0,"L2":0,"L3":0}}
stages = {"F1":0,"F15":0,"F2":0,"dep0":0}
strict_cat = {"ESTRITO":0,"UNIAO":0,"PURO_CTF":0,"SEM_DEP":0}
strict_inst_ge1 = 0; strict_inst_both = 0; obs_dif_edges = 0
klass_stats = {}
colapsos = []
sumP_M3 = 0.0
trunc_counterex = 0   # arestas nao-L1 com DeltaA=DeltaB=0 (analise j)
L2_sig = []
iso_gt1 = 0; equid = 0
n_edges = 0

for tent_i, th in fams:
    tab, n, lay = g.tabela_transicao("II", th, False)
    T = np.asarray(tab, dtype=np.int64)
    s0 = g._campos_para_int(g.estado_inicial("II", th), lay)
    orb = cl.orbita(T, s0)
    p0 = list(th.pi[0]); p1 = list(th.pi[1])
    p0inv = [0]*4
    for i,v in enumerate(p0): p0inv[v] = i
    tau = tuple(p1[p0inv[i]] for i in range(4))
    tclass = CLASSNAME[cyc(tau)]
    lam = pairing_img(p0, P_BL)
    aligned = pairing_img(tau, lam) == lam
    fam_levels = {}
    fam_est = {}
    for ename, e in EDGES:
        n_edges += 1
        M = th.G0 if ename == "B" else th.F0
        # geometria W_M (frame imagem-de-pi) e Wtil_0 (frame canal)
        W = [[sum(PC2[M[r][p] ^ M[r][q]] for r in range(4)) for q in range(4)] for p in range(4)]
        Wt0 = [[W[p0[a]][p0[b]] for b in range(4)] for a in range(4)]
        Wt1 = [[W[p1[a]][p1[b]] for b in range(4)] for a in range(4)]
        isoW = [p for p in S4 if all(W[p[a]][p[b]] == W[a][b] for a in range(4) for b in range(4))]
        if len(isoW) > 1: iso_gt1 += 1
        if all(W[a][b] == W[0][1] for a in range(4) for b in range(4) if a != b): equid += 1
        K = all(W[tau[a]][tau[b]] == W[a][b] for a in range(4) for b in range(4))
        K2 = (Wt0 == Wt1)
        assert K == K2, "K por Iso != K por Wtil"
        # maquinaria congelada
        eB = cl.extractor(e["bbits"], n); popB = cl.popcount_tab(3)
        ints = cl.intervencoes(e["abits"])
        lo = e["abits"][0]
        subs = []  # sub_a local por intervencao
        for (mk,vl) in ints:
            subs.append([(((c << lo) & ~mk) | vl) >> lo for c in range(4)])
        ds = {}; Fs = {}
        for m in (0,1):
            Z = cl.estados_da_fibra(n, e["mem"], m)
            nx0 = eB[T[Z]]; F=[]; d=[]
            for (mk,vl) in ints:
                xr = eB[T[(Z & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
                F.append(xr); d.append(int(popB[xr].sum()))
            ds[m]=d; Fs[m]=F
        dep = sum(int(np.count_nonzero(Fs[0][ki] ^ Fs[1][ki])) for ki in range(9))
        # formula propria
        dhat = {}
        for m,pi in ((0,p0),(1,p1)):
            dhat[m] = [32*sum(W[pi[c]][pi[s[c]]] for c in range(4)) for s in subs]
        if dhat[0] != ds[0] or dhat[1] != ds[1]:
            viol["formula"].append((tent_i, ename))
        lvl = "L1" if ds[0]==ds[1] else ("L2" if cl.rank_canonico(ds[0])==cl.rank_canonico(ds[1]) else "L3")
        cnt[lvl] += 1; cnt_edge[ename][lvl] += 1
        fam_levels[ename] = lvl
        fam_est[ename] = (lvl != "L3")
        ks = klass_stats.setdefault(tclass, {"edges":0,"L1":0,"L2":0})
        ks["edges"] += 1
        if lvl in ("L1","L2"): ks[lvl] += 1
        if (K and lvl != "L1") or ((not K) and lvl == "L1"):
            viol["K_vs_L1"].append((tent_i, ename, K, lvl))
        # fingerprint + multiset + transporte
        for m in (0,1):
            d = ds[m]
            if not (d[0]==0 and d[1]==d[2] and d[3]==d[4]):
                viol["fingerprint"].append((tent_i, ename, m))
        if sorted(ds[0][5:9]) != sorted(ds[1][5:9]):
            viol["multiset"].append((tent_i, ename))
        # transporte: pares e V
        rho = tuple(p0inv[tau[p0[i]]] for i in range(4))  # rho = p0^-1 tau p0 = p0^-1 p1
        def S_pair(Wm, pairing):
            return sum(Wm[a][b] for blk in pairing for a,b in [sorted(blk)])
        pl_img = pairing_img(rho, P_LO); ph_img = pairing_img(rho, P_HI)
        expA = 32*S_pair(Wt0, pl_img); expB_ = 32*S_pair(Wt0, ph_img)
        V0 = [sum(Wt0[c][gm] for c in range(4)) for gm in range(4)]
        okT = (ds[1][1] == expA and ds[1][3] == expB_ and
               all(ds[1][5+gm] == 32*V0[rho[gm]] for gm in range(4)))
        if not okT:
            viol["transporte"].append((tent_i, ename))
        # celulas por (k,c): somas e estagios (a partir de theta)
        if lvl == "L1" and dep > 0:
            stage = "F1"
            for ki in range(1,9):
                for c in range(4):
                    q0 = [PC2[M[r][p0[c]] ^ M[r][p0[subs[ki][c]]]] for r in range(4)]
                    q1 = [PC2[M[r][p1[c]] ^ M[r][p1[subs[ki][c]]]] for r in range(4)]
                    if sum(q0) != sum(q1):
                        viol["B4_em_L1"].append((tent_i, ename, ki, c)); stage = "F2"
                    elif sorted(q0) != sorted(q1):
                        stage = "F2"
                    elif q0 != q1 and stage == "F1":
                        stage = "F15"
            stages[{"F1":"F1","F15":"F15","F2":"F2"}[stage]] += 1
        elif lvl == "L1":
            stages["dep0"] += 1
        # quantum 64
        for i9 in range(9):
            dd = abs(ds[0][i9]-ds[1][i9])
            if dd % 64 != 0:
                viol["quantum64"].append((tent_i, ename, i9, dd))
        # alinhamento / L2
        if lvl == "L2":
            if aligned:
                viol["L2_alinhada"].append((tent_i, ename, tclass))
            changed = [i9 for i9 in range(9) if ds[0][i9] != ds[1][i9]]
            S1s = 32*S_pair(Wt0, P_LO); S2s = 32*S_pair(Wt0, P_HI); S3s = 32*S_pair(Wt0, P_BL)
            sig_ok = None
            if tclass in ("T","FC"):
                pair = None
                if changed == [1,2]: pair = ("P1", ds[1][1])
                elif changed == [3,4]: pair = ("P2", ds[1][3])
                sig_ok = (pair is not None) and (pair[1] == S3s)
            elif tclass == "C3":
                sig_ok = (changed == [1,2,3,4])
            L2_sig.append({"tent": tent_i, "aresta": ename, "classe": tclass,
                           "mudadas": changed, "novo_par_valor": ds[1][1] if changed[:2]==[1,2] else ds[1][3] if changed[:2]==[3,4] else None,
                           "S_lam_x32": S3s, "assinatura_ok": bool(sig_ok)})
            if sig_ok is False:
                viol["L2_assinatura"].append((tent_i, ename))
        # contra-exemplo lattice truncado (analise j)
        if lvl != "L1" and ds[0][1]==ds[1][1] and ds[0][3]==ds[1][3]:
            trunc_counterex += 1
        # realizacao estrita (r,c)
        Cm = {0:set(), 1:set()}
        for z in orb:
            mz = (z >> e["mem"][0]) & 1
            Cm[mz].add(((z >> e["rsh"]) & 3, (z >> e["csh"]) & 3))
        I = Cm[0] & Cm[1]; U = Cm[0] | Cm[1]
        def patt(m, pi, ki, r, c):
            return M[r][pi[c]] ^ M[r][pi[subs[ki][c]]]
        nstrict = sum(1 for ki in range(1,9) for (r,c) in I
                      if patt(0,p0,ki,r,c) != patt(1,p1,ki,r,c))
        nunion = sum(1 for ki in range(1,9) for (r,c) in U
                     if patt(0,p0,ki,r,c) != patt(1,p1,ki,r,c))
        if nstrict > 0: cat = "ESTRITO"
        elif nunion > 0: cat = "UNIAO"
        elif dep > 0: cat = "PURO_CTF"
        else: cat = "SEM_DEP"
        strict_cat[cat] += 1
        fam_est.setdefault("_strict", []).append(cat == "ESTRITO")
        # testemunha observacional
        obsd = False
        for r in range(4):
            cs = sorted(c for (rr,c) in I if rr == r)
            for c1, c2 in itertools.combinations(cs, 2):
                if (M[r][p0[c1]] ^ M[r][p0[c2]]) != (M[r][p1[c1]] ^ M[r][p1[c2]]):
                    obsd = True; break
            if obsd: break
        if obsd: obs_dif_edges += 1
    stt = fam_est.pop("_strict")
    if any(stt): strict_inst_ge1 += 1
    if all(stt): strict_inst_both += 1
    colapso_obs = fam_est["B"] and fam_est["A"]
    if colapso_obs:
        colapsos.append({"tent": tent_i, "niveis": fam_levels, "classe_tau": tclass, "alinhada": bool(aligned)})
    # M3: enumeracao dos 23 pi1'
    eq_both = 0
    rank0 = {}
    for ename, e in EDGES:
        M = th.G0 if ename == "B" else th.F0
        W = [[sum(PC2[M[r][p] ^ M[r][q]] for r in range(4)) for q in range(4)] for p in range(4)]
        lo = e["abits"][0]
        ints = cl.intervencoes(e["abits"])
        subs = [[(((c << lo) & ~mk) | vl) >> lo for c in range(4)] for (mk,vl) in ints]
        prof0 = [sum(W[p0[c]][p0[s[c]]] for c in range(4)) for s in subs]
        rank0[ename] = (cl.rank_canonico(prof0), W, subs)
    pred_actual = None
    for p1c in S4:
        if list(p1c) == p0: continue
        both = True
        for ename in ("B","A"):
            r0, W, subs = rank0[ename]
            prof1 = [sum(W[p1c[c]][p1c[s[c]]] for c in range(4)) for s in subs]
            if cl.rank_canonico(prof1) != r0:
                both = False; break
        eq_both += 1 if both else 0
        if list(p1c) == p1:
            pred_actual = both
    sumP_M3 += eq_both / 23.0
    if pred_actual != colapso_obs:
        viol["M3_inconsistente"].append((tent_i, pred_actual, colapso_obs))

out = {
 "rotulo": "POST-CONFIRMATORY / EXPLORATORY", "script": "coord_c_fresh_II.py",
 "seed": SEED, "N_aceites": NFAM, "tentativas": tent, "n_arestas": n_edges,
 "duracao_s": round(time.time()-t0, 1),
 "niveis": cnt, "niveis_por_aresta": cnt_edge,
 "K_vs_L1_excepcoes": len(viol["K_vs_L1"]),
 "violacoes": {k: len(v) for k, v in viol.items()},
 "violacoes_detalhe": {k: v[:5] for k, v in viol.items() if v},
 "estagios_L1": stages,
 "estagios_fraccoes_dep>0": {k: round(stages[k]/max(1,(stages['F1']+stages['F15']+stages['F2'])),3)
                              for k in ("F1","F15","F2")},
 "estrito": {"cat": strict_cat,
             "fraccao_ESTRITO": round(strict_cat["ESTRITO"]/n_edges, 4),
             "inst_ge1": strict_inst_ge1, "inst_both": strict_inst_both},
 "obs_testemunha_diferente_arestas": obs_dif_edges,
 "classes_tau": {k: {"arestas": v["edges"], "L1": v["L1"], "L2": v["L2"],
                     "taxa_L1": round(v["L1"]/v["edges"], 4)} for k, v in klass_stats.items()},
 "colapsos_observados": len(colapsos), "colapsos": colapsos,
 "M3_soma_prob": round(sumP_M3, 3),
 "L2_assinaturas": L2_sig,
 "lattice_truncado_contraexemplos_naoL1_com_dA=dB=0": trunc_counterex,
 "iso_gt1_arestas": iso_gt1, "equidistantes": equid,
}
print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
