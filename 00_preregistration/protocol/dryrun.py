# -*- coding: utf-8 -*-
"""
dryrun.py — Pré-registo A v8.3, secção 11.1a. Selector determinístico da
amostra temporal (emenda n.º 1, item 7, com regra algorítmica completa).

Regra congelada: ordenar lexicograficamente os IDs dentro de cada grupo
(E1,I), (E1,II), (E1,III), (E2,II), (E2,III); inicializar UMA
Generator(PCG64(777000300)); percorrer os cinco grupos NESSA ordem e
seleccionar em cada um três índices com choice(replace=False). Sem selecção
manual em nenhum passo.

O selector não consulta classificações. Em modo --cronometrar, executa o
arnês confirmatório de equivalências sobre os 15 casos seleccionados, o que
corre C1', C2 e C3 internamente, SEM inspeccionar os resultados e
descartando-os imediatamente; apenas os tempos sobrevivem. O registo
temporal é gravado em ficheiro datado, porque é o dado que decide a
passagem das 72 horas.
"""

import json
import numpy as np

SEMENTE_DRYRUN = 777000300
GRUPOS = (("E1", "I"), ("E1", "II"), ("E1", "III"), ("E2", "II"), ("E2", "III"))


def seleccionar(chave_e1, chave_e2, por_grupo=3):
    """chaves: dicts id -> {variante, ...}. Devolve dict grupo -> [ids]."""
    rng = np.random.Generator(np.random.PCG64(SEMENTE_DRYRUN))
    sel = {}
    for estrato, var in GRUPOS:
        chave = chave_e1 if estrato == "E1" else chave_e2
        ids = sorted(i for i, k in chave.items() if k["variante"] == var)
        if len(ids) < por_grupo:
            raise ValueError(f"grupo ({estrato},{var}) tem {len(ids)} < {por_grupo}")
        idx = rng.choice(len(ids), size=por_grupo, replace=False)
        sel[f"{estrato}:{var}"] = [ids[int(i)] for i in sorted(idx)]
    return sel


def cronometrar(seleccao, dir_e1, dir_e2, amostra=None):
    """Executa as equivalências EXAUSTIVAS exactamente sobre os IDs
    seleccionados e devolve o wall time acumulado por grupo: os t_g da
    fórmula congelada do guião. Sem cópias manuais, sem escolhas durante
    a execução. As saídas classificatórias são DESCARTADAS: só o relógio
    sobrevive (secção 11.1a). O parâmetro amostra existe SÓ para o fumo
    de engenharia deste próprio runner; no dry run oficial é None."""
    import os
    import time
    import equivalencias as eq
    indice = {}
    for d in (dir_e1, dir_e2):
        for f in sorted(os.listdir(d)):
            if f.endswith(".json"):
                caminho = os.path.join(d, f)
                iid = json.load(open(caminho))["id"]     # pelo CONTEUDO
                if iid in indice:
                    raise ValueError(f"ID repetido nos lotes: {iid}")
                indice[iid] = caminho
    em_falta = [iid for ids in seleccao.values() for iid in ids
                if iid not in indice]
    if em_falta:
        raise ValueError(f"IDs seleccionados ausentes dos lotes: {em_falta}")
    tempos = {}
    ordem = [f"{e}:{v}" for (e, v) in GRUPOS]
    for grupo in ordem:
        ids = seleccao[grupo]
        t0 = time.perf_counter()
        for iid in ids:
            inst = json.load(open(indice[iid]))
            eq.testar_instancia(inst, amostra=amostra)   # resultado descartado
        tempos[grupo] = time.perf_counter() - t0
    est = (50.0 / 3.0) * (tempos["E1:I"] + tempos["E1:II"] + tempos["E1:III"]) \
        + (25.0 / 3.0) * (tempos["E2:II"] + tempos["E2:III"])
    return {"t_por_grupo_segundos": tempos,
            "T_equiv_estimado_horas": est / 3600.0}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--chave-e1", required=True)
    ap.add_argument("--chave-e2", required=True)
    ap.add_argument("--saida", default=None,
                    help="grava a selecção em JSON (dryrun-seleccao.json)")
    ap.add_argument("--cronometrar", nargs=2, metavar=("DIR_E1", "DIR_E2"),
                    default=None, help="executa os 15 casos e imprime t_g")
    ap.add_argument("--amostra", type=int, default=None,
                    help="APENAS fumo mecânico do runner; o dry run oficial "
                         "NUNCA usa esta opção (exaustivo por omissão)")
    a = ap.parse_args()
    sel = seleccionar(json.load(open(a.chave_e1)), json.load(open(a.chave_e2)))
    corpo = json.dumps(sel, sort_keys=True, indent=1)
    if a.saida:
        import os
        if os.path.exists(a.saida):
            raise FileExistsError(a.saida)
        open(a.saida, "w").write(corpo)
    print(corpo)
    if a.cronometrar:
        import datetime
        import os
        registo = "dryrun-tempos.json"
        if os.path.exists(registo):
            # verificar ANTES de gastar horas de relógio, não depois
            raise FileExistsError(registo)
        r = cronometrar(sel, a.cronometrar[0], a.cronometrar[1],
                        amostra=a.amostra)
        r["registado_em"] = datetime.datetime.now().isoformat()
        open(registo, "w").write(json.dumps(r, sort_keys=True, indent=1))
        print(json.dumps(r, sort_keys=True, indent=1))
        print(f"tempos gravados em {registo}")
