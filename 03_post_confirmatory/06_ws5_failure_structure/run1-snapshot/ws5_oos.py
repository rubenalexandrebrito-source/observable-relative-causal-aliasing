# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY - Pre-registo A v8.3, Fase 6, WS5.
Validacao OOS pre-comprometida (precommit-ws5-oos.txt, registado ANTES):
  (a) OOS elegivel: semente 910000030, N=5000 familias aceites;
  (b) RAW sem elegibilidade: semente 910000031, N=20000 thetas (pi0!=pi1).
Predicoes P1..P7 do precommit avaliadas tal como saem. Nada confirmatorio
e tocado; escreve apenas no ws dir.
"""
import sys, json, time, hashlib, itertools, math
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws5-failure-structure"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

SEED_OOS = 910000030
N_OOS = 5000
SEED_RAW = 910000031
N_RAW = 20000
SAIDA = WS + "/ws5-oos.json"

Q_FIXO = {  # in-sample, ws5-correlacao.json (b24c0979...) - congelado no precommit
    "C3": (0.011011, 0.011591), "DT_lam": (0.088729, 0.076739),
    "DT_oth": (0.079646, 0.073009), "FC_lam": (0.012291, 0.014525),
    "FC_oth": (0.020373, 0.016298), "T_in": (0.091018, 0.070659),
    "T_out": (0.115730, 0.121910)}

ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5], "G0"),
           ("C_BA->A", [8, 9], [0, 1, 2], [2], "F0"))
PERMS = [tuple(p) for p in itertools.permutations(range(4))]
SUBS = [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2),
        (3, 0), (3, 1), (3, 2), (3, 3)]
MATCHINGS = [frozenset([frozenset([0, 1]), frozenset([2, 3])]),
             frozenset([frozenset([0, 2]), frozenset([1, 3])]),
             frozenset([frozenset([0, 3]), frozenset([1, 2])])]
CELL_PSI_FIXA_LAM = ("T_in", "DT_lam", "DT_oth", "FC_lam")


def pc2(v):
    return bin(v).count("1")


def w_base(M):
    return tuple(tuple(sum(pc2(M[r][p] ^ M[r][q]) for r in range(4))
                       for q in range(4)) for p in range(4))


def compoe(a, b):
    return tuple(a[b[c]] for c in range(4))


def inverte(p):
    inv = [0] * 4
    for c, v in enumerate(p):
        inv[v] = c
    return tuple(inv)


def cycle_type(p):
    seen = [False] * 4
    t = []
    for i in range(4):
        if not seen[i]:
            l, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                l += 1
            t.append(l)
    return tuple(sorted(t))


def perm_matching(p, mi):
    return frozenset(frozenset(p[v] for v in bloco) for bloco in MATCHINGS[mi])


def matching_de_dt(t):
    pares = set()
    for a in range(4):
        pares.add(frozenset([a, t[a]]))
    return frozenset(pares)


def celula(tau, lam):
    ct = cycle_type(tau)
    if ct == (1, 1, 2):
        ab = frozenset(a for a in range(4) if tau[a] != a)
        return "T_in" if ab in lam else "T_out"
    if ct == (2, 2):
        return "DT_lam" if matching_de_dt(tau) == lam else "DT_oth"
    if ct == (4,):
        return "FC_lam" if matching_de_dt(compoe(tau, tau)) == lam else "FC_oth"
    return "C3"


def perfil_S(W, p):
    return [sum(W[p[c]][p[(c & ~mc) | vc]] for c in range(4))
            for (mc, vc) in SUBS]


def rank_canonico(vals):
    o = sorted(set(vals))
    idx = {v: i for i, v in enumerate(o)}
    return tuple(idx[v] for v in vals)


def grupo_iso(W):
    return frozenset(p for p in PERMS
                     if all(W[p[a]][p[b]] == W[a][b]
                            for a in range(4) for b in range(4)))


def wtil_tuple(W, p):
    return tuple(W[p[c1]][p[c2]] for c1 in range(4) for c2 in range(4))


def analisa_theta(th):
    """caracteristicas por familia via formula W exacta."""
    pi0 = tuple(th.pi[0]); pi1 = tuple(th.pi[1])
    tau = compoe(pi1, inverte(pi0))
    lam = perm_matching(pi0, 2)
    cell = celula(tau, lam)
    rec = {"cell": cell}
    eqs, isos = {}, {}
    for nome, ba, bb, mem, tn in ARESTAS:
        M = th.G0 if tn == "G0" else th.F0
        W = w_base(M)
        r0 = rank_canonico(perfil_S(W, pi0))
        r1 = rank_canonico(perfil_S(W, pi1))
        if wtil_tuple(W, pi0) == wtil_tuple(W, pi1):
            nv = "L1"
        elif r0 == r1:
            nv = "L2"
        else:
            nv = "L3"
        iso = grupo_iso(W)
        eqc = frozenset(p for p in PERMS
                        if rank_canonico(perfil_S(W, p)) == r0)
        lado = "B" if tn == "G0" else "A"
        rec["niv" + lado] = nv
        eqs[lado] = eqc
        isos[lado] = iso
    rec["iEq"] = len(eqs["B"] & eqs["A"])
    rec["iIso"] = len(isos["B"] & isos["A"])
    return rec


def fibra_maquinaria(T, n, ints, bits_b, mem):
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    Z0 = cl.estados_da_fibra(n, mem, 0)
    Z1 = cl.estados_da_fibra(n, mem, 1)
    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    d0, d1 = [], []
    for (mk, vl) in ints:
        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
        d0.append(int(popB[x0].sum()))
        d1.append(int(popB[x1].sum()))
    return d0, d1


def auditoria_maquinaria(th, rec):
    tab, n, lay = g.tabela_transicao("II", th, False)
    T = np.asarray(tab, dtype=np.int64)
    pi0, pi1 = tuple(th.pi[0]), tuple(th.pi[1])
    ok = True
    for nome, ba, bb, mem, tn in ARESTAS:
        ints = cl.intervencoes(ba)
        d0, d1 = fibra_maquinaria(T, n, ints, bb, mem)
        M = th.G0 if tn == "G0" else th.F0
        W = w_base(M)
        if d0 != [32 * s for s in perfil_S(W, pi0)]:
            ok = False
        if d1 != [32 * s for s in perfil_S(W, pi1)]:
            ok = False
        nv = ("L1" if d0 == d1 else
              "L2" if rank_canonico(d0) == rank_canonico(d1) else "L3")
        lado = "B" if tn == "G0" else "A"
        if nv != rec["niv" + lado]:
            ok = False
    return ok


def fisher_2x2(a, b, c, d):
    n = a + b + c + d
    r1, c1 = a + b, a + c
    lo = max(0, r1 + c1 - n)
    hi = min(r1, c1)
    def pmf(x):
        return (math.comb(c1, x) * math.comb(n - c1, r1 - x)
                / math.comb(n, r1))
    pobs = pmf(a)
    return sum(pmf(x) for x in range(lo, hi + 1) if pmf(x) <= pobs * (1 + 1e-12))


def tabelas(regs):
    porc = {}
    for f in regs:
        r = porc.setdefault(f["cell"], {"n": 0, "estB": 0, "estA": 0,
                                        "l1B": 0, "l1A": 0, "l2B": 0,
                                        "l2A": 0, "ambos_est": 0,
                                        "ambos_l1": 0})
        r["n"] += 1
        eB = f["nivB"] != "L3"; eA = f["nivA"] != "L3"
        r["estB"] += eB; r["estA"] += eA
        r["l1B"] += f["nivB"] == "L1"; r["l1A"] += f["nivA"] == "L1"
        r["l2B"] += f["nivB"] == "L2"; r["l2A"] += f["nivA"] == "L2"
        r["ambos_est"] += eB and eA
        r["ambos_l1"] += (f["nivB"] == "L1") and (f["nivA"] == "L1")
    return {k: porc[k] for k in sorted(porc)}


def main():
    t0 = time.time()
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY", "ws": "ws5",
           "resultado_confirmatorio": "negativo (imutavel)",
           "precommit": "precommit-ws5-oos.txt (registado antes desta execucao)"}

    # ------------------------- (a) OOS elegivel -------------------------
    ss = np.random.SeedSequence(SEED_OOS)
    rng = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))
    regs = []
    tent = 0
    audit_ok = audit_falha = 0
    colapsos = []
    while len(regs) < N_OOS and tent < 200000:
        tent += 1
        th = g.sample_theta_base(rng)
        if th.pi[0] == th.pi[1]:
            continue
        ok, _, _ = g.elegibilidade(th, False)
        if not ok:
            continue
        rec = analisa_theta(th)
        idx = len(regs)
        eh_colapso = rec["nivB"] != "L3" and rec["nivA"] != "L3"
        if eh_colapso:
            colapsos.append({"idx": idx, "tentativa": tent,
                             "cell": rec["cell"],
                             "subtipo": (rec["nivB"], rec["nivA"])})
        if eh_colapso or idx % 500 == 0:
            if auditoria_maquinaria(th, rec):
                audit_ok += 1
            else:
                audit_falha += 1
        regs.append(rec)
    tab = tabelas(regs)
    out["oos"] = {"semente": SEED_OOS, "N": len(regs), "tentativas": tent,
                  "auditoria_maquinaria": {"ok": audit_ok,
                                           "falha": audit_falha},
                  "tabela_por_celula": tab,
                  "colapsos": colapsos, "n_colapsos": len(colapsos)}

    # P1: zero L2 nas celulas psi-fixa-lam
    p1 = {c: {"l2B": tab.get(c, {}).get("l2B", 0),
              "l2A": tab.get(c, {}).get("l2A", 0)}
          for c in CELL_PSI_FIXA_LAM}
    out["P1_zero_L2_celulas_alinhadas"] = {
        "contagens": p1,
        "cumprido": all(v["l2B"] == 0 and v["l2A"] == 0 for v in p1.values())}

    # P2: taxas de estado por celula vs q fixos
    p2 = {}
    somaB = somaA = varB = varA = 0.0
    kB = kA = 0
    for c, r in tab.items():
        qB, qA = Q_FIXO[c]
        eB = r["n"] * qB; eA = r["n"] * qA
        vB = r["n"] * qB * (1 - qB); vA = r["n"] * qA * (1 - qA)
        p2[c] = {"n": r["n"], "estB": r["estB"], "espB": round(eB, 2),
                 "zB": round((r["estB"] - eB) / math.sqrt(vB), 3),
                 "estA": r["estA"], "espA": round(eA, 2),
                 "zA": round((r["estA"] - eA) / math.sqrt(vA), 3)}
        somaB += eB; somaA += eA; varB += vB; varA += vA
        kB += r["estB"]; kA += r["estA"]
    out["P2_taxas_por_celula"] = p2
    out["P2_global"] = {"zB": round((kB - somaB) / math.sqrt(varB), 3),
                        "zA": round((kA - somaA) / math.sqrt(varA), 3)}

    # P3/P4: colapso duplo vs M2(q fixos) e M3; both-L1 vs M3'
    m2 = sum(r["n"] * Q_FIXO[c][0] * Q_FIXO[c][1] for c, r in tab.items())
    m3 = sum((f["iEq"] - 1) / 23.0 for f in regs)
    v3 = sum(((f["iEq"] - 1) / 23.0) * (1 - (f["iEq"] - 1) / 23.0)
             for f in regs)
    obs_both = sum(1 for f in regs if f["nivB"] != "L3" and f["nivA"] != "L3")
    m3l = sum((f["iIso"] - 1) / 23.0 for f in regs)
    v3l = sum(((f["iIso"] - 1) / 23.0) * (1 - (f["iIso"] - 1) / 23.0)
              for f in regs)
    obs_l1 = sum(1 for f in regs if f["nivB"] == "L1" and f["nivA"] == "L1")
    nBt = sum(1 for f in regs if f["nivB"] != "L3")
    nAt = sum(1 for f in regs if f["nivA"] != "L3")
    m0 = nBt * nAt / len(regs)
    out["P3_colapso_duplo"] = {
        "obs": obs_both, "M0_indep": round(m0, 3),
        "M2_q_fixos": round(m2, 3),
        "z_vs_M2": round((obs_both - m2) / math.sqrt(m2), 3),
        "M3_geometria": round(m3, 3), "sd_M3": round(math.sqrt(v3), 3),
        "z_vs_M3": round((obs_both - m3) / math.sqrt(v3), 3),
        "razao_obs_M0": round(obs_both / m0, 3) if m0 else None}
    m0l = (sum(1 for f in regs if f["nivB"] == "L1")
           * sum(1 for f in regs if f["nivA"] == "L1") / len(regs))
    out["P4_bothL1"] = {
        "obs": obs_l1, "M0_indep": round(m0l, 3),
        "M3l_geometria": round(m3l, 3), "sd": round(math.sqrt(v3l), 3),
        "z_vs_M3l": round((obs_l1 - m3l) / math.sqrt(v3l), 3),
        "razao_obs_M0": round(obs_l1 / m0l, 3) if m0l else None}

    # P5: DT_lam vs DT_oth (estado)
    dl, do = tab.get("DT_lam"), tab.get("DT_oth")
    out["P5_DT_iguais"] = {
        "estB": {"lam": [dl["estB"], dl["n"]], "oth": [do["estB"], do["n"]],
                 "p_fisher": round(fisher_2x2(dl["estB"], dl["n"] - dl["estB"],
                                              do["estB"], do["n"] - do["estB"]), 5)},
        "estA": {"lam": [dl["estA"], dl["n"]], "oth": [do["estA"], do["n"]],
                 "p_fisher": round(fisher_2x2(dl["estA"], dl["n"] - dl["estA"],
                                              do["estA"], do["n"] - do["estA"]), 5)}}

    # P6: taxas L2 por celula
    out["P6_taxas_L2"] = {c: {"l2B": r["l2B"], "l2A": r["l2A"], "n": r["n"],
                              "taxaB": round(r["l2B"] / r["n"], 5),
                              "taxaA": round(r["l2A"] / r["n"], 5)}
                          for c, r in tab.items()}

    print("OOS elegivel concluido: %d familias, %d tentativas, %.1fs"
          % (len(regs), tent, time.time() - t0), flush=True)

    # ------------------------- (b) RAW sem elegibilidade -----------------
    t1 = time.time()
    ssr = np.random.SeedSequence(SEED_RAW)
    rngr = np.random.Generator(np.random.PCG64(ssr.spawn(4)[0]))
    regs_raw = []
    while len(regs_raw) < N_RAW:
        th = g.sample_theta_base(rngr)
        if th.pi[0] == th.pi[1]:
            continue
        regs_raw.append(analisa_theta(th))
    tabr = tabelas(regs_raw)
    out["raw"] = {"semente": SEED_RAW, "N": len(regs_raw),
                  "tabela_por_celula": tabr}
    # P7: no RAW, class-model e geometria exacta devem coincidir
    CLASSE = {"T_in": "T", "T_out": "T", "DT_lam": "DT", "DT_oth": "DT",
              "FC_lam": "FC", "FC_oth": "FC", "C3": "C3"}
    porcl = {}
    for f in regs_raw:
        cl_ = CLASSE[f["cell"]]
        r = porcl.setdefault(cl_, [0, 0, 0, 0, 0])
        r[0] += 1
        r[1] += f["nivB"] == "L1"; r[2] += f["nivA"] == "L1"
        r[3] += (f["nivB"] == "L1") and (f["nivA"] == "L1")
        r[4] += (f["nivB"] != "L3") and (f["nivA"] != "L3")
    m1_raw = sum(r[1] * r[2] / r[0] for r in porcl.values())
    m3l_raw = sum((f["iIso"] - 1) / 23.0 for f in regs_raw)
    v3l_raw = sum(((f["iIso"] - 1) / 23.0) * (1 - (f["iIso"] - 1) / 23.0)
                  for f in regs_raw)
    obs_l1_raw = sum(r[3] for r in porcl.values())
    m3_raw = sum((f["iEq"] - 1) / 23.0 for f in regs_raw)
    obs_both_raw = sum(r[4] for r in porcl.values())
    m2_raw_cell = 0.0
    for c, r in tabr.items():
        m2_raw_cell += r["estB"] * r["estA"] / r["n"]
    out["P7_raw_controlo"] = {
        "obs_bothL1_raw": obs_l1_raw,
        "M1_classe_raw": round(m1_raw, 3),
        "M3l_geom_raw": round(m3l_raw, 3),
        "sd_M3l_raw": round(math.sqrt(v3l_raw), 3),
        "diff_M3l_M1_raw": round(m3l_raw - m1_raw, 3),
        "obs_both_est_raw": obs_both_raw,
        "M2_celula_raw_insample_dela_propria": round(m2_raw_cell, 3),
        "M3_geom_raw": round(m3_raw, 3),
        "z_obsL1_vs_M3l_raw": round((obs_l1_raw - m3l_raw)
                                    / math.sqrt(v3l_raw), 3)}
    # taxas raw vs elegivel por celula (efeito da elegibilidade nos q)
    cmpq = {}
    for c in sorted(tabr):
        rr, re = tabr[c], tab.get(c)
        cmpq[c] = {"raw_qB": round(rr["estB"] / rr["n"], 5),
                   "raw_qA": round(rr["estA"] / rr["n"], 5),
                   "oos_qB": round(re["estB"] / re["n"], 5) if re else None,
                   "oos_qA": round(re["estA"] / re["n"], 5) if re else None,
                   "raw_l2B": round(rr["l2B"] / rr["n"], 5),
                   "raw_l2A": round(rr["l2A"] / rr["n"], 5)}
    out["q_raw_vs_oos"] = cmpq
    out["duracao_s"] = {"oos": round(t1 - t0, 1),
                        "raw": round(time.time() - t1, 1)}

    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print(json.dumps(out, sort_keys=True, indent=1))
    print("sha256 oos:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
