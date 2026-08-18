# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, ws3.
# Verificação independente (auditoria) dos resultados da tentativa-interrompida-1:
#   Parte 1: fam-20 (7bb0baab3a8ed7aa, n=12, tabela cega) — todos os campos.
#   Parte 2: bateria de 126 famílias (replay próprio + análise própria) —
#            comparação campo a campo com ws3-strict-bateria.json e datasets.
# Nada fora do ws3 dir é escrito. Resultado confirmatório: NEGATIVO, imutável.
import json, sys, hashlib, time
import numpy as np
import ws3_indep as W

DST = W.DST
WS = W.WS
TI = W.TI
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl
import pontuacao as pt

t0 = time.time()
res = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
       "reafirmacao": "resultado_confirmatorio_A = negativo (fechado, imutavel)",
       "proposito": "verificacao independente (rota testemunhas-realizadas) da tentativa-interrompida-1"}
mismatches = []
ncomp = [0]


def cmpv(rotulo, a, b):
    ncomp[0] += 1
    if a != b:
        mismatches.append("%s: %r != %r" % (rotulo, a, b))


# ================================================================ Parte 1: fam-20
ID = "7bb0baab3a8ed7aa"
claims = json.load(open(TI + "/ws3-strict-fam20.json"))
inst_path = DST + "/conf-e2/instancias/%s.json" % ID
inst_bytes = open(inst_path, "rb").read()
res["sha256_instancia"] = hashlib.sha256(inst_bytes).hexdigest()
inst = json.loads(inst_bytes)
chave = json.load(open(DST + "/chave-e2.json"))

# tipos: reimplementação própria de pt._tipos_e2 + cross-check
canon = ["A", "B", "C_AB", "C_BA", "D1", "D2"]
tipos = [canon[j] for j in chave[ID]["ordem_modulos"]]
cmpv("fam20.tipos_vs_pt", tipos, pt._tipos_e2(chave[ID]))
idx = {t: i for i, t in enumerate(tipos)}

n = inst["n"]
T = np.asarray(inst["transicao"], dtype=np.int64)
s0 = int(inst["estado_inicial"])
mods = inst["modulos"]
orb = W.minha_orbita(T, s0)
cmpv("fam20.orbita_vs_cl", orb, cl.orbita(T, s0))
cmpv("fam20.len_orbita", len(orb), claims["orbita"])
cmpv("fam20.s0", s0, claims["estado_inicial"])

core_bits = sorted(sum((mods[idx[t]]["bits"] for t in ("A", "B", "C_AB", "C_BA")), []))
res["fam20"] = {"tipos": tipos, "core_bits": core_bits, "n": n, "orbita": len(orb)}

for nome, a_t, b_t in (("C_AB->B", "C_AB", "B"), ("C_BA->A", "C_BA", "A")):
    a_i, b_i = idx[a_t], idx[b_t]
    bits_a = mods[a_i]["bits"]
    bits_b = mods[b_i]["bits"]
    membits = mods[b_i]["bits_memoria"]
    r = W.analisa_aresta_indep(T, n, bits_a, bits_b, membits, orb, len(bits_b))
    ca = claims["arestas"][nome]

    # órbita_coords (as 25 coordenadas (m,r,c) desta aresta)
    mm = 1 << membits[0]
    procbits = [b for b in bits_b if b not in membits]
    eP = W.ext_tab(procbits, n); eC = W.ext_tab(bits_a, n)
    for t_i, s in enumerate(orb):
        row = claims["orbita_coords"][t_i]
        cmpv("fam20.%s.coords[%d].estado" % (nome, t_i), int(s), row["estado"])
        cmpv("fam20.%s.coords[%d]" % (nome, t_i),
             {"m": int((s & mm) != 0), "r": int(eP[s]), "c": int(eC[s])}, row[nome])

    cmpv("fam20.%s.nivel" % nome, r["nivel"], ca["nivel"])
    cmpv("fam20.%s.d0" % nome, r["d0"], ca["d0"])
    cmpv("fam20.%s.d1" % nome, r["d1"], ca["d1"])
    cmpv("fam20.%s.dep_total" % nome, r["dep_total"], ca["dep_total"])
    cmpv("fam20.%s.exc_reducao" % nome, r["exc_reducao"], 0)
    cmpv("fam20.%s.cfg" % nome, r["cfg"], ca["cfg"])
    cmpv("fam20.%s.rc" % nome,
         {k: r["rc"][k] for k in ("I", "n_C0", "n_C1", "n_I", "n_U",
                                  "sitios_totais", "sitios_uniao", "sitios_estritos")},
         {k: ca["rc"][k] for k in ("I", "n_C0", "n_C1", "n_I", "n_U",
                                   "sitios_totais", "sitios_uniao", "sitios_estritos")})
    cmpv("fam20.%s.obs" % nome, r["obs"], ca["obs"])
    cmpv("fam20.%s.obs_detalhe" % nome, r["obs_detalhe"], ca["obs_detalhe"])
    cmpv("fam20.%s.categoria_cfg" % nome, r["categoria_cfg"], ca["categoria_cfg"])
    cmpv("fam20.%s.categoria_rc" % nome, r["categoria_rc"], ca["categoria_rc"])
    cmpv("fam20.%s.intervencoes" % nome, [[mk, vl] for (mk, vl) in r["ints"]],
         ca["intervencoes"])
    cmpv("fam20.%s.pat_cells" % nome,
         {str(m): [list(map(int, p)) for p in r["pat"][m]] for m in (0, 1)},
         ca["pat_cells"])
    minhas_test = sorted((k, cell, p0, p1) for (k, cell, p0, p1) in r["testemunhas"])
    deles = sorted((w["intervencao"], (w["r"] << 2) | w["c"], w["padrao_m0"], w["padrao_m1"])
                   for w in ca["testemunhas_estritas"])
    cmpv("fam20.%s.testemunhas" % nome, minhas_test, deles)

    # granularidade nuclear (configuração sem bits D, sem bit de memória do receptor)
    core_free = [b for b in core_bits if b not in membits]
    cmask = np.int64(0)
    for b in core_free:
        cmask |= np.int64(1 << b)
    orbA = np.array(orb, dtype=np.int64)
    m_orb = ((orbA & mm) != 0).astype(int)
    ckey = orbA & cmask
    Sc = {0: set(), 1: set()}
    for i in range(len(orb)):
        Sc[int(m_orb[i])].add(int(ckey[i]))
    interC = Sc[0] & Sc[1]; uniC = Sc[0] | Sc[1]
    eB = W.ext_tab(bits_b, n)
    core_estr = core_uni = 0
    for k_i, (mk, vl) in enumerate(r["ints"]):
        p0, p1 = r["pat"][0][k_i], r["pat"][1][k_i]
        for kv in interC:
            cell = int((eP[kv] << 2) | eC[kv])
            if p0[cell] != p1[cell]:
                core_estr += 1
        for kv in uniC:
            cell = int((eP[kv] << 2) | eC[kv])
            if p0[cell] != p1[cell]:
                core_uni += 1
    cmpv("fam20.%s.core" % nome,
         {"S0": len(Sc[0]), "S1": len(Sc[1]), "intersecao": len(interC),
          "uniao": len(uniC), "sitios_estritos": core_estr, "sitios_uniao": core_uni},
         ca["core"])
    cmpv("fam20.%s.categoria_core" % nome,
         W.categoria(core_estr, core_uni, r["dep_total"], len(interC) == 0),
         ca["categoria_core"])

cmpv("fam20.OR_54_51",
     sorted(claims["replicacao_OR_step3b"]["sitios_uniao_config_por_aresta"].values()),
     [51, 54])
res["fam20"]["comparacoes_ok"] = not any(m.startswith("fam20") for m in mismatches)
print("Parte 1 (fam-20): %d comparacoes, mismatches ate agora: %d"
      % (ncomp[0], len(mismatches)))

# ================================================================ Parte 2: bateria
bat = json.load(open(TI + "/ws3-strict-bateria.json"))
LOTES = {910000001: DST + "/prevalencia/prevalencia-cancelamento-II.json",
         910000002: DST + "/prevalencia/prevalencia-cancelamento-II-lote2.json"}
GRUPO = {"colapso_total": "G2_colapso", "individua_ambas": "G3_controlo_L3L3",
         "individua_uma": "G4_misto"}
alvos = []
counts_classe = {}
for seed, path in LOTES.items():
    d = json.load(open(path))
    for classe, grupo in GRUPO.items():
        rs = d["exemplos"][classe]
        counts_classe["%d/%s" % (seed, classe)] = len(rs)
        for rec in rs:
            alvos.append({"seed": seed, "tentativa": rec["tentativa"], "fam": rec["fam"],
                          "grupo": grupo, "theta_sha": rec["theta_sha"],
                          "arestas_dataset": rec["arestas"]})
res["counts_classe_datasets"] = counts_classe
cmpv("bateria.n_alvos", len(alvos), 126)
cmpv("bateria.classes_esperadas", counts_classe,
     {"910000001/colapso_total": 22, "910000001/individua_ambas": 20,
      "910000001/individua_uma": 20, "910000002/colapso_total": 24,
      "910000002/individua_ambas": 20, "910000002/individua_uma": 20})

thetas = {}
for seed in LOTES:
    alvo_sha = {a["tentativa"]: a["theta_sha"] for a in alvos if a["seed"] == seed}
    reps = W.replay_meu(seed, alvo_sha)
    thetas.update({(seed, t): th for t, th in reps.items()})
print("replay proprio: %d thetas verificados por sha" % len(thetas))
cmpv("bateria.replay", len(thetas), 126)

regs_meus = {}
ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5]), ("C_BA->A", [8, 9], [0, 1, 2], [2]))
claims_by = {(rec["seed"], rec["tentativa"]): rec for rec in bat["registos"]}
cmpv("bateria.n_registos_claims", len(claims_by), 126)

for a in alvos:
    th = thetas[(a["seed"], a["tentativa"])]
    tab, n10, lay = g.tabela_transicao("II", th, False)
    cmpv("t%d.tabela_g_vs_minha" % a["tentativa"], list(tab), W.tabela_II_minha(th))
    T10 = np.asarray(tab, dtype=np.int64)
    s010 = g._campos_para_int(g.estado_inicial("II", th), lay)
    orb10 = W.minha_orbita(T10, s010)
    cmpv("t%d.orbita_vs_cl" % a["tentativa"], orb10, cl.orbita(T10, s010))
    crec = claims_by[(a["seed"], a["tentativa"])]
    cmpv("t%d.orbita_len" % a["tentativa"], len(orb10), crec["orbita"])
    cats_rc = []
    for nome, bits_a, bits_b, membits in ARESTAS:
        r = W.analisa_aresta_indep(T10, n10, bits_a, bits_b, membits, orb10, len(bits_b))
        cl_ar = crec["arestas"][nome]
        ds = a["arestas_dataset"][nome]
        cmpv("t%d.%s.nivel" % (a["tentativa"], nome), r["nivel"], cl_ar["nivel"])
        cmpv("t%d.%s.nivel_ds" % (a["tentativa"], nome), r["nivel"], ds["nivel"])
        cmpv("t%d.%s.dep" % (a["tentativa"], nome), r["dep_total"], cl_ar["dep_total"])
        cmpv("t%d.%s.dep_ds" % (a["tentativa"], nome), r["dep_total"], ds["dep_sites"])
        if "d0" in ds:
            cmpv("t%d.%s.d_ds" % (a["tentativa"], nome), [r["d0"], r["d1"]],
                 [ds["d0"], ds["d1"]])
        cmpv("t%d.%s.cfg" % (a["tentativa"], nome), r["cfg"], cl_ar["cfg"])
        cmpv("t%d.%s.rc" % (a["tentativa"], nome),
             {k: r["rc"][k] for k in cl_ar["rc"]}, cl_ar["rc"])
        cmpv("t%d.%s.obs" % (a["tentativa"], nome), r["obs"], cl_ar["obs"])
        cmpv("t%d.%s.cat_cfg" % (a["tentativa"], nome), r["categoria_cfg"], cl_ar["categoria_cfg"])
        cmpv("t%d.%s.cat_rc" % (a["tentativa"], nome), r["categoria_rc"], cl_ar["categoria_rc"])
        cmpv("t%d.%s.exc_red" % (a["tentativa"], nome), r["exc_reducao"], 0)
        # fórmula a partir de theta (independente da tabela): padrões e d
        eCi = W.ext_tab(bits_a, n10)
        dth, pth = W.formula_theta(th, nome, r["ints"], lambda v: int(eCi[v]))
        cmpv("t%d.%s.formula_d" % (a["tentativa"], nome), [dth[0], dth[1]], [r["d0"], r["d1"]])
        cmpv("t%d.%s.formula_pat" % (a["tentativa"], nome),
             [[list(map(int, p)) for p in r["pat"][m]] for m in (0, 1)],
             [pth[0], pth[1]])
        iso = W.tau_isometria(th, nome)
        cmpv("t%d.%s.tau_iso" % (a["tentativa"], nome), iso, cl_ar["tau_isometria_W"])
        cmpv("t%d.%s.K_L1" % (a["tentativa"], nome), iso, r["nivel"] == "L1_d_iguais")
        cats_rc.append(r["categoria_rc"])
        regs_meus.setdefault((a["seed"], a["tentativa"]), {}).update(
            {nome: {"nivel": r["nivel"], "categoria_rc": r["categoria_rc"],
                    "categoria_cfg": r["categoria_cfg"], "n_I": r["rc"]["n_I"],
                    "sitios_estritos": r["rc"]["sitios_estritos"],
                    "obs": r["obs"], "grupo": a["grupo"]}})
    inst_cat = ("ambas" if all(c == "ESTRITO" for c in cats_rc)
                else ("pelo_menos_uma" if any(c == "ESTRITO" for c in cats_rc) else "nenhuma"))
    cmpv("t%d.instancia" % a["tentativa"], inst_cat, crec["instancia_estrito_rc"])

# agregados recomputados dos MEUS registos vs agregados do claims JSON
def agrega_minha(chave_cat):
    out = {}
    for (seed, t), edges in regs_meus.items():
        for nome, e in edges.items():
            d = out.setdefault(e["grupo"], {})
            d[e[chave_cat]] = d.get(e[chave_cat], 0) + 1
    return out

agg_rc = agrega_minha("categoria_rc")
agg_cfg = agrega_minha("categoria_cfg")
for grupo in ("G2_colapso", "G3_controlo_L3L3", "G4_misto"):
    cmpv("agg.rc.%s" % grupo, agg_rc.get(grupo, {}),
         bat["prevalencia_categoria_rc_por_grupo"].get(grupo, {}))
    cmpv("agg.cfg.%s" % grupo, agg_cfg.get(grupo, {}),
         bat["prevalencia_categoria_cfg_por_grupo"].get(grupo, {}))

inst_meus = {}
for a in alvos:
    edges = regs_meus[(a["seed"], a["tentativa"])]
    cats = [edges[nm]["categoria_rc"] for nm in ("C_AB->B", "C_BA->A")]
    cat = ("ambas" if all(c == "ESTRITO" for c in cats)
           else ("pelo_menos_uma" if any(c == "ESTRITO" for c in cats) else "nenhuma"))
    dd = inst_meus.setdefault(a["grupo"], {"ambas": 0, "pelo_menos_uma": 0, "nenhuma": 0, "n": 0})
    dd[cat] += 1
    dd["n"] += 1
cmpv("agg.instancias", inst_meus, bat["instancias_estrito_rc"])

# proporções com IC95 (Wilson) para o relatório
def prop(grupo, cat, gran):
    src = agg_rc if gran == "rc" else agg_cfg
    tot = sum(src[grupo].values())
    k = src[grupo].get(cat, 0)
    lo, hi = W.wilson(k, tot)
    return {"k": k, "n": tot, "prop": round(k / tot, 4), "ic95": [lo, hi]}

res["proporcoes"] = {
    "edges_ESTRITO_rc": {gr: prop(gr, "ESTRITO", "rc") for gr in agg_rc},
    "edges_ESTRITO_cfg": {gr: prop(gr, "ESTRITO", "cfg") for gr in agg_cfg},
    "instancias": {gr: {"ambas": inst_meus[gr]["ambas"],
                        "pelo_menos_uma_ou_ambas": inst_meus[gr]["ambas"] + inst_meus[gr]["pelo_menos_uma"],
                        "n": inst_meus[gr]["n"],
                        "ic95_pelo_menos_uma": W.wilson(
                            inst_meus[gr]["ambas"] + inst_meus[gr]["pelo_menos_uma"],
                            inst_meus[gr]["n"])} for gr in inst_meus},
}

res["comparacoes_total"] = ncomp[0]
res["mismatches"] = mismatches
res["veredicto"] = "VERIFICADO_SEM_DISCREPANCIAS" if not mismatches else "DISCREPANCIAS_ENCONTRADAS"
res["duracao_s"] = round(time.time() - t0, 1)

corpo = json.dumps(res, sort_keys=True, indent=1).encode()
open(WS + "/ws3-verificacao-independente.json", "wb").write(corpo)
print("comparacoes totais: %d" % ncomp[0])
print("MISMATCHES: %s" % (mismatches[:20] if mismatches else "nenhum"))
print("veredicto: %s" % res["veredicto"])
print("proporcoes:", json.dumps(res["proporcoes"], indent=1, sort_keys=True))
print("duracao: %.1fs" % res["duracao_s"])
print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
