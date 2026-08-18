# -*- coding: utf-8 -*-
"""
pontuacao.py — Pré-registo A v8.3, secções 10.1 a 10.3. Marco 5b, revisto
pela auditoria (P0.1, P0.2, P0.3, P0.6).

ORDEM DE AVALIAÇÃO, congelada:
  0. AUDITORIA DE INTEGRIDADE: cardinalidades exactas (Estrato 1:
     150 = 50 I + 50 II + 50 III; Estrato 2: 50 = 25 II + 25 III),
     conjuntos de IDs coincidentes com as chaves, equivalências sobre
     E1 ∪ E2 com testados == grupo_total em TODAS as instâncias.
     Violação -> ANULAR_EXECUCAO_INTEGRIDADE (procedimental, não científico).
  1. VALIDADE 6.4 em todas as instâncias E2 -> senão,
     ANULAR_EXECUCAO_ESTRATO2_INVALIDO (a construção falhou, não a candidata).
  2. CANÁRIO ESPECÍFICO (derivação v8): nas 75 instâncias II confirmatórias,
     50 do Estrato 1 e 25 do Estrato 2, as arestas C_AB->B e C_BA->A
     existem em E_C e C3 = estado.
     Aresta ausente ou sinal -> ANULAR_EXECUCAO_CANARIO (erro de implementação).
  3. Só então: itens 10.1 por candidata, com equivalências POR CANDIDATA.
"""

import json
import hashlib

CANON = {"I": ["A", "B"], "II": ["A", "B", "C_AB", "C_BA"],
         "III": ["A", "B", "C_AB", "C_BA"],
         "II_E2": ["A", "B", "C_AB", "C_BA", "D1", "D2"],
         "III_E2": ["A", "B", "C_AB", "C_BA", "D1", "D2"]}

ALVOS_E2 = {
    "II":  {"comps": {frozenset({"A"}), frozenset({"B"}),
                      frozenset({"C_AB"}), frozenset({"C_BA"}),
                      frozenset({"D1"}), frozenset({"D2"})},
            "meios": {frozenset({"A"}), frozenset({"B"})}},
    "III": {"comps": {frozenset({"A", "B", "C_AB", "C_BA"}),
                      frozenset({"D1"}), frozenset({"D2"})},
            "meios": {frozenset({"A", "B", "C_AB", "C_BA"})}},
}

ALVOS = {
    "I":   {"comps": {frozenset({"A", "B"})},
            "meios": {frozenset({"A", "B"})}},
    "III": {"comps": {frozenset({"A", "B", "C_AB", "C_BA"})},
            "meios": {frozenset({"A", "B", "C_AB", "C_BA"})}},
    "II":  {"comps": {frozenset({"A"}), frozenset({"B"}),
                      frozenset({"C_AB"}), frozenset({"C_BA"})},
            "meios": {frozenset({"A"}), frozenset({"B"})}},
}

ESPERADO_E1 = {"I": 50, "II": 50, "III": 50}
ESPERADO_E2 = {"II": 25, "III": 25}
GRUPOS_ESPERADOS = {("E1", "I"): 512, ("E1", "II"): 65536,
                    ("E1", "III"): 65536,
                    ("E2", "II"): 524288, ("E2", "III"): 524288}


def _tipos(k, variante):
    return [CANON[variante][j] for j in k["ordem_modulos"]]


def _tipos_e2(k):
    canon = ["A", "B", "C_AB", "C_BA", "D1", "D2"]
    return [canon[j] for j in k["ordem_modulos"]]


def _auditoria(classif, escala, equiv, chave_e1, chave_e2,
               esperado_e1, esperado_e2, grupos_esperados):
    v = []
    ids_e1, ids_e2 = set(chave_e1), set(chave_e2)
    if ids_e1 & ids_e2:
        v.append("colisão de IDs entre E1 e E2")
    if len(ids_e1) != sum(esperado_e1.values()):
        v.append(f"Estrato 1: {len(ids_e1)} instâncias, "
                 f"esperado {sum(esperado_e1.values())}")
    if len(ids_e2) != sum(esperado_e2.values()):
        v.append(f"Estrato 2: {len(ids_e2)} instâncias, "
                 f"esperado {sum(esperado_e2.values())}")
    for iid, k in chave_e1.items():
        if k["variante"] not in esperado_e1:
            v.append(f"variante desconhecida no Estrato 1: {k['variante']}")
            break
    for iid, k in chave_e2.items():
        if k["variante"] not in esperado_e2:
            v.append(f"variante desconhecida no Estrato 2: {k['variante']}")
            break
    if set(classif) != ids_e1:
        v.append("IDs de classificações != chave E1")
    if set(escala) != ids_e2:
        v.append("IDs de escala != chave E2")
    if set(equiv) != ids_e1 | ids_e2:
        v.append("IDs de equivalências != E1 ∪ E2")
    for var, n_esp in esperado_e1.items():
        n = sum(1 for k in chave_e1.values() if k["variante"] == var)
        if n != n_esp:
            v.append(f"Estrato 1: {var} tem {n}, esperado {n_esp}")
    for var, n_esp in esperado_e2.items():
        n = sum(1 for k in chave_e2.values() if k["variante"] == var)
        if n != n_esp:
            v.append(f"Estrato 2: {var} tem {n}, esperado {n_esp}")
    for iid, r in equiv.items():
        estrato = "E1" if iid in ids_e1 else "E2"
        var = (chave_e1 if estrato == "E1" else chave_e2).get(iid, {}).get("variante")
        esp = grupos_esperados.get((estrato, var))
        if esp is not None and r.get("grupo_total") != esp:
            v.append(f"grupo_total inesperado em {iid}: "
                     f"{r.get('grupo_total')} != {esp}")
        if r.get("testados") != r.get("grupo_total"):
            v.append(f"equivalências incompletas em {iid}: "
                     f"{r.get('testados')}/{r.get('grupo_total')}")
        if r.get("discrepancias_base", 0) != 0:
            v.append(f"discrepância de G_C sob conjugação em {iid}: "
                     "falha do instrumento, não das candidatas")
    return v


def _canario(classif, chave_e1, escala_e2, chave_e2):
    """C3(C_AB->B) = estado E C3(C_BA->A) = estado em TODAS as instâncias II
    confirmatórias: 50 do Estrato 1 + 25 do Estrato 2 = 75. A derivação da
    v8 não deixa de valer com D1, D2 presentes; um erro dependente de n=12
    tem de disparar o canário, não passar despercebido."""
    falhas = []
    def verificar(iid, tipos, arestas):
        idx = {t: i for i, t in enumerate(tipos)}
        for (a, b) in ((idx["C_AB"], idx["B"]), (idx["C_BA"], idx["A"])):
            aresta = f"{a}->{b}"
            if aresta not in arestas:
                falhas.append({"id": iid, "aresta": aresta, "tipo": "ausente"})
            elif arestas[aresta]["C3"] != "estado":
                falhas.append({"id": iid, "aresta": aresta, "tipo": "sinal"})
    for iid, k in chave_e1.items():
        if k["variante"] == "II":
            verificar(iid, _tipos(k, "II"), classif[iid]["arestas"])
    for iid, k in chave_e2.items():
        if k["variante"] == "II":
            verificar(iid, _tipos_e2(k), escala_e2[iid]["micro"]["arestas"])
    return falhas


def pontuar(classif_path, escala_e1_path, escala_e2_path, equiv_path,
            chave_e1_path, chave_e2_path, esperado_e1=None, esperado_e2=None,
            grupos_esperados=None):
    classif = json.load(open(classif_path))
    escala_e1 = json.load(open(escala_e1_path))
    escala = json.load(open(escala_e2_path))
    equiv = json.load(open(equiv_path))
    chave_e1 = json.load(open(chave_e1_path))
    chave_e2 = json.load(open(chave_e2_path))
    esperado_e1 = esperado_e1 or ESPERADO_E1
    esperado_e2 = esperado_e2 or ESPERADO_E2
    grupos_esperados = grupos_esperados or GRUPOS_ESPERADOS

    # 0. integridade
    viol = _auditoria(classif, escala, equiv, chave_e1, chave_e2,
                      esperado_e1, esperado_e2, grupos_esperados)
    if set(escala_e1) != set(chave_e1):
        viol.append("IDs de escala E1 != chave E1")
    if viol:
        return {"resultado_confirmatorio_A": "ANULAR_EXECUCAO_INTEGRIDADE",
                "violacoes": viol}

    # 1. validade 6.4: exigida APENAS no Estrato 2, cuja construção a
    # garante; no Estrato 1 a existência de projecções não é prometida.
    invalidas = [iid for iid, r in escala.items() if not r["validade_6_4"]]
    if invalidas:
        return {"resultado_confirmatorio_A": "ANULAR_EXECUCAO_ESTRATO2_INVALIDO",
                "instancias": invalidas}

    # 2. canário específico, nos 75 II confirmatórios
    fc = _canario(classif, chave_e1, escala, chave_e2)
    if fc:
        return {"resultado_confirmatorio_A": "ANULAR_EXECUCAO_CANARIO",
                "falhas_canario": fc}

    # 3. itens por candidata: as 200 instâncias confirmatórias (150 E1 +
    # 50 E2 micro) contam TODAS para a totalidade. Estabilidade de uma
    # resposta errada não é sucesso.
    veredicto = {}
    for cand in ("C1p", "C2", "C3"):
        ac_e1, err_e1 = 0, []
        for iid, res in classif.items():
            k = chave_e1[iid]
            var = k["variante"]
            tipos = _tipos(k, var)
            comps = {frozenset(tipos[m] for m in c)
                     for c in res[cand]["componentes"]}
            meios = {frozenset(tipos[m] for m in c)
                     for c in res[cand]["meios"]}
            if comps == ALVOS[var]["comps"] and meios == ALVOS[var]["meios"]:
                ac_e1 += 1
            else:
                err_e1.append({"id": iid, "variante": var})
        ac_e2, err_e2 = 0, []
        for iid, r in escala.items():
            k = chave_e2[iid]
            var = k["variante"]
            tipos = _tipos_e2(k)
            comps = {frozenset(tipos[m] for m in c)
                     for c in r["micro"][cand]["componentes"]}
            meios = {frozenset(tipos[m] for m in c)
                     for c in r["micro"][cand]["meios"]}
            if (comps == ALVOS_E2[var]["comps"]
                    and meios == ALVOS_E2[var]["meios"]):
                ac_e2 += 1
            else:
                err_e2.append({"id": iid, "variante": var})
        itens = {
            "alvos_E1": ac_e1 == len(classif),
            "alvos_E2": ac_e2 == len(escala),
            "escala": (all(len(r["falhas"][cand]) == 0
                           for r in escala_e1.values())
                       and all(len(r["falhas"][cand]) == 0
                               for r in escala.values())),
            "equivalencias": all(r["discrepancias"][cand] == 0
                                 for r in equiv.values()),
        }
        veredicto[cand] = {"itens": itens,
                           "passa": all(itens.values()),
                           "acertos_E1": f"{ac_e1}/{len(classif)}",
                           "acertos_E2": f"{ac_e2}/{len(escala)}",
                           "erros": (err_e1 + err_e2)[:10],
                           "n_erros": len(err_e1) + len(err_e2)}

    resultado = ("positivo" if (veredicto["C1p"]["passa"]
                                or veredicto["C2"]["passa"]) else "negativo")
    return {"veredicto_por_candidata": veredicto,
            "resultado_confirmatorio_A": resultado,
            "nota": ("Cláusulas D1-D3 (10.2) são procedimentais e "
                     "verificam-se por auditoria, não por este script. "
                     "O resultado não prova nem refuta H* (10.2). C3 é "
                     "canário e não entra em H_A.")}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--classificacoes", required=True)
    ap.add_argument("--escala-e1", required=True)
    ap.add_argument("--escala-e2", required=True)
    ap.add_argument("--equivalencias", required=True)
    ap.add_argument("--chave-e1", required=True)
    ap.add_argument("--chave-e2", required=True)
    a = ap.parse_args()
    s = pontuar(a.classificacoes, a.escala_e1, a.escala_e2, a.equivalencias,
                a.chave_e1, a.chave_e2)
    corpo = json.dumps(s, sort_keys=True, indent=1).encode()
    print(corpo.decode())
    print("sha_pontuacao:", hashlib.sha256(corpo).hexdigest())
