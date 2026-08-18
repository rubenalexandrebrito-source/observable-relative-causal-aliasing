# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — WS1 (álgebra do L1), script s12b.
Fecha o elo com o CLASSIFICADOR REAL congelado (cl.classificar, o mesmo objecto
que correu na fase confirmatória): nas 126 famílias-exemplo dos dois lotes
(46 colapsos + 40 individua_uma + 40 individua_ambas), constrói a instância
canónica II (n=10, sem exportação) e verifica:
  (i)   C1p da aresta C_AB->B ("2->1") e C_BA->A ("3->0") == previsão ordinal
        da fórmula (nível != L3);
  (ii)  as arestas processador->canal (A->C_AB "0->2", B->C_BA "1->3") são
        sempre 'estado' em C1p;
  (iii) o núcleo {A,B,C_AB,C_BA} funde numa componente única de C1p sse a
        instância é colapso_total (ambas canal->proc não-L3) — a semântica
        exacta do erro confirmatório.
Escreve apenas em ws1-algebra-l1/.
"""
import sys, json, hashlib
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws1-algebra-l1"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

PC2 = [bin(v).count("1") for v in range(8)]


def formula_nivel(th, nome, n=10):
    if nome == "C_BA->A":
        R, sig = th.F0, th.sigmaA
    else:
        R, sig = th.G0, th.sigmaB
    Phi = [[[R[x][th.pi[m][c]] ^ sig[m] for c in range(4)] for x in range(4)]
           for m in range(2)]
    mult = 1 << (n - 5)
    d = []
    for m in range(2):
        W = [[sum(PC2[Phi[m][x][a] ^ Phi[m][x][b]] for x in range(4))
              for b in range(4)] for a in range(4)]
        A = W[0][1] + W[2][3]
        B = W[0][2] + W[1][3]
        V = [sum(W[w][c] for c in range(4)) for w in range(4)]
        d.append([0, mult * A, mult * A, mult * B, mult * B,
                  mult * V[0], mult * V[1], mult * V[2], mult * V[3]])
    if d[0] == d[1]:
        return "L1_d_iguais"
    if cl.rank_canonico(d[0]) == cl.rank_canonico(d[1]):
        return "L2_rank_igual_d_diferente"
    return "L3_rank_diferente"


def theta_sha(th):
    return hashlib.sha256(
        json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()


def replay(seed, tentativas):
    ss = np.random.SeedSequence(seed)
    filhos = ss.spawn(4)
    rng = np.random.Generator(np.random.PCG64(filhos[0]))
    alvo, out, t = set(tentativas), {}, 0
    mx = max(alvo)
    while t < mx:
        th = g.sample_theta_base(rng)
        t += 1
        if t in alvo:
            out[t] = th
    return out


def instancia_canonica(th):
    tab, n, lay = g.tabela_transicao("II", th, False)
    mods = g._modulos_canonicos("II", False)
    return {"id": "canonico", "n": n, "transicao": tab,
            "modulos": [{"id": "Q%d" % i, "bits": m["bits"],
                         "bits_memoria": m["mem"]} for i, m in enumerate(mods)],
            "estado_inicial": g._campos_para_int(g.estado_inicial("II", th), lay)}


def main():
    lotes = {910000001: "prevalencia-cancelamento-II.json",
             910000002: "prevalencia-cancelamento-II-lote2.json"}
    ok = {"c1p_canal_proc": 0, "err_c1p_canal_proc": 0,
          "proc_canal_estado": 0, "err_proc_canal": 0,
          "fusao_ok": 0, "err_fusao": 0}
    detalhes_err = []
    for seed, fjson in lotes.items():
        data = json.load(open(DST + "/prevalencia/" + fjson))
        ex = data["exemplos"]
        registos = (ex["colapso_total"] + ex["individua_uma"]
                    + ex["individua_ambas"])
        ths = replay(seed, [r["tentativa"] for r in registos])
        for r in registos:
            th = ths[r["tentativa"]]
            assert theta_sha(th) == r["theta_sha"]
            res = cl.classificar(instancia_canonica(th))
            arestas = res["arestas"]
            # (i) canal->processador
            for nome, aresta in (("C_AB->B", "2->1"), ("C_BA->A", "3->0")):
                prev = formula_nivel(th, nome) != "L3_rank_diferente"
                real = arestas[aresta]["C1p"] == "estado"
                if prev == real:
                    ok["c1p_canal_proc"] += 1
                else:
                    ok["err_c1p_canal_proc"] += 1
                    detalhes_err.append({"seed": seed, "fam": r["fam"],
                                         "aresta": nome, "prev": prev,
                                         "real": real})
            # (ii) processador->canal sempre estado
            for aresta in ("0->2", "1->3"):
                if aresta in arestas and arestas[aresta]["C1p"] == "estado":
                    ok["proc_canal_estado"] += 1
                else:
                    ok["err_proc_canal"] += 1
                    detalhes_err.append({"seed": seed, "fam": r["fam"],
                                         "aresta": aresta,
                                         "info": arestas.get(aresta)})
            # (iii) fusão do núcleo sse colapso_total
            comps = res["C1p"]["componentes"]
            nucleo_fundido = any(set(c) >= {0, 1, 2, 3} for c in comps)
            if nucleo_fundido == (r["classe"] == "colapso_total"):
                ok["fusao_ok"] += 1
            else:
                ok["err_fusao"] += 1
                detalhes_err.append({"seed": seed, "fam": r["fam"],
                                     "classe": r["classe"], "comps": comps})
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "script": "s12b_classificar_real.py",
           "contagens": ok, "erros": detalhes_err}
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(WS + "/out-s12b.json", "wb").write(corpo)
    print("=== s12b RESUMO (classificador real) ===")
    print(ok)
    if detalhes_err:
        print("ERROS:", json.dumps(detalhes_err[:10], indent=1))
    print("sha256 out-s12b.json:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
