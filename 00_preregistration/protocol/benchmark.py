# -*- coding: utf-8 -*-
"""
benchmark.py — Pré-registo A v8.3, secção 11.0. Marco 2.

Mede o custo real (comparações, avaliações de estado, memória, tempo) da
enumeração de projecções (secção 6.3) e da verificação exacta de A1 por
constância nas fibras (secção 6.2), para n em {6, 8, 10, 11, 12}.

6, 10 e 12 são as dimensões realmente utilizadas: medem-se sobre instâncias
geradas pelo gerador congelado com semente descartável. 8 e 11 servem apenas
para caracterizar a curva: medem-se sobre tabelas de transição uniformes
sintéticas, porque não existem sistemas do protocolo nessas dimensões.

NESTA FASE NÃO SE EXECUTA NENHUMA CANDIDATA E NÃO SE OBSERVA NENHUMA
CLASSIFICAÇÃO (secção 11.0). O único produto é a curva de custo que alimenta
a decisão de viabilidade da secção 2. Este ficheiro corre na máquina
registada; execuções noutras máquinas são fumo de engenharia.

Semântica das intervenções: transitória (secção 6.2 / A1): substituem-se os
bits intervencionados no estado corrente e aplica-se UMA transição global.
A1 por constância nas fibras: p_S(z) = p_S(z') => p_S(Phi^i(z)) = p_S(Phi^i(z')).
"""

import argparse
import itertools
import json
import time
import tracemalloc
import hashlib
import numpy as np

import gerador as g

SEMENTE_DESCARTAVEL = 900_000_001   # nunca usada em desenvolvimento nem confirmação
DIMENSOES = (6, 8, 10, 11, 12)


# ----------------------------------------------------------------------
# Tabelas de transição (arrays numpy) para as três origens de sistemas
# ----------------------------------------------------------------------

def tabela_do_gerador(n: int) -> np.ndarray:
    """Instância real do protocolo com semente descartável: n=6 (variante I),
    n=10 (variante II), n=12 (Estrato 2, variante II)."""
    if n == 6:
        _, _, _, fams = g.gerar_lote(SEMENTE_DESCARTAVEL, 1, False)
        tab, nn, _ = g.tabela_transicao("I", fams[0][0], False)
    elif n == 10:
        _, _, _, fams = g.gerar_lote(SEMENTE_DESCARTAVEL, 1, False)
        tab, nn, _ = g.tabela_transicao("II", fams[0][0], False)
    elif n == 12:
        _, _, _, fams = g.gerar_lote(SEMENTE_DESCARTAVEL, 1, True)
        tab, nn, _ = g.tabela_transicao("II", fams[0][0], True)
    else:
        raise ValueError(n)
    assert nn == n
    return np.asarray(tab, dtype=np.int64)

def tabela_sintetica(n: int) -> np.ndarray:
    """Só para n em {8, 11}: dinâmica uniforme sintética, curva de custo."""
    rng = np.random.Generator(np.random.PCG64(
        np.random.SeedSequence([SEMENTE_DESCARTAVEL, n])))
    return rng.integers(0, 1 << n, size=1 << n, dtype=np.int64)

def obter_tabela(n: int) -> tuple:
    if n in (6, 10, 12):
        return tabela_do_gerador(n), "gerador"
    return tabela_sintetica(n), "sintetica_curva"


# ----------------------------------------------------------------------
# A1 por constância nas fibras, vectorizado, com contadores exactos
# ----------------------------------------------------------------------

def projector(n: int, S: tuple) -> np.ndarray:
    """proj_tab[z] = inteiro com os bits de S de z, compactados por ordem de S."""
    estados = np.arange(1 << n, dtype=np.int64)
    p = np.zeros(1 << n, dtype=np.int64)
    for pos, b in enumerate(S):
        p |= ((estados >> b) & 1) << pos
    return p

def a1_para_projeccao(T: np.ndarray, n: int, S: tuple, contadores: dict) -> bool:
    """Verificação exaustiva de A1 para a projecção S.
    Intervenções admissíveis: do(J = eta), J subconjunto de S (incl. vazio),
    eta em {0,1}^|J|; total 3^|S| (secção 5, domínio; secção 6.2, A1)."""
    proj = projector(n, S)
    k = len(S)
    n_fibras = 1 << k
    estados = np.arange(1 << n, dtype=np.int64)
    ok = True
    for J in itertools.chain.from_iterable(
            itertools.combinations(S, r) for r in range(k + 1)):
        mascara = 0
        for b in J:
            mascara |= (1 << b)
        vals_bits = [sum(((eta >> i) & 1) << b for i, b in enumerate(J))
                     for eta in range(1 << len(J))]
        base = estados & ~np.int64(mascara)
        for vb in vals_bits:
            z_i = base | np.int64(vb)              # substituição transitória
            proj_seg = proj[T[z_i]]                 # p_S(Phi^i(z))
            # constância nas fibras: última atribuição + comparação vectorizada
            ref = np.empty(n_fibras, dtype=np.int64)
            ref[proj] = proj_seg
            contadores["comparacoes"] += int(estados.size)
            contadores["avaliacoes_estado"] += int(estados.size)
            contadores["intervencoes"] += 1
            if not np.array_equal(ref[proj], proj_seg):
                ok = False
                # continua a contagem? Não: o custo real de uma execução pára
                # na primeira violação; o benchmark mede o custo real.
                return False
    return ok

def medir_dimensao(n: int, max_projeccoes: int | None) -> dict:
    T, origem = obter_tabela(n)
    S_todos = [tuple(c) for r in range(2, n)
               for c in itertools.combinations(range(n), r)]
    total_S = len(S_todos)                          # = 2^n - n - 2
    if max_projeccoes is not None:
        S_exec = S_todos[:max_projeccoes]
    else:
        S_exec = S_todos
    contadores = {"comparacoes": 0, "avaliacoes_estado": 0, "intervencoes": 0}
    tracemalloc.start()
    t0 = time.perf_counter()
    admissiveis = 0
    for S in S_exec:
        if a1_para_projeccao(T, n, S, contadores):
            admissiveis += 1
    dt = time.perf_counter() - t0
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # Totais analíticos exactos do workload completo (secção 11.0 exige o
    # número real; quando max_projeccoes trunca, o real do subconjunto é o
    # contado e o total analítico é o majorante do completo sem violações):
    interv_total = sum(3 ** len(S) for S in S_todos)
    return {
        "n": n,
        "origem_sistema": origem,
        "projeccoes_total": total_S,
        "projeccoes_executadas": len(S_exec),
        "projeccoes_admissiveis_no_executado": admissiveis,
        "contadores_reais": contadores,
        "intervencoes_workload_completo_analitico": interv_total,
        "avaliacoes_estado_workload_completo_analitico": interv_total * (1 << n),
        "segundos": dt,
        "segundos_por_intervencao": dt / max(contadores["intervencoes"], 1),
        "pico_memoria_bytes": pico,
        "bytes_tabela_transicao": int(T.nbytes),
    }


# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", type=str, required=True)
    ap.add_argument("--max-projeccoes", type=int, default=None,
                    help="truncar por dimensão (APENAS fumo de engenharia; "
                         "o benchmark oficial corre completo na máquina registada)")
    ap.add_argument("--dimensoes", type=int, nargs="*", default=list(DIMENSOES))
    a = ap.parse_args()

    resultados = []
    for n in a.dimensoes:
        r = medir_dimensao(n, a.max_projeccoes)
        resultados.append(r)
        print(f"n={n}: {r['projeccoes_executadas']}/{r['projeccoes_total']} projeccoes, "
              f"{r['contadores_reais']['intervencoes']} intervencoes reais, "
              f"{r['segundos']:.2f}s, "
              f"{r['segundos_por_intervencao']*1e6:.1f} us/intervencao")

    # Estimativa para a decisão de viabilidade da secção 2 (só a componente
    # A1+enumeração; o pipeline completo é objecto do dry run 11.1a):
    taxa = {r["n"]: r["segundos_por_intervencao"] for r in resultados}
    est = {}
    if 6 in taxa and 10 in taxa and 12 in taxa:
        est["estrato1_A1_horas"] = (
            50 * sum(3 ** len(S) for S in
                     (tuple(c) for r_ in range(2, 6)
                      for c in itertools.combinations(range(6), r_))) * taxa[6]
            + 100 * sum(3 ** len(S) for S in
                        (tuple(c) for r_ in range(2, 10)
                         for c in itertools.combinations(range(10), r_))) * taxa[10]
        ) / 3600.0
        est["estrato2_A1_horas"] = (
            50 * sum(3 ** len(S) for S in
                     (tuple(c) for r_ in range(2, 12)
                      for c in itertools.combinations(range(12), r_))) * taxa[12]
        ) / 3600.0
        est["nota"] = ("Estimativa da componente A1+enumeracao apenas, por "
                       "extrapolacao linear da taxa medida; orcamento de 72h "
                       "avalia o workload completo no dry run 11.1a.")

    saida = {
        "seccao_protocolo": "11.0",
        "semente_descartavel": SEMENTE_DESCARTAVEL,
        "resultados": resultados,
        "estimativa_confirmatoria": est,
        "declaracao": ("Nenhuma candidata executada; nenhuma classificacao "
                       "observada; sistemas descartaveis nunca reutilizados."),
    }
    corpo = json.dumps(saida, sort_keys=True, indent=1).encode()
    with open(a.saida, "wb") as f:
        f.write(corpo)
    print("sha_benchmark:", hashlib.sha256(corpo).hexdigest())

if __name__ == "__main__":
    main()
