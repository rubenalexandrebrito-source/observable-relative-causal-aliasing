# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY - Pre-registo A v8.3, Fase 6, WS5.
Correlacao entre arestas no colapso duplo: escada de modelos
  M0 independencia total
  M1 tau partilhado, so classe de conjugacao (replica/estende agente unico)
  M2 tau partilhado + lam partilhado (7 celulas = orbitas D4; derivacao WS5)
  M3 geometria exacta por familia: P(colapso|W_B,W_A,pi0) = (|EqB∩EqA|-1)/23
para ambos os alvos: colapso 'estado' (46) e colapso both-L1 (29).
Diagnosticos de elegibilidade (tilt) e efeito-lam em L2 por celula.
Le apenas ws5-familias-N10000.json; escreve apenas no ws dir.
"""
import json, hashlib, math

WS = "/root/causal-A-postconfirmatory-analysis/multiagent/ws5-failure-structure"
SAIDA = WS + "/ws5-correlacao.json"

CLASSE_DE_CELL = {"T_in": "T", "T_out": "T", "DT_lam": "DT", "DT_oth": "DT",
                  "FC_lam": "FC", "FC_oth": "FC", "C3": "C3"}


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 6), round((c + h) / d, 6)]


def fisher_2x2(a, b, c, d):
    """p bicaudal exacto para tabela [[a,b],[c,d]] (linha=aresta-B estado?,
    coluna=aresta-A estado?) ou comparacao de duas taxas."""
    n = a + b + c + d
    r1, c1 = a + b, a + c
    lo = max(0, r1 + c1 - n)
    hi = min(r1, c1)
    def pmf(x):
        return (math.comb(c1, x) * math.comb(n - c1, r1 - x)
                / math.comb(n, r1))
    pobs = pmf(a)
    return sum(pmf(x) for x in range(lo, hi + 1) if pmf(x) <= pobs * (1 + 1e-12))


def main():
    fams = json.load(open(WS + "/ws5-familias-N10000.json"))["familias"]
    N = len(fams)
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY", "ws": "ws5",
           "resultado_confirmatorio": "negativo (imutavel)", "N": N}

    for f in fams:
        f["estB"] = int(f["nivB"] != "L3")
        f["estA"] = int(f["nivA"] != "L3")
        f["l1B"] = int(f["nivB"] == "L1")
        f["l1A"] = int(f["nivA"] == "L1")
        f["l2B"] = int(f["nivB"] == "L2")
        f["l2A"] = int(f["nivA"] == "L2")

    def escada(chB, chA, alvo_nome):
        nB = sum(f[chB] for f in fams)
        nA = sum(f[chA] for f in fams)
        obs = sum(f[chB] * f[chA] for f in fams)
        m0 = nB * nA / N
        # por classe
        por = {}
        for f in fams:
            cl_ = CLASSE_DE_CELL[f["cell"]]
            r = por.setdefault(cl_, [0, 0, 0, 0])   # n, B, A, ambos
            r[0] += 1; r[1] += f[chB]; r[2] += f[chA]; r[3] += f[chB] * f[chA]
        m1 = sum(r[1] * r[2] / r[0] for r in por.values())
        porc = {}
        for f in fams:
            r = porc.setdefault(f["cell"], [0, 0, 0, 0])
            r[0] += 1; r[1] += f[chB]; r[2] += f[chA]; r[3] += f[chB] * f[chA]
        m2 = sum(r[1] * r[2] / r[0] for r in porc.values())
        return {"alvo": alvo_nome, "obs": obs,
                "n_aresta_B": nB, "n_aresta_A": nA,
                "M0_indep": round(m0, 3),
                "M1_classe": round(m1, 3),
                "M2_celula7": round(m2, 3),
                "razao_obs_M0": round(obs / m0, 3),
                "razao_M1_M0": round(m1 / m0, 3),
                "razao_M2_M0": round(m2 / m0, 3),
                "tabela_por_classe": {k: {"n": r[0], "B": r[1], "A": r[2],
                                          "ambos": r[3]}
                                      for k, r in sorted(por.items())},
                "tabela_por_celula": {k: {"n": r[0], "B": r[1], "A": r[2],
                                          "ambos": r[3]}
                                      for k, r in sorted(porc.items())}}

    esc_est = escada("estB", "estA", "estado=L1uL2 (colapso C1', 46)")
    esc_l1 = escada("l1B", "l1A", "both-L1 (29)")

    # M3 geometria exacta por familia
    def m3(campo, obs):
        soma = 0.0
        var = 0.0
        for f in fams:
            p = (f[campo] - 1) / 23.0
            soma += p
            var += p * (1 - p)
        sd = math.sqrt(var)
        return {"pred": round(soma, 3), "sd_binomial": round(sd, 3),
                "obs": obs, "z": round((obs - soma) / sd, 3)}

    esc_est["M3_geometria_exacta_iEq"] = m3("iEq", esc_est["obs"])
    esc_l1["M3_geometria_exacta_iIso"] = m3("iIso", esc_l1["obs"])
    m0e = esc_est["M0_indep"]
    esc_est["razao_M3_M0"] = round(
        esc_est["M3_geometria_exacta_iEq"]["pred"] / m0e, 3)
    esc_l1["razao_M3_M0"] = round(
        esc_l1["M3_geometria_exacta_iIso"]["pred"] / esc_l1["M0_indep"], 3)
    out["escada_estado"] = esc_est
    out["escada_bothL1"] = esc_l1

    # residuo dos modelos M1/M2 com sd Poisson da predicao
    for esc in (esc_est, esc_l1):
        o = esc["obs"]
        for m in ("M1_classe", "M2_celula7"):
            pred = esc[m]
            esc["z_obs_vs_" + m] = round((o - pred) / math.sqrt(pred), 3)

    # independencia condicional dentro de cada celula (Fisher exacto)
    fisher = {}
    for cell, r in esc_est["tabela_por_celula"].items():
        n, b, a, ambos = r["n"], r["B"], r["A"], r["ambos"]
        t = [[ambos, b - ambos], [a - ambos, n - b - a + ambos]]
        fisher[cell] = {"tabela": t,
                        "esperado_indep": round(b * a / n, 3),
                        "p_fisher_bicaudal": round(
                            fisher_2x2(t[0][0], t[0][1], t[1][0], t[1][1]), 5)}
    out["independencia_condicional_por_celula_estado"] = fisher

    # diagnostico de elegibilidade (tilt): medias geometricas vs observado
    def tilt(campo_tam, campo_obs, nome):
        pred = sum((f[campo_tam] - 1) / 23.0 for f in fams)
        var = sum(((f[campo_tam] - 1) / 23.0) * (1 - (f[campo_tam] - 1) / 23.0)
                  for f in fams)
        o = sum(f[campo_obs] for f in fams)
        return {nome: {"pred_se_pi1_uniforme": round(pred, 2),
                       "obs": o, "z": round((o - pred) / math.sqrt(var), 3)}}
    tilts = {}
    tilts.update(tilt("isoB", "l1B", "L1_aresta_B"))
    tilts.update(tilt("isoA", "l1A", "L1_aresta_A"))
    tilts.update(tilt("neqB", "estB", "estado_aresta_B"))
    tilts.update(tilt("neqA", "estA", "estado_aresta_A"))
    out["tilt_elegibilidade"] = tilts

    # efeito-lam: dentro de cada classe {T, DT, FC}, taxas por sub-celula,
    # separadas em L1 (teoria: SEM efeito) e L2 (teoria: efeito possivel)
    efeito = {}
    for cl_, (ci, co) in (("T", ("T_in", "T_out")),
                          ("DT", ("DT_lam", "DT_oth")),
                          ("FC", ("FC_lam", "FC_oth"))):
        li = [f for f in fams if f["cell"] == ci]
        lo = [f for f in fams if f["cell"] == co]
        reg = {}
        for alvo in ("l1B", "l1A", "l2B", "l2A", "estB", "estA"):
            ki = sum(f[alvo] for f in li)
            ko = sum(f[alvo] for f in lo)
            reg[alvo] = {
                "alinhado": {"k": ki, "n": len(li),
                             "taxa": round(ki / len(li), 5),
                             "IC95": wilson(ki, len(li))},
                "outro": {"k": ko, "n": len(lo),
                          "taxa": round(ko / len(lo), 5),
                          "IC95": wilson(ko, len(lo))},
                "p_fisher": round(fisher_2x2(ki, len(li) - ki,
                                             ko, len(lo) - ko), 5)}
        efeito[cl_] = reg
    out["efeito_lam_por_classe"] = efeito

    # tabela q por celula (para precommit OOS)
    qtab = {}
    for cell, r in esc_est["tabela_por_celula"].items():
        qtab[cell] = {"qB_est": round(r["B"] / r["n"], 6),
                      "qA_est": round(r["A"] / r["n"], 6)}
    out["q_por_celula_para_OOS"] = qtab
    ql1 = {}
    for cl_, r in esc_l1["tabela_por_classe"].items():
        ql1[cl_] = {"qB_L1": round(r["B"] / r["n"], 6),
                    "qA_L1": round(r["A"] / r["n"], 6)}
    out["qL1_por_classe_para_OOS"] = ql1

    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print(json.dumps(out, sort_keys=True, indent=1))
    print("sha256 correlacao:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
