# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — WS1 (álgebra do L1), script s11.
Teste CEGO na instância confirmatória falhada 7bb0baab3a8ed7aa (fam 20, II, E2,
n=12): SEM θ e SEM sementes confirmatórias (proibidas), extrai as tabelas de
resposta condicionadas Φ_m directamente da tabela de transição EXPORTADA
(leitura da cópia read-only), verifica o Lema 1 (boa definição de Φ), aplica a
fórmula fechada (Prop. 3) com factor 2^(12-5)=128, e compara com:
  (i) os vectores d0/d1 registados em fam20_confirmatoria_referencia do dataset;
  (ii) a recomputação directa com a maquinaria congelada (analisa_aresta).
Também infere ρ' (permutação de transporte entre contextos, coords exportadas)
e reporta as condições (a)/(b)/(c) do Teorema 5.
Nada é escrito fora de ws1-algebra-l1/.
"""
import sys, json, hashlib
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws1-algebra-l1"
sys.path.insert(0, DST + "/frozen-copy")
import classificador as cl
import pontuacao as pt

ID = "7bb0baab3a8ed7aa"
PC3 = [bin(v).count("1") for v in range(16)]


def analisa_aresta(T, n, bits_a, bits_b, membits):
    """Cópia literal de prevalencia_cancelamento.py (maquinaria congelada)."""
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    ints = cl.intervencoes(bits_a)
    Z0 = cl.estados_da_fibra(n, membits, 0)
    Z1 = cl.estados_da_fibra(n, membits, 1)
    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    d0, d1, dep = [], [], 0
    for (mk, vl) in ints:
        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
        d0.append(int(popB[x0].sum()))
        d1.append(int(popB[x1].sum()))
        dep += int((x0 != x1).sum())
    if d0 == d1:
        nivel = "L1_d_iguais"
    elif cl.rank_canonico(d0) == cl.rank_canonico(d1):
        nivel = "L2_rank_igual_d_diferente"
    else:
        nivel = "L3_rank_diferente"
    return {"nivel": nivel, "dep_sites": dep, "d0": d0, "d1": d1}


def main():
    chave = json.load(open(DST + "/chave-e2.json"))
    inst = json.load(open(DST + "/conf-e2/instancias/%s.json" % ID))
    ref = json.load(open(DST + "/prevalencia/prevalencia-cancelamento-II.json")
                    )["fam20_confirmatoria_referencia"]
    tipos = pt._tipos_e2(chave[ID])
    n = inst["n"]
    T = np.asarray(inst["transicao"], dtype=np.int64)
    mods = inst["modulos"]
    idx = {t: i for i, t in enumerate(tipos)}
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "script": "s11_fam20_cega.py", "id": ID, "n": n,
           "tipos": tipos, "arestas": {}}
    todos_ok = True
    for nome, a_t, b_t in (("C_AB->B", "C_AB", "B"), ("C_BA->A", "C_BA", "A")):
        a_i, b_i = idx[a_t], idx[b_t]
        bits_a = sorted(mods[a_i]["bits"])
        bits_b = sorted(mods[b_i]["bits"])
        membits = sorted(mods[b_i]["bits_memoria"])
        xbits = [b for b in bits_b if b not in membits]
        eB = cl.extractor(bits_b, n)
        eA = cl.extractor(bits_a, n)
        em = cl.extractor(membits, n)
        ex = cl.extractor(xbits, n)
        z = np.arange(1 << n, dtype=np.int64)
        val = eB[T[z]]
        m_of, x_of, c_of = em[z], ex[z], eA[z]
        # Lema 1: boa definição de Phi (val constante por (m,x,c))
        Phi = np.full((2, 4, 4), -1, dtype=np.int64)
        bem_definido = True
        for m in range(2):
            for x in range(4):
                for c in range(4):
                    sel = val[(m_of == m) & (x_of == x) & (c_of == c)]
                    if sel.size != (1 << (n - 5)):
                        bem_definido = False
                    u = np.unique(sel)
                    if u.size != 1:
                        bem_definido = False
                    else:
                        Phi[m, x, c] = int(u[0])
        # posição do bit de memória dentro da extracção do receptor
        pos_mem = bits_b.index(membits[0])
        xmask = sum(1 << k for k in range(len(bits_b)) if k != pos_mem)
        # fórmula fechada
        mult = 1 << (n - 5)
        d_pred, ABV = [], []
        for m in range(2):
            W = [[sum(PC3[int(Phi[m, x, a] ^ Phi[m, x, b])] for x in range(4))
                  for b in range(4)] for a in range(4)]
            A = W[0][1] + W[2][3]
            B = W[0][2] + W[1][3]
            V = [sum(W[w][c] for c in range(4)) for w in range(4)]
            WM3 = W[0][3] + W[1][2]
            ABV.append({"A": A, "B": B, "V": V, "WM3": WM3})
            d_pred.append([0, mult * A, mult * A, mult * B, mult * B,
                           mult * V[0], mult * V[1], mult * V[2], mult * V[3]])
        cnt = 0
        for x in range(4):
            for c in range(4):
                for j in (0, 1):
                    if (Phi[0, x, c ^ (1 << j)] ^ Phi[0, x, c]) != \
                       (Phi[1, x, c ^ (1 << j)] ^ Phi[1, x, c]):
                        cnt += 1
                for w in range(4):
                    if w == c:
                        continue
                    if (Phi[0, x, w] ^ Phi[0, x, c]) != \
                       (Phi[1, x, w] ^ Phi[1, x, c]):
                        cnt += 1
        dep_pred = mult * cnt
        # maquinaria congelada, directa
        fro = analisa_aresta(T, n, bits_a, bits_b, membits)
        # inferência de rho' (coords exportadas), na parte x' (sem slot memória)
        Phix = np.zeros((2, 4, 4), dtype=np.int64)
        for m in range(2):
            for x in range(4):
                for c in range(4):
                    v = int(Phi[m, x, c])
                    compact = 0
                    kk = 0
                    for k in range(len(bits_b)):
                        if k == pos_mem:
                            continue
                        compact |= ((v >> k) & 1) << kk
                        kk += 1
                    Phix[m, x, c] = compact
        import itertools
        rhos = []
        for r in itertools.permutations(range(4)):
            for delta in range(4):
                if all(Phix[1, x, c] == (Phix[0, x, r[c]] ^ delta)
                       for x in range(4) for c in range(4)):
                    rhos.append({"rho": list(r), "delta": delta})
        def tipo(p):
            vis, cyc = [False] * 4, []
            for i in range(4):
                if not vis[i]:
                    l, j = 0, i
                    while not vis[j]:
                        vis[j] = True
                        j = p[j]
                        l += 1
                    cyc.append(l)
            cyc.sort(reverse=True)
            return "+".join(map(str, cyc))
        reg = ref[nome]
        ok = {
            "lema1_bem_definido": bem_definido,
            "d0_pred_eq_registado": d_pred[0] == reg["d0"],
            "d1_pred_eq_registado": d_pred[1] == reg["d1"],
            "d0_pred_eq_frozen": d_pred[0] == fro["d0"],
            "d1_pred_eq_frozen": d_pred[1] == fro["d1"],
            "dep_pred_eq_registado": dep_pred == reg["dep_sites"],
            "dep_pred_eq_frozen": dep_pred == fro["dep_sites"],
            "nivel_L1": (d_pred[0] == d_pred[1]) and reg["nivel"] == "L1_d_iguais"
                        and fro["nivel"] == "L1_d_iguais",
        }
        todos_ok = todos_ok and all(ok.values())
        a0, a1 = ABV
        out["arestas"][nome] = {
            "bits_a": bits_a, "bits_b": bits_b, "membits": membits,
            "verificacoes": ok,
            "d_pred": d_pred, "dep_pred": dep_pred,
            "ABV0": a0, "ABV1": a1,
            "cond_a": a0["A"] == a1["A"], "cond_b": a0["B"] == a1["B"],
            "cond_c": a0["V"] == a1["V"],
            "K": d_pred[0] == d_pred[1],
            "dep_positivo": dep_pred > 0,
            "rhos_transporte": rhos,
            "rho_tipos": sorted({tipo(r["rho"]) for r in rhos}),
        }
    out["todas_verificacoes_ok"] = todos_ok
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(WS + "/out-s11.json", "wb").write(corpo)
    print("=== s11 RESUMO (fam20 cega) ===")
    for nome, a in out["arestas"].items():
        print(nome, "verificacoes:", a["verificacoes"])
        print("   ABV0:", a["ABV0"])
        print("   ABV1:", a["ABV1"])
        print("   K:", a["K"], "dep_pred:", a["dep_pred"],
              "rho tipos:", a["rho_tipos"],
              "n rhos:", len(a["rhos_transporte"]))
    print("TODAS OK:", todos_ok)
    print("sha256 out-s11.json:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()
