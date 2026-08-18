# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY - Pre-registo A v8.3, Fase 6 multiagente, WS5.
ESTRUTURA DA CLASSE DE FALHA: replay deterministico dos lotes exploratorios
910000001/910000002 (dados JA REGISTADOS; nao e amostra nova), extraccao de
caracteristicas por familia e por caso de colapso, e AUDITORIA independente
das alegacoes do agente unico que este WS reutiliza.

O resultado confirmatorio permanece NEGATIVO e imutavel. Nada aqui recalcula
ou reinterpreta o confirmatorio. Escreve apenas em ws5-failure-structure/.

Quantidades exactas (derivadas da dinamica congelada, verificadas aqui):
  W_M(p,q)   = sum_r pc2(M[r][p] ^ M[r][q]),  M = G0 (aresta C_AB->B, r=y)
                                              M = F0 (aresta C_BA->A, r=x)
  S_pi(a)    = sum_c W_M(pi[c], pi[sub_a(c)]) ; d_m = 32 * S_{pi_m}  (n=10)
  perfil     = [0, P1,P1, P2,P2, D0,D1,D2,D3] com
               P1 = W(pi0',pi1')+W(pi2',pi3'), P2 = W(pi0',pi2')+W(pi1',pi3'),
               D_w = deg_W(pi[w])  (pi[c]=pi c)
  L1  <=> Wtil_0 == Wtil_1  <=> tau = pi1 o pi0^{-1} in Iso(W_M)
  estado (C1') <=> rank_canonico(S_{pi_0}) == rank_canonico(S_{pi_1})
  celula = orbita de rho = pi_0^{-1} o pi_1 sob conjugacao por D4 = Stab(M_C),
           equivalente a (classe de tau, relacao de lam = pi_0({{0,3},{1,2}})
           com tau); 7 celulas. As duas arestas PARTILHAM (tau, lam).
"""
import sys, json, time, hashlib, itertools
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws5-failure-structure"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

SEEDS = [910000001, 910000002]   # lotes REGISTADOS (replay, nao amostra nova)
N_POR_SEED = 5000
AUDIT_EVERY = 250                # familia fam_global % 250 == 0 -> maquinaria
SAIDA_FAM = WS + "/ws5-familias-N10000.json"
SAIDA_46 = WS + "/ws5-casos46.json"

ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5], "G0"),
           ("C_BA->A", [8, 9], [0, 1, 2], [2], "F0"))

PERMS = [tuple(p) for p in itertools.permutations(range(4))]
IDP = (0, 1, 2, 3)

# matchings do conjunto de 4 vertices: 0:{{0,1},{2,3}} 1:{{0,2},{1,3}} 2:{{0,3},{1,2}}
MATCHINGS = [frozenset([frozenset([0, 1]), frozenset([2, 3])]),
             frozenset([frozenset([0, 2]), frozenset([1, 3])]),
             frozenset([frozenset([0, 3]), frozenset([1, 2])])]


def pc2(v):
    return bin(v).count("1")


def w_base(M):
    return tuple(tuple(sum(pc2(M[r][p] ^ M[r][q]) for r in range(4))
                       for q in range(4)) for p in range(4))


def compõe(a, b):
    # (a o b)(c) = a[b[c]]
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
    # t double-transposition -> o matching {{a,t(a)},{b,t(b)}}
    pares = set()
    for a in range(4):
        pares.add(frozenset([a, t[a]]))
    return frozenset(pares)


# substituicoes de canal na ordem EXACTA de cl.intervencoes (auditada em main)
def subs_canal(bits):
    lo, hi = bits
    out = []
    for (mk, vl) in cl.intervencoes(bits):
        mc = ((mk >> lo) & 1) | (((mk >> hi) & 1) << 1)
        vc = ((vl >> lo) & 1) | (((vl >> hi) & 1) << 1)
        out.append((mc, vc))
    return out


def perfil_S(W, p, subs):
    return [sum(W[p[c]][p[(c & ~mc) | vc]] for c in range(4))
            for (mc, vc) in subs]


def grupo_iso(W):
    return frozenset(p for p in PERMS
                     if all(W[p[a]][p[b]] == W[a][b]
                            for a in range(4) for b in range(4)))


def wtil_tuple(W, p):
    return tuple(W[p[c1]][p[c2]] for c1 in range(4) for c2 in range(4))


# ---- celula: via (tau, lam) ------------------------------------------------
def celula_tau_lam(tau, lam):
    ct = cycle_type(tau)
    if ct == (1, 1, 2):
        # transposicao (a b): "in" se {a,b} e' aresta de lam
        ab = frozenset(a for a in range(4) if tau[a] != a)
        return "T_in" if ab in lam else "T_out"
    if ct == (2, 2):
        return "DT_lam" if matching_de_dt(tau) == lam else "DT_oth"
    if ct == (4,):
        t2 = compõe(tau, tau)
        return "FC_lam" if matching_de_dt(t2) == lam else "FC_oth"
    return "C3"


# ---- celula: via orbita de rho sob conjugacao por D4 = Stab(M_C) -----------
def _stab_MC():
    return [p for p in PERMS if perm_matching(p, 2) == MATCHINGS[2]]

D4 = _stab_MC()

def celula_rho_D4(rho):
    # normaliza para pi_0 = id: tau = rho, lam = M_C
    orb = frozenset(compõe(compõe(s, rho), inverte(s)) for s in D4)
    rep = min(orb)
    return _ORBIT_LABEL[rep]

def _build_orbit_labels():
    lab = {}
    for rho in PERMS:
        if rho == IDP:
            continue
        c = celula_tau_lam(rho, MATCHINGS[2])
        orb = frozenset(compõe(compõe(s, rho), inverte(s)) for s in D4)
        rep = min(orb)
        if rep in lab:
            assert lab[rep] == c, (rep, lab[rep], c)
        else:
            lab[rep] = c
    return lab

_ORBIT_LABEL = _build_orbit_labels()


def theta_sha(th):
    return hashlib.sha256(
        json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()


def fibra_maquinaria(T, n, ints, bits_b, mem):
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    Z0 = cl.estados_da_fibra(n, mem, 0)
    Z1 = cl.estados_da_fibra(n, mem, 1)
    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    d0, d1, dep = [], [], 0
    for (mk, vl) in ints:
        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
        d0.append(int(popB[x0].sum()))
        d1.append(int(popB[x1].sum()))
        dep += int((x0 != x1).sum())
    return d0, d1, dep


def main():
    t0 = time.time()
    # substituicoes de canal: iguais para as duas arestas (auditoria)
    sc_B = subs_canal([6, 7])
    sc_A = subs_canal([8, 9])
    assert sc_B == sc_A, "substituicoes de canal divergem entre arestas"
    SUBS = sc_B
    assert SUBS == [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2),
                    (3, 0), (3, 1), (3, 2), (3, 3)], SUBS

    # exemplos registados (leitura apenas)
    stored = {}
    for seed, fn in ((910000001, "prevalencia-cancelamento-II.json"),
                     (910000002, "prevalencia-cancelamento-II-lote2.json")):
        d = json.load(open(DST + "/prevalencia/" + fn))
        for classe, lst in d["exemplos"].items():
            for r in lst:
                stored[(seed, r["tentativa"])] = (classe, r)
    stored_colapsos = {k for k, (c, _) in stored.items()
                      if c == "colapso_total"}
    print("registos armazenados carregados:", len(stored),
          "dos quais colapsos:", len(stored_colapsos), flush=True)

    NIVEL_MAP = {"L1_d_iguais": "L1", "L2_rank_igual_d_diferente": "L2",
                 "L3_rank_diferente": "L3"}

    familias = []
    casos = []
    cnt_niv = {"B": {"L1": 0, "L2": 0, "L3": 0},
               "A": {"L1": 0, "L2": 0, "L3": 0}}
    cnt_cell = {}
    cnt_classe_inst = {"colapso_total": 0, "individua_uma": 0,
                       "individua_ambas": 0}
    auditorias = {"maquinaria_ok": 0, "maquinaria_falha": 0,
                  "stored_match_ok": 0, "stored_match_falha": 0,
                  "coset_ok": 0, "coset_falha": 0,
                  "cell_agree_ok": 0, "cell_agree_falha": 0,
                  "estado_consistente_ok": 0, "estado_consistente_falha": 0,
                  "sha_ok": 0, "sha_falha": 0}
    fam_global = 0

    for seed in SEEDS:
        ss = np.random.SeedSequence(seed)
        rng_theta = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))
        aceites = 0
        tent = 0
        while aceites < N_POR_SEED and tent < 200000:
            tent += 1
            th = g.sample_theta_base(rng_theta)
            if th.pi[0] == th.pi[1]:
                continue
            ok, _, _ = g.elegibilidade(th, False)
            if not ok:
                continue
            aceites += 1
            eh_audit = (fam_global % AUDIT_EVERY == 0)

            pi0 = tuple(th.pi[0]); pi1 = tuple(th.pi[1])
            tau = compõe(pi1, inverte(pi0))
            rho = compõe(inverte(pi0), pi1)
            ct = cycle_type(tau)
            assert ct == cycle_type(rho)
            lam = perm_matching(pi0, 2)     # imagem de M_C^canal por pi_0
            cell1 = celula_tau_lam(tau, lam)
            cell2 = celula_rho_D4(rho)
            if cell1 == cell2:
                auditorias["cell_agree_ok"] += 1
            else:
                auditorias["cell_agree_falha"] += 1

            reg = {"seed": seed, "fam": aceites - 1, "tentativa": tent,
                   "sha16": theta_sha(th)[:16], "tau_classe": str(ct),
                   "cell": cell1}
            niveis = {}
            por_aresta = {}
            for nome, ba, bb, mem, tn in ARESTAS:
                M = th.G0 if tn == "G0" else th.F0
                W = w_base(M)
                r0 = cl.rank_canonico(perfil_S(W, pi0, SUBS))
                r1 = cl.rank_canonico(perfil_S(W, pi1, SUBS))
                wt0 = wtil_tuple(W, pi0)
                wt1 = wtil_tuple(W, pi1)
                if wt0 == wt1:
                    nv = "L1"
                elif r0 == r1:
                    nv = "L2"
                else:
                    nv = "L3"
                iso = grupo_iso(W)
                if eh_audit:
                    # coset: {p: Wtil(p)==Wtil(pi0)} == {s o pi0 : s in iso}
                    exact = frozenset(p for p in PERMS
                                      if wtil_tuple(W, p) == wt0)
                    cos = frozenset(compõe(s, pi0) for s in iso)
                    if exact == cos:
                        auditorias["coset_ok"] += 1
                    else:
                        auditorias["coset_falha"] += 1
                eqc = frozenset(p for p in PERMS
                                if cl.rank_canonico(perfil_S(W, p, SUBS)) == r0)
                # consistencia: estado <=> pi1 in eqc ; L1 <=> tau in iso
                est = (nv != "L3")
                if ((pi1 in eqc) == est) and ((tau in iso) == (nv == "L1")):
                    auditorias["estado_consistente_ok"] += 1
                else:
                    auditorias["estado_consistente_falha"] += 1
                niveis[nome] = nv
                lado = "B" if tn == "G0" else "A"
                cnt_niv[lado][nv] += 1
                por_aresta[nome] = {"nivel": nv, "W": W, "iso": iso,
                                    "eqc": eqc, "pi0": pi0, "pi1": pi1}

            eqB = por_aresta["C_AB->B"]["eqc"]
            eqA = por_aresta["C_BA->A"]["eqc"]
            isoB = por_aresta["C_AB->B"]["iso"]
            isoA = por_aresta["C_BA->A"]["iso"]
            inter_eq = len(eqB & eqA)
            inter_iso = len(isoB & isoA)

            n_l3 = sum(1 for v in niveis.values() if v == "L3")
            classe_i = {2: "individua_ambas", 1: "individua_uma",
                        0: "colapso_total"}[n_l3]
            cnt_classe_inst[classe_i] += 1
            cnt_cell[cell1] = cnt_cell.get(cell1, 0) + 1

            reg.update({
                "nivB": niveis["C_AB->B"], "nivA": niveis["C_BA->A"],
                "isoB": len(isoB), "isoA": len(isoA),
                "neqB": len(eqB), "neqA": len(eqA),
                "iEq": inter_eq, "iIso": inter_iso})
            familias.append(reg)

            eh_colapso = (classe_i == "colapso_total")
            eh_stored = (seed, tent) in stored
            fam_global += 1

            if eh_colapso or eh_stored or eh_audit:
                tab, n, lay = g.tabela_transicao("II", th, False)
                T = np.asarray(tab, dtype=np.int64)
                mq = {}
                ok_mq = True
                for nome, ba, bb, mem, tn in ARESTAS:
                    ints = cl.intervencoes(ba)
                    d0, d1, dep = fibra_maquinaria(T, n, ints, bb, mem)
                    M = th.G0 if tn == "G0" else th.F0
                    W = w_base(M)
                    dp0 = [32 * s for s in perfil_S(W, pi0, SUBS)]
                    dp1 = [32 * s for s in perfil_S(W, pi1, SUBS)]
                    nv_mq = ("L1" if d0 == d1 else
                             "L2" if cl.rank_canonico(d0) == cl.rank_canonico(d1)
                             else "L3")
                    if not (dp0 == d0 and dp1 == d1 and nv_mq == niveis[nome]):
                        ok_mq = False
                    mq[nome] = {"d0": d0, "d1": d1, "dep": dep}
                auditorias["maquinaria_ok" if ok_mq else "maquinaria_falha"] += 1

                if eh_stored:
                    classe_s, r_s = stored[(seed, tent)]
                    ok_s = (classe_s == classe_i and
                            r_s["theta_sha"] == theta_sha(th))
                    for nome in ("C_AB->B", "C_BA->A"):
                        ra = r_s["arestas"][nome]
                        ok_s = ok_s and (NIVEL_MAP[ra["nivel"]] == niveis[nome])
                        ok_s = ok_s and (ra["dep_sites"] == mq[nome]["dep"])
                        if "d0" in ra:
                            ok_s = ok_s and (ra["d0"] == mq[nome]["d0"] and
                                             ra["d1"] == mq[nome]["d1"])
                    auditorias["stored_match_ok" if ok_s
                               else "stored_match_falha"] += 1
                    if r_s["theta_sha"] == theta_sha(th):
                        auditorias["sha_ok"] += 1
                    else:
                        auditorias["sha_falha"] += 1

                if eh_colapso:
                    s0 = g._campos_para_int(g.estado_inicial("II", th), lay)
                    orb = cl.orbita(T, s0)
                    caso = {"seed": seed, "fam": aceites - 1,
                            "tentativa": tent, "theta_sha": theta_sha(th),
                            "pi0": list(pi0), "pi1": list(pi1),
                            "tau": list(tau), "rho": list(rho),
                            "tau_classe": str(ct), "cell": cell1,
                            "lam": sorted(sorted(b) for b in lam),
                            "sigmaA": th.sigmaA, "sigmaB": th.sigmaB,
                            "orbita_len": len(orb),
                            "mem_alcancada": {
                                "mA": sorted({(z >> 2) & 1 for z in orb}),
                                "mB": sorted({(z >> 5) & 1 for z in orb})},
                            "subtipo": (niveis["C_AB->B"], niveis["C_BA->A"]),
                            "arestas": {}}
                    for nome, ba, bb, mem, tn in ARESTAS:
                        M = th.G0 if tn == "G0" else th.F0
                        W = w_base(M)
                        pa = por_aresta[nome]
                        offd = sorted(W[a][b] for a in range(4)
                                      for b in range(a + 1, 4))
                        degs = sorted(sum(W[p][q] for q in range(4))
                                      for p in range(4))
                        m_sums = sorted(
                            sum(W[min(b)][max(b)] for b in mm)
                            for mm in MATCHINGS)
                        S0 = perfil_S(W, pi0, SUBS)
                        S1 = perfil_S(W, pi1, SUBS)
                        caso["arestas"][nome] = {
                            "M_nome": tn, "nivel": pa["nivel"],
                            "W": [list(r) for r in W],
                            "iso_n": len(pa["iso"]),
                            "neq": len(pa["eqc"]),
                            "offdiag": offd,
                            "n_offdiag_dist": len(set(offd)),
                            "equidistante": len(set(offd)) == 1,
                            "graus": degs,
                            "n_graus_dist": len(set(degs)),
                            "somas_matchings": m_sums,
                            "S0": S0, "S1": S1,
                            "d0": mq[nome]["d0"], "d1": mq[nome]["d1"],
                            "dep_sites": mq[nome]["dep"],
                            "n_dist_perfil0": len(set(S0)),
                            "n_dist_perfil1": len(set(S1)),
                            "tau_in_iso": tau in pa["iso"],
                        }
                    caso["iEq"] = inter_eq
                    caso["iIso"] = inter_iso
                    casos.append(caso)

        print("seed %d: aceites=%d tentativas=%d t=%.1fs"
              % (seed, aceites, tent, time.time() - t0), flush=True)

    # verificacao contra o conjunto armazenado de colapsos
    meus_colapsos = {(c["seed"], c["tentativa"]) for c in casos}
    assert meus_colapsos == stored_colapsos, (
        "conjunto de colapsos nao coincide",
        sorted(meus_colapsos - stored_colapsos),
        sorted(stored_colapsos - meus_colapsos))
    print("CONJUNTO DOS 46 COLAPSOS COINCIDE com o registado", flush=True)

    resumo = {
        "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
        "ws": "ws5-failure-structure",
        "resultado_confirmatorio": "negativo (imutavel; nada aqui o altera)",
        "seeds_replay": SEEDS,
        "nota_replay": "replay deterministico de lotes ja registados; nao e amostra nova",
        "n_familias": len(familias),
        "contagens_nivel": cnt_niv,
        "contagens_celula": cnt_cell,
        "contagens_instancia": cnt_classe_inst,
        "auditorias": auditorias,
        "n_casos_colapso": len(casos),
        "subs_canal": SUBS,
        "duracao_s": round(time.time() - t0, 1),
    }

    corpo = json.dumps({"resumo": resumo, "familias": familias},
                       sort_keys=True).encode()
    open(SAIDA_FAM, "wb").write(corpo)
    corpo46 = json.dumps({"resumo": resumo, "casos": casos},
                         sort_keys=True, indent=1).encode()
    open(SAIDA_46, "wb").write(corpo46)
    print(json.dumps(resumo, sort_keys=True, indent=1))
    print("sha256 familias:", hashlib.sha256(corpo).hexdigest())
    print("sha256 casos46 :", hashlib.sha256(corpo46).hexdigest())


if __name__ == "__main__":
    main()
