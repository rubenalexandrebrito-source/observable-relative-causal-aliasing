# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — WS1 (álgebra do L1), script s12.
Replay COMPLETO dos dois lotes exploratórios existentes (sementes 910000001 e
910000002; NENHUMA semente nova) reproduzindo o loop exacto do dataset:
sample_theta_base → rejeitar π0==π1 → elegibilidade. Para cada família aceite:
  (i)  maquinaria congelada (analisa_aresta, cópia literal) → d0,d1,dep,nível;
  (ii) fórmula fechada WS1 (Prop. 3) directamente de θ → previsão;
  (iii) igualdade EXACTA (i)==(ii) componente a componente; K ⟺ L1.
Reconcilia os agregados com os JSON publicados e tabula níveis por classe de
conjugação de ρ = π0⁻¹π1 (Teorema 9: correlação inter-arestas).
Escreve apenas em ws1-algebra-l1/.
"""
import sys, json, time, hashlib
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
N_ALVO = 5000
MAX_TENT = 200000


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


def correr_lote(seed):
    t0 = time.time()
    ss = np.random.SeedSequence(seed)
    filhos = ss.spawn(4)
    rng = np.random.Generator(np.random.PCG64(filhos[0]))
    tentativa, aceites = 0, 0
    mismatch = {"d": 0, "nivel": 0, "dep": 0, "K_vs_L1": 0}
    niveis_cont = {"L1_d_iguais": 0, "L2_rank_igual_d_diferente": 0,
                   "L3_rank_diferente": 0}
    dep_zero = 0
    classes = {"individua_ambas": 0, "individua_uma": 0, "colapso_total": 0}
    subtipos = {}
    por_rho = {}
    exemplos_mismatch = []
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
        niveis = []
        for nome, ba, bb, mem in ARESTAS:
            fro = analisa_aresta(T, n, ba, bb, mem)
            frm = formula_aresta(th, nome, n)
            if fro["d0"] != frm["d0"] or fro["d1"] != frm["d1"]:
                mismatch["d"] += 1
                if len(exemplos_mismatch) < 5:
                    exemplos_mismatch.append({"seed": seed, "tentativa": tentativa,
                                              "aresta": nome, "tipo": "d"})
            if fro["nivel"] != frm["nivel"]:
                mismatch["nivel"] += 1
            if fro["dep_sites"] != frm["dep_sites"]:
                mismatch["dep"] += 1
            K = frm["d0"] == frm["d1"]
            if K != (fro["nivel"] == "L1_d_iguais"):
                mismatch["K_vs_L1"] += 1
            niveis_cont[fro["nivel"]] += 1
            if fro["dep_sites"] == 0:
                dep_zero += 1
            niveis.append(fro["nivel"])
            pr["L1" if fro["nivel"] == "L1_d_iguais" else
               ("L2" if fro["nivel"].startswith("L2") else "L3")] += 1
        n_l3 = sum(1 for v in niveis if v == "L3_rank_diferente")
        cls = {2: "individua_ambas", 1: "individua_uma", 0: "colapso_total"}[n_l3]
        classes[cls] += 1
        if niveis[0] == "L1_d_iguais" and niveis[1] == "L1_d_iguais":
            pr["L1L1"] += 1
        if cls == "colapso_total":
            pr["colapso"] += 1
            st = str(tuple(sorted(niveis)))
            subtipos[st] = subtipos.get(st, 0) + 1
    return {"seed": seed, "tentativas": tentativa, "aceites": aceites,
            "duracao_s": round(time.time() - t0, 1),
            "mismatch": mismatch, "exemplos_mismatch": exemplos_mismatch,
            "niveis_por_aresta": niveis_cont, "dep_zero_arestas": dep_zero,
            "classes_por_instancia": classes, "subtipos_colapso": subtipos,
            "por_rho": por_rho}


def main():
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "script": "s12_replay_completo.py", "lotes": []}
    esperado = {
        910000001: {"tentativas": 17135, "L1": 358, "L2": 113, "L3": 9529,
                    "dep_zero": 4, "colapsos": 22},
        910000002: {"tentativas": 16845, "L1": 347, "L2": 112, "L3": 9541,
                    "dep_zero": 3, "colapsos": 24},
    }
    total_rho = {}
    for seed in (910000001, 910000002):
        r = correr_lote(seed)
        e = esperado[seed]
        r["reconciliacao_com_dataset_publicado"] = {
            "tentativas_ok": r["tentativas"] == e["tentativas"],
            "L1_ok": r["niveis_por_aresta"]["L1_d_iguais"] == e["L1"],
            "L2_ok": r["niveis_por_aresta"]["L2_rank_igual_d_diferente"] == e["L2"],
            "L3_ok": r["niveis_por_aresta"]["L3_rank_diferente"] == e["L3"],
            "dep_zero_ok": r["dep_zero_arestas"] == e["dep_zero"],
            "colapsos_ok": r["classes_por_instancia"]["colapso_total"] == e["colapsos"],
        }
        out["lotes"].append(r)
        for k, v in r["por_rho"].items():
            t = total_rho.setdefault(k, {kk: 0 for kk in v})
            for kk in v:
                t[kk] += v[kk]
    out["por_rho_combinado"] = total_rho
    # decomposição da correlação (Teorema 9)
    n_fam = sum(v["fam"] for v in total_rho.values())
    p_l1 = sum(v["L1"] for v in total_rho.values()) / (2.0 * n_fam)
    p_joint = sum(v["L1L1"] for v in total_rho.values()) / float(n_fam)
    p_joint_modelo = 0.0
    for v in total_rho.values():
        pcl = v["fam"] / float(n_fam)
        pl1 = v["L1"] / (2.0 * v["fam"])
        p_joint_modelo += pcl * pl1 * pl1
    out["correlacao"] = {
        "P_L1_aresta": p_l1,
        "P_L1L1_observado": p_joint,
        "P_L1L1_independencia_global": p_l1 ** 2,
        "P_L1L1_modelo_classe_condicional": p_joint_modelo,
        "lift_observado": p_joint / (p_l1 ** 2) if p_l1 else None,
        "lift_modelo": p_joint_modelo / (p_l1 ** 2) if p_l1 else None,
    }
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(WS + "/out-s12.json", "wb").write(corpo)
    print("=== s12 RESUMO ===")
    for r in out["lotes"]:
        print("lote", r["seed"], "aceites", r["aceites"], "tentativas",
              r["tentativas"], "em", r["duracao_s"], "s")
        print("  mismatch:", r["mismatch"])
        print("  reconciliacao:", r["reconciliacao_com_dataset_publicado"])
        print("  niveis:", r["niveis_por_aresta"], "dep_zero:",
              r["dep_zero_arestas"])
        print("  classes:", r["classes_por_instancia"], r["subtipos_colapso"])
    print("por_rho combinado:")
    for k in sorted(total_rho):
        v = total_rho[k]
        print("  %-13s fam=%5d  L1/aresta=%.4f  L2=%.4f  L1L1/fam=%.5f  colapso=%d"
              % (k, v["fam"], v["L1"] / (2.0 * v["fam"]),
                 v["L2"] / (2.0 * v["fam"]), v["L1L1"] / float(v["fam"]),
                 v["colapso"]))
    print("correlacao:", json.dumps(out["correlacao"], indent=1))
    print("sha256 out-s12.json:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
