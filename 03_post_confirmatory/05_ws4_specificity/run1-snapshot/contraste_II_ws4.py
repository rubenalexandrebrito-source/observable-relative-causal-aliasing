# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS4.
Contraste II: leitura DETERMINÍSTICA dos datasets exploratórios existentes
(NUNCA editados; sementes 910000001/910000002, alheias ao WS4 — nenhuma
amostragem nova aqui). Objectivo: situar o zero exacto de III (Teorema
III-1) face ao lado II à mesma resolução (dep_sites ponto-a-ponto).
NÃO propõe regra de decisão, threshold, C1'' nem correcção alguma.
"""
import json, hashlib
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws4-classIII-specificity"
SAIDA = WS + "/ws4-contraste-II.json"

comb = json.load(open(DST + "/prevalencia/prevalencia-combinada-N10000.json"))
l1 = json.load(open(DST + "/prevalencia/prevalencia-cancelamento-II.json"))
l2 = json.load(open(DST + "/prevalencia/prevalencia-cancelamento-II-lote2.json"))

colapsos = (l1["exemplos"]["colapso_total"] + l2["exemplos"]["colapso_total"])
outros = (l1["exemplos"]["individua_uma"] + l2["exemplos"]["individua_uma"] +
          l1["exemplos"]["individua_ambas"] + l2["exemplos"]["individua_ambas"])

deps_colapso = []
arestas_zero_colapso = []
inst_ambas_pos = 0
for r in colapsos:
    vals = []
    for nome, a in r["arestas"].items():
        deps_colapso.append(a["dep_sites"])
        vals.append(a["dep_sites"])
        if a["dep_sites"] == 0:
            arestas_zero_colapso.append(
                {"theta_sha": r["theta_sha"][:16], "aresta": nome,
                 "nivel": a["nivel"], "dep": a["dep_sites"]})
    if all(v > 0 for v in vals):
        inst_ambas_pos += 1

deps_arr = sorted(deps_colapso)


def q(v, p):
    return v[min(len(v) - 1, int(p * len(v)))] if v else None


# arestas dep==0 nos exemplos preservados de outras classes
zero_outros = []
for r in outros:
    for nome, a in r["arestas"].items():
        if a["dep_sites"] == 0:
            zero_outros.append({"theta_sha": r["theta_sha"][:16],
                                "classe": r["classe"], "aresta": nome,
                                "nivel": a["nivel"]})

pa = comb["por_ARESTA"]
pi_ = comb["por_INSTANCIA"]

fam20 = l1.get("fam20_confirmatoria_referencia")

saida = {
    "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
    "workstream": "ws4-classIII-specificity",
    "nota": "leitura deterministica de datasets existentes; nenhuma amostragem nova; nenhuma proposta de classificador",
    "agregado_global_II_N10000": {
        "total_arestas": pa["total_arestas"],
        "com_dep_ponto_a_ponto": pa["com_dependencia_ponto_a_ponto"],
        "sem_dep_ponto_a_ponto": pa["sem_dependencia_ponto_a_ponto"],
        "L1": pa["L1_d_iguais"], "L2": pa["L2_rank_igual_d_diferente"],
        "L3": pa["L3_rank_diferente"],
        "colapso_total_instancias": pi_["colapso_total_erro_C1p"],
        "subtipos": pi_["subtipos_colapso_total"],
    },
    "colapsos_46_dep_sites": {
        "n_instancias": len(colapsos),
        "n_arestas": len(deps_colapso),
        "min": deps_arr[0] if deps_arr else None,
        "p25": q(deps_arr, 0.25), "mediana": q(deps_arr, 0.5),
        "p75": q(deps_arr, 0.75), "max": deps_arr[-1] if deps_arr else None,
        "arestas_dep_zero_nos_colapsos": len(arestas_zero_colapso),
        "detalhe_dep_zero": arestas_zero_colapso,
        "instancias_com_AMBAS_arestas_dep_pos": inst_ambas_pos,
        "todos_os_valores": deps_arr,
    },
    "arestas_dep_zero_nos_exemplos_preservados_de_outras_classes": zero_outros,
    "nota_dep0_implica_L1": "dep_sites==0 => x0==x1 ponto a ponto => d0==d1 => L1 (implicacao analitica)",
    "fam20_referencia_do_lote1": fam20,
}
corpo = json.dumps(saida, sort_keys=True, indent=1).encode()
open(SAIDA, "wb").write(corpo)
print(json.dumps({k: v for k, v in saida.items()
                  if k not in ("colapsos_46_dep_sites",)}, sort_keys=True,
                 indent=1)[:1200])
print("colapsos_46_dep_sites:",
      json.dumps({k: v for k, v in saida["colapsos_46_dep_sites"].items()
                  if k != "todos_os_valores"}, sort_keys=True, indent=1))
print("todos_os_valores:", deps_arr)
print("saida:", SAIDA)
print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
print("sha256_script:", hashlib.sha256(open(__file__, "rb").read()).hexdigest())
