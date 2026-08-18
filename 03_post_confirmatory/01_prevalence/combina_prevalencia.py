# -*- coding: utf-8 -*-
"""POST-CONFIRMATORY / EXPLORATORY — combinação pré-declarada dos lotes 1+2
(N=10000) da prevalência do cancelamento. Ver precommit-lote2.txt."""
import json, math, hashlib

DIR = "/root/causal-A-postconfirmatory-analysis/prevalencia/"
A = json.load(open(DIR + "prevalencia-cancelamento-II.json"))
B = json.load(open(DIR + "prevalencia-cancelamento-II-lote2.json"))


def wilson(x, n, z=1.96):
    p = x / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(c - h, 6), round(c + h, 6)]


def soma_int(d1, d2):
    return {k: d1[k] + d2[k] for k in d1 if isinstance(d1[k], int)}


ca = soma_int(A["contagens_por_ARESTA"], B["contagens_por_ARESTA"])
ci = {k: A["contagens_por_INSTANCIA"][k] + B["contagens_por_INSTANCIA"][k]
      for k in ("individua_ambas", "individua_uma", "colapso_total_erro_C1p")}
sub = dict(A["contagens_por_INSTANCIA"]["subtipos_colapso_total"])
for k, v in B["contagens_por_INSTANCIA"]["subtipos_colapso_total"].items():
    sub[k] = sub.get(k, 0) + v

n_inst = A["aceites_total_instancias"] + B["aceites_total_instancias"]
n_edge = ca["total_arestas"]
x_col = ci["colapso_total_erro_C1p"]
x_l12 = ca["dependencia_desaparece_apos_agregacao_L1_mais_L2"]
q = x_l12 / n_edge

out = {
    "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
    "combinacao": "lotes 1+2 pre-declarados (precommit-lote2.txt); N total fixado em 10000",
    "lote1": {"semente": 910000001, "n": A["aceites_total_instancias"],
              "colapsos": A["contagens_por_INSTANCIA"]["colapso_total_erro_C1p"],
              "sha_saida": "ver ficheiro proprio"},
    "lote2": {"semente": 910000002, "n": B["aceites_total_instancias"],
              "colapsos": B["contagens_por_INSTANCIA"]["colapso_total_erro_C1p"]},
    "instancias_total": n_inst,
    "por_ARESTA": {
        **ca,
        "prop_L1": round(ca["L1_d_iguais"] / n_edge, 6),
        "prop_L2": round(ca["L2_rank_igual_d_diferente"] / n_edge, 6),
        "prop_L3": round(ca["L3_rank_diferente"] / n_edge, 6),
        "prop_L1_mais_L2": round(q, 6),
        "IC95_L1_mais_L2": wilson(x_l12, n_edge),
    },
    "por_INSTANCIA": {
        **ci,
        "subtipos_colapso_total": sub,
        "P_falha_identificabilidade_C1p_dado_II": round(x_col / n_inst, 6),
        "IC95_wilson": wilson(x_col, n_inst),
        "esperado_sob_independencia_das_arestas_q2": round(q * q, 6),
        "razao_observado_sobre_independencia": round((x_col / n_inst) / (q * q), 2),
    },
    "consistencia_confirmatoria": {
        "P_de_pelo_menos_1_colapso_em_25_II_E2": round(1 - (1 - x_col / n_inst) ** 25, 4),
        "P_de_0_colapsos_em_50_II_E1": round((1 - x_col / n_inst) ** 50, 4),
        "fam20_subtipo": "(L1,L1) - cancelamento exacto na soma de Hamming",
    },
    "lema_E1_E2": "d_E2 = 4*d_E1 provado e verificado (verifica_E1_E2.out): niveis identicos nos dois regimes",
}
corpo = json.dumps(out, sort_keys=True, indent=1).encode()
open(DIR + "prevalencia-combinada-N10000.json", "wb").write(corpo)
print(json.dumps(out, sort_keys=True, indent=1))
print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
