# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS4 (2.ª passagem).
EXTENSÃO HORIZONTE 2 (adenda, secção B): T2 = T∘T, mesma maquinaria congelada,
MESMA amostra determinística (seed 910000020, N=2000; identidade verificada
por theta_sha contra a 1.ª passagem). Teorema III-2 e previsões PH1-PH4
enunciados no precommit ANTES desta execução.
O estatístico de horizonte 2 é exploratório e NÃO pertence ao instrumento
congelado (semântica congelada: UMA transição global). O resultado
confirmatório permanece NEGATIVO e imutável. Nenhuma proposta de correcção.
"""
import sys, json, time, hashlib, math, platform
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws4-classIII-specificity"
sys.path.insert(0, DST + "/frozen-copy")
sys.path.insert(0, WS)
import gerador as g
import classificador as cl
import medicao_ws4_classIII as m1

SEED = 910000020
N_ALVO = 2000
MAX_TENTATIVAS = 200000
SAIDA = WS + "/ws4-horizonte2.json"


def pc(v):
    return bin(v).count("1")


def d2_fechada(M, Kx, s_m, k_row, scn):
    """Forma fechada do Teorema III-2 (precommit adenda, B3).
    M 4x4 -> 0..3; Kx 2x4 -> 0..1; s_m escalar; k_row = Kx[m] (linha m)."""
    out = []
    for (mc, vc) in scn:
        tot = 0
        for r in range(4):
            km = k_row[r]
            for c in range(4):
                a = M[r][(c & ~mc) | vc] ^ s_m
                b = M[r][c] ^ s_m
                for o in range(4):
                    tot += pc(M[a][o] ^ M[b][o])
                tot += 4 * pc(Kx[km][a] ^ Kx[km][b])
        out.append(8 * tot)
    return out


def cp_ci(k, n, alpha=0.05):
    """Clopper-Pearson bilateral exacto via CDF binomial (lgamma) + bissecção."""
    def logC(n_, i_):
        return (math.lgamma(n_ + 1) - math.lgamma(i_ + 1)
                - math.lgamma(n_ - i_ + 1))

    def tail_ge(k_, n_, p_):     # P(X >= k_)
        if p_ <= 0.0:
            return 0.0 if k_ > 0 else 1.0
        if p_ >= 1.0:
            return 1.0
        s = 0.0
        for i in range(k_, n_ + 1):
            s += math.exp(logC(n_, i) + i * math.log(p_)
                          + (n_ - i) * math.log(1 - p_))
        return min(s, 1.0)

    def tail_le(k_, n_, p_):     # P(X <= k_)
        if p_ <= 0.0:
            return 1.0
        if p_ >= 1.0:
            return 0.0 if k_ < n_ else 1.0
        s = 0.0
        for i in range(0, k_ + 1):
            s += math.exp(logC(n_, i) + i * math.log(p_)
                          + (n_ - i) * math.log(1 - p_))
        return min(s, 1.0)

    if k == 0:
        lo = 0.0
    elif k == n:
        lo = (alpha / 2) ** (1.0 / n)
    else:
        a, b = 0.0, 1.0
        for _ in range(80):
            mid = (a + b) / 2
            if tail_ge(k, n, mid) < alpha / 2:
                a = mid
            else:
                b = mid
        lo = (a + b) / 2
    if k == n:
        hi = 1.0
    elif k == 0:
        hi = 1.0 - (alpha / 2) ** (1.0 / n)
    else:
        a, b = 0.0, 1.0
        for _ in range(80):
            mid = (a + b) / 2
            if tail_le(k, n, mid) > alpha / 2:
                a = mid
            else:
                b = mid
        hi = (a + b) / 2
    return lo, hi


def main():
    t0 = time.time()
    pass1 = json.load(open(WS + "/ws4-classIII-medicao.json"))
    regs1 = pass1["registos"]
    assert len(regs1) == N_ALVO

    ss = np.random.SeedSequence(SEED)
    rng = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))

    tentativa = 0
    registos = []
    sha_iguais = 0
    dep2_all = {"C_AB->B": [], "C_BA->A": []}
    niveis2 = {"C_AB->B": {}, "C_BA->A": {}}
    formula2_ok = 0
    formula2_falha = 0
    dep2_zero_detalhe = []
    anomalias = []

    while len(registos) < N_ALVO and tentativa < MAX_TENTATIVAS:
        tentativa += 1
        th = g.sample_theta_base(rng)
        if th.pi[0] == th.pi[1]:
            continue
        ok, _, _ = g.elegibilidade(th, False)
        if not ok:
            continue

        i = len(registos)
        sha = m1.theta_sha(th)
        if regs1[i]["theta_sha"] == sha and regs1[i]["tentativa"] == tentativa:
            sha_iguais += 1
        else:
            anomalias.append({"fam": i, "campo": "corrente_divergente",
                              "tentativa": tentativa})

        tab, n, lay = g.tabela_transicao("III", th, False)
        T = np.asarray(tab, dtype=np.int64)
        T2 = T[T]

        rec = {"fam": i, "tentativa": tentativa, "theta_sha": sha,
               "arestas": {}}
        for nome, ba, bb, mem, tn, sr, sc, sm in m1.ARESTAS:
            r = m1.analisa_aresta_completa(T2, n, ba, bb, mem)
            scn = m1.subs_canal(r["ints"], ba)
            if tn == "G0":
                M, Kx = th.G0, th.K
                sig = th.sigmaB
                rows = sum(1 for q in range(4) if th.K[0][q] != th.K[1][q])
                s_diff = th.sigmaB[0] != th.sigmaB[1]
            else:
                M, Kx = th.F0, th.H
                sig = th.sigmaA
                rows = sum(1 for q in range(4) if th.H[0][q] != th.H[1][q])
                s_diff = th.sigmaA[0] != th.sigmaA[1]
            dp0 = d2_fechada(M, Kx, sig[0], Kx[0], scn)
            dp1 = d2_fechada(M, Kx, sig[1], Kx[1], scn)
            f_ok = (dp0 == r["d0"] and dp1 == r["d1"])
            if f_ok:
                formula2_ok += 1
            else:
                formula2_falha += 1
                anomalias.append({"fam": i, "aresta": nome,
                                  "campo": "formula2",
                                  "d2_0": r["d0"], "dp0": dp0,
                                  "d2_1": r["d1"], "dp1": dp1})
            rec["arestas"][nome] = {
                "dep2_sites": r["dep_sites"], "d2_0": r["d0"],
                "d2_1": r["d1"], "nivel2": r["nivel"],
                "formula2_ok": f_ok, "mem_rows_dif": rows,
                "sigma_diff": bool(s_diff)}
            dep2_all[nome].append(r["dep_sites"])
            niveis2[nome][r["nivel"]] = niveis2[nome].get(r["nivel"], 0) + 1
            if r["dep_sites"] == 0:
                dep2_zero_detalhe.append({
                    "fam": i, "theta_sha": sha, "aresta": nome,
                    "nivel2": r["nivel"], "mem_rows_dif": rows,
                    "sigma_diff": bool(s_diff), "d2_0": r["d0"],
                    "d2_1": r["d1"]})
        registos.append(rec)
        if len(registos) % 400 == 0:
            print("progresso: %d aceites, %d tentativas, %.0fs"
                  % (len(registos), tentativa, time.time() - t0), flush=True)

    total = len(registos)
    todos = dep2_all["C_AB->B"] + dep2_all["C_BA->A"]
    n_ar = len(todos)
    k_ar = sum(1 for d in todos if d > 0)
    inst_alguma = sum(1 for r in registos
                      if any(a["dep2_sites"] > 0 for a in r["arestas"].values()))
    inst_ambas = sum(1 for r in registos
                     if all(a["dep2_sites"] > 0 for a in r["arestas"].values()))

    def qs(v):
        s = sorted(v)
        if not s:
            return None
        def q(p):
            return s[min(len(s) - 1, int(p * len(s)))]
        return {"min": s[0], "p25": q(0.25), "mediana": q(0.5),
                "p75": q(0.75), "max": s[-1]}

    ci_ar = cp_ci(k_ar, n_ar)
    ci_alguma = cp_ci(inst_alguma, total)
    ci_ambas = cp_ci(inst_ambas, total)

    saida = {
        "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
        "workstream": "ws4-classIII-specificity",
        "fase": "adenda 2a passagem — horizonte 2 (T2=T∘T); estatistico exploratorio, NAO pertence ao instrumento congelado",
        "precommit": "precommit-ws4-adenda-h2-auditoria.txt",
        "semente": SEED, "n_alvo": N_ALVO, "aceites": total,
        "tentativas": tentativa,
        "corrente_identica_1a_passagem": {"iguais": sha_iguais, "N": total},
        "PH1_dep2_pos_por_aresta": {"ocorrencias": k_ar, "N": n_ar,
                                    "proporcao": k_ar / n_ar if n_ar else None,
                                    "IC95_clopper_pearson": ci_ar},
        "PH1_dep2_pos_por_instancia_alguma_aresta": {
            "ocorrencias": inst_alguma, "N": total,
            "IC95_clopper_pearson": ci_alguma},
        "PH1_dep2_pos_por_instancia_ambas_arestas": {
            "ocorrencias": inst_ambas, "N": total,
            "IC95_clopper_pearson": ci_ambas},
        "PH2_formula2": {"ok": formula2_ok, "falha": formula2_falha},
        "PH3_niveis2": niveis2,
        "PH4_dep2_quantis": {nome: qs(v) for nome, v in dep2_all.items()},
        "PH4_dep2_quantis_global": qs(todos),
        "dep2_zero_detalhe": dep2_zero_detalhe,
        "n_dep2_zero": len(dep2_zero_detalhe),
        "anomalias": anomalias, "n_anomalias": len(anomalias),
        "registos": registos,
        "duracao_s": round(time.time() - t0, 1),
        "ambiente": {"python": platform.python_version(),
                     "numpy": np.__version__,
                     "plataforma": platform.platform()},
    }
    try:
        saida["sha256_script"] = hashlib.sha256(
            open(__file__, "rb").read()).hexdigest()
    except Exception:
        saida["sha256_script"] = None
    corpo = json.dumps(saida, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)

    print("\n===== RESUMO WS4 HORIZONTE 2 (III, N=%d, seed %d) =====" % (total, SEED))
    print("corrente identica 1a passagem:", sha_iguais, "/", total)
    print("PH1 dep2>0 por aresta      : %d/%d (%.4f) IC95 [%.6f, %.6f]"
          % (k_ar, n_ar, k_ar / n_ar, ci_ar[0], ci_ar[1]))
    print("PH1 por instancia (alguma) : %d/%d IC95 [%.6f, %.6f]"
          % (inst_alguma, total, ci_alguma[0], ci_alguma[1]))
    print("PH1 por instancia (ambas)  : %d/%d IC95 [%.6f, %.6f]"
          % (inst_ambas, total, ci_ambas[0], ci_ambas[1]))
    print("PH2 formula2 exacta        : ok %d / falha %d"
          % (formula2_ok, formula2_falha))
    print("PH3 niveis2                :", json.dumps(niveis2, sort_keys=True))
    print("PH4 dep2 quantis           :",
          json.dumps(saida["PH4_dep2_quantis"], sort_keys=True))
    print("dep2==0 detalhe (n=%d)     :" % len(dep2_zero_detalhe),
          json.dumps(dep2_zero_detalhe)[:900])
    print("anomalias                  :", len(anomalias))
    print("duracao_s:", saida["duracao_s"])
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
    print("sha256_script:", saida["sha256_script"])


if __name__ == "__main__":
    main()
