# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, ws3.
# Script A: dinâmica realizada ESTRITA na instância confirmatória falhada
# 7bb0baab3a8ed7aa (fam 20, II, E2, n=12). Tabela CEGA + chave-e2 (aberta na
# Fase 5) apenas para tipos de módulo. NADA é alterado fora do ws3 dir.
# Resultado confirmatório: NEGATIVO, imutável. Precommit: precommit-ws3-strict.txt.
import json, hashlib
import numpy as np
import ws3_lib as L
import sys
sys.path.insert(0, L.DST + "/frozen-copy")
import classificador as cl
import pontuacao as pt

ID = "7bb0baab3a8ed7aa"
SAIDA = L.DST + "/multiagent/ws3-realized-dynamics/ws3-strict-fam20.json"

chave = json.load(open(L.DST + "/chave-e2.json"))
inst = json.load(open(L.DST + "/conf-e2/instancias/%s.json" % ID))
tipos = pt._tipos_e2(chave[ID])
_, n, T, mods, s0 = cl.carregar(inst)
T = np.asarray(T, dtype=np.int64)
idx = {t: i for i, t in enumerate(tipos)}

orb = cl.orbita(T, s0)
orbset = set(int(s) for s in orb)
print("POST-CONFIRMATORY / EXPLORATORY — ws3 Script A (fam-20, n=12)")
print("id=%s  tipos=%s  |orbita|=%d  s0=%d" % (ID, tipos, len(orb), s0))
assert len(orb) == 25, "orbita != 25 — PARAR (regra 10)"

# bits do nucleo (A,B,C_AB,C_BA) para a granularidade intermedia
core_bits = sorted(sum((mods[idx[t]]["bits"] for t in ("A", "B", "C_AB", "C_BA")), []))
print("core_bits =", core_bits)

falhas = []
res = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
       "reafirmacao": "resultado_confirmatorio_A = negativo (fechado, imutavel)",
       "id": ID, "familia": 20, "variante": "II", "estrato": 2, "n": n,
       "orbita": len(orb), "estado_inicial": int(s0),
       "arestas": {}}

# tabela da orbita com coordenadas por aresta (para o relatorio)
tab_orb = []
for t_i, s in enumerate(orb):
    row = {"t": t_i, "estado": int(s)}
    for nome, a_t, b_t in (("C_AB->B", "C_AB", "B"), ("C_BA->A", "C_BA", "A")):
        a_i, b_i = idx[a_t], idx[b_t]
        membits = mods[b_i]["bits_memoria"]
        procbits = [b for b in mods[b_i]["bits"] if b not in membits]
        eP = cl.extractor(procbits, n)
        eC = cl.extractor(mods[a_i]["bits"], n)
        eM = cl.extractor(membits, n)
        row[nome] = {"m": int(eM[s]), "r": int(eP[s]), "c": int(eC[s])}
    tab_orb.append(row)
res["orbita_coords"] = tab_orb

for nome, a_t, b_t in (("C_AB->B", "C_AB", "B"), ("C_BA->A", "C_BA", "A")):
    a_i, b_i = idx[a_t], idx[b_t]
    membits = mods[b_i]["bits_memoria"]
    corefree = [b for b in core_bits if b not in membits]
    eCore = cl.extractor(corefree, n)
    r = L.analisa_aresta_realizada(T, n, mods[a_i]["bits"], mods[b_i]["bits"],
                                   membits, orb, detalhe=True, proj_core=eCore)
    if "nivel" not in r:
        print("PARAR (regra 10): mem_reach=%s em %s — sem contraste" % (r["mem_reach"], nome))
        sys.exit(1)
    r.pop("_pat_cells_np")
    res["arestas"][nome] = r

    # ---- cross-checks X4/X5 (precommit) ----
    if r["nivel"] != "L1_d_iguais":
        falhas.append("%s: nivel %s != L1" % (nome, r["nivel"]))
    if r["dep_total"] != 4608:
        falhas.append("%s: dep_total %d != 4608" % (nome, r["dep_total"]))
    if r["exc_reducao"] != 0:
        falhas.append("%s: reducao (r,c) violada em %d verificacoes" % (nome, r["exc_reducao"]))
    if r["dep_total"] != r["multiplicidade_celula"] * r["rc"]["sitios_totais"]:
        falhas.append("%s: dep_total != mult * sitios_celula" % nome)
    print("\n=== aresta %s (a=%s '%s', b=%s '%s') ===" % (nome, a_i, a_t, b_i, b_t))
    print(" nivel=%s  dep_total=%d (mult=%d x %d celulas-sitio de 144)"
          % (r["nivel"], r["dep_total"], r["multiplicidade_celula"], r["rc"]["sitios_totais"]))
    print(" d0=%s" % r["d0"])
    print(" d1=%s" % r["d1"])
    print(" orbita: m=0 em %d estados, m=1 em %d estados" % (r["cfg"]["R0"], r["cfg"]["R1"]))
    print(" CONFIG   : uniao=%d intersecao_estrita=%d | sitios uniao=%d estritos=%d -> %s"
          % (r["cfg"]["uniao"], r["cfg"]["intersecao_estrita"],
             r["cfg"]["sitios_uniao"], r["cfg"]["sitios_estritos"], r["categoria_cfg"]))
    print(" NUCLEO   : uniao=%d intersecao=%d | sitios uniao=%d estritos=%d -> %s"
          % (r["core"]["uniao"], r["core"]["intersecao"],
             r["core"]["sitios_uniao"], r["core"]["sitios_estritos"], r["categoria_core"]))
    print(" (r,c)    : |C0|=%d |C1|=%d |I|=%d |U|=%d | sitios: totais=%d uniao=%d ESTRITOS=%d -> %s"
          % (r["rc"]["n_C0"], r["rc"]["n_C1"], r["rc"]["n_I"], r["rc"]["n_U"],
             r["rc"]["sitios_totais"], r["rc"]["sitios_uniao"], r["rc"]["sitios_estritos"],
             r["categoria_rc"]))
    print(" I (celulas (r,c) em AMBOS os contextos): %s"
          % [((cell >> 2), (cell & 3)) for cell in r["rc"]["I"]])
    print(" OBS (sem cirurgia): pares=%d diferentes=%d" % (r["obs"]["pares"], r["obs"]["pares_diferentes"]))
    if r["testemunhas_estritas"]:
        print(" testemunhas estritas (intervencao, (r,c), padrao m0 vs m1):")
        for w in r["testemunhas_estritas"]:
            print("   int#%d (mk=%d,vl=%d) r=%d c=%d : %d vs %d (pesos %d vs %d)"
                  % (w["intervencao"], w["mascara"], w["valor"], w["r"], w["c"],
                     w["padrao_m0"], w["padrao_m1"], w["peso_m0"], w["peso_m1"]))
    if r["obs_detalhe"]:
        for o in r["obs_detalhe"]:
            print("   obs r=%d (c1=%d,c2=%d): O_m0=%d O_m1=%d difere=%s"
                  % (o["r"], o["c1"], o["c2"], o["O_m0"], o["O_m1"], o["difere"]))

# X4: criterio OR anterior (step3b) = sitios_uniao ao nivel CONFIG, por aresta
or_sites = sorted(res["arestas"][nm]["cfg"]["sitios_uniao"] for nm in res["arestas"])
print("\nreplicacao criterio OR (config, uniao): %s  (esperado {51,54})" % or_sites)
if or_sites != [51, 54]:
    falhas.append("OR nao replicou {51,54}: %s" % or_sites)

res["replicacao_OR_step3b"] = {"sitios_uniao_config_por_aresta":
                               {nm: res["arestas"][nm]["cfg"]["sitios_uniao"]
                                for nm in res["arestas"]},
                               "esperado": [51, 54], "ok": or_sites == [51, 54]}
res["cross_checks_falhas"] = falhas
res["sumario"] = {
    nm: {"categoria_rc": res["arestas"][nm]["categoria_rc"],
         "categoria_core": res["arestas"][nm]["categoria_core"],
         "categoria_cfg": res["arestas"][nm]["categoria_cfg"],
         "sitios_estritos_rc": res["arestas"][nm]["rc"]["sitios_estritos"],
         "obs_pares_diferentes": res["arestas"][nm]["obs"]["pares_diferentes"]}
    for nm in res["arestas"]}
res["instancia_estrito_rc_pelo_menos_uma"] = any(
    res["arestas"][nm]["categoria_rc"] == "ESTRITO" for nm in res["arestas"])
res["instancia_estrito_rc_ambas"] = all(
    res["arestas"][nm]["categoria_rc"] == "ESTRITO" for nm in res["arestas"])

corpo = json.dumps(res, sort_keys=True, indent=1).encode()
open(SAIDA, "wb").write(corpo)
print("\nFALHAS DE CROSS-CHECK:", falhas if falhas else "nenhuma")
print("instancia: >=1 aresta ESTRITO (rc)?", res["instancia_estrito_rc_pelo_menos_uma"],
      "| ambas?", res["instancia_estrito_rc_ambas"])
print("saida:", SAIDA)
print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
