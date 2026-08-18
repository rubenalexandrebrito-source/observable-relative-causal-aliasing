# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY - Pre-registo A v8.3, Fase 6, WS5.
AUDITORIA DE SEGUNDA PASSAGEM (agente WS5, implementacao independente).
Verifica, sem reutilizar o codigo dos scripts ws5_* (apenas o instrumento
congelado em frozen-copy), as alegacoes centrais dos artefactos WS5:
  A0  ordem congelada das 9 intervencoes -> substituicoes de canal
  A1  teorema do alinhamento: enumeracao psi(tau) fixa lam <=> celula alinhada
  A2  lema de necessidade: rank 6 do sistema 9x6 (eliminacao exacta em Q)
  A3  replay independente dos lotes 910000001/2: reproducao campo-a-campo
      das 10000 linhas de ws5-familias-N10000.json
  A4  via da MAQUINARIA congelada (tabela de transicao + fibra cl.*) para
      TODOS os 46 casos + controlo deterministico (fam_global % 67 == 0):
      d0/d1/dep/nivel/orbita/theta_sha vs ws5-casos46.json
  A5  agregados F5/F6/F7 recalculados dos meus proprios registos e
      comparados com ws5-correlacao.json / relatorio
  A6  estatisticas dos 46 (orbitas, dep, sigma, assinatura L2 = par P)
  A7  dep_sites==0 na populacao (prevalencia JSONs, leitura apenas)
Nao usa sementes novas (replay de lotes registados apenas). Escreve apenas
ws5-audit-agent2.json no ws dir.
"""
import sys, json, time, hashlib, itertools, math
from dataclasses import asdict
from fractions import Fraction
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws5-failure-structure"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

PERMS = [tuple(p) for p in itertools.permutations(range(4))]
IDP = (0, 1, 2, 3)
SUBS_ESPERADAS = [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2),
                  (3, 0), (3, 1), (3, 2), (3, 3)]
MATCH = [frozenset([frozenset([0, 1]), frozenset([2, 3])]),
         frozenset([frozenset([0, 2]), frozenset([1, 3])]),
         frozenset([frozenset([0, 3]), frozenset([1, 2])])]
ALINHADAS = ("T_in", "DT_lam", "DT_oth", "FC_lam")

res = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
       "resultado_confirmatorio": "negativo (imutavel)",
       "ws": "ws5 (auditoria segunda passagem)"}
fails = []


def chk(nome, ok, detalhe=None):
    res.setdefault("checks", {})[nome] = {"ok": bool(ok)}
    if detalhe is not None:
        res["checks"][nome]["detalhe"] = detalhe
    if not ok:
        fails.append(nome)


# ---------- utilidades independentes (implementadas de fresco) ----------
def pc2(v):
    return bin(v).count("1")


def wmat(M):
    return tuple(tuple(sum(pc2(M[r][p] ^ M[r][q]) for r in range(4))
                       for q in range(4)) for p in range(4))


def comp(a, b):
    return tuple(a[b[i]] for i in range(4))


def inv(p):
    q = [0] * 4
    for i, v in enumerate(p):
        q[v] = i
    return tuple(q)


def ctype(p):
    vis, t = [False] * 4, []
    for i in range(4):
        if not vis[i]:
            l, j = 0, i
            while not vis[j]:
                vis[j] = True
                j = p[j]
                l += 1
            t.append(l)
    return tuple(sorted(t))


def img_match(p, m):
    return frozenset(frozenset(p[v] for v in par) for par in m)


def match_dt(t):
    return frozenset(frozenset([a, t[a]]) for a in range(4))


def celula(tau, lam):
    ct = ctype(tau)
    if ct == (1, 1, 2):
        ab = frozenset(a for a in range(4) if tau[a] != a)
        return "T_in" if ab in lam else "T_out"
    if ct == (2, 2):
        return "DT_lam" if match_dt(tau) == lam else "DT_oth"
    if ct == (4,):
        return "FC_lam" if match_dt(comp(tau, tau)) == lam else "FC_oth"
    return "C3"


def perfil(W, p, subs):
    return [sum(W[p[c]][p[(c & ~mc) | vc]] for c in range(4))
            for (mc, vc) in subs]


def iso_grp(W):
    return frozenset(p for p in PERMS
                     if all(W[p[a]][p[b]] == W[a][b]
                            for a in range(4) for b in range(4)))


def sha_th(th):
    return hashlib.sha256(
        json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()


def main():
    t0 = time.time()

    # ---------------- A0: intervencoes congeladas ----------------
    subs = []
    for (mk, vl) in cl.intervencoes([6, 7]):
        subs.append((((mk >> 6) & 1) | (((mk >> 7) & 1) << 1),
                     ((vl >> 6) & 1) | (((vl >> 7) & 1) << 1)))
    chk("A0_subs_ordem_congelada", subs == SUBS_ESPERADAS, subs)
    subs2 = []
    for (mk, vl) in cl.intervencoes([8, 9]):
        subs2.append((((mk >> 8) & 1) | (((mk >> 9) & 1) << 1),
                      ((vl >> 8) & 1) | (((vl >> 9) & 1) << 1)))
    chk("A0_subs_iguais_nas_duas_arestas", subs2 == subs)
    SUBS = subs
    # estrutura [0,P1,P1,P2,P2,D0..D3] e emparelhacao cega = MATCH[2]:
    pares_por_int = []
    for (mc, vc) in SUBS:
        pares = frozenset(frozenset([c, (c & ~mc) | vc])
                          for c in range(4) if c != (c & ~mc) | vc)
        pares_por_int.append(pares)
    ok_estr = (pares_por_int[0] == frozenset()
               and pares_por_int[1] == pares_por_int[2] == MATCH[0]
               and pares_por_int[3] == pares_por_int[4] == MATCH[1]
               and all(len(pares_por_int[k]) == 3 for k in (5, 6, 7, 8)))
    chk("A0_estrutura_P1P1P2P2_D_e_M2_cega", ok_estr)

    # ---------------- A1: teorema do alinhamento (enumeracao) -------------
    ok_a1 = True
    for tau in PERMS:
        if tau == IDP:
            continue
        for lam in MATCH:
            alin = (img_match(tau, lam) == lam)
            cel = celula(tau, lam)
            if alin != (cel in ALINHADAS):
                ok_a1 = False
    chk("A1_alinhado_sse_celula_alinhada_(69_combos)", ok_a1)
    # e: em celula alinhada, para TODA W (aqui: 200 M aleatorias fixas por
    # enumeracao de tau), estado => L1 (verificacao da consequencia
    # posicional): S1 e permutacao posicional de S0
    # semente do intervalo WS5 (910000033), precommit-ws5-audit.txt; NAO e
    # amostra estatistica: busca deterministica de contraexemplo do teorema
    rng_chk = np.random.Generator(np.random.PCG64(910000033))
    ok_pos = True
    for _ in range(200):
        M = [[int(rng_chk.integers(4)) for _ in range(2)] for __ in range(4)]
        M = [[M[r][0], M[r][1], int(rng_chk.integers(4)),
              int(rng_chk.integers(4))] for r in range(4)]
        W = wmat(M)
        pi0 = PERMS[int(rng_chk.integers(24))]
        lam = img_match(pi0, MATCH[2])
        for tau in PERMS:
            if tau == IDP or img_match(tau, lam) != lam:
                continue
            pi1 = comp(tau, pi0)
            S0 = perfil(W, pi0, SUBS)
            S1 = perfil(W, pi1, SUBS)
            if sorted(S0) != sorted(S1):
                ok_pos = False
            if cl.rank_canonico(S0) == cl.rank_canonico(S1) and S0 != S1:
                ok_pos = False   # L2 em celula alinhada: proibido
    chk("A1_alinhado_multiconjunto_igual_e_sem_L2_(200_W_x_tau)", ok_pos)

    # ---------------- A2: lema de necessidade ----------------
    PARES = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    A = []
    for (mc, vc) in SUBS:
        row = [0] * 6
        for c in range(4):
            t = (c & ~mc) | vc
            if t != c:
                row[PARES.index((min(c, t), max(c, t)))] += 1
        A.append([Fraction(x) for x in row])
    Mx = [r[:] for r in A]
    rank, ri = 0, 0
    for col in range(6):
        piv = next((r for r in range(ri, 9) if Mx[r][col] != 0), None)
        if piv is None:
            continue
        Mx[ri], Mx[piv] = Mx[piv], Mx[ri]
        pv = Mx[ri][col]
        Mx[ri] = [x / pv for x in Mx[ri]]
        for r in range(9):
            if r != ri and Mx[r][col] != 0:
                f = Mx[r][col]
                Mx[r] = [x - f * y for x, y in zip(Mx[r], Mx[ri])]
        ri += 1
        rank += 1
    chk("A2_lema_necessidade_rank6", rank == 6, rank)

    # ---------------- A3+A4: replay independente ----------------
    fams_stored = json.load(open(WS + "/ws5-familias-N10000.json"))["familias"]
    casos_stored = {(c["seed"], c["tentativa"]): c
                    for c in json.load(open(WS + "/ws5-casos46.json"))["casos"]}
    fs_idx = {(f["seed"], f["tentativa"]): f for f in fams_stored}
    chk("A3_familias_stored_n", len(fams_stored) == 10000, len(fams_stored))
    chk("A4_casos_stored_n", len(casos_stored) == 46, len(casos_stored))

    mism_rows = 0
    maq_ok = maq_bad = 0
    caso_ok = caso_bad = 0
    cnt_niv = {"B": {"L1": 0, "L2": 0, "L3": 0},
               "A": {"L1": 0, "L2": 0, "L3": 0}}
    cnt_cell = {}
    iso_hist = {"B": {}, "A": {}}
    sym_fail = {"B": 0, "A": 0}
    forced24 = {"B": 0, "A": 0}
    forced24_L1 = {"B": 0, "A": 0}
    l2_por_cell = {"B": {}, "A": {}}
    soma_tilt = {"isoB": 0.0, "isoA": 0.0, "neqB": 0.0, "neqA": 0.0}
    meus_fams = []
    orb46, dep46B, dep46A, sigA46 = [], [], [], set()
    l2_sigs = []           # (cell, lado, difs, eh_colapso, valor_novo_e_S_lam)
    dep0_casos = []
    fam_global = 0

    for seed in (910000001, 910000002):
        rng = np.random.Generator(np.random.PCG64(
            np.random.SeedSequence(seed).spawn(4)[0]))
        ac, tent = 0, 0
        while ac < 5000 and tent < 200000:
            tent += 1
            th = g.sample_theta_base(rng)
            if th.pi[0] == th.pi[1]:
                continue
            if not g.elegibilidade(th, False)[0]:
                continue
            ac += 1
            pi0, pi1 = tuple(th.pi[0]), tuple(th.pi[1])
            tau = comp(pi1, inv(pi0))
            lam = img_match(pi0, MATCH[2])
            cel = celula(tau, lam)
            row = {"seed": seed, "fam": ac - 1, "tentativa": tent,
                   "sha16": sha_th(th)[:16], "tau_classe": str(ctype(tau)),
                   "cell": cel}
            eqs, isos, nivs, Ws = {}, {}, {}, {}
            for lado, Mth in (("B", th.G0), ("A", th.F0)):
                W = wmat(Mth)
                Ws[lado] = W
                S0 = perfil(W, pi0, SUBS)
                S1 = perfil(W, pi1, SUBS)
                r0 = cl.rank_canonico(S0)
                wt0 = tuple(W[pi0[a]][pi0[b]] for a in range(4) for b in range(4))
                wt1 = tuple(W[pi1[a]][pi1[b]] for a in range(4) for b in range(4))
                nv = ("L1" if wt0 == wt1 else
                      "L2" if r0 == cl.rank_canonico(S1) else "L3")
                iso = iso_grp(W)
                eqc = frozenset(p for p in PERMS
                                if cl.rank_canonico(perfil(W, p, SUBS)) == r0)
                nivs[lado] = nv
                isos[lado] = iso
                eqs[lado] = eqc
                cnt_niv[lado][nv] += 1
                iso_hist[lado][len(iso)] = iso_hist[lado].get(len(iso), 0) + 1
                if len(iso) > 1 and nv != "L1":
                    sym_fail[lado] += 1
                if len(iso) == 24:
                    forced24[lado] += 1
                    if nv == "L1":
                        forced24_L1[lado] += 1
                if nv == "L2":
                    l2_por_cell[lado][cel] = l2_por_cell[lado].get(cel, 0) + 1
                    # assinatura L2: posicoes alteradas do perfil
                    difs = tuple(i for i in range(9) if S0[i] != S1[i])
                    s_lam = sum(W[min(p)][max(p)] for p in
                                (tuple(sorted(pp)) for pp in lam))
                    if difs in ((1, 2), (3, 4)):
                        val_ok = (S1[difs[0]] == s_lam)
                    elif difs == (1, 2, 3, 4):
                        val_ok = (s_lam in (S1[1], S1[3]))
                    else:
                        val_ok = None
                    l2_sigs.append((cel, lado, difs, None, val_ok))
                soma_tilt["iso" + lado] += (len(iso) - 1) / 23.0
                soma_tilt["neq" + lado] += (len(eqc) - 1) / 23.0
            row.update({"nivB": nivs["B"], "nivA": nivs["A"],
                        "isoB": len(isos["B"]), "isoA": len(isos["A"]),
                        "neqB": len(eqs["B"]), "neqA": len(eqs["A"]),
                        "iEq": len(eqs["B"] & eqs["A"]),
                        "iIso": len(isos["B"] & isos["A"])})
            meus_fams.append(row)
            cnt_cell[cel] = cnt_cell.get(cel, 0) + 1
            if fs_idx.get((seed, tent)) != row:
                mism_rows += 1

            colapso = nivs["B"] != "L3" and nivs["A"] != "L3"
            if colapso:
                # marca as assinaturas L2 desta familia como de colapso
                nl2 = (nivs["B"] == "L2") + (nivs["A"] == "L2")
                for k in range(len(l2_sigs) - nl2, len(l2_sigs)):
                    l2_sigs[k] = l2_sigs[k][:3] + (True,) + l2_sigs[k][4:]
            if colapso or fam_global % 67 == 0:
                # ---- via da maquinaria congelada, do zero ----
                tab, n, lay = g.tabela_transicao("II", th, False)
                T = np.asarray(tab, dtype=np.int64)
                mq = {}
                for nome, ba, bb, mem, lado in (("C_AB->B", [6, 7], [3, 4, 5], [5], "B"),
                                                 ("C_BA->A", [8, 9], [0, 1, 2], [2], "A")):
                    eB = cl.extractor(bb, n)
                    popB = cl.popcount_tab(len(bb))
                    Z0 = cl.estados_da_fibra(n, mem, 0)
                    Z1 = cl.estados_da_fibra(n, mem, 1)
                    nx0, nx1 = eB[T[Z0]], eB[T[Z1]]
                    d0, d1, dep = [], [], 0
                    for (mk, vl) in cl.intervencoes(ba):
                        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
                        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
                        d0.append(int(popB[x0].sum()))
                        d1.append(int(popB[x1].sum()))
                        dep += int((x0 != x1).sum())
                    nv_m = ("L1" if d0 == d1 else
                            "L2" if cl.rank_canonico(d0) == cl.rank_canonico(d1)
                            else "L3")
                    W = Ws[lado]
                    okf = (d0 == [32 * s for s in perfil(W, pi0, SUBS)] and
                           d1 == [32 * s for s in perfil(W, pi1, SUBS)] and
                           nv_m == nivs[lado])
                    mq[nome] = {"d0": d0, "d1": d1, "dep": dep, "ok": okf,
                                "lado": lado}
                if all(v["ok"] for v in mq.values()):
                    maq_ok += 1
                else:
                    maq_bad += 1
                if colapso:
                    s0i = g._campos_para_int(g.estado_inicial("II", th), lay)
                    orb = cl.orbita(T, s0i)
                    cs = casos_stored.get((seed, tent))
                    okc = cs is not None
                    if okc:
                        okc = (cs["theta_sha"] == sha_th(th)
                               and tuple(cs["pi0"]) == pi0
                               and tuple(cs["pi1"]) == pi1
                               and tuple(cs["tau"]) == tau
                               and cs["cell"] == cel
                               and tuple(cs["subtipo"]) == (nivs["B"], nivs["A"])
                               and cs["orbita_len"] == len(orb))
                        for nome in ("C_AB->B", "C_BA->A"):
                            ca = cs["arestas"][nome]
                            okc = okc and (ca["d0"] == mq[nome]["d0"]
                                           and ca["d1"] == mq[nome]["d1"]
                                           and ca["dep_sites"] == mq[nome]["dep"]
                                           and ca["nivel"] == nivs[mq[nome]["lado"]]
                                           and [list(r) for r in Ws[mq[nome]["lado"]]] == ca["W"]
                                           and ca["iso_n"] == len(isos[mq[nome]["lado"]])
                                           and ca["neq"] == len(eqs[mq[nome]["lado"]]))
                    if okc:
                        caso_ok += 1
                    else:
                        caso_bad += 1
                    orb46.append(len(orb))
                    dep46B.append(mq["C_AB->B"]["dep"])
                    dep46A.append(mq["C_BA->A"]["dep"])
                    sigA46.add(tuple(th.sigmaA))
                    if mq["C_AB->B"]["dep"] == 0 or mq["C_BA->A"]["dep"] == 0:
                        dep0_casos.append((seed, tent, cel,
                                           "B" if mq["C_AB->B"]["dep"] == 0 else "A"))
            fam_global += 1

    chk("A3_linhas_familias_identicas_10000", mism_rows == 0, mism_rows)
    chk("A4_maquinaria_ok", maq_bad == 0,
        {"ok": maq_ok, "falha": maq_bad})
    chk("A4_casos46_identicos", caso_ok == 46 and caso_bad == 0,
        {"ok": caso_ok, "falha": caso_bad})

    # A6/A6b: assinaturas L2 - (i) nos 24 colapsos: sempre UM par P;
    # (ii) populacao 225: distribuicao por celula; (iii) valor novo = S(lam)
    col24 = [s for s in l2_sigs if s[3]]
    chk("A6_L2_24colapsos_assinatura_um_par_P",
        len(col24) == 24 and all(s[2] in ((1, 2), (3, 4)) for s in col24),
        {"n": len(col24)})
    pop_sig = {}
    for cel, lado, difs, _, _ in l2_sigs:
        k = (cel, str(difs))
        pop_sig[k] = pop_sig.get(k, 0) + 1
    res["A6b_populacao_L2_assinaturas"] = {
        "%s|%s" % k: v for k, v in sorted(pop_sig.items())}
    ok_teoria = all(
        (cel in ("T_out", "FC_oth") and difs in ((1, 2), (3, 4)))
        or (cel == "C3" and difs in ((1, 2), (3, 4), (1, 2, 3, 4)))
        for cel, lado, difs, _, _ in l2_sigs)
    chk("A6b_L2_225_assinaturas_por_celula_teoria",
        ok_teoria and len(l2_sigs) == 225,
        {"n": len(l2_sigs)})
    chk("A6b_L2_valor_novo_eh_soma_lam_(T_out,FC_oth)",
        all(v for cel, _, _, _, v in l2_sigs
            if cel in ("T_out", "FC_oth")))
    chk("A6b_L2_bloco_D_nunca_alterado",
        all(all(i < 5 for i in difs) for _, _, difs, _, _ in l2_sigs))

    # niveis totais (compara com combinada N10000: L1 705, L2 225, L3 19070)
    tot = {k: sum(cnt_niv[l][k] for l in ("B", "A")) for k in ("L1", "L2", "L3")}
    chk("A5_totais_niveis_705_225_19070",
        tot == {"L1": 705, "L2": 225, "L3": 19070}, tot)
    chk("A5_niveis_por_lado",
        cnt_niv == {"B": {"L1": 370, "L2": 105, "L3": 9525},
                    "A": {"L1": 335, "L2": 120, "L3": 9545}}, cnt_niv)

    # F5: histogramas e contagens
    res["F5_iso_hist_B"] = dict(sorted(iso_hist["B"].items()))
    res["F5_iso_hist_A"] = dict(sorted(iso_hist["A"].items()))
    res["F5_sym_mas_falhou"] = sym_fail
    res["F5_forced24"] = {"iso24": forced24, "iso24_e_L1": forced24_L1}
    chk("F5_iso24_sempre_L1",
        forced24 == forced24_L1,
        {"forced": forced24, "forced_L1": forced24_L1})
    chk("F5_sym_fail_4620_4619",
        sym_fail == {"B": 4620, "A": 4619}, sym_fail)
    chk("F5_forced_total_60_de_705",
        forced24["B"] + forced24["A"] == 60, forced24)
    chk("F5_iso_hist_B_relatorio",
        iso_hist["B"] == {1: 5010, 2: 4102, 4: 534, 6: 169, 8: 157, 24: 28},
        iso_hist["B"])

    # tilt (F5): somas vs observados
    tilt_cmp = {
        "L1_B": (round(soma_tilt["isoB"], 1), cnt_niv["B"]["L1"]),
        "L1_A": (round(soma_tilt["isoA"], 1), cnt_niv["A"]["L1"]),
        "est_B": (round(soma_tilt["neqB"], 1),
                  cnt_niv["B"]["L1"] + cnt_niv["B"]["L2"]),
        "est_A": (round(soma_tilt["neqA"], 1),
                  cnt_niv["A"]["L1"] + cnt_niv["A"]["L2"])}
    res["F5_tilt"] = tilt_cmp
    chk("F5_tilt_valores_relatorio",
        tilt_cmp["L1_B"][0] == 360.5 and tilt_cmp["est_B"][0] == 467.9
        and tilt_cmp["L1_A"][0] == 362.7 and tilt_cmp["est_A"][0] == 462.8,
        tilt_cmp)

    # F6: escada recalculada
    N = len(meus_fams)
    CLS = {"T_in": "T", "T_out": "T", "DT_lam": "DT", "DT_oth": "DT",
           "FC_lam": "FC", "FC_oth": "FC", "C3": "C3"}
    def escada(fn_b, fn_a):
        nB = sum(1 for f in meus_fams if fn_b(f))
        nA = sum(1 for f in meus_fams if fn_a(f))
        obs = sum(1 for f in meus_fams if fn_b(f) and fn_a(f))
        m0 = nB * nA / N
        por, porc = {}, {}
        for f in meus_fams:
            for key, d in ((CLS[f["cell"]], por), (f["cell"], porc)):
                r = d.setdefault(key, [0, 0, 0])
                r[0] += 1
                r[1] += fn_b(f)
                r[2] += fn_a(f)
        m1 = sum(r[1] * r[2] / r[0] for r in por.values())
        m2 = sum(r[1] * r[2] / r[0] for r in porc.values())
        return obs, m0, m1, m2
    obs_e, m0_e, m1_e, m2_e = escada(lambda f: f["nivB"] != "L3",
                                     lambda f: f["nivA"] != "L3")
    obs_l, m0_l, m1_l, m2_l = escada(lambda f: f["nivB"] == "L1",
                                     lambda f: f["nivA"] == "L1")
    m3_e = sum((f["iEq"] - 1) / 23.0 for f in meus_fams)
    v3_e = sum(((f["iEq"] - 1) / 23.0) * (1 - (f["iEq"] - 1) / 23.0)
               for f in meus_fams)
    m3_l = sum((f["iIso"] - 1) / 23.0 for f in meus_fams)
    esc = {"estado": {"obs": obs_e, "M0": round(m0_e, 2), "M1": round(m1_e, 2),
                      "M2": round(m2_e, 2), "M3": round(m3_e, 2),
                      "sd_M3": round(math.sqrt(v3_e), 2)},
           "bothL1": {"obs": obs_l, "M0": round(m0_l, 2), "M1": round(m1_l, 2),
                      "M2": round(m2_l, 2), "M3l": round(m3_l, 2)}}
    res["F6_escada"] = esc
    chk("F6_escada_relatorio",
        esc["estado"]["obs"] == 46 and abs(m0_e - 21.61) < 0.01
        and abs(m1_e - 39.01) < 0.01 and abs(m2_e - 39.75) < 0.01
        and abs(m3_e - 44.00) < 0.01 and esc["bothL1"]["obs"] == 29
        and abs(m0_l - 12.40) < 0.01 and abs(m1_l - 23.65) < 0.01
        and abs(m3_l - 28.04) < 0.01, esc)

    # F7: efeito-lam L2 e zero-L2 alinhado
    zero_alin = all(l2_por_cell[l].get(c, 0) == 0
                    for l in ("B", "A") for c in ALINHADAS)
    chk("F7_zero_L2_celulas_alinhadas_insample", zero_alin, l2_por_cell)
    chk("F7_L2_Tout_FCoth_C3",
        l2_por_cell["B"].get("T_out") == 68 and l2_por_cell["A"].get("T_out") == 91
        and l2_por_cell["B"].get("FC_oth") == 22 and l2_por_cell["A"].get("FC_oth") == 12
        and l2_por_cell["B"].get("C3") == 15 and l2_por_cell["A"].get("C3") == 17,
        l2_por_cell)

    # A6: estatisticas dos 46
    orb46s = sorted(orb46)
    res["A6_orbitas"] = {"min": orb46s[0], "mediana": orb46s[23],
                         "max": orb46s[-1]}
    res["A6_dep"] = {"B": [min(dep46B), max(dep46B)],
                     "A": [min(dep46A), max(dep46A)]}
    res["A6_sigmaA_distintos"] = len(sigA46)
    res["A6_dep0"] = dep0_casos
    chk("A6_relatorio_orbitas_dep_sigma",
        orb46s[0] == 7 and orb46s[23] == 21 and orb46s[-1] == 40
        and min(dep46B) == 0 and max(dep46B) == 2048
        and min(dep46A) == 384 and max(dep46A) == 2048
        and len(sigA46) == 11
        and dep0_casos == [(910000001, 14155, "DT_oth", "B")],
        {"orb": res["A6_orbitas"], "dep": res["A6_dep"],
         "sigA": len(sigA46), "dep0": dep0_casos})

    # celulas (contagens da populacao)
    chk("A3_celulas_populacao",
        cnt_cell == {"C3": 3451, "DT_lam": 417, "DT_oth": 904, "FC_lam": 895,
                     "FC_oth": 1718, "T_in": 835, "T_out": 1780}, cnt_cell)

    # A7: dep na populacao (prevalencia combinada, leitura apenas)
    comb = json.load(open(DST + "/prevalencia/prevalencia-combinada-N10000.json"))
    res["A7_dep_presente_combinada"] = comb.get("dep_presente",
                                                comb.get("dep", "n/d"))

    # comparacao com ws5-correlacao.json (valores ja publicados)
    corr = json.load(open(WS + "/ws5-correlacao.json"))
    ee = corr["escada_estado"]
    el = corr["escada_bothL1"]
    chk("A5_correlacao_json_coincide",
        ee["obs"] == obs_e and abs(ee["M0_indep"] - round(m0_e, 3)) < 1e-9
        and abs(ee["M1_classe"] - round(m1_e, 3)) < 1e-9
        and abs(ee["M2_celula7"] - round(m2_e, 3)) < 1e-9
        and abs(ee["M3_geometria_exacta_iEq"]["pred"] - round(m3_e, 3)) < 1e-9
        and el["obs"] == obs_l
        and abs(el["M3_geometria_exacta_iIso"]["pred"] - round(m3_l, 3)) < 1e-9)
    fis = corr["independencia_condicional_por_celula_estado"]
    res["A5_fisher_FC_oth"] = fis["FC_oth"]["p_fisher_bicaudal"]
    chk("A5_fisher_FC_oth_0018",
        abs(fis["FC_oth"]["p_fisher_bicaudal"] - 0.018) < 5e-3,
        fis["FC_oth"]["p_fisher_bicaudal"])

    res["duracao_s"] = round(time.time() - t0, 1)
    res["n_falhas"] = len(fails)
    res["falhas"] = fails
    corpo = json.dumps(res, sort_keys=True, indent=1, default=str).encode()
    open(WS + "/ws5-audit-agent2.json", "wb").write(corpo)
    print(json.dumps({k: v for k, v in res.items() if k != "checks"},
                     sort_keys=True, indent=1, default=str))
    print("CHECKS:")
    for k, v in sorted(res["checks"].items()):
        print(("  PASS " if v["ok"] else "  FAIL ") + k)
    print("sha256 audit:", hashlib.sha256(corpo).hexdigest())
    print("TOTAL FALHAS:", len(fails))


if __name__ == "__main__":
    main()
