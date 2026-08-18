# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, ws3
# Biblioteca partilhada da análise "dinâmica realizada estrita".
# Importa APENAS o instrumento congelado (frozen-copy); não altera nada
# fora de multiagent/ws3-realized-dynamics/. Definições: precommit-ws3-strict.txt.
import sys, json, hashlib
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g         # congelado (12/12 vs MANIFEST)
import classificador as cl  # congelado

ARESTAS_N10 = (("C_AB->B", [6, 7], [3, 4, 5], [5]),
               ("C_BA->A", [8, 9], [0, 1, 2], [2]))
PC2 = (0, 1, 1, 2)


def theta_sha(th):
    return hashlib.sha256(json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()


def wilson(k, n_):
    if n_ == 0:
        return (None, None)
    z = 1.959963984540054
    p = k / n_
    den = 1 + z * z / n_
    ctr = p + z * z / (2 * n_)
    adj = z * ((p * (1 - p) / n_ + z * z / (4 * n_ * n_)) ** 0.5)
    return (round((ctr - adj) / den, 6), round((ctr + adj) / den, 6))


def _categoria(s_estr, s_uni, dep_tot, inter_vazia):
    if dep_tot == 0:
        return "SEM_DEP"
    if s_estr >= 1:
        return "ESTRITO"
    if s_uni >= 1:
        return "UNIAO_APENAS_B1" if inter_vazia else "UNIAO_APENAS_B2"
    return "PURO_CONTRAFACTUAL"


def analisa_aresta_realizada(T, n, bits_a, bits_b, membits, orb,
                             detalhe=False, proj_core=None):
    """Análise estrita/união/contrafactual de uma aresta canal->processador.
    Convenções congeladas: fibras alinhadas (cl.estados_da_fibra), 9 intervenções
    (cl.intervencoes), sítio de dependência = (intervenção, ponto) com padrão
    xr_0 != xr_1 (= prevalencia/autopsia step3b). Granularidades: configuração
    completa, (r,c) e, opcionalmente, uma projeção extra (ex.: configuração
    nuclear sem bits D), dada como tabela extractor sobre estados."""
    orbset = set(int(s) for s in orb)
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    ints = cl.intervencoes(bits_a)
    procbits = [b for b in bits_b if b not in membits]
    eProc = cl.extractor(procbits, n)
    eChan = cl.extractor(bits_a, n)
    emem = cl.extractor(membits, n)
    mem_reach = sorted({int(emem[s]) for s in orbset})
    if mem_reach != [0, 1]:
        return {"mem_reach": mem_reach, "categoria_rc": "SEM_CONTRASTE",
                "categoria_cfg": "SEM_CONTRASTE"}

    Z0 = cl.estados_da_fibra(n, membits, 0)
    Z1 = cl.estados_da_fibra(n, membits, 1)
    onorb0 = np.fromiter((int(z) in orbset for z in Z0), dtype=bool, count=len(Z0))
    onorb1 = np.fromiter((int(z) in orbset for z in Z1), dtype=bool, count=len(Z1))
    uniao_cfg = onorb0 | onorb1
    estr_cfg = onorb0 & onorb1

    rc = ((eProc[Z0] << 2) | eChan[Z0]).astype(np.int64)
    rc_1 = ((eProc[Z1] << 2) | eChan[Z1]).astype(np.int64)
    if not np.array_equal(rc, rc_1):
        raise RuntimeError("eixo (r,c) nao alinhado entre fibras")
    cell_idx = [np.flatnonzero(rc == cell) for cell in range(16)]
    mult = len(Z0) // 16
    for cell in range(16):
        if len(cell_idx[cell]) != mult:
            raise RuntimeError("celulas (r,c) de tamanho desigual")
    reps = np.array([ci[0] for ci in cell_idx], dtype=np.int64)

    exc_reducao = [0]

    def constancia(vec):
        for cell in range(16):
            ci = cell_idx[cell]
            if not np.all(vec[ci] == vec[ci[0]]):
                exc_reducao[0] += 1

    C0 = sorted({int(v) for v in rc[onorb0]})
    C1 = sorted({int(v) for v in rc[onorb1]})
    Iset = sorted(set(C0) & set(C1))
    Uset = sorted(set(C0) | set(C1))

    # projeção extra (granularidade intermédia), opcional
    core = None
    if proj_core is not None:
        pe = proj_core[Z0].astype(np.int64)
        if not np.array_equal(pe, proj_core[Z1].astype(np.int64)):
            raise RuntimeError("projecao extra nao alinhada entre fibras")
        Sc0 = {int(v) for v in pe[onorb0]}
        Sc1 = {int(v) for v in pe[onorb1]}
        interC = sorted(Sc0 & Sc1)
        uniC = sorted(Sc0 | Sc1)
        repC = {}
        for j, v in enumerate(pe):
            v = int(v)
            if v not in repC:
                repC[v] = j
        core = {"S0": len(Sc0), "S1": len(Sc1), "intersecao": len(interC),
                "uniao": len(uniC), "sitios_estritos": 0, "sitios_uniao": 0,
                "_interC": interC, "_uniC": uniC, "_repC": repC}

    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    constancia(nx0)
    constancia(nx1)

    d0v, d1v = [], []
    dep_total = dep_uniao_cfg = dep_estr_cfg = 0
    cel_total = cel_uniao = cel_estr = 0
    pat_cells = {0: [], 1: []}          # por intervenção: array (16,) de padrões xr
    testemunhas = []
    for k_int, (mk, vl) in enumerate(ints):
        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
        constancia(x0)
        constancia(x1)
        d0v.append(int(popB[x0].sum()))
        d1v.append(int(popB[x1].sum()))
        dep = x0 != x1
        dep_total += int(dep.sum())
        dep_uniao_cfg += int((dep & uniao_cfg).sum())
        dep_estr_cfg += int((dep & estr_cfg).sum())
        dif_cells = dep[reps]
        cel_total += int(dif_cells.sum())
        cel_uniao += sum(1 for cell in Uset if dif_cells[cell])
        cel_estr += sum(1 for cell in Iset if dif_cells[cell])
        if core is not None:
            core["sitios_uniao"] += sum(1 for v in core["_uniC"] if dep[core["_repC"][v]])
            core["sitios_estritos"] += sum(1 for v in core["_interC"] if dep[core["_repC"][v]])
        pat_cells[0].append(x0[reps].astype(np.int64))
        pat_cells[1].append(x1[reps].astype(np.int64))
        if detalhe:
            for cell in Iset:
                if dif_cells[cell]:
                    testemunhas.append({
                        "intervencao": k_int, "mascara": int(mk), "valor": int(vl),
                        "r": cell >> 2, "c": cell & 3,
                        "padrao_m0": int(x0[reps[cell]]),
                        "padrao_m1": int(x1[reps[cell]]),
                        "peso_m0": int(popB[x0[reps[cell]]]),
                        "peso_m1": int(popB[x1[reps[cell]]])})

    # contraste observacional (D7): pares (r,c1),(r,c2) ambos na interseção estrita
    obs_pares = obs_dif = 0
    obs_det = []
    por_r = {}
    for cell in Iset:
        por_r.setdefault(cell >> 2, []).append(cell & 3)
    for r_ in sorted(por_r):
        cs = sorted(por_r[r_])
        for i in range(len(cs)):
            for j in range(i + 1, len(cs)):
                a_, b_ = (r_ << 2) | cs[i], (r_ << 2) | cs[j]
                o0 = int(nx0[reps[a_]] ^ nx0[reps[b_]])
                o1 = int(nx1[reps[a_]] ^ nx1[reps[b_]])
                obs_pares += 1
                dif = bool(o0 != o1)
                if dif:
                    obs_dif += 1
                if detalhe:
                    obs_det.append({"r": r_, "c1": cs[i], "c2": cs[j],
                                    "O_m0": o0, "O_m1": o1, "difere": dif})

    if d0v == d1v:
        nivel = "L1_d_iguais"
    elif cl.rank_canonico(d0v) == cl.rank_canonico(d1v):
        nivel = "L2_rank_igual_d_diferente"
    else:
        nivel = "L3_rank_diferente"

    out = {
        "mem_reach": mem_reach,
        "nivel": nivel, "d0": d0v, "d1": d1v,
        "dep_total": dep_total,
        "multiplicidade_celula": mult,
        "cfg": {"R0": int(onorb0.sum()), "R1": int(onorb1.sum()),
                "uniao": int(uniao_cfg.sum()), "intersecao_estrita": int(estr_cfg.sum()),
                "sitios_uniao": dep_uniao_cfg, "sitios_estritos": dep_estr_cfg},
        "rc": {"C0": C0, "C1": C1, "I": Iset, "U": Uset,
               "n_C0": len(C0), "n_C1": len(C1), "n_I": len(Iset), "n_U": len(Uset),
               "sitios_totais": cel_total, "sitios_uniao": cel_uniao,
               "sitios_estritos": cel_estr},
        "obs": {"pares": obs_pares, "pares_diferentes": obs_dif},
        "categoria_cfg": _categoria(dep_estr_cfg, dep_uniao_cfg, dep_total,
                                    int(estr_cfg.sum()) == 0),
        "categoria_rc": _categoria(cel_estr, cel_uniao, dep_total, len(Iset) == 0),
        "exc_reducao": exc_reducao[0],
    }
    if core is not None:
        out["core"] = {k: v for k, v in core.items() if not k.startswith("_")}
        out["categoria_core"] = _categoria(core["sitios_estritos"], core["sitios_uniao"],
                                           dep_total, core["intersecao"] == 0)
    if detalhe:
        out["testemunhas_estritas"] = testemunhas
        out["obs_detalhe"] = obs_det
        out["pat_cells"] = {str(m): [v.tolist() for v in pat_cells[m]] for m in (0, 1)}
        out["intervencoes"] = [[int(mk), int(vl)] for (mk, vl) in ints]
    out["_pat_cells_np"] = pat_cells
    return out


def formula_theta_aresta(th, nome, bits_a, n):
    """d_m e padrões por célula derivados DIRETAMENTE de theta (variante II,
    canónico n=10): xr(r,c;int,m) = M[r][pi_m(c)] XOR M[r][pi_m(c')], c'=(c&~mk_c)|vl_c;
    d_m = mult * soma_r,c pc2. Devolve (d0, d1, padroes[m][k_int][celula])."""
    M = th.G0 if nome == "C_AB->B" else th.F0
    pi = th.pi
    ints = cl.intervencoes(bits_a)
    eChan = cl.extractor(bits_a, n)
    mult = (1 << (n - 1)) // 16
    d = {0: [], 1: []}
    pats = {0: [], 1: []}
    for m in (0, 1):
        for (mk, vl) in ints:
            mkc, vlc = int(eChan[mk]), int(eChan[vl])
            tot = 0
            pk = [0] * 16
            for cell in range(16):
                r_, c_ = cell >> 2, cell & 3
                c2 = (c_ & (~mkc & 3)) | vlc
                p = M[r_][pi[m][c_]] ^ M[r_][pi[m][c2]]
                pk[cell] = p
                tot += PC2[p]
            d[m].append(mult * tot)
            pats[m].append(pk)
    return d[0], d[1], pats


def k_audit(th, nome):
    """tau = pi1 o pi0^{-1}; K <=> tau isometria de W_M (teorema da autópsia,
    reverificado aqui por aresta)."""
    M = th.G0 if nome == "C_AB->B" else th.F0
    W = [[sum(PC2[M[r][p] ^ M[r][q]] for r in range(4)) for q in range(4)]
         for p in range(4)]
    pi0, pi1 = th.pi
    inv0 = [0] * 4
    for i, v in enumerate(pi0):
        inv0[v] = i
    tau = [pi1[inv0[p]] for p in range(4)]
    iso = all(W[tau[p]][tau[q]] == W[p][q] for p in range(4) for q in range(4))
    return iso, tau, W


def replay_lote(seed, alvo_sha_por_tentativa):
    """Replay determinístico: percorre o fluxo theta nuclear do lote registado,
    contando CADA theta amostrado; verifica theta_sha nos alvos. Sem sementes novas."""
    ss = np.random.SeedSequence(seed)
    filhos = ss.spawn(4)
    rng = np.random.Generator(np.random.PCG64(filhos[0]))
    maxt = max(alvo_sha_por_tentativa)
    out = {}
    for t in range(1, maxt + 1):
        th = g.sample_theta_base(rng)
        if t in alvo_sha_por_tentativa:
            sha = theta_sha(th)
            if sha != alvo_sha_por_tentativa[t]:
                raise RuntimeError("REPLAY FALHOU: seed=%d tentativa=%d sha=%s != %s"
                                   % (seed, t, sha[:16], alvo_sha_por_tentativa[t][:16]))
            if th.pi[0] == th.pi[1]:
                raise RuntimeError("replay: pi identicas em alvo aceite (seed=%d t=%d)" % (seed, t))
            ok, razao, _ = g.elegibilidade(th, False)
            if not ok:
                raise RuntimeError("replay: alvo inelegivel (%s) seed=%d t=%d" % (razao, seed, t))
            out[t] = th
    return out
