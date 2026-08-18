# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, ws3.
# Baseline populacional fresco (EMENDA 1 do precommit; escrita antes de correr):
# semente 910000010, N=200 famílias II aceites; definições D1-D10 inalteradas;
# implementação independente ws3_indep (verificada: 0 discrepâncias em 4312).
# Resultado confirmatório: NEGATIVO, imutável.
import json, sys, hashlib, time
import numpy as np
import ws3_indep as W

DST = W.DST
WS = W.WS
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g

SEED = 910000010
N_ALVO = 200
ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5]), ("C_BA->A", [8, 9], [0, 1, 2], [2]))

t0 = time.time()
rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(SEED).spawn(4)[0]))
aceites = 0
tentativas = 0
regs = []
while aceites < N_ALVO:
    tentativas += 1
    th = g.sample_theta_base(rng)
    if th.pi[0] == th.pi[1]:
        continue
    ok, _, _ = g.elegibilidade(th, False)
    if not ok:
        continue
    aceites += 1
    tab, n, lay = g.tabela_transicao("II", th, False)
    T = np.asarray(tab, dtype=np.int64)
    s0 = g._campos_para_int(g.estado_inicial("II", th), lay)
    orb = W.minha_orbita(T, s0)
    rec = {"tentativa": tentativas, "orbita": len(orb), "arestas": {}}
    for nome, bits_a, bits_b, membits in ARESTAS:
        r = W.analisa_aresta_indep(T, n, bits_a, bits_b, membits, orb, len(bits_b))
        assert r["exc_reducao"] == 0, "reducao (r,c) violada (regra 10)"
        rec["arestas"][nome] = {
            "nivel": r["nivel"], "categoria_cfg": r["categoria_cfg"],
            "categoria_rc": r["categoria_rc"], "mem_reach": r["mem_reach"],
            "n_C0": r["rc"]["n_C0"], "n_C1": r["rc"]["n_C1"], "n_I": r["rc"]["n_I"],
            "sitios_estritos_rc": r["rc"]["sitios_estritos"],
            "sitios_uniao_rc": r["rc"]["sitios_uniao"],
            "sitios_totais_rc": r["rc"]["sitios_totais"],
            "cfg_intersecao": r["cfg"]["intersecao_estrita"],
            "cfg_sitios_estritos": r["cfg"]["sitios_estritos"],
            "cfg_sitios_uniao": r["cfg"]["sitios_uniao"],
            "dep_total": r["dep_total"], "obs": r["obs"]}
    cats = [rec["arestas"][nm]["categoria_rc"] for nm, *_ in ARESTAS]
    rec["instancia_estrito_rc"] = ("ambas" if all(c == "ESTRITO" for c in cats)
                                   else ("pelo_menos_uma" if any(c == "ESTRITO" for c in cats)
                                         else "nenhuma"))
    regs.append(rec)

# agregação
def conta(f):
    out = {}
    for rec in regs:
        for nome, ar in rec["arestas"].items():
            k = f(ar)
            out[k] = out.get(k, 0) + 1
    return out

cat_rc = conta(lambda ar: ar["categoria_rc"])
cat_cfg = conta(lambda ar: ar["categoria_cfg"])
niveis = conta(lambda ar: ar["nivel"])
inst = {"ambas": 0, "pelo_menos_uma": 0, "nenhuma": 0}
for rec in regs:
    inst[rec["instancia_estrito_rc"]] += 1

def stats_int(vals):
    vals = sorted(vals)
    n_ = len(vals)
    med = vals[n_ // 2] if n_ % 2 else (vals[n_ // 2 - 1] + vals[n_ // 2]) / 2
    return {"n": n_, "min": vals[0], "mediana": med, "max": vals[-1],
            "media": round(sum(vals) / n_, 3)}

nI = [ar["n_I"] for rec in regs for ar in rec["arestas"].values()]
sest = [ar["sitios_estritos_rc"] for rec in regs for ar in rec["arestas"].values()]
orbl = [rec["orbita"] for rec in regs]
obs_c = sum(1 for rec in regs for ar in rec["arestas"].values() if ar["obs"]["pares"] > 0)
obs_d = sum(1 for rec in regs for ar in rec["arestas"].values()
            if ar["obs"]["pares_diferentes"] > 0)

n_ar = 2 * len(regs)
saida = {
    "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
    "reafirmacao": "resultado_confirmatorio_A = negativo (fechado, imutavel)",
    "precommit": "precommit-ws3-fresh-emenda.txt (escrito antes desta execucao)",
    "seed": SEED, "n_aceites": aceites, "tentativas_total": tentativas,
    "taxa_aceitacao": round(aceites / tentativas, 4),
    "prevalencia_categoria_rc": cat_rc,
    "prevalencia_categoria_cfg": cat_cfg,
    "prevalencia_niveis": niveis,
    "instancias_estrito_rc": dict(inst, n=len(regs)),
    "ic95_wilson": {
        "aresta_ESTRITO_rc": dict(k=cat_rc.get("ESTRITO", 0), n=n_ar,
                                  ic=W.wilson(cat_rc.get("ESTRITO", 0), n_ar)),
        "aresta_ESTRITO_cfg": dict(k=cat_cfg.get("ESTRITO", 0), n=n_ar,
                                   ic=W.wilson(cat_cfg.get("ESTRITO", 0), n_ar)),
        "instancia_pelo_menos_uma": dict(
            k=inst["ambas"] + inst["pelo_menos_uma"], n=len(regs),
            ic=W.wilson(inst["ambas"] + inst["pelo_menos_uma"], len(regs))),
        "instancia_ambas": dict(k=inst["ambas"], n=len(regs),
                                ic=W.wilson(inst["ambas"], len(regs))),
    },
    "dist_tamanho_I_rc": stats_int(nI),
    "dist_sitios_estritos_rc": stats_int(sest),
    "dist_orbita": stats_int(orbl),
    "observacional": {"arestas": n_ar, "com_pares": obs_c, "com_par_diferente": obs_d},
    "registos": regs,
    "duracao_s": round(time.time() - t0, 1),
}
corpo = json.dumps(saida, sort_keys=True, indent=1).encode()
open(WS + "/ws3-fresh-baseline.json", "wb").write(corpo)
print("POST-CONFIRMATORY / EXPLORATORY — ws3 baseline fresco (seed %d)" % SEED)
print("aceites=%d de %d tentativas (taxa %.3f)" % (aceites, tentativas, aceites / tentativas))
print("niveis:", niveis)
print("categoria (r,c):", cat_rc)
print("categoria cfg:", cat_cfg)
print("instancias:", dict(inst, n=len(regs)))
print("IC95:", json.dumps(saida["ic95_wilson"], sort_keys=True))
print("|I| rc:", saida["dist_tamanho_I_rc"])
print("sitios estritos rc:", saida["dist_sitios_estritos_rc"])
print("orbita:", saida["dist_orbita"])
print("observacional:", saida["observacional"])
print("duracao: %.1fs" % saida["duracao_s"])
print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
