# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS4.
ESPECIFICIDADE NA CLASSE III: medição pré-comprometida.

O resultado confirmatório permanece NEGATIVO e imutável. Este script NÃO lê
nem escreve artefactos confirmatórios, NÃO altera o instrumento congelado e
NÃO propõe classificador. Executa EXACTAMENTE o plano do ficheiro
precommit-ws4-classIII-especificidade.txt (depositado antes desta execução):
N=2000 famílias elegíveis, semente 910000020, instâncias III canónicas,
previsões P1..P8 derivadas ANTES de medir.
"""
import sys, json, time, hashlib, platform
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws4-classIII-specificity"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g            # congelado (12/12 vs MANIFEST, verificado)
import classificador as cl     # congelado

SEED = 910000020               # intervalo WS4; fixado no precommit
N_ALVO = 2000
MAX_TENTATIVAS = 200000
SAIDA = WS + "/ws4-classIII-medicao.json"

# arestas canal->processador no layout canónico III (n=10)
# (nome, bits_canal, bits_receptor, mem_bits, nome_M, shift_r, shift_c, shift_m)
ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5], "G0", 3, 6, 5),
           ("C_BA->A", [8, 9], [0, 1, 2], [2], "F0", 0, 8, 2))


def pc2(v):
    return bin(v).count("1")


def w_base(M):
    return [[sum(pc2(M[r][p] ^ M[r][q]) for r in range(4)) for q in range(4)]
            for p in range(4)]


def subs_canal(ints, bits_a):
    lo, hi = bits_a
    out = []
    for (mk, vl) in ints:
        mc = ((mk >> lo) & 1) | (((mk >> hi) & 1) << 1)
        vc = ((vl >> lo) & 1) | (((vl >> hi) & 1) << 1)
        out.append((mc, vc))
    return out


def analisa_aresta_completa(T, n, bits_a, bits_b, membits):
    """Réplica exacta da maquinaria congelada de C1' (fibra completa) +
    C2-eficácia e C3-suporte por contexto + baseline alinhado (bdep)."""
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    ints = cl.intervencoes(bits_a)
    Z0 = cl.estados_da_fibra(n, membits, 0)
    Z1 = cl.estados_da_fibra(n, membits, 1)
    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    nb = len(bits_b)
    d0, d1, dep = [], [], 0
    efic0, efic1 = [], []
    sig0 = [set() for _ in range(nb)]
    sig1 = [set() for _ in range(nb)]
    for (mk, vl) in ints:
        nxt0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]]
        nxt1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]]
        x0 = nxt0 ^ nx0
        x1 = nxt1 ^ nx1
        d0.append(int(popB[x0].sum()))
        d1.append(int(popB[x1].sum()))
        dep += int((x0 != x1).sum())
        efic0.append(tuple(bool(np.any((x0 >> k) & 1)) for k in range(nb)))
        efic1.append(tuple(bool(np.any((x1 >> k) & 1)) for k in range(nb)))
        for k in range(nb):
            sig0[k].add(((nxt0 >> k) & 1).astype(np.uint8).tobytes())
            sig1[k].add(((nxt1 >> k) & 1).astype(np.uint8).tobytes())
    if d0 == d1:
        nivel = "L1_d_iguais"
    elif cl.rank_canonico(d0) == cl.rank_canonico(d1):
        nivel = "L2_rank_igual_d_diferente"
    else:
        nivel = "L3_rank_diferente"
    supp0 = frozenset(k for k in range(nb) if len(sig0[k]) > 1)
    supp1 = frozenset(k for k in range(nb) if len(sig1[k]) > 1)
    bdep = int((nx0 != nx1).sum())
    return {"nivel": nivel, "dep_sites": dep, "d0": d0, "d1": d1,
            "efic_igual": efic0 == efic1,
            "supp_igual": supp0 == supp1,
            "bdep": bdep, "ints": ints}


def theta_sha(th):
    return hashlib.sha256(
        json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()


def main():
    t0 = time.time()
    ss = np.random.SeedSequence(SEED)
    rng_theta = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))

    rejeicoes = {}
    tentativa = 0
    registos = []
    anomalias = []

    # contadores de previsões (precommit A: P1..P7)
    C = {"arestas_total": 0,
         "P1_dep_zero": 0, "P1_dep_pos": 0,
         "P2_L1": 0, "P2_nao_L1": 0, "P2_d_igual": 0,
         "P3_formula_ok": 0, "P3_formula_falha": 0,
         "P4_efic_igual": 0, "P4_supp_igual": 0, "P4_falhas": 0,
         "P5_bdep_ok": 0, "P5_bdep_falha": 0, "P5_bdep_512": 0,
         "P5_sigma_diff": 0,
         "P6_ambos_contextos": 0, "P6_falha": 0,
         "P7_fact_ok": 0, "P7_fact_falha": 0,
         "P7_cnt_igual": 0, "P7_S_igual": 0, "P7_Snorm_igual": 0,
         "P7_cnt_igual_e_S_dif": 0,
         "d_max_zero": 0}
    delta_norms = {"C_AB->B": [], "C_BA->A": []}
    orb_lens = []
    exemplos = []

    while len(registos) < N_ALVO and tentativa < MAX_TENTATIVAS:
        tentativa += 1
        th = g.sample_theta_base(rng_theta)
        if th.pi[0] == th.pi[1]:
            rejeicoes["pi_identicas"] = rejeicoes.get("pi_identicas", 0) + 1
            continue
        ok, razao, _ = g.elegibilidade(th, False)
        if not ok:
            rejeicoes[razao] = rejeicoes.get(razao, 0) + 1
            continue

        tab, n, lay = g.tabela_transicao("III", th, False)
        T = np.asarray(tab, dtype=np.int64)
        s0 = g._campos_para_int(g.estado_inicial("III", th), lay)
        orb = cl.orbita(T, s0)
        V = np.asarray(orb, dtype=np.int64)
        orb_lens.append(len(orb))

        rec = {"fam": len(registos), "tentativa": tentativa,
               "theta_sha": theta_sha(th), "orbita": len(orb), "arestas": {}}

        for nome, ba, bb, mem, tn, sr, sc, sm in ARESTAS:
            C["arestas_total"] += 1
            r = analisa_aresta_completa(T, n, ba, bb, mem)
            M = th.G0 if tn == "G0" else th.F0
            WM = w_base(M)
            scn = subs_canal(r["ints"], ba)
            dpred = [32 * sum(WM[c][(c & ~mc) | vc] for c in range(4))
                     for (mc, vc) in scn]

            # P1/P2
            if r["dep_sites"] == 0:
                C["P1_dep_zero"] += 1
            else:
                C["P1_dep_pos"] += 1
            if r["nivel"] == "L1_d_iguais":
                C["P2_L1"] += 1
            else:
                C["P2_nao_L1"] += 1
            if r["d0"] == r["d1"]:
                C["P2_d_igual"] += 1
            # P3
            f_ok = (dpred == r["d0"] == r["d1"])
            C["P3_formula_ok" if f_ok else "P3_formula_falha"] += 1
            # P4
            if r["efic_igual"] and r["supp_igual"]:
                C["P4_efic_igual"] += int(r["efic_igual"])
                C["P4_supp_igual"] += int(r["supp_igual"])
            else:
                C["P4_efic_igual"] += int(r["efic_igual"])
                C["P4_supp_igual"] += int(r["supp_igual"])
                C["P4_falhas"] += 1
            # P5 baseline
            if tn == "G0":
                s_diff = th.sigmaB[0] != th.sigmaB[1]
                rows = sum(1 for q in range(4) if th.K[0][q] != th.K[1][q])
            else:
                s_diff = th.sigmaA[0] != th.sigmaA[1]
                rows = sum(1 for q in range(4) if th.H[0][q] != th.H[1][q])
            bpred = 512 if s_diff else 128 * rows
            C["P5_bdep_ok" if r["bdep"] == bpred else "P5_bdep_falha"] += 1
            C["P5_bdep_512"] += int(r["bdep"] == 512)
            C["P5_sigma_diff"] += int(s_diff)
            # sanidade: canal eficaz nalguma intervenção
            if max(r["d0"]) == 0:
                C["d_max_zero"] += 1
            # P6/P7 órbita
            mv = (V >> sm) & 1
            V0 = V[mv == 0]
            V1 = V[mv == 1]
            ambos = len(V0) > 0 and len(V1) > 0
            C["P6_ambos_contextos" if ambos else "P6_falha"] += 1
            eB = cl.extractor(bb, n)
            popB = cl.popcount_tab(len(bb))
            S0, S1 = [], []
            for (mk, vl) in r["ints"]:
                nxa = eB[T[V0]]
                nxb = eB[T[(V0 & ~np.int64(mk)) | np.int64(vl)]]
                S0.append(int(popB[nxb ^ nxa].sum()))
                nxa = eB[T[V1]]
                nxb = eB[T[(V1 & ~np.int64(mk)) | np.int64(vl)]]
                S1.append(int(popB[nxb ^ nxa].sum()))
            # factorização pelo Teorema III-1: S_m = sum_{r,c} Cnt_m[r][c]*resp_k[r][c]
            cnt = {}
            for mval, Vm in ((0, V0), (1, V1)):
                cm = np.zeros((4, 4), dtype=np.int64)
                if len(Vm):
                    rv = ((Vm >> sr) & 3).astype(np.int64)
                    cv = ((Vm >> sc) & 3).astype(np.int64)
                    np.add.at(cm, (rv, cv), 1)
                cnt[mval] = cm
            fact_ok = True
            for ki, (mc, vc) in enumerate(scn):
                resp = np.array([[pc2(M[rr][(cc & ~mc) | vc] ^ M[rr][cc])
                                  for cc in range(4)] for rr in range(4)],
                                dtype=np.int64)
                if int((cnt[0] * resp).sum()) != S0[ki] or \
                   int((cnt[1] * resp).sum()) != S1[ki]:
                    fact_ok = False
            C["P7_fact_ok" if fact_ok else "P7_fact_falha"] += 1
            cnt_igual = bool((cnt[0] == cnt[1]).all())
            s_igual = (S0 == S1)
            snorm_igual = ambos and all(S0[k] * len(V1) == S1[k] * len(V0)
                                        for k in range(len(S0)))
            C["P7_cnt_igual"] += int(cnt_igual)
            C["P7_S_igual"] += int(s_igual)
            C["P7_Snorm_igual"] += int(snorm_igual)
            if cnt_igual and not s_igual:
                C["P7_cnt_igual_e_S_dif"] += 1
            dnorm = 0.0
            if ambos:
                dnorm = max(abs(S0[k] / len(V0) - S1[k] / len(V1))
                            for k in range(len(S0)))
            delta_norms[nome].append(round(dnorm, 6))

            ok_all = (r["dep_sites"] == 0 and r["nivel"] == "L1_d_iguais"
                      and f_ok and r["efic_igual"] and r["supp_igual"]
                      and r["bdep"] == bpred and ambos and fact_ok)
            rec["arestas"][nome] = {
                "dep_sites": r["dep_sites"], "nivel": r["nivel"],
                "formula_ok": f_ok, "efic_igual": r["efic_igual"],
                "supp_igual": r["supp_igual"], "bdep": r["bdep"],
                "bdep_previsto": bpred, "sigma_diff": bool(s_diff),
                "mem_rows_dif": rows, "V0": int(len(V0)), "V1": int(len(V1)),
                "cnt_igual": cnt_igual, "S_igual": s_igual,
                "Snorm_igual": bool(snorm_igual),
                "delta_norm": round(dnorm, 6), "fact_ok": fact_ok}
            if not ok_all:
                anomalias.append({"fam": rec["fam"], "tentativa": tentativa,
                                  "theta_sha": rec["theta_sha"], "aresta": nome,
                                  "detalhe": {"d0": r["d0"], "d1": r["d1"],
                                              "dpred": dpred,
                                              "aresta_rec": rec["arestas"][nome]}})
            if len(exemplos) < 6:
                exemplos.append({"fam": rec["fam"], "aresta": nome,
                                 "d0": r["d0"], "d1": r["d1"], "dpred": dpred,
                                 "S0": S0, "S1": S1,
                                 "V0": int(len(V0)), "V1": int(len(V1)),
                                 "bdep": r["bdep"]})
        registos.append(rec)
        if len(registos) % 200 == 0:
            print("progresso: %d aceites, %d tentativas, %.0fs"
                  % (len(registos), tentativa, time.time() - t0), flush=True)

    total = len(registos)
    n_inst_dep_pos = sum(1 for r in registos
                         if any(a["dep_sites"] > 0
                                for a in r["arestas"].values()))
    n_inst_nao_L1 = sum(1 for r in registos
                        if any(a["nivel"] != "L1_d_iguais"
                               for a in r["arestas"].values()))

    def ic_zero(nn):
        return None if nn == 0 else 1.0 - 0.05 ** (1.0 / nn)

    def q(v, p):
        vs = sorted(v)
        return vs[min(len(vs) - 1, int(p * len(vs)))] if vs else None

    resumo_dnorm = {}
    for nome, v in delta_norms.items():
        nz = [x for x in v if x > 0]
        resumo_dnorm[nome] = {
            "n": len(v), "zeros": len(v) - len(nz),
            "mediana": q(v, 0.5), "p90": q(v, 0.9), "max": max(v) if v else None}

    try:
        sha_script = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    except Exception:
        sha_script = None

    saida = {
        "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
        "workstream": "ws4-classIII-specificity",
        "objectivo": "especificidade da classe III face a dependencia de memoria de alta resolucao",
        "precommit": "precommit-ws4-classIII-especificidade.txt (depositado antes desta execucao)",
        "semente_exploratoria": SEED,
        "fluxo": "SeedSequence(910000020).spawn(4)[0] = theta nuclear (como gerar_lote); [1..3] nao usados",
        "n_alvo": N_ALVO,
        "aceites": total,
        "tentativas": tentativa,
        "taxa_aceitacao": (total / tentativa) if tentativa else None,
        "rejeicoes": rejeicoes,
        "contadores_previsoes": C,
        "P_dep_pos_por_instancia": {
            "ocorrencias": n_inst_dep_pos, "N": total,
            "IC95_unilateral_superior_se_zero": ic_zero(total)},
        "P_dep_pos_por_aresta": {
            "ocorrencias": C["P1_dep_pos"], "N": C["arestas_total"],
            "IC95_unilateral_superior_se_zero": ic_zero(C["arestas_total"])},
        "P_nao_L1_por_instancia": {
            "ocorrencias": n_inst_nao_L1, "N": total,
            "IC95_unilateral_superior_se_zero": ic_zero(total)},
        "orbitas": {"min": min(orb_lens) if orb_lens else None,
                    "mediana": q(orb_lens, 0.5),
                    "max": max(orb_lens) if orb_lens else None},
        "delta_norm_orbita": resumo_dnorm,
        "anomalias": anomalias,
        "n_anomalias": len(anomalias),
        "exemplos": exemplos,
        "registos": registos,
        "duracao_s": round(time.time() - t0, 1),
        "ambiente": {"python": platform.python_version(),
                     "numpy": np.__version__,
                     "plataforma": platform.platform()},
        "sha256_script": sha_script,
    }
    corpo = json.dumps(saida, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)

    print("\n===== RESUMO WS4 (III, N=%d, seed %d) =====" % (total, SEED))
    print("tentativas %d, taxa aceitacao %.3f, duracao %.1fs"
          % (tentativa, total / tentativa if tentativa else 0,
             saida["duracao_s"]))
    print("P1 dep=0            : %d/%d arestas (dep>0: %d)"
          % (C["P1_dep_zero"], C["arestas_total"], C["P1_dep_pos"]))
    print("P2 nivel L1         : %d/%d (nao-L1: %d; d0==d1: %d)"
          % (C["P2_L1"], C["arestas_total"], C["P2_nao_L1"], C["P2_d_igual"]))
    print("P3 formula exacta   : ok %d / falha %d"
          % (C["P3_formula_ok"], C["P3_formula_falha"]))
    print("P4 C2/C3 contexto   : efic_igual %d, supp_igual %d, falhas %d"
          % (C["P4_efic_igual"], C["P4_supp_igual"], C["P4_falhas"]))
    print("P5 baseline         : bdep ok %d / falha %d; bdep=512: %d; sigma_diff: %d"
          % (C["P5_bdep_ok"], C["P5_bdep_falha"], C["P5_bdep_512"],
             C["P5_sigma_diff"]))
    print("P6 ambos contextos  : %d/%d (falhas %d)"
          % (C["P6_ambos_contextos"], C["arestas_total"], C["P6_falha"]))
    print("P7 orbita           : fact_ok %d/falha %d; cnt_igual %d; S_igual %d; Snorm_igual %d; cnt_igual&S_dif %d"
          % (C["P7_fact_ok"], C["P7_fact_falha"], C["P7_cnt_igual"],
             C["P7_S_igual"], C["P7_Snorm_igual"], C["P7_cnt_igual_e_S_dif"]))
    print("d_max==0 (sanidade) :", C["d_max_zero"])
    print("delta_norm orbita   :", json.dumps(resumo_dnorm))
    print("instancias com dep>0:", n_inst_dep_pos,
          " IC95 sup (se 0):", saida["P_dep_pos_por_instancia"]["IC95_unilateral_superior_se_zero"])
    print("anomalias           :", len(anomalias))
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
    print("sha256_script:", sha_script)


if __name__ == "__main__":
    main()
