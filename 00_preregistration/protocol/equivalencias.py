# -*- coding: utf-8 -*-
"""
equivalencias.py — Pré-registo A v8.3, item 10.1(6). Marco 4.

Grupo congelado: isomorfismos que preservam a estrutura modular, a
designação dos bits de memória e a álgebra das intervenções atómicas:
  (i)   renomeação de módulos do MESMO tipo e dimensão (mesma contagem de
        bits e de bits de memória);
  (ii)  permutação de coordenadas dentro de cada sub-vector, respeitando a
        designação (memória -> memória, não-memória -> não-memória);
  (iii) inversão independente 0<->1 de coordenadas;
com conjugação de tabela de transição, intervenções e CONDIÇÕES INICIAIS
(revisão 8.1: sem conjugar o estado inicial, órbitas divergiriam por
acidente de representação).

Não se inclui S_{2^d}: uma bijecção arbitrária de estados destruiria as
intervenções coordenadas, que é o mecanismo de remapeamento do Sistema II.

Confirmação: enumeração EXAUSTIVA. Desenvolvimento: --amostra permite
subamostragem uniforme para fumo, declarada como tal.
"""

import argparse
import itertools
import json
import hashlib
import numpy as np

import classificador as cl


# ----------------------------------------------------------------------
def formas_dos_modulos(mods):
    """Assinatura de forma: (n_bits, n_bits_memoria)."""
    return [(len(m["bits"]), len(m["bits_memoria"])) for m in mods]


def renomeacoes(mods):
    """Todas as permutações de módulos dentro de cada classe de forma."""
    formas = formas_dos_modulos(mods)
    classes = {}
    for i, f in enumerate(formas):
        classes.setdefault(f, []).append(i)
    listas = []
    for f, idxs in sorted(classes.items()):
        listas.append([dict(zip(idxs, p))
                       for p in itertools.permutations(idxs)])
    for combo in itertools.product(*listas):
        sigma = {}
        for d in combo:
            sigma.update(d)
        yield sigma


def permutacoes_internas(mods):
    """Para cada módulo, permutações (memória entre si, resto entre si).
    Devolve gerador de tuplos: um par (perm_mem, perm_out) por módulo."""
    por_mod = []
    for m in mods:
        mem = m["bits_memoria"]
        out = [b for b in m["bits"] if b not in mem]
        por_mod.append([
            (pm, po)
            for pm in itertools.permutations(range(len(mem)))
            for po in itertools.permutations(range(len(out)))
        ])
    return itertools.product(*por_mod)


def bijeccao_de_bits(mods, sigma, internas):
    """Constrói p: posição_origem -> posição_destino. O módulo i vai para
    sigma[i]; dentro, memória->memória e resto->resto pelas permutações."""
    n = sum(len(m["bits"]) for m in mods)
    p = [None] * n
    for i, m in enumerate(mods):
        alvo = mods[sigma[i]]
        mem_o = m["bits_memoria"]
        out_o = [b for b in m["bits"] if b not in mem_o]
        mem_d = alvo["bits_memoria"]
        out_d = [b for b in alvo["bits"] if b not in mem_d]
        pm, po = internas[i]
        for k, b in enumerate(mem_o):
            p[b] = mem_d[pm[k]]
        for k, b in enumerate(out_o):
            p[b] = out_d[po[k]]
    return p


def aplicar_phi(v, p, flips, n):
    out = 0
    for i in range(n):
        out |= ((v >> i) & 1) << p[i]
    return out ^ flips


def transformar_instancia(inst, p, flips):
    """Instância conjugada: T' = phi . T . phi^{-1}; s0' = phi(s0).
    Os descritores de módulos ficam FIXOS (posições), a dinâmica muda."""
    n = inst["n"]
    T = inst["transicao"]
    inv = [0] * n
    for i, pi in enumerate(p):
        inv[pi] = i
    def phi(v):
        return aplicar_phi(v, p, flips, n)
    def phi_inv(v):
        return aplicar_phi(v ^ flips, inv, 0, n)
    T2 = [0] * len(T)
    for s in range(len(T)):
        T2[s] = phi(T[phi_inv(s)])
    return {"id": inst["id"] + "-eq", "n": n, "modulos": inst["modulos"],
            "estado_inicial": phi(inst["estado_inicial"]), "transicao": T2}


def comparar(res_o, res_t, sigma):
    """Discrepâncias POR CANDIDATA (10.1: a derrota é por candidata; uma
    falha de invariância de C2 não pode derrubar C1'). E_C é estrutural e
    ANTERIOR às candidatas: uma discrepância em E_C devolve BASE e é
    tratada na pontuação como falha do instrumento, com anulação por
    integridade, nunca como derrota de candidata (emenda n.º 1, item 3)."""
    falhas = {"C1p": None, "C2": None, "C3": None}
    ec_o = {(sigma[a], sigma[b]) for (a, b) in res_o["E_C"]}
    ec_t = {tuple(e) for e in res_t["E_C"]}
    if ec_o != ec_t:
        # G_C é ANTERIOR às candidatas: a sua invariância decorre da
        # definição intervencional. Discrepância aqui = falha do instrumento,
        # a tratar por ANULAÇÃO na pontuação, nunca como derrota de candidata.
        return "BASE"
    for cand in ("C1p", "C2", "C3"):
        rot_o = {(sigma[int(k.split("->")[0])], sigma[int(k.split("->")[1])]):
                 v[cand] for k, v in res_o["arestas"].items()}
        rot_t = {(int(k.split("->")[0]), int(k.split("->")[1])): v[cand]
                 for k, v in res_t["arestas"].items()}
        if rot_o != rot_t:
            falhas[cand] = "arestas"
            continue
        c_o = {frozenset(sigma[m] for m in c) for c in res_o[cand]["componentes"]}
        c_t = {frozenset(c) for c in res_t[cand]["componentes"]}
        if c_o != c_t:
            falhas[cand] = "componentes"
            continue
        m_o = {frozenset(sigma[m] for m in c) for c in res_o[cand]["meios"]}
        m_t = {frozenset(c) for c in res_t[cand]["meios"]}
        if m_o != m_t:
            falhas[cand] = "meios"
    return falhas


def testar_instancia(inst, amostra=None, semente_amostra=0):
    """Enumera o grupo (exaustivo, ou amostra uniforme para fumo) e devolve
    (n_testados, discrepâncias)."""
    n = inst["n"]
    mods = inst["modulos"]
    res_o = cl.classificar(inst)
    elementos = []
    for sigma in renomeacoes(mods):
        for internas in permutacoes_internas(mods):
            p = bijeccao_de_bits(mods, sigma, internas)
            elementos.append((sigma, p))
    total = len(elementos) * (1 << n)
    rng = np.random.Generator(np.random.PCG64(semente_amostra))
    if amostra is None:
        universo = ((e, f) for e in elementos for f in range(1 << n))
        n_exec = total
    else:
        n_exec = min(amostra, total)
        pares = rng.choice(total, size=n_exec, replace=False)
        universo = ((elementos[int(x) // (1 << n)], int(x) % (1 << n))
                    for x in pares)
    # Sem break: a enumeração é EXAUSTIVA mesmo com discrepâncias (P0.5).
    # Contam-se todas; guardam-se no máximo 5 testemunhos por candidata.
    n_disc = {"C1p": 0, "C2": 0, "C3": 0}
    n_base = 0
    exemplos = {"C1p": [], "C2": [], "C3": [], "BASE": []}
    executados = 0
    for (sigma, p), flips in universo:
        executados += 1
        inst2 = transformar_instancia(inst, p, flips)
        res_t = cl.classificar(inst2)
        falhas = comparar(res_o, res_t, sigma)
        if falhas == "BASE":
            n_base += 1
            if len(exemplos["BASE"]) < 5:
                exemplos["BASE"].append({"sigma": sigma, "p": p, "flips": flips})
            continue
        for cand, tipo in falhas.items():
            if tipo is not None:
                n_disc[cand] += 1
                if len(exemplos[cand]) < 5:
                    exemplos[cand].append({"sigma": sigma, "p": p,
                                           "flips": flips, "tipo": tipo})
    return {"grupo_total": total, "testados": executados,
            "discrepancias_base": n_base,
            "discrepancias": n_disc, "exemplos": exemplos}


def correr_lote(directorios, saida, amostra=None, semente_amostra=0):
    """Agregador determinístico: um ou mais directórios -> UM JSON.
    Erro em ID repetido: a fusão E1+E2 é uma função, não uma operação
    humana. Confirmação: amostra=None (exaustivo)."""
    import os
    if isinstance(directorios, str):
        directorios = [directorios]
    if os.path.exists(saida):
        raise FileExistsError(saida)
    agregado = {}
    for directorio in directorios:
        for f in sorted(os.listdir(directorio)):
            if f.endswith(".json"):
                inst = json.load(open(os.path.join(directorio, f)))
                if inst["id"] in agregado:
                    raise ValueError(f"ID repetido entre lotes: {inst['id']}")
                agregado[inst["id"]] = testar_instancia(
                    inst, amostra, semente_amostra)
    corpo = json.dumps(agregado, sort_keys=True, indent=1, default=str).encode()
    open(saida, "wb").write(corpo)
    return hashlib.sha256(corpo).hexdigest()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--instancia", type=str, default=None)
    ap.add_argument("--instancias", type=str, action="append", default=None,
                    help="directório (repetível): modo lote, agrega num JSON")
    ap.add_argument("--saida", type=str, default=None)
    ap.add_argument("--amostra", type=int, default=None,
                    help="APENAS fumo de desenvolvimento; confirmação = exaustivo")
    ap.add_argument("--semente-amostra", type=int, default=0)
    a = ap.parse_args()
    if a.instancias:
        sha = correr_lote(a.instancias, a.saida, a.amostra, a.semente_amostra)
        print("sha_equivalencias:", sha)
        raise SystemExit(0)
    inst = json.load(open(a.instancia))
    r = testar_instancia(inst, a.amostra, a.semente_amostra)
    print(json.dumps({"id": inst["id"], "grupo_total": r["grupo_total"],
          "testados": r["testados"], "discrepancias": r["discrepancias"],
          "sha": hashlib.sha256(json.dumps(r, sort_keys=True, default=str)
                                .encode()).hexdigest()}, indent=1))
