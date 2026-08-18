# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS2 (information loss).
Script G (precommit-ws2-v2.txt, ponto 2b): identificação do operador F por nível.
 (i)   testemunhas concretas X0!=X1 -> F(X0)=F(X1) por estágio (B1, B2, B3, hist
       global com s1>0, e L2 ordinal) — extraídas analiticamente dos thetas já
       replayados (casos pré-comprometidos);
 (ii)  caracterização analítica do estágio F1_pc_pontual nas 705 arestas L1:
       {s1==0} ⟺ {tau ∈ ∩_r Iso(w_r)}, w_r(p,q)=pc2(M[r][p]^M[r][q]);
       replay determinístico dos thetas das famílias L1 (sementes REGISTADAS);
 (iii) corolários do lema das somas-linha em TODAS as 20000 arestas:
       multiset{d[5..8]} invariante entre contextos; bloco completo pontualmente
       fixo em L2; contagem de permutações do bloco completo em L3;
 (iv)  refinamento das 174 arestas F1.5: só blocos <=B2 (permutação intra-bloco)
       vs >=1 bloco B3 (compensação entre blocos no histograma global);
 (v)   fibra da ordinalização restrita às 225 arestas L2 (pares (d0,d1) distintos,
       padrões, vetores por padrão).
NENHUMA amostra nova; nenhuma semente nova. Escreve apenas no ws2 dir.
"""
import sys, json, hashlib, itertools
from collections import Counter
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws2-information-loss"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

SAIDA = WS + "/ws2-operator-findings.json"
PC2 = [bin(v).count("1") for v in range(4)]
SUBS = [(int(mk), int(vl)) for (mk, vl) in cl.intervencoes([0, 1])]


def tau_de(pi0, pi1):
    inv0 = [0] * 4
    for c, p in enumerate(pi0):
        inv0[p] = c
    return tuple(pi1[inv0[p]] for p in range(4))


def cells(M, pim):
    """D[k][c][r] = M[r][pim c] ^ M[r][pim sub_k(c)] (forma fechada verificada
    sítio-a-sítio no Script B)."""
    Mp = [[M[r][pim[c]] for c in range(4)] for r in range(4)]
    out = []
    for (mc, vc) in SUBS:
        out.append([[Mp[r][c] ^ Mp[r][(c & ~mc) | vc] for r in range(4)]
                    for c in range(4)])
    return out


def w_rows(M):
    return [[[PC2[M[r][p] ^ M[r][q]] for q in range(4)] for p in range(4)]
            for r in range(4)]


def main():
    pop = json.load(open(WS + "/ws2-population-stages.json"))
    cases = json.load(open(WS + "/ws2-cases-sitelevel.json"))
    thetas = json.load(open(WS + "/ws2-thetas-cases.json"))["thetas"]
    edges = pop["edges"]
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "descricao": "operador F por nivel: testemunhas, caracterizacao F1, "
                        "corolarios somas-linha, refinamento F1.5, fibra L2"}

    # ---------------- (i) testemunhas -----------------------------------
    Mname = {"C_AB->B": "G0", "C_BA->A": "F0"}
    wit = {}

    def edge_theta(ar):
        th_d = thetas["%d:%d" % (ar["seed"], ar["tentativa"])]
        return th_d[Mname[ar["nome"]]], th_d["pi"]

    def find_edge(pred):
        for ar in cases["arestas"]:
            if pred(ar):
                return ar
        return None

    # B1: estágio F1_pc_pontual — padrões diferem, pc pontual igual
    ar = find_edge(lambda a: a.get("estagio_perda_L1") == "F1_pc_pontual")
    if ar:
        M, pi = edge_theta(ar)
        D0, D1 = cells(M, pi[0]), cells(M, pi[1])
        for k in range(9):
            for c in range(4):
                for r in range(4):
                    if D0[k][c][r] != D1[k][c][r]:
                        assert PC2[D0[k][c][r]] == PC2[D1[k][c][r]]
                        wit["B1_pc_pontual"] = {
                            "aresta": {kk: ar[kk] for kk in ("seed", "fam", "nome")},
                            "celula": {"k": k, "sub_k": SUBS[k], "c": c, "r": r},
                            "X0": D0[k][c][r], "X1": D1[k][c][r],
                            "pc": PC2[D0[k][c][r]],
                            "nota": "padroes de bits diferentes, popcount igual: "
                                    "F_pc destroi a identidade dos bits"}
                        break
                if "B1_pc_pontual" in wit:
                    break
            if "B1_pc_pontual" in wit:
                break

    # B2 + histograma global: estágio F1.5
    ar = find_edge(lambda a: a.get("estagio_perda_L1") == "F1.5_histograma")
    if ar:
        M, pi = edge_theta(ar)
        D0, D1 = cells(M, pi[0]), cells(M, pi[1])
        for k in range(9):
            for c in range(4):
                p0 = [PC2[D0[k][c][r]] for r in range(4)]
                p1 = [PC2[D1[k][c][r]] for r in range(4)]
                if p0 != p1 and sorted(p0) == sorted(p1):
                    wit["B2_permutacao_intra_bloco"] = {
                        "aresta": {kk: ar[kk] for kk in ("seed", "fam", "nome")},
                        "bloco": {"k": k, "sub_k": SUBS[k], "c": c},
                        "pc_por_r_m0": p0, "pc_por_r_m1": p1,
                        "nota": "vetor de pc por r difere; multiconjunto igual: "
                                "a soma na fibra e cega a permutacoes de sitios"}
                    break
            if "B2_permutacao_intra_bloco" in wit:
                break
        pk = next((p for p in ar["per_k"] if p["s1_pc_diferente"] > 0
                   and p["eq_hist"]), None)
        if pk:
            wit["hist_global_igual_pc_pontual_diferente"] = {
                "aresta": {kk: ar[kk] for kk in ("seed", "fam", "nome")},
                "k": pk["k"], "s1_sitios_pc_diferente": pk["s1_pc_diferente"],
                "hist0": pk["hist0"], "hist1": pk["hist1"], "d": pk["d0"]}

    # B3: exemplar F2_soma_por_bloco (o exemplar verboso se existir)
    ar = find_edge(lambda a: a.get("exemplar_verboso")) or \
        find_edge(lambda a: a.get("estagio_perda_L1") == "F2_soma_por_bloco")
    if ar:
        M, pi = edge_theta(ar)
        D0, D1 = cells(M, pi[0]), cells(M, pi[1])
        for k in range(9):
            for c in range(4):
                p0 = [PC2[D0[k][c][r]] for r in range(4)]
                p1 = [PC2[D1[k][c][r]] for r in range(4)]
                if sorted(p0) != sorted(p1) and sum(p0) == sum(p1):
                    wit["B3_cancelamento_na_soma"] = {
                        "aresta": {kk: ar[kk] for kk in ("seed", "fam", "nome")},
                        "bloco": {"k": k, "sub_k": SUBS[k], "c": c},
                        "pc_por_r_m0": p0, "pc_por_r_m1": p1,
                        "soma_bloco": sum(p0),
                        "nota": "multiconjuntos de pc diferem; somas iguais: "
                                "perda estritamente na agregacao linear"}
                    break
            if "B3_cancelamento_na_soma" in wit:
                break
        pk = next((p for p in ar["per_k"] if not p["eq_hist"]), None)
        if pk:
            wit["hist_global_diferente_soma_igual"] = {
                "aresta": {kk: ar[kk] for kk in ("seed", "fam", "nome")},
                "k": pk["k"], "hist0": pk["hist0"], "hist1": pk["hist1"],
                "d0": pk["d0"], "d1": pk["d1"]}

    # L2: ordinalização
    ar = find_edge(lambda a: a["nivel"] == "L2")
    if ar:
        d0, d1 = ar["d0"], ar["d1"]
        wit["L2_ordinalizacao"] = {
            "aresta": {kk: ar[kk] for kk in ("seed", "fam", "nome")},
            "d0": d0, "d1": d1,
            "k_mudados": [k for k in range(9) if d0[k] != d1[k]],
            "deltas": [d1[k] - d0[k] for k in range(9) if d0[k] != d1[k]],
            "rank_comum": ar["rank0"],
            "nota": "d0 != d1; rank_canonico identico: F_rank destroi magnitude "
                    "cardinal dentro da mesma celula de ordem"}
    out["testemunhas"] = wit

    # ---------------- (ii) caracterizacao F1 nas 705 L1 ------------------
    fam_l1 = {}
    for e in edges:
        if e["n"] == "L1":
            fam_l1.setdefault((e["s"], e["t"]), []).append(e)
    need = {}
    for (s, t) in fam_l1:
        need.setdefault(s, set()).add(t)
    th_by = {}
    for seed in sorted(need):
        wanted = need[seed]
        tmax = max(wanted)
        rng = np.random.Generator(np.random.PCG64(
            np.random.SeedSequence(seed).spawn(4)[0]))
        for t in range(1, tmax + 1):
            th = g.sample_theta_base(rng)
            if t in wanted:
                th_by[(seed, t)] = th
    conf = {"s1_0_e_isoall": 0, "s1_0_sem_isoall": 0,
            "isoall_com_s1_pos": 0, "nem_um_nem_outro": 0}
    iso_sizes = Counter()
    stage_by_isoall = Counter()
    for (s, t), lst in fam_l1.items():
        th = th_by[(s, t)]
        tau = tau_de(th.pi[0], th.pi[1])
        for e in lst:
            M = th.G0 if e["e"] == "C_AB->B" else th.F0
            wr = w_rows(M)
            iso_all = all(wr[r][tau[a]][tau[b]] == wr[r][a][b]
                          for r in range(4) for a in range(4) for b in range(4))
            grp = sum(1 for p in itertools.permutations(range(4))
                      if all(wr[r][p[a]][p[b]] == wr[r][a][b]
                             for r in range(4) for a in range(4) for b in range(4)))
            iso_sizes[grp] += 1
            z = (e["s1"] == 0)
            if z and iso_all:
                conf["s1_0_e_isoall"] += 1
            elif z:
                conf["s1_0_sem_isoall"] += 1
            elif iso_all:
                conf["isoall_com_s1_pos"] += 1
            else:
                conf["nem_um_nem_outro"] += 1
            if iso_all:
                stage_by_isoall[e["st"]] += 1
    out["F1_caracterizacao"] = {
        "definicao": "iso_all := tau ∈ ∩_r Iso(w_r); previsao: s1==0 ⟺ iso_all",
        "confusao": conf,
        "estagios_das_arestas_iso_all": dict(stage_by_isoall),
        "tamanho_grupo_∩Iso(w_r)_nas_L1": dict(sorted(iso_sizes.items()))}

    # ---------------- (iii) corolarios somas-linha, 20000 arestas ---------
    viol_multiset = 0
    full_pointwise_changed = Counter()
    soma_full_dif = 0
    for e in edges:
        d0 = e["d0"]
        d1 = e.get("d1", d0)
        if sorted(d0[5:9]) != sorted(d1[5:9]):
            viol_multiset += 1
        if sum(d0[5:9]) != sum(d1[5:9]):
            soma_full_dif += 1
        if any(d0[i] != d1[i] for i in range(5, 9)):
            full_pointwise_changed[e["n"]] += 1
    out["corolarios_somas_linha"] = {
        "arestas": len(edges),
        "violacoes_multiset_bloco_completo": viol_multiset,
        "violacoes_soma_bloco_completo": soma_full_dif,
        "bloco_completo_pontualmente_mudado_por_nivel":
            dict(full_pointwise_changed),
        "nota": "multiset{d[5..8]} e Σd[5..8] sao invariantes exactos entre "
                "contextos (lema: bloco completo de m=1 e permutacao rho do de "
                "m=0); esperado 0 e 0; em L2 esperado bloco fixo pontualmente"}

    # ---------------- (iv) refinamento F1.5 ------------------------------
    f15 = [e for e in edges if e["n"] == "L1" and e.get("st") == "F1.5_histograma"]
    so_b2 = sum(1 for e in f15 if e["bl"]["B3"] == 0 and e["bl"]["B4"] == 0)
    com_b3 = sum(1 for e in f15 if e["bl"]["B3"] > 0)
    f2 = [e for e in edges if e["n"] == "L1" and e.get("st") == "F2_soma_por_bloco"]
    f2_com_b2 = sum(1 for e in f2 if e["bl"]["B2"] > 0)
    f2_nk = Counter()
    for e in f2:
        f2_nk[e["nk"]["igual_so_S2_soma"]] += 1
    out["refinamento_F15_F2"] = {
        "F1.5_total": len(f15),
        "F1.5_so_permutacao_intra_bloco(B<=B2)": so_b2,
        "F1.5_com_bloco_B3_compensado_entre_blocos": com_b3,
        "F2_total": len(f2),
        "F2_com_algum_bloco_B2": f2_com_b2,
        "F2_n_intervencoes_igual_so_na_soma_dist": dict(sorted(f2_nk.items()))}

    # ---------------- (v) fibra L2 ---------------------------------------
    L2 = [e for e in edges if e["n"] == "L2"]
    pares = {(tuple(e["d0"]), tuple(e["d1"])) for e in L2}
    por_rank = {}
    for e in L2:
        rk = tuple(cl.rank_canonico(e["d0"]))
        por_rank.setdefault(rk, set()).update([tuple(e["d0"]), tuple(e["d1"])])
    out["fibra_L2"] = {
        "n_arestas": len(L2),
        "pares_(d0,d1)_distintos": len(pares),
        "padroes_rank_L2": len(por_rank),
        "vetores_distintos_por_padrao": dict(sorted(Counter(
            len(v) for v in por_rank.values()).items())),
        "max_vetores_num_padrao": max(len(v) for v in por_rank.values())}

    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print(json.dumps({k: out[k] for k in
                      ("F1_caracterizacao", "corolarios_somas_linha",
                       "refinamento_F15_F2", "fibra_L2")}, indent=1))
    print("testemunhas:", sorted(wit))
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
