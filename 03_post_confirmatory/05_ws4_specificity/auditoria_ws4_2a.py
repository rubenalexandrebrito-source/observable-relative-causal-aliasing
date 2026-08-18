# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS4 (2.ª passagem).
AUDITORIA determinística (adenda, secção A): SEM amostragem nova.
A1: reprodução de fatia (25 famílias) da medição 910000020 da 1.ª passagem.
A2: replay de famílias REGISTADAS do lote 1 (semente registada 910000001)
    para validar dep/d0/d1/nivel em regime NÃO-nulo + fórmula Wtil com pi.
A3: recontagem independente dos agregados do contraste.
O resultado confirmatório permanece NEGATIVO e imutável. Nenhuma escrita
fora desta área; nenhuma proposta de classificador.
"""
import sys, json, time, hashlib
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws4-classIII-specificity"
sys.path.insert(0, DST + "/frozen-copy")
sys.path.insert(0, WS)
import gerador as g
import classificador as cl
import medicao_ws4_classIII as m1   # funções da 1.ª passagem (área própria)

t0 = time.time()
res = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
       "workstream": "ws4-classIII-specificity",
       "fase": "adenda 2a passagem — auditoria",
       "precommit": "precommit-ws4-adenda-h2-auditoria.txt"}
falhas = []

def pc2(v):
    return bin(v).count("1")

# ---------------------------------------------------------------- A1
pass1 = json.load(open(WS + "/ws4-classIII-medicao.json"))
regs = pass1["registos"]
assert len(regs) == 2000

ss = np.random.SeedSequence(910000020)
rng = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))
aceites = []
tent = 0
while len(aceites) < 25:
    tent += 1
    th = g.sample_theta_base(rng)
    if th.pi[0] == th.pi[1]:
        continue
    ok, _, _ = g.elegibilidade(th, False)
    if ok:
        aceites.append((th, tent))

a1_cmp = 0
for i, (th, tent_i) in enumerate(aceites):
    r0 = regs[i]
    if r0["tentativa"] != tent_i or r0["theta_sha"] != m1.theta_sha(th):
        falhas.append({"A1": i, "campo": "tentativa/theta_sha"})
        continue
    tab, n, lay = g.tabela_transicao("III", th, False)
    T = np.asarray(tab, dtype=np.int64)
    s0 = g._campos_para_int(g.estado_inicial("III", th), lay)
    orb = cl.orbita(T, s0)
    V = np.asarray(orb, dtype=np.int64)
    for nome, ba, bb, mem, tn, sr, sc, sm in m1.ARESTAS:
        r = m1.analisa_aresta_completa(T, n, ba, bb, mem)
        e0 = r0["arestas"][nome]
        mv = (V >> sm) & 1
        v0n, v1n = int((mv == 0).sum()), int((mv == 1).sum())
        for campo, novo in (("dep_sites", r["dep_sites"]), ("nivel", r["nivel"]),
                            ("bdep", r["bdep"]), ("V0", v0n), ("V1", v1n)):
            if e0[campo] != novo:
                falhas.append({"A1": i, "aresta": nome, "campo": campo,
                               "registado": e0[campo], "novo": novo})
        a1_cmp += 1
# exemplos (têm d0/d1 integrais): comparar com recomputação
for ex in pass1["exemplos"]:
    th = aceites[ex["fam"]][0]
    tab, n, lay = g.tabela_transicao("III", th, False)
    T = np.asarray(tab, dtype=np.int64)
    for nome, ba, bb, mem, tn, sr, sc, sm in m1.ARESTAS:
        if nome != ex["aresta"]:
            continue
        r = m1.analisa_aresta_completa(T, n, ba, bb, mem)
        if r["d0"] != ex["d0"] or r["d1"] != ex["d1"]:
            falhas.append({"A1_exemplo": ex["fam"], "aresta": nome})
res["A1"] = {"familias_reproduzidas": len(aceites),
             "arestas_comparadas": a1_cmp,
             "campos_comparados_por_aresta": ["dep_sites", "nivel", "bdep", "V0", "V1"],
             "exemplos_d0d1_comparados": len(pass1["exemplos"]),
             "falhas": [f for f in falhas if "A1" in f or "A1_exemplo" in f]}

# ---------------------------------------------------------------- A2
l1 = json.load(open(DST + "/prevalencia/prevalencia-cancelamento-II.json"))
alvo = {}
reg_c = l1["exemplos"]["colapso_total"][0]     # fam 289, tentativa 1003
reg_i = l1["exemplos"]["individua_ambas"][0]   # fam 0, tentativa 9
for r0 in (reg_c, reg_i):
    alvo[r0["tentativa"]] = r0

ss2 = np.random.SeedSequence(910000001)
rng2 = np.random.Generator(np.random.PCG64(ss2.spawn(4)[0]))
achados = {}
n_aceites = 0
for tent in range(1, max(alvo) + 1):
    th = g.sample_theta_base(rng2)
    if th.pi[0] == th.pi[1]:
        continue
    ok, _, _ = g.elegibilidade(th, False)
    if not ok:
        continue
    fam_idx = n_aceites
    n_aceites += 1
    if tent in alvo:
        achados[tent] = (th, fam_idx)

a2 = {"alvos": [], "wtil_pi": []}
for tent, r0 in sorted(alvo.items()):
    th, fam_idx = achados.get(tent, (None, None))
    item = {"tentativa": tent, "fam_registada": r0["fam"],
            "fam_replay": fam_idx, "classe": r0["classe"]}
    if th is None or fam_idx != r0["fam"] or m1.theta_sha(th) != r0["theta_sha"]:
        item["theta_sha_ok"] = False
        falhas.append({"A2": tent, "campo": "replay/theta_sha"})
        a2["alvos"].append(item)
        continue
    item["theta_sha_ok"] = True
    tab, n, lay = g.tabela_transicao("II", th, False)
    T = np.asarray(tab, dtype=np.int64)
    for nome, ba, bb, mem, tn, sr, sc, sm in m1.ARESTAS:
        r = m1.analisa_aresta_completa(T, n, ba, bb, mem)
        e0 = r0["arestas"][nome]
        cmpf = {"nivel": (e0["nivel"], r["nivel"]),
                "dep_sites": (e0["dep_sites"], r["dep_sites"])}
        okc = e0["nivel"] == r["nivel"] and e0["dep_sites"] == r["dep_sites"]
        if "d0" in e0:
            cmpf["d0"] = (e0["d0"] == r["d0"])
            cmpf["d1"] = (e0["d1"] == r["d1"])
            okc = okc and e0["d0"] == r["d0"] and e0["d1"] == r["d1"]
        if not okc:
            falhas.append({"A2": tent, "aresta": nome, "cmp": str(cmpf)})
        item[nome] = {"ok": okc, "dep_registado": e0["dep_sites"],
                      "dep_replay": r["dep_sites"], "nivel": r["nivel"]}
        # fórmula Wtil com pi (auditoria da derivação prévia, caso pi0!=pi1)
        M = th.G0 if tn == "G0" else th.F0
        scn = m1.subs_canal(r["ints"], ba)
        wt_ok = True
        for mval, dm in ((0, r["d0"]), (1, r["d1"])):
            pi_m = th.pi[mval]
            wt = [[sum(pc2(M[rr][pi_m[p]] ^ M[rr][pi_m[q]]) for rr in range(4))
                   for q in range(4)] for p in range(4)]
            dpred = [32 * sum(wt[c][(c & ~mc) | vc] for c in range(4))
                     for (mc, vc) in scn]
            if dpred != dm:
                wt_ok = False
        a2["wtil_pi"].append({"tentativa": tent, "aresta": nome, "ok": wt_ok})
        if not wt_ok:
            falhas.append({"A2_wtil": tent, "aresta": nome})
    a2["alvos"].append(item)
res["A2"] = a2

# ---------------------------------------------------------------- A3
l2 = json.load(open(DST + "/prevalencia/prevalencia-cancelamento-II-lote2.json"))
contr = json.load(open(WS + "/ws4-contraste-II.json"))
colapsos = l1["exemplos"]["colapso_total"] + l2["exemplos"]["colapso_total"]
deps = sorted(a["dep_sites"] for r in colapsos for a in r["arestas"].values())
nzero = sum(1 for d in deps if d == 0)
ambas_pos = sum(1 for r in colapsos
                if all(a["dep_sites"] > 0 for a in r["arestas"].values()))
sem_dep = (l1["contagens_por_ARESTA"]["sem_dependencia_ponto_a_ponto"]
           + l2["contagens_por_ARESTA"]["sem_dependencia_ponto_a_ponto"])
c0 = contr["colapsos_46_dep_sites"]
a3 = {"n_colapsos": (len(colapsos), c0["n_instancias"]),
      "n_arestas": (len(deps), c0["n_arestas"]),
      "min": (deps[0], c0["min"]), "max": (deps[-1], c0["max"]),
      "mediana": (deps[len(deps)//2], c0["mediana"]),
      "arestas_dep_zero": (nzero, c0["arestas_dep_zero_nos_colapsos"]),
      "ambas_pos": (ambas_pos, c0["instancias_com_AMBAS_arestas_dep_pos"]),
      "sem_dep_agregado_lotes": (sem_dep,
          contr["agregado_global_II_N10000"]["sem_dep_ponto_a_ponto"]),
      "todos_os_valores_iguais": deps == c0["todos_os_valores"]}
for k, v in a3.items():
    if isinstance(v, tuple) and v[0] != v[1]:
        falhas.append({"A3": k, "valores": v})
res["A3"] = a3

res["falhas_total"] = len(falhas)
res["falhas"] = falhas
res["duracao_s"] = round(time.time() - t0, 1)
try:
    res["sha256_script"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
except Exception:
    res["sha256_script"] = None

corpo = json.dumps(res, sort_keys=True, indent=1).encode()
open(WS + "/ws4-auditoria-2a.json", "wb").write(corpo)
print("A1: familias 25, arestas comparadas", res["A1"]["arestas_comparadas"],
      "falhas", len(res["A1"]["falhas"]))
print("A2:", json.dumps(a2, sort_keys=True)[:1600])
print("A3:", json.dumps(a3, sort_keys=True))
print("FALHAS TOTAIS:", len(falhas))
print("duracao_s:", res["duracao_s"])
print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
print("sha256_script:", res["sha256_script"])
