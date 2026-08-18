# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS2 (information loss).
Script B: decomposição da perda de informação AO NIVEL DE SITIO nos casos
pré-comprometidos (precommit-ws2.txt): cadeia
  S0 respostas ponto-a-ponto -> S1 pc por sítio -> S1.5 histograma por intervenção
  -> S2 soma na fibra (com refinamento por blocos (k,c) e células (k,c,r))
  -> S3 vetor d_m -> S4 rank.
Inclui verificação EXACTA, sítio-a-sítio, da forma fechada
  X_m[k][z] = M[r][pi_m(c)] ^ M[r][pi_m(sub_k(c))]  (M=G0 ou F0; bit de memória do receptor: 0)
contra a enumeração pela tabela congelada. Nada é alterado fora do ws2 dir.
"""
import sys, json, hashlib, itertools
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws2-information-loss"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

SAIDA = WS + "/ws2-cases-sitelevel.json"

ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5], "G0", [3, 4]),
           ("C_BA->A", [8, 9], [0, 1, 2], [2], "F0", [0, 1]))


def pc2(v):
    return bin(v).count("1")


def subs_canal(ints, bits_a):
    lo, hi = bits_a
    out = []
    for (mk, vl) in ints:
        mc = ((mk >> lo) & 1) | (((mk >> hi) & 1) << 1)
        vc = ((vl >> lo) & 1) | (((vl >> hi) & 1) << 1)
        out.append((mc, vc))
    return out


def tau_de(pi0, pi1):
    inv0 = [0] * 4
    for c, p in enumerate(pi0):
        inv0[p] = c
    return tuple(pi1[inv0[p]] for p in range(4))


def w_base(M):
    return [[sum(pc2(M[r][p] ^ M[r][q]) for r in range(4)) for q in range(4)]
            for p in range(4)]


def grupo_iso(W):
    return [p for p in itertools.permutations(range(4))
            if all(W[p[a]][p[b]] == W[a][b] for a in range(4) for b in range(4))]


def analisa_aresta_sitio(T, n, th_d, nome, bits_a, bits_b, mem, Mname, rbits):
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    ints = cl.intervencoes(bits_a)
    subs = subs_canal(ints, bits_a)
    Z0 = cl.estados_da_fibra(n, mem, 0)
    Z1 = cl.estados_da_fibra(n, mem, 1)
    memmask = sum(1 << b for b in mem)
    assert int(np.bitwise_xor(Z0, Z1).min()) == memmask
    assert int(np.bitwise_xor(Z0, Z1).max()) == memmask
    ec = cl.extractor(bits_a, n)[Z0]          # canal por sítio (igual em Z1)
    er = cl.extractor(rbits, n)[Z0]           # estado não-memória do receptor
    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    M = th_d[Mname]
    pi = th_d["pi"]

    # células analíticas D_m[k][c][r]
    D = [[[[0] * 4 for _ in range(4)] for _ in range(len(ints))] for _ in range(2)]
    for m in (0, 1):
        pim = pi[m]
        for k, (mc, vc) in enumerate(subs):
            for c in range(4):
                c2 = (c & ~mc) | vc
                for r in range(4):
                    D[m][k][c][r] = M[r][pim[c]] ^ M[r][pim[c2]]

    per_k = []
    d0v, d1v = [], []
    dep_tot = s1_tot = swap_tot = 0
    delta_site_hist = {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0}
    site_check_fail = 0
    bloco_census = {"B0": 0, "B1": 0, "B2": 0, "B3": 0, "B4": 0}
    bloco_census_efect = {"B0": 0, "B1": 0, "B2": 0, "B3": 0, "B4": 0}
    k_comp_bloco = 0   # intervenções com histograma global igual mas >=1 bloco B3
    for k, (mk, vl) in enumerate(ints):
        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
        # verificação sítio-a-sítio da forma fechada (bit de memória: 0)
        pred0 = np.array([D[0][k][int(c)][int(r)] for c, r in zip(ec, er)], dtype=np.int64)
        pred1 = np.array([D[1][k][int(c)][int(r)] for c, r in zip(ec, er)], dtype=np.int64)
        site_check_fail += int((x0 != pred0).sum()) + int((x1 != pred1).sum())
        h0 = popB[x0]
        h1 = popB[x1]
        dep_k = int((x0 != x1).sum())
        s1_k = int((h0 != h1).sum())
        swap_k = dep_k - s1_k
        hist0 = np.bincount(h0, minlength=4)
        hist1 = np.bincount(h1, minlength=4)
        assert hist0[3] == 0 and hist1[3] == 0   # bit de memória do receptor nunca responde
        dlt = h0 - h1
        for v in (-2, -1, 0, 1, 2):
            delta_site_hist[v] += int((dlt == v).sum())
        d0k, d1k = int(h0.sum()), int(h1.sum())
        d0v.append(d0k)
        d1v.append(d1k)
        dep_tot += dep_k
        s1_tot += s1_k
        swap_tot += swap_k
        # blocos (k,c): células r=0..3
        tem_B3 = False
        for c in range(4):
            p0 = [pc2(D[0][k][c][r]) for r in range(4)]
            p1 = [pc2(D[1][k][c][r]) for r in range(4)]
            if all(D[0][k][c][r] == D[1][k][c][r] for r in range(4)):
                b = "B0"
            elif p0 == p1:
                b = "B1"
            elif sorted(p0) == sorted(p1):
                b = "B2"
            elif sum(p0) == sum(p1):
                b = "B3"
                tem_B3 = True
            else:
                b = "B4"
            bloco_census[b] += 1
            if mk != 0:
                bloco_census_efect[b] += 1
        eq_hist = bool((hist0 == hist1).all())
        if eq_hist and tem_B3:
            k_comp_bloco += 1
        per_k.append({"k": k, "mask_canal": subs[k][0], "val_canal": subs[k][1],
                      "dep": dep_k, "s1_pc_diferente": s1_k, "swap_pc_igual": swap_k,
                      "hist0": [int(x) for x in hist0[:3]],
                      "hist1": [int(x) for x in hist1[:3]],
                      "eq_hist": eq_hist, "d0": d0k, "d1": d1k})

    if d0v == d1v:
        nivel = "L1"
    elif cl.rank_canonico(d0v) == cl.rank_canonico(d1v):
        nivel = "L2"
    else:
        nivel = "L3"

    # estágio de perda (arestas L1): primeiro F da cadeia que iguala
    estagio = None
    if nivel == "L1" and dep_tot > 0:
        if s1_tot == 0:
            estagio = "F1_pc_pontual"
        elif all(pk["eq_hist"] for pk in per_k):
            estagio = "F1.5_histograma"
        elif bloco_census["B4"] == 0:
            estagio = "F2_soma_por_bloco"
        else:
            estagio = "F2_global_INESPERADO"

    # dep e d recomputados das células (multiplicidade 32) — forma fechada
    dep_cells = 32 * sum(1 for m_k in range(len(ints)) for c in range(4) for r in range(4)
                         if D[0][m_k][c][r] != D[1][m_k][c][r])
    d_cells = [[32 * sum(pc2(D[m][k][c][r]) for c in range(4) for r in range(4))
                for k in range(len(ints))] for m in (0, 1)]

    tau = tau_de(pi[0], pi[1])
    W = w_base(M)
    K_cond = all(W[tau[a]][tau[b]] == W[a][b] for a in range(4) for b in range(4))

    return {"nome": nome, "nivel": nivel, "dep_sites": dep_tot,
            "s1_sites_pc_diferente": s1_tot, "swap_sites_pc_igual": swap_tot,
            "delta_pc_por_sitio_hist": {str(k): v for k, v in delta_site_hist.items()},
            "d0": d0v, "d1": d1v,
            "rank0": list(cl.rank_canonico(d0v)), "rank1": list(cl.rank_canonico(d1v)),
            "blocos": bloco_census, "blocos_sem_nulo": bloco_census_efect,
            "k_hist_igual_com_B3": k_comp_bloco,
            "estagio_perda_L1": estagio,
            "verif_sitio_falhas": site_check_fail,
            "verif_dep_cells_igual": bool(dep_cells == dep_tot),
            "verif_d_cells_igual": bool(d_cells[0] == d0v and d_cells[1] == d1v),
            "tau": list(tau), "K": bool(K_cond),
            "per_k": per_k}


def main():
    dados = json.load(open(WS + "/ws2-thetas-cases.json"))
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "descricao": "decomposicao da perda ao nivel de sitio, casos precomprometidos",
           "arestas": []}
    verboso_feito = False
    resumo = {"L1": {"F1_pc_pontual": 0, "F1.5_histograma": 0,
                     "F2_soma_por_bloco": 0, "F2_global_INESPERADO": 0,
                     "sem_dep": 0},
              "verif_sitio_falhas_total": 0, "verif_reg_falhas": 0,
              "K_incoerencias_L1": 0}
    for caso in dados["casos"]:
        key = "%d:%d" % (caso["seed"], caso["tentativa"])
        th_d = dados["thetas"][key]
        th = g.Theta(**th_d)
        tab, n, lay = g.tabela_transicao("II", th, False)
        T = np.asarray(tab, dtype=np.int64)
        for (nome, bits_a, bits_b, mem, Mname, rbits) in ARESTAS:
            r = analisa_aresta_sitio(T, n, th_d, nome, bits_a, bits_b, mem, Mname, rbits)
            reg = caso["arestas_reg"][nome]
            niv_reg = {"L1_d_iguais": "L1", "L2_rank_igual_d_diferente": "L2",
                       "L3_rank_diferente": "L3"}[reg["nivel"]]
            ok_reg = (r["nivel"] == niv_reg and r["dep_sites"] == reg["dep_sites"])
            if "d0" in reg:
                ok_reg = ok_reg and (r["d0"] == reg["d0"] and r["d1"] == reg["d1"])
            if not ok_reg:
                resumo["verif_reg_falhas"] += 1
                print("DISCREPANCIA vs registo:", caso["seed"], caso["fam"], nome)
            resumo["verif_sitio_falhas_total"] += r["verif_sitio_falhas"]
            if r["nivel"] == "L1":
                resumo["L1"][r["estagio_perda_L1"] or "sem_dep"] += 1
                if not r["K"]:
                    resumo["K_incoerencias_L1"] += 1
            rec = {"seed": caso["seed"], "fam": caso["fam"], "grupo": caso["grupo"],
                   "tentativa": caso["tentativa"], **r}
            if not verboso_feito and caso["grupo"] == "colapso" and nome == "C_AB->B" \
               and r["nivel"] == "L1":
                rec["exemplar_verboso"] = True
            out["arestas"].append(rec)
        if not verboso_feito and caso["grupo"] == "colapso":
            verboso_feito = True   # o primeiro colapso do lote1 é o exemplar
    out["resumo"] = resumo
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print("arestas analisadas:", len(out["arestas"]))
    print("resumo:", json.dumps(resumo))
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())

if __name__ == "__main__":
    main()
