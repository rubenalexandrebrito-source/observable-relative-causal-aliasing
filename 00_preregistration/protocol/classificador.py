# -*- coding: utf-8 -*-
"""
classificador.py — Pré-registo A v8.3. Marco 3.

Função pura: instância cega (JSON do gerador) -> classificação.
NUNCA lê a chave. Implementa exclusivamente as definições congeladas:

  G_C   (secção 3): A->B em E_C sse existe intervenção sobre A, contexto
        ALCANÇÁVEL e alternativa intervencional com diferença no estado
        seguinte de B. Sem auto-arestas.
  I_A   (secção 5): do(J=eta), J subconjunto dos bits de A, incluindo a
        intervenção nula, que é o baseline de C1' e C2.
  Emparelhamento contrafactual (secção 5): z=(r,m); m ∈ M_B alcançáveis;
        r percorre TODAS as configurações dos restantes bits, as mesmas
        para m1 e m2.
  C1'   ordem fraca do perfil d_m(a) = soma_r HamB(Phi^a(r,m), Phi^0(r,m)),
        com preservação de empates.
  C2    ordem parcial por inclusão dos conjuntos I_m(b) de intervenções
        eficazes, incluindo igualdades.
  C3    canário analítico (derrotada na v8): invariância de suporte por
        pares de intervenções. Executa-se; se não falhar onde a derivação
        prevê, é erro de implementação.
  Meio  (secção 3, com emenda n.º 1, item 1a): SCC com >=2 módulos, ou
        singular com estado retido designado, rho(Q) não vazio; Rec é
        certificado pela elegibilidade (E3 e E5) antes da exportação e
        transportado por rho, NÃO re-inferido do efeito líquido da tabela,
        que no Sistema II pode conter cancelamento sigma/pi. Módulos sem
        memória têm Rec falso por definição.

Semântica intervencional transitória: substituir bits e aplicar UMA
transição global (a tabela da instância).
"""

import json
import hashlib
import itertools
import numpy as np


# ----------------------------------------------------------------------
def carregar(caminho_ou_dict):
    inst = (json.load(open(caminho_ou_dict))
            if isinstance(caminho_ou_dict, str) else caminho_ou_dict)
    n = inst["n"]
    T = np.asarray(inst["transicao"], dtype=np.int64)
    mods = inst["modulos"]
    return inst["id"], n, T, mods, int(inst["estado_inicial"])


def orbita(T, s0):
    vistos, ordem, s = set(), [], int(s0)
    while s not in vistos:
        vistos.add(s)
        ordem.append(s)
        s = int(T[s])
    return ordem


def mascara(bits):
    m = 0
    for b in bits:
        m |= (1 << b)
    return m


def intervencoes(bits):
    """I_A completo: (mascara, valor) para todo J ⊆ bits, eta ∈ {0,1}^|J|.
    Inclui (0,0), a intervenção nula. |I_A| = 3^|bits|."""
    out = []
    for r in range(len(bits) + 1):
        for J in itertools.combinations(bits, r):
            mJ = mascara(J)
            for eta in range(1 << len(J)):
                v = 0
                for i, b in enumerate(J):
                    v |= ((eta >> i) & 1) << b
                out.append((mJ, v))
    return out


def extractor(bits, n):
    """tab[z] = bits de 'bits' de z, compactados; vectorizável por indexação."""
    z = np.arange(1 << n, dtype=np.int64)
    e = np.zeros(1 << n, dtype=np.int64)
    for pos, b in enumerate(bits):
        e |= ((z >> b) & 1) << pos
    return e


def popcount_tab(k):
    v = np.arange(1 << k, dtype=np.int64)
    p = np.zeros(1 << k, dtype=np.int64)
    for i in range(k):
        p += (v >> i) & 1
    return p


def estados_da_fibra(n, mem_bits, m_val):
    """Todos os z com os bits de memória fixados em m_val: o eixo r,
    idêntico para todos os m (emparelhamento contrafactual)."""
    livres = [b for b in range(n) if b not in mem_bits]
    r = np.arange(1 << len(livres), dtype=np.int64)
    Z = np.zeros(1 << len(livres), dtype=np.int64)
    for pos, b in enumerate(livres):
        Z |= ((r >> pos) & 1) << b
    mv = 0
    for pos, b in enumerate(mem_bits):
        mv |= ((m_val >> pos) & 1) << b
    return Z | mv


def rank_canonico(valores):
    """Forma canónica da ordem fraca com empates: a cada posição, o número
    de valores distintos estritamente menores. Igualdade das formas
    canónicas <=> mesma ordem fraca com os mesmos empates."""
    ordenados = sorted(set(valores))
    idx = {v: i for i, v in enumerate(ordenados)}
    return tuple(idx[v] for v in valores)


# ----------------------------------------------------------------------
def classificar(caminho_ou_dict):
    iid, n, T, mods, s0 = carregar(caminho_ou_dict)
    orb = orbita(T, s0)
    orb_arr = np.asarray(orb, dtype=np.int64)
    nm = len(mods)
    ext = {i: extractor(m["bits"], n) for i, m in enumerate(mods)}
    pop = {i: popcount_tab(len(m["bits"])) for i, m in enumerate(mods)}
    ints = {i: intervencoes(m["bits"]) for i, m in enumerate(mods)}
    mem_reach = {}
    for i, m in enumerate(mods):
        if m["bits_memoria"]:
            emem = extractor(m["bits_memoria"], n)
            mem_reach[i] = sorted({int(emem[z]) for z in orb})
        else:
            mem_reach[i] = [None]        # conjunto contextual singular {⊥}

    # --- G_C: contexto alcançável, alternativa contra a intervenção nula ---
    EC = []
    for a_i in range(nm):
        for b_i in range(nm):
            if a_i == b_i:
                continue
            eB = ext[b_i]
            base = eB[T[orb_arr]]
            achou = False
            for (mk, vl) in ints[a_i]:
                if mk == 0:
                    continue
                alt = eB[T[(orb_arr & ~np.int64(mk)) | np.int64(vl)]]
                if not np.array_equal(alt, base):
                    achou = True
                    break
            if achou:
                EC.append((a_i, b_i))

    # --- classificação de arestas de E_C pelas três candidatas ---
    def perfis_aresta(a_i, b_i):
        eB, popB = ext[b_i], pop[b_i]
        membits = mods[b_i]["bits_memoria"]
        dados = {}
        for m_val in mem_reach[b_i]:
            Z = (estados_da_fibra(n, membits, m_val) if m_val is not None
                 else np.arange(1 << n, dtype=np.int64))
            nxt0 = eB[T[Z]]
            d, efic, supp_assin = [], [], []
            for (mk, vl) in ints[a_i]:
                nxt = eB[T[(Z & ~np.int64(mk)) | np.int64(vl)]]
                xr = nxt ^ nxt0
                d.append(int(popB[xr].sum()))
                efic.append(int(xr.max()) if xr.size else 0)  # placeholder
                # eficácia por bit de B (C2) e assinatura por bit (C3):
                efic[-1] = tuple(bool(np.any((xr >> k) & 1))
                                 for k in range(len(mods[b_i]["bits"])))
                # igualdade EXACTA dos vectores de bits (sem hash: uma
                # experiência exacta não admite aproximação probabilística)
                supp_assin.append(tuple(
                    ((nxt >> k) & 1).astype(np.uint8).tobytes()
                    for k in range(len(mods[b_i]["bits"]))))
            dados[m_val] = {"d": d, "efic": efic, "assin": supp_assin}
        return dados

    def c1_estado(dados):
        formas = [rank_canonico(v["d"]) for v in dados.values()]
        return all(f == formas[0] for f in formas)

    def c2_estado(dados):
        # I_m(b) por bit; ordem parcial por inclusão com igualdades.
        def relacao(v):
            nb = len(v["efic"][0])
            conj = [frozenset(ai for ai, e in enumerate(v["efic"]) if e[k])
                    for k in range(nb)]
            return tuple((conj[i] <= conj[j], conj[i] == conj[j])
                         for i in range(nb) for j in range(nb))
        rels = [relacao(v) for v in dados.values()]
        return all(r == rels[0] for r in rels)

    def c3_estado(dados):
        # Supp(T^m) = bits com >1 assinatura distinta entre intervenções.
        def supp(v):
            nb = len(v["assin"][0])
            return frozenset(k for k in range(nb)
                             if len({a[k] for a in v["assin"]}) > 1)
        ss = [supp(v) for v in dados.values()]
        return all(s == ss[0] for s in ss)

    classif = {}
    for (a_i, b_i) in EC:
        dados = perfis_aresta(a_i, b_i)
        classif[(a_i, b_i)] = {
            "C1p": "estado" if c1_estado(dados) else "sinal",
            "C2":  "estado" if c2_estado(dados) else "sinal",
            "C3":  "estado" if c3_estado(dados) else "sinal",
        }

    # --- G_S, SCC e meios por candidata ---
    def scc(arestas):
        alcanca = [set([i]) for i in range(nm)]
        mudou = True
        while mudou:
            mudou = False
            for (u, v) in arestas:
                novo = alcanca[u] | alcanca[v]
                if novo != alcanca[u]:
                    alcanca[u] = novo
                    mudou = True
                for w in range(nm):
                    if u in alcanca[w] and not alcanca[u] <= alcanca[w]:
                        alcanca[w] |= alcanca[u]
                        mudou = True
        comp = {}
        for i in range(nm):
            chave_c = frozenset(j for j in range(nm)
                                if j in alcanca[i] and i in alcanca[j])
            comp.setdefault(chave_c, set()).add(i)
        return sorted((sorted(c) for c in comp), key=lambda c: c[0])

    resultado = {"id": iid, "n": n, "n_modulos": nm,
                 "orbita": len(orb),
                 "E_C": sorted(EC),
                 "arestas": {f"{a}->{b}": v for (a, b), v in sorted(classif.items())}}
    for cand in ("C1p", "C2", "C3"):
        ES = [e for e in EC if classif[e][cand] == "estado"]
        comps = scc(ES)
        laco = {i: False for i in range(nm)}      # sem auto-arestas em G_S
        meios = []
        for c in comps:
            if len(c) >= 2:
                meios.append(c)
            elif mods[c[0]]["bits_memoria"]:
                # Emenda n.º 1, item 1a: nas instâncias aceites, Rec é
                # certificado por E3 E E5 antes da exportação (E3 dá
                # x~>m, E5 dá m~>x via eficácia de sigma) e equivale a
                # rho(Q) não vazio. Re-inferir Rec do efeito líquido da
                # memória na tabela global seria ERRADO no Sistema II, onde
                # sigma e pi_m podem cancelar-se: o efeito líquido nulo não
                # nega a translação interna. Canais e jusante: rho vazio.
                meios.append(c)
        resultado[cand] = {"E_S": sorted(ES), "componentes": comps,
                           "meios": sorted(meios)}
    return resultado


def sha_resultado(res) -> str:
    return hashlib.sha256(
        json.dumps(res, sort_keys=True, separators=(",", ":"), default=str)
        .encode()).hexdigest()


if __name__ == "__main__":
    import argparse, os
    ap = argparse.ArgumentParser()
    ap.add_argument("--instancias", type=str, required=True)
    ap.add_argument("--saida", type=str, required=True)
    a = ap.parse_args()
    if os.path.exists(a.saida):
        raise FileExistsError(a.saida)
    todos = {}
    for f in sorted(os.listdir(a.instancias)):
        if f.endswith(".json"):
            r = classificar(os.path.join(a.instancias, f))
            todos[r["id"]] = r
    corpo = json.dumps(todos, sort_keys=True, indent=1, default=str).encode()
    with open(a.saida, "wb") as fp:
        fp.write(corpo)
    print("sha_classificacoes:", hashlib.sha256(corpo).hexdigest())
