# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — coordenador Fase 6.
# coord_b_fam20.py:
#  Parte 1 — instancia confirmatoria 7bb0baab3a8ed7aa (copia read-only + chave
#  aberta na Fase 5): despermutacao, d/dep, Wtil, Iso, transporte rho', sitios
#  estritos (r,c), testemunha observacional, fusao via cl.classificar.
#  Parte 2 — replay do lote registado 910000001 ate a tentativa 14155
#  (reconciliacao fam4159 <-> t14155 e verificacao dep=0/V-constante/DT).
# Nenhuma semente nova; nenhuma semente confirmatoria; escrita apenas em stdout.
import sys, json, hashlib, itertools, dataclasses
sys.path.insert(0, "/root/causal-A-postconfirmatory-analysis/frozen-copy")
import gerador as g, classificador as cl, pontuacao as pt
import numpy as np

OUT = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY", "script": "coord_b_fam20.py"}
base = "/root/causal-A-postconfirmatory-analysis"

def pc2(v): return bin(v).count("1")

def iso_group(W):
    return [p for p in itertools.permutations(range(4))
            if all(W[p[a]][p[b]] == W[a][b] for a in range(4) for b in range(4))]

# ============ Parte 1: instancia confirmatoria ============
iid = "7bb0baab3a8ed7aa"
inst = json.load(open(f"{base}/conf-e2/instancias/{iid}.json"))
chave = json.load(open(f"{base}/chave-e2.json"))
k = chave[iid]
assert k["variante"] == "II"
n = inst["n"]; perm = k["perm"]
OUT["fam20"] = {"familia": k["familia"], "n": n, "tipos": pt._tipos_e2(k)}

def unexport(v):
    s = 0
    for i in range(n):
        s |= ((v >> perm[i]) & 1) << i
    return s
def export(v):
    s = 0
    for i in range(n):
        s |= ((v >> i) & 1) << perm[i]
    return s

tab_exp = inst["transicao"]
tab = np.zeros(1 << n, dtype=np.int64)
for s_int in range(1 << n):
    tab[s_int] = unexport(tab_exp[export(s_int)])
s0 = unexport(inst["estado_inicial"])
orb = cl.orbita(tab, s0)
OUT["fam20"]["orbita"] = len(orb)  # esperado 25

# modulos canonicos II/E2: A=[0,1,2](mem 2), B=[3,4,5](mem 5), C_AB=[6,7], C_BA=[8,9], D=[10],[11]
edges = {
  "C_AB->B": dict(abits=[6,7], bbits=[3,4,5], mem=[5], rshift=3, cshift=6),
  "C_BA->A": dict(abits=[8,9], bbits=[0,1,2], mem=[2], rshift=0, cshift=8),
}
esperado_d = {
  "C_AB->B": [0,1024,1024,1024,1024,1792,1280,1536,1536],
  "C_BA->A": [0,1024,1024,1024,1024,1536,1536,1536,1536],
}
res_edges = {}
for nome, e in edges.items():
    eB = cl.extractor(e["bbits"], n); popB = cl.popcount_tab(len(e["bbits"]))
    ints = cl.intervencoes(e["abits"])
    fields = {}; ds = {}
    for m in (0,1):
        Z = cl.estados_da_fibra(n, e["mem"], m)
        nx0 = eB[tab[Z]]
        F = []; d = []
        for (mk,vl) in ints:
            xr = eB[tab[(Z & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
            F.append(xr); d.append(int(popB[xr].sum()))
        fields[m] = F; ds[m] = d
        # coords das fibras
        if m == 0:
            rv = ((Z >> e["rshift"]) & 3); cv = ((Z >> e["cshift"]) & 3)
    dep = 0
    # constancia por celula (k,(r,c)) e Phi bem definida
    const_ok = True
    pat = {0: {}, 1: {}}
    for ki in range(9):
        for m in (0,1):
            for cell in range(16):
                r_, c_ = cell >> 2, cell & 3
                selv = fields[m][ki][(rv == r_) & (cv == c_)]
                if selv.size and not np.all(selv == selv[0]):
                    const_ok = False
                pat[m][(ki, r_, c_)] = int(selv[0]) if selv.size else None
        dep += int(np.count_nonzero(fields[0][ki] ^ fields[1][ki]))
    # Wtil por contexto a partir de Phi (parte-y dos padroes do(c=g))
    # Phi_m(r,c) = parte nao-memoria de eB no proximo estado, extraida da tabela:
    Phi = {}
    for m in (0,1):
        Zm = cl.estados_da_fibra(n, e["mem"], m)
        nxt = eB[tab[Zm]]
        ph = {}
        for cell in range(16):
            r_, c_ = cell >> 2, cell & 3
            selv = nxt[( ((Zm >> e["rshift"]) & 3) == r_) & (((Zm >> e["cshift"]) & 3) == c_)]
            vals = set(int(x) & 3 for x in selv)  # parte nao-memoria (2 bits baixos do extractor)
            ph[(r_, c_)] = vals
        Phi[m] = ph
    phi_bem_def = all(len(v) == 1 for m in (0,1) for v in Phi[m].values())
    phi0 = {kk: next(iter(v)) for kk, v in Phi[0].items()}
    phi1 = {kk: next(iter(v)) for kk, v in Phi[1].items()}
    def wtil(phi):
        return [[sum(pc2(phi[(r_, c1)] ^ phi[(r_, c2)]) for r_ in range(4)) for c2 in range(4)] for c1 in range(4)]
    W0 = wtil(phi0); W1 = wtil(phi1)
    isoW = iso_group(W0)
    # transporte: Phi1(r,c) == Phi0(r,rho c) ^ delta ?
    rhos = []
    for p in itertools.permutations(range(4)):
        ds_ = {phi1[(r_, c_)] ^ phi0[(r_, p[c_])] for r_ in range(4) for c_ in range(4)}
        if len(ds_) == 1:
            rhos.append({"rho": list(p), "delta": ds_.pop()})
    # classe de ciclo de rho
    def cyc(p):
        seen = set(); lens = []
        for i in range(4):
            if i in seen: continue
            l = 0; j = i
            while j not in seen:
                seen.add(j); j = p[j]; l += 1
            lens.append(l)
        return tuple(sorted(lens, reverse=True))
    V0 = [sum(W0[w][c] for c in range(4)) for w in range(4)]
    # sitios estritos (r,c) na orbita
    Cm = {0: set(), 1: set()}
    for z in orb:
        m = (z >> e["mem"][0]) & 1
        Cm[m].add(((z >> e["rshift"]) & 3, (z >> e["cshift"]) & 3))
    I = Cm[0] & Cm[1]; U = Cm[0] | Cm[1]
    strict = [(ki, rc) for ki in range(1,9) for rc in sorted(I)
              if pat[0][(ki, rc[0], rc[1])] != pat[1][(ki, rc[0], rc[1])]]
    union_sites = [(ki, rc) for ki in range(1,9) for rc in sorted(U)
                   if pat[0][(ki, rc[0], rc[1])] != pat[1][(ki, rc[0], rc[1])]]
    # testemunha observacional: r com (r,c1),(r,c2) em I e O_m diferente
    obs = []
    for r_ in range(4):
        cs = sorted(c_ for (rr, c_) in I if rr == r_)
        for c1, c2 in itertools.combinations(cs, 2):
            O0 = phi0[(r_, c1)] ^ phi0[(r_, c2)]
            O1 = phi1[(r_, c1)] ^ phi1[(r_, c2)]
            if O0 != O1:
                obs.append({"r": r_, "c1": c1, "c2": c2, "O0": O0, "O1": O1})
    res_edges[nome] = {
        "d0": ds[0], "d1": ds[1], "d0==d1": ds[0] == ds[1],
        "d==esperado_WS1_F4": ds[0] == esperado_d[nome],
        "dep": dep, "const_por_celula": const_ok, "phi_bem_definida": phi_bem_def,
        "Wtil0": W0, "Wtil0==Wtil1": W0 == W1,
        "V0": V0, "|Iso(W)|": len(isoW),
        "iso_nao_triviais": [list(p) for p in isoW if list(p) != [0,1,2,3]][:3],
        "equidistante": all(W0[a][b] == W0[0][1] for a in range(4) for b in range(4) if a != b),
        "transportes_rho": rhos, "classe_rho": [cyc(tuple(r["rho"])) for r in rhos],
        "|C0|": len(Cm[0]), "|C1|": len(Cm[1]), "I": sorted(I), "n_I": len(I),
        "sitios_estritos": len(strict), "sitios_uniao": len(union_sites),
        "testemunhas_observacionais_diferentes": obs,
    }
OUT["fam20"]["arestas"] = res_edges

# fusao do nucleo via cl.classificar sobre a instancia canonica reconstruida
mods_can = [{"id":"A","bits":[0,1,2],"bits_memoria":[2]},
            {"id":"B","bits":[3,4,5],"bits_memoria":[5]},
            {"id":"CAB","bits":[6,7],"bits_memoria":[]},
            {"id":"CBA","bits":[8,9],"bits_memoria":[]},
            {"id":"D1","bits":[10],"bits_memoria":[]},
            {"id":"D2","bits":[11],"bits_memoria":[]}]
inst_can = {"id":"coord-fam20-canonica","n":n,"modulos":mods_can,
            "estado_inicial":int(s0),"transicao":[int(x) for x in tab]}
rc = cl.classificar(inst_can)
OUT["fam20"]["classificar_C1p_componentes"] = rc["C1p"]["componentes"]
OUT["fam20"]["nucleo_fundido_C1p"] = [0,1,2,3] in rc["C1p"]["componentes"]

# ============ Parte 2: replay lote1 ate tentativa 14155 ============
rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(910000001).spawn(4)[0]))
tent = 0; aceites = 0; alvo = None
while tent < 14155:
    th = g.sample_theta_base(rng); tent += 1
    if th.pi[0] == th.pi[1]:
        continue
    ok = g.elegibilidade(th, False)[0]
    if ok:
        aceites += 1
        if tent == 14155:
            alvo = th
if alvo is None:
    OUT["replay14155"] = {"erro": "tentativa 14155 nao foi aceite", "aceites_ate_14155": aceites}
else:
    tsha = hashlib.sha256(json.dumps(dataclasses.asdict(alvo), sort_keys=True).encode()).hexdigest()
    tab2, n2, lay2 = g.tabela_transicao("II", alvo, False)
    T2 = np.asarray(tab2, dtype=np.int64)
    r2 = {}
    for nome, e in (("C_AB->B", dict(abits=[6,7], bbits=[3,4,5], mem=[5], M=alvo.G0)),
                    ("C_BA->A", dict(abits=[8,9], bbits=[0,1,2], mem=[2], M=alvo.F0))):
        eB = cl.extractor(e["bbits"], n2); popB = cl.popcount_tab(3)
        ints = cl.intervencoes(e["abits"])
        ds = {}; dep = 0; Fs = {}
        for m in (0,1):
            Z = cl.estados_da_fibra(n2, e["mem"], m)
            nx0 = eB[T2[Z]]; F=[]; d=[]
            for (mk,vl) in ints:
                xr = eB[T2[(Z & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
                F.append(xr); d.append(int(popB[xr].sum()))
            Fs[m]=F; ds[m]=d
        for ki in range(9):
            dep += int(np.count_nonzero(Fs[0][ki] ^ Fs[1][ki]))
        W = [[sum(pc2(e["M"][r_][p] ^ e["M"][r_][q]) for r_ in range(4)) for q in range(4)] for p in range(4)]
        V = [sum(W[w][c] for c in range(4)) for w in range(4)]
        lvl = "L1" if ds[0]==ds[1] else ("L2" if cl.rank_canonico(ds[0])==cl.rank_canonico(ds[1]) else "L3")
        r2[nome] = {"nivel": lvl, "dep": dep, "V_de_W_M": V, "V_constante": len(set(V))==1}
    p0inv = [0]*4
    for i,v in enumerate(alvo.pi[0]): p0inv[v] = i
    tau = [alvo.pi[1][p0inv[i]] for i in range(4)]
    def cyc(p):
        seen=set(); lens=[]
        for i in range(4):
            if i in seen: continue
            l=0; j=i
            while j not in seen: seen.add(j); j=p[j]; l+=1
            lens.append(l)
        return tuple(sorted(lens,reverse=True))
    OUT["replay14155"] = {
        "aceites_ate_14155_inclusive": aceites,
        "indice_familia_0based": aceites-1,
        "theta_sha_prefixo": tsha[:16],
        "esperado_WS4": "964a55337a7a502f",
        "classe_tau": cyc(tau),
        "arestas": r2,
        "colapso_ambas_estado": all(v["nivel"] in ("L1","L2") for v in r2.values()),
    }

print(json.dumps(OUT, indent=1, ensure_ascii=False, default=str))
