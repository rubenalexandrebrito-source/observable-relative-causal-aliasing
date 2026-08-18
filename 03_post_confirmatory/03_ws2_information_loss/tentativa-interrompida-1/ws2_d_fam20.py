# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6, WS2 (information loss).
Script D: autópsia AO NIVEL DE SITIO da instância confirmatória falhada
7bb0baab3a8ed7aa (fam 20, II, Estrato 2, n=12), na TABELA CEGA (cópia
read-only) com a chave já aberta na Fase 5 para localizar módulos.
Cadeia S0->S4 por aresta canal->processador; verificação da estrutura de
células (c,r) com multiplicidade 128 (inclui inércia dos módulos D);
reconstrução do W-efectivo por contexto a partir dos dados de sítio
(auditoria das afirmações do agente único). NADA é modificado.
"""
import sys, json, hashlib
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws2-information-loss"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl
import pontuacao as pt

ID = "7bb0baab3a8ed7aa"
SAIDA = WS + "/ws2-fam20-sitelevel.json"

PC2 = [bin(v).count("1") for v in range(8)]


def main():
    chave = json.load(open(DST + "/chave-e2.json"))
    inst = json.load(open(DST + "/conf-e2/instancias/%s.json" % ID))
    tipos = pt._tipos_e2(chave[ID])
    _, n, T, mods, s0 = cl.carregar(inst)
    T = np.asarray(T, dtype=np.int64)
    idx = {t: i for i, t in enumerate(tipos)}
    orb = cl.orbita(T, s0)
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY", "id": ID, "n": n,
           "orbita": len(orb), "tipos": tipos, "arestas": {}}

    for nome, a_t, b_t in (("C_AB->B", "C_AB", "B"), ("C_BA->A", "C_BA", "A")):
        A, B = mods[idx[a_t]], mods[idx[b_t]]
        mem = B["bits_memoria"]
        mb = mem[0]
        bits_b = B["bits"]
        rbits = [b for b in bits_b if b != mb]
        pos_mem = bits_b.index(mb)          # posição do bit de memória no extractor
        eB = cl.extractor(bits_b, n)
        popB = cl.popcount_tab(len(bits_b))
        ints = cl.intervencoes(A["bits"])
        lo, hi = A["bits"]
        Z0 = cl.estados_da_fibra(n, mem, 0)
        Z1 = cl.estados_da_fibra(n, mem, 1)
        assert int(np.bitwise_xor(Z0, Z1).min()) == (1 << mb)
        assert int(np.bitwise_xor(Z0, Z1).max()) == (1 << mb)
        ec = cl.extractor(A["bits"], n)[Z0]
        er = cl.extractor(rbits, n)[Z0]
        cell_key = (ec << 2) | er           # 16 células por intervenção
        nx0 = eB[T[Z0]]
        nx1 = eB[T[Z1]]

        per_k = []
        d0v, d1v = [], []
        dep = s1 = swap = 0
        delta_hist = {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0}
        blocos = {"B0": 0, "B1": 0, "B2": 0, "B3": 0, "B4": 0}
        mult_ok = True
        membit_resposta = 0
        D = {0: {}, 1: {}}                  # D[m][k] = tabela 4x4 (c,r) -> padrão
        for k, (mk, vl) in enumerate(ints):
            x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
            x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
            membit_resposta += int(((x0 >> pos_mem) & 1).sum()) + \
                int(((x1 >> pos_mem) & 1).sum())
            # multiplicidade: X constante em cada célula (c,r)?
            t0 = [[None] * 4 for _ in range(4)]
            t1 = [[None] * 4 for _ in range(4)]
            for cell in range(16):
                selm = (cell_key == cell)
                v0 = x0[selm]
                v1 = x1[selm]
                if v0.size != 128 or int(v0.min()) != int(v0.max()) \
                   or int(v1.min()) != int(v1.max()):
                    mult_ok = False
                t0[cell >> 2][cell & 3] = int(v0[0])
                t1[cell >> 2][cell & 3] = int(v1[0])
            D[0][k] = t0
            D[1][k] = t1
            h0 = popB[x0]
            h1 = popB[x1]
            dep_k = int((x0 != x1).sum())
            s1_k = int((h0 != h1).sum())
            dep += dep_k
            s1 += s1_k
            swap += dep_k - s1_k
            dlt = h0 - h1
            for v in (-2, -1, 0, 1, 2):
                delta_hist[v] += int((dlt == v).sum())
            hist0 = [int(x) for x in np.bincount(h0, minlength=4)]
            hist1 = [int(x) for x in np.bincount(h1, minlength=4)]
            assert hist0[3] == 0 and hist1[3] == 0
            d0k, d1k = int(h0.sum()), int(h1.sum())
            d0v.append(d0k)
            d1v.append(d1k)
            mc = ((mk >> lo) & 1) | (((mk >> hi) & 1) << 1)
            if mc != 0:
                for c in range(4):
                    p0 = [PC2[t0[c][r]] for r in range(4)]
                    p1 = [PC2[t1[c][r]] for r in range(4)]
                    if all(t0[c][r] == t1[c][r] for r in range(4)):
                        b = "B0"
                    elif p0 == p1:
                        b = "B1"
                    elif sorted(p0) == sorted(p1):
                        b = "B2"
                    elif sum(p0) == sum(p1):
                        b = "B3"
                    else:
                        b = "B4"
                    blocos[b] += 1
            per_k.append({"k": k, "mask_canal": mc,
                          "val_canal": ((vl >> lo) & 1) | (((vl >> hi) & 1) << 1),
                          "dep": dep_k, "s1": s1_k, "swap": dep_k - s1_k,
                          "hist0": hist0[:3], "hist1": hist1[:3],
                          "eq_hist": hist0 == hist1, "d0": d0k, "d1": d1k})

        # W-efectivo por contexto, das intervenções de máscara completa
        Wm = {}
        for m in (0, 1):
            W = [[0] * 4 for _ in range(4)]
            for k, (mk, vl) in enumerate(ints):
                mc = ((mk >> lo) & 1) | (((mk >> hi) & 1) << 1)
                if mc != 3:
                    continue
                gam = ((vl >> lo) & 1) | (((vl >> hi) & 1) << 1)
                for c in range(4):
                    W[c][gam] = sum(PC2[D[m][k][c][r]] for r in range(4))
            Wm[m] = W
        sim0 = all(Wm[0][a][b] == Wm[0][b][a] for a in range(4) for b in range(4))
        sim1 = all(Wm[1][a][b] == Wm[1][b][a] for a in range(4) for b in range(4))
        K_eff = (Wm[0] == Wm[1])
        equid = all(Wm[0][a][b] == 4 for a in range(4) for b in range(4) if a != b)

        nivel = ("L1" if d0v == d1v else
                 "L2" if cl.rank_canonico(d0v) == cl.rank_canonico(d1v) else "L3")
        estagio = None
        if nivel == "L1" and dep > 0:
            if s1 == 0:
                estagio = "F1_pc_pontual"
            elif all(pk["eq_hist"] for pk in per_k):
                estagio = "F1.5_histograma"
            elif blocos["B4"] == 0:
                estagio = "F2_soma_por_bloco"
            else:
                estagio = "F2_global_INESPERADO"

        out["arestas"][nome] = {
            "nivel": nivel, "estagio_perda_L1": estagio,
            "dep_sites": dep, "s1_sites": s1, "swap_sites": swap,
            "celulas_diferentes": dep // 128,
            "multiplicidade_128_ok": bool(mult_ok),
            "bit_memoria_resposta_sempre_zero": (membit_resposta == 0),
            "delta_pc_por_sitio_hist": {str(kk): v for kk, v in delta_hist.items()},
            "d0": d0v, "d1": d1v,
            "rank": list(cl.rank_canonico(d0v)),
            "blocos_sem_nulo": blocos,
            "W_efectivo_m0": Wm[0], "W_efectivo_m1": Wm[1],
            "W_simetrico": bool(sim0 and sim1), "K_efectivo": bool(K_eff),
            "W_equidistante_todos_4": bool(equid),
            "per_k": per_k,
            "D_m0": D[0], "D_m1": D[1],
        }

    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    for nome, a in out["arestas"].items():
        print(nome, "nivel", a["nivel"], "estagio", a["estagio_perda_L1"],
              "dep", a["dep_sites"], "s1", a["s1_sites"], "swap", a["swap_sites"],
              "cel_dif", a["celulas_diferentes"], "mult128", a["multiplicidade_128_ok"],
              "membit0", a["bit_memoria_resposta_sempre_zero"])
        print("  blocos", a["blocos_sem_nulo"], "K_eff", a["K_efectivo"],
              "equid", a["W_equidistante_todos_4"])
        print("  W0", a["W_efectivo_m0"])
        print("  W1", a["W_efectivo_m1"])
        print("  d0", a["d0"])
        eqs = [pk["eq_hist"] for pk in a["per_k"]]
        print("  eq_hist por k:", eqs)
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())

if __name__ == "__main__":
    main()
