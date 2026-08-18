# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS2 (information loss).
Script H (precommit-ws2-v2.txt, ponto 2c): ligação ponta-a-ponta da decomposição
ao VEREDICTO do classificador congelado (cl.classificar), sem alterar nada:
 (1) primeira família colapso_total do lote1 (replay registado), reconstruída
     canonicamente (variante II, n=10) -> esperado: C1p funde o núcleo;
 (2) primeira família individua_ambas do lote1 (controlo) -> esperado: sem fusão;
 (3) instância confirmatória CEGA 7bb0baab3a8ed7aa (JSON read-only) -> reproduz
     o erro conhecido (fusão do núcleo por C1p), sem reinterpretação.
NENHUMA amostra nova; nenhuma semente nova.
"""
import sys, json, hashlib
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws2-information-loss"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl
import pontuacao as pt

SAIDA = WS + "/ws2-endtoend.json"


def instancia_canonica(th_d, iid):
    th = g.Theta(**th_d)
    tab, n, lay = g.tabela_transicao("II", th, False)
    mods = g._modulos_canonicos("II", False)
    return {"id": iid, "n": n, "transicao": tab,
            "estado_inicial": g._campos_para_int(
                g.estado_inicial("II", th), lay),
            "modulos": [{"id": "Q%d" % i, "bits": m["bits"],
                         "bits_memoria": m["mem"]}
                        for i, m in enumerate(mods)]}


def resumo_c1p(res, tipos):
    comps = res["C1p"]["componentes"]
    multi = [sorted(tipos[i] for i in c) for c in comps if len(c) >= 2]
    return {"E_S_C1p": res["C1p"]["E_S"],
            "componentes_multi": multi,
            "nucleo_fundido": any(set(c) == {"A", "B", "C_AB", "C_BA"}
                                  for c in map(set, multi)),
            "arestas": res["arestas"]}


def main():
    dados = json.load(open(WS + "/ws2-thetas-cases.json"))
    casos = dados["casos"]
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "descricao": "cl.classificar ponta-a-ponta: colapso, controlo, confirmatoria"}
    tipos_canon = ["A", "B", "C_AB", "C_BA"]

    c_col = next(c for c in casos if c["grupo"] == "colapso" and c["seed"] == 910000001)
    c_ctl = next(c for c in casos if c["grupo"] == "ctrl_L3L3")
    for rot, caso in (("colapso_lote1_fam%d" % c_col["fam"], c_col),
                      ("controlo_L3L3_fam%d" % c_ctl["fam"], c_ctl)):
        th_d = dados["thetas"]["%d:%d" % (caso["seed"], caso["tentativa"])]
        res = cl.classificar(instancia_canonica(th_d, "ws2-" + rot))
        out[rot] = {"seed": caso["seed"], "tentativa": caso["tentativa"],
                    "theta_sha": caso["theta_sha"],
                    "orbita": res["orbita"], **resumo_c1p(res, tipos_canon)}

    ID = "7bb0baab3a8ed7aa"
    chave = json.load(open(DST + "/chave-e2.json"))
    tipos = pt._tipos_e2(chave[ID])
    res = cl.classificar(DST + "/conf-e2/instancias/%s.json" % ID)
    out["confirmatoria_" + ID] = {"tipos": tipos, "orbita": res["orbita"],
                                  **resumo_c1p(res, tipos)}

    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    for k in out:
        if k in ("rotulo", "descricao"):
            continue
        v = out[k]
        print(k, "orbita", v["orbita"], "nucleo_fundido", v["nucleo_fundido"],
              "componentes_multi", v["componentes_multi"])
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
