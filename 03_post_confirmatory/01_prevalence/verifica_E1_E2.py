# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — verificação empírica do lema d^{E2} = 4·d^{E1}.

Lema (formal): no layout do Estrato 2, z = (core bits 0..9, D1=bit 10, D2=bit 11);
a transição do núcleo não depende dos bits D (D'_i = R_i(core_t), e o núcleo só lê
o núcleo). O receptor (A ou B) e o canal intervencionado estão no núcleo. Na fibra
counterfactual do receptor (todos os bits livres excepto o bit de memória), cada
configuração-livre do núcleo aparece exactamente 4 vezes (as 4 escolhas de D1,D2),
com resposta do receptor IDÊNTICA (baseline e pós-intervenção). Logo, somando
Hamming sobre a fibra completa: d^{n=12} = 4·d^{n=10}, componente a componente;
dep_sites^{n=12} = 4·dep_sites^{n=10}; rank_canonico é invariante a escala
positiva (ordem e empates preservados) e as igualdades d0==d1 preservam-se.
=> Os níveis L1/L2/L3 são IDÊNTICOS nos dois regimes: medir em n=10 transfere
exactamente para o regime confirmatório E2 (n=12).

Este script verifica o lema por comparação directa em K famílias elegíveis novas
(semente 910000003; extensão E2 pelo fluxo posicional [3], como no gerador).
Não altera nada; descritivo.
"""
import sys, json, hashlib
import numpy as np
DST = "/root/causal-A-postconfirmatory-analysis"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

SEED = 910000003
K = 10
ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5]),
           ("C_BA->A", [8, 9], [0, 1, 2], [2]))


def dvecs(T, n, bits_a, bits_b, mem):
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    ints = cl.intervencoes(bits_a)
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


def nivel(d0, d1):
    if d0 == d1:
        return "L1"
    if cl.rank_canonico(d0) == cl.rank_canonico(d1):
        return "L2"
    return "L3"


def main():
    ss = np.random.SeedSequence(SEED)
    f = ss.spawn(4)
    rng_theta = np.random.Generator(np.random.PCG64(f[0]))
    rng_e2 = np.random.Generator(np.random.PCG64(f[3]))
    ok_all = True
    k = 0
    tent = 0
    linhas = []
    while k < K and tent < 100000:
        tent += 1
        th = g.sample_theta_base(rng_theta)
        if th.pi[0] == th.pi[1]:
            continue
        ok, _, _ = g.elegibilidade(th, False)
        if not ok:
            continue
        g.estender_theta_e2(th, rng_e2)
        t10, n10, _ = g.tabela_transicao("II", th, False)
        t12, n12, _ = g.tabela_transicao("II", th, True)
        T10 = np.asarray(t10, dtype=np.int64)
        T12 = np.asarray(t12, dtype=np.int64)
        for nome, ba, bb, mem in ARESTAS:
            d0a, d1a, depa = dvecs(T10, n10, ba, bb, mem)
            d0b, d1b, depb = dvecs(T12, n12, ba, bb, mem)
            c_d = (d0b == [4 * x for x in d0a]) and (d1b == [4 * x for x in d1a])
            c_dep = (depb == 4 * depa)
            c_rank = ((cl.rank_canonico(d0a), cl.rank_canonico(d1a))
                      == (cl.rank_canonico(d0b), cl.rank_canonico(d1b)))
            c_niv = nivel(d0a, d1a) == nivel(d0b, d1b)
            ok_row = c_d and c_dep and c_rank and c_niv
            ok_all = ok_all and ok_row
            linhas.append((k, nome, c_d, c_dep, c_rank, c_niv,
                           nivel(d0b, d1b), depa, depb))
        k += 1
    print("fam | aresta   | d12==4*d10 | dep12==4*dep10 | ranks iguais | nivel igual | nivel | dep10 -> dep12")
    for (kk, nome, c_d, c_dep, c_rank, c_niv, nv, da, db) in linhas:
        print(" %2d | %-8s | %s | %s | %s | %s | %s | %d -> %d"
              % (kk, nome, c_d, c_dep, c_rank, c_niv, nv, da, db))
    print("\nfamilias verificadas:", k, "(tentativas:", tent, ")")
    print("LEMA d_E2 = 4*d_E1:", "CONFIRMADO em todas as arestas/famílias"
          if ok_all else "FALHOU (ver linhas)")
    print("nota fam-20 confirmatoria: dep observado n=12 foi 4608 por aresta")
    print("=> o lema preve dep nuclear n=10 = 1152 (4608/4), consistente.")
    try:
        print("sha256_script:",
              hashlib.sha256(open(__file__, "rb").read()).hexdigest())
    except Exception:
        pass


if __name__ == "__main__":
    main()
