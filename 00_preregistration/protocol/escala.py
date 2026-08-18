# -*- coding: utf-8 -*-
"""
escala.py — Pré-registo A v8.3, item 10.1(4) e secção 7. Marco 5a.

Para cada instância confirmatória:
  1. enumera as projecções admissíveis por A1 exacto (constância nas fibras,
     secção 6.2), sobre todos os S com 2 <= |S| < n;
  2. para cada admissível, constrói o SISTEMA PROJECTADO: tabela quociente
     F_S(p(z)) := p(T[z]), bem definida por A1; módulos sobreviventes com
     bits reindexados; memória retida = memória ∩ S (revisão 8.1: o contexto
     também é projectado, e o colapso para {⊥} é permitido e testado);
     estado inicial projectado;
  3. classifica o projectado com o MESMO classificador congelado;
  4. verifica, por candidata: para todos os módulos sobreviventes Qi, Qj,
     mesma componente no projectado <=> mesma componente no micro
     (secção 7). Falha em qualquer instância = derrota da candidata no
     item 4 (secção 10.1).

COBERTURA POR ESTRATO: este executor corre nos DOIS estratos. No Estrato 1
aplica 10.1(4) a toda a projecção admissível que exista, sem exigir a
condição 6.4 (que é de construção do Estrato 2); no Estrato 2 aplica
10.1(4) e a validade 6.4. O benchmark sempre orçamentou A1 para ambos.

NOTA SOBRE MEIOS NOS SISTEMAS PROJECTADOS: o classificador devolve também
"meios" para os quocientes, calculados por rho, mas a secção 7 compara
EXCLUSIVAMENTE componentes, e este executor não interpreta nem pontua os
meios projectados. O certificado da emenda n.º 1, item 1a, está autorizado
para instâncias confirmatórias NÃO projectadas; a sua extensão aos
quocientes não é assumida aqui nem em lado nenhum.

Condição de validade (secção 6.4): |A| >= 2 COM granularidades distintas,
por instância do Estrato 2;
instância que não cumpra é registada como violação de construção.
"""

import itertools
import json
import hashlib
import numpy as np

import classificador as cl


def a1_admissivel(T, n, S):
    """Constância nas fibras para todas as intervenções sobre subconjuntos
    de S (secção 6.2). Vectorizado; saída antecipada na primeira violação."""
    proj = cl.extractor(S, n)
    estados = np.arange(1 << n, dtype=np.int64)
    for r in range(len(S) + 1):
        for J in itertools.combinations(S, r):
            mk = cl.mascara(J)
            for eta in range(1 << len(J)):
                vl = 0
                for i, b in enumerate(J):
                    vl |= ((eta >> i) & 1) << b
                z = (estados & ~np.int64(mk)) | np.int64(vl)
                seg = proj[T[z]]
                ref = np.empty(1 << len(S), dtype=np.int64)
                ref[proj] = seg
                if not np.array_equal(ref[proj], seg):
                    return False
    return True


def projectar_instancia(inst, S):
    """Sistema projectado sob alpha_S, pressupondo A1 verificado."""
    n = inst["n"]
    T = np.asarray(inst["transicao"], dtype=np.int64)
    S = sorted(S)
    novo_idx = {b: i for i, b in enumerate(S)}
    proj = cl.extractor(S, n)
    # representante de fibra: bits esquecidos a zero (constância garante
    # independência do representante)
    rep = np.zeros(1 << len(S), dtype=np.int64)
    for i, b in enumerate(S):
        rep |= ((np.arange(1 << len(S), dtype=np.int64) >> i) & 1) << b
    T_S = proj[T[rep]].tolist()
    mods_S = []
    for m in inst["modulos"]:
        bits = sorted(novo_idx[b] for b in m["bits"] if b in novo_idx)
        if not bits:
            continue                       # módulo não sobrevive
        mem = sorted(novo_idx[b] for b in m["bits_memoria"] if b in novo_idx)
        mods_S.append({"id": m["id"], "bits": bits, "bits_memoria": mem})
    s0 = int(proj[inst["estado_inicial"]])
    return {"id": inst["id"] + f"-S{''.join(map(str, S))}", "n": len(S),
            "modulos": mods_S, "estado_inicial": s0, "transicao": T_S}


def validade_6_4(admissiveis):
    """Secção 6.4: |A| >= 2 COM granularidades distintas."""
    return (len(admissiveis) >= 2
            and len({len(S) for S in admissiveis}) >= 2)


def testar_instancia(inst):
    n = inst["n"]
    T = np.asarray(inst["transicao"], dtype=np.int64)
    res_micro = cl.classificar(inst)
    ids_por_indice = [m["id"] for m in inst["modulos"]]

    admissiveis = [S for r in range(2, n)
                   for S in itertools.combinations(range(n), r)
                   if a1_admissivel(T, n, S)]
    saida = {"id": inst["id"], "n_admissiveis": len(admissiveis),
             # Audit trail: os S exactos preservam-se SEMPRE, não só nas
             # falhas. O diagnóstico do protocolo sobre as projecções
             # admissíveis seria irrecuperável a partir de contagens.
             "admissiveis": [sorted(S) for S in admissiveis],
             "granularidades_admissiveis": sorted({len(S) for S in admissiveis}),
             "projeccoes": [{"S": sorted(S),
                             "bits_removidos": sorted(set(range(n)) - set(S))}
                            for S in admissiveis],
             "validade_6_4": validade_6_4(admissiveis),
             # As 50 instâncias E2 são CONFIRMATÓRIAS: a classificação micro
             # é exportada para pontuação contra os alvos E2. Sem isto, uma
             # partição micro errada mas estável em todas as projecções
             # contaria como sucesso ("wrong but stable").
             "micro": {**{cand: {"componentes": res_micro[cand]["componentes"],
                                 "meios": res_micro[cand]["meios"]}
                          for cand in ("C1p", "C2", "C3")},
                       "E_C": res_micro["E_C"],
                       "arestas": res_micro["arestas"]},
             "falhas": {"C1p": [], "C2": [], "C3": []}}

    for S in admissiveis:
        inst_S = projectar_instancia(inst, S)
        sobreviventes = {m["id"] for m in inst_S["modulos"]}
        res_S = cl.classificar(inst_S)
        ids_S = [m["id"] for m in inst_S["modulos"]]
        for cand in ("C1p", "C2", "C3"):
            comp_micro = {}
            for ci, c in enumerate(res_micro[cand]["componentes"]):
                for m in c:
                    comp_micro[ids_por_indice[m]] = ci
            comp_S = {}
            for ci, c in enumerate(res_S[cand]["componentes"]):
                for m in c:
                    comp_S[ids_S[m]] = ci
            ok = all(
                (comp_S[a] == comp_S[b]) == (comp_micro[a] == comp_micro[b])
                for a in sobreviventes for b in sobreviventes)
            if not ok:
                saida["falhas"][cand].append(sorted(S))
    return saida


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
            r = testar_instancia(json.load(open(os.path.join(a.instancias, f))))
            todos[r["id"]] = r
    corpo = json.dumps(todos, sort_keys=True, indent=1).encode()
    open(a.saida, "wb").write(corpo)
    print("sha_escala:", hashlib.sha256(corpo).hexdigest())
