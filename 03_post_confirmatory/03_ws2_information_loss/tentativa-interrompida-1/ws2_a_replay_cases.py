# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS2 (information loss).
Script A: replay determinístico dos thetas dos CASOS pré-comprometidos
(precommit-ws2.txt, secção 2): 46 colapso_total (lotes 1+2), 6 primeiros
individua_ambas (lote1), 6 primeiros individua_uma (lote1).
NENHUMA amostra nova; sementes registadas 910000001/910000002 apenas (replay).
Instrumento congelado importado, nunca editado. Saída apenas no ws2 dir.
"""
import sys, json, hashlib
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws2-information-loss"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g

SAIDA = WS + "/ws2-thetas-cases.json"

def theta_sha(th):
    return hashlib.sha256(json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()

def main():
    j1 = json.load(open(DST + "/prevalencia/prevalencia-cancelamento-II.json"))
    j2 = json.load(open(DST + "/prevalencia/prevalencia-cancelamento-II-lote2.json"))
    assert j1["semente_exploratoria"] == 910000001
    assert j2["semente_exploratoria"] == 910000002

    casos = []  # (seed, grupo, registo)
    for r in j1["exemplos"]["colapso_total"]:
        casos.append((910000001, "colapso", r))
    for r in j2["exemplos"]["colapso_total"]:
        casos.append((910000002, "colapso", r))
    for r in j1["exemplos"]["individua_ambas"][:6]:
        casos.append((910000001, "ctrl_L3L3", r))
    for r in j1["exemplos"]["individua_uma"][:6]:
        casos.append((910000001, "ctrl_misto", r))
    print("casos totais:", len(casos))

    por_seed = {}
    for seed, grupo, r in casos:
        por_seed.setdefault(seed, {})[r["tentativa"]] = r

    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "descricao": "replay dos thetas dos casos precomprometidos (precommit-ws2.txt)",
           "seeds_replay_registadas": sorted(por_seed), "casos": []}
    thetas = {}
    for seed in sorted(por_seed):
        wanted = por_seed[seed]
        tmax = max(wanted)
        ss = np.random.SeedSequence(seed)
        rng = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))
        got = {}
        for t in range(1, tmax + 1):
            th = g.sample_theta_base(rng)
            if t in wanted:
                got[t] = th
        for t, reg in sorted(wanted.items()):
            th = got[t]
            sha = theta_sha(th)
            ok_sha = (sha == reg["theta_sha"])
            ok_pi = (th.pi[0] != th.pi[1])
            ok_eleg = g.elegibilidade(th, False)[0]
            if not (ok_sha and ok_pi and ok_eleg):
                print("FALHA replay seed=%d tentativa=%d sha_ok=%s pi_ok=%s eleg_ok=%s"
                      % (seed, t, ok_sha, ok_pi, ok_eleg))
                raise SystemExit(1)
            thetas["%d:%d" % (seed, t)] = asdict(th)
    for seed, grupo, r in casos:
        out["casos"].append({"seed": seed, "grupo": grupo, "fam": r["fam"],
                             "tentativa": r["tentativa"], "theta_sha": r["theta_sha"],
                             "classe": r["classe"],
                             "arestas_reg": r["arestas"]})
    out["thetas"] = thetas
    out["verificacao"] = "todos os theta_sha, pi0!=pi1 e elegibilidade confirmados"
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print("casos verificados:", len(out["casos"]), "thetas:", len(thetas))
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())

if __name__ == "__main__":
    main()
