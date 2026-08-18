# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS2 (information loss).
Script C: passo populacional — replay determinístico dos DOIS lotes registados
(sementes registadas 910000001/910000002; nenhuma amostra nova), com métricas de
perda por estágio derivadas ANALITICAMENTE das células (k,c,r) via theta
(forma fechada verificada sítio-a-sítio no Script B). Sem tabela_transicao.
Valida contra os exemplos registados e os agregados publicados. Auditoria
independente da condição K (tau ∈ Iso(W_M)) vs L1.
"""
import sys, json, time, hashlib, itertools
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws2-information-loss"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

SEEDS = [910000001, 910000002]
N_POR_SEED = 5000
SAIDA = WS + "/ws2-population-stages.json"

ARESTAS = (("C_AB->B", [6, 7], "G0"),
           ("C_BA->A", [8, 9], "F0"))

PC2 = [bin(v).count("1") for v in range(4)]


def subs_canal_local():
    """(mc, vc) das 9 intervenções de cl.intervencoes para um canal de 2 bits,
    na MESMA ordem; derivado uma vez de bits genéricos [0,1]."""
    ints = cl.intervencoes([0, 1])
    return [(int(mk), int(vl)) for (mk, vl) in ints]


SUBS = subs_canal_local()


def tau_de(pi0, pi1):
    inv0 = [0] * 4
    for c, p in enumerate(pi0):
        inv0[p] = c
    return tuple(pi1[inv0[p]] for p in range(4))


def cycle_type(perm):
    seen = [False] * 4
    t = []
    for i in range(4):
        if not seen[i]:
            l, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                l += 1
            t.append(l)
    return tuple(sorted(t))


def w_base(M):
    return [[sum(PC2[M[r][p] ^ M[r][q]] for r in range(4)) for q in range(4)]
            for p in range(4)]


def analisa_aresta_analitica(M, pi):
    """Devolve métricas de estágio por aresta, das células (k,c,r), mult. 32."""
    Dm = []
    for m in (0, 1):
        pim = pi[m]
        Mp = [[M[r][pim[c]] for c in range(4)] for r in range(4)]  # M[r][pi_m c]
        Dk = []
        for (mc, vc) in SUBS:
            tab = [[Mp[r][c] ^ Mp[r][(c & ~mc) | vc] for r in range(4)]
                   for c in range(4)]
            Dk.append(tab)
        Dm.append(Dk)
    d0, d1 = [], []
    dep = s1 = swap = 0
    nk = {"igual_S0": 0, "igual_S1_pc": 0, "igual_S1.5_hist": 0,
          "igual_so_S2_soma": 0, "desigual_S2": 0}
    blocos = {"B0": 0, "B1": 0, "B2": 0, "B3": 0, "B4": 0}
    k_hist_igual_com_B3 = 0
    for k in range(9):
        mc, vc = SUBS[k]
        dep_k = s1_k = 0
        h0 = [0, 0, 0]
        h1 = [0, 0, 0]
        s0 = s1s = 0
        tem_B3 = False
        for c in range(4):
            p0 = [PC2[Dm[0][k][c][r]] for r in range(4)]
            p1 = [PC2[Dm[1][k][c][r]] for r in range(4)]
            iguais = all(Dm[0][k][c][r] == Dm[1][k][c][r] for r in range(4))
            for r in range(4):
                if Dm[0][k][c][r] != Dm[1][k][c][r]:
                    dep_k += 1
                    if p0[r] == p1[r]:
                        swap += 1
                    else:
                        s1_k += 1
                h0[p0[r]] += 1
                h1[p1[r]] += 1
                s0 += p0[r]
                s1s += p1[r]
            if mc != 0:
                if iguais:
                    blocos["B0"] += 1
                elif p0 == p1:
                    blocos["B1"] += 1
                elif sorted(p0) == sorted(p1):
                    blocos["B2"] += 1
                elif sum(p0) == sum(p1):
                    blocos["B3"] += 1
                    tem_B3 = True
                else:
                    blocos["B4"] += 1
        d0k = 32 * sum(PC2[Dm[0][k][c][r]] for c in range(4) for r in range(4))
        d1k = 32 * sum(PC2[Dm[1][k][c][r]] for c in range(4) for r in range(4))
        d0.append(d0k)
        d1.append(d1k)
        dep += 32 * dep_k
        s1 += 32 * s1_k
        eq_hist = (h0 == h1)
        if mc != 0:
            if dep_k == 0:
                nk["igual_S0"] += 1
            elif s1_k == 0:
                nk["igual_S1_pc"] += 1
            elif eq_hist:
                nk["igual_S1.5_hist"] += 1
            elif d0k == d1k:
                nk["igual_so_S2_soma"] += 1
            else:
                nk["desigual_S2"] += 1
            if eq_hist and tem_B3:
                k_hist_igual_com_B3 += 1
    swap *= 32
    if d0 == d1:
        nivel = "L1"
    elif cl.rank_canonico(d0) == cl.rank_canonico(d1):
        nivel = "L2"
    else:
        nivel = "L3"
    estagio = None
    if nivel == "L1" and dep > 0:
        if s1 == 0:
            estagio = "F1_pc_pontual"
        elif nk["igual_so_S2_soma"] == 0 and nk["desigual_S2"] == 0:
            estagio = "F1.5_histograma"
        elif blocos["B4"] == 0:
            estagio = "F2_soma_por_bloco"
        else:
            estagio = "F2_global_INESPERADO"
    return {"nivel": nivel, "dep": dep, "s1": s1, "swap": swap, "d0": d0, "d1": d1,
            "nk": nk, "blocos": blocos, "estagio": estagio,
            "k_hist_igual_com_B3": k_hist_igual_com_B3}


def theta_sha(th):
    return hashlib.sha256(json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()


def main():
    t0 = time.time()
    exemplos_reg = {}
    for seed, path in ((910000001, "/prevalencia/prevalencia-cancelamento-II.json"),
                       (910000002, "/prevalencia/prevalencia-cancelamento-II-lote2.json")):
        jj = json.load(open(DST + path))
        for cls in ("colapso_total", "individua_uma", "individua_ambas"):
            for r in jj["exemplos"][cls]:
                exemplos_reg[(seed, r["tentativa"])] = r

    edges_out = []
    níveis = {"L1": 0, "L2": 0, "L3": 0}
    conf = {nm: {"TP": 0, "FP": 0, "TN": 0, "FN": 0} for nm, _, _ in ARESTAS}
    por_tau_classe = {}
    inst_classes = {"individua_ambas": 0, "individua_uma": 0, "colapso_total": 0}
    subtipos = {}
    estagios_L1 = {"F1_pc_pontual": 0, "F1.5_histograma": 0,
                   "F2_soma_por_bloco": 0, "F2_global_INESPERADO": 0, "sem_dep": 0}
    blocos_L1 = {"B0": 0, "B1": 0, "B2": 0, "B3": 0, "B4": 0}
    blocos_L2 = {"B0": 0, "B1": 0, "B2": 0, "B3": 0, "B4": 0}
    blocos_L3 = {"B0": 0, "B1": 0, "B2": 0, "B3": 0, "B4": 0}
    nk_L1 = {"igual_S0": 0, "igual_S1_pc": 0, "igual_S1.5_hist": 0,
             "igual_so_S2_soma": 0, "desigual_S2": 0}
    dep_zero_edges = 0
    dep_pos_edges = 0
    verif = {"exemplos_encontrados": 0, "exemplos_sha_ok": 0, "exemplos_dados_ok": 0}
    comp_hist_L1_edges = 0

    for seed in SEEDS:
        ss = np.random.SeedSequence(seed)
        rng = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))
        aceites = 0
        tentativa = 0
        while aceites < N_POR_SEED:
            tentativa += 1
            th = g.sample_theta_base(rng)
            if th.pi[0] == th.pi[1]:
                continue
            ok, _, _ = g.elegibilidade(th, False)
            if not ok:
                continue
            fam = aceites
            aceites += 1
            tau = tau_de(th.pi[0], th.pi[1])
            ttype = "x".join(map(str, cycle_type(tau)))
            reg = exemplos_reg.get((seed, tentativa))
            if reg is not None:
                verif["exemplos_encontrados"] += 1
                if theta_sha(th) == reg["theta_sha"]:
                    verif["exemplos_sha_ok"] += 1
            niveis_fam = []
            for (nome, bits_a, Mname) in ARESTAS:
                M = getattr(th, Mname)
                r = analisa_aresta_analitica(M, th.pi)
                W = w_base(M)
                K = all(W[tau[a]][tau[b]] == W[a][b] for a in range(4) for b in range(4))
                níveis[r["nivel"]] += 1
                niveis_fam.append(r["nivel"])
                if r["dep"] == 0:
                    dep_zero_edges += 1
                else:
                    dep_pos_edges += 1
                L1 = (r["nivel"] == "L1")
                cellK = conf[nome]
                if K and L1:
                    cellK["TP"] += 1
                elif K and not L1:
                    cellK["FP"] += 1
                elif not K and L1:
                    cellK["FN"] += 1
                else:
                    cellK["TN"] += 1
                pt = por_tau_classe.setdefault(ttype, {"n": 0, "L1": 0})
                pt["n"] += 1
                pt["L1"] += int(L1)
                if L1:
                    estagios_L1[r["estagio"] or "sem_dep"] += 1
                    for b, v in r["blocos"].items():
                        blocos_L1[b] += v
                    for kk, v in r["nk"].items():
                        nk_L1[kk] += v
                    if r["k_hist_igual_com_B3"] > 0:
                        comp_hist_L1_edges += 1
                elif r["nivel"] == "L2":
                    for b, v in r["blocos"].items():
                        blocos_L2[b] += v
                else:
                    for b, v in r["blocos"].items():
                        blocos_L3[b] += v
                if reg is not None and nome in reg["arestas"]:
                    ra = reg["arestas"][nome]
                    niv_reg = {"L1_d_iguais": "L1", "L2_rank_igual_d_diferente": "L2",
                               "L3_rank_diferente": "L3"}[ra["nivel"]]
                    ok_d = (ra.get("d0") is None or
                            (ra["d0"] == r["d0"] and ra["d1"] == r["d1"]))
                    if niv_reg == r["nivel"] and ra["dep_sites"] == r["dep"] and ok_d:
                        verif["exemplos_dados_ok"] += 1
                row = {"s": seed, "f": fam, "t": tentativa, "e": nome,
                       "n": r["nivel"], "dep": r["dep"], "s1": r["s1"],
                       "sw": r["swap"], "d0": r["d0"], "K": bool(K), "tau": ttype}
                if r["nivel"] != "L1":
                    row["d1"] = r["d1"]
                if r["nivel"] == "L1":
                    row["st"] = r["estagio"] or "sem_dep"
                    row["bl"] = r["blocos"]
                    row["nk"] = r["nk"]
                if r["nivel"] == "L2":
                    row["bl"] = r["blocos"]
                    row["nk"] = r["nk"]
                edges_out.append(row)
            n_l3 = sum(1 for v in niveis_fam if v == "L3")
            cls = {2: "individua_ambas", 1: "individua_uma", 0: "colapso_total"}[n_l3]
            inst_classes[cls] += 1
            if cls == "colapso_total":
                stt = tuple(sorted(niveis_fam))
                subtipos[str(stt)] = subtipos.get(str(stt), 0) + 1
            if aceites % 1000 == 0:
                print("seed %d: %d aceites, %d tentativas, %.0fs"
                      % (seed, aceites, tentativa, time.time() - t0), flush=True)

    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "descricao": "estagios de perda por aresta, populacao replay N=10000 (2 lotes registados)",
           "seeds_replay_registadas": SEEDS,
           "niveis": níveis, "dep_zero": dep_zero_edges, "dep_pos": dep_pos_edges,
           "confusao_K_vs_L1": conf, "por_tau_classe": por_tau_classe,
           "instancias": inst_classes, "subtipos_colapso": subtipos,
           "estagios_L1": estagios_L1,
           "blocos_L1": blocos_L1, "blocos_L2": blocos_L2, "blocos_L3": blocos_L3,
           "nk_L1": nk_L1,
           "arestas_L1_com_compensacao_hist_entre_blocos": comp_hist_L1_edges,
           "verificacao_exemplos": verif,
           "duracao_s": round(time.time() - t0, 1),
           "edges": edges_out}
    corpo = json.dumps(out, sort_keys=True, separators=(",", ":")).encode()
    open(SAIDA, "wb").write(corpo)
    print("niveis:", níveis)
    print("estagios_L1:", estagios_L1)
    print("blocos_L1:", blocos_L1)
    print("nk_L1:", nk_L1)
    print("confusao:", conf)
    print("instancias:", inst_classes, "subtipos:", subtipos)
    print("verif exemplos:", verif)
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())

if __name__ == "__main__":
    main()
