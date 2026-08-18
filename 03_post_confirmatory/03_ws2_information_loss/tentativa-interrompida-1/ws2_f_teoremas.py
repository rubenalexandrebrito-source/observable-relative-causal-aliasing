# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS2 (information loss).
Script F: verificação empírica dos enunciados estruturais derivados
(sobre o output do Script C + thetas dos casos):
 T1 (empates estruturais): d[0]=0, d[1]=d[2], d[3]=d[4] em toda a aresta e contexto;
 T2 (inversão): o vetor d determina linearmente os 6 valores de pares
     W̃(p,q), p<q — em particular d0=d1 <=> W̃_0=W̃_1 (necessidade de K);
     fórmulas: m1=e01+e23=d[1]/32; m2=e02+e13=d[3]/32; rs_γ=d[5+γ]/32;
     Σ=(Σ_γ rs_γ)/2; m3=e03+e12=Σ-m1-m2;
     e01=(rs_0+rs_1-m2-m3)/2 ... (sistema resolvido por pares);
 T3 (paridade): componentes de Δd múltiplas de 64 (já verificado no Script E;
     aqui re-verificado nos casos, por via analítica directa de ΔW̃);
 T4: agregados dep/s1/swap por nível; censos de blocos e nk para L2.
"""
import sys, json, hashlib
from collections import Counter

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws2-information-loss"
sys.path.insert(0, DST + "/frozen-copy")

PC2 = [bin(v).count("1") for v in range(4)]
SAIDA = WS + "/ws2-teoremas-verif.json"


def wtil(M, pim):
    return [[sum(PC2[M[r][pim[c1]] ^ M[r][pim[c2]]] for r in range(4))
             for c2 in range(4)] for c1 in range(4)]


def inverte_d_para_pares(d):
    m1 = d[1] / 32.0
    m2 = d[3] / 32.0
    rs = [d[5 + g] / 32.0 for g in range(4)]
    S = sum(rs) / 2.0
    m3 = S - m1 - m2
    e01 = (rs[0] + rs[1] - m2 - m3) / 2.0
    e23 = m1 - e01
    e02 = (rs[0] + rs[2] - m1 - m3) / 2.0
    e13 = m2 - e02
    e03 = (rs[0] + rs[3] - m1 - m2) / 2.0
    e12 = m3 - e03
    return {(0, 1): e01, (2, 3): e23, (0, 2): e02, (1, 3): e13,
            (0, 3): e03, (1, 2): e12}


def main():
    pop = json.load(open(WS + "/ws2-population-stages.json"))
    edges = pop["edges"]
    t1_fail = 0
    n_vec = 0
    for e in edges:
        for dv in ([e["d0"]] if e["n"] == "L1" else [e["d0"], e["d1"]]):
            n_vec += 1
            if not (dv[0] == 0 and dv[1] == dv[2] and dv[3] == dv[4]):
                t1_fail += 1

    casos = json.load(open(WS + "/ws2-thetas-cases.json"))
    t2_max_err = 0.0
    t2_n = 0
    t3_fail = 0
    for key, th_d in casos["thetas"].items():
        for Mname in ("G0", "F0"):
            M = th_d[Mname]
            for m in (0, 1):
                W = wtil(M, th_d["pi"][m])
                d = [0,
                     32 * (W[0][1] + W[2][3]), 32 * (W[0][1] + W[2][3]),
                     32 * (W[0][2] + W[1][3]), 32 * (W[0][2] + W[1][3]),
                     32 * sum(W[c][0] for c in range(4)),
                     32 * sum(W[c][1] for c in range(4)),
                     32 * sum(W[c][2] for c in range(4)),
                     32 * sum(W[c][3] for c in range(4))]
                rec = inverte_d_para_pares(d)
                for (p, q), v in rec.items():
                    t2_n += 1
                    err = abs(v - W[p][q])
                    t2_max_err = max(t2_max_err, err)
            W0 = wtil(M, th_d["pi"][0])
            W1 = wtil(M, th_d["pi"][1])
            for p in range(4):
                for q in range(p + 1, 4):
                    dl = W0[p][q] - W1[p][q]
                    # paridade: ΔW̃(p,q) tem paridade S(pi0 p)+S(pi0 q)+S(pi1 p)+S(pi1 q);
                    # somas m1, m2, rs_γ de ΔW̃ são pares => Δd ≡ 0 (mod 64)
            for pares in (((0, 1), (2, 3)), ((0, 2), (1, 3))):
                s = sum(W0[p][q] - W1[p][q] for (p, q) in pares)
                if s % 2 != 0:
                    t3_fail += 1
            for g in range(4):
                s = sum((W0[min(c, g)][max(c, g)] - W1[min(c, g)][max(c, g)])
                        for c in range(4) if c != g)
                if s % 2 != 0:
                    t3_fail += 1

    # T4: agregados por nível
    agg = {}
    for e in edges:
        a = agg.setdefault(e["n"], {"n": 0, "dep": 0, "s1": 0, "sw": 0})
        a["n"] += 1
        a["dep"] += e["dep"]
        a["s1"] += e["s1"]
        a["sw"] += e["sw"]
    nk_L2 = Counter()
    bl_L2 = Counter()
    for e in edges:
        if e["n"] == "L2":
            for k, v in e["nk"].items():
                nk_L2[k] += v
            for k, v in e["bl"].items():
                bl_L2[k] += v

    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "T1_empates_estruturais": {"vetores": n_vec, "falhas": t1_fail},
           "T2_inversao_d_para_Wpares": {"valores": t2_n,
                                         "erro_max": t2_max_err},
           "T3_paridade_somas_agregadas": {"falhas": t3_fail},
           "T4_agregados_por_nivel": agg,
           "T4_nk_L2": dict(nk_L2), "T4_blocos_L2": dict(bl_L2),
           "blocos_L2_top": pop["blocos_L2"], "blocos_L3_top": pop["blocos_L3"],
           "L1_comp_hist_entre_blocos": pop["arestas_L1_com_compensacao_hist_entre_blocos"]}
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print(json.dumps(out, indent=1))
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())

if __name__ == "__main__":
    main()
