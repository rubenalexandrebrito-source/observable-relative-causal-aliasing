# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, ws3.
# Script B: bateria pré-definida (precommit-ws3-strict.txt):
#   G2 = TODOS os 46 colapso_total (lotes 910000001/910000002),
#   G3 = 40 controlos L3/L3 (individua_ambas), G4 = 40 mistos (individua_uma).
# Replay por (seed registada, tentativa) com verificação theta_sha; análise
# estrita por aresta nas granularidades configuração e (r,c); cross-checks
# X1-X3, X5, X6 obrigatórios. Sem sementes novas. Resultado confirmatório:
# NEGATIVO, imutável.
import json, time, hashlib
import numpy as np
import ws3_lib as L
import sys
sys.path.insert(0, L.DST + "/frozen-copy")
import gerador as g
import classificador as cl

SAIDA = L.DST + "/multiagent/ws3-realized-dynamics/ws3-strict-bateria.json"
t0 = time.time()

LOTES = {910000001: L.DST + "/prevalencia/prevalencia-cancelamento-II.json",
         910000002: L.DST + "/prevalencia/prevalencia-cancelamento-II-lote2.json"}
GRUPO_POR_CLASSE = {"colapso_total": "G2_colapso",
                    "individua_ambas": "G3_controlo_L3L3",
                    "individua_uma": "G4_misto"}

alvos = []          # [{seed, tentativa, fam, grupo, subtipo, arestas_dataset}]
for seed, path in LOTES.items():
    d = json.load(open(path))
    for classe, grupo in GRUPO_POR_CLASSE.items():
        for rec in d["exemplos"][classe]:
            niveis = sorted(v["nivel"] for v in rec["arestas"].values())
            subt = "+".join(x.split("_")[0] for x in niveis)
            alvos.append({"seed": seed, "tentativa": rec["tentativa"],
                          "fam": rec["fam"], "grupo": grupo, "subtipo": subt,
                          "theta_sha": rec["theta_sha"],
                          "arestas_dataset": rec["arestas"]})
print("alvos: %d (G2=%d G3=%d G4=%d)" % (
    len(alvos), sum(a["grupo"] == "G2_colapso" for a in alvos),
    sum(a["grupo"] == "G3_controlo_L3L3" for a in alvos),
    sum(a["grupo"] == "G4_misto" for a in alvos)))
assert len(alvos) == 126, "bateria != 126 alvos — PARAR (regra 10)"

# ---- X1: replay com verificacao de theta_sha ----
thetas = {}
for seed in LOTES:
    alvo_sha = {a["tentativa"]: a["theta_sha"] for a in alvos if a["seed"] == seed}
    reps = L.replay_lote(seed, alvo_sha)
    for t, th in reps.items():
        thetas[(seed, t)] = th
    print("replay seed %d: %d/%d alvos verificados (theta_sha + elegibilidade)"
          % (seed, len(reps), len(alvo_sha)))
assert len(thetas) == 126

# ---- analise por familia ----
cc = {"nivel_ok": 0, "dep_ok": 0, "d_ok": 0, "d_presentes": 0,
      "formula_d_ok": 0, "formula_pat_ok": 0, "k_ok": 0, "reducao_ok": 0,
      "total_arestas": 0}
falhas = []
registos = []
for a in alvos:
    th = thetas[(a["seed"], a["tentativa"])]
    tab, n, lay = g.tabela_transicao("II", th, False)
    T = np.asarray(tab, dtype=np.int64)
    s0 = g._campos_para_int(g.estado_inicial("II", th), lay)
    orb = cl.orbita(T, s0)
    rec = {"seed": a["seed"], "tentativa": a["tentativa"], "fam": a["fam"],
           "grupo": a["grupo"], "subtipo": a["subtipo"], "orbita": len(orb),
           "arestas": {}}
    for nome, bits_a, bits_b, membits in L.ARESTAS_N10:
        cc["total_arestas"] += 1
        r = L.analisa_aresta_realizada(T, n, bits_a, bits_b, membits, orb)
        pat_np = r.pop("_pat_cells_np")
        ds = a["arestas_dataset"][nome]
        # X2/X3
        if r["nivel"] == ds["nivel"]:
            cc["nivel_ok"] += 1
        else:
            falhas.append("%s t%d %s nivel %s != %s" % (a["seed"], a["tentativa"], nome, r["nivel"], ds["nivel"]))
        if r["dep_total"] == ds["dep_sites"]:
            cc["dep_ok"] += 1
        else:
            falhas.append("%s t%d %s dep %d != %d" % (a["seed"], a["tentativa"], nome, r["dep_total"], ds["dep_sites"]))
        if "d0" in ds:
            cc["d_presentes"] += 1
            if r["d0"] == ds["d0"] and r["d1"] == ds["d1"]:
                cc["d_ok"] += 1
            else:
                falhas.append("%s t%d %s d0/d1 != dataset" % (a["seed"], a["tentativa"], nome))
        # X5
        if r["exc_reducao"] == 0 and r["dep_total"] == r["multiplicidade_celula"] * r["rc"]["sitios_totais"]:
            cc["reducao_ok"] += 1
        else:
            falhas.append("%s t%d %s reducao violada" % (a["seed"], a["tentativa"], nome))
        # X6: formula a partir de theta
        fd0, fd1, fpats = L.formula_theta_aresta(th, nome, bits_a, n)
        if fd0 == r["d0"] and fd1 == r["d1"]:
            cc["formula_d_ok"] += 1
        else:
            falhas.append("%s t%d %s formula d != fibra" % (a["seed"], a["tentativa"], nome))
        pat_ok = all(int(pat_np[m][k][cell]) == fpats[m][k][cell]
                     for m in (0, 1) for k in range(9) for cell in range(16))
        if pat_ok:
            cc["formula_pat_ok"] += 1
        else:
            falhas.append("%s t%d %s padroes formula != fibra" % (a["seed"], a["tentativa"], nome))
        iso, tau, _ = L.k_audit(th, nome)
        if iso == (r["nivel"] == "L1_d_iguais"):
            cc["k_ok"] += 1
        else:
            falhas.append("%s t%d %s K-audit: iso=%s mas nivel=%s" % (a["seed"], a["tentativa"], nome, iso, r["nivel"]))
        rec["arestas"][nome] = {
            "nivel": r["nivel"], "dep_total": r["dep_total"],
            "cfg": r["cfg"], "rc": {k: v for k, v in r["rc"].items()
                                    if k not in ("C0", "C1", "U")},
            "obs": r["obs"],
            "categoria_cfg": r["categoria_cfg"], "categoria_rc": r["categoria_rc"],
            "tau_isometria_W": bool(iso)}
    cats = [rec["arestas"][nm]["categoria_rc"] for nm in rec["arestas"]]
    rec["instancia_estrito_rc"] = ("ambas" if all(c == "ESTRITO" for c in cats)
                                   else ("pelo_menos_uma" if any(c == "ESTRITO" for c in cats)
                                         else "nenhuma"))
    registos.append(rec)

# ---- agregacao ----
def agrega(regs, chave_cat):
    grupos = {}
    for rec in regs:
        for nome, ar in rec["arestas"].items():
            gkey = (rec["grupo"], rec["subtipo"]) if rec["grupo"] == "G2_colapso" else (rec["grupo"],)
            for k in [gkey, (rec["grupo"],)] if rec["grupo"] == "G2_colapso" else [gkey]:
                d = grupos.setdefault("/".join(k), {})
                d[ar[chave_cat]] = d.get(ar[chave_cat], 0) + 1
    return grupos

def agrega_por_nivel(regs, chave_cat):
    out = {}
    for rec in regs:
        for nome, ar in rec["arestas"].items():
            d = out.setdefault(ar["nivel"], {})
            d[ar[chave_cat]] = d.get(ar[chave_cat], 0) + 1
    return out

prev_rc = agrega(registos, "categoria_rc")
prev_cfg = agrega(registos, "categoria_cfg")
prev_nivel_rc = agrega_por_nivel(registos, "categoria_rc")

inst_prev = {}
for rec in registos:
    d = inst_prev.setdefault(rec["grupo"], {"ambas": 0, "pelo_menos_uma": 0, "nenhuma": 0, "n": 0})
    d[rec["instancia_estrito_rc"]] += 1
    d["n"] += 1

def stats_int(vals):
    vals = sorted(vals)
    n_ = len(vals)
    return {"n": n_, "min": vals[0], "mediana": vals[n_ // 2] if n_ % 2 else (vals[n_ // 2 - 1] + vals[n_ // 2]) / 2,
            "max": vals[-1], "media": round(sum(vals) / n_, 3)}

dist_I = {}
dist_sitios = {}
obs_res = {}
for rec in registos:
    for nome, ar in rec["arestas"].items():
        gk = rec["grupo"] + ("/" + rec["subtipo"] if rec["grupo"] == "G2_colapso" else "")
        dist_I.setdefault(gk, []).append(ar["rc"]["n_I"])
        dist_sitios.setdefault(gk, []).append(ar["rc"]["sitios_estritos"])
        o = obs_res.setdefault(gk, {"arestas": 0, "com_pares": 0, "com_par_diferente": 0})
        o["arestas"] += 1
        if ar["obs"]["pares"] > 0:
            o["com_pares"] += 1
        if ar["obs"]["pares_diferentes"] > 0:
            o["com_par_diferente"] += 1

saida = {
    "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
    "reafirmacao": "resultado_confirmatorio_A = negativo (fechado, imutavel)",
    "precommit": "precommit-ws3-strict.txt (sha registada no SHAS.txt)",
    "bateria": {"n_familias": len(registos), "G2": 46, "G3": 40, "G4": 40},
    "cross_checks": cc, "cross_checks_falhas": falhas,
    "prevalencia_categoria_rc_por_grupo": prev_rc,
    "prevalencia_categoria_cfg_por_grupo": prev_cfg,
    "prevalencia_categoria_rc_por_nivel_aresta": prev_nivel_rc,
    "instancias_estrito_rc": inst_prev,
    "dist_tamanho_I_rc": {k: stats_int(v) for k, v in sorted(dist_I.items())},
    "dist_sitios_estritos_rc": {k: stats_int(v) for k, v in sorted(dist_sitios.items())},
    "observacional": obs_res,
    "registos": registos,
    "duracao_s": round(time.time() - t0, 1),
}
corpo = json.dumps(saida, sort_keys=True, indent=1).encode()
open(SAIDA, "wb").write(corpo)

print("\n===== CROSS-CHECKS (252 arestas) =====")
for k in sorted(cc):
    print("  %-16s: %d" % (k, cc[k]))
print("  FALHAS: %s" % (falhas if falhas else "nenhuma"))
print("\n===== PREVALENCIA categoria (r,c) por grupo/aresta =====")
for k in sorted(prev_rc):
    print("  %-24s: %s" % (k, prev_rc[k]))
print("===== PREVALENCIA categoria CONFIG por grupo/aresta =====")
for k in sorted(prev_cfg):
    print("  %-24s: %s" % (k, prev_cfg[k]))
print("===== por nivel de aresta (rc) =====")
for k in sorted(prev_nivel_rc):
    print("  %-28s: %s" % (k, prev_nivel_rc[k]))
print("===== instancias (>=1 / ambas ESTRITO rc) =====")
for k in sorted(inst_prev):
    print("  %-20s: %s" % (k, inst_prev[k]))
print("===== |I| (celulas (r,c) em ambos os contextos) =====")
for k in sorted(dist_I):
    print("  %-24s: %s" % (k, stats_int(dist_I[k])))
print("===== sitios estritos (rc) =====")
for k in sorted(dist_sitios):
    print("  %-24s: %s" % (k, stats_int(dist_sitios[k])))
print("===== observacional =====")
for k in sorted(obs_res):
    print("  %-24s: %s" % (k, obs_res[k]))
print("\nduracao: %.1fs" % (time.time() - t0))
print("saida:", SAIDA)
print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
