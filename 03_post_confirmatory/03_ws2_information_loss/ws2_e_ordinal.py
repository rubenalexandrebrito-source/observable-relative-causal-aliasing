# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS2 (information loss).
Script E: análise da ORDINALIZACAO (S3 -> S4, operador rank_canonico) sobre o
output populacional do Script C (replay das 10000 famílias registadas).
 (i) L2: que informação exacta o rank destrói — componentes mudadas, quantum,
     classes de empate movidas em bloco, margens ao flip;
 (ii) teorema de paridade: TODAS as componentes de d0-d1 são múltiplas de 64;
 (iii) fibra da ordinalização: agrupamento dos vetores d observados por padrão
     de rank + contagem teórica C(33,t);
 (iv) contraste L3: o que muda (inversões estritas vs empates quebrados/criados)
     e magnitudes. Diagnóstico apenas; nenhuma regra nova é proposta.
"""
import sys, json, hashlib
from math import comb
from collections import Counter

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws2-information-loss"
sys.path.insert(0, DST + "/frozen-copy")
import classificador as cl

SAIDA = WS + "/ws2-L2-ordinal.json"


def classes_de(d):
    """classes de empate: valor -> lista de componentes, ordenadas por valor."""
    byv = {}
    for i, v in enumerate(d):
        byv.setdefault(v, []).append(i)
    return sorted(byv.items())


def main():
    pop = json.load(open(WS + "/ws2-population-stages.json"))
    edges = pop["edges"]

    # (ii) paridade mod 64 de todas as diferenças
    par_ok = 0
    par_fail = 0
    deltas_all = Counter()
    for e in edges:
        if e["n"] == "L1":
            continue
        for a, b in zip(e["d0"], e["d1"]):
            dl = a - b
            if dl:
                deltas_all[abs(dl)] += 1
                if dl % 64 == 0:
                    par_ok += 1
                else:
                    par_fail += 1

    # (i) L2 em detalhe
    L2 = [e for e in edges if e["n"] == "L2"]
    l2_ncomp = Counter()
    l2_kpat = Counter()
    l2_absdelta = Counter()
    l2_classes_uniformes = 0
    l2_classes_nao_uniformes = 0
    l2_margem_min = Counter()
    l2_tie_sizes = Counter()
    l2_rank_t = Counter()
    for e in L2:
        d0, d1 = e["d0"], e["d1"]
        J = [k for k in range(9) if d0[k] != d1[k]]
        l2_ncomp[len(J)] += 1
        l2_kpat[tuple(J)] += 1
        for k in J:
            l2_absdelta[abs(d0[k] - d1[k])] += 1
        cls0 = classes_de(d0)
        l2_rank_t[len(cls0)] += 1
        for v, mem in cls0:
            l2_tie_sizes[len(mem)] += 1
            ds = {d1[i] - d0[i] for i in mem}
            if len(ds) == 1:
                l2_classes_uniformes += 1
            else:
                l2_classes_nao_uniformes += 1
        # margens: valores de classe em d1 mantêm ordem estrita; margem mínima
        vals1 = [min(d1[i] for i in mem) for v, mem in cls0]
        gaps = [vals1[i + 1] - vals1[i] for i in range(len(vals1) - 1)]
        if gaps:
            l2_margem_min[min(gaps)] += 1

    # (iv) contraste L3: tipo de mudança ordinal
    l3_tipo = Counter()
    l3_absdelta = Counter()
    l3_ncomp = Counter()
    for e in edges:
        if e["n"] != "L3":
            continue
        d0, d1 = e["d0"], e["d1"]
        J = [k for k in range(9) if d0[k] != d1[k]]
        l3_ncomp[len(J)] += 1
        for k in J:
            l3_absdelta[abs(d0[k] - d1[k])] += 1
        r0, r1 = cl.rank_canonico(d0), cl.rank_canonico(d1)
        t0, t1 = len(set(r0)), len(set(r1))
        # pares concordantes/discordantes
        inv = emp_q = emp_c = 0
        for i in range(9):
            for j in range(i + 1, 9):
                s0 = (d0[i] > d0[j]) - (d0[i] < d0[j])
                s1 = (d1[i] > d1[j]) - (d1[i] < d1[j])
                if s0 == s1:
                    continue
                if s0 == 0:
                    emp_q += 1          # empate quebrado
                elif s1 == 0:
                    emp_c += 1          # empate criado
                else:
                    inv += 1            # inversão estrita
        tipo = ("so_empates" if inv == 0 else
                "so_inversoes" if (emp_q == 0 and emp_c == 0) else "misto")
        l3_tipo[tipo] += 1

    # (iii) fibra da ordinalização: vetores d observados por padrão de rank
    por_rank = {}
    for e in edges:
        for dv in ([e["d0"]] if e["n"] == "L1" else [e["d0"], e["d1"]]):
            r = tuple(cl.rank_canonico(dv))
            por_rank.setdefault(r, set()).add(tuple(dv))
    mult = Counter(len(s) for s in por_rank.values())
    top = sorted(((len(s), list(r)) for r, s in por_rank.items()), reverse=True)[:5]
    t_obs = Counter(len(set(r)) for r in por_rank)
    fibra_teorica = {t: comb(33, t) for t in range(1, 10)}

    # atenuação: massa sobrevivente ao S2 vs sítios com pc diferente
    aten = {"L2": [0, 0], "L3": [0, 0]}
    for e in edges:
        if e["n"] == "L1":
            continue
        soma_abs = sum(abs(a - b) for a, b in zip(e["d0"], e["d1"]))
        aten[e["n"]][0] += soma_abs
        aten[e["n"]][1] += e["s1"]

    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "descricao": "ordinalizacao S3->S4: o que rank_canonico destroi/preserva",
           "paridade_mod64": {"componentes_nao_nulas_ok": par_ok,
                              "violacoes": par_fail,
                              "distribuicao_abs_delta_todas": dict(sorted(deltas_all.items()))},
           "L2": {"n_arestas": len(L2),
                  "n_componentes_mudadas": dict(sorted(l2_ncomp.items())),
                  "padroes_k_mudados": {str(k): v for k, v in sorted(l2_kpat.items())},
                  "abs_delta": dict(sorted(l2_absdelta.items())),
                  "classes_de_empate_movidas_uniformemente": l2_classes_uniformes,
                  "classes_nao_uniformes(viola_empate)": l2_classes_nao_uniformes,
                  "margem_minima_pos_mudanca": dict(sorted(l2_margem_min.items())),
                  "tamanhos_de_classes_de_empate": dict(sorted(l2_tie_sizes.items())),
                  "n_valores_distintos_t": dict(sorted(l2_rank_t.items()))},
           "L3": {"n_arestas": sum(l3_tipo.values()),
                  "tipo_mudanca_ordinal": dict(l3_tipo),
                  "n_componentes_mudadas": dict(sorted(l3_ncomp.items())),
                  "abs_delta": dict(sorted(l3_absdelta.items()))},
           "fibra_ordinalizacao": {
               "padroes_rank_observados": len(por_rank),
               "vetores_d_distintos_observados": sum(len(s) for s in por_rank.values()),
               "multiplicidade_vetores_por_padrao": dict(sorted(mult.items())),
               "top5_padroes_mais_povoados": top,
               "t_valores_distintos_por_padrao_observado": dict(sorted(t_obs.items())),
               "fibra_teorica_C33t_valores_em_32Z": fibra_teorica},
           "atenuacao_massa_pos_S2_sobre_sitios_pc_dif": {
               k: {"soma_abs_delta_d": v[0], "s1_sites": v[1],
                   "razao": (v[0] / v[1]) if v[1] else None}
               for k, v in aten.items()}}
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print(json.dumps({k: out[k] for k in ("paridade_mod64", "L2", "L3")}, indent=1))
    print("fibra:", json.dumps(out["fibra_ordinalizacao"], default=str)[:600])
    print("atenuacao:", out["atenuacao_massa_pos_S2_sobre_sitios_pc_dif"])
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())

if __name__ == "__main__":
    main()
