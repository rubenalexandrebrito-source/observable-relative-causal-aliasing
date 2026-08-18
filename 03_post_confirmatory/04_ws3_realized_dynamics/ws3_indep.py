# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, ws3.
# VERIFICAÇÃO INDEPENDENTE da análise "dinâmica realizada estrita"
# (tentativa-interrompida-1): reimplementação própria, VIA ESTADOS DA ÓRBITA
# (testemunhas realizadas), sem reutilizar ws3_lib.py; a fibra completa só é
# usada para dep_total/d e para provar a redução (r,c) — com indexação própria.
# Compara campo a campo com ws3-strict-fam20.json / ws3-strict-bateria.json e
# com os datasets registados. Resultado confirmatório: NEGATIVO, imutável.
import json, sys, hashlib, time
from itertools import combinations
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws3-realized-dynamics"
TI = WS + "/tentativa-interrompida-1"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g          # congelado: sample_theta_base, elegibilidade, tabela_transicao
import classificador as cl   # congelado: usado APENAS como referência de cross-check
import pontuacao as pt

PC2 = (0, 1, 1, 2)

# ---------------------------------------------------------------- utilitários próprios

def ext_tab(bits, n):
    """Tabela própria de extração (equivalente a cl.extractor, codificada de raiz)."""
    z = np.arange(1 << n, dtype=np.int64)
    out = np.zeros(1 << n, dtype=np.int64)
    for pos, b in enumerate(bits):
        out |= ((z >> b) & np.int64(1)) << pos
    return out


def minhas_intervencoes(bits):
    """Enumeração própria de I_A = {(mask,valor): J ⊆ bits, eta ∈ {0,1}^|J|}."""
    out = []
    for r in range(len(bits) + 1):
        for J in combinations(bits, r):
            mJ = 0
            for b in J:
                mJ |= 1 << b
            for eta in range(1 << len(J)):
                v = 0
                for i, b in enumerate(J):
                    v |= ((eta >> i) & 1) << b
                out.append((mJ, v))
    return out


def minha_orbita(T, s0):
    vistos, ordem, s = set(), [], int(s0)
    while s not in vistos:
        vistos.add(s)
        ordem.append(s)
        s = int(T[s])
    return ordem


def pop2b(v):
    return PC2[v & 3] + PC2[(v >> 2) & 3] if v > 3 else PC2[v]


def categoria(s_estr, s_uni, dep_tot, inter_vazia):
    if dep_tot == 0:
        return "SEM_DEP"
    if s_estr >= 1:
        return "ESTRITO"
    if s_uni >= 1:
        return "UNIAO_APENAS_B1" if inter_vazia else "UNIAO_APENAS_B2"
    return "PURO_CONTRAFACTUAL"


def wilson(k, n_):
    if n_ == 0:
        return (None, None)
    z = 1.959963984540054
    p = k / n_
    den = 1 + z * z / n_
    ctr = p + z * z / (2 * n_)
    adj = z * ((p * (1 - p) / n_ + z * z / (4 * n_ * n_)) ** 0.5)
    return (round((ctr - adj) / den, 4), round((ctr + adj) / den, 4))


def analisa_aresta_indep(T, n, bits_a, bits_b, membits, orb, popB_bits):
    """Análise independente de uma aresta canal->processador.

    Rota principal REALIZADA: testemunhas = estados da órbita; resposta
    intervencional avaliada DIRETAMENTE no estado realizado
    xr(s) = eB[T[(s&~mk)|vl]] ^ eB[T[s]].
    Fibra completa (indexação própria: Z0 = estados com bit de memória 0,
    Z1 = Z0|mm) apenas para dep_total, d_m e prova da redução (r,c)."""
    assert len(membits) == 1
    mm = np.int64(1 << membits[0])
    procbits = [b for b in bits_b if b not in membits]
    eB = ext_tab(bits_b, n)
    eP = ext_tab(procbits, n)
    eC = ext_tab(bits_a, n)
    ints = minhas_intervencoes(bits_a)
    assert ints == cl.intervencoes(bits_a), "ordem/conteudo de I_A difere do congelado"
    nb = len(bits_b)
    popB = np.array([bin(v).count("1") for v in range(1 << nb)], dtype=np.int64)

    S = np.arange(1 << n, dtype=np.int64)
    Z0 = S[(S & mm) == 0]          # representantes do eixo livre (mem=0)
    Z1 = Z0 | mm
    cells = (eP[Z0] << 2) | eC[Z0]
    assert np.array_equal(cells, (eP[Z1] << 2) | eC[Z1])
    nx0f, nx1f = eB[T[Z0]], eB[T[Z1]]

    orbA = np.array(orb, dtype=np.int64)
    m_orb = ((orbA & mm) != 0).astype(np.int64)
    key_cfg = orbA & ~mm
    cell_orb = (eP[orbA] << 2) | eC[orbA]
    R = {0: set(), 1: set()}
    C = {0: set(), 1: set()}
    wit_cell = {0: {}, 1: {}}      # primeira testemunha realizada por (m, célula)
    wit_cfg = {0: {}, 1: {}}
    for i, s in enumerate(orbA):
        m = int(m_orb[i])
        R[m].add(int(key_cfg[i]))
        C[m].add(int(cell_orb[i]))
        wit_cell[m].setdefault(int(cell_orb[i]), int(s))
        wit_cfg[m].setdefault(int(key_cfg[i]), int(s))
    I_cfg = R[0] & R[1]; U_cfg = R[0] | R[1]
    I_rc = sorted(C[0] & C[1]); U_rc = sorted(C[0] | C[1])

    d0, d1 = [], []
    dep_total = 0
    cfg_estr = cfg_uni = 0
    rc_tot = rc_estr = rc_uni = 0
    pat = {0: [], 1: []}           # padrões por célula via fibra (para prova de redução)
    exc_reducao = 0
    testemunhas = []
    for k_i, (mk, vl) in enumerate(ints):
        mkN, vlN = np.int64(mk), np.int64(vl)
        x0 = eB[T[(Z0 & ~mkN) | vlN]] ^ nx0f
        x1 = eB[T[(Z1 & ~mkN) | vlN]] ^ nx1f
        d0.append(int(popB[x0].sum()))
        d1.append(int(popB[x1].sum()))
        dep = x0 != x1
        dep_total += int(dep.sum())
        # prova da redução (r,c) por rota própria: padrão único por célula
        p0 = np.full(16, -1, dtype=np.int64)
        p1 = np.full(16, -1, dtype=np.int64)
        for cell in range(16):
            sel = cells == cell
            u0 = np.unique(x0[sel]); u1 = np.unique(x1[sel])
            if len(u0) != 1 or len(u1) != 1:
                exc_reducao += 1
                u0, u1 = u0[:1], u1[:1]
            p0[cell], p1[cell] = int(u0[0]), int(u1[0])
        pat[0].append(p0); pat[1].append(p1)
        # sítios cfg estritos/união — via estados realizados (chave = estado sem bit mem)
        for zk in I_cfg:
            xr0 = int(eB[T[(np.int64(zk) & ~mkN) | vlN]] ^ eB[T[np.int64(zk)]])
            z1k = np.int64(zk) | mm
            xr1 = int(eB[T[(z1k & ~mkN) | vlN]] ^ eB[T[z1k]])
            if xr0 != xr1:
                cfg_estr += 1
        for zk in U_cfg:
            xr0 = int(eB[T[(np.int64(zk) & ~mkN) | vlN]] ^ eB[T[np.int64(zk)]])
            z1k = np.int64(zk) | mm
            xr1 = int(eB[T[(z1k & ~mkN) | vlN]] ^ eB[T[z1k]])
            if xr0 != xr1:
                cfg_uni += 1
        # sítios (r,c): totais via fibra; estritos/união via TESTEMUNHAS realizadas
        difc = p0 != p1
        rc_tot += int(difc.sum())
        for cell in I_rc:
            s0w, s1w = wit_cell[0][cell], wit_cell[1][cell]
            r0 = int(eB[T[(np.int64(s0w) & ~mkN) | vlN]] ^ eB[T[np.int64(s0w)]])
            r1 = int(eB[T[(np.int64(s1w) & ~mkN) | vlN]] ^ eB[T[np.int64(s1w)]])
            assert r0 == int(p0[cell]) and r1 == int(p1[cell]), \
                "testemunha realizada difere do padrao da fibra (reducao violada)"
            if r0 != r1:
                rc_estr += 1
                testemunhas.append((k_i, cell, r0, r1))
        for cell in U_rc:
            sw0 = wit_cell[0].get(cell)
            sw1 = wit_cell[1].get(cell)
            s0w = np.int64(sw0) if sw0 is not None else (np.int64(wit_cell[1][cell]) & ~mm)
            s1w = np.int64(sw1) if sw1 is not None else (np.int64(wit_cell[0][cell]) | mm)
            r0 = int(eB[T[(s0w & ~mkN) | vlN]] ^ eB[T[s0w]])
            r1 = int(eB[T[(s1w & ~mkN) | vlN]] ^ eB[T[s1w]])
            if r0 != r1:
                rc_uni += 1

    # contraste observacional (D7): só testemunhas realizadas, pares na interseção
    por_r = {}
    for cell in I_rc:
        por_r.setdefault(cell >> 2, []).append(cell & 3)
    obs_pares = obs_dif = 0
    obs_det = []
    for r_ in sorted(por_r):
        cs = sorted(por_r[r_])
        for i in range(len(cs)):
            for j in range(i + 1, len(cs)):
                ca, cb = (r_ << 2) | cs[i], (r_ << 2) | cs[j]
                o = {}
                for m in (0, 1):
                    sa, sb = np.int64(wit_cell[m][ca]), np.int64(wit_cell[m][cb])
                    o[m] = int(eB[T[sa]] ^ eB[T[sb]])
                obs_pares += 1
                dif = o[0] != o[1]
                obs_dif += int(dif)
                obs_det.append({"r": r_, "c1": cs[i], "c2": cs[j],
                                "O_m0": o[0], "O_m1": o[1], "difere": bool(dif)})

    if d0 == d1:
        nivel = "L1_d_iguais"
    elif cl.rank_canonico(d0) == cl.rank_canonico(d1):
        nivel = "L2_rank_igual_d_diferente"
    else:
        nivel = "L3_rank_diferente"

    return {
        "nivel": nivel, "d0": d0, "d1": d1, "dep_total": dep_total,
        "exc_reducao": exc_reducao,
        "cfg": {"R0": len(R[0]), "R1": len(R[1]), "uniao": len(U_cfg),
                "intersecao_estrita": len(I_cfg),
                "sitios_uniao": cfg_uni, "sitios_estritos": cfg_estr},
        "rc": {"I": I_rc, "n_C0": len(C[0]), "n_C1": len(C[1]),
               "n_I": len(I_rc), "n_U": len(U_rc),
               "sitios_totais": rc_tot, "sitios_uniao": rc_uni,
               "sitios_estritos": rc_estr},
        "obs": {"pares": obs_pares, "pares_diferentes": obs_dif},
        "obs_detalhe": obs_det,
        "testemunhas": testemunhas,
        "categoria_cfg": categoria(cfg_estr, cfg_uni, dep_total, len(I_cfg) == 0),
        "categoria_rc": categoria(rc_estr, rc_uni, dep_total, len(I_rc) == 0),
        "pat": pat, "ints": ints,
        "wit_cell": wit_cell, "mem_reach": sorted({int(m) for m in m_orb}),
    }


def formula_theta(th, nome, ints, eC_int):
    """Padrões e d_m derivados SÓ de theta (variante II canónica):
    xr(r,c;int,m) = M[r][pi_m(c)] ^ M[r][pi_m(c')], c' = (c&~mk_c)|vl_c."""
    M = th.G0 if nome == "C_AB->B" else th.F0
    pats = {0: [], 1: []}
    d = {0: [], 1: []}
    for m in (0, 1):
        for (mk, vl) in ints:
            mkc, vlc = eC_int(mk), eC_int(vl)
            pk = []
            tot = 0
            for cell in range(16):
                r_, c_ = cell >> 2, cell & 3
                c2 = (c_ & (~mkc & 3)) | vlc
                p = M[r_][th.pi[m][c_]] ^ M[r_][th.pi[m][c2]]
                pk.append(p)
                tot += PC2[p]
            pats[m].append(pk)
            d[m].append(32 * tot)
    return d, pats


def tau_isometria(th, nome):
    M = th.G0 if nome == "C_AB->B" else th.F0
    W = [[sum(PC2[M[r][p] ^ M[r][q]] for r in range(4)) for q in range(4)]
         for p in range(4)]
    pi0, pi1 = th.pi
    inv0 = [0] * 4
    for i, v in enumerate(pi0):
        inv0[v] = i
    tau = [pi1[inv0[p]] for p in range(4)]
    return all(W[tau[p]][tau[q]] == W[p][q] for p in range(4) for q in range(4))


def replay_meu(seed, alvo_sha):
    """Replay próprio (contador por CADA theta amostrado; elegibilidade é
    determinística e não consome o fluxo — verificado por 126/126 shas)."""
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(seed).spawn(4)[0]))
    out = {}
    for t in range(1, max(alvo_sha) + 1):
        th = g.sample_theta_base(rng)
        if t in alvo_sha:
            sha = hashlib.sha256(json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()
            if sha != alvo_sha[t]:
                raise RuntimeError("replay proprio falhou seed=%d t=%d" % (seed, t))
            if th.pi[0] == th.pi[1]:
                raise RuntimeError("pi iguais em alvo aceite")
            ok, razao, _ = g.elegibilidade(th, False)
            if not ok:
                raise RuntimeError("alvo inelegivel: %s" % razao)
            out[t] = th
    return out


def tabela_II_minha(th):
    """Tabela de transição própria a partir de theta (variante II, n=10),
    para verificar g.tabela_transicao de forma independente."""
    tab = [0] * 1024
    for v in range(1024):
        x = v & 3; mA = (v >> 2) & 1; y = (v >> 3) & 3
        mB = (v >> 5) & 1; cAB = (v >> 6) & 3; cBA = (v >> 8) & 3
        vv = th.pi[mB][cAB]
        uu = th.pi[mA][cBA]
        x2 = th.F0[x][uu] ^ th.sigmaA[mA]
        mA2 = th.H[mA][x]
        y2 = th.G0[y][vv] ^ th.sigmaB[mB]
        mB2 = th.K[mB][y]
        tab[v] = x2 | (mA2 << 2) | (y2 << 3) | (mB2 << 5) | (x << 6) | (y << 8)
    return tab
