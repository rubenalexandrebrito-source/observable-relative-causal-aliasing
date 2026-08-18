# POST-CONFIRMATORY / EXPLORATORY  ---  Passo 3b
# Teste REACHABLE vs UNREACHABLE do remapeamento de memoria no acoplamento
# canal->processador. Faithful ao classificador congelado. NAO altera nada.
import sys, json
import numpy as np
DST = "/root/causal-A-postconfirmatory-analysis"
sys.path.insert(0, DST + "/frozen-copy")
import classificador as cl
import pontuacao as pt

chave = json.load(open(DST + "/chave-e2.json"))


def analisa(iid):
    inst = json.load(open(DST + "/conf-e2/instancias/%s.json" % iid))
    _, n, T, mods, s0 = cl.carregar(inst)
    T = np.asarray(T, dtype=np.int64)
    orb = cl.orbita(T, s0)
    orbset = set(int(z) for z in orb)
    tipos = pt._tipos_e2(chave[iid])
    res = cl.classificar(inst)
    proc = [i for i, m in enumerate(mods) if m["bits_memoria"]]
    arestas = [(a, b) for (a, b) in res["E_C"] if b in proc]
    print("\n" + "#" * 74)
    print("# familia %s  id %s  (variante II)" % (chave[iid]["familia"], iid))
    print("# |orbita|=%d" % len(orb))
    for (a_i, b_i) in arestas:
        membits = mods[b_i]["bits_memoria"]
        mb = membits[0]
        ext_b = cl.extractor(mods[b_i]["bits"], n)
        pop_b = cl.popcount_tab(len(mods[b_i]["bits"]))
        ints_a = cl.intervencoes(mods[a_i]["bits"])
        emem = cl.extractor(membits, n)
        mem_reach = sorted({int(emem[int(z)]) for z in orb})

        # fibras alinhadas m=0 / m=1 (mesmo eixo de bits livres)
        Z0 = cl.estados_da_fibra(n, membits, 0)
        Z1 = cl.estados_da_fibra(n, membits, 1)
        onorb0 = np.array([int(z) in orbset for z in Z0])
        onorb1 = np.array([int(z) in orbset for z in Z1])
        reach_pair = onorb0 | onorb1          # config livre tocada pela orbita

        # (1) d_m FULL (=C1'): rank por contexto
        def dvec(Z):
            nx0 = ext_b[T[Z]]
            return [int(pop_b[(ext_b[T[(Z & ~np.int64(mk)) | np.int64(vl)]] ^ nx0)].sum())
                    for (mk, vl) in ints_a]
        rank_full = [cl.rank_canonico(dvec(Z0)), cl.rank_canonico(dvec(Z1))]

        # (2) d_m REACHABLE (fibra restrita a estados na orbita)
        def dvec_reach(m):
            idx = [j for j in range(len(Z0)) if (int(Z0[j]) in orbset and m == 0) or (int(Z1[j]) in orbset and m == 1)]
            Zr = (Z0 if m == 0 else Z1)[idx]
            if len(Zr) == 0:
                return None
            nx0 = ext_b[T[Zr]]
            return [int(pop_b[(ext_b[T[(Zr & ~np.int64(mk)) | np.int64(vl)]] ^ nx0)].sum())
                    for (mk, vl) in ints_a]
        dr0, dr1 = dvec_reach(0), dvec_reach(1)
        rank_reach = [cl.rank_canonico(dr0) if dr0 else None,
                      cl.rank_canonico(dr1) if dr1 else None]

        # (3) memory-dependence PONTO-A-PONTO: para cada config livre e cada
        #     intervencao, a resposta do receptor muda entre m=0 e m=1?
        nx0_0 = ext_b[T[Z0]]
        nx0_1 = ext_b[T[Z1]]
        total_sites = 0
        reach_sites = 0
        for (mk, vl) in ints_a:
            x0 = ext_b[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0_0
            x1 = ext_b[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0_1
            dep = (x0 != x1)                    # dependencia da memoria por config
            total_sites += int(dep.sum())
            reach_sites += int((dep & reach_pair).sum())

        print("  aresta %s->%s  (mem bit=%d)  mem_reach=%s" % (tipos[a_i], tipos[b_i], mb, mem_reach))
        print("     C1' rank FULL  m0/m1 : %s  -> %s" % (rank_full, "SINAL(individua)" if rank_full[0] != rank_full[1] else "ESTADO(funde)"))
        print("     rank REACHABLE m0/m1 : %s  -> %s" % (rank_reach, "SINAL" if (rank_reach[0] is not None and rank_reach[1] is not None and rank_reach[0] != rank_reach[1]) else "ESTADO/indef"))
        print("     estados-orbita com m=0 : %d ; com m=1 : %d" % (int(onorb0.sum()), int(onorb1.sum())))
        print("     memory-dependence ponto-a-ponto: total=%d sites ; em config TOCADA pela orbita=%d" % (total_sites, reach_sites))


for iid in ["7bb0baab3a8ed7aa", "070e525e441ee298"]:   # fam 20 (falhada) vs fam 10 (correta)
    analisa(iid)
print("\n[fim 3b]")
