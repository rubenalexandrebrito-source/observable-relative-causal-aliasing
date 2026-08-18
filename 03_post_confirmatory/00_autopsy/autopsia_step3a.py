# POST-CONFIRMATORY / EXPLORATORY  ---  Passo 3a
# Testa, nas 25 II de E2, se a ordem fraca de d_m(a) MUDA entre contextos de
# memoria ALCANCADOS (reachable), aresta a aresta que entra num processador.
# Replica EXACTAMENTE a maquinaria de C1' (classificador congelado). NAO altera nada.
import sys, json
import numpy as np
DST = "/root/causal-A-postconfirmatory-analysis"
sys.path.insert(0, DST + "/frozen-copy")
import classificador as cl
import pontuacao as pt

chave = json.load(open(DST + "/chave-e2.json"))
FALHADA = "7bb0baab3a8ed7aa"


def edge_profiles(inst, a_i, b_i):
    """Replica a parte C1' de perfis_aresta: para cada contexto de memoria
    ALCANCADO m do receptor b, devolve d_m (perfil sobre intervencoes) e o
    rank_canonico (forma da ordem fraca)."""
    _, n, T, mods, s0 = cl.carregar(inst)
    orb = cl.orbita(T, s0)
    ext_b = cl.extractor(mods[b_i]["bits"], n)
    pop_b = cl.popcount_tab(len(mods[b_i]["bits"]))
    ints_a = cl.intervencoes(mods[a_i]["bits"])
    membits = mods[b_i]["bits_memoria"]
    emem = cl.extractor(membits, n)
    mem_reach = sorted({int(emem[z]) for z in orb})
    prof = {}
    for m_val in mem_reach:
        Z = cl.estados_da_fibra(n, membits, m_val)
        nxt0 = ext_b[T[Z]]
        d = []
        for (mk, vl) in ints_a:
            nxt = ext_b[T[(Z & ~np.int64(mk)) | np.int64(vl)]]
            d.append(int(pop_b[(nxt ^ nxt0)].sum()))
        prof[m_val] = {"d": d, "rank": cl.rank_canonico(d)}
    return mem_reach, prof


resumo = []
for iid, kk in sorted(chave.items()):
    if kk["variante"] != "II":
        continue
    inst = json.load(open(DST + "/conf-e2/instancias/%s.json" % iid))
    _, n, T, mods, s0 = cl.carregar(inst)
    tipos = pt._tipos_e2(kk)
    # indices dos processadores (tem memoria) e das arestas E_C que os alimentam
    res = cl.classificar(inst)
    proc = [i for i, m in enumerate(mods) if m["bits_memoria"]]
    arestas_proc = [(a, b) for (a, b) in res["E_C"] if b in proc]
    linhas = []
    algum_sinal = False
    for (a, b) in arestas_proc:
        mr, prof = edge_profiles(inst, a, b)
        ranks = [prof[m]["rank"] for m in mr]
        muda = len(set(ranks)) > 1
        if muda:
            algum_sinal = True
        linhas.append((tipos[a], tipos[b], mr, ranks, muda))
    resumo.append((iid, kk["familia"], algum_sinal, linhas))

print("=" * 78)
print("POST-CONFIRMATORY / EXPLORATORY  ---  Passo 3a: 25 II de E2")
print("mem_reach = contextos de memoria ALCANCADOS do receptor")
print("rank muda entre contextos alcancados?  SIM=sinal(individua)  NAO=estado(funde)")
print("=" * 78)
n_split = 0
for iid, fam, algum_sinal, linhas in resumo:
    flag = "  <<< FALHADA" if iid == FALHADA else ""
    veredicto = "SPLIT/II (>=1 aresta sinal)" if algum_sinal else "MERGE/III (todas estado)"
    if algum_sinal:
        n_split += 1
    print("\nfam %-3s id %s : %s%s" % (fam, iid, veredicto, flag))
    for (ta, tb, mr, ranks, muda) in linhas:
        print("    %s->%s  mem_reach=%s  ranks_por_contexto=%s  muda=%s"
              % (ta, tb, mr, ranks, "SIM" if muda else "nao"))

print("\n" + "=" * 78)
print("II que individuam (>=1 aresta sinal): %d / 25" % n_split)
print("II que fundem (todas estado, = III):  %d / 25" % (25 - n_split))
print("=" * 78)
