# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — WS1 (álgebra do L1), script s13.
Validação FORA-DA-AMOSTRA da condição K (Teorema 5), nos termos EXACTOS de
precommit-ws1-oos.txt (semente 910000005, N=5000, métricas pré-fixadas).
Previsão = fórmula fechada a partir de θ; verdade-terreno = maquinaria
congelada (analisa_aresta, cópia literal). Escreve apenas em ws1-algebra-l1/.
"""
import sys, json, time, hashlib
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws1-algebra-l1"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

SEED = 910000005
N_ALVO = 5000
MAX_TENT = 200000
ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5]),
           ("C_BA->A", [8, 9], [0, 1, 2], [2]))
PC2 = [bin(v).count("1") for v in range(8)]


def analisa_aresta(T, n, bits_a, bits_b, membits):
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    ints = cl.intervencoes(bits_a)
    Z0 = cl.estados_da_fibra(n, membits, 0)
    Z1 = cl.estados_da_fibra(n, membits, 1)
    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    d0, d1, dep = [], [], 0
    for (mk, vl) in ints:
        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
        d0.append(int(popB[x0].sum()))
        d1.append(int(popB[x1].sum()))
        dep += int((x0 != x1).sum())
    if d0 == d1:
        nivel = "L1_d_iguais"
    elif cl.rank_canonico(d0) == cl.rank_canonico(d1):
        nivel = "L2_rank_igual_d_diferente"
    else:
        nivel = "L3_rank_diferente"
    return {"nivel": nivel, "dep_sites": dep, "d0": d0, "d1": d1}


def formula_aresta(th, nome, n):
    if nome == "C_BA->A":
        R, sig = th.F0, th.sigmaA
    else:
        R, sig = th.G0, th.sigmaB
    Phi = [[[R[x][th.pi[m][c]] ^ sig[m] for c in range(4)] for x in range(4)]
           for m in range(2)]
    mult = 1 << (n - 5)
    d = []
    for m in range(2):
        W = [[sum(PC2[Phi[m][x][a] ^ Phi[m][x][b]] for x in range(4))
              for b in range(4)] for a in range(4)]
        A = W[0][1] + W[2][3]
        B = W[0][2] + W[1][3]
        V = [sum(W[w][c] for c in range(4)) for w in range(4)]
        d.append([0, mult * A, mult * A, mult * B, mult * B,
                  mult * V[0], mult * V[1], mult * V[2], mult * V[3]])
    cnt = 0
    for x in range(4):
        for c in range(4):
            for j in (0, 1):
                if (Phi[0][x][c ^ (1 << j)] ^ Phi[0][x][c]) != \
                   (Phi[1][x][c ^ (1 << j)] ^ Phi[1][x][c]):
                    cnt += 1
            for w in range(4):
                if w != c and (Phi[0][x][w] ^ Phi[0][x][c]) != \
                              (Phi[1][x][w] ^ Phi[1][x][c]):
                    cnt += 1
    dep = mult * cnt
    if d[0] == d[1]:
        nivel = "L1_d_iguais"
    elif cl.rank_canonico(d[0]) == cl.rank_canonico(d[1]):
        nivel = "L2_rank_igual_d_diferente"
    else:
        nivel = "L3_rank_diferente"
    return {"nivel": nivel, "dep_sites": dep, "d0": d[0], "d1": d[1]}


def rho_classe(th):
    inv0 = [0] * 4
    for i, v in enumerate(th.pi[0]):
        inv0[v] = i
    rho = [inv0[th.pi[1][c]] for c in range(4)]
    vis, cyc = [False] * 4, []
    for i in range(4):
        if not vis[i]:
            l, j = 0, i
            while not vis[j]:
                vis[j] = True
                j = rho[j]
                l += 1
            cyc.append(l)
    cyc.sort(reverse=True)
    return {"2+1+1": "transposicao", "2+2": "V4", "3+1": "3-ciclo",
            "4": "4-ciclo"}["+".join(map(str, cyc))]


def main():
    t0 = time.time()
    ss = np.random.SeedSequence(SEED)
    filhos = ss.spawn(4)
    rng = np.random.Generator(np.random.PCG64(filhos[0]))
    tentativa, aceites = 0, 0
    conf = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    conf_estado = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}   # previsão L1∪L2 (ordinal)
    div = {"d": 0, "nivel": 0, "dep": 0}
    niveis_cont = {"L1_d_iguais": 0, "L2_rank_igual_d_diferente": 0,
                   "L3_rank_diferente": 0}
    dep_zero = 0
    classes = {"individua_ambas": 0, "individua_uma": 0, "colapso_total": 0}
    conf_colapso = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    subtipos = {}
    por_rho = {}
    while aceites < N_ALVO and tentativa < MAX_TENT:
        tentativa += 1
        th = g.sample_theta_base(rng)
        if th.pi[0] == th.pi[1]:
            continue
        ok, razao, _ = g.elegibilidade(th, False)
        if not ok:
            continue
        aceites += 1
        tab, n, lay = g.tabela_transicao("II", th, False)
        T = np.asarray(tab, dtype=np.int64)
        rc = rho_classe(th)
        pr = por_rho.setdefault(rc, {"fam": 0, "L1": 0, "L2": 0, "L3": 0,
                                     "L1L1": 0, "colapso": 0})
        pr["fam"] += 1
        niveis, prev_l3 = [], 0
        for nome, ba, bb, mem in ARESTAS:
            fro = analisa_aresta(T, n, ba, bb, mem)
            frm = formula_aresta(th, nome, n)
            K = frm["d0"] == frm["d1"]
            L1 = fro["nivel"] == "L1_d_iguais"
            conf["TP" if K and L1 else "FP" if K else "FN" if L1 else "TN"] += 1
            Kest = frm["nivel"] != "L3_rank_diferente"
            Est = fro["nivel"] != "L3_rank_diferente"
            conf_estado["TP" if Kest and Est else "FP" if Kest
                        else "FN" if Est else "TN"] += 1
            if fro["d0"] != frm["d0"] or fro["d1"] != frm["d1"]:
                div["d"] += 1
            if fro["nivel"] != frm["nivel"]:
                div["nivel"] += 1
            if fro["dep_sites"] != frm["dep_sites"]:
                div["dep"] += 1
            niveis_cont[fro["nivel"]] += 1
            if fro["dep_sites"] == 0:
                dep_zero += 1
            niveis.append(fro["nivel"])
            if frm["nivel"] == "L3_rank_diferente":
                prev_l3 += 1
            pr["L1" if fro["nivel"] == "L1_d_iguais" else
               ("L2" if fro["nivel"].startswith("L2") else "L3")] += 1
        n_l3 = sum(1 for v in niveis if v == "L3_rank_diferente")
        cls = {2: "individua_ambas", 1: "individua_uma", 0: "colapso_total"}[n_l3]
        classes[cls] += 1
        col_prev = prev_l3 == 0
        col_real = cls == "colapso_total"
        conf_colapso["TP" if col_prev and col_real else "FP" if col_prev
                     else "FN" if col_real else "TN"] += 1
        if col_real:
            pr["colapso"] += 1
            st = str(tuple(sorted(niveis)))
            subtipos[st] = subtipos.get(st, 0) + 1
        if niveis[0] == "L1_d_iguais" and niveis[1] == "L1_d_iguais":
            pr["L1L1"] += 1

    def metricas(c):
        TP, FP, FN, TN = c["TP"], c["FP"], c["FN"], c["TN"]
        return {"TP": TP, "FP": FP, "FN": FN, "TN": TN,
                "sensibilidade": TP / (TP + FN) if TP + FN else None,
                "especificidade": TN / (TN + FP) if TN + FP else None,
                "precisao": TP / (TP + FP) if TP + FP else None,
                "NPV": TN / (TN + FN) if TN + FN else None}

    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "script": "s13_oos.py", "precommit": "precommit-ws1-oos.txt",
           "semente": SEED, "n_alvo": N_ALVO,
           "tentativas": tentativa, "aceites": aceites,
           "duracao_s": round(time.time() - t0, 1),
           "confusao_K_vs_L1_por_aresta": metricas(conf),
           "confusao_ordinal_vs_L1uL2_por_aresta": metricas(conf_estado),
           "confusao_colapso_por_instancia": metricas(conf_colapso),
           "divergencias_formula_vs_congelado": div,
           "niveis_por_aresta": niveis_cont,
           "dep_zero_arestas": dep_zero,
           "classes_por_instancia": classes,
           "subtipos_colapso": subtipos,
           "por_rho": por_rho}
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(WS + "/out-s13.json", "wb").write(corpo)
    print("=== s13 RESUMO (OOS, semente %d) ===" % SEED)
    print("aceites %d / tentativas %d em %.1fs" % (aceites, tentativa,
                                                   out["duracao_s"]))
    print("K vs L1   :", json.dumps(out["confusao_K_vs_L1_por_aresta"]))
    print("ord vs L12:", json.dumps(out["confusao_ordinal_vs_L1uL2_por_aresta"]))
    print("colapso   :", json.dumps(out["confusao_colapso_por_instancia"]))
    print("divergencias:", div)
    print("niveis:", niveis_cont, "dep_zero:", dep_zero)
    print("classes:", classes, subtipos)
    for k in sorted(por_rho):
        v = por_rho[k]
        print("  %-13s fam=%5d L1/aresta=%.4f colapso=%d"
              % (k, v["fam"], v["L1"] / (2.0 * v["fam"]), v["colapso"]))
    print("sha256 out-s13.json:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
