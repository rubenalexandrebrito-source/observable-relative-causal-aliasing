# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — WS1 (álgebra do L1), script s10.
Valida a fórmula fechada da Prop. 3 / Teorema 5 (NOTAS-DERIVACAO.md) contra
TODOS os exemplos registados nos datasets permitidos:
  - 46 colapso_total (22 lote1 + 24 lote2)  — arestas L1/L2 com d0/d1 registados
  - 40 individua_uma (20+20)                — mistas
  - 40 individua_ambas (20+20)              — CONTROLOS L3/L3, critério objectivo:
    são os "primeiros 20" de cada lote fixados pelo script original do dataset,
    não escolhidos por este agente.
Replay de θ por (semente, tentativa) com verificação de theta_sha; para cada
aresta compara três vias: (i) registado no dataset, (ii) recomputação com a
maquinaria congelada (cópia literal de analisa_aresta), (iii) fórmula fechada.
NÃO altera nada fora de ws1-algebra-l1/. Não usa sementes novas.
"""
import sys, json, hashlib, itertools
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws1-algebra-l1"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5]),
           ("C_BA->A", [8, 9], [0, 1, 2], [2]))

PC2 = [bin(v).count("1") for v in range(8)]


def analisa_aresta(T, n, bits_a, bits_b, membits):
    """Cópia literal de prevalencia_cancelamento.py (maquinaria congelada)."""
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


# ---------------- fórmula fechada (derivação WS1) ----------------

def phi_edge(th, nome):
    """Φ_m(x,c) (parte x' apenas; σ incluído, cancela nos XOR)."""
    if nome == "C_BA->A":
        R, sig = th.F0, th.sigmaA
    else:
        R, sig = th.G0, th.sigmaB
    return [[[R[x][th.pi[m][c]] ^ sig[m] for c in range(4)] for x in range(4)]
            for m in range(2)]


def agregados(Phi_m):
    W = [[sum(PC2[Phi_m[x][a] ^ Phi_m[x][b]] for x in range(4))
          for b in range(4)] for a in range(4)]
    A = W[0][1] + W[2][3]
    B = W[0][2] + W[1][3]
    V = [sum(W[w][c] for c in range(4)) for w in range(4)]
    WM3 = W[0][3] + W[1][2]
    return A, B, V, WM3


def formula_aresta(th, nome, n):
    Phi = phi_edge(th, nome)
    mult = 1 << (n - 5)
    d, ABV = [], []
    for m in range(2):
        A, B, V, WM3 = agregados(Phi[m])
        ABV.append({"A": A, "B": B, "V": V, "WM3": WM3})
        d.append([0, mult * A, mult * A, mult * B, mult * B,
                  mult * V[0], mult * V[1], mult * V[2], mult * V[3]])
    # dep previsto
    cnt = 0
    for x in range(4):
        for c in range(4):
            for j in (0, 1):                      # bit único := v (v != c_j)
                p0 = Phi[0][x][c ^ (1 << j)] ^ Phi[0][x][c]
                p1 = Phi[1][x][c ^ (1 << j)] ^ Phi[1][x][c]
                if p0 != p1:
                    cnt += 1                       # conta para o v que difere
            for w in range(4):                    # máscara cheia := w
                if w == c:
                    continue
                p0 = Phi[0][x][w] ^ Phi[0][x][c]
                p1 = Phi[1][x][w] ^ Phi[1][x][c]
                if p0 != p1:
                    cnt += 1
    dep = mult * cnt
    if d[0] == d[1]:
        nivel = "L1_d_iguais"
    elif cl.rank_canonico(d[0]) == cl.rank_canonico(d[1]):
        nivel = "L2_rank_igual_d_diferente"
    else:
        nivel = "L3_rank_diferente"
    return {"nivel": nivel, "dep_sites": dep, "d0": d[0], "d1": d[1],
            "ABV": ABV}


def rho_de(th):
    inv0 = [0] * 4
    for i, v in enumerate(th.pi[0]):
        inv0[v] = i
    return [inv0[th.pi[1][c]] for c in range(4)]


def tipo_ciclo(p):
    vis, cyc = [False] * 4, []
    for i in range(4):
        if not vis[i]:
            l, j = 0, i
            while not vis[j]:
                vis[j] = True
                j = p[j]
                l += 1
            cyc.append(l)
    cyc.sort(reverse=True)
    t = "+".join(map(str, cyc))
    return {"2+1+1": "transposicao", "2+2": "V4", "3+1": "3-ciclo",
            "4": "4-ciclo", "1+1+1+1": "identidade"}[t]


def theta_sha(th):
    return hashlib.sha256(
        json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()


def replay(seed, tentativas):
    ss = np.random.SeedSequence(seed)
    filhos = ss.spawn(4)
    rng = np.random.Generator(np.random.PCG64(filhos[0]))
    alvo, out, t = set(tentativas), {}, 0
    mx = max(alvo)
    while t < mx:
        th = g.sample_theta_base(rng)
        t += 1
        if t in alvo:
            out[t] = th
    return out


def main():
    lotes = {910000001: "prevalencia-cancelamento-II.json",
             910000002: "prevalencia-cancelamento-II-lote2.json"}
    resultados = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
                  "script": "s10_exemplos_validacao.py",
                  "criterio_controlos_L3L3": ("exemplos individua_ambas dos datasets"
                                              " = primeiros 20 de cada lote, regra"
                                              " fixada pelo script original"),
                  "lotes": {}}
    tot_cmp = {"niveis_ok": 0, "niveis_err": 0, "d_reg_ok": 0, "d_reg_err": 0,
               "d_frozen_ok": 0, "d_frozen_err": 0, "dep_ok": 0, "dep_err": 0,
               "sha_ok": 0, "sha_err": 0}
    tabela_colapsos = []
    for seed, fjson in lotes.items():
        data = json.load(open(DST + "/prevalencia/" + fjson))
        ex = data["exemplos"]
        registos = (ex["colapso_total"] + ex["individua_uma"]
                    + ex["individua_ambas"])
        ths = replay(seed, [r["tentativa"] for r in registos])
        lote_out = []
        for r in registos:
            th = ths[r["tentativa"]]
            sha_ok = theta_sha(th) == r["theta_sha"]
            tot_cmp["sha_ok" if sha_ok else "sha_err"] += 1
            if not sha_ok:
                print("SHA MISMATCH", seed, r["fam"], r["tentativa"])
                continue
            tab, n, lay = g.tabela_transicao("II", th, False)
            T = np.asarray(tab, dtype=np.int64)
            rho = rho_de(th)
            fam_out = {"lote": seed, "fam": r["fam"], "classe": r["classe"],
                       "rho": rho, "rho_classe": tipo_ciclo(rho), "arestas": {}}
            for nome, ba, bb, mem in ARESTAS:
                reg = r["arestas"][nome]
                fro = analisa_aresta(T, n, ba, bb, mem)
                frm = formula_aresta(th, nome, n)
                ok_n = (reg["nivel"] == fro["nivel"] == frm["nivel"])
                tot_cmp["niveis_ok" if ok_n else "niveis_err"] += 1
                ok_dep = (reg["dep_sites"] == fro["dep_sites"] == frm["dep_sites"])
                tot_cmp["dep_ok" if ok_dep else "dep_err"] += 1
                if "d0" in reg:
                    ok_dr = (reg["d0"] == frm["d0"] and reg["d1"] == frm["d1"])
                    tot_cmp["d_reg_ok" if ok_dr else "d_reg_err"] += 1
                ok_df = (fro["d0"] == frm["d0"] and fro["d1"] == frm["d1"])
                tot_cmp["d_frozen_ok" if ok_df else "d_frozen_err"] += 1
                a0, a1 = frm["ABV"]
                fam_out["arestas"][nome] = {
                    "nivel": frm["nivel"], "dep": frm["dep_sites"],
                    "cond_a_A0eqA1": a0["A"] == a1["A"],
                    "cond_b_B0eqB1": a0["B"] == a1["B"],
                    "cond_c_V0eqV1": a0["V"] == a1["V"],
                    "K": frm["d0"] == frm["d1"],
                    "ABV0": a0, "ABV1": a1,
                    "ok_nivel": ok_n, "ok_dep": ok_dep, "ok_d_frozen": ok_df,
                }
            lote_out.append(fam_out)
            if r["classe"] == "colapso_total":
                tabela_colapsos.append(fam_out)
        resultados["lotes"][str(seed)] = lote_out
    resultados["comparacoes"] = tot_cmp
    # resumo dos 46 colapsos por classe de rho
    dist = {}
    for f in tabela_colapsos:
        key = (f["rho_classe"],
               tuple(sorted(f["arestas"][a]["nivel"] for a in f["arestas"])))
        dist[str(key)] = dist.get(str(key), 0) + 1
    resultados["colapsos_por_rho"] = dist
    corpo = json.dumps(resultados, sort_keys=True, indent=1).encode()
    open(WS + "/out-s10.json", "wb").write(corpo)
    print("=== s10 RESUMO ===")
    print("comparacoes:", tot_cmp)
    print("colapsos por (rho, niveis):")
    for k in sorted(dist):
        print("  ", k, dist[k])
    print("sha256 out-s10.json:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
