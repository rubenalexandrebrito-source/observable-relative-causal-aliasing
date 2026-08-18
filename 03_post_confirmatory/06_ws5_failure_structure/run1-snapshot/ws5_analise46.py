# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY - Pre-registo A v8.3, Fase 6, WS5.
Analise estrutural dos 46 casos de colapso: lema de necessidade (prova por
eliminacao inteira exacta), caracterizacao por caso, mecanismo de L2,
referencia fam-20, e clustering hierarquico sem k fixado a priori.
So le ws5-casos46.json / ws5-familias-N10000.json e a referencia fam20 ja
publicada; escreve apenas no ws dir. NADA confirmatorio e alterado.
"""
import json, hashlib, itertools
from fractions import Fraction

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws5-failure-structure"
SAIDA = WS + "/ws5-analise46.json"

SUBS = [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2),
        (3, 0), (3, 1), (3, 2), (3, 3)]
PERMS = [tuple(p) for p in itertools.permutations(range(4))]
PARES = [(a, b) for a in range(4) for b in range(a + 1, 4)]


# ---------------------------------------------------------------- lema
def lema_necessidade():
    """Sistema linear: para Delta simetrica (diag nula, 6 g.l.),
    S_a(Delta) = sum_c Delta(c, sub_a(c)) = 0 para as 9 intervencoes
    => Delta = 0. Eliminacao de Gauss exacta sobre Q."""
    A = []
    for (mc, vc) in SUBS:
        row = [0] * 6
        for c in range(4):
            t = (c & ~mc) | vc
            if t != c:
                i = PARES.index((min(c, t), max(c, t)))
                row[i] += 1
        A.append([Fraction(x) for x in row])
    # rank por eliminacao
    M = [r[:] for r in A]
    rank, rowi = 0, 0
    for col in range(6):
        piv = None
        for r in range(rowi, len(M)):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        M[rowi], M[piv] = M[piv], M[rowi]
        pv = M[rowi][col]
        M[rowi] = [x / pv for x in M[rowi]]
        for r in range(len(M)):
            if r != rowi and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[rowi])]
        rowi += 1
        rank += 1
    return {"matriz_9x6": [[int(x) for x in r] for r in A],
            "rank": rank, "nucleo_trivial": rank == 6}


# ------------------------------------------------------- utilidades W
def degs_de(W):
    return [sum(W[p][q] for q in range(4)) for p in range(4)]


def grupo_iso(W):
    return [p for p in PERMS
            if all(W[p[a]][p[b]] == W[a][b] for a in range(4) for b in range(4))]


def rank_canonico(vals):
    ordenados = sorted(set(vals))
    idx = {v: i for i, v in enumerate(ordenados)}
    return tuple(idx[v] for v in vals)


def hist(xs):
    h = {}
    for x in xs:
        h[str(x)] = h.get(str(x), 0) + 1
    return dict(sorted(h.items(), key=lambda kv: kv[0]))


# ------------------------------------------------------- clustering
def gower(X, tipos):
    n = len(X)
    m = len(tipos)
    rng = []
    for j, t in enumerate(tipos):
        if t == "num":
            v = [x[j] for x in X]
            rng.append(max(v) - min(v) or 1.0)
        else:
            rng.append(None)
    D = [[0.0] * n for _ in range(n)]
    for a in range(n):
        for b in range(a + 1, n):
            s = 0.0
            for j, t in enumerate(tipos):
                if t == "num":
                    s += abs(X[a][j] - X[b][j]) / rng[j]
                else:
                    s += 0.0 if X[a][j] == X[b][j] else 1.0
            D[a][b] = D[b][a] = s / m
    return D


def hier(D, linkage):
    n = len(D)
    ativo = {i: [i] for i in range(n)}
    dist = {(a, b): D[a][b] for a in range(n) for b in range(a + 1, n)}
    merges = []          # (altura, membros_novos)
    rotulos = {i: i for i in range(n)}
    nxt = n
    def dpair(ca, cb):
        vals = [D[x][y] for x in ativo[ca] for y in ativo[cb]]
        if linkage == "single":
            return min(vals)
        if linkage == "complete":
            return max(vals)
        return sum(vals) / len(vals)
    chaves = list(ativo)
    while len(ativo) > 1:
        melhor, par = None, None
        ks = sorted(ativo)
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                d = dpair(ks[i], ks[j])
                if melhor is None or d < melhor:
                    melhor, par = d, (ks[i], ks[j])
        a, b = par
        ativo[nxt] = ativo.pop(a) + ativo.pop(b)
        merges.append((melhor, sorted(ativo[nxt])))
        nxt += 1
    return merges


def corta(merges, n, k):
    # reconstruir: aplicar merges ate restarem k clusters
    ativo = {i: [i] for i in range(n)}
    nxt = n
    for h, membros in merges:
        if len(ativo) <= k:
            break
        # encontrar os dois clusters cuja uniao = membros
        alvo = set(membros)
        fontes = [c for c, ms in ativo.items() if set(ms) <= alvo]
        novo = []
        for c in fontes:
            novo += ativo.pop(c)
        ativo[nxt] = sorted(novo)
        nxt += 1
    lab = [0] * n
    for ci, (c, ms) in enumerate(sorted(ativo.items())):
        for m in ms:
            lab[m] = ci
    return lab


def silhueta(D, lab):
    n = len(lab)
    ks = set(lab)
    if len(ks) < 2:
        return None
    ss = []
    for i in range(n):
        mesmos = [j for j in range(n) if lab[j] == lab[i] and j != i]
        if not mesmos:
            ss.append(0.0)        # convencao: silhueta 0 para singletoes
            continue
        a = sum(D[i][j] for j in mesmos) / len(mesmos)
        bs = []
        for c in ks:
            if c == lab[i]:
                continue
            outros = [j for j in range(n) if lab[j] == c]
            bs.append(sum(D[i][j] for j in outros) / len(outros))
        b = min(bs)
        ss.append((b - a) / max(a, b) if max(a, b) > 0 else 0.0)
    return sum(ss) / n


def ari(l1, l2):
    n = len(l1)
    from collections import Counter
    c1, c2 = Counter(l1), Counter(l2)
    c12 = Counter(zip(l1, l2))
    def comb2(x):
        return x * (x - 1) // 2
    idx = sum(comb2(v) for v in c12.values())
    e1 = sum(comb2(v) for v in c1.values())
    e2 = sum(comb2(v) for v in c2.values())
    tot = comb2(n)
    exp = e1 * e2 / tot if tot else 0.0
    mx = (e1 + e2) / 2
    return (idx - exp) / (mx - exp) if mx != exp else 1.0


# ------------------------------------------------------------------ main
def main():
    dados = json.load(open(WS + "/ws5-casos46.json"))
    casos = dados["casos"]
    fams = json.load(open(WS + "/ws5-familias-N10000.json"))["familias"]
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY", "ws": "ws5",
           "resultado_confirmatorio": "negativo (imutavel)"}

    # (A) lema de necessidade
    out["lema_necessidade"] = lema_necessidade()
    print("LEMA necessidade: rank =", out["lema_necessidade"]["rank"],
          "nucleo trivial =", out["lema_necessidade"]["nucleo_trivial"])

    # (B) caracterizacao
    assert len(casos) == 46
    subt_ord = hist([str(tuple(c["subtipo"])) for c in casos])
    subt_uno = hist([str(tuple(sorted(c["subtipo"]))) for c in casos])
    out["subtipos_ordenados_(nivB,nivA)"] = subt_ord
    out["subtipos_nao_ordenados"] = subt_uno

    tau46 = hist([c["tau_classe"] for c in casos])
    tau_all = hist([f["tau_classe"] for f in fams])
    cell46 = hist([c["cell"] for c in casos])
    cell_all = hist([f["cell"] for f in fams])
    out["tau_classe_46"] = tau46
    out["tau_classe_10000"] = tau_all
    out["cell_46"] = cell46
    out["cell_10000"] = cell_all

    # enriquecimento por celula: P(colapso | celula)
    col_by_cell = {}
    n_by_cell = {}
    for f in fams:
        n_by_cell[f["cell"]] = n_by_cell.get(f["cell"], 0) + 1
        if f["nivB"] != "L3" and f["nivA"] != "L3":
            col_by_cell[f["cell"]] = col_by_cell.get(f["cell"], 0) + 1
    out["P_colapso_por_celula"] = {
        c: {"n": n_by_cell[c], "colapsos": col_by_cell.get(c, 0),
            "taxa": round(col_by_cell.get(c, 0) / n_by_cell[c], 6)}
        for c in sorted(n_by_cell)}

    # por aresta e nivel: geometria
    geom = {"L1": {"iso": [], "equidist": 0, "neq": [], "n": 0},
            "L2": {"iso": [], "equidist": 0, "neq": [], "n": 0}}
    forced_sel = {"forced_iso24": 0, "sel_iso<24": 0}
    iso_pairs = []
    for c in casos:
        for nome in ("C_AB->B", "C_BA->A"):
            a = c["arestas"][nome]
            gv = geom[a["nivel"]]
            gv["n"] += 1
            gv["iso"].append(a["iso_n"])
            gv["neq"].append(a["neq"])
            gv["equidist"] += int(a["equidistante"])
            if a["nivel"] == "L1":
                forced_sel["forced_iso24" if a["iso_n"] == 24
                           else "sel_iso<24"] += 1
        iso_pairs.append(tuple(sorted([c["arestas"]["C_AB->B"]["iso_n"],
                                       c["arestas"]["C_BA->A"]["iso_n"]])))
    out["geometria_por_nivel"] = {
        nv: {"n_arestas": gv["n"], "equidistantes": gv["equidist"],
             "hist_iso": hist(gv["iso"]), "hist_neq": hist(gv["neq"])}
        for nv, gv in geom.items()}
    out["L1_forced_vs_selected"] = forced_sel
    out["pares_iso_por_caso"] = hist([str(p) for p in iso_pairs])
    out["hist_orbita"] = hist([c["orbita_len"] for c in casos])
    out["hist_dep_B"] = hist([c["arestas"]["C_AB->B"]["dep_sites"] for c in casos])
    out["hist_dep_A"] = hist([c["arestas"]["C_BA->A"]["dep_sites"] for c in casos])
    out["controlo_sigma"] = {
        "sigmaA": hist([str(c["sigmaA"]) for c in casos]),
        "sigmaB_dist": hist([len(set(c["sigmaB"])) for c in casos])}

    # (C) mecanismo de L2 - verificacao das condicoes ordinais
    l2_edges = []
    for c in casos:
        for nome in ("C_AB->B", "C_BA->A"):
            a = c["arestas"][nome]
            if a["nivel"] != "L2":
                continue
            W = a["W"]
            degs = degs_de(W)
            S0, S1 = a["S0"], a["S1"]
            assert S0 != S1 and rank_canonico(S0) == rank_canonico(S1)
            assert not a["tau_in_iso"]
            n_changed = sum(1 for x, y in zip(S0, S1) if x != y)
            l2_edges.append({
                "caso": c["theta_sha"][:16], "aresta": nome,
                "iso_n": a["iso_n"], "neq": a["neq"],
                "n_dist_perfil": a["n_dist_perfil0"],
                "posicoes_alteradas": n_changed,
                "graus_regulares": len(set(degs)) == 1,
                "n_graus_dist": a["n_graus_dist"],
                "n_offdiag_dist": a["n_offdiag_dist"],
                "S0": S0, "S1": S1})
    out["L2_arestas"] = l2_edges
    out["L2_resumo"] = {
        "n": len(l2_edges),
        "hist_n_dist_perfil": hist([e["n_dist_perfil"] for e in l2_edges]),
        "hist_posicoes_alteradas": hist([e["posicoes_alteradas"]
                                         for e in l2_edges]),
        "graus_regulares": sum(e["graus_regulares"] for e in l2_edges),
        "hist_iso": hist([e["iso_n"] for e in l2_edges]),
        "hist_neq": hist([e["neq"] for e in l2_edges])}

    # tambem: perfis L1 (para contraste)
    l1_ndist = [c["arestas"][nome]["n_dist_perfil0"]
                for c in casos for nome in ("C_AB->B", "C_BA->A")
                if c["arestas"][nome]["nivel"] == "L1"]
    out["L1_hist_n_dist_perfil"] = hist(l1_ndist)

    # (D) fam-20 como referencia (Wtil ja publicados; NAO regenerado)
    f20 = json.load(open(DST + "/prevalencia/condicao-L1-insample.json"))["fam20"]
    ref = {}
    for nome in ("C_AB->B", "C_BA->A"):
        W = [tuple(r) for r in f20[nome]["Wtil_m0"]]
        offd = sorted(W[a][b] for a in range(4) for b in range(a + 1, 4))
        ref[nome] = {"W": [list(r) for r in W], "iso_n": len(grupo_iso(W)),
                     "offdiag": offd, "equidistante": len(set(offd)) == 1,
                     "graus": sorted(degs_de(W))}
    out["fam20_referencia"] = ref
    # padrao emparelhado (iso_n das duas arestas) da fam20 vs os 29 (L1,L1)
    par20 = tuple(sorted([ref["C_AB->B"]["iso_n"], ref["C_BA->A"]["iso_n"]]))
    n_match = sum(1 for c in casos
                  if tuple(c["subtipo"]) == ("L1", "L1") and
                  tuple(sorted([c["arestas"]["C_AB->B"]["iso_n"],
                                c["arestas"]["C_BA->A"]["iso_n"]])) == par20)
    out["fam20_par_iso"] = {"par": list(par20),
                            "n_L1L1_com_mesmo_par": n_match}

    # (E) clustering
    def feats(c, conjunto):
        aB = c["arestas"]["C_AB->B"]; aA = c["arestas"]["C_BA->A"]
        import math
        base = [
            ("nivB", "cat", aB["nivel"]),
            ("nivA", "cat", aA["nivel"]),
            ("log2isoB", "num", math.log2(aB["iso_n"])),
            ("log2isoA", "num", math.log2(aA["iso_n"])),
            ("log2neqB", "num", math.log2(aB["neq"])),
            ("log2neqA", "num", math.log2(aA["neq"])),
            ("equidB", "cat", aB["equidistante"]),
            ("equidA", "cat", aA["equidistante"]),
            ("noffB", "num", aB["n_offdiag_dist"]),
            ("noffA", "num", aA["n_offdiag_dist"]),
            ("ngrB", "num", aB["n_graus_dist"]),
            ("ngrA", "num", aA["n_graus_dist"]),
            ("taucl", "cat", c["tau_classe"]),
            ("lam_alinhado", "cat", c["cell"] in ("T_in", "DT_lam", "FC_lam")),
        ]
        if conjunto == "alargado":
            base += [("orb", "num", c["orbita_len"]),
                     ("depB", "num", aB["dep_sites"]),
                     ("depA", "num", aA["dep_sites"]),
                     ("log2iEq", "num", math.log2(c["iEq"]))]
        if conjunto == "geometria":
            base = [b for b in base if b[0] in
                    ("log2isoB", "log2isoA", "log2neqB", "log2neqA",
                     "equidB", "equidA", "noffB", "noffA", "ngrB", "ngrA")]
        return base

    res_clust = {}
    particoes = {}
    for conjunto in ("nuclear", "alargado", "geometria"):
        F = [feats(c, conjunto) for c in casos]
        nomes = [f[0] for f in F[0]]
        tipos = [f[1] for f in F[0]]
        X = [[f[2] for f in fc] for fc in F]
        D = gower(X, tipos)
        rc = {}
        for linkage in ("average", "complete", "single"):
            merges = hier(D, linkage)
            alturas = [m[0] for m in merges]
            # maior salto RELATIVO nas ultimas fusoes -> k natural
            saltos = []
            for i in range(1, len(alturas)):
                prev = alturas[i - 1]
                saltos.append((alturas[i] - prev, len(casos) - i))
            saltos.sort(reverse=True)
            k_salto = saltos[0][1] if saltos else 1
            sil = {}
            for k in range(2, 9):
                lab = corta(merges, len(casos), k)
                s = silhueta(D, lab)
                sil[k] = round(s, 4)
            k_sil = max(sil, key=sil.get)
            lab_sil = corta(merges, len(casos), k_sil)
            rc[linkage] = {"k_por_salto": k_salto, "silhuetas": sil,
                           "k_por_silhueta": k_sil,
                           "alturas_ultimas8": [round(a, 4)
                                                for a in alturas[-8:]]}
            particoes[(conjunto, linkage)] = lab_sil
        res_clust[conjunto] = {"features": nomes, "linkages": rc}
    out["clustering"] = res_clust

    # robustez: ARI entre linkages e entre conjuntos (no k da silhueta)
    aris = {}
    pares = [(("nuclear", "average"), ("nuclear", "complete")),
             (("nuclear", "average"), ("nuclear", "single")),
             (("nuclear", "average"), ("alargado", "average")),
             (("nuclear", "average"), ("geometria", "average"))]
    for p1, p2 in pares:
        aris["%s/%s vs %s/%s" % (p1 + p2)] = round(
            ari(particoes[p1], particoes[p2]), 4)
    out["robustez_ARI"] = aris

    # particao de referencia: composicao dos clusters (nuclear/average)
    labref = particoes[("nuclear", "average")]
    comp = {}
    for i, c in enumerate(casos):
        cl_ = labref[i]
        comp.setdefault(cl_, {"n": 0, "subtipos": {}, "tau": {},
                              "iso_pares": {}})
        comp[cl_]["n"] += 1
        st = str(tuple(c["subtipo"]))
        comp[cl_]["subtipos"][st] = comp[cl_]["subtipos"].get(st, 0) + 1
        comp[cl_]["tau"][c["tau_classe"]] = \
            comp[cl_]["tau"].get(c["tau_classe"], 0) + 1
        ip = str(tuple(sorted([c["arestas"]["C_AB->B"]["iso_n"],
                               c["arestas"]["C_BA->A"]["iso_n"]])))
        comp[cl_]["iso_pares"][ip] = comp[cl_]["iso_pares"].get(ip, 0) + 1
    out["composicao_clusters_ref"] = {str(k): v
                                      for k, v in sorted(comp.items())}
    out["particao_ref"] = labref
    # cruzamentos da particao de referencia com rotulos mecanicistas
    lab_sub = [str(tuple(c["subtipo"])) for c in casos]
    lab_tau = [c["tau_classe"] for c in casos]
    lab_forced = [str((c["arestas"]["C_AB->B"]["iso_n"] == 24,
                       c["arestas"]["C_BA->A"]["iso_n"] == 24))
                  for c in casos]
    def to_int(ls):
        u = {v: i for i, v in enumerate(sorted(set(ls)))}
        return [u[v] for v in ls]
    out["ARI_ref_vs_subtipo"] = round(ari(labref, to_int(lab_sub)), 4)
    out["ARI_ref_vs_tau_classe"] = round(ari(labref, to_int(lab_tau)), 4)
    out["ARI_ref_vs_forced24"] = round(ari(labref, to_int(lab_forced)), 4)

    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print(json.dumps({k: out[k] for k in
                      ("subtipos_ordenados_(nivB,nivA)", "tau_classe_46",
                       "cell_46", "L1_forced_vs_selected", "L2_resumo",
                       "fam20_par_iso", "robustez_ARI",
                       "ARI_ref_vs_subtipo", "ARI_ref_vs_tau_classe",
                       "ARI_ref_vs_forced24")},
                     sort_keys=True, indent=1))
    print("clusters ref (nuclear/average):",
          json.dumps(out["composicao_clusters_ref"], sort_keys=True))
    print("P(colapso|celula):",
          json.dumps(out["P_colapso_por_celula"], sort_keys=True, indent=1))
    print("sha256 analise:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
